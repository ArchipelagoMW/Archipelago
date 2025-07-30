"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test accessibility of region with the unconfined home water option via transportation
             turtle and energy door
"""

from . import AquariaTestBase
from ..Options import UnconfineHomeWater, EarlyEnergyForm


class UnconfineHomeWaterBothAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of region with the unconfine home water option enabled"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_both,
        "early_energy_form": EarlyEnergyForm.option_off
    }

    def test_unconfine_home_water_both_location(self) -> None:
        """Test locations accessible with unconfined home water via energy door and transportation turtle"""
        self.assertTrue(self.can_reach_region("Open Waters top left area"), "Cannot reach Open Waters top left area")
        self.assertTrue(self.can_reach_region("Home Waters, turtle room"), "Cannot reach Home Waters, turtle room")
