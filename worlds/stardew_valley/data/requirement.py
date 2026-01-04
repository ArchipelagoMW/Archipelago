from dataclasses import dataclass

from .game_item import Requirement
from ..strings.tool_names import ToolMaterial


@dataclass(frozen=True)
class BookRequirement(Requirement):
    book: str


@dataclass(frozen=True)
class ToolRequirement(Requirement):
    tool: str
    tier: str = ToolMaterial.basic


@dataclass(frozen=True)
class SkillRequirement(Requirement):
    skill: str
    level: int


@dataclass(frozen=True)
class RegionRequirement(Requirement):
    region: str


@dataclass(frozen=True)
class SeasonRequirement(Requirement):
    season: str


@dataclass(frozen=True)
class YearRequirement(Requirement):
    year: int


@dataclass(frozen=True)
class CombatRequirement(Requirement):
    level: str


@dataclass(frozen=True)
class QuestRequirement(Requirement):
    quest: str


@dataclass(frozen=True)
class RelationshipRequirement(Requirement):
    npc: str
    hearts: int


@dataclass(frozen=True)
class FishingRequirement(Requirement):
    region: str


@dataclass(frozen=True)
class WalnutRequirement(Requirement):
    amount: int
