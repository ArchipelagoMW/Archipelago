"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without a light (Dumbo pet or sun form)
"""

from . import AquariaTestBase


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
            # "Sun Temple, bulb in the top left part",
            # "Sun Temple, bulb in the top right part",
            # "Sun Temple, bulb at the top of the high dark room",
            # "Sun Temple, Golden Gear",
            # "Sun Worm path, first path bulb",
            # "Sun Worm path, second path bulb",
            # "Sun Worm path, first cliff bulb",
            "Octopus Cave, Dumbo Egg",
            "Kelp Forest bottom right area, Odd Container",
            "Kelp Forest top right area, Black Pearl",
            "Abyss left area, bulb in hidden path room",
            "Abyss left area, bulb in the right part",
            "Abyss left area, Glowing Seed",
            "Abyss left area, Glowing Plant",
            "Abyss left area, bulb in the bottom fish pass",
            "Abyss right area, bulb behind the rock in the whale room",
            "Abyss right area, bulb in the middle path",
            "Abyss right area, bulb behind the rock in the middle path",
            "Abyss right area, bulb in the left green room",
            "Ice Cave, bulb in the room to the right",
            "Ice Cave, first bulb in the top exit room",
            "Ice Cave, second bulb in the top exit room",
            "Ice Cave, third bulb in the top exit room",
            "Ice Cave, bulb in the left room",
            "Bubble Cave, bulb in the left cave wall",
            "Bubble Cave, bulb in the right cave wall (behind the ice crystal)",
            "Bubble Cave, Verse Egg",
            "Beating Mantis Shrimp Prime",
            "King Jellyfish Cave, bulb in the right path from King Jelly",
            "King Jellyfish Cave, Jellyfish Costume",
            "Beating King Jellyfish God Prime",
            "The Whale, Verse Egg",
            "First secret",
            "Sunken City right area, crate close to the save crystal",
            "Sunken City right area, crate in the left bottom room",
            "Sunken City left area, crate in the little pipe room",
            "Sunken City left area, crate close to the save crystal",
            "Sunken City left area, crate before the bedroom",
            "Sunken City left area, Girl Costume",
            "Sunken City, bulb on top of the boss area",
            "Sunken City cleared",
            "Beating the Golem",
            "Beating Octopus Prime",
            "Final Boss area, bulb in the boss third form room",
            "Objective complete",
        ]
        items = [["Sun form", "Baby Dumbo", "Has sun crystal"]]
        self.assertAccessDependency(locations, items)
