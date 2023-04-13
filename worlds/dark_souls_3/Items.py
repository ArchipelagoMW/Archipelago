import sys

from BaseClasses import Item
from worlds.dark_souls_3.data.items_data import item_tables, dlc_shields_table, dlc_weapons_upgrade_10_table, \
    dlc_weapons_upgrade_5_table, dlc_goods_table, dlc_spells_table, dlc_armor_table, dlc_ring_table, dlc_misc_table, dlc_goods_2_table, \
    weapons_upgrade_5_table, weapons_upgrade_10_table, shields_table, armor_table, rings_table, spells_table, items_for_misc_location_list, \
    items_for_dlc_misc_location_list, items_for_npc_location_list


class DarkSouls3Item(Item):
    game: str = "Dark Souls III"

    dlc_set = {**dlc_shields_table, **dlc_weapons_upgrade_10_table, **dlc_weapons_upgrade_5_table,
               **dlc_goods_table, **dlc_spells_table, **dlc_armor_table, **dlc_ring_table, **dlc_misc_table}

    dlc_progressive = {**dlc_goods_2_table}

    weapon_item = {**weapons_upgrade_5_table, **weapons_upgrade_10_table}
    
    dlc_weapon_item = {**dlc_weapons_upgrade_10_table, **dlc_weapons_upgrade_5_table}

    shield_item = {**shields_table}

    dlc_shield_item = {**dlc_shields_table}

    armor_item = {**armor_table}

    dlc_armor_item = {**dlc_armor_table}

    ring_item = {**rings_table}

    dlc_ring_item = {**dlc_ring_table}

    spell_item = {**spells_table}

    dlc_spell_item = {**dlc_spells_table}

    misc_item = ("Braille Divine Tome of Carim",
                 "Great Swamp Pyromancy Tome",
                 "Farron Coal",
                 "Paladin's Ashes",
                 "Deep Braille Divine Tome",
                 "Golden Scroll",
                 "Sage's Coal",
                 "Sage's Scroll",
                 "Dreamchaser's Ashes",
                 "Carthus Pyromancy Tome",
                 "Grave Warden's Ashes",
                 "Grave Warden Pyromancy Tome",
                 "Quelana Pyromancy Tome",
                 "Izalith Pyromancy Tome",
                 "Greirat's Ashes",
                 "Excrement-covered Ashes",
                 "Easterner's Ashes",
                 "Dragon Torso Stone",
                 "Profaned Coal",
                 "Xanthous Ashes",
                 "Logan's Scroll",
                 "Giant's Coal",
                 "Coiled Sword Fragment",
                 "Dragon Chaser's Ashes",
                 "Twinkling Dragon Torso Stone",
                 "Braille Divine Tome of Lothric",
                 "Fire Gem"
                 )

    dlc_misc_item = ("Captains Ashes")

    npc_item = ("Irina's Ashes", "Tower Key (Irina Drop)", "Karla's Ashes", "Karla's Pointed Hat", "Karla's Coat", "Karla's Gloves", "Karla's Trousers",
                "Cornyx's Ashes", "Pyromancy Flame", "Cornyx's Wrap", "Cornyx's Garb", "Cornyx's Skirt", "Orbeck's Ashes")

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

    @staticmethod
    def is_weapon_item(name) -> bool:
        return name in DarkSouls3Item.weapon_item
    
    @staticmethod
    def is_dlc_weapon_item(name) -> bool:
        return name in DarkSouls3Item.dlc_weapon_item
   
    @staticmethod
    def is_shield_item(name) -> bool:
        return name in DarkSouls3Item.shield_item
    
    @staticmethod
    def is_dlc_shield_item(name) -> bool:
        return name in DarkSouls3Item.dlc_shield_item
    
    @staticmethod
    def is_armor_item(name) -> bool:
        return name in DarkSouls3Item.armor_item
    
    @staticmethod
    def is_dlc_armor_item(name) -> bool:
        return name in DarkSouls3Item.dlc_armor_item
    
    @staticmethod
    def is_ring_item(name) -> bool:
        return name in DarkSouls3Item.ring_item
    
    @staticmethod
    def is_dlc_ring_item(name) -> bool:
        return name in DarkSouls3Item.dlc_ring_item
    
    @staticmethod
    def is_spell_item(name) -> bool:
        return name in DarkSouls3Item.spell_item
    
    @staticmethod
    def is_dlc_spell_item(name) -> bool:
        return name in DarkSouls3Item.dlc_spell_item
    
    @staticmethod
    def is_misc_item(name) -> bool:
        return name in DarkSouls3Item.misc_item
    
    @staticmethod
    def is_dlc_misc_item(name) -> bool:
        return name in DarkSouls3Item.dlc_misc_item
    
    @staticmethod
    def is_npc_item(name) -> bool:
        return name in DarkSouls3Item.npc_item