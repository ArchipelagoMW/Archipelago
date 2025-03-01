from dataclasses import dataclass, field
from functools import cached_property
from typing import Iterable, Tuple


@dataclass(frozen=True)
class Skill:
    name: str
    has_mastery: bool = field(kw_only=True)

    @cached_property
    def mastery_name(self) -> str:
        return f"{self.name} Mastery"

    @cached_property
    def level_name(self) -> str:
        return f"{self.name} Level"

    @cached_property
    def level_names_by_level(self) -> Iterable[Tuple[int, str]]:
        return tuple((level, f"Level {level} {self.name}") for level in range(1, 11))
