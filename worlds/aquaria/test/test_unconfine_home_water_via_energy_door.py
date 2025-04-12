"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test accessibility of region with the unconfined home water option via the energy door
"""

from . import AquariaTestBase
from ..Options import UnconfineHomeWater, EarlyEnergyForm


class UnconfineHomeWaterEnergyDoorAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of region with the unconfine home water option enabled"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
        "early_energy_form": EarlyEnergyForm.option_off
    }

    def test_unconfine_home_water_energy_door_location(self) -> None:
        """Test locations accessible with unconfined home water via energy door"""
        self.assertTrue(self.can_reach_region("Open Waters top left area"), "Cannot reach Open Waters top left area")
        self.assertFalse(self.can_reach_region("Home Waters, turtle room"), "Can reach Home Waters, turtle room")
