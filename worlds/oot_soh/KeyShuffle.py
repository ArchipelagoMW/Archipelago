from typing import TYPE_CHECKING
from collections import namedtuple
from Fill import fill_restrictive

from .Items import Items, item_data_table
from .Locations import Location, location_data_table
from .Regions import dungeon_reward_item_mapping, map_and_compass_vanilla_mapping
from .Enums import KeyShuffleLocations, Locations
from .ShopItems import get_vanilla_shop_locations
from .SongShuffle import dungeon_reward_song_locations
from .LogicHelpers import key_to_ring

if TYPE_CHECKING:
    from . import SohWorld

option_mapping = namedtuple('Key_Mapping', ['Dungeon', 'Option', 'Quantity'])

def get_own_dungeon_prefill_items(world: "SohWorld") -> dict[KeyShuffleLocations, list[Items]]:
        key_shuffle_locations = dict[KeyShuffleLocations, list[Items]]()
        for location_type in KeyShuffleLocations:
            key_shuffle_locations[location_type] = list[Items]()

        # Boss Keys
        if world.options.boss_key_shuffle == "own_dungeon":
            key_shuffle_locations[KeyShuffleLocations.FOREST_TEMPLE].append(Items.FOREST_TEMPLE_BOSS_KEY)
            key_shuffle_locations[KeyShuffleLocations.FIRE_TEMPLE].append(Items.FIRE_TEMPLE_BOSS_KEY)
            key_shuffle_locations[KeyShuffleLocations.WATER_TEMPLE].append(Items.WATER_TEMPLE_BOSS_KEY)
            key_shuffle_locations[KeyShuffleLocations.SPIRIT_TEMPLE].append(Items.SPIRIT_TEMPLE_BOSS_KEY)
            key_shuffle_locations[KeyShuffleLocations.SHADOW_TEMPLE].append(Items.SHADOW_TEMPLE_BOSS_KEY)

        # Small Keys
        small_key_option_mapping = small_key_option_matching(world)
        
        if world.options.small_key_shuffle == "own_dungeon":
            # Put the small keys or keyrings in the appropriate pool
            for key, data in small_key_option_mapping.items():
                dungeon = data.Dungeon
                key_ring_option = data.Option

                if key_ring_option:
                    item = key_to_ring[key]
                    count = 1
                else:
                    item = key
                    count = data.Quantity

                for _ in range(count):
                    key_shuffle_locations[dungeon].append(item)

        # Maps and Compasses
        if world.options.maps_and_compasses == "own_dungeon":
            map_and_compass_dungeon_mapping: dict[KeyShuffleLocations, list[Items]] = {
                KeyShuffleLocations.DEKU_TREE : [Items.GREAT_DEKU_TREE_MAP, Items.GREAT_DEKU_TREE_COMPASS],
                KeyShuffleLocations.DODONGOS_CAVERN : [Items.DODONGOS_CAVERN_MAP, Items.DODONGOS_CAVERN_COMPASS],
                KeyShuffleLocations.JABU_JABUS_BELLY : [Items.JABU_JABUS_BELLY_MAP, Items.JABU_JABUS_BELLY_COMPASS],
                KeyShuffleLocations.FOREST_TEMPLE : [Items.FOREST_TEMPLE_MAP, Items.FOREST_TEMPLE_COMPASS],
                KeyShuffleLocations.FIRE_TEMPLE : [Items.FIRE_TEMPLE_MAP, Items.FIRE_TEMPLE_COMPASS],
                KeyShuffleLocations.WATER_TEMPLE : [Items.WATER_TEMPLE_MAP, Items.WATER_TEMPLE_COMPASS],
                KeyShuffleLocations.SPIRIT_TEMPLE : [Items.SPIRIT_TEMPLE_MAP, Items.SPIRIT_TEMPLE_COMPASS],
                KeyShuffleLocations.SHADOW_TEMPLE : [Items.SHADOW_TEMPLE_MAP, Items.SHADOW_TEMPLE_COMPASS],
                KeyShuffleLocations.BOTTOM_OF_THE_WELL : [Items.BOTTOM_OF_THE_WELL_MAP, Items.BOTTOM_OF_THE_WELL_COMPASS],
                KeyShuffleLocations.ICE_CAVERN : [Items.ICE_CAVERN_MAP, Items.ICE_CAVERN_COMPASS]
            }

            for shuffle_location, items in map_and_compass_dungeon_mapping.items():
                key_shuffle_locations[shuffle_location] += items

        return key_shuffle_locations

def get_any_dungeon_prefill_items(world: "SohWorld") -> list[Items]:
        any_dungeon_items = list[Items]()

        # Boss Keys
        if world.options.boss_key_shuffle == "any_dungeon":
            any_dungeon_items += [Items.FOREST_TEMPLE_BOSS_KEY, Items.FIRE_TEMPLE_BOSS_KEY, Items.WATER_TEMPLE_BOSS_KEY, Items.SPIRIT_TEMPLE_BOSS_KEY, Items.SHADOW_TEMPLE_BOSS_KEY]

        # Small Keys
        small_key_option_mapping = small_key_option_matching(world)
        
        if world.options.small_key_shuffle == "any_dungeon":
            # Put the small keys or keyrings in the appropriate pool
            for key, data in small_key_option_mapping.items():
                key_ring_option = data.Option

                if key_ring_option:
                    item = key_to_ring[key]
                    count = 1
                else:
                    item = key
                    count = data.Quantity

                for _ in range(count):
                    any_dungeon_items.append(item)

        # Gerudo Fortress Keys
        if world.options.fortress_carpenters != "free":
            if world.options.gerudo_fortress_key_shuffle == "any_dungeon":
                if world.options.gerudo_fortress_key_ring and world.options.fortress_carpenters == "normal" and world.options.gerudo_fortress_key_shuffle != "vanilla":
                    any_dungeon_items.append(Items.GERUDO_FORTRESS_KEY_RING)
                else:
                    for _ in range(item_data_table[Items.GERUDO_FORTRESS_SMALL_KEY].quantity_in_item_pool if world.options.fortress_carpenters == "normal" else 1):
                        any_dungeon_items.append(Items.GERUDO_FORTRESS_SMALL_KEY)

        # Maps and Compasses
        if world.options.maps_and_compasses == "any_dungeon":
            any_dungeon_items += list(map_and_compass_vanilla_mapping.values())

        return any_dungeon_items
        
def get_overworld_prefill_items(world: "SohWorld") -> list[Items]:
        overworld_items = list[Items]()

        # Boss Keys
        if world.options.boss_key_shuffle == "overworld":
            overworld_items += [Items.FOREST_TEMPLE_BOSS_KEY, Items.FIRE_TEMPLE_BOSS_KEY, Items.WATER_TEMPLE_BOSS_KEY, Items.SPIRIT_TEMPLE_BOSS_KEY, Items.SHADOW_TEMPLE_BOSS_KEY]

        # Small Keys
        small_key_option_mapping = small_key_option_matching(world)
        
        if world.options.small_key_shuffle == "overworld":
            # Put the small keys or keyrings in the appropriate pool
            for key, data in small_key_option_mapping.items():
                key_ring_option = data.Option

                if key_ring_option:
                    item = key_to_ring[key]
                    count = 1
                else:
                    item = key
                    count = data.Quantity

                for _ in range(count):
                    overworld_items.append(item)

        # Gerudo Fortress Keys
        if world.options.fortress_carpenters != "free":
            if world.options.gerudo_fortress_key_shuffle == "overworld":
                if world.options.gerudo_fortress_key_ring and world.options.fortress_carpenters == "normal" and world.options.gerudo_fortress_key_shuffle != "vanilla":
                    overworld_items.append(Items.GERUDO_FORTRESS_KEY_RING)
                else:
                    for _ in range(item_data_table[Items.GERUDO_FORTRESS_SMALL_KEY].quantity_in_item_pool if world.options.fortress_carpenters == "normal" else 1):
                        overworld_items.append(Items.GERUDO_FORTRESS_SMALL_KEY)

        # Maps and Compasses
        if world.options.maps_and_compasses == "overworld":
            overworld_items += list(map_and_compass_vanilla_mapping.values())

        return overworld_items

def pre_fill_own_dungeon_items(world: "SohWorld") -> None:
        all_locations: list[str] = [location.name for location in world.multiworld.get_unfilled_locations(world.player)]
        reserved_locations: list[Locations] = []

        # Reserve dungeon reward locations if a dungeon reward should be there
        if world.options.shuffle_dungeon_rewards != "anywhere":
            reserved_locations += list(dungeon_reward_item_mapping.keys())

        if world.options.shuffle_songs == "dungeon_rewards":
            reserved_locations += dungeon_reward_song_locations

        key_shuffle_keys = get_own_dungeon_prefill_items(world)
        key_shuffle_locations = dict[KeyShuffleLocations, list[Locations]]()
        for location_type in KeyShuffleLocations:
            key_shuffle_locations[location_type] = list[Locations]()

        # This loops through all unfilled locations in the players world, removes any from our reserved list (Shops and Dungeon Rewards if applicable), then sorts them into three categories: Overworld, Any Dungeon, and Own Dungeon
        for name, data in location_data_table.items():
            if name in all_locations and name not in reserved_locations:
                if data.key_suffle_location != None:
                    key_shuffle_locations[data.key_suffle_location].append(Locations(name))

        # Resolve own_dungeon
        for shuffle_location, keys in key_shuffle_keys.items():
            if not keys:
                continue

            # use full dungeon accessability as the goal for filling
            own_dungeon_location_goal = [world.get_location(loc) for loc in key_shuffle_locations[shuffle_location]]
            world.multiworld.completion_condition[world.player] = lambda state: all([state.can_reach(loc) for loc in own_dungeon_location_goal])

            # remove items from the prefill pool
            for key in keys:
                if key in world.pre_fill_pool: 
                    world.pre_fill_pool.remove(key)

            prefill_state = world.get_pre_fill_state()

            empty_locations = world.get_empty_locations_from_list_shuffled(key_shuffle_locations[shuffle_location])
            key_items = [world.create_item(str(key)) for key in keys]

            fill_restrictive(world.multiworld, prefill_state, empty_locations, key_items, single_player_placement=True, lock=True) 

def pre_fill_any_dungeon_keys(world: "SohWorld") -> None:
        all_locations: list[str] = [location.name for location in world.multiworld.get_unfilled_locations(world.player)]
        reserved_locations: list[Locations] = []

        # Reserve dungeon reward locations if a dungeon reward should be there
        if world.options.shuffle_dungeon_rewards != "anywhere":
            reserved_locations += [location for location in dungeon_reward_item_mapping.keys()]

        if world.options.shuffle_songs == "dungeon_rewards":
            reserved_locations += dungeon_reward_song_locations

        any_dungeon_items = get_any_dungeon_prefill_items(world)
        any_dungeon_locations = list[Locations]()

        # This loops through all unfilled locations in the players world, removes any from our reserved list (Shops and Dungeon Rewards if applicable), then sorts them into three categories: Overworld, Any Dungeon, and Own Dungeon
        for name, data in location_data_table.items():
            if name in all_locations and name not in reserved_locations:
                if data.key_suffle_location != None:
                    any_dungeon_locations.append(Locations(name))

        # use full dungeon accessability as the goal for filling
        all_dungeon_location_goal = [world.get_location(loc) for loc in any_dungeon_locations]
        world.multiworld.completion_condition[world.player] = lambda state: all([state.can_reach(loc) for loc in all_dungeon_location_goal])

        # Resolve any_dungeon
        for item in any_dungeon_items:
            if item in world.pre_fill_pool: 
                world.pre_fill_pool.remove(item)

        prefill_state = world.get_pre_fill_state()

        empty_locations = world.get_empty_locations_from_list_shuffled(any_dungeon_locations)
        key_items = [world.create_item(str(item)) for item in any_dungeon_items]

        fill_restrictive(world.multiworld, prefill_state, empty_locations, key_items, single_player_placement=True, lock=True)

def pre_fill_overworld_items(world: "SohWorld") -> None:
        all_locations: list[str] = [location.name for location in world.multiworld.get_unfilled_locations(world.player)]
        reserved_locations: list[Locations] = []

        # Reserve Shop Locations
        for shop_loc in get_vanilla_shop_locations(world):
            reserved_locations.append(Locations(shop_loc))

        overworld_items = get_overworld_prefill_items(world)
        overworld_locations = list[Locations]()

        # This loops through all unfilled locations in the players world, removes any from our reserved list (Shops and Dungeon Rewards if applicable), then sorts them into three categories: Overworld, Any Dungeon, and Own Dungeon
        for name, data in location_data_table.items():
            if name in all_locations and name not in reserved_locations:
                if data.key_suffle_location == None:
                    overworld_locations.append(Locations(name))

        # use full dungeon accessability as the goal for filling
        all_dungeon_location_goal = [world.get_location(loc) for loc in overworld_locations]
        world.multiworld.completion_condition[world.player] = lambda state: all([state.can_reach(loc) for loc in all_dungeon_location_goal])

        # Resolve overworld
        for item in overworld_items:
            if item in world.pre_fill_pool: 
                world.pre_fill_pool.remove(item)

        prefill_state = world.get_pre_fill_state()

        empty_locations = world.get_empty_locations_from_list_shuffled(overworld_locations)
        key_items = [world.create_item(str(item)) for item in overworld_items]

        fill_restrictive(world.multiworld, prefill_state, empty_locations, key_items, single_player_placement=True, lock=True)

def small_key_option_matching(world: "SohWorld") -> dict[Items, option_mapping]:
    return {
            Items.FOREST_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.FOREST_TEMPLE, world.options.forest_temple_key_ring, item_data_table[Items.FOREST_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.FIRE_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.FIRE_TEMPLE, world.options.fire_temple_key_ring, item_data_table[Items.FIRE_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.WATER_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.WATER_TEMPLE, world.options.water_temple_key_ring, item_data_table[Items.WATER_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.SPIRIT_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.SPIRIT_TEMPLE, world.options.spirit_temple_key_ring, item_data_table[Items.SPIRIT_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.SHADOW_TEMPLE_SMALL_KEY: option_mapping(KeyShuffleLocations.SHADOW_TEMPLE, world.options.shadow_temple_key_ring, item_data_table[Items.SHADOW_TEMPLE_SMALL_KEY].quantity_in_item_pool),
            Items.BOTTOM_OF_THE_WELL_SMALL_KEY: option_mapping(KeyShuffleLocations.BOTTOM_OF_THE_WELL, world.options.bottom_of_the_well_key_ring, item_data_table[Items.BOTTOM_OF_THE_WELL_SMALL_KEY].quantity_in_item_pool),
            Items.GANONS_CASTLE_SMALL_KEY: option_mapping(KeyShuffleLocations.GANONS_CASTLE, world.options.ganons_castle_key_ring, item_data_table[Items.GANONS_CASTLE_SMALL_KEY].quantity_in_item_pool),
            Items.TRAINING_GROUND_SMALL_KEY: option_mapping(KeyShuffleLocations.GERUDO_TRAINING_GROUNDS, world.options.gerudo_training_ground_key_ring, item_data_table[Items.TRAINING_GROUND_SMALL_KEY].quantity_in_item_pool)
        }