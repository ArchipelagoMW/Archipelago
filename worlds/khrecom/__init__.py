from typing import List

from BaseClasses import Tutorial, MultiWorld
from worlds.AutoWorld import WebWorld, World
from .Items import KHRECOMItem, KHRECOMItemData, get_items_by_category, item_table, item_name_groups
from .Locations import location_table, location_name_groups
from .Options import KHRECOMOptions, khrecom_option_groups
from .Regions import create_regions
from .Rules import set_rules
from .Presets import khrecom_option_presets
from worlds.LauncherComponents import Component, components, Type, launch_subprocess



def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="KHRECOM Client")


components.append(Component("KHRECOM Client", "KHRECOMClient", func=launch_client, component_type=Type.CLIENT))

class KHRECOMWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Kingdom Hearts RE Chain of Memories Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "khrecom_en.md",
        "khrecom/en",
        ["Gicu"]
    )]
    option_groups = khrecom_option_groups
    options_presets = khrecom_option_presets

class KHRECOMWorld(World):
    """
    Kingdom Hearts RE Chain of Memories is an action card RPG following
    Sora on his journey through Castle Oblivion to find Riku and Kairi.
    """
    game = "Kingdom Hearts RE Chain of Memories"
    options_dataclass = KHRECOMOptions
    options: KHRECOMOptions
    topology_present = True
    data_version = 4
    web = KHRECOMWeb()
    world_order = []

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups
    
    def create_items(self):
        self.place_predetermined_items()
        # Handle starting worlds
        starting_worlds = []
        if self.options.starting_worlds > 0:
            possible_starting_worlds = [
                "World Card Wonderland",
                "World Card Olympus Coliseum",
                "World Card Agrabah",
                "World Card Monstro",
                "World Card Atlantica",
                "World Card Halloween Town",
                "World Card Neverland",
                "World Card Hollow Bastion",
                "World Card 100 Acre Wood",
                "World Card Twilight Town",
                "World Card Destiny Islands"]
            starting_worlds = self.random.sample(possible_starting_worlds, min(self.options.starting_worlds.value, len(possible_starting_worlds)))
            for starting_world in starting_worlds:
                self.multiworld.push_precollected(self.create_item(starting_world))
        if self.options.starting_cure:
            self.multiworld.push_precollected(self.create_item("Card Set Cure"))
        
        item_pool: List[KHRECOMItem] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        sleights_added = 0
        enemy_cards_added = 0
        shuffled_item_list = list(item_table.items())
        self.random.shuffle(shuffled_item_list)
        for name, data in shuffled_item_list:
            # Ignore filler, it will be added in a later stage.
            if data.category not in ["World Unlocks", "Gold Map Cards", "Friend Cards", "Enemy Cards", "Sleights"]:
                continue
            elif data.category == "Enemy Cards" and enemy_cards_added < self.options.enemy_card_amount and name not in ["Enemy Card " + card_name for card_name in self.options.exclude_enemy_cards.value]:
                enemy_cards_added = enemy_cards_added + 1
                item_pool.append(self.create_item(name))
            elif data.category == "Sleights" and sleights_added < self.options.sleight_amount and name not in ["Sleight " + sleight_name for sleight_name in self.options.exclude_sleights.value]:
                sleights_added = sleights_added + 1
                item_pool.append(self.create_item(name))
            elif data.category not in ["Sleights", "Enemy Cards"] and name not in starting_worlds and name != "Friend Card Pluto":
                item_pool.append(self.create_item(name))
        
        # Fill any empty locations with filler items.
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))
        
        self.multiworld.itempool += item_pool

    def place_predetermined_items(self) -> None:
        self.get_location("12F Exit Hall Larxene II (Enemy Cards Larxene)").place_locked_item(self.create_item("Friend Card Pluto"))
        self.get_location("Final Marluxia").place_locked_item(self.create_item("Victory"))

    def get_filler_item_name(self) -> str:
        fillers = {}
        exclude = []
        for card in self.options.exclude_cards.value:
            exclude.append("Card Set " + card)
        fillers.update(get_items_by_category("Sets", exclude))
        return self.random.choices([filler for filler in fillers.keys()], k=1)[0]
        
    def create_item(self, name: str) -> KHRECOMItem:
        data = item_table[name]
        return KHRECOMItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)
    
    def fill_slot_data(self) -> dict:
        self.decide_world_order()
        world_order_string = ""
        for world_id in self.world_order:
            world_order_string = world_order_string + str(world_id) + ","
        world_order_string = world_order_string[:-1]
        
        set_values = [
            self.options.value_0_on,
            self.options.value_1_on,
            self.options.value_2_on,
            self.options.value_3_on,
            self.options.value_4_on,
            self.options.value_5_on,
            self.options.value_6_on,
            self.options.value_7_on,
            self.options.value_8_on,
            self.options.value_9_on,
            self.options.value_0_p_on,
            self.options.value_1_p_on,
            self.options.value_2_p_on,
            self.options.value_3_p_on,
            self.options.value_4_p_on,
            self.options.value_5_p_on,
            self.options.value_6_p_on,
            self.options.value_7_p_on,
            self.options.value_8_p_on,
            self.options.value_9_p_on]
        set_data = []
        set_data_string = ""
        for i in range(20):
            set_data.append([])
            for set_index, set_value in enumerate(set_values):
                if set_value == i + 1:
                    set_data[i].append(set_index)
            set_data_string = set_data_string + ','.join(map(str, set_data[i])) + "\n"
        slot_data = {"xpmult": int(self.options.exp_multiplier)
                    ,"worldorder":    world_order_string
                    ,"attackpower":   int(self.options.attack_power)
                    ,"setdata": set_data_string}
        return slot_data
    
    def decide_world_order(self):
        if len(self.world_order) == 0:
            possible_world_assignments = [2,3,4,5,6,7,8,9,10]
            self.random.shuffle(possible_world_assignments)
            self.world_order = possible_world_assignments
