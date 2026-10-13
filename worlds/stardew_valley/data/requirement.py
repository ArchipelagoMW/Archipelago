from dataclasses import dataclass, field
from typing import Tuple

from .game_item import Requirement
from ..strings.tool_names import ToolMaterial


@dataclass(frozen=True)
class HasItemRequirement(Requirement):
    item: str


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
class MeetRequirement(Requirement):
    npc: str


@dataclass(frozen=True)
class SpecificFriendRequirement(Requirement):
    npc: str
    hearts: int


@dataclass(frozen=True)
class NumberOfFriendsRequirement(Requirement):
    friends: int
    hearts: int


@dataclass(frozen=True)
class FishingRequirement(Requirement):
    region: str


@dataclass(frozen=True)
class WalnutRequirement(Requirement):
    amount: int


@dataclass(frozen=True)
class TotalEarningsRequirement(Requirement):
    amount: int


@dataclass(frozen=True)
class GrangeDisplayRequirement(Requirement):
    pass


@dataclass(frozen=True)
class EggHuntRequirement(Requirement):
    pass


@dataclass(frozen=True)
class FishingCompetitionRequirement(Requirement):
    pass


@dataclass(frozen=True)
class LuauDelightRequirementRequirement(Requirement):
    pass


@dataclass(frozen=True)
class MovieRequirement(Requirement):
    pass


@dataclass(frozen=True)
class ForgeInfinityWeaponRequirement(Requirement):
    pass


@dataclass(frozen=True)
class CaughtFishRequirement(Requirement):
    number_fish: int
    unique: bool = field(kw_only=True)


@dataclass(frozen=True)
class MuseumCompletionRequirement(Requirement):
    number_donated: int = 95


@dataclass(frozen=True)
class FullShipmentRequirement(Requirement):
    pass


@dataclass(frozen=True)
class BuildingRequirement(Requirement):
    building: str


@dataclass(frozen=True)
class CookedRecipesRequirement(Requirement):
    number_of_recipes: int


@dataclass(frozen=True)
class CraftedItemsRequirement(Requirement):
    number_of_recipes: int


@dataclass(frozen=True)
class HelpWantedRequirement(Requirement):
    number_of_quests: int


@dataclass(frozen=True)
class ShipOneCropRequirement(Requirement):
    number: int


@dataclass(frozen=True)
class ReceivedRaccoonsRequirement(Requirement):
    number_of_raccoons: int


@dataclass(frozen=True)
class PrizeMachineRequirement(Requirement):
    number_of_tickets: int


@dataclass(frozen=True)
class AllAchievementsRequirement(Requirement):
    pass


@dataclass(frozen=True)
class PerfectionPercentRequirement(Requirement):
    percent: int


@dataclass(frozen=True)
class ReadAllBooksRequirement(Requirement):
    pass


@dataclass(frozen=True)
class MinesRequirement(Requirement):
    floor: int


@dataclass(frozen=True)
class DangerousMinesRequirement(Requirement):
    floor: int


@dataclass(frozen=True)
class MonsterKillRequirement(Requirement):
    monsters: Tuple[str, ...]
    amount: int = 1


@dataclass(frozen=True)
class CatalogueRequirement(Requirement):
    catalogue: str
