from . import MuseDashTestBase

# The worst case settings are DLC songs off, and enabling streamer mode.
# This ends up with only 25 valid songs that can be chosen.
# These tests ensure that this won't fail generation

class TestWorstCaseHighDifficulty(MuseDashTestBase):
    options = {
        "starting_song_count": 10,
        "allow_just_as_planned_dlc_songs": True,
        "additional_song_count": 500,
    }

    removed_songs = [
        "CHAOS Glitch",
        "FM 17314 SUGAR RADIO"
    ]

    def test_songs_have_difficulty(self) -> None:
        # This test is done on a world where every song should be added.
        muse_dash_world = self.multiworld.worlds[1]

        for song_name in self.removed_songs:
            assert song_name not in muse_dash_world.starting_songs, \
                f"Song '{song_name}' was included into the starting songs when it shouldn't."

            assert song_name not in muse_dash_world.included_songs, \
                f"Song '{song_name}' was included into the included songs when it shouldn't."