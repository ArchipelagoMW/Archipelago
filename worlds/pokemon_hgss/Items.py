from dataclasses import dataclass

from BaseClasses import Item, ItemClassification


GAME_NAME = "Pokemon HeartGold SoulSilver"


class PokemonHGSSItem(Item):
    game = GAME_NAME


@dataclass(frozen=True)
class ItemData:
    code: int | None
    classification: ItemClassification


ITEM_TABLE = {
    "Zephyr Badge": ItemData(835000001, ItemClassification.progression),
    "Hive Badge": ItemData(835000002, ItemClassification.progression),
    "Plain Badge": ItemData(835000003, ItemClassification.progression),
    "Fog Badge": ItemData(835000004, ItemClassification.progression),
    "Storm Badge": ItemData(835000005, ItemClassification.progression),
    "Mineral Badge": ItemData(835000006, ItemClassification.progression),
    "Glacier Badge": ItemData(835000007, ItemClassification.progression),
    "Rising Badge": ItemData(835000008, ItemClassification.progression),

    # Event item.
    # This is not placed in the random item pool.
    # It is locked to "Pokemon League - Defeat Lance".
    "Victory": ItemData(None, ItemClassification.progression),
}


item_name_to_id = {
    item_name: item_data.code
    for item_name, item_data in ITEM_TABLE.items()
    if item_data.code is not None
}


def create_item(player: int, item_name: str) -> PokemonHGSSItem:
    item_data = ITEM_TABLE[item_name]

    return PokemonHGSSItem(
        item_name,
        item_data.classification,
        item_data.code,
        player,
    )