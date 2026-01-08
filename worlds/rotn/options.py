from Options import Toggle, Range, Choice, ItemSet, OptionSet, PerGameCommonOptions, OptionGroup
from dataclasses import dataclass
from .RiftCollections import RotNCollections

class DLCMusicPacks(OptionSet):
    """
    Choose which DLC Packs will be included in the pool of chooseable songs.
    Both individual songs and dlc pack names work.

    Current DLC Pack Groups: ["Celeste", "Pizza Tower", "Hatsune Miku", "Hololive", "Everhood", "Monstercat", "Shovel Knight", "Friday Night Funkin'"]
    """
    display_name = "DLC Packs"
    valid_keys = [dlc for dlc in RotNCollections.DLC]

class StartingSongs(Range):
    """The number of songs that will be unlocked from the start"""
    range_start = 3
    range_end = 10
    default = 5
    display_name = "Starting Song Count"

class AdditionalSongs(Range):
    """The total number of songs that will be placed in the randomization pool.
    - This does not count any starting songs or the goal song.
    - The final song count may be lower due to other settings.
    """
    range_start = 15
    range_end = 2000
    default = 30
    display_name = "Additional Song Count"

class DuplicateSongPercentage(Range):
    """
    Percentage of duplicate songs to place in remaining filler slots.
    Duplicate songs are considered Useful and thus out of logic.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Duplicate Song Percentage"

class IncludeRemixMode(Toggle):
    """
    Adds remix mode songs as separate items and locations. When off, both normal and remix mode unlocks are the same. 
    """
    display_name = "Include Remix Mode"

class IncludeMinigames(Choice):
    """
    Adds minigames to the song pool.
    Split allows medium and hard variants to be shuffled separately.
    """
    display_name = "Include Minigames"
    option_false = 0
    option_true = 1
    option_Split = 2

class IncludeBossBattles(Choice):
    """
    Add boss battles to the song pool
    Split allows medium and hard variants to be shuffled separately.
    """
    display_name = "Include Boss Battles"
    option_false = 0
    option_true = 1
    option_Split = 2

class DifficultyOption(OptionSet):
    """
    Determines what difficulties to be selected for song filtering (Rhythm Rifts only)
    This setting will not force you to play on any of the selected difficulties and intened to be used with the following intensity settings
    """
    display_name = "Difficulty Selection"
    default = ["Easy", "Medium", "Hard", "Impossible"]
    valid_keys = ["Easy", "Medium", "Hard", "Impossible"]

class MinIntensity(Range):
    """ 
    Ensures chosen rhythm rift will have a chart with an intensity value higher than this value (Rhythm Rifts only)
    """
    range_start = 1
    range_end = 40
    default = 1
    display_name = "Minimum Intensity"

class MaxIntensity(Range):
    """
    Ensures chosen rhythm rift will have a chart with an intensity value lower than this value (Rhythm Rifts only)
    """
    range_start = 1
    range_end = 40
    default = 30
    display_name = "Maximum Intensity"

class GradeNeeded(Choice):
    """
    Minimum Grade required on song completion to send a check
    """
    display_name = "Grade Needed"
    option_Any = 0
    option_C = 1
    option_B = 2
    option_A = 3
    option_S = 4
    option_S_Plus = 5
    default = 0
    
class FullComboNeeded(Toggle):
    """
    Requires a full combo on song completion to send a check
    """
    display_name = "Full Combo Needed"
    default = False

class DiamondCountPercentage(Range):
    """Percentage of filler item to be replaced with diamonds."""
    range_start = 50
    range_end = 100
    default = 80
    display_name = "Diamond Percentage"

class DiamondWinPercentage(Range):
    """The percentage of diamonds in the item pool that are needed to unlock the winning song."""
    range_start = 50
    range_end = 100
    default = 80
    display_name = "Diamonds Needed to Win"

class IncludeSongs(ItemSet):
    """
    These songs will be guaranteed to show up within the seed.
    - You must have the DLC enabled to play those songs.
    - Difficulty options will not affect these songs.
    - If there are too many included songs, this will act as a whitelist ignoring song difficulty.
    """
    verify_item_name = True
    display_name = "Include Songs"


class ExcludeSongs(ItemSet):
    """
    These songs will be guaranteed to not show up within the seed.
    
    Note: Does not affect songs within the "Include Songs" list.
    """
    verify_item_name = True
    display_name = "Exclude Songs"

class GoalSongPool(ItemSet):
    """Songs listed here will randomly chosen to be the final song.
    If empty, the goal song will be chosen randomly from all included songs."""
    verify_item_name = True
    display_name = "Goal Song Pool"

rotn_option_groups = [
    OptionGroup("Song Pool Settings", [
        DLCMusicPacks,
        IncludeRemixMode,
        IncludeBossBattles,
        IncludeMinigames,
        IncludeSongs,
        ExcludeSongs,
        GoalSongPool,
    ]),
    OptionGroup("Difficulty Settings", [
        DifficultyOption,
        MinIntensity,
        MaxIntensity,
        GradeNeeded,
        FullComboNeeded,
    ]),
]

@dataclass
class RotNOptions(PerGameCommonOptions):
    dlc_songs: DLCMusicPacks
    starting_song_count: StartingSongs
    additional_song_count: AdditionalSongs
    duplicate_song_percentage: DuplicateSongPercentage
    include_remix: IncludeRemixMode
    include_minigames: IncludeMinigames
    include_boss_battle: IncludeBossBattles
    difficulty_option: DifficultyOption
    min_intensity: MinIntensity
    max_intensity: MaxIntensity
    grade_needed: GradeNeeded
    full_combo_needed: FullComboNeeded
    diamond_count_percentage: DiamondCountPercentage
    diamond_win_percentage: DiamondWinPercentage
    include_songs: IncludeSongs
    exclude_songs: ExcludeSongs
    goal_song_pool: GoalSongPool