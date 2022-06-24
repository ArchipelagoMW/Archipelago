
from Options import Choice, Toggle, DefaultOnToggle, Range, OptionList
from .Characters import all_chars


class Characters(OptionList):
    """Characters which contain checks. Each will be represented at least once."""
    display_name = "Available Characters"
    valid_keys = frozenset(all_chars)


class ReduceStartingItems(Toggle):
    """Normally, all diamond-unlocked items are restricted. If this is turned on, almost all item types are initially restricted."""
    display_name = "Reduce Starting Available Items"


class RandomizeFlawless(Toggle):
    """Flawless boss chests will additionally contain AP sendable items. Flawlessing bosses can be difficult, though!"""
    display_name = "Randomize Boss Flawless Chests"


class FreeSamples(Toggle):
    """Receive a free copy of an item type when received, if the current character can use it."""
    display_name = "Free Samples"


class PreventBadSamples(DefaultOnToggle):
    """Don't receive free copies of items with potentially negative effects: Karate Gi, Crown of Thorns, Glass Jaw, Sunglasses, Boots of Pain, Ring of Pain, Ring of Becoming, Ring of Shadows."""
    display_name = "Prevent Bad Samples"


class TrapPercentage(Range):
    """Percentage chance for a junk item to be a negative trap."""
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


cotnd_options = {
    'available_characters':     Characters,
    'reduce_starting_items':    ReduceStartingItems,
    'randomize_flawless':       RandomizeFlawless,
    'free_samples':             FreeSamples,
    'prevent_bad_samples':      PreventBadSamples,
    'trap_percentage':          TrapPercentage,
}
