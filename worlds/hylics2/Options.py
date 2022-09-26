from Options import Choice, Toggle, DefaultOnToggle, DeathLink

class PartyShuffle(Toggle):
    """Shuffles party members into the pool.
    Note that enabling this can potentially increase both the difficulty and length of a run."""
    display_name = "Shuffle Party Members"

class GestureShuffle(Choice):
    """Choose where gestures will appear in the item pool."""
    display_name = "Shuffle Gestures"
    option_anywhere = 0
    option_tvs_only = 1
    option_default_locations = 2
    default = 0

class MedallionShuffle(Toggle):
    """Shuffles red medallions into the pool."""
    display_name = "Shuffle Red Medallions"

class RandomStart(Toggle):
    """Start the randomizer in 1 of 4 positions.
    (Waynehouse, Viewax's Edifice, TV Island, Shield Facility)"""
    display_name = "Randomize Start Location"

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
    "medallion_shuffle" : MedallionShuffle,
    "random_start" : RandomStart,
    "extra_items_in_logic": ExtraLogic,
    "death_link": Hylics2DeathLink
}