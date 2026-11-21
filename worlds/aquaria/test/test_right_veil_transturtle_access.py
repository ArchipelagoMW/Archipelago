"""
Author: Louis M
Date: Sat, 22 Mar 2025 13:23:48 +0000
Description: Unit test used to test accessibility of entrances with and without Veil top right transturtle
"""
from BaseClasses import CollectionState
from . import AquariaTestBase, after_home_water_locations
from ..Items import ItemNames
from ..Locations import AquariaLocationNames
from ..Options import UnconfineHomeWater


class RightVeilTransturtleTest(AquariaTestBase):
    """Unit test used to test accessibility of entrances with and without Right Veil Transturtle"""
    options = {
        "unconfine_home_water": UnconfineHomeWater.option_via_transturtle
    }

    def test_right_veil_transturtle_location(self) -> None:
        """Test entrances that require right veil transturtle"""
        entrances = [
            'Sun Temple left area entrance to The Veil top right area, left of temple',
            'The Veil top right area, left of temple to Sun Temple left area entrance',
            'The Veil top right area, left of temple to The Veil top right area, fish pass left of temple',
            'The Veil top right area, fish pass left of temple to The Veil top right area, left of temple',
            'The Veil top right area, fish pass left of temple to Octopus Cave bottom entrance',
            'Octopus Cave bottom entrance to The Veil top right area, fish pass left of temple',
            'Home Waters, turtle room to The Veil top right area, left of temple'
        ]
        tested_items = [ItemNames.TRANSTURTLE_VEIL_TOP_RIGHT]
        initial_items = [ItemNames.FISH_FORM]
        self.assertAccessWith(entrances, tested_items, initial_items, "Entrance")

