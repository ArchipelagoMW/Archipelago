from BaseClasses import Item
import typing
import Names


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool


class MM2Item(Item):
    game = "Mega Man 2"


robot_master_weapon_table = {
    Names.crash_bomber: ItemData(0x880001, True),
    Names.metal_blade: ItemData(0x880002, True),
    Names.quick_boomerang: ItemData(0x880003, True),
    Names.bubble_lead: ItemData(0x880004, True),
    Names.atomic_fire: ItemData(0x880005, True),
    Names.leaf_shield: ItemData(0x880006, True),
    Names.time_stopper: ItemData(0x880007, True),
    Names.air_shooter: ItemData(0x880008, True)
}

item_item_table = {
    Names.item_1: ItemData(0x880011, True),
    Names.item_2: ItemData(0x880012, True),
    Names.item_3: ItemData(0x880013, True)
}

filler_item_table = {
    Names.one_up: ItemData(0x880020, False),
    Names.weapon_energy: ItemData(0x880021, False),
    Names.health_energy: ItemData(0x880022, False),
    Names.e_tank: ItemData(0x880023, False),
}

filler_item_weights = {
    Names.one_up: ItemData(0x880020, False),
    Names.weapon_energy: ItemData(0x880021, False),
    Names.health_energy: ItemData(0x880022, False),
    Names.e_tank: ItemData(0x880023, False),
}

item_table = {
    **robot_master_weapon_table,
    **item_item_table,
    **filler_item_table,
}

item_names = {
    "Weapons": {name for name in robot_master_weapon_table.keys()},
    "Items": {name for name in item_item_table.keys()}
}

lookup_name_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
