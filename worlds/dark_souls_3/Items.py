import sys

from BaseClasses import Item
from worlds.dark_souls_3.data.items_data import item_tables, dlc_shields_table, dlc_weapons_upgrade_10_table, \
    dlc_weapons_upgrade_5_table, dlc_goods_table, dlc_spells_table, dlc_armor_table, dlc_ring_table, dlc_misc_table, dlc_goods_2_table


class DarkSouls3Item(Item):
    game: str = "Dark Souls III"

    dlc_set = {**dlc_shields_table, **dlc_weapons_upgrade_10_table, **dlc_weapons_upgrade_5_table,
               **dlc_goods_table, **dlc_spells_table, **dlc_armor_table, **dlc_ring_table, **dlc_misc_table}

    dlc_progressive = {**dlc_goods_2_table}

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 100000
        table_offset = 100

        output = {}
        for i, table in enumerate(item_tables):
            if len(table) > table_offset:
                raise Exception("An item table has {} entries, that is more than {} entries (table #{})".format(len(table), table_offset, i))
            output.update({name: id for id, name in enumerate(table, base_id + (table_offset * i))})

        return output

    @staticmethod
    def is_dlc_item(name) -> bool:
        return name in DarkSouls3Item.dlc_set

    @staticmethod
    def is_dlc_progressive(name) -> bool:
        return name in DarkSouls3Item.dlc_progressive

