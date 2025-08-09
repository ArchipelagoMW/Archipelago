import os
import logging
import random
from typing import List, Union, ClassVar, Any, Optional, Tuple
import settings
from BaseClasses import Tutorial, Region, Location, LocationProgressType, Item, ItemClassification
from Fill import fill_restrictive, FillError
from Options import Accessibility, OptionError
from worlds.AutoWorld import WebWorld, World

from .Util import *
from .Options import *
from .Logic import create_connections
from .data import LOCATIONS_DATA
from .data.Constants import *
from .data.Items import ITEMS_DATA
from .data.Regions import REGIONS
from .data.LogicPredicates import *

from .Client import SpiritTracksClient  # Unused, but required to register with BizHawkClient


class SpiritTracksWeb(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Spirit Tracks for Archipelago on your computer.",
        "English",
        "st_setup_en.md",
        "st_setup/en",
        ["DayKat"]
    )

    tutorials = [setup_en]


# Adds a consistent count of items to pool, independent of how many are from locations
def add_items_from_filler(item_pool_dict: dict, filler_item_count: int, item: str, count: int):
    if filler_item_count >= count:
        filler_item_count -= count
        item_pool_dict[item] = count
    else:
        item_pool_dict[item] = filler_item_count
        filler_item_count = 0

    return [item_pool_dict, filler_item_count]


"""TODO def add_additional_spirit_gems(item_pool_dict: dict, filler_item_count: int):
    def add_gems(gem: str, filler_count: int):
        gems = 20 - item_pool_dict[gem]
        if filler_count >= gems:
            filler_count -= gems
            item_pool_dict[gem] = 20
        return filler_count

    filler_item_count = add_gems("Power Gem", filler_item_count)
    filler_item_count = add_gems("Wisdom Gem", filler_item_count)
    filler_item_count = add_gems("Courage Gem", filler_item_count)

    return [item_pool_dict, filler_item_count] """


class SpiritTracksWorld(World):
    """
    The Legend of Zelda: Spirit Tracks is the train bound handheld sequel to Phantom Hourglass.
    """
    game = "The Legend of Zelda - Spirit Tracks"
    options_dataclass = SpiritTracksOptions
    options: SpiritTracksOptions
    required_client_version = (0, 6, 1)
    web = SpiritTracksWeb()
    topology_present = True

    settings_key = "tloz_st_options"

    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    item_name_groups = ITEM_GROUPS
    origin_region_name = "aboda village"

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

        self.pre_fill_items: List[Item] = []
        self.required_dungeons = []
        self.boss_reward_items_pool = []
        self.boss_reward_location_names = []
        self.dungeon_name_groups = {}
        self.locations_to_exclude = set()
        self.ut_locations_to_exclude = set()
        self.extra_filler_items = []
        self.excluded_dungeons = []

    def generate_early(self):
        # self.pick_required_dungeons()
        # self.restrict_non_local_items()
        pass

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        if not self.options.keysanity == "anywhere":
            self.options.non_local_items.value -= self.item_name_groups["Small Keys"]
        self.options.non_local_items.value -= set(self.boss_reward_items_pool)

    def create_location(self, region_name: str, location_name: str, local: bool):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
        region.locations.append(location)

        if local:
            location.item_rule = lambda item: item.player == self.player

    def create_regions(self):
        # Create regions
        for region_name in REGIONS:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations
        for location_name, location_data in LOCATIONS_DATA.items():
            if not self.location_is_active(location_name, location_data):
                continue

            is_local = "local" in location_data and location_data["local"] is True
            self.create_location(location_data['region_id'], location_name, is_local)

        self.create_events()
        # self.exclude_locations_automatically()

    def create_event(self, region_name, event_item_name):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, region_name + ".event", None, region)
        region.locations.append(location)
        location.place_locked_item(Item(event_item_name, ItemClassification.progression, None, self.player))

    def location_is_active(self, location_name, location_data):
        if not location_data.get("conditional", False):
            return True
        return False

    """TODO def pick_required_dungeons(self):
        implemented_dungeons = ["Temple of Fire",
                                "Temple of Wind",
                                "Temple of Courage",
                                "Goron Temple",
                                "Temple of Ice",
                                "Mutoh's Temple",
                                "Ghost Ship",
                                "Temple of the Ocean King"] 
        # Remove optional dungeons from pool
        if self.options.ghost_ship_in_dungeon_pool == "false":
            implemented_dungeons.remove("Ghost Ship")
        if not self.options.totok_in_dungeon_pool:
            implemented_dungeons.remove("Temple of the Ocean King")
        self.random.shuffle(implemented_dungeons)
        # Cap dungeons required if over the number of eligible dungeons
        dungeons_required = len(implemented_dungeons) if self.options.dungeons_required > len(implemented_dungeons) \
            else self.options.dungeons_required.value
        self.options.dungeons_required.value = dungeons_required
        self.required_dungeons = implemented_dungeons[:dungeons_required]

        # Extend mcguffin list
        boss_reward_pool = ITEM_GROUPS["Vanilla Metals"]
        self.random.shuffle(boss_reward_pool)
        while self.options.dungeons_required > len(boss_reward_pool):
            boss_reward_pool.append("Additional Rare Metal")
        self.boss_reward_items_pool = boss_reward_pool[:self.options.dungeons_required]"""

    def create_events(self):
        # if "Temple of Fire" in self.required_dungeons:
        #     self.create_event("tof blaaz", "_required_dungeon")
        self.create_event("goal", "_beaten_game")

    def exclude_locations_automatically(self):
        locations_to_exclude = set()

        # If non required dungeons need to be excluded, and not UT
        if self.options.exclude_non_required_dungeons and not getattr(self.multiworld, "generation_is_fake", False):
            #TODO always_include = ["Temple of the Ocean King", "Mountain Passage"]
            always_include = []
            excluded_dungeons = [d for d in DUNGEON_NAMES
                                 if d not in self.required_dungeons + always_include]
            self.excluded_dungeons = excluded_dungeons
            for dungeon in excluded_dungeons:
                locations_to_exclude.update(self.dungeon_name_groups[dungeon])

            self.ut_locations_to_exclude = locations_to_exclude.copy()
            # Unexclude locations that have vanilla small keys/dung items cause in excluded dungeons, keys are vanilla
            for location in locations_to_exclude.copy():
                if ("Small Key" in LOCATIONS_DATA[location]["vanilla_item"] or
                        "Boss Key" in LOCATIONS_DATA[location]["vanilla_item"]):
                    locations_to_exclude.remove(location)

        self.locations_to_exclude = locations_to_exclude
        for name in locations_to_exclude:
            self.multiworld.get_location(name, self.player).progress_type = LocationProgressType.EXCLUDED

    def set_rules(self):
        create_connections(self.multiworld, self.player, self.origin_region_name, self.options)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("_beaten_game", self.player)

    def create_item(self, name: str) -> Item:
        classification = ITEMS_DATA[name]['classification']
        if name in self.extra_filler_items:
            self.extra_filler_items.remove(name)
            classification = ItemClassification.filler

        ap_code = self.item_name_to_id[name]
        return Item(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        removed_item_quantities = self.options.remove_items_from_pool.value.copy()
        item_pool_dict = {}
        filler_item_count = 0
        rupee_item_count = 0
        boss_reward_item_count = self.options.dungeons_required
        for loc_name, loc_data in LOCATIONS_DATA.items():
            print(f"New Location: {loc_name}")
            if not self.location_is_active(loc_name, loc_data):
                print(f"{loc_name} is not active")
                continue
            # If no defined vanilla item, fill with filler
            if "vanilla_item" not in loc_data:
                print(f"{loc_name} has no defined vanilla item")
                filler_item_count += 1
                continue

            item_name = loc_data.get("item_override", loc_data["vanilla_item"])
            if item_name in removed_item_quantities and removed_item_quantities[item_name] > 0:
                # If item was put in the "remove_items_from_pool" option, replace it with a random filler item
                removed_item_quantities[item_name] -= 1
                filler_item_count += 1
                continue
            if item_name == "Filler Item":
                filler_item_count += 1
                continue
            if "force_vanilla" in loc_data and loc_data["force_vanilla"]:
                forced_item = self.create_item(item_name)
                self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                continue

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # TODO Fill filler count with consistent amounts of items, when filler count is empty it won't add any more items
        # so add progression items first
        add_items = [("Heart Container", 13)]
        for i, count in add_items:
            item_pool_dict, filler_item_count = add_items_from_filler(item_pool_dict, filler_item_count, i, count)

        # Add as many filler items as required
        for _ in range(filler_item_count):
            random_filler_item = self.get_filler_item_name()
            item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1

        return item_pool_dict

    def create_items(self):
        item_pool_dict = self.build_item_pool_dict()
        self.get_extra_filler_items(item_pool_dict)
        items = []
        for item_name, quantity in item_pool_dict.items():
            for _ in range(quantity):
                items.append(self.create_item(item_name))

        # self.filter_confined_dungeon_items_from_pool(items)
        self.multiworld.itempool.extend(items)

    def get_extra_filler_items(self, item_pool_dict):
        # Create a random list of useful or currency items to turn into filler to satisfy all removed locations
        filler_count = 0
        extra_items_list = []
        for item, count in item_pool_dict.items():
            if 'backup_filler' in ITEMS_DATA[item]:
                extra_items_list.extend([item] * count)
            if ITEMS_DATA[item]["classification"] in [ItemClassification.filler, ItemClassification.trap]:
                filler_count += count

        extra_item_count = len(self.locations_to_exclude) - filler_count + 20
        if extra_item_count > 0:
            self.random.shuffle(extra_items_list)
            self.extra_filler_items = extra_items_list[:extra_item_count]

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        # self.pre_fill_boss_rewards()
        # self.pre_fill_dungeon_items()
        pass

    def filter_confined_dungeon_items_from_pool(self, items: List[Item]):
        confined_dungeon_items = []

        # Confine small keys to own dungeon if option is enabled
        if self.options.keysanity == "in_own_dungeon":
            confined_dungeon_items.extend([item for item in items if item.name.startswith("Small Key")])

        # Remove boss reward items from pool for pre filling
        confined_dungeon_items.extend([item for item in items if item.name in self.boss_reward_items_pool])

        for item in confined_dungeon_items:
            items.remove(item)
        self.pre_fill_items.extend(confined_dungeon_items)

    def pre_fill_boss_rewards(self):
        boss_reward_location_names = [DUNGEON_TO_BOSS_ITEM_LOCATION[dung_name] for dung_name in self.required_dungeons]
        self.boss_reward_location_names = boss_reward_location_names

        boss_reward_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                 if loc.name in boss_reward_location_names]
        boss_reward_items = [item for item in self.pre_fill_items if item.name in self.boss_reward_items_pool]

        # Remove from the all_state the items we're about to place
        for item in boss_reward_items:
            self.pre_fill_items.remove(item)

        collection_state = self.multiworld.get_all_state(False)
        # Perform a prefill to place confined items inside locations of this dungeon
        self.random.shuffle(boss_reward_locations)
        fill_restrictive(self.multiworld, collection_state, boss_reward_locations, boss_reward_items,
                         single_player_placement=True, lock=True, allow_excluded=True)

    def pre_fill_dungeon_items(self):
        # If keysanity is off, dungeon items can only be put inside local dungeon locations, and there are not so many
        # of those which makes them pretty crowded.
        # This usually ends up with generator not having anywhere to place a few small keys, making the seed unbeatable.
        # To circumvent this, we perform a restricted pre-fill here, placing only those dungeon items
        # before anything else.
        for dung_name in DUNGEON_NAMES:
            # Build a list of locations in this dungeon
            print(f"Pre-filling {dung_name}")
            dungeon_location_names = [name for name, loc in LOCATIONS_DATA.items()
                                      if "dungeon" in loc and loc["dungeon"] == dung_name]
            dungeon_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                 if loc.name in dungeon_location_names and not loc.locked]

            # From the list of all dungeon items that needs to be placed restrictively, only filter the ones for the
            # dungeon we are currently processing.
            confined_dungeon_items = [item for item in self.pre_fill_items
                                      if item.name.endswith(f"({dung_name})")]
            if len(confined_dungeon_items) == 0:
                continue  # This list might be empty with some keysanity options

            # Remove from the all_state the items we're about to place
            for item in confined_dungeon_items:
                self.pre_fill_items.remove(item)
            collection_state = self.multiworld.get_all_state(False)
            # Perform a prefill to place confined items inside locations of this dungeon
            self.random.shuffle(dungeon_locations)
            fill_restrictive(self.multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                             single_player_placement=True, lock=True, allow_excluded=True)

    def get_filler_item_name(self) -> str:
        filler_item_names = [
            "Blue Rupee (5)",
            "Red Rupee (20)",
            "Rupoor (-10)"
        ]

        item_name = self.random.choice(filler_item_names)
        return item_name

    def fill_slot_data(self) -> dict:
        options = ["keysanity", "goal", "logic"]
        # slot_data = self.options.as_dict(*options)
        slot_data = {}
        return slot_data

    def write_spoiler(self, spoiler_handle):
        return
        
        spoiler_handle.write(f"\n\nRequired Dungeons ({self.multiworld.player_name[self.player]}):\n")
        for dung in self.required_dungeons:
            spoiler_handle.write(f"\t- {dung}\n")

    # UT stuff
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, any]) -> None:
        return slot_data

