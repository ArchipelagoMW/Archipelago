from random import Random
from typing import Dict, TYPE_CHECKING, Tuple, NamedTuple

from BaseClasses import LocationProgressType

if TYPE_CHECKING:
    from . import MessengerWorld
else:
    MessengerWorld = object

PROG_SHOP_ITEMS = [
    "Path of Resilience",
    "Meditation",
    "Strike of the Ninja",
    "Second Wind",
    "Currents Master",
    "Aerobatics Warrior",
]

USEFUL_SHOP_ITEMS = [
    "Karuta Plates",
    "Serendipitous Bodies",
    "Kusari Jacket",
    "Energy Shuriken",
    "Serendipitous Minds",
    "Rejuvenate Spirit",
    "Demon's Bane",
]


class ShopData(NamedTuple):
    internal_name: str
    min_price: int
    max_price: int


SHOP_ITEMS: Dict[str, ShopData] = {
    "Karuta Plates":        ShopData("HP_UPGRADE_1", 20, 100),
    "Serendipitous Bodies": ShopData("ENEMY_DROP_HP", 20, 200),
    "Path of Resilience":   ShopData("DAMAGE_REDUCTION", 100, 500),
    "Kusari Jacket":        ShopData("HP_UPGRADE_2", 100, 500),
    "Energy Shuriken":      ShopData("SHURIKEN", 20, 100),
    "Serendipitous Minds":  ShopData("ENEMY_DROP_MANA", 20, 200),
    "Prepared Mind":        ShopData("SHURIKEN_UPGRADE_1", 100, 500),
    "Meditation":           ShopData("CHECKPOINT_FULL", 100, 800),
    "Rejuvenative Spirit":  ShopData("POTION_FULL_HEAL_AND_HP", 400, 1000),
    "Centered Mind":        ShopData("SHURIKEN_UPGRADE_2", 400, 1000),
    "Strike of the Ninja":  ShopData("ATTACK_PROJECTILE", 20, 100),
    "Second Wind":          ShopData("AIR_RECOVER", 20, 150),
    "Currents Master":      ShopData("SWIM_DASH", 100, 500),
    "Aerobatics Warrior":   ShopData("GLIDE_ATTACK", 400, 1000),
    "Demon's Bane":         ShopData("CHARGED_ATTACK", 500, 2000),
    "Devil's Due":          ShopData("QUARBLE_DISCOUNT_50", 20, 100),
    "Time Sense":           ShopData("TIME_WARP", 20, 200),
    "Power Sense":          ShopData("POWER_SEAL", 100, 500),
    "Focused Power Sense":  ShopData("POWER_SEAL_WORLD_MAP", 400, 1000),
}


def shuffle_shop_prices(world: MessengerWorld) -> Dict[str, int]:
    shop_price_mod = world.multiworld.shop_price[world.player].value
    shop_price_planned = world.multiworld.shop_price_plan[world.player]
    random: Random = world.multiworld.per_slot_randoms[world.player]

    shop_prices: Dict[str, int] = {}
    for item, price in shop_price_planned.value.items():
        if isinstance(price, int):
            shop_prices[item] = price
        else:
            shop_prices[item] = random.choices(list(price.keys()), weights=list(price.values()))[0]

    remaining_slots = [item for item in SHOP_ITEMS if item not in shop_prices]
    if remaining_slots:
        for shop_item in remaining_slots:
            shop_data = SHOP_ITEMS[shop_item]
            price = random.randint(shop_data.min_price, shop_data.max_price)
            shop_loc = world.multiworld.get_location(shop_item, world.player)
            if price >= 800:
                shop_loc.progress_type = LocationProgressType.PRIORITY
            elif price <= 200:
                shop_loc.progress_type = LocationProgressType.EXCLUDED
            shop_prices[shop_item] = min(int(price * shop_price_mod / 100), 5000)

    return shop_prices
