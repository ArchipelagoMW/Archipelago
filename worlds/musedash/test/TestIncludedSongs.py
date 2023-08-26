from . import MuseDashTestBase


class TestIncludedSongs(MuseDashTestBase):
    options = {
        "additional_song_count": 500,
        "allow_just_as_planned_dlc_songs": False,
    }

    def test_free_dlc_included_in_base_songs(self) -> None:
        muse_dash_world = self.multiworld.worlds[1]
        songs = muse_dash_world.included_songs.copy()
        songs.extend(muse_dash_world.starting_songs)
        songs.append(muse_dash_world.victory_song_name)

        assert "Glimmer" in songs, "Budget Is Burning Vol.1 is not being included in base songs"
        assert "Out of Sense" in songs, "Budget Is Burning: Nano Core is not being included in base songs"