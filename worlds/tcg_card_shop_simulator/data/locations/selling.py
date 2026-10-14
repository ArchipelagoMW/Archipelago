from enum import IntEnum
from .. import GeneratedLocationData
from ...constants import LOCATIONS_SELL_OFFSET


class Shop(IntEnum):
    BOOSTER_PACK_SHOP = 1
    ACCESSORIES_SHOP = 2
    FIGURINE_SHOP = 3
    TABLETOP_SHOP = 4
    WORKBENCH = 5


class ShopProduct(IntEnum):
    BASIC_CARD_PACK = 0
    BASIC_CARD_BOX = 1
    RARE_CARD_PACK = 2
    RARE_CARD_BOX = 3
    EPIC_CARD_PACK = 4
    EPIC_CARD_BOX = 5
    LEGENDARY_CARD_PACK = 6
    LEGENDARY_CARD_BOX = 7
    BASIC_DESTINY_PACK = 8
    BASIC_DESTINY_BOX = 9
    RARE_DESTINY_PACK = 10
    RARE_DESTINY_BOX = 11
    EPIC_DESTINY_PACK = 12
    EPIC_DESTINY_BOX = 13
    LEGENDARY_DESTINY_PACK = 14
    LEGENDARY_DESTINY_BOX = 15
    FIRE_BATTLE_DECK = 55
    EARTH_BATTLE_DECK = 56
    WATER_BATTLE_DECK = 57
    WIND_BATTLE_DECK = 58
    FIRE_DESTINY_DECK = 59
    EARTH_DESTINY_DECK = 60
    WATER_DESTINY_DECK = 61
    WIND_DESTINY_DECK = 62
    CLEANSER = 23
    CARD_SLEEVES_CLEAR = 63
    CARD_SLEEVES_TETRAMON = 64
    D20_DICE_RED = 29
    D20_DICE_BLUE = 30
    D20_DICE_BLACK = 31
    D20_DICE_WHITE = 32
    CARD_SLEEVES_FIRE = 65
    CARD_SLEEVES_EARTH = 66
    CARD_SLEEVES_WATER = 67
    CARD_SLEEVES_WIND = 68
    DECK_BOX_RED = 24
    DECK_BOX_GREEN = 25
    DECK_BOX_BLUE = 26
    DECK_BOX_YELLOW = 27
    COLLECTION_BOOK = 28
    PREMIUM_COLLECTION_BOOK = 54
    PLAYMAT_DRILCEROS = 71
    PLAYMAT_CLAMIGO = 69
    PLAYMAT_WISPO = 75
    PLAYMAT_LUNIGHT = 83
    PLAYMAT_KYRONE = 78
    PLAYMAT_DUEL = 70
    PLAYMAT_DRACUNIX1 = 74
    PLAYMAT_THE_FOUR_DRAGONS = 73
    PLAYMAT_DRAKON = 72
    PLAYMAT_GIGATRON_X_EVO = 76
    PLAYMAT_FIRE = 79
    PLAYMAT_EARTH = 80
    PLAYMAT_WATER = 82
    PLAYMAT_WIND = 81
    PLAYMAT_TETRAMON = 77
    PLAYMAT_DRACUNIX2 = 109
    PLAYMAT_GIGATRON_X = 110
    PLAYMAT_KATENGU_BLACK = 111
    PLAYMAT_KATENGU_WHITE = 112
    MANGA_1 = 95
    MANGA_2 = 96
    MANGA_3 = 97
    MANGA_4 = 98
    MANGA_5 = 99
    MANGA_6 = 100
    MANGA_7 = 101
    MANGA_8 = 102
    MANGA_9 = 103
    MANGA_10 = 104
    MANGA_11 = 105
    MANGA_12 = 106
    PIGNI_PLUSHIE = 33
    NANOMITE_PLUSHIE = 34
    MINSTAR_PLUSHIE = 35
    NOCTI_PLUSHIE = 36
    BULKBOX_TETRAMON = 37
    BULKBOX_DESTINY = 38
    BURPIG_FIGURINE = 39
    DECIMITE_FIGURINE = 42
    TRICKSTAR_FIGURINE = 45
    LUNIGHT_FIGURINE = 48
    INFERHOG_FIGURINE = 40
    MEGANITE_FIGURINE = 43
    PRINCESTAR_FIGURINE = 46
    VAMPICANT_FIGURINE = 49
    BLAZOAR_PLUSHIE = 41
    GIGANITE_STATUE = 44
    KINGSTAR_PLUSHIE = 47
    DRACUNIX_FIGURINE = 50
    BONFIOX_PLUSHIE = 52
    DRILCEROS_ACTION_FIGURE = 51
    TOON_Z_PLUSHIE = 53
    PENNY_SLEEVES = 118
    TOWER_DECKBOX = 124
    MAGNETIC_HOLDER = 113
    TOPLOADER = 117
    CARD_PRESERVER = 114
    PLAYMAT_GRAY = 119
    PLAYMAT_GREEN = 120
    PLAYMAT_PURPLE = 121
    PLAYMAT_YELLOW = 122
    POCKET_PAGES = 115
    CARD_HOLDER = 116
    COLLECTORS_ALBUM = 123
    SYSTEM_GATE_1 = 87
    SYSTEM_GATE_2 = 88
    MAFIA_WORKS = 86
    NECROMONSTERS = 84
    CLAIM = 85


PRODUCT_NAMES: dict[ShopProduct, str] = {
    ShopProduct.BULKBOX_TETRAMON: 'Bulk Box of Tetramon Base Cards',
    ShopProduct.BULKBOX_DESTINY: 'Bulk Box of Tetramon Destiny Cards',
    ShopProduct.BASIC_CARD_PACK: 'Basic Card Pack',
    ShopProduct.BASIC_CARD_BOX: 'Basic Card Box',
    ShopProduct.RARE_CARD_PACK: 'Rare Card Pack',
    ShopProduct.RARE_CARD_BOX: 'Rare Card Box',
    ShopProduct.EPIC_CARD_PACK: 'Epic Card Pack',
    ShopProduct.EPIC_CARD_BOX: 'Epic Card Box',
    ShopProduct.LEGENDARY_CARD_PACK: 'Legendary Card Pack',
    ShopProduct.LEGENDARY_CARD_BOX: 'Legendary Card Box',
    ShopProduct.BASIC_DESTINY_PACK: 'Basic Destiny Pack',
    ShopProduct.BASIC_DESTINY_BOX: 'Basic Destiny Box',
    ShopProduct.RARE_DESTINY_PACK: 'Rare Destiny Pack',
    ShopProduct.RARE_DESTINY_BOX: 'Rare Destiny Box',
    ShopProduct.EPIC_DESTINY_PACK: 'Epic Destiny Pack',
    ShopProduct.EPIC_DESTINY_BOX: 'Epic Destiny Box',
    ShopProduct.LEGENDARY_DESTINY_PACK: 'Legendary Destiny Pack',
    ShopProduct.LEGENDARY_DESTINY_BOX: 'Legendary Destiny Box',
    ShopProduct.FIRE_BATTLE_DECK: 'Fire Battle Deck',
    ShopProduct.EARTH_BATTLE_DECK: 'Earth Battle Deck',
    ShopProduct.WATER_BATTLE_DECK: 'Water Battle Deck',
    ShopProduct.WIND_BATTLE_DECK: 'Wind Battle Deck',
    ShopProduct.FIRE_DESTINY_DECK: 'Fire Destiny Deck',
    ShopProduct.EARTH_DESTINY_DECK: 'Earth Destiny Deck',
    ShopProduct.WATER_DESTINY_DECK: 'Water Destiny Deck',
    ShopProduct.WIND_DESTINY_DECK: 'Wind Destiny Deck',
    ShopProduct.CLEANSER: 'Cleanser',
    ShopProduct.CARD_SLEEVES_CLEAR: 'Card Sleeves (Clear)',
    ShopProduct.CARD_SLEEVES_TETRAMON: 'Card Sleeves (Tetramon)',
    ShopProduct.D20_DICE_RED: 'D20 Dice Red',
    ShopProduct.D20_DICE_BLUE: 'D20 Dice Blue',
    ShopProduct.D20_DICE_BLACK: 'D20 Dice Black',
    ShopProduct.D20_DICE_WHITE: 'D20 Dice White',
    ShopProduct.CARD_SLEEVES_FIRE: 'Card Sleeves (Fire)',
    ShopProduct.CARD_SLEEVES_EARTH: 'Card Sleeves (Earth)',
    ShopProduct.CARD_SLEEVES_WATER: 'Card Sleeves (Water)',
    ShopProduct.CARD_SLEEVES_WIND: 'Card Sleeves (Wind)',
    ShopProduct.DECK_BOX_RED: 'Deck Box Red',
    ShopProduct.DECK_BOX_GREEN: 'Deck Box Green',
    ShopProduct.DECK_BOX_BLUE: 'Deck Box Blue',
    ShopProduct.DECK_BOX_YELLOW: 'Deck Box Yellow',
    ShopProduct.COLLECTION_BOOK: 'Collection Book',
    ShopProduct.PREMIUM_COLLECTION_BOOK: 'Premium Collection Book',
    ShopProduct.PLAYMAT_DRILCEROS: 'Playmat (Drilceros)',
    ShopProduct.PLAYMAT_CLAMIGO: 'Playmat (Clamigo)',
    ShopProduct.PLAYMAT_WISPO: 'Playmat (Wispo)',
    ShopProduct.PLAYMAT_LUNIGHT: 'Playmat (Lunight)',
    ShopProduct.PLAYMAT_KYRONE: 'Playmat (Kyrone)',
    ShopProduct.PLAYMAT_DUEL: 'Playmat (Duel)',
    ShopProduct.PLAYMAT_DRACUNIX1: 'Playmat (Dracunix1)',
    ShopProduct.PLAYMAT_THE_FOUR_DRAGONS: 'Playmat (The Four Dragons)',
    ShopProduct.PLAYMAT_DRAKON: 'Playmat (Drakon)',
    ShopProduct.PLAYMAT_GIGATRON_X_EVO: 'Playmat (GigatronX Evo)',
    ShopProduct.PLAYMAT_FIRE: 'Playmat (Fire)',
    ShopProduct.PLAYMAT_EARTH: 'Playmat (Earth)',
    ShopProduct.PLAYMAT_WATER: 'Playmat (Water)',
    ShopProduct.PLAYMAT_WIND: 'Playmat (Wind)',
    ShopProduct.PLAYMAT_TETRAMON: 'Playmat (Tetramon)',
    ShopProduct.PLAYMAT_DRACUNIX2: 'Playmat (Dracunix2)',
    ShopProduct.PLAYMAT_GIGATRON_X: 'Playmat (GigatronX)',
    ShopProduct.PLAYMAT_KATENGU_BLACK: 'Playmat (Katengu Black)',
    ShopProduct.PLAYMAT_KATENGU_WHITE: 'Playmat (Katengu White)',
    ShopProduct.MANGA_1: 'Manga 1',
    ShopProduct.MANGA_2: 'Manga 2',
    ShopProduct.MANGA_3: 'Manga 3',
    ShopProduct.MANGA_4: 'Manga 4',
    ShopProduct.MANGA_5: 'Manga 5',
    ShopProduct.MANGA_6: 'Manga 6',
    ShopProduct.MANGA_7: 'Manga 7',
    ShopProduct.MANGA_8: 'Manga 8',
    ShopProduct.MANGA_9: 'Manga 9',
    ShopProduct.MANGA_10: 'Manga 10',
    ShopProduct.MANGA_11: 'Manga 11',
    ShopProduct.MANGA_12: 'Manga 12',
    ShopProduct.PIGNI_PLUSHIE: 'Pigni Plushie',
    ShopProduct.NANOMITE_PLUSHIE: 'Nanomite Plushie',
    ShopProduct.MINSTAR_PLUSHIE: 'Minstar Plushie',
    ShopProduct.NOCTI_PLUSHIE: 'Nocti Plushie',
    ShopProduct.BURPIG_FIGURINE: 'Burpig Figurine',
    ShopProduct.DECIMITE_FIGURINE: 'Decimite Figurine',
    ShopProduct.TRICKSTAR_FIGURINE: 'Trickstar Figurine',
    ShopProduct.LUNIGHT_FIGURINE: 'Lunight Figurine',
    ShopProduct.INFERHOG_FIGURINE: 'Inferhog Figurine',
    ShopProduct.MEGANITE_FIGURINE: 'Meganite Figurine',
    ShopProduct.PRINCESTAR_FIGURINE: 'Princestar Figurine',
    ShopProduct.VAMPICANT_FIGURINE: 'Vampicant Figurine',
    ShopProduct.BLAZOAR_PLUSHIE: 'Blazoar Plushie',
    ShopProduct.GIGANITE_STATUE: 'Giganite Statue',
    ShopProduct.KINGSTAR_PLUSHIE: 'Kingstar Plushie',
    ShopProduct.DRACUNIX_FIGURINE: 'Dracunix Figurine',
    ShopProduct.BONFIOX_PLUSHIE: 'Bonfiox Plushie',
    ShopProduct.DRILCEROS_ACTION_FIGURE: 'Drilceros Action Figure',
    ShopProduct.TOON_Z_PLUSHIE: 'ToonZ Plushie',
    ShopProduct.PENNY_SLEEVES: 'Penny Sleeves',
    ShopProduct.TOWER_DECKBOX: 'Tower Deckbox',
    ShopProduct.MAGNETIC_HOLDER: 'Magnetic Holder',
    ShopProduct.TOPLOADER: 'Toploader',
    ShopProduct.CARD_PRESERVER: 'Card Preserver',
    ShopProduct.PLAYMAT_GRAY: 'Playmat Gray',
    ShopProduct.PLAYMAT_GREEN: 'Playmat Green',
    ShopProduct.PLAYMAT_PURPLE: 'Playmat Purple',
    ShopProduct.PLAYMAT_YELLOW: 'Playmat Yellow',
    ShopProduct.POCKET_PAGES: 'Pocket Pages',
    ShopProduct.CARD_HOLDER: 'Card Holder',
    ShopProduct.COLLECTORS_ALBUM: 'Collectors Album',
    ShopProduct.SYSTEM_GATE_1: 'System Gate #1',
    ShopProduct.SYSTEM_GATE_2: 'System Gate #2',
    ShopProduct.MAFIA_WORKS: 'Mafia Works',
    ShopProduct.NECROMONSTERS: 'Necromonsters',
    ShopProduct.CLAIM: 'Claim!',
}

SHOP_PRODUCTS: dict[Shop, tuple[ShopProduct, ...]] = {
    Shop.BOOSTER_PACK_SHOP: (
        ShopProduct.BASIC_CARD_PACK,
        ShopProduct.BASIC_CARD_BOX,
        ShopProduct.RARE_CARD_PACK,
        ShopProduct.RARE_CARD_BOX,
        ShopProduct.EPIC_CARD_PACK,
        ShopProduct.EPIC_CARD_BOX,
        ShopProduct.LEGENDARY_CARD_PACK,
        ShopProduct.LEGENDARY_CARD_BOX,
        ShopProduct.BASIC_DESTINY_PACK,
        ShopProduct.BASIC_DESTINY_BOX,
        ShopProduct.RARE_DESTINY_PACK,
        ShopProduct.RARE_DESTINY_BOX,
        ShopProduct.EPIC_DESTINY_PACK,
        ShopProduct.EPIC_DESTINY_BOX,
        ShopProduct.LEGENDARY_DESTINY_PACK,
        ShopProduct.LEGENDARY_DESTINY_BOX,
        ShopProduct.FIRE_BATTLE_DECK,
        ShopProduct.EARTH_BATTLE_DECK,
        ShopProduct.WATER_BATTLE_DECK,
        ShopProduct.WIND_BATTLE_DECK,
        ShopProduct.FIRE_DESTINY_DECK,
        ShopProduct.EARTH_DESTINY_DECK,
        ShopProduct.WATER_DESTINY_DECK,
        ShopProduct.WIND_DESTINY_DECK,
    ),
    Shop.ACCESSORIES_SHOP: (
        ShopProduct.CLEANSER,
        ShopProduct.CARD_SLEEVES_CLEAR,
        ShopProduct.CARD_SLEEVES_TETRAMON,
        ShopProduct.D20_DICE_RED,
        ShopProduct.D20_DICE_BLUE,
        ShopProduct.D20_DICE_BLACK,
        ShopProduct.D20_DICE_WHITE,
        ShopProduct.CARD_SLEEVES_FIRE,
        ShopProduct.CARD_SLEEVES_EARTH,
        ShopProduct.CARD_SLEEVES_WATER,
        ShopProduct.CARD_SLEEVES_WIND,
        ShopProduct.DECK_BOX_RED,
        ShopProduct.DECK_BOX_GREEN,
        ShopProduct.DECK_BOX_BLUE,
        ShopProduct.DECK_BOX_YELLOW,
        ShopProduct.COLLECTION_BOOK,
        ShopProduct.PREMIUM_COLLECTION_BOOK,
        ShopProduct.PLAYMAT_DRILCEROS,
        ShopProduct.PLAYMAT_CLAMIGO,
        ShopProduct.PLAYMAT_WISPO,
        ShopProduct.PLAYMAT_LUNIGHT,
        ShopProduct.PLAYMAT_KYRONE,
        ShopProduct.PLAYMAT_DUEL,
        ShopProduct.PLAYMAT_DRACUNIX1,
        ShopProduct.PLAYMAT_THE_FOUR_DRAGONS,
        ShopProduct.PLAYMAT_DRAKON,
        ShopProduct.PLAYMAT_GIGATRON_X_EVO,
        ShopProduct.PLAYMAT_FIRE,
        ShopProduct.PLAYMAT_EARTH,
        ShopProduct.PLAYMAT_WATER,
        ShopProduct.PLAYMAT_WIND,
        ShopProduct.PLAYMAT_TETRAMON,
        ShopProduct.PLAYMAT_DRACUNIX2,
        ShopProduct.PLAYMAT_GIGATRON_X,
        ShopProduct.PLAYMAT_KATENGU_BLACK,
        ShopProduct.PLAYMAT_KATENGU_WHITE,
        ShopProduct.MANGA_1,
        ShopProduct.MANGA_2,
        ShopProduct.MANGA_3,
        ShopProduct.MANGA_4,
        ShopProduct.MANGA_5,
        ShopProduct.MANGA_6,
        ShopProduct.MANGA_7,
        ShopProduct.MANGA_8,
        ShopProduct.MANGA_9,
        ShopProduct.MANGA_10,
        ShopProduct.MANGA_11,
        ShopProduct.MANGA_12,
    ),
    Shop.FIGURINE_SHOP: (
        ShopProduct.PIGNI_PLUSHIE,
        ShopProduct.NANOMITE_PLUSHIE,
        ShopProduct.MINSTAR_PLUSHIE,
        ShopProduct.NOCTI_PLUSHIE,
        ShopProduct.BURPIG_FIGURINE,
        ShopProduct.DECIMITE_FIGURINE,
        ShopProduct.TRICKSTAR_FIGURINE,
        ShopProduct.LUNIGHT_FIGURINE,
        ShopProduct.INFERHOG_FIGURINE,
        ShopProduct.MEGANITE_FIGURINE,
        ShopProduct.PRINCESTAR_FIGURINE,
        ShopProduct.VAMPICANT_FIGURINE,
        ShopProduct.BLAZOAR_PLUSHIE,
        ShopProduct.GIGANITE_STATUE,
        ShopProduct.KINGSTAR_PLUSHIE,
        ShopProduct.DRACUNIX_FIGURINE,
        ShopProduct.BONFIOX_PLUSHIE,
        ShopProduct.DRILCEROS_ACTION_FIGURE,
        ShopProduct.TOON_Z_PLUSHIE,
    ),
    Shop.TABLETOP_SHOP: (
        ShopProduct.PENNY_SLEEVES,
        ShopProduct.TOWER_DECKBOX,
        ShopProduct.MAGNETIC_HOLDER,
        ShopProduct.TOPLOADER,
        ShopProduct.CARD_PRESERVER,
        ShopProduct.PLAYMAT_GRAY,
        ShopProduct.PLAYMAT_GREEN,
        ShopProduct.PLAYMAT_PURPLE,
        ShopProduct.PLAYMAT_YELLOW,
        ShopProduct.POCKET_PAGES,
        ShopProduct.CARD_HOLDER,
        ShopProduct.COLLECTORS_ALBUM,
        ShopProduct.SYSTEM_GATE_1,
        ShopProduct.SYSTEM_GATE_2,
        ShopProduct.MAFIA_WORKS,
        ShopProduct.NECROMONSTERS,
        ShopProduct.CLAIM,
    ),
    Shop.WORKBENCH: (
        ShopProduct.BULKBOX_TETRAMON,
        ShopProduct.BULKBOX_DESTINY,
    )
}


def generate_license_locations(
    region, product: ShopProduct, check_count: int, starting_checks: int = 0,
    starting_products: frozenset[ShopProduct] = frozenset(),
) -> list[GeneratedLocationData]:
    if check_count < 0 or starting_checks < 0 or check_count + starting_checks > 999:
        raise ValueError("license sale checks out of bounds")
    results = []
    count = check_count + (starting_checks if product in starting_products else 0)
    for n in range(1, count + 1):
        results.append(GeneratedLocationData(
            name=f"Sell {n} {'Box' if n == 1 else 'Boxes'} of {PRODUCT_NAMES[product]}",
            location_id=(LOCATIONS_SELL_OFFSET + (product.value * 1000) + n),
            region=region,
            ))
    return results