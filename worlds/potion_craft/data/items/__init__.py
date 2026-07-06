from typing import List

from BaseClasses import ItemClassification
from .potions import PotionEffectType
from .talents import TalentType
from .. import ItemData, IngredientData, Direction, ItemTypeEnum, ItemFiller
from .ingredients import IngredientType


class KeyItemType(ItemTypeEnum):
    PROGRESSIVE_ALCHEMY_MACHINE = ("Progressive Alchemy Machine",500,ItemClassification.progression)
    PROGRESSIVE_GARDEN = ("Progressive Garden",501,ItemClassification.progression)
    RECIPE_PAGE = ("Recipe Page",502, ItemClassification.useful)
    PROGRESSIVE_SALT = ("Progressive Salt", 503,ItemClassification.progression)
    PROGRESSIVE_CRYSTAL_RECIPE = ("Progressive Crystal Recipe",504, ItemClassification.progression)
    PROGRESSIVE_POTION_BASE = ("Progressive Potion Base",505,ItemClassification.progression)

class JunkItemType(ItemTypeEnum):
    XP = ("Xp", 1000, ItemClassification.filler)
    MONEY = ("Money", 1001, ItemClassification.filler)
    BULK_NORTH_INGREDIENT_BUNDLE = ("Bulk North Ingredient Bundle",1002,ItemClassification.filler)
    BULK_EAST_INGREDIENT_BUNDLE = ("Bulk East Ingredient Bundle",1003, ItemClassification.filler)
    BULK_SOUTH_INGREDIENT_BUNDLE = ( "Bulk South Ingredient Bundle",1004,ItemClassification.filler)
    BULK_WEST_INGREDIENT_BUNDLE = ("Bulk West Ingredient Bundle",1005, ItemClassification.filler)

key_items = [
    ItemData(item)
    for item in KeyItemType
]

junk_items = [
    ItemData(item)
    for item in JunkItemType
]

junk_fillers = [
    ItemFiller(JunkItemType.XP, 50),
    ItemFiller(JunkItemType.MONEY, 50),
    ItemFiller(JunkItemType.BULK_NORTH_INGREDIENT_BUNDLE, 20),
    ItemFiller(KeyItemType.RECIPE_PAGE)
]

ingredient_data: list[IngredientData] = [
    IngredientData(IngredientType.WINDBLOOM, 1, [Direction.NORTH]),
    IngredientData(IngredientType.WATERBLOOM, 1, [Direction.EAST]),
    IngredientData(IngredientType.TERRARIA, 1, [Direction.SOUTH]),
    IngredientData(IngredientType.TANGLEWEED, 1, [Direction.EAST]),
    IngredientData(IngredientType.LIFELEAF, 1, [Direction.EAST, Direction.SOUTH]),
    IngredientData(IngredientType.FIREBELL, 1, [Direction.WEST]),
    IngredientData(IngredientType.THUNDER_THISTLE, 2, [Direction.WEST, Direction.SOUTH]),
    IngredientData(IngredientType.ICEFRUIT, 2, [Direction.NORTH, Direction.SOUTH, Direction.EAST]),
    IngredientData(IngredientType.HAIRY_BANANA, 2, [Direction.SOUTH, Direction.WEST]),
    IngredientData(IngredientType.GOODBERRY, 2, [Direction.EAST, Direction.SOUTH]),
    IngredientData(IngredientType.GOLDTHORN, 2, [Direction.SOUTH, Direction.EAST]),
    IngredientData(IngredientType.LAVA_ROOT, 3, [Direction.WEST]),
    IngredientData(IngredientType.FEATHERBLOOM, 3, [Direction.NORTH]),
    IngredientData(IngredientType.DRUIDS_ROSEMARY, 3, [Direction.SOUTH, Direction.EAST]),
    IngredientData(IngredientType.DREAM_BEET, 3, [Direction.EAST, Direction.NORTH]),
    IngredientData(IngredientType.BLOODTHORN, 3, [Direction.NORTH, Direction.WEST]),
    IngredientData(IngredientType.WHIRLWEED, 4, [Direction.NORTH]),
    IngredientData(IngredientType.THORNSTICK, 4, [Direction.SOUTH, Direction.WEST]),
    IngredientData(IngredientType.GRASPING_ROOT, 4, [Direction.NORTH, Direction.WEST]),
    IngredientData(IngredientType.FLAMEWEED, 4, [Direction.WEST]),
    IngredientData(IngredientType.COLDLEAF, 4, [Direction.EAST]),
    IngredientData(IngredientType.SPELLBLOOM, 5, [Direction.NORTH, Direction.EAST]),
    IngredientData(IngredientType.HEALERS_HEATHER, 5, [Direction.SOUTH, Direction.EAST]),
    IngredientData(IngredientType.FLUFFBLOOM, 5, [Direction.NORTH, Direction.EAST]),
    IngredientData(IngredientType.DRAGON_PEPPER, 5, [Direction.SOUTH, Direction.WEST, Direction.NORTH]),
    IngredientData(IngredientType.BOOMBLOOM, 5, [Direction.NORTH, Direction.WEST]),
    IngredientData(IngredientType.TERROR_BUD, 6, [Direction.SOUTH, Direction.WEST, Direction.NORTH]),
    IngredientData(IngredientType.MAGEBERRY, 6, [Direction.EAST, Direction.NORTH]),
    IngredientData(IngredientType.EVERGREEN_FERN, 6, [Direction.EAST, Direction.SOUTH]),

    IngredientData(IngredientType.DRYADS_SADDLE, 1, [Direction.SOUTH]),
    IngredientData(IngredientType.MAD_MUSHROOM, 1, [Direction.NORTH, Direction.WEST]),
    IngredientData(IngredientType.MARSHROOM, 1, [Direction.SOUTH, Direction.EAST]),
    IngredientData(IngredientType.MUDSHROOM, 1, [Direction.SOUTH]),
    IngredientData(IngredientType.STINK_MUSHROOM, 1, [Direction.NORTH, Direction.EAST]),
    IngredientData(IngredientType.SULPHUR_SHELF, 1, [Direction.WEST]),
    IngredientData(IngredientType.WITCH_MUSHROOM, 1, [Direction.SOUTH, Direction.WEST]),
    IngredientData(IngredientType.SHADOW_CHANTERELLE, 2, [Direction.NORTH, Direction.EAST]),
    IngredientData(IngredientType.WEIRDSHROOM, 2, [Direction.SOUTH, Direction.EAST]),
    IngredientData(IngredientType.FOGGY_PARASOL, 3, [Direction.NORTH]),
    IngredientData(IngredientType.GOBLIN_SHROOM, 3, [Direction.SOUTH, Direction.WEST]),
    IngredientData(IngredientType.MOSS_SHROOM, 3, [Direction.SOUTH, Direction.EAST]),
    IngredientData(IngredientType.PHANTOM_SKIRT, 4, [Direction.NORTH, Direction.EAST, Direction.WEST]),
    IngredientData(IngredientType.POOPSHROOM, 4, [Direction.SOUTH]),
    IngredientData(IngredientType.WATERCAP, 4, [Direction.EAST]),
    IngredientData(IngredientType.KRAKEN_MUSHROOM, 5, [Direction.EAST]),
    IngredientData(IngredientType.LUST_MUSHROOM, 5, [Direction.SOUTH]),
    IngredientData(IngredientType.MAGMA_MOREL, 5, [Direction.EAST]),
    IngredientData(IngredientType.GRAVE_TRUFFLE, 6, [Direction.SOUTH, Direction.WEST]),
    IngredientData(IngredientType.RAINBOW_CAP, 6, [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]),

    IngredientData(IngredientType.CLOUD_CRYSTAL, 2, [Direction.NORTH]),
    IngredientData(IngredientType.EARTH_PYRITE, 2, [Direction.SOUTH]),
    IngredientData(IngredientType.FROST_SAPPHIRE, 2, [Direction.EAST]),
    IngredientData(IngredientType.FIRE_CITRINE, 2, [Direction.WEST]),
    IngredientData(IngredientType.BLOOD_RUBY, 3, [Direction.NORTH, Direction.WEST]),
    IngredientData(IngredientType.ARCANE_CRYSTAL, 4, [Direction.NORTH, Direction.EAST]),
    IngredientData(IngredientType.LIFE_CRYSTAL, 5, [Direction.SOUTH, Direction.EAST]),
    IngredientData(IngredientType.PLAGUE_STIBNITE, 6, [Direction.SOUTH, Direction.WEST]),
    IngredientData(IngredientType.FABLE_BISMUTH, 7, [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]),
]

progressive_items: list[ItemData] = [
    ItemData(KeyItemType.PROGRESSIVE_ALCHEMY_MACHINE, 4),
    ItemData(KeyItemType.PROGRESSIVE_GARDEN, 3),
    ItemData(KeyItemType.PROGRESSIVE_SALT, 3),
    ItemData(KeyItemType.PROGRESSIVE_CRYSTAL_RECIPE, 3),
    ItemData(KeyItemType.PROGRESSIVE_POTION_BASE, 2),
]


all_items: list[ItemTypeEnum] = [
    *JunkItemType,
    *KeyItemType,
    *IngredientType,
    *PotionEffectType,
    *TalentType
]

item_name_to_type = {
    item.value: item
    for item in all_items
}

def get_ingredients_by_direction(direction: Direction) -> List[ItemTypeEnum]:

    return [
        data.type
        for data in ingredient_data
        if data.direction is not None and direction in data.direction
    ]