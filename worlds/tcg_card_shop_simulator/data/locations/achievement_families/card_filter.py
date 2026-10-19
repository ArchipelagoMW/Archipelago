from __future__ import annotations

from enum import IntEnum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from BaseClasses import CollectionRule
from rule_builder.rules import Rule, True_
if TYPE_CHECKING:
    from ....world_base import TCGSimulatorBase

from . import CardAchievementFamily, CardAchievementDefinition, ACHIEVEMENT_FLAG, AchievementKind, FAMILY_SHIFT, \
    MAX_LOCATION_ID, encode, ACTION_TO_CODE
from ... import RegionTypeEnum
from ...helpers.card_types import (
    Border, CardAction, CardSpecies, Difficulty, Expansion, Foil, Rarity, SPECIES_NAMES,
)
from ...regions.regions import GenericRegions

CARD_FILTER_FIELD_OFFSETS: dict[str, tuple[int, int]] = {
    "threshold": (0, 12),
    "species": (12, 8),
    "rarity": (20, 3),
    "expansion": (23, 3),
    "border": (26, 3),
    "foil": (29, 2),
    "grade": (31, 4),
    "group_by": (35, 5),
    "count_mode": (40, 2),
    "action": (42, 2),
}

class CountMode(IntEnum):
    TOTAL = 0      # total amount that match a filter
    DISTINCT = 1   # every group that matches the filter increments in a group

class GroupBy(IntEnum):
    NONE = 0
    SPECIES = 1



ALL_ACTIONS = (CardAction.OPEN, CardAction.SELL, CardAction.GRADE)

@dataclass(frozen=True, kw_only=True)
class CardFilters:
    """None means ANY"""
    rarity: Rarity | None = None
    expansion: Expansion | None = None
    border: Border | None = None
    foil: Foil | None = None
    species: CardSpecies | None = None
    grade: int | None = None



@dataclass(frozen=True, kw_only=True)
class CardClause:
    action: CardAction
    threshold: int
    filters: CardFilters = field(default_factory=CardFilters)
    count_mode: CountMode = CountMode.TOTAL
    group_by: GroupBy = GroupBy.NONE




@dataclass(frozen=True)
class Tier:
    threshold: int
    difficulty: Difficulty


@dataclass(frozen=True, kw_only=True)
class CardTemplate:
    action: CardAction
    tiers: tuple[Tier, ...]
    count_mode: CountMode = CountMode.TOTAL
    group_by: GroupBy = GroupBy.NONE
    rarity:Rarity | None = None
    expansion: Expansion | None = None
    border: Border | None = None
    foil: Foil | None = None
    species: CardSpecies | None = None
    minimum_grade: int | None = None
    rule: CollectionRule | Rule[TCGSimulatorBase] = field(default_factory=True_)
    region: RegionTypeEnum

    def get_location_id(self, difficulty: Difficulty) -> int:
        threshold = next(
            tier.threshold
            for tier in self.tiers
            if tier.difficulty == difficulty
        )
        values = {
            "threshold": threshold,
            "species": 255 if self.species is None else int(self.species),
            "rarity": 0 if self.rarity is None else int(self.rarity),
            "expansion": 7 if self.expansion is None else int(self.expansion),
            "border": 7 if self.border is None else int(self.border),
            "foil": 2 if self.foil is None else int(self.foil),
            "grade": 0 if self.minimum_grade is None else self.minimum_grade,
            "group_by": int(self.group_by),
            "count_mode": int(self.count_mode),
            "action": ACTION_TO_CODE[self.action],
        }
        payload = 0
        for value_field, value in values.items():
            payload = encode(payload, value_field, CARD_FILTER_FIELD_OFFSETS, value)
        result = ACHIEVEMENT_FLAG | (int(AchievementKind.CARD_FILTER) << FAMILY_SHIFT) | payload
        assert ACHIEVEMENT_FLAG <= result <= MAX_LOCATION_ID
        return result

    def get_name(self, difficulty: Difficulty) -> str:
        threshold = next(
            tier.threshold
            for tier in self.tiers
            if tier.difficulty == difficulty
        )
        pieces: list[str] = []
        if self.expansion is not None:
            pieces.append(self.expansion.name.title())
        if self.rarity is not None:
            pieces.append(self.rarity.name.title())
        if self.border is not None:
            pieces.append(self.border.name.replace("_", " ").title() + " Border")
        if self.foil is not None:
            pieces.append("Foil" if self.foil == Foil.FOIL else "Non-Foil")
        if self.species is not None:
            pieces.append(SPECIES_NAMES[self.species])
        modifier = (" ".join(pieces) + " ") if pieces else ""
        grade_suffix = f" at Grade {self.minimum_grade}" if self.minimum_grade is not None else ""
        if self.count_mode == CountMode.TOTAL:
            return f"{self.action.value} {threshold} {modifier}Cards{grade_suffix}"
        if self.count_mode == CountMode.DISTINCT:
            key = "Card Species" if self.group_by == GroupBy.SPECIES else "Card Variants"
            return f"{self.action.value} {threshold} Different {modifier}{key}{grade_suffix}"
        key = "Card Species" if self.group_by == GroupBy.SPECIES else "Card Variant"
        return f"{self.action.value} {threshold} of the Same {modifier}{key}{grade_suffix}"

    def get_locations(self, difficulty: Difficulty) -> list[CardAchievementDefinition]:
        achievements: list[CardAchievementDefinition] = []
        achievements.extend(
            CardAchievementDefinition(
                difficulty = tier.difficulty,
                location_id = self.get_location_id(tier.difficulty),
                name = self.get_name(tier.difficulty),
                rule = self.rule,
                region = self.region
            )
            for tier in self.tiers
            if tier.difficulty <= difficulty
        )
        return achievements



OPEN_TEMPLATES: dict[CardAchievementFamily, tuple[CardTemplate, ...]] = {
    CardAchievementFamily.GENERAL: (
        CardTemplate(
            action=CardAction.OPEN,
            tiers=(Tier(5, Difficulty.EASY), Tier(15, Difficulty.MEDIUM),
                   Tier(30, Difficulty.HARD), Tier(100, Difficulty.IMPOSSIBLE)),
            region=GenericRegions.GENERIC_OPEN_PACKS
        ),
    ),
    CardAchievementFamily.FOIL: (
    ),
    CardAchievementFamily.RARITY: (),
    CardAchievementFamily.EXPANSION: (),
    CardAchievementFamily.BORDER: (),
    CardAchievementFamily.SPECIFIC_SPECIES: (),
    CardAchievementFamily.DISTINCT_SPECIES: (),
    CardAchievementFamily.SAME_SPECIES: (),
    CardAchievementFamily.SAME_VARIANT: (),
    CardAchievementFamily.RARE_FOILS: (),
    CardAchievementFamily.HIGH_GRADE: (),
    CardAchievementFamily.PACK_RARITY: (),
}

SELL_TEMPLATES: dict[CardAchievementFamily, tuple[CardTemplate, ...]] = {
    CardAchievementFamily.GENERAL: (
        CardTemplate(
            action=CardAction.SELL,
            tiers=(Tier(3, Difficulty.EASY), Tier(10, Difficulty.MEDIUM),
                   Tier(25, Difficulty.HARD), Tier(50, Difficulty.IMPOSSIBLE)),
            region=GenericRegions.GENERIC_SELL_CARDS
        ),
    ),
    CardAchievementFamily.FOIL: (),
    CardAchievementFamily.RARITY: (),
    CardAchievementFamily.EXPANSION: (),
    CardAchievementFamily.BORDER: (),
    CardAchievementFamily.SPECIFIC_SPECIES: (),
    CardAchievementFamily.DISTINCT_SPECIES: (),
    CardAchievementFamily.SAME_SPECIES: (),
    CardAchievementFamily.SAME_VARIANT: (),
    CardAchievementFamily.RARE_FOILS: (),
    CardAchievementFamily.HIGH_GRADE: (),
    CardAchievementFamily.PACK_RARITY: (),
}

GRADE_TEMPLATES: dict[CardAchievementFamily, tuple[CardTemplate, ...]] = {
    CardAchievementFamily.GENERAL: (
        CardTemplate(
            action=CardAction.GRADE,
            tiers=(Tier(1, Difficulty.EASY), Tier(3, Difficulty.MEDIUM),
                   Tier(6, Difficulty.HARD), Tier(12, Difficulty.IMPOSSIBLE)),
            region=GenericRegions.GENERIC_GRADE_CARDS
        ),
    ),
    CardAchievementFamily.FOIL: (),
    CardAchievementFamily.RARITY: (),
    CardAchievementFamily.EXPANSION: (),
    CardAchievementFamily.BORDER: (),
    CardAchievementFamily.SPECIFIC_SPECIES: (),
    CardAchievementFamily.DISTINCT_SPECIES: (),
    CardAchievementFamily.SAME_SPECIES: (),
    CardAchievementFamily.SAME_VARIANT: (),
    CardAchievementFamily.RARE_FOILS: (),
    CardAchievementFamily.HIGH_GRADE: (),
    CardAchievementFamily.PACK_RARITY: (),
}