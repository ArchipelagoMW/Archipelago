from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from BaseClasses import CollectionRule
from rule_builder.rules import Rule, Has, AtLeast
from .. import GeneratedLocationData
from ..items import DIYItems, BoosterPackItems, TableTopItems, FigurineItems, AccessoriesItems
from ..regions.regions import GenericRegions
from ..rules.state_rules import accessToTetramonBasePacks, accessToTetramonDestinyPacks
from ...constants import LOCATIONS_SELL_OFFSET

if TYPE_CHECKING:
    from ...world_base import TCGSimulatorBase

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
    EVO_BLAZOAR = 125
    EVO_STARFISH = 126
    ASCENSION_PACK = 129


PRODUCT_DATA: dict[ShopProduct, tuple[str, CollectionRule | Rule[TCGSimulatorBase]]] = {
    # Bulk Boxes
    ShopProduct.BULKBOX_TETRAMON: (
        'Bulk Box of Tetramon Base Cards',
        Has(DIYItems.WORKBENCH.value) & accessToTetramonBasePacks()
    ),
    ShopProduct.BULKBOX_DESTINY: (
        'Bulk Box of Tetramon Destiny Cards',
        Has(DIYItems.WORKBENCH.value) & accessToTetramonDestinyPacks()
    ),

    # Tetramon Card Packs and Boxes
    ShopProduct.BASIC_CARD_PACK: (
        'Basic Card Pack',
        Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX.value)
    ),
    ShopProduct.BASIC_CARD_BOX: (
        'Basic Card Box',
        Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX.value)
    ),
    ShopProduct.RARE_CARD_PACK: (
        'Rare Card Pack',
        Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_BOX.value)
    ),
    ShopProduct.RARE_CARD_BOX: (
        'Rare Card Box',
        Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_BOX.value)
    ),
    ShopProduct.EPIC_CARD_PACK: (
        'Epic Card Pack',
        Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_BOX.value)
    ),
    ShopProduct.EPIC_CARD_BOX: (
        'Epic Card Box',
        Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_BOX.value)
    ),
    ShopProduct.LEGENDARY_CARD_PACK: (
        'Legendary Card Pack',
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_BOX.value)
    ),
    ShopProduct.LEGENDARY_CARD_BOX: (
        'Legendary Card Box',
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_BOX.value)
    ),

    # Destiny Card Packs and Boxes
    ShopProduct.BASIC_DESTINY_PACK: (
        'Basic Destiny Pack',
        Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_BOX.value)
    ),
    ShopProduct.BASIC_DESTINY_BOX: (
        'Basic Destiny Box',
        Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_BOX.value)
    ),
    ShopProduct.RARE_DESTINY_PACK: (
        'Rare Destiny Pack',
        Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_BOX.value)
    ),
    ShopProduct.RARE_DESTINY_BOX: (
        'Rare Destiny Box',
        Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_BOX.value)
    ),
    ShopProduct.EPIC_DESTINY_PACK: (
        'Epic Destiny Pack',
        Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_BOX.value)
    ),
    ShopProduct.EPIC_DESTINY_BOX: (
        'Epic Destiny Box',
        Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_BOX.value)
    ),
    ShopProduct.LEGENDARY_DESTINY_PACK: (
        'Legendary Destiny Pack',
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_BOX.value)
    ),
    ShopProduct.LEGENDARY_DESTINY_BOX: (
        'Legendary Destiny Box',
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_BOX.value)
    ),

    # Battle Decks
    ShopProduct.FIRE_BATTLE_DECK: (
        'Fire Battle Deck', Has(BoosterPackItems.FIRE_BATTLE_DECK.value)
    ),
    ShopProduct.EARTH_BATTLE_DECK: (
        'Earth Battle Deck', Has(BoosterPackItems.EARTH_BATTLE_DECK.value)
    ),
    ShopProduct.WATER_BATTLE_DECK: (
        'Water Battle Deck', Has(BoosterPackItems.WATER_BATTLE_DECK.value)
    ),
    ShopProduct.WIND_BATTLE_DECK: (
        'Wind Battle Deck', Has(BoosterPackItems.WIND_BATTLE_DECK.value)
    ),
    ShopProduct.FIRE_DESTINY_DECK: (
        'Fire Destiny Deck', Has(BoosterPackItems.FIRE_DESTINY_DECK.value)
    ),
    ShopProduct.EARTH_DESTINY_DECK: (
        'Earth Destiny Deck', Has(BoosterPackItems.EARTH_DESTINY_DECK.value)
    ),
    ShopProduct.WATER_DESTINY_DECK: (
        'Water Destiny Deck', Has(BoosterPackItems.WATER_DESTINY_DECK.value)
    ),
    ShopProduct.WIND_DESTINY_DECK: (
        'Wind Destiny Deck', Has(BoosterPackItems.WIND_DESTINY_DECK.value)
    ),
    ShopProduct.ASCENSION_PACK: (
        'Ascension Card Pack', Has(BoosterPackItems.PROGRESSIVE_ASCENSION_PACK.value)
    ),

    # Accessories
    ShopProduct.CLEANSER: (
        'Cleanser', Has(AccessoriesItems.PROGRESSIVE_CLEANSER.value)
    ),
    ShopProduct.CARD_SLEEVES_CLEAR: (
        'Card Sleeves (Clear)', Has(AccessoriesItems.CARD_SLEEVES_CLEAR.value)
    ),
    ShopProduct.CARD_SLEEVES_TETRAMON: (
        'Card Sleeves (Tetramon)', Has(AccessoriesItems.CARD_SLEEVES_TETRAMON.value)
    ),
    ShopProduct.D20_DICE_RED: (
        'D20 Dice Red', Has(AccessoriesItems.D20_DICE_RED.value)
    ),
    ShopProduct.D20_DICE_BLUE: (
        'D20 Dice Blue', Has(AccessoriesItems.D20_DICE_BLUE.value)
    ),
    ShopProduct.D20_DICE_BLACK: (
        'D20 Dice Black', Has(AccessoriesItems.D20_DICE_BLACK.value)
    ),
    ShopProduct.D20_DICE_WHITE: (
        'D20 Dice White', Has(AccessoriesItems.D20_DICE_WHITE.value)
    ),
    ShopProduct.CARD_SLEEVES_FIRE: (
        'Card Sleeves (Fire)', Has(AccessoriesItems.CARD_SLEEVES_FIRE.value)
    ),
    ShopProduct.CARD_SLEEVES_EARTH: (
        'Card Sleeves (Earth)', Has(AccessoriesItems.CARD_SLEEVES_EARTH.value)
    ),
    ShopProduct.CARD_SLEEVES_WATER: (
        'Card Sleeves (Water)', Has(AccessoriesItems.CARD_SLEEVES_WATER.value)
    ),
    ShopProduct.CARD_SLEEVES_WIND: (
        'Card Sleeves (Wind)', Has(AccessoriesItems.CARD_SLEEVES_WIND.value)
    ),

    # Deck Boxes
    ShopProduct.DECK_BOX_RED: (
        'Deck Box Red', Has(AccessoriesItems.PROGRESSIVE_DECK_BOX_RED.value)
    ),
    ShopProduct.DECK_BOX_GREEN: (
        'Deck Box Green', Has(AccessoriesItems.PROGRESSIVE_DECK_BOX_GREEN.value)
    ),
    ShopProduct.DECK_BOX_BLUE: (
        'Deck Box Blue', Has(AccessoriesItems.PROGRESSIVE_DECK_BOX_BLUE.value)
    ),
    ShopProduct.DECK_BOX_YELLOW: (
        'Deck Box Yellow', Has(AccessoriesItems.PROGRESSIVE_DECK_BOX_YELLOW.value)
    ),

    # Collection Books
    ShopProduct.COLLECTION_BOOK: (
        'Collection Book', Has(AccessoriesItems.COLLECTION_BOOK.value)
    ),
    ShopProduct.PREMIUM_COLLECTION_BOOK: (
        'Premium Collection Book', Has(AccessoriesItems.PREMIUM_COLLECTION_BOOK.value)
    ),

    # Playmats
    ShopProduct.PLAYMAT_DRILCEROS: (
        'Playmat (Drilceros)', Has(AccessoriesItems.PLAYMAT_DRILCEROS.value)
    ),
    ShopProduct.PLAYMAT_CLAMIGO: (
        'Playmat (Clamigo)', Has(AccessoriesItems.PLAYMAT_CLAMIGO.value)
    ),
    ShopProduct.PLAYMAT_WISPO: (
        'Playmat (Wispo)', Has(AccessoriesItems.PLAYMAT_WISPO.value)
    ),
    ShopProduct.PLAYMAT_LUNIGHT: (
        'Playmat (Lunight)', Has(AccessoriesItems.PLAYMAT_LUNIGHT.value)
    ),
    ShopProduct.PLAYMAT_KYRONE: (
        'Playmat (Kyrone)', Has(AccessoriesItems.PLAYMAT_KYRONE.value)
    ),
    ShopProduct.PLAYMAT_DUEL: (
        'Playmat (Duel)', Has(AccessoriesItems.PLAYMAT_DUEL.value)
    ),
    ShopProduct.PLAYMAT_DRACUNIX1: (
        'Playmat (Dracunix1)', Has(AccessoriesItems.PLAYMAT_DRACUNIX1.value)
    ),
    ShopProduct.PLAYMAT_THE_FOUR_DRAGONS: (
        'Playmat (The Four Dragons)', Has(AccessoriesItems.PLAYMAT_THE_FOUR_DRAGONS.value)
    ),
    ShopProduct.PLAYMAT_DRAKON: (
        'Playmat (Drakon)', Has(AccessoriesItems.PLAYMAT_DRAKON.value)
    ),
    ShopProduct.PLAYMAT_GIGATRON_X_EVO: (
        'Playmat (GigatronX Evo)', Has(AccessoriesItems.PLAYMAT_GIGATRONX_EVO.value)
    ),
    ShopProduct.PLAYMAT_FIRE: (
        'Playmat (Fire)', Has(AccessoriesItems.PLAYMAT_FIRE.value)
    ),
    ShopProduct.PLAYMAT_EARTH: (
        'Playmat (Earth)', Has(AccessoriesItems.PLAYMAT_EARTH.value)
    ),
    ShopProduct.PLAYMAT_WATER: (
        'Playmat (Water)', Has(AccessoriesItems.PLAYMAT_WATER.value)
    ),
    ShopProduct.PLAYMAT_WIND: (
        'Playmat (Wind)', Has(AccessoriesItems.PLAYMAT_WIND.value)
    ),
    ShopProduct.PLAYMAT_TETRAMON: (
        'Playmat (Tetramon)', Has(AccessoriesItems.PLAYMAT_TETRAMON.value)
    ),
    ShopProduct.PLAYMAT_DRACUNIX2: (
        'Playmat (Dracunix2)', Has(AccessoriesItems.PLAYMAT_DRACUNIX2.value)
    ),
    ShopProduct.PLAYMAT_GIGATRON_X: (
        'Playmat (GigatronX)', Has(AccessoriesItems.PLAYMAT_GIGATRONX.value)
    ),
    ShopProduct.PLAYMAT_KATENGU_BLACK: (
        'Playmat (Katengu Black)', Has(AccessoriesItems.PLAYMAT_KATENGU_BLACK.value)
    ),
    ShopProduct.PLAYMAT_KATENGU_WHITE: (
        'Playmat (Katengu White)', Has(AccessoriesItems.PLAYMAT_KATENGU_WHITE.value)
    ),

    # Manga
    ShopProduct.MANGA_1: ('Manga 1', Has(AccessoriesItems.MANGA_1.value)),
    ShopProduct.MANGA_2: ('Manga 2', Has(AccessoriesItems.MANGA_2.value)),
    ShopProduct.MANGA_3: ('Manga 3', Has(AccessoriesItems.MANGA_3.value)),
    ShopProduct.MANGA_4: ('Manga 4', Has(AccessoriesItems.MANGA_4.value)),
    ShopProduct.MANGA_5: ('Manga 5', Has(AccessoriesItems.MANGA_5.value)),
    ShopProduct.MANGA_6: ('Manga 6', Has(AccessoriesItems.MANGA_6.value)),
    ShopProduct.MANGA_7: ('Manga 7', Has(AccessoriesItems.MANGA_7.value)),
    ShopProduct.MANGA_8: ('Manga 8', Has(AccessoriesItems.MANGA_8.value)),
    ShopProduct.MANGA_9: ('Manga 9', Has(AccessoriesItems.MANGA_9.value)),
    ShopProduct.MANGA_10: ('Manga 10', Has(AccessoriesItems.MANGA_10.value)),
    ShopProduct.MANGA_11: ('Manga 11', Has(AccessoriesItems.MANGA_11.value)),
    ShopProduct.MANGA_12: ('Manga 12', Has(AccessoriesItems.MANGA_12.value)),

    # Plushies and Figurines
    ShopProduct.PIGNI_PLUSHIE: (
        'Pigni Plushie', Has(FigurineItems.PIGNI_PLUSHIE.value)
    ),
    ShopProduct.NANOMITE_PLUSHIE: (
        'Nanomite Plushie', Has(FigurineItems.NANOMITE_PLUSHIE.value)
    ),
    ShopProduct.MINSTAR_PLUSHIE: (
        'Minstar Plushie', Has(FigurineItems.MINSTAR_PLUSHIE.value)
    ),
    ShopProduct.NOCTI_PLUSHIE: (
        'Nocti Plushie', Has(FigurineItems.NOCTI_PLUSHIE.value)
    ),
    ShopProduct.BURPIG_FIGURINE: (
        'Burpig Figurine', Has(FigurineItems.BURPIG_FIGURINE.value)
    ),
    ShopProduct.DECIMITE_FIGURINE: (
        'Decimite Figurine', Has(FigurineItems.DECIMITE_FIGURINE.value)
    ),
    ShopProduct.TRICKSTAR_FIGURINE: (
        'Trickstar Figurine', Has(FigurineItems.TRICKSTAR_FIGURINE.value)
    ),
    ShopProduct.LUNIGHT_FIGURINE: (
        'Lunight Figurine', Has(FigurineItems.LUNIGHT_FIGURINE.value)
    ),
    ShopProduct.INFERHOG_FIGURINE: (
        'Inferhog Figurine', Has(FigurineItems.INFERHOG_FIGURINE.value)
    ),
    ShopProduct.MEGANITE_FIGURINE: (
        'Meganite Figurine', Has(FigurineItems.MEGANITE_FIGURINE.value)
    ),
    ShopProduct.PRINCESTAR_FIGURINE: (
        'Princestar Figurine', Has(FigurineItems.PRINCESTAR_FIGURINE.value)
    ),
    ShopProduct.VAMPICANT_FIGURINE: (
        'Vampicant Figurine', Has(FigurineItems.VAMPICANT_FIGURINE.value)
    ),
    ShopProduct.BLAZOAR_PLUSHIE: (
        'Blazoar Plushie', Has(FigurineItems.BLAZOAR_PLUSHIE.value)
    ),
    ShopProduct.GIGANITE_STATUE: (
        'Giganite Statue', Has(FigurineItems.GIGANITE_STATUE.value)
    ),
    ShopProduct.KINGSTAR_PLUSHIE: (
        'Kingstar Plushie', Has(FigurineItems.KINGSTAR_PLUSHIE.value)
    ),
    ShopProduct.DRACUNIX_FIGURINE: (
        'Dracunix Figurine', Has(FigurineItems.DRACUNIX_FIGURINE.value)
    ),
    ShopProduct.BONFIOX_PLUSHIE: (
        'Bonfiox Plushie', Has(FigurineItems.BONFIOX_PLUSHIE.value)
    ),
    ShopProduct.DRILCEROS_ACTION_FIGURE: (
        'Drilceros Action Figure', Has(FigurineItems.DRILCEROS_ACTION_FIGURE.value)
    ),
    ShopProduct.TOON_Z_PLUSHIE: (
        'ToonZ Plushie', Has(FigurineItems.TOONZ_PLUSHIE.value)
    ),

ShopProduct.EVO_BLAZOAR: (
        'EVO Blazoar', Has(FigurineItems.EVO_BLAZOAR.value)
    ),

ShopProduct.EVO_STARFISH: (
        'EVO Starfish', Has(FigurineItems.EVO_STARFISH.value)
    ),

    # Tabletop Products
    ShopProduct.PENNY_SLEEVES: (
        'Penny Sleeves', Has(TableTopItems.PENNY_SLEEVES.value)
    ),
    ShopProduct.TOWER_DECKBOX: (
        'Tower Deckbox', Has(TableTopItems.TOWER_DECKBOX.value)
    ),
    ShopProduct.MAGNETIC_HOLDER: (
        'Magnetic Holder', Has(TableTopItems.MAGNETIC_HOLDER.value)
    ),
    ShopProduct.TOPLOADER: (
        'Toploader', Has(TableTopItems.TOPLOADER.value)
    ),
    ShopProduct.CARD_PRESERVER: (
        'Card Preserver', Has(TableTopItems.CARD_PRESERVER.value)
    ),
    ShopProduct.PLAYMAT_GRAY: (
        'Playmat Gray', Has(TableTopItems.PLAYMAT_GRAY.value)
    ),
    ShopProduct.PLAYMAT_GREEN: (
        'Playmat Green', Has(TableTopItems.PLAYMAT_GREEN.value)
    ),
    ShopProduct.PLAYMAT_PURPLE: (
        'Playmat Purple', Has(TableTopItems.PLAYMAT_PURPLE.value)
    ),
    ShopProduct.PLAYMAT_YELLOW: (
        'Playmat Yellow', Has(TableTopItems.PLAYMAT_YELLOW.value)
    ),
    ShopProduct.POCKET_PAGES: (
        'Pocket Pages', Has(TableTopItems.POCKET_PAGES.value)
    ),
    ShopProduct.CARD_HOLDER: (
        'Card Holder', Has(TableTopItems.CARD_HOLDER.value)
    ),
    ShopProduct.COLLECTORS_ALBUM: (
        'Collectors Album', Has(TableTopItems.COLLECTORS_ALBUM.value)
    ),
    ShopProduct.SYSTEM_GATE_1: (
        'System Gate #1', Has(TableTopItems.SYSTEM_GATE_1.value)
    ),
    ShopProduct.SYSTEM_GATE_2: (
        'System Gate #2', Has(TableTopItems.SYSTEM_GATE_2.value)
    ),
    ShopProduct.MAFIA_WORKS: (
        'Mafia Works', Has(TableTopItems.MAFIA_WORKS.value)
    ),
    ShopProduct.NECROMONSTERS: (
        'Necromonsters', Has(TableTopItems.NECROMONSTERS.value)
    ),
    ShopProduct.CLAIM: (
        'Claim!', Has(TableTopItems.CLAIM.value)
    ),
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
        ShopProduct.ASCENSION_PACK
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
        ShopProduct.EVO_STARFISH,
        ShopProduct.EVO_BLAZOAR
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


def generate_license_locations(product: ShopProduct, check_count: int, starting_checks: int = 0,
    starting_products: frozenset[ShopProduct] = frozenset(),
) -> list[GeneratedLocationData]:
    if check_count < 0 or starting_checks < 0 or check_count + starting_checks > 999:
        raise ValueError("license sale checks out of bounds")
    results = []
    count = check_count + (starting_checks if product in starting_products else 0)
    for n in range(1, count + 1):
        product_name, product_rule = PRODUCT_DATA[product]
        results.append(GeneratedLocationData(
            name=f"Sell {n} {'Box' if n == 1 else 'Boxes'} of {product_name}",
            location_id=(LOCATIONS_SELL_OFFSET + (product.value * 1000) + n),
            region=GenericRegions.PRODUCT_SELLING,
            rule=product_rule
            ))
    return results