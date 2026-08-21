"""
Author: Louis M
Date: Sun, 06 Apr 2025 14:00:32 +0000
Description: Unit test used to test Sun Temple cliffs access
"""
from BaseClasses import CollectionState
from . import AquariaTestBase
from ..Items import ItemNames
from ..Options import UnconfineHomeWater
from ..Locations import AquariaLocationNames


class SunTempleCliffAccessTest(AquariaTestBase):
    """Unit test used to test Sun Temple cliffs access"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door
    }

    def test_sun_temple_cliff_access(self) -> None:
        """test Sun Temple cliffs access"""
        state = CollectionState(self.multiworld)
        state.collect(self.get_item_by_name(ItemNames.BEAST_FORM))
        state.collect(self.get_item_by_name(ItemNames.SUN_FORM))
        first_cliff_location = self.multiworld.get_location(
            AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB, 1)
        self.assertFalse(first_cliff_location.can_reach(state))
        second_cliff_location = self.multiworld.get_location(
            AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB, 1)
        self.assertFalse(second_cliff_location.can_reach(state))