from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from . import MessengerWorld
else:
    MessengerWorld = object

PROG_SHOP_ITEMS: list[str] = [
    "Path of Resilience",
    "Meditation",
    "Strike of the Ninja",
    "Second Wind",
    "Currents Master",
    "Aerobatics Warrior",
]

USEFUL_SHOP_ITEMS: list[str] = [
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
    prerequisite: str | set[str] | None = None


SHOP_ITEMS: dict[str, ShopData] = {
    "Karuta Plates":        ShopData("HP_UPGRADE_1", 20, 200),
    "Serendipitous Bodies": ShopData("ENEMY_DROP_HP", 20, 300, "The Shop - Karuta Plates"),
    "Path of Resilience":   ShopData("DAMAGE_REDUCTION", 100, 500, "The Shop - Serendipitous Bodies"),
    "Kusari Jacket":        ShopData("HP_UPGRADE_2", 100, 500, "The Shop - Serendipitous Bodies"),
    "Energy Shuriken":      ShopData("SHURIKEN", 20, 200),
    "Serendipitous Minds":  ShopData("ENEMY_DROP_MANA", 20, 300, "The Shop - Energy Shuriken"),
    "Prepared Mind":        ShopData("SHURIKEN_UPGRADE_1", 100, 600, "The Shop - Serendipitous Minds"),
    "Meditation":           ShopData("CHECKPOINT_FULL", 100, 600,
                                     {"The Shop - Prepared Mind", "The Shop - Kusari Jacket"}),
    "Rejuvenative Spirit":  ShopData("POTION_FULL_HEAL_AND_HP", 300, 800, "The Shop - Meditation"),
    "Centered Mind":        ShopData("SHURIKEN_UPGRADE_2", 300, 800, "The Shop - Meditation"),
    "Strike of the Ninja":  ShopData("ATTACK_PROJECTILE", 20, 200),
    "Second Wind":          ShopData("AIR_RECOVER", 20, 350, "The Shop - Strike of the Ninja"),
    "Currents Master":      ShopData("SWIM_DASH", 100, 600, "The Shop - Second Wind"),
    "Aerobatics Warrior":   ShopData("GLIDE_ATTACK", 300, 800, "The Shop - Currents Master"),
    "Demon's Bane":         ShopData("CHARGED_ATTACK", 400, 1000,
                                     {"The Shop - Rejuvenative Spirit", "The Shop - Aerobatics Warrior"}),
    "Devil's Due":          ShopData("QUARBLE_DISCOUNT_50", 20, 200),
    "Time Sense":           ShopData("TIME_WARP", 20, 300),
    "Power Sense":          ShopData("POWER_SEAL", 100, 800, "The Shop - Time Sense"),
    "Focused Power Sense":  ShopData("POWER_SEAL_WORLD_MAP", 300, 600, "The Shop - Power Sense"),
}

FIGURINES: dict[str, ShopData] = {
    "Green Kappa Figurine":         ShopData("GREEN_KAPPA", 100, 500),
    "Blue Kappa Figurine":          ShopData("BLUE_KAPPA", 100, 500),
    "Ountarde Figurine":            ShopData("OUNTARDE", 100, 500),
    "Red Kappa Figurine":           ShopData("RED_KAPPA", 100, 500),
    "Demon King Figurine":          ShopData("DEMON_KING", 600, 2000),
    "Quillshroom Figurine":         ShopData("QUILLSHROOM", 100, 500),
    "Jumping Quillshroom Figurine": ShopData("JUMPING_QUILLSHROOM", 100, 500),
    "Scurubu Figurine":             ShopData("SCURUBU", 100, 500),
    "Jumping Scurubu Figurine":     ShopData("JUMPING_SCURUBU", 100, 500),
    "Wallaxer Figurine":            ShopData("WALLAXER", 100, 500),
    "Barmath'azel Figurine":        ShopData("BARMATHAZEL", 600, 2000),
    "Queen of Quills Figurine":     ShopData("QUEEN_OF_QUILLS", 400, 1000),
    "Demon Hive Figurine":          ShopData("DEMON_HIVE", 100, 500),
}


def shuffle_shop_prices(world: MessengerWorld) -> tuple[dict[str, int], dict[str, int]]:
    shop_price_mod = world.options.shop_price.value
    shop_price_planned = world.options.shop_price_plan

    shop_prices: dict[str, int] = {}
    figurine_prices: dict[str, int] = {}
    for item, price in shop_price_planned.value.items():
        if not isinstance(price, int):
            price = world.random.choices(list(price.keys()), weights=list(price.values()))[0]
        if "Figurine" in item:
            figurine_prices[item] = price
        else:
            shop_prices[item] = price

    remaining_slots = [item for item in [*SHOP_ITEMS, *FIGURINES] if item not in shop_price_planned.value]
    for shop_item in remaining_slots:
        shop_data = SHOP_ITEMS.get(shop_item, FIGURINES.get(shop_item))
        price = world.random.randint(shop_data.min_price, shop_data.max_price)
        adjusted_price = min(int(price * shop_price_mod / 100), 5000)
        if "Figurine" in shop_item:
            figurine_prices[shop_item] = adjusted_price
        else:
            shop_prices[shop_item] = adjusted_price

    return shop_prices, figurine_prices
