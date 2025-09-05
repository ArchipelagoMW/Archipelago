"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the fish form
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import TurtleRandomizer


class FishFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the fish form"""
    options = {
        "turtle_randomizer": TurtleRandomizer.option_all,
    }

    def test_fish_form_location(self) -> None:
        """Test locations that require fish form"""
        locations = [
            AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_INSIDE_THE_FISH_PASS,
            AquariaLocationNames.ENERGY_TEMPLE_ENERGY_IDOL,
            AquariaLocationNames.MITHALAS_CITY_DOLL,
            AquariaLocationNames.MITHALAS_CITY_URN_INSIDE_A_HOME_FISH_PASS,
            AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_TOP_FISH_PASS,
            AquariaLocationNames.THE_VEIL_BOTTOM_AREA_VERSE_EGG,
            AquariaLocationNames.OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_INSIDE_THE_LOWEST_FISH_PASS,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_CLOSE_TO_THE_VERSE_EGG,
            AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_VERSE_EGG,
            AquariaLocationNames.MERMOG_CAVE_BULB_IN_THE_LEFT_PART_OF_THE_CAVE,
            AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG,
            AquariaLocationNames.BEATING_MERGOG,
            AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
            AquariaLocationNames.OCTOPUS_CAVE_BULB_IN_THE_PATH_BELOW_THE_OCTOPUS_CAVE_PATH,
            AquariaLocationNames.BEATING_OCTOPUS_PRIME,
            AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_BOTTOM_FISH_PASS
        ]
        items = [[ItemNames.FISH_FORM]]
        self.assertAccessDependency(locations, items)
