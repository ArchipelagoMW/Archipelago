from dataclasses import dataclass, field
from typing import Optional, Tuple

from .game_item import Source, kw_only


@dataclass(frozen=True)
class Building:
    name: str
    sources: Tuple[Source, ...] = field(**kw_only)
    upgrade_from: Optional[str] = field(default=None, **kw_only)
