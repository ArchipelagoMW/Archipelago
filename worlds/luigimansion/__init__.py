import os
from dataclasses import fields
from itertools import count
import random
from typing import Dict, ClassVar

import yaml

from .LMGenerator import LuigisMansionRandomizer
from BaseClasses import Tutorial, Item, ItemClassification
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from .Items import ITEM_TABLE, LMItem, get_item_names_per_category, filler_items, ALL_ITEMS_TABLE
from .Locations import *
from .Options import LMOptions
from .Regions import *
from . import Rules


def run_client():
    print("Running LM Client")
    from .LMClient import main  # lazy import

    launch_subprocess(main, name="LuigiMansionClient")


components.append(
    Component("LM Client", func=run_client, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apLM"))
)


class LMWeb(WebWorld):
    theme = "stone"
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
    Luigi has won a strange mansion but on arriving, he discovers it's full of ghosts!
    Armed with the mysterious Poltergust 3000, Luigi will need to overcome his fears to kick the ghosts out
    before he can move in. Wait! Is that Mario?
    """

    game: ClassVar[str] = "Luigi's Mansion"
    options_dataclass = LMOptions
    options: LMOptions

    topology_present = True
    item_name_to_id: ClassVar[Dict[str, int]] = {
        name: LMItem.get_apid(data.code) for name, data in ALL_ITEMS_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[Dict[str, int]] = {
        name: LMLocation.get_apid(data.code) for name, data in ALL_LOCATION_TABLE.items() if data.code is not None
    }

    item_name_groups = get_item_names_per_category()
    required_client_version = (0, 5, 1)
    web = LMWeb()
    ghost_affected_regions: dict[str, str] = {
        "Wardrobe": "No Element",
        "Laundry Room": "No Element",
        "Hidden Room": "No Element", #"Ice",
        "Storage Room": "No Element",
        "Kitchen": "No Element", #"Ice",
        "1F Bathroom": "No Element",
        "Courtyard": "No Element",
        "Tea Room": "No Element",
        "2F Washroom": "No Element", #"Fire",
        "Projection Room": "No Element",
        "Safari Room": "No Element", #"Water",
        "Cellar": "No Element",
        "Roof": "No Element",
        "Sealed Room": "No Element",
        "Armory": "No Element",
        "Pipe Room": "No Element"
    }

    open_doors: dict[int, int] = {
        34: 0,
        38: 0,
        43: 1,
        41: 1,
        33: 0,
        32: 1,
        31: 0,
        27: 0,
        28: 0,
        3:  0,
        1:  1,
        4:  0,
        5:  1,
        7:  0,
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
        9:  1,
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
        if self.options.knocksanity:
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
        if self.options.portrait_ghosts:
            for location, data in PORTRAIT_LOCATION_TABLE.items():
                region = self.multiworld.get_region(data.region, self.player)
                entry = LMLocation(self.player, location, region, data)
                if entry.code == 624:
                    add_rule(entry, lambda state: state.has_group("Medal", self.player), "and")
                elif entry.code == 627:
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
                add_rule(entry, lambda state: state.has("Boo Radar", self.player), "and")
                if entry.code == 675:
                    add_rule(entry, lambda state: state.has_group("Medal", self.player), "and")
                elif entry.code == 679:
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
                add_rule(entry, lambda state: state.has("Boo Radar", self.player), "and")
                if entry.code == 675:
                    add_rule(entry, lambda state: state.has_group("Medal", self.player), "and")
                elif entry.code == 679:
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
        # if self.options.enemizer == 1:
        #     set_ghost_type(self.multiworld, self.ghost_affected_regions)

        if self.options.door_rando == 1:
            random.seed(self.multiworld.seed)
            self.open_doors = dict(zip(random.sample(self.open_doors.keys(), k=len(self.open_doors)),
                                       self.open_doors.values()))

        # If sword mode is Start with Hero's Sword, then send the player a starting sword
        if self.options.boo_radar == 1:
            self.options.start_inventory.value["Boo Radar"] = (
                    self.options.start_inventory.value.get("Boo Radar", 0) + 1
            )
        # if not self.options.knocksanity:
        #     self.multiworld.push_precollected(self.create_item("Heart Key"))

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
            if entry.code == 5:
                add_rule(entry, lambda state: state.has_group("Mario Item", self.player, self.options.mario_items))
            elif entry.code == 25:
                add_rule(entry, lambda state: state.has_group("Medal", self.player))
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
        if not self.options.boosanity:
            for _ in range(35):
                exclude += ["Boo"]
        if self.options.good_vacuum == 2:
            exclude += ["Poltergust 4000"]
        for item, data in ITEM_TABLE.items():
            if data.doorid in self.open_doors.keys() and self.open_doors[data.doorid] == 1:
                exclude += [item]
            copies_to_place = data.quantity - exclude.count(item)
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
        return self.multiworld.random.choice([item_name for item_name in filler_items])

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Mario's Painting", self.player)

    # TODO: UPDATE FOR LM
    def generate_output(self, output_directory: str):
        # Output seed name and slot number to seed RNG in randomizer client
        output_data = {
            "Seed": self.multiworld.seed,
            "Slot": self.player,
            "Name": self.multiworld.get_player_name(self.player),
            "Options": {},
            "Locations": {},
            "Entrances": {},
        }

        # Output relevant options to file
        for field in fields(self.options):
            output_data["Options"][field.name] = getattr(self.options, field.name).value

        output_data["Entrances"] = self.open_doors

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
                        item_info = {
                            "player": location.item.player,
                            "name": location.item.name,
                            "game": location.item.game,
                            "classification": location.item.classification.name,
                            "JMPentry": location.jmpentry
                        }
                        output_data["Locations"][location.name] = item_info
                else:
                    item_info = {"name": "Nothing", "game": "Luigi's Mansion", "classification": "filler"}
                output_data["Locations"][location.name] = item_info

        # # Output the mapping of entrances to exits
        # entrances = self.multiworld.get_entrances(self.player)
        # for entrance in entrances:
        #     if entrance.parent_region.name in ALL_ENTRANCES:
        #         output_data["Entrances"][entrance.parent_region.name] = entrance.connected_region.name

        # Output the plando details to file
        file_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.aplm")

        LuigisMansionRandomizer("C:\\Users\\Melon\\Desktop\\LM Tools\\lm.iso", "C:\\Users\\Melon\\Desktop\\LM Tools\\", False, output_data)

        with open(file_path, "w") as f:
            f.write(yaml.dump(output_data, sort_keys=False))

    # TODO: UPDATE FOR LM IF NEEDED
    def fill_slot_data(self):
        # return {
        #     "progression_dungeons": self.options.progression_dungeons.value,
        #     "progression_tingle_chests": self.options.progression_tingle_chests.value,
        #     "progression_dungeon_secrets": self.options.progression_dungeon_secrets.value,
        #     "progression_puzzle_secret_caves": self.options.progression_puzzle_secret_caves.value,
        #     "progression_combat_secret_caves": self.options.progression_combat_secret_caves.value,
        #     "progression_savage_labyrinth": self.options.progression_savage_labyrinth.value,
        #     "progression_great_fairies": self.options.progression_great_fairies.value,
        #     "progression_short_sidequests": self.options.progression_short_sidequests.value,
        #     "progression_long_sidequests": self.options.progression_long_sidequests.value,
        #     "progression_spoils_trading": self.options.progression_spoils_trading.value,
        #     "progression_minigames": self.options.progression_minigames.value,
        #     "progression_battlesquid": self.options.progression_battlesquid.value,
        #     "progression_free_gifts": self.options.progression_free_gifts.value,
        #     "progression_mail": self.options.progression_mail.value,
        #     "progression_platforms_rafts": self.options.progression_platforms_rafts.value,
        #     "progression_submarines": self.options.progression_submarines.value,
        #     "progression_eye_reef_chests": self.options.progression_eye_reef_chests.value,
        #     "progression_big_octos_gunboats": self.options.progression_big_octos_gunboats.value,
        #     "progression_triforce_charts": self.options.progression_triforce_charts.value,
        #     "progression_treasure_charts": self.options.progression_treasure_charts.value,
        #     "progression_expensive_purchases": self.options.progression_expensive_purchases.value,
        #     "progression_island_puzzles": self.options.progression_island_puzzles.value,
        #     "progression_misc": self.options.progression_misc.value,
        #     "randomize_mapcompass": self.options.randomize_mapcompass.value,
        #     "randomize_smallkeys": self.options.randomize_smallkeys.value,
        #     "randomize_bigkeys": self.options.randomize_bigkeys.value,
        #     "sword_mode": self.options.sword_mode.value,
        #     "required_bosses": self.options.required_bosses.value,
        #     "num_required_bosses": self.options.num_required_bosses.value,
        #     "chest_type_matches_contents": self.options.chest_type_matches_contents.value,
        #     "included_dungeons": self.options.included_dungeons.value,
        #     "excluded_dungeons": self.options.excluded_dungeons.value,
        #     # "trap_chests": self.options.trap_chests.value,
        #     "hero_mode": self.options.hero_mode.value,
        #     "logic_obscurity": self.options.logic_obscurity.value,
        #     "logic_precision": self.options.logic_precision.value,
        #     "enable_tuner_logic": self.options.enable_tuner_logic.value,
        #     "randomize_dungeon_entrances": self.options.randomize_dungeon_entrances.value,
        #     "randomize_secret_cave_entrances": self.options.randomize_secret_cave_entrances.value,
        #     "randomize_miniboss_entrances": self.options.randomize_miniboss_entrances.value,
        #     "randomize_boss_entrances": self.options.randomize_boss_entrances.value,
        #     "randomize_secret_cave_inner_entrances": self.options.randomize_secret_cave_inner_entrances.value,
        #     "randomize_fairy_fountain_entrances": self.options.randomize_fairy_fountain_entrances.value,
        #     "mix_entrances": self.options.mix_entrances.value,
        #     "randomize_enemies": self.options.randomize_enemies.value,
        #     # "randomize_music": self.options.randomize_music.value,
        #     "randomize_starting_island": self.options.randomize_starting_island.value,
        #     "randomize_charts": self.options.randomize_charts.value,
        #     # "hoho_hints": self.options.hoho_hints.value,
        #     # "fishmen_hints": self.options.fishmen_hints.value,
        #     # "korl_hints": self.options.korl_hints.value,
        #     # "num_item_hints": self.options.num_item_hints.value,
        #     # "num_location_hints": self.options.num_location_hints.value,
        #     # "num_barren_hints": self.options.num_barren_hints.value,
        #     # "num_path_hints": self.options.num_path_hints.value,
        #     # "prioritize_remote_hints": self.options.prioritize_remote_hints.value,
        #     "swift_sail": self.options.swift_sail.value,
        #     "instant_text_boxes": self.options.instant_text_boxes.value,
        #     "reveal_full_sea_chart": self.options.reveal_full_sea_chart.value,
        #     "add_shortcut_warps_between_dungeons": self.options.add_shortcut_warps_between_dungeons.value,
        #     "skip_rematch_bosses": self.options.skip_rematch_bosses.value,
        #     "remove_music": self.options.remove_music.value,
        #     "death_link": self.options.death_link.value,
        # }
        pass
