import math
import os
import threading
from dataclasses import fields
from typing import ClassVar

import yaml

import Options
import settings
from BaseClasses import Tutorial, Item, ItemClassification, MultiWorld
from Utils import visualize_regions, local_path
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths
from worlds.generic.Rules import add_item_rule, add_rule
from Options import OptionGroup

# Relative Imports
from .Items import ITEM_TABLE, LMItem, get_item_names_per_category, filler_items, ALL_ITEMS_TABLE, BOO_ITEM_TABLE
from .Locations import *
from . import LuigiOptions
from .Hints import get_hints_by_option, ALWAYS_HINT, PORTRAIT_HINTS
from .Presets import lm_options_presets
from .Regions import *
from . import Rules


def run_client(*args):
    print("Running LM Client")
    from .LMClient import main  # lazy import
    launch_subprocess(main, name="LuigiMansionClient", args=args)


components.append(
    Component("LM Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".aplm"),
              icon="archiboolego")
)

icon_paths["archiboolego"] = f"ap:{__name__}/data/archiboolego.png"

CLIENT_VERSION = "0.4.1"

class LuigisMansionSettings(settings.Group):
    class ISOFile(settings.UserFilePath):
        """
        Locate your Luigi's Mansion ISO
        """
        description = "Luigi's Mansion (NTSC-U) ISO"
        copy_to = "Luigi's Mansion (NTSC-U).iso"
        md5s = ["6e3d9ae0ed2fbd2f77fa1ca09a60c494"]

    iso_file: ISOFile = ISOFile(ISOFile.copy_to)


class LMWeb(WebWorld):
    theme = "stone"
    options_presets = lm_options_presets
    option_groups = [
        OptionGroup("Extra Locations", [
            LuigiOptions.Furnisanity,
            LuigiOptions.Toadsanity,
            LuigiOptions.GoldMice,
            LuigiOptions.Boosanity,
            LuigiOptions.Portrification,
            LuigiOptions.SpeedySpirits,
            LuigiOptions.Lightsanity,
            LuigiOptions.Walksanity
        ]),
        OptionGroup("Access Options", [
            LuigiOptions.RankRequirement,
            LuigiOptions.MarioItems,
            LuigiOptions.BooGates,
            LuigiOptions.WashroomBooCount,
            LuigiOptions.BalconyBooCount,
            LuigiOptions.FinalBooCount,
            LuigiOptions.Enemizer,
            LuigiOptions.DoorRando,
            LuigiOptions.RandomSpawn,
            LuigiOptions.EarlyFirstKey,
        ]),
        OptionGroup("QOL Changes", [
            LuigiOptions.TrapLink,
            LuigiOptions.LuigiFearAnim,
            LuigiOptions.PickupAnim,
            LuigiOptions.LuigiWalkSpeed,
            LuigiOptions.LuigiMaxHealth,
            LuigiOptions.BetterVacuum,
            LuigiOptions.KingBooHealth,
            LuigiOptions.StartWithBooRadar,
            LuigiOptions.StartHiddenMansion,
            LuigiOptions.HintDistribution,
            LuigiOptions.PortraitHints,
            LuigiOptions.BooHealthOption,
            LuigiOptions.BooHealthValue,
            LuigiOptions.BooSpeed,
            LuigiOptions.BooEscapeTime,
            LuigiOptions.BooAnger,
            LuigiOptions.ExtraBooSpots,
        ]),
        OptionGroup("Filler Weights", [
            LuigiOptions.BundleWeight,
            LuigiOptions.CoinWeight,
            LuigiOptions.BillWeight,
            LuigiOptions.BarsWeight,
            LuigiOptions.GemsWeight,
            LuigiOptions.PoisonTrapWeight,
            LuigiOptions.BombWeight,
            LuigiOptions.IceTrapWeight,
            LuigiOptions.BananaTrapWeight,
            LuigiOptions.PossTrapWeight,
            LuigiOptions.BonkTrapWeight,
            LuigiOptions.GhostTrapWeight,
            LuigiOptions.NothingWeight,
            LuigiOptions.HeartWeight,
        ]),
        OptionGroup("Cosmetics", [
            LuigiOptions.RandomMusic,
            LuigiOptions.DoorModelRando,
            LuigiOptions.ChestTypes,
            LuigiOptions.TrapChestType,
        ])
    ]

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Luigi's Mansion randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["BootsinSoots"],
        )
    ]


class LMWorld(World):
    """
    Luigi's Mansion is an adventure game starring everyone's favorite plumber brother, Luigi.
    Luigi has won a strange mansion but upon arriving, he discovers it's full of ghosts, with his brother inside!
    Armed with the mysterious Poltergust 3000, Luigi will need to overcome his fears to kick the ghosts out
    before he can move in and save Mario!
    """

    game: ClassVar[str] = "Luigi's Mansion"
    options_dataclass = LuigiOptions.LMOptions
    options: LuigiOptions.LMOptions

    topology_present = True
    item_name_to_id: ClassVar[dict[str, int]] = {
        name: LMItem.get_apid(data.code) for name, data in ALL_ITEMS_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: LMLocation.get_apid(data.code) for name, data in ALL_LOCATION_TABLE.items() if data.code is not None
    }
    settings: LuigisMansionSettings
    item_name_groups = get_item_names_per_category()
    required_client_version = (0, 6, 0)
    web = LMWeb()

    using_ut: bool # so we can check if we're using UT only once
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml


    def __init__(self, *args, **kwargs):
        self.itempool: list[LMItem] = []
        self.pre_fill_items: list[LMItem] = []
        super(LMWorld, self).__init__(*args, **kwargs)
        self.ghost_affected_regions: dict[str, str] = GHOST_TO_ROOM
        self.open_doors: dict[int, int] = vanilla_door_state
        self.origin_region_name: str = "Foyer"
        self.finished_hints = threading.Event()
        self.finished_boo_scaling = threading.Event()
        self.boo_spheres: dict[str, int] = {}
        self.hints: dict[str, dict[str, str]] = {}

    def interpret_slot_data(self, slot_data):
        # There are more clever ways to do this, but all would require much larger changes
        return slot_data  # Tell UT that we have logic to fix

    def _set_optional_locations(self):

        # Set the flags for progression location by checking player's settings
        if self.options.toadsanity:
            for location, data in TOAD_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if region.name in GHOST_TO_ROOM.keys():
                    # if fire, require water
                    if self.ghost_affected_regions[region.name] == "Fire":
                        add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                    # if water, require ice
                    elif self.ghost_affected_regions[region.name] == "Water":
                        add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                    # if ice, require fire
                    elif self.ghost_affected_regions[region.name] == "Ice":
                        add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                    else:
                        pass
                region.locations.append(entry)
        if "Full" in self.options.furnisanity.value:
            for location, data in FURNITURE_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if len(entry.access) != 0:
                    for item in entry.access:
                        if item == "Fire Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                        elif item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                        elif item == "Ice Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                        else:
                            add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
                region.locations.append(entry)
        else:
            LOCATION_DICT = {}
            for group in self.options.furnisanity.value:
                match group:
                    case "Ceiling":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **CEILING_LOCATION_TABLE
                        }
                    case "Decor":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **DECOR_LOCATION_TABLE
                        }
                    case "Hangables":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **HANGABLES_LOCATION_TABLE
                        }
                    case "Seating":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **SEATING_LOCATION_TABLE
                        }
                    case "Candles":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **CANDLES_LOCATION_TABLE
                        }
                    case "Surfaces":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **SURFACES_LOCATION_TABLE
                        }
                    case "Storage":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **STORAGE_LOCATION_TABLE
                        }
                    case "Drawers":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **DRAWERS_LOCATION_TABLE
                        }
                    case "Treasures":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **TREASURES_LOCATION_TABLE
                        }
                    case "Plants":
                        LOCATION_DICT = {
                            **LOCATION_DICT,
                            **PLANT_LOCATION_TABLE
                        }
            for location, data in LOCATION_DICT.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if len(entry.access) != 0:
                    for item in entry.access:
                        if item == "Fire Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                        elif item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                        elif item == "Ice Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                        else:
                            add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
                region.locations.append(entry)
        if self.options.gold_mice:
            for location, data in GOLD_MICE_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Blackout", self.player), "and")
                region.locations.append(entry)
        if self.options.speedy_spirits:
            for location, data in SPEEDY_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Blackout", self.player), "and")
                region.locations.append(entry)
        if self.options.portrification:
            for location, data in PORTRAIT_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if entry.code == 624 and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if entry.code == 627:
                    add_rule(entry,
                             lambda state: state.has_group("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                if len(entry.access) != 0:
                    for item in entry.access:
                        if item == "Fire Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                        elif item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                        elif item == "Ice Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                        else:
                            add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
                if region.name in GHOST_TO_ROOM.keys() and location != "Uncle Grimmly, Hermit of the Darkness":
                    # if fire, require water
                    if self.ghost_affected_regions[region.name] == "Fire":
                        add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                    # if water, require ice
                    elif self.ghost_affected_regions[region.name] == "Water":
                        add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                    # if ice, require fire
                    elif self.ghost_affected_regions[region.name] == "Ice":
                        add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                    else:
                        pass
                region.locations.append(entry)
        if self.options.lightsanity:
            for location, data in LIGHT_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if entry.code == 741 and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if entry.code == 745:
                    add_rule(entry,
                             lambda state: state.has_group("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                elif entry.code == 772:
                    add_rule(entry, lambda state: state.can_reach_location("Nursery Clear Chest", self.player))
                elif entry.code in [773]:
                    add_rule(entry, lambda state: state.can_reach_location("Graveyard Clear Chest", self.player))
                elif entry.code in [778, 782, 784, 789, 790, 851]:
                    add_rule(entry, lambda state: state.can_reach_location("Balcony Clear Chest", self.player))
                elif entry.code == 757 and self.options.enemizer.value != 2:
                    add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                if len(entry.access) != 0:
                    for item in entry.access:
                        if item == "Fire Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                        elif item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                        elif item == "Ice Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                        else:
                            add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
                if region.name in GHOST_TO_ROOM.keys():
                    # if fire, require water
                    if self.ghost_affected_regions[region.name] == "Fire":
                        add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                    # if water, require ice
                    elif self.ghost_affected_regions[region.name] == "Water":
                        add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                    # if ice, require fire
                    elif self.ghost_affected_regions[region.name] == "Ice":
                        add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                    else:
                        pass
                region.locations.append(entry)
        if self.options.walksanity:
            for location, data in WALK_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if len(entry.access) != 0:
                    for item in entry.access:
                        if item == "Fire Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                        elif item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                        elif item == "Ice Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                        else:
                            add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
                region.locations.append(entry)
        if self.options.boosanity:
            for location, data in ROOM_BOO_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if self.options.boo_gates == 1 and self.options.boo_radar != 2:
                    add_rule(entry, lambda state: state.has("Boo Radar", self.player), "and")
                if entry.code == 675 and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if data.code == 674 and self.open_doors.get(27) == 0:
                    add_rule(entry, lambda state: state.has("Nursery Key", self.player), "and")
                if entry.code == 679:
                    add_rule(entry,
                             lambda state: state.has_group("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                if len(entry.access) != 0:
                    for item in entry.access:
                        if item == "Fire Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                        elif item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                        elif item == "Ice Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                        else:
                            add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
                if region.name in GHOST_TO_ROOM.keys():
                    # if fire, require water
                    if self.ghost_affected_regions[region.name] == "Fire":
                        add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                    # if water, require ice
                    elif self.ghost_affected_regions[region.name] == "Water":
                        add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                    # if ice, require fire
                    elif self.ghost_affected_regions[region.name] == "Ice":
                        add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                    else:
                        pass
                region.locations.append(entry)
            for location, data in BOOLOSSUS_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Ice Element Medal", self.player), "and")
                region.locations.append(entry)
        else:
            for location, data in ROOM_BOO_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                entry.address = None
                entry.place_locked_item(Item("Boo", ItemClassification.progression, None, self.player))
                if self.options.boo_gates == 1 and self.options.boo_radar != 2:
                    add_rule(entry, lambda state: state.has("Boo Radar", self.player), "and")
                if data.code == 675 and self.open_doors.get(28) == 0:
                    add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
                if data.code == 674 and self.open_doors.get(27) == 0:
                    add_rule(entry, lambda state: state.has("Nursery Key", self.player), "and")
                if data.code == 679:
                    add_rule(entry,
                             lambda state: state.has_group("Mario Item", self.player, self.options.mario_items.value),
                             "and")
                entry.code = None
                if len(entry.access) != 0:
                    for item in entry.access:
                        if item == "Fire Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                        elif item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                        elif item == "Ice Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                        else:
                            add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
                if region.name in GHOST_TO_ROOM.keys():
                    # if fire, require water
                    if self.ghost_affected_regions[region.name] == "Fire":
                        add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                    # if water, require ice
                    elif self.ghost_affected_regions[region.name] == "Water":
                        add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                    # if ice, require fire
                    elif self.ghost_affected_regions[region.name] == "Ice":
                        add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                    else:
                        pass
                region.locations.append(entry)
            for location, data in BOOLOSSUS_LOCATION_TABLE.items():
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                entry.address = None
                entry.code = None
                entry.place_locked_item(Item("Boo", ItemClassification.progression, None, self.player))
                add_rule(entry, lambda state: state.has("Ice Element Medal", self.player), "and")
                region.locations.append(entry)

        rankcalc = 0
        if self.options.rank_requirement < 3:
            rankcalc = 1
        elif self.options.rank_requirement == 3:
            rankcalc = 2
        elif 3 < self.options.rank_requirement < 5:
            rankcalc = 3
        elif self.options.rank_requirement == 6:
            rankcalc = 4
        else:
            rankcalc = 5
        loc = self.multiworld.get_location("King Boo", self.player)
        add_rule(loc, lambda state: state.has("Gold Diamond", self.player, rankcalc), "and")

    def generate_early(self):
        if (self.options.boosanity == 1 or self.options.boo_gates == 1) and self.options.boo_radar == 2:
            raise Options.OptionError(f"When Boo Radar is excluded, neither Boosanity nor Boo Gates can be active "
                                      f"This error was found in {self.player_name}'s Luigi's Mansion world. "
                                      f"Their YAML must be fixed")
        
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Luigi's Mansion" in self.multiworld.re_gen_passthrough:
                self.using_ut = True
                passthrough = self.multiworld.re_gen_passthrough["Luigi's Mansion"]
                self.options.rank_requirement.value = passthrough["rank requirement"]
                self.options.good_vacuum.value = passthrough["better vacuum"]
                self.options.door_rando.value = passthrough["door rando"]
                self.options.toadsanity.value = passthrough["toadsanity"]
                self.options.gold_mice.value = passthrough["gold_mice"]
                self.options.furnisanity.value = passthrough["furnisanity"]
                self.options.boosanity.value = passthrough["boosanity"]
                self.options.portrification.value = passthrough["portrait ghosts"]
                self.options.speedy_spirits.value = passthrough["speedy spirits"]
                self.options.lightsanity.value = passthrough["lightsanity"]
                self.options.walksanity.value = passthrough["walksanity"]
                self.options.mario_items.value = passthrough["clairvoya requirement"]
                self.options.boo_gates.value = passthrough["boo gates"]
                self.options.washroom_boo_count.value = passthrough["washroom boo count"]
                self.options.balcony_boo_count.value = passthrough["balcony boo count"]
                self.options.final_boo_count.value = passthrough["final boo count"]
                self.options.enemizer.value = passthrough["enemizer"]
                self.options.luigi_max_health.value = passthrough["luigi max health"]
            else:
                self.using_ut = False
        else:
            self.using_ut = False

        if self.using_ut:
            # We know we're in second gen
            self.origin_region_name = passthrough["spawn_region"]  # this should be the same region from slot data
        elif self.options.random_spawn.value > 0:
            self.origin_region_name = self.random.choice(list(spawn_locations.keys()))

        if self.using_ut:
            # We know we're in second gen
            self.ghost_affected_regions = passthrough["ghost elements"]  # this should be the same list from slot data
        elif self.options.enemizer == 1:
            set_ghost_type(self, self.ghost_affected_regions)
        elif self.options.enemizer == 2:
            for key in self.ghost_affected_regions.keys():
                self.ghost_affected_regions[key] = "No Element"

        if self.using_ut:
            # We know we're in second gen
            self.open_doors = passthrough["door rando list"]  # this should be the same list from slot data
            self.open_doors = {int(k): v for k, v in self.open_doors.items()}
        elif self.options.door_rando == 1:
            k = list(self.open_doors.keys())
            v = list(self.open_doors.values())
            self.open_doors = dict(zip(self.random.sample(k, k=len(self.open_doors)),
                                       v))

        # If player wants to start with boo radar or good vacuum
        if self.options.boo_radar == 0:
            self.options.start_inventory.value["Boo Radar"] = (
                    self.options.start_inventory.value.get("Boo Radar", 0) + 1
            )

        if self.options.good_vacuum == 0:
            self.options.start_inventory.value["Poltergust 4000"] = (
                    self.options.start_inventory.value.get("Poltergust 4000", 0) + 1
            )

        if self.options.boosanity == 0 and self.options.balcony_boo_count > 36:
            self.options.balcony_boo_count.value = 36

        if self.options.boo_gates.value == 0:
            self.options.final_boo_count.value = 0
            self.options.balcony_boo_count.value = 0
            self.options.washroom_boo_count.value = 0

    def create_regions(self):
        # Add all randomizable regions
        for region_name in REGION_LIST.values():
            if region_name in self.multiworld.regions.region_cache[self.player]:
                continue
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        # Assign each location to their region
        for location, data in BASE_LOCATION_TABLE.items():
            if location == "Luigi's Courage" or location == "E. Gadd's Gift":
                region = self.get_region(self.origin_region_name)
                entry = LMLocation(self.player, location, region, data)
                region.locations.append(entry)
            else:
                region = self.get_region(data.region)
                entry = LMLocation(self.player, location, region, data)
                if entry.type == "Freestanding":
                    add_item_rule(entry, lambda
                        item: item.player != self.player or (
                            item.player == self.player and item.type != "Money" and item.type != "Trap" and item.type != "Medal"))
                if len(entry.access) != 0:
                    for item in entry.access:
                        if item == "Fire Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                        elif item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                        elif item == "Ice Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                        else:
                            add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
                if location == "Huge Flower (Boneyard)":
                    add_rule(entry, lambda state: state.has("Progressive Flower", self.player, 3))
                if entry.code is None:
                    entry.place_locked_item(Item(entry.locked_item, ItemClassification.progression, None, self.player))
                region.locations.append(entry)
        for location, data in ENEMIZER_LOCATION_TABLE.items():
            region = self.get_region(data.region)
            entry = LMLocation(self.player, location, region, data)
            if entry.type == "Freestanding":
                add_item_rule(entry, lambda
                    item: item.player != self.player or (
                        item.player == self.player and item.type != "Money" and item.type != "Trap" and item.type != "Medal"))
            if len(entry.access) != 0:
                for item in entry.access:
                    if item == "Fire Element Medal":
                        add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                    elif item == "Water Element Medal":
                        add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                    elif item == "Ice Element Medal":
                        add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                    else:
                        add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
            if region.name in GHOST_TO_ROOM.keys():
                # if fire, require water
                if self.ghost_affected_regions[region.name] == "Fire":
                    add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                # if water, require ice
                elif self.ghost_affected_regions[region.name] == "Water":
                    add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                # if ice, require fire
                elif self.ghost_affected_regions[region.name] == "Ice":
                    add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                else:
                    pass
            region.locations.append(entry)
        for location, data in CLEAR_LOCATION_TABLE.items():
            region = self.get_region(data.region)
            entry = LMLocation(self.player, location, region, data)
            if entry.type == "Freestanding":
                add_item_rule(entry, lambda
                    item: item.player != self.player or (
                        item.player == self.player and item.type != "Money" and item.type != "Trap" and item.type != "Medal"))
            if entry.code == 5:
                add_rule(entry,
                         lambda state: state.has_group("Mario Item", self.player, self.options.mario_items.value))
            if entry.code == 25 and self.open_doors.get(28) == 0:
                add_rule(entry, lambda state: state.has("Twins Bedroom Key", self.player), "and")
            if len(entry.access) != 0:
                for item in entry.access:
                    if item == "Fire Element Medal":
                        add_rule(entry, lambda state: Rules.can_fst_fire(state, self.player), "and")
                    elif item == "Water Element Medal":
                        add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                    elif item == "Ice Element Medal":
                        add_rule(entry, lambda state: Rules.can_fst_ice(state, self.player), "and")
                    else:
                        add_rule(entry, lambda state, i=item: state.has(i, self.player), "and")
            region.locations.append(entry)
        self._set_optional_locations()
        connect_regions(self)

    def create_item(self, item: str) -> LMItem:
        set_non_progress = False

        if item in ALL_ITEMS_TABLE:
            return LMItem(item, self.player, ALL_ITEMS_TABLE[item], set_non_progress)
        raise Exception(f"Invalid item name: {item}")

    # def post_fill(self):
    #     visualize_regions(self.multiworld.get_region(self.origin_region_name, self.player), "luigiregions.puml", linetype_ortho=False)

    def create_items(self):
        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        if self.options.boosanity:
            for item, data in BOO_ITEM_TABLE.items():
                copies_to_place = 1
                copies_to_place = 0 if copies_to_place - exclude.count(item) <= 0 else 1 - exclude.count(item)
                for _ in range(copies_to_place):
                    self.itempool.append(self.create_item(item))
        if self.options.good_vacuum == 2:
            exclude += ["Poltergust 4000"]
        if self.options.boo_radar == 2:
            exclude += ["Boo Radar"]
        item_list = []
        for item, data in ITEM_TABLE.items():
            if data.doorid in self.open_doors.keys() and self.open_doors.get(data.doorid) == 1:
                exclude += [item]
            if data.code == 65:
                copies_to_place = 5
            elif data.code == 140:
                copies_to_place = 3
            else:
                copies_to_place = 1
            copies_to_place = 0 if copies_to_place - exclude.count(item) <= 0 else copies_to_place - exclude.count(item)
            for _ in range(copies_to_place):
                item_list.append(item)
                self.itempool.append(self.create_item(item))
        if self.options.early_first_key.value == 1:
            early_key = ""
            for key in spawn_locations[self.origin_region_name]["key"]:
                if key in item_list:
                    early_key = key
                    break
            if len(early_key) > 0:
                self.multiworld.local_early_items[self.player].update({early_key: 1})

        # Calculate the number of additional filler items to create to fill all locations
        n_locations = len(self.multiworld.get_unfilled_locations(self.player))
        n_items = len(self.pre_fill_items) + len(self.itempool)
        n_filler_items = n_locations - n_items

        # Add filler items to the item pool.
        for _ in range(n_filler_items):
            self.itempool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += self.itempool

    def get_filler_item_name(self) -> str:
        filler = list(filler_items.keys())
        thircoin = 0 if self.options.coin_weight.value - 10 <= 0 else self.options.coin_weight.value - 10
        twencoin = 0 if self.options.coin_weight.value - 5 <= 0 else self.options.coin_weight.value - 5
        twenbill = 0 if self.options.bill_weight.value - 5 <= 0 else self.options.bill_weight.value - 5
        morebar = 0 if self.options.bars_weight.value - 5 <= 0 else self.options.bars_weight.value - 5
        diamweight = math.ceil(self.options.gems_weight.value * 0.4)
        lheart = 0 if self.options.heart_weight.value - 5 <= 0 else self.options.heart_weight.value - 5
        filler_weights = [self.options.bundle_weight.value, self.options.gems_weight.value,  # coins & bills, sapphire
                          self.options.gems_weight.value, self.options.gems_weight.value, diamweight,
                          # emerald, ruby, diamond
                          self.options.poison_trap_weight.value, self.options.ghost_weight, self.options.nothing_weight.value,
                          self.options.heart_weight.value, lheart,  # poison mush, nothing, sm heart, l heart
                          self.options.bomb_trap_weight.value, self.options.ice_trap_weight.value,  # bomb, ice
                          self.options.banana_trap_weight.value, self.options.coin_weight.value, twencoin, thircoin,
                          # banana, 10coin, 20coin, 30coin
                          self.options.bill_weight.value, twenbill, self.options.bars_weight.value,
                          morebar, self.options.poss_trap_weight.value, self.options.bonk_trap_weight.value]  # 15bill, 25bill, 1bar, 2bar
        return self.random.choices(filler, weights=filler_weights, k=1)[0]

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Mario's Painting", self.player)

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        hint_worlds = [world for world in multiworld.get_game_worlds(cls.game)
                       if (world.options.hint_distribution.value != 5 and world.options.hint_distribution.value != 1)]
        boo_worlds = [world for world in multiworld.get_game_worlds(cls.game) if world.options.boo_health_option == 2]
        if not boo_worlds and not hint_worlds:
            return
        player_hints = {world.player for world in hint_worlds}
        if player_hints:
            get_hints_by_option(multiworld, player_hints)
        if not boo_worlds:
            return
        boo_players = {world.player for world in boo_worlds}
        def check_boo_players_done() -> None:
            done_players = set()
            for player in boo_players:
                player_world = multiworld.worlds[player]
                if len(player_world.boo_spheres.keys()) == len(ROOM_BOO_LOCATION_TABLE.keys()):
                    player_world.finished_boo_scaling.set()
                    done_players.add(player)
            boo_players.difference_update(done_players)
        for sphere_num, sphere in enumerate(multiworld.get_spheres(), 1):
            for loc in sphere:
                if loc.player in boo_players and loc.name in ROOM_BOO_LOCATION_TABLE.keys():
                    player_world = multiworld.worlds[loc.player]
                    player_world.boo_spheres.update({loc.name: sphere_num})
            check_boo_players_done()
            if not boo_players:
                return


    # Output options, locations and doors for patcher
    def generate_output(self, output_directory: str):
        # Output seed name and slot number to seed RNG in randomizer client
        output_data = {
            "Seed": self.multiworld.seed,
            "Slot": self.player,
            "Name": self.player_name,
            "Options": {},
            "Locations": {},
            "Entrances": {},
            "Room Enemies": {},
            "Hints": {},
        }

        # Output relevant options to file
        for field in fields(self.options):
            output_data["Options"][field.name] = getattr(self.options, field.name).value
            output_data["Options"]["spawn"]: str = self.origin_region_name

        output_data["Entrances"] = self.open_doors
        output_data["Room Enemies"] = self.ghost_affected_regions
        if self.options.hint_distribution != 5 and self.options.hint_distribution != 1:
            self.finished_hints.wait()
            output_data["Hints"] = self.hints
        if self.options.boo_health_option.value == 2:
            self.finished_boo_scaling.wait()

        # Output which item has been placed at each location
        locations = self.multiworld.get_locations(self.player)
        for location in locations:
            if location.address is not None or (location.name in ROOM_BOO_LOCATION_TABLE.keys()):
                if location.item:
                    itemid = 0
                    if location.item.player == self.player:
                        if location.address:
                            if location.item.type == "Door Key":
                                itemid = location.item.doorid
                        inv_reg_list = dict((v, k) for k, v in REGION_LIST.items())
                        roomid = inv_reg_list[location.parent_region.name]
                        item_info = {
                            "player": location.item.player,
                            "name": location.item.name,
                            "game": location.item.game,
                            "classification": location.item.classification.name,
                            "door_id": itemid,
                            "room_no": roomid,
                            "type": location.type,
                            "loc_enum": location.jmpentry
                        }
                        if self.options.boo_health_option.value == 2 and location.name in ROOM_BOO_LOCATION_TABLE.keys():
                                item_info.update({"boo_sphere": self.boo_spheres[location.name]})

                        output_data["Locations"][location.name] = item_info
                    else:
                        inv_reg_list = dict((v, k) for k, v in REGION_LIST.items())
                        roomid = inv_reg_list[location.parent_region.name]
                        item_info = {
                            "player": location.item.player,
                            "name": location.item.name,
                            "game": location.item.game,
                            "classification": location.item.classification.name,
                            "door_id": itemid,
                            "room_no": roomid,
                            "type": location.type,
                            "loc_enum": location.jmpentry,
                        }
                        output_data["Locations"][location.name] = item_info
                        if self.options.boo_health_option.value == 2 and location.name in ROOM_BOO_LOCATION_TABLE.keys():
                                item_info.update({"boo_sphere": self.boo_spheres[location.name]})
                else:
                    item_info = {"name": "Nothing", "game": "Luigi's Mansion", "classification": "filler"}
                output_data["Locations"][location.name] = item_info

        # Output the plando details to file
        file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.aplm")
        with open(file_path, "w") as f:
            f.write(yaml.dump(output_data, sort_keys=False))

    # TODO: UPDATE FOR LM tracker
    def fill_slot_data(self):
        return {
            "rank requirement": self.options.rank_requirement.value,
            "better vacuum": self.options.good_vacuum.value,
            "door rando": self.options.door_rando.value,
            "door rando list": self.open_doors,
            "ghost elements": self.ghost_affected_regions,
            "toadsanity": self.options.toadsanity.value,
            "gold_mice": self.options.gold_mice.value,
            "furnisanity": self.options.furnisanity.value,
            "boosanity": self.options.boosanity.value,
            "portrait ghosts": self.options.portrification.value,
            "speedy spirits": self.options.speedy_spirits.value,
            "lightsanity": self.options.lightsanity.value,
            "walksanity": self.options.walksanity.value,
            "clairvoya requirement": self.options.mario_items.value,
            "boo gates": self.options.boo_gates.value,
            "washroom boo count": self.options.washroom_boo_count.value,
            "balcony boo count": self.options.balcony_boo_count.value,
            "final boo count": self.options.final_boo_count.value,
            "enemizer": self.options.enemizer.value,
            "spawn_region": self.origin_region_name,
            "death_link": self.options.death_link.value,
            "trap_link": self.options.trap_link.value,
            "luigi max health": self.options.luigi_max_health.value,
            "pickup animation": self.options.pickup_animation.value,
            "apworld version": CLIENT_VERSION,
            "seed": self.multiworld.seed,
        }
