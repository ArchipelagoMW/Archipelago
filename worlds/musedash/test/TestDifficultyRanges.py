from . import MuseDashTestBase
from typing import List


class DifficultyRanges(MuseDashTestBase):
    DIFF_OVERRIDES: List[str] = [
        "MuseDash ka nanika hi",
        "Rush-Hour",
        "Find this Month's Featured Playlist",
        "PeroPero in the Universe",
        "umpopoff",
        "P E R O P E R O Brother Dance",
    ]

    def test_all_difficulty_ranges(self) -> None:
        muse_dash_world = self.get_world()
        dlc_set = {x for x in muse_dash_world.md_collection.DLC}
        difficulty_choice = muse_dash_world.options.song_difficulty_mode
        difficulty_min = muse_dash_world.options.song_difficulty_min
        difficulty_max = muse_dash_world.options.song_difficulty_max

        def test_range(input_range, lower, upper):
            self.assertEqual(input_range[0], lower)
            self.assertEqual(input_range[1], upper)

            songs = muse_dash_world.md_collection.get_songs_with_settings(dlc_set, False, input_range[0], input_range[1])
            for songKey in songs:
                song = muse_dash_world.md_collection.song_items[songKey]
                if song.easy is not None and input_range[0] <= song.easy <= input_range[1]:
                    continue

                if song.hard is not None and input_range[0] <= song.hard <= input_range[1]:
                    continue

                if song.master is not None and input_range[0] <= song.master <= input_range[1]:
                    continue

                self.fail(f"Invalid song '{songKey}' was given for range '{input_range[0]} to {input_range[1]}'")

        # auto ranges
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
        muse_dash_world = self.get_world()

        for song_name in self.DIFF_OVERRIDES:
            song = muse_dash_world.md_collection.song_items[song_name]

            # Some songs are weird and have less than the usual 3 difficulties.
            # So this override is to avoid failing on these songs.
            if song_name in ("umpopoff", "P E R O P E R O Brother Dance"):
                self.assertTrue(song.easy is None and song.hard is not None and song.master is None,
                                f"Song '{song_name}' difficulty not set when it should be.")
            else:
                self.assertTrue(song.easy is not None and song.hard is not None and song.master is not None,
                                f"Song '{song_name}' difficulty not set when it should be.")
