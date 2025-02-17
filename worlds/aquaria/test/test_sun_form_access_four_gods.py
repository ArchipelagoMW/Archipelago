"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the sun form with the goal four gods
"""

from . import AquariaTestBase
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import UnconfineHomeWater, Objective


class SunFormFourGodsAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the sun form with the goal four gods"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_energy_door,
        "objective": Objective.option_killing_the_four_gods
    }


    def test_sun_form_location(self) -> None:
        """Test locations that require sun form with the goal four gods"""
        locations = [
            AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG,
            AquariaLocationNames.BEATING_OCTOPUS_PRIME,
            AquariaLocationNames.BEATING_THE_GOLEM,
            AquariaLocationNames.SUNKEN_CITY_CLEARED
        ]
        items = [[ItemNames.SUN_FORM]]
        self.assertAccessDependency(locations, items, True)
