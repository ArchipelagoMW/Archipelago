from typing import Any, Dict, List, Set

from BaseClasses import Entrance, Location, Region, Tutorial
from Options import OptionError
from worlds.AutoWorld import WebWorld, World

from .Constants import *
from .Items import SRItem, TrapItemData, filler, item_table, stages, traps
from .Locations import (SRLocation, books_table, enemies_table,
                        location_name_to_id, stages_table)
from .Options import SROptions
from .Regions import regions
from .Rules import set_rules


class StickRangerWeb(WebWorld):
    tutorials: List[Tutorial] = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Stick Ranger randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Kryen112"]
    )]


class StickRanger(World):
    """
    Stick Ranger is a unique 2D action RPG developed by Dan-Ball.
    Assemble a team of rangers, customize their classes, and battle through a variety of stages filled with enemies.
    """
    game: str = "Stick Ranger"
    options_dataclass = SROptions
    options: SROptions
    location_name_to_id: Dict[str, int] = location_name_to_id
    item_name_to_id: Dict[str, int] = { name: data.code for name, data in item_table.items() }
    web: StickRangerWeb = StickRangerWeb()

    def generate_early(self) -> None:
        """
        Called per player before any items or locations are created.
        Used to exclude locations that are non-goal locations.
        """
        self.excluded_locations: Set[str] = set()
        chosen_goals: List[str] = Constants.GOAL_OPTIONS_MAP[self.options.goal.value]
        allowed: Set[str] = set()
        for goal in chosen_goals:
            allowed.update(Constants.GOAL_LOCATIONS[goal])
        all_goal_locations: Set[str] = set().union(*Constants.GOAL_LOCATIONS.values())
        non_goal_locations: Set[str] = all_goal_locations - allowed

        existing_names: Set[str] = set(self.location_name_to_id.keys())
        to_exclude: Set[str] = non_goal_locations & existing_names

        self.excluded_locations |= to_exclude

    def create_regions(self) -> None:
        if self.options.shuffle_books == 0 and self.options.shuffle_enemies == 0:
            raise OptionError(
                "At least one of 'shuffle_books' or 'shuffle_enemies' must be enabled."
            )

        menu_region: Region = Region("Menu", self.player, self.multiworld)
        world_map_region: Region = Region("World Map", self.player, self.multiworld)
        self.multiworld.regions += [menu_region, world_map_region]
        menu_to_world_map_exit: Entrance = Entrance(self.player, "World Map", menu_region)
        menu_region.exits.append(menu_to_world_map_exit)
        menu_to_world_map_exit.connect(world_map_region)

        def filter_locations(table, region, filter_func=None) -> Dict[str, int]:
            return {
                loc["name"]: loc_id
                for loc_id, loc in table.items()
                if loc["region"] == region and (filter_func(loc) if filter_func else True)
            }

        def make_unlock_rule(region_name) -> bool:
            return lambda state: state.has(f"Unlock {region_name}", self.player)

        for region_name in regions:
            region: Region = Region(region_name, self.player, self.multiworld)

            stage_locs: Dict[str, int] = filter_locations(stages_table, region_name)
            region.add_locations(stage_locs, SRLocation)

            if self.options.shuffle_books == 1:
                book_locs: Dict[str, int] = filter_locations(books_table, region_name)
                region.add_locations(book_locs, SRLocation)

            if self.options.shuffle_enemies > 0:
                enemy_filters: Dict[int, Any] = {
                    Constants.ENEMIES_OPTION_NON_BOSS: lambda loc: "boss" not in loc["name"].lower(),
                    Constants.ENEMIES_OPTION_BOSS: lambda loc: "boss" in loc["name"].lower(),
                    Constants.ENEMIES_OPTION_ALL: None
                }

                enemy_locations: Dict[str, int] = filter_locations(enemies_table, region_name, enemy_filters.get(self.options.shuffle_enemies))
                region.add_locations(enemy_locations, SRLocation)

            self.multiworld.regions.append(region)

            world_map_exit: Entrance = Entrance(self.player, region_name, world_map_region)
            if region_name != "Opening Street":
                world_map_exit.access_rule = make_unlock_rule(region_name)
            world_map_region.exits.append(world_map_exit)
            world_map_exit.connect(region)

        self.location_count: int = len(self.multiworld.get_locations(self.player))

    def create_item(self, name: str) -> SRItem:
        item_data: Any | None = item_table.get(name)
        return SRItem(name, item_data.classification, item_data.code, self.player)

    def create_items(self) -> None:
        # Make sure at least 1 Opening Street check is an early unlock
        starter_item_name: str = self.multiworld.random.choice(Constants.STARTER_UNLOCK_CHOICES)
        starter_item: SRItem = self.create_item(starter_item_name)

        starter_location_names: List[str] = [Constants.OPENING_STREET_EXIT]
        if self.options.shuffle_books.value == 1:
            starter_location_names.append(Constants.OPENING_STREET_BOOK)
        shuffle_enemies: int = self.options.shuffle_enemies.value
        if shuffle_enemies in (1, 3):
            starter_location_names.extend(Constants.OPENING_STREET_ENEMIES)
        if shuffle_enemies in (2, 3):
            starter_location_names.append(Constants.OPENING_STREET_BOSS)

        random_loc_name: str = self.multiworld.random.choice(starter_location_names)
        starter_loc: Location = self.multiworld.get_location(random_loc_name, self.player)
        starter_loc.place_locked_item(starter_item)
        self.location_count -= 1

        itempool: List[SRItem] = []
        # Add Ranger Classes
        if self.options.ranger_class_randomizer.value:
            for cls in Constants.RANGER_CLASSES:
                if cls != self.options.ranger_class_selected.value:
                    itempool.append(self.create_item(f"Unlock {cls} Class"))

        # Add Unlock Stages into the pool
        itempool.extend(
            self.create_item(unlock.item_name)
            for unlock in stages
            if unlock.item_name != starter_item_name
            if unlock.item_name not in self.excluded_locations
            and (
                not self.options.ranger_class_randomizer.value
                or unlock.item_name != "Unlock Forget Tree"
            )
        )

        # Add Traps
        traps_option: int = self.options.traps.value
        missing_locs: int = self.location_count - len(itempool)
        traps_percentage: int = 0
        if traps_option >= 1:
            traps_percentage = traps_option * Constants.TRAP_STEP_PERCENT

        trap_count: int = int((traps_percentage / 100) * missing_locs)
        trap_weights: List[int] = [trap.weight for trap in traps]
        for _ in range(trap_count):
            trap: TrapItemData = self.multiworld.random.choices(traps, weights=trap_weights, k=1)[0]
            itempool.append(self.create_item(trap.item_name))

        # Add Filler
        while len(itempool) < self.location_count:
            itempool.append(self.create_item(self.multiworld.random.choice(filler).item_name))

        self.multiworld.itempool += itempool

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = self.options.as_dict(
            "goal",
            "ranger_class_randomizer",
            "ranger_class_selected",
            "classes_req_for_castle",
            "classes_req_for_submarine_shrine",
            "classes_req_for_pyramid",
            "classes_req_for_ice_castle",
            "classes_req_for_hell_castle",
            "min_stages_req_for_castle",
            "max_stages_req_for_castle",
            "min_stages_req_for_submarine_shrine",
            "max_stages_req_for_submarine_shrine",
            "min_stages_req_for_pyramid",
            "max_stages_req_for_pyramid",
            "min_stages_req_for_ice_castle",
            "max_stages_req_for_ice_castle",
            "min_stages_req_for_hell_castle",
            "max_stages_req_for_hell_castle",
            "shuffle_books",
            "shuffle_enemies",
            "gold_multiplier",
            "xp_multiplier",
            "drop_multiplier",
            "randomize_book_costs",
            "shop_hints",
            "traps",
            "remove_null_compo",
            "death_link"
        )
        slot_data.update({
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player
        })
        return slot_data

    set_rules = set_rules