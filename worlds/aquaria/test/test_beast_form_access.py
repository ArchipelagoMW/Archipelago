"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the beast form
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames


class BeastFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the beast form"""

    def test_beast_form_location(self) -> None:
        """Test locations that require beast form"""
        locations = [
            AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_JELLY_EGG,
            AquariaLocationNames.MITHALAS_CATHEDRAL_MITHALAN_DRESS,
            AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL,
            AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
            AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.BEATING_MERGOG,
            AquariaLocationNames.BEATING_OCTOPUS_PRIME,
            AquariaLocationNames.SUNKEN_CITY_CLEARED,
        ]
        items = [[ItemNames.BEAST_FORM]]
        self.assertAccessDependency(locations, items)
