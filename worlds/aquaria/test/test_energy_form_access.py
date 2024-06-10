"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the bind song (without the early
             energy form option)
"""

from worlds.aquaria.test import AquariaTestBase


class EnergyFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the energy form"""
    options = {
        "early_energy_form": False,
    }

    def test_energy_form_location(self) -> None:
        """Test locations that require Energy form"""
        locations = [
            "Home Water, Nautilus Egg",
            "Naija's Home, bulb after the energy door",
            "Energy Temple first area, bulb in the bottom room blocked by a rock",
            "Energy Temple second area, bulb under the rock",
            "Energy Temple bottom entrance, Krotite Armor",
            "Energy Temple third area, bulb in the bottom path",
            "Energy Temple boss area, Fallen God Tooth",
            "Energy Temple blaster room, Blaster Egg",
            "Mithalas City Castle, beating the Priests",
            "Mithalas Cathedral, first urn in the top right room",
            "Mithalas Cathedral, second urn in the top right room",
            "Mithalas Cathedral, third urn in the top right room",
            "Mithalas Cathedral, urn in the flesh room with fleas",
            "Mithalas Cathedral, first urn in the bottom right path",
            "Mithalas Cathedral, second urn in the bottom right path",
            "Mithalas Cathedral, urn behind the flesh vein",
            "Mithalas Cathedral, urn in the top left eyes boss room",
            "Mithalas Cathedral, first urn in the path behind the flesh vein",
            "Mithalas Cathedral, second urn in the path behind the flesh vein",
            "Mithalas Cathedral, third urn in the path behind the flesh vein",
            "Mithalas Cathedral, fourth urn in the top right room",
            "Mithalas Cathedral, Mithalan Dress",
            "Mithalas Cathedral right area, urn below the left entrance",
            "Cathedral boss area, beating Mithalan God",
            "Kelp Forest top left area, bulb close to the Verse Egg",
            "Kelp Forest top left area, Verse Egg",
            "Kelp Forest boss area, beating Drunian God",
            "Mermog cave, Piranha Egg",
            "Octopus Cave, Dumbo Egg",
            "Sun Temple boss area, beating Sun God",
            "Arnassi Ruins, Crab Armor",
            "King Jellyfish Cave, bulb in the right path from King Jelly",
            "King Jellyfish Cave, Jellyfish Costume",
            "Sunken City, bulb on top of the boss area",
            "Final Boss area, bulb in the boss third form room",
            "Beating Fallen God",
            "Beating Mithalan God",
            "Beating Drunian God",
            "Beating Sun God",
            "Beating the Golem",
            "Beating Nautilus Prime",
            "Beating Blaster Peg Prime",
            "Beating Mergog",
            "Beating Mithalan priests",
            "Beating Octopus Prime",
            "Beating Crabbius Maximus",
            "Beating King Jellyfish God Prime",
            "First secret",
            "Sunken City cleared",
            "Objective complete",
        ]
        items = [["Energy form"]]
        self.assertAccessDependency(locations, items)
