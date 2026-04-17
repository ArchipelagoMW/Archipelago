"""Per-slot options for Ducks Can Drive.

Intentionally minimal for the first working APWorld — only the common options
every game gets. Ducks-specific options (book shuffle, TT par-time gating,
starting stats, etc.) will be added as the content surface grows.
"""
from __future__ import annotations

from dataclasses import dataclass

from Options import PerGameCommonOptions


@dataclass
class DucksOptions(PerGameCommonOptions):
    pass
