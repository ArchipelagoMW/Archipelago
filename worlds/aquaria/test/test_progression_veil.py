"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that progression items can be put in the Veil area when option enabled
"""

from . import AquariaTestBase
from ..Locations import AquariaLocationNames


class ProgressionVeilTest(AquariaTestBase):
    """Unit test used to test that progression items can be put in the Veil area when option enabled"""
    options = {
        "no_progression_veil": False
    }

    unfillable_locations = [
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_IN_LI_S_CAVE,
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_TOP_RIGHT_PATH,
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_HIDDEN_BEHIND_THE_BLOCKING_ROCK,
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_TRANSTURTLE,
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_INSIDE_THE_FISH_PASS,
        AquariaLocationNames.TURTLE_CAVE_TURTLE_EGG,
        AquariaLocationNames.TURTLE_CAVE_BULB_IN_BUBBLE_CLIFF,
        AquariaLocationNames.TURTLE_CAVE_URCHIN_COSTUME,
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_IN_THE_MIDDLE_OF_THE_WALL_JUMP_CLIFF,
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_GOLDEN_STARFISH,
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL,
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_TRANSTURTLE,
        AquariaLocationNames.THE_VEIL_BOTTOM_AREA_BULB_IN_THE_LEFT_PATH,
        AquariaLocationNames.THE_VEIL_BOTTOM_AREA_BULB_IN_THE_SPIRIT_PATH,
        AquariaLocationNames.THE_VEIL_BOTTOM_AREA_VERSE_EGG,
        AquariaLocationNames.THE_VEIL_BOTTOM_AREA_STONE_HEAD,
        AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
        AquariaLocationNames.OCTOPUS_CAVE_BULB_IN_THE_PATH_BELOW_THE_OCTOPUS_CAVE_PATH,
        AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_TOP_LEFT_PART,
        AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_TOP_RIGHT_PART,
        AquariaLocationNames.SUN_TEMPLE_BULB_AT_THE_TOP_OF_THE_HIGH_DARK_ROOM,
        AquariaLocationNames.SUN_TEMPLE_GOLDEN_GEAR,
        AquariaLocationNames.SUN_TEMPLE_FIRST_BULB_OF_THE_TEMPLE,
        AquariaLocationNames.SUN_TEMPLE_BULB_ON_THE_RIGHT_PART,
        AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_HIDDEN_ROOM_OF_THE_RIGHT_PART,
        AquariaLocationNames.SUN_TEMPLE_SUN_KEY,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_PATH_BULB,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_PATH_BULB,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB,
        AquariaLocationNames.SUN_TEMPLE_BOSS_AREA_BEATING_LUMEREAN_GOD,
    ]

    def test_progression_veil(self) -> None:
        """
            Unit test used to test that progression items can be put in the Veil area when option enabled
        """
        for location in self.unfillable_locations:
            for item_name in self.world.item_names:
                item = self.get_item_by_name(item_name)
                self.assertTrue(
                    self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                    "The location \"" + location + "\" cannot be filled with \"" + item_name + "\"")
