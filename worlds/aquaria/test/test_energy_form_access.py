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
            "Home water, Nautilus egg",
            "Naija's home, bulb after the energy door",
            "Energy temple first area, bulb in the bottom room blocked by a rock",
            "Energy temple second area, bulb under the rock",
            "Energy temple bottom entrance, Krotite armor",
            "Energy temple third area, bulb in the bottom path",
            "Energy temple boss area, Fallen god tooth",
            "Energy temple blaster room, Blaster egg",
            "Mithalas city castle, beating the priests",
            "Mithalas cathedral, first urn in the top right room",
            "Mithalas cathedral, second urn in the top right room",
            "Mithalas cathedral, third urn in the top right room",
            "Mithalas cathedral, urn in the flesh room with fleas",
            "Mithalas cathedral, first urn in the bottom right path",
            "Mithalas cathedral, second urn in the bottom right path",
            "Mithalas cathedral, urn behind the flesh vein",
            "Mithalas cathedral, urn in the top left eyes boss room",
            "Mithalas cathedral, first urn in the path behind the flesh vein",
            "Mithalas cathedral, second urn in the path behind the flesh vein",
            "Mithalas cathedral, third urn in the path behind the flesh vein",
            "Mithalas cathedral, fourth urn in the top right room",
            "Mithalas cathedral, Mithalan dress",
            "Mithalas cathedral right area, urn below the left entrance",
            "Cathedral boss area, beating Mithalan God",
            "Kelp forest top left area, bulb close to the Verse egg",
            "Kelp forest top left area, Verse egg",
            "Kelp forest boss area, beating Drunian God",
            "Mermog cave, Piranha egg",
            "Octopus cave, Dumbo egg",
            "Sun temple boss area, beating Sun God",
            "Arnassi ruins, Crab armor",
            "King Jellyfish cave, bulb in the right path from King Jelly",
            "King Jellyfish cave, Jellyfish Costume",
            "Sunken city, bulb on top of the boss area",
            "Final boss area, bulb in the boss third form room",
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
