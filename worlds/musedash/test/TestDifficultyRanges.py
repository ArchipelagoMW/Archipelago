import unittest
import logging

from . import MuseDashTestBase

class DifficultyRanges(MuseDashTestBase):
    def test_all_difficulty_ranges(self) -> None:
        museDashWorld = self.multiworld.worlds[1]
        difficultyChoice = self.multiworld.song_difficulty_mode[1]
        difficultyMin = self.multiworld.song_difficulty_min[1]
        difficultyMax = self.multiworld.song_difficulty_max[1]

        def test_range(inputRange, lower, upper):
            assert inputRange[0] == lower and inputRange[1] == upper, f"Output incorrect. Got: {inputRange[0]} to {inputRange[1]}. Expected: {lower} to {upper}"
            songs = museDashWorld.museDashCollection.get_all_songs_with_settings(True, False, inputRange[0], inputRange[1])

            for songKey in songs:
                song = museDashWorld.museDashCollection.SongItems[songKey]
                if (song.easy is not None and inputRange[0] <= song.easy <= inputRange[1]):
                    continue

                if (song.hard is not None and inputRange[0] <= song.hard <= inputRange[1]):
                    continue

                if (song.master is not None and inputRange[0] <= song.master <= inputRange[1]):
                    continue

                assert False, f"Invalid song '{songKey}' was given for range '{inputRange[0]} to {inputRange[1]}'"

        #auto ranges
        difficultyChoice.value = 0
        test_range(museDashWorld.get_difficulty_range(), 1, 12)
        difficultyChoice.value = 1
        test_range(museDashWorld.get_difficulty_range(), 1, 3)
        difficultyChoice.value = 2
        test_range(museDashWorld.get_difficulty_range(), 4, 5)
        difficultyChoice.value = 3
        test_range(museDashWorld.get_difficulty_range(), 6, 7)
        difficultyChoice.value = 4
        test_range(museDashWorld.get_difficulty_range(), 8, 9)
        difficultyChoice.value = 5
        test_range(museDashWorld.get_difficulty_range(), 10, 12)

        #manual ranges
        difficultyChoice.value = 6

        difficultyMin.value = 1
        difficultyMax.value = 11
        test_range(museDashWorld.get_difficulty_range(), 1, 11)

        difficultyMin.value = 1
        difficultyMax.value = 1
        test_range(museDashWorld.get_difficulty_range(), 1, 1)

        difficultyMin.value = 11
        difficultyMax.value = 11
        test_range(museDashWorld.get_difficulty_range(), 11, 11)

        difficultyMin.value = 4
        difficultyMax.value = 6
        test_range(museDashWorld.get_difficulty_range(), 4, 6)
