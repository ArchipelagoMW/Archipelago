"""This module provides data structures for individual items occupying a vendor slot"""
from dataclasses import dataclass

from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.locations.vendors import RAC3VENDORLOCATION
from worlds.rac3.constants.region import RAC3REGION
from worlds.rac3.constants.vendors.vendor import RAC3ARMORVENDOR, RAC3SHIPVENDOR, RAC3SKINVENDOR, RAC3WEAPONVENDOR


@dataclass
class RAC3VENDORSLOTDATA:
    """Struct for the data of individual items occupying slots in a vendor"""

    @dataclass
    class Property:
        """Structure for storing the data of each property of a vendor item"""
        name: str
        value: int
        read: int
        size: int
        offset: int

        def __init__(self,
                     name: str,
                     value: int = 0,
                     read: int = 0,
                     size: int = 1,
                     offset: int = 0):
            self.name = name
            self.value = value
            self.read = read
            self.size = size
            self.offset = offset

        def read_property(self):
            """format the value correctly for printing"""
            match self.read:
                case 0:
                    return self.value
                case 1:
                    return bool(self.value)
                case 2:
                    return hex(self.value)
            return None

    def get_data(self) -> list[Property]:
        """return a list containing the data of each property this item has"""
        return []


@dataclass
class RAC3WEAPONVENDORSLOTDATA(RAC3VENDORSLOTDATA):
    item_id: RAC3VENDORSLOTDATA.Property
    ammo_text: RAC3VENDORSLOTDATA.Property
    item_class: RAC3VENDORSLOTDATA.Property
    free: RAC3VENDORSLOTDATA.Property
    mega: RAC3VENDORSLOTDATA.Property
    all_ammo: RAC3VENDORSLOTDATA.Property
    memcard: RAC3VENDORSLOTDATA.Property

    def __init__(self,
                 item_id: int = 0,
                 ammo_text: int = 0,
                 item_class: int = 0x0CDB,
                 free: int = 0,
                 mega: int = 0,
                 all_ammo: int = 0,
                 memcard: int = 0):
        self.item_id = self.Property("ID", item_id, 2, RAC3WEAPONVENDOR.ITEM_ID_SIZE, RAC3WEAPONVENDOR.ITEM_ID_OFFSET)
        self.ammo_text = self.Property("Ammo text?", ammo_text, 1, RAC3WEAPONVENDOR.ITEM_AMMO_TEXT_SIZE,
                                       RAC3WEAPONVENDOR.ITEM_AMMO_TEXT_OFFSET)
        self.item_class = self.Property("Class", item_class, 2, RAC3WEAPONVENDOR.ITEM_CLASS_SIZE,
                                        RAC3WEAPONVENDOR.ITEM_CLASS_OFFSET)
        self.free = self.Property("Free?", free, 1, RAC3WEAPONVENDOR.ITEM_COST_SIZE, RAC3WEAPONVENDOR.ITEM_COST_OFFSET)
        self.mega = self.Property("Mega?", mega, 1, RAC3WEAPONVENDOR.ITEM_MEGA_SIZE, RAC3WEAPONVENDOR.ITEM_MEGA_OFFSET)
        self.all_ammo = self.Property("All Ammo?", all_ammo, 1, RAC3WEAPONVENDOR.ITEM_ALL_AMMO_SIZE,
                                      RAC3WEAPONVENDOR.ITEM_ALL_AMMO_OFFSET)
        self.memcard = self.Property("Memory Card?", memcard, 1, RAC3WEAPONVENDOR.ITEM_MEMCARD_SIZE,
                                     RAC3WEAPONVENDOR.ITEM_MEMCARD_OFFSET)

    def get_data(self) -> list[RAC3VENDORSLOTDATA.Property]:
        """return a list containing the data of each property this item has"""
        return [self.item_id, self.ammo_text, self.item_class,
                self.free, self.mega, self.all_ammo, self.memcard]


@dataclass
class RAC3ARMORVENDORSLOTDATA(RAC3VENDORSLOTDATA):
    icon: RAC3VENDORSLOTDATA.Property
    cost: RAC3VENDORSLOTDATA.Property
    armor_level: RAC3VENDORSLOTDATA.Property

    def __init__(self,
                 icon: int = 0,
                 cost: int = 0,
                 armor_level: int = 0):
        self.icon = self.Property("Icon", icon, 2, RAC3ARMORVENDOR.ITEM_ICON_SIZE, RAC3ARMORVENDOR.ITEM_ICON_OFFSET)
        self.cost = self.Property("Cost", cost, 0, RAC3ARMORVENDOR.ITEM_COST_SIZE,
                                  RAC3ARMORVENDOR.ITEM_COST_OFFSET)
        self.armor_level = self.Property("Armor Level", armor_level, 0, RAC3ARMORVENDOR.ITEM_LEVEL_SIZE,
                                         RAC3ARMORVENDOR.ITEM_LEVEL_OFFSET)

    def get_data(self) -> list[RAC3VENDORSLOTDATA.Property]:
        """return a list containing the data of each property this item has"""
        return [self.icon, self.cost, self.armor_level]


@dataclass
class RAC3SHIPVENDORSLOTDATA(RAC3VENDORSLOTDATA):
    icon_id: RAC3VENDORSLOTDATA.Property
    cost: RAC3VENDORSLOTDATA.Property
    highlighted_part: RAC3VENDORSLOTDATA.Property
    color_id: RAC3VENDORSLOTDATA.Property
    ship_config: RAC3VENDORSLOTDATA.Property
    unlock_id: RAC3VENDORSLOTDATA.Property
    item_name_ptr: RAC3VENDORSLOTDATA.Property
    icon_color: RAC3VENDORSLOTDATA.Property
    is_equipped: RAC3VENDORSLOTDATA.Property

    def __init__(self,
                 icon_id: int = 0,
                 cost: int = 0,
                 highlighted_part: int = 0,
                 color_id: int = 0,
                 ship_config: int = 0,
                 unlock_id: int = 0,
                 item_name_ptr: int = 0,
                 icon_color: int = 0,
                 is_equipped: int = 0):
        self.icon_id = self.Property("Icon ID", icon_id, 2, RAC3SHIPVENDOR.ITEM_ICON_SIZE,
                                     RAC3SHIPVENDOR.ITEM_ICON_OFFSET)
        self.cost = self.Property("Cost", cost, 0, RAC3SHIPVENDOR.ITEM_COST_SIZE, RAC3SHIPVENDOR.ITEM_COST_OFFSET)
        self.highlighted_part = self.Property("Highlighted Part", highlighted_part, 2,
                                              RAC3SHIPVENDOR.ITEM_HIGHLIGHTED_PART_SIZE,
                                              RAC3SHIPVENDOR.ITEM_HIGHLIGHTED_PART_OFFSET)
        self.color_id = self.Property("Color ID", color_id, 2, RAC3SHIPVENDOR.ITEM_COLOR_ID_SIZE,
                                      RAC3SHIPVENDOR.ITEM_COLOR_ID_OFFSET)
        self.ship_config = self.Property("Ship Config", ship_config, 2, RAC3SHIPVENDOR.ITEM_SHIP_CONFIG_SIZE,
                                         RAC3SHIPVENDOR.ITEM_SHIP_CONFIG_OFFSET)
        self.unlock_id = self.Property("Unlock ID", unlock_id, 2, RAC3SHIPVENDOR.ITEM_UNLOCK_ID_SIZE,
                                       RAC3SHIPVENDOR.ITEM_UNLOCK_ID_OFFSET)
        self.item_name_ptr = self.Property("Item Name Pointer", item_name_ptr, 2, RAC3SHIPVENDOR.ITEM_NAME_PTR_SIZE,
                                           RAC3SHIPVENDOR.ITEM_NAME_PTR_OFFSET)
        self.icon_color = self.Property("Icon Color", icon_color, 2, RAC3SHIPVENDOR.ITEM_ICON_COLOR_SIZE,
                                        RAC3SHIPVENDOR.ITEM_ICON_COLOR_OFFSET)
        self.is_equipped = self.Property("Is Equipped?", is_equipped, 1, RAC3SHIPVENDOR.ITEM_IS_EQUIPPED_SIZE,
                                         RAC3SHIPVENDOR.ITEM_IS_EQUIPPED_OFFSET)

    def get_data(self) -> list[RAC3VENDORSLOTDATA.Property]:
        """return a list containing the data of each property this item has"""
        return [self.icon_id, self.cost, self.highlighted_part, self.color_id,
                self.ship_config, self.unlock_id, self.item_name_ptr, self.icon_color, self.is_equipped]


class RAC3SKINVENDORSLOTDATA(RAC3VENDORSLOTDATA):
    cost: RAC3VENDORSLOTDATA.Property
    skin_id: RAC3VENDORSLOTDATA.Property
    description_string_id: RAC3VENDORSLOTDATA.Property

    def __init__(self,
                 cost: int = 0,
                 skin_id: int = 0,
                 description_string_id: int = 0):
        self.cost = self.Property("Cost", cost, 0, RAC3SKINVENDOR.ITEM_COST_SIZE, RAC3SKINVENDOR.ITEM_COST_OFFSET)
        self.skin_id = self.Property("Skin ID", skin_id, 2, RAC3SKINVENDOR.ITEM_SKIN_ID_SIZE,
                                     RAC3SKINVENDOR.ITEM_SKIN_ID_OFFSET)
        self.description_string_id = self.Property("Description String ID", description_string_id, 2,
                                                   RAC3SKINVENDOR.ITEM_DESCRIPTION_STRING_ID_SIZE,
                                                   RAC3SKINVENDOR.ITEM_DESCRIPTION_STRING_ID_OFFSET)

    def get_data(self) -> list[RAC3VENDORSLOTDATA.Property]:
        """return a list containing the data of each property this item has"""
        return [self.cost, self.skin_id, self.description_string_id]


WEAPON_VENDOR_LOCATION_TO_ITEM: dict[str, str] = {
    RAC3LOCATION.VELDIN_FIRST_RANGER: RAC3ITEM.SHOCK_BLASTER,
    RAC3LOCATION.VELDIN_SECOND_RANGER: RAC3ITEM.NITRO_LAUNCHER,
    RAC3VENDORLOCATION.FLORANA_WHIP: RAC3ITEM.PLASMA_WHIP,
    RAC3VENDORLOCATION.FLORANA_N60: RAC3ITEM.N60_STORM,
    RAC3VENDORLOCATION.PHOENIX_SUCK: RAC3ITEM.SUCK_CANNON,
    RAC3VENDORLOCATION.PHOENIX_INFECTOR: RAC3ITEM.INFECTOR,
    RAC3VENDORLOCATION.MARCADIA_HYDRA: RAC3ITEM.SPITTING_HYDRA,
    RAC3VENDORLOCATION.NATION_AGENTS: RAC3ITEM.AGENTS_OF_DOOM,
    RAC3VENDORLOCATION.AQUATOS_FLUX_RIFLE: RAC3ITEM.FLUX_RIFLE,
    RAC3VENDORLOCATION.AQUATOS_MINI_TURRET: RAC3ITEM.MINI_TURRET,
    RAC3VENDORLOCATION.AQUATOS_LAVA_GUN: RAC3ITEM.LAVA_GUN,
    RAC3VENDORLOCATION.AQUATOS_SHIELD_CHARGER: RAC3ITEM.SHIELD_CHARGER,
    RAC3VENDORLOCATION.AQUATOS_BOUNCER: RAC3ITEM.BOUNCER,
    RAC3VENDORLOCATION.AQUATOS_PLASMA_COIL: RAC3ITEM.PLASMA_COIL,
    RAC3VENDORLOCATION.TYHRRANOSIS_ANNIHILATOR: RAC3ITEM.ANNIHILATOR,
    RAC3VENDORLOCATION.TYHRRANOSIS_SHIELD_GLOVE: RAC3ITEM.HOLO_SHIELD,
    RAC3VENDORLOCATION.OBANI_GEMINI_DISC: RAC3ITEM.DISC_BLADE,
    RAC3VENDORLOCATION.HOLOSTAR_RIFT_INDUCER: RAC3ITEM.RIFT_INDUCER,
    RAC3VENDORLOCATION.ARIDIA_QWACK_O_RAY: RAC3ITEM.QWACK_O_RAY,
    RAC3VENDORLOCATION.NGPLUS_RY3N0: RAC3ITEM.RY3N0,
}
ITEM_TO_WEAPON_VENDOR_LOCATION: dict[str, str] = {item: location for location, item in
                                                  WEAPON_VENDOR_LOCATION_TO_ITEM.items()}
WEAPON_VENDOR_LOCATION_TO_UNLOCK_REGION: dict[str, str] = {
    RAC3LOCATION.VELDIN_FIRST_RANGER: RAC3REGION.VELDIN,
    RAC3LOCATION.VELDIN_SECOND_RANGER: RAC3REGION.VELDIN,
    RAC3VENDORLOCATION.FLORANA_WHIP: RAC3REGION.FLORANA,
    RAC3VENDORLOCATION.FLORANA_N60: RAC3REGION.FLORANA,
    RAC3VENDORLOCATION.PHOENIX_SUCK: RAC3REGION.STARSHIP_PHOENIX,
    RAC3VENDORLOCATION.PHOENIX_INFECTOR: RAC3REGION.STARSHIP_PHOENIX,
    RAC3VENDORLOCATION.MARCADIA_HYDRA: RAC3REGION.MARCADIA,
    RAC3VENDORLOCATION.NATION_AGENTS: RAC3REGION.ANNIHILATION_NATION,
    RAC3VENDORLOCATION.AQUATOS_FLUX_RIFLE: RAC3REGION.AQUATOS,
    RAC3VENDORLOCATION.AQUATOS_MINI_TURRET: RAC3REGION.AQUATOS,
    RAC3VENDORLOCATION.AQUATOS_LAVA_GUN: RAC3REGION.AQUATOS,
    RAC3VENDORLOCATION.AQUATOS_SHIELD_CHARGER: RAC3REGION.COMMAND_CENTER,
    RAC3VENDORLOCATION.AQUATOS_BOUNCER: RAC3REGION.QWARKS_HIDEOUT,
    RAC3VENDORLOCATION.AQUATOS_PLASMA_COIL: RAC3REGION.KOROS,
    RAC3VENDORLOCATION.TYHRRANOSIS_ANNIHILATOR: RAC3REGION.TYHRRANOSIS,
    RAC3VENDORLOCATION.TYHRRANOSIS_SHIELD_GLOVE: RAC3REGION.TYHRRANOSIS,
    RAC3VENDORLOCATION.OBANI_GEMINI_DISC: RAC3REGION.OBANI_GEMINI,
    RAC3VENDORLOCATION.HOLOSTAR_RIFT_INDUCER: RAC3REGION.HOLOSTAR_STUDIOS,
    RAC3VENDORLOCATION.ARIDIA_QWACK_O_RAY: RAC3REGION.ARIDIA,
    RAC3VENDORLOCATION.NGPLUS_RY3N0: RAC3REGION.STARSHIP_PHOENIX,
}
ARMOR_VENDOR_LOCATION_TO_ITEM: dict[str, str] = {
    RAC3VENDORLOCATION.PHOENIX_MAGNA_ARMOR: RAC3ITEM.MAGNAPLATE,
    RAC3VENDORLOCATION.PHOENIX_ADAMANTINE: RAC3ITEM.ADAMANTINE,
    RAC3VENDORLOCATION.PHOENIX_AEGIS_ARMOR: RAC3ITEM.AEGIS,
    RAC3VENDORLOCATION.PHOENIX_INFERNOX: RAC3ITEM.INFERNOX,
}
ITEM_TO_ARMOR_VENDOR_LOCATION: dict[str, str] = {item: location for location, item in
                                                 ARMOR_VENDOR_LOCATION_TO_ITEM.items()}
ARMOR_VENDOR_LOCATION_TO_UNLOCK_REGION: dict[str, str] = {
    RAC3VENDORLOCATION.PHOENIX_MAGNA_ARMOR: RAC3REGION.STARSHIP_PHOENIX,
    RAC3VENDORLOCATION.PHOENIX_ADAMANTINE: RAC3REGION.AQUATOS,
    RAC3VENDORLOCATION.PHOENIX_AEGIS_ARMOR: RAC3REGION.ZELDRIN_STARPORT,
    RAC3VENDORLOCATION.PHOENIX_INFERNOX: RAC3REGION.KOROS
}
ARMOR_VENDOR_INVENTORY: dict[str, RAC3ARMORVENDORSLOTDATA] = {
    RAC3VENDORLOCATION.PHOENIX_MAGNA_ARMOR: RAC3ARMORVENDORSLOTDATA(0xEA93, 10000, 0x1),
    RAC3VENDORLOCATION.PHOENIX_ADAMANTINE: RAC3ARMORVENDORSLOTDATA(0xEA94, 60000, 0x2),
    RAC3VENDORLOCATION.PHOENIX_AEGIS_ARMOR: RAC3ARMORVENDORSLOTDATA(0xEA95, 250000, 0x3),
    RAC3VENDORLOCATION.PHOENIX_INFERNOX: RAC3ARMORVENDORSLOTDATA(0xEA96, 1000000, 0x4),
}
SHIP_VENDOR_INVENTORY: dict[str, RAC3SHIPVENDORSLOTDATA] = {
    RAC3VENDORLOCATION.PHOENIX_WINGS_1: RAC3SHIPVENDORSLOTDATA(5, 2000, 0xC, 0, 0, 0, 0x1c21160),
    RAC3VENDORLOCATION.PHOENIX_WINGS_2: RAC3SHIPVENDORSLOTDATA(6, 4000, 0xC, 0, 4, 1, 0x1c1ff4a),
    RAC3VENDORLOCATION.PHOENIX_WINGS_3: RAC3SHIPVENDORSLOTDATA(7, 6000, 0xC, 0, 8, 2, 0x1c1ff58),
    RAC3VENDORLOCATION.PHOENIX_NOSE_1: RAC3SHIPVENDORSLOTDATA(3, 8000, 0x3, 0, 0, 3, 0x1c2116f),
    RAC3VENDORLOCATION.PHOENIX_NOSE_2: RAC3SHIPVENDORSLOTDATA(4, 10000, 0x3, 0, 1, 4, 0x1c1ff79),
    RAC3VENDORLOCATION.PHOENIX_NOSE_3: RAC3SHIPVENDORSLOTDATA(2, 12000, 0x3, 0, 2, 5, 0x1c1ff6e),
    RAC3VENDORLOCATION.PHOENIX_SKIN_1: RAC3SHIPVENDORSLOTDATA(0, 14000, 0x1f0000, 0, 0, 6, 0x1c1fc64, 0x15236d),
    RAC3VENDORLOCATION.PHOENIX_SKIN_2: RAC3SHIPVENDORSLOTDATA(0, 15000, 0x1f0000, 0x17, 0, 7, 0x1c249d3, 0x4ea220),
    RAC3VENDORLOCATION.PHOENIX_SKIN_3: RAC3SHIPVENDORSLOTDATA(0, 16000, 0x1f0000, 0x19, 0, 8, 0x1c24a25, 0xa0215e),
    RAC3VENDORLOCATION.PHOENIX_SKIN_4: RAC3SHIPVENDORSLOTDATA(0, 17000, 0x1f0000, 0x18, 0, 9, 0x1c24ae7, 0x7bbe),
    RAC3VENDORLOCATION.PHOENIX_SKIN_5: RAC3SHIPVENDORSLOTDATA(0, 18000, 0x1f0000, 0x1a, 0, 0xa, 0x1c24b27, 0x99900a),
    RAC3VENDORLOCATION.PHOENIX_SKIN_6: RAC3SHIPVENDORSLOTDATA(0, 19000, 0x1f0000, 0x1b, 0, 0xb, 0x1c24a50, 0xb8565d),
    RAC3VENDORLOCATION.PHOENIX_SKIN_7: RAC3SHIPVENDORSLOTDATA(0, 20000, 0x1f0000, 0x1c, 0, 0xc, 0x1c249e2, 0x1f60ac),
    RAC3VENDORLOCATION.PHOENIX_SKIN_8: RAC3SHIPVENDORSLOTDATA(0, 21000, 0x1f0000, 2, 0, 0xd, 0x1c1fcac, 0x543d1c),
    RAC3VENDORLOCATION.PHOENIX_SKIN_9: RAC3SHIPVENDORSLOTDATA(0, 22000, 0x1f0000, 1, 0, 0xe, 0x1c1fc71, 0x185527),
    RAC3VENDORLOCATION.PHOENIX_SKIN_10: RAC3SHIPVENDORSLOTDATA(0, 23000, 0x1f0000, 0xd, 0, 0xf, 0x1c1fcb7, 0x471a4),
    RAC3VENDORLOCATION.PHOENIX_SKIN_11: RAC3SHIPVENDORSLOTDATA(0, 24000, 0x1f0000, 0x10, 0, 0x10, 0x1c24b31, 0x1f1fe3),
    RAC3VENDORLOCATION.PHOENIX_SKIN_12: RAC3SHIPVENDORSLOTDATA(0, 25000, 0x1f0000, 0x14, 0, 0x11, 0x1c1fca0, 0x229038),
    RAC3VENDORLOCATION.PHOENIX_SKIN_13: RAC3SHIPVENDORSLOTDATA(0, 26000, 0x1f0000, 0x15, 0, 0x12, 0x1c24a7e, 0x429af),
    RAC3VENDORLOCATION.PHOENIX_SKIN_14: RAC3SHIPVENDORSLOTDATA(0, 27000, 0x1f0000, 0x16, 0, 0x13, 0x1c24abf, 0x89461e),
    RAC3VENDORLOCATION.PHOENIX_SKIN_15: RAC3SHIPVENDORSLOTDATA(0, 28000, 0x1f0000, 6, 0, 0x14, 0x1c1fce6, 0x364a3b),
    RAC3VENDORLOCATION.PHOENIX_SKIN_16: RAC3SHIPVENDORSLOTDATA(0, 29000, 0x1f0000, 0x11, 0, 0x15, 0x1c24b03, 0x638035),
    RAC3VENDORLOCATION.PHOENIX_SKIN_17: RAC3SHIPVENDORSLOTDATA(0, 30000, 0x1f0000, 0x12, 0, 0x16, 0x1c24af4, 0x5e1d54),
    RAC3VENDORLOCATION.PHOENIX_SKIN_18: RAC3SHIPVENDORSLOTDATA(0, 31000, 0x1f0000, 0x13, 0, 0x17, 0x1c24a6a, 0x94493c),
    RAC3VENDORLOCATION.PHOENIX_SKIN_19: RAC3SHIPVENDORSLOTDATA(0, 32000, 0x1f0000, 0x1d, 0, 0x18, 0x1c24aca, 0xaacea8),
    RAC3VENDORLOCATION.PHOENIX_SKIN_20: RAC3SHIPVENDORSLOTDATA(0, 33000, 0x1f0000, 0x1e, 0, 0x19, 0x1c24a34, 0xf3b067),
    RAC3VENDORLOCATION.PHOENIX_SKIN_21: RAC3SHIPVENDORSLOTDATA(0, 34000, 0x1f0000, 0x1f, 0, 0x1a, 0x1c24b68, 0xbbd7),
    RAC3VENDORLOCATION.PHOENIX_SKIN_22: RAC3SHIPVENDORSLOTDATA(0, 35000, 0x1f0000, 0xc, 0, 0x1b, 0x1c1fd08, 0x544c49),
    RAC3VENDORLOCATION.PHOENIX_SKIN_23: RAC3SHIPVENDORSLOTDATA(0, 36000, 0x1f0000, 9, 0, 0x1c, 0x1c1fcfe, 0x471a4),
    RAC3VENDORLOCATION.PHOENIX_SKIN_24: RAC3SHIPVENDORSLOTDATA(0, 37000, 0x1f0000, 5, 0, 0x1d, 0x1c1fcd3, 0x331f29),
    RAC3VENDORLOCATION.PHOENIX_SKIN_25: RAC3SHIPVENDORSLOTDATA(0, 38000, 0x1f0000, 0xe, 0, 0x1e, 0x1c1fd39, 0x626262),
    RAC3VENDORLOCATION.PHOENIX_SKIN_26: RAC3SHIPVENDORSLOTDATA(0, 39000, 0x1f0000, 7, 0, 0x1f, 0x1c1fd55, 0x404649),
    RAC3VENDORLOCATION.PHOENIX_SKIN_27: RAC3SHIPVENDORSLOTDATA(0, 40000, 0x1f0000, 0xa, 0, 0x20, 0x1c1fd16, 0xa1544d),
    RAC3VENDORLOCATION.PHOENIX_SKIN_28: RAC3SHIPVENDORSLOTDATA(0, 41000, 0x1f0000, 4, 0, 0x21, 0x1c1fd21, 0x47312b),
    RAC3VENDORLOCATION.PHOENIX_SKIN_29: RAC3SHIPVENDORSLOTDATA(0, 42000, 0x1f0000, 0xf, 0, 0x22, 0x1c1fd46, 0x95bd),
    RAC3VENDORLOCATION.PHOENIX_SKIN_30: RAC3SHIPVENDORSLOTDATA(0, 43000, 0x1f0000, 0xb, 0, 0x23, 0x1c1fd75, 0xd1d71),
    RAC3VENDORLOCATION.PHOENIX_SKIN_31: RAC3SHIPVENDORSLOTDATA(0, 44000, 0x1f0000, 8, 0, 0x24, 0x1c1fd7d, 0x463686),
    RAC3VENDORLOCATION.PHOENIX_SKIN_32: RAC3SHIPVENDORSLOTDATA(0, 45000, 0x1f0000, 3, 0, 0x25, 0x1c1fd92, 0x897a46),
}
MEGACORP_WEAPONS: set[str] = {
    RAC3ITEM.LAVA_GUN,
    RAC3ITEM.MINI_TURRET,
    RAC3ITEM.BOUNCER,
    RAC3ITEM.PLASMA_COIL,
    RAC3ITEM.SHIELD_CHARGER,
}
