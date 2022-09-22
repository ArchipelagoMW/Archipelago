import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    itemID: typing.Optional[int]
    subItemID: typing.Optional[int]
    progression: bool
    sender: str
    type: str
    count: int

class MMBN3Item(Item):
    game: str = "MegaMan Battle Network 3"

item_table = {
    ItemName.Progressive_Undernet_Rank: ItemData(0xB31000, True),
    ItemName.WWW_ID: ItemData(0xB31001, True)
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}