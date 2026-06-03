from BaseClasses import Item, ItemClassification


GAME_NAME = "Pokemon HeartGold SoulSilver"


class PokemonHGSSItem(Item):
    game = GAME_NAME


ITEM_TABLE = {
    "Zephyr Badge": {
        "id": 835000001,
        "classification": ItemClassification.progression,
    },
    "Hive Badge": {
        "id": 835000002,
        "classification": ItemClassification.progression,
    },
    "Plain Badge": {
        "id": 835000003,
        "classification": ItemClassification.progression,
    },
    "Fog Badge": {
        "id": 835000004,
        "classification": ItemClassification.progression,
    },
    "Storm Badge": {
        "id": 835000005,
        "classification": ItemClassification.progression,
    },
    "Mineral Badge": {
        "id": 835000006,
        "classification": ItemClassification.progression,
    },
    "Glacier Badge": {
        "id": 835000007,
        "classification": ItemClassification.progression,
    },
    "Rising Badge": {
        "id": 835000008,
        "classification": ItemClassification.progression,
    },
}


item_name_to_id = {
    item_name: item_data["id"]
    for item_name, item_data in ITEM_TABLE.items()
}


def create_item(player: int, item_name: str) -> PokemonHGSSItem:
    item_data = ITEM_TABLE[item_name]

    return PokemonHGSSItem(
        item_name,
        item_data["classification"],
        item_data["id"],
        player,
    )