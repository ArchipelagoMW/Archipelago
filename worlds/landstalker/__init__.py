from typing import List
from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Options import ls_options
from .Items import *
from .Regions import *
from .Locations import *
from .Rules import *

# TODO: Docs
class LandstalkerWeb(WebWorld):
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Landstalker Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "landstalker_en.md",
        "landstalker/en",
        ["Dinopony"]
    )]
    bug_report_page = "https://github.com/Dinopony/randstalker/issues/"


class LandstalkerWorld(World):
    """
    Landstalker: The Treasures of King Nole is a classic Action-RPG with an isometric view (also known as "2.5D").
    You play Nigel, a treasure hunter exploring the island of Mercator trying to find the legendary treasure.
    Roam freely on the island, get stronger to beat dungeons and gather the required key items in order to reach the
    hidden palace and claim the treasure.
    """
    game = "Landstalker"
    option_definitions = ls_options
    topology_present = True
    data_version = 0
    required_client_version = (0, 3, 8)
    web = LandstalkerWeb()

    item_name_to_id = build_item_name_to_id_table()
    location_name_to_id = build_location_name_to_id_table()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.regions_table: Dict[str, Region] = {}
        self.dark_dungeon_id = "None"
        self.dark_region_ids = []
        self.teleport_tree_pairs = []

    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        # Put options, locations' contents and some additional data inside slot data
        slot_data = {option_name: self.get_setting(option_name).value for option_name in ls_options}
        slot_data["seed"] = self.multiworld.per_slot_randoms[self.player].randint(0, 4294967295)
        slot_data["dark_region"] = self.dark_dungeon_id

        slot_data["locations"] = {}
        for location in self.multiworld.get_locations(self.player):
            slot_data['locations'][location.name] = {
                "item": location.item.name,
                "player": self.multiworld.get_player_name(location.item.player)
            }
            if location.price > 0:
                slot_data['locations'][location.name]['price'] = location.price

        slot_data["hints"] = {
            "Lithograph": self.generate_lithograph_hint(),
            "Oracle Stone": self.generate_oracle_stone_hint()
        }

        slot_data["teleport_tree_pairs"] = []
        for pair in self.teleport_tree_pairs:
            slot_data["teleport_tree_pairs"].append([pair[0]['name'], pair[1]['name']])

        return slot_data

    def generate_early(self):
        # Randomly pick a set of dark regions where Lantern is needed
        darkenable_regions = get_darkenable_regions()
        self.dark_dungeon_id = self.multiworld.random.choices(list(darkenable_regions.keys()))[0]
        self.dark_region_ids = darkenable_regions[self.dark_dungeon_id]

    def create_item(self, name: str) -> LandstalkerItem:
        if self.get_setting('progressive_armors').value == 1 and 'Breast' in name:
            name = 'Progressive Armor'
        data = item_table[name]
        item = LandstalkerItem(name, data.classification, BASE_ITEM_ID + data.id, self.player)
        item.price_in_shops = data.price_in_shops
        return item

    def generate_output(self, output_directory: str) -> None:
        earlygame_price_factor = 0.5
        endgame_price_factor = 2.0
        factor_diff = endgame_price_factor - earlygame_price_factor

        spheres = list(self.multiworld.get_spheres())
        sphere_id = 0
        sphere_count = len(spheres)
        for sphere in spheres:
            for location in sphere:
                if location.player == self.player and location.type_string == 'shop':
                    current_playthrough_progression = sphere_id / sphere_count
                    progression_price_factor = earlygame_price_factor + (current_playthrough_progression * factor_diff)

                    price = location.item.price_in_shops if location.item.player == self.player else 100
                    price *= progression_price_factor
                    price -= price % 10
                    location.price = int(price)
            sphere_id += 1

    def create_items(self):
        item_pool: List[LandstalkerItem] = []
        for name, data in item_table.items():
            item_pool += [self.create_item(name) for _ in range(0, data.quantity)]

        # Add jewels to the item pool depending on the number of jewels set in generation settings
        jewel_count = self.get_setting('jewel_count').value
        required_jewels = ["Red Jewel", "Purple Jewel", "Green Jewel", "Blue Jewel", "Yellow Jewel"]
        del required_jewels[jewel_count:]
        item_pool += [self.create_item(name) for name in required_jewels]

        # Fill the rest of the item pool with EkeEke
        unfilled_location_count = len(self.multiworld.get_unfilled_locations(self.player))
        while len(item_pool) < unfilled_location_count:
            item_pool.append(self.create_item("EkeEke"))

        self.multiworld.itempool += item_pool

    def create_regions(self):
        self.regions_table = Regions.create_regions(self.multiworld, self.player)
        Locations.create_locations(self.player, self.regions_table, self.location_name_to_id)
        self.create_teleportation_trees()

    def create_teleportation_trees(self):
        self.teleport_tree_pairs = load_teleport_trees()

        # Shuffle teleport tree pairs if the matching setting is on
        if self.multiworld.shuffle_trees[self.player].value == 1:
            all_trees = []
            for pair in self.teleport_tree_pairs:
                all_trees += [pair[0], pair[1]]
            self.multiworld.random.shuffle(all_trees)
            self.teleport_tree_pairs = []
            while len(all_trees) > 0:
                self.teleport_tree_pairs.append([all_trees[0], all_trees[1]])
                all_trees = all_trees[2:]

        # If a specific setting is set, teleport trees are potentially active without visiting both sides.
        # This means we need to add those as explorable paths for the generation algorithm.
        teleport_trees_mode = self.multiworld.teleport_tree_requirements[self.player].value
        created_entrances = []
        if teleport_trees_mode < 2:
            for pair in self.teleport_tree_pairs:
                entrances = create_entrance(pair[0]['region'], pair[1]['region'], True, self.player, self.regions_table)
                created_entrances += entrances
        if teleport_trees_mode == 1:  # Teleport trees are open but require access to Tibor in order to work
            for entrance in created_entrances:
                entrance.access_rule = make_path_requirement_lambda(self.player, [], [self.regions_table['tibor']])

    def set_rules(self):
        Rules.create_rules(self.multiworld, self.player, self.regions_table, self.dark_region_ids)

    def generate_lithograph_hint(self):
        jewels = {}
        for item in self.multiworld.itempool:
            if item.player != self.player:
                continue
            if " Jewel" in item.name:
                jewels[item.name] = self.multiworld.get_player_name(item.location.player)

        hint_text = ""
        for [jewel_name, player_name] in jewels.items():
            if hint_text != "":
                hint_text += "\n"
            hint_text += f"{jewel_name} is in {player_name}'s world."

        return hint_text

    def generate_oracle_stone_hint(self):
        return f"It shows {self.dark_dungeon_id}\nenshrouded in darkness."

#   def get_filler_item_name(self) -> str:
#       fillers = get_weighted_filler_item_names()
#       return self.multiworld.random.choices(fillers)[0]
