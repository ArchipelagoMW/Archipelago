"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in Mithalas when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification


class NoProgressionMithalasTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in Mithalas when option enabled"""
    options = {
        "no_progression_mithalas": True
    }

    unfillable_locations = [
        "Mithalas City, first bulb in the left city part",
        "Mithalas City, second bulb in the left city part",
        "Mithalas City, bulb in the right part",
        "Mithalas City, bulb at the top of the city",
        "Mithalas City, first bulb in a broken home",
        "Mithalas City, second bulb in a broken home",
        "Mithalas City, bulb in the bottom left part",
        "Mithalas City, first bulb in one of the homes",
        "Mithalas City, second bulb in one of the homes",
        "Mithalas City, first urn in one of the homes",
        "Mithalas City, second urn in one of the homes",
        "Mithalas City, first urn in the city reserve",
        "Mithalas City, second urn in the city reserve",
        "Mithalas City, third urn in the city reserve",
        "Mithalas City, first bulb at the end of the top path",
        "Mithalas City, second bulb at the end of the top path",
        "Mithalas City, bulb in the top path",
        "Mithalas City, Mithalas Pot",
        "Mithalas City, urn in the Castle flower tube entrance",
        "Mithalas City, Doll",
        "Mithalas City, urn inside a home fish pass",
        "Mithalas City Castle, bulb in the flesh hole",
        "Mithalas City Castle, Blue Banner",
        "Mithalas City Castle, urn in the bedroom",
        "Mithalas City Castle, first urn of the single lamp path",
        "Mithalas City Castle, second urn of the single lamp path",
        "Mithalas City Castle, urn in the bottom room",
        "Mithalas City Castle, first urn on the entrance path",
        "Mithalas City Castle, second urn on the entrance path",
        "Mithalas City Castle, beating the Priests",
        "Mithalas City Castle, Trident Head",
        "Mithalas Cathedral, first urn in the top right room",
        "Mithalas Cathedral, second urn in the top right room",
        "Mithalas Cathedral, third urn in the top right room",
        "Mithalas Cathedral, bulb in the flesh room with fleas",
        "Mithalas Cathedral, first urn in the bottom right path",
        "Mithalas Cathedral, second urn in the bottom right path",
        "Mithalas Cathedral, urn behind the flesh vein",
        "Mithalas Cathedral, urn in the top left eyes boss room",
        "Mithalas Cathedral, first urn in the path behind the flesh vein",
        "Mithalas Cathedral, second urn in the path behind the flesh vein",
        "Mithalas Cathedral, third urn in the path behind the flesh vein",
        "Mithalas Cathedral, fourth urn in the top right room",
        "Mithalas Cathedral, Mithalan Dress",
        "Mithalas Cathedral, urn below the left entrance",
        "Cathedral Underground, bulb in the center part",
        "Cathedral Underground, first bulb in the top left part",
        "Cathedral Underground, second bulb in the top left part",
        "Cathedral Underground, third bulb in the top left part",
        "Cathedral Underground, bulb close to the save crystal",
        "Cathedral Underground, bulb in the bottom right path",
        "Mithalas boss area, beating Mithalan God",
    ]

    def test_no_progression_mithalas(self) -> None:
        """
            Unit test used to test that no progression items can be put in Mithalas when option enabled
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

