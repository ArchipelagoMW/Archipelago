"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test accessibility of region with the home water confine via option
"""

from . import AquariaTestBase
from ..Options import UnconfineHomeWater, EarlyEnergyForm


class ConfinedHomeWaterAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of region with the unconfine home water option disabled"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_off,
        "early_energy_form": EarlyEnergyForm.option_off
    }

    def test_confine_home_water_location(self) -> None:
        """Test region accessible with confined home water"""
        self.assertFalse(self.can_reach_region("Open Waters top left area"), "Can reach Open Waters top left area")
        self.assertFalse(self.can_reach_region("Home Waters, turtle room"), "Can reach Home Waters, turtle room")
