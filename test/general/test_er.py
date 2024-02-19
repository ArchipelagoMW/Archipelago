import unittest
from typing import Optional, List, Type

from BaseClasses import Region, EntranceType, MultiWorld, Entrance
from EntranceRando import disconnect_entrance_for_randomization, randomize_entrances, EntranceRandomizationError, \
    ERPlacementState
from test.general import generate_multiworld, generate_locations
from worlds.generic.Rules import set_rule


def generate_entrance_pair(region: Region, name_suffix: str, group: str):
    lx = region.create_exit(region.name + name_suffix)
    lx.er_group = group
    lx.er_type = EntranceType.TWO_WAY
    le = region.create_er_target(region.name + name_suffix)
    le.er_group = group
    le.er_type = EntranceType.TWO_WAY


def generate_disconnected_region_grid(multiworld: MultiWorld, grid_side_length: int, region_size: int = 0,
                                      region_type: Type[Region] = Region):
    """
    Generates a grid-like region structure for ER testing, where menu is connected to the top-left region, and each
    region "in vanilla" has 2 2-way exits going either down or to the right, until reaching the goal region in the
    bottom right
    """
    for row in range(grid_side_length):
        for col in range(grid_side_length):
            index = row * grid_side_length + col
            name = f"region{index}"
            region = region_type(name, 1, multiworld)
            multiworld.regions.append(region)
            generate_locations(region_size, 1, region=region)

            if row == 0 and col == 0:
                multiworld.get_region("Menu", 1).connect(region)
            if col != 0:
                generate_entrance_pair(region, "_left", "Left")
            if col != grid_side_length - 1:
                generate_entrance_pair(region, "_right", "Right")
            if row != 0:
                generate_entrance_pair(region, "_top", "Top")
            if row != grid_side_length - 1:
                generate_entrance_pair(region, "_bottom", "Bottom")


def directionally_matched_group_selection(group: str) -> List[str]:
    if group == "Left":
        return ["Right"]
    elif group == "Right":
        return ["Left"]
    elif group == "Top":
        return ["Bottom"]
    elif group == "Bottom":
        return ["Top"]
    else:
        return []


class TestDisconnectForRandomization(unittest.TestCase):
    def test_disconnect_default_2way(self):
        multiworld = generate_multiworld()
        r1 = Region("r1", 1, multiworld)
        r2 = Region("r2", 1, multiworld)
        e = r1.create_exit("e")
        e.er_type = EntranceType.TWO_WAY
        e.er_group = "Group1"
        e.connect(r2)

        disconnect_entrance_for_randomization(e)

        self.assertIsNone(e.connected_region)
        self.assertEqual([], r2.entrances)

        self.assertEqual(1, len(r1.exits))
        self.assertEqual(e, r1.exits[0])

        self.assertEqual(1, len(r1.entrances))
        self.assertIsNone(r1.entrances[0].parent_region)
        self.assertEqual("e", r1.entrances[0].name)
        self.assertEqual(EntranceType.TWO_WAY, r1.entrances[0].er_type)
        self.assertEqual("Group1", r1.entrances[0].er_group)

    def test_disconnect_default_1way(self):
        multiworld = generate_multiworld()
        r1 = Region("r1", 1, multiworld)
        r2 = Region("r2", 1, multiworld)
        e = r1.create_exit("e")
        e.er_type = EntranceType.ONE_WAY
        e.er_group = "Group1"
        e.connect(r2)

        disconnect_entrance_for_randomization(e)

        self.assertIsNone(e.connected_region)
        self.assertEqual([], r1.entrances)

        self.assertEqual(1, len(r1.exits))
        self.assertEqual(e, r1.exits[0])

        self.assertEqual(1, len(r2.entrances))
        self.assertIsNone(r2.entrances[0].parent_region)
        self.assertEqual("r2", r2.entrances[0].name)
        self.assertEqual(EntranceType.ONE_WAY, r2.entrances[0].er_type)
        self.assertEqual("Group1", r2.entrances[0].er_group)

    def test_disconnect_uses_alternate_group(self):
        multiworld = generate_multiworld()
        r1 = Region("r1", 1, multiworld)
        r2 = Region("r2", 1, multiworld)
        e = r1.create_exit("e")
        e.er_type = EntranceType.ONE_WAY
        e.er_group = "Group1"
        e.connect(r2)

        disconnect_entrance_for_randomization(e, "Group2")

        self.assertIsNone(e.connected_region)
        self.assertEqual([], r1.entrances)

        self.assertEqual(1, len(r1.exits))
        self.assertEqual(e, r1.exits[0])

        self.assertEqual(1, len(r2.entrances))
        self.assertIsNone(r2.entrances[0].parent_region)
        self.assertEqual("r2", r2.entrances[0].name)
        self.assertEqual(EntranceType.ONE_WAY, r2.entrances[0].er_type)
        self.assertEqual("Group2", r2.entrances[0].er_group)


class TestRandomizeEntrances(unittest.TestCase):
    def test_determinism(self):
        self.fail()

    def test_all_entrances_placed(self):
        """tests that all entrances and exits were placed, all regions are connected, and no dangling edges exist"""
        multiworld = generate_multiworld()
        multiworld.worlds[1].random = multiworld.per_slot_randoms[1]
        generate_disconnected_region_grid(multiworld, 5)

        result = randomize_entrances(multiworld.worlds[1], False, directionally_matched_group_selection)

        self.assertEqual([], [entrance for region in multiworld.get_regions()
                              for entrance in region.entrances if not entrance.parent_region])
        self.assertEqual([], [exit_ for region in multiworld.get_regions()
                              for exit_ in region.exits if not exit_.connected_region])
        # 5x5 grid + menu
        self.assertEqual(26, len(result.placed_regions))
        self.assertEqual(80, len(result.pairings))
        self.assertEqual(80, len(result.placements))

    def test_coupling(self):
        """tests that in coupled mode, all 2 way transitions have an inverse"""
        self.fail()

    def test_oneway_twoway_pairing(self):
        """tests that 1 ways are only paired to 1 ways and 2 ways are only paired to 2 ways"""
        self.fail()

    def test_group_constraints_satisfied(self):
        """tests that all grouping constraints are satisfied"""
        self.fail()

    def test_minimal_entrance_rando(self):
        """tests that entrance randomization can complete with minimal accessibility and unreachable exits"""
        self.fail()

    def test_fails_when_mismatched_entrance_and_exit_count(self):
        """tests that entrance randomization fast-fails if the input exit and entrance count do not match"""
        multiworld = generate_multiworld()
        multiworld.worlds[1].random = multiworld.per_slot_randoms[1]
        generate_disconnected_region_grid(multiworld, 5)
        multiworld.get_region("region1", 1).create_exit("extra")

        self.assertRaises(EntranceRandomizationError, randomize_entrances, multiworld.worlds[1], False,
                          directionally_matched_group_selection)

    def test_fails_when_some_unreachable_exit(self):
        """tests that entrance randomization fails if an exit is never reachable (non-minimal accessibility)"""
        multiworld = generate_multiworld()
        multiworld.worlds[1].random = multiworld.per_slot_randoms[1]
        generate_disconnected_region_grid(multiworld, 5)
        e = multiworld.get_entrance("region1_right", 1)
        set_rule(e, lambda state: False)

        self.assertRaises(EntranceRandomizationError, randomize_entrances, multiworld.worlds[1], False,
                          directionally_matched_group_selection)

    def test_fails_when_some_unconnectable_exit(self):
        class CustomEntrance(Entrance):
            def can_connect_to(self, other: Entrance, state: "ERPlacementState") -> bool:
                if other.name == "region1_right":
                    return False

        class CustomRegion(Region):
            entrance_type = CustomEntrance

        multiworld = generate_multiworld()
        multiworld.worlds[1].random = multiworld.per_slot_randoms[1]
        generate_disconnected_region_grid(multiworld, 5, region_type=CustomRegion)

        self.assertRaises(EntranceRandomizationError, randomize_entrances, multiworld.worlds[1], False,
                          directionally_matched_group_selection)