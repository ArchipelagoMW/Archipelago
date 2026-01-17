from dataclasses import dataclass
from Options import Toggle, Option, Range, Choice, ItemSet, OptionSet, PerGameCommonOptions, StartHints, TextChoice

class RequiredBingos(Range):
    """The number of Bingo's required to goal, min is 1, max is 22
    max per board size: 3x3 = 8, 4x4 = 10, 5x5 = 12, 6x6 = 14, 7x7 = 16, 8x8 = 18, 9x9 = 20, 10x10 = 22 """
    range_start = 1
    range_end = 22
    default = 1
    display_name = "Required Bingos"


class BoardSize(Range):
    """The size of the bingo board (3 = 3x3, 10 = 10x10)"""
    range_start = 3
    range_end = 10
    default = 5
    display_name = "Board Size"

class BingoBalancing(Range):
    """The percentage of bingo squares that'll be forcibly equally divided amongst the other worlds"""
    range_start = 0
    range_end = 100
    default = 0
    display_name = "Bingo Forced Balancing"

class AutoHints(Toggle):
    """If true, automatically hint all board squares"""
    display_name = "Auto Hints"


class CustomBoardColor(TextChoice):
    """Choose the background Color (Use colors or Hex)"""
    display_name = "Background Color"
    default = "White"


class CustomSquareColor(TextChoice):
    """Choose the Square Color (Use colors or Hex)"""
    display_name = "Square Color"
    default = "White"


class CustomHLSquareColor(TextChoice):
    """Choose the Highlighted Square Color (Use colors or Hex)"""
    display_name = "Highlighted Square Color"
    default = "Green"


class CustomTextColor(TextChoice):
    """Choose the Text Color (Use colors or Hex)"""
    display_name = "Text Color"
    default = "Black"

class BingoStartHints(StartHints):
    """Start with these item's locations prefilled into the ``!hint`` command."""
    default = []

@dataclass
class BingoOptions(PerGameCommonOptions):
    required_bingos: RequiredBingos
    board_size: BoardSize
    bingo_balance: BingoBalancing
    auto_hints: AutoHints
    board_color: CustomBoardColor
    square_color: CustomSquareColor
    hl_square_color: CustomHLSquareColor
    text_color: CustomTextColor
    start_hints: BingoStartHints
