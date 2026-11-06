"""
Author: Louis M
Date: Sat, 22 Mar 2025 13:23:48 +0000
Description: Unit test used to test accessibility of entrances with and without Simon Says transturtle
"""
from BaseClasses import CollectionState
from . import AquariaTestBase, after_home_water_locations
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import UnconfineHomeWater


class SimonSaysTransturtleTest(AquariaTestBase):
    """Unit test used to test accessibility of entrances with and without Simon Says Transturtle"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_transturtle
    }

    def test_simon_says_transturtle_location(self) -> None:
        """Test entrances that require Simon Says transturtle"""
        entrances = [
            AquariaLocationNames.SIMON_SAYS_AREA_TRANSTURTLE,
            AquariaLocationNames.SIMON_SAYS_AREA_BEATING_SIMON_SAYS
        ]
        tested_items = [ItemNames.TRANSTURTLE_SIMON_SAYS]
        self.assertAccessWith(entrances, tested_items)

