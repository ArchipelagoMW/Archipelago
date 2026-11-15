"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that progression items can be put in Mithalas area when option enabled
"""

from . import AquariaTestBase
from ..Locations import AquariaLocationNames


class ProgressionMithalasTest(AquariaTestBase):
    """Unit test used to test that progression items can be put in Mithalas area when option enabled"""
    options = {
        "no_progression_mithalas": False
    }

    unfillable_locations = [
        AquariaLocationNames.SIMON_SAYS_AREA_BEATING_SIMON_SAYS,
        AquariaLocationNames.SIMON_SAYS_AREA_TRANSTURTLE,
    ]

    def test_progression_mithalas(self) -> None:
        """
            Unit test used to test that progression items can be put in Mithalas area when option enabled
        """
        for location in self.unfillable_locations:
            for item_name in self.world.item_names:
                item = self.get_item_by_name(item_name)
                self.assertTrue(
                    self.world.get_location(location).can_fill(self.multiworld.state, item, False),
                    "The location \"" + location + "\" cannot be filled with \"" + item_name + "\"")