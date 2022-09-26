import typing
from Options import Choice, Option, Toggle, Range, DefaultOnToggle, OptionList

class ExtraLevels(Toggle):
    """Whether or not to include the difficult Extra Stages."""
    display_name = "Include Extra Stages"

class CoinVisibility(Choice):
    """
    Which Palette to use for the Kongs
    """
    display_name = "Magnifying Glass Mode"
    option_none = 0
    option_coins_only = 1
    option_full = 2
    default = 1

class YoshiColors(Choice):
    """
    Which colors the Yoshis will use
    """
    display_name = "Yoshi Colors"
    option_normal = 0
    option_shuffled = 1
    option_randomize = 2
    default = 0

class StageLogic(Choice):
    """
    loose n
    """
    display_name = "Stage Logic"
    option_strict = 0
    option_loose = 1
    option_difficult = 2
    option_glitched = 3
    default = 1

class FinalLevelUnlock(Choice):
    """
    Condition under which to open 6-8
    """
    display_name = "6-8 Unlock"
    option_open = 0
    option_score = 1
    option_castles = 2
    option_bosses = 3
    default = 2

yoshi_options: typing.Dict[str, type(Option)] = {
    "extras_required":  ExtraLevels,
    "coin_visibility": CoinVisibility,
    "yoshi_colors": YoshiColors,
    "stage_logic": StageLogic,
    
}