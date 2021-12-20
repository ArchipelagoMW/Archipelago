import unittest
from worlds.AutoWorld import World
from Fill import fill_restrictive
from BaseClasses import MultiWorld, Region, RegionType, Item, Location
from worlds.generic.Rules import set_rule


def generate_multi_world() -> MultiWorld:
    multi_world = MultiWorld(1)
    player1_id = 1
    world = World(multi_world, player1_id)
    multi_world.game[player1_id] = world
    multi_world.worlds[player1_id] = world
    multi_world.player_name = {player1_id: "Test Player 1"}
    multi_world.set_seed()
    # args = Namespace()
    # for name, option in world_type.options.items():
    #     setattr(args, name, {1: option.from_any(option.default)})
    # multi_world.set_options(args)
    multi_world.set_default_common_options()

    region = Region("Menu", RegionType.Generic,
                    "Menu Region Hint", player1_id, multi_world)
    multi_world.regions.append(region)

    return multi_world


def generate_locations(count: int, player_id: int, address: int = None, region: Region = None) -> list[Location]:
    locations = []
    for i in range(count):
        name = "player" + str(player_id) + "_location" + str(i)
        location = Location(player_id, name, address, region)
        locations.append(location)
        region.locations.append(location)
    return locations


def generate_items(count: int, player_id: int, advancement: bool = False, code: int = None) -> list[Location]:
    items = []
    for i in range(count):
        name = "player" + str(player_id) + "_item" + str(i)
        items.append(Item(name, advancement, code, player_id))
    return items


class TestBase(unittest.TestCase):
    def test_basic_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1_id = 1
        player1_menu = multi_world.get_region("Menu", player1_id)

        locations = generate_locations(2, player1_id, None, player1_menu)
        items = generate_items(2, player1_id, True)

        item0 = items[0]
        item1 = items[1]
        loc0 = locations[0]
        loc1 = locations[1]

        fill_restrictive(multi_world, multi_world.state, locations, items)

        self.assertEqual(loc0.item, item1)
        self.assertEqual(loc1.item, item0)
        self.assertEqual([], locations)
        self.assertEqual([], items)

    def test_ordered_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1_id = 1
        player1_menu = multi_world.get_region("Menu", player1_id)

        locations = generate_locations(2, player1_id, None, player1_menu)
        items = generate_items(2, player1_id, True)

        item0 = items[0]
        item1 = items[1]
        loc0 = locations[0]
        loc1 = locations[1]

        multi_world.completion_condition[player1_id] = lambda state: state.has(
            item0.name, player1_id) and state.has(item1.name, player1_id)
        set_rule(loc1, lambda state: state.has(item0.name, player1_id))
        fill_restrictive(multi_world, multi_world.state, locations, items)

        self.assertEqual(loc0.item, item0)
        self.assertEqual(loc1.item, item1)

    def test_reversed_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1_id = 1
        player1_menu = multi_world.get_region("Menu", player1_id)

        locations = generate_locations(2, player1_id, None, player1_menu)
        items = generate_items(2, player1_id, True)

        item0 = items[0]
        item1 = items[1]
        loc0 = locations[0]
        loc1 = locations[1]

        multi_world.completion_condition[player1_id] = lambda state: state.has(
            item0.name, player1_id) and state.has(item1.name, player1_id)
        set_rule(loc1, lambda state: state.has(item1.name, player1_id))
        fill_restrictive(multi_world, multi_world.state, locations, items)

        self.assertEqual(loc0.item, item1)
        self.assertEqual(loc1.item, item0)