from dataclasses import dataclass, field
from enum import IntEnum

from ... import GeneratedLocationData
from ...helpers.card_types import (
    Border, CardAction, CardSpecies, Difficulty, Expansion, Foil, Rarity,
    SPECIES_NAMES, SPECIES_RARITIES,
)



MAX_LOCATION_ID = (1 << 53) - 1
ACHIEVEMENT_FLAG = 1 << 52
FAMILY_SHIFT = 44
PAYLOAD_MASK = (1 << 44) - 1

ACTION_TO_CODE = {CardAction.OPEN: 0, CardAction.SELL: 1, CardAction.GRADE: 2}
CODE_TO_ACTION = {value: key for key, value in ACTION_TO_CODE.items()}

class AchievementKind(IntEnum):
    CARD_FILTER = 1


class CardAchievementFamily(IntEnum):
    GENERAL = 1
    FOIL = 2
    RARITY = 3
    EXPANSION = 4
    BORDER = 5
    SPECIFIC_SPECIES = 6
    DISTINCT_SPECIES = 7
    SAME_SPECIES = 8
    SAME_VARIANT = 9
    RARE_FOILS = 10
    HIGH_GRADE = 11
    PACK_RARITY = 12

@dataclass(frozen=True)
class CardAchievementDefinition(GeneratedLocationData):
    difficulty: Difficulty


def encode(payload: int, field: str, field_offsets: dict[str, tuple[int, int]], value: int) -> int:
    shift, width = field_offsets[field]
    if not 0 <= value < (1 << width):
        raise ValueError(f"{field}={value} does not fit {width} bits")
    return payload | (value << shift)