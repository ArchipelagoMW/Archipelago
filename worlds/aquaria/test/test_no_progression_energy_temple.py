"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in Energy Temple when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification
from ..Locations import AquariaLocationNames


class NoProgressionEnergyTempleTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in Energy Temple when option enabled"""
    options = {
        "no_progression_energy_temple": True
    }

    unfillable_locations = [
        AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BEATING_THE_ENERGY_STATUE,
        AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BULB_IN_THE_BOTTOM_ROOM_BLOCKED_BY_A_ROCK,
        AquariaLocationNames.ENERGY_TEMPLE_ENERGY_IDOL,
        AquariaLocationNames.ENERGY_TEMPLE_SECOND_AREA_BULB_UNDER_THE_ROCK,
        AquariaLocationNames.ENERGY_TEMPLE_BOTTOM_ENTRANCE_KROTITE_ARMOR,
        AquariaLocationNames.ENERGY_TEMPLE_THIRD_AREA_BULB_IN_THE_BOTTOM_PATH,
        AquariaLocationNames.ENERGY_TEMPLE_BOSS_AREA_FALLEN_GOD_TOOTH,
        AquariaLocationNames.ENERGY_TEMPLE_BLASTER_ROOM_BLASTER_EGG,
    ]

    def test_no_progression_energy_temple(self) -> None:
        """
            Unit test used to test that no progression items can be put in Energy Temple when option enabled
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

