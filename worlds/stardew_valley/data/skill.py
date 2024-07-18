from dataclasses import dataclass, field
from functools import cached_property

from ..data.game_item import kw_only


@dataclass(frozen=True)
class Skill:
    name: str
    has_mastery: bool = field(**kw_only)

    @cached_property
    def mastery_name(self) -> str:
        return f"{self.name} Mastery"
