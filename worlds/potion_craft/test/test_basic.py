from .. import PotionCraftWorld
from .bases import PotionCraftTestBase


class TestBasic(PotionCraftTestBase):
    options = {}
    world: PotionCraftWorld

    def test_can_beat_game(self):
        self.collect_all_but([])
        self.assertBeatable(True)
