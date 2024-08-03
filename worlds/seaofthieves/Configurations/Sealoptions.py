import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import Toggle


class SealRange(Range):
    range_start = 0
    range_end = 5


class SealsRequired(SealRange):
    """The Fort of the Damned location is locked behind the selected number of seals."""
    display_name = "FOD Seal Requirement"
    default = 3


class VodRequired(Toggle):
    """If enabled, the Fort of the Damned location is locked behind the Voyage of Destiny (Skull of Destiny Voyage)"""
    display_name = "FOD Require Skull of Destiny"
    default = 0
