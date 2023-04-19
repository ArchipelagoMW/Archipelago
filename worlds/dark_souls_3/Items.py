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

    weapon_item = ("Irithyll Straight Sword", 
                   "Chaos Blade", 
                   "Dragonrider Bow", 
                   "White Hair Talisman", 
                   "Izalith Staff", 
                   "Fume Ultra Greatsword", 
                   "Black Knight Sword", 
                   "Yorshka's Spear", 
                   "Smough's Great Hammer", 
                   "Dragonslayer Greatbow", 
                   "Golden Ritual Spear", 
                   "Eleonora", 
                   "Witch's Locks", 
                   "Crystal Chime", 
                   "Black Knight Glaive", 
                   "Dragonslayer Spear", 
                   "Caitha's Chime", 
                   "Sunlight Straight Sword", 
                   "Firelink Greatsword",
                   "Hollowslayer Greatsword",
                   "Arstor's Spear",
                   "Vordt's Great Hammer",
                   "Crystal Sage's Rapier",
                   "Farron Greatsword",
                   "Wolf Knight's Greatsword",
                   "Dancer's Enchanted Swords",
                   "Wolnir's Holy Sword",
                   "Demon's Greataxe",
                   "Demon's Fist",
                   "Old King's Great Hammer",
                   "Greatsword of Judgment",
                   "Profaned Greatsword",
                   "Yhorm's Great Machete",
                   "Cleric's Candlestick",
                   "Dragonslayer Greataxe",
                   "Moonlight Greatsword",
                   "Gundyr's Halberd", 
                   "Lothric's Holy Sword", 
                   "Lorian's Greatsword", 
                   "Twin Princes' Greatsword", 
                   "Storm Curved Sword", 
                   "Dragonslayer Swordspear", 
                   "Sage's Crystal Staff", 
                   "Irithyll Rapier", 
                   "Dragon Tooth",  #NEW
                   "Deep Battle Axe", 
                   "Club", 
                   "Astora's Straight Sword", 
                   "Lucerne", 
                   "Reinforced Club", 
                   "Caestus", 
                   "Partizan", 
                   "Red Hilted Halberd", 
                   "Saint's Talisman", 
                   "Large Club", 
                   "Brigand Twindaggers", 
                   "Butcher Knife", 
                   "Brigand Axe", 
                   "Heretic's Staff", 
                   "Great Club", 
                   "Exile Greatsword", 
                   "Sellsword Twinblades", 
                   "Notched Whip", 
                   "Astora Greatsword", 
                   "Executioner's Greatsword", 
                   "Saint-tree Bellvine", 
                   "Saint Bident", 
                   "Drang Hammers", 
                   "Arbalest", 
                   "Sunlight Talisman", 
                   "Greatsword", 
                   "Black Bow of Pharis", 
                   "Great Axe", 
                   "Black Blade", 
                   "Blacksmith Hammer", 
                   "Witchtree Branch", 
                   "Painting Guardian's Curved Sword", 
                   "Court Sorcerer's Staff", 
                   "Avelyn", 
                   "Onikiri and Ubadachi", 
                   "Ricard's Rapier", 
                   "Drakeblood Greatsword", 
                   "Greatlance", 
                   "Claw", 
                   "Drang Twinspears", 
                   "Gotthard Twinswords"  # On Black Hand Gotthard corpse | NEW
                   )
    
    dlc_weapon_item = {**dlc_weapons_upgrade_10_table, **dlc_weapons_upgrade_5_table}

    shield_item = {**shields_table}

    dlc_shield_item = {**dlc_shields_table}

    armor_item = ("Fire Keeper Robe", 
                  "Fire Keeper Gloves", 
                  "Fire Keeper Skirt", 
                  "Deserter Trousers",
                  "Cleric Hat", 
                  "Cleric Blue Robe", 
                  "Cleric Gloves", 
                  "Cleric Trousers", 
                  "Northern Helm", 
                  "Northern Armor", 
                  "Northern Gloves", 
                  "Northern Trousers", 
                  "Loincloth", 
                  "Brigand Hood", 
                  "Brigand Armor", 
                  "Brigand Gauntlets", 
                  "Brigand Trousers", 
                  "Sorcerer Hood", 
                  "Sorcerer Robe", 
                  "Sorcerer Gloves", 
                  "Sorcerer Trousers", 
                  "Fallen Knight Helm", 
                  "Fallen Knight Armor", 
                  "Fallen Knight Gauntlets", 
                  "Fallen Knight Trousers", 
                  "Conjurator Hood", 
                  "Conjurator Robe", 
                  "Conjurator Manchettes", 
                  "Conjurator Boots", 
                  "Sellsword Helm", 
                  "Sellsword Armor", 
                  "Sellsword Gauntlet", 
                  "Sellsword Trousers", 
                  "Herald Helm", 
                  "Herald Armor", 
                  "Herald Gloves", 
                  "Herald Trousers", 
                  "Maiden Hood", 
                  "Maiden Robe", 
                  "Maiden Gloves", 
                  "Maiden Skirt", 
                  "Drang Armor", 
                  "Drang Gauntlets", 
                  "Drang Shoes", 
                  "Archdeacon White Crown", 
                  "Archdeacon Holy Garb", 
                  "Archdeacon Skirt", 
                  "Antiquated Dress", 
                  "Antiquated Gloves", 
                  "Antiquated Skirt", 
                  "Ragged Mask", 
                  "Crown of Dusk", 
                  "Pharis's Hat", 
                  "Old Sage's Blindfold", 
                  "Painting Guardian Hood", 
                  "Painting Guardian Gown", 
                  "Painting Guardian Gloves", 
                  "Painting Guardian Waistcloth", 
                  "Brass Helm", 
                  "Brass Armor", 
                  "Brass Gauntlets", 
                  "Brass Leggings", 
                  "Old Sorcerer Hat", 
                  "Old Sorcerer Coat", 
                  "Old Sorcerer Gauntlets", 
                  "Old Sorcerer Boots", 
                  "Court Sorcerer Hood", 
                  "Court Sorcerer Robe", 
                  "Court Sorcerer Gloves", 
                  "Court Sorcerer Trousers", 
                  "Dragonslayer Helm", 
                  "Dragonslayer Armor", 
                  "Dragonslayer Gauntlets", 
                  "Dragonslayer Leggings", 
                  "Hood of Prayer", 
                  "Robe of Prayer", 
                  "Skirt of Prayer", 
                  "Winged Knight Helm", 
                  "Winged Knight Armor", 
                  "Winged Knight Gauntlets", 
                  "Winged Knight Leggings", 
                  "Shadow Mask", 
                  "Shadow Garb", 
                  "Shadow Gauntlets", 
                  "Shadow Leggings", 
                  "Outrider Knight Helm", 
                  "Outrider Knight Armor", 
                  "Outrider Knight Gauntlets", 
                  "Outrider Knight Leggings", 
                  "Nameless Knight Helm",  #NEW
                  "Nameless Knight Armor",  #NEW
                  "Nameless Knight Gauntlets",
                  "Nameless Knight Leggings"
                  )

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

    npc_item = ("Greirat's Ashes",
                "Irina's Ashes",
                "Karla's Ashes",
                "Karla's Pointed Hat",
                "Karla's Coat",
                "Karla's Gloves",
                "Karla's Trousers",
                "Cornyx's Ashes",
                "Pyromancy Flame",
                "Cornyx's Wrap",
                "Cornyx's Garb",
                "Cornyx's Skirt",
                "Orbeck's Ashes")

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