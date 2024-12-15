"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in hard or hidden locations when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification


class UNoProgressionHardHiddenTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in hard or hidden locations when option enabled"""
    options = {
        "no_progression_hard_or_hidden_locations": True
    }

    unfillable_locations = [
        "Energy Temple boss area, Fallen God Tooth",
        "Mithalas boss area, beating Mithalan God",
        "Kelp Forest boss area, beating Drunian God",
        "Sun Temple boss area, beating Sun God",
        "Sunken City, bulb on top of the boss area",
        "Home Water, Nautilus Egg",
        "Energy Temple blaster room, Blaster Egg",
        "Mithalas City Castle, beating the Priests",
        "Mermog cave, Piranha Egg",
        "Octopus Cave, Dumbo Egg",
        "King Jellyfish Cave, bulb in the right path from King Jelly",
        "King Jellyfish Cave, Jellyfish Costume",
        "Final Boss area, bulb in the boss third form room",
        "Sun Worm path, first cliff bulb",
        "Sun Worm path, second cliff bulb",
        "The Veil top right area, bulb at the top of the waterfall",
        "Bubble Cave, bulb in the left cave wall",
        "Bubble Cave, bulb in the right cave wall (behind the ice crystal)",
        "Bubble Cave, Verse Egg",
        "Kelp Forest bottom left area, bulb close to the spirit crystals",
        "Kelp Forest bottom left area, Walker Baby",
        "Sun Temple, Sun Key",
        "The Body bottom area, Mutant Costume",
        "Sun Temple, bulb in the hidden room of the right part",
        "Arnassi Ruins, Arnassi Armor",
    ]

    def test_unconfine_home_water_both_location_fillable(self) -> None:
        """
            Unit test used to test that no progression items can be put in hard or hidden locations when option enabled
        """
        for location in self.unfillable_locations:
            for item_name in self.world.item_names:
                item = self.get_item_by_name(item_name)
                if item.advancement:
                    self.assertFalse(
                        self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                        "The location \"" + location + "\" can be filled with \"" + item_name + "\"")
                else:
                    self.assertTrue(
                        self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                        "The location \"" + location + "\" cannot be filled with \"" + item_name + "\"")

