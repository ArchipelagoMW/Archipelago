"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the bind song (with the location
             under rock needing bind song option)
"""

from worlds.aquaria.test import AquariaTestBase
from worlds.aquaria.test.test_bind_song_access import after_home_water_locations


class BindSongOptionAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the bind song"""
    options = {
        "bind_song_needed_to_get_under_rock_bulb": True,
    }

    def test_bind_song_location(self) -> None:
        """Test locations that require Bind song with the bind song needed option activated"""
        locations = [
            "Verse cave right area, Big Seed",
            "Verse cave left area, bulb under the rock at the end of the path",
            "Home water, bulb under the rock in the left path from the verse cave",
            "Song cave, bulb under the rock close to the song door",
            "Song cave, bulb under the rock in the path to the singing statues",
            "Naija's home, bulb under the rock at the right of the main path",
            "Home water, bulb in the path below Nautilus Prime",
            "Home water, bulb in the bottom left room",
            "Home water, Nautilus Egg",
            "Song cave, Verse egg",
            "Energy temple first area, beating the energy statue",
            "Energy temple first area, bulb in the bottom room blocked by a rock",
            "Energy temple first area, Energy Idol",
            "Energy temple second area, bulb under the rock",
            "Energy temple bottom entrance, Krotite armor",
            "Energy temple third area, bulb in the bottom path",
            "Energy temple boss area, Fallen god tooth",
            "Energy temple blaster room, Blaster egg",
            *after_home_water_locations
        ]
        items = [["Bind song"]]
        self.assertAccessDependency(locations, items)
