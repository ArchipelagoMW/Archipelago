from BaseClasses import EntranceType
from rule_builder.options import OptionFilter
from rule_builder.rules import Has
from .regions import DefaultRegions
from .. import EntranceTypeEnum
from ..items import BoosterPackItems, DIYItems
from ..items.blockers import Blockers
from ..regions.regions import Regions
from ..rules.state_rules import HasLicensesForLevel

class Entrances(EntranceTypeEnum):
    SELLING = (
        "Sell Product",
        DefaultRegions.MENU,
        Regions.PRODUCT_SELLING,
        EntranceType.ONE_WAY,
    )
    EVENTS = (
        "Run Daily Events",
        DefaultRegions.MENU,
        Regions.EVENTS,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_PLAY_TABLE.value)
    )

class LevelEntrances(EntranceTypeEnum):
    LEVEL_1 = (
        "Level 1",
        DefaultRegions.MENU,
        Regions.LEVELS_1_TO_4,
        EntranceType.ONE_WAY,
    )
    LEVEL_5 = (
        "Level 5",
        Regions.LEVELS_1_TO_4,
        Regions.LEVELS_5_TO_9,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=5),
    )
    LEVEL_10 = (
        "Level 10",
        Regions.LEVELS_5_TO_9,
        Regions.LEVELS_10_TO_14,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=10),
    )
    LEVEL_15 = (
        "Level 15",
        Regions.LEVELS_10_TO_14,
        Regions.LEVELS_15_TO_19,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=15),
    )
    LEVEL_20 = (
        "Level 20",
        Regions.LEVELS_15_TO_19,
        Regions.LEVELS_20_TO_24,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=20),
    )
    LEVEL_25 = (
        "Level 25",
        Regions.LEVELS_20_TO_24,
        Regions.LEVELS_25_TO_29,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=25),
    )
    LEVEL_30 = (
        "Level 30",
        Regions.LEVELS_25_TO_29,
        Regions.LEVELS_30_TO_34,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=30),
    )
    LEVEL_35 = (
        "Level 35",
        Regions.LEVELS_30_TO_34,
        Regions.LEVELS_35_TO_39,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=35),
    )
    LEVEL_40 = (
        "Level 40",
        Regions.LEVELS_35_TO_39,
        Regions.LEVELS_40_TO_44,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=40),
    )
    LEVEL_45 = (
        "Level 45",
        Regions.LEVELS_40_TO_44,
        Regions.LEVELS_45_TO_49,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=45),
    )
    LEVEL_50 = (
        "Level 50",
        Regions.LEVELS_45_TO_49,
        Regions.LEVELS_50_TO_54,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=50),
    )
    LEVEL_55 = (
        "Level 55",
        Regions.LEVELS_50_TO_54,
        Regions.LEVELS_55_TO_59,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=55),
    )
    LEVEL_60 = (
        "Level 60",
        Regions.LEVELS_55_TO_59,
        Regions.LEVELS_60_TO_64,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=60),
    )
    LEVEL_65 = (
        "Level 65",
        Regions.LEVELS_60_TO_64,
        Regions.LEVELS_65_TO_69,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=65),
    )
    LEVEL_70 = (
        "Level 70",
        Regions.LEVELS_65_TO_69,
        Regions.LEVELS_70_TO_74,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=70),
    )
    LEVEL_75 = (
        "Level 75",
        Regions.LEVELS_70_TO_74,
        Regions.LEVELS_75_TO_79,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=75),
    )
    LEVEL_80 = (
        "Level 80",
        Regions.LEVELS_75_TO_79,
        Regions.LEVELS_80_TO_84,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=80),
    )
    LEVEL_85 = (
        "Level 85",
        Regions.LEVELS_80_TO_84,
        Regions.LEVELS_85_TO_89,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=85),
    )
    LEVEL_90 = (
        "Level 90",
        Regions.LEVELS_85_TO_89,
        Regions.LEVELS_90_TO_94,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=90),
    )
    LEVEL_95 = (
        "Level 95",
        Regions.LEVELS_90_TO_94,
        Regions.LEVELS_95_TO_99,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=95),
    )
    LEVEL_100 = (
        "Level 100",
        Regions.LEVELS_95_TO_99,
        Regions.LEVEL_100,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=100),
    )

class PackEntrances(EntranceTypeEnum):
    # Tetramon Base - Basic
    BASIC_PACKS = (
        "Open Tetramon Base Basic Packs",
        DefaultRegions.MENU,
        Regions.BASIC_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX.value),
    )
    BASIC_PACKS_SELL = (
        "Sell Tetramon Base Basic Cards",
        Regions.BASIC_PACKS,
        Regions.BASIC_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    BASIC_PACKS_GRADE = (
        "Grade Tetramon Base Basic Cards",
        Regions.BASIC_PACKS,
        Regions.BASIC_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Base - Rare
    RARE_PACKS = (
        "Open Tetramon Base Rare Packs",
        DefaultRegions.MENU,
        Regions.RARE_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_BOX.value),
    )
    RARE_PACKS_SELL = (
        "Sell Tetramon Base Rare Cards",
        Regions.RARE_PACKS,
        Regions.RARE_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    RARE_PACKS_GRADE = (
        "Grade Tetramon Base Rare Cards",
        Regions.RARE_PACKS,
        Regions.RARE_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Base - Epic
    EPIC_PACKS = (
        "Open Tetramon Base Epic Packs",
        DefaultRegions.MENU,
        Regions.EPIC_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_BOX.value),
    )
    EPIC_PACKS_SELL = (
        "Sell Tetramon Base Epic Cards",
        Regions.EPIC_PACKS,
        Regions.EPIC_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    EPIC_PACKS_GRADE = (
        "Grade Tetramon Base Epic Cards",
        Regions.EPIC_PACKS,
        Regions.EPIC_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Base - Legendary
    LEGENDARY_PACKS = (
        "Open Tetramon Base Legendary Packs",
        DefaultRegions.MENU,
        Regions.LEGENDARY_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_BOX.value),
    )
    LEGENDARY_PACKS_SELL = (
        "Sell Tetramon Base Legendary Cards",
        Regions.LEGENDARY_PACKS,
        Regions.LEGENDARY_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    LEGENDARY_PACKS_GRADE = (
        "Grade Tetramon Base Legendary Cards",
        Regions.LEGENDARY_PACKS,
        Regions.LEGENDARY_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Destiny - Basic
    DESTINY_BASIC_PACKS = (
        "Open Tetramon Destiny Basic Packs",
        DefaultRegions.MENU,
        Regions.DESTINY_BASIC_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_BOX.value),
    )
    DESTINY_BASIC_PACKS_SELL = (
        "Sell Tetramon Destiny Basic Cards",
        Regions.DESTINY_BASIC_PACKS,
        Regions.DESTINY_BASIC_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    DESTINY_BASIC_PACKS_GRADE = (
        "Grade Tetramon Destiny Basic Cards",
        Regions.DESTINY_BASIC_PACKS,
        Regions.DESTINY_BASIC_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Destiny - Rare
    DESTINY_RARE_PACKS = (
        "Open Tetramon Destiny Rare Packs",
        DefaultRegions.MENU,
        Regions.DESTINY_RARE_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_BOX.value),
    )
    DESTINY_RARE_PACKS_SELL = (
        "Sell Tetramon Destiny Rare Cards",
        Regions.DESTINY_RARE_PACKS,
        Regions.DESTINY_RARE_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    DESTINY_RARE_PACKS_GRADE = (
        "Grade Tetramon Destiny Rare Cards",
        Regions.DESTINY_RARE_PACKS,
        Regions.DESTINY_RARE_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Destiny - Epic
    DESTINY_EPIC_PACKS = (
        "Open Tetramon Destiny Epic Packs",
        DefaultRegions.MENU,
        Regions.DESTINY_EPIC_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_BOX.value),
    )
    DESTINY_EPIC_PACKS_SELL = (
        "Sell Tetramon Destiny Epic Cards",
        Regions.DESTINY_EPIC_PACKS,
        Regions.DESTINY_EPIC_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    DESTINY_EPIC_PACKS_GRADE = (
        "Grade Tetramon Destiny Epic Cards",
        Regions.DESTINY_EPIC_PACKS,
        Regions.DESTINY_EPIC_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Destiny - Legendary
    DESTINY_LEGENDARY_PACKS = (
        "Open Tetramon Destiny Legendary Packs",
        DefaultRegions.MENU,
        Regions.DESTINY_LEGENDARY_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_BOX.value),
    )
    DESTINY_LEGENDARY_PACKS_SELL = (
        "Sell Tetramon Destiny Legendary Cards",
        Regions.DESTINY_LEGENDARY_PACKS,
        Regions.DESTINY_LEGENDARY_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    DESTINY_LEGENDARY_PACKS_GRADE = (
        "Grade Tetramon Destiny Legendary Cards",
        Regions.DESTINY_LEGENDARY_PACKS,
        Regions.DESTINY_LEGENDARY_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )