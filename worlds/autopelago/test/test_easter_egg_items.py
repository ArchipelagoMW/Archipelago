from typing import TypeVar

from test.bases import WorldTestBase
from test.general import setup_multiworld

from worlds.autopelago import AutopelagoWorld
from worlds.yachtdice import YachtDiceWorld

T = TypeVar("T")


class EasterEggItemTestWhenYachtDiceAbsent(WorldTestBase):
    game = "Autopelago"
    run_default_tests = False

    def test_without_yacht_dice(self) -> None:
        self.assertNotIn("Two Yachts", (item.name for item in self.multiworld.get_items()))


class EasterEggItemTestWhenYachtDicePresent(WorldTestBase):
    auto_construct = False
    run_default_tests = False

    def setUp(self):
        self.multiworld = setup_multiworld([AutopelagoWorld, YachtDiceWorld])
        super().setUp()

    def test_with_yacht_dice(self) -> None:
        self.assertIn("Two Yachts", (item.name for item in self.multiworld.get_items()))
