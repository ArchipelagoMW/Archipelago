"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the sun form
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames


class SunFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the sun form"""

    def test_sun_form_location(self) -> None:
        """Test locations that require sun form"""
        locations = [
            AquariaLocationNames.FIRST_SECRET,
            AquariaLocationNames.THE_WHALE_VERSE_EGG,
            AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_WHALE_ROOM,
            AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
            AquariaLocationNames.BEATING_OCTOPUS_PRIME,
            AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.SUNKEN_CITY_CLEARED,
            AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
            AquariaLocationNames.OBJECTIVE_COMPLETE
        ]
        items = [[ItemNames.SUN_FORM]]
        self.assertAccessDependency(locations, items)
