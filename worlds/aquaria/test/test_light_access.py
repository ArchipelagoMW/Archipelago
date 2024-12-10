"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without a light (Dumbo pet or sun form)
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import TurtleRandomizer


class LightAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without light"""
    options = {
        "turtle_randomizer": TurtleRandomizer.option_all,
        "light_needed_to_get_to_dark_places": True,
    }

    def test_light_location(self) -> None:
        """Test locations that require light"""
        locations = [
            # Since the `assertAccessDependency` sweep for events even if I tell it not to, those location cannot be
            # tested.
            # AquariaLocationNames.THIRD_SECRET,
            # AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_TOP_LEFT_PART,
            # AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_TOP_RIGHT_PART,
            # AquariaLocationNames.SUN_TEMPLE_BULB_AT_THE_TOP_OF_THE_HIGH_DARK_ROOM,
            # AquariaLocationNames.SUN_TEMPLE_GOLDEN_GEAR,
            # AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_PATH_BULB,
            # AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_PATH_BULB,
            # AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB,
            AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
            AquariaLocationNames.KELP_FOREST_BOTTOM_RIGHT_AREA_ODD_CONTAINER,
            AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BLACK_PEARL,
            AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_HIDDEN_PATH_ROOM,
            AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_RIGHT_PART,
            AquariaLocationNames.ABYSS_LEFT_AREA_GLOWING_SEED,
            AquariaLocationNames.ABYSS_LEFT_AREA_GLOWING_PLANT,
            AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_BOTTOM_FISH_PASS,
            AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_WHALE_ROOM,
            AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_IN_THE_MIDDLE_PATH,
            AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_MIDDLE_PATH,
            AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_IN_THE_LEFT_GREEN_ROOM,
            AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_ROOM_TO_THE_RIGHT,
            AquariaLocationNames.ICE_CAVERN_FIRST_BULB_IN_THE_TOP_EXIT_ROOM,
            AquariaLocationNames.ICE_CAVERN_SECOND_BULB_IN_THE_TOP_EXIT_ROOM,
            AquariaLocationNames.ICE_CAVERN_THIRD_BULB_IN_THE_TOP_EXIT_ROOM,
            AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_LEFT_ROOM,
            AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL,
            AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL,
            AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG,
            AquariaLocationNames.BEATING_MANTIS_SHRIMP_PRIME,
            AquariaLocationNames.KING_JELLYFISH_CAVE_BULB_IN_THE_RIGHT_PATH_FROM_KING_JELLY,
            AquariaLocationNames.KING_JELLYFISH_CAVE_JELLYFISH_COSTUME,
            AquariaLocationNames.BEATING_KING_JELLYFISH_GOD_PRIME,
            AquariaLocationNames.THE_WHALE_VERSE_EGG,
            AquariaLocationNames.FIRST_SECRET,
            AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL,
            AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_IN_THE_LEFT_BOTTOM_ROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_IN_THE_LITTLE_PIPE_ROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_BEFORE_THE_BEDROOM,
            AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_GIRL_COSTUME,
            AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
            AquariaLocationNames.SUNKEN_CITY_CLEARED,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.BEATING_OCTOPUS_PRIME,
            AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
            AquariaLocationNames.OBJECTIVE_COMPLETE,
        ]
        items = [[ItemNames.SUN_FORM, ItemNames.BABY_DUMBO, ItemNames.HAS_SUN_CRYSTAL]]
        self.assertAccessDependency(locations, items)
