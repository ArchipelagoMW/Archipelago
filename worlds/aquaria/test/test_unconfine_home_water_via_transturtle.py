"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test accessibility of region with the unconfined home water option via transturtle
"""

from . import AquariaTestBase
from ..Options import UnconfineHomeWater, EarlyEnergyForm


class UnconfineHomeWaterTransturtleAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of region with the unconfine home water option enabled"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_transturtle,
        "early_energy_form": EarlyEnergyForm.option_off
    }

    def test_unconfine_home_water_transturtle_location(self) -> None:
        """Test locations accessible with unconfined home water via transportation turtle"""
        self.assertTrue(self.can_reach_region("Home Waters, turtle room"), "Cannot reach Home Waters, turtle room")
        self.assertFalse(self.can_reach_region("Open Waters top left area"), "Can reach Open Waters top left area")
