"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the nature form
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import TurtleRandomizer


class NatureFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the nature form"""
    options = {
        "turtle_randomizer": TurtleRandomizer.option_all,
    }

    def test_nature_form_location(self) -> None:
        """Test locations that require nature form"""
        locations = [
            AquariaLocationNames.SONG_CAVE_ANEMONE_SEED,
            AquariaLocationNames.ENERGY_TEMPLE_BLASTER_ROOM_BLASTER_EGG,
            AquariaLocationNames.BEATING_BLASTER_PEG_PRIME,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_VERSE_EGG,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_CLOSE_TO_THE_VERSE_EGG,
            AquariaLocationNames.MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS,
            AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_BULB_IN_THE_SECOND_ROOM,
            AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_SEED_BAG,
            AquariaLocationNames.BEATING_MITHALAN_PRIESTS,
            AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_BOTTOM_FISH_PASS,
            AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG,
            AquariaLocationNames.BEATING_MANTIS_SHRIMP_PRIME,
            AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL,
            AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_IN_THE_LEFT_BOTTOM_ROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_IN_THE_LITTLE_PIPE_ROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_BEFORE_THE_BEDROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_GIRL_COSTUME,
            AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.SUNKEN_CITY_CLEARED,
            AquariaLocationNames.THE_BODY_CENTER_AREA_BREAKING_LI_S_CAGE,
            AquariaLocationNames.THE_BODY_CENTER_AREA_BULB_ON_THE_MAIN_PATH_BLOCKING_TUBE,
            AquariaLocationNames.THE_BODY_LEFT_AREA_FIRST_BULB_IN_THE_TOP_FACE_ROOM,
            AquariaLocationNames.THE_BODY_LEFT_AREA_SECOND_BULB_IN_THE_TOP_FACE_ROOM,
            AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_BELOW_THE_WATER_STREAM,
            AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_TOP_FACE_ROOM,
            AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM,
            AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_FACE_ROOM,
            AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_BOTTOM_FACE_ROOM,
            AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM,
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_JELLY_ZAP_ROOM,
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_NAUTILUS_ROOM,
            AquariaLocationNames.THE_BODY_BOTTOM_AREA_MUTANT_COSTUME,
            AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
            AquariaLocationNames.OBJECTIVE_COMPLETE
        ]
        items = [[ItemNames.NATURE_FORM]]
        self.assertAccessDependency(locations, items)
