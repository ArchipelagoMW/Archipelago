from dataclasses import dataclass
from typing import Optional, Tuple

from .game_item import Source


@dataclass(frozen=True)
class Building:
    name: str
    sources: Tuple[Source, ...]
    upgrade_from: Optional[str] = None
