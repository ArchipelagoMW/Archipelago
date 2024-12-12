"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the beast form or arnassi armor
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames


class BeastForArnassiArmormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the beast form or arnassi armor"""

    def test_beast_form_arnassi_armor_location(self) -> None:
        """Test locations that require beast form or arnassi armor"""
        locations = [
            AquariaLocationNames.MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS,
            AquariaLocationNames.ARNASSI_RUINS_CRAB_ARMOR,
            AquariaLocationNames.ARNASSI_RUINS_SONG_PLANT_SPORE,
            AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_AT_THE_END_OF_THE_TOP_PATH,
            AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_AT_THE_END_OF_THE_TOP_PATH,
            AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_TOP_PATH,
            AquariaLocationNames.MITHALAS_CITY_MITHALAS_POT,
            AquariaLocationNames.MITHALAS_CITY_URN_IN_THE_CASTLE_FLOWER_TUBE_ENTRANCE,
            AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
            AquariaLocationNames.MITHALAS_CATHEDRAL_MITHALAN_DRESS,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_JELLY_EGG,
            AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_IN_THE_MIDDLE_OF_THE_WALL_JUMP_CLIFF,
            AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL,
            AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
            AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.BEATING_MERGOG,
            AquariaLocationNames.BEATING_CRABBIUS_MAXIMUS,
            AquariaLocationNames.BEATING_OCTOPUS_PRIME,
            AquariaLocationNames.BEATING_MITHALAN_PRIESTS,
            AquariaLocationNames.SUNKEN_CITY_CLEARED
        ]
        items = [[ItemNames.BEAST_FORM, ItemNames.ARNASSI_ARMOR]]
        self.assertAccessDependency(locations, items)
