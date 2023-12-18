import base64

import Utils
import settings
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Item, ItemClassification

from . import client
from .rom import generate_output, SuperMarioLand2DeltaPatch
from .options import sml2options

START_IDS = 7770000

locations = {
    'Mushroom Zone': {'id': 0x00, 'ram_index': 0, 'type': 'level'},
    'Mushroom Zone Midway Bell': {'id': 0x00, 'ram_index': 0, 'clear_condition': ("Mushroom Zone Midway Bell", 1), 'type': 'bell'},
    'Scenic Course': {'id': 0x19, 'ram_index': 40, 'type': 'level'},
    'Tree Zone 1 - Invincibility!': {'id': 0x01, 'ram_index': 1, 'clear_condition': ("Progressive Tree Zone", 1), 'type': 'level'},
    'Tree Zone 1 - Invincibility! Midway Bell': {'id': 0x01, 'ram_index': 1,  'clear_condition': ("Tree Zone 1 - Invincibility! Midway Bell", 1), 'type': 'bell'},
    'Tree Zone 2 - In the Trees': {'id': 0x02, 'ram_index': 2, 'clear_condition': ("Progressive Tree Zone", 2), 'type': 'level'},
    'Tree Zone 2 - In the Trees Midway Bell': {'id': 0x02, 'ram_index': 2, 'clear_condition': ("Progressive Tree Zone", 2), 'type': 'bell'},
    'Tree Zone 3 - The Exit': {'id': 0x04, 'ram_index': 4, 'clear_condition': ("Progressive Tree Zone", 3), 'type': 'level'},
    'Tree Zone 4 - Honeybees': {'id': 0x03, 'ram_index': 3, 'clear_condition': ("Progressive Tree Zone", 3), 'type': 'level'},
    'Tree Zone 4 - Honeybees Midway Bell': {'id': 0x03, 'ram_index': 3, 'clear_condition': ("Tree Zone 4 - Honeybees Midway Bell", 1), 'type': 'bell'},
    'Tree Zone 5 - The Big Bird': {'id': 0x05, 'ram_index': 5, 'clear_condition': ("Tree Coin", 1), 'type': 'level'},
    'Tree Zone 5 - The Big Bird Midway Bell': {'id': 0x05, 'ram_index': 5, 'clear_condition': ("Tree Zone 5 - The Big Bird Midway Bell", 1), 'type': 'bell'},
    'Tree Zone - Secret Course': {'id': 0x1D, 'ram_index': 36, 'type': 'level'},
    'Hippo Zone': {'id': 0x11, 'ram_index': 31, 'type': 'level'},
    'Space Zone 1 - Moon Stage': {'id': 0x12, 'ram_index': 16, 'clear_condition': ("Progressive Space Zone", 2), 'type': 'level'},
    'Space Zone 1 - Moon Stage Midway Bell': {'id': 0x12, 'ram_index': 16, 'clear_condition': ("Space Zone 1 - Moon Stage Midway Bell", 1), 'type': 'bell'},
    'Space Zone - Secret Course': {'id': 0x1C, 'ram_index': 41, 'type': 'level'},
    'Space Zone 2 - Star Stage': {'id': 0x13, 'ram_index': 17, 'clear_condition': ("Space Coin", 1), 'type': 'level'},
    'Space Zone 2 - Star Stage Midway Bell': {'id': 0x13, 'ram_index': 17, 'clear_condition': ("Space Zone 2 - Star Stage Midway Bell", 1), 'type': 'bell'},
    'Macro Zone 1 - The Ant Monsters': {'id': 0x14, 'ram_index': 11, 'clear_condition': ("Progressive Macro Zone", 1), 'type': 'level'},
    'Macro Zone 1 - The Ant Monsters Midway Bell': {'id': 0x14, 'ram_index': 11, 'clear_condition': ("Macro Zone 1 - The Ant Monsters Midway Bell", 1), 'type': 'bell'},
    'Macro Zone 2 - In the Syrup Sea': {'id': 0x15, 'ram_index': 12, 'clear_condition': ("Progressive Macro Zone", 2), 'type': 'level'},
    'Macro Zone 2 - In the Syrup Sea Midway Bell': {'id': 0x15, 'ram_index': 12, 'clear_condition': ("Macro Zone 2 - In the Syrup Sea Midway Bell", 1), 'type': 'bell'},
    'Macro Zone 3 - Fiery Mario-Special Agent': {'id': 0x16, 'ram_index': 13, 'clear_condition': ("Progressive Macro Zone", 3), 'type': 'level'},
    'Macro Zone 3 - Fiery Mario-Special Agent Midway Bell': {'id': 0x16, 'ram_index': 13, 'clear_condition': ("Macro Zone 3 - Fiery Mario-Special Agent Midway Bell", 1), 'type': 'bell'},
    'Macro Zone 4 - One Mighty Mouse': {'id': 0x17, 'ram_index': 14, 'clear_condition': ("Macro Coin", 1), 'type': 'level'},
    'Macro Zone 4 - One Mighty Mouse Midway Bell': {'id': 0x17, 'ram_index': 14, 'clear_condition': ("Macro Zone 4 - One Mighty Mouse Midway Bell", 1), 'type': 'bell'},
    'Macro Zone - Secret Course': {'id': 0x1E, 'ram_index': 35, 'clear_condition': ("Macro Zone Secret", 1), 'type': 'level'},
    'Pumpkin Zone 1 - Bat Course': {'id': 0x06, 'ram_index': 6, 'clear_condition': ("Progressive Pumpkin Zone", 1), 'type': 'level'},
    'Pumpkin Zone 1 - Bat Course Midway Bell': {'id': 0x06, 'ram_index': 6, 'clear_condition': ("Pumpkin Zone 1 - Bat Course Midway Bell", 1), 'type': 'bell'},
    'Pumpkin Zone 2 - Cyclops Course': {'id': 0x07, 'ram_index': 7, 'clear_condition': ("Progressive Pumpkin Zone", 2), 'type': 'level'},
    'Pumpkin Zone 2 - Cyclops Course Midway Bell': {'id': 0x07, 'ram_index': 7, 'clear_condition': ("Progressive Pumpkin Zone", 2), 'type': 'bell'},
    'Pumpkin Zone 3 - Ghost House': {'id': 0x08, 'ram_index': 8, 'clear_condition': ("Progressive Pumpkin Zone", 3), 'type': 'level'},
    'Pumpkin Zone 3 - Ghost House Midway Bell': {'id': 0x08, 'ram_index': 8, 'clear_condition': ("Progressive Pumpkin Zone", 3), 'type': 'bell'},
    "Pumpkin Zone 4 - Witch's Mansion": {'id': 0x09, 'ram_index': 9, 'clear_condition': ("Pumpkin Coin", 1), 'type': 'level'},
    "Pumpkin Zone 4 - Witch's Mansion Midway Bell": {'id': 0x09, 'ram_index': 9, 'clear_condition': ("Pumpkin Coin", 1), 'type': 'bell'},
    'Pumpkin Zone - Secret Course 1': {'id': 0x1B, 'ram_index': 38, 'type': 'level'},
    'Pumpkin Zone - Secret Course 2': {'id': 0x1F, 'ram_index': 39, 'type': 'level'},
    'Mario Zone 1 - Fiery Blocks': {'id': 0x0A, 'ram_index': 26, 'clear_condition': ("Progressive Mario Zone", 1), 'type': 'level'},
    'Mario Zone 1 - Fiery Blocks Midway Bell': {'id': 0x0A, 'ram_index': 26, 'clear_condition': ("Mario Zone 1 - Fiery Blocks Midway Bell", 1), 'type': 'bell'},
    'Mario Zone 2 - Mario the Circus Star!': {'id': 0x0B, 'ram_index': 27, 'clear_condition': ("Progressive Mario Zone", 2), 'type': 'level'},
    'Mario Zone 2 - Mario the Circus Star! Midway Bell': {'id': 0x0B, 'ram_index': 27, 'clear_condition': ("Mario Zone 2 - Mario the Circus Star! Midway Bell", 1), 'type': 'bell'},
    'Mario Zone 3 - Beware: Jagged Spikes': {'id': 0x0C, 'ram_index': 28, 'clear_condition': ("Progressive Mario Zone", 3), 'type': 'level'},
    'Mario Zone 3 - Beware: Jagged Spikes Midway Bell': {'id': 0x0C, 'ram_index': 28, 'clear_condition': ("Mario Zone 3 - Beware: Jagged Spikes Midway Bell", 1), 'type': 'bell'},
    'Mario Zone 4 - Three Mean Pigs!': {'id': 0x0D, 'ram_index': 29, 'clear_condition': ("Mario Coin", 1), 'type': 'level'},
    'Mario Zone 4 - Three Mean Pigs! Midway Bell': {'id': 0x0D, 'ram_index': 29, 'clear_condition': ("Mario Zone 4 - Three Mean Pigs! Midway Bell", 1), 'type': 'bell'},
    'Turtle Zone 1 - Cheep Cheep Course': {'id': 0x0E, 'ram_index': 21, 'clear_condition': ("Progressive Turtle Zone", 1), 'type': 'level'},
    'Turtle Zone 1 - Cheep Cheep Course Midway Bell': {'id': 0x0E, 'ram_index': 21, 'clear_condition': ("Turtle Zone 1 - Cheep Cheep Course Midway Bell", 1), 'type': 'bell'},
    'Turtle Zone 2 - Turtle Zone': {'id': 0x0F, 'ram_index': 22, 'clear_condition': ("Progressive Turtle Zone", 2), 'type': 'level'},
    'Turtle Zone 2 - Turtle Zone Midway Bell': {'id': 0x0F, 'ram_index': 22, 'clear_condition': ("Turtle Zone 2 - Turtle Zone Midway Bell", 1), 'type': 'bell'},
    'Turtle Zone 3 - Whale Course': {'id': 0x10, 'ram_index': 23, 'clear_condition': ("Turtle Coin", 1), 'type': 'level'},
    'Turtle Zone 3 - Whale Course Midway Bell': {'id': 0x10, 'ram_index': 23, 'clear_condition': ("Turtle Zone 3 - Whale Course Midway Bell", 1), 'type': 'bell'},
    'Turtle Zone - Secret Course': {'id': 0x1A, 'ram_index': 37, 'type': 'level'}
}

items = {
    "Progressive Space Zone": ItemClassification.progression,
    "Progressive Tree Zone": ItemClassification.progression,
    "Progressive Macro Zone": ItemClassification.progression,
    "Macro Zone Secret": ItemClassification.progression_skip_balancing,
    "Progressive Pumpkin Zone": ItemClassification.progression,
    "Progressive Mario Zone": ItemClassification.progression,
    "Progressive Turtle Zone": ItemClassification.progression,
    "Tree Coin": ItemClassification.progression_skip_balancing,
    "Space Coin": ItemClassification.progression_skip_balancing,
    "Macro Coin": ItemClassification.progression_skip_balancing,
    "Pumpkin Coin": ItemClassification.progression_skip_balancing,
    "Mario Coin": ItemClassification.progression_skip_balancing,
    "Turtle Coin": ItemClassification.progression_skip_balancing,
    "Mushroom": ItemClassification.progression,
    "Fire Flower": ItemClassification.progression,
    "Carrot": ItemClassification.progression,
    "Progressive Invincibility Star": ItemClassification.filler,
    "Space Physics": ItemClassification.progression,
    "Easy Mode": ItemClassification.useful,
    "Normal Mode": ItemClassification.trap,
    "Auto Scroll": ItemClassification.trap,
    "Mushroom Zone Midway Bell": ItemClassification.filler,
    "Tree Zone 1 - Invincibility! Midway Bell": ItemClassification.filler,
    "Tree Zone 3 - The Exit Midway Bell": ItemClassification.filler,
    "Tree Zone 4 - Honeybees Midway Bell": ItemClassification.filler,
    "Tree Zone 5 - The Big Bird Midway Bell": ItemClassification.filler,
    "Space Zone 1 - Moon Stage Midway Bell": ItemClassification.filler,
    "Space Zone 2 - Star Stage Midway Bell": ItemClassification.filler,
    "Macro Zone 1 - The Ant Monsters Midway Bell": ItemClassification.filler,
    "Macro Zone 2 - In the Syrup Sea Midway Bell": ItemClassification.filler,
    "Macro Zone 3 - Fiery Mario-Special Agent Midway Bell": ItemClassification.filler,
    "Macro Zone 4 - One Mighty Mouse Midway Bell": ItemClassification.filler,
    "Pumpkin Zone 1 - Bat Course Midway Bell": ItemClassification.filler,
    "Pumpkin Zone 2 - Cyclops Course Midway Bell": ItemClassification.filler,
    "Pumpkin Zone 3 - Ghost House Midway Bell": ItemClassification.filler,
    "Pumpkin Zone 4 - Witch's Mansion Midway Bell": ItemClassification.filler,
    "Mario Zone 1 - Fiery Blocks Midway Bell": ItemClassification.filler,
    "Mario Zone 2 - Mario the Circus Star! Midway Bell": ItemClassification.filler,
    "Mario Zone 3 - Beware: Jagged Spikes Midway Bell": ItemClassification.filler,
    "Mario Zone 4 - Three Mean Pigs! Midway Bell": ItemClassification.filler,
    "Turtle Zone 1 - Cheep Cheep Course Midway Bell": ItemClassification.filler,
    "Turtle Zone 2 - Turtle Zone Midway Bell": ItemClassification.filler,
    "Turtle Zone 3 - Whale Course Midway Bell": ItemClassification.filler,
}


class MarioLand2Settings(settings.Group):
    class SML2RomFile(settings.UserFilePath):
        """File name of the Super Mario Land 2 1.0 ROM"""
        description = "Super Mario Land 2 - 6 Golden Coins (USA, Europe) 1.0 ROM File"
        copy_to = "Super Mario Land 2 - 6 Golden Coins (USA, Europe).gb"
        md5s = [SuperMarioLand2DeltaPatch.hash]

    rom_file: SML2RomFile = SML2RomFile(SML2RomFile.copy_to)


class MarioLand2World(World):
    game = "Super Mario Land 2"

    settings_key = "sml2_options"
    settings: MarioLand2Settings

    location_name_to_id = {location_name: ID for ID, location_name in enumerate(locations, START_IDS)}
    item_name_to_id = {item_name: ID for ID, item_name in enumerate(items, START_IDS)}

    item_name_groups = {
        "Coins": {item_name for item_name in items if "Coin" in item_name},
        "Powerups": {"Mushroom", "Fire Flower", "Carrot"},
        "Difficulties": {"Easy Mode", "Normal Mode"}
    }

    location_name_groups = {
        "Bosses": {
            "Tree Zone 5 - The Big Bird", "Space Zone 2 - Star Stage", "Macro Zone 4 - One Mighty Mouse",
            "Pumpkin Zone 4 - Witch's Mansion", "Mario Zone 4 - Three Mean Pigs!", "Turtle Zone 3 - Whale Course"
                   }
    }

    option_definitions = sml2options

    generate_output = generate_output

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        for location_name in locations:
            if "Midway Bell" in location_name and not self.multiworld.shuffle_midway_bells[self.player]:
                continue
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
            # You can use a Fire Flower to get the Secret Course from Macro Zone 1, or if you have every Progressive
            # Macro Zone and the Macro Zone Secret paths, you can get here from the boss level
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
            # The powerups are needed not for the secret exit in Turtle Zone 2, but to fly over or take damage in the
            # spikes in the secret course
            "Turtle Zone - Secret Course": lambda state: state.has("Progressive Turtle Zone", self.player) and state.has_any(["Mushroom", "Fire Flower", "Carrot"], self.player),
            "Turtle Zone 3 - Whale Course": lambda state: state.has("Progressive Turtle Zone", self.player, 2),
        }

        if self.multiworld.shuffle_midway_bells[self.player]:
            # copy level access rules onto midway point rules
            for midway_loc in [loc for loc in locations if "Midway Bell" in loc]:
                level_loc = midway_loc[:-12]
                if level_loc in rules:
                    rules[midway_loc] = rules[level_loc]

        for level, rule in rules.items():
            self.multiworld.get_location(level, self.player).access_rule = rule

        if self.multiworld.golden_coins[self.player] == "progressive":
            self.multiworld.completion_condition[self.player] = lambda state: [
                state.has("Progressive Space Zone", self.player, 3),
                state.has("Progressive Tree Zone", self.player, 4),
                state.has("Progressive Macro Zone", self.player, 4),
                state.has("Progressive Pumpkin Zone", self.player, 4),
                state.has("Progressive Mario Zone", self.player, 4),
                state.has("Progressive Turtle Zone", self.player, 3)
                ].count(True) >= self.multiworld.required_golden_coins[self.player]
        else:
            self.multiworld.completion_condition[self.player] = lambda state: [
                state.has("Tree Coin", self.player), state.has("Space Coin", self.player),
                state.has("Macro Coin", self.player), state.has("Pumpkin Coin", self.player),
                state.has("Mario Coin", self.player), state.has("Turtle Coin", self.player)
                ].count(True) >= self.multiworld.required_golden_coins[self.player]

    def create_items(self):
        item_counts = {
            "Progressive Space Zone": 2,
            "Progressive Tree Zone": 3,
            "Progressive Macro Zone": 3,
            "Macro Zone Secret": 1,
            "Progressive Pumpkin Zone": 3,
            "Progressive Mario Zone": 3,
            "Progressive Turtle Zone": 2,
            "Mushroom": 1,
            "Fire Flower": 1,
            "Carrot": 1,
            "Progressive Invincibility Star": 4,
        }

        if self.multiworld.golden_coins[self.player] == "vanilla":
            for item, location_name in (
                    ("Macro Coin", "Mario Zone 4 - Three Mean Pigs!"),
                    ("Mario Coin", "Tree Zone 5 - The Big Bird"),
                    ("Space Coin", "Space Zone 2 - Star Stage"),
                    ("Pumpkin Coin", "Macro Zone 4 - One Mighty Mouse"),
                    ("Turtle Coin", "Pumpkin Zone 4 - Witch's Mansion"),
                    ("Tree Coin", "Turtle Zone 3 - Whale Course")
            ):
                location = self.multiworld.get_location(location_name, self.player)
                location.place_locked_item(self.create_item(item))
                location.address = None
                location.item.code = None
        elif self.multiworld.golden_coins[self.player] == "shuffled":
            for item in self.item_name_groups["Coins"]:
                item_counts[item] = 1
        elif self.multiworld.golden_coins[self.player] == "progressive":
            for item in [item for item in items if "Progressive" in item and "Zone" in item]:
                item_counts[item] += 1

        if self.multiworld.shuffle_midway_bells[self.player]:
            for item in [item for item in items if "Midway Bell" in item]:
                item_counts[item] = 1

        if self.multiworld.difficulty_mode[self.player] == "easy_to_normal":
            item_counts["Normal Mode"] = 1
        elif self.multiworld.difficulty_mode[self.player] == "normal_to_easy":
            item_counts["Easy Mode"] = 1
        else:
            item_counts["Progressive Invincibility Star"] += 1

        if self.multiworld.shuffle_space_physics[self.player]:
            item_counts["Progressive Invincibility Star"] -= 1
            item_counts["Space Physics"] = 1
        else:
            self.multiworld.push_precollected(self.create_item("Space Physics"))

        if self.multiworld.auto_scroll_trap[self.player]:
            item_counts["Progressive Invincibility Star"] -= 1
            item_counts["Auto Scroll"] = 1

        for item_name, count in item_counts.items():
            self.multiworld.itempool += [self.create_item(item_name) for _ in range(count)]

    def fill_slot_data(self):
        return {
            "mode": self.multiworld.difficulty_mode[self.player].value,
            "stars": max(len([loc for loc in self.multiworld.get_filled_locations() if loc.item.player == self.player
                              and loc.item.name == "Progressive Invincibility Star"]), 1),
            "midway_bells": self.multiworld.shuffle_midway_bells[self.player].value
        }

    def create_item(self, name: str) -> Item:
        return MarioLand2Item(name, items[name], self.item_name_to_id[name], self.player)

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