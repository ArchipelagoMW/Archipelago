from test.TestBase import WorldTestBase
from typing import Iterable


class SoETestBase(WorldTestBase):
    game = "Secret of Evermore"

    def assertLocationReachability(self, reachable: Iterable[str] = (), unreachable: Iterable[str] = (),
                                   satisfied=True) -> None:
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
