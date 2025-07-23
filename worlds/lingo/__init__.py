"""
Archipelago init file for Lingo
"""
from logging import warning

from BaseClasses import CollectionState, Item, ItemClassification, Tutorial, Location, LocationProgressType
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from .datatypes import Room, RoomEntrance
from .items import ALL_ITEM_TABLE, ITEMS_BY_GROUP, TRAP_ITEMS, LingoItem
from .locations import ALL_LOCATION_TABLE, LOCATIONS_BY_GROUP
from .options import LingoOptions, lingo_option_groups, SunwarpAccess, VictoryCondition
from .player_logic import LingoPlayerLogic
from .regions import create_regions


class LingoWebWorld(WebWorld):
    option_groups = lingo_option_groups
    rich_text_options_doc = True
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Lingo with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["hatkirby"]
    )]


class LingoWorld(World):
    """
    Lingo is a first person indie puzzle game in the vein of The Witness. You find yourself in a mazelike, non-Euclidean
    world filled with 800 word puzzles that use a variety of different mechanics.
    """
    game = "Lingo"
    web = LingoWebWorld()

    base_id = 444400
    topology_present = True

    options_dataclass = LingoOptions
    options: LingoOptions

    item_name_to_id = {
        name: data.code for name, data in ALL_ITEM_TABLE.items()
    }
    location_name_to_id = {
        name: data.code for name, data in ALL_LOCATION_TABLE.items()
    }
    item_name_groups = ITEMS_BY_GROUP
    location_name_groups = LOCATIONS_BY_GROUP

    player_logic: LingoPlayerLogic

    def generate_early(self):
        if not (self.options.shuffle_doors or self.options.shuffle_colors or
                (self.options.sunwarp_access >= SunwarpAccess.option_unlock and
                 self.options.victory_condition == VictoryCondition.option_pilgrimage)):
            if self.multiworld.players == 1:
                warning(f"{self.player_name}'s Lingo world doesn't have any progression items. Please turn on Door"
                        f" Shuffle or Color Shuffle, or use item-blocked sunwarps with the Pilgrimage victory condition"
                        f" if that doesn't seem right.")
            else:
                raise OptionError(f"{self.player_name}'s Lingo world doesn't have any progression items. Please turn on"
                                  f" Door Shuffle or Color Shuffle, or use item-blocked sunwarps with the Pilgrimage"
                                  f" victory condition.")

        self.player_logic = LingoPlayerLogic(self)

    def create_regions(self):
        create_regions(self)

        if not self.options.shuffle_postgame:
            state = CollectionState(self.multiworld)
            state.collect(LingoItem("Prevent Victory", ItemClassification.progression, None, self.player), True)

            # Note: relies on the assumption that real_items is a definitive list of real progression items in this
            # world, and is not modified after being created.
            for item in self.player_logic.real_items:
                state.collect(self.create_item(item), True)

            all_locations = self.multiworld.get_locations(self.player)
            state.sweep_for_advancements(locations=all_locations)

            unreachable_locations = [location for location in all_locations
                                     if not state.can_reach_location(location.name, self.player)]

            for location in unreachable_locations:
                if location.name in self.player_logic.event_loc_to_item.keys():
                    continue

                self.player_logic.real_locations.remove(location.name)
                location.parent_region.locations.remove(location)

            if len(self.player_logic.real_items) > len(self.player_logic.real_locations):
                raise OptionError(f"{self.player_name}'s Lingo world does not have enough locations to fit the number"
                                  f" of required items without shuffling the postgame. Either enable postgame"
                                  f" shuffling, or choose different options.")

    def create_items(self):
        pool = [self.create_item(name) for name in self.player_logic.real_items]

        item_difference = len(self.player_logic.real_locations) - len(pool)
        if item_difference:
            trap_percentage = self.options.trap_percentage
            traps = int(item_difference * trap_percentage / 100.0)
            non_traps = item_difference - traps

            if non_traps:
                skip_percentage = self.options.puzzle_skip_percentage
                skips = int(non_traps * skip_percentage / 100.0)
                non_skips = non_traps - skips

                for i in range(0, non_skips):
                    pool.append(self.create_item(self.get_filler_item_name()))

                for i in range(0, skips):
                    pool.append(self.create_item("Puzzle Skip"))

            if traps:
                if self.options.speed_boost_mode:
                    self.options.trap_weights.value["Slowness Trap"] = 0

                total_weight = sum(self.options.trap_weights.values())

                if total_weight == 0:
                    raise OptionError("Sum of trap weights must be at least one.")

                trap_counts = {name: int(weight * traps / total_weight)
                               for name, weight in self.options.trap_weights.items()}

                trap_difference = traps - sum(trap_counts.values())
                if trap_difference > 0:
                    allowed_traps = [name for name in TRAP_ITEMS if self.options.trap_weights[name] > 0]
                    for i in range(0, trap_difference):
                        trap_counts[allowed_traps[i % len(allowed_traps)]] += 1

                for name, count in trap_counts.items():
                    for i in range(0, count):
                        pool.append(self.create_item(name))

        self.multiworld.itempool += pool

    def create_item(self, name: str) -> Item:
        item = ALL_ITEM_TABLE[name]

        classification = item.classification
        if hasattr(self, "options") and self.options.shuffle_paintings and len(item.painting_ids) > 0 \
                and not item.has_doors and all(painting_id not in self.player_logic.painting_mapping
                                               for painting_id in item.painting_ids) \
                and "pilgrim_painting2" not in item.painting_ids:
            # If this is a "door" that just moves one or more paintings, and painting shuffle is on and those paintings
            # go nowhere, then this item should not be progression. The Pilgrim Room painting is special and needs to be
            # excluded from this.
            classification = ItemClassification.filler

        return LingoItem(name, classification, item.code, self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def place_good_item(self, progitempool: list[Item], fill_locations: list[Location]):
        if len(self.player_logic.good_item_options) == 0:
            return

        good_location = self.get_location("Second Room - Good Luck")
        if good_location.progress_type == LocationProgressType.EXCLUDED or good_location not in fill_locations:
            return

        good_items = list(filter(lambda progitem: progitem.player == self.player and
                                                  progitem.name in self.player_logic.good_item_options, progitempool))

        if len(good_items) == 0:
            return

        good_item = self.random.choice(good_items)
        good_location.place_locked_item(good_item)

        progitempool.remove(good_item)
        fill_locations.remove(good_location)

    def fill_hook(self, progitempool: list[Item], usefulitempool: list[Item], filleritempool: list[Item],
                  fill_locations: list[Location]):
        self.place_good_item(progitempool, fill_locations)

    def fill_slot_data(self):
        slot_options = [
            "death_link", "victory_condition", "shuffle_colors", "shuffle_doors", "shuffle_paintings", "shuffle_panels",
            "enable_pilgrimage", "sunwarp_access", "mastery_achievements", "level_2_requirement", "location_checks",
            "early_color_hallways", "pilgrimage_allows_roof_access", "pilgrimage_allows_paintings", "shuffle_sunwarps",
            "group_doors", "speed_boost_mode", "shuffle_postgame"
        ]

        slot_data = {
            "seed": self.random.randint(0, 1000000),
            **self.options.as_dict(*slot_options),
        }

        if self.options.shuffle_paintings:
            slot_data["painting_entrance_to_exit"] = self.player_logic.painting_mapping

        if self.options.shuffle_sunwarps:
            slot_data["sunwarp_permutation"] = self.player_logic.sunwarp_mapping

        return slot_data

    def get_filler_item_name(self) -> str:
        if self.options.speed_boost_mode:
            return "Speed Boost"
        else:
            filler_list = [":)", "The Feeling of Being Lost", "Wanderlust", "Empty White Hallways"]
            return self.random.choice(filler_list)
