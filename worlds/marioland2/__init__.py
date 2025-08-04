import base64
import Utils
import settings
from copy import deepcopy

from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Item, ItemClassification, Tutorial

from . import client
from .rom import generate_output, SuperMarioLand2ProcedurePatch
from .options import SML2Options
from .locations import (locations, location_name_to_id, level_name_to_id, level_id_to_name, START_IDS, coins_coords,
                        auto_scroll_max)
from .items import items
from .sprites import level_sprites
from .sprite_randomizer import randomize_enemies, randomize_platforms
from .logic import has_pipe_up, has_pipe_down, has_pipe_left, has_pipe_right, has_level_progression, is_auto_scroll
from . import logic


class MarioLand2Settings(settings.Group):
    class SML2RomFile(settings.UserFilePath):
        """File name of the Super Mario Land 2 1.0 ROM"""
        description = "Super Mario Land 2 - 6 Golden Coins (USA, Europe) 1.0 ROM File"
        copy_to = "Super Mario Land 2 - 6 Golden Coins (USA, Europe).gb"
        md5s = [SuperMarioLand2ProcedurePatch.hash]

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

    location_name_to_id = location_name_to_id
    item_name_to_id = {item_name: ID for ID, item_name in enumerate(items, START_IDS)}

    web = MarioLand2WebWorld()

    item_name_groups = {
        "Level Progression": {
            item_name for item_name in items if item_name.endswith(("Progression", "Secret", "Secret 1", "Secret 2"))
                                                and "Auto Scroll" not in item_name
        },
        "Bells": {item_name for item_name in items if "Bell" in item_name},
        "Golden Coins": {"Mario Coin", "Macro Coin", "Space Coin", "Tree Coin", "Turtle Coin", "Pumpkin Coin"},
        "Coins": {"1 Coin", *{f"{i} Coins" for i in range(2, 169)}},
        "Powerups": {"Mushroom", "Fire Flower", "Carrot"},
        "Difficulties": {"Easy Mode", "Normal Mode"},
        "Auto Scroll Traps": {item_name for item_name in items
                              if "Auto Scroll" in item_name and "Cancel" not in item_name},
        "Cancel Auto Scrolls": {item_name for item_name in items if "Cancel Auto Scroll" in item_name},
    }

    location_name_groups = {
        "Bosses": {
            "Tree Zone 5 - Boss", "Space Zone 2 - Boss", "Macro Zone 4 - Boss",
            "Pumpkin Zone 4 - Boss", "Mario Zone 4 - Boss", "Turtle Zone 3 - Boss"
                   },
        "Normal Exits": {location for location in locations if locations[location]["type"] == "level"},
        "Secret Exits": {location for location in locations if locations[location]["type"] == "secret"},
        "Bells": {location for location in locations if locations[location]["type"] == "bell"},
        "Coins": {location for location in location_name_to_id if "Coin" in location}
    }

    options_dataclass = SML2Options
    options: SML2Options

    generate_output = generate_output

    def __init__(self, world, player: int):
        super().__init__(world, player)
        self.auto_scroll_levels = []
        self.num_coin_locations = []
        self.max_coin_locations = {}
        self.sprite_data = {}
        self.coin_fragments_required = 0

    def generate_early(self):
        self.sprite_data = deepcopy(level_sprites)
        if self.options.randomize_enemies:
            randomize_enemies(self.sprite_data, self.random)
        if self.options.randomize_platforms:
            randomize_platforms(self.sprite_data, self.random)

        if self.options.marios_castle_midway_bell:
            self.sprite_data["Mario's Castle"][35]["sprite"] = "Midway Bell"

        if self.options.auto_scroll_chances == "vanilla":
            self.auto_scroll_levels = [int(i in [19, 25, 30]) for i in range(32)]
        else:
            self.auto_scroll_levels = [int(self.random.randint(1, 100) <= self.options.auto_scroll_chances)
                                       for _ in range(32)]

        self.auto_scroll_levels[level_name_to_id["Mario's Castle"]] = 0
        unbeatable_scroll_levels = ["Tree Zone 3", "Macro Zone 2", "Space Zone 1", "Turtle Zone 2", "Pumpkin Zone 2"]
        if not self.options.shuffle_midway_bells:
            unbeatable_scroll_levels.append("Pumpkin Zone 1")
        for level, i in enumerate(self.auto_scroll_levels):
            if i == 1:
                if self.options.auto_scroll_mode in ("global_cancel_item", "level_cancel_items"):
                    self.auto_scroll_levels[level] = 2
                elif self.options.auto_scroll_mode == "chaos":
                    if (self.options.accessibility == "full"
                            and level_id_to_name[level] in unbeatable_scroll_levels):
                        self.auto_scroll_levels[level] = 2
                    else:
                        self.auto_scroll_levels[level] = self.random.randint(1, 3)
                elif (self.options.accessibility == "full"
                      and level_id_to_name[level] in unbeatable_scroll_levels):
                    self.auto_scroll_levels[level] = 0
                if self.auto_scroll_levels[level] == 1 and "trap" in self.options.auto_scroll_mode.current_key:
                    self.auto_scroll_levels[level] = 3

    def create_regions(self):
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)
        created_regions = []
        for location_name, data in locations.items():
            region_name = location_name.split(" -")[0]
            if region_name in created_regions:
                region = self.multiworld.get_region(region_name, self.player)
            else:
                region = Region(region_name, self.player, self.multiworld)
                if region_name == "Tree Zone Secret Course":
                    region_to_connect = self.multiworld.get_region("Tree Zone 2", self.player)
                elif region_name == "Space Zone Secret Course":
                    region_to_connect = self.multiworld.get_region("Space Zone 1", self.player)
                elif region_name == "Macro Zone Secret Course":
                    region_to_connect = self.multiworld.get_region("Macro Zone 1", self.player)
                elif region_name == "Pumpkin Zone Secret Course 1":
                    region_to_connect = self.multiworld.get_region("Pumpkin Zone 2", self.player)
                elif region_name == "Pumpkin Zone Secret Course 2":
                    region_to_connect = self.multiworld.get_region("Pumpkin Zone 3", self.player)
                elif region_name == "Turtle Zone Secret Course":
                    region_to_connect = self.multiworld.get_region("Turtle Zone 2", self.player)
                elif region_name.split(" ")[-1].isdigit() and int(region_name.split(" ")[-1]) > 1:
                    region_to_connect = self.multiworld.get_region(" ".join(region_name.split(" ")[:2])
                                                                   + f" {int(region_name.split(' ')[2]) - 1}",
                                                                   self.player)
                else:
                    region_to_connect = menu_region
                region_to_connect.connect(region)
                self.multiworld.regions.append(region)
                created_regions.append(region_name)

            if location_name == "Mario's Castle - Midway Bell" and not self.options.marios_castle_midway_bell:
                continue
            region.locations.append(MarioLand2Location(self.player, location_name,
                                                       self.location_name_to_id[location_name], region))
        self.multiworld.get_region("Macro Zone Secret Course", self.player).connect(
            self.multiworld.get_region("Macro Zone 4", self.player))
        self.multiworld.get_region("Macro Zone 4", self.player).connect(
            self.multiworld.get_region("Macro Zone Secret Course", self.player))

        castle = self.multiworld.get_region("Mario's Castle", self.player)
        wario = MarioLand2Location(self.player, "Mario's Castle - Wario", parent=castle)
        castle.locations.append(wario)
        wario.place_locked_item(MarioLand2Item("Wario Defeated", ItemClassification.progression, None, self.player))

        if self.options.coinsanity:
            coinsanity_checks = self.options.coinsanity_checks.value
            self.num_coin_locations = [[region, 1] for region in created_regions if region != "Mario's Castle"]
            self.max_coin_locations = {region: len(coins_coords[region]) for region in created_regions
                                       if region != "Mario's Castle"}
            if self.options.accessibility == "full" or self.options.auto_scroll_mode == "always":
                for level in self.max_coin_locations:
                    if level in auto_scroll_max and self.auto_scroll_levels[level_name_to_id[level]] in (1, 3):
                        if isinstance(auto_scroll_max[level], tuple):
                            self.max_coin_locations[level] = min(
                                auto_scroll_max[level][int(self.options.shuffle_midway_bells.value)],
                                self.max_coin_locations[level])
                        else:
                            self.max_coin_locations[level] = min(auto_scroll_max[level], self.max_coin_locations[level])
            coinsanity_checks = min(sum(self.max_coin_locations.values()), coinsanity_checks)
            for i in range(coinsanity_checks - 31):
                self.num_coin_locations.sort(key=lambda region: self.max_coin_locations[region[0]] / region[1])
                self.num_coin_locations[-1][1] += 1
            coin_locations = []
            for level, coins in self.num_coin_locations:
                if self.max_coin_locations[level]:
                    coin_thresholds = self.random.sample(range(1, self.max_coin_locations[level] + 1), coins)
                    coin_locations += [f"{level} - {i} Coin{'s' if i > 1 else ''}" for i in coin_thresholds]
            for location_name in coin_locations:
                region = self.multiworld.get_region(location_name.split(" -")[0], self.player)
                region.locations.append(MarioLand2Location(self.player, location_name,
                                                           self.location_name_to_id[location_name], parent=region))

    def set_rules(self):
        entrance_rules = {
            "Menu -> Space Zone 1": lambda state: state.has("Hippo Bubble", self.player)
                                                  or (state.has("Carrot", self.player)
                                                      and not is_auto_scroll(state, self.player, "Hippo Zone")),
            "Space Zone 1 -> Space Zone Secret Course": lambda state: state.has("Space Zone Secret", self.player),
            "Space Zone 1 -> Space Zone 2": lambda state: has_level_progression(state, "Space Zone Progression", self.player),
            "Tree Zone 1 -> Tree Zone 2": lambda state: has_level_progression(state, "Tree Zone Progression", self.player),
            "Tree Zone 2 -> Tree Zone Secret Course": lambda state: state.has("Tree Zone Secret", self.player),
            "Tree Zone 2 -> Tree Zone 3": lambda state: has_level_progression(state, "Tree Zone Progression", self.player, 2),
            "Tree Zone 4 -> Tree Zone 5": lambda state: has_level_progression(state, "Tree Zone Progression", self.player, 3),
            "Macro Zone 1 -> Macro Zone Secret Course": lambda state: state.has("Macro Zone Secret 1", self.player),
            "Macro Zone Secret Course -> Macro Zone 4": lambda state: state.has("Macro Zone Secret 2", self.player),
            "Macro Zone 1 -> Macro Zone 2": lambda state: has_level_progression(state, "Macro Zone Progression", self.player),
            "Macro Zone 2 -> Macro Zone 3": lambda state: has_level_progression(state, "Macro Zone Progression", self.player, 2),
            "Macro Zone 3 -> Macro Zone 4": lambda state: has_level_progression(state, "Macro Zone Progression", self.player, 3),
            "Macro Zone 4 -> Macro Zone Secret Course": lambda state: state.has("Macro Zone Secret 2", self.player),
            "Pumpkin Zone 1 -> Pumpkin Zone 2": lambda state: has_level_progression(state, "Pumpkin Zone Progression", self.player),
            "Pumpkin Zone 2 -> Pumpkin Zone Secret Course 1": lambda state: state.has("Pumpkin Zone Secret 1", self.player),
            "Pumpkin Zone 2 -> Pumpkin Zone 3": lambda state: has_level_progression(state, "Pumpkin Zone Progression", self.player, 2),
            "Pumpkin Zone 3 -> Pumpkin Zone Secret Course 2": lambda state: state.has("Pumpkin Zone Secret 2", self.player),
            "Pumpkin Zone 3 -> Pumpkin Zone 4": lambda state: has_level_progression(state, "Pumpkin Zone Progression", self.player, 3),
            "Mario Zone 1 -> Mario Zone 2": lambda state: has_level_progression(state, "Mario Zone Progression", self.player),
            "Mario Zone 2 -> Mario Zone 3": lambda state: has_level_progression(state, "Mario Zone Progression", self.player, 2),
            "Mario Zone 3 -> Mario Zone 4": lambda state: has_level_progression(state, "Mario Zone Progression", self.player, 3),
            "Turtle Zone 1 -> Turtle Zone 2": lambda state: has_level_progression(state, "Turtle Zone Progression", self.player),
            "Turtle Zone 2 -> Turtle Zone Secret Course": lambda state: state.has("Turtle Zone Secret", self.player),
            "Turtle Zone 2 -> Turtle Zone 3": lambda state: has_level_progression(state, "Turtle Zone Progression", self.player, 2),
        }

        if self.options.shuffle_golden_coins == "mario_coin_fragment_hunt":
            # Require the other coins just to ensure they are being added to start inventory properly,
            # and so they show up in Playthrough as required
            entrance_rules["Menu -> Mario's Castle"] = lambda state: (state.has_all(
                ["Tree Coin", "Space Coin", "Macro Coin", "Pumpkin Coin", "Turtle Coin"], self.player)
                and state.has("Mario Coin Fragment", self.player, self.coin_fragments_required))
        else:
            entrance_rules["Menu -> Mario's Castle"] = lambda state: state.has_from_list_unique([
                "Tree Coin", "Space Coin", "Macro Coin", "Pumpkin Coin", "Mario Coin", "Turtle Coin"
                ], self.player, self.options.required_golden_coins)


        for entrance, rule in entrance_rules.items():
            self.multiworld.get_entrance(entrance, self.player).access_rule = rule

        for location in self.multiworld.get_locations(self.player):
            if location.name.endswith(("Coins", "Coin")):
                rule = getattr(logic, location.parent_region.name.lower().replace(" ", "_") + "_coins", None)
                if rule:
                    coins = int(location.name.split(" ")[-2])
                    location.access_rule = lambda state, coin_rule=rule, num_coins=coins: \
                        coin_rule(state, self.player, num_coins)
            else:
                rule = getattr(logic, location.name.lower().replace(
                    " - ", "_").replace(" ", "_").replace("'", ""), None)
                if rule:
                    location.access_rule = lambda state, loc_rule=rule: loc_rule(state, self.player)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Wario Defeated", self.player)

    def create_items(self):
        item_counts = {
            "Space Zone Progression": 1,
            "Space Zone Secret": 1,
            "Tree Zone Progression": 3,
            "Tree Zone Secret": 1,
            "Macro Zone Progression": 3,
            "Macro Zone Secret 1": 1,
            "Macro Zone Secret 2": 1,
            "Pumpkin Zone Progression": 3,
            "Pumpkin Zone Secret 1": 1,
            "Pumpkin Zone Secret 2": 1,
            "Mario Zone Progression": 3,
            "Turtle Zone Progression": 2,
            "Turtle Zone Secret": 1,
            "Mushroom": 1,
            "Fire Flower": 1,
            "Carrot": 1,
            "Space Physics": 1,
            "Hippo Bubble": 1,
            "Water Physics": 1,
            "Super Star Duration Increase": 2,
            "Mario Coin Fragment": 0,
        }

        if self.options.shuffle_golden_coins == "mario_coin_fragment_hunt":
            # There are 5 Zone Progression items that can be condensed.
            item_counts["Mario Coin Fragment"] = 1 + ((5 * self.options.mario_coin_fragment_percentage) // 100)

        if self.options.coinsanity:
            coin_count = sum([level[1] for level in self.num_coin_locations])
            max_coins = sum(self.max_coin_locations.values())
            if self.options.shuffle_golden_coins == "mario_coin_fragment_hunt":
                removed_coins = (coin_count * self.options.mario_coin_fragment_percentage) // 100
                coin_count -= removed_coins
                item_counts["Mario Coin Fragment"] += removed_coins
                # Randomly remove some coin items for variety
                coin_count -= (coin_count // self.random.randint(100, max(100, coin_count)))

            if coin_count:
                coin_bundle_sizes = [max_coins // coin_count] * coin_count
                remainder = max_coins - sum(coin_bundle_sizes)
                for i in range(remainder):
                    coin_bundle_sizes[i] += 1
                for a, b in zip(range(1, len(coin_bundle_sizes), 2), range(2, len(coin_bundle_sizes), 2)):
                    split = self.random.randint(1, coin_bundle_sizes[a] + coin_bundle_sizes[b] - 1)
                    coin_bundle_sizes[a], coin_bundle_sizes[b] = split, coin_bundle_sizes[a] + coin_bundle_sizes[b] - split
                for coin_bundle_size in coin_bundle_sizes:
                    item_name = f"{coin_bundle_size} Coin{'s' if coin_bundle_size > 1 else ''}"
                    if item_name in item_counts:
                        item_counts[item_name] += 1
                    else:
                        item_counts[item_name] = 1

        if self.options.shuffle_golden_coins == "shuffle":
            for item in self.item_name_groups["Golden Coins"]:
                item_counts[item] = 1
        elif self.options.shuffle_golden_coins == "mario_coin_fragment_hunt":
            for item in ("Tree Coin", "Space Coin", "Macro Coin", "Pumpkin Coin", "Turtle Coin"):
                self.multiworld.push_precollected(self.create_item(item))
        else:
            for item, location_name in (
                    ("Mario Coin", "Mario Zone 4 - Boss"),
                    ("Tree Coin", "Tree Zone 5 - Boss"),
                    ("Space Coin", "Space Zone 2 - Boss"),
                    ("Macro Coin", "Macro Zone 4 - Boss"),
                    ("Pumpkin Coin", "Pumpkin Zone 4 - Boss"),
                    ("Turtle Coin", "Turtle Zone 3 - Boss")
            ):
                location = self.multiworld.get_location(location_name, self.player)
                location.place_locked_item(self.create_item(item))
                location.address = None
                location.item.code = None

        if self.options.shuffle_midway_bells:
            for item in [item for item in items if "Midway Bell" in item]:
                if item != "Mario's Castle Midway Bell" or self.options.marios_castle_midway_bell:
                    item_counts[item] = 1

        if self.options.difficulty_mode == "easy_to_normal":
            item_counts["Normal Mode"] = 1
        elif self.options.difficulty_mode == "normal_to_easy":
            item_counts["Easy Mode"] = 1

        if self.options.shuffle_pipe_traversal == "single":
            item_counts["Pipe Traversal"] = 1
        elif self.options.shuffle_pipe_traversal == "split":
            item_counts["Pipe Traversal - Right"] = 1
            item_counts["Pipe Traversal - Left"] = 1
            item_counts["Pipe Traversal - Up"] = 1
            item_counts["Pipe Traversal - Down"] = 1
        else:
            self.multiworld.push_precollected(self.create_item("Pipe Traversal"))

        if any(self.auto_scroll_levels):
            if self.options.auto_scroll_mode == "global_trap_item":
                item_counts["Auto Scroll"] = 1
            elif self.options.auto_scroll_mode == "global_cancel_item":
                item_counts["Cancel Auto Scroll"] = 1
            else:
                for level, i in enumerate(self.auto_scroll_levels):
                    if i == 3:
                        item_counts[f"Auto Scroll - {level_id_to_name[level]}"] = 1
                    elif i == 2:
                        item_counts[f"Cancel Auto Scroll - {level_id_to_name[level]}"] = 1

        for item in self.multiworld.precollected_items[self.player]:
            if item.name in item_counts and item_counts[item.name] > 0:
                item_counts[item.name] -= 1

        location_count = len(self.multiworld.get_unfilled_locations(self.player))
        items_to_add = location_count - sum(item_counts.values())
        if items_to_add > 0:
            mario_coin_frags = 0
            if self.options.shuffle_golden_coins == "mario_coin_fragment_hunt":
                mario_coin_frags = (items_to_add * self.options.mario_coin_fragment_percentage) // 100
                item_counts["Mario Coin Fragment"] += mario_coin_frags
            item_counts["Super Star Duration Increase"] += items_to_add - mario_coin_frags
        elif items_to_add < 0:
            if self.options.coinsanity:
                for i in range(1, 168):
                    coin_name = f"{i} Coin{'s' if i > 1 else ''}"
                    if coin_name in item_counts:
                        amount_to_remove = min(-items_to_add, item_counts[coin_name])
                        item_counts[coin_name] -= amount_to_remove
                        items_to_add += amount_to_remove
                        if items_to_add >= 0:
                            break

            double_progression_items = ["Tree Zone Progression", "Macro Zone Progression", "Pumpkin Zone Progression",
                                        "Mario Zone Progression", "Turtle Zone Progression"]
            self.random.shuffle(double_progression_items)
            while sum(item_counts.values()) > location_count:
                if double_progression_items:
                    double_progression_item = double_progression_items.pop()
                    item_counts[double_progression_item] -= 2
                    item_counts[double_progression_item + " x2"] = 1
                    continue
                if self.options.auto_scroll_mode in ("level_trap_items", "level_cancel_items",
                                                     "chaos"):
                    auto_scroll_item = self.random.choice([item for item in item_counts if "Auto Scroll" in item])
                    level = auto_scroll_item.split("- ")[1]
                    self.auto_scroll_levels[level_name_to_id[level]] = 0
                    del item_counts[auto_scroll_item]
                    continue
                raise Exception(f"Too many items in the item pool for Super Mario Land 2 player {self.player_name}")
                # item = self.random.choice(list(item_counts))
                # item_counts[item] -= 1
                # if item_counts[item] == 0:
                #     del item_counts[item]
                # self.multiworld.push_precollected(self.create_item(item))

        self.coin_fragments_required = max((item_counts["Mario Coin Fragment"]
                                           * self.options.mario_coin_fragments_required_percentage) // 100, 1)

        for item_name, count in item_counts.items():
            self.multiworld.itempool += [self.create_item(item_name) for _ in range(count)]

    def fill_slot_data(self):
        return {
            "energy_link": self.options.energy_link.value
        }

    def create_item(self, name: str) -> Item:
        return MarioLand2Item(name, items[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self):
        return "1 Coin"

    def modify_multidata(self, multidata: dict):
        rom_name = bytearray(f'AP{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0',
                             'utf8')[:21]
        rom_name.extend([0] * (21 - len(rom_name)))
        new_name = base64.b64encode(bytes(rom_name)).decode()
        multidata["connect_names"][new_name] = multidata["connect_names"][self.player_name]


class MarioLand2Location(Location):
    game = "Super Mario Land 2"


class MarioLand2Item(Item):
    game = "Super Mario Land 2"
