from collections import Counter

from BaseClasses import Region, Entrance, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from .Items import PokepelagoItem, item_table, item_data_table, GEN_1_TYPES, FILLER_ITEM_CATEGORIES
from .Locations import PokepelagoLocation, location_table, milestones, starting_locations, TYPE_MILESTONE_STEPS
from .Options import PokepelagoOptions, REGION_OPTION_ATTRS
from .data import (POKEMON_DATA, GAME_REGIONS, REGION_RANGES, STARTERS_BY_REGION, get_pokemon_region,
                   LEGENDARY_SUB_IDS, LEGENDARY_BOX_IDS, LEGENDARY_MYTHIC_IDS,
                   BABY_IDS, TRADE_EVO_IDS, FOSSIL_IDS, ULTRA_BEAST_IDS, PARADOX_IDS,
                   STONE_EVO_GROUPS)

class PokepelagoWeb(WebWorld):
    tutorials = [Tutorial(
        "Pokepelago Setup Guide",
        "A guide to setting up the Pokepelago Archipelago world.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Appie"]
    )]

class PokepelagoWorld(World):
    """
    Pokepelago: A collection-based world where you catch 'em all by guessing their names.
    Each game region acts as a zone gated by a Region Pass item.
    Type Keys gate access to Pokemon of that type (creates cross-player dependencies).
    """
    game: str = "Pokepelago"
    options_dataclass = PokepelagoOptions
    options: PokepelagoOptions
    topology_present: bool = True
    web = PokepelagoWeb()

    item_name_to_id = item_table
    location_name_to_id = location_table

    def generate_early(self):
        # Build list of active regions in canonical order
        self.active_regions = [
            r for r in GAME_REGIONS
            if getattr(self.options, REGION_OPTION_ATTRS[r]).value
        ]
        if not self.active_regions:
            self.active_regions = ["Kanto"]

        # Determine starting region from starter_region option (0 = any = random active region).
        _REGION_BY_IDX = {
            1: "Kanto", 2: "Johto", 3: "Hoenn", 4: "Sinnoh", 5: "Unova",
            6: "Kalos", 7: "Alola", 8: "Galar", 9: "Hisui", 10: "Paldea",
        }
        sr_value = self.options.starter_region.value
        chosen_region = _REGION_BY_IDX.get(sr_value)
        if sr_value == 0 or chosen_region not in self.active_regions:
            self.starting_region = self.random.choice(self.active_regions)
        else:
            self.starting_region = chosen_region

        # Pick a single starter Pokémon; only its Type Keys are pre-collected.
        starter_list = STARTERS_BY_REGION.get(self.starting_region, [])
        if starter_list:
            idx = self.options.starter_pokemon.value
            if idx == 0:  # any = random
                chosen = self.random.choice(starter_list)
            else:
                chosen = starter_list[min(idx - 1, len(starter_list) - 1)]
            self.starter_names: set = {chosen}
            self.chosen_starter: str | None = chosen
        else:
            self.starter_names = set()
            self.chosen_starter = None

        # Collect active Pokemon across all selected regions
        active_ids: set = set()
        for r in self.active_regions:
            lo, hi = REGION_RANGES[r]
            active_ids.update(range(lo, hi + 1))

        self.active_pokemon = [mon for mon in POKEMON_DATA if mon["id"] in active_ids]
        self.active_pokemon_names = [mon["name"] for mon in self.active_pokemon]
        self._mon_lookup: dict = {mon["name"]: mon for mon in self.active_pokemon}

        # Pre-compute which active Pokémon fall into each lock category.
        # Used by _extra_reqs() and create_items() to determine which gate items are needed.
        self._gl_sub   = active_ids & LEGENDARY_SUB_IDS
        self._gl_box   = active_ids & LEGENDARY_BOX_IDS
        self._gl_myth  = active_ids & LEGENDARY_MYTHIC_IDS
        self._g_baby   = active_ids & BABY_IDS
        self._g_trade  = active_ids & TRADE_EVO_IDS
        self._g_fossil = active_ids & FOSSIL_IDS
        self._g_ub     = active_ids & ULTRA_BEAST_IDS
        self._g_para   = active_ids & PARADOX_IDS
        # Only include stone types that have at least one active Pokémon in the pool
        self._g_stone: dict = {s: active_ids & ids for s, ids in STONE_EVO_GROUPS.items() if active_ids & ids}

        # Goal count: number of Pokemon the client needs to catch for victory
        total = len(self.active_pokemon)
        if self.options.goal_type.value == 0:  # percentage
            raw_goal = max(1, round(total * self.options.goal_percentage.value / 100))
        else:  # count
            raw_goal = min(self.options.goal_count.value, total)

        # Snap to closest valid milestone; always include total so 100% goals resolve exactly
        valid_milestones = sorted(set([m for m in milestones if m <= total] + [total]))
        capped_goal = min(raw_goal, total)
        self.goal_count = min(valid_milestones, key=lambda m: abs(m - capped_goal))

        # ── Pre-compute requirement groups for milestone logic ──
        # For each non-starter active Pokémon, record (region_pass_needed, type_keys_needed).
        # Group by these requirements and count how many Pokémon share each requirement set.
        # This lets milestone rules efficiently check how many Pokémon are logically accessible.
        region_locks = bool(self.options.region_locks.value)
        type_locks = bool(self.options.type_locks.value)

        global_req_counter: Counter = Counter()
        type_req_counters: dict[str, Counter] = {t: Counter() for t in GEN_1_TYPES}

        for mon in self.active_pokemon:
            region = get_pokemon_region(mon["id"])
            region_req = None
            if region_locks and region != self.starting_region:
                region_req = f"{region} Pass"
            type_reqs: frozenset = frozenset()
            if type_locks:
                type_reqs = frozenset(f"{t} Type Key" for t in mon["types"])

            extra_reqs = self._extra_reqs(mon["id"])
            key = (region_req, type_reqs, extra_reqs)
            global_req_counter[key] += 1
            for t in mon["types"]:
                if t in type_req_counters:
                    type_req_counters[t][key] += 1

        # List of (region_req_or_None, frozenset_of_type_keys, extra_reqs_frozenset, pokemon_count)
        self._milestone_req_groups = [
            (rr, tr, er, c) for (rr, tr, er), c in global_req_counter.items()
        ]
        self._type_milestone_req_groups: dict[str, list] = {
            t: [(rr, tr, er, c) for (rr, tr, er), c in counter.items()]
            for t, counter in type_req_counters.items()
        }
        # Max non-starter Pokémon of each type across active regions
        self._active_type_counts: dict[str, int] = {
            t: sum(counter.values()) for t, counter in type_req_counters.items()
        }

    def _extra_reqs(self, mon_id: int) -> frozenset:
        """Return extra gate requirements for a Pokémon beyond region/type locks.

        Returns a frozenset of (item_name, required_count) tuples. An empty frozenset
        means no extra gate applies. Used in milestone rules and access rules.
        """
        o = self.options
        reqs: list = []
        if o.legendary_locks.value:
            if mon_id in self._gl_myth:
                reqs.append(("Gym Badge", 8))
            elif mon_id in self._gl_box:
                reqs.append(("Gym Badge", 7))
            elif mon_id in self._gl_sub:
                reqs.append(("Gym Badge", 6))
        if o.trade_locks.value and mon_id in self._g_trade:
            reqs.append(("Link Cable", 1))
        if o.baby_locks.value and mon_id in self._g_baby:
            reqs.append(("Daycare", o.daycare_count.value))
        if o.fossil_locks.value and mon_id in self._g_fossil:
            reqs.append(("Fossil Restorer", 1))
        if o.ultra_beast_locks.value and mon_id in self._g_ub:
            reqs.append(("Ultra Wormhole", 1))
        if o.paradox_locks.value and mon_id in self._g_para:
            reqs.append(("Time Rift", 1))
        if o.stone_locks.value:
            for stone, ids in self._g_stone.items():
                if mon_id in ids:
                    reqs.append((f"{stone.title()} Stone", 1))
                    break
        return frozenset(reqs)

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
        return PokepelagoItem(name, ItemClassification.progression, None, self.player)

    def create_items(self):
        # Determine which types the starters cover
        starter_types: set = set()
        for name in self.starter_names:
            if mon := self._mon_lookup.get(name):
                starter_types.update(mon["types"])

        my_items_in_pool = 0

        # Pre-collect starter Type Keys so those types are accessible from game start.
        # These are NOT placed in the pool — they go directly into the player's start inventory.
        for p_type in sorted(starter_types):
            self.multiworld.push_precollected(self.create_item(f"{p_type} Type Key"))

        # Add non-starter Type Keys to the pool as progression items.
        # They gate "Guess X" locations (AP access rules), creating real cross-player dependencies.
        if self.options.type_locks.value:
            for p_type in GEN_1_TYPES:
                if p_type not in starter_types:
                    self.multiworld.itempool.append(self.create_item(f"{p_type} Type Key"))
                    my_items_in_pool += 1

        # Region Passes for non-starting regions (the Zone Keys).
        # Added whenever region_locks=ON, regardless of dexsanity.
        # Even with dexsanity=OFF, the client respects region locks, so passes must be in the pool.
        if self.options.region_locks.value:
            for region in self.active_regions:
                if region == self.starting_region:
                    continue
                self.multiworld.itempool.append(self.create_item(f"{region} Pass"))
                my_items_in_pool += 1

        # ── New lock gate items ──────────────────────────────────────────────────
        o = self.options

        # Legendary gate: 8 progressive Gym Badge items (only if there are active legendaries)
        if o.legendary_locks.value and (self._gl_sub or self._gl_box or self._gl_myth):
            for _ in range(8):
                self.multiworld.itempool.append(self.create_item("Gym Badge"))
                my_items_in_pool += 1

        # Trade evolution gate: single Link Cable
        if o.trade_locks.value and self._g_trade:
            self.multiworld.itempool.append(self.create_item("Link Cable"))
            my_items_in_pool += 1

        # Baby Pokémon gate: N Daycare items (configurable count)
        if o.baby_locks.value and self._g_baby:
            for _ in range(o.daycare_count.value):
                self.multiworld.itempool.append(self.create_item("Daycare"))
                my_items_in_pool += 1

        # Fossil Pokémon gate: single Fossil Restorer
        if o.fossil_locks.value and self._g_fossil:
            self.multiworld.itempool.append(self.create_item("Fossil Restorer"))
            my_items_in_pool += 1

        # Ultra Beast gate: single Ultra Wormhole
        if o.ultra_beast_locks.value and self._g_ub:
            self.multiworld.itempool.append(self.create_item("Ultra Wormhole"))
            my_items_in_pool += 1

        # Paradox Pokémon gate: single Time Rift
        if o.paradox_locks.value and self._g_para:
            self.multiworld.itempool.append(self.create_item("Time Rift"))
            my_items_in_pool += 1

        # Stone evolution gates: one item per stone type with active Pokémon in pool
        if o.stone_locks.value:
            for stone in self._g_stone:
                self.multiworld.itempool.append(self.create_item(f"{stone.title()} Stone"))
                my_items_in_pool += 1

        # Shiny Tokens: cosmetic filler items (~5% of active Pokémon count)
        if o.include_shinies.value and self.active_pokemon:
            shiny_count = max(1, len(self.active_pokemon) // 20)
            for _ in range(shiny_count):
                self.multiworld.itempool.append(self.create_item("Shiny Token"))
                my_items_in_pool += 1

        # Fill remaining locations with useful items/traps
        total_locations = sum(
            1 for loc in self.multiworld.get_locations(self.player) if loc.address is not None
        )
        trap_key_to_name = {
            "small_shuffle": "Small Shuffle Trap",
            "big_shuffle":   "Big Shuffle Trap",
            "derpy_mon":     "Derpy Mon Trap",
            "release":       "Release Trap",
        }
        trap_names = list(trap_key_to_name.values())
        raw_trap_weights = [self.options.trap_weights.value.get(k, 0) for k in trap_key_to_name]
        if sum(raw_trap_weights) == 0:
            raw_trap_weights = [1] * len(trap_names)
        trap_chance = self.options.trap_chance.value

        category_names = list(FILLER_ITEM_CATEGORIES.keys())
        category_weights = [self.options.filler_weights.value.get(cat, 0) for cat in category_names]
        if sum(category_weights) == 0:
            category_weights = [1] * len(category_names)

        while my_items_in_pool < total_locations:
            if self.random.randint(1, 100) <= trap_chance:
                filler_name = self.random.choices(trap_names, weights=raw_trap_weights, k=1)[0]
            else:
                chosen_category = self.random.choices(category_names, weights=category_weights, k=1)[0]
                filler_name = self.random.choice(FILLER_ITEM_CATEGORIES[chosen_category])
            self.multiworld.itempool.append(self.create_item(filler_name))
            my_items_in_pool += 1

    def _make_milestone_rule(self, target_count, req_groups):
        """Build an access rule that checks whether >= target_count Pokémon are logically accessible.

        req_groups is a list of (region_req, type_reqs_frozenset, extra_reqs_frozenset, count) tuples.
        A group's Pokémon are accessible when:
          - region_req is None (starting region / no region locks) OR the player has the Region Pass
          - type_reqs is empty (no type locks) OR the player has ALL required Type Keys
          - extra_reqs is empty OR the player meets all (item, min_count) requirements
        """
        player = self.player

        def rule(state):
            accessible = 0
            for region_req, type_reqs, extra_reqs, count in req_groups:
                if region_req and not state.has(region_req, player):
                    continue
                if type_reqs and not state.has_all(type_reqs, player):
                    continue
                if extra_reqs and not all(state.count(item, player) >= n for item, n in extra_reqs):
                    continue
                accessible += count
                if accessible >= target_count:
                    return True
            return False

        return rule

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # One AP Region per active game region
        game_regions: dict = {}
        for region_name in self.active_regions:
            ap_region = Region(f"{region_name} Region", self.player, self.multiworld)
            self.multiworld.regions.append(ap_region)
            game_regions[region_name] = ap_region

            ent = Entrance(self.player, f"Menu To {region_name}", menu_region)
            menu_region.exits.append(ent)
            ent.connect(ap_region)

            # Non-starting regions gated by Region Pass (dexsanity=ON only)
            if (self.options.region_locks.value and self.options.dexsanity.value
                    and region_name != self.starting_region):
                pass_name = f"{region_name} Pass"
                ent.access_rule = lambda state, p=pass_name: state.has(p, self.player)

        # Starting locations and global milestone locations → Menu region
        # Access rules for milestones are applied later in set_rules().
        start_loc_count = self.options.starting_location_count.value
        active_starting_locs = set(starting_locations[:start_loc_count])

        for loc_name, loc_id in self.location_name_to_id.items():
            if loc_name.startswith("Guess ") or loc_name.startswith("Caught "):
                continue  # Per-Pokemon handled below; type milestones handled below

            if loc_name in starting_locations and loc_name not in active_starting_locs:
                continue  # Excluded by starting_location_count option

            if loc_name.startswith("Guessed "):
                count = int(loc_name.split(" ")[1])
                if count > len(self.active_pokemon) - len(self.starter_names):
                    continue

            location = PokepelagoLocation(self.player, loc_name, loc_id, menu_region)
            menu_region.locations.append(location)

        # Type-specific milestone locations (e.g. "Caught 5 Fire Pokemon")
        # Only add milestones achievable with the current active Pokémon set.
        for p_type in GEN_1_TYPES:
            max_catchable = self._active_type_counts.get(p_type, 0)
            for step in TYPE_MILESTONE_STEPS:
                if step <= max_catchable:
                    loc_name = f"Caught {step} {p_type} Pokemon"
                    loc_id = self.location_name_to_id.get(loc_name)
                    if loc_id is not None:
                        location = PokepelagoLocation(self.player, loc_name, loc_id, menu_region)
                        menu_region.locations.append(location)

        if self.options.dexsanity.value:
            # Per-Pokemon sub-regions connected from their game region.
            # No access rules here — type key rules are set in set_rules().
            for mon in self.active_pokemon:
                mon_name = mon["name"]
                mon_region_name = get_pokemon_region(mon["id"])
                parent_region = game_regions.get(mon_region_name, menu_region)

                mon_sub_region = Region(f"Region {mon_name}", self.player, self.multiworld)
                self.multiworld.regions.append(mon_sub_region)

                loc_name = f"Guess {mon_name}"
                loc_id = self.location_name_to_id[loc_name]
                location = PokepelagoLocation(self.player, loc_name, loc_id, mon_sub_region)
                mon_sub_region.locations.append(location)

                entrance = Entrance(self.player, f"Catch {mon_name}", parent_region)
                parent_region.exits.append(entrance)
                entrance.connect(mon_sub_region)

        # Victory event location — client sends this check when goal_count Pokemon caught
        victory_location = PokepelagoLocation(self.player, "Pokepelago Victory", None, menu_region)
        menu_region.locations.append(victory_location)

    def set_rules(self):
        player = self.player

        # Type key access rules on "Guess X" locations.
        # Receiving a Type Key (from any player's game) enables guessing Pokemon of that type.
        # This creates real AP-tracked cross-player dependencies.
        if self.options.dexsanity.value and self.options.type_locks.value:
            for mon in self.active_pokemon:
                mon_name = mon["name"]
                type_keys = [f"{t} Type Key" for t in mon["types"]]
                location = self.multiworld.get_location(f"Guess {mon_name}", player)
                set_rule(location, lambda state, tk=type_keys: state.has_all(tk, self.player))

        # Extra gate access rules (legendary, trade, baby, fossil, UB, paradox, stone).
        # Applied on top of any existing type key rules — both must be satisfied.
        if self.options.dexsanity.value:
            for mon in self.active_pokemon:
                extra = self._extra_reqs(mon["id"])
                if not extra:
                    continue
                loc = self.multiworld.get_location(f"Guess {mon['name']}", player)
                prev_rule = loc.access_rule
                def _make_combined_rule(prev=prev_rule, er=extra, pl=player):
                    def rule(state):
                        return prev(state) and all(state.count(item, pl) >= n for item, n in er)
                    return rule
                set_rule(loc, _make_combined_rule())

        # ── Milestone access rules ──
        # "Guessed X Pokemon" milestones require that X non-starter Pokémon are
        # logically accessible (correct Region Passes + Type Keys).
        # Without these rules, "Guessed 1000 Pokemon" would be in logic immediately
        # even when only 151 Pokémon are reachable (starting region only).
        for loc in self.multiworld.get_locations(player):
            if loc.address is not None and loc.name.startswith("Guessed "):
                count = int(loc.name.split(" ")[1])
                set_rule(loc, self._make_milestone_rule(count, self._milestone_req_groups))

        # "Caught X {Type} Pokemon" milestones require that X non-starter Pokémon
        # of the given type are logically accessible.
        for loc in self.multiworld.get_locations(player):
            if loc.address is not None and loc.name.startswith("Caught "):
                parts = loc.name.split(" ")
                count = int(parts[1])
                p_type = parts[2]  # All type names are single words
                groups = self._type_milestone_req_groups.get(p_type, [])
                if groups:
                    set_rule(loc, self._make_milestone_rule(count, groups))

        # ── Victory rule ──
        # Victory requires that goal_count Pokémon are logically accessible.
        # This properly accounts for Region Passes AND Type Keys, rather than just
        # requiring all Region Passes blindly.
        victory_location = self.multiworld.get_location("Pokepelago Victory", player)
        set_rule(victory_location,
                 self._make_milestone_rule(self.goal_count, self._milestone_req_groups))

        victory_item = self.create_event_item("Victory")
        victory_location.place_locked_item(victory_item)

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> dict:
        o = self.options
        return {
            "type_locks": bool(o.type_locks.value),
            "region_locks": bool(o.region_locks.value),
            "active_regions": {r: list(REGION_RANGES[r]) for r in self.active_regions},
            "starting_region": self.starting_region,
            "goal_count": self.goal_count,
            "dexsanity": bool(o.dexsanity.value),
            "starting_locations": o.starting_location_count.value,
            "milestones": list(milestones),
            "starter_count": o.starting_location_count.value,
            # New lock flags
            "legendary_locks":   bool(o.legendary_locks.value),
            "trade_locks":       bool(o.trade_locks.value),
            "baby_locks":        bool(o.baby_locks.value),
            "daycare_count":     int(o.daycare_count.value),
            "fossil_locks":      bool(o.fossil_locks.value),
            "ultra_beast_locks": bool(o.ultra_beast_locks.value),
            "paradox_locks":     bool(o.paradox_locks.value),
            "stone_locks":       bool(o.stone_locks.value),
            "include_shinies":   bool(o.include_shinies.value),
            "starting_starter":  self.chosen_starter,
        }
