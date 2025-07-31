from . import MuseDashTestBase


class TestPlandoSettings(MuseDashTestBase):
    options = {
        "additional_song_count": 15,
        "dlc_packs": {"Muse Plus"},
        "include_songs": [
            "Lunatic",
            "Out of Sense",
            "Magic Knight Girl",
        ]
    }

    def test_included_songs_didnt_grow_item_count(self) -> None:
        muse_dash_world = self.get_world()
        self.assertEqual(len(muse_dash_world.included_songs), 15, "Logical songs size grew when it shouldn't.")

    def test_included_songs_plando(self) -> None:
        muse_dash_world = self.get_world()
        songs = muse_dash_world.included_songs.copy()
        songs.append(muse_dash_world.victory_song_name)

        self.assertIn("Lunatic", songs, "Logical songs is missing a plando song: Lunatic")
        self.assertIn("Out of Sense", songs, "Logical songs is missing a plando song: Out of Sense")
        self.assertIn("Magic Knight Girl", songs, "Logical songs is missing a plando song: Magic Knight Girl")


class TestFilteredPlandoSettings(MuseDashTestBase):
    options = {
        "additional_song_count": 15,
        "dlc_packs": {"MSR Anthology"},
        "include_songs": [
            "Operation Blade",
            "Autumn Moods",
            "Fireflies",
        ]
    }

    def test_included_songs_didnt_grow_item_count(self) -> None:
        muse_dash_world = self.get_world()
        self.assertEqual(len(muse_dash_world.included_songs), 15, "Logical songs size grew when it shouldn't.")

    # Tests for excluding included songs when the right dlc isn't enabled
    def test_filtered_included_songs_plando(self) -> None:
        muse_dash_world = self.get_world()
        songs = muse_dash_world.included_songs.copy()
        songs.append(muse_dash_world.victory_song_name)

        self.assertIn("Operation Blade", songs, "Logical songs is missing a plando song: Operation Blade")
        self.assertIn("Autumn Moods", songs, "Logical songs is missing a plando song: Autumn Moods")
        self.assertNotIn("Fireflies", songs, "Logical songs has added a filtered a plando song: Fireflies")
