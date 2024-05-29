"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the nature form
"""

from worlds.aquaria.test import AquariaTestBase


class NatureFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the nature form"""
    options = {
        "turtle_randomizer": 1,
    }

    def test_nature_form_location(self) -> None:
        """Test locations that require nature form"""
        locations = [
            "Song cave, Anemone seed",
            "Energy temple blaster room, Blaster egg",
            "Beating Blaster Peg Prime",
            "Kelp forest top left area, Verse egg",
            "Kelp Forest top left area, bulb close to the Verse egg",
            "Mithalas castle, beating the priests",
            "Kelp Forest sprite cave, bulb in the second room",
            "Kelp Forest Sprite Cave, Seed bag",
            "Beating Mithalan priests",
            "Abyss left area, bulb in the bottom fish pass",
            "Bubble cave, Verse egg",
            "Beating Mantis Shrimp Prime",
            "Sunken city right area, crate close to the save cristal",
            "Sunken city right area, crate in the left bottom room",
            "Sunken city left area, crate in the little pipe room",
            "Sunken city left area, crate close to the save cristal",
            "Sunken city left area, crate before the bedroom",
            "Sunken city left area, Girl Costume",
            "Sunken city, bulb on the top of the boss area (boiler room)",
            "Beating the Golem",
            "Sunken City cleared",
            "The body center area, breaking li cage",
            "The body main area, bulb on the main path blocking tube",
            "The body left area, first bulb in the top face room",
            "The body left area, second bulb in the top face room",
            "The body left area, bulb below the water stream",
            "The body left area, bulb in the top path to the top face room",
            "The body left area, bulb in the bottom face room",
            "The body right area, bulb in the top face room",
            "The body right area, bulb in the top path to the bottom face room",
            "The body right area, bulb in the bottom face room",
            "The body bottom area, bulb in the Jelly Zap room",
            "The body bottom area, bulb in the nautilus room",
            "The body bottom area, Mutant Costume",
            "Final boss area, bulb in the boss third form room",
            "Objective complete"
        ]
        items = [["Nature form"]]
        self.assertAccessDependency(locations, items)
