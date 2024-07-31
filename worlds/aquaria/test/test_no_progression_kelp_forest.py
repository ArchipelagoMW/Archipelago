"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in Kelp Forest when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification


class NoProgressionKelpForestTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in Kelp Forest when option enabled"""
    options = {
        "no_progression_kelp_forest": True
    }

    unfillable_locations = [
        "Kelp Forest top left area, bulb in the bottom left clearing",
        "Kelp Forest top left area, bulb in the path down from the top left clearing",
        "Kelp Forest top left area, bulb in the top left clearing",
        "Kelp Forest top left area, Jelly Egg",
        "Kelp Forest top left area, bulb close to the Verse Egg",
        "Kelp Forest top left area, Verse Egg",
        "Kelp Forest top right area, bulb under the rock in the right path",
        "Kelp Forest top right area, bulb at the left of the center clearing",
        "Kelp Forest top right area, bulb in the left path's big room",
        "Kelp Forest top right area, bulb in the left path's small room",
        "Kelp Forest top right area, bulb at the top of the center clearing",
        "Kelp Forest top right area, Black Pearl",
        "Kelp Forest top right area, bulb in the top fish pass",
        "Kelp Forest bottom left area, bulb close to the spirit crystals",
        "Kelp Forest bottom left area, Walker Baby",
        "Kelp Forest bottom left area, Transturtle",
        "Kelp Forest bottom right area, Odd Container",
        "Kelp Forest boss area, beating Drunian God",
        "Kelp Forest boss room, bulb at the bottom of the area",
        "Kelp Forest bottom left area, Fish Cave puzzle",
        "Kelp Forest sprite cave, bulb inside the fish pass",
        "Kelp Forest sprite cave, bulb in the second room",
        "Kelp Forest sprite cave, Seed Bag",
        "Mermog cave, bulb in the left part of the cave",
        "Mermog cave, Piranha Egg",
    ]

    def test_no_progression_kelp_forest(self) -> None:
        """
            Unit test used to test that no progression items can be put in Kelp Forest when option enabled
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

