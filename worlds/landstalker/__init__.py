from typing import ClassVar, Set

from BaseClasses import LocationProgressType, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Constants import *
from .Hints import *
from .Items import *
from .Locations import *
from .Options import JewelCount, LandstalkerGoal, LandstalkerOptions, ProgressiveArmors, TeleportTreeRequirements
from .Regions import *
from .Rules import *


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
    options_dataclass = LandstalkerOptions
    options: LandstalkerOptions
    required_client_version = (0, 4, 4)
    web = LandstalkerWeb()

    item_name_to_id = build_item_name_to_id_table()
    location_name_to_id = build_location_name_to_id_table()

    cached_spheres: List[Set[Location]] = []

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.regions_table: Dict[str, LandstalkerRegion] = {}
        self.dark_dungeon_id = "None"
        self.dark_region_ids = []
        self.teleport_tree_pairs = []
        self.jewel_items = []

    def fill_slot_data(self) -> dict:
        if not LandstalkerWorld.cached_spheres:
            LandstalkerWorld.cached_spheres = list(self.multiworld.get_spheres())

        # Generate hints.
        self.adjust_shop_prices()
        hints = Hints.generate_random_hints(self)
        hints["Lithograph"] = Hints.generate_lithograph_hint(self)
        hints["Oracle Stone"] = f"It shows {self.dark_dungeon_id}\nenshrouded in darkness."

        # Put options, locations' contents and some additional data inside slot data
        options = [
            "goal", "jewel_count", "progressive_armors", "use_record_book", "use_spell_book", "shop_prices_factor",
            "combat_difficulty", "teleport_tree_requirements", "shuffle_trees", "ensure_ekeeke_in_shops",
            "remove_gumi_boulder", "allow_whistle_usage_behind_trees", "handle_damage_boosting_in_logic",
            "handle_enemy_jumping_in_logic", "handle_tree_cutting_glitch_in_logic", "hint_count", "death_link",
            "revive_using_ekeeke",
        ]

        slot_data = self.options.as_dict(*options)
        slot_data["spawn_region"] = self.options.spawn_region.current_key
        slot_data["seed"] = self.random.randint(0, 2 ** 32 - 1)
        slot_data["dark_region"] = self.dark_dungeon_id
        slot_data["hints"] = hints
        slot_data["teleport_tree_pairs"] = [[pair[0]["name"], pair[1]["name"]] for pair in self.teleport_tree_pairs]

        # Type hinting for location.
        location: LandstalkerLocation
        slot_data["location_prices"] = {
            location.name: location.price for location in self.multiworld.get_locations(self.player) if location.price}

        return slot_data

    def generate_early(self):
        # Randomly pick a set of dark regions where Lantern is needed
        darkenable_regions = get_darkenable_regions()
        self.dark_dungeon_id = self.random.choice(list(darkenable_regions))
        self.dark_region_ids = darkenable_regions[self.dark_dungeon_id]

    def create_regions(self):
        self.regions_table = Regions.create_regions(self)
        Locations.create_locations(self.player, self.regions_table, self.location_name_to_id,
                                   self.options.goal == "reach_kazalt")
        self.create_teleportation_trees()

    def create_item(self, name: str, classification_override: Optional[ItemClassification] = None) -> LandstalkerItem:
        data = item_table[name]
        classification = classification_override or data.classification
        item = LandstalkerItem(name, classification, BASE_ITEM_ID + data.id, self.player)
        item.price_in_shops = data.price_in_shops
        return item

    def create_event(self, name: str) -> LandstalkerItem:
        return LandstalkerItem(name, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self) -> str:
        return "EkeEke"

    def create_items(self):
        item_pool: List[LandstalkerItem] = []
        for name, data in item_table.items():
            # If item is an armor and progressive armors are enabled, transform it into a progressive armor item
            if self.options.progressive_armors and "Breast" in name:
                name = "Progressive Armor"

            qty = data.quantity
            if self.options.goal == "reach_kazalt":
                # In "Reach Kazalt" goal, remove all endgame progression items that would be useless anyway
                if name in ENDGAME_PROGRESSION_ITEMS:
                    continue
                # Also reduce quantities for most filler items to let space for more EkeEke (see end of function)
                if data.classification == ItemClassification.filler:
                    qty = int(qty * 0.8)
            item_pool += [self.create_item(name) for _ in range(qty)]

        # If the appropriate setting is on, place one EkeEke in one shop in every town in the game
        if self.options.ensure_ekeeke_in_shops:
            shops_to_fill = [
                "Massan: Shop item #1",
                "Gumi: Inn item #1",
                "Ryuma: Inn item",
                "Mercator: Shop item #1",
                "Verla: Shop item #1",
                "Destel: Inn item",
                "Route to Lake Shrine: Greedly's shop item #1"
            ]
            if self.options.goal != "reach_kazalt":
                shops_to_fill.append("Kazalt: Shop item #1")
            for location_name in shops_to_fill:
                self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item("EkeEke"))

        # Add a fixed amount of progression Life Stock for a specific requirement (Fahl)
        fahl_lifestock_req = 15
        item_pool += [self.create_item("Life Stock", ItemClassification.progression) for _ in range(fahl_lifestock_req)]
        # Add a unique progression EkeEke for a specific requirement (Cutter)
        item_pool.append(self.create_item("EkeEke", ItemClassification.progression))

        # Add a variable amount of "useful" Life Stock to the pool, depending on the amount of starting Life Stock
        # (i.e. on the starting location)
        starting_lifestocks = self.get_starting_health() - 4
        lifestock_count = 80 - starting_lifestocks - fahl_lifestock_req
        item_pool += [self.create_item("Life Stock") for _ in range(lifestock_count)]

        # Add jewels to the item pool depending on the number of jewels set in generation settings
        self.jewel_items = [self.create_item(name) for name in self.get_jewel_names(self.options.jewel_count)]
        item_pool += self.jewel_items

        # Add a pre-placed fake win condition item
        self.multiworld.get_location("End", self.player).place_locked_item(self.create_event("King Nole's Treasure"))

        # Fill the rest of the item pool with EkeEke
        remaining_items = len(self.multiworld.get_unfilled_locations(self.player)) - len(item_pool)
        item_pool += [self.create_item(self.get_filler_item_name()) for _ in range(remaining_items)]

        self.multiworld.itempool += item_pool

    def create_teleportation_trees(self):
        self.teleport_tree_pairs = load_teleport_trees()

        def pairwise(iterable):
            """Yields pairs of elements from the given list -> [0,1], [2,3]..."""
            a = iter(iterable)
            return zip(a, a)

        # Shuffle teleport tree pairs if the matching setting is on
        if self.options.shuffle_trees:
            all_trees = [item for pair in self.teleport_tree_pairs for item in pair]
            self.random.shuffle(all_trees)
            self.teleport_tree_pairs = [[x, y] for x, y in pairwise(all_trees)]

        # If a specific setting is set, teleport trees are potentially active without visiting both sides.
        # This means we need to add those as explorable paths for the generation algorithm.
        teleport_trees_mode = self.options.teleport_tree_requirements.value
        created_entrances = []
        if teleport_trees_mode in [TeleportTreeRequirements.option_none, TeleportTreeRequirements.option_clear_tibor]:
            for pair in self.teleport_tree_pairs:
                entrances = create_entrance(pair[0]["region"], pair[1]["region"], True, self.regions_table)
                created_entrances += entrances

        # Teleport trees are open but require access to Tibor to work
        if teleport_trees_mode == TeleportTreeRequirements.option_clear_tibor:
            for entrance in created_entrances:
                entrance.access_rule = make_path_requirement_lambda(self.player, [], [self.regions_table["tibor"]])

    def set_rules(self):
        Rules.create_rules(self)

        # In "Reach Kazalt" goal, player doesn't have access to Kazalt, King Nole's Labyrinth & King Nole's Palace.
        # As a consequence, all locations inside those regions must be excluded, and the teleporter from
        # King Nole's Cave to Kazalt must go to the end region instead.
        if self.options.goal == LandstalkerGoal.option_reach_kazalt:
            kazalt_tp = self.multiworld.get_entrance("king_nole_cave -> kazalt", self.player)
            kazalt_tp.connected_region = self.regions_table["end"]

            excluded_regions = [
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
                if location.parent_region.name in excluded_regions:
                    location.progress_type = LocationProgressType.EXCLUDED
                # We need to make that event non-progression since it would crash generation in reach_kazalt goal
                if location.item is not None and location.item.name == "event_visited_king_nole_labyrinth_raft_entrance":
                    location.item.classification = ItemClassification.filler

    def get_starting_health(self):
        spawn_id = self.options.spawn_region.current_key
        if spawn_id == "destel":
            return 20
        elif spawn_id == "verla":
            return 16
        elif spawn_id in ["waterfall", "mercator", "greenmaze"]:
            return 10
        else:
            return 4

    @classmethod
    def stage_modify_multidata(cls, multiworld: MultiWorld, *_):
        LandstalkerWorld.cached_spheres = []

    def adjust_shop_prices(self):
        # Calculate prices for items in shops once all items have their final position
        unknown_items_price = 250
        earlygame_price_factor = 1.0
        endgame_price_factor = 2.0
        factor_diff = endgame_price_factor - earlygame_price_factor

        global_price_factor = self.options.shop_prices_factor / 100.0

        spheres = LandstalkerWorld.cached_spheres
        sphere_count = len(spheres)
        for sphere_id, sphere in enumerate(spheres):
            location: LandstalkerLocation  # after conditional, we guarantee it's this kind of location.
            for location in sphere:
                if location.player != self.player or location.type_string != "shop":
                    continue

                current_playthrough_progression = sphere_id / sphere_count
                progression_price_factor = earlygame_price_factor + (current_playthrough_progression * factor_diff)

                price = location.item.price_in_shops \
                    if location.item.game == "Landstalker - The Treasures of King Nole" else unknown_items_price
                price *= progression_price_factor
                price *= global_price_factor
                price -= price % 5
                price = max(price, 5)
                location.price = int(price)

    @staticmethod
    def get_jewel_names(count: JewelCount):
        if count < 6:
            return ["Red Jewel", "Purple Jewel", "Green Jewel", "Blue Jewel", "Yellow Jewel"][:count]

        return ["Kazalt Jewel"] * count
