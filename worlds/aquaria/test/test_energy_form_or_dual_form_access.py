"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the energy form and dual form (and Li)
"""

from . import AquariaTestBase


class EnergyFormDualFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the energy form and dual form (and Li)"""
    options = {
        "early_energy_form": False,
    }

    def test_energy_form_or_dual_form_location(self) -> None:
        """Test locations that require Energy form or dual form"""
        locations = [
            "Naija's Home, bulb after the energy door",
            "Home Water, Nautilus Egg",
            "Energy Temple second area, bulb under the rock",
            "Energy Temple bottom entrance, Krotite Armor",
            "Energy Temple third area, bulb in the bottom path",
            "Energy Temple blaster room, Blaster Egg",
            "Energy Temple boss area, Fallen God Tooth",
            "Mithalas City Castle, beating the Priests",
            "Mithalas boss area, beating Mithalan God",
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
            "Mithalas Cathedral, urn below the left entrance",
            "Kelp Forest top left area, bulb close to the Verse Egg",
            "Kelp Forest top left area, Verse Egg",
            "Kelp Forest boss area, beating Drunian God",
            "Mermog cave, Piranha Egg",
            "Octopus Cave, Dumbo Egg",
            "Sun Temple boss area, beating Sun God",
            "King Jellyfish Cave, bulb in the right path from King Jelly",
            "King Jellyfish Cave, Jellyfish Costume",
            "Sunken City right area, crate close to the save crystal",
            "Sunken City right area, crate in the left bottom room",
            "Sunken City left area, crate in the little pipe room",
            "Sunken City left area, crate close to the save crystal",
            "Sunken City left area, crate before the bedroom",
            "Sunken City left area, Girl Costume",
            "Sunken City, bulb on top of the boss area",
            "The Body center area, breaking Li's cage",
            "The Body center area, bulb on the main path blocking tube",
            "The Body left area, first bulb in the top face room",
            "The Body left area, second bulb in the top face room",
            "The Body left area, bulb below the water stream",
            "The Body left area, bulb in the top path to the top face room",
            "The Body left area, bulb in the bottom face room",
            "The Body right area, bulb in the top face room",
            "The Body right area, bulb in the top path to the bottom face room",
            "The Body right area, bulb in the bottom face room",
            "The Body bottom area, bulb in the Jelly Zap room",
            "The Body bottom area, bulb in the nautilus room",
            "The Body bottom area, Mutant Costume",
            "Final Boss area, bulb in the boss third form room",
            "Final Boss area, first bulb in the turtle room",
            "Final Boss area, second bulb in the turtle room",
            "Final Boss area, third bulb in the turtle room",
            "Final Boss area, Transturtle",
            "Beating Fallen God",
            "Beating Blaster Peg Prime",
            "Beating Mithalan God",
            "Beating Drunian God",
            "Beating Sun God",
            "Beating the Golem",
            "Beating Nautilus Prime",
            "Beating Mergog",
            "Beating Mithalan priests",
            "Beating Octopus Prime",
            "Beating King Jellyfish God Prime",
            "Beating the Golem",
            "Sunken City cleared",
            "First secret",
            "Objective complete"
        ]
        items = [["Energy form", "Dual form", "Li and Li song", "Body tongue cleared"]]
        self.assertAccessDependency(locations, items)
