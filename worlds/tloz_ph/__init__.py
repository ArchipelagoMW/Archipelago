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


# Adds a consistent count of items to pool, independent of how many are from locations
def add_items_from_filler(item_pool_dict: dict, filler_item_count: int, item: str, count: int):
    if filler_item_count >= count:
        filler_item_count -= count
        item_pool_dict[item] = count
    else:
        item_pool_dict[item] = filler_item_count
        filler_item_count = 0

    return [item_pool_dict, filler_item_count]


def add_additional_spirit_gems(item_pool_dict: dict, filler_item_count: int):
    def add_gems(gem: str, filler_count: int):
        gems = 20 - item_pool_dict[gem]
        print(f"Processing {gem}: adding {gems}")
        if filler_count >= gems:
            filler_count -= gems
            item_pool_dict[gem] = 20
        return filler_count

    filler_item_count = add_gems("Power Gem", filler_item_count)
    filler_item_count = add_gems("Wisdom Gem", filler_item_count)
    filler_item_count = add_gems("Courage Gem", filler_item_count)

    return [item_pool_dict, filler_item_count]


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
        self.required_dungeons = []
        self.boss_reward_items_pool = []
        self.boss_reward_location_names = []
        self.dungeon_name_groups = {}
        self.locations_to_exclude = set()
        self.ut_locations_to_exclude = set()
        self.extra_filler_items = []
        self.excluded_dungeons = []

    def generate_early(self):
        print("GENERATING EARLY")
        self.pick_required_dungeons()
        self.restrict_non_local_items()

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        if not self.options.keysanity == "anywhere":
            self.options.non_local_items.value -= self.item_name_groups["Small Keys"]

    def create_location(self, region_name: str, location_name: str, local: bool):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
        region.locations.append(location)
        if "dungeon" in LOCATIONS_DATA[location_name]:
            self.dungeon_name_groups.setdefault(LOCATIONS_DATA[location_name]["dungeon"], set())
            self.dungeon_name_groups[LOCATIONS_DATA[location_name]["dungeon"]].add(location_name)
        # For excluding post-dungeon checks from excluded dungeons
        if "post_dungeon" in LOCATIONS_DATA[location_name]:
            self.dungeon_name_groups.setdefault(LOCATIONS_DATA[location_name]["post_dungeon"], set())
            self.dungeon_name_groups[LOCATIONS_DATA[location_name]["post_dungeon"]].add(location_name)

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
        print(f"Created Event for {event_item_name} at {region_name}")

    def location_is_active(self, location_name, location_data):
        if not location_data.get("conditional", False):
            return True
        else:
            if location_name in FROG_LOCATION_NAMES:
                return self.options.randomize_frogs != PhantomHourglassFrogRandomization.option_start_with
            if "Harrow Island" in location_name:
                return self.options.randomize_harrow
            if "Zauz's Island Triforce Crest" in location_name:
                return self.options.randomize_triforce_crest
            if "Masked Beedle" in location_name:
                return self.options.randomize_masked_beedle
            if "GOAL" in location_name:
                if location_name == "GOAL: Beat Bellumbeck" and self.options.goal == "beat_bellumbeck":
                    return True
                elif location_name == "GOAL: Triforce Door" and self.options.goal == "triforce_door":
                    return True
            return False

    def pick_required_dungeons(self):
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
        print(f"dungeons required {self.options.dungeons_required.value}")
        self.required_dungeons = implemented_dungeons[:dungeons_required]

        # Extend mcguffin list
        boss_reward_pool = ITEM_GROUPS["Vanilla Metals"]
        self.random.shuffle(boss_reward_pool)
        while self.options.dungeons_required > len(boss_reward_pool):
            boss_reward_pool.append("Additional Rare Metal")
        self.boss_reward_items_pool = boss_reward_pool[:self.options.dungeons_required]

    def create_events(self):
        # Create events for required dungeons
        if "Temple of Fire" in self.required_dungeons:
            self.create_event("tof blaaz", "_required_dungeon")
        if "Temple of Wind" in self.required_dungeons:
            self.create_event("tow cyclok", "_required_dungeon")
        if "Temple of Courage" in self.required_dungeons:
            self.create_event("toc crayk", "_required_dungeon")
        if "Ghost Ship" in self.required_dungeons:
            if self.options.ghost_ship_in_dungeon_pool == "rescue_tetra":
                self.create_event("ghost ship tetra", "_required_dungeon")
            elif self.options.ghost_ship_in_dungeon_pool == "cubus_sisters":
                self.create_event("ghost ship cubus", "_required_dungeon")
        if "Goron Temple" in self.required_dungeons:
            self.create_event("gt dongo", "_required_dungeon")
        if "Temple of Ice" in self.required_dungeons:
            self.create_event("toi gleeok", "_required_dungeon")
        if "Mutoh's Temple" in self.required_dungeons:
            self.create_event("mutoh eox", "_required_dungeon")
        self.create_event("beat required dungeons", "_has_bellum_requirement")
        # Post Dungeon Events
        self.create_event("post tof", "_beat_tof")
        self.create_event("post toc", "_beat_toc")
        self.create_event("post tow", "_beat_tow")
        self.create_event("spawn pirate ambush", "_beat_ghost_ship")
        # Farmable minigame events
        self.create_event("bannan cannon game", "_can_play_cannon_game")
        self.create_event("harrow dig", "_can_play_harrow")
        self.create_event("ds race", "_can_play_goron_race")
        # Goal
        self.create_event("goal", "_beaten_game")

    def exclude_locations_automatically(self):
        locations_to_exclude = set()

        # If non required dungeons need to be excluded, and not UT
        if self.options.exclude_non_required_dungeons and not getattr(self.multiworld, "generation_is_fake", False):
            always_include = ["Temple of the Ocean King", "Mountain Passage"]
            if self.options.ghost_ship_in_dungeon_pool == "false":
                always_include.append("Ghost Ship")
            print(f"required dungeons {self.required_dungeons}")
            excluded_dungeons = [d for d in DUNGEON_NAMES
                                 if d not in self.required_dungeons + always_include]
            print(f"excluded dungeons {excluded_dungeons}")
            self.excluded_dungeons = excluded_dungeons
            for dungeon in excluded_dungeons:
                print(f"Excluding: {self.dungeon_name_groups[dungeon]}")
                locations_to_exclude.update(self.dungeon_name_groups[dungeon])

            self.ut_locations_to_exclude = locations_to_exclude.copy()
            # Unexclude locations that have vanilla small keys/dung items cause in excluded dungeons, keys are vanilla
            for location in locations_to_exclude.copy():
                if ("Small Key" in LOCATIONS_DATA[location]["vanilla_item"] or
                        "Boss Key" in LOCATIONS_DATA[location]["vanilla_item"] or
                        "Crystal" in LOCATIONS_DATA[location]["vanilla_item"]):
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
        if classification == ItemClassification.filler:
            print(f"Created item {name} as {CLASSIFICATION[classification]}")
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
                print(f"{item_name} @ {loc_name} was removed from pool")
                removed_item_quantities[item_name] -= 1
                filler_item_count += 1
                continue
            if item_name == "Filler Item":
                filler_item_count += 1
                print(f"added filler item @ {loc_name}")
                continue
            if self.options.keysanity == "vanilla":
                # Place small key in vanilla location
                if "Small Key" in item_name:
                    key_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(key_item)
                    continue
            if "force_vanilla" in loc_data and loc_data["force_vanilla"]:
                print(f"Forcing {loc_name} with item {item_name}")
                forced_item = self.create_item(item_name)
                self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                continue
            if 'dungeon' in ITEMS_DATA[item_name]:
                # if dungeon is excluded, place keys in vanilla locations
                dung = item_name.rsplit('(', 1)[1][:-1]
                if self.options.exclude_non_required_dungeons and dung in self.excluded_dungeons:
                    print(f"Forcing {loc_name} with item {item_name} because excluded dungeon")
                    forced_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                    continue
            if item_name in FROG_NAMES:
                if self.options.randomize_frogs == "vanilla":
                    forced_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                    continue
            if item_name == "Rare Metal":  # Change rare metals to filler items for unrequired dungeons
                if boss_reward_item_count <= 0:
                    filler_item_count += 1
                    print(f"added filler item @ {loc_name}")
                    continue
                item_name = self.boss_reward_items_pool[boss_reward_item_count - 1]
                boss_reward_item_count -= 1
            if item_name == "Triforce Crest" and not self.options.randomize_triforce_crest:
                filler_item_count += 1
                print(f"added filler item @ {loc_name}")
                continue
            if (item_name in ["Treasure", "Ship Part", "Nothing!", "Potion", "Red Potion", "Purple Potion",
                              "Yellow Potion", "Power Gem", "Wisdom Gem", "Courage Gem", "Heart Container"]
                    or "Treasure Map" in item_name):
                filler_item_count += 1
                print(f"added filler item @ {loc_name}")
                continue

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # Fill filler count with consistent amounts of items, when filler count is empty it won't add any more items
        # so add progression items first
        print(f"Finished making item dict from locations, filler count {filler_item_count}")
        add_items = [("Wisdom Gem", 20), ("Power Gem", 20), ("Courage Gem", 20), ("Heart Container", 13)]
        for i, count in add_items:
            item_pool_dict, filler_item_count = add_items_from_filler(item_pool_dict, filler_item_count, i, count)
        # Add ships if enough room in filler pool
        if filler_item_count >= 8:
            for i in SHIPS[1:]:
                item_pool_dict[i] = 1
            filler_item_count -= 8

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

        self.filter_confined_dungeon_items_from_pool(items)
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
        print(f"Excluded locations: {len(self.locations_to_exclude)}, filler items: {filler_count}, "
              f"extra items {extra_item_count}, eligible items: {len(extra_items_list)}")
        if extra_item_count > 0:
            self.random.shuffle(extra_items_list)
            self.extra_filler_items = extra_items_list[:extra_item_count]

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        self.pre_fill_boss_rewards()
        self.pre_fill_dungeon_items()

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
        print(f"Filtered pre fill items {self.pre_fill_items}")

    def pre_fill_boss_rewards(self):
        boss_reward_location_names = [DUNGEON_TO_BOSS_ITEM_LOCATION[dung_name] for dung_name in self.required_dungeons]
        if "_gs" in boss_reward_location_names:  # Ghost ship can have variable dungeon reward location
            boss_reward_location_names.remove("_gs")
            boss_reward_location_names.append(
                GHOST_SHIP_BOSS_ITEM_LOCATION[self.options.ghost_ship_in_dungeon_pool.value])
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
        print(f"Removing items {boss_reward_items}")
        print(f"Filling locations {boss_reward_locations}")
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
            print(f"Removing items {confined_dungeon_items}")
            print(f"Filling locations {dungeon_locations}")
            fill_restrictive(self.multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                             single_player_placement=True, lock=True, allow_excluded=True)

    def get_filler_item_name(self) -> str:
        filler_item_names = [
            "Blue Rupee (5)",
            "Red Rupee (20)",
            "Rupoor (-10)"
        ]
        filler_item_names += ITEM_GROUPS["Treasure Items"]
        filler_item_names += ITEM_GROUPS["Ammo Refills"]

        item_name = self.random.choice(filler_item_names)
        return item_name

    def fill_slot_data(self) -> dict:
        options = ["goal", "dungeons_required", "bellum_access",
                   "ghost_ship_in_dungeon_pool", "exclude_non_required_dungeons",
                   "logic", "phantom_combat_difficulty", "boat_requires_sea_chart",
                   "keysanity", "randomize_frogs", "randomize_triforce_crest", "randomize_harrow",
                   "randomize_masked_beedle",
                   "fog_settings",
                   "dungeon_hints", "shop_hints", "spirit_island_hints",
                   "ph_starting_time", "ph_time_increment",
                   "death_link"]
        slot_data = self.options.as_dict(*options)
        slot_data["excluded_dungeons"] = self.excluded_dungeons
        slot_data["locations_to_exclude"] = self.ut_locations_to_exclude
        slot_data["boss_rewards"] = self.boss_reward_items_pool
        slot_data["required_dungeon_locations"] = self.boss_reward_location_names
        print(f"Slot Data: {slot_data}")
        return slot_data

    def write_spoiler(self, spoiler_handle):
        spoiler_handle.write(f"\n\nRequired Dungeons ({self.multiworld.player_name[self.player]}):\n")
        for dung in self.required_dungeons:
            spoiler_handle.write(f"\t- {dung}\n")

    # UT stuff
    def interpret_slot_data(self, slot_data: dict[str, any]) -> None:
        # Excluded dungeons depend on seed
        print(f"UT Excluding: {slot_data["locations_to_exclude"]}")
        for location in slot_data["locations_to_exclude"]:
            self.multiworld.get_location(location, self.player).progress_type = LocationProgressType.EXCLUDED

