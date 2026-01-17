import logging
from worlds.plateup.test.bases import PlateUpTestBase


class TestDayOptionLogic(PlateUpTestBase):
    options = {
        "goal": 1, # Complete x days
        "day_count": 100,
    }

    # Optionally, turn up the logging
    # logging.getLogger().setLevel(logging.INFO)

    def test_has_completion_condition(self) -> None:
        """ Can you even beat PlateUp? """
        self.assertIsNotNone(self.multiworld.completion_condition[self.player])
