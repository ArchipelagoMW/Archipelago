from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule
from Fill import fill_restrictive

from .LogicHelpers import rule_wrapper, can_afford, can_afford_slot
from .Locations import scrubs_location_table, merchants_items_location_table, scrubs_one_time_only
from .Enums import *
from . import SohItem

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


shop_locations_kf_shop: dict[Locations, Items] = {
    Locations.KF_SHOP_ITEM1: Items.BUY_DEKU_SHIELD,
    Locations.KF_SHOP_ITEM2: Items.BUY_DEKU_NUTS5,
    Locations.KF_SHOP_ITEM3: Items.BUY_DEKU_NUTS10,
    Locations.KF_SHOP_ITEM4: Items.BUY_DEKU_STICK1,
    Locations.KF_SHOP_ITEM5: Items.BUY_DEKU_SEEDS30,
    Locations.KF_SHOP_ITEM6: Items.BUY_ARROWS10,
    Locations.KF_SHOP_ITEM7: Items.BUY_ARROWS30,
    Locations.KF_SHOP_ITEM8: Items.BUY_HEART,
}

shop_locations_market_bazaar: dict[Locations, Items] = {
    Locations.MARKET_BAZAAR_ITEM1: Items.BUY_HYLIAN_SHIELD,
    Locations.MARKET_BAZAAR_ITEM2: Items.BUY_BOMBS535,
    Locations.MARKET_BAZAAR_ITEM3: Items.BUY_DEKU_NUTS5,
    Locations.MARKET_BAZAAR_ITEM4: Items.BUY_HEART,
    Locations.MARKET_BAZAAR_ITEM5: Items.BUY_ARROWS10,
    Locations.MARKET_BAZAAR_ITEM6: Items.BUY_ARROWS50,
    Locations.MARKET_BAZAAR_ITEM7: Items.BUY_DEKU_STICK1,
    Locations.MARKET_BAZAAR_ITEM8: Items.BUY_ARROWS30,
}

shop_locations_market_potion_shop: dict[Locations, Items] = {
    Locations.MARKET_POTION_SHOP_ITEM1: Items.BUY_GREEN_POTION,
    Locations.MARKET_POTION_SHOP_ITEM2: Items.BUY_BLUE_FIRE,
    Locations.MARKET_POTION_SHOP_ITEM3: Items.BUY_RED_POTION30,
    Locations.MARKET_POTION_SHOP_ITEM4: Items.BUY_FAIRYS_SPIRIT,
    Locations.MARKET_POTION_SHOP_ITEM5: Items.BUY_DEKU_NUTS5,
    Locations.MARKET_POTION_SHOP_ITEM6: Items.BUY_BOTTLE_BUG,
    Locations.MARKET_POTION_SHOP_ITEM7: Items.BUY_POE,
    Locations.MARKET_POTION_SHOP_ITEM8: Items.BUY_FISH,
}

shop_locations_market_bombchu_shop: dict[Locations, Items] = {
    Locations.MARKET_BOMBCHU_SHOP_ITEM1: Items.BUY_BOMBCHUS10,
    Locations.MARKET_BOMBCHU_SHOP_ITEM2: Items.BUY_BOMBCHUS10,
    Locations.MARKET_BOMBCHU_SHOP_ITEM3: Items.BUY_BOMBCHUS10,
    Locations.MARKET_BOMBCHU_SHOP_ITEM4: Items.BUY_BOMBCHUS10,
    Locations.MARKET_BOMBCHU_SHOP_ITEM5: Items.BUY_BOMBCHUS20,
    Locations.MARKET_BOMBCHU_SHOP_ITEM6: Items.BUY_BOMBCHUS20,
    Locations.MARKET_BOMBCHU_SHOP_ITEM7: Items.BUY_BOMBCHUS20,
    Locations.MARKET_BOMBCHU_SHOP_ITEM8: Items.BUY_BOMBCHUS20,
}

shop_locations_kak_bazaar: dict[Locations, Items] = {
    Locations.KAK_BAZAAR_ITEM1: Items.BUY_HYLIAN_SHIELD,
    Locations.KAK_BAZAAR_ITEM2: Items.BUY_BOMBS535,
    Locations.KAK_BAZAAR_ITEM3: Items.BUY_DEKU_NUTS5,
    Locations.KAK_BAZAAR_ITEM4: Items.BUY_HEART,
    Locations.KAK_BAZAAR_ITEM5: Items.BUY_ARROWS10,
    Locations.KAK_BAZAAR_ITEM6: Items.BUY_ARROWS50,
    Locations.KAK_BAZAAR_ITEM7: Items.BUY_DEKU_STICK1,
    Locations.KAK_BAZAAR_ITEM8: Items.BUY_ARROWS30,
}

shop_locations_kak_potion_shop: dict[Locations, Items] = {
    Locations.KAK_POTION_SHOP_ITEM1: Items.BUY_GREEN_POTION,
    Locations.KAK_POTION_SHOP_ITEM2: Items.BUY_BLUE_FIRE,
    Locations.KAK_POTION_SHOP_ITEM3: Items.BUY_RED_POTION30,
    Locations.KAK_POTION_SHOP_ITEM4: Items.BUY_FAIRYS_SPIRIT,
    Locations.KAK_POTION_SHOP_ITEM5: Items.BUY_DEKU_NUTS5,
    Locations.KAK_POTION_SHOP_ITEM6: Items.BUY_BOTTLE_BUG,
    Locations.KAK_POTION_SHOP_ITEM7: Items.BUY_POE,
    Locations.KAK_POTION_SHOP_ITEM8: Items.BUY_FISH,
}

shop_locations_gc_shop: dict[Locations, Items] = {
    Locations.GC_SHOP_ITEM1: Items.BUY_BOMBS525,
    Locations.GC_SHOP_ITEM2: Items.BUY_BOMBS10,
    Locations.GC_SHOP_ITEM3: Items.BUY_BOMBS20,
    Locations.GC_SHOP_ITEM4: Items.BUY_BOMBS30,
    Locations.GC_SHOP_ITEM5: Items.BUY_GORON_TUNIC,
    Locations.GC_SHOP_ITEM6: Items.BUY_HEART,
    Locations.GC_SHOP_ITEM7: Items.BUY_RED_POTION40,
    Locations.GC_SHOP_ITEM8: Items.BUY_HEART,
}

shop_locations_zd_shop: dict[Locations, Items] = {
    Locations.ZD_SHOP_ITEM1: Items.BUY_ZORA_TUNIC,
    Locations.ZD_SHOP_ITEM2: Items.BUY_ARROWS10,
    Locations.ZD_SHOP_ITEM3: Items.BUY_HEART,
    Locations.ZD_SHOP_ITEM4: Items.BUY_ARROWS30,
    Locations.ZD_SHOP_ITEM5: Items.BUY_DEKU_NUTS5,
    Locations.ZD_SHOP_ITEM6: Items.BUY_ARROWS50,
    Locations.ZD_SHOP_ITEM7: Items.BUY_FISH,
    Locations.ZD_SHOP_ITEM8: Items.BUY_RED_POTION30,
}

all_shop_locations: list[tuple[Regions, dict[Locations, Items]]] = [
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

def get_vanilla_shop_pool(world: "SohWorld") -> list[Items]:
    vanilla_shop_pool = list[Items]()
    if not world.options.shuffle_shops:
        for region, shop in all_shop_locations:
            for item in shop.values():
                vanilla_shop_pool.append(item)
        return vanilla_shop_pool

    num_vanilla = 8 - world.options.shuffle_shops_item_amount
    for i in range(0, num_vanilla):
        vanilla_shop_pool += vanilla_items_to_add[i]
    return vanilla_shop_pool

def get_vanilla_shop_locations(world: "SohWorld") -> list[str]:
    vanilla_shop_slots = list[str]()
    if not world.options.shuffle_shops:
        for region, shop in all_shop_locations:
            for slot in shop.keys():
                vanilla_shop_slots.append(slot)
        return vanilla_shop_slots

    # select what shop slots to and vanilla items to shuffle
    num_vanilla = 8 - world.options.shuffle_shops_item_amount
    for region, shop in all_shop_locations:
        vanilla_shop_slots += list(shop.keys())[0: num_vanilla]
    return vanilla_shop_slots


def reserve_vanilla_shop_locations(world: "SohWorld") -> None:
    if not world.options.shuffle_shops:
        return
    vanilla_shop_slots = get_vanilla_shop_locations(world)
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        location.place_locked_item(world.create_item(Items.RESERVATION))

def remove_vanilla_shop_reservations(world: "SohWorld") -> None:
    vanilla_shop_slots = get_vanilla_shop_locations(world)
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        if location.item == world.create_item(Items.RESERVATION):
            location.item = None
            location.locked = False

def fill_shop_items(world: "SohWorld") -> None:
    # if we're using UT, we just want to place the event shop items in their proper spots
    if world.using_ut:
        world.shop_vanilla_items = world.passthrough["shop_vanilla_items"]
        world.shop_prices = world.passthrough["shop_prices"]
        for slot, item in world.shop_vanilla_items.items():
            location = world.get_location(slot)
            location.address = None
            location.place_locked_item(world.create_item(item, create_as_event=True))
        return

    if not world.options.shuffle_shops:
        return

    remove_vanilla_shop_reservations(world)
    
    # select what shop slots to and vanilla items to shuffle
    num_vanilla = 8 - world.options.shuffle_shops_item_amount
    vanilla_pool = get_vanilla_shop_pool(world)
    vanilla_items = list[SohItem]()
    for item in vanilla_pool:
        world.pre_fill_pool.remove(item)
        vanilla_items.append(world.create_item(item))

    vanilla_shop_slots = get_vanilla_shop_locations(world)
    vanilla_shop_locations = [world.get_location(slot) for slot in vanilla_shop_slots]
    world.random.shuffle(vanilla_items)

    goal_locations = [loc for loc in vanilla_shop_locations]
    world.multiworld.completion_condition[world.player] = lambda state: all([state.can_reach(loc) for loc in goal_locations])

    prefill_state = world.get_pre_fill_state()

    # place the vanilla shop items
    fill_restrictive(world.multiworld, prefill_state, vanilla_shop_locations,
                     vanilla_items, single_player_placement=True, lock=True)
    
    for slot in vanilla_shop_slots:
        location = world.get_location(slot)
        location.address = None
        world.shop_prices[slot] = vanilla_shop_prices[Items(location.item.name)]
        world.shop_vanilla_items[slot] = location.item.name


def no_shop_shuffle(world: "SohWorld") -> None:
    # put everything in its place as plain vanilla
    for region, shop in all_shop_locations:
        for slot, item in shop.items():
            world.shop_prices[slot] = vanilla_shop_prices[item]
            world.get_location(slot).place_locked_item(world.create_item(item))
            world.get_location(slot).address = None
            world.shop_vanilla_items[slot] = item.value


def generate_shop_prices(world: "SohWorld") -> None:
    if not world.options.shuffle_shops:
        return

    min_shop_price = world.options.shuffle_shops_minimum_price.value
    max_shop_price = world.options.shuffle_shops_maximum_price.value

    for region, shop in all_shop_locations:
        for slot in shop.keys():
            world.shop_prices[slot] = create_random_price(min_shop_price, max_shop_price, world)


def generate_scrub_prices(world: "SohWorld") -> None:
    if world.options.shuffle_scrubs:
        min_scrub_price = world.options.shuffle_scrubs_minimum_price.value
        max_scrub_price = world.options.shuffle_scrubs_maximum_price.value

        if world.options.shuffle_scrubs == "all":
            for slot in scrubs_location_table.keys():
                world.scrub_prices[slot] = create_random_price(
                    min_scrub_price, max_scrub_price, world)
        else:
            for slot in scrubs_one_time_only:
                world.scrub_prices[slot] = create_random_price(
                    min_scrub_price, max_scrub_price, world)

        if world.using_ut:
            world.scrub_prices = world.passthrough["scrub_prices"]


def generate_merchant_prices(world: "SohWorld") -> None:
    if world.options.shuffle_merchants:
        min_merchant_price = world.options.shuffle_merchants_minimum_price.value
        max_merchant_price = world.options.shuffle_merchants_maximum_price.value

        for slot in merchants_items_location_table.keys():
            if world.options.shuffle_merchants == "bean_merchant_only" and slot != Locations.ZR_MAGIC_BEAN_SALESMAN:
                continue
            if world.options.shuffle_merchants == "all_but_beans" and slot == Locations.ZR_MAGIC_BEAN_SALESMAN:
                continue

            world.merchant_prices[slot] = create_random_price(min_merchant_price, max_merchant_price, world)

        if world.using_ut and "merchant_prices" in world.passthrough:
            world.merchant_prices = world.passthrough["merchant_prices"]


def create_random_price(min_price: int, max_price: int, world: "SohWorld") -> int:
    # randrange needs an actual range to work, so just pick the price directly if min/max are the same.
    if min_price == max_price:
        price = min_price
    else:
        price = world.random.randrange(min_price, max_price)

    price = price - (price % 5)
    return price


def set_price_rules(world: "SohWorld") -> None:
    if world.options.true_no_logic:
        return
    # Shop Price Rules
    for region, shop in all_shop_locations:
        for slot in shop.keys():
            def shop_rule(bundle, s=slot): return can_afford_slot(str(s), bundle)
            location = world.get_location(slot)
            add_rule(location, rule_wrapper.wrap(region, shop_rule, world))

    # Scrub Price Rules
    if world.options.shuffle_scrubs:
        scrubs_list = list()
        if world.options.shuffle_scrubs == "all":
            scrubs_list = scrubs_location_table.keys()
        else:
            scrubs_list += [location for location in scrubs_one_time_only]
        for slot in scrubs_list:
            price = world.scrub_prices[slot]
            def price_rule(bundle, p=price): return can_afford(p, bundle)
            location = world.get_location(slot)
            # Parent region shouldn't matter at all here, so just add ROOT so we don't have to make a list of all scrubs and their regions.
            add_rule(location, rule_wrapper.wrap(
                Regions.ROOT, price_rule, world))
            
    # Merchant Price Rules
    if world.options.shuffle_merchants:
        for slot in merchants_items_location_table.keys():
            if world.options.shuffle_merchants == "bean_merchant_only" and slot != Locations.ZR_MAGIC_BEAN_SALESMAN:
                continue
            if world.options.shuffle_merchants == "all_but_beans" and slot == Locations.ZR_MAGIC_BEAN_SALESMAN:
                continue

            price = world.merchant_prices[slot]
            def price_rule(bundle, p=price): return can_afford(p, bundle)
            location = world.get_location(slot)
            add_rule(location, rule_wrapper.wrap(location.parent_region, price_rule, world))
