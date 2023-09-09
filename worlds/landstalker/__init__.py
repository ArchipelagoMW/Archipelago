import threading
from typing import List
from BaseClasses import Tutorial, LocationProgressType
from worlds.AutoWorld import WebWorld, World
from .Options import ls_options, ProgressiveArmors, LandstalkerGoal, TeleportTreeRequirements
from .Items import *
from .Regions import *
from .Locations import *
from .Rules import *
from .Hints import *


class LandstalkerWeb(WebWorld):
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Landstalker Randomizer software on your computer.",
        "English",
        "landstalker_setup_en.md",
        "landstalker_setup/en",
        ["Dinopony"]
    )]


class LandstalkerWorld(World):
    """
    Landstalker: The Treasures of King Nole is a classic Action-RPG with an isometric view (also known as "2.5D").
    You play Nigel, a treasure hunter exploring the island of Mercator trying to find the legendary treasure.
    Roam freely on the island, get stronger to beat dungeons and gather the required key items in order to reach the
    hidden palace and claim the treasure.
    """
    game = "Landstalker - The Treasures of King Nole"
    option_definitions = ls_options
    topology_present = True
    data_version = 1
    required_client_version = (0, 3, 8)
    web = LandstalkerWeb()

    item_name_to_id = build_item_name_to_id_table()
    location_name_to_id = build_location_name_to_id_table()

    """ This is needed to force fill_slot_data to happen after generate_output finished balancing shop prices. """
    can_fill_slot_data: threading.Event

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.regions_table: Dict[str, Region] = {}
        self.dark_dungeon_id = "None"
        self.dark_region_ids = []
        self.teleport_tree_pairs = []
        self.can_fill_slot_data = threading.Event()
        self.hints = {}

    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        self.can_fill_slot_data.wait()

        # Put options, locations' contents and some additional data inside slot data
        slot_data = {option_name: self.get_setting(option_name).value for option_name in ls_options}
        slot_data["seed"] = self.random.randint(0, 4294967295)
        slot_data["dark_region"] = self.dark_dungeon_id
        slot_data["location_prices"] = {location.name: location.price for location in self.multiworld.get_locations(self.player) if location.price}
        slot_data["hints"] = self.hints
        slot_data["teleport_tree_pairs"] = [[pair[0]['name'], pair[1]['name']] for pair in self.teleport_tree_pairs]

        return slot_data

    def generate_early(self):
        # Randomly pick a set of dark regions where Lantern is needed
        darkenable_regions = get_darkenable_regions()
        self.dark_dungeon_id = self.random.choice(list(darkenable_regions))
        self.dark_region_ids = darkenable_regions[self.dark_dungeon_id]

    def create_regions(self):
        self.regions_table = Regions.create_regions(self.multiworld, self.player)
        Locations.create_locations(self.player, self.regions_table, self.location_name_to_id)
        self.create_teleportation_trees()

    def create_item(self, name: str, classification_override: Optional[ItemClassification] = None) -> LandstalkerItem:
        data = item_table[name]
        classification = classification_override or data.classification
        item = LandstalkerItem(name, classification, BASE_ITEM_ID + data.id, self.player)
        item.price_in_shops = data.price_in_shops
        return item

    def create_items(self):
        item_pool: List[LandstalkerItem] = []
        for name, data in item_table.items():
            # If item is an armor and progressive armors are enabled, transform it into a progressive armor item
            if self.get_setting('progressive_armors') and 'Breast' in name:
                name = 'Progressive Armor'
            item_pool += [self.create_item(name) for _ in range(0, data.quantity)]

        # If the appropriate setting is on, place one EkeEke in one shop in every town in the game
        if self.get_setting("ensure_ekeeke_in_shops"):
            SHOPS_TO_FILL = [
                "Massan: Shop item #1",
                "Gumi: Inn item #1",
                "Ryuma: Inn item",
                "Mercator: Shop item #1",
                "Verla: Shop item #1",
                "Destel: Inn item",
                "Route to Lake Shrine: Greedly's shop item #1",
                "Kazalt: Shop item #1"
            ]
            for location_name in SHOPS_TO_FILL:
                self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item("EkeEke"))

        # Add a fixed amount of "progression" Life Stock for a specific requirement
        FAHL_LIFESTOCK_REQ = 15
        item_pool += [self.create_item("Life Stock", ItemClassification.progression) for _ in range(FAHL_LIFESTOCK_REQ)]

        # Add a variable amount of "useful" Life Stock to the pool, depending on the amount of starting Life Stock
        # (i.e. on the starting location)
        starting_lifestocks = self.get_starting_health() - 4
        lifestock_count = 80 - starting_lifestocks - FAHL_LIFESTOCK_REQ
        item_pool += [self.create_item("Life Stock") for _ in range(lifestock_count)]

        # Add jewels to the item pool depending on the number of jewels set in generation settings
        required_jewels = ["Red Jewel", "Purple Jewel", "Green Jewel", "Blue Jewel", "Yellow Jewel"]
        del required_jewels[self.get_setting('jewel_count'):]
        item_pool += [self.create_item(name) for name in required_jewels]

        # Add a pre-placed fake win condition item
        win_condition_item = LandstalkerItem("King Nole's Treasure", ItemClassification.progression, None, self.player)
        self.multiworld.get_location("End", self.player).place_locked_item(win_condition_item)

        # Fill the rest of the item pool with EkeEke
        remaining_items = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        item_pool += [self.create_item("EkeEke") for _ in range(remaining_items)]

        self.multiworld.itempool += item_pool

    def create_teleportation_trees(self):
        self.teleport_tree_pairs = load_teleport_trees()

        def pairwise(iterable):
            """Yields pairs of elements from the given list -> [0,1], [2,3]..."""
            a = iter(iterable)
            return zip(a, a)

        # Shuffle teleport tree pairs if the matching setting is on
        if self.get_setting("shuffle_trees"):
            all_trees = [item for pair in self.teleport_tree_pairs for item in pair]
            self.multiworld.random.shuffle(all_trees)
            self.teleport_tree_pairs = [[x, y] for x, y in pairwise(all_trees)]

        # If a specific setting is set, teleport trees are potentially active without visiting both sides.
        # This means we need to add those as explorable paths for the generation algorithm.
        teleport_trees_mode = self.get_setting("teleport_tree_requirements")
        created_entrances = []
        if teleport_trees_mode in [TeleportTreeRequirements.option_none, TeleportTreeRequirements.option_clear_tibor]:
            for pair in self.teleport_tree_pairs:
                entrances = create_entrance(pair[0]['region'], pair[1]['region'], True, self.player, self.regions_table)
                created_entrances += entrances
        # Teleport trees are open but require access to Tibor in order to work
        if teleport_trees_mode == TeleportTreeRequirements.option_clear_tibor:
            for entrance in created_entrances:
                entrance.access_rule = make_path_requirement_lambda(self.player, [], [self.regions_table['tibor']])

    def set_rules(self):
        Rules.create_rules(self.multiworld, self.player, self.regions_table, self.dark_region_ids)

        # In "Reach Kazalt" goal, player doesn't have access to Kazalt, King Nole's Labyrinth & King Nole's Palace.
        # As a consequence, all locations inside those regions must be excluded and the teleporter from
        # King Nole's Cave to Kazalt must go to the end region instead.
        if self.get_setting("goal") == LandstalkerGoal.option_reach_kazalt:
            kazalt_tp = self.multiworld.get_entrance("king_nole_cave -> kazalt", self.player)
            kazalt_tp.connected_region = self.regions_table["end"]

            EXCLUDED_REGIONS = [
                "kazalt",
                "king_nole_labyrinth_pre_door",
                "king_nole_labyrinth_post_door",
                "king_nole_labyrinth_exterior",
                "king_nole_labyrinth_fall_from_exterior",
                "king_nole_labyrinth_raft_entrance",
                "king_nole_labyrinth_raft",
                "king_nole_labyrinth_sacred_tree",
                "king_nole_labyrinth_path_to_palace",
                "king_nole_palace"
            ]

            for location in self.multiworld.get_locations(self.player):
                if location.parent_region.name in EXCLUDED_REGIONS:
                    location.progress_type = LocationProgressType.EXCLUDED

    def get_starting_health(self):
        spawn_id = self.get_setting('spawn_region')
        if spawn_id == "destel":
            return 20
        elif spawn_id == "verla":
            return 16
        elif spawn_id in ["waterfall", "mercator", "greenmaze"]:
            return 10
        else:
            return 4

    def generate_output(self, output_directory: str) -> None:
        self.adjust_shop_prices()

        self.hints = Hints.generate_random_hints(self.multiworld, self.player)
        self.hints["Lithograph"] = Hints.generate_lithograph_hint(self.multiworld, self.player)
        self.hints["Oracle Stone"] = f"It shows {self.dark_dungeon_id}\nenshrouded in darkness."

        self.can_fill_slot_data.set()

    def adjust_shop_prices(self):
        # Calculate prices for items in shops once all items have their final position
        unknown_items_price = 250
        earlygame_price_factor = 1.0
        endgame_price_factor = 2.0
        factor_diff = endgame_price_factor - earlygame_price_factor

        global_price_factor = self.get_setting("shop_prices_factor") / 100.0

        spheres = list(self.multiworld.get_spheres())
        sphere_id = 0
        sphere_count = len(spheres)
        for sphere in spheres:
            for location in sphere:
                if location.player != self.player or location.type_string != 'shop':
                    continue
                current_playthrough_progression = sphere_id / sphere_count
                progression_price_factor = earlygame_price_factor + (current_playthrough_progression * factor_diff)

                price = location.item.price_in_shops if location.item.game == 'Landstalker' else unknown_items_price
                price *= progression_price_factor
                price *= global_price_factor
                price -= price % 5
                price = max(price, 5)
                location.price = int(price)
            sphere_id += 1
