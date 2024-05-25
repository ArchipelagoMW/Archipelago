"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the fish form
"""

from worlds.aquaria.test import AquariaTestBase


class FishFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the fish form"""
    options = {
        "turtle_randomizer": 1,
    }

    def test_fish_form_location(self) -> None:
        """Test locations that require fish form"""
        locations = [
            "The veil top left area, bulb inside the fish pass",
            "Mithalas city, Doll",
            "Mithalas city, urn inside a home fish pass",
            "Kelp Forest top right area, bulb in the top fish pass",
            "The veil bottom area, Verse egg",
            "Open water bottom left area, bulb inside the lowest fish pass",
            "Kelp Forest top left area, bulb close to the Verse egg",
            "Kelp forest top left area, Verse egg",
            "Mermog cave, bulb in the left part of the cave",
            "Mermog cave, Piranha Egg",
            "Beating Mergog",
            "Octopus cave, Dumbo Egg",
            "Octopus cave, bulb in the path below the octopus cave path",
            "Beating Octopus Prime",
            "Abyss left area, bulb in the bottom fish pass",
            "Arnassi ruins, Arnassi Armor"
        ]
        items = [["Fish form"]]
        self.assertAccessDependency(locations, items)
