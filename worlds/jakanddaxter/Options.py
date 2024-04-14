import typing
from dataclasses import dataclass
from Options import DefaultOnToggle, Range, Toggle, DeathLink, Choice, PerGameCommonOptions, OptionSet
from .Items import action_item_table

class EnableScoutFlies(Toggle):
    """Enable to include each Scout Fly as a check. Adds 213 checks to the pool."""
    display_name = "Enable Scout Flies"

# class EnablePrecursorOrbs(Toggle):
#     """Enable to include each Precursor Orb as a check. Adds 2000 checks to the pool."""
#     display_name = "Enable Precursor Orbs"