"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in the Veil when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification


class NoProgressionVeilTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in the Veil when option enabled"""
    options = {
        "no_progression_veil": True
    }

    unfillable_locations = [
        "The Veil top left area, In Li's cave",
        "The Veil top left area, bulb under the rock in the top right path",
        "The Veil top left area, bulb hidden behind the blocking rock",
        "The Veil top left area, Transturtle",
        "The Veil top left area, bulb inside the fish pass",
        "Turtle cave, Turtle Egg",
        "Turtle cave, bulb in Bubble Cliff",
        "Turtle cave, Urchin Costume",
        "The Veil top right area, bulb in the middle of the wall jump cliff",
        "The Veil top right area, Golden Starfish",
        "The Veil top right area, bulb at the top of the waterfall",
        "The Veil top right area, Transturtle",
        "The Veil bottom area, bulb in the left path",
        "The Veil bottom area, bulb in the spirit path",
        "The Veil bottom area, Verse Egg",
        "The Veil bottom area, Stone Head",
        "Octopus Cave, Dumbo Egg",
        "Octopus Cave, bulb in the path below the Octopus Cave path",
        "Sun Temple, bulb in the top left part",
        "Sun Temple, bulb in the top right part",
        "Sun Temple, bulb at the top of the high dark room",
        "Sun Temple, Golden Gear",
        "Sun Temple, first bulb of the temple",
        "Sun Temple, bulb on the right part",
        "Sun Temple, bulb in the hidden room of the right part",
        "Sun Temple, Sun Key",
        "Sun Worm path, first path bulb",
        "Sun Worm path, second path bulb",
        "Sun Worm path, first cliff bulb",
        "Sun Worm path, second cliff bulb",
        "Sun Temple boss area, beating Sun God",
    ]

    def test_no_progression_veil(self) -> None:
        """
            Unit test used to test that no progression items can be put in the Veil when option enabled
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

