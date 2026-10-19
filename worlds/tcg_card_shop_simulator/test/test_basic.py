
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