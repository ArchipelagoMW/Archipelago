from dataclasses import dataclass

from BaseClasses import Item, ItemClassification


GAME_NAME = "Pokemon HeartGold SoulSilver"


class PokemonHGSSItem(Item):
    game = GAME_NAME


@dataclass(frozen=True)
class ItemData:
    code: int | None
    classification: ItemClassification
    count: int = 1


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
    "Rare Candy": ItemData(835000100, ItemClassification.filler, count=3),

    # Event item
    # This is not placed in the random item pool.
    # It is locked to "Pokemon League - Defeat Lance".
    "Victory": ItemData(None, ItemClassification.progression, count=0),
}


item_name_to_id = {
    item_name: item_data.code
    for item_name, item_data in ITEM_TABLE.items()
    if item_data.code is not None
}


def get_item_pool_names() -> list[str]:
    item_pool_names: list[str] = []

    for item_name, item_data in ITEM_TABLE.items():
        if item_data.code is None:
            continue

        for _ in range(item_data.count):
            item_pool_names.append(item_name)

    return item_pool_names


def create_item(player: int, item_name: str) -> PokemonHGSSItem:
    item_data = ITEM_TABLE[item_name]

    return PokemonHGSSItem(
        item_name,
        item_data.classification,
        item_data.code,
        player,
    )