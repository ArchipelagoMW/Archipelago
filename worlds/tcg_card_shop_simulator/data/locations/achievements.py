from .achievement_families.card_filter import OPEN_TEMPLATES, SELL_TEMPLATES, GRADE_TEMPLATES
from ...data import GeneratedLocationData
from ..helpers.card_types import Difficulty
from .achievement_families import CardAchievementFamily


def generate_all_achievement_locations(family: CardAchievementFamily) -> list[GeneratedLocationData]:
    locations: list[GeneratedLocationData] = []
    locations.extend(
        location
        for location in generate_open_achievement_locations(family, Difficulty.IMPOSSIBLE)
    )
    locations.extend(
        location
        for location in generate_sell_achievement_locations(family, Difficulty.IMPOSSIBLE)
    )
    locations.extend(
        location
        for location in generate_grade_achievement_locations(family, Difficulty.IMPOSSIBLE)
    )
    return locations

def generate_open_achievement_locations(family: CardAchievementFamily, difficulty: Difficulty) -> list[GeneratedLocationData]:
    locations: list[GeneratedLocationData] = []
    if family.value <= CardAchievementFamily.PACK_RARITY and difficulty != Difficulty.DISABLED:
        locations.extend(
            location
            for template in OPEN_TEMPLATES[family]
            for location in template.get_locations(difficulty)
        )
    return locations

def generate_sell_achievement_locations(family: CardAchievementFamily, difficulty: Difficulty) -> list[GeneratedLocationData]:
    locations: list[GeneratedLocationData] = []
    if family.value <= CardAchievementFamily.PACK_RARITY and difficulty != Difficulty.DISABLED:
        locations.extend(
            location
            for template in SELL_TEMPLATES[family]
            for location in template.get_locations(difficulty)
        )
    return locations

def generate_grade_achievement_locations(family: CardAchievementFamily, difficulty: Difficulty) -> list[GeneratedLocationData]:
    locations: list[GeneratedLocationData] = []
    if family.value <= CardAchievementFamily.PACK_RARITY and difficulty != Difficulty.DISABLED:
        locations.extend(
            location
            for template in GRADE_TEMPLATES[family]
            for location in template.get_locations(difficulty)
        )
    return locations