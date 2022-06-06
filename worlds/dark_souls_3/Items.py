import typing
from BaseClasses import Item
from worlds.dark_souls_3.data.items_data import item_dictionary_table


class DarkSouls3Item(Item):
    game: str = "Dark Souls III"

    @staticmethod
    def get_item_name_to_id() -> typing.Dict[str, int]:
        return item_dictionary_table
