
from .. import options, TCGSimulatorWorld, get_level_region
from .bases import TCGSimulatorTestBase


class TestBasic(TCGSimulatorTestBase):
    options = {}
    world: TCGSimulatorWorld

    def test_can_beat_game(self):
        self.collect_all_but([])
        self.assertBeatable(True)

class TestGeneration(TCGSimulatorTestBase):
    options = {
        "max_level": 10,
        "product_licenses": 12,
        "goal": 1,
        "bulk_box": 1,
    }

    def test_can_beat_game(self):
        self.collect_all_but([])
        self.assertBeatable(True)

def test_all_level_regions(self):
    regions = [
        get_level_region(level)
        for level in range(0, 101, 5)
    ]

    self.assertEqual(
        len(regions),
        len(set(regions)),
        "Duplicate level regions detected",
    )

class TestGhostCardCapacity(TCGSimulatorTestBase):
    #from a yaml that failed repeatable because the location amount was perfect to cause and error with minimal items logic
    options = {
        "max_level": 53,
        "product_licenses": 48,
        "goal": "grade_ghost_cards",
        "ghost_goal_amount": 77,
        "card_sanity": "disabled",
        "checks_opening_difficulty": "disabled",
        "checks_selling_difficulty": "easy",
        "checks_grading_difficulty": "disabled",
        "play_table_checks": 17,
        "no_formats": True,
    }

    def test_can_beat_game(self):
        self.collect_all_but([])
        self.assertBeatable(True)