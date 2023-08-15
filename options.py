from typing import Dict, Type
from Options import Choice, Option, DefaultOnToggle, DeathLink


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


class EarlyEntryJewels(DefaultOnToggle):
    '''
    Force the Entry Passage Jewel Pieces to appear early in the seed as a local item.
    Recommended to prevent early BK
    '''
    display_name = 'Early Entry Passage Jewels'


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
    'early_entry_jewels': EarlyEntryJewels,
    'death_link': DeathLink,
    #'music_shuffle': MusicShuffle,
}
