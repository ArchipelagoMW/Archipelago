from BaseClasses import ItemClassification
from .. import ItemTypeEnum
from ...constants import ITEMS_PROGRESSIVE_LICENSE_OFFSET, ITEMS_LICENSE_OFFSET


class ProgressiveLicenses(ItemTypeEnum):
    PROGRESSIVE_BOOSTER_PACK_LICENSE = ("Progressive Booster Pack Shop License", ITEMS_PROGRESSIVE_LICENSE_OFFSET + 0, ItemClassification.progression)
    PROGRESSIVE_ACCESSORIES_LICENSE = ( "Progressive Accessories Shop License", ITEMS_PROGRESSIVE_LICENSE_OFFSET + 1, ItemClassification.progression)
    PROGRESSIVE_FIGURINE_LICENSE = ("Progressive Figurine Shop License", ITEMS_PROGRESSIVE_LICENSE_OFFSET + 2, ItemClassification.progression)
    PROGRESSIVE_TABLETOP_LICENSE = ("Progressive Tabletop Shop License", ITEMS_PROGRESSIVE_LICENSE_OFFSET + 3, ItemClassification.progression)

class BoosterPackItems(ItemTypeEnum):
    PROGRESSIVE_BASIC_CARD_PACK = ("Progressive Basic Card Pack", ITEMS_LICENSE_OFFSET + 0, ItemClassification.progression)
    PROGRESSIVE_BASIC_CARD_BOX = ("Progressive Basic Card Box", ITEMS_LICENSE_OFFSET + 1, ItemClassification.progression)
    PROGRESSIVE_RARE_CARD_PACK = ("Progressive Rare Card Pack", ITEMS_LICENSE_OFFSET + 2, ItemClassification.progression)
    PROGRESSIVE_RARE_CARD_BOX = ("Progressive Rare Card Box", ITEMS_LICENSE_OFFSET + 3, ItemClassification.progression)
    PROGRESSIVE_EPIC_CARD_PACK = ("Progressive Epic Card Pack", ITEMS_LICENSE_OFFSET + 4, ItemClassification.progression)
    PROGRESSIVE_EPIC_CARD_BOX = ("Progressive Epic Card Box", ITEMS_LICENSE_OFFSET + 5, ItemClassification.progression)
    PROGRESSIVE_LEGENDARY_CARD_PACK = ("Progressive Legendary Card Pack", ITEMS_LICENSE_OFFSET + 6, ItemClassification.progression)
    PROGRESSIVE_LEGENDARY_CARD_BOX = ("Progressive Legendary Card Box", ITEMS_LICENSE_OFFSET + 7, ItemClassification.progression)
    PROGRESSIVE_BASIC_DESTINY_PACK = ("Progressive Basic Destiny Pack", ITEMS_LICENSE_OFFSET + 8, ItemClassification.progression)
    PROGRESSIVE_BASIC_DESTINY_BOX = ("Progressive Basic Destiny Box", ITEMS_LICENSE_OFFSET + 9, ItemClassification.progression)
    PROGRESSIVE_RARE_DESTINY_PACK = ("Progressive Rare Destiny Pack", ITEMS_LICENSE_OFFSET + 10, ItemClassification.progression)
    PROGRESSIVE_RARE_DESTINY_BOX = ("Progressive Rare Destiny Box", ITEMS_LICENSE_OFFSET + 11, ItemClassification.progression)
    PROGRESSIVE_EPIC_DESTINY_PACK = ("Progressive Epic Destiny Pack", ITEMS_LICENSE_OFFSET + 12, ItemClassification.progression)
    PROGRESSIVE_EPIC_DESTINY_BOX = ("Progressive Epic Destiny Box", ITEMS_LICENSE_OFFSET + 13, ItemClassification.progression)
    PROGRESSIVE_LEGENDARY_DESTINY_PACK = ("Progressive Legendary Destiny Pack", ITEMS_LICENSE_OFFSET + 14, ItemClassification.progression)
    PROGRESSIVE_LEGENDARY_DESTINY_BOX = ("Progressive Legendary Destiny Box", ITEMS_LICENSE_OFFSET + 15, ItemClassification.progression)
    PROGRESSIVE_ASCENSION_PACK = ("Progressive Ascension Card Pack", ITEMS_LICENSE_OFFSET + 129, ItemClassification.progression)

    FIRE_BATTLE_DECK = ("Fire Battle Deck", ITEMS_LICENSE_OFFSET + 55, ItemClassification.progression)
    EARTH_BATTLE_DECK = ("Earth Battle Deck", ITEMS_LICENSE_OFFSET + 56, ItemClassification.progression)
    WATER_BATTLE_DECK = ("Water Battle Deck", ITEMS_LICENSE_OFFSET + 57, ItemClassification.progression)
    WIND_BATTLE_DECK = ("Wind Battle Deck", ITEMS_LICENSE_OFFSET + 58, ItemClassification.progression)
    FIRE_DESTINY_DECK = ("Fire Destiny Deck", ITEMS_LICENSE_OFFSET + 59, ItemClassification.progression)
    EARTH_DESTINY_DECK = ("Earth Destiny Deck", ITEMS_LICENSE_OFFSET + 60, ItemClassification.progression)
    WATER_DESTINY_DECK = ("Water Destiny Deck", ITEMS_LICENSE_OFFSET + 61, ItemClassification.progression)
    WIND_DESTINY_DECK = ("Wind Destiny Deck", ITEMS_LICENSE_OFFSET + 62, ItemClassification.progression)


class AccessoriesItems(ItemTypeEnum):
    PROGRESSIVE_CLEANSER = ("Progressive Cleanser", ITEMS_LICENSE_OFFSET + 23, ItemClassification.progression)

    CARD_SLEEVES_CLEAR = ("Card Sleeves (Clear)", ITEMS_LICENSE_OFFSET + 63, ItemClassification.progression)
    CARD_SLEEVES_TETRAMON = ("Card Sleeves (Tetramon)", ITEMS_LICENSE_OFFSET + 64, ItemClassification.progression)
    D20_DICE_RED = ("D20 Dice Red", ITEMS_LICENSE_OFFSET + 29, ItemClassification.progression)
    D20_DICE_BLUE = ("D20 Dice Blue", ITEMS_LICENSE_OFFSET + 30, ItemClassification.progression)
    D20_DICE_BLACK = ("D20 Dice Black", ITEMS_LICENSE_OFFSET + 31, ItemClassification.progression)
    D20_DICE_WHITE = ("D20 Dice White", ITEMS_LICENSE_OFFSET + 32, ItemClassification.progression)
    CARD_SLEEVES_FIRE = ("Card Sleeves (Fire)", ITEMS_LICENSE_OFFSET + 65, ItemClassification.progression)
    CARD_SLEEVES_EARTH = ("Card Sleeves (Earth)", ITEMS_LICENSE_OFFSET + 66, ItemClassification.progression)
    CARD_SLEEVES_WATER = ("Card Sleeves (Water)", ITEMS_LICENSE_OFFSET + 67, ItemClassification.progression)
    CARD_SLEEVES_WIND = ("Card Sleeves (Wind)", ITEMS_LICENSE_OFFSET + 68, ItemClassification.progression)

    PROGRESSIVE_DECK_BOX_RED = ("Progressive Deck Box Red", ITEMS_LICENSE_OFFSET + 24, ItemClassification.progression)
    PROGRESSIVE_DECK_BOX_GREEN = ("Progressive Deck Box Green", ITEMS_LICENSE_OFFSET + 25, ItemClassification.progression)
    PROGRESSIVE_DECK_BOX_BLUE = ("Progressive Deck Box Blue", ITEMS_LICENSE_OFFSET + 26, ItemClassification.progression)
    PROGRESSIVE_DECK_BOX_YELLOW = ("Progressive Deck Box Yellow", ITEMS_LICENSE_OFFSET + 27, ItemClassification.progression)

    COLLECTION_BOOK = ("Collection Book", ITEMS_LICENSE_OFFSET + 28, ItemClassification.progression)
    PREMIUM_COLLECTION_BOOK = ("Premium Collection Book", ITEMS_LICENSE_OFFSET + 54, ItemClassification.progression)

    PLAYMAT_DRILCEROS = ("Playmat (Drilceros)", ITEMS_LICENSE_OFFSET + 71, ItemClassification.progression)
    PLAYMAT_CLAMIGO = ("Playmat (Clamigo)", ITEMS_LICENSE_OFFSET + 69, ItemClassification.progression)
    PLAYMAT_WISPO = ("Playmat (Wispo)", ITEMS_LICENSE_OFFSET + 75, ItemClassification.progression)
    PLAYMAT_LUNIGHT = ("Playmat (Lunight)", ITEMS_LICENSE_OFFSET + 83, ItemClassification.progression)
    PLAYMAT_KYRONE = ("Playmat (Kyrone)", ITEMS_LICENSE_OFFSET + 78, ItemClassification.progression)
    PLAYMAT_DUEL = ("Playmat (Duel)", ITEMS_LICENSE_OFFSET + 70, ItemClassification.progression)
    PLAYMAT_DRACUNIX1 = ("Playmat (Dracunix1)", ITEMS_LICENSE_OFFSET + 74, ItemClassification.progression)
    PLAYMAT_THE_FOUR_DRAGONS = ("Playmat (The Four Dragons)", ITEMS_LICENSE_OFFSET + 73, ItemClassification.progression)
    PLAYMAT_DRAKON = ("Playmat (Drakon)", ITEMS_LICENSE_OFFSET + 72, ItemClassification.progression)
    PLAYMAT_GIGATRONX_EVO = ("Playmat (GigatronX Evo)", ITEMS_LICENSE_OFFSET + 76, ItemClassification.progression)
    PLAYMAT_FIRE = ("Playmat (Fire)", ITEMS_LICENSE_OFFSET + 79, ItemClassification.progression)
    PLAYMAT_EARTH = ("Playmat (Earth)", ITEMS_LICENSE_OFFSET + 80, ItemClassification.progression)
    PLAYMAT_WATER = ("Playmat (Water)", ITEMS_LICENSE_OFFSET + 82, ItemClassification.progression)
    PLAYMAT_WIND = ("Playmat (Wind)", ITEMS_LICENSE_OFFSET + 81, ItemClassification.progression)
    PLAYMAT_TETRAMON = ("Playmat (Tetramon)", ITEMS_LICENSE_OFFSET + 77, ItemClassification.progression)
    PLAYMAT_DRACUNIX2 = ("Playmat (Dracunix2)", ITEMS_LICENSE_OFFSET + 109, ItemClassification.progression)
    PLAYMAT_GIGATRONX = ("Playmat (GigatronX)", ITEMS_LICENSE_OFFSET + 110, ItemClassification.progression)
    PLAYMAT_KATENGU_BLACK = ("Playmat (Katengu Black)", ITEMS_LICENSE_OFFSET + 111, ItemClassification.progression)
    PLAYMAT_KATENGU_WHITE = ("Playmat (Katengu White)", ITEMS_LICENSE_OFFSET + 112, ItemClassification.progression)

    MANGA_1 = ("Manga 1", ITEMS_LICENSE_OFFSET + 95, ItemClassification.progression)
    MANGA_2 = ("Manga 2", ITEMS_LICENSE_OFFSET + 96, ItemClassification.progression)
    MANGA_3 = ("Manga 3", ITEMS_LICENSE_OFFSET + 97, ItemClassification.progression)
    MANGA_4 = ("Manga 4", ITEMS_LICENSE_OFFSET + 98, ItemClassification.progression)
    MANGA_5 = ("Manga 5", ITEMS_LICENSE_OFFSET + 99, ItemClassification.progression)
    MANGA_6 = ("Manga 6", ITEMS_LICENSE_OFFSET + 100, ItemClassification.progression)
    MANGA_7 = ("Manga 7", ITEMS_LICENSE_OFFSET + 101, ItemClassification.progression)
    MANGA_8 = ("Manga 8", ITEMS_LICENSE_OFFSET + 102, ItemClassification.progression)
    MANGA_9 = ("Manga 9", ITEMS_LICENSE_OFFSET + 103, ItemClassification.progression)
    MANGA_10 = ("Manga 10", ITEMS_LICENSE_OFFSET + 104, ItemClassification.progression)
    MANGA_11 = ("Manga 11", ITEMS_LICENSE_OFFSET + 105, ItemClassification.progression)
    MANGA_12 = ("Manga 12", ITEMS_LICENSE_OFFSET + 106, ItemClassification.progression)


class FigurineItems(ItemTypeEnum):
    PIGNI_PLUSHIE = ("Pigni Plushie", ITEMS_LICENSE_OFFSET + 33, ItemClassification.progression)
    NANOMITE_PLUSHIE = ("Nanomite Plushie", ITEMS_LICENSE_OFFSET + 34, ItemClassification.progression)
    MINSTAR_PLUSHIE = ("Minstar Plushie", ITEMS_LICENSE_OFFSET + 35, ItemClassification.progression)
    NOCTI_PLUSHIE = ("Nocti Plushie", ITEMS_LICENSE_OFFSET + 36, ItemClassification.progression)
    BURPIG_FIGURINE = ("Burpig Figurine", ITEMS_LICENSE_OFFSET + 39, ItemClassification.progression)
    DECIMITE_FIGURINE = ("Decimite Figurine", ITEMS_LICENSE_OFFSET + 42, ItemClassification.progression)
    TRICKSTAR_FIGURINE = ("Trickstar Figurine", ITEMS_LICENSE_OFFSET + 45, ItemClassification.progression)
    LUNIGHT_FIGURINE = ("Lunight Figurine", ITEMS_LICENSE_OFFSET + 48, ItemClassification.progression)
    INFERHOG_FIGURINE = ("Inferhog Figurine", ITEMS_LICENSE_OFFSET + 40, ItemClassification.progression)
    MEGANITE_FIGURINE = ("Meganite Figurine", ITEMS_LICENSE_OFFSET + 43, ItemClassification.progression)
    PRINCESTAR_FIGURINE = ("Princestar Figurine", ITEMS_LICENSE_OFFSET + 46, ItemClassification.progression)
    VAMPICANT_FIGURINE = ("Vampicant Figurine", ITEMS_LICENSE_OFFSET + 49, ItemClassification.progression)
    BLAZOAR_PLUSHIE = ("Blazoar Plushie", ITEMS_LICENSE_OFFSET + 41, ItemClassification.progression)
    GIGANITE_STATUE = ("Giganite Statue", ITEMS_LICENSE_OFFSET + 44, ItemClassification.progression)
    KINGSTAR_PLUSHIE = ("Kingstar Plushie", ITEMS_LICENSE_OFFSET + 47, ItemClassification.progression)
    DRACUNIX_FIGURINE = ("Dracunix Figurine", ITEMS_LICENSE_OFFSET + 50, ItemClassification.progression)
    BONFIOX_PLUSHIE = ("Bonfiox Plushie", ITEMS_LICENSE_OFFSET + 52, ItemClassification.progression)
    DRILCEROS_ACTION_FIGURE = ("Drilceros Action Figure", ITEMS_LICENSE_OFFSET + 51, ItemClassification.progression)
    TOONZ_PLUSHIE = ("ToonZ Plushie", ITEMS_LICENSE_OFFSET + 53, ItemClassification.progression)
    EVO_BLAZOAR = ("EVO Blazoar", ITEMS_LICENSE_OFFSET + 125, ItemClassification.progression)
    EVO_STARFISH = ("EVO Starfish", ITEMS_LICENSE_OFFSET + 126, ItemClassification.progression)


class TableTopItems(ItemTypeEnum):
    PENNY_SLEEVES = ("Penny Sleeves", ITEMS_LICENSE_OFFSET + 118, ItemClassification.progression)
    TOWER_DECKBOX = ("Tower Deckbox", ITEMS_LICENSE_OFFSET + 124, ItemClassification.progression)
    MAGNETIC_HOLDER = ("Magnetic Holder", ITEMS_LICENSE_OFFSET + 113, ItemClassification.progression)
    TOPLOADER = ("Toploader", ITEMS_LICENSE_OFFSET + 117, ItemClassification.progression)
    CARD_PRESERVER = ("Card Preserver", ITEMS_LICENSE_OFFSET + 114, ItemClassification.progression)
    PLAYMAT_GRAY = ("Playmat Gray", ITEMS_LICENSE_OFFSET + 119, ItemClassification.progression)
    PLAYMAT_GREEN = ("Playmat Green", ITEMS_LICENSE_OFFSET + 120, ItemClassification.progression)
    PLAYMAT_PURPLE = ("Playmat Purple", ITEMS_LICENSE_OFFSET + 121, ItemClassification.progression)
    PLAYMAT_YELLOW = ("Playmat Yellow", ITEMS_LICENSE_OFFSET + 122, ItemClassification.progression)
    POCKET_PAGES = ("Pocket Pages", ITEMS_LICENSE_OFFSET + 115, ItemClassification.progression)
    CARD_HOLDER = ("Card Holder", ITEMS_LICENSE_OFFSET + 116, ItemClassification.progression)
    COLLECTORS_ALBUM = ("Collectors Album", ITEMS_LICENSE_OFFSET + 123, ItemClassification.progression)
    SYSTEM_GATE_1 = ("System Gate #1", ITEMS_LICENSE_OFFSET + 87, ItemClassification.progression)
    SYSTEM_GATE_2 = ("System Gate #2", ITEMS_LICENSE_OFFSET + 88, ItemClassification.progression)
    MAFIA_WORKS = ("Mafia Works", ITEMS_LICENSE_OFFSET + 86, ItemClassification.progression)
    NECROMONSTERS = ("Necromonsters", ITEMS_LICENSE_OFFSET + 84, ItemClassification.progression)
    CLAIM = ("Claim!", ITEMS_LICENSE_OFFSET + 85, ItemClassification.progression)


def get_total_licenses():
    return len(TableTopItems) + len(FigurineItems) + len(AccessoriesItems) + len(BoosterPackItems)

ITEM_BY_ID = {
    item.item_id: item
    for enum in (
        BoosterPackItems,
        AccessoriesItems,
        FigurineItems,
        TableTopItems,
    )
    for item in enum
}


TETRAMON_BASE_PACK_ITEMS = {
    BoosterPackItems.PROGRESSIVE_BASIC_CARD_PACK,
    BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX,
    BoosterPackItems.PROGRESSIVE_RARE_CARD_PACK,
    BoosterPackItems.PROGRESSIVE_RARE_CARD_BOX,
    BoosterPackItems.PROGRESSIVE_EPIC_CARD_PACK,
    BoosterPackItems.PROGRESSIVE_EPIC_CARD_BOX,
    BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_PACK,
    BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_BOX,
}

TETRAMON_DESTINY_PACK_ITEMS = {
    BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_PACK,
    BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_BOX,
    BoosterPackItems.PROGRESSIVE_RARE_DESTINY_PACK,
    BoosterPackItems.PROGRESSIVE_RARE_DESTINY_BOX,
    BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_PACK,
    BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_BOX,
    BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_PACK,
    BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_BOX,
}