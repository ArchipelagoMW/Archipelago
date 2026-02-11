SHOP_ID_WITCH_POTION_3 = 0x00 # SI_POTION_RED_1
SHOP_ID_WITCH_POTION_2 = 0x01 # SI_POTION_GREEN_1
SHOP_ID_WITCH_POTION_1 = 0x02 # SI_POTION_BLUE
SHOP_ID_TRADING_POST_4 = 0x03 # SI_FAIRY_1
SHOP_ID_TRADING_POST_8 = 0x04 # SI_ARROWS_LARGE_1
SHOP_ID_TRADING_POST_2 = 0x05 # SI_POTION_GREEN_2
SHOP_ID_TRADING_POST_3 = 0x06 # SI_SHIELD_HERO_1
SHOP_ID_TRADING_POST_5 = 0x07 # SI_STICK_1
SHOP_ID_TRADING_POST_6 = 0x08 # SI_ARROWS_MEDIUM_1
SHOP_ID_TRADING_POST_7 = 0x09 # SI_NUTS_1
SHOP_ID_TRADING_POST_1 = 0x0A # SI_POTION_RED_2
SHOP_ID_TRADING_POST_NIGHT_4 = 0x0B # SI_FAIRY_2
SHOP_ID_TRADING_POST_NIGHT_6 = 0x0C # SI_ARROWS_MEDIUM_2
SHOP_ID_TRADING_POST_NIGHT_8 = 0x0D # SI_ARROWS_LARGE_2
SHOP_ID_TRADING_POST_NIGHT_2 = 0x0E # SI_POTION_GREEN_3
SHOP_ID_TRADING_POST_NIGHT_7 = 0x0F # SI_NUTS_2
SHOP_ID_TRADING_POST_NIGHT_5 = 0x10 # SI_STICK_2
SHOP_ID_TRADING_POST_NIGHT_3 = 0x11 # SI_SHIELD_HERO_2
SHOP_ID_TRADING_POST_NIGHT_1 = 0x12 # SI_POTION_RED_3
SHOP_ID_CURIOSITY_SHOP_MASK = 0x13 # SI_MASK_ALL_NIGHT
SHOP_ID_CURIOSITY_SHOP_BOMB_BAG = 0x15 # SI_BOMB_BAG_30_1
SHOP_ID_BOMB_SHOP_3 = 0x17 # SI_BOMB_BAG_20_2
SHOP_ID_BOMB_SHOP_3_UPGRADE = 0x18 # SI_BOMB_BAG_30_2
SHOP_ID_BOMB_SHOP_2 = 0x19 # SI_BOMBCHU
SHOP_ID_BOMB_SHOP_1 = 0x1A # SI_BOMB_1
SHOP_ID_ZORA_SHOP_1 = 0x1B # SI_SHIELD_HERO_3
SHOP_ID_ZORA_SHOP_2 = 0x1C # SI_ARROWS_SMALL_1
SHOP_ID_ZORA_SHOP_3 = 0x1D # SI_POTION_RED_4
SHOP_ID_GORON_SHOP_1 = 0x1E # SI_BOMB_2
SHOP_ID_GORON_SHOP_2 = 0x1F # SI_ARROWS_SMALL_2
SHOP_ID_GORON_SHOP_3 = 0x20 # SI_POTION_RED_5
SHOP_ID_GORON_SHOP_SPRING_1 = 0x21 # SI_BOMB_3
SHOP_ID_GORON_SHOP_SPRING_2 = 0x22 # SI_ARROWS_SMALL_3
SHOP_ID_GORON_SHOP_SPRING_3 = 0x23 # SI_POTION_RED_6
SHOP_ID_CURIOSITY_STOLEN_BOTTLE = 0x24 # SI_BOTTLE
SHOP_ID_CURIOSITY_STOLEN_GFS = 0x25 # SI_SWORD_GREAT_FAIRY
SHOP_ID_CURIOSITY_STOLEN_SWORD_KOKIRI = 0x26 # SI_SWORD_KOKIRI
SHOP_ID_CURIOSITY_STOLEN_SWORD_RAZOR = 0x27 # SI_SWORD_RAZOR
SHOP_ID_CURIOSITY_STOLEN_SWORD_GILDED = 0x28 # SI_SWORD_GILDED

default_shop_prices = [
    20,     # SI_POTION_RED_1
    10,     # SI_POTION_GREEN_1
    60,     # SI_POTION_BLUE
    50,     # SI_FAIRY_1
    40,     # SI_ARROWS_LARGE_1
    30,     # SI_POTION_GREEN_2
    80,     # SI_SHIELD_HERO_1
    10,     # SI_STICK_1
    30,     # SI_ARROWS_MEDIUM_1
    30,     # SI_NUTS_1
    30,     # SI_POTION_RED_2
    50,     # SI_FAIRY_2
    30,     # SI_ARROWS_MEDIUM_2
    40,     # SI_ARROWS_LARGE_2
    30,     # SI_POTION_GREEN_3
    30,     # SI_NUTS_2
    10,     # SI_STICK_2
    80,     # SI_SHIELD_HERO_2
    30,     # SI_POTION_RED_3
    500,    # SI_MASK_ALL_NIGHT
    100,    # SI_BOMB_BAG_20_1 (unused)
    100,    # SI_BOMB_BAG_30_1
    100,    # SI_BOMB_BAG_40 (unused)
    50,     # SI_BOMB_BAG_20_2
    90,     # SI_BOMB_BAG_30_2
    40,     # SI_BOMBCHU
    30,     # SI_BOMB_1
    90,     # SI_SHIELD_HERO_3
    20,     # SI_ARROWS_SMALL_1
    60,     # SI_POTION_RED_4
    40,     # SI_BOMB_2
    40,     # SI_ARROWS_SMALL_2
    80,     # SI_POTION_RED_5
    10,     # SI_BOMB_3
    20,     # SI_ARROWS_SMALL_3
    50,     # SI_POTION_RED_6
    20,     # SI_BOTTLE (curiosity shop)
    100,    # SI_SWORD_GREAT_FAIRY (curiosity shop)
    50,     # SI_SWORD_KOKIRI (curiosity shop)
    50,     # SI_SWORD_RAZOR (curiosity shop)
    50,     # SI_SWORD_GILDED (curiosity shop)
    0,      # SI_SHIELD_HERO_4 (curiosity shop, unused)
    0,      # SI_SHIELD_MIRROR (curiosity shop, unused)
]

shop_location_to_id = {
    # Trading Post
    "Clock Town Trading Post Shop Item 1": SHOP_ID_TRADING_POST_1,
    "Clock Town Trading Post Shop Item 2": SHOP_ID_TRADING_POST_2,
    "Clock Town Trading Post Shop Item 3": SHOP_ID_TRADING_POST_3,
    "Clock Town Trading Post Shop Item 4": SHOP_ID_TRADING_POST_4,
    "Clock Town Trading Post Shop Item 5": SHOP_ID_TRADING_POST_5,
    "Clock Town Trading Post Shop Item 6": SHOP_ID_TRADING_POST_6,
    "Clock Town Trading Post Shop Item 7": SHOP_ID_TRADING_POST_7,
    "Clock Town Trading Post Shop Item 8": SHOP_ID_TRADING_POST_8,
    # Trading Post (Night)
    "Clock Town Trading Post Shop (Night) Item 1": SHOP_ID_TRADING_POST_NIGHT_1,
    "Clock Town Trading Post Shop (Night) Item 2": SHOP_ID_TRADING_POST_NIGHT_2,
    "Clock Town Trading Post Shop (Night) Item 3": SHOP_ID_TRADING_POST_NIGHT_3,
    "Clock Town Trading Post Shop (Night) Item 4": SHOP_ID_TRADING_POST_NIGHT_4,
    "Clock Town Trading Post Shop (Night) Item 5": SHOP_ID_TRADING_POST_NIGHT_5,
    "Clock Town Trading Post Shop (Night) Item 6": SHOP_ID_TRADING_POST_NIGHT_6,
    "Clock Town Trading Post Shop (Night) Item 7": SHOP_ID_TRADING_POST_NIGHT_7,
    "Clock Town Trading Post Shop (Night) Item 8": SHOP_ID_TRADING_POST_NIGHT_8,
    # Bomb Shop
    "Clock Town Bomb Shop Item 1": SHOP_ID_BOMB_SHOP_1,
    "Clock Town Bomb Shop Item 2": SHOP_ID_BOMB_SHOP_2,
    "Clock Town Bomb Shop Item 3": SHOP_ID_BOMB_SHOP_3,
    "Clock Town Bomb Shop Item 3 (Stop Thief)": SHOP_ID_BOMB_SHOP_3_UPGRADE,
    # Curiosity Shop
    "Curiosity Shop Night 3 Thief Stolen Item": SHOP_ID_CURIOSITY_SHOP_BOMB_BAG,
    "Curiosity Shop Night 3 (Stop Thief)": SHOP_ID_CURIOSITY_SHOP_MASK,
    # Magic Hags' Potion Shop
    "Southern Swamp Witch Shop Item 1": SHOP_ID_WITCH_POTION_1,
    "Southern Swamp Witch Shop Item 2": SHOP_ID_WITCH_POTION_2,
    "Southern Swamp Witch Shop Item 3": SHOP_ID_WITCH_POTION_3,
    # Goron Village Shop
    "Goron Village Shop Item 1": SHOP_ID_GORON_SHOP_1,
    "Goron Village Shop Item 2": SHOP_ID_GORON_SHOP_2,
    "Goron Village Shop Item 3": SHOP_ID_GORON_SHOP_3,
    # Goron Village Shop (Spring)
    "Goron Village Shop (Spring) Item 1": SHOP_ID_GORON_SHOP_SPRING_1,
    "Goron Village Shop (Spring) Item 2": SHOP_ID_GORON_SHOP_SPRING_2,
    "Goron Village Shop (Spring) Item 3": SHOP_ID_GORON_SHOP_SPRING_3,
	# Zora Hall Shop
	"Zora Hall Shop Item 1": SHOP_ID_ZORA_SHOP_1,
	"Zora Hall Shop Item 2": SHOP_ID_ZORA_SHOP_2,
	"Zora Hall Shop Item 3": SHOP_ID_ZORA_SHOP_3,
}