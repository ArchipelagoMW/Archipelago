"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in Frozen Veil when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification
from ..Locations import AquariaLocationNames


class NoProgressionFrozenVeilTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in Frozen Veil when option enabled"""
    options = {
        "no_progression_frozen_veil": True
    }

    unfillable_locations = [
        AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_ROOM_TO_THE_RIGHT,
        AquariaLocationNames.ICE_CAVERN_FIRST_BULB_IN_THE_TOP_EXIT_ROOM,
        AquariaLocationNames.ICE_CAVERN_SECOND_BULB_IN_THE_TOP_EXIT_ROOM,
        AquariaLocationNames.ICE_CAVERN_THIRD_BULB_IN_THE_TOP_EXIT_ROOM,
        AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_LEFT_ROOM,
        AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL,
        AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL,
        AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG,
    ]

    def test_no_progression_frozen_veil(self) -> None:
        """
            Unit test used to test that no progression items can be put in Frozen Veil when option enabled
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

