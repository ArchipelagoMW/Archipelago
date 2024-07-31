"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the beast form or hot soup
"""

from . import AquariaTestBase


class BeastOrSoupAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the beast form or hot soup"""

    def test_beast_or_soup_location(self) -> None:
        """Test locations that require beast form or hot soup"""
        locations = [
            "Mermog cave, Piranha Egg",
            "Mithalas Cathedral, Mithalan Dress",
            "Kelp Forest top left area, Jelly Egg",
            "Turtle cave, Urchin Costume",
            "The Veil top right area, bulb at the top of the waterfall",
            "Sunken City, bulb on top of the boss area",
            "Octopus Cave, Dumbo Egg",
            "Bubble Cave, bulb in the left cave wall",
            "Bubble Cave, bulb in the right cave wall (behind the ice crystal)",
            "Bubble Cave, Verse Egg",
            "Beating Mantis Shrimp Prime",
            "Beating the Golem",
            "Beating Mergog",
            "Beating Octopus Prime",
            "Sunken City cleared"
        ]
        items = [["Beast Form", "Hot Soup", "Hot Soup x 2"]]
        self.assertAccessDependency(locations, items)
