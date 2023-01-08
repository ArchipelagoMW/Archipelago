from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, Option, Range, Choice

# Should this be default on or off?
class AllowJustAsPlannedDLCSongs(Toggle):
    """Whether or not Just as Planned DLC songs, and all the DLCs along with it, will be included in the randomiser.
    Note: The newest DLC songs will most likely not be included in any randomisation."""
    display_name = "Allow Just As Planned DLC Songs"

class StartingSongs(Range):
    """The number of songs that will be automatically unlocked at the start of a run."""
    display_name = "Starting Amout of Songs"
    range_start = 3
    range_end = 10
    default = 5
    display_name = "Starting Song Count"


class AdditionalSongs(Range):
    """The total number of songs that will be placed in the randomisation pool.
    Does not count any starting songs or the final goal.
    //Todo: Correct length suggestions
    Game Length Suggestions:
    - Short (1-2 hours): 40
    - Long (4 hours): 80
    """
    range_start = 20
    range_end = 400  # Todo: Add song count here
    default = 40
    display_name = "Additional Song Count"


class AdditionalItemsAreSongs(DefaultOnToggle):
    """2 Extra items are added to the pool per Song that is unlocked at the start. Turning this one means these items will be songs."""
    display_name = "Additional Items Are Songs"

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


class SongThreshold(Range):
    """The maximum difficulty of song which would be allowed to be a part of the main route."""
    display_name = "Song Threshold"
    range_start = 1
    range_end = 13  # Is there anything over this?
    default = 11


musedash_options: Dict[str, type(Option)] = {
    "allow_just_as_planned_dlc_songs": AllowJustAsPlannedDLCSongs,
    "starting_song_count": StartingSongs,
    "additional_song_count": AdditionalSongs,
    "extra_items_are_songs": AdditionalItemsAreSongs,
}
