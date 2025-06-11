
from enum import Enum


class PieceLimitCascade(Enum):
    """Controls how child pieces are considered when checking piece limits."""
    NO_CHILDREN = 1  # Only consider the piece itself
    ACTUAL_CHILDREN = 2  # Consider the piece and its existing children
    POTENTIAL_CHILDREN = 3  # Consider the piece and all possible children

