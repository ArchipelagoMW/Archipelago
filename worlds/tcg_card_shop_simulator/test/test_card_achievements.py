from .. import TCGSimulatorWorld
from ..data.helpers.card_types import Difficulty
from ..data.locations import CardAchievementFamily, generate_achievement_locations
from .bases import TCGSimulatorTestBase


class TestAchievementLocations(TCGSimulatorTestBase):
    options = {}
    world: TCGSimulatorWorld

    def test_unique_achievement_location_ids(self):
        locations = [
            location
            for family in CardAchievementFamily
            for location in generate_achievement_locations(
                family,
                Difficulty.IMPOSSIBLE
            )
        ]

        ids = [location.location_id for location in locations]

        self.assertEqual(
            len(ids),
            len(set(ids)),
            "Duplicate achievement location IDs detected"
        )