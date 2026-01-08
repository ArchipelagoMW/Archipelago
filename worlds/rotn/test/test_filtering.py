from . import RotNTestBase
from typing import List

class DifficultyRanges(RotNTestBase):
    def test_all_difficulty_ranges(self) -> None:
        rotn_world = self.get_world()
        dlc_set = {x for x in rotn_world.rift_collection.DLC}
        intensity_min = rotn_world.options.min_intensity
        intensity_max = rotn_world.options.max_intensity
        difficulty = rotn_world.options.difficulty_option

        def test_range(lower, upper, diff):

            songs = rotn_world.rift_collection.getSongsWithSettings(dlc_set, False, lower, upper)
            for songKey in songs:
                song = rotn_world.rift_collection.song_items[songKey]
                if song.diff_easy is -1 and "Easy" in diff and upper <= song.diff_easy <= upper:
                    continue

                if song.diff_medium is -1 and "Medium" in diff and upper <= song.diff_medium <= upper:
                    continue

                if song.diff_hard is -1 and "Hard" in diff and upper <= song.diff_hard <= upper:
                    continue

                if song.diff_impossible is -1 and "Impossible" in diff and upper <= song.diff_impossible <= upper:
                    continue

                self.fail(f"Invalid song '{songKey}' was given for range '{upper} to {upper}' with difficulties '{diff}'")

        # Test the ranges
        intensity_min.value = 1
        intensity_max.value = 40
        difficulty.value = ["Easy", "Medium", "Hard", "Impossible"]
        test_range(1, 40, ["Easy", "Medium", "Hard", "Impossible"])

        intensity_min.value = 1
        intensity_max.value = 1
        difficulty.value = ["Easy"]
        test_range(1, 1)

        intensity_min.value = 30
        intensity_max.value = 30
        test_range(30, 30, ["Impossible"])

        intensity_min.value = 4
        intensity_max.value = 12
        test_range(4, 12, ["Medium", "Hard"])