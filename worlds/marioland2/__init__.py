import base64

import Utils
import settings

from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Item, ItemClassification, Tutorial

from . import client
from .rom import generate_output, SuperMarioLand2DeltaPatch
from .options import SML2Options
from .locations import locations
from .items import items
from .logic import has_pipe_up, has_pipe_down, has_pipe_left, has_pipe_right, has_level_progression

START_IDS = 7770000


class MarioLand2Settings(settings.Group):
    class SML2RomFile(settings.UserFilePath):
        """File name of the Super Mario Land 2 1.0 ROM"""
        description = "Super Mario Land 2 - 6 Golden Coins (USA, Europe) 1.0 ROM File"
        copy_to = "Super Mario Land 2 - 6 Golden Coins (USA, Europe).gb"
        md5s = [SuperMarioLand2DeltaPatch.hash]

    rom_file: SML2RomFile = SML2RomFile(SML2RomFile.copy_to)


class MarioLand2WebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Super Mario Land 2 with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Alchav"]
    )

    tutorials = [setup_en]


class MarioLand2World(World):
    """Super Mario Land 2 is a classic platformer that follows Mario on a quest to reclaim his castle from the
    villainous Wario. This iconic game features 32 levels, unique power-ups, and introduces Wario as Mario's
    arch-rival."""  # -ChatGPT

    game = "Super Mario Land 2"

    settings_key = "sml2_options"
    settings: MarioLand2Settings

    location_name_to_id = {location_name: ID for ID, location_name in enumerate(locations, START_IDS)}
    item_name_to_id = {item_name: ID for ID, item_name in enumerate(items, START_IDS)}

    web = MarioLand2WebWorld()

    item_name_groups = {
        "Level Progression": {item_name for item_name in items if item_name.endswith("Progression")
                              or item_name.endswith("Secret")},
        "Bells": {item_name for item_name in items if "Bell" in item_name},
        "Coins": {item_name for item_name in items if "Coin" in item_name},
        "Powerups": {"Mushroom", "Fire Flower", "Carrot"},
        "Difficulties": {"Easy Mode", "Normal Mode"}
    }

    location_name_groups = {
        "Bosses": {
            "Tree Zone 5 - The Big Bird", "Space Zone 2 - Star Stage", "Macro Zone 4 - One Mighty Mouse",
            "Pumpkin Zone 4 - Witch's Mansion", "Mario Zone 4 - Three Mean Pigs!", "Turtle Zone 3 - Whale Course"
                   },
        "Normal Exits": {location for location in locations if locations[location]["type"] == "level"},
        "Secret Exits": {location for location in locations if locations[location]["type"] == "secret"},
        "Bells": {location for location in locations if locations[location]["type"] == "bell"},
    }

    options_dataclass = SML2Options
    options: SML2Options

    generate_output = generate_output

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        created_regions = []
        for location_name, data in locations.items():
            if "Secret Course" in location_name:
                region_name = location_name
            elif "Mushroom Zone" in location_name:
                region_name = "Mushroom Zone"
            else:
                region_name = location_name.split(" -")[0]
            if region_name in created_regions:
                region = self.multiworld.get_region(region_name, self.player)
            else:
                region = Region(region_name, self.player, self.multiworld)
                if location_name == "Tree Zone - Secret Course":
                    region_to_connect = self.multiworld.get_region("Tree Zone 2", self.player)
                elif location_name == "Space Zone - Secret Course":
                    region_to_connect = self.multiworld.get_region("Space Zone 1", self.player)
                elif location_name == "Macro Zone - Secret Course":
                    region_to_connect = self.multiworld.get_region("Macro Zone 1", self.player)
                elif location_name == "Pumpkin Zone - Secret Course 1":
                    region_to_connect = self.multiworld.get_region("Pumpkin Zone 2", self.player)
                elif location_name == "Pumpkin Zone - Secret Course 2":
                    region_to_connect = self.multiworld.get_region("Pumpkin Zone 3", self.player)
                elif location_name == "Turtle Zone - Secret Course":
                    region_to_connect = self.multiworld.get_region("Turtle Zone 2", self.player)
                elif "-" in location_name and int(location_name.split(" ")[2]) > 1:
                    region_to_connect = self.multiworld.get_region(" ".join(location_name.split(" ")[:2])
                                                                   + f" {int(location_name.split(' ')[2]) - 1}",
                                                                   self.player)
                else:
                    region_to_connect = menu_region
                region_to_connect.connect(region)
                self.multiworld.regions.append(region)
                created_regions.append(region_name)

            if "Midway Bell" in location_name and not self.options.shuffle_midway_bells:
                continue
            region.locations.append(MarioLand2Location(self.player, location_name,
                                                       self.location_name_to_id[location_name], region))
        self.multiworld.get_region("Macro Zone - Secret Course",
                                   self.player).connect(self.multiworld.get_region("Macro Zone 4", self.player))
        self.multiworld.get_region("Macro Zone 4",
                                   self.player).connect(self.multiworld.get_region("Macro Zone - Secret Course",
                                                                                   self.player))
        castle = Region("Mario's Castle", self.player, self.multiworld)
        menu_region.connect(castle)
        wario = MarioLand2Location(self.player, "Mario's Castle - Wario", parent=castle)
        castle.locations.append(wario)
        wario.place_locked_item(MarioLand2Item("Wario Defeated", ItemClassification.progression, None, self.player))

    def set_rules(self):
        entrance_rules = {
            "Menu -> Space Zone 1": lambda state: state.has_any(["Hippo Bubble", "Carrot"], self.player),
            "Space Zone 1 -> Space Zone - Secret Course": lambda state: state.has("Space Zone Secret", self.player),
            "Space Zone 1 -> Space Zone 2": lambda state: has_level_progression(state, "Space Zone Progression", self.player),
            "Tree Zone 1 -> Tree Zone 2": lambda state: has_level_progression(state, "Tree Zone Progression", self.player),
            "Tree Zone 2 -> Tree Zone - Secret Course": lambda state: state.has("Tree Zone Secret", self.player),
            "Tree Zone 2 -> Tree Zone 3": lambda state: has_level_progression(state, "Tree Zone Progression", self.player, 2),
            "Tree Zone 4 -> Tree Zone 5": lambda state: has_level_progression(state, "Tree Zone Progression", self.player, 3),
            "Macro Zone 1 -> Macro Zone - Secret Course": lambda state: state.has("Macro Zone Secret 1", self.player),
            "Macro Zone - Secret Course -> Macro Zone 4": lambda state: state.has("Macro Zone Secret 2", self.player),
            "Macro Zone 1 -> Macro Zone 2": lambda state: has_level_progression(state, "Macro Zone Progression", self.player),
            "Macro Zone 2 -> Macro Zone 3": lambda state: has_level_progression(state, "Macro Zone Progression", self.player, 2),
            "Macro Zone 3 -> Macro Zone 4": lambda state: has_level_progression(state, "Macro Zone Progression", self.player, 3),
            "Macro Zone 4 -> Macro Zone - Secret Course": lambda state: state.has("Macro Zone Secret 2", self.player),
            "Pumpkin Zone 1 -> Pumpkin Zone 2": lambda state: has_level_progression(state, "Pumpkin Zone Progression", self.player),
            "Pumpkin Zone 2 -> Pumpkin Zone - Secret Course 1": lambda state: state.has("Pumpkin Zone Secret 1", self.player),
            "Pumpkin Zone 2 -> Pumpkin Zone 3": lambda state: has_level_progression(state, "Pumpkin Zone Progression", self.player, 2),
            "Pumpkin Zone 3 -> Pumpkin Zone - Secret Course 2": lambda state: state.has("Pumpkin Zone Secret 2", self.player),
            "Pumpkin Zone 3 -> Pumpkin Zone 4": lambda state: has_level_progression(state, "Pumpkin Zone Progression", self.player, 3),
            "Mario Zone 1 -> Mario Zone 2": lambda state: has_level_progression(state, "Mario Zone Progression", self.player),
            "Mario Zone 2 -> Mario Zone 3": lambda state: has_level_progression(state, "Mario Zone Progression", self.player, 2),
            "Mario Zone 3 -> Mario Zone 4": lambda state: has_level_progression(state, "Mario Zone Progression", self.player, 3),
            "Turtle Zone 1 -> Turtle Zone 2": lambda state: has_level_progression(state, "Turtle Zone Progression", self.player),
            "Turtle Zone 2 -> Turtle Zone - Secret Course": lambda state: state.has("Turtle Zone Secret", self.player),
            "Turtle Zone 2 -> Turtle Zone 3": lambda state: has_level_progression(state, "Turtle Zone Progression", self.player, 2),
            "Menu -> Mario's Castle": lambda state: ([
                    state.has("Tree Coin", self.player), state.has("Space Coin", self.player),
                    state.has("Macro Coin", self.player), state.has("Pumpkin Coin", self.player),
                    state.has("Mario Coin", self.player), state.has("Turtle Coin", self.player)
                ].count(True) >= self.options.required_golden_coins)
        }
        location_rules = {
            "Hippo Zone": lambda state: state.has_any(["Hippo Bubble", "Carrot", "Swim"], self.player),
            # It is possible, however tricky, to beat the Moon Stage without Carrot or Space Physics.
            # However, it requires somewhat precisely jumping off enemies. Enemy shuffle may make this impossible.
            # I have not done any testing there. Instead, I will just always make one or the other required, since
            # it is difficult without them anyway.
            "Space Zone 1 - Moon Stage": lambda state: state.has_any(["Space Physics", "Carrot"], self.player),
            # One or the other is actually necessary for the secret exit.
            "Space Zone 1 - Moon Stage Secret Exit": lambda state: state.has_any(
                ["Space Physics", "Carrot"], self.player),
            # Without Space Physics, you must be able to take damage once to reach the bell, and again after the bell.
            # If bells are not shuffled, then any one powerup will do, as you can get the bell and come back.
            # Otherwise, you need the bell item from the item pool, or you need to be able to take damage twice in one
            # visit.
            "Space Zone 2 - Star Stage": lambda state: has_pipe_right(state, self.player) and (state.has(
                "Space Physics", self.player) or ((not
                state.multiworld.worlds[self.player].options.shuffle_midway_bells) and state.has_any(["Mushroom",
                "Fire Flower", "Carrot"], self.player)) or (state.has("Mushroom", self.player)
                and state.has_any(["Fire Flower", "Carrot"], self.player))
                or (state.has("Space Zone 2 - Star Stage Midway Bell", self.player) and state.has_any(["Mushroom",
                "Fire Flower", "Carrot"], self.player))),
            "Space Zone 2 - Star Stage Midway Bell": lambda state: state.has_any(
                ["Space Physics", "Space Zone 2 - Star Stage Midway Bell", "Mushroom", "Fire Flower", "Carrot"],
                self.player),
            "Tree Zone 2 - In the Trees": lambda state: has_pipe_right(state, self.player) or state.has(
                "Tree Zone 2 - In the Trees Midway Bell", self.player),
            "Tree Zone 2 - In the Trees Midway Bell": lambda state: has_pipe_right(state, self.player) or state.has(
                "Tree Zone 2 - In the Trees Midway Bell", self.player),
            "Tree Zone 2 - In the Trees Secret Exit": lambda state: has_pipe_right(state, self.player)
                                                                      and state.has("Carrot", self.player),
            "Tree Zone 4 - Honeybees": lambda state: has_pipe_down(state, self.player)
                and ((has_pipe_right(state, self.player) and has_pipe_up(state, self.player))
                or state.has("Tree Zone 4 - Honeybees Midway Bell", self.player)),
            "Tree Zone 4 - Honeybees Midway Bell": lambda state: ((has_pipe_right(state, self.player)
                and has_pipe_up(state, self.player)) or state.has("Tree Zone 4 - Honeybees Midway Bell", self.player)),
            "Tree Zone 5 - The Big Bird": lambda state: has_pipe_right(state, self.player)
                                                     and (has_pipe_up(state, self.player)
                                                          or state.has("Carrot", self.player)),
            "Macro Zone 1 - The Ant Monsters": lambda state: has_pipe_down(state, self.player)
                                                             or state.has("Macro Zone 1 - The Ant Monsters Midway Bell",
                                                                          self.player),
            "Macro Zone 1 - The Ant Monsters Midway Bell": lambda state: has_pipe_down(state, self.player)
                                                             or state.has("Macro Zone 1 - The Ant Monsters Midway Bell",
                                                                          self.player),
            "Macro Zone 1 - The Ant Monsters Secret Exit": lambda state: (has_pipe_down(state, self.player)
                or state.has("Macro Zone 1 - The Ant Monsters Midway Bell", self.player))
                and state.has("Fire Flower", self.player) and has_pipe_up(state, self.player),
            "Macro Zone 2 - In the Syrup Sea": lambda state: (has_pipe_down(state, self.player) or state.has(
                "Macro Zone 2 - In the Syrup Sea Midway Bell", self.player))
                and state.has("Swim", self.player) and has_pipe_up(state, self.player),
            "Macro Zone 2 - In the Syrup Sea Midway Bell": lambda state: (has_pipe_down(
                state, self.player) and state.has("Swim", self.player)) or state.has(
                "Macro Zone 2 - In the Syrup Sea Midway Bell", self.player),
            "Macro Zone 3 - Fiery Mario-Special Agent": lambda state: (has_pipe_down(state, self.player)
                and has_pipe_down(state, self.player)) or state.has(
                "Macro Zone 3 - Fiery Mario-Special Agent Midway Bell", self.player),
            "Macro Zone 3 - Fiery Mario-Special Agent Midway Bell": lambda state: (has_pipe_down(state, self.player)
                and has_pipe_down(state, self.player)) or state.has(
                "Macro Zone 3 - Fiery Mario-Special Agent Midway Bell", self.player),
            "Macro Zone 4 - One Mighty Mouse": lambda state: has_pipe_right(state, self.player),
            "Pumpkin Zone 1 - Bat Course": lambda state: has_pipe_down(state, self.player) or state.has(
                "Pumpkin Zone 1 - Bat Course Midway Bell", self.player),
            "Pumpkin Zone 1 - Bat Course Midway Bell": lambda state: has_pipe_down(state, self.player) or state.has(
                "Pumpkin Zone 1 - Bat Course Midway Bell", self.player),
            "Pumpkin Zone 2 - Cyclops Course": lambda state: has_pipe_down(state, self.player) and has_pipe_up(
                state, self.player) and has_pipe_right(state, self.player) and state.has("Swim", self.player),
            # You can only spin jump as Big Mario or Fire Mario
            "Pumpkin Zone 2 - Cyclops Course Secret Exit": lambda state: has_pipe_down(
                state, self.player) and has_pipe_up(state, self.player) and has_pipe_right(
                state, self.player) and state.has("Swim", self.player) and state.has_any(
                ["Mushroom", "Fire Flower"], self.player),
            "Pumpkin Zone 3 - Ghost House Secret Exit": lambda state: state.has("Carrot", self.player),
            "Pumpkin Zone 4 - Witch's Mansion": lambda state: has_pipe_right(state, self.player),
            "Mario Zone 1 - Fiery Blocks": lambda state: has_pipe_right(state, self.player),
            # It is possible to get as small mario, but it is a very precise jump and you will die afterward.
            "Mario Zone 1 - Fiery Blocks Midway Bell": lambda state: (state.has_any(
                ["Mushroom", "Fire Flower", "Carrot"], self.player) and has_pipe_right(state, self.player))
                or state.has("Mario Zone 1 - Fiery Blocks Midway Bell", self.player),
            "Mario Zone 4 - Three Mean Pigs!": lambda state: has_pipe_right(state, self.player),
            "Turtle Zone 2 - Turtle Zone": lambda state: has_pipe_up(state, self.player) and has_pipe_down(
                state, self.player) and has_pipe_right(state, self.player) and has_pipe_left(state, self.player)
                and state.has("Swim", self.player),
            "Turtle Zone 2 - Turtle Zone Midway Bell": lambda state: state.has_any(
                ["Swim", "Turtle Zone 2 - Turtle Zone Midway Bell"], self.player),
            "Turtle Zone 2 - Turtle Zone Secret Exit": lambda state: has_pipe_up(
                state, self.player) and state.has("Swim", self.player), #state.has_any(["Swim", "Turtle Zone 2 - Turtle Zone Midway Bell"], self.player),  # hard logic option?
            "Turtle Zone - Secret Course": lambda state: state.has_any(["Fire Flower", "Carrot"], self.player),
            "Turtle Zone 3 - Whale Course": lambda state: has_pipe_right(state, self.player),
            "Mario's Castle - Wario": lambda state: has_pipe_right(
                state, self.player) and has_pipe_left(state, self.player)
        }

        for entrance, rule in entrance_rules.items():
            self.multiworld.get_entrance(entrance, self.player).access_rule = rule

        for level, rule in location_rules.items():
            if ("Midway Bell" not in level) or self.options.shuffle_midway_bells:
                self.multiworld.get_location(level, self.player).access_rule = rule

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Wario Defeated", self.player)

    def create_items(self):
        item_counts = {
            "Space Zone Progression": 1,
            "Space Zone Secret": 1,
            "Tree Zone Progression": 1,
            "Tree Zone Progression x2": 1,
            "Tree Zone Secret": 1,
            "Macro Zone Progression": 1,
            "Macro Zone Progression x2": 1,
            "Macro Zone Secret 1": 1,
            "Macro Zone Secret 2": 1,
            "Pumpkin Zone Progression": 1,
            "Pumpkin Zone Progression x2": 1,
            "Pumpkin Zone Secret 1": 1,
            "Pumpkin Zone Secret 2": 1,
            "Mario Zone Progression": 1,
            "Mario Zone Progression x2": 1,
            "Turtle Zone Progression": 2,
            "Turtle Zone Secret": 1,
            "Mushroom": 1,
            "Fire Flower": 1,
            "Carrot": 1,
            "Space Physics": 1,
            "Hippo Bubble": 1,
            "Swim": 1,
            "Super Star Duration Increase": 6,
        }

        if self.options.coinsanity:
            for item in self.item_name_groups["Coins"]:
                item_counts[item] = 1
        else:
            for item, location_name in (
                    ("Mario Coin", "Mario Zone 4 - Three Mean Pigs!"),
                    ("Tree Coin", "Tree Zone 5 - The Big Bird"),
                    ("Space Coin", "Space Zone 2 - Star Stage"),
                    ("Macro Coin", "Macro Zone 4 - One Mighty Mouse"),
                    ("Pumpkin Coin", "Pumpkin Zone 4 - Witch's Mansion"),
                    ("Turtle Coin", "Turtle Zone 3 - Whale Course")
            ):
                location = self.multiworld.get_location(location_name, self.player)
                location.place_locked_item(self.create_item(item))
                location.address = None
                location.item.code = None

        if self.options.shuffle_midway_bells:
            for item in [item for item in items if "Midway Bell" in item]:
                item_counts[item] = 1

        if self.options.difficulty_mode == "easy_to_normal":
            item_counts["Normal Mode"] = 1
        elif self.options.difficulty_mode == "normal_to_easy":
            item_counts["Easy Mode"] = 1
        else:
            item_counts["Super Star Duration Increase"] += 1

        if self.options.shuffle_pipe_traversal == "single":
            item_counts["Super Star Duration Increase"] -= 1
            item_counts["Pipe Traversal"] = 1
        elif self.options.shuffle_pipe_traversal == "split":
            item_counts["Super Star Duration Increase"] -= 4
            item_counts["Pipe Traversal - Right"] = 1
            item_counts["Pipe Traversal - Left"] = 1
            item_counts["Pipe Traversal - Up"] = 1
            item_counts["Pipe Traversal - Down"] = 1
        else:
            self.multiworld.push_precollected(self.create_item("Pipe Traversal"))

        if self.options.auto_scroll_trap:
            item_counts["Super Star Duration Increase"] -= 1
            item_counts["Auto Scroll"] = 1

        for item in self.multiworld.precollected_items[self.player]:
            if item.name in item_counts and item_counts[item.name] > 0:
                item_counts[item.name] -= 1
                item_counts["Super Star Duration Increase"] += 1

        for item_name, count in item_counts.items():
            self.multiworld.itempool += [self.create_item(item_name) for _ in range(count)]

    def fill_slot_data(self):
        return {
            "mode": self.options.difficulty_mode.value,
            "stars": max(len([loc for loc in self.multiworld.get_filled_locations() if loc.item.player == self.player
                              and loc.item.name == "Super Star Duration Increase"]), 1),
            "midway_bells": self.options.shuffle_midway_bells.value,
            "energy_link": self.options.energy_link.value
        }

    def create_item(self, name: str) -> Item:
        return MarioLand2Item(name, items[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self):
        return "Super Star Duration Increase"

    def modify_multidata(self, multidata: dict):
        rom_name = bytearray(f'AP{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0',
                             'utf8')[:21]
        rom_name.extend([0] * (21 - len(rom_name)))
        new_name = base64.b64encode(bytes(rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]


class MarioLand2Location(Location):
    game = "Super Mario Land 2"


class MarioLand2Item(Item):
    game = "Super Mario Land 2"
