"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test accessibility of region with the unconfined home water option via transportation
             turtle and energy door
"""

from . import AquariaTestBase


class UnconfineHomeWaterBothAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of region with the unconfine home water option enabled"""
    options = {
        "unconfine_home_water": 3,
        "early_energy_form": False
    }

    def test_unconfine_home_water_both_location(self) -> None:
        """Test locations accessible with unconfined home water via energy door and transportation turtle"""
        self.assertTrue(self.can_reach_region("Open Water top left area"), "Cannot reach Open Water top left area")
        self.assertTrue(self.can_reach_region("Home Water, turtle room"), "Cannot reach Home Water, turtle room")
