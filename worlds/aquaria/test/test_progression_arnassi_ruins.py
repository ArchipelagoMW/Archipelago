"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that progression items can be put in Arnassi Ruins area when option enabled
"""

from . import AquariaTestBase
from ..Locations import AquariaLocationNames


class ProgressionArnassiRuinsTest(AquariaTestBase):
    """Unit test used to test that progression items can be put in Arnassi Ruins area when option enabled"""
    options = {
        "no_progression_arnassi_ruins": False
    }

    unfillable_locations = [
        AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_RIGHT_PART,
        AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_LEFT_PART,
        AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_CENTER_PART,
        AquariaLocationNames.ARNASSI_RUINS_SONG_PLANT_SPORE,
        AquariaLocationNames.ARNASSI_RUINS_ARNASSI_ARMOR,
        AquariaLocationNames.ARNASSI_RUINS_ARNASSI_STATUE,
        AquariaLocationNames.ARNASSI_RUINS_TRANSTURTLE,
        AquariaLocationNames.ARNASSI_RUINS_CRAB_ARMOR,
    ]

    def test_progression_arnassi_ruins(self) -> None:
        """
            Unit test used to test that progression items can be put in Arnassi Ruins area when option enabled
        """
        for location in self.unfillable_locations:
            for item_name in self.world.item_names:
                item = self.get_item_by_name(item_name)
                self.assertTrue(
                    self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                    "The location \"" + location + "\" cannot be filled with \"" + item_name + "\"")