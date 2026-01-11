from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import KHBBSItem, KHBBSItemData, event_item_table, get_items_by_category, item_table, item_name_groups
from .Locations import KHBBSLocation, location_table, get_locations_by_category, location_name_groups
from .Options import KHBBSOptions, khbbs_option_groups
from .Regions import create_regions
from .Rules import set_rules
from .OpenKH import patch_khbbs
from worlds.LauncherComponents import Component, components, Type, launch_subprocess


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="KHBBS Client")


components.append(Component("KHBBS Client", "KHBBSClient", func=launch_client, component_type=Type.CLIENT))


class KHBBSWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Kingdom Hearts BBS Randomizer software on your computer. This guide covers single-player, "
            "multiworld, and related software.",
            "English",
            "kh1_en.md",
            "kh1/en",
            ["Gicu"]
    )]
    option_groups = khbbs_option_groups


class KHBBSWorld(World):
    """
    Kingdom Hearts Birth by Sleep is an action RPG following three friends, 
    Terra, Ventus, and Aqua on a journey through many worlds to defeat Xehanort.
    """
    game = "Kingdom Hearts Birth by Sleep"
    options_dataclass = KHBBSOptions
    options: KHBBSOptions
    topology_present = True
    required_client_version = (0, 3, 5)
    web = KHBBSWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    def create_items(self):
        self.place_predetermined_items()
        
        character_letters = ["V", "A", "T"]
        # Handle starting worlds
        starting_worlds = []
        if self.options.starting_worlds > 0:
            possible_starting_worlds = ["Dwarf Woodlands", 
                "Castle of Dreams", "Enchanted Dominion", "The Mysterious Tower", 
                "Radiant Garden", "Olympus Coliseum", "Deep Space",
                "Never Land", "Disney Town"]
            if self.options.mirage_arena or self.options.command_board or self.options.minigames:
                possible_starting_worlds.append("Mirage Arena")
            if self.options.character == 1 and self.options.realm_of_darkness:
                possible_starting_worlds.append("Realm of Darkness")
            starting_worlds = self.random.sample(possible_starting_worlds, min(self.options.starting_worlds, len(possible_starting_worlds)))
            for starting_world in starting_worlds:
                self.multiworld.push_precollected(self.create_item(starting_world))
        item_pool: List[KHBBSItem] = []
        
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        
        non_filler_item_categories = ["Movement Command", "Defense Command", "Reprisal Command", "Command Board",
            "Shotlock Command", "Command Style", "Ability", "Key Item", "World", "Stat Up", "D-Link"]
        for name, data in item_table.items():
            quantity = data.max_quantity
            if data.category not in non_filler_item_categories:
                continue
            if name in starting_worlds:
                continue
            if name == "Mirage Arena" and not (self.options.mirage_arena or self.options.command_board or self.options.minigames):
                continue
            if name == "Realm of Darkness" and not self.options.realm_of_darkness:
                continue
            if name == "HP Increase":
                item_pool += [self.create_item(name) for _ in range(0, self.options.max_hp_increases.value)]
            elif character_letters[self.options.character] in data.characters:
                item_pool += [self.create_item(name) for _ in range(0, quantity)]
        
        # These are magic commands (normally filler) but a few locations require them so guaranteeing some in the pool
        if self.options.character != 0: #Ventus doesn't need Fire
            item_pool += [self.create_item("Fire")]
        if self.options.character != 1: #Aqua starts with Thunder
            item_pool += [self.create_item("Thunder")]

        # Fill any empty locations with filler items.
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))
        
        self.multiworld.itempool += item_pool

    def place_predetermined_items(self) -> None:
        goal_locations = ["(V) The Keyblade Graveyard Defeat Final Vanitas",
            "(A) The Keyblade Graveyard Defeat Ventus-Vanitas",
            "(T) The Keyblade Graveyard Defeat Terra-Xehanort"]
        if self.options.character == 1 and self.options.final_terra_xehanort_ii:
             self.get_location("(A) Radiant Garden Defeat Final Terra-Xehanort II").place_locked_item(self.create_item("Victory"))
        else:
            self.get_location(goal_locations[self.options.character]).place_locked_item(self.create_item("Victory"))

    def get_filler_item_name(self) -> str:
        fillers = {}
        exclude = []
        characters = ["V","A","T"]
        fillers.update(get_items_by_category("Attack Command",     characters[self.options.character]))
        fillers.update(get_items_by_category("Magic Command",      characters[self.options.character]))
        fillers.update(get_items_by_category("Item Command",       characters[self.options.character]))
        fillers.update(get_items_by_category("Friendship Command", characters[self.options.character]))
        return self.random.choices([filler for filler in fillers.keys()])[0]

    def fill_slot_data(self) -> dict:
        slot_data = {"xpmult":                  int(self.options.exp_multiplier)/16,
                     "non_remote_location_ids": self.get_non_remote_location_ids(),
                     "character":               int(self.options.character),
                     "mirage_arena":            bool(self.options.mirage_arena),
                     "command_board":           bool(self.options.command_board),
                     "minigames":               bool(self.options.minigames),
                     "arena_medals":            bool(self.options.arena_medals),
                     "superbosses":             bool(self.options.super_bosses),
                     "arena_global":            bool(self.options.arena_global_locations),
                     "advanced_logic":          bool(self.options.advanced_logic),
                     "realm":                   bool(self.options.realm_of_darkness),
                     "final_terranort":         bool(self.options.final_terra_xehanort_ii)}
        if self.options.randomize_keyblade_stats:
            min_str_bonus = min(self.options.keyblade_min_str.value, self.options.keyblade_max_str.value)
            max_str_bonus = max(self.options.keyblade_min_str.value, self.options.keyblade_max_str.value)
            self.options.keyblade_min_str.value = min_str_bonus
            self.options.keyblade_max_str.value = max_str_bonus
            min_mgc_bonus = min(self.options.keyblade_min_mgc.value, self.options.keyblade_max_mgc.value)
            max_mgc_bonus = max(self.options.keyblade_min_mgc.value, self.options.keyblade_max_mgc.value)
            self.options.keyblade_min_mgc.value = min_mgc_bonus
            self.options.keyblade_max_mgc.value = max_mgc_bonus
            slot_data["keyblade_stats"] = ""
            for i in range(49):
                str_bonus = int(self.random.randint(min_str_bonus, max_str_bonus))
                mgc_bonus = int(self.random.randint(min_mgc_bonus, max_mgc_bonus))
                slot_data["keyblade_stats"] = slot_data["keyblade_stats"] + str(str_bonus) + "," + str(mgc_bonus) + ","
            slot_data["keyblade_stats"] = slot_data["keyblade_stats"][:-1]
        return slot_data
    
    def create_item(self, name: str) -> KHBBSItem:
        data = item_table[name]
        return KHBBSItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> KHBBSItem:
        data = event_item_table[name]
        return KHBBSItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)

    def generate_output(self, output_directory: str):
        """
        Generates the .zip for OpenKH (The KH Mod Manager)
        """
        patch_khbbs(self, output_directory, self.options.character)
    
    def get_non_remote_location_ids(self):
        non_remote_location_ids = []
        for location in self.multiworld.get_filled_locations(self.player):
            location_data = location_table[location.name]
            if self.player == location.item.player:
                item_data = item_table[location.item.name]
                if location_data.type == "Chest":
                    if item_data.category in ["Attack Command", "Magic Command", "Item Command", "Friendship Command", "Movement Command", "Defense Command", "Reprisal Command", "Shotlock Command", "Key Item"] and not location_data.forced_remote and "Wayfinder" not in location.item.name:
                        non_remote_location_ids.append(location_data.code)
                if location_data.type == "Sticker":
                    if item_data.category in ["Key Item"] and "Wayfinder" not in location.item.name:
                        non_remote_location_ids.append(location_data.code)
        return non_remote_location_ids