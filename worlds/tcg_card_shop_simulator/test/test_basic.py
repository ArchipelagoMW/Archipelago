
from .. import options, TCGSimulatorWorld
from .bases import TCGSimulatorTestBase


class TestBasic(TCGSimulatorTestBase):
    options = {}
    world: TCGSimulatorWorld

    def test_can_beat_game(self):
        self.collect_all_but([])
        self.assertBeatable(True)

