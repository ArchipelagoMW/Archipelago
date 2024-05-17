"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in hard or hidden locations when option enabled
"""

from worlds.aquaria.test import AquariaTestBase
from BaseClasses import ItemClassification


class UNoProgressionHardHiddenTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in hard or hidden locations when option enabled"""
    options = {
        "no_progression_hard_or_hidden_locations": True
    }

    unfillable_locations = [
        "Energy temple boss area, Fallen god tooth",
        "Cathedral boss area, beating Mithalan God",
        "Kelp forest boss area, beating Drunian God",
        "Sun temple boss area, beating Sun God",
        "Sunken city, bulb on the top of the boss area (boiler room)",
        "Home water, Nautilus Egg",
        "Energy temple blaster room, Blaster egg",
        "Mithalas castle, beating the priests",
        "Mermog cave, Piranha Egg",
        "Octopus cave, Dumbo Egg",
        "King Jellyfish cave, bulb in the right path from King Jelly",
        "King Jellyfish cave, Jellyfish Costume",
        "Final boss area, bulb in the boss third form room",
        "Sun Worm path, first cliff bulb",
        "Sun Worm path, second cliff bulb",
        "The veil top right area, bulb in the top of the water fall",
        "Bubble cave, bulb in the left cave wall",
        "Bubble cave, bulb in the right cave wall (behind the ice cristal)",
        "Bubble cave, Verse egg",
        "Kelp Forest bottom left area, bulb close to the spirit crystals",
        "Kelp forest bottom left area, Walker baby",
        "Sun temple, Sun key",
        "The body bottom area, Mutant Costume",
        "Sun temple, bulb in the hidden room of the right part",
        "Arnassi ruins, Arnassi Armor",
    ]

    def test_unconfine_home_water_both_location_fillable(self) -> None:
        """
            Unit test used to test that no progression items can be put in hard or hidden locations when option enabled
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

