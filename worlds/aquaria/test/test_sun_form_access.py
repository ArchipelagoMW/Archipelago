"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the sun form
"""

from worlds.aquaria.test import AquariaTestBase


class SunFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the sun form"""

    def test_sun_form_location(self) -> None:
        """Test locations that require sun form"""
        locations = [
            "First secret",
            "The whale, Verse egg",
            "Abyss right area, bulb behind the rock in the whale room",
            "Octopus cave, Dumbo Egg",
            "Beating Octopus Prime",
            "Final boss area, bulb in the boss third form room",
            "Objective complete"
        ]
        items = [["Sun form"]]
        self.assertAccessDependency(locations, items)
