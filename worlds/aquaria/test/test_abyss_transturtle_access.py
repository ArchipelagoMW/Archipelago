"""
Author: Louis M
Date: Sat, 22 Mar 2025 13:23:48 +0000
Description: Unit test used to test accessibility of entrances with and without Abyss transturtle
"""
from BaseClasses import CollectionState
from . import AquariaTestBase, after_home_water_locations
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import UnconfineHomeWater


class AbyssTransturtleTest(AquariaTestBase):
    """Unit test used to test accessibility of entrances with and without Abyss Transturtle"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_transturtle
    }

    def test_abyss_transturtle_location(self) -> None:
        """Test entrances that require Abyss transturtle"""
        entrances = [
            'Abyss right area, transturtle'
        ]
        tested_items = [ItemNames.TRANSTURTLE_ABYSS]
        self.assertAccessWith(entrances, tested_items, resolution_hint="Region")

