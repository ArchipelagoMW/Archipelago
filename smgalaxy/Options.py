import typing
from Options import Choice, Range
 
# this defines the enable_purple_coin_stars setting 
class EnablePurpleCoinStars(Choice):
    """tuning this off we allow purple coin stars to count as checks do note all purple coin stars are postgame only but one."""
    display_name = "Enable Purple Coin Stars"
    option_main_game_only = 0
    option_all = 1
    option_none = 2

# this allows players to pick their own star count to finish the game. 
class StarstoFinish(Range):
    "This will set the number of stars required to reach the center of the universe."
    display_name = "Stars to finish"
    range_start = 25
    range_end = 99
    default = 60
 
# this defines all the options.
galaxy_options = {
    "enable_purple_coin_stars": EnablePurpleCoinStars,
    "Stars_to_finish": StarstoFinish,
}


