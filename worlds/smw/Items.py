import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    quantity: int = 1
    event: bool = False


class SMWItem(Item):
    game: str = "Super Mario World"


# Separate tables for each type of item.
junk_table = {
    ItemName.one_coin:        ItemData(0xBC0017, False),
    ItemName.five_coins:      ItemData(0xBC0018, False),
    ItemName.ten_coins:       ItemData(0xBC0019, False),
    ItemName.fifty_coins:     ItemData(0xBC001A, False),
    ItemName.one_up_mushroom: ItemData(0xBC0001, False),
}

collectable_table = {
    ItemName.yoshi_egg:       ItemData(0xBC0002, True),
}

upgrade_table = {
    ItemName.mario_run:           ItemData(0xBC0003, True),
    ItemName.mario_carry:         ItemData(0xBC0004, True),
    ItemName.mario_swim:          ItemData(0xBC0005, True),
    ItemName.mario_spin_jump:     ItemData(0xBC0006, True),
    ItemName.mario_climb:         ItemData(0xBC0007, True),
    ItemName.yoshi_activate:      ItemData(0xBC0008, True),
    ItemName.p_switch:            ItemData(0xBC0009, True),
    ItemName.progressive_powerup: ItemData(0xBC000A, True),
    ItemName.p_balloon:           ItemData(0xBC000B, True),
    ItemName.super_star_active:   ItemData(0xBC000D, True),
    ItemName.special_world_clear: ItemData(0xBC001B, True),
}

switch_palace_table = {
    ItemName.yellow_switch_palace: ItemData(0xBC000E, True),
    ItemName.green_switch_palace:  ItemData(0xBC000F, True),
    ItemName.red_switch_palace:    ItemData(0xBC0010, True),
    ItemName.blue_switch_palace:   ItemData(0xBC0011, True),
}

trap_table = {
    ItemName.ice_trap:              ItemData(0xBC0013, False, True),
    ItemName.stun_trap:             ItemData(0xBC0014, False, True),
    ItemName.literature_trap:       ItemData(0xBC0015, False, True),
    ItemName.timer_trap:            ItemData(0xBC0016, False, True),
    ItemName.reverse_controls_trap: ItemData(0xBC001C, False, True),
    ItemName.thwimp_trap:           ItemData(0xBC001D, False, True),
}

event_table = {
    ItemName.victory:   ItemData(0xBC0000, True),
    ItemName.koopaling: ItemData(0xBC0012, True),
}

# Complete item table.
item_table = {
    **junk_table,
    **collectable_table,
    **upgrade_table,
    **switch_palace_table,
    **trap_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
