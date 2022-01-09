from typing import NamedTuple, List
import unittest
from worlds.AutoWorld import World
from Fill import FillError, fill_restrictive
from BaseClasses import MultiWorld, Region, RegionType, Item, Location
from worlds.generic.Rules import set_rule


def generate_multi_world(players: int = 1) -> MultiWorld:
    multi_world = MultiWorld(players)
    multi_world.player_name = {}
    for i in range(players):
        player_id = i+1
        world = World(multi_world, player_id)
        multi_world.game[player_id] = world
        multi_world.worlds[player_id] = world
        multi_world.player_name[player_id] = "Test Player " + str(player_id)
        region = Region("Menu", RegionType.Generic,
                        "Menu Region Hint", player_id, multi_world)
        multi_world.regions.append(region)

    multi_world.set_seed()
    multi_world.set_default_common_options()

    return multi_world


class PlayerDefinition(NamedTuple):
    id: int
    menu: Region
    locations: List[Location]
    prog_items: List[Item]


def generate_player_data(multi_world: MultiWorld, player_id: int, location_count: int, prog_item_count: int) -> PlayerDefinition:
    menu = multi_world.get_region("Menu", player_id)
    locations = generate_locations(location_count, player_id, None, menu)
    prog_items = generate_items(prog_item_count, player_id, True)

    return PlayerDefinition(player_id, menu, locations, prog_items)


def generate_locations(count: int, player_id: int, address: int = None, region: Region = None) -> List[Location]:
    locations = []
    for i in range(count):
        name = "player" + str(player_id) + "_location" + str(i)
        location = Location(player_id, name, address, region)
        locations.append(location)
        region.locations.append(location)
    return locations


def generate_items(count: int, player_id: int, advancement: bool = False, code: int = None) -> List[Item]:
    items = []
    for i in range(count):
        name = "player" + str(player_id) + "_item" + str(i)
        items.append(Item(name, advancement, code, player_id))
    return items


class TestBase(unittest.TestCase):
    def test_basic_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 2, 2)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        loc0 = player1.locations[0]
        loc1 = player1.locations[1]

        fill_restrictive(multi_world, multi_world.state,
                         player1.locations, player1.prog_items)

        self.assertEqual(loc0.item, item1)
        self.assertEqual(loc1.item, item0)
        self.assertEqual([], player1.locations)
        self.assertEqual([], player1.prog_items)

    def test_ordered_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 2, 2)
        items = player1.prog_items
        locations = player1.locations

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            items[0].name, player1.id) and state.has(items[1].name, player1.id)
        set_rule(locations[1], lambda state: state.has(
            items[0].name, player1.id))
        fill_restrictive(multi_world, multi_world.state,
                         player1.locations.copy(), player1.prog_items.copy())

        self.assertEqual(locations[0].item, items[0])
        self.assertEqual(locations[1].item, items[1])

    def test_fill_restrictive_remaining_locations(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 3, 2)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        loc0 = player1.locations[0]
        loc1 = player1.locations[1]
        loc2 = player1.locations[2]

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            item0.name, player1.id) and state.has(item1.name, player1.id)
        set_rule(loc1, lambda state: state.has(
            item0.name, player1.id))
        #forces a swap
        set_rule(loc2, lambda state: state.has(
            item0.name, player1.id))
        fill_restrictive(multi_world, multi_world.state,
                         player1.locations, player1.prog_items)

        self.assertEqual(loc0.item, item0)
        self.assertEqual(loc1.item, item1)
        self.assertEqual(1, len(player1.locations))
        self.assertEqual(player1.locations[0], loc2)

    def test_minimal_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 2, 2)

        items = player1.prog_items
        locations = player1.locations

        multi_world.accessibility[player1.id] = 'minimal'
        multi_world.completion_condition[player1.id] = lambda state: state.has(
            items[1].name, player1.id)
        set_rule(locations[1], lambda state: state.has(
            items[0].name, player1.id))

        fill_restrictive(multi_world, multi_world.state,
                         player1.locations.copy(), player1.prog_items.copy())

        self.assertEqual(locations[0].item, items[1])
        # Unnecessary unreachable Item
        self.assertEqual(locations[1].item, items[0])

    def test_reversed_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 2, 2)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        loc0 = player1.locations[0]
        loc1 = player1.locations[1]

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            item0.name, player1.id) and state.has(item1.name, player1.id)
        set_rule(loc1, lambda state: state.has(item1.name, player1.id))
        fill_restrictive(multi_world, multi_world.state,
                         player1.locations, player1.prog_items)

        self.assertEqual(loc0.item, item1)
        self.assertEqual(loc1.item, item0)

    def test_multi_step_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 4, 4)

        items = player1.prog_items
        locations = player1.locations

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            items[2].name, player1.id) and state.has(items[3].name, player1.id)
        set_rule(locations[1], lambda state: state.has(
            items[0].name, player1.id))
        set_rule(locations[2], lambda state: state.has(
            items[1].name, player1.id))
        set_rule(locations[3], lambda state: state.has(
            items[1].name, player1.id))

        fill_restrictive(multi_world, multi_world.state,
                         player1.locations.copy(), player1.prog_items.copy())

        self.assertEqual(locations[0].item, items[1])
        self.assertEqual(locations[1].item, items[2])
        self.assertEqual(locations[2].item, items[0])
        self.assertEqual(locations[3].item, items[3])

    def test_impossible_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 2, 2)
        items = player1.prog_items
        locations = player1.locations

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            items[0].name, player1.id) and state.has(items[1].name, player1.id)
        set_rule(locations[1], lambda state: state.has(
            items[1].name, player1.id))
        set_rule(locations[0], lambda state: state.has(
            items[0].name, player1.id))

        self.assertRaises(FillError, fill_restrictive, multi_world, multi_world.state,
                          player1.locations.copy(), player1.prog_items.copy())

    def test_circular_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 3, 3)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        item2 = player1.prog_items[2]
        loc0 = player1.locations[0]
        loc1 = player1.locations[1]
        loc2 = player1.locations[2]

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            item0.name, player1.id) and state.has(item1.name, player1.id) and state.has(item2.name, player1.id)
        set_rule(loc1, lambda state: state.has(item0.name, player1.id))
        set_rule(loc2, lambda state: state.has(item1.name, player1.id))
        set_rule(loc0, lambda state: state.has(item2.name, player1.id))

        self.assertRaises(FillError, fill_restrictive, multi_world, multi_world.state,
                          player1.locations.copy(), player1.prog_items.copy())

    def test_competing_fill_restrictive(self):
        multi_world = generate_multi_world()
        player1 = generate_player_data(multi_world, 1, 2, 2)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        loc1 = player1.locations[1]

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            item0.name, player1.id) and state.has(item0.name, player1.id) and state.has(item1.name, player1.id)
        set_rule(loc1, lambda state: state.has(item0.name, player1.id)
                 and state.has(item1.name, player1.id))

        self.assertRaises(FillError, fill_restrictive, multi_world, multi_world.state,
                          player1.locations.copy(), player1.prog_items.copy())

    def test_multiplayer_fill_restrictive(self):
        multi_world = generate_multi_world(2)
        player1 = generate_player_data(multi_world, 1, 2, 2)
        player2 = generate_player_data(multi_world, 2, 2, 2)

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            player1.prog_items[0].name, player1.id) and state.has(
            player1.prog_items[1].name, player1.id)
        multi_world.completion_condition[player2.id] = lambda state: state.has(
            player2.prog_items[0].name, player2.id) and state.has(
            player2.prog_items[1].name, player2.id)

        fill_restrictive(multi_world, multi_world.state, player1.locations +
                         player2.locations, player1.prog_items + player2.prog_items)

        self.assertEqual(player1.locations[0].item, player1.prog_items[1])
        self.assertEqual(player1.locations[1].item, player2.prog_items[1])
        self.assertEqual(player2.locations[0].item, player1.prog_items[0])
        self.assertEqual(player2.locations[1].item, player2.prog_items[0])

    def test_multiplayer_rules_fill_restrictive(self):
        multi_world = generate_multi_world(2)
        player1 = generate_player_data(multi_world, 1, 2, 2)
        player2 = generate_player_data(multi_world, 2, 2, 2)

        multi_world.completion_condition[player1.id] = lambda state: state.has(
            player1.prog_items[0].name, player1.id) and state.has(
            player1.prog_items[1].name, player1.id)
        multi_world.completion_condition[player2.id] = lambda state: state.has(
            player2.prog_items[0].name, player2.id) and state.has(
            player2.prog_items[1].name, player2.id)

        set_rule(player2.locations[1], lambda state: state.has(
            player2.prog_items[0].name, player2.id))

        fill_restrictive(multi_world, multi_world.state, player1.locations +
                         player2.locations, player1.prog_items + player2.prog_items)

        self.assertEqual(player1.locations[0].item, player2.prog_items[0])
        self.assertEqual(player1.locations[1].item, player2.prog_items[1])
        self.assertEqual(player2.locations[0].item, player1.prog_items[0])
        self.assertEqual(player2.locations[1].item, player1.prog_items[1])
