from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Tuple

from .game_item import Source


@dataclass(frozen=True)
class Building:
    name: str
    sources: Tuple[Source, ...] = field(kw_only=True)
    upgrade_from: Optional[str] = field(default=None, kw_only=True)

    @cached_property
    def is_upgrade(self) -> bool:
        return self.upgrade_from is not None
