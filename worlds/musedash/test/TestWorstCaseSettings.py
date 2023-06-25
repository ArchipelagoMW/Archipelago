from . import MuseDashTestBase

# The worst case settings are DLC songs off, and enabling streamer mode.
# This ends up with only 25 valid songs that can be chosen.
# These tests ensure that this won't fail generation

class TestWorstCaseHighDifficulty(MuseDashTestBase):
    options = {
        "starting_song_count": 10,
        "allow_just_as_planned_dlc_songs": False,
        "streamer_mode_enabled": True,
        "song_difficulty_mode": 6,
        "song_difficulty_min": 11,
        "song_difficulty_max": 11,
    }

class TestWorstCaseMidDifficulty(MuseDashTestBase):
    options = {
        "starting_song_count": 10,
        "allow_just_as_planned_dlc_songs": False,
        "streamer_mode_enabled": True,
        "song_difficulty_mode": 6,
        "song_difficulty_min": 6,
        "song_difficulty_max": 6,
    }

class TestWorstCaseLowDifficulty(MuseDashTestBase):
    options = {
        "starting_song_count": 10,
        "allow_just_as_planned_dlc_songs": False,
        "streamer_mode_enabled": True,
        "song_difficulty_mode": 6,
        "song_difficulty_min": 1,
        "song_difficulty_max": 1,
    }
