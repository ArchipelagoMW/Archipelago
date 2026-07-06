from BaseClasses import ItemClassification
from .. import ItemTypeEnum


class TalentType(ItemTypeEnum):
    # Trading Start
    TRADING = ("Trading", 100, ItemClassification.useful)
    IRREPRESSIBLE_SELLER = ("Irrepressible Seller", 101, ItemClassification.useful)
    CHARISMA = ("Charisma", 102, ItemClassification.useful)
    GREAT_POTION_DEMAND = ("Great Potion Demand", 103, ItemClassification.useful)
    ADVERTISING_MASTER = ("Advertising Master", 104, ItemClassification.useful)
    PERFECT_HAGGLING = ("Perfect Haggling", 105, ItemClassification.useful)
    HAGGLING_OVER_COMPLEX_TOPICS = ("Haggling over complex topics", 106, ItemClassification.useful)
    HAGGLING_OVER_EXTREMELY_COMPLEX_TOPICS = ("Haggling over extremely complex topics", 107, ItemClassification.useful)
    UNHURRIED_HAGGLING = ("Unhurried Haggling", 108, ItemClassification.useful)
    ACCOMMODATING_HAGGLING = ("Accommodating Haggling", 109, ItemClassification.useful)
    CALMING_HAGGLING_MANNER = ("Calming Haggling Manner", 110, ItemClassification.useful)
    GOOD_POTION_SELLER = ("Good Potion Seller", 111, ItemClassification.useful)
    BEST_SIMPLE_POTION_SELLER = ("Best Simple Potion Seller", 112, ItemClassification.useful)
    SELLING_POTIONS_TO_MERCHANTS = ("Selling Potions to Merchants", 113, ItemClassification.useful)
    FRIENDSHIP_WITH_MERCHANTS = ("Friendship with Merchants", 114, ItemClassification.useful)
    INCREASED_DISCOUNT_CHANCE = ("Increased Discount Chance", 115, ItemClassification.useful)
    REDUCED_MARKUP_CHANCE = ("Reduced Markup Chance", 116, ItemClassification.useful)
    SKILLED_MANIPULATOR = ("Skilled Manipulator", 117, ItemClassification.useful)
    TALENTED_POTION_SELLER = ("Talented Potion Seller", 118, ItemClassification.useful)
    # Trading End

    # Gardening Start
    FERTILIZING_HERBS_AND_MUSHROOMS_WITH_POTIONS = ("Fertilizing Herbs and Mushrooms with Potions", 119, ItemClassification.progression)
    CAREFUL_HERB_CARE = ("Careful Herb Care", 120, ItemClassification.useful)
    CAREFUL_MUSHROOM_CARE = ("Careful Mushroom Care", 121, ItemClassification.useful)
    CAREFUL_CRYSTAL_CARE = ("Careful Crystal Care", 122, ItemClassification.useful)
    HERBALISM = ("Herbalism", 123, ItemClassification.useful)
    WILDLY_OVERGROWN_HERB_HARVESTING = ("Wildly Overgrown Herb Harvesting", 124, ItemClassification.useful)
    MUSHROOM_HARVESTING = ("Mushroom Harvesting", 125, ItemClassification.useful)
    WILDLY_OVERGROWN_MUSHROOM_HARVESTING = ("Wildly Overgrown Mushroom Harvesting", 126, ItemClassification.useful)
    CRYSTAL_HARVESTING = ("Crystal Harvesting", 127, ItemClassification.useful)
    WILDLY_OVERGROWN_CRYSTAL_HARVESTING = ("Wildly Overgrown Crystal Harvesting", 128, ItemClassification.useful)
    GOLD_DIGGER = ("Gold Digger", 129, ItemClassification.useful)
    GOLD_FEVER = ("Gold Fever", 130, ItemClassification.useful)
    HERB_PLANTING = ("Herb Planting", 131, ItemClassification.progression)
    HERB_REPLANTING = ("Herb Replanting", 132, ItemClassification.progression)
    HERB_SEED_HARVESTING = ("Herb Seed Harvesting", 133, ItemClassification.useful)
    QUICK_HERB_GROWTH = ("Quick Herb Growth", 134, ItemClassification.useful)
    UNDERWATER_GROWING = ("Underwater Growing", 135, ItemClassification.progression)
    CAVE_HERBS = ("Cave Herbs", 136, ItemClassification.progression)
    MUSHROOM_PLANTING = ("Mushroom Planting", 137, ItemClassification.useful)
    MUSHROOM_REPLANTING = ("Mushroom Replanting", 138, ItemClassification.useful)
    MYCELIUM_HARVESTING = ("Mycelium Harvesting", 139, ItemClassification.useful)
    QUICK_MUSHROOM_GROWTH = ("Quick Mushroom Growth", 140, ItemClassification.useful)
    TRUFFLE_GROWING = ("Truffle Growing", 141, ItemClassification.progression)
    CRYSTAL_PLANTING = ("Crystal Planting", 142, ItemClassification.progression)
    CRYSTAL_REPLANTING = ("Crystal Replanting", 143, ItemClassification.progression)
    CRYSTAL_SEED_HARVESTING = ("Crystal Seed Harvesting", 144, ItemClassification.useful)
    QUICK_CRYSTAL_GROWTH = ("Quick Crystal Growth", 145, ItemClassification.useful)
    FERTILIZING_CRYSTALS_WITH_POTIONS = ("Fertilizing Crystals with Potions", 146, ItemClassification.useful)
    # Gardening End

    # Alchemy Start
    BULK_BREWING = ("Bulk Brewing", 147, ItemClassification.useful)
    ALCHEMICAL_PRACTICE = ("Alchemical Practice", 148, ItemClassification.useful)
    PRECIOUS_RESIDUE = ("Precious Residue", 149, ItemClassification.useful)
    ALCHEMY_MAP_VISIBILITY_RADIUS = ("Alchemy Map: Visibility Radius", 150, ItemClassification.useful)
    THE_KEY_IS_TO_PULL_IT_OUT_JUST_IN_TIME = ("The key is to pull it out just in time", 151, ItemClassification.useful)
    BETTER_RESTORE_SALT = ("Better Restore Salt", 152, ItemClassification.useful)
    SALT_SPECIALIST = ("Salt Specialist", 153, ItemClassification.useful)
    # Alchemy End / Talents End