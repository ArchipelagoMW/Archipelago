from test.bases import WorldTestBase
from typing import Iterable
from .. import SoEWorld


class SoETestBase(WorldTestBase):
    game = "Secret of Evermore"
    world: SoEWorld

    def assertLocationReachability(self, reachable: Iterable[str] = (), unreachable: Iterable[str] = (),
                                   satisfied: bool = True) -> None:
        """
        Tests that unreachable can't be reached. Tests that reachable can be reached if satisfied=True.
        Usage: test with satisfied=False, collect requirements into state, test again with satisfied=True
        """
        for location in reachable:
            self.assertEqual(self.can_reach_location(location), satisfied,
                             f"{location} is unreachable but should be" if satisfied else
                             f"{location} is reachable but shouldn't be")
        for location in unreachable:
            self.assertFalse(self.can_reach_location(location),
                             f"{location} is reachable but shouldn't be")

    def testRocketPartsExist(self) -> None:
        """Tests that rocket parts exist and are unique"""
        self.assertEqual(len(self.get_items_by_name("Gauge")), 1)
        self.assertEqual(len(self.get_items_by_name("Wheel")), 1)
        diamond_eyes = self.get_items_by_name("Diamond Eye")
        self.assertEqual(len(diamond_eyes), 3)
        # verify diamond eyes are individual items
        self.assertFalse(diamond_eyes[0] is diamond_eyes[1])
        self.assertFalse(diamond_eyes[0] is diamond_eyes[2])
        self.assertFalse(diamond_eyes[1] is diamond_eyes[2])
