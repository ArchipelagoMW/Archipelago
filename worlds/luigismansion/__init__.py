import os
from dataclasses import fields
from typing import ClassVar

import yaml

import Options
import settings
from BaseClasses import Tutorial, Item, ItemClassification
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
from worlds.generic.Rules import add_item_rule
from Options import OptionGroup

# Relative Imports
from .Items import ITEM_TABLE, LMItem, get_item_names_per_category, filler_items, ALL_ITEMS_TABLE, BOO_ITEM_TABLE
from .Locations import *
from .LuigiOptions import LMOptions
from .Hints import get_hints_by_option
from .Regions import *
from . import Rules


def run_client(*args):
    print("Running LM Client")
    from .LMClient import main  # lazy import
    launch_subprocess(main, name="LuigiMansionClient", args=args)


components.append(
    Component("LM Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".aplm"))
)


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
    option_groups = [
        OptionGroup("Extra Locations", [
            LuigiOptions.Furnisanity,
            LuigiOptions.Plants,
            LuigiOptions.Toadsanity,
            LuigiOptions.Boosanity,
            LuigiOptions.Portrification,
            LuigiOptions.SpeedySpirits
        ]),
        OptionGroup("QOL Changes", [
            LuigiOptions.LuigiFearAnim,
            LuigiOptions.PickupAnim,
            LuigiOptions.LuigiWalkSpeed,
            LuigiOptions.BetterVacuum,
            LuigiOptions.StartWithBooRadar,
            LuigiOptions.StartHiddenMansion,
            LuigiOptions.RandomMusic,
            LuigiOptions.HintDistribution,
            LuigiOptions.PortraitHints,
            LuigiOptions.Deathlink
        ]),
        OptionGroup("Access Options", [
            LuigiOptions.Goal,
            LuigiOptions.RankRequirement,
            LuigiOptions.MarioItems,
            LuigiOptions.BooGates,
            LuigiOptions.WashroomBooCount,
            LuigiOptions.BalconyBooCount,
            LuigiOptions.FinalBooCount,
            LuigiOptions.Enemizer,
            LuigiOptions.DoorRando
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
    options_dataclass = LMOptions
    options: LMOptions

    topology_present = True
    item_name_to_id: ClassVar[dict[str, int]] = {
        name: LMItem.get_apid(data.code) for name, data in ALL_ITEMS_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: LMLocation.get_apid(data.code) for name, data in ALL_LOCATION_TABLE.items() if data.code is not None
    }
    settings: LuigisMansionSettings
    item_name_groups = get_item_names_per_category()
    required_client_version = (0, 5, 1)
    web = LMWeb()
    ghost_affected_regions: dict[str, str] = GHOST_TO_ROOM

    open_doors: dict[int, int] = {  # TODO maybe move to imported class
        34: 1,
        38: 0,
        43: 1,
        41: 1,
        33: 0,
        32: 1,
        31: 0,
        27: 0,
        28: 0,
        3: 0,
        1: 1,
        4: 0,
        5: 1,
        7: 0,
        11: 1,
        14: 0,
        15: 0,
        10: 1,
        17: 0,
        18: 1,
        20: 1,
        16: 0,
        74: 0,
        75: 1,
        23: 1,
        21: 0,
        25: 0,
        24: 1,
        42: 0,
        29: 0,
        30: 1,
        44: 1,
        40: 1,
        45: 1,
        48: 1,
        49: 1,
        47: 1,
        51: 0,
        63: 0,
        52: 1,
        59: 0,
        62: 0,
        55: 1,
        53: 0,
        56: 0,
        50: 1,
        65: 0,
        9: 1,
        71: 0,
        68: 0,
        67: 1,
        69: 0,
        70: 1,
        72: 0
    }

    def __init__(self, *args, **kwargs):
        self.itempool: list[LMItem] = []
        self.pre_fill_items: list[LMItem] = []
        super(LMWorld, self).__init__(*args, **kwargs)

    def _set_optional_locations(self):

        # Set the flags for progression location by checking player's settings
        if self.options.toadsanity:
            for location, data in TOAD_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
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
        if self.options.plantsanity:
            for location, data in PLANT_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                if len(entry.access) != 0:
                    # if entry.code == 70:     # Placed here for eventual Huge Flower Support
                    #    add_rule(entry,
                    #             lambda state: state.has("Progressive Flower", self.player, 4)
                    #             and Rules.can_fst_water(state, player))
                    # else:
                    for item in entry.access:
                        if item == "Water Element Medal":
                            add_rule(entry, lambda state: Rules.can_fst_water(state, self.player), "and")
                region.locations.append(entry)
        if self.options.furnisanity:
            for location, data in FURNITURE_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
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
        if self.options.speedy_spirits:
            for location, data in SPEEDY_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                add_rule(entry, lambda state: state.has("Blackout", self.player), "and")
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
        if self.options.portrification:
            for location, data in PORTRAIT_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                if entry.code == 627:
                    add_rule(entry,
                             lambda state: state.has_group("Mario Item", self.player, self.options.mario_items), "and")
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
            for location, data in BOO_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                if self.options.boo_gates == 1 and self.options.boo_radar != 2:
                    add_rule(entry, lambda state: state.has("Boo Radar", self.player), "and")
                if entry.code == 679:
                    add_rule(entry,
                             lambda state: state.has_group("Mario Item", self.player, self.options.mario_items), "and")
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
            for location, data in BOO_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                entry.address = None
                entry.code = None
                entry.place_locked_item(Item("Boo", ItemClassification.progression, None, self.player))
                if self.options.boo_gates == 1 and self.options.boo_radar != 2:
                    add_rule(entry, lambda state: state.has("Boo Radar", self.player), "and")
                if entry.code == 679:
                    add_rule(entry,
                             lambda state: state.has_group("Mario Item", self.player, self.options.mario_items), "and")
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
        if self.options.goal == 1:
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
                                      f"Please fix their YAML")

        if self.options.enemizer == 1:
            set_ghost_type(self, self.ghost_affected_regions)
        elif self.options.enemizer == 2:
            for key in self.ghost_affected_regions.keys():
                self.ghost_affected_regions[key] = "No Element"

        if self.options.door_rando == 1:
            k = list(self.open_doors.keys())
            v = list(self.open_doors.values())
            self.open_doors = dict(zip(self.random.sample(k, k=len(self.open_doors)),
                                       v))

        # If sword mode is Start with Hero's Sword, then send the player a starting sword
        if self.options.boo_radar == 0:
            self.options.start_inventory.value["Boo Radar"] = (
                    self.options.start_inventory.value.get("Boo Radar", 0) + 1
            )

        if self.options.good_vacuum == 0:
            self.options.start_inventory.value["Poltergust 4000"] = (
                    self.options.start_inventory.value.get("Poltergust 4000", 0) + 1
            )

        if self.options.boosanity == 0 and self.options.balcony_boo_count > 30:
            self.options.balcony_boo_count.value = 30

    def create_regions(self):
        # "Menu" is the required starting point
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Add all randomizable regions
        for region_name in REGION_LIST.values():
            if region_name in self.multiworld.regions.region_cache[self.player]:
                continue
            self.multiworld.regions.append(Region(region_name, self.player, self.multiworld))

        # Assign each location to their region
        for location, data in BASE_LOCATION_TABLE.items():
            region = self.multiworld.get_region(data.region, self.player)
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
            if entry.code is None:
                entry.place_locked_item(Item(entry.locked_item, ItemClassification.progression, None, self.player))
            region.locations.append(entry)
        for location, data in ENEMIZER_LOCATION_TABLE.items():
            region = self.multiworld.get_region(data.region, self.player)
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
            region.locations.append(entry)
        for location, data in CLEAR_LOCATION_TABLE.items():
            region = self.multiworld.get_region(data.region, self.player)
            entry = LMLocation(self.player, location, region, data)
            if entry.type == "Freestanding":
                add_item_rule(entry, lambda
                    item: item.player != self.player or (
                        item.player == self.player and item.type != "Money" and item.type != "Trap" and item.type != "Medal"))
            if entry.code == 5:
                add_rule(entry, lambda state: state.has_group("Mario Item", self.player, self.options.mario_items))
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
        connect_regions(self.multiworld, self.player)

    def create_item(self, item: str) -> LMItem:
        set_non_progress = False

        if item in ALL_ITEMS_TABLE:
            if item == "Gold Diamond":
                if self.options.goal == 1:
                    return LMItem(item, self.player, ITEM_TABLE[item], False)
                else:
                    return LMItem(item, self.player, ITEM_TABLE[item], True)
            else:
                return LMItem(item, self.player, ALL_ITEMS_TABLE[item], set_non_progress)
        raise Exception(f"Invalid item name: {item}")

    def post_fill(self):
        visualize_regions(self.multiworld.get_region("Menu", self.player), "luigiregions.puml", linetype_ortho=False)

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
        for item, data in ITEM_TABLE.items():
            if data.doorid in self.open_doors.keys() and self.open_doors[data.doorid] == 1:
                exclude += [item]
            if data.code == 49:
                copies_to_place = 5
            else:
                copies_to_place = 1
            copies_to_place = 0 if copies_to_place - exclude.count(item) <= 0 else copies_to_place - exclude.count(item)
            for _ in range(copies_to_place):
                self.itempool.append(self.create_item(item))
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
        filler_weights = [10, 10, 20, 10, 5, 10, 15, 15]
        return self.random.choices(filler, weights=filler_weights, k=1)[0]

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Mario's Painting", self.player)

    # Output options, locations and doors for patcher
    def generate_output(self, output_directory: str):
        # Output seed name and slot number to seed RNG in randomizer client
        output_data = {
            "Seed": self.multiworld.seed,
            "Slot": self.player,
            "Name": self.multiworld.get_player_name(self.player),
            "Options": {},
            "Locations": {},
            "Entrances": {},
            "Room Enemies": {},
            "Hints": {},
        }

        # Output relevant options to file
        for field in fields(self.options):
            output_data["Options"][field.name] = getattr(self.options, field.name).value

        output_data["Entrances"] = self.open_doors
        output_data["Room Enemies"] = self.ghost_affected_regions
        output_data["Hints"] = get_hints_by_option(self.multiworld, self.player)

        # Output which item has been placed at each location
        locations = self.multiworld.get_locations(self.player)
        for location in locations:
            if location.address is not None:
                if location.item:
                    itemid = 0
                    if location.item.player == self.player:
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
            "goal": self.options.goal.value,
            "rank requirement": self.options.rank_requirement.value,
            "better vacuum": self.options.good_vacuum.value,
            "door rando": self.options.door_rando.value,
            "toadsanity": self.options.toadsanity.value,
            "plantsanity": self.options.plantsanity.value,
            "furnisanity": self.options.furnisanity.value,
            "boosanity": self.options.boosanity.value,
            "boo gates": self.options.boo_gates.value,
            "portrait ghosts": self.options.portrification.value,
            "speedy spirits": self.options.speedy_spirits.value,
            "clairvoya requirement": self.options.mario_items.value,
            "washroom boo count": self.options.washroom_boo_count.value,
            "balcony boo count": self.options.balcony_boo_count.value,
            "final boo count": self.options.final_boo_count.value,
            "enemizer": self.options.enemizer.value,
            "death_link": self.options.deathlink
        }
