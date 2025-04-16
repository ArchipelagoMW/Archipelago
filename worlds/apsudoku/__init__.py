from typing import Dict

from BaseClasses import Tutorial
from ..AutoWorld import WebWorld, World

class AP_SudokuWebWorld(WebWorld):
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

class AP_SudokuWorld(World):
    """
    Play a little Sudoku while you're in BK mode to maybe get some useful hints
    """
    game = "Sudoku"
    web = AP_SudokuWebWorld()

    item_name_to_id: Dict[str, int] = {}
    location_name_to_id: Dict[str, int] = {}

    @classmethod
    def stage_assert_generate(cls, multiworld):
        raise Exception("APSudoku cannot be used for generating worlds, the client can instead connect to any slot from any world")

