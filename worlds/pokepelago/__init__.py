from BaseClasses import Region, Entrance, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from .Items import PokepelagoItem, item_table, item_data_table, GEN_1_TYPES, FILLER_ITEM_CATEGORIES
from .Locations import PokepelagoLocation, location_table, milestones, starting_locations
from .Options import PokepelagoOptions, REGION_OPTION_ATTRS
from .data import POKEMON_DATA, GAME_REGIONS, REGION_RANGES, STARTERS_BY_REGION, get_pokemon_region

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

        self.starting_region = self.active_regions[0]
        self.starter_names: set = set(STARTERS_BY_REGION.get(self.starting_region, []))

        # Collect active Pokemon across all selected regions
        active_ids: set = set()
        for r in self.active_regions:
            lo, hi = REGION_RANGES[r]
            active_ids.update(range(lo, hi + 1))

        self.active_pokemon = [mon for mon in POKEMON_DATA if mon["id"] in active_ids]
        self.active_pokemon_names = [mon["name"] for mon in self.active_pokemon]
        self._mon_lookup: dict = {mon["name"]: mon for mon in self.active_pokemon}

        # Goal count: number of Pokemon the client needs to catch for victory
        total = len(self.active_pokemon)
        if self.options.goal_type.value == 0:  # percentage
            raw_goal = max(1, round(total * self.options.goal_percentage.value / 100))
        else:  # count
            raw_goal = min(self.options.goal_count.value, total)

        # Snap to closest valid milestone
        total_guessable = total - len(self.starter_names)
        valid_milestones = [m for m in milestones if m <= total_guessable]
        if not valid_milestones:
            valid_milestones = [1]
        capped_goal = min(raw_goal, max(valid_milestones))
        self.goal_count = min(valid_milestones, key=lambda m: abs(m - capped_goal))

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
        for p_type in starter_types:
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
            for region in self.active_regions[1:]:
                self.multiworld.itempool.append(self.create_item(f"{region} Pass"))
                my_items_in_pool += 1

        # Fill remaining locations with useful items/traps
        total_locations = sum(
            1 for loc in self.multiworld.get_locations(self.player) if loc.address is not None
        )
        trap_fillers = ["Small Shuffle Trap", "Big Shuffle Trap", "Derpy Mon Trap", "Release Trap"]
        trap_chance = self.options.trap_chance.value

        category_names = list(FILLER_ITEM_CATEGORIES.keys())
        category_weights = [self.options.filler_weights.value.get(cat, 0) for cat in category_names]
        if sum(category_weights) == 0:
            category_weights = [1] * len(category_names)

        while my_items_in_pool < total_locations:
            if self.random.randint(1, 100) <= trap_chance:
                filler_name = self.random.choice(trap_fillers)
            else:
                chosen_category = self.random.choices(category_names, weights=category_weights, k=1)[0]
                filler_name = self.random.choice(FILLER_ITEM_CATEGORIES[chosen_category])
            self.multiworld.itempool.append(self.create_item(filler_name))
            my_items_in_pool += 1

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

        # Starting locations and global milestone locations → Menu region (no rules)
        starting_loc_set = set(starting_locations) if not self.options.include_starting_locations.value else set()

        for loc_name, loc_id in self.location_name_to_id.items():
            if loc_name.startswith("Guess ") or loc_name.startswith("Caught "):
                continue  # Per-Pokemon handled below; type milestones skipped

            if loc_name in starting_loc_set:
                continue  # Disabled by include_starting_locations option

            if loc_name.startswith("Guessed "):
                count = int(loc_name.split(" ")[1])
                if count > len(self.active_pokemon) - len(self.starter_names):
                    continue

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

        # Victory: require all Region Passes for non-starting regions.
        # This gives AP a meaningful completion condition for sphere calculation.
        victory_location = self.multiworld.get_location("Pokepelago Victory", player)

        non_starting = (
            self.active_regions[1:]
            if self.options.region_locks.value and self.options.dexsanity.value
            else []
        )
        if non_starting:
            victory_location.access_rule = lambda state: all(
                state.has(f"{r} Pass", player) for r in non_starting
            )

        victory_item = self.create_event_item("Victory")
        victory_location.place_locked_item(victory_item)

        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)

    def fill_slot_data(self) -> dict:
        return {
            "type_locks": bool(self.options.type_locks.value),
            "region_locks": bool(self.options.region_locks.value),
            "active_regions": {r: list(REGION_RANGES[r]) for r in self.active_regions},
            "starting_region": self.starting_region,
            "goal_count": self.goal_count,
            "dexsanity": bool(self.options.dexsanity.value),
            "starting_locations": bool(self.options.include_starting_locations.value),
        }
