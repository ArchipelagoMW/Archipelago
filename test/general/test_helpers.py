import unittest
from typing import Callable, Dict, Optional

from typing_extensions import override

from BaseClasses import CollectionState, MultiWorld, Region


class TestHelpers(unittest.TestCase):
    multiworld: MultiWorld
    player: int = 1

    @override
    def setUp(self) -> None:
        self.multiworld = MultiWorld(self.player)
        self.multiworld.game[self.player] = "helper_test_game"
        self.multiworld.player_name = {1: "Tester"}
        self.multiworld.set_seed()

    def test_region_helpers(self) -> None:
        """Tests `Region.add_locations()` and `Region.add_exits()` have correct behavior"""
        regions: Dict[str, str] = {
            "TestRegion1": "I'm an apple",
            "TestRegion2": "I'm a banana",
            "TestRegion3": "Empty Region",
        }

        locations: Dict[str, Dict[str, Optional[int]]] = {
            "TestRegion1": {
                "loc_1": 123,
                "loc_2": 456,
                "event_loc": None,
            },
            "TestRegion2": {
                "loc_3": 321,
                "loc_4": 654,
            }
        }

        reg_exits: Dict[str, Dict[str, Optional[str]]] = {
            "TestRegion1": {"TestRegion2": "connection"},
            "TestRegion2": {"TestRegion1": None},
        }

        reg_exit_set: Dict[str, set[str]] = {
            "TestRegion1": {"TestRegion3"}
        }

        exit_rules: Dict[str, Callable[[CollectionState], bool]] = {
            "TestRegion1": lambda state: state.has("test_item", self.player)
        }

        self.multiworld.regions += [Region(region, self.player, self.multiworld, regions[region]) for region in regions]

        with self.subTest("Test Location Creation Helper"):
            for region, loc_pair in locations.items():
                self.multiworld.get_region(region, self.player).add_locations(loc_pair)

            created_location_names = [loc.name for loc in self.multiworld.get_locations()]
            for loc_pair in locations.values():
                for loc_name in loc_pair:
                    self.assertTrue(loc_name in created_location_names)

        with self.subTest("Test Exit Creation Helper"):
            for region, exit_dict in reg_exits.items():
                self.multiworld.get_region(region, self.player).add_exits(exit_dict, exit_rules)

            created_exit_names = [exit.name for region in self.multiworld.get_regions() for exit in region.exits]
            for parent, exit_pair in reg_exits.items():
                for exit_reg, exit_name in exit_pair.items():
                    if exit_name:
                        self.assertTrue(exit_name in created_exit_names)
                    else:
                        self.assertTrue(f"{parent} -> {exit_reg}" in created_exit_names)
                    if exit_reg in exit_rules:
                        entrance_name = exit_name if exit_name else f"{parent} -> {exit_reg}"
                        self.assertEqual(exit_rules[exit_reg],
                                         self.multiworld.get_entrance(entrance_name, self.player).access_rule)

            for region in reg_exit_set:
                current_region = self.multiworld.get_region(region, self.player)
                current_region.add_exits(reg_exit_set[region])
                exit_names = {_exit.name for _exit in current_region.exits}
                for reg_exit in reg_exit_set[region]:
                    self.assertTrue(f"{region} -> {reg_exit}" in exit_names,
                                    f"{region} -> {reg_exit} not in {exit_names}")
