"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the bind song (with the location
             under rock needing bind song option)
"""

from . import AquariaTestBase
from .test_bind_song_access import after_home_water_locations


class BindSongOptionAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the bind song"""
    options = {
        "bind_song_needed_to_get_under_rock_bulb": True,
    }

    def test_bind_song_location(self) -> None:
        """Test locations that require Bind song with the bind song needed option activated"""
        locations = [
            "Verse Cave right area, Big Seed",
            "Verse Cave left area, bulb under the rock at the end of the path",
            "Home Water, bulb under the rock in the left path from the Verse Cave",
            "Song Cave, bulb under the rock close to the song door",
            "Song Cave, bulb under the rock in the path to the singing statues",
            "Naija's Home, bulb under the rock at the right of the main path",
            "Home Water, bulb in the path below Nautilus Prime",
            "Home Water, bulb in the bottom left room",
            "Home Water, Nautilus Egg",
            "Song Cave, Verse Egg",
            "Energy Temple first area, beating the Energy Statue",
            "Energy Temple first area, bulb in the bottom room blocked by a rock",
            "Energy Temple first area, Energy Idol",
            "Energy Temple second area, bulb under the rock",
            "Energy Temple bottom entrance, Krotite Armor",
            "Energy Temple third area, bulb in the bottom path",
            "Energy Temple boss area, Fallen God Tooth",
            "Energy Temple blaster room, Blaster Egg",
            *after_home_water_locations
        ]
        items = [["Bind song"]]
        self.assertAccessDependency(locations, items)
