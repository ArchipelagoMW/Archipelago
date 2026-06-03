from dataclasses import dataclass
from random import Random

from BaseClasses import Item, ItemClassification


GAME_NAME = "Pokemon HeartGold SoulSilver"


class PokemonHGSSItem(Item):
    game = GAME_NAME


@dataclass(frozen=True)
class ItemData:
    code: int | None
    classification: ItemClassification
    pool_count: int = 1


BADGE_ITEMS = {
    "Zephyr Badge",
    "Hive Badge",
    "Plain Badge",
    "Fog Badge",
    "Storm Badge",
    "Mineral Badge",
    "Glacier Badge",
    "Rising Badge",
}


HM_ITEMS = {
    "HM01 Cut",
    "HM03 Surf",
    "HM04 Strength",
    "HM05 Whirlpool",
    "HM07 Waterfall",
}


KEY_ITEMS = {
    "SquirtBottle",
    "SecretPotion",
    "Radio Card",
    "Basement Key",
    "Card Key",
    "Machine Part",
}


FILLER_ITEMS = {
    "Potion",
    "Super Potion",
    "Hyper Potion",
    "Full Heal",
    "Escape Rope",
    "Repel",
    "Max Repel",
    "Nugget",
    "Rare Candy",
    "PP Up",
}


EVENT_ITEMS = {
    "Victory",
}


ITEM_TABLE = {
    # Johto badges
    "Zephyr Badge": ItemData(835000001, ItemClassification.progression),
    "Hive Badge": ItemData(835000002, ItemClassification.progression),
    "Plain Badge": ItemData(835000003, ItemClassification.progression),
    "Fog Badge": ItemData(835000004, ItemClassification.progression),
    "Storm Badge": ItemData(835000005, ItemClassification.progression),
    "Mineral Badge": ItemData(835000006, ItemClassification.progression),
    "Glacier Badge": ItemData(835000007, ItemClassification.progression),
    "Rising Badge": ItemData(835000008, ItemClassification.progression),

    # HM progression items
    "HM01 Cut": ItemData(835000020, ItemClassification.progression),
    "HM03 Surf": ItemData(835000021, ItemClassification.progression),
    "HM04 Strength": ItemData(835000022, ItemClassification.progression),
    "HM05 Whirlpool": ItemData(835000023, ItemClassification.progression),
    "HM07 Waterfall": ItemData(835000024, ItemClassification.progression),

    # Key progression items
    "SquirtBottle": ItemData(835000040, ItemClassification.progression),
    "SecretPotion": ItemData(835000041, ItemClassification.progression),
    "Radio Card": ItemData(835000042, ItemClassification.progression),
    "Basement Key": ItemData(835000043, ItemClassification.progression),
    "Card Key": ItemData(835000044, ItemClassification.progression),
    "Machine Part": ItemData(835000045, ItemClassification.progression),

    # Filler items
    # These are available as filler, but are not all placed every seed.
    "Potion": ItemData(835000100, ItemClassification.filler, pool_count=0),
    "Super Potion": ItemData(835000101, ItemClassification.filler, pool_count=0),
    "Hyper Potion": ItemData(835000102, ItemClassification.filler, pool_count=0),
    "Full Heal": ItemData(835000103, ItemClassification.filler, pool_count=0),
    "Escape Rope": ItemData(835000104, ItemClassification.filler, pool_count=0),
    "Repel": ItemData(835000105, ItemClassification.filler, pool_count=0),
    "Max Repel": ItemData(835000106, ItemClassification.filler, pool_count=0),
    "Nugget": ItemData(835000107, ItemClassification.filler, pool_count=0),
    "Rare Candy": ItemData(835000108, ItemClassification.filler, pool_count=0),
    "PP Up": ItemData(835000109, ItemClassification.filler, pool_count=0),

    # Event item
    # This is not placed in the random item pool.
    # It is locked to "Pokemon League - Defeat Lance".
    "Victory": ItemData(None, ItemClassification.progression, pool_count=0),
}


item_name_to_id = {
    item_name: item_data.code
    for item_name, item_data in ITEM_TABLE.items()
    if item_data.code is not None
}


item_name_groups = {
    "Badges": BADGE_ITEMS,
    "HMs": HM_ITEMS,
    "Key Items": KEY_ITEMS,
    "Filler": FILLER_ITEMS,
    "Events": EVENT_ITEMS,
    "Progression": BADGE_ITEMS | HM_ITEMS | KEY_ITEMS,
}


def get_required_item_pool_names() -> list[str]:
    item_pool_names: list[str] = []

    for item_name, item_data in ITEM_TABLE.items():
        if item_data.code is None:
            continue

        if item_data.classification == ItemClassification.filler:
            continue

        for _ in range(item_data.pool_count):
            item_pool_names.append(item_name)

    return item_pool_names


def get_random_filler_items(random: Random, filler_count: int) -> list[str]:
    filler_item_names = sorted(FILLER_ITEMS)

    return [
        random.choice(filler_item_names)
        for _ in range(filler_count)
    ]


def get_item_pool_names(random: Random, location_count: int) -> list[str]:
    item_pool_names = get_required_item_pool_names()

    filler_count = location_count - len(item_pool_names)

    if filler_count < 0:
        raise ValueError(
            "HGSS item pool has more required items than available locations. "
            f"Required items: {len(item_pool_names)}, "
            f"Locations: {location_count}."
        )

    item_pool_names.extend(
        get_random_filler_items(random, filler_count)
    )

    return item_pool_names


def create_item(player: int, item_name: str) -> PokemonHGSSItem:
    item_data = ITEM_TABLE[item_name]

    return PokemonHGSSItem(
        item_name,
        item_data.classification,
        item_data.code,
        player,
    )