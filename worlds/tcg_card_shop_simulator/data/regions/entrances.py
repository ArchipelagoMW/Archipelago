from BaseClasses import EntranceType
from rule_builder.options import OptionFilter
from rule_builder.rules import Has
from .regions import DefaultRegions, GenericRegions, LevelRegions, PackRegions
from .. import EntranceTypeEnum, RegionTypeEnum, ItemTypeEnum
from ..items import BoosterPackItems, DIYItems
from ..items.blockers import Blockers
from ..rules.state_rules import HasLicensesForLevel

class Entrances(EntranceTypeEnum):
    SELLING = (
        "Sell Product",
        DefaultRegions.MENU,
        GenericRegions.PRODUCT_SELLING,
        EntranceType.ONE_WAY,
    )
    EVENTS = (
        "Run Daily Events",
        DefaultRegions.MENU,
        GenericRegions.EVENTS,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_PLAY_TABLE.value)
    )

class LevelEntrances(EntranceTypeEnum):
    LEVEL_1 = (
        "Level 1",
        DefaultRegions.MENU,
        LevelRegions.LEVELS_1_TO_4,
        EntranceType.ONE_WAY,
    )
    LEVEL_5 = (
        "Level 5",
        LevelRegions.LEVELS_1_TO_4,
        LevelRegions.LEVELS_5_TO_9,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=5),
    )
    LEVEL_10 = (
        "Level 10",
        LevelRegions.LEVELS_5_TO_9,
        LevelRegions.LEVELS_10_TO_14,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=10),
    )
    LEVEL_15 = (
        "Level 15",
        LevelRegions.LEVELS_10_TO_14,
        LevelRegions.LEVELS_15_TO_19,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=15),
    )
    LEVEL_20 = (
        "Level 20",
        LevelRegions.LEVELS_15_TO_19,
        LevelRegions.LEVELS_20_TO_24,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=20),
    )
    LEVEL_25 = (
        "Level 25",
        LevelRegions.LEVELS_20_TO_24,
        LevelRegions.LEVELS_25_TO_29,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=25),
    )
    LEVEL_30 = (
        "Level 30",
        LevelRegions.LEVELS_25_TO_29,
        LevelRegions.LEVELS_30_TO_34,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=30),
    )
    LEVEL_35 = (
        "Level 35",
        LevelRegions.LEVELS_30_TO_34,
        LevelRegions.LEVELS_35_TO_39,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=35),
    )
    LEVEL_40 = (
        "Level 40",
        LevelRegions.LEVELS_35_TO_39,
        LevelRegions.LEVELS_40_TO_44,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=40),
    )
    LEVEL_45 = (
        "Level 45",
        LevelRegions.LEVELS_40_TO_44,
        LevelRegions.LEVELS_45_TO_49,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=45),
    )
    LEVEL_50 = (
        "Level 50",
        LevelRegions.LEVELS_45_TO_49,
        LevelRegions.LEVELS_50_TO_54,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=50),
    )
    LEVEL_55 = (
        "Level 55",
        LevelRegions.LEVELS_50_TO_54,
        LevelRegions.LEVELS_55_TO_59,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=55),
    )
    LEVEL_60 = (
        "Level 60",
        LevelRegions.LEVELS_55_TO_59,
        LevelRegions.LEVELS_60_TO_64,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=60),
    )
    LEVEL_65 = (
        "Level 65",
        LevelRegions.LEVELS_60_TO_64,
        LevelRegions.LEVELS_65_TO_69,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=65),
    )
    LEVEL_70 = (
        "Level 70",
        LevelRegions.LEVELS_65_TO_69,
        LevelRegions.LEVELS_70_TO_74,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=70),
    )
    LEVEL_75 = (
        "Level 75",
        LevelRegions.LEVELS_70_TO_74,
        LevelRegions.LEVELS_75_TO_79,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=75),
    )
    LEVEL_80 = (
        "Level 80",
        LevelRegions.LEVELS_75_TO_79,
        LevelRegions.LEVELS_80_TO_84,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=80),
    )
    LEVEL_85 = (
        "Level 85",
        LevelRegions.LEVELS_80_TO_84,
        LevelRegions.LEVELS_85_TO_89,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=85),
    )
    LEVEL_90 = (
        "Level 90",
        LevelRegions.LEVELS_85_TO_89,
        LevelRegions.LEVELS_90_TO_94,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=90),
    )
    LEVEL_95 = (
        "Level 95",
        LevelRegions.LEVELS_90_TO_94,
        LevelRegions.LEVELS_95_TO_99,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=95),
    )
    LEVEL_100 = (
        "Level 100",
        LevelRegions.LEVELS_95_TO_99,
        LevelRegions.LEVEL_100,
        EntranceType.ONE_WAY,
        HasLicensesForLevel(level=100),
    )

class PackEntrances(EntranceTypeEnum):
    GENERIC_OPEN_PACKS = (
        "Open Any Card Packs",
        DefaultRegions.MENU,
        GenericRegions.GENERIC_OPEN_PACKS,
        EntranceType.ONE_WAY,
    )

    GENERIC_SELL_CARDS = (
        "Sell Any Cards",
        GenericRegions.GENERIC_OPEN_PACKS,
        GenericRegions.GENERIC_SELL_CARDS,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )

    GENERIC_GRADE_CARDS = (
        "Grade Any Cards",
        GenericRegions.GENERIC_OPEN_PACKS,
        GenericRegions.GENERIC_GRADE_CARDS,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )
    # Tetramon Base - Basic
    BASIC_PACKS = (
        "Open Tetramon Base Basic Packs",
        DefaultRegions.MENU,
        PackRegions.BASIC_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX.value),
    )
    BASIC_PACKS_SELL = (
        "Sell Tetramon Base Basic Cards",
        PackRegions.BASIC_PACKS,
        PackRegions.BASIC_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    BASIC_PACKS_GRADE = (
        "Grade Tetramon Base Basic Cards",
        PackRegions.BASIC_PACKS,
        PackRegions.BASIC_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Base - Rare
    RARE_PACKS = (
        "Open Tetramon Base Rare Packs",
        DefaultRegions.MENU,
        PackRegions.RARE_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_BOX.value),
    )
    RARE_PACKS_SELL = (
        "Sell Tetramon Base Rare Cards",
        PackRegions.RARE_PACKS,
        PackRegions.RARE_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    RARE_PACKS_GRADE = (
        "Grade Tetramon Base Rare Cards",
        PackRegions.RARE_PACKS,
        PackRegions.RARE_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Base - Epic
    EPIC_PACKS = (
        "Open Tetramon Base Epic Packs",
        DefaultRegions.MENU,
        PackRegions.EPIC_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_BOX.value),
    )
    EPIC_PACKS_SELL = (
        "Sell Tetramon Base Epic Cards",
        PackRegions.EPIC_PACKS,
        PackRegions.EPIC_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    EPIC_PACKS_GRADE = (
        "Grade Tetramon Base Epic Cards",
        PackRegions.EPIC_PACKS,
        PackRegions.EPIC_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Base - Legendary
    LEGENDARY_PACKS = (
        "Open Tetramon Base Legendary Packs",
        DefaultRegions.MENU,
        PackRegions.LEGENDARY_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_BOX.value),
    )
    LEGENDARY_PACKS_SELL = (
        "Sell Tetramon Base Legendary Cards",
        PackRegions.LEGENDARY_PACKS,
        PackRegions.LEGENDARY_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    LEGENDARY_PACKS_GRADE = (
        "Grade Tetramon Base Legendary Cards",
        PackRegions.LEGENDARY_PACKS,
        PackRegions.LEGENDARY_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Destiny - Basic
    DESTINY_BASIC_PACKS = (
        "Open Tetramon Destiny Basic Packs",
        DefaultRegions.MENU,
        PackRegions.DESTINY_BASIC_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_BOX.value),
    )
    DESTINY_BASIC_PACKS_SELL = (
        "Sell Tetramon Destiny Basic Cards",
        PackRegions.DESTINY_BASIC_PACKS,
        PackRegions.DESTINY_BASIC_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    DESTINY_BASIC_PACKS_GRADE = (
        "Grade Tetramon Destiny Basic Cards",
        PackRegions.DESTINY_BASIC_PACKS,
        PackRegions.DESTINY_BASIC_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Destiny - Rare
    DESTINY_RARE_PACKS = (
        "Open Tetramon Destiny Rare Packs",
        DefaultRegions.MENU,
        PackRegions.DESTINY_RARE_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_BOX.value),
    )
    DESTINY_RARE_PACKS_SELL = (
        "Sell Tetramon Destiny Rare Cards",
        PackRegions.DESTINY_RARE_PACKS,
        PackRegions.DESTINY_RARE_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    DESTINY_RARE_PACKS_GRADE = (
        "Grade Tetramon Destiny Rare Cards",
        PackRegions.DESTINY_RARE_PACKS,
        PackRegions.DESTINY_RARE_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Destiny - Epic
    DESTINY_EPIC_PACKS = (
        "Open Tetramon Destiny Epic Packs",
        DefaultRegions.MENU,
        PackRegions.DESTINY_EPIC_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_BOX.value),
    )
    DESTINY_EPIC_PACKS_SELL = (
        "Sell Tetramon Destiny Epic Cards",
        PackRegions.DESTINY_EPIC_PACKS,
        PackRegions.DESTINY_EPIC_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    DESTINY_EPIC_PACKS_GRADE = (
        "Grade Tetramon Destiny Epic Cards",
        PackRegions.DESTINY_EPIC_PACKS,
        PackRegions.DESTINY_EPIC_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

    # Tetramon Destiny - Legendary
    DESTINY_LEGENDARY_PACKS = (
        "Open Tetramon Destiny Legendary Packs",
        DefaultRegions.MENU,
        PackRegions.DESTINY_LEGENDARY_PACKS,
        EntranceType.ONE_WAY,
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_PACK.value)
        | Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_BOX.value),
    )
    DESTINY_LEGENDARY_PACKS_SELL = (
        "Sell Tetramon Destiny Legendary Cards",
        PackRegions.DESTINY_LEGENDARY_PACKS,
        PackRegions.DESTINY_LEGENDARY_PACKS_SELL,
        EntranceType.ONE_WAY,
        Has(DIYItems.PROGRESSIVE_CARD_TABLE.value),
    )
    DESTINY_LEGENDARY_PACKS_GRADE = (
        "Grade Tetramon Destiny Legendary Cards",
        PackRegions.DESTINY_LEGENDARY_PACKS,
        PackRegions.DESTINY_LEGENDARY_PACKS_GRADE,
        EntranceType.ONE_WAY,
        Has(Blockers.GRADING_UNLOCK.value),
    )

pack_regions: dict[
    PackRegions,
    tuple[
        tuple[ItemTypeEnum, ItemTypeEnum],
        PackRegions,
        PackRegions,
    ],
] = {
    PackRegions.BASIC_PACKS: (
        (
            BoosterPackItems.PROGRESSIVE_BASIC_CARD_PACK,
            BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX,
        ),
        PackRegions.BASIC_PACKS_SELL,
        PackRegions.BASIC_PACKS_GRADE,
    ),
    PackRegions.RARE_PACKS: (
        (
            BoosterPackItems.PROGRESSIVE_RARE_CARD_PACK,
            BoosterPackItems.PROGRESSIVE_RARE_CARD_BOX,
        ),
        PackRegions.RARE_PACKS_SELL,
        PackRegions.RARE_PACKS_GRADE,
    ),
    PackRegions.EPIC_PACKS: (
        (
            BoosterPackItems.PROGRESSIVE_EPIC_CARD_PACK,
            BoosterPackItems.PROGRESSIVE_EPIC_CARD_BOX,
        ),
        PackRegions.EPIC_PACKS_SELL,
        PackRegions.EPIC_PACKS_GRADE,
    ),
    PackRegions.LEGENDARY_PACKS: (
        (
            BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_PACK,
            BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_BOX,
        ),
        PackRegions.LEGENDARY_PACKS_SELL,
        PackRegions.LEGENDARY_PACKS_GRADE,
    ),

    PackRegions.DESTINY_BASIC_PACKS: (
        (
            BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_PACK,
            BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_BOX,
        ),
        PackRegions.DESTINY_BASIC_PACKS_SELL,
        PackRegions.DESTINY_BASIC_PACKS_GRADE,
    ),
    PackRegions.DESTINY_RARE_PACKS: (
        (
            BoosterPackItems.PROGRESSIVE_RARE_DESTINY_PACK,
            BoosterPackItems.PROGRESSIVE_RARE_DESTINY_BOX,
        ),
        PackRegions.DESTINY_RARE_PACKS_SELL,
        PackRegions.DESTINY_RARE_PACKS_GRADE,
    ),
    PackRegions.DESTINY_EPIC_PACKS: (
        (
            BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_PACK,
            BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_BOX,
        ),
        PackRegions.DESTINY_EPIC_PACKS_SELL,
        PackRegions.DESTINY_EPIC_PACKS_GRADE,
    ),
    PackRegions.DESTINY_LEGENDARY_PACKS: (
        (
            BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_PACK,
            BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_BOX,
        ),
        PackRegions.DESTINY_LEGENDARY_PACKS_SELL,
        PackRegions.DESTINY_LEGENDARY_PACKS_GRADE,
    ),
}