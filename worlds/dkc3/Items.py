import typing

from BaseClasses import Item
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


class DKC3Item(Item):
    game: str = "Donkey Kong Country 3"


# Separate tables for each type of item.
junk_table = {
    ItemName.one_up_balloon: ItemData(0xDC3001, False),
    ItemName.bear_coin:      ItemData(0xDC3002, False),
}

collectable_table = {
    ItemName.bonus_coin:       ItemData(0xDC3003, True),
    ItemName.dk_coin:          ItemData(0xDC3004, True),
    ItemName.banana_bird:      ItemData(0xDC3005, True),
    ItemName.krematoa_cog:     ItemData(0xDC3006, True),
    ItemName.progressive_boat: ItemData(0xDC3007, True),
}

inventory_table = {
    ItemName.present:      ItemData(0xDC3008, True),
    ItemName.bowling_ball: ItemData(0xDC3009, True),
    ItemName.shell:        ItemData(0xDC300A, True),
    ItemName.mirror:       ItemData(0xDC300B, True),
    ItemName.flower:       ItemData(0xDC300C, True),
    ItemName.wrench:       ItemData(0xDC300D, True),
}

event_table = {
    ItemName.victory: ItemData(0xDC3000, True),
}

# Complete item table.
item_table = {
    **junk_table,
    **collectable_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
