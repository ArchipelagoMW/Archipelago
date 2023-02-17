from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class PokemonEmeraldItem(Item):
    game: str = "Pokemon Emerald"


item_table = {
    "Potion": ItemData(13, False),
    "Rare Candy": ItemData(68, True),
}

required_items = {
    "Rare Candy": 1
}

item_frequencies = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
