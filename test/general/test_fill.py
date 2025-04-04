from typing import List, Iterable
import unittest

from Options import Accessibility
from test.general import generate_items, generate_locations, generate_test_multiworld
from Fill import FillError, balance_multiworld_progression, fill_restrictive, \
    distribute_early_items, distribute_items_restrictive
from BaseClasses import Entrance, LocationProgressType, MultiWorld, Region, Item, Location, \
    ItemClassification
from worlds.generic.Rules import CollectionRule, add_item_rule, locality_rules, set_rule


class PlayerDefinition(object):
    multiworld: MultiWorld
    id: int
    menu: Region
    locations: List[Location]
    prog_items: List[Item]
    basic_items: List[Item]
    regions: List[Region]

    def __init__(self, multiworld: MultiWorld, id: int, menu: Region, locations: List[Location] = [], prog_items: List[Item] = [], basic_items: List[Item] = []):
        self.multiworld = multiworld
        self.id = id
        self.menu = menu
        self.locations = locations
        self.prog_items = prog_items
        self.basic_items = basic_items
        self.regions = [menu]

    def generate_region(self, parent: Region, size: int, access_rule: CollectionRule = lambda state: True) -> Region:
        region_tag = f"_region{len(self.regions)}"
        region_name = f"player{self.id}{region_tag}"
        region = Region(f"player{self.id}{region_tag}", self.id, self.multiworld)
        self.locations += generate_locations(size, self.id, region, None, region_tag)

        entrance = Entrance(self.id, f"{region_name}_entrance", parent)
        parent.exits.append(entrance)
        entrance.connect(region)
        entrance.access_rule = access_rule

        self.regions.append(region)
        self.multiworld.regions.append(region)

        return region


def fill_region(multiworld: MultiWorld, region: Region, items: List[Item]) -> List[Item]:
    items = items.copy()
    while len(items) > 0:
        location = region.locations.pop(0)
        region.locations.append(location)
        if location.item:
            return items
        item = items.pop(0)
        multiworld.push_item(location, item, False)

    return items


def region_contains(region: Region, item: Item) -> bool:
    for location in region.locations:
        if location.item == item:
            return True

    return False


def generate_player_data(multiworld: MultiWorld, player_id: int, location_count: int = 0, prog_item_count: int = 0, basic_item_count: int = 0) -> PlayerDefinition:
    menu = multiworld.get_region("Menu", player_id)
    locations = generate_locations(location_count, player_id, menu, None)
    prog_items = generate_items(prog_item_count, player_id, True)
    multiworld.itempool += prog_items
    basic_items = generate_items(basic_item_count, player_id, False)
    multiworld.itempool += basic_items

    return PlayerDefinition(multiworld, player_id, menu, locations, prog_items, basic_items)


def names(objs: list) -> Iterable[str]:
    return map(lambda o: o.name, objs)


class TestFillRestrictive(unittest.TestCase):
    def test_basic_fill(self):
        """Tests `fill_restrictive` fills and removes the locations and items from their respective lists"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 2, 2)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        loc0 = player1.locations[0]
        loc1 = player1.locations[1]

        fill_restrictive(multiworld, multiworld.state,
                         player1.locations, player1.prog_items)

        self.assertEqual(loc0.item, item1)
        self.assertEqual(loc1.item, item0)
        self.assertEqual([], player1.locations)
        self.assertEqual([], player1.prog_items)

    def test_ordered_fill(self):
        """Tests `fill_restrictive` fulfills set rules"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 2, 2)
        items = player1.prog_items
        locations = player1.locations

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            items[0].name, player1.id) and state.has(items[1].name, player1.id)
        set_rule(locations[1], lambda state: state.has(
            items[0].name, player1.id))
        fill_restrictive(multiworld, multiworld.state,
                         player1.locations.copy(), player1.prog_items.copy())

        self.assertEqual(locations[0].item, items[0])
        self.assertEqual(locations[1].item, items[1])

    def test_partial_fill(self):
        """Tests that `fill_restrictive` returns unfilled locations"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 3, 2)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        loc0 = player1.locations[0]
        loc1 = player1.locations[1]
        loc2 = player1.locations[2]

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            item0.name, player1.id) and state.has(item1.name, player1.id)
        set_rule(loc1, lambda state: state.has(
            item0.name, player1.id))
        # forces a swap
        set_rule(loc2, lambda state: state.has(
            item0.name, player1.id))
        fill_restrictive(multiworld, multiworld.state,
                         player1.locations, player1.prog_items)

        self.assertEqual(loc0.item, item0)
        self.assertEqual(loc1.item, item1)
        self.assertEqual(1, len(player1.locations))
        self.assertEqual(player1.locations[0], loc2)

    def test_minimal_fill(self):
        """Test that fill for minimal player can have unreachable items"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 2, 2)

        items = player1.prog_items
        locations = player1.locations

        multiworld.worlds[player1.id].options.accessibility = Accessibility.from_any(Accessibility.option_minimal)
        multiworld.completion_condition[player1.id] = lambda state: state.has(
            items[1].name, player1.id)
        set_rule(locations[1], lambda state: state.has(
            items[0].name, player1.id))

        fill_restrictive(multiworld, multiworld.state,
                         player1.locations.copy(), player1.prog_items.copy())

        self.assertEqual(locations[0].item, items[1])
        # Unnecessary unreachable Item
        self.assertEqual(locations[1].item, items[0])

    def test_minimal_mixed_fill(self):
        """
        Test that fill for 1 minimal and 1 non-minimal player will correctly place items in a way that lets
        the non-minimal player get all items.
        """

        multiworld = generate_test_multiworld(2)
        player1 = generate_player_data(multiworld, 1, 3, 3)
        player2 = generate_player_data(multiworld, 2, 3, 3)

        multiworld.worlds[player1.id].options.accessibility.value = Accessibility.option_minimal
        multiworld.worlds[player2.id].options.accessibility.value = Accessibility.option_full

        multiworld.completion_condition[player1.id] = lambda state: True
        multiworld.completion_condition[player2.id] = lambda state: state.has(player2.prog_items[2].name, player2.id)

        set_rule(player1.locations[1], lambda state: state.has(player1.prog_items[0].name, player1.id))
        set_rule(player1.locations[2], lambda state: state.has(player1.prog_items[1].name, player1.id))
        set_rule(player2.locations[1], lambda state: state.has(player2.prog_items[0].name, player2.id))
        set_rule(player2.locations[2], lambda state: state.has(player2.prog_items[1].name, player2.id))

        # force-place an item that makes it impossible to have all locations accessible
        player1.locations[0].place_locked_item(player1.prog_items[2])

        # fill remaining locations with remaining items
        location_pool = player1.locations[1:] + player2.locations
        item_pool = player1.prog_items[:-1] + player2.prog_items
        fill_restrictive(multiworld, multiworld.state, location_pool, item_pool)
        multiworld.state.sweep_for_advancements()  # collect everything

        # all of player2's locations and items should be accessible (not all of player1's)
        for item in player2.prog_items:
            self.assertTrue(multiworld.state.has(item.name, player2.id),
                            f"{item} is unreachable in {item.location}")

    def test_reversed_fill(self):
        """Test a different set of rules can be satisfied"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 2, 2)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        loc0 = player1.locations[0]
        loc1 = player1.locations[1]

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            item0.name, player1.id) and state.has(item1.name, player1.id)
        set_rule(loc1, lambda state: state.has(item1.name, player1.id))
        fill_restrictive(multiworld, multiworld.state,
                         player1.locations, player1.prog_items)

        self.assertEqual(loc0.item, item1)
        self.assertEqual(loc1.item, item0)

    def test_multi_step_fill(self):
        """Test that fill is able to satisfy multiple spheres"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 4, 4)

        items = player1.prog_items
        locations = player1.locations

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            items[2].name, player1.id) and state.has(items[3].name, player1.id)
        set_rule(locations[1], lambda state: state.has(
            items[0].name, player1.id))
        set_rule(locations[2], lambda state: state.has(
            items[1].name, player1.id))
        set_rule(locations[3], lambda state: state.has(
            items[1].name, player1.id))

        fill_restrictive(multiworld, multiworld.state,
                         player1.locations.copy(), player1.prog_items.copy())

        self.assertEqual(locations[0].item, items[1])
        self.assertEqual(locations[1].item, items[2])
        self.assertEqual(locations[2].item, items[0])
        self.assertEqual(locations[3].item, items[3])

    def test_impossible_fill(self):
        """Test that fill raises an error when it can't place any items"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 2, 2)
        items = player1.prog_items
        locations = player1.locations

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            items[0].name, player1.id) and state.has(items[1].name, player1.id)
        set_rule(locations[1], lambda state: state.has(
            items[1].name, player1.id))
        set_rule(locations[0], lambda state: state.has(
            items[0].name, player1.id))

        self.assertRaises(FillError, fill_restrictive, multiworld, multiworld.state,
                          player1.locations.copy(), player1.prog_items.copy())

    def test_circular_fill(self):
        """Test that fill raises an error when it can't place all items"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 3, 3)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        item2 = player1.prog_items[2]
        loc0 = player1.locations[0]
        loc1 = player1.locations[1]
        loc2 = player1.locations[2]

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            item0.name, player1.id) and state.has(item1.name, player1.id) and state.has(item2.name, player1.id)
        set_rule(loc1, lambda state: state.has(item0.name, player1.id))
        set_rule(loc2, lambda state: state.has(item1.name, player1.id))
        set_rule(loc0, lambda state: state.has(item2.name, player1.id))

        self.assertRaises(FillError, fill_restrictive, multiworld, multiworld.state,
                          player1.locations.copy(), player1.prog_items.copy())

    def test_competing_fill(self):
        """Test that fill raises an error when it can't place items in a way to satisfy the conditions"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 2, 2)

        item0 = player1.prog_items[0]
        item1 = player1.prog_items[1]
        loc1 = player1.locations[1]

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            item0.name, player1.id) and state.has(item0.name, player1.id) and state.has(item1.name, player1.id)
        set_rule(loc1, lambda state: state.has(item0.name, player1.id)
                 and state.has(item1.name, player1.id))

        self.assertRaises(FillError, fill_restrictive, multiworld, multiworld.state,
                          player1.locations.copy(), player1.prog_items.copy())

    def test_multiplayer_fill(self):
        """Test that items can be placed across worlds"""
        multiworld = generate_test_multiworld(2)
        player1 = generate_player_data(multiworld, 1, 2, 2)
        player2 = generate_player_data(multiworld, 2, 2, 2)

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            player1.prog_items[0].name, player1.id) and state.has(
            player1.prog_items[1].name, player1.id)
        multiworld.completion_condition[player2.id] = lambda state: state.has(
            player2.prog_items[0].name, player2.id) and state.has(
            player2.prog_items[1].name, player2.id)

        fill_restrictive(multiworld, multiworld.state, player1.locations +
                         player2.locations, player1.prog_items + player2.prog_items)

        self.assertEqual(player1.locations[0].item, player1.prog_items[1])
        self.assertEqual(player1.locations[1].item, player2.prog_items[1])
        self.assertEqual(player2.locations[0].item, player1.prog_items[0])
        self.assertEqual(player2.locations[1].item, player2.prog_items[0])

    def test_multiplayer_rules_fill(self):
        """Test that fill across worlds satisfies the rules"""
        multiworld = generate_test_multiworld(2)
        player1 = generate_player_data(multiworld, 1, 2, 2)
        player2 = generate_player_data(multiworld, 2, 2, 2)

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            player1.prog_items[0].name, player1.id) and state.has(
            player1.prog_items[1].name, player1.id)
        multiworld.completion_condition[player2.id] = lambda state: state.has(
            player2.prog_items[0].name, player2.id) and state.has(
            player2.prog_items[1].name, player2.id)

        set_rule(player2.locations[1], lambda state: state.has(
            player2.prog_items[0].name, player2.id))

        fill_restrictive(multiworld, multiworld.state, player1.locations +
                         player2.locations, player1.prog_items + player2.prog_items)

        self.assertEqual(player1.locations[0].item, player2.prog_items[0])
        self.assertEqual(player1.locations[1].item, player2.prog_items[1])
        self.assertEqual(player2.locations[0].item, player1.prog_items[0])
        self.assertEqual(player2.locations[1].item, player1.prog_items[1])

    def test_restrictive_progress(self):
        """Test that various spheres with different requirements can be filled"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, prog_item_count=25)
        items = player1.prog_items.copy()
        multiworld.completion_condition[player1.id] = lambda state: state.has_all(
            names(player1.prog_items), player1.id)

        player1.generate_region(player1.menu, 5)
        player1.generate_region(player1.menu, 5, lambda state: state.has_all(
            names(items[2:7]), player1.id))
        player1.generate_region(player1.menu, 5, lambda state: state.has_all(
            names(items[7:12]), player1.id))
        player1.generate_region(player1.menu, 5, lambda state: state.has_all(
            names(items[12:17]), player1.id))
        player1.generate_region(player1.menu, 5, lambda state: state.has_all(
            names(items[17:22]), player1.id))

        locations = multiworld.get_unfilled_locations()

        fill_restrictive(multiworld, multiworld.state,
                         locations, player1.prog_items)

    def test_swap_to_earlier_location_with_item_rule(self):
        """Test that item swap happens and works as intended"""
        # test for PR#1109
        multiworld = generate_test_multiworld(1)
        player1 = generate_player_data(multiworld, 1, 4, 4)
        locations = player1.locations[:]  # copy required
        items = player1.prog_items[:]  # copy required
        # for the test to work, item and location order is relevant: Sphere 1 last, allowed_item not last
        for location in locations[:-1]:  # Sphere 2
            # any one provides access to Sphere 2
            set_rule(location, lambda state: any(state.has(item.name, player1.id) for item in items))
        # forbid all but 1 item in Sphere 1
        sphere1_loc = locations[-1]
        allowed_item = items[1]
        add_item_rule(sphere1_loc, lambda item_to_place: item_to_place == allowed_item)
        # test our rules
        self.assertTrue(location.can_fill(None, allowed_item, False), "Test is flawed")
        self.assertTrue(location.can_fill(None, items[2], False), "Test is flawed")
        self.assertTrue(sphere1_loc.can_fill(None, allowed_item, False), "Test is flawed")
        self.assertFalse(sphere1_loc.can_fill(None, items[2], False), "Test is flawed")
        # fill has to place items[1] in locations[0] which will result in a swap because of placement order
        fill_restrictive(multiworld, multiworld.state, player1.locations, player1.prog_items)
        # assert swap happened
        self.assertTrue(sphere1_loc.item, "Did not swap required item into Sphere 1")
        self.assertEqual(sphere1_loc.item, allowed_item, "Wrong item in Sphere 1")

    def test_swap_to_earlier_location_with_item_rule2(self):
        """Test that swap works before all items are placed"""
        multiworld = generate_test_multiworld(1)
        player1 = generate_player_data(multiworld, 1, 5, 5)
        locations = player1.locations[:]  # copy required
        items = player1.prog_items[:]  # copy required
        # Two items provide access to sphere 2.
        # One of them is forbidden in sphere 1, the other is first placed in sphere 4 because of placement order,
        # requiring a swap.
        # There are spheres in between, so for the swap to work, it'll have to assume all other items are collected.
        one_to_two1 = items[4].name
        one_to_two2 = items[3].name
        three_to_four = items[2].name
        two_to_three1 = items[1].name
        two_to_three2 = items[0].name
        # Sphere 4
        set_rule(locations[0], lambda state: ((state.has(one_to_two1, player1.id) or state.has(one_to_two2, player1.id))
                                              and state.has(two_to_three1, player1.id)
                                              and state.has(two_to_three2, player1.id)
                                              and state.has(three_to_four, player1.id)))
        # Sphere 3
        set_rule(locations[1], lambda state: ((state.has(one_to_two1, player1.id) or state.has(one_to_two2, player1.id))
                                              and state.has(two_to_three1, player1.id)
                                              and state.has(two_to_three2, player1.id)))
        # Sphere 2
        set_rule(locations[2], lambda state: state.has(one_to_two1, player1.id) or state.has(one_to_two2, player1.id))
        # Sphere 1
        sphere1_loc1 = locations[3]
        sphere1_loc2 = locations[4]
        # forbid one_to_two2 in sphere 1 to make the swap happen as described above
        add_item_rule(sphere1_loc1, lambda item_to_place: item_to_place.name != one_to_two2)
        add_item_rule(sphere1_loc2, lambda item_to_place: item_to_place.name != one_to_two2)

        # Now fill should place one_to_two1 in sphere1_loc1 or sphere1_loc2 via swap,
        # which it will attempt before two_to_three and three_to_four are placed, testing the behavior.
        fill_restrictive(multiworld, multiworld.state, player1.locations, player1.prog_items)
        # assert swap happened
        self.assertTrue(sphere1_loc1.item and sphere1_loc2.item, "Did not swap required item into Sphere 1")
        self.assertTrue(sphere1_loc1.item.name == one_to_two1 or
                        sphere1_loc2.item.name == one_to_two1, "Wrong item in Sphere 1")

    def test_double_sweep(self):
        """Test that sweep doesn't duplicate Event items when sweeping"""
        # test for PR1114
        multiworld = generate_test_multiworld(1)
        player1 = generate_player_data(multiworld, 1, 1, 1)
        location = player1.locations[0]
        location.address = None
        item = player1.prog_items[0]
        item.code = None
        location.place_locked_item(item)
        multiworld.state.sweep_for_advancements()
        multiworld.state.sweep_for_advancements()
        self.assertTrue(multiworld.state.prog_items[item.player][item.name], "Sweep did not collect - Test flawed")
        self.assertEqual(multiworld.state.prog_items[item.player][item.name], 1, "Sweep collected multiple times")

    def test_correct_item_instance_removed_from_pool(self):
        """Test that a placed item gets removed from the submitted pool"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(multiworld, 1, 2, 2)

        player1.prog_items[0].name = "Different_item_instance_but_same_item_name"
        player1.prog_items[1].name = "Different_item_instance_but_same_item_name"
        loc0 = player1.locations[0]

        fill_restrictive(multiworld, multiworld.state,
                         [loc0], player1.prog_items)

        self.assertEqual(1, len(player1.prog_items))
        self.assertIsNot(loc0.item, player1.prog_items[0], "Filled item was still present in item pool")


class TestDistributeItemsRestrictive(unittest.TestCase):
    def test_basic_distribute(self):
        """Test that distribute_items_restrictive is deterministic"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)
        locations = player1.locations
        prog_items = player1.prog_items
        basic_items = player1.basic_items

        distribute_items_restrictive(multiworld)

        self.assertEqual(locations[0].item, basic_items[1])
        self.assertFalse(locations[0].advancement)
        self.assertEqual(locations[1].item, prog_items[0])
        self.assertTrue(locations[1].advancement)
        self.assertEqual(locations[2].item, prog_items[1])
        self.assertTrue(locations[2].advancement)
        self.assertEqual(locations[3].item, basic_items[0])
        self.assertFalse(locations[3].advancement)

    def test_excluded_distribute(self):
        """Test that distribute_items_restrictive doesn't put advancement items on excluded locations"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)
        locations = player1.locations

        locations[1].progress_type = LocationProgressType.EXCLUDED
        locations[2].progress_type = LocationProgressType.EXCLUDED

        distribute_items_restrictive(multiworld)

        self.assertFalse(locations[1].item.advancement)
        self.assertFalse(locations[2].item.advancement)

    def test_non_excluded_item_distribute(self):
        """Test that useful items aren't placed on excluded locations"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)
        locations = player1.locations
        basic_items = player1.basic_items

        locations[1].progress_type = LocationProgressType.EXCLUDED
        basic_items[1].classification = ItemClassification.useful

        distribute_items_restrictive(multiworld)

        self.assertEqual(locations[1].item, basic_items[0])

    def test_too_many_excluded_distribute(self):
        """Test that fill fails if it can't place all progression items due to too many excluded locations"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)
        locations = player1.locations

        locations[0].progress_type = LocationProgressType.EXCLUDED
        locations[1].progress_type = LocationProgressType.EXCLUDED
        locations[2].progress_type = LocationProgressType.EXCLUDED

        self.assertRaises(FillError, distribute_items_restrictive, multiworld)

    def test_non_excluded_item_must_distribute(self):
        """Test that fill fails if it can't place useful items due to too many excluded locations"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)
        locations = player1.locations
        basic_items = player1.basic_items

        locations[1].progress_type = LocationProgressType.EXCLUDED
        locations[2].progress_type = LocationProgressType.EXCLUDED
        basic_items[0].classification = ItemClassification.useful
        basic_items[1].classification = ItemClassification.useful

        self.assertRaises(FillError, distribute_items_restrictive, multiworld)

    def test_priority_distribute(self):
        """Test that priority locations receive advancement items"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)
        locations = player1.locations

        locations[0].progress_type = LocationProgressType.PRIORITY
        locations[3].progress_type = LocationProgressType.PRIORITY

        distribute_items_restrictive(multiworld)

        self.assertTrue(locations[0].item.advancement)
        self.assertTrue(locations[3].item.advancement)

    def test_excess_priority_distribute(self):
        """Test that if there's more priority locations than advancement items, they can still fill"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)
        locations = player1.locations

        locations[0].progress_type = LocationProgressType.PRIORITY
        locations[1].progress_type = LocationProgressType.PRIORITY
        locations[2].progress_type = LocationProgressType.PRIORITY

        distribute_items_restrictive(multiworld)

        self.assertFalse(locations[3].item.advancement)

    def test_multiple_world_priority_distribute(self):
        """Test that priority fill can be satisfied for multiple worlds"""
        multiworld = generate_test_multiworld(3)
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)
        player2 = generate_player_data(
            multiworld, 2, 4, prog_item_count=1, basic_item_count=3)
        player3 = generate_player_data(
            multiworld, 3, 6, prog_item_count=4, basic_item_count=2)

        player1.locations[2].progress_type = LocationProgressType.PRIORITY
        player1.locations[3].progress_type = LocationProgressType.PRIORITY

        player2.locations[1].progress_type = LocationProgressType.PRIORITY

        player3.locations[0].progress_type = LocationProgressType.PRIORITY
        player3.locations[1].progress_type = LocationProgressType.PRIORITY
        player3.locations[2].progress_type = LocationProgressType.PRIORITY
        player3.locations[3].progress_type = LocationProgressType.PRIORITY

        distribute_items_restrictive(multiworld)

        self.assertTrue(player1.locations[2].item.advancement)
        self.assertTrue(player1.locations[3].item.advancement)
        self.assertTrue(player2.locations[1].item.advancement)
        self.assertTrue(player3.locations[0].item.advancement)
        self.assertTrue(player3.locations[1].item.advancement)
        self.assertTrue(player3.locations[2].item.advancement)
        self.assertTrue(player3.locations[3].item.advancement)

    def test_can_remove_locations_in_fill_hook(self):
        """Test that distribute_items_restrictive calls the fill hook and allows for item and location removal"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, 4, prog_item_count=2, basic_item_count=2)

        removed_item: list[Item] = []
        removed_location: list[Location] = []

        def fill_hook(progitempool, usefulitempool, filleritempool, fill_locations):
            removed_item.append(filleritempool.pop(0))
            removed_location.append(fill_locations.pop(0))

        multiworld.worlds[player1.id].fill_hook = fill_hook

        distribute_items_restrictive(multiworld)

        self.assertIsNone(removed_item[0].location)
        self.assertIsNone(removed_location[0].item)

    def test_seed_robust_to_item_order(self):
        """Test deterministic fill"""
        mw1 = generate_test_multiworld()
        gen1 = generate_player_data(
            mw1, 1, 4, prog_item_count=2, basic_item_count=2)
        distribute_items_restrictive(mw1)

        mw2 = generate_test_multiworld()
        gen2 = generate_player_data(
            mw2, 1, 4, prog_item_count=2, basic_item_count=2)
        mw2.itempool.append(mw2.itempool.pop(0))
        distribute_items_restrictive(mw2)

        self.assertEqual(gen1.locations[0].item, gen2.locations[0].item)
        self.assertEqual(gen1.locations[1].item, gen2.locations[1].item)
        self.assertEqual(gen1.locations[2].item, gen2.locations[2].item)
        self.assertEqual(gen1.locations[3].item, gen2.locations[3].item)

    def test_seed_robust_to_location_order(self):
        """Test deterministic fill even if locations in a region are reordered"""
        mw1 = generate_test_multiworld()
        gen1 = generate_player_data(
            mw1, 1, 4, prog_item_count=2, basic_item_count=2)
        distribute_items_restrictive(mw1)

        mw2 = generate_test_multiworld()
        gen2 = generate_player_data(
            mw2, 1, 4, prog_item_count=2, basic_item_count=2)
        reg = mw2.get_region("Menu", gen2.id)
        reg.locations.append(reg.locations.pop(0))
        distribute_items_restrictive(mw2)

        self.assertEqual(gen1.locations[0].item, gen2.locations[0].item)
        self.assertEqual(gen1.locations[1].item, gen2.locations[1].item)
        self.assertEqual(gen1.locations[2].item, gen2.locations[2].item)
        self.assertEqual(gen1.locations[3].item, gen2.locations[3].item)

    def test_can_reserve_advancement_items_for_general_fill(self):
        """Test that priority locations fill still satisfies item rules"""
        multiworld = generate_test_multiworld()
        player1 = generate_player_data(
            multiworld, 1, location_count=5, prog_item_count=5)
        items = player1.prog_items
        multiworld.completion_condition[player1.id] = lambda state: state.has_all(
            names(items), player1.id)

        location = player1.locations[0]
        location.progress_type = LocationProgressType.PRIORITY
        location.item_rule = lambda item: item not in items[:4]

        distribute_items_restrictive(multiworld)

        self.assertEqual(location.item, items[4])

    def test_non_excluded_local_items(self):
        """Test that local items get placed locally in a multiworld"""
        multiworld = generate_test_multiworld(2)
        player1 = generate_player_data(
            multiworld, 1, location_count=5, basic_item_count=5)
        player2 = generate_player_data(
            multiworld, 2, location_count=5, basic_item_count=5)

        for item in multiworld.get_items():
            item.classification = ItemClassification.useful

        multiworld.worlds[player1.id].options.local_items.value = set(names(player1.basic_items))
        multiworld.worlds[player2.id].options.local_items.value = set(names(player2.basic_items))
        locality_rules(multiworld)

        distribute_items_restrictive(multiworld)

        for item in multiworld.get_items():
            self.assertEqual(item.player, item.location.player)
            self.assertFalse(item.location.advancement, False)

    def test_early_items(self) -> None:
        """Test that the early items API successfully places items early"""
        mw = generate_test_multiworld(2)
        player1 = generate_player_data(mw, 1, location_count=5, basic_item_count=5)
        player2 = generate_player_data(mw, 2, location_count=5, basic_item_count=5)
        mw.early_items[1][player1.basic_items[0].name] = 1
        mw.early_items[2][player2.basic_items[2].name] = 1
        mw.early_items[2][player2.basic_items[3].name] = 1

        early_items = [
            player1.basic_items[0],
            player2.basic_items[2],
            player2.basic_items[3],
        ]

        # copied this code from the beginning of `distribute_items_restrictive`
        # before `distribute_early_items` is called
        fill_locations = sorted(mw.get_unfilled_locations())
        mw.random.shuffle(fill_locations)
        itempool = sorted(mw.itempool)
        mw.random.shuffle(itempool)

        fill_locations, itempool = distribute_early_items(mw, fill_locations, itempool)

        remaining_p1 = [item for item in itempool if item.player == 1]
        remaining_p2 = [item for item in itempool if item.player == 2]

        assert len(itempool) == 7, f"number of items remaining after early_items: {len(itempool)}"
        assert len(remaining_p1) == 4, f"number of p1 items after early_items: {len(remaining_p1)}"
        assert len(remaining_p2) == 3, f"number of p2 items after early_items: {len(remaining_p1)}"
        for i in range(5):
            if i != 0:
                assert player1.basic_items[i] in itempool, "non-early item to remain in itempool"
            if i not in {2, 3}:
                assert player2.basic_items[i] in itempool, "non-early item to remain in itempool"
        for item in early_items:
            assert item not in itempool, "early item to be taken out of itempool"

        assert len(fill_locations) == len(mw.get_locations()) - len(early_items), \
            f"early location count from {mw.get_locations()} to {len(fill_locations)} " \
            f"after {len(early_items)} early items"

        items_in_locations = {loc.item for loc in mw.get_locations() if loc.item}

        assert len(items_in_locations) == len(early_items), \
            f"{len(early_items)} early items in {len(items_in_locations)} locations"

        for item in early_items:
            assert item in items_in_locations, "early item to be placed in location"


class TestBalanceMultiworldProgression(unittest.TestCase):
    def assertRegionContains(self, region: Region, item: Item) -> bool:
        for location in region.locations:
            if location.item and location.item == item:
                return True

        self.fail(f"Expected {region.name} to contain {item.name}.\n"
                  f"Contains{list(map(lambda location: location.item, region.locations))}")

    def setUp(self) -> None:
        multiworld = generate_test_multiworld(2)
        self.multiworld = multiworld
        player1 = generate_player_data(
            multiworld, 1, prog_item_count=2, basic_item_count=40)
        self.player1 = player1
        player2 = generate_player_data(
            multiworld, 2, prog_item_count=2, basic_item_count=40)
        self.player2 = player2

        multiworld.completion_condition[player1.id] = lambda state: state.has(
            player1.prog_items[0].name, player1.id) and state.has(
            player1.prog_items[1].name, player1.id)
        multiworld.completion_condition[player2.id] = lambda state: state.has(
            player2.prog_items[0].name, player2.id) and state.has(
            player2.prog_items[1].name, player2.id)

        items = player1.basic_items + player2.basic_items

        # Sphere 1
        region = player1.generate_region(player1.menu, 20)
        items = fill_region(multiworld, region, [
            player1.prog_items[0]] + items)

        # Sphere 2
        region = player1.generate_region(
            player1.regions[1], 20, lambda state: state.has(player1.prog_items[0].name, player1.id))
        items = fill_region(
            multiworld, region, [player1.prog_items[1], player2.prog_items[0]] + items)

        # Sphere 3
        region = player2.generate_region(
            player2.menu, 20, lambda state: state.has(player2.prog_items[0].name, player2.id))
        fill_region(multiworld, region, [player2.prog_items[1]] + items)

    def test_balances_progression(self) -> None:
        """Tests that progression balancing moves progression items earlier"""
        self.multiworld.worlds[self.player1.id].options.progression_balancing.value = 50
        self.multiworld.worlds[self.player2.id].options.progression_balancing.value = 50

        self.assertRegionContains(
            self.player1.regions[2], self.player2.prog_items[0])

        balance_multiworld_progression(self.multiworld)

        self.assertRegionContains(
            self.player1.regions[1], self.player2.prog_items[0])

    def test_balances_progression_light(self) -> None:
        """Test that progression balancing still moves items earlier on minimum value"""
        self.multiworld.worlds[self.player1.id].options.progression_balancing.value = 1
        self.multiworld.worlds[self.player2.id].options.progression_balancing.value = 1

        self.assertRegionContains(
            self.player1.regions[2], self.player2.prog_items[0])

        balance_multiworld_progression(self.multiworld)

        # TODO: arrange for a result that's different from the default
        self.assertRegionContains(
            self.player1.regions[1], self.player2.prog_items[0])

    def test_balances_progression_heavy(self) -> None:
        """Test that progression balancing moves items earlier on maximum value"""
        self.multiworld.worlds[self.player1.id].options.progression_balancing.value = 99
        self.multiworld.worlds[self.player2.id].options.progression_balancing.value = 99

        self.assertRegionContains(
            self.player1.regions[2], self.player2.prog_items[0])

        balance_multiworld_progression(self.multiworld)

        # TODO: arrange for a result that's different from the default
        self.assertRegionContains(
            self.player1.regions[1], self.player2.prog_items[0])

    def test_skips_balancing_progression(self) -> None:
        """Test that progression balancing is skipped when players have it disabled"""
        self.multiworld.worlds[self.player1.id].options.progression_balancing.value = 0
        self.multiworld.worlds[self.player2.id].options.progression_balancing.value = 0

        self.assertRegionContains(
            self.player1.regions[2], self.player2.prog_items[0])

        balance_multiworld_progression(self.multiworld)

        self.assertRegionContains(
            self.player1.regions[2], self.player2.prog_items[0])

    def test_ignores_priority_locations(self) -> None:
        """Test that progression items on priority locations don't get moved by balancing"""
        self.multiworld.worlds[self.player1.id].options.progression_balancing.value = 50
        self.multiworld.worlds[self.player2.id].options.progression_balancing.value = 50

        self.player2.prog_items[0].location.progress_type = LocationProgressType.PRIORITY

        balance_multiworld_progression(self.multiworld)

        self.assertRegionContains(
            self.player1.regions[2], self.player2.prog_items[0])
