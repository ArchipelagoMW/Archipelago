import logging
from BaseClasses import CollectionState, Region, Entrance, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from rule_builder.cached_world import CachedRuleBuilderWorld
from .Items import PokepelagoItem, item_table, pokemon_names, GEN_1_TYPES, item_data_table
from .Locations import PokepelagoLocation, location_table, milestones
from .Options import PokepelagoOptions
from .data import POKEMON_DATA
from . import Rules

class PokepelagoWeb(WebWorld):
    tutorials = [Tutorial(
        "Pokepelago Setup Guide",
        "A guide to setting up the Pokepelago Archipelago world.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Appie"]
    )]

class PokepelagoWorld(CachedRuleBuilderWorld):
    """
    Pokepelago: A collection-based world where you catch 'em all by guessing their names.
    """
    game: str = "Pokepelago"
    options_dataclass = PokepelagoOptions
    options: PokepelagoOptions
    topology_present: bool = True
    web = PokepelagoWeb()

    # Tier entrances use has("Pokemon Unlocks", player, thresh) which depends on a virtual
    # counter maintained by collect/remove overrides — O(1) per check. AP can't register
    # item-count rules in indirect_conditions (only region-reachability rules), so
    # explicit_indirect_conditions=False is needed to re-check the 4 tier entrances whenever
    # any region becomes newly reachable. With only 4 blocked tier connections, the cost is
    # O(4 × regions) per sweep, which is fast.
    explicit_indirect_conditions: bool = False

    item_name_to_id = item_table
    location_name_to_id = location_table
    
    # We define item groups for each Pokémon type to facilitate milestone logic.
    # A Pokémon can belong to multiple groups if it has multiple types.
    item_name_groups = {
        "Pokemon Unlocks": {f"{name} Unlock" for name in pokemon_names},
        "Type Unlocks": {f"{p_type} Type Key" for p_type in GEN_1_TYPES},
        **{f"{p_type} Pokemon": {f"{mon['name']} Unlock" for mon in POKEMON_DATA if p_type in mon['types']} 
           for p_type in GEN_1_TYPES}
    }

    def generate_early(self):
        gen_option = self.options.pokemon_generations.value
        limit = {
            0: 151,
            1: 251,
            2: 386,
            3: 493,
            4: 649,
            5: 721,
            6: 809,
            7: 898,
            8: 1025
        }.get(gen_option, 151)
        self.active_pokemon = [mon for mon in POKEMON_DATA if mon["id"] <= limit]
        self.active_pokemon_names = [mon["name"] for mon in self.active_pokemon]
        # Fast lookup by name for collect/remove counter updates.
        self._mon_lookup: dict = {mon["name"]: mon for mon in self.active_pokemon}

        # Total new Pokémon guessable (all active minus the 3 precollected starters)
        total_guessable = len(self.active_pokemon) - 3

        # Determine raw goal count from options
        if self.options.goal_type.value == 0:  # percentage
            raw_goal = max(1, round(len(self.active_pokemon) * self.options.goal_percentage.value / 100))
        else:  # count
            raw_goal = min(self.options.goal_count.value, len(self.active_pokemon))

        # The goal is expressed as the number of Pokémon guessed AFTER the starters,
        # so we snap to the closest available "Guessed X Pokemon" milestone that is
        # <= total_guessable. The milestones list (from Locations.py) is already sorted.
        valid_milestones = [m for m in milestones if m <= total_guessable]

        # Find the closest milestone to raw_goal (but cap at max valid milestone)
        capped_goal = min(raw_goal, max(valid_milestones))
        self.goal_count = min(valid_milestones, key=lambda m: abs(m - capped_goal))

    def collect(self, state: CollectionState, item: "PokepelagoItem") -> bool:
        changed = super().collect(state, item)
        if changed and item.name.endswith(" Unlock"):
            state.prog_items[self.player]["Pokemon Unlocks"] += 1
            mon_name = item.name[:-7]  # strip " Unlock"
            if mon := self._mon_lookup.get(mon_name):
                for t in mon["types"]:
                    state.prog_items[self.player][f"{t} Pokemon"] += 1
        return changed

    def remove(self, state: CollectionState, item: "PokepelagoItem") -> bool:
        changed = super().remove(state, item)
        if changed and item.name.endswith(" Unlock"):
            state.prog_items[self.player]["Pokemon Unlocks"] -= 1
            mon_name = item.name[:-7]
            if mon := self._mon_lookup.get(mon_name):
                for t in mon["types"]:
                    state.prog_items[self.player][f"{t} Pokemon"] -= 1
        return changed

    def create_item(self, name: str) -> PokepelagoItem:
        data = item_data_table.get(name)
        if data:
            classification = data[1]
            item_id = data[0]
        else:
            classification = ItemClassification.filler
            item_id = item_table.get(name, 0)
            
        return PokepelagoItem(name, classification, item_id, self.player)

    def create_event_item(self, name: str) -> PokepelagoItem:
        """Create an event item (ID=None) for server-side goal/release tracking."""
        return PokepelagoItem(name, ItemClassification.progression, None, self.player)

    def create_items(self):
        starters = ["Bulbasaur", "Charmander", "Squirtle"]
        starter_types = {"Grass", "Poison", "Fire", "Water"}

        # Track items added to the pool by this player specifically.
        # We must NOT use len(self.multiworld.itempool) because that is the global
        # pool shared by ALL players. When other games run create_items() before us,
        # their items inflate the count and prevent us from adding our fillers.
        my_items_in_pool = 0

        if self.options.dexsanity.value:
            # 1a. Dexsanity ON: precollect starter Unlock items and add remaining Unlocks to pool
            for name in starters:
                self.multiworld.push_precollected(self.create_item(f"{name} Unlock"))

            for name in self.active_pokemon_names:
                if name not in starters:
                    self.multiworld.itempool.append(self.create_item(f"{name} Unlock"))
                    my_items_in_pool += 1

        # 1b. Precollect starter Type Keys so those types are accessible from the start
        for p_type in starter_types:
            self.multiworld.push_precollected(self.create_item(f"{p_type} Type Key"))

        # 2. Add remaining Type Keys to the pool if Type Locks are enabled
        if self.options.type_locks.value:
            for p_type in GEN_1_TYPES:
                if p_type not in starter_types:
                    self.multiworld.itempool.append(self.create_item(f"{p_type} Type Key"))
                    my_items_in_pool += 1

        # 4. Fill remaining locations with useful items/fillers and traps.
        # NOTE: event locations (ID=None, like "Pokepelago Victory") are server-side only and
        # do NOT need a pool item — only real sendable locations need to be filled.
        total_locations = sum(1 for loc in self.multiworld.get_locations(self.player) if loc.address is not None)
        useful_fillers = ["Master Ball", "Pokedex", "Pokegear"]
        trap_fillers = ["Small Shuffle Trap", "Big Shuffle Trap", "Derpy Mon Trap", "Release Trap"]
        
        trap_chance = self.options.trap_chance.value
        
        while my_items_in_pool < total_locations:
            if self.random.randint(1, 100) <= trap_chance:
                # Add a trap
                filler_name = self.random.choice(trap_fillers)
            else:
                # Add a useful item
                filler_name = useful_fillers[my_items_in_pool % len(useful_fillers)]
                
            self.multiworld.itempool.append(self.create_item(filler_name))
            my_items_in_pool += 1

    def create_regions(self):
        STARTER_NAMES = {"Bulbasaur", "Charmander", "Squirtle"}

        # Compute how many of each type are catchable after subtracting pre-collected starters.
        # A type milestone "Caught N X Pokemon" is only valid if N <= catchable count for X.
        type_catchable = {}
        for mon in self.active_pokemon:
            for t in mon["types"]:
                type_catchable[t] = type_catchable.get(t, 0) + 1
        for mon in self.active_pokemon:
            if mon["name"] in STARTER_NAMES:
                for t in mon["types"]:
                    if t in type_catchable:
                        type_catchable[t] -= 1

        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        if self.options.dexsanity.value:
            # --- Dexsanity ON: full tier + per-Pokemon region setup ---
            TIER_THRESHOLDS = {0: 0, 1: 50, 2: 150, 3: 400, 4: 800}
            # TYPE_MILESTONE_STEPS [1,2,5,10,20,35,50] distributed evenly across 5 tiers.
            TYPE_STEP_TO_TIER = {1: 0, 2: 0, 5: 1, 10: 1, 20: 2, 35: 3, 50: 4}

            tier0 = Region("Tier 0", self.player, self.multiworld)
            tier1 = Region("Tier 1", self.player, self.multiworld)
            tier2 = Region("Tier 2", self.player, self.multiworld)
            tier3 = Region("Tier 3", self.player, self.multiworld)
            tier4 = Region("Tier 4", self.player, self.multiworld)
            tiers = [tier0, tier1, tier2, tier3, tier4]
            self.multiworld.regions.extend([tier0, tier1, tier2, tier3, tier4])

            # Parallel connections: Menu -> each Tier directly.
            # Tier entrances gate access based on how many Pokemon Unlock items the player has.
            # Using has_group on real items means BFS state is fixed per sweep — no within-sweep
            # re-evaluation needed, so explicit_indirect_conditions can stay True (default).
            for t, threshold in [(tier0, 0), (tier1, 50), (tier2, 150), (tier3, 400), (tier4, 800)]:
                ent = Entrance(self.player, f"Menu To {t.name}", menu_region)
                menu_region.exits.append(ent)
                ent.connect(t)
                if threshold > 0:
                    ent.access_rule = lambda state, thresh=threshold: state.has("Pokemon Unlocks", self.player, thresh)

            # Assign milestone and starting locations to their target tiers.
            for loc_name, loc_id in self.location_name_to_id.items():
                if loc_name.startswith("Guess "):
                    continue  # Handled in per-Pokemon loop below.

                target_region = menu_region  # Default: starting locations on Menu, no gate.

                if loc_name.startswith("Guessed "):
                    count = int(loc_name.split(" ")[1])
                    if count > len(self.active_pokemon) - 3:
                        continue
                    if count < 50:      target_region = tier0
                    elif count < 150:   target_region = tier1
                    elif count < 400:   target_region = tier2
                    elif count < 800:   target_region = tier3
                    else:               target_region = tier4

                    tier_idx = tiers.index(target_region)
                    tier_threshold = TIER_THRESHOLDS[tier_idx]
                    rule_requires = count + 3  # +3 for pre-collected starters
                    if tier_threshold > rule_requires:
                        logging.warning(
                            f"[Pokepelago] Sanity: '{loc_name}' in Tier {tier_idx} "
                            f"(entrance needs {tier_threshold} catches) but its rule only needs "
                            f"{rule_requires} catches. Location may be unreachable — check tier assignment."
                        )

                elif loc_name.startswith("Caught "):
                    parts = loc_name.split(" ")
                    step = int(parts[1])
                    p_type = parts[2]
                    if step > type_catchable.get(p_type, 0):
                        continue
                    tier_idx = TYPE_STEP_TO_TIER.get(step, 0)
                    if TIER_THRESHOLDS[tier_idx] > len(self.active_pokemon):
                        continue
                    target_region = tiers[tier_idx]

                location = PokepelagoLocation(self.player, loc_name, loc_id, target_region)
                target_region.locations.append(location)

            # Each Pokemon gets its own sub-region connected from the appropriate tier.
            # Tiering is by Pokedex ID as a proxy for generation/game-era difficulty.
            for mon in self.active_pokemon:
                mon_name = mon["name"]
                mon_region = Region(f"Region {mon_name}", self.player, self.multiworld)
                self.multiworld.regions.append(mon_region)

                loc_name = f"Guess {mon_name}"
                loc_id = self.location_name_to_id[loc_name]
                location = PokepelagoLocation(self.player, loc_name, loc_id, mon_region)
                mon_region.locations.append(location)

                mon_id = mon["id"]
                if mon_name in STARTER_NAMES:
                    mon_tier = tier0
                else:
                    if mon_id < 100:    mon_tier = tier0
                    elif mon_id < 300:  mon_tier = tier1
                    elif mon_id < 600:  mon_tier = tier2
                    elif mon_id < 900:  mon_tier = tier3
                    else:               mon_tier = tier4

                entrance = Entrance(self.player, f"Catch {mon_name}", mon_tier)
                mon_tier.exits.append(entrance)
                entrance.connect(mon_region)

        else:
            # --- Dexsanity OFF: flat milestone-only structure in menu_region ---
            # No tiers, no per-Pokemon regions. All milestone and starting locations live in
            # menu_region. Type milestone access rules (via Type Keys) are set in set_rules().
            for loc_name, loc_id in self.location_name_to_id.items():
                if loc_name.startswith("Guess "):
                    continue  # No per-Pokemon locations in this mode.

                if loc_name.startswith("Guessed "):
                    count = int(loc_name.split(" ")[1])
                    if count > len(self.active_pokemon) - 3:
                        continue

                elif loc_name.startswith("Caught "):
                    parts = loc_name.split(" ")
                    step = int(parts[1])
                    p_type = parts[2]
                    if step > type_catchable.get(p_type, 0):
                        continue

                location = PokepelagoLocation(self.player, loc_name, loc_id, menu_region)
                menu_region.locations.append(location)

        # Victory event location (ID=None marks it as a server-side event, not a sendable check).
        # The Victory item placed here is what triggers the server's release/goal-completion mechanism.
        victory_location = PokepelagoLocation(self.player, "Pokepelago Victory", None, menu_region)
        menu_region.locations.append(victory_location)

    def pre_fill(self):
        """Pre-place non-starter Type Keys into global milestone locations.

        With type_locks enabled, Type Keys gate type-milestone and individual Pokemon locations.
        Placing a Type Key in a location that itself requires that Type Key creates a circular
        dependency. Global milestone locations ("Guessed N Pokemon") have no type-key access rules,
        making them always safe for pre-placement.

        With dexsanity=on: milestone locations are gated by Pokemon-count rules, so Type Keys are
        naturally distributed through progression (first key after 1st catch, last after ~100th).
        With dexsanity=off: milestone locations have no AP-side rules (client-driven), so AP
        considers them accessible in sphere 0 — but the client still gates them by guess count.

        Applies whenever type_locks=on regardless of dexsanity setting.
        """
        if not self.options.type_locks.value:
            return

        from .Locations import milestones
        from .data import GEN_1_TYPES

        STARTER_TYPES = {"Grass", "Poison", "Fire", "Water"}
        non_starter_key_names = {f"{t} Type Key" for t in GEN_1_TYPES if t not in STARTER_TYPES}

        # Pull this player's non-starter Type Keys out of the global item pool.
        my_keys: list = []
        remaining: list = []
        for item in self.multiworld.itempool:
            if item.player == self.player and item.name in non_starter_key_names:
                my_keys.append(item)
            else:
                remaining.append(item)

        if not my_keys:
            return

        # Collect unfilled global milestone locations for this player.
        # These are safe: their access rules depend only on Pokemon count, never on Type Keys.
        milestone_locs: list = []
        for count in milestones:
            if count > len(self.active_pokemon) - 3:
                break
            loc_name = f"Guessed {count} Pokemon"
            try:
                loc = self.multiworld.get_location(loc_name, self.player)
                if loc.item is None:
                    milestone_locs.append(loc)
            except KeyError:
                pass

        if len(milestone_locs) < len(my_keys):
            # Fewer milestone locs than keys — shouldn't happen with 20+ milestones and 14 keys.
            return

        self.multiworld.itempool[:] = remaining
        self.random.shuffle(milestone_locs)
        for key, loc in zip(my_keys, milestone_locs):
            loc.place_locked_item(key)

    def set_rules(self):
        Rules.set_rules(self)

        # Canonical Archipelago goal pattern: place a locked "Victory" event item at an event
        # location whose access rule enforces the goal. The server's release/completion mechanism
        # triggers when state.has("Victory") becomes true — can_reach() alone doesn't do this.
        victory_location = self.multiworld.get_location("Pokepelago Victory", self.player)

        if self.options.dexsanity.value:
            # Starters' Unlock items are push_precollected, so has_group("Pokemon Unlocks") already
            # counts them. goal_count + 3 = goal new catches + 3 pre-collected starters.
            victory_location.access_rule = lambda state: state.has(
                "Pokemon Unlocks", self.player, self.goal_count + 3)
        # Dexsanity OFF: no AP-side access rule. The client drives victory by checking the
        # goal milestone location when the player has guessed enough Pokemon.

        victory_item = self.create_event_item("Victory")
        victory_location.place_locked_item(victory_item)

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> dict:
        return {
            "type_locks": bool(self.options.type_locks.value),
            "pokemon_generations": self.options.pokemon_generations.value,
            "goal_count": self.goal_count,
            "dexsanity": bool(self.options.dexsanity.value),
        }