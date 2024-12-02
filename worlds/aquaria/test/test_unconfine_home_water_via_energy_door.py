"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test accessibility of region with the unconfined home water option via the energy door
"""

from . import AquariaTestBase


class UnconfineHomeWaterEnergyDoorAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of region with the unconfine home water option enabled"""
    options = {
        "unconfine_home_water": 1,
        "early_energy_form": False
    }

    def test_unconfine_home_water_energy_door_location(self) -> None:
        """Test locations accessible with unconfined home water via energy door"""
        self.assertTrue(self.can_reach_region("Open Water top left area"), "Cannot reach Open Water top left area")
        self.assertFalse(self.can_reach_region("Home Water, turtle room"), "Can reach Home Water, turtle room")
