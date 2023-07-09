from BaseClasses import Item
import typing

class ItemData(typing.NamedTuple) :
    progression: bool

class GoldenSunItem(Item):
    game: str = "Golden Sun: The Dark Age"

item_table = {
    "Battle Axe": ItemData (27, False) ,
}

item_frequencies = {
    "Battle Axe": 87
}

lookup_id_to_name: typing.Dict[int,str] = {data.code: item_name for item_name,data in item_table.items() if data.code}