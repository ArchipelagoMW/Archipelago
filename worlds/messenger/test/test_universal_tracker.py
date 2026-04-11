import unittest
from typing import cast, Any

from test.general import setup_multiworld, gen_steps
from . import MessengerTestBase
from .. import MessengerWorld
from ...AutoWorld import call_all


class UniversalTrackerTestBase(MessengerTestBase):
    """
    Will generate a solo seed to build a real slot data. Then, will generate a
    second solo seed using said slot data for the `re_gen_passthrough` used by
    universal tracker.
    """
    run_default_tests = False

    slot_data: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        if cls is UniversalTrackerTestBase:
            raise unittest.SkipTest("No running tests on UniversalTrackerTestBase import.")
        super().setUpClass()

    def setUp(self) -> None:
        super().setUp()
        if not hasattr(self, "world"):
            return

        self.slot_data = self.world.fill_slot_data()

        self.multiworld = setup_multiworld(MessengerWorld, steps=(), options=self.options)
        self.world = cast(MessengerWorld, self.multiworld.worlds[self.player])

        setattr(self.multiworld, "re_gen_passthrough", {MessengerWorld.game: self.slot_data})

        for step in gen_steps:
            call_all(self.multiworld, step)


class DefaultUniversalTrackerTest(UniversalTrackerTestBase):

    def test_can_recreate_world(self) -> None:
        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)


class ShufflePortalsShopsUniversalTrackerTest(UniversalTrackerTestBase):
    options = {
        "shuffle_portals": "shops",
    }

    def test_can_recreate_world(self) -> None:
        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)
        self.assertListEqual(self.slot_data["portal_exits"], self.world.portal_mapping)


class ShufflePortalsCheckpointsUniversalTrackerTest(UniversalTrackerTestBase):
    options = {
        "shuffle_portals": "checkpoints",
    }

    def test_can_recreate_world(self) -> None:
        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)
        self.assertListEqual(self.slot_data["portal_exits"], self.world.portal_mapping)


class ShufflePortalsAnywhereUniversalTrackerTest(UniversalTrackerTestBase):
    options = {
        "shuffle_portals": "anywhere",
    }

    def test_can_recreate_world(self) -> None:
        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)
        self.assertListEqual(self.slot_data["portal_exits"], self.world.portal_mapping)


class ShuffleTransitionsCoupledUniversalTrackerTest(UniversalTrackerTestBase):
    options = {
        "shuffle_transitions": "coupled",
    }

    def test_can_recreate_world(self) -> None:
        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)
        # Should be empty ,
        self.assertListEqual([], self.world.transitions)


class ShuffleTransitionsDecoupledUniversalTrackerTest(UniversalTrackerTestBase):
    options = {
        "shuffle_transitions": "decoupled",
    }

    def test_can_recreate_world(self) -> None:
        re_gen_slot_data = self.world.fill_slot_data()

        self.assertListEqual(self.slot_data["starting_portals"], self.world.starting_portals)
        self.assertListEqual(self.slot_data["transitions"], re_gen_slot_data["transitions"])
