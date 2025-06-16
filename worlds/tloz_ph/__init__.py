import os
import logging
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

from .Client import PhantomHourglassClient  # Unused, but required to register with BizHawkClient


class PhantomHourglassWeb(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Phantom Hourglass pseudo manual for Archipelago on your computer.",
        "English",
        "ph_setup_en.md",
        "ph_setup/en",
        ["Carrotinator"]
    )

    tutorials = [setup_en]


class PhantomHourglassWorld(World):
    """
    The Legend of Zelda: Phantom Hourglass is the sea bound handheld sequel to the Wind Waker.
    """
    game = "The Legend of Zelda - Phantom Hourglass"
    options_dataclass = PhantomHourglassOptions
    options: PhantomHourglassOptions
    required_client_version = (0, 6, 1)
    web = PhantomHourglassWeb()
    topology_present = True

    settings_key = "tloz_ph_options"

    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    item_name_groups = ITEM_GROUPS
    origin_region_name = "mercay island"

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

        self.pre_fill_items: List[Item] = []

    def generate_early(self):
        self.restrict_non_local_items()

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        print(f"Keysanity value: {self.options.keysanity}, {self.options.keysanity.current_option_name}")
        if not self.options.keysanity == "anywhere":
            self.options.non_local_items.value -= self.item_name_groups["Small Keys"]

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
        self.exclude_locations_automatically()

    def create_event(self, region_name, event_item_name):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, region_name + ".event", None, region)
        region.locations.append(location)
        location.place_locked_item(Item(event_item_name, ItemClassification.progression, None, self.player))

    def location_is_active(self, location_name, location_data):
        if not location_data.get("conditional", False):
            return True
        else:
            if location_name in FROG_LOCATION_NAMES:
                return self.options.randomize_frogs != PhantomHourglassFrogRandomization.option_start_with
            return False


    def create_events(self):
        self.create_event("goal", "_beaten_game")

    def exclude_locations_automatically(self):
        locations_to_exclude = set()
        for name in locations_to_exclude:
            self.multiworld.get_location(name, self.player).progress_type = LocationProgressType.EXCLUDED

    def set_rules(self):
        create_connections(self.multiworld, self.player, self.origin_region_name, self.options)
        self.multiworld.completion_condition[self.player] = lambda state: ph_has_sea_chart(state, self.player, "SW")
        self.multiworld.completion_condition[self.player] = lambda state: state.has("_beaten_game", self.player)

    def create_item(self, name: str) -> Item:
        classification = ITEMS_DATA[name]['classification']
        ap_code = self.item_name_to_id[name]
        print(f"Created item {name}")
        return Item(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        removed_item_quantities = self.options.remove_items_from_pool.value.copy()
        item_pool_dict = {}
        filler_item_count = 0
        rupee_item_count = 0
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
                print(f"{item_name} @ {loc_name} was removed from pool")
                removed_item_quantities[item_name] -= 1
                filler_item_count += 1
                continue
            if item_name == "Filler Item":
                filler_item_count += 1
                print(f"added filler item @ {loc_name}")
                continue
            if self.options.keysanity == "vanilla":
                if "Small Key" in item_name:
                    key_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(key_item)
                    continue
            if "force_vanilla" in loc_data and loc_data["force_vanilla"]:
                print(f"Forcing {loc_name} with item {item_name}")
                forced_item = self.create_item(item_name)
                self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                continue
            if item_name in FROG_NAMES:
                if self.options.randomize_frogs == "vanilla":
                    forced_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                    continue

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # Add as many filler items as required
        for _ in range(filler_item_count):
            random_filler_item = self.get_filler_item_name()
            item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1

        return item_pool_dict

    def create_items(self):
        item_pool_dict = self.build_item_pool_dict()
        items = []
        for item_name, quantity in item_pool_dict.items():
            for _ in range(quantity):
                items.append(self.create_item(item_name))

        self.filter_confined_dungeon_items_from_pool(items)
        self.multiworld.itempool.extend(items)

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        self.pre_fill_dungeon_items()

    def filter_confined_dungeon_items_from_pool(self, items: List[Item]):
        confined_dungeon_items = []

        # Confine small keys to own dungeon if option is enabled
        if self.options.keysanity == "in_own_dungeon":
            confined_dungeon_items.extend([item for item in items if item.name.startswith("Small Key")])

        for item in confined_dungeon_items:
            items.remove(item)
        self.pre_fill_items.extend(confined_dungeon_items)


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
            print(f"Removing items {confined_dungeon_items}")
            print(f"Filling locations {dungeon_locations}")
            fill_restrictive(self.multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                             single_player_placement=True, lock=True, allow_excluded=True)


    def get_filler_item_name(self) -> str:
        FILLER_ITEM_NAMES = [
            "Red Rupee (20)"
        ]

        item_name = self.random.choice(FILLER_ITEM_NAMES)
        return item_name

    def fill_slot_data(self) -> dict:
        options = ["goal", "logic", "keysanity", "phantom_combat_difficulty",
                   "ph_starting_time", "ph_time_increment", "randomize_frogs"]
        slot_data = self.options.as_dict(*options)
        print(slot_data)
        return slot_data

    def write_spoiler(self, spoiler_handle):
        pass
