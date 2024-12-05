from . import SM64TestBase
from .. import Options
from ..Locations import loc100Coin_table

class DefaultTestBase(SM64TestBase):
    options = {}

# Enable Coin Stars
class EnableCoinStarsTestBase(SM64TestBase):
    options = {
        "enable_coin_stars": Options.EnableCoinStars.option_true
    }

    # Ensure Coin Star locations are created
    def test_coin_star_locations(self):
        for loc in loc100Coin_table:
            assert loc in self.world.location_names

class DisableCoinStarsTestBase(SM64TestBase):
    options = {
        "enable_coin_stars": Options.EnableCoinStars.option_false
    }

    # Ensure Coin Star locations are not created
    def test_coin_star_locations(self):
        for loc in self.multiworld.get_locations():
            assert loc not in loc100Coin_table

# Completion Type
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

    # There will be less Power Stars than filler with this low of a star count
    def test_stars_vs_filler(self):
        filler_count = len(self.get_items_by_name("1Up Mushroom"))
        star_count = len(self.get_items_by_name("Power Star"))
        self.assertGreater(filler_count, star_count)