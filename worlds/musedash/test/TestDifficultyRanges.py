from . import MuseDashTestBase


class DifficultyRanges(MuseDashTestBase):
    def test_all_difficulty_ranges(self) -> None:
        muse_dash_world = self.multiworld.worlds[1]
        dlc_set = {x for x in muse_dash_world.md_collection.DLC}
        difficulty_choice = self.multiworld.song_difficulty_mode[1]
        difficulty_min = self.multiworld.song_difficulty_min[1]
        difficulty_max = self.multiworld.song_difficulty_max[1]

        def test_range(inputRange, lower, upper):
            self.assertEqual(inputRange[0], lower)
            self.assertEqual(inputRange[1], upper)

            songs = muse_dash_world.md_collection.get_songs_with_settings(dlc_set, False, inputRange[0], inputRange[1])
            for songKey in songs:
                song = muse_dash_world.md_collection.song_items[songKey]
                if (song.easy is not None and inputRange[0] <= song.easy <= inputRange[1]):
                    continue

                if (song.hard is not None and inputRange[0] <= song.hard <= inputRange[1]):
                    continue

                if (song.master is not None and inputRange[0] <= song.master <= inputRange[1]):
                    continue

                self.fail(f"Invalid song '{songKey}' was given for range '{inputRange[0]} to {inputRange[1]}'")

        #auto ranges
        difficulty_choice.value = 0
        test_range(muse_dash_world.get_difficulty_range(), 0, 12)
        difficulty_choice.value = 1
        test_range(muse_dash_world.get_difficulty_range(), 0, 3)
        difficulty_choice.value = 2
        test_range(muse_dash_world.get_difficulty_range(), 4, 5)
        difficulty_choice.value = 3
        test_range(muse_dash_world.get_difficulty_range(), 6, 7)
        difficulty_choice.value = 4
        test_range(muse_dash_world.get_difficulty_range(), 8, 9)
        difficulty_choice.value = 5
        test_range(muse_dash_world.get_difficulty_range(), 10, 12)

        # Test the Manual ranges
        difficulty_choice.value = 6

        difficulty_min.value = 1
        difficulty_max.value = 11
        test_range(muse_dash_world.get_difficulty_range(), 1, 11)

        difficulty_min.value = 1
        difficulty_max.value = 1
        test_range(muse_dash_world.get_difficulty_range(), 1, 1)

        difficulty_min.value = 11
        difficulty_max.value = 11
        test_range(muse_dash_world.get_difficulty_range(), 11, 11)

        difficulty_min.value = 4
        difficulty_max.value = 6
        test_range(muse_dash_world.get_difficulty_range(), 4, 6)

    def test_songs_have_difficulty(self) -> None:
        muse_dash_world = self.multiworld.worlds[1]

        for song_name in muse_dash_world.md_collection.DIFF_OVERRIDES:
            song = muse_dash_world.md_collection.song_items[song_name]

            self.assertTrue(song.easy is not None and song.hard is not None and song.master is not None,
                f"Song '{song_name}' difficulty not set when it should be.")
