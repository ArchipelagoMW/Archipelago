from typing import List, Dict, TYPE_CHECKING

from .Enums import *

if TYPE_CHECKING:
    from . import SohWorld


vanilla_shop_prices: Dict[Items, int] = {
    Items.BUY_ARROWS10: 0,
    Items.BUY_DEKU_NUTS5: 0,
    Items.BUY_ARROWS30: 0,
    Items.BUY_ARROWS50: 0,
    Items.BUY_BOMBS525: 0,
    Items.BUY_DEKU_NUTS10: 0,
    Items.BUY_DEKU_STICK1: 0,
    Items.BUY_BOMBS10: 0,
    Items.BUY_FISH: 0,
    Items.BUY_RED_POTION30: 0,
    Items.BUY_GREEN_POTION: 0,
    Items.BUY_BLUE_POTION: 0,
    Items.BUY_HYLIAN_SHIELD: 0,
    Items.BUY_DEKU_SHIELD: 0,
    Items.BUY_GORON_TUNIC: 0,
    Items.BUY_ZORA_TUNIC: 0,
    Items.BUY_HEART: 0,
    Items.BUY_BOMBCHUS10: 0,
    Items.BUY_BOMBCHUS20: 0,
    Items.BUY_DEKU_SEEDS30: 0,
    Items.BUY_BLUE_FIRE: 0,
    Items.BUY_BOTTLE_BUG: 0,
    Items.BUY_POE: 0,
    Items.BUY_FAIRYS_SPIRIT: 0,
    Items.BUY_ARROWS10: 0,
    Items.BUY_BOMBS20: 0,
    Items.BUY_BOMBS30: 0,
    Items.BUY_BOMBS535: 0,
    Items.BUY_RED_POTION40: 0,
    Items.BUY_RED_POTION50: 0,
}


shop_locations_kf_shop: Dict[str, Items] = {
    "KF Shop Item 1": Items.BUY_ARROWS10,
    "KF Shop Item 2": Items.BUY_ARROWS10,
    "KF Shop Item 3": Items.BUY_ARROWS10,
    "KF Shop Item 4": Items.BUY_ARROWS10,
    "KF Shop Item 5": Items.BUY_ARROWS10,
    "KF Shop Item 6": Items.BUY_ARROWS10,
    "KF Shop Item 7": Items.BUY_ARROWS10,
    "KF Shop Item 8": Items.BUY_ARROWS10,
}

shop_locations_market_bazaar: Dict[str, Items] = {
    "Market Bazaar Item 1": Items.BUY_ARROWS10,
    "Market Bazaar Item 2": Items.BUY_ARROWS10,
    "Market Bazaar Item 3": Items.BUY_ARROWS10,
    "Market Bazaar Item 4": Items.BUY_ARROWS10,
    "Market Bazaar Item 5": Items.BUY_ARROWS10,
    "Market Bazaar Item 6": Items.BUY_ARROWS10,
    "Market Bazaar Item 7": Items.BUY_ARROWS10,
    "Market Bazaar Item 8": Items.BUY_ARROWS10,
}

shop_locations_market_potion_shop: Dict[str, Items] = {
    "Market Potion Shop Item 1": Items.BUY_ARROWS10,
    "Market Potion Shop Item 2": Items.BUY_ARROWS10,
    "Market Potion Shop Item 3": Items.BUY_ARROWS10,
    "Market Potion Shop Item 4": Items.BUY_ARROWS10,
    "Market Potion Shop Item 5": Items.BUY_ARROWS10,
    "Market Potion Shop Item 6": Items.BUY_ARROWS10,
    "Market Potion Shop Item 7": Items.BUY_ARROWS10,
    "Market Potion Shop Item 8": Items.BUY_ARROWS10,
}

shop_locations_market_bombchu_shop: Dict[str, Items] = {
    "Market Bombchu Shop Item 1": Items.BUY_ARROWS10,
    "Market Bombchu Shop Item 2": Items.BUY_ARROWS10,
    "Market Bombchu Shop Item 3": Items.BUY_ARROWS10,
    "Market Bombchu Shop Item 4": Items.BUY_ARROWS10,
    "Market Bombchu Shop Item 5": Items.BUY_ARROWS10,
    "Market Bombchu Shop Item 6": Items.BUY_ARROWS10,
    "Market Bombchu Shop Item 7": Items.BUY_ARROWS10,
    "Market Bombchu Shop Item 8": Items.BUY_ARROWS10,
}

shop_locations_kak_bazaar: Dict[str, Items] = {
    "Kak Bazaar Item 1": Items.BUY_ARROWS10,
    "Kak Bazaar Item 2": Items.BUY_ARROWS10,
    "Kak Bazaar Item 3": Items.BUY_ARROWS10,
    "Kak Bazaar Item 4": Items.BUY_ARROWS10,
    "Kak Bazaar Item 5": Items.BUY_ARROWS10,
    "Kak Bazaar Item 6": Items.BUY_ARROWS10,
    "Kak Bazaar Item 7": Items.BUY_ARROWS10,
    "Kak Bazaar Item 8": Items.BUY_ARROWS10,
}

shop_locations_kak_potion_shop: Dict[str, Items] = {
    "Kak Potion Shop Item 1": Items.BUY_ARROWS10,
    "Kak Potion Shop Item 2": Items.BUY_ARROWS10,
    "Kak Potion Shop Item 3": Items.BUY_ARROWS10,
    "Kak Potion Shop Item 4": Items.BUY_ARROWS10,
    "Kak Potion Shop Item 5": Items.BUY_ARROWS10,
    "Kak Potion Shop Item 6": Items.BUY_ARROWS10,
    "Kak Potion Shop Item 7": Items.BUY_ARROWS10,
    "Kak Potion Shop Item 8": Items.BUY_ARROWS10,
}

shop_locations_gc_shop: Dict[str, Items] = {
    "GC Shop Item 1": Items.BUY_ARROWS10,
    "GC Shop Item 2": Items.BUY_ARROWS10,
    "GC Shop Item 3": Items.BUY_ARROWS10,
    "GC Shop Item 4": Items.BUY_ARROWS10,
    "GC Shop Item 5": Items.BUY_ARROWS10,
    "GC Shop Item 6": Items.BUY_ARROWS10,
    "GC Shop Item 7": Items.BUY_ARROWS10,
    "GC Shop Item 8": Items.BUY_ARROWS10,
}

shop_locations_zd_shop: Dict[str, Items] = {
    "ZD Shop Item 1": Items.BUY_ARROWS10,
    "ZD Shop Item 2": Items.BUY_ARROWS10,
    "ZD Shop Item 3": Items.BUY_ARROWS10,
    "ZD Shop Item 4": Items.BUY_ARROWS10,
    "ZD Shop Item 5": Items.BUY_ARROWS10,
    "ZD Shop Item 6": Items.BUY_ARROWS10,
    "ZD Shop Item 7": Items.BUY_ARROWS10,
    "ZD Shop Item 8": Items.BUY_ARROWS10,
}

all_shop_locations = [
    shop_locations_kf_shop, shop_locations_market_bazaar, shop_locations_market_potion_shop, shop_locations_market_bombchu_shop,
    shop_locations_kak_bazaar, shop_locations_kak_potion_shop, shop_locations_gc_shop, shop_locations_zd_shop
]

vanilla_items_to_add: List[List[Items]] = [
    [Items.BUY_DEKU_SHIELD, Items.BUY_HYLIAN_SHIELD, Items.BUY_GORON_TUNIC, Items.BUY_ZORA_TUNIC, Items.BUY_DEKU_NUTS5, Items.BUY_BOMBS20, Items.BUY_BOMBCHUS10, Items.BUY_DEKU_STICK1],
    [Items.BUY_FAIRYS_SPIRIT, Items.BUY_DEKU_SEEDS30, Items.BUY_ARROWS10, Items.BUY_BLUE_FIRE, Items.BUY_RED_POTION30, Items.BUY_GREEN_POTION, Items.BUY_DEKU_NUTS10, Items.BUY_BOMBCHUS10],
    [Items.BUY_BOMBCHUS10, Items.BUY_BOMBCHUS20, Items.BUY_BOMBS525, Items.BUY_BOMBS535, Items.BUY_BOMBS10, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS30, Items.BUY_ARROWS50],
    [Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20],
    [Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20],
    [Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20],
    [Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20],
    [Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20, Items.BUY_BOMBS20],
]

def generate_shop_items() -> None:
    return
