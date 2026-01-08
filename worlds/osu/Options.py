from Options import Toggle, Option, Range, Choice, DeathLink, ItemSet, OptionSet, PerGameCommonOptions
from dataclasses import dataclass
from .Items import get_song_data


class StartingSongs(Range):
    """The number of songs that will be automatically unlocked at the start of a run."""
    range_start = 3
    range_end = 10
    default = 5
    display_name = "Starting Song Count"


class AdditionalSongs(Range):
    """The total number of songs that will be placed in the randomization pool.
    - This does not count any starting songs or the goal song.
    Not all gamemodes have enough songs for the maximum amount on their own.
    """
    range_start = 15
    range_end = 400
    default = 40
    display_name = "Additional Song Count"


class MaximumLength(Range):
    """Maximum Length a Song can be, in seconds.
    """
    range_start = 0
    range_end = 2200
    default = 300
    display_name = "Maximum Length"


class DisableDifficultyReduction(Toggle):
    """Prevents plays using difficulty reduction mods from sending checks."""
    display_name = "Disable Difficulty Reduction"


class DifficultySync(Choice):
    """Changes which difficulties of each beatmapset are able to send checks
    Off - Any difficulty of each Beatmapset will send a check.
    Strict_Any - Only difficulties that fall in your difficulty ranges will send checks
    Strict_Random - A randomly chosen difficulty within your range has to be played. /check will tell you the diff.
    """
    display_name = "Strict Difficulty Sync"
    option_Off = 0
    option_Strict_Any = 1
    option_Strict_Random = 2
    default = 0


class MinimumGrade(Choice):
    """If Enabled, only send checks for plays with a grade above this value.
    If using "CL" mod on Laser, will use Stable's Grading calculation.
    """
    display_name = "Minimum Grade"
    option_Off = 0
    option_SS = 1
    option_S = 2
    option_A = 3
    option_B = 4
    option_C = 5
    default = 0


class DisallowConverts(Toggle):
    """Prevents Converts from sending checks. Reccomended if using strict difficulty Sync."""
    display_name = "Disallow Converts"


class DisableStandard(Toggle):
    """Ignores Standard beatmaps when Generating."""
    display_name = "Exclude Standard"


class StandardMinimumDifficulty(Range):
    """Atleast 1 beatmap of each included Beatmapset will have a difficulty between the Maximum and Minimum for an included Mode.
    Star Ratings are multipled by 100, ie: a Star Rating of 1.23 will be 123.
    Has No Effect if the given mode is Excluded.
    """
    range_start = 0
    range_end = 1000
    default = 0
    display_name = "Standard Minimum Star Rating"


class StandardMaximumDifficulty(Range):
    """Maximum Difficulty for Standard beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 1000
    display_name = "Standard Maximum Star Rating"


class DisableCatch(Toggle):
    """Ignores Catch The Beat beatmaps when Generating."""
    display_name = "Exclude Catch The Beat"


class CatchMinimumDifficulty(Range):
    """Minimum Difficulty for Catch the Beat beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 0
    display_name = "Catch Minimum Star Rating"


class CatchMaximumDifficulty(Range):
    """Maximum Difficulty for Catch the Beat beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 1000
    display_name = "Catch Maximum Star Rating"


class DisableTaiko(Toggle):
    """Ignores Taiko beatmaps when Generating."""
    display_name = "Exclude Taiko"


class TaikoMinimumDifficulty(Range):
    """Minimum Difficulty for Taiko beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 0
    display_name = "Taiko Minimum Star Rating"


class TaikoMaximumDifficulty(Range):
    """Maximum Difficulty for Taiko beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 1000
    display_name = "Taiko Maximum Star Rating"


class Disable4k(Toggle):
    """Ignores 4-Key Mania beatmaps when Generating."""
    display_name = "Exclude 4k"


class FourKeyMinimumDifficulty(Range):
    """Minimum Difficulty for 4-Key Mania beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 0
    display_name = "4-Key Mania Minimum Star Rating"


class FourKeyMaximumDifficulty(Range):
    """Maximum Difficulty for 4-Key Mania beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 1000
    display_name = "4-Key Mania Maximum Star Rating"


class Disable7k(Toggle):
    """Ignores 7-Key Mania beatmaps when Generating."""
    display_name = "Exclude 7k"


class SevenKeyMinimumDifficulty(Range):
    """Minimum Difficulty for 7-Key Mania beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 0
    display_name = "7-Key Mania Minimum Star Rating"


class SevenKeyMaximumDifficulty(Range):
    """Maximum Difficulty for 7-Key Mania beatmaps. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 1000
    display_name = "7-Key Mania Maximum Star Rating"


class DisableMiscKeymodes(Toggle):
    """Ignores Mania beatmaps of Key Counts other than 4 and 7 when Generating."""
    display_name = "Exclude Miscellaneous Key Counts"


class MiscKeyMinimumDifficulty(Range):
    """Minimum Difficulty for beatmaps of Key Counts other than 4 and 7. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 0
    display_name = "Miscellaneous Key Counts Minimum Star Rating"


class MiscKeyMaximumDifficulty(Range):
    """Maximum Difficulty for beatmaps of Key Counts other than 4 and 7. Star Ratings are multipled by 100."""
    range_start = 0
    range_end = 1000
    default = 1000
    display_name = "Miscellaneous Key Counts Maximum Star Rating"


class EnableExplicitLyrics(Toggle):
    """Allows Songs with 18+ Lyrics to generate.
    While this can be played on the main Archipelago Server, Streaming them there is not reccomended."""
    display_name = "Include Explicit Lyrics"


class EnableLoved(Toggle):
    """Allows Loved Beatmaps to Appear when Generating. Not Reccomended with 'Disable Difficulty Reduction' Enabled."""
    display_name = "Enable Loved Beatmaps"


# next few taken pretty much or entirely from Muse Dash
class AdditionalItemPercentage(Range):
    """The percentage of songs that will have 2 items instead of 1 when completing them.
    Starting Songs will always have 2 items.
    Locations will be filled with duplicate songs if there are not enough items.
    """
    display_name = "Additional Item %"
    range_start = 50
    default = 80
    range_end = 100


class PerformancePointsPercentage(Range):
    """Collecting enough 'Performace Points' will unlock the goal song needed for completion.
    This option controls how many are in the item pool, based on the total number of songs.
    The 'Performance Points' in this multiworld are unrelated to your accounts PP Score."""
    range_start = 10
    range_end = 40
    default = 20
    display_name = "Performance Points Percentage"


class PerformancePointsWinCountPercentage(Range):
    """The percentage of Performance Points in the item pool required to unlock the winning song."""
    range_start = 50
    range_end = 100
    default = 80
    display_name = "Percentage of Performace Points Needed"


class ShuffleIncludedSongs(Toggle):
    """Shuffles the songs in "Include Songs" to be randomly placed anywhere in the Rando.
    IF Enabled, included songs can appear as starting or goal songs.
    If Disabled, included songs will be added in ascending order by ID after the starting songs.
    IE: If you have 5 starting songs, the first ID will be song 6, the next will be song 6, etc."""
    display_name = "Shuffle Included Songs"


class IncludeSongs(OptionSet):
    """List of Beatmapset IDs to include, each replacing a Rando song.
    If Shuffle Included songs is disabled, songs can't appear as your starting songs."""
    display_name = "Include Songs"
    valid_keys = {str(beatmapset['id']) for beatmapset in get_song_data()}


class ExcludeSongs(OptionSet):
    """List of Beatmapset IDs to exclude. Listed Beatmapset IDs cannot appear in the Rando.
    """
    display_name = "Exclude Songs"
    valid_keys = {str(beatmapset['id']) for beatmapset in get_song_data()}


@dataclass
class OsuOptions(PerGameCommonOptions):
    starting_songs: StartingSongs
    additional_songs: AdditionalSongs
    additional_item_percentage: AdditionalItemPercentage
    disable_difficulty_reduction: DisableDifficultyReduction
    minimum_grade: MinimumGrade
    difficulty_sync: DifficultySync
    disallow_converts: DisallowConverts
    maximum_length: MaximumLength
    exclude_standard: DisableStandard
    minimum_difficulty_standard: StandardMinimumDifficulty
    maximum_difficulty_standard: StandardMaximumDifficulty
    exclude_catch: DisableCatch
    minimum_difficulty_catch: CatchMinimumDifficulty
    maximum_difficulty_catch: CatchMaximumDifficulty
    exclude_taiko: DisableTaiko
    minimum_difficulty_taiko: TaikoMinimumDifficulty
    maximum_difficulty_taiko: TaikoMaximumDifficulty
    exclude_4k: Disable4k
    minimum_difficulty_4k: FourKeyMinimumDifficulty
    maximum_difficulty_4k: FourKeyMaximumDifficulty
    exclude_7k: Disable7k
    minimum_difficulty_7k: SevenKeyMinimumDifficulty
    maximum_difficulty_7k: SevenKeyMaximumDifficulty
    exclude_other_keys: DisableMiscKeymodes
    minimum_difficulty_other: MiscKeyMinimumDifficulty
    maximum_difficulty_other: MiscKeyMaximumDifficulty
    performance_points_count_percentage: PerformancePointsPercentage
    performance_points_win_count_percentage: PerformancePointsWinCountPercentage
    explicit_lyrics: EnableExplicitLyrics
    enable_loved: EnableLoved
    shuffle_included_songs: ShuffleIncludedSongs
    include_songs: IncludeSongs
    exclude_songs: ExcludeSongs
