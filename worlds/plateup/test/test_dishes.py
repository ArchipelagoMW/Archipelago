import logging
from worlds.plateup.test.bases import PlateUpTestBase


class TestDishOptionLogic(PlateUpTestBase):
    options = {
        "goal": 0, # Franchise x times
        "franchise_count": 1,
        "dish": 2,
    }

    # Optionally, turn up the logging
    # logging.getLogger().setLevel(logging.INFO)

    def test_has_completion_condition(self) -> None:
        """ Can you even beat PlateUp? """
        self.assertIsNotNone(self.multiworld.completion_condition[self.player])
