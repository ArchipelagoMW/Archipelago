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

    def create_items(self):
        item_pool: List[KHRECOMItem] = []
        self.multiworld.get_location("Destiny Islands Post Floor (Enemy Cards Larxene)", self.player).place_locked_item(self.create_item("Friend Card Pluto"))
        self.multiworld.get_location("Final Marluxia", self.player).place_locked_item(self.create_item("Victory"))
        starting_locations = get_locations_by_category("Starting")
        starting_locations = self.random.sample(list(starting_locations.keys()),4)
        starting_worlds = get_items_by_category("World Unlocks", [])
        starting_worlds = self.random.sample(list(starting_worlds.keys()),3)
        i = 0
        while i < 4:
            if i < 3:
                self.multiworld.get_location(starting_locations[i], self.player).place_locked_item(self.create_item(starting_worlds[i]))
            elif i == 3 and self.options.early_cure:
                self.multiworld.get_location(starting_locations[i], self.player).place_locked_item(self.create_item("Card Set Cure 4-6"))
            i = i + 1
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        for name, data in item_table.items():
            quantity = data.max_quantity
            
            # Ignore filler, it will be added in a later stage.
            if data.category not in ["World Unlocks", "Gold Map Cards", "Friend Cards"]:
                continue
            if name not in starting_worlds:
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

    def get_filler_item_name(self) -> str:
        fillers = {}
        disclude = []
        if not self.options.zeroes:
            disclude.append("0")
        if not self.options.cure:
            disclude.append("Cure")
        if self.options.early_cure:
            disclude.append("Cure 4-6")
        if self.options.enemy_cards:
            fillers.update(get_items_by_category("Enemy Cards", disclude))
        if self.options.days_items:
            fillers.update(get_items_by_category("Days Sets", disclude))
            fillers.update(get_items_by_category("Days Enemy Cards", disclude))
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
        set_rules(self.multiworld, self.player, self.options.days_locations)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options.days_locations, self.options.checks_behind_leon)
    
    def fill_slot_data(self) -> dict:
        slot_data = {"EXP Multiplier":      int(self.options.exp_multiplier)}
        return slot_data