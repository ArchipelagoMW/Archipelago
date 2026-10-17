from .. import RegionTypeEnum
from ..helpers.card_types import Expansion, Rarity

class DefaultRegions(RegionTypeEnum):
    MENU = "Menu"

class Regions(RegionTypeEnum):

    EVENTS = "Play Table Events"

    PRODUCT_SELLING = "Products"

    LEVELS_1_TO_4 = "Levels 1-4"
    LEVELS_5_TO_9 = "Levels 5-9"
    LEVELS_10_TO_14 = "Levels 10-14"
    LEVELS_15_TO_19 = "Levels 15-19"
    LEVELS_20_TO_24 = "Levels 20-24"
    LEVELS_25_TO_29 = "Levels 25-29"
    LEVELS_30_TO_34 = "Levels 30-34"
    LEVELS_35_TO_39 = "Levels 35-39"
    LEVELS_40_TO_44 = "Levels 40-44"
    LEVELS_45_TO_49 = "Levels 45-49"
    LEVELS_50_TO_54 = "Levels 50-54"
    LEVELS_55_TO_59 = "Levels 55-59"
    LEVELS_60_TO_64 = "Levels 60-64"
    LEVELS_65_TO_69 = "Levels 65-69"
    LEVELS_70_TO_74 = "Levels 70-74"
    LEVELS_75_TO_79 = "Levels 75-79"
    LEVELS_80_TO_84 = "Levels 80-84"
    LEVELS_85_TO_89 = "Levels 85-89"
    LEVELS_90_TO_94 = "Levels 90-94"
    LEVELS_95_TO_99 = "Levels 95-99"
    LEVEL_100 = "Level 100"

    BASIC_PACKS = "Basic Card Packs"
    BASIC_PACKS_SELL = "Sell Basic Card Packs"
    BASIC_PACKS_GRADE = "Grade Basic Card Packs"

    RARE_PACKS = "Rare Card Packs"
    RARE_PACKS_SELL = "Sell Rare Card Packs"
    RARE_PACKS_GRADE = "Grade Rare Card Packs"

    EPIC_PACKS = "Epic Card Packs"
    EPIC_PACKS_SELL = "Sell Epic Card Packs"
    EPIC_PACKS_GRADE = "Grade Epic Card Packs"

    LEGENDARY_PACKS = "Legendary Card Packs"
    LEGENDARY_PACKS_SELL = "Sell Legendary Card Packs"
    LEGENDARY_PACKS_GRADE = "Grade Legendary Card Packs"

    DESTINY_BASIC_PACKS = "Basic Destiny Card Packs"
    DESTINY_BASIC_PACKS_SELL = "Sell Basic Destiny Card Packs"
    DESTINY_BASIC_PACKS_GRADE = "Grade Basic Destiny Card Packs"

    DESTINY_RARE_PACKS = "Rare Destiny Card Packs"
    DESTINY_RARE_PACKS_SELL = "Sell Rare Destiny Card Packs"
    DESTINY_RARE_PACKS_GRADE = "Grade Rare Destiny Card Packs"

    DESTINY_EPIC_PACKS = "Epic Destiny Card Packs"
    DESTINY_EPIC_PACKS_SELL = "Sell Epic Destiny Cards"
    DESTINY_EPIC_PACKS_GRADE = "Grade Epic Destiny Cards"

    DESTINY_LEGENDARY_PACKS = "Legendary Destiny Card Packs"
    DESTINY_LEGENDARY_PACKS_SELL = "Sell Legendary Destiny Cards"
    DESTINY_LEGENDARY_PACKS_GRADE = "Grade Legendary Destiny Cards"

    GENERIC_OPEN_PACKS = "Legendary Destiny Card Packs"
    GENERIC_SELL_CARDS= "Sell Legendary Destiny Cards"
    GENERIC_GRADE_CARDS = "Grade Legendary Destiny Cards"


def get_level_region(level: int) -> RegionTypeEnum:
    match level:
        case int() if level < 5:
            return Regions.LEVELS_1_TO_4
        case int() if level < 10:
            return Regions.LEVELS_5_TO_9
        case int() if level < 15:
            return Regions.LEVELS_10_TO_14
        case int() if level < 20:
            return Regions.LEVELS_15_TO_19
        case int() if level < 25:
            return Regions.LEVELS_20_TO_24
        case int() if level < 30:
            return Regions.LEVELS_25_TO_29
        case int() if level < 35:
            return Regions.LEVELS_30_TO_34
        case int() if level < 40:
            return Regions.LEVELS_35_TO_39
        case int() if level < 45:
            return Regions.LEVELS_40_TO_44
        case int() if level < 50:
            return Regions.LEVELS_45_TO_49
        case int() if level < 55:
            return Regions.LEVELS_50_TO_54
        case int() if level < 60:
            return Regions.LEVELS_55_TO_59
        case int() if level < 65:
            return Regions.LEVELS_60_TO_64
        case int() if level < 70:
            return Regions.LEVELS_65_TO_69
        case int() if level < 75:
            return Regions.LEVELS_70_TO_74
        case int() if level < 80:
            return Regions.LEVELS_75_TO_79
        case int() if level < 85:
            return Regions.LEVELS_80_TO_84
        case int() if level < 90:
            return Regions.LEVELS_85_TO_89
        case int() if level < 95:
            return Regions.LEVELS_90_TO_94
        case int() if level >= 100:
            return Regions.LEVEL_100
    return Regions.LEVELS_1_TO_4

region_by_pack: dict[tuple[Expansion, Rarity], RegionTypeEnum] = {
    # Tetramon
    (Expansion.TETRAMON, Rarity.COMMON): Regions.BASIC_PACKS,
    (Expansion.TETRAMON, Rarity.RARE): Regions.RARE_PACKS,
    (Expansion.TETRAMON, Rarity.EPIC): Regions.EPIC_PACKS,
    (Expansion.TETRAMON, Rarity.LEGENDARY): Regions.LEGENDARY_PACKS,

    # Destiny
    (Expansion.DESTINY, Rarity.COMMON): Regions.DESTINY_BASIC_PACKS,
    (Expansion.DESTINY, Rarity.RARE): Regions.DESTINY_RARE_PACKS,
    (Expansion.DESTINY, Rarity.EPIC): Regions.DESTINY_EPIC_PACKS,
    (Expansion.DESTINY, Rarity.LEGENDARY): Regions.DESTINY_LEGENDARY_PACKS,
}
