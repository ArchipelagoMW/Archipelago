"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the nature form
"""

from . import AquariaTestBase


class NatureFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the nature form"""
    options = {
        "turtle_randomizer": 1,
    }

    def test_nature_form_location(self) -> None:
        """Test locations that require nature form"""
        locations = [
            "Song Cave, Anemone Seed",
            "Energy Temple blaster room, Blaster Egg",
            "Beating Blaster Peg Prime",
            "Kelp Forest top left area, Verse Egg",
            "Kelp Forest top left area, bulb close to the Verse Egg",
            "Mithalas City Castle, beating the Priests",
            "Kelp Forest sprite cave, bulb in the second room",
            "Kelp Forest sprite cave, Seed Bag",
            "Beating Mithalan priests",
            "Abyss left area, bulb in the bottom fish pass",
            "Bubble Cave, Verse Egg",
            "Beating Mantis Shrimp Prime",
            "Sunken City right area, crate close to the save crystal",
            "Sunken City right area, crate in the left bottom room",
            "Sunken City left area, crate in the little pipe room",
            "Sunken City left area, crate close to the save crystal",
            "Sunken City left area, crate before the bedroom",
            "Sunken City left area, Girl Costume",
            "Sunken City, bulb on top of the boss area",
            "Beating the Golem",
            "Sunken City cleared",
            "The Body center area, breaking Li's cage",
            "The Body center area, bulb on the main path blocking tube",
            "The Body left area, first bulb in the top face room",
            "The Body left area, second bulb in the top face room",
            "The Body left area, bulb below the water stream",
            "The Body left area, bulb in the top path to the top face room",
            "The Body left area, bulb in the bottom face room",
            "The Body right area, bulb in the top face room",
            "The Body right area, bulb in the top path to the bottom face room",
            "The Body right area, bulb in the bottom face room",
            "The Body bottom area, bulb in the Jelly Zap room",
            "The Body bottom area, bulb in the nautilus room",
            "The Body bottom area, Mutant Costume",
            "Final Boss area, bulb in the boss third form room",
            "Objective complete"
        ]
        items = [["Nature form"]]
        self.assertAccessDependency(locations, items)
