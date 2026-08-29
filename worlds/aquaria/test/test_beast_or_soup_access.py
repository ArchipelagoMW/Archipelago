"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the beast form or hot soup
"""

from . import AquariaTestBase
from ..Locations import AquariaLocationNames
from ..Items import ItemNames


class BeastOrSoupAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the beast form or hot soup"""

    def test_beast_or_soup_location(self) -> None:
        """Test locations that require beast form or hot soup"""
        locations = [
            AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
            AquariaLocationNames.MITHALAS_CATHEDRAL_MITHALAN_DRESS,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_JELLY_EGG,
            AquariaLocationNames.TURTLE_CAVE_URCHIN_COSTUME,
            AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL,
            AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
            AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
            AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL,
            AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL,
            AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG,
            AquariaLocationNames.BEATING_MANTIS_SHRIMP_PRIME,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.BEATING_MERGOG,
            AquariaLocationNames.BEATING_OCTOPUS_PRIME,
            AquariaLocationNames.SUNKEN_CITY_CLEARED
        ]
        items = [[ItemNames.BEAST_FORM, ItemNames.HOT_SOUP, ItemNames.HOT_SOUP_X_2]]
        self.assertAccessDependency(locations, items)
