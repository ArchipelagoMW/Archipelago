from . import BombRushCyberfunkTestBase
from typing import List


rep_item_names: List[str] = [
    "8 REP",
    "16 REP",
    "24 REP",
    "32 REP",
    "48 REP"
]


class TestCollectAndRemoveREP(BombRushCyberfunkTestBase):
    @property
    def run_default_tests(self) -> bool:
        return False
    
    def test_default_rep_total(self) -> None:
        self.collect_by_name(rep_item_names)
        self.assertEqual(1400, self.multiworld.state.prog_items[self.player]["rep"])

        new_total = 1400

        if self.count("8 REP") > 0:
            new_total -= 8
            self.remove(self.get_item_by_name("8 REP"))

        if self.count("16 REP") > 0:
            new_total -= 16
            self.remove(self.get_item_by_name("16 REP"))

        if self.count("24 REP") > 0:
            new_total -= 24
            self.remove(self.get_item_by_name("24 REP"))

        if self.count("32 REP") > 0:
            new_total -= 32
            self.remove(self.get_item_by_name("32 REP"))

        if self.count("48 REP") > 0:
            new_total -= 48
            self.remove(self.get_item_by_name("48 REP"))

        self.assertEqual(new_total, self.multiworld.state.prog_items[self.player]["rep"])