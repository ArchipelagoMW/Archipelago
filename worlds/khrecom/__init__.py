from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import KHRECOMItem, KHRECOMItemData, event_item_table, get_items_by_category, item_table
from .Locations import KHRECOMLocation, location_table, get_locations_by_category
from .Options import KHRECOMOptions
from .Regions import create_regions
from .Rules import set_rules
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
    required_client_version = (0, 3, 5)
    web = KHRECOMWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}
    
    def __init__(self, multiworld: "MultiWorld", player: int):
        super(KHRECOMWorld, self).__init__(multiworld, player)
        self.world_order = []
    
    def create_items(self):
        item_pool: List[KHRECOMItem] = []
        self.multiworld.get_location("12F Exit Hall Larxene II (Enemy Cards Larxene)", self.player).place_locked_item(self.create_item("Friend Card Pluto"))
        self.multiworld.get_location("Final Marluxia", self.player).place_locked_item(self.create_item("Victory"))
        starting_locations = get_locations_by_category("Starting")
        starting_locations = self.random.sample(list(starting_locations.keys()),4)
        starting_worlds = get_items_by_category("World Unlocks", [])
        starting_worlds = self.random.sample(list(starting_worlds.keys()),3)
        i = 0
        while i < 4:
            if i < 3 and self.options.starting_worlds:
                self.multiworld.get_location(starting_locations[i], self.player).place_locked_item(self.create_item(starting_worlds[i]))
            elif i == 3 and self.options.early_cure:
                self.multiworld.get_location(starting_locations[i], self.player).place_locked_item(self.create_item("Card Set Cure"))
            i = i + 1
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        for name, data in item_table.items():
            quantity = data.max_quantity
            
            # Ignore filler, it will be added in a later stage.
            if data.category not in ["World Unlocks", "Gold Map Cards", "Friend Cards", "Enemy Cards", "Sleights"]:
                continue
            if not self.options.starting_worlds or name not in starting_worlds:
                item_pool += [self.create_item(name) for _ in range(0, quantity)]

        # Fill any empty locations with filler items.
        item_names = []
        attempts = 0 #If we ever try to add items 200 times, and all the items are used up, lets clear the item_names array, we probably don't have enough items
        while len(item_pool) < total_locations:
            item_name = self.get_filler_item_name()
            if item_name not in item_names or "Pack" in item_name:
                item_names.append(item_name)
                item_pool.append(self.create_item(item_name))
                attempts = 0
            elif attempts >= 200:
                item_names = []
                attempts = 0
            else:
                attempts = attempts + 1

        self.multiworld.itempool += item_pool
        
        print("Total Locations: " + str(total_locations))
        print("Item Pool Length: " + str(len(item_pool)))

    def get_filler_item_name(self) -> str:
        fillers = {}
        disclude = []
        if not self.options.cure:
            disclude.append("Cure")
        if self.options.early_cure:
            disclude.append("Cure")
        fillers.update(get_items_by_category("Sets", disclude))
        weights = [data.weight for data in fillers.values()]
        return self.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
        
    def create_item(self, name: str) -> KHRECOMItem:
        data = item_table[name]
        return KHRECOMItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> KHRECOMItem:
        data = event_item_table[name]
        return KHRECOMItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)
    
    def fill_slot_data(self) -> dict:
        self.decide_world_order()
        zeroes_string = "Yes"
        world_order_string = ""
        for world_id in self.world_order:
            world_order_string = world_order_string + str(world_id) + ","
        world_order_string = world_order_string[:-1]
        if not self.options.zeroes:
            zeroes_string = "No"
        slot_data = {"EXP Multiplier": int(self.options.exp_multiplier)
                    ,"World Order":    world_order_string
                    ,"Zeroes":         zeroes_string
                    ,"Attack Power":   int(self.options.attack_power)}
        return slot_data
    
    def decide_world_order(self):
        if len(self.world_order) == 0:
            possible_world_assignments = [2,3,4,5,6,7,8,9,10]
            self.random.shuffle(possible_world_assignments)
            self.world_order = possible_world_assignments