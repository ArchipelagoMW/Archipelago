import os
import logging
import random
from math import ceil
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

logger = logging.getLogger("Client")


class PhantomHourglassWeb(WebWorld):
    theme = "grass"
    setup_en = Tutorial(
        "Phantom Hourglass Setup Guide",
        "A guide to setting up Phantom Hourglass Archipelago Randomizer on your computer.",
        "English",
        "setup.md",
        "setup/en",
        ["Carrotinator"]
    )
    faq = Tutorial(
        "Phantom Hourglass FAQ",
        "Questions you might have about the implementation, and credits",
        "English",
        "faq_and_credits.md",
        "faq/en",
        ["Carrotinator"]
    )
    tricks = Tutorial(
        "Phantom Hourglass Tricks and Skips",
        "Tricks and skips that might be required in harder logic settings, with videos when available",
        "English",
        "tricks_and_skips.md",
        "tricks_and_skips/en",
        ["Carrotinator"]
    )

    tutorials = [setup_en, faq, tricks]


# Adds a consistent count of items to pool, independent of how many are from locations
def add_items_from_filler(item_pool_dict: dict, filler_item_count: int, item: str, count: int):
    if filler_item_count >= count:
        filler_item_count -= count
        item_pool_dict[item] = count
    else:
        item_pool_dict[item] = filler_item_count
        filler_item_count = 0

    return [item_pool_dict, filler_item_count]


def add_spirit_gems(pack_option, add_option):
    if pack_option == 1:
        return [("Power Gem", 20), ("Wisdom Gem", 20), ("Courage Gem", 20)]
    else:
        count = ceil(20 / pack_option.value) + add_option
        return [("Power Gem Pack", count), ("Wisdom Gem Pack", count), ("Courage Gem Pack", count)]


def add_sand(starting_time, time_incr, time_logic):
    max_sand_count = ceil((5999 - starting_time) / time_incr)
    max_time = 1
    if time_logic <= 2:
        max_time = 310 // [1, 2, 4, 0.5][time_logic]
    min_sand_count = ceil(max(max_time - starting_time, 1) / time_incr)
    if min_sand_count > 20:
        print(f"Too many sand items? Adding {min_sand_count} Sands or Hours to pool")

    # Balance to limits
    sand_count = min_sand_count + 2
    if sand_count < 5:
        sand_count = 5
    if sand_count > max_sand_count:
        sand_count = max_sand_count
    # print(f"Sand count: {sand_count} total {starting_time.value + min_sand_count * time_incr.value}")
    return [("Sand of Hours", sand_count)]


def add_beedle_point_items():
    return [("Beedle Points (50)", 2), ("Beedle Points (20)", 3), ("Beedle Points (10)", 4)]


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

    glitches_item_name = "_UT_Glitched_logic"
    ut_can_gen_without_yaml = True
    location_id_to_alias: Dict[int, str]

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
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            # slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_data.items():
                opt = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))

            # Set randomized data that effects exclusions etc
            self.required_dungeons = slot_data["required_dungeons"]
            self.boss_reward_items_pool = slot_data["boss_reward_items_pool"]

        else:
            self.pick_required_dungeons()
        self.restrict_non_local_items()

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        if not self.options.keysanity == "anywhere":
            self.options.non_local_items.value -= set(ITEM_GROUPS["Small Keys"])
        self.options.non_local_items.value -= set(ITEM_GROUPS["Throwable Keys"])
        self.options.non_local_items.value -= set(self.boss_reward_items_pool)

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

    def location_is_active(self, location_name, location_data):
        if not location_data.get("conditional", False):
            return True
        else:
            if location_name in LOCATION_GROUPS["Golden Frogs"]:
                return self.options.randomize_frogs != PhantomHourglassFrogRandomization.option_start_with
            if "Harrow Island" in location_name:
                return self.options.randomize_harrow
            if "Zauz's Island Triforce Crest" == location_name:
                return self.options.randomize_triforce_crest
            if "Masked Beedle" in location_name:
                return self.options.randomize_masked_beedle
            if "Molida Archery 2000" == location_name:
                return self.options.logic in ["hard", "glitched"]
            if location_name in LOCATION_GROUPS["Rupee Dig Spots"]:
                return self.options.randomize_digs
            if location_name in LOCATION_GROUPS["Minigames"]:
                return self.options.randomize_minigames
            if location_name in LOCATION_GROUPS["Fishing Locations"]:
                return self.options.randomize_fishing
            if location_name in LOCATION_GROUPS["Salvage Locations"]:
                return self.options.randomize_salvage
            if "Beedle Membership" in location_name:
                return self.options.randomize_beedle_membership.value > 1
            if "GOAL" in location_name:
                if location_name == "GOAL: Beat Bellumbeck" and self.options.bellum_access != "win":
                    return True
                elif location_name == "GOAL: Triforce Door" and self.options.goal_requirements == "triforce_door":
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
        self.required_dungeons = implemented_dungeons[:dungeons_required]

        # Cap zauz metals at number of metals
        if self.options.goal_requirements == "complete_dungeons":
            if self.options.zauz_required_metals > dungeons_required:
                self.options.zauz_required_metals.value = dungeons_required
        elif self.options.goal_requirements == "metal_hunt":
            if self.options.zauz_required_metals > self.options.metal_hunt_total:
                self.options.zauz_required_metals.value = self.options.metal_hunt_total.value
        else:
            self.options.zauz_required_metals.value = 0

        # Cap metal hunt items
        if self.options.metal_hunt_total < self.options.metal_hunt_required:
            self.options.metal_hunt_total.value = self.options.metal_hunt_required.value

        # Extend mcguffin list
        if self.options.goal_requirements == "complete_dungeons":
            self.boss_reward_items_pool = self.pick_metals(self.options.dungeons_required)

    def pick_metals(self, count):
        metal_items = ITEM_GROUPS["Vanilla Metals"]
        extended_pool = []
        if self.options.additional_metal_names == "vanilla_only":
            extended_pool = ITEM_GROUPS["Vanilla Metals"]
        elif self.options.additional_metal_names == "additional_rare_metal":
            extended_pool = ["Additional Rare Metal"]
        elif self.options.additional_metal_names == "custom":
            metal_items = ITEM_GROUPS["Vanilla Metals"] + ITEM_GROUPS["Custom Metals"]
            extended_pool = ITEM_GROUPS["Vanilla Metals"] + ITEM_GROUPS["Custom Metals"]
        elif self.options.additional_metal_names == "custom_unique":
            metal_items = ITEM_GROUPS["Vanilla Metals"] + ITEM_GROUPS["Custom Metals"]
            extended_pool = ["Additional Rare Metal"]

        while len(metal_items) < count:
            metal_items += self.random.choice([extended_pool])

        self.random.shuffle(metal_items)
        return metal_items[:count]

    def create_events(self):
        # Create events for required dungeons
        if self.options.goal_requirements == "complete_dungeons":
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

        # If non required dungeons need to be excluded, and UT can now participate too!
        if self.options.exclude_non_required_dungeons:
            always_include = ["Temple of the Ocean King", "Mountain Passage"]
            if self.options.ghost_ship_in_dungeon_pool == "false":
                always_include.append("Ghost Ship")
            excluded_dungeons = [d for d in DUNGEON_NAMES
                                 if d not in self.required_dungeons + always_include]
            self.excluded_dungeons = excluded_dungeons
            for dungeon in excluded_dungeons:
                locations_to_exclude.update(self.dungeon_name_groups[dungeon])

            self.ut_locations_to_exclude = locations_to_exclude.copy()
            # Unexclude locations that have vanilla small keys/dung items cause in excluded dungeons, keys are vanilla
            if not getattr(self.multiworld, "generation_is_fake", False):
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
        if name == "Swordsman's Scroll" and self.options.logic == "glitched":
            classification = ItemClassification.progression
        if self.options.ph_time_logic.value > 2:
            if name in ["Sand of Hours", "Heart Container"]:
                classification = ItemClassification.useful
        if name == "Heart Container" and self.options.ph_heart_time == 0:
            classification = ItemClassification.useful
        if name == "Phantom Hourglass" and self.options.ph_time_logic.value == 5:
            classification = ItemClassification.useful

        ap_code = self.item_name_to_id[name]
        return Item(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        removed_item_quantities = self.options.remove_items_from_pool.value.copy()
        item_pool_dict = {}
        filler_item_count = 0
        boss_reward_item_count = self.options.dungeons_required
        for loc_name, loc_data in LOCATIONS_DATA.items():
            # print(f"New Location: {loc_name}")
            if not self.location_is_active(loc_name, loc_data):
                # print(f"{loc_name} is not active")
                continue
            # If no defined vanilla item, fill with filler
            if "vanilla_item" not in loc_data:
                # print(f"{loc_name} has no defined vanilla item")
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
            if self.options.keysanity == "vanilla":
                # Place small key in vanilla location
                if "Small Key" in item_name:
                    key_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(key_item)
                    continue
            if "force_vanilla" in loc_data and loc_data["force_vanilla"]:
                forced_item = self.create_item(item_name)
                self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                continue
            if 'dungeon' in ITEMS_DATA[item_name]:
                # if dungeon is excluded, place keys in vanilla locations
                dung = item_name.rsplit('(', 1)[1][:-1]
                if self.options.exclude_non_required_dungeons and dung in self.excluded_dungeons:
                    forced_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                    continue
            if item_name in ITEM_GROUPS["Golden Frog Glyphs"]:
                if self.options.randomize_frogs == "vanilla":
                    forced_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                    continue
            if item_name == "Rare Metal":  # Change rare metals to filler items for unrequired dungeons
                if boss_reward_item_count <= 0 or self.options.goal_requirements != "complete_dungeons":
                    filler_item_count += 1
                    continue
                item_name = self.boss_reward_items_pool[boss_reward_item_count - 1]
                boss_reward_item_count -= 1
            if item_name == "Triforce Crest" and not self.options.randomize_triforce_crest:
                filler_item_count += 1
                continue
            if (item_name in ["Treasure", "Ship Part", "Nothing!", "Potion", "Red Potion", "Purple Potion",
                              "Yellow Potion", "Power Gem", "Wisdom Gem", "Courage Gem", "Heart Container",
                              "Bombs (Progressive)", "Bow (Progressive)", "Bombchus (Progressive)",
                              "Sand of Hours (Boss)"]
                    or "Treasure Map" in item_name):
                filler_item_count += 1
                continue

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # Fill filler count with consistent amounts of items, when filler count is empty it won't add any more items
        # so add progression items first
        add_items = [("Bombs (Progressive)", 3), ("Bow (Progressive)", 3), ("Bombchus (Progressive)", 3)]
        add_items += [("Phantom Hourglass", 1)]
        # If metal hunt create and add metals
        if self.options.goal_requirements == "metal_hunt":
            metal_pool = {}
            for i in self.pick_metals(self.options.metal_hunt_total):
                metal_pool.setdefault(i, 0)
                metal_pool[i] += 1
            add_items += metal_pool.items()
        add_items += add_spirit_gems(self.options.spirit_gem_packs, self.options.additional_spirit_gems)

        # If salvage add treasure maps
        if self.options.randomize_salvage:
            add_items += [(i, 1) for i in ITEM_GROUPS["Treasure Maps"]]
        add_items += [("Heart Container", 13)]

        # Add sand items to pool
        add_items += add_sand(self.options.ph_starting_time, self.options.ph_time_increment, self.options.ph_time_logic)

        # Add beedle point items
        if self.options.randomize_beedle_membership.value > 0:
            add_items += [("Freebie Card", 1), ("Complimentary Card", 1)]
            if self.options.randomize_beedle_membership.value > 1:
                add_items += add_beedle_point_items()

        # add items to item pool
        for i, count in add_items:
            item_pool_dict, filler_item_count = add_items_from_filler(item_pool_dict, filler_item_count, i, count)

        # Add ships if enough room in filler pool
        if filler_item_count >= 8:
            for i in ITEM_GROUPS["Ships"][1:]:
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
            # Add sand of hours to extra filler list only if not progression
            if self.options.ph_time_logic > 2:
                if item in ["Sand of Hours", "Heart Container"]:
                    extra_items_list.extend([item] * count)
            # Add hearts if their time is zero
            if item == "Heart Container" and self.options.ph_heart_time == 0:
                extra_items_list.extend([item] * count)

        extra_item_count = len(self.locations_to_exclude) - filler_count + 20
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

    def pre_fill_boss_rewards(self):
        # Calculate dungeon reward locations
        boss_reward_location_names = [DUNGEON_TO_BOSS_ITEM_LOCATION[dung_name] for dung_name in self.required_dungeons]
        if "_gs" in boss_reward_location_names:  # Ghost ship can have variable dungeon reward location
            boss_reward_location_names.remove("_gs")
            boss_reward_location_names.append(
                GHOST_SHIP_BOSS_ITEM_LOCATION[self.options.ghost_ship_in_dungeon_pool.value])
        self.boss_reward_location_names = boss_reward_location_names

        # Pre-fill dungeon rewards
        if self.options.goal_requirements == "complete_dungeons":
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
        filler_item_names += ITEM_GROUPS["Treasure Items"]
        filler_item_names += ITEM_GROUPS["Ammo Refills"]
        if self.options.randomize_fishing:  # If fishing is enable add useless fish to filler pool cause funny :3
            filler_item_names += ["Fish: Skippyjack", "Fish: Toona"]
        if self.options.randomize_salvage:
            filler_item_names += ["Salvage Repair Kit"]
        if self.options.randomize_beedle_membership:
            filler_item_names += ["Compliment Card"]

        item_name = self.random.choice(filler_item_names)
        return item_name

    def fill_slot_data(self) -> dict:
        options = [
            # Goal
            "goal_requirements", "bellum_access",
            # Dungeons
            "dungeons_required", "ghost_ship_in_dungeon_pool", "exclude_non_required_dungeons",
            # Metal Hunt
            "metal_hunt_total", "metal_hunt_required", "zauz_required_metals",
            # Logic
            "logic", "phantom_combat_difficulty", "boat_requires_sea_chart",
            # Item Randomization
            "randomize_minigames", "randomize_digs", "randomize_fishing",
            "keysanity", "randomize_frogs", "randomize_salvage",
            "randomize_triforce_crest", "randomize_harrow",
            # Beedle randomization
            "randomize_masked_beedle", "randomize_beedle_membership",
            # World Settings
            "fog_settings", "skip_ocean_fights",
            # Spirit Packs
            "spirit_gem_packs", "additional_spirit_gems",
            # Hint settings
            "dungeon_hints", "shop_hints", "spirit_island_hints",
            # PH settings
            "ph_time_logic", "ph_starting_time", "ph_time_increment", "ph_heart_time", "ph_required",
            # Cosmetic
            "additional_metal_names",
            # Deathlink
            "death_link"
        ]
        slot_data = self.options.as_dict(*options)
        # Used to make excluded dungeons consistent for UT
        slot_data["required_dungeons"] = self.required_dungeons
        # Used to determine if reached goal in client
        slot_data[
            "required_metals"] = self.options.metal_hunt_required.value if self.options.goal_requirements == "metal_hunt" \
            else self.options.dungeons_required.value
        # Used for dungeon hints in client
        slot_data["required_dungeon_locations"] = self.boss_reward_location_names  # for dungeon hints
        slot_data["boss_reward_items_pool"] = self.boss_reward_items_pool
        return slot_data

    def write_spoiler(self, spoiler_handle):
        spoiler_handle.write(f"\n\nRequired Dungeons ({self.multiworld.player_name[self.player]}):\n")
        for dung in self.required_dungeons:
            spoiler_handle.write(f"\t- {dung}\n")

    # UT stuff
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, any]):
        return slot_data
