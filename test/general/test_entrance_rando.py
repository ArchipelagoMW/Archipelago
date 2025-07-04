from typing import Callable
import unittest
from enum import IntEnum

from BaseClasses import Region, EntranceType, MultiWorld, Entrance
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances, EntranceRandomizationError, \
    ERPlacementState, EntranceLookup, bake_target_group_lookup
from Options import Accessibility
from test.general import generate_test_multiworld, generate_locations, generate_items
from worlds.generic.Rules import set_rule


class ERTestGroups(IntEnum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4


directionally_matched_group_lookup = {
    ERTestGroups.LEFT: [ERTestGroups.RIGHT],
    ERTestGroups.RIGHT: [ERTestGroups.LEFT],
    ERTestGroups.TOP: [ERTestGroups.BOTTOM],
    ERTestGroups.BOTTOM: [ERTestGroups.TOP]
}


def generate_entrance_pair(region: Region, name_suffix: str, group: int):
    lx = region.create_exit(region.name + name_suffix)
    lx.randomization_group = group
    lx.randomization_type = EntranceType.TWO_WAY
    le = region.create_er_target(region.name + name_suffix)
    le.randomization_group = group
    le.randomization_type = EntranceType.TWO_WAY


def generate_disconnected_region_grid(multiworld: MultiWorld, grid_side_length: int, region_size: int = 0,
                                      region_creator: Callable[[str, int, MultiWorld], Region] = Region):
    """
    Generates a grid-like region structure for ER testing, where menu is connected to the top-left region, and each
    region "in vanilla" has 2 2-way exits going either down or to the right, until reaching the goal region in the
    bottom right
    """
    for row in range(grid_side_length):
        for col in range(grid_side_length):
            index = row * grid_side_length + col
            name = f"region{index}"
            region = region_creator(name, 1, multiworld)
            multiworld.regions.append(region)
            generate_locations(region_size, 1, region=region, tag=f"_{name}")

            if row == 0 and col == 0:
                multiworld.get_region("Menu", 1).connect(region)
            if col != 0:
                generate_entrance_pair(region, "_left", ERTestGroups.LEFT)
            if col != grid_side_length - 1:
                generate_entrance_pair(region, "_right", ERTestGroups.RIGHT)
            if row != 0:
                generate_entrance_pair(region, "_top", ERTestGroups.TOP)
            if row != grid_side_length - 1:
                generate_entrance_pair(region, "_bottom", ERTestGroups.BOTTOM)


class TestEntranceLookup(unittest.TestCase):
    def test_shuffled_targets(self):
        """tests that get_targets shuffles targets between groups when requested"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        exits_set = set([ex for region in multiworld.get_regions(1)
                        for ex in region.exits if not ex.connected_region])

        lookup = EntranceLookup(multiworld.worlds[1].random, coupled=True, usable_exits=exits_set)
        er_targets = [entrance for region in multiworld.get_regions(1)
                      for entrance in region.entrances if not entrance.parent_region]
        for entrance in er_targets:
            lookup.add(entrance)

        retrieved_targets = lookup.get_targets([ERTestGroups.TOP, ERTestGroups.BOTTOM],
                                               False, False)
        prev = None
        group_order = [prev := group.randomization_group for group in retrieved_targets
                       if prev != group.randomization_group]
        # technically possible that group order may not be shuffled, by some small chance, on some seeds. but generally
        # a shuffled list should alternate more frequently which is the desired behavior here
        self.assertGreater(len(group_order), 2)


    def test_ordered_targets(self):
        """tests that get_targets does not shuffle targets between groups when requested"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        exits_set = set([ex for region in multiworld.get_regions(1)
                        for ex in region.exits if not ex.connected_region])

        lookup = EntranceLookup(multiworld.worlds[1].random, coupled=True, usable_exits=exits_set)
        er_targets = [entrance for region in multiworld.get_regions(1)
                      for entrance in region.entrances if not entrance.parent_region]
        for entrance in er_targets:
            lookup.add(entrance)

        retrieved_targets = lookup.get_targets([ERTestGroups.TOP, ERTestGroups.BOTTOM],
                                               False, True)
        prev = None
        group_order = [prev := group.randomization_group for group in retrieved_targets if prev != group.randomization_group]
        self.assertEqual([ERTestGroups.TOP, ERTestGroups.BOTTOM], group_order)

    def test_selective_dead_ends(self):
        """test that entrances that EntranceLookup has not been told to consider are ignored when finding dead-ends"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        exits_set = set([ex for region in multiworld.get_regions(1)
                        for ex in region.exits if not ex.connected_region
                         and ex.name != "region20_right" and ex.name != "region21_left"])

        lookup = EntranceLookup(multiworld.worlds[1].random, coupled=True, usable_exits=exits_set)
        er_targets = [entrance for region in multiworld.get_regions(1)
                      for entrance in region.entrances if not entrance.parent_region and
                      entrance.name != "region20_right" and entrance.name != "region21_left"]
        for entrance in er_targets:
            lookup.add(entrance)
        # region 20 is the bottom left corner of the grid, and therefore only has a right entrance from region 21
        # and a top entrance from region 15; since we've told lookup to ignore the right entrance from region 21,
        # the top entrance from region 15 should be considered a dead-end
        dead_end_region = multiworld.get_region("region20", 1)
        for dead_end in dead_end_region.entrances:
            if dead_end.name == "region20_top":
                break
        # there should be only this one dead-end
        self.assertTrue(dead_end in lookup.dead_ends)
        self.assertEqual(len(lookup.dead_ends), 1)

class TestBakeTargetGroupLookup(unittest.TestCase):
    def test_lookup_generation(self):
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        world = multiworld.worlds[1]
        expected = {
            ERTestGroups.LEFT: [-ERTestGroups.LEFT],
            ERTestGroups.RIGHT: [-ERTestGroups.RIGHT],
            ERTestGroups.TOP: [-ERTestGroups.TOP],
            ERTestGroups.BOTTOM: [-ERTestGroups.BOTTOM]
        }
        actual = bake_target_group_lookup(world, lambda g: [-g])
        self.assertEqual(expected, actual)


class TestDisconnectForRandomization(unittest.TestCase):
    def test_disconnect_default_2way(self):
        multiworld = generate_test_multiworld()
        r1 = Region("r1", 1, multiworld)
        r2 = Region("r2", 1, multiworld)
        e = r1.create_exit("e")
        e.randomization_type = EntranceType.TWO_WAY
        e.randomization_group = 1
        e.connect(r2)

        disconnect_entrance_for_randomization(e)

        self.assertIsNone(e.connected_region)
        self.assertEqual([], r2.entrances)

        self.assertEqual(1, len(r1.exits))
        self.assertEqual(e, r1.exits[0])

        self.assertEqual(1, len(r1.entrances))
        self.assertIsNone(r1.entrances[0].parent_region)
        self.assertEqual("e", r1.entrances[0].name)
        self.assertEqual(EntranceType.TWO_WAY, r1.entrances[0].randomization_type)
        self.assertEqual(1, r1.entrances[0].randomization_group)

    def test_disconnect_default_1way(self):
        multiworld = generate_test_multiworld()
        r1 = Region("r1", 1, multiworld)
        r2 = Region("r2", 1, multiworld)
        e = r1.create_exit("e")
        e.randomization_type = EntranceType.ONE_WAY
        e.randomization_group = 1
        e.connect(r2)

        disconnect_entrance_for_randomization(e, one_way_target_name="foo")

        self.assertIsNone(e.connected_region)
        self.assertEqual([], r1.entrances)

        self.assertEqual(1, len(r1.exits))
        self.assertEqual(e, r1.exits[0])

        self.assertEqual(1, len(r2.entrances))
        self.assertIsNone(r2.entrances[0].parent_region)
        self.assertEqual("foo", r2.entrances[0].name)
        self.assertEqual(EntranceType.ONE_WAY, r2.entrances[0].randomization_type)
        self.assertEqual(1, r2.entrances[0].randomization_group)

    def test_disconnect_default_1way_no_vanilla_target_raises(self):
        multiworld = generate_test_multiworld()
        r1 = Region("r1", 1, multiworld)
        r2 = Region("r2", 1, multiworld)
        e = r1.create_exit("e")
        e.randomization_type = EntranceType.ONE_WAY
        e.randomization_group = 1
        e.connect(r2)

        with self.assertRaises(ValueError):
            disconnect_entrance_for_randomization(e)

    def test_disconnect_uses_alternate_group(self):
        multiworld = generate_test_multiworld()
        r1 = Region("r1", 1, multiworld)
        r2 = Region("r2", 1, multiworld)
        e = r1.create_exit("e")
        e.randomization_type = EntranceType.ONE_WAY
        e.randomization_group = 1
        e.connect(r2)

        disconnect_entrance_for_randomization(e, 2, "foo")

        self.assertIsNone(e.connected_region)
        self.assertEqual([], r1.entrances)

        self.assertEqual(1, len(r1.exits))
        self.assertEqual(e, r1.exits[0])

        self.assertEqual(1, len(r2.entrances))
        self.assertIsNone(r2.entrances[0].parent_region)
        self.assertEqual("foo", r2.entrances[0].name)
        self.assertEqual(EntranceType.ONE_WAY, r2.entrances[0].randomization_type)
        self.assertEqual(2, r2.entrances[0].randomization_group)


class TestRandomizeEntrances(unittest.TestCase):
    def test_determinism(self):
        """tests that the same output is produced for the same input"""
        multiworld1 = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld1, 5)
        multiworld2 = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld2, 5)

        result1 = randomize_entrances(multiworld1.worlds[1], False, directionally_matched_group_lookup)
        result2 = randomize_entrances(multiworld2.worlds[1], False, directionally_matched_group_lookup)
        self.assertEqual(result1.pairings, result2.pairings)
        for e1, e2 in zip(result1.placements, result2.placements):
            self.assertEqual(e1.name, e2.name)
            self.assertEqual(e1.parent_region.name, e1.parent_region.name)
            self.assertEqual(e1.connected_region.name, e2.connected_region.name)

    def test_all_entrances_placed(self):
        """tests that all entrances and exits were placed, all regions are connected, and no dangling edges exist"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)

        result = randomize_entrances(multiworld.worlds[1], False, directionally_matched_group_lookup)

        self.assertEqual([], [entrance for region in multiworld.get_regions()
                              for entrance in region.entrances if not entrance.parent_region])
        self.assertEqual([], [exit_ for region in multiworld.get_regions()
                              for exit_ in region.exits if not exit_.connected_region])
        # 5x5 grid + menu
        self.assertEqual(26, len(result.placed_regions))
        self.assertEqual(80, len(result.pairings))
        self.assertEqual(80, len(result.placements))

    def test_coupled(self):
        """tests that in coupled mode, all 2 way transitions have an inverse"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        seen_placement_count = 0

        def verify_coupled(_: ERPlacementState, placed_entrances: list[Entrance]):
            nonlocal seen_placement_count
            seen_placement_count += len(placed_entrances)
            self.assertEqual(2, len(placed_entrances))
            self.assertEqual(placed_entrances[0].parent_region, placed_entrances[1].connected_region)
            self.assertEqual(placed_entrances[1].parent_region, placed_entrances[0].connected_region)

        result = randomize_entrances(multiworld.worlds[1], True, directionally_matched_group_lookup,
                                     on_connect=verify_coupled)
        # if we didn't visit every placement the verification on_connect doesn't really mean much
        self.assertEqual(len(result.placements), seen_placement_count)

    def test_uncoupled_succeeds_stage1_indirect_condition(self):
        multiworld = generate_test_multiworld()
        menu = multiworld.get_region("Menu", 1)
        generate_entrance_pair(menu, "_right", ERTestGroups.RIGHT)
        end = Region("End", 1, multiworld)
        multiworld.regions.append(end)
        generate_entrance_pair(end, "_left", ERTestGroups.LEFT)
        multiworld.register_indirect_condition(end, None)

        result = randomize_entrances(multiworld.worlds[1], False, directionally_matched_group_lookup)
        self.assertSetEqual({
            ("Menu_right", "End_left"),
            ("End_left", "Menu_right")
        }, set(result.pairings))

    def test_coupled_succeeds_stage1_indirect_condition(self):
        multiworld = generate_test_multiworld()
        menu = multiworld.get_region("Menu", 1)
        generate_entrance_pair(menu, "_right", ERTestGroups.RIGHT)
        end = Region("End", 1, multiworld)
        multiworld.regions.append(end)
        generate_entrance_pair(end, "_left", ERTestGroups.LEFT)
        multiworld.register_indirect_condition(end, None)

        result = randomize_entrances(multiworld.worlds[1], True, directionally_matched_group_lookup)
        self.assertSetEqual({
            ("Menu_right", "End_left"),
            ("End_left", "Menu_right")
        }, set(result.pairings))

    def test_uncoupled(self):
        """tests that in uncoupled mode, no transitions have an (intentional) inverse"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        seen_placement_count = 0

        def verify_uncoupled(state: ERPlacementState, placed_entrances: list[Entrance]):
            nonlocal seen_placement_count
            seen_placement_count += len(placed_entrances)
            self.assertEqual(1, len(placed_entrances))

        result = randomize_entrances(multiworld.worlds[1], False, directionally_matched_group_lookup,
                                     on_connect=verify_uncoupled)
        # if we didn't visit every placement the verification on_connect doesn't really mean much
        self.assertEqual(len(result.placements), seen_placement_count)

    def test_oneway_twoway_pairing(self):
        """tests that 1 ways are only paired to 1 ways and 2 ways are only paired to 2 ways"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        region26 = Region("region26", 1, multiworld)
        multiworld.regions.append(region26)
        for index, region in enumerate(["region4", "region20", "region24"]):
            x = multiworld.get_region(region, 1).create_exit(f"{region}_bottom_1way")
            x.randomization_type = EntranceType.ONE_WAY
            x.randomization_group = ERTestGroups.BOTTOM
            e = region26.create_er_target(f"region26_top_1way{index}")
            e.randomization_type = EntranceType.ONE_WAY
            e.randomization_group = ERTestGroups.TOP

        result = randomize_entrances(multiworld.worlds[1], False, directionally_matched_group_lookup)
        for exit_name, entrance_name in result.pairings:
            # we have labeled our entrances in such a way that all the 1 way entrances have 1way in the name,
            # so test for that since the ER target will have been discarded
            if "1way" in exit_name:
                self.assertIn("1way", entrance_name)

    def test_group_constraints_satisfied(self):
        """tests that all grouping constraints are satisfied"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)

        result = randomize_entrances(multiworld.worlds[1], False, directionally_matched_group_lookup)
        for exit_name, entrance_name in result.pairings:
            # we have labeled our entrances in such a way that all the entrances contain their group in the name
            # so test for that since the ER target will have been discarded
            if "top" in exit_name:
                self.assertIn("bottom", entrance_name)
            if "bottom" in exit_name:
                self.assertIn("top", entrance_name)
            if "left" in exit_name:
                self.assertIn("right", entrance_name)
            if "right" in exit_name:
                self.assertIn("left", entrance_name)

    def test_minimal_entrance_rando(self):
        """tests that entrance randomization can complete with minimal accessibility and unreachable exits"""
        multiworld = generate_test_multiworld()
        multiworld.worlds[1].options.accessibility = Accessibility.from_any(Accessibility.option_minimal)
        multiworld.completion_condition[1] = lambda state: state.can_reach("region24", player=1)
        generate_disconnected_region_grid(multiworld, 5, 1)
        prog_items = generate_items(10, 1, True)
        multiworld.itempool += prog_items
        filler_items = generate_items(15, 1, False)
        multiworld.itempool += filler_items
        e = multiworld.get_entrance("region1_right", 1)
        set_rule(e, lambda state: False)

        randomize_entrances(multiworld.worlds[1], False, directionally_matched_group_lookup)

        self.assertEqual([], [entrance for region in multiworld.get_regions()
                              for entrance in region.entrances if not entrance.parent_region])
        self.assertEqual([], [exit_ for region in multiworld.get_regions()
                              for exit_ in region.exits if not exit_.connected_region])

    def test_minimal_entrance_rando_with_collect_override(self):
        """
        tests that entrance randomization can complete with minimal accessibility and unreachable exits
        when the world defines a collect override that add extra values to prog_items
        """
        multiworld = generate_test_multiworld()
        multiworld.worlds[1].options.accessibility = Accessibility.from_any(Accessibility.option_minimal)
        multiworld.completion_condition[1] = lambda state: state.can_reach("region24", player=1)
        generate_disconnected_region_grid(multiworld, 5, 1)
        prog_items = generate_items(10, 1, True)
        multiworld.itempool += prog_items
        filler_items = generate_items(15, 1, False)
        multiworld.itempool += filler_items
        e = multiworld.get_entrance("region1_right", 1)
        set_rule(e, lambda state: False)

        old_collect = multiworld.worlds[1].collect

        def new_collect(state, item):
            old_collect(state, item)
            state.prog_items[item.player]["counter"] += 300

        multiworld.worlds[1].collect = new_collect

        randomize_entrances(multiworld.worlds[1], False, directionally_matched_group_lookup)

        self.assertEqual([], [entrance for region in multiworld.get_regions()
                              for entrance in region.entrances if not entrance.parent_region])
        self.assertEqual([], [exit_ for region in multiworld.get_regions()
                              for exit_ in region.exits if not exit_.connected_region])

    def test_restrictive_region_requirement_does_not_fail(self):
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 2, 1)

        region = Region("region4", 1, multiworld)
        multiworld.regions.append(region)
        generate_entrance_pair(multiworld.get_region("region0", 1), "_right2", ERTestGroups.RIGHT)
        generate_entrance_pair(region, "_left", ERTestGroups.LEFT)

        blocked_exits = ["region1_left", "region1_bottom",
                         "region2_top", "region2_right",
                         "region3_left", "region3_top"]
        for exit_name in blocked_exits:
            blocked_exit = multiworld.get_entrance(exit_name, 1)
            blocked_exit.access_rule = lambda state: state.can_reach_region("region4", 1)
            multiworld.register_indirect_condition(region, blocked_exit)

        result = randomize_entrances(multiworld.worlds[1], True, directionally_matched_group_lookup)
        # verifying that we did in fact place region3 adjacent to region0 to unblock all the other connections
        # (and implicitly, that ER didn't fail)
        self.assertTrue(("region0_right", "region4_left") in result.pairings
                        or ("region0_right2", "region4_left") in result.pairings)

    def test_fails_when_mismatched_entrance_and_exit_count(self):
        """tests that entrance randomization fast-fails if the input exit and entrance count do not match"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        multiworld.get_region("region1", 1).create_exit("extra")

        self.assertRaises(EntranceRandomizationError, randomize_entrances, multiworld.worlds[1], False,
                          directionally_matched_group_lookup)

    def test_fails_when_some_unreachable_exit(self):
        """tests that entrance randomization fails if an exit is never reachable (non-minimal accessibility)"""
        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5)
        e = multiworld.get_entrance("region1_right", 1)
        set_rule(e, lambda state: False)

        self.assertRaises(EntranceRandomizationError, randomize_entrances, multiworld.worlds[1], False,
                          directionally_matched_group_lookup)

    def test_fails_when_some_unconnectable_exit(self):
        """tests that entrance randomization fails if an exit can't be made into a valid placement (non-minimal)"""
        class CustomEntrance(Entrance):
            def can_connect_to(self, other: Entrance, dead_end: bool, er_state: "ERPlacementState") -> bool:
                if other.name == "region1_right":
                    return False

        class CustomRegion(Region):
            entrance_type = CustomEntrance

        multiworld = generate_test_multiworld()
        generate_disconnected_region_grid(multiworld, 5, region_creator=CustomRegion)

        self.assertRaises(EntranceRandomizationError, randomize_entrances, multiworld.worlds[1], False,
                          directionally_matched_group_lookup)

    def test_minimal_er_fails_when_not_enough_locations_to_fit_progression(self):
        """
        tests that entrance randomization fails in minimal accessibility if there are not enough locations
        available to place all progression items locally
        """
        multiworld = generate_test_multiworld()
        multiworld.worlds[1].options.accessibility = Accessibility.from_any(Accessibility.option_minimal)
        multiworld.completion_condition[1] = lambda state: state.can_reach("region24", player=1)
        generate_disconnected_region_grid(multiworld, 5, 1)
        prog_items = generate_items(30, 1, True)
        multiworld.itempool += prog_items
        e = multiworld.get_entrance("region1_right", 1)
        set_rule(e, lambda state: False)

        self.assertRaises(EntranceRandomizationError, randomize_entrances, multiworld.worlds[1], False,
                          directionally_matched_group_lookup)
