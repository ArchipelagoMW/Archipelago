from BaseClasses import Item
import typing
from .names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    skip_balancing: bool = False
    trap: bool = False


class K64Item(Item):
    game = "Kirby 64 - The Crystal Shards"


copy_ability_table = {
    ItemName.burn:      ItemData(0x640001, True),
    ItemName.stone:     ItemData(0x640002, True),
    ItemName.ice:       ItemData(0x640003, True),
    ItemName.needle:    ItemData(0x640004, True),
    ItemName.bomb:      ItemData(0x640005, True),
    ItemName.spark:     ItemData(0x640006, True),
    ItemName.cutter:    ItemData(0x640007, True)
}

friend_table = {
    ItemName.waddle_dee:    ItemData(0x640100, True),
    ItemName.adeleine:      ItemData(0x640101, True),
    ItemName.king_dedede:   ItemData(0x600102, True),
}

power_combo_table = {
    ItemName.burn_burn:     ItemData(0x640200, True),
    ItemName.burn_stone:    ItemData(0x640201, True),
    ItemName.burn_ice:      ItemData(0x640202, True),
    ItemName.burn_needle:   ItemData(0x640203, True),
    ItemName.burn_bomb:     ItemData(0x640204, True),
    ItemName.burn_spark:    ItemData(0x640205, True),
    ItemName.burn_cutter:   ItemData(0x640206, True),
    ItemName.stone_stone:   ItemData(0x640207, True),
    ItemName.stone_ice:     ItemData(0x640208, True),
    ItemName.stone_needle:  ItemData(0x640209, True),
    ItemName.stone_bomb:    ItemData(0x64020A, True),
    ItemName.stone_spark:   ItemData(0x64020B, True),
    ItemName.stone_cutter:  ItemData(0x64020C, True),
    ItemName.ice_ice:       ItemData(0x64020D, True),
    ItemName.ice_needle:    ItemData(0x64020E, True),
    ItemName.ice_bomb:      ItemData(0x64020F, True),
    ItemName.ice_spark:     ItemData(0x640210, True),
    ItemName.ice_cutter:    ItemData(0x640211, True),
    ItemName.needle_needle: ItemData(0x640212, True),
    ItemName.needle_bomb:   ItemData(0x640213, True),
    ItemName.needle_spark:  ItemData(0x640214, True),
    ItemName.needle_cutter: ItemData(0x640215, True),
    ItemName.bomb_bomb:     ItemData(0x640216, True),
    ItemName.bomb_spark:    ItemData(0x640217, True),
    ItemName.bomb_cutter:   ItemData(0x640218, True),
    ItemName.spark_spark:   ItemData(0x640219, True),
    ItemName.spark_cutter:  ItemData(0x64021A, True),
    ItemName.cutter_cutter: ItemData(0x64021B, True),
}

power_combo_map = {
    (1, 1): ItemName.burn_burn,
    (1, 2): ItemName.burn_stone,
    (1, 3): ItemName.burn_ice,
    (1, 4): ItemName.burn_needle,
    (1, 5): ItemName.burn_bomb,
    (1, 6): ItemName.burn_spark,
    (1, 7): ItemName.burn_cutter,
    (2, 2): ItemName.stone_stone,
    (2, 3): ItemName.stone_ice,
    (2, 4): ItemName.stone_needle,
    (2, 5): ItemName.stone_bomb,
    (2, 6): ItemName.stone_spark,
    (2, 7): ItemName.stone_cutter,
    (3, 3): ItemName.ice_ice,
    (3, 4): ItemName.ice_needle,
    (3, 5): ItemName.ice_bomb,
    (3, 6): ItemName.ice_spark,
    (3, 7): ItemName.ice_cutter,
    (4, 4): ItemName.needle_needle,
    (4, 5): ItemName.needle_bomb,
    (4, 6): ItemName.needle_spark,
    (4, 7): ItemName.needle_cutter,
    (5, 5): ItemName.bomb_bomb,
    (5, 6): ItemName.bomb_spark,
    (5, 7): ItemName.bomb_cutter,
    (6, 6): ItemName.spark_spark,
    (6, 7): ItemName.spark_cutter,
    (7, 7): ItemName.cutter_cutter,
}

copy_ability_access_table = {
    "No Ability": ItemData(None, False),
    "Burning Ability": ItemData(None, True),
    "Stone Ability": ItemData(None, True),
    "Ice Ability": ItemData(None, True),
    "Needle Ability": ItemData(None, True),
    "Bomb Ability": ItemData(None, True),
    "Spark Ability": ItemData(None, True),
    "Cutter Ability": ItemData(None, True),
}

misc_item_table = {
    ItemName.crystal_shard: ItemData(0x640020, True, True),
    ItemName.one_up: ItemData(0x640021, False),
    ItemName.maxim_tomato: ItemData(0x640022, False),
    ItemName.invincibility_candy: ItemData(0x640023, False),
}

filler_item_weights = {
    ItemName.one_up: 4,
    ItemName.maxim_tomato: 2,
    ItemName.invincibility_candy: 2,
}


item_table = {
    **copy_ability_table,
    **power_combo_table,
    **copy_ability_access_table,
    **friend_table,
    **misc_item_table,
}

power_combo_aliases = {}

for i, ability in enumerate(copy_ability_table, 1):
    for j, other in enumerate(copy_ability_table, 1):
        group_name = f"{ability}/{other}"
        if group_name not in power_combo_aliases:
            power_combo_aliases[group_name] = {power_combo_map[min((i,j), (j, i))]}

item_names = {
    "Copy Ability": {name for name in copy_ability_table.keys()},
    "Power Combo": {name for name in power_combo_table.keys()},
    "Friend": {name for name in friend_table.keys()},
    **power_combo_aliases
}

lookup_name_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
