"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the dual song
"""

from . import AquariaTestBase


class LiAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the dual song"""
    options = {
        "turtle_randomizer": 1,
    }

    def test_li_song_location(self) -> None:
        """Test locations that require the dual song"""
        locations = [
            "The Body bottom area, bulb in the Jelly Zap room",
            "The Body bottom area, bulb in the nautilus room",
            "The Body bottom area, Mutant Costume",
            "Final Boss area, bulb in the boss third form room",
            "Objective complete"
        ]
        items = [["Dual form"]]
        self.assertAccessDependency(locations, items)
