import unittest
from typing import ClassVar

from test.param import classvar_matrix
from . import MessengerTestBase
from ..connections import RANDOMIZED_CONNECTIONS, TRANSITIONS, ONE_WAY_EXITS, ONE_WAY_ENTRANCES


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


@classvar_matrix(entrance=ONE_WAY_EXITS, exit=ONE_WAY_ENTRANCES)
class OneWayTransitionPlandoTest(MessengerTestBase):
    entrance: ClassVar[str]
    exit: ClassVar[str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = {
            "shuffle_transitions": "coupled",
            "plando_connections": [
                {"entrance": self.entrance, "exit": self.exit, }
            ],
        }

    @property
    def run_default_tests(self) -> bool:
        return False

    def test_validate_plando(self) -> None:
        entrance = self.world.get_entrance(self.entrance)
        self.assertIsNotNone(entrance.connected_region)
        self.assertEqual(self.exit, entrance.connected_region.name)


class ConnectionsConstantTest(MessengerTestBase):

    @property
    def run_default_tests(self) -> bool:
        return False

    def test_all_transitions_exist(self) -> None:
        for transition in sorted(RANDOMIZED_CONNECTIONS.keys()):
            with self.subTest(transition=transition):
                self.assertIn(transition.replace(" exit", ""), TRANSITIONS)
                entrance = self.world.get_entrance(transition)
                self.assertIsNotNone(entrance)

        for transition in sorted(RANDOMIZED_CONNECTIONS.values()):
            with self.subTest(transition=transition):
                self.assertIn(transition, TRANSITIONS)

                if transition not in ONE_WAY_ENTRANCES:
                    entrance = self.world.get_entrance(transition + " exit")
                    self.assertIsNotNone(entrance)
