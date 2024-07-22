"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the bind song (without the early
             energy form option)
"""

from . import AquariaTestBase


class EnergyFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the energy form"""
    options = {
        "early_energy_form": False,
    }

    def test_energy_form_location(self) -> None:
        """Test locations that require Energy form"""
        locations = [
            "Energy Temple second area, bulb under the rock",
            "Energy Temple third area, bulb in the bottom path",
            "The Body left area, first bulb in the top face room",
            "The Body left area, second bulb in the top face room",
            "The Body left area, bulb below the water stream",
            "The Body left area, bulb in the top path to the top face room",
            "The Body left area, bulb in the bottom face room",
            "The Body right area, bulb in the top path to the bottom face room",
            "The Body right area, bulb in the bottom face room",
            "Final Boss area, bulb in the boss third form room",
            "Objective complete",
        ]
        items = [["Energy form"]]
        self.assertAccessDependency(locations, items)
