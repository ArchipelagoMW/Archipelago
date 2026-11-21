"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in Mithalas when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification
from ..Locations import AquariaLocationNames


class NoProgressionMithalasTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in Mithalas when option enabled"""
    options = {
        "no_progression_mithalas": True
    }

    unfillable_locations = [
        AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_THE_LEFT_CITY_PART,
        AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_THE_LEFT_CITY_PART,
        AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_RIGHT_PART,
        AquariaLocationNames.MITHALAS_CITY_BULB_AT_THE_TOP_OF_THE_CITY,
        AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_A_BROKEN_HOME,
        AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_A_BROKEN_HOME,
        AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_BOTTOM_LEFT_PART,
        AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_ONE_OF_THE_HOMES,
        AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_ONE_OF_THE_HOMES,
        AquariaLocationNames.MITHALAS_CITY_FIRST_URN_IN_ONE_OF_THE_HOMES,
        AquariaLocationNames.MITHALAS_CITY_SECOND_URN_IN_ONE_OF_THE_HOMES,
        AquariaLocationNames.MITHALAS_CITY_FIRST_URN_IN_THE_CITY_RESERVE,
        AquariaLocationNames.MITHALAS_CITY_SECOND_URN_IN_THE_CITY_RESERVE,
        AquariaLocationNames.MITHALAS_CITY_THIRD_URN_IN_THE_CITY_RESERVE,
        AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_AT_THE_END_OF_THE_TOP_PATH,
        AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_AT_THE_END_OF_THE_TOP_PATH,
        AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_TOP_PATH,
        AquariaLocationNames.MITHALAS_CITY_MITHALAS_POT,
        AquariaLocationNames.MITHALAS_CITY_URN_IN_THE_CASTLE_FLOWER_TUBE_ENTRANCE,
        AquariaLocationNames.MITHALAS_CITY_DOLL,
        AquariaLocationNames.MITHALAS_CITY_URN_INSIDE_A_HOME_FISH_PASS,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_BULB_IN_THE_FLESH_HOLE,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_BLUE_BANNER,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_URN_IN_THE_BEDROOM,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_FIRST_URN_OF_THE_SINGLE_LAMP_PATH,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_SECOND_URN_OF_THE_SINGLE_LAMP_PATH,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_URN_IN_THE_BOTTOM_ROOM,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_FIRST_URN_ON_THE_ENTRANCE_PATH,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_SECOND_URN_ON_THE_ENTRANCE_PATH,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_TRIDENT_HEAD,
        AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_TOP_RIGHT_ROOM,
        AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_TOP_RIGHT_ROOM,
        AquariaLocationNames.MITHALAS_CATHEDRAL_THIRD_URN_IN_THE_TOP_RIGHT_ROOM,
        AquariaLocationNames.MITHALAS_CATHEDRAL_BULB_IN_THE_FLESH_ROOM_WITH_FLEAS,
        AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_BOTTOM_RIGHT_PATH,
        AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_BOTTOM_RIGHT_PATH,
        AquariaLocationNames.MITHALAS_CATHEDRAL_URN_BEHIND_THE_FLESH_VEIN,
        AquariaLocationNames.MITHALAS_CATHEDRAL_URN_IN_THE_TOP_LEFT_EYES_BOSS_ROOM,
        AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN,
        AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN,
        AquariaLocationNames.MITHALAS_CATHEDRAL_THIRD_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN,
        AquariaLocationNames.MITHALAS_CATHEDRAL_FOURTH_URN_IN_THE_TOP_RIGHT_ROOM,
        AquariaLocationNames.MITHALAS_CATHEDRAL_MITHALAN_DRESS,
        AquariaLocationNames.MITHALAS_CATHEDRAL_URN_BELOW_THE_LEFT_ENTRANCE,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_IN_THE_CENTER_PART,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_FIRST_BULB_IN_THE_TOP_LEFT_PART,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_SECOND_BULB_IN_THE_TOP_LEFT_PART,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_THIRD_BULB_IN_THE_TOP_LEFT_PART,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_CLOSE_TO_THE_SAVE_CRYSTAL,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_IN_THE_BOTTOM_RIGHT_PATH,
        AquariaLocationNames.MITHALAS_BOSS_AREA_BEATING_MITHALAN_GOD,
    ]

    def test_no_progression_mithalas(self) -> None:
        """
            Unit test used to test that no progression items can be put in Mithalas when option enabled
        """
        for location in self.unfillable_locations:
            for item_name in self.world.item_names:
                item = self.get_item_by_name(item_name)
                if item.classification == ItemClassification.progression:
                    self.assertFalse(
                        self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                        "The location \"" + location + "\" can be filled with \"" + item_name + "\"")
                else:
                    self.assertTrue(
                        self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                        "The location \"" + location + "\" cannot be filled with \"" + item_name + "\"")

