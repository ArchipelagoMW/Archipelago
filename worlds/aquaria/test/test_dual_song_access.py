"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the dual song
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import TurtleRandomizer


class LiAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the dual song"""
    options = {
        "turtle_randomizer": TurtleRandomizer.option_all,
    }

    def test_li_song_location(self) -> None:
        """Test locations that require the dual song"""
        locations = [
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_JELLY_ZAP_ROOM,
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_NAUTILUS_ROOM,
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_MUTANT_COSTUME,
            AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
            AquariaLocationNames.OBJECTIVE_COMPLETE
        ]
        items = [[ItemNames.DUAL_FORM]]
        self.assertAccessDependency(locations, items)
