from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class ChecksFinderItem(Item):
    game: str = "ChecksFinder"


item_table = {
    "Map Width": ItemData(80000, True),
    "Map Height": ItemData(80001, True),
    "Map Bombs": ItemData(80002, True),
}

required_items = {
}

item_frequencies = {

}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
