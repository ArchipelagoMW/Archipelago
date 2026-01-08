"""Kong enum."""

from __future__ import annotations
from randomizer.JsonReader import generate_globals

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from randomizer.Enums.Kongs import Kongs
globals().update(generate_globals(__file__))


def GetKongs() -> List[Kongs]:
    """Return list of kongs without any."""
    return [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
