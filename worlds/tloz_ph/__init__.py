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
from .data.LogicPredicates import ph_has_sw_sea_chart

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
    required_client_version = (0, 5, 1)
    web = PhantomHourglassWeb()
    topology_present = True

    settings_key = "tloz_ph_options"

    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    origin_region_name = "mercay island"

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

        self.pre_fill_items: List[Item] = []

    def generate_early(self):
        pass

    def create_location(self, region_name: str, location_name: str, local: bool):
        region = self.multiworld.get_region(region_name, self.player)
        print(f"Creating Location: {location_name} with id {self.location_name_to_id[location_name]}")
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
            return False

    def create_events(self):
        pass

    def exclude_locations_automatically(self):
        locations_to_exclude = set()
        for name in locations_to_exclude:
            self.multiworld.get_location(name, self.player).progress_type = LocationProgressType.EXCLUDED

    def set_rules(self):
        create_connections(self.multiworld, self.player, self.origin_region_name, self.options)
        self.multiworld.completion_condition[self.player] = lambda state: ph_has_sw_sea_chart(state, self.player)

    def create_item(self, name: str) -> Item:
        classification = ITEMS_DATA[name]['classification']
        ap_code = self.item_name_to_id[name]
        print(f"Created item {name} from {self.item_name_to_id}")
        return Item(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        removed_item_quantities = self.options.remove_items_from_pool.value.copy()
        item_pool_dict = {}
        filler_item_count = 0
        rupee_item_count = 0
        for loc_name, loc_data in LOCATIONS_DATA.items():
            if not self.location_is_active(loc_name, loc_data):
                continue
            if "vanilla_item" not in loc_data:
                continue

            item_name = loc_data['vanilla_item']
            if item_name in removed_item_quantities and removed_item_quantities[item_name] > 0:
                # If item was put in the "remove_items_from_pool" option, replace it with a random filler item
                removed_item_quantities[item_name] -= 1
                filler_item_count += 1
                continue
            if item_name == "Filler Item":
                filler_item_count += 1
                continue

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # Add as many filler items as required
        for _ in range(filler_item_count):
            random_filler_item = self.get_filler_item_name()
            item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1

        return item_pool_dict

    def create_items(self):
        item_pool_dict = self.build_item_pool_dict()
        print(item_pool_dict)
        items = []
        for item_name, quantity in item_pool_dict.items():
            for _ in range(quantity):
                items.append(self.create_item(item_name))
        self.multiworld.itempool.extend(items)

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        pass

    def get_filler_item_name(self) -> str:
        FILLER_ITEM_NAMES = [
            "Red Rupee"
        ]

        item_name = self.random.choice(FILLER_ITEM_NAMES)
        return item_name

    def fill_slot_data(self) -> dict:
        slot_data = self.options.as_dict(*options)
        return {}

    def write_spoiler(self, spoiler_handle):
        pass


