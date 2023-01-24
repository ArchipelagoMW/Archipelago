from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, Option, Range, Choice

# Should this be default on or off?
class AllowJustAsPlannedDLCSongs(Toggle):
    """Whether or not Just as Planned DLC songs, and all the DLCs along with it, will be included in the randomiser.
    Note: The newest DLC songs will most likely not be included in any randomisation."""
    display_name = "Allow Just As Planned DLC Songs"


class StreamerModeEnabled(Toggle):
    """Whether or not the randomisation will take into account Streamer Mode. If enabled, only songs available in Streamer Mode will be randomised."""
    display_name = "Streamer Mode Only Songs"


class StartingSongs(Range):
    """The number of songs that will be automatically unlocked at the start of a run."""
    display_name = "Starting Amout of Songs"
    range_start = 3
    range_end = 10
    default = 5
    display_name = "Starting Song Count"


class AdditionalSongs(Range):
    """The total number of songs that will be placed in the randomisation pool.
    - Does not count any starting songs or the final goal.
    - Final count may be lower due to other settings.
    """
    range_start = 15
    range_end = 400  # Todo: Add song count here
    default = 31
    display_name = "Additional Song Count"


#Todo: Get feedback on these ranges.
class DifficultyMode(Choice):
    """Filters songs based:
    - Easy: At least 1 difficulty between 1-5
    - Medium: At least 1 difficulty between 5-8
    - Hard: At least 1 difficulty between 8+
    - Any: All songs are available"""
    display_name = "Song Difficulty"
    option_Any = 0
    option_Easy = 1
    option_Medium = 2
    option_Hard = 3


class MusicSheetCount(Range):
    """The amount of Music Sheets spread around this seed. Music Sheets are required to unlock the final song."""
    range_start = 1
    range_end = 12
    default = 6
    display_name = "Music Sheet Count"


class MusicSheetWinCount(Range):
    """The number of Music Sheets needed to unlock the winning song."""
    range_start = 1
    range_end = 12
    default = 4
    display_name = "Music Sheets Needed to Win"

class AdditionalItemPercentage(Range):
    """What percentage of songs will have 2 items instead of 1. Starting Songs are always first in line to have extra locations.
    If there are not enough locations to place Music Sheets, extra locations will be added."""
    display_name = "Additional Item %"
    range_start = 0
    default = 33
    range_end = 100

# Options Beyond this point are not Implemented

class RandomisationMode(Choice):
    """The way that MuseDash will be randomised:
    'Albums' - Items will unlock albums. A certain number of songs will need to be completed per Album.
    'Songs' - Items will unlock songs."""
    display_name = "Randomisation Mode"
    option_Albums = 0
    option_Songs = 1


class StartingAlbums(Range):
    """The number of albums that are given at the start.
    Only applicable in 'Album' gamemode."""
    display_name = "Starting Amout of Albums"
    range_start = 1
    range_end = 5  # Todo: Make Sane Maximum
    default = 3
    heading = "Album_Mode"


class AlbumDepth(Range):
    """The number of albums deep the goal will be.
    Only applicable in 'Album' gamemode."""
    display_name = "Minumum Albums To Goal"
    range_start = 3
    range_end = 10
    default = 5


class MinimumDifficulty(Choice):
    """"""
    display_name = "Minimum Song Difficulty"
    option_Easy_Or_Above = 0
    option_hard = "Hard or Above"
    option_expert = "Expert Only"


musedash_options: Dict[str, type(Option)] = {
    "allow_just_as_planned_dlc_songs": AllowJustAsPlannedDLCSongs,
    "streamer_mode_enabled": StreamerModeEnabled,
    "starting_song_count": StartingSongs,
    "additional_song_count": AdditionalSongs,
    "additional_item_percentage": AdditionalItemPercentage,
    "song_difficulty_mode": DifficultyMode,
    "music_sheet_count": MusicSheetCount,
    "music_sheet_win_count": MusicSheetWinCount
}
