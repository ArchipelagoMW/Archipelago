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
            "Mithalas city castle, beating the priests",
            "Arnassi ruins, Crab armor",
            "Arnassi ruins, Song plant spore",
            "Mithalas city, first bulb at the end of the top path",
            "Mithalas city, second bulb at the end of the top path",
            "Mithalas city, bulb in the top path",
            "Mithalas city, Mithalas pot",
            "Mithalas city, urn in the cathedral flower tube entrance",
            "Mermog cave, Piranha egg",
            "Mithalas cathedral, Mithalan dress",
            "Turtle cave, bulb in bubble cliff",
            "Turtle cave, Urchin costume",
            "Sun Worm path, first cliff bulb",
            "Sun Worm path, second cliff bulb",
            "The veil top right area, bulb in the top of the waterfall",
            "Bubble cave, bulb in the left cave wall",
            "Bubble cave, bulb in the right cave wall (behind the ice crystal)",
            "Bubble cave, Verse egg",
            "Sunken city, bulb on top of the boss area",
            "Octopus cave, Dumbo egg",
            "Beating the Golem",
            "Beating Mergog",
            "Beating Crabbius Maximus",
            "Beating Octopus Prime",
            "Beating Mantis Shrimp Prime",
            "King Jellyfish cave, Jellyfish Costume",
            "King Jellyfish cave, bulb in the right path from King Jelly",
            "Beating King Jellyfish God Prime",
            "Beating Mithalan priests",
            "Sunken City cleared"
        ]
        items = [["Beast form"]]
        self.assertAccessDependency(locations, items)
