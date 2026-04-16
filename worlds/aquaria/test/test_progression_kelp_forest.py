"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that progression items can be put in Kelp Forest when option enabled
"""

from . import AquariaTestBase
from ..Locations import AquariaLocationNames


class ProgressionKelpForestTest(AquariaTestBase):
    """Unit test used to test that progression items can be put in Kelp Forest when option enabled"""
    options = {
        "no_progression_kelp_forest": False
    }

    unfillable_locations = [
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_BOTTOM_LEFT_CLEARING,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_PATH_DOWN_FROM_THE_TOP_LEFT_CLEARING,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_TOP_LEFT_CLEARING,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_JELLY_EGG,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_CLOSE_TO_THE_VERSE_EGG,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_VERSE_EGG,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_AT_THE_LEFT_OF_THE_CENTER_CLEARING,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_LEFT_PATH_S_BIG_ROOM,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_LEFT_PATH_S_SMALL_ROOM,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_CENTER_CLEARING,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BLACK_PEARL,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_TOP_FISH_PASS,
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_BULB_CLOSE_TO_THE_SPIRIT_CRYSTALS,
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_WALKER_BABY,
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_TRANSTURTLE,
        AquariaLocationNames.KELP_FOREST_BOTTOM_RIGHT_AREA_ODD_CONTAINER,
        AquariaLocationNames.KELP_FOREST_BOSS_AREA_BEATING_DRUNIAN_GOD,
        AquariaLocationNames.KELP_FOREST_BOSS_ROOM_BULB_AT_THE_BOTTOM_OF_THE_AREA,
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_FISH_CAVE_PUZZLE,
        AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_BULB_INSIDE_THE_FISH_PASS,
        AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_BULB_IN_THE_SECOND_ROOM,
        AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_SEED_BAG,
        AquariaLocationNames.MERMOG_CAVE_BULB_IN_THE_LEFT_PART_OF_THE_CAVE,
        AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
    ]

    def test_progression_kelp_forest(self) -> None:
        """
            Unit test used to test that progression items can be put in Kelp Forest when option enabled
        """
        for location in self.unfillable_locations:
            for item_name in self.world.item_names:
                item = self.get_item_by_name(item_name)
                self.assertTrue(
                    self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                    "The location \"" + location + "\" cannot be filled with \"" + item_name + "\"")