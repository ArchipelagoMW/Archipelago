from dataclasses import dataclass, field
from functools import cached_property
from typing import Iterable, Sequence, Tuple

from ..data.game_item import kw_only


@dataclass(frozen=True)
class Skill:
    name: str
    has_mastery: bool = field(**kw_only)

    @cached_property
    def mastery_name(self) -> str:
        return f"{self.name} Mastery"

    @cached_property
    def level_name(self) -> str:
        return f"{self.name} Level"

    @cached_property
    def levels(self) -> Sequence[int]:
        return range(1, 11)

    @cached_property
    def level_names(self) -> Iterable[str]:
        return tuple(f"Level {level} {self.name}" for level in self.levels)

    @cached_property
    def level_names_by_level(self) -> Iterable[Tuple[int, str]]:
        return tuple((level, f"Level {level} {self.name}") for level in self.levels)
