import typing
from BaseClasses import Item
from worlds.dark_souls_3.data.locations_data import dictionary_table


class ItemData(typing.NamedTuple):
    code: int
    progression: bool


class DarkSouls3Item(Item):
    game: str = "Dark Souls III"

    @staticmethod
    def get_item_name_to_id() -> typing.Dict[str, int]:
        return dictionary_table
