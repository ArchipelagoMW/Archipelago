"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the spirit form
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames


class SpiritFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the spirit form"""

    def test_spirit_form_location(self) -> None:
        """Test locations that require spirit form"""
        locations = [
            AquariaLocationNames.THE_VEIL_BOTTOM_AREA_BULB_IN_THE_SPIRIT_PATH,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_TRIDENT_HEAD,
            AquariaLocationNames.OPEN_WATERS_SKELETON_PATH_KING_SKULL,
            AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_WALKER_BABY,
            AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_WHALE_ROOM,
            AquariaLocationNames.THE_WHALE_VERSE_EGG,
            AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_ROOM_TO_THE_RIGHT,
            AquariaLocationNames.ICE_CAVERN_FIRST_BULB_IN_THE_TOP_EXIT_ROOM,
            AquariaLocationNames.ICE_CAVERN_SECOND_BULB_IN_THE_TOP_EXIT_ROOM,
            AquariaLocationNames.ICE_CAVERN_THIRD_BULB_IN_THE_TOP_EXIT_ROOM,
            AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_LEFT_ROOM,
            AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL,
            AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL,
            AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_GIRL_COSTUME,
            AquariaLocationNames.BEATING_MANTIS_SHRIMP_PRIME,
            AquariaLocationNames.FIRST_SECRET,
        ]
        items = [[ItemNames.SPIRIT_FORM]]
        self.assertAccessDependency(locations, items)
