from typing import Dict

from BaseClasses import Tutorial
from ..AutoWorld import WebWorld, World


class Bk_SudokuWebWorld(WebWorld):
    options_page = "games/Sudoku/info/en"
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing BK Sudoku',
            language='English',
            file_name='setup_en.md',
            link='setup/en',
            authors=['Jarno']
        )
    ]


class Bk_SudokuWorld(World):
    """
    Play a little Sudoku while you're in BK mode to maybe get some useful hints
    """
    game = "Sudoku"
    web = Bk_SudokuWebWorld()
    data_version = 1

    item_name_to_id: Dict[str, int] = {}
    location_name_to_id: Dict[str, int] = {}

    @classmethod
    def stage_assert_generate(cls, multiworld):
        raise Exception("BK Sudoku cannot be used for generating worlds, the client can instead connect to any other world")
