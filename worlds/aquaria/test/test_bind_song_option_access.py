"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the bind song (with the location
             under rock needing bind song option)
"""

from . import AquariaTestBase
from .test_bind_song_access import after_home_water_locations
from ..Items import ItemNames
from ..Locations import AquariaLocationNames


class BindSongOptionAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the bind song"""
    options = {
        "bind_song_needed_to_get_under_rock_bulb": True,
    }

    def test_bind_song_location(self) -> None:
        """Test locations that require Bind song with the bind song needed option activated"""
        locations = [
            AquariaLocationNames.VERSE_CAVE_RIGHT_AREA_BIG_SEED,
            AquariaLocationNames.VERSE_CAVE_LEFT_AREA_BULB_UNDER_THE_ROCK_AT_THE_END_OF_THE_PATH,
            AquariaLocationNames.HOME_WATERS_BULB_UNDER_THE_ROCK_IN_THE_LEFT_PATH_FROM_THE_VERSE_CAVE,
            AquariaLocationNames.SONG_CAVE_BULB_UNDER_THE_ROCK_CLOSE_TO_THE_SONG_DOOR,
            AquariaLocationNames.SONG_CAVE_BULB_UNDER_THE_ROCK_IN_THE_PATH_TO_THE_SINGING_STATUES,
            AquariaLocationNames.NAIJA_S_HOME_BULB_UNDER_THE_ROCK_AT_THE_RIGHT_OF_THE_MAIN_PATH,
            AquariaLocationNames.HOME_WATERS_BULB_IN_THE_PATH_BELOW_NAUTILUS_PRIME,
            AquariaLocationNames.HOME_WATERS_BULB_IN_THE_BOTTOM_LEFT_ROOM,
            AquariaLocationNames.HOME_WATERS_NAUTILUS_EGG,
            AquariaLocationNames.SONG_CAVE_VERSE_EGG,
            AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BEATING_THE_ENERGY_STATUE,
            AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BULB_IN_THE_BOTTOM_ROOM_BLOCKED_BY_A_ROCK,
            AquariaLocationNames.ENERGY_TEMPLE_ENERGY_IDOL,
            AquariaLocationNames.ENERGY_TEMPLE_SECOND_AREA_BULB_UNDER_THE_ROCK,
            AquariaLocationNames.ENERGY_TEMPLE_BOTTOM_ENTRANCE_KROTITE_ARMOR,
            AquariaLocationNames.ENERGY_TEMPLE_THIRD_AREA_BULB_IN_THE_BOTTOM_PATH,
            AquariaLocationNames.ENERGY_TEMPLE_BOSS_AREA_FALLEN_GOD_TOOTH,
            AquariaLocationNames.ENERGY_TEMPLE_BLASTER_ROOM_BLASTER_EGG,
            *after_home_water_locations
        ]
        items = [[ItemNames.BIND_SONG]]
        self.assertAccessDependency(locations, items)
