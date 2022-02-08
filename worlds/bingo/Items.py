from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool = True
    event: bool = False


class BingoItem(Item):
    game: str = "Bingo"


bingo_calls = {f"Bingo Call {i}": ItemData(i+999) for i in range(1, 961)}

item_table = {
    **bingo_calls,
    "Completion": ItemData(None)
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
