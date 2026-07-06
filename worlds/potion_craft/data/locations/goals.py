from .. import LocationTypeEnum
from ..regions.chapters import ChapterRegions
from ...constants import CHAPTER_COMPLETE_OFFSET


class ChapterCompletes(LocationTypeEnum):
    COMPLETE_CHAPTER_1 = ("Complete Chapter 1", CHAPTER_COMPLETE_OFFSET + 0, ChapterRegions.CHAPTER_1)
    COMPLETE_CHAPTER_2 = ("Complete Chapter 2", CHAPTER_COMPLETE_OFFSET + 1, ChapterRegions.CHAPTER_2)
    COMPLETE_CHAPTER_3 = ("Complete Chapter 3", CHAPTER_COMPLETE_OFFSET + 2, ChapterRegions.CHAPTER_3)
    COMPLETE_CHAPTER_4 = ("Complete Chapter 4", CHAPTER_COMPLETE_OFFSET + 3, ChapterRegions.CHAPTER_4)
    COMPLETE_CHAPTER_5 = ("Complete Chapter 5", CHAPTER_COMPLETE_OFFSET + 4, ChapterRegions.CHAPTER_5)
    COMPLETE_CHAPTER_6 = ("Complete Chapter 6", CHAPTER_COMPLETE_OFFSET + 5, ChapterRegions.CHAPTER_6)
    COMPLETE_CHAPTER_7 = ("Complete Chapter 7", CHAPTER_COMPLETE_OFFSET + 6, ChapterRegions.CHAPTER_7)
    COMPLETE_CHAPTER_8 = ("Complete Chapter 8", CHAPTER_COMPLETE_OFFSET + 7, ChapterRegions.CHAPTER_8)
    COMPLETE_CHAPTER_9 = ("Complete Chapter 9", CHAPTER_COMPLETE_OFFSET + 8, ChapterRegions.CHAPTER_9)
    COMPLETE_CHAPTER_10 = ("Complete Chapter 10", CHAPTER_COMPLETE_OFFSET + 9, ChapterRegions.CHAPTER_10)

class Chapter1LocationType(LocationTypeEnum):
    GRAB_AN_INGREDIENT_FROM_INVENTORY = ("Grab an ingredient from Inventory", 1, ChapterRegions.CHAPTER_1_GOALS)
    GRIND_AN_INGREDIENT = ("Grind an Ingredient", 2, ChapterRegions.CHAPTER_1_GOALS)
    TOSS_INGREDIENT_IN_CAULDRON = ("Toss Ingredient in Cauldron", 3, ChapterRegions.CHAPTER_1_GOALS)
    STIR_CAULDRON = ("Stir Cauldron", 4, ChapterRegions.CHAPTER_1_GOALS)
    HEAT_CAULDRON = ("Heat Cauldron", 5, ChapterRegions.CHAPTER_1_GOALS)
    CRAFT_A_POTION = ("Craft a Potion", 6, ChapterRegions.CHAPTER_1_GOALS)
    GO_TO_GARDEN = ("Go to Garden", 7, ChapterRegions.CHAPTER_1_GOALS)
    GATHER_INGREDIENTS = ("Gather Ingredients", 8, ChapterRegions.CHAPTER_1_GOALS)
    GO_TO_SHOP = ("Go to Shop", 9, ChapterRegions.CHAPTER_1_GOALS)
    SELL_A_POTION = ("Sell a Potion", 10, ChapterRegions.CHAPTER_1_GOALS)
    BUY_FROM_MERCHANT = ("Buy From Merchant", 11, ChapterRegions.CHAPTER_1_GOALS)
    COLLECT_SMALL_EXPERIENCE = ("Collect Small Experience", 12, ChapterRegions.CHAPTER_1_GOALS)
    LEARN_NEW_TALENT = ("Learn New Talent", 13, ChapterRegions.CHAPTER_1_GOALS)
    GO_TO_BASEMENT = ("Go to Basement", 14, ChapterRegions.CHAPTER_1_GOALS)
    GO_TO_BEDROOM = ("Go to Bedroom", 15, ChapterRegions.CHAPTER_1_GOALS)
    START_A_NEW_DAY = ("Start a New Day", 16, ChapterRegions.CHAPTER_1_GOALS)
    REACH_POPULARITY_LEVEL_2 = ("Reach Popularity Level 2", 17, ChapterRegions.CHAPTER_1_GOALS)
    CREATE_POTION_OF_HEALING = ("Create Potion of Healing", 18, ChapterRegions.CHAPTER_1_GOALS)
    CREATE_POTION_OF_POISONING = ("Create Potion of Poisoning", 19, ChapterRegions.CHAPTER_1_GOALS)
    CREATE_POTION_OF_FIRE = ("Create Potion of Fire", 20, ChapterRegions.CHAPTER_1_GOALS)
    CREATE_POTION_OF_FROST = ("Create Potion of Frost", 21, ChapterRegions.CHAPTER_1_GOALS)


class Chapter2LocationType(LocationTypeEnum):
    USE_WATER = ("Use Water", 22, ChapterRegions.CHAPTER_2_GOALS)
    CREATE_A_TIER_2_OR_HIGHER_POTION = ("Create a Tier 2 Or Higher Potion", 23, ChapterRegions.CHAPTER_2_GOALS)
    CREATE_A_POTION_WITH_2_DIFFERENT_EFFECTS = ("Create a Potion with 2 different effects", 24, ChapterRegions.CHAPTER_2_GOALS)
    SAVE_A_NEW_RECIPE = ("Save a New Recipe", 25, ChapterRegions.CHAPTER_2_GOALS)
    BREW_A_POTION_FROM_RECIPE_BOOK = ("Brew a Potion From Recipe Book", 26, ChapterRegions.CHAPTER_2_GOALS)
    HAGGLE_FOR_A_BETTER_DEAL = ("Haggle For a Better Deal", 27, ChapterRegions.CHAPTER_2_GOALS)
    REACH_A_POPULARITY_LEVEL_OF_4 = ("Reach a Popularity Level Of 4", 28, ChapterRegions.CHAPTER_2_GOALS)
    COLLECT_SMALL_EXPERIENCE_ON_THE_ALCHEMY_MAP = ("Collect small experience on the Alchemy Map", 29, ChapterRegions.CHAPTER_2_GOALS)
    CREATE_POTION_OF_EXPLOSION = ("Create Potion of Explosion", 30, ChapterRegions.CHAPTER_2_GOALS)
    CREATE_POTION_OF_WILD_GROWTH = ("Create Potion of Wild Growth", 31, ChapterRegions.CHAPTER_2_GOALS)
    CREATE_POTION_OF_STRENGTH = ("Create Potion of Strength", 32, ChapterRegions.CHAPTER_2_GOALS)
    CREATE_POTION_OF_DEXTERITY = ("Create Potion of Dexterity", 33, ChapterRegions.CHAPTER_2_GOALS)
    CREATE_POTION_OF_SWIFTNESS = ("Create Potion of Swiftness", 34, ChapterRegions.CHAPTER_2_GOALS)

class Chapter3LocationType(LocationTypeEnum):
    REPAIR_THE_ALCHEMY_MACHINE = ("Repair the Alchemy Machine", 35, ChapterRegions.CHAPTER_3_GOALS)
    BUY_A_PAGE_FOR_THE_RECIPE_BOOK = ("Buy a page for the Recipe Book", 36, ChapterRegions.CHAPTER_3_GOALS)
    CREATE_A_POTION_WITH_EFFECT_OF_TIER_3 = ("Create a potion with effect of tier 3", 37, ChapterRegions.CHAPTER_3_GOALS)
    CREATE_A_POTION_WITH_3_DIFFERENT_EFFECTS = ("Create a potion with 3 different effects", 38, ChapterRegions.CHAPTER_3_GOALS)
    COLLECT_MEDIUM_EXPERIENCE_BOOK_ON_THE_ALCHEMY_MAP_3_BOOK_ICON = ("Collect medium experience book on the Alchemy Map (3 book icon)", 39, ChapterRegions.CHAPTER_3_GOALS)
    REACH_A_POPULARITY_LEVEL_OF_5 = ("Reach a popularity level of 5", 40, ChapterRegions.CHAPTER_3_GOALS)
    CREATE_A_POTION_WITH_CUSTOM_APPEARANCE_OR_NAME = ("Create a potion with custom appearance or name", 41, ChapterRegions.CHAPTER_3_GOALS)
    CREATE_POTION_OF_LIGHTNING = ("Create Potion of Lightning", 42, ChapterRegions.CHAPTER_3_GOALS)
    CREATE_POTION_OF_MANA = ("Create Potion of Mana", 43, ChapterRegions.CHAPTER_3_GOALS)
    CREATE_POTION_OF_STONE_SKIN = ("Create Potion of Stone Skin", 44, ChapterRegions.CHAPTER_3_GOALS)
    CREATE_POTION_OF_SLEEP = ("Create Potion of Sleep", 45, ChapterRegions.CHAPTER_3_GOALS)
    CREATE_POTION_OF_LIGHT = ("Create Potion of Light", 46, ChapterRegions.CHAPTER_3_GOALS)


class Chapter4LocationType(LocationTypeEnum):
    CREATE_NIGREDO = ("Create Nigredo", 47, ChapterRegions.CHAPTER_4_GOALS)
    CREATE_A_POTION_WITH_4_DIFFERENT_EFFECTS = ("Create a Potion with 4 different Effects", 48, ChapterRegions.CHAPTER_4_GOALS)
    REACH_POPULARITY_6 = ("Reach Popularity 6", 49, ChapterRegions.CHAPTER_4_GOALS)
    COLLECT_BIG_EXPERIENCE = ("Collect Big Experience", 50, ChapterRegions.CHAPTER_4_GOALS)
    CREATE_POTION_OF_CHARM = ("Create Potion of Charm", 51, ChapterRegions.CHAPTER_4_GOALS)
    CREATE_POTION_OF_SLOWNESS = ("Create Potion of Slowness", 52, ChapterRegions.CHAPTER_4_GOALS)
    CREATE_POTION_OF_RAGE = ("Create Potion of Rage", 53, ChapterRegions.CHAPTER_4_GOALS)
    CREATE_POTION_OF_MAGICAL_VISION = ("Create Potion of Magical Vision", 54, ChapterRegions.CHAPTER_4_GOALS)


class Chapter5LocationType(LocationTypeEnum):
    BUY_BASIC_ALCHEMY_MACHINE_UPGRADE = ("Buy Basic Alchemy Machine Upgrade", 55, ChapterRegions.CHAPTER_5_GOALS)
    BUY_VOID_SALT_RECIPE = ("Buy Void Salt Recipe", 56, ChapterRegions.CHAPTER_5_GOALS)
    CREATE_VOID_SALT = ("Create Void Salt", 57, ChapterRegions.CHAPTER_5_GOALS)
    CREATE_A_POTION_WITH_5_DIFFERENT_EFFECTS = ("Create a potion with 5 different effects", 58, ChapterRegions.CHAPTER_5_GOALS)
    COLLECT_VERY_BIG_EXPERIENCE = ("Collect Very Big Experience", 59, ChapterRegions.CHAPTER_5_GOALS)
    REACH_POPULARITY_7 = ("Reach Popularity 7", 60, ChapterRegions.CHAPTER_5_GOALS)
    CREATE_POTION_OF_ACID = ("Create Potion of Acid", 61, ChapterRegions.CHAPTER_5_GOALS)
    CREATE_POTION_OF_LIBIDO = ("Create Potion of Libido", 62, ChapterRegions.CHAPTER_5_GOALS)
    CREATE_POTION_OF_INVISIBILITY = ("Create Potion of Invisibility", 63, ChapterRegions.CHAPTER_5_GOALS)
    CREATE_POTION_OF_LEVITATION = ("Create Potion of Levitation", 64, ChapterRegions.CHAPTER_5_GOALS)
    CREATE_POTION_OF_NECROMANCY = ("Create Potion of Necromancy", 65, ChapterRegions.CHAPTER_5_GOALS)

class Chapter6LocationType(LocationTypeEnum):
    BUY_POTION_BASE_OIL = ("Buy Potion Base: Oil", 66, ChapterRegions.CHAPTER_6_GOALS)
    CREATE_ALBEDO = ("Create Albedo", 67, ChapterRegions.CHAPTER_6_GOALS)
    REACH_A_POPULARITY_LEVEL_OF_8 = ("Reach a popularity level of 8", 68, ChapterRegions.CHAPTER_6_GOALS)
    CREATE_POTION_OF_POISON_PROTECTION = ("Create Potion of Poison Protection", 69, ChapterRegions.CHAPTER_6_GOALS)
    CREATE_POTION_OF_LIGHTNING_PROTECTION = ("Create Potion of Lightning Protection", 70, ChapterRegions.CHAPTER_6_GOALS)
    CREATE_POTION_OF_FIRE_PROTECTION = ("Create Potion of Fire Protection", 71, ChapterRegions.CHAPTER_6_GOALS)
    CREATE_POTION_OF_FROST_PROTECTION = ("Create Potion of Frost Protection", 72, ChapterRegions.CHAPTER_6_GOALS)
    CREATE_POTION_OF_GLUING = ("Create Potion of Gluing", 73, ChapterRegions.CHAPTER_6_GOALS)
    CREATE_POTION_OF_SLIPPERINESS = ("Create Potion of Slipperiness", 74, ChapterRegions.CHAPTER_6_GOALS)
    CREATE_POTION_OF_STENCH = ("Create Potion of Stench", 75, ChapterRegions.CHAPTER_6_GOALS)


class Chapter7LocationType(LocationTypeEnum):
    BUY_ADVANCED_ALCHEMY_MACHINE = ("Buy Advanced Alchemy Machine", 76, ChapterRegions.CHAPTER_7_GOALS)
    BUY_THE_MOON_SALT_RECIPE = ("Buy the Moon Salt Recipe", 77, ChapterRegions.CHAPTER_7_GOALS)
    CREATE_MOON_SALT = ("Create Moon Salt", 78, ChapterRegions.CHAPTER_7_GOALS)
    REACH_A_POPULARITY_LEVEL_OF_9 = ("Reach a popularity level of 9", 79, ChapterRegions.CHAPTER_7_GOALS)
    CREATE_POTION_OF_ACID_PROTECTION = ("Create Potion of Acid Protection", 80, ChapterRegions.CHAPTER_7_GOALS)
    CREATE_POTION_OF_ANTI_MAGIC = ("Create Potion of Anti-Magic", 81, ChapterRegions.CHAPTER_7_GOALS)
    CREATE_POTION_OF_SHRINKING = ("Create Potion of Shrinking", 82, ChapterRegions.CHAPTER_7_GOALS)
    CREATE_POTION_OF_ENLARGEMENT = ("Create Potion of Enlargement", 83, ChapterRegions.CHAPTER_7_GOALS)
    CREATE_POTION_OF_REJUVENATION = ("Create Potion of Rejuvenation", 84, ChapterRegions.CHAPTER_7_GOALS)

class Chapter8LocationType(LocationTypeEnum):
    CREATE_CITRINITAS = ("Create Citrinitas", 85, ChapterRegions.CHAPTER_8_GOALS)
    REACH_POPULARITY_LEVEL_10 = ("Reach Popularity level 10", 86, ChapterRegions.CHAPTER_8_GOALS)
    CREATE_POTION_OF_INSPIRATION = ("Create Potion of Inspiration", 87, ChapterRegions.CHAPTER_8_GOALS)
    CREATE_POTION_OF_FRAGRANCE = ("Create Potion of Fragrance", 88, ChapterRegions.CHAPTER_8_GOALS)
    CREATE_POTION_OF_FEAR = ("Create Potion of Fear", 89, ChapterRegions.CHAPTER_8_GOALS)


class Chapter9LocationType(LocationTypeEnum):
    BUY_THE_SUN_SALT_RECIPE = ("Buy the Sun Salt recipe", 90, ChapterRegions.CHAPTER_9_GOALS)
    CREATE_SUN_SALT = ("Create Sun Salt", 91, ChapterRegions.CHAPTER_9_GOALS)
    CREATE_RUBEDO = ("Create Rubedo", 92, ChapterRegions.CHAPTER_9_GOALS)
    REACH_A_POPULARITY_LEVEL_OF_12 = ("Reach a popularity level of 12", 93, ChapterRegions.CHAPTER_9_GOALS)
    CREATE_POTION_OF_HALLUCINATIONS = ("Create Potion of Hallucinations", 94, ChapterRegions.CHAPTER_9_GOALS)
    CREATE_POTION_OF_LUCK = ("Create Potion of Luck", 95, ChapterRegions.CHAPTER_9_GOALS)
    CREATE_POTION_OF_CURSE = ("Create Potion of Curse", 96, ChapterRegions.CHAPTER_9_GOALS)


class Chapter10LocationType(LocationTypeEnum):
    CREATE_PHILOSOPHERS_STONE = ("Create Philosopher's Stone", 97, ChapterRegions.CHAPTER_10_GOALS)
    BUY_THE_LIFE_SALT_RECIPE = ("Buy the Life Salt recipe", 98, ChapterRegions.CHAPTER_10_GOALS)
    CREATE_LIFE_SALT = ("Create Life Salt", 99, ChapterRegions.CHAPTER_10_GOALS)
    BUY_THE_PHILOSOPHERS_SALT_RECIPE = ("Buy the Philosopher's Salt recipe", 100, ChapterRegions.CHAPTER_10_GOALS)
    CREATE_PHILOSOPHERS_SALT = ("Create Philosopher's Salt", 101, ChapterRegions.CHAPTER_10_GOALS)
    REACH_A_POPULARITY_LEVEL_OF_15 = ("Reach a popularity level of 15", 102, ChapterRegions.CHAPTER_10_GOALS)