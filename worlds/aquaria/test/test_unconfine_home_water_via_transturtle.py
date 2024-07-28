"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test accessibility of region with the unconfined home water option via transturtle
"""

from . import AquariaTestBase


class UnconfineHomeWaterTransturtleAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of region with the unconfine home water option enabled"""
    options = {
        "unconfine_home_water": 2,
        "early_energy_form": False
    }

    def test_unconfine_home_water_transturtle_location(self) -> None:
        """Test locations accessible with unconfined home water via transportation turtle"""
        self.assertTrue(self.can_reach_region("Home Water, turtle room"), "Cannot reach Home Water, turtle room")
        self.assertFalse(self.can_reach_region("Open Water top left area"), "Can reach Open Water top left area")
