from dataclasses import dataclass

from Options import Choice, Range, PerGameCommonOptions, OptionSet, Toggle


class GalaxyShuffle(OptionSet):
    """
    Determine what kinds of galaxies should be shuffled between each other

    Full: Any galaxy in any galaxy position
    Dome Majors: Add Major galaxies to shuffle pool
    Dome Minors: Add Minor galaxies to shuffle pool
    Observatory Specials: Add Direct from Observatory galaxies to shuffle pool, such as Trials or Hungry Luma galaxies
    Bosses: Add Boss galaxies to shuffle pool
    """
    display_name = "Galaxy Shuffle"
    internal_name = "galaxy_shuffle"
    valid_keys = {"Full", "Dome Majors", "Dome Minors", "Observatory Specials", "Bosses"}

class ShuffleDomes(Toggle):
    """
    Shuffle Dome entrances
    """
    display_name = "Dome Shuffle"
    internal_name = "dome_shuffle"

# this defines the enable_purple_coin_stars setting 
class EnablePurpleCoinStars(Choice):
    """
    Add Purple Coin star location. Only one of these is normally available outside of post game
    """
    display_name = "Enable Purple Coin Stars"
    internal_name = "enable_purple_coin_stars"
    option_main_game_only = 0
    option_all = 1
    option_none = 2

# this allows players to pick their own star count to finish the game. 
class StarstoFinish(Range):
    """This will set the number of stars required to reach the center of the universe."""
    display_name = "Stars to finish"
    internal_name = "stars_to_finish"
    range_start = 25
    range_end = 99
    default = 60
 
# this defines all the options.
@dataclass
class SMGOptions(PerGameCommonOptions):
    enable_purple_coin_stars: EnablePurpleCoinStars
    stars_to_finish: StarstoFinish
    #dome_shuffle: ShuffleDomes Enable when Ready
    #galaxy_shuffle: GalaxyShuffle Enable when Ready


