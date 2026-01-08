"""Search mode enum."""

from enum import IntEnum, auto


class SearchMode(IntEnum):
    """Search mode enum."""

    GetReachable = auto()
    GetReachableForFilling = auto()
    GeneratePlaythrough = auto()
    CheckBeatable = auto()
    CheckAllReachable = auto()
    GetUnreachable = auto()
    GetReachableWithControlledPurchases = auto()
    CheckSpecificItemReachable = auto()
