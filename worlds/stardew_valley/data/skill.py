from dataclasses import dataclass, field


@dataclass(frozen=True)
class Skill:
    name: str
    has_mastery: bool = field(kw_only=True)
