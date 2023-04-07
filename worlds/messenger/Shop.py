from random import Random
from typing import Dict, TYPE_CHECKING

from BaseClasses import LocationProgressType

if TYPE_CHECKING:
    from . import MessengerWorld
else:
    MessengerWorld = object


SHOP_ITEMS = {
    "Karuta Plates": "HP_UPGRADE_1",
    "Serendipitous Bodies": "ENEMY_DROP_HP",
    "Path of Resilience": "DAMAGE_REDUCTION",
    "Kusari Jacket": "HP_UPGRADE_2",
    "Energy Shuriken": "SHURIKEN",
    "Serendipitous Minds": "ENEMY_DROP_MANA",
    "Prepared Mind": "SHURIKEN_UPGRADE_1",
    "Meditation": "CHECKPOINT_FULL",
    "Rejuvenative Spirit": "POTION_FULL_HEAL_AND_HP",
    "Centered Mind": "SHURIKEN_UPGRADE_2",
    "Strike of the Ninja": "ATTACK_PROJECTILE",
    "Second Wind": "AIR_RECOVER",
    "Currents Master": "SWIM_DASH",
    "Aerobatics Warrior": "GLIDE_ATTACK",
    "Demon's Bane": "CHARGED_ATTACK",
    "Devil's Due": "QUARBLE_DISCOUNT_50",
    "Time Sense": "TIME_WARP",
    "Power Sense": "POWER_SEAL",
    "Focused Power Sense": "POWER_SEAL_WORLD_MAP",
}


def shuffle_shop_prices(world: MessengerWorld) -> Dict[str, int]:
    shop_price_mod = world.multiworld.shop_price[world.player].value
    shop_price_planned = world.multiworld.shop_price_plan[world.player]

    shop_prices: Dict[str, int] = {}
    for item, price in shop_price_planned.value.items():
        shop_prices[item] = price

    remaining_slots = [item for item in shop_price_mod.valid_keys if item not in shop_prices]
    if remaining_slots and shop_price_mod:
        random: Random = world.multiworld.per_slot_randoms[world.player]
        for shop_item in remaining_slots:
            price = random.randint(20, 2000)
            shop_loc = world.multiworld.get_location(shop_item, world.player)
            if price >= 800:
                shop_loc.progress_type = LocationProgressType.PRIORITY
            elif price <= 200:
                shop_loc.progress_type = LocationProgressType.EXCLUDED
            shop_prices[shop_item] = min(int(price * shop_price_mod / 100), 5000)

    return shop_prices
