from dataclasses import dataclass, field

from ..data.game_item import kw_only


@dataclass(frozen=True)
class Skill:
    name: str
    has_mastery: bool = field(**kw_only)
