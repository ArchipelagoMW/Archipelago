from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule
from Fill import fill_restrictive
from BaseClasses import CollectionState

from .LogicHelpers import rule_wrapper, can_afford
from .Locations import scrubs_location_table
from .Enums import *

if TYPE_CHECKING:
    from . import SohWorld


vanilla_shop_prices: dict[Items, int] = {
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


shop_locations_kf_shop: dict[str, Items] = {
    "KF Shop Item 1": Items.BUY_DEKU_SHIELD,
    "KF Shop Item 2": Items.BUY_DEKU_NUTS5,
    "KF Shop Item 3": Items.BUY_DEKU_NUTS10,
    "KF Shop Item 4": Items.BUY_DEKU_STICK1,
    "KF Shop Item 5": Items.BUY_DEKU_SEEDS30,
    "KF Shop Item 6": Items.BUY_ARROWS10,
    "KF Shop Item 7": Items.BUY_ARROWS30,
    "KF Shop Item 8": Items.BUY_HEART,
}

shop_locations_market_bazaar: dict[str, Items] = {
    "Market Bazaar Item 1": Items.BUY_HYLIAN_SHIELD,
    "Market Bazaar Item 2": Items.BUY_BOMBS535,
    "Market Bazaar Item 3": Items.BUY_DEKU_NUTS5,
    "Market Bazaar Item 4": Items.BUY_HEART,
    "Market Bazaar Item 5": Items.BUY_ARROWS10,
    "Market Bazaar Item 6": Items.BUY_ARROWS50,
    "Market Bazaar Item 7": Items.BUY_DEKU_STICK1,
    "Market Bazaar Item 8": Items.BUY_ARROWS30,
}

shop_locations_market_potion_shop: dict[str, Items] = {
    "Market Potion Shop Item 1": Items.BUY_GREEN_POTION,
    "Market Potion Shop Item 2": Items.BUY_BLUE_FIRE,
    "Market Potion Shop Item 3": Items.BUY_RED_POTION30,
    "Market Potion Shop Item 4": Items.BUY_FAIRYS_SPIRIT,
    "Market Potion Shop Item 5": Items.BUY_DEKU_NUTS5,
    "Market Potion Shop Item 6": Items.BUY_BOTTLE_BUG,
    "Market Potion Shop Item 7": Items.BUY_POE,
    "Market Potion Shop Item 8": Items.BUY_FISH,
}

shop_locations_market_bombchu_shop: dict[str, Items] = {
    "Market Bombchu Shop Item 1": Items.BUY_BOMBCHUS10,
    "Market Bombchu Shop Item 2": Items.BUY_BOMBCHUS10,
    "Market Bombchu Shop Item 3": Items.BUY_BOMBCHUS10,
    "Market Bombchu Shop Item 4": Items.BUY_BOMBCHUS10,
    "Market Bombchu Shop Item 5": Items.BUY_BOMBCHUS20,
    "Market Bombchu Shop Item 6": Items.BUY_BOMBCHUS20,
    "Market Bombchu Shop Item 7": Items.BUY_BOMBCHUS20,
    "Market Bombchu Shop Item 8": Items.BUY_BOMBCHUS20,
}

shop_locations_kak_bazaar: dict[str, Items] = {
    "Kak Bazaar Item 1": Items.BUY_HYLIAN_SHIELD,
    "Kak Bazaar Item 2": Items.BUY_BOMBS535,
    "Kak Bazaar Item 3": Items.BUY_DEKU_NUTS5,
    "Kak Bazaar Item 4": Items.BUY_HEART,
    "Kak Bazaar Item 5": Items.BUY_ARROWS10,
    "Kak Bazaar Item 6": Items.BUY_ARROWS50,
    "Kak Bazaar Item 7": Items.BUY_DEKU_STICK1,
    "Kak Bazaar Item 8": Items.BUY_ARROWS30,
}

shop_locations_kak_potion_shop: dict[str, Items] = {
    "Kak Potion Shop Item 1": Items.BUY_GREEN_POTION,
    "Kak Potion Shop Item 2": Items.BUY_BLUE_FIRE,
    "Kak Potion Shop Item 3": Items.BUY_RED_POTION30,
    "Kak Potion Shop Item 4": Items.BUY_FAIRYS_SPIRIT,
    "Kak Potion Shop Item 5": Items.BUY_DEKU_NUTS5,
    "Kak Potion Shop Item 6": Items.BUY_BOTTLE_BUG,
    "Kak Potion Shop Item 7": Items.BUY_POE,
    "Kak Potion Shop Item 8": Items.BUY_FISH,
}

shop_locations_gc_shop: dict[str, Items] = {
    "GC Shop Item 1": Items.BUY_BOMBS525,
    "GC Shop Item 2": Items.BUY_BOMBS10,
    "GC Shop Item 3": Items.BUY_BOMBS20,
    "GC Shop Item 4": Items.BUY_BOMBS30,
    "GC Shop Item 5": Items.BUY_GORON_TUNIC,
    "GC Shop Item 6": Items.BUY_HEART,
    "GC Shop Item 7": Items.BUY_RED_POTION40,
    "GC Shop Item 8": Items.BUY_HEART,
}

shop_locations_zd_shop: dict[str, Items] = {
    "ZD Shop Item 1": Items.BUY_ZORA_TUNIC,
    "ZD Shop Item 2": Items.BUY_ARROWS10,
    "ZD Shop Item 3": Items.BUY_HEART,
    "ZD Shop Item 4": Items.BUY_ARROWS30,
    "ZD Shop Item 5": Items.BUY_DEKU_NUTS5,
    "ZD Shop Item 6": Items.BUY_ARROWS50,
    "ZD Shop Item 7": Items.BUY_FISH,
    "ZD Shop Item 8": Items.BUY_RED_POTION30,
}

all_shop_locations: list[tuple[Regions, dict[str, Items]]] = [
    (Regions.KF_KOKIRI_SHOP, shop_locations_kf_shop),
    (Regions.MARKET_BAZAAR, shop_locations_market_bazaar),
    (Regions.MARKET_POTION_SHOP, shop_locations_market_potion_shop),
    (Regions.MARKET_BOMBCHU_SHOP, shop_locations_market_bombchu_shop),
    (Regions.KAK_BAZAAR, shop_locations_kak_bazaar),
    (Regions.KAK_POTION_SHOP_FRONT, shop_locations_kak_potion_shop),
    (Regions.GC_SHOP, shop_locations_gc_shop),
    (Regions.ZD_SHOP, shop_locations_zd_shop)
]

vanilla_items_to_add: list[list[Items]] = [
    [Items.BUY_DEKU_SHIELD, Items.BUY_HYLIAN_SHIELD, Items.BUY_GORON_TUNIC, Items.BUY_ZORA_TUNIC,
        Items.BUY_DEKU_NUTS5, Items.BUY_BOMBS20, Items.BUY_BOMBCHUS10, Items.BUY_DEKU_STICK1],
    [Items.BUY_FAIRYS_SPIRIT, Items.BUY_DEKU_SEEDS30, Items.BUY_ARROWS10, Items.BUY_BLUE_FIRE,
        Items.BUY_RED_POTION30, Items.BUY_GREEN_POTION, Items.BUY_DEKU_NUTS10, Items.BUY_BOMBCHUS10],
    [Items.BUY_BOMBCHUS10, Items.BUY_BOMBCHUS20, Items.BUY_BOMBS525, Items.BUY_BOMBS535,
        Items.BUY_BOMBS10, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS30, Items.BUY_ARROWS50],
    [Items.BUY_ARROWS10, Items.BUY_FAIRYS_SPIRIT, Items.BUY_BOTTLE_BUG, Items.BUY_FISH,
        Items.BUY_HYLIAN_SHIELD, Items.BUY_BOTTLE_BUG, Items.BUY_DEKU_STICK1, Items.BUY_DEKU_STICK1],
    [Items.BUY_BLUE_FIRE, Items.BUY_FISH, Items.BUY_BOMBCHUS10, Items.BUY_DEKU_NUTS5,
        Items.BUY_ARROWS10, Items.BUY_BOMBCHUS20, Items.BUY_BOMBS535, Items.BUY_RED_POTION30],
    [Items.BUY_BOMBS30, Items.BUY_BOMBCHUS20, Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS10,
        Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS30, Items.BUY_RED_POTION40, Items.BUY_FISH],
    [Items.BUY_BOMBCHUS20, Items.BUY_ARROWS30, Items.BUY_RED_POTION50, Items.BUY_ARROWS30,
        Items.BUY_DEKU_NUTS5, Items.BUY_ARROWS50, Items.BUY_ARROWS50, Items.BUY_GREEN_POTION],
    [Items.BUY_POE, Items.BUY_POE, Items.BUY_HEART, Items.BUY_HEART,
        Items.BUY_HEART, Items.BUY_HEART, Items.BUY_HEART, Items.BUY_HEART],
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

    vanilla_shop_locations = [world.get_location(
        slot) for slot in vanilla_shop_slots]
    vanilla_items = [world.create_item(item) for item in vanilla_pool]
    world.multiworld.random.shuffle(vanilla_items)

    # create a filled copy of the state so the multiworld can place the vanilla shop items using logic
    prefill_state = CollectionState(world.multiworld)
    for item in world.item_pool:
        prefill_state.collect(item, True)
    prefill_state.sweep_for_advancements()

    # place the vanilla shop items
    fill_restrictive(world.multiworld, prefill_state, vanilla_shop_locations,
                     vanilla_items, single_player_placement=True, lock=True)
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        world.get_location(slot).address = None
        world.shop_prices[slot] = vanilla_shop_prices[Items(
            location.item.name)]
        world.shop_vanilla_items[slot] = location.item.name

    min_shop_price = world.options.shuffle_shops_minimum_price.value
    max_shop_price = world.options.shuffle_shops_maximum_price.value

    for region, shop in all_shop_locations:
        for slot in shop.keys():
            if slot in world.shop_prices:
                continue
            world.shop_prices[slot] = create_random_price(
                min_shop_price, max_shop_price, world)


def no_shop_shuffle(world: "SohWorld") -> None:
    # put everything in its place as plain vanilla
    for region, shop in all_shop_locations:
        for slot, item in shop.items():
            world.shop_prices[slot] = vanilla_shop_prices[item]
            world.get_location(slot).place_locked_item(world.create_item(item))
            world.get_location(slot).address = None
            world.shop_vanilla_items[slot] = item.value


def generate_scrub_prices(world: "SohWorld") -> None:
    if world.options.shuffle_scrubs:
        min_scrub_price = world.options.shuffle_scrubs_minimum_price.value
        max_scrub_price = world.options.shuffle_scrubs_maximum_price.value

        for slot in scrubs_location_table.keys():
            world.scrub_prices[slot] = create_random_price(
                min_scrub_price, max_scrub_price, world)

        if world.using_ut:
            world.scrub_prices = world.passthrough["scrub_prices"]


def create_random_price(min_price: int, max_price: int, world: "SohWorld") -> int:
    # randrange needs an actual range to work, so just pick the price directly if min/max are the same.
    if min_price == max_price:
        price = min_price
    else:
        price = world.random.randrange(min_price, max_price)

    price = price - (price % 5)
    return price


def set_price_rules(world: "SohWorld") -> None:
    # Shop Price Rules
    for region, shop in all_shop_locations:
        for slot in shop.keys():
            price = world.shop_prices[slot]
            def price_rule(bundle, p=price): return can_afford(p, bundle)
            location = world.get_location(slot)
            add_rule(location, rule_wrapper.wrap(region, price_rule, world))

    # Scrub Price Rules
    if world.options.shuffle_scrubs:
        for slot in scrubs_location_table.keys():
            price = world.scrub_prices[slot]
            def price_rule(bundle, p=price): return can_afford(p, bundle)
            location = world.get_location(slot)
            # Parent region shouldn't matter at all here, so just add ROOT so we don't have to make a list of all scrubs and their regions.
            add_rule(location, rule_wrapper.wrap(
                Regions.ROOT, price_rule, world))
