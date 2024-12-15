"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test accessibility of region with the home water confine via option
"""

from . import AquariaTestBase


class ConfinedHomeWaterAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of region with the unconfine home water option disabled"""
    options = {
        "unconfine_home_water": 0,
        "early_energy_form": False
    }

    def test_confine_home_water_location(self) -> None:
        """Test region accessible with confined home water"""
        self.assertFalse(self.can_reach_region("Open Water top left area"), "Can reach Open Water top left area")
        self.assertFalse(self.can_reach_region("Home Water, turtle room"), "Can reach Home Water, turtle room")
