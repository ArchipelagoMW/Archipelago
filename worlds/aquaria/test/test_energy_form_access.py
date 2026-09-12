"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the bind song (without the early
             energy form option)
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import EarlyEnergyForm


class EnergyFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the energy form"""
    options = {
        "early_energy_form": EarlyEnergyForm.option_off
    }

    def test_energy_form_location(self) -> None:
        """Test locations that require Energy form"""
        locations = [
            AquariaLocationNames.ENERGY_TEMPLE_SECOND_AREA_BULB_UNDER_THE_ROCK,
            AquariaLocationNames.ENERGY_TEMPLE_THIRD_AREA_BULB_IN_THE_BOTTOM_PATH,
            AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
            AquariaLocationNames.OBJECTIVE_COMPLETE,
        ]
        items = [[ItemNames.ENERGY_FORM]]
        self.assertAccessDependency(locations, items)
