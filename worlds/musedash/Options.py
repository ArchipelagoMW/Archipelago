from Options import Toggle, Range, Choice, DeathLink, OptionSet, PerGameCommonOptions, OptionGroup, Removed
from dataclasses import dataclass

from .MuseDashCollection import MuseDashCollections
from .MuseDashData import SONG_DATA


class DLCMusicPacks(OptionSet):
    """
    Choose which DLC Packs will be included in the pool of chooseable songs.

    Note: The [Just As Planned] DLC contains all [Muse Plus] songs.
    """
    display_name = "DLC Packs"
    valid_keys = [dlc for dlc in MuseDashCollections.DLC]


class StreamerModeEnabled(Toggle):
    """
    In Muse Dash, an option named 'Streamer Mode' removes songs which may trigger copyright issues when streaming.

    If this is enabled, only songs available under Streamer Mode will be available for randomization.
    """
    display_name = "Streamer Mode Only Songs"


class StartingSongs(Range):
    """The number of songs that will be automatically unlocked at the start of a run."""
    range_start = 3
    range_end = 10
    default = 5
    display_name = "Starting Song Count"


class AdditionalSongs(Range):
    """
    The total number of songs that will be placed in the randomization pool.
    - This does not count any starting songs or the goal song.
    - The final song count may be lower due to other settings.
    """
    range_start = 15
    range_end = 600  # Note will probably not reach this high if any other settings are done.
    default = 40
    display_name = "Additional Song Count"


class DifficultyMode(Choice):
    """
    Ensures that at any chosen song has at least 1 value falling within these values.
    - Any: All songs are available
    - Easy: 1, 2 or 3
    - Medium: 4, 5
    - Hard: 6, 7
    - Expert: 8, 9
    - Master: 10+
    - Manual: Uses the provided minimum and maximum range.
    """
    display_name = "Song Difficulty"
    option_Any = 0
    option_Easy = 1
    option_Medium = 2
    option_Hard = 3
    option_Expert = 4
    option_Master = 5
    option_Manual = 6
    default = 0


# Todo: Investigate options to make this non randomizable
class DifficultyModeOverrideMin(Range):
    """
    Ensures that 1 difficulty has at least 1 this value or higher per song.

    Note: Difficulty Mode must be set to Manual.
    """
    display_name = "Manual Difficulty Min"
    range_start = 1
    range_end = 11
    default = 4


# Todo: Investigate options to make this non randomizable
class DifficultyModeOverrideMax(Range):
    """
    Ensures that 1 difficulty has at least 1 this value or lower per song.

    Note: Difficulty Mode must be set to Manual.
    """
    display_name = "Manual Difficulty Max"
    range_start = 1
    range_end = 11
    default = 8


class GradeNeeded(Choice):
    """
    Completing a song will require a grade of this value or higher in order to unlock items.
    The grades are as follows:
    - Silver S (SS): >= 95% accuracy
    - Pink S (S): >= 90% accuracy
    - A: >= 80% or a Full Combo
    - B: >= 70%
    - C: >= 60%
    """
    display_name = "Grade Needed"
    option_Any = 0
    option_C = 1
    option_B = 2
    option_A = 3
    option_PinkS = 4
    option_SilverS = 5
    default = 0


class MusicSheetCountPercentage(Range):
    """
    Controls how many music sheets are added to the pool based on the number of songs, including starting songs.

    Higher numbers leads to more consistent game lengths, but will cause individual music sheets to be less important.
    """
    range_start = 10
    range_end = 40
    default = 20
    display_name = "Music Sheet Percentage"


class MusicSheetWinCountPercentage(Range):
    """The percentage of Music Sheets in the item pool that are needed to unlock the winning song."""
    range_start = 50
    range_end = 100
    default = 80
    display_name = "Music Sheets Needed to Win"


class ChosenTraps(OptionSet):
    """
    This controls the types of traps that can be added to the pool.
    - Traps last the length of a song, or until you die.
    - VFX Traps consist of visual effects that play over the song. (i.e. Grayscale.)
    - SFX Traps consist of changing your sfx setting to one possibly more annoying sfx.

    Note: SFX traps are only available if [Just as Planned] DLC songs are enabled.
    """
    display_name = "Chosen Traps"
    valid_keys = {trap for trap in MuseDashCollections.trap_items.keys()}


class TrapCountPercentage(Range):
    """This controls how many traps to add into the pool, based the total number of songs."""
    range_start = 0
    range_end = 35
    default = 15
    display_name = "Trap Percentage"


class SongSet(OptionSet):
    valid_keys = SONG_DATA.keys()


class IncludeSongs(SongSet):
    """
    These songs will be guaranteed to show up within the seed.
    - You must have the DLC enabled to play these songs.
    - Difficulty options will not affect these songs.
    - If there are too many included songs, this will act as a whitelist ignoring song difficulty.
    """
    display_name = "Include Songs"


class ExcludeSongs(SongSet):
    """
    These songs will be guaranteed to not show up within the seed.

    Note: Does not affect songs within the "Include Songs" list.
    """
    display_name = "Exclude Songs"


md_option_groups = [
    OptionGroup("Song Choice", [
        DLCMusicPacks,
        StreamerModeEnabled,
        IncludeSongs,
        ExcludeSongs,
    ]),
    OptionGroup("Difficulty", [
        GradeNeeded,
        DifficultyMode,
        DifficultyModeOverrideMin,
        DifficultyModeOverrideMax,
        DeathLink,
    ]),
    OptionGroup("Traps", [
        ChosenTraps,
        TrapCountPercentage,
    ]),
]


@dataclass
class MuseDashOptions(PerGameCommonOptions):
    dlc_packs: DLCMusicPacks
    streamer_mode_enabled: StreamerModeEnabled
    starting_song_count: StartingSongs
    additional_song_count: AdditionalSongs
    song_difficulty_mode: DifficultyMode
    song_difficulty_min: DifficultyModeOverrideMin
    song_difficulty_max: DifficultyModeOverrideMax
    grade_needed: GradeNeeded
    music_sheet_count_percentage: MusicSheetCountPercentage
    music_sheet_win_count_percentage: MusicSheetWinCountPercentage
    chosen_traps: ChosenTraps
    trap_count_percentage: TrapCountPercentage
    death_link: DeathLink
    include_songs: IncludeSongs
    exclude_songs: ExcludeSongs

    # Removed
    allow_just_as_planned_dlc_songs: Removed
    available_trap_types: Removed
