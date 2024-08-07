"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the beast form or arnassi armor
"""

from . import AquariaTestBase


class BeastForArnassiArmormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the beast form or arnassi armor"""

    def test_beast_form_arnassi_armor_location(self) -> None:
        """Test locations that require beast form or arnassi armor"""
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
            "Kelp Forest top left area, Jelly Egg",
            "The Veil top right area, bulb in the middle of the wall jump cliff",
            "The Veil top right area, bulb at the top of the waterfall",
            "Sunken City, bulb on top of the boss area",
            "Octopus Cave, Dumbo Egg",
            "Beating the Golem",
            "Beating Mergog",
            "Beating Crabbius Maximus",
            "Beating Octopus Prime",
            "Beating Mithalan priests",
            "Sunken City cleared"
        ]
        items = [["Beast form", "Arnassi Armor"]]
        self.assertAccessDependency(locations, items)
