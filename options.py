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


class RequiredJewels(Range):
    '''
    Number of jewels required to fight the bosses.
    The Entry Passage and Golden Pyramid always require 1 unless this option is
    set to 0.
    '''
    range_start = 0
    range_end = 4
    default = 3
    display_name = 'Required Jewels'


class OpenDoors(Toggle):
    '''
    Start with all doors in the passages unlocked. This skips the requirement
    to find Keyzer in each level, opening more locations earlier.
    '''
    display_name = 'Open Level Doors'


class MusicShuffle(Choice):
    '''
    Music shuffle type
    None: Music is not shuffled
    Levels only: Only shuffle music between the main levels besides the Golden Passage
    Full: Shuffle all music
    '''
    display_name = 'Music Shuffle'
    option_none = 0
    option_levels_only = 1
    option_full = 2
    default = 0


wl4_options: Dict[str, Type[Option]] = {
    'difficulty': Difficulty,
    'required_jewels': RequiredJewels,
    'open_doors': OpenDoors,
    'death_link': DeathLink,
    #'music_shuffle': MusicShuffle,
}
