from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule
from .options import Pikmin2Options
from .items import item_data, get_classification, pikmin2_items, Pikmin2Item, buried_treasure, explorer_kit_treasure
from .locations import location_data, Pikmin2Location, vor_prefixes, aw_prefixes, pp_prefixes, ww_prefixes, cave_pikmin_types_required, caves
from BaseClasses import Region, ItemClassification, CollectionState, Entrance, Tutorial
import json
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess, icon_paths
from settings import UserFilePath, Group, UserFolderPath
from typing import ClassVar
import os

def launch_client(*args):
    from .Pikmin2Client import launch
    launch_subprocess(launch, name="Pikmin2Client", args=args)


components.append(
    Component(
        "Pikmin2Client",
        func=launch_client,
        component_type=Type.CLIENT
        # icon="Pikmin 2"
    ),
)
# icon_paths["Pikmin 2"] = "ap:worlds.pikmin2/icon.png"

def item_name_id_mapping(items):
    item_dict = {}
    modifier = 1
    for item in items:
        if (item[0] == "Brute Knuckles"):
            modifier = 501
        item_dict[item[0]] = item[2] + modifier
    return item_dict

def location_name_id_mapping(locations):
    loc_dict = {}
    count = 1
    for loc in locations:
        loc_dict[loc[0]] = count
        count += 1
    for i in range(1, 202):
        loc_dict[f"Collect {i} Treasures"] = count
        count += 1
    for i in range(1, 11):
        loc_dict[f"Collect {10 * i}% of Debt"] = count
        count += 1
    return loc_dict

def test_location(name, prefix_list):
    for prefix in prefix_list:
        if (name.startswith(prefix)):
            return True
    return False

class PikminWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Pikmin 2 for Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["chpas"]
    )]

class Pikmin2Settings(Group):
    class DolphinPath(UserFilePath):
        """
        Dolphin executable location
        """
        is_exe = True
        description = "Dolphin Executable"
    class SaveFolder(UserFolderPath):
        """
        Path to Dolphin save folder
        """
        description = "Pikmin 2 Save Folder"

    dolphin_path: DolphinPath = DolphinPath(None)
    save_folder: SaveFolder =  SaveFolder(None)

class Pikmin2World(World):
    """
    Tasked with helping pay off their employer's debt, explorers Olimar and Louie team up with Pikmin (including purple and white Pikmin) to collect treasure on a strange planet. Time ticks away on the surface, but cave systems let you take your time to let your strategy blossom.  
    """
    game = "Pikmin 2"
    options_dataclass = Pikmin2Options
    options: Pikmin2Options
    topology_present = True
    settings: ClassVar[Pikmin2Settings]
    
    item_name_to_id = item_name_id_mapping(item_data)
    location_name_to_id = location_name_id_mapping(location_data)
    web = PikminWeb()
    origin_region_name = "Valley of Repose"
    treasure_check_count = 0
    poko_check_count = 0

    def check_pokos(self, state, amt):
        pokos = 0
        for item in state.prog_items[self.player].keys(): # this should only consider each item once, which is the intention
            for i in item_data:
                if (i[0] == item):
                    pokos += i[4]
                    break
        return pokos >= amt
    
    def check_treasures(self, state, t_amt):
        treasures = 0
        for item in state.prog_items[self.player].keys():
            if (item != "Pay Off Debt" and item != "Nothing" and item != "Ultra-Spicy Spray" and item != "Ultra-Bitter Spray"):
                treasures += 1
        return treasures >= t_amt
    
    def cave_rando(self):
        cave_list = list(caves.values())
        cave_mapping = {}
        if self.options.shuffle_caves == 0: # vanilla
            for cave in cave_list:
                cave_mapping[cave] = cave
            return cave_mapping
        elif self.options.shuffle_caves == 1: # keep Dream Den
            cave_mapping["DD"] = "DD"
            cave_list.remove("DD")
        elif self.options.shuffle_caves == 2: # Wistful Wild Lock
            cave_list.remove("CoC")
            cave_list.remove("HoH")
            cave_list.remove("DD")
            shuffled_ww_caves = ["CoC", "HoH", "DD"]
            self.random.shuffle(shuffled_ww_caves)
            cave_mapping["CoC"] = shuffled_ww_caves[0]
            cave_mapping["HoH"] = shuffled_ww_caves[1]
            cave_mapping["DD"] = shuffled_ww_caves[2]

        shuffled_caves = cave_list[:] # copy for shuffling
        self.random.shuffle(shuffled_caves)
        for cave_index in range(0, len(cave_list)):
            cave_mapping[cave_list[cave_index]] = shuffled_caves[cave_index]
        return cave_mapping

    def onion_rando(self):
        vanilla = {"VoR": "red", "AW": "blue", "PP": "yellow"}
        if (self.options.onion_shuffle == 0):
            return vanilla
        while True:
            onions = ["red", "yellow", "blue"]
            self.random.shuffle(onions)
            onion_mapping = {}
            onion_mapping["VoR"] = onions[0]
            onion_mapping["AW"] = onions[1]
            onion_mapping["PP"] = onions[2]
            if (self.options.onion_shuffle != 2 or (self.options.onion_shuffle == 2 and onion_mapping != vanilla)):
                break
        if (self.options.onion_shuffle == 3):
            onion_mapping["AW"] = "none"
            onion_mapping["PP"] = "none"
        return onion_mapping

    def sublevel_rando(self):
        cave_lengths = {"EC": 2, "SC": 9, "FC": 8, "HoB": 5, "WFG": 5, "BK": 7, "SH": 7, "CoS": 5, "GK": 6, "SR": 7, "SMGC": 5, "CoC": 10, "HoH": 15, "DD": 14}
        sublevel_mapping = {}
        for k in cave_lengths.keys():
            pattern = [i for i in range(0, cave_lengths[k])]
            if (self.options.sublevel_shuffle != 0):
                self.random.shuffle(pattern)
            sublevel_mapping[k] = pattern
        return sublevel_mapping
    
    def create_regions(self):
        self.cave_mapping = self.cave_rando() # {vanilla cave: what is now there}
        # regenerate prefix lists after cave rando
        self.vor_prefixes_rando = ["VoR"]
        self.aw_prefixes_rando = ["AW"]
        self.pp_prefixes_rando = ["PP"]
        self.ww_prefixes_rando = ["WW"]
        for cave in self.cave_mapping.keys():
            if (cave in vor_prefixes):
                self.vor_prefixes_rando.append(self.cave_mapping[cave])
            if (cave in aw_prefixes):
                self.aw_prefixes_rando.append(self.cave_mapping[cave])
            if (cave in pp_prefixes):
                self.pp_prefixes_rando.append(self.cave_mapping[cave])
            if (cave in ww_prefixes):
                self.ww_prefixes_rando.append(self.cave_mapping[cave])
        valley_of_repose_region = Region("Valley of Repose", self.player, self.multiworld)
        valley_of_repose_locations = {name: id for name, id in self.location_name_to_id.items() if test_location(name, self.vor_prefixes_rando)}
        valley_of_repose_region.add_locations(valley_of_repose_locations, Pikmin2Location)
        self.multiworld.regions.append(valley_of_repose_region)
        awakening_wood_region = Region("Awakening Wood", self.player, self.multiworld)
        awakening_wood_locations = {name: id for name, id in self.location_name_to_id.items() if test_location(name, self.aw_prefixes_rando)}
        awakening_wood_region.add_locations(awakening_wood_locations, Pikmin2Location)
        self.multiworld.regions.append(awakening_wood_region)
        perplexing_pool_region = Region("Perplexing Pool", self.player, self.multiworld)
        perplexing_pool_locations = {name: id for name, id in self.location_name_to_id.items() if test_location(name, self.pp_prefixes_rando)}
        perplexing_pool_region.add_locations(perplexing_pool_locations, Pikmin2Location)
        self.multiworld.regions.append(perplexing_pool_region)
        wistful_wild_region = Region("Wistful Wild", self.player, self.multiworld)
        wistful_wild_locations = {name: id for name, id in self.location_name_to_id.items() if test_location(name, self.ww_prefixes_rando)}
        wistful_wild_region.add_locations(wistful_wild_locations, Pikmin2Location)
        pay_debt_region = Region("Pay Debt", self.player, self.multiworld)
        pay_debt_region.locations.append(Pikmin2Location(self.player, "Pay Off Debt", None, pay_debt_region))
        boss_region = wistful_wild_region # for collect louie
        if ("DD" in self.vor_prefixes_rando):
            boss_region = valley_of_repose_region
        if ("DD" in self.aw_prefixes_rando):
            boss_region = awakening_wood_region
        if ("DD" in self.pp_prefixes_rando):
            boss_region = perplexing_pool_region
        if (self.options.win_condition == 0):
            boss_region.locations.append(Pikmin2Location(self.player, "Beat Titan Dweevil", None, boss_region))
        elif (self.options.win_condition == 1):
            victory_region = Region("Victory Region", self.player, self.multiworld)
            victory_region.locations.append(Pikmin2Location(self.player, "Reach Poko Count", None, victory_region))
            self.multiworld.regions.append(victory_region)
        elif (self.options.win_condition == 2):
            victory_region = Region("Victory Region", self.player, self.multiworld)
            victory_region.locations.append(Pikmin2Location(self.player, "Reach Treasure Count", None, victory_region))
            self.multiworld.regions.append(victory_region)
        self.multiworld.regions.append(wistful_wild_region)
        valley_of_repose_region.connect(awakening_wood_region)
        valley_of_repose_region.connect(perplexing_pool_region)
        awakening_wood_region.connect(valley_of_repose_region)
        awakening_wood_region.connect(perplexing_pool_region)
        perplexing_pool_region.connect(awakening_wood_region)
        perplexing_pool_region.connect(valley_of_repose_region)
        valley_of_repose_region.connect(pay_debt_region)
        awakening_wood_region.connect(pay_debt_region)
        perplexing_pool_region.connect(pay_debt_region)
        pay_debt_region.connect(wistful_wild_region)
        if (self.options.win_condition == 1 or self.options.win_condition == 2):
            valley_of_repose_region.connect(victory_region)
            awakening_wood_region.connect(victory_region)
            perplexing_pool_region.connect(victory_region)
            wistful_wild_region.connect(victory_region)
        if (self.options.treasure_collection_checks != 0):
            treasure_checks_region = Region("Treasure Checks", self.player, self.multiworld)
            treasure_checks_locations = {}
            for i in range(self.options.treasure_collection_start_value, self.options.treasure_collection_end_value + 1, self.options.treasure_collection_interval):
                treasure_checks_locations[f"Collect {i} Treasures"] = self.location_name_to_id[f"Collect {i} Treasures"]
                self.treasure_check_count += 1
            treasure_checks_region.add_locations(treasure_checks_locations, Pikmin2Location)
            self.multiworld.regions.append(treasure_checks_region)
            valley_of_repose_region.connect(treasure_checks_region)
            awakening_wood_region.connect(treasure_checks_region)
            perplexing_pool_region.connect(treasure_checks_region)
            wistful_wild_region.connect(treasure_checks_region)
        if (self.options.poko_collection_checks != 0):
            poko_checks_region = Region("Poko Checks", self.player, self.multiworld)
            poko_checks_locations = {name: id for name, id in self.location_name_to_id.items() if name.startswith("Collect") and name.endswith("Debt")}
            poko_checks_region.add_locations(poko_checks_locations, Pikmin2Location)
            self.multiworld.regions.append(poko_checks_region)
            valley_of_repose_region.connect(poko_checks_region)
            awakening_wood_region.connect(poko_checks_region)
            perplexing_pool_region.connect(poko_checks_region)
            wistful_wild_region.connect(poko_checks_region)
            self.poko_check_count = 10
        self.onion_mapping = self.onion_rando() # {location: onion}
        self.sublevel_mapping = self.sublevel_rando()
        self.starting_type = self.onion_mapping["VoR"] 

    def create_item(self, item):
        return Pikmin2Item(item, get_classification(item), self.item_name_to_id[item], self.player)
    
    def create_event(self, event):
        return Pikmin2Item(event, ItemClassification.progression, None, self.player)
    
    def create_items(self):
        num_items_to_remove = 0
        num_items = 196
        if (self.options.onion_shuffle == 3):
            num_items_to_remove += 2
        if (self.options.cave_keys == 1):
            num_items_to_remove += 14
        if (self.options.weapons_in_pool == 1):
            num_items_to_remove += 4
        extra_spots = 0
        if (self.options.treasure_collection_checks != 0):
            for _ in range(self.options.treasure_collection_start_value, self.options.treasure_collection_end_value + 1, self.options.treasure_collection_interval):
                extra_spots += 1
        if (self.options.poko_collection_checks != 0):
            extra_spots += 10
        num_items += num_items_to_remove
        num_items_to_remove -= extra_spots
        num_items_to_remove = max(0, num_items_to_remove)
        removable_items = ["Flame of Tomorrow", "Leviathan Feather", "Comfort Cookie", "Compelling Cookie", "Conifer Spire", "Bug Bait", "King of Sweets", "Cupid's Grenade", "Science Project", "Impenetrable Cookie", "Imperative Cookie", "Diet Doomer", "Pale Passion", "Infernal Vegetable", "Anti-hiccup Fungus", "Toxic Toadstool", "Onion Replica", "Master's Instrument", "Abstract Masterpiece", "Salivatrix"]
        count = 0
        for item in map(self.create_item, pikmin2_items):
            self.multiworld.itempool.append(item)

            if (item.name == "Nothing"):
                self.multiworld.itempool.remove(item)
            if (item.name == "Ultra-Spicy Spray"):
                self.multiworld.itempool.remove(item)
            if (item.name == "Ultra-Bitter Spray"):
                self.multiworld.itempool.remove(item)

            if (item.name in removable_items and count < num_items_to_remove):
                self.multiworld.itempool.remove(item)
                count += 1
            # remove onions from pool if the setting is off
            if (self.options.onion_shuffle != 3 and (item.name == "Red Onion" or item.name == "Yellow Onion" or item.name == "Blue Onion")):
                self.multiworld.itempool.remove(item)
            elif (self.options.onion_shuffle == 3 and item.name == "Red Onion" and self.starting_type == "red"): # remove starting onion item from pool
                self.multiworld.itempool.remove(item)
            elif (self.options.onion_shuffle == 3 and item.name == "Yellow Onion" and self.starting_type == "yellow"):
                self.multiworld.itempool.remove(item)
            elif (self.options.onion_shuffle == 3 and item.name == "Blue Onion" and self.starting_type == "blue"):
                self.multiworld.itempool.remove(item)
            
            if (self.options.cave_keys == 0 and "Entrance Key" in item.name):
                self.multiworld.itempool.remove(item)
            
            # remove the titan dweevil treasures
            if (self.options.weapons_in_pool == 0):
                if (item.name == "Shock Therapist" or item.name == "Flare Cannon" or item.name == "Comedy Bomb" or item.name == "Monster Pump"):
                    self.multiworld.itempool.remove(item)
            if (item.name == "King of Bugs"):
                self.multiworld.itempool.remove(item)
        filler_item_num = (201 + self.treasure_check_count + self.poko_check_count) - 5 - num_items
        sprays = ["Ultra-Spicy Spray", "Ultra-Bitter Spray"]
        self.multiworld.itempool += [self.create_item(sprays[self.random.randint(0, 1)]) for _ in range(filler_item_num)]
    
    def set_rules(self):
        # There are definitely duplicate rules here, but who cares
        add_item_rule(self.multiworld.get_location("VoR Courage Reactor", self.player),
                      lambda item: item.player != self.player or item.get_weight() <= 20) # this is supposed to disallow placing items that weigh more than 20
        
        for item in explorer_kit_treasure:
            forbid_item(self.multiworld.get_location("VoR Courage Reactor", self.player), item, self.player) # can't have EK items in day 1 location
        # no filler in day 1 location
        forbid_item(self.multiworld.get_location("VoR Courage Reactor", self.player), "Ultra-Spicy Spray", self.player)
        forbid_item(self.multiworld.get_location("VoR Courage Reactor", self.player), "Ultra-Bitter Spray", self.player)
        
        self.multiworld.get_location("Pay Off Debt", self.player).place_locked_item(self.create_event("Pay Off Debt"))

        add_rule(self.multiworld.get_location("Pay Off Debt", self.player),
                        lambda state: self.check_pokos(state, self.options.debt))

        if (self.options.win_condition == 0):
            self.multiworld.get_location("Beat Titan Dweevil", self.player).place_locked_item(self.create_event("Victory"))
            add_rule(self.multiworld.get_location("Beat Titan Dweevil", self.player),
                     lambda state: state.has("King of Bugs", self.player))
        elif (self.options.win_condition == 1):
            self.multiworld.get_location("Reach Poko Count", self.player).place_locked_item(self.create_event("Victory"))
        elif (self.options.win_condition == 2):
            self.multiworld.get_location("Reach Treasure Count", self.player).place_locked_item(self.create_event("Victory"))

        for region in self.multiworld.regions:
            if (region.player == self.player):
                for exit in region.exits:
                    if (exit.connected_region.name == "Awakening Wood"):
                        if (self.options.progressive_globes):
                            add_rule(exit,
                                    lambda state: state.has("Spherical Atlas", self.player) or state.has("Geographic Projection", self.player))
                        else:
                            add_rule(exit,
                                    lambda state: state.has("Spherical Atlas", self.player))
                    if (exit.connected_region.name == "Perplexing Pool"):
                        if (self.options.progressive_globes):
                            add_rule(exit,
                                    lambda state: state.has("Spherical Atlas", self.player) and state.has("Geographic Projection", self.player))
                        else:
                            add_rule(exit,
                                    lambda state: state.has("Geographic Projection", self.player))
                    if (exit.connected_region.name == "Pay Debt"):
                        add_rule(exit,
                                lambda state: self.check_pokos(state, self.options.debt))
                    if (exit.connected_region.name == "Wistful Wild"):
                        add_rule(exit,
                                lambda state: state.has("Spherical Atlas", self.player) and state.has("Geographic Projection", self.player) and state.has("Pay Off Debt", self.player))
                    if (exit.connected_region.name == "Victory Region"):
                        if (self.options.win_condition == 1):
                            add_rule(exit,
                                    lambda state: self.check_pokos(state, self.options.poko_amount))
                        if (self.options.win_condition == 2):
                            add_rule(exit,
                                    lambda state: self.check_treasures(state, self.options.treasure_amount))
        if (self.options.treasure_collection_checks != 0):
            region = self.multiworld.get_region("Treasure Checks", self.player)
            for loc in region.locations:
                num = int(loc.name.split(" ")[1])
                add_rule(loc,
                    lambda state, n=num: self.check_treasures(state, n))
        if (self.options.poko_collection_checks != 0):
            region = self.multiworld.get_region("Poko Checks", self.player)
            for loc in region.locations:
                num = int(loc.name.split(" ")[1][:-1])
                num = int(num / 100.0 * self.options.debt)
                add_rule(loc,
                    lambda state, n=num: self.check_pokos(state, n))
        globes_needed_for_aw_onion = 2
        if (self.onion_mapping["AW"] == "yellow" or self.onion_mapping["VoR"] == "yellow"):
            globes_needed_for_aw_onion = 1
        for location in location_data: # handle checks locked behind locations, as well as buried treasure
            pikmin_needed = location[4]
            if (test_location(location[0], caves.values())): # location is in a cave
                vanilla_cave = location[0].split(" ")[0]
                # We want to know which vanilla cave has the cave that this item is normally in
                for vanilla_cave_location, new_cave in self.cave_mapping.items(): 
                    if (new_cave == vanilla_cave):
                        shuffled_cave = vanilla_cave_location # shuffled_cave is the location that this cave is now at
                        break
                pikmin_needed += cave_pikmin_types_required[shuffled_cave]
                if (self.options.cave_keys):
                    # I have no idea why using an f-string and interpolating the cave name didn't work but it didn't so we get if statements instead XD
                    add_rule(self.multiworld.get_location(location[0], self.player),
                            lambda state, cave=shuffled_cave: state.has(f"{cave} Entrance Key", self.player))
                    # if (shuffled_cave == "EC"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("EC Entrance Key", self.player))
                    # elif (shuffled_cave == "SC"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("SC Entrance Key", self.player))
                    # elif (shuffled_cave == "FC"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("FC Entrance Key", self.player))
                    # elif (shuffled_cave == "HoB"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("HoB Entrance Key", self.player))
                    # elif (shuffled_cave == "WFG"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("WFG Entrance Key", self.player))
                    # elif (shuffled_cave == "BK"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("BK Entrance Key", self.player))
                    # elif (shuffled_cave == "SH"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("SH Entrance Key", self.player))
                    # elif (shuffled_cave == "CoS"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("CoS Entrance Key", self.player))
                    # elif (shuffled_cave == "GK"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("GK Entrance Key", self.player))
                    # elif (shuffled_cave == "SR"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("SR Entrance Key", self.player))
                    # elif (shuffled_cave == "SMGC"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("SMGC Entrance Key", self.player))
                    # elif (shuffled_cave == "CoC"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("CoC Entrance Key", self.player))
                    # elif (shuffled_cave == "HoH"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("HoH Entrance Key", self.player))
                    # elif (shuffled_cave == "DD"):
                    #     add_rule(self.multiworld.get_location(location[0], self.player),
                    #         lambda state: state.has("DD Entrance Key", self.player))
                # shuffled cave should be used to add cave key check

            # In theory, Spherical Atlas should handle opening AW and Geographic Projection should handle opening PP. The code even supports this. But, when the 
            # Geographic Projection is collected before the Spherical Atlas, both AW and PP open, but only AW is selectable. Then, the next time the player visits
            # the world map, only AW shows up. So basically, a single half gets you to AW, and both halves get you to PP.
            needs_one = False
            needs_both = False
            needs_debt_paid = False
            forbid_buried = False
            needs_red_item = False
            needs_yellow_item = False
            needs_blue_item = False
            needs_spherical_atlas = False
            needs_geographic_projection = False
            # checks based on pikmin types
            if (self.options.onion_shuffle == 3): # pikis are in pool
                if ("red" in pikmin_needed and "red" != self.starting_type):
                    needs_red_item = True
                if ("yellow" in pikmin_needed and "yellow" != self.starting_type):
                    needs_yellow_item = True
                if ("blue" in pikmin_needed and "blue" != self.starting_type):
                    needs_blue_item = True
            else:
                if (self.onion_mapping["PP"] in pikmin_needed):
                    needs_both = True
                    needs_geographic_projection = True
                if (self.onion_mapping["AW"] in pikmin_needed):
                    if (globes_needed_for_aw_onion == 2):
                        needs_both = True
                        needs_geographic_projection = True
                        needs_spherical_atlas = True
                    if (globes_needed_for_aw_onion == 1):
                        needs_one = True
                        needs_spherical_atlas = True
            
            # checks based on globes/debt
            if (test_location(location[0], self.aw_prefixes_rando) or "white" in pikmin_needed or (location[0] == "Beat Titan Dweevil" and "DD" in self.aw_prefixes_rando)): # whites can always be found in AW
                needs_one = True
                needs_spherical_atlas = True
            if (test_location(location[0], self.pp_prefixes_rando) or (location[0] == "Beat Titan Dweevil" and "DD" in self.pp_prefixes_rando)):
                needs_both = True
                needs_geographic_projection = True
            if (test_location(location[0], self.ww_prefixes_rando) or (location[0] == "Beat Titan Dweevil" and "DD" in self.ww_prefixes_rando)):
                needs_both = True
                needs_debt_paid = True
            
            if (self.options.progressive_globes):
                if (needs_debt_paid):
                    add_rule(self.multiworld.get_location(location[0], self.player),
                            lambda state: state.has("Spherical Atlas", self.player) and state.has("Geographic Projection", self.player) and state.has("Pay Off Debt", self.player))
                elif (needs_both):
                    add_rule(self.multiworld.get_location(location[0], self.player),
                            lambda state: state.has("Spherical Atlas", self.player) and state.has("Geographic Projection", self.player))
                elif (needs_one):
                    add_rule(self.multiworld.get_location(location[0], self.player),
                            lambda state: state.has("Geographic Projection", self.player) or state.has("Spherical Atlas", self.player))
                else:
                    forbid_buried = True # if location requires no globes, we may not have white pikmin, so don't put buried treasure here
            else:
                forbid_buried = True # VoR and PP can't have buried treasures since we may not have whites, TODO fix that
                if (needs_debt_paid):
                    add_rule(self.multiworld.get_location(location[0], self.player),
                            lambda state: state.has("Spherical Atlas", self.player) and state.has("Geographic Projection", self.player) and state.has("Pay Off Debt", self.player))
                    forbid_buried = False
                if (needs_spherical_atlas):
                    add_rule(self.multiworld.get_location(location[0], self.player),
                            lambda state: state.has("Spherical Atlas", self.player))
                    forbid_buried = False
                if (needs_geographic_projection):
                    add_rule(self.multiworld.get_location(location[0], self.player),
                            lambda state: state.has("Geographic Projection", self.player))
                    
            if (location[7] == False): # area is inaccessible by purples + whites, so forbid the heavy items + buried items
                forbid_item(self.multiworld.get_location(location[0], self.player), "Doomsday Apparatus", self.player)
                forbid_item(self.multiworld.get_location(location[0], self.player), "Spherical Atlas", self.player)
                forbid_item(self.multiworld.get_location(location[0], self.player), "Geographic Projection", self.player)
                forbid_buried = True

            if (needs_red_item):
                add_rule(self.multiworld.get_location(location[0], self.player),
                        lambda state: state.has("Red Onion", self.player))
            if (needs_yellow_item):
                add_rule(self.multiworld.get_location(location[0], self.player),
                        lambda state: state.has("Yellow Onion", self.player))
            if (needs_blue_item):
                add_rule(self.multiworld.get_location(location[0], self.player),
                        lambda state: state.has("Blue Onion", self.player))
                
            if (forbid_buried):
                for item in buried_treasure:
                    forbid_item(self.multiworld.get_location(location[0], self.player), item, self.player)

            if (not(test_location(location[0], caves.values()))): # location is NOT in a cave
                for item in self.options.start_inventory.keys(): # forbid starting items from appearing in the overworld, as this crashes the game
                    forbid_item(self.multiworld.get_location(location[0], self.player), item, self.player)
                if self.options.weapons_in_pool: # forbid Titan Dweevil weapons from appearing in the overworld, as collecting them off the Titan Dweevil will cause the game to crash
                    for item in ["Shock Therapist", "Flare Cannon", "Monster Pump", "Comedy Bomb"]:
                        forbid_item(self.multiworld.get_location(location[0], self.player), item, self.player)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def get_pre_fill_items(self):
        elec = Pikmin2Item("Shock Therapist", get_classification("Shock Therapist"), 80, self.player)
        fire = Pikmin2Item("Flare Cannon", get_classification("Flare Cannon"), 81, self.player)
        gas = Pikmin2Item("Comedy Bomb", get_classification("Comedy Bomb"), 82, self.player)
        water = Pikmin2Item("Monster Pump", get_classification("Monster Pump"), 83, self.player)
        louie = Pikmin2Item("King of Bugs", get_classification("King of Bugs"), 90, self.player)
        nothing = Pikmin2Item("Nothing", get_classification("Nothing"), 236, self.player)
        return [elec, fire, gas, water, louie, nothing]
    
    def pre_fill(self):
        # manually assign these since they can't be randomized
        # archipelago items are 1-indexed
        elec = Pikmin2Item("Shock Therapist", get_classification("Shock Therapist"), 80, self.player)
        fire = Pikmin2Item("Flare Cannon", get_classification("Flare Cannon"), 81, self.player)
        gas = Pikmin2Item("Comedy Bomb", get_classification("Comedy Bomb"), 82, self.player)
        water = Pikmin2Item("Monster Pump", get_classification("Monster Pump"), 83, self.player)
        louie = Pikmin2Item("King of Bugs", get_classification("King of Bugs"), 90, self.player)
        nothing = Pikmin2Item("Nothing", get_classification("Nothing"), 236, self.player)
        if self.options.weapons_in_pool == 0:
            self.multiworld.get_location("DD Shock Therapist", self.player).item = elec
            self.multiworld.get_location("DD Flare Cannon", self.player).item = fire
            self.multiworld.get_location("DD Comedy Bomb", self.player).item = gas
            self.multiworld.get_location("DD Monster Pump", self.player).item = water
        else:
            self.multiworld.get_location("DD Shock Therapist", self.player).item = nothing
            self.multiworld.get_location("DD Flare Cannon", self.player).item = nothing
            self.multiworld.get_location("DD Comedy Bomb", self.player).item = nothing
            self.multiworld.get_location("DD Monster Pump", self.player).item = nothing
        self.multiworld.get_location("DD King of Bugs", self.player).item = louie

    def generate_output(self, output_directory):
        data = {
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.player,
            "slot_name": self.multiworld.player_name[self.player],  # to connect to server
            "items": {location.name: location.item.name
                    if location.item.player == self.player else "Remote"
                    for location in self.multiworld.get_filled_locations(self.player) if location.name != "Pay Off Debt" and location.name != "Beat Titan Dweevil" and location.name != "Reach Poko Count" and location.name != "Reach Treasure Count"},
            "starter_items": [item.name for item in self.multiworld.precollected_items[self.player]],
            "win_condition": int(self.options.win_condition),
            "poko_amount": int(self.options.poko_amount),
            "treasure_amount": int(self.options.treasure_amount),
            "caves": self.cave_mapping,
            "cave_rando": int(self.options.shuffle_caves),
            "death_link": int(self.options.death_link),
            "boss_rando": int(self.options.boss_rando),
            "enemy_rando": int(self.options.enemy_rando),
            "boss_and_enemy_rando": int(self.options.boss_and_enemy_rando),
            "sublevel_shuffle": int(self.options.sublevel_shuffle),
            "onion_shuffle": int(self.options.onion_shuffle),
            "onion_locations": self.onion_mapping,
            "debt": int(self.options.debt),
            "progressive_globes": int(self.options.progressive_globes),
            "cave_keys": int(self.options.cave_keys),
            "sublevels": self.sublevel_mapping,
            "treasure_collection_checks": int(self.options.treasure_collection_checks),
            "treasure_collection_sv": int(self.options.treasure_collection_start_value),
            "treasure_collection_ev": int(self.options.treasure_collection_end_value),
            "treasure_collection_i": int(self.options.treasure_collection_interval),
            "poko_collection_checks": int(self.options.poko_collection_checks)
        }
        f = open(os.path.join(output_directory, f"AP_{self.multiworld.seed_name}_P{self.player}_{self.multiworld.player_name[self.player]}.appik2"), "w")
        json.dump(data, f)
        f.close()

    def fill_slot_data(self):
        data = self.options.as_dict("debt", "cave_keys", "progressive_globes", "weapons_in_pool")
        data["caves"] = self.cave_mapping
        data["onion_locations"] = self.onion_mapping
        data["sublevels"] = self.sublevel_mapping
        buried_locs = []
        for item in buried_treasure:
            for location in location_data:
                i = Pikmin2Item(item, get_classification(item), self.item_name_to_id[item], self.player)
                l = self.multiworld.get_location(location[0], self.player)
                if (l.item == i):
                    buried_locs.append([item, location[0]])
        data["buried_treasure_locations"] = buried_locs
        return data



