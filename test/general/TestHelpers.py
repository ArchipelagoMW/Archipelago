from random import seed
from typing import Dict, Optional, Callable, Tuple, List

from BaseClasses import MultiWorld, CollectionState
import unittest


class TestHelpers(unittest.TestCase):
    multiworld: MultiWorld
    player: int = 1

    def setUp(self) -> None:
        self.multiworld = MultiWorld(self.player)
        self.multiworld.game[self.player] = "helper_test_game"
        self.multiworld.player_name = {1: "Tester"}
        self.multiworld.set_seed(seed)
        self.multiworld.set_default_common_options()

    def testRegionHelpers(self) -> None:
        regions: Dict[str, str] = {
            "TestRegion1": "I'm an apple",
            "TestRegion2": "I'm a banana",
        }

        locations: Dict[str, Dict[str, Optional[int]]] = {
            "TestRegion1": {
                "loc_1": 123,
                "loc_2": 456,
                "event_loc": None,
            },
            "TestRegion2": {
                "loc_1": 321,
                "loc_2": 654,
            }
        }

        reg_exits: Dict[str, Dict[str, List[str, Callable[[CollectionState], bool]]]] = {
            "TestRegion1": {
                "TestRegion2": ["Region 1 -> Region 2"],
            },
            "TestRegion2": {
                "TestRegion1": ["Region 2 -> Region 1", lambda state: state.has("testItem", self.player)]
            }
        }

        with self.subTest("Test Region Creation Helper"):
            for region, hint in regions.items():
                self.multiworld.regions.append(self.multiworld.create_region(region, self.player, hint))

            created_region_names = [region.name for region in self.multiworld.get_regions()]
            for region_name in regions:
                self.assertTrue(region_name in created_region_names)

        with self.subTest("Test Location Creation Helper"):
            for region, loc_pair in locations.items():
                self.multiworld.get_region(region, self.player).add_locations(loc_pair)

            created_location_names = [loc.name for loc in self.multiworld.get_locations()]
            for loc_pair in locations.values():
                for loc_name in loc_pair:
                    self.assertTrue(loc_name in created_location_names)

        with self.subTest("Test Exit Creation Helper"):
            for region, exit_region in reg_exits.items():
                self.multiworld.get_region(region, self.player).add_exits(exit_region)

            created_exit_names = [exit.name for region in self.multiworld.get_regions() for exit in region.exits]
            for exit_pair in reg_exits.values():
                for exit_list in exit_pair.values():
                    self.assertTrue(exit_list[0] in created_exit_names)
                    if len(exit_list) > 1:
                        self.assertEqual(exit_list[1], self.multiworld.get_entrance(exit_list[0], self.player).access_rule)
