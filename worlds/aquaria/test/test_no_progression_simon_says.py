"""
Author: Louis M
Date: Fri, 03 May 2024 14:07:35 +0000
Description: Unit test used to test that no progression items can be put in Simon says when option enabled
"""

from . import AquariaTestBase
from BaseClasses import ItemClassification
from ..Locations import AquariaLocationNames


class NoProgressionSimonSaysTest(AquariaTestBase):
    """Unit test used to test that no progression items can be put in Simon says when option enabled"""
    options = {
        "no_progression_simon_says": True
    }

    unfillable_locations = [
        AquariaLocationNames.SIMON_SAYS_AREA_BEATING_SIMON_SAYS,
        AquariaLocationNames.SIMON_SAYS_AREA_TRANSTURTLE,
    ]

    def test_no_progression_simon_says(self) -> None:
        """
            Unit test used to test that no progression items can be put in Simon says when option enabled
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

