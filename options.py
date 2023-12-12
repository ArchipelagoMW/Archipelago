from typing import Dict, Type

from Options import Choice, Option, Toggle, DeathLink, Range


class Difficulty(Choice):
    '''
    The game's difficulty level.
    Hard and S-Hard have slightly less locations to check since some Full Health item boxes are missing on those difficulties.
    '''
    display_name = 'Difficulty'
    option_normal = 0
    option_hard = 1
    option_s_hard = 2
    default = 0


class PoolJewels(Range):
    '''
    Number of jewels in the item pool per passage for the main four.
    The number of pieces will be four times this number.
    '''
    range_start = 0
    range_end = 4
    default = 3
    display_name = 'Jewels in Pool'


class GoldenJewels(Range):
    '''
    Number of copies of the golden pyramid jewel in the item pool.
    '''
    range_start = 0
    range_end = 2
    default = 1
    display_name = 'Golden Pyramid Jewels'


class RequiredJewels(Range):
    '''
    Number of jewels required to fight the bosses.
    The Entry Passage and Golden Pyramid always require 1 unless this option is
    set to 0.
    '''
    range_start = 0
    range_end = 4
    default = 2
    display_name = 'Required Jewels'


class OpenDoors(Choice):
    '''
    Start with all doors in the passages unlocked. This skips the requirement
    to find Keyzer in each level, opening more locations earlier.
    '''
    display_name = 'Open Level Doors'
    option_off = 0
    option_closed_diva = 1
    option_open = 2
    default = option_off


class SmashThroughHardBlocks(Toggle):
    """
    Break hard, teal blocks with the dash attack and super ground pound without stopping,
    as in Pizza Tower and Wario Land: Shake It!
    This option does not affect logic.
    """
    display_name = "Smash Hard Blocks Without Stopping"


class MusicShuffle(Choice):
    '''
    Music shuffle type
    None: Music is not shuffled
    Levels only: Only shuffle music between the main levels
    Levels and extras: Shuffle any music that plays in levels, including the 'Hurry up!' and boss themes
    Full: Shuffle all music
    '''
    display_name = 'Music Shuffle'
    option_none = 0
    option_levels_only = 1
    option_levels_and_extras = 2
    option_full = 3
    default = 0


class WarioVoiceShuffle(Toggle):
    '''
    Randomize the things Wario says.
    '''
    display_name = "Shuffle Wario's voices"


wl4_options: Dict[str, Type[Option]] = {
    'difficulty': Difficulty,
    'pool_jewels': PoolJewels,
    'golden_jewels': GoldenJewels,
    'required_jewels': RequiredJewels,
    'open_doors': OpenDoors,
    'smash_through_hard_blocks': SmashThroughHardBlocks,
    'death_link': DeathLink,
    'music_shuffle': MusicShuffle,
    'wario_voice_shuffle': WarioVoiceShuffle,
}
