from typing import Any, Dict, List
from BaseClasses import CollectionState, Item, ItemClassification, Location, Region, Tutorial
from Fill import fill_restrictive
from worlds.generic.Rules import set_rule
from worlds.minishoot.options import MinishootOptions
from .pool import MinishootPool
from .rules import simple_parse
from .items import MinishootItemData, item_name_to_id, item_table
from .locations import location_name_to_id, location_table
from .regions import region_table
from .transitions import transition_table
from .dungeons import dungeon_reward_location_mapping, get_dungeon_for_item, get_dungeons
from .zones import zone_table
from worlds.AutoWorld import WebWorld, World

class MinishootWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the Minishoot' Adventure Randomizer for Archipelago multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["TheNouillet"]
        )
    ]
    theme = "grass"
    game = "Minishoot Adventures"

class MinishootItem(Item):
    game: str = "Minishoot Adventures"

class MinishootLocation(Location):
    game: str = "Minishoot Adventures"

class MinishootWorld(World):
    """
    Fly into a charming handcrafted world and go on an adventure that mixes up open exploration with crispy twin-stick shooter action. Fight your way from the shiny overworld to the deepest caves, improve your ship and overcome the dungeons' bosses to rescue your friends!
    """
    game = "Minishoot Adventures"
    web = MinishootWeb()
    options: MinishootOptions
    options_dataclass = MinishootOptions

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    # This version is checked in the client to ensure that the client and the server are on the same page feature-wise.
    # The client will throw an error to the player if the server is on a different version.
    # This is to avoid issues where a player would use a client with a different version than the APWorld.
    ap_world_version = "0.5.1"

    def create_item(self, name: str) -> MinishootItem:
        if name not in item_table:
            raise ValueError(f"Could not find item {name} in item table")
        item_data = item_table[name]
        item = MinishootItem(name, item_data.classification, self.item_name_to_id[name], self.player)
        if item.name == "Progressive Cannon" and self.options.ignore_cannon_level_requirements:
            item.classification = ItemClassification.useful

        return item

    def create_regions(self) -> None:
        menu_region: Region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        randomized_pools = self.get_randomized_pools()

        for region_name, data in region_table.items():
            region: Region = Region(region_name, self.player, self.multiworld)
            for location_name in data.locations:
                if location_name != '' and location_name in location_table:
                    location = MinishootLocation(
                        self.player,
                        location_name,
                        location_name_to_id[location_name],
                        region
                    )
                    if location_table[location_name].pool not in randomized_pools:
                        location.show_in_spoiler = False
                    region.locations.append(location)

            self.multiworld.regions.append(region)

        menu_region.add_exits({"Starting Grotto - Lake": "Start Transition"})

        for region_name, data in region_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            exits: Dict[str, str] = {}
            for transition_name in data.outgoing_transitions:
                if transition_name != '':
                    transition_data = transition_table[transition_name]
                    exits[transition_data.destination] = transition_name

            region.add_exits(exits)

        normal_ending_victory_location = self.multiworld.get_location("Dungeon 5 - Beat the boss", self.player)
        normal_ending_victory_location.place_locked_item(MinishootItem("Normal Ending Victory", ItemClassification.progression, None, self.player))

        true_ending_victory_location = self.multiworld.get_location("Snow - Beat the Unchosen", self.player)
        true_ending_victory_location.place_locked_item(MinishootItem("True Ending Victory", ItemClassification.progression, None, self.player))

        if self.options.completion_goals == "spirit_tower":
            spirit_tower_victory_location = self.multiworld.get_location("Spirit Tower - Item", self.player)
            spirit_tower_victory_location.place_locked_item(self.try_create_item("Golden Crystal Heart"))

        self.multiworld.completion_condition[self.player] = lambda state: self.completion_condition(state)
    
    def completion_condition(self, state: CollectionState) -> bool:
        if self.options.completion_goals == "dungeon_5":
            return state.has("Normal Ending Victory", self.player)
        elif self.options.completion_goals == "snow":
            return state.has("True Ending Victory", self.player)
        elif self.options.completion_goals == "dungeon_5_and_snow":
            return state.has("Normal Ending Victory", self.player) and state.has("True Ending Victory", self.player)
        elif self.options.completion_goals == "spirit_tower":
            return state.has("Golden Crystal Heart", self.player)
        else:
            return False

    def get_randomized_pools(self) -> List[MinishootPool]:
        randomized_pools = [MinishootPool.default, MinishootPool.dungeon_small_key, MinishootPool.dungeon_big_key, MinishootPool.dungeon_reward]
        if self.options.npc_sanity:
            randomized_pools.append(MinishootPool.npc)
        if self.options.shard_sanity:
            randomized_pools.append(MinishootPool.xp_crystals)
        if self.options.scarab_sanity:
            randomized_pools.append(MinishootPool.scarab)
        if self.options.spirit_sanity:
            randomized_pools.append(MinishootPool.spirit)

        return randomized_pools
    
    def get_ignored_items(self) -> List[str]:
        return [
            "Abyss Map",
            "Beach Map",
            "Blue Forest Map",
            "Desert Map",
            "Green Map",
            "Junkyard Map",
            "Sunken City Map",
            "Swamp Map",
            "Ancient Astrolabe",
            "Compass",
            "Explorer"
        ]

    def get_fallback_items(self) -> List[str]:
        fallback_items = ["Super Crystals x2", "Super Crystals x5", "Super Crystals x10", "Super Crystals x15"]
        if self.options.add_trap_items:
            fallback_items += ["Primordial Scarab Dialog"] * 2

        return fallback_items
    
    def get_filler_item_name(self) -> str:
        return self.random.choice(self.get_fallback_items())

    def try_create_item(self, item_name: str) -> MinishootItem:
        name = item_name
        if name in self.get_ignored_items():
            name = self.get_filler_item_name()
        if self.options.progressive_dash.value == 1 and name in ["Dash", "Spirit Dash"]:
            name = "Progressive Dash"
        
        return self.create_item(name)

    def create_items(self) -> None:
        minishoot_items: List[MinishootItem] = []

        randomized_pools = self.get_randomized_pools()

        self.pre_fill_items: List[MinishootItem] = []
        self.pre_fill_small_key_item_datas_by_dungeons: Dict[str, List[MinishootItemData]] = {
            dungeon_name: [] for dungeon_name in get_dungeons()
        }
        self.pre_fill_item_datas_by_dungeons: Dict[str, List[MinishootItemData]] = {
            dungeon_name: [] for dungeon_name in get_dungeons()
        }

        for item_name, data in item_table.items():
            quantity = data.quantity_in_item_pool
            if item_name == "Progressive Cannon":
                quantity -= 1 # The plugin will add the first cannon level automatically.
            if item_name == "Ancient Tablet" and self.options.completion_goals == "spirit_tower":
                quantity -= 1 # We remove one Ancient Tablet to make room for the Golden Crystal Heart.
            for i in range(0, quantity):
                # For dungeon rewards, place them in the vanilla locations.
                if data.pool == MinishootPool.dungeon_reward:
                    location = self.multiworld.get_location(dungeon_reward_location_mapping[item_name], self.player)
                    if not location:
                        raise ValueError(f"Could not find location for dungeon reward {item_name}")
                    location.place_locked_item(self.try_create_item(item_name))
                # For dungeon keys, place them in the appropriate dungeon (if no keysanity).
                elif data.pool == MinishootPool.dungeon_small_key and not self.options.key_sanity:
                    dungeon = get_dungeon_for_item(item_name)

                    if not dungeon:
                        raise ValueError(f"Could not find dungeon for key {item_name}")
                    self.pre_fill_small_key_item_datas_by_dungeons[dungeon].append(data)
                    self.pre_fill_items.append(self.try_create_item(item_name))
                elif data.pool == MinishootPool.dungeon_big_key and not self.options.boss_key_sanity:
                    dungeon = get_dungeon_for_item(item_name)

                    if not dungeon:
                        raise ValueError(f"Could not find dungeon for key {item_name}")
                    self.pre_fill_item_datas_by_dungeons[dungeon].append(data)
                    self.pre_fill_items.append(self.try_create_item(item_name))
                # For other items, place them in the multiworld item pool.
                elif data.pool in randomized_pools:
                    minishoot_item: MinishootItem = self.try_create_item(item_name)
                    minishoot_items.append(minishoot_item)
            # We add one filler item to compensate for the cannon level that is added automatically.
            if item_name == "Progressive Cannon":
                minishoot_item: MinishootItem = self.try_create_item(self.get_filler_item_name())
                minishoot_items.append(minishoot_item)
                    
        for location_name, data in location_table.items():
            if data.pool not in randomized_pools and data.pool != MinishootPool.goal:
                location = self.multiworld.get_location(location_name, self.player)
                if not location:
                    raise ValueError(f"Could not find location {location_name}")
                location.place_locked_item(self.try_create_item(data.vanilla_item_name))

        self.itempool = minishoot_items
        self.multiworld.itempool += minishoot_items

    def set_rules(self) -> None:
        player = self.player

        for transition_name, data in transition_table.items():
            self.multiworld.get_entrance(transition_name, player).access_rule = \
                lambda state, rule=data.logic_rule: simple_parse(rule, state, self)
            
        for location_name, data in location_table.items():
            location = self.multiworld.get_location(location_name, player)
            set_rule(location,
                lambda state, rule=data.logic_rule: simple_parse(rule, state, self)
            )
            

    def get_pre_fill_items(self):
        return self.pre_fill_items
    
    def get_locations(self):
        return self.multiworld.get_locations(self.player)

    def pre_fill(self) -> None:

        def prefill_state(base_state):
            state = base_state.copy()
            for item in self.get_pre_fill_items():
                self.collect(state, item)
            state.sweep_for_advancements(locations=self.get_locations())
            return state
        
        randomized_pools = self.get_randomized_pools()

        # Set up initial state
        state = CollectionState(self.multiworld)
        for item in self.itempool:
            self.collect(state, item)
        state.sweep_for_advancements(locations=self.get_locations())

        for dungeon in get_dungeons():
            # Pre-fill dungeon with small keys first, then with other items.
            small_key_item_datas = self.pre_fill_small_key_item_datas_by_dungeons[dungeon]
            dungeon_item_datas = self.pre_fill_item_datas_by_dungeons[dungeon]
            item_datas = small_key_item_datas + dungeon_item_datas
            if not item_datas:
                continue

            dungeon_zone = zone_table[dungeon]
            dungeon_locations  = []
            for location_name in dungeon_zone.locations:
                location_data = location_table[location_name]
                if location_data.pool in randomized_pools and location_data.pool != MinishootPool.dungeon_reward:
                    dungeon_locations.append(self.multiworld.get_location(location_name, self.player))

            dungeon_items: List[MinishootItem] = [self.try_create_item(item_data.name) for item_data in item_datas]
            if not dungeon_items or not dungeon_locations:
                continue
            for item in dungeon_items:
                self.pre_fill_items.remove(item)

            self.multiworld.random.shuffle(dungeon_locations)
            fill_restrictive(
                multiworld=self.multiworld,
                base_state=prefill_state(state),
                locations=dungeon_locations,
                item_pool=dungeon_items,
                single_player_placement=True,
                lock=True,
                allow_partial=False,
                name="Minishoot Dungeon Pre-fill",
            )
            
        # Stolen from OOT APWorld : Locations which are not sendable must be converted to events
        for loc in self.get_locations():
            if loc.address is not None and not loc.show_in_spoiler:
                loc.address = None

    def post_fill(self) -> None:
        # Fill the remaining locations with filler items.
        for location in self.multiworld.get_unfilled_locations(self.player):
            location.place_locked_item(self.try_create_item(self.get_filler_item_name()))
            
    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "npc_sanity": self.options.npc_sanity.value,
            "scarab_sanity": self.options.scarab_sanity.value,
            "spirit_sanity": self.options.spirit_sanity.value,
            "shard_sanity": self.options.shard_sanity.value,
            "key_sanity": self.options.key_sanity.value,
            "boss_key_sanity": self.options.boss_key_sanity.value,
            "add_trap_items": self.options.add_trap_items.value,
            "trap_items_appearance": self.options.trap_items_appearance.value,
            "shop_cost_modifier": self.options.shop_cost_modifier.value,
            "scarab_items_cost": self.options.scarab_items_cost.value,
            "spirit_tower_requirement": self.options.spirit_tower_requirement.value,
            "show_archipelago_item_category": self.options.show_archipelago_item_category.value,
            "blocked_forest": self.options.blocked_forest.value,
            "ignore_cannon_level_requirements": self.options.ignore_cannon_level_requirements.value,
            "boostless_springboards": self.options.boostless_springboards.value,
            "boostless_spirit_races": self.options.boostless_spirit_races.value,
            "boostless_torch_races": self.options.boostless_torch_races.value,
            "enable_primordial_crystal_logic": self.options.enable_primordial_crystal_logic.value,
            "progressive_dash": self.options.progressive_dash.value,
            "dashless_gaps": self.options.dashless_gaps.value,
            "completion_goals": self.options.completion_goals.value,
            "ap_world_version": self.ap_world_version
        }

        return slot_data
