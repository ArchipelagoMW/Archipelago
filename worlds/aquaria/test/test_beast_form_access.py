"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the beast form
"""

from worlds.aquaria.test import AquariaTestBase


class BeastFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the beast form"""

    def test_beast_form_location(self) -> None:
        """Test locations that require beast form"""
        locations = [
            "Mithalas City Castle, beating the Priests",
            "Arnassi Ruins, Crab Armor",
            "Arnassi Ruins, Song Plant Spore",
            "Mithalas City, first bulb at the end of the top path",
            "Mithalas City, second bulb at the end of the top path",
            "Mithalas City, bulb in the top path",
            "Mithalas City, Mithalas Pot",
            "Mithalas City, urn in the Castle flower tube entrance",
            "Mermog cave, Piranha Egg",
            "Mithalas Cathedral, Mithalan Dress",
            "Turtle cave, bulb in Bubble Cliff",
            "Turtle cave, Urchin Costume",
            "Sun Worm path, first cliff bulb",
            "Sun Worm path, second cliff bulb",
            "The Veil top right area, bulb at the top of the waterfall",
            "Bubble Cave, bulb in the left cave wall",
            "Bubble Cave, bulb in the right cave wall (behind the ice crystal)",
            "Bubble Cave, Verse Egg",
            "Sunken City, bulb on top of the boss area",
            "Octopus Cave, Dumbo Egg",
            "Beating the Golem",
            "Beating Mergog",
            "Beating Crabbius Maximus",
            "Beating Octopus Prime",
            "Beating Mantis Shrimp Prime",
            "King Jellyfish Cave, Jellyfish Costume",
            "King Jellyfish Cave, bulb in the right path from King Jelly",
            "Beating King Jellyfish God Prime",
            "Beating Mithalan priests",
            "Sunken City cleared"
        ]
        items = [["Beast form"]]
        self.assertAccessDependency(locations, items)
