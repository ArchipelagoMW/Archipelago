"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without a light (Dumbo pet or sun form)
"""

from worlds.aquaria.test import AquariaTestBase


class LightAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without light"""
    options = {
        "turtle_randomizer": 1,
        "light_needed_to_get_to_dark_places": True,
    }

    def test_light_location(self) -> None:
        """Test locations that require light"""
        locations = [
            # Since the `assertAccessDependency` sweep for events even if I tell it not to, those location cannot be
            # tested.
            # "Third secret",
            # "Sun temple, bulb in the top left part",
            # "Sun temple, bulb in the top right part",
            # "Sun temple, bulb at the top of the high dark room",
            # "Sun temple, Golden Gear",
            # "Sun Worm path, first path bulb",
            # "Sun Worm path, second path bulb",
            # "Sun Worm path, first cliff bulb",
            "Octopus cave, Dumbo Egg",
            "Kelp forest bottom right area, Odd Container",
            "Kelp forest top right area, Black pearl",
            "Abyss left area, bulb in hidden path room",
            "Abyss left area, bulb in the right part",
            "Abyss left area, Glowing seed",
            "Abyss left area, Glowing Plant",
            "Abyss left area, bulb in the bottom fish pass",
            "Abyss right area, bulb behind the rock in the whale room",
            "Abyss right area, bulb in the middle path",
            "Abyss right area, bulb behind the rock in the middle path",
            "Abyss right area, bulb in the left green room",
            "Abyss right area, Transturtle",
            "Ice cave, bulb in the room to the right",
            "Ice cave, First bulbs in the top exit room",
            "Ice cave, Second bulbs in the top exit room",
            "Ice cave, third bulbs in the top exit room",
            "Ice cave, bulb in the left room",
            "Bubble cave, bulb in the left cave wall",
            "Bubble cave, bulb in the right cave wall (behind the ice cristal)",
            "Bubble cave, Verse egg",
            "Beating Mantis Shrimp Prime",
            "King Jellyfish cave, bulb in the right path from King Jelly",
            "King Jellyfish cave, Jellyfish Costume",
            "Beating King Jellyfish God Prime",
            "The whale, Verse egg",
            "First secret",
            "Sunken city right area, crate close to the save cristal",
            "Sunken city right area, crate in the left bottom room",
            "Sunken city left area, crate in the little pipe room",
            "Sunken city left area, crate close to the save cristal",
            "Sunken city left area, crate before the bedroom",
            "Sunken city left area, Girl Costume",
            "Sunken city, bulb on the top of the boss area (boiler room)",
            "Sunken City cleared",
            "Beating the Golem",
            "Beating Octopus Prime",
            "Final boss area, bulb in the boss third form room",
            "Objective complete",
        ]
        items = [["Sun form", "Baby dumbo", "Has sun crystal"]]
        self.assertAccessDependency(locations, items)
