from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class ChecksFinderItem(Item):
    game: str = "ChecksFinder"


item_table = {
    "Map Width": ItemData(80000, True),
    "Map Height": ItemData(80000, True),
    "Map Bomb": ItemData(80000, True),
}

# 33 required items
required_items = {
    "Archery": 1,
}

item_frequencies = {
    "Map Width": 9,
    "Map Height": 9,
    "Map Bomb": 15,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
