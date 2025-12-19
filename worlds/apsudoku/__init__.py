from typing import Dict

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, WorldType


class AP_SudokuWebWorld(WebWorld):
    """
    Play a little Sudoku while you're in BK mode to maybe get some useful hints
    """
    game = 'Sudoku'
    world_type = WorldType.HINT_GAME
    options_page = False
    theme = 'partyTime'

    setup_en = Tutorial(
        tutorial_name='Setup Guide',
        description='A guide to playing APSudoku',
        language='English',
        file_name='setup_en.md',
        link='setup/en',
        authors=['EmilyV']
    )
    
    tutorials = [setup_en]
