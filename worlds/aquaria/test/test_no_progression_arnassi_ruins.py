"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in Arnassi Ruins when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification


class NoProgressionArnassiRuinsTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in Arnassi Ruins when option enabled"""
    options = {
        "no_progression_arnassi_ruins": True
    }

    unfillable_locations = [
        "Arnassi Ruins, bulb in the right part",
        "Arnassi Ruins, bulb in the left part",
        "Arnassi Ruins, bulb in the center part",
        "Arnassi Ruins, Song Plant Spore",
        "Arnassi Ruins, Arnassi Armor",
        "Arnassi Ruins, Arnassi Statue",
        "Arnassi Ruins, Transturtle",
        "Arnassi Ruins, Crab Armor",
    ]

    def test_no_progression_arnassi_ruins(self) -> None:
        """
            Unit test used to test that no progression items can be put in Arnassi Ruins when option enabled
        """
        for location in self.unfillable_locations:
            for item_name in self.world.item_names:
                item = self.get_item_by_name(item_name)
                if item.classification == ItemClassification.progression:
                    self.assertFalse(
                        self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                        "The location \"" + location + "\" can be filled with \"" + item_name + "\"")
                else:
                    self.assertTrue(
                        self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                        "The location \"" + location + "\" cannot be filled with \"" + item_name + "\"")

