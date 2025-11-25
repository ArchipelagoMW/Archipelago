import unittest

from . import MessengerTestBase


class StrictEntranceRandoTest(MessengerTestBase):
    """Bare-bones world that tests the strictest possible settings to ensure it doesn't crash"""
    auto_construct = True
    options = {
        "limited_movement": 1,
        "available_portals": 3,
        "shuffle_portals": 1,
        "shuffle_transitions": 1,
    }

    @unittest.skip
    def test_all_state_can_reach_everything(self) -> None:
        """It's not possible to reach everything with these options so skip this test."""
        pass
