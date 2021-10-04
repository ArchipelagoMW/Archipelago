from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class TerrariaItem(Item):
    game: str = "Terraria"


item_table = {
    "Copper Shortsword": ItemData(73001, False),

    "Victory": ItemData(73000, True)
}

# If not listed here then has frequency 1
item_frequencies = {
    "Copper Shortsword": 87,
    
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
