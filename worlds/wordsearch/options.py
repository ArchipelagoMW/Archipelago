from dataclasses import dataclass
from Options import FreeText, Range, Toggle, DefaultOnToggle, PerGameCommonOptions, StartInventoryPool

class GridSize(Range):
    """How large the game grid is, both dimensions are equal."""
    display_name = "Grid Size"
    range_start = 5
    default = 20
    range_end = 100

class TotalWordCount(Range):
    """How many words you have to get find to hit you goal."""
    display_name = "Total Word Count"
    range_start = 1
    default = 10
    range_end = 100

class StartingWordCount(Range):
    """How many words you start with, others become items."""
    display_name = "Starting Word Count"
    range_start = 1
    default = 4
    range_end = 100

class OutOfLogicWords(DefaultOnToggle):
    """Whether you can find a word before it is revealed."""
    display_name = "Out of Logic Words"

class StartingLoopCount(Range):
    """How many words you can find, Others become items."""
    display_name = "Starting Loop Count"
    range_start = 1
    default = 10
    range_end = 100

class DiagonalWords(DefaultOnToggle):
    """Whether words will generate diagonally."""
    display_name = "Diagonal Words"
    
class BackwardsWords(Toggle):
    """Whether words will generate backwards."""
    display_name = "Backwards Words"

class CustomWordList(FreeText):
    """A comma seperated list of words to hide in the wordsearch."""
    display_name = "Custom Word List"

class ExclusivelyCustomWords(Toggle):
    """Whether to use the custom word list exclusively or to seed the original word list."""
    display_name = "Exclusively Custom Words"

@dataclass
class WordSearchOptions(PerGameCommonOptions):
    grid_size: GridSize
    total_word_count: TotalWordCount
    starting_word_count: StartingWordCount
    out_of_logic_words: OutOfLogicWords
    starting_loop_count: StartingLoopCount
    diagonal_words: DiagonalWords
    backwards_words: BackwardsWords
    custom_word_list: CustomWordList
    exclusively_custom_words: ExclusivelyCustomWords
    
    start_inventory_from_pool: StartInventoryPool
