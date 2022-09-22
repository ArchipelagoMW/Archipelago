import typing
from Options import Choice, Option, Toggle, DefaultOnToggle, Range, OptionList, DeathLink

class PartyShuffle(Toggle):
    """Choose whether or not to shuffle party members.
    Note that enabling this can drastically increase both the difficulty and length of a run."""
    display_name = "Shuffle Party Members"

class GestureShuffle(Choice):
    """Choose where gestures will appear in the item pool."""
    display_name = "Shuffle Gestures"
    option_on = 0
    option_tvs_only = 1
    option_off = 2
    alias_true = 0
    alias_false = 2
    default = 0

class ExtraLogic(DefaultOnToggle):
    """Include some extra items in logic (CHARGE UP, 1x PAPER CUP) to prevent the game from becoming too difficult."""
    display_name = "Extra Items in Logic"

class Hylics2DeathLink(DeathLink):
    """When you die, everyone dies. The reverse is also true.
    Note that this also includes death by using the PERISH gesture.
    Can be toggled via in-game console command "/deathlink"."""

hylics2_options = {
    "party_shuffle": PartyShuffle,
    "gesture_shuffle" : GestureShuffle,
    "extra_items_in_logic": ExtraLogic,
    "death_link": Hylics2DeathLink
}