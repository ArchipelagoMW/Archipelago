import base64
from typing import Dict, Any

import Utils
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Item, ItemClassification

from . import client
from .rom import generate_output
from .options import sml2options

locations = [
    "Mushroom Zone", #A848
    "Scenic Course", #A870
    "Tree Zone 1 - Invincibility!", #A849
    "Tree Zone 2 - In the Trees", #A84A
    "Tree Zone 3 - The Exit", #A84C
    "Tree Zone 4 - Honeybees", #A84B
    "Tree Zone 5 - The Big Bird", #A84D
    "Tree Zone - Secret Course", #A84B
    "Hippo Zone", #A867
    "Space Zone 1 - Moon Stage", #A858
    "Space Zone 2 - Star Stage", #A859
    "Space Zone - Secret Course", #A871
    "Macro Zone 1 - The Ant Monsters", #A853
    "Macro Zone 2 - In the Syrup Sea", #A854
    "Macro Zone 3 - Fiery Mario-Special Agent", #A855
    "Macro Zone 4 - One Mighty Mouse", #A856
    "Macro Zone - Secret Course", #A86B
    "Pumpkin Zone 1 - Bat Course", #A84E
    "Pumpkin Zone 2 - Cyclops Course", #A84F
    "Pumpkin Zone 3 - Ghost House", #A850
    "Pumpkin Zone 4 - Witch's Mansion", #A851
    "Pumpkin Zone - Secret Course 1", #A86E
    "Pumpkin Zone - Secret Course 2", #A86F
    "Mario Zone 1 - Fiery Blocks", #A862
    "Mario Zone 2 - Mario the Circus Star!", #A863
    "Mario Zone 3 - Beware: Jagged Spikes", #A864
    "Mario Zone 4 - Three Mean Pigs!", #A865
    "Turtle Zone 1 - Cheep Cheep Course", #A85D
    "Turtle Zone 2 - Turtle Zone", #A85E
    "Turtle Zone 3 - Whale Course", #A85F
    "Turtle Zone - Secret Course", #A86D
]
locations = {
    "Mushroom Zone": 0,
    "Scenic Course": 40,
    "Tree Zone 1 - Invincibility!": 1,
    "Tree Zone 2 - In the Trees": 2,
    "Tree Zone 3 - The Exit": 4,
    "Tree Zone 4 - Honeybees": 3,
    "Tree Zone 5 - The Big Bird": 5,
    "Tree Zone - Secret Course": 3,
    "Hippo Zone": 31,
    "Space Zone 1 - Moon Stage": 16,
    "Space Zone 2 - Star Stage": 17,
    "Space Zone - Secret Course": 41,
    "Macro Zone 1 - The Ant Monsters": 11,
    "Macro Zone 2 - In the Syrup Sea": 12,
    "Macro Zone 3 - Fiery Mario-Special Agent": 13,
    "Macro Zone 4 - One Mighty Mouse": 14,
    "Macro Zone - Secret Course": 35,
    "Pumpkin Zone 1 - Bat Course": 6,
    "Pumpkin Zone 2 - Cyclops Course": 7,
    "Pumpkin Zone 3 - Ghost House": 8,
    "Pumpkin Zone 4 - Witch's Mansion": 9,
    "Pumpkin Zone - Secret Course 1": 38,
    "Pumpkin Zone - Secret Course 2": 39,
    "Mario Zone 1 - Fiery Blocks": 26,
    "Mario Zone 2 - Mario the Circus Star!": 27,
    "Mario Zone 3 - Beware: Jagged Spikes": 28,
    "Mario Zone 4 - Three Mean Pigs!": 29,
    "Turtle Zone 1 - Cheep Cheep Course": 21,
    "Turtle Zone 2 - Turtle Zone": 22,
    "Turtle Zone 3 - Whale Course": 23,
    "Turtle Zone - Secret Course": 37,
}
locations = {
    'Mushroom Zone': {'ram_index': 0},
    'Scenic Course': {'ram_index': 40},
    'Tree Zone 1 - Invincibility!': {'ram_index': 1, 'clear_condition': ("Progressive Tree Zone", 1)},
    'Tree Zone 2 - In the Trees': {'ram_index': 2, 'clear_condition': ("Progressive Tree Zone", 2)},
    'Tree Zone 3 - The Exit': {'ram_index': 4, 'clear_condition': ("Progressive Tree Zone", 3)},
    'Tree Zone 4 - Honeybees': {'ram_index': 3, 'clear_condition': ("Progressive Tree Zone", 3)},
    'Tree Zone 5 - The Big Bird': {'ram_index': 5, 'clear_condition': ("Tree Coin", 1)},
    'Tree Zone - Secret Course': {'ram_index': 3},
    'Hippo Zone': {'ram_index': 31},
    'Space Zone 1 - Moon Stage': {'ram_index': 16, 'clear_condition': ("Progressive Space Zone", 2)},
    'Space Zone 2 - Star Stage': {'ram_index': 17, 'clear_condition': ("Space Coin", 1)},
    'Space Zone - Secret Course': {'ram_index': 41},
    'Macro Zone 1 - The Ant Monsters': {'ram_index': 11, 'clear_condition': ("Progressive Macro Zone", 1)},
    'Macro Zone 2 - In the Syrup Sea': {'ram_index': 12, 'clear_condition': ("Progressive Macro Zone", 2)},
    'Macro Zone 3 - Fiery Mario-Special Agent': {'ram_index': 13, 'clear_condition': ("Progressive Macro Zone", 3)},
    'Macro Zone 4 - One Mighty Mouse': {'ram_index': 14, 'clear_condition': ("Macro Coin", 1)},
    'Macro Zone - Secret Course': {'ram_index': 35, 'clear_condition': ("Macro Zone Secret", 1)},
    'Pumpkin Zone 1 - Bat Course': {'ram_index': 6, 'clear_condition': ("Progressive Pumpkin Zone", 1)},
    'Pumpkin Zone 2 - Cyclops Course': {'ram_index': 7, 'clear_condition': ("Progressive Pumpkin Zone", 2)},
    'Pumpkin Zone 3 - Ghost House': {'ram_index': 8, 'clear_condition': ("Progressive Pumpkin Zone", 3)},
    "Pumpkin Zone 4 - Witch's Mansion": {'ram_index': 9, 'clear_condition': ("Pumpkin Coin", 1)},
    'Pumpkin Zone - Secret Course 1': {'ram_index': 38},
    'Pumpkin Zone - Secret Course 2': {'ram_index': 39},
    'Mario Zone 1 - Fiery Blocks': {'ram_index': 26, 'clear_condition': ("Progressive Mario Zone", 1)},
    'Mario Zone 2 - Mario the Circus Star!': {'ram_index': 27, 'clear_condition': ("Progressive Mario Zone", 2)},
    'Mario Zone 3 - Beware: Jagged Spikes': {'ram_index': 28, 'clear_condition': ("Progressive Mario Zone", 3)},
    'Mario Zone 4 - Three Mean Pigs!': {'ram_index': 29, 'clear_condition': ("Mario Coin", 1)},
    'Turtle Zone 1 - Cheep Cheep Course': {'ram_index': 21, 'clear_condition': ("Progressive Turtle Zone", 1)},
    'Turtle Zone 2 - Turtle Zone': {'ram_index': 22, 'clear_condition': ("Progressive Turtle Zone", 2)},
    'Turtle Zone 3 - Whale Course': {'ram_index': 23, 'clear_condition': ("Turtle Coin", 1)},
    'Turtle Zone - Secret Course': {'ram_index': 37}}

items = [
    "Progressive Space Zone",
    "Progressive Tree Zone",
    "Progressive Macro Zone",
    "Macro Zone Secret",
    "Progressive Pumpkin Zone",
    "Progressive Mario Zone",
    "Progressive Turtle Zone",
    "Tree Coin",
    "Space Coin",
    "Macro Coin",
    "Pumpkin Coin",
    "Mario Coin",
    "Turtle Coin",
    "Mushroom",
    "Fire Flower",
    "Carrot",
    "Progressive Invincibility Star",
    "Space Physics",
    "Easy Mode",
    "Normal Mode",
]
START_IDS = 7770000
class MarioLand2World(World):
    game = "Super Mario Land 2"

    location_name_to_id = {location_name: ID for ID, location_name in enumerate(locations, START_IDS)}
    item_name_to_id = {item_name: ID for ID, item_name in enumerate(items, START_IDS)}

    option_definitions = sml2options

    generate_output = generate_output

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        for location_name in locations:
            menu_region.locations.append(Location(self.player, location_name, self.location_name_to_id[location_name], menu_region))

    def set_rules(self):
        rules = {
            "Space Zone 1 - Moon Stage": lambda state: state.has("Progressive Space Zone", self.player), # this is really hard though
            "Space Zone - Secret Course": lambda state: state.has("Progressive Space Zone", self.player, 2) and state.has_any(["Space Physics", "Carrot"], self.player),
            "Space Zone 2 - Star Stage": lambda state: state.has("Progressive Space Zone", self.player, 2) and state.has("Space Physics", self.player),
            "Tree Zone 2 - In the Trees": lambda state: state.has("Progressive Tree Zone", self.player),
            "Tree Zone - Secret Course": lambda state: state.has_all(["Progressive Tree Zone", "Carrot"], self.player),
            "Tree Zone 3 - The Exit": lambda state: state.has("Progressive Tree Zone", self.player, 2),
            "Tree Zone 4 - Honeybees": lambda state: state.has("Progressive Tree Zone", self.player, 2),
            "Tree Zone 5 - The Big Bird": lambda state: state.has("Progressive Tree Zone", self.player, 3),
            # You can use a Fire Flower to get here from Macro Zone 1, or if you have every Progressive Macro Zone and the Macro Zone Secret paths, you can get here from the boss levl
            "Macro Zone - Secret Course": lambda state: state.has("Fire Flower", self.player) or (state.has("Macro Zone Secret", self.player) and state.has("Progressive Macro Zone", self.player, 3)),
            "Macro Zone 2 - In the Syrup Sea": lambda state: state.has("Progressive Macro Zone", self.player),
            "Macro Zone 3 - Fiery Mario-Special Agent": lambda state: state.has("Progressive Macro Zone", self.player, 2),
            "Macro Zone 4 - One Mighty Mouse": lambda state: state.has("Progressive Macro Zone", self.player, 3) or (state.has("Fire Flower", self.player) and state.has("Macro Zone Secret", self.player)),
            "Pumpkin Zone 2 - Cyclops Course": lambda state: state.has("Progressive Pumpkin Zone", self.player),
            # You can only spin jump as Big Mario or Fire Mario
            "Pumpkin Zone - Secret Course 1": lambda state: state.has("Progressive Pumpkin Zone", self.player) and state.has_any(["Mushroom", "Fire Flower"], self.player),
            "Pumpkin Zone 3 - Ghost House": lambda state: state.has("Progressive Pumpkin Zone", self.player, 2),
            "Pumpkin Zone - Secret Course 2": lambda state: state.has("Progressive Pumpkin Zone", self.player, 2) and state.has("Carrot", self.player),
            "Pumpkin Zone 4 - Witch's Mansion": lambda state: state.has("Progressive Pumpkin Zone", self.player, 3),
            "Mario Zone 2 - Mario the Circus Star!": lambda state: state.has("Progressive Mario Zone", self.player),
            "Mario Zone 3 - Beware: Jagged Spikes": lambda state: state.has("Progressive Mario Zone", self.player, 2),
            "Mario Zone 4 - Three Mean Pigs!": lambda state: state.has("Progressive Mario Zone", self.player, 3),
            "Turtle Zone 2 - Turtle Zone": lambda state: state.has("Progressive Turtle Zone", self.player),
            # The powerups are needed not for the secret exit in Turtle Zone 2, but to fly over or take damage in the spikes in the secret course
            "Turtle Zone - Secret Course": lambda state: state.has("Progressive Turtle Zone", self.player) and state.has_any(["Mushroom", "Fire Flower", "Carrot"], self.player),
            "Turtle Zone 3 - Whale Course": lambda state: state.has("Progressive Turtle Zone", self.player, 2),
        }

        for level, rule in rules.items():
            self.multiworld.get_location(level, self.player).access_rule = rule

        self.multiworld.completion_condition[self.player] = lambda state: state.has_all(["Tree Coin", "Space Coin",
            "Macro Coin", "Pumpkin Coin", "Mario Coin", "Turtle Coin",], self.player)

    def create_items(self):
        item_counts = {
            "Progressive Space Zone": 2,
            "Progressive Tree Zone": 3,
            "Progressive Macro Zone": 3,
            "Macro Zone Secret": 1,
            "Progressive Pumpkin Zone": 3,
            "Progressive Mario Zone": 3,
            "Progressive Turtle Zone": 2,
            "Tree Coin": 1,
            "Space Coin": 1,
            "Macro Coin": 1,
            "Pumpkin Coin": 1,
            "Mario Coin": 1,
            "Turtle Coin": 1,
            "Mushroom": 1,
            "Fire Flower": 1,
            "Carrot": 1,
            "Progressive Invincibility Star": 3,
            "Space Physics": 1,
        }

        if self.multiworld.difficulty_mode[self.player] == "easy_to_normal":
            item_counts["Normal Mode"] = 1
        else:
            item_counts["Easy Mode"] = 1

        for item_name, count in item_counts.items():
            for _ in range(count):
                classification = (ItemClassification.trap if item_name == "Normal Mode"
                                  else ItemClassification.useful if item_name == "Easy Mode"
                                  else ItemClassification.filler if item_name == "Progressive Invincibility Star"
                                  else ItemClassification.progression)
                self.multiworld.itempool.append(MarioLand2Item(item_name, classification, self.item_name_to_id[item_name], self.player))

    def fill_slot_data(self):
        return {
            "mode": self.multiworld.difficulty_mode[self.player].value
        }

    def get_filler_item_name(self):
        return "Progressive Invincibility Star"

    def modify_multidata(self, multidata: dict):
        rom_name = bytearray(f'AP{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0',
                             'utf8')[:21]
        rom_name.extend([0] * (21 - len(rom_name)))
        new_name = base64.b64encode(bytes(rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

class MarioLand2Item(Item):
    game = "Super Mario Land 2"