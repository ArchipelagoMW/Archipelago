"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that progression items can be put in hard or hidden locations when option disabled
"""

from . import AquariaTestBase
from ..Locations import AquariaLocationNames


class UNoProgressionHardHiddenTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in hard or hidden locations when option disabled"""
    options = {
        "no_progression_hard_or_hidden_locations": False
    }

    unfillable_locations = [
        AquariaLocationNames.ENERGY_TEMPLE_BOSS_AREA_FALLEN_GOD_TOOTH,
        AquariaLocationNames.MITHALAS_BOSS_AREA_BEATING_MITHALAN_GOD,
        AquariaLocationNames.KELP_FOREST_BOSS_AREA_BEATING_DRUNIAN_GOD,
        AquariaLocationNames.SUN_TEMPLE_BOSS_AREA_BEATING_LUMEREAN_GOD,
        AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA,
        AquariaLocationNames.HOME_WATERS_NAUTILUS_EGG,
        AquariaLocationNames.ENERGY_TEMPLE_BLASTER_ROOM_BLASTER_EGG,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS,
        AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
        AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
        AquariaLocationNames.KING_JELLYFISH_CAVE_BULB_IN_THE_RIGHT_PATH_FROM_KING_JELLY,
        AquariaLocationNames.KING_JELLYFISH_CAVE_JELLYFISH_COSTUME,
        AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB,
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL,
        AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL,
        AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL,
        AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG,
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_BULB_CLOSE_TO_THE_SPIRIT_CRYSTALS,
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_WALKER_BABY,
        AquariaLocationNames.SUN_TEMPLE_SUN_KEY,
        AquariaLocationNames.THE_BODY_BOTTOM_AREA_MUTANT_COSTUME,
        AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_HIDDEN_ROOM_OF_THE_RIGHT_PART,
        AquariaLocationNames.ARNASSI_RUINS_ARNASSI_ARMOR,
    ]

    def test_unconfine_home_water_both_location_fillable(self) -> None:
        """Unit test used to test that progression items can be put in hard or hidden locations when option disabled"""
        for location in self.unfillable_locations:
            for item_name in self.world.item_names:
                item = self.get_item_by_name(item_name)
                self.assertTrue(
                    self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                    "The location \"" + location + "\" cannot be filled with \"" + item_name + "\"")

