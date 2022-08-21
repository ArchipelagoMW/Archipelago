import typing
from Options import Choice, Option, Toggle, DefaultOnToggle, Range, OptionList, DeathLink

class GestureShuffle(Choice):
    """Choose where gestures will appear in the item pool."""
    display_name = "Shuffle Gestures"
    option_anywhere = 0
    option_tvs_only = 1
    option_not_shuffled = 2
    default = 0

class Hylics2DeathLink(DeathLink):
    """When you die, everyone dies. The reverse is also true.
    Note that this also includes death by using the PERISH gesture.
    Can be toggled via in-game console command "deathlink"."""

options = {
    "gesture_shuffle" : GestureShuffle,
    "death_link": Hylics2DeathLink
}