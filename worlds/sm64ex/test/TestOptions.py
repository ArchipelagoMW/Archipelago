from . import SM64TestBase
from .. import Options

# Completion Types
class CompletionLastBowserTestBase(SM64TestBase):
    options = {
        "completion_type": Options.CompletionType.option_Last_Bowser_Stage
    }

class CompletionAllBowserTestBase(SM64TestBase):
    options = {
        "completion_type": Options.CompletionType.option_All_Bowser_Stages
    }

# Combinations

class MinimumStarsPossibleTestBase(SM64TestBase):
    options = {
        "amount_of_stars": Options.AmountOfStars.range_start,
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "exclamation_boxes": Options.ExclamationBoxes.option_false,
        "enable_coin_stars": Options.EnableCoinStars.option_false
    }