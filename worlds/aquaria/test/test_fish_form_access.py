"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the fish form
"""

from . import AquariaTestBase


class FishFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the fish form"""
    options = {
        "turtle_randomizer": 1,
    }

    def test_fish_form_location(self) -> None:
        """Test locations that require fish form"""
        locations = [
            "The Veil top left area, bulb inside the fish pass",
            "Energy Temple first area, Energy Idol",
            "Mithalas City, Doll",
            "Mithalas City, urn inside a home fish pass",
            "Kelp Forest top right area, bulb in the top fish pass",
            "The Veil bottom area, Verse Egg",
            "Open Water bottom left area, bulb inside the lowest fish pass",
            "Kelp Forest top left area, bulb close to the Verse Egg",
            "Kelp Forest top left area, Verse Egg",
            "Mermog cave, bulb in the left part of the cave",
            "Mermog cave, Piranha Egg",
            "Beating Mergog",
            "Octopus Cave, Dumbo Egg",
            "Octopus Cave, bulb in the path below the Octopus Cave path",
            "Beating Octopus Prime",
            "Abyss left area, bulb in the bottom fish pass"
        ]
        items = [["Fish form"]]
        self.assertAccessDependency(locations, items)
