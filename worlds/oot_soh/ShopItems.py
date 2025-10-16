from typing import List, Dict, TYPE_CHECKING
from worlds.generic.Rules import add_rule
from .LogicHelpers import rule_wrapper, can_afford
from Fill import fill_restrictive
from BaseClasses import CollectionState

from .Enums import *

if TYPE_CHECKING:
    from . import SohWorld


vanilla_shop_prices: Dict[Items, int] = {
    Items.BUY_ARROWS10: 20,
    Items.BUY_DEKU_NUTS5: 15,
    Items.BUY_ARROWS30: 60,
    Items.BUY_ARROWS50: 90,
    Items.BUY_BOMBS525: 25,
    Items.BUY_DEKU_NUTS10: 30,
    Items.BUY_DEKU_STICK1: 10,
    Items.BUY_BOMBS10: 50,
    Items.BUY_FISH: 200,
    Items.BUY_RED_POTION30: 30,
    Items.BUY_GREEN_POTION: 30,
    Items.BUY_BLUE_POTION: 100,
    Items.BUY_HYLIAN_SHIELD: 80,
    Items.BUY_DEKU_SHIELD: 40,
    Items.BUY_GORON_TUNIC: 200,
    Items.BUY_ZORA_TUNIC: 20,
    Items.BUY_HEART: 10,
    Items.BUY_BOMBCHUS10: 99,
    Items.BUY_BOMBCHUS20: 180,
    Items.BUY_DEKU_SEEDS30: 30,
    Items.BUY_BLUE_FIRE: 300,
    Items.BUY_BOTTLE_BUG: 50,
    Items.BUY_POE: 30,
    Items.BUY_FAIRYS_SPIRIT: 50,
    Items.BUY_BOMBS20: 80,
    Items.BUY_BOMBS30: 120,
    Items.BUY_BOMBS535: 35,
    Items.BUY_RED_POTION40: 40,
    Items.BUY_RED_POTION50: 50,
}


shop_locations_kf_shop: Dict[str, Items] = {
    "KF Shop Item 1": Items.BUY_DEKU_SHIELD,
    "KF Shop Item 2": Items.BUY_DEKU_NUTS5,
    "KF Shop Item 3": Items.BUY_DEKU_NUTS10,
    "KF Shop Item 4": Items.BUY_DEKU_STICK1,
    "KF Shop Item 5": Items.BUY_DEKU_SEEDS30,
    "KF Shop Item 6": Items.BUY_ARROWS10,
    "KF Shop Item 7": Items.BUY_ARROWS30,
    "KF Shop Item 8": Items.BUY_HEART,
}

shop_locations_market_bazaar: Dict[str, Items] = {
    "Market Bazaar Item 1": Items.BUY_HYLIAN_SHIELD,
    "Market Bazaar Item 2": Items.BUY_BOMBS535,
    "Market Bazaar Item 3": Items.BUY_DEKU_NUTS5,
    "Market Bazaar Item 4": Items.BUY_HEART,
    "Market Bazaar Item 5": Items.BUY_ARROWS10,
    "Market Bazaar Item 6": Items.BUY_ARROWS50,
    "Market Bazaar Item 7": Items.BUY_DEKU_STICK1,
    "Market Bazaar Item 8": Items.BUY_ARROWS30,
}

shop_locations_market_potion_shop: Dict[str, Items] = {
    "Market Potion Shop Item 1": Items.BUY_GREEN_POTION,
    "Market Potion Shop Item 2": Items.BUY_BLUE_FIRE,
    "Market Potion Shop Item 3": Items.BUY_RED_POTION30,
    "Market Potion Shop Item 4": Items.BUY_FAIRYS_SPIRIT,
    "Market Potion Shop Item 5": Items.BUY_DEKU_NUTS5,
    "Market Potion Shop Item 6": Items.BUY_BOTTLE_BUG,
    "Market Potion Shop Item 7": Items.BUY_POE,
    "Market Potion Shop Item 8": Items.BUY_FISH,
}

shop_locations_market_bombchu_shop: Dict[str, Items] = {
    "Market Bombchu Shop Item 1": Items.BUY_BOMBCHUS10,
    "Market Bombchu Shop Item 2": Items.BUY_BOMBCHUS10,
    "Market Bombchu Shop Item 3": Items.BUY_BOMBCHUS10,
    "Market Bombchu Shop Item 4": Items.BUY_BOMBCHUS10,
    "Market Bombchu Shop Item 5": Items.BUY_BOMBCHUS20,
    "Market Bombchu Shop Item 6": Items.BUY_BOMBCHUS20,
    "Market Bombchu Shop Item 7": Items.BUY_BOMBCHUS20,
    "Market Bombchu Shop Item 8": Items.BUY_BOMBCHUS20,
}

shop_locations_kak_bazaar: Dict[str, Items] = {
    "Kak Bazaar Item 1": Items.BUY_HYLIAN_SHIELD,
    "Kak Bazaar Item 2": Items.BUY_BOMBS535,
    "Kak Bazaar Item 3": Items.BUY_DEKU_NUTS5,
    "Kak Bazaar Item 4": Items.BUY_HEART,
    "Kak Bazaar Item 5": Items.BUY_ARROWS10,
    "Kak Bazaar Item 6": Items.BUY_ARROWS50,
    "Kak Bazaar Item 7": Items.BUY_DEKU_STICK1,
    "Kak Bazaar Item 8": Items.BUY_ARROWS30,
}

shop_locations_kak_potion_shop: Dict[str, Items] = {
    "Kak Potion Shop Item 1": Items.BUY_GREEN_POTION,
    "Kak Potion Shop Item 2": Items.BUY_BLUE_FIRE,
    "Kak Potion Shop Item 3": Items.BUY_RED_POTION30,
    "Kak Potion Shop Item 4": Items.BUY_FAIRYS_SPIRIT,
    "Kak Potion Shop Item 5": Items.BUY_DEKU_NUTS5,
    "Kak Potion Shop Item 6": Items.BUY_BOTTLE_BUG,
    "Kak Potion Shop Item 7": Items.BUY_POE,
    "Kak Potion Shop Item 8": Items.BUY_FISH,
}

shop_locations_gc_shop: Dict[str, Items] = {
    "GC Shop Item 1": Items.BUY_BOMBS525,
    "GC Shop Item 2": Items.BUY_BOMBS10,
    "GC Shop Item 3": Items.BUY_BOMBS20,
    "GC Shop Item 4": Items.BUY_BOMBS30,
    "GC Shop Item 5": Items.BUY_GORON_TUNIC,
    "GC Shop Item 6": Items.BUY_HEART,
    "GC Shop Item 7": Items.BUY_RED_POTION40,
    "GC Shop Item 8": Items.BUY_HEART,
}

shop_locations_zd_shop: Dict[str, Items] = {
    "ZD Shop Item 1": Items.BUY_ZORA_TUNIC,
    "ZD Shop Item 2": Items.BUY_ARROWS10,
    "ZD Shop Item 3": Items.BUY_HEART,
    "ZD Shop Item 4": Items.BUY_ARROWS30,
    "ZD Shop Item 5": Items.BUY_DEKU_NUTS5,
    "ZD Shop Item 6": Items.BUY_ARROWS50,
    "ZD Shop Item 7": Items.BUY_FISH,
    "ZD Shop Item 8": Items.BUY_RED_POTION30,
}

all_shop_locations: List[tuple[Regions, Dict[str, Items]]] = [
    (Regions.KF_KOKIRI_SHOP, shop_locations_kf_shop),
    (Regions.MARKET_BAZAAR, shop_locations_market_bazaar),
    (Regions.MARKET_POTION_SHOP, shop_locations_market_potion_shop),
    (Regions.MARKET_BOMBCHU_SHOP, shop_locations_market_bombchu_shop),
    (Regions.KAK_BAZAAR, shop_locations_kak_bazaar),
    (Regions.KAK_POTION_SHOP_FRONT, shop_locations_kak_potion_shop),
    (Regions.GC_SHOP, shop_locations_gc_shop), 
    (Regions.ZD_SHOP, shop_locations_zd_shop)
]

vanilla_items_to_add: List[List[Items]] = [
    [Items.BUY_DEKU_SHIELD, Items.BUY_HYLIAN_SHIELD, Items.BUY_GORON_TUNIC, Items.BUY_ZORA_TUNIC, Items.BUY_DEKU_NUTS5, Items.BUY_BOMBS20, Items.BUY_BOMBCHUS10, Items.BUY_DEKU_STICK1],
    [Items.BUY_FAIRYS_SPIRIT, Items.BUY_DEKU_SEEDS30, Items.BUY_ARROWS10, Items.BUY_BLUE_FIRE, Items.BUY_RED_POTION30, Items.BUY_GREEN_POTION, Items.BUY_DEKU_NUTS10, Items.BUY_BOMBCHUS10],
    [Items.BUY_BOMBCHUS10, Items.BUY_BOMBCHUS20, Items.BUY_BOMBS525, Items.BUY_BOMBS535, Items.BUY_BOMBS10, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS30, Items.BUY_ARROWS50],
    [Items.BUY_ARROWS10, Items.BUY_FAIRYS_SPIRIT, Items.BUY_BOTTLE_BUG, Items.BUY_FISH, Items.BUY_HYLIAN_SHIELD, Items.BUY_BOTTLE_BUG, Items.BUY_DEKU_STICK1, Items.BUY_DEKU_STICK1],
    [Items.BUY_BLUE_FIRE, Items.BUY_FISH, Items.BUY_BOMBCHUS10, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS10, Items.BUY_BOMBCHUS20, Items.BUY_BOMBS535, Items.BUY_RED_POTION30],
    [Items.BUY_BOMBS30, Items.BUY_BOMBCHUS20, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS10, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS30, Items.BUY_RED_POTION40, Items.BUY_FISH],
    [Items.BUY_BOMBCHUS20, Items.BUY_ARROWS30, Items.BUY_RED_POTION50, Items.BUY_ARROWS30, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS50, Items.BUY_ARROWS50, Items.BUY_GREEN_POTION],
    [Items.BUY_POE, Items.BUY_POE, Items.BUY_HEART, Items.BUY_HEART, Items.BUY_HEART, Items.BUY_HEART, Items.BUY_HEART, Items.BUY_HEART],
]

def fill_shop_items(world: "SohWorld") -> None:
    if not world.options.shuffle_shops:
        no_shop_shuffle(world)
        return
    
    # select what shop slots to and vanilla items to shuffle
    num_vanilla = 8 - world.options.shuffle_shops_item_amount
    vanilla_pool = list[Items]()
    vanilla_shop_slots = list[str]()

    for i in range(0, num_vanilla):
        vanilla_pool += vanilla_items_to_add[i]

    for region, shop in all_shop_locations:
        vanilla_shop_slots += list(shop.keys())[0: num_vanilla]

    vanilla_shop_locations = [world.get_location(slot) for slot in vanilla_shop_slots]
    vanilla_items = [world.create_item(item) for item in vanilla_pool]

    # create a filled copy of the state so the multiworld can place the vanilla shop items using logic
    prefill_state = CollectionState(world.multiworld)
    for item in world.item_pool:
        prefill_state.collect(item, False)
    prefill_state.sweep_for_advancements()

    # place the vanilla shop items
    fill_restrictive(world.multiworld, prefill_state, vanilla_shop_locations, vanilla_items, single_player_placement=True, lock=True)
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        world.get_location(slot).address = None
        world.shop_prices[slot] = vanilla_shop_prices[Items(location.item.name)]
        world.shop_vanilla_items[slot] = location.item.name
    
    for region, shop in all_shop_locations:
        for slot in shop.keys():
            if slot in world.shop_prices:
                continue
            world.shop_prices[slot] = create_random_shop_price(world)

    set_price_rules(world)

def no_shop_shuffle(world: "SohWorld") -> None:
    # put everything in its place as plain vanilla
    for region, shop in all_shop_locations:
        for slot, item in shop.items():
            world.shop_prices[slot] = vanilla_shop_prices[item]
            world.get_location(slot).place_locked_item(world.create_item(item))
            world.get_location(slot).address = None
            world.shop_vanilla_items[slot] = item.value

def create_random_shop_price(world: "SohWorld") -> int:
    # Todo randomized prices depending on the settings
    price = 10
    match world.options.shuffle_shops_prices:
        case 0: 
            # affordable prices
            price = 10
        case 1:
            # child wallet
            price = world.random.randrange(10, 101, 5)
            if price == 100:
                price = 99
        case 2:
            # adult wallet
            price = world.random.randrange(10, 201, 5)
        case 3:
            # giant wallet
            price = world.random.randrange(10, 501, 5)
        case 4:
            # tycoon's wallet
            price = world.random.randrange(10, 1001, 5)
            if price == 1000:
                price = 999

    return price

def set_price_rules(world: "SohWorld") -> None:
    for region, shop in all_shop_locations:
        for slot in shop.keys():
            price = world.shop_prices[slot]
            price_rule = lambda bundle: can_afford(price, bundle)
            location = world.get_location(slot)
            add_rule(location, rule_wrapper.wrap(region, price_rule, world))
