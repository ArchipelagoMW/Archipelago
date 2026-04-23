"""This module provides data structures for individual items occupying a vendor slot"""
from dataclasses import dataclass

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

    def __init__(self, values_list: list[int] | None = None):
        values = [0, 0, 0x0CDB, 0, 0, 0, 0] if values_list is None else values_list
        self.item_id = self.Property("ID", values[0], 2, RAC3WEAPONVENDOR.ITEM_ID_SIZE, RAC3WEAPONVENDOR.ITEM_ID_OFFSET)
        self.ammo_text = self.Property("Ammo text?", values[1], 1, RAC3WEAPONVENDOR.ITEM_AMMO_TEXT_SIZE,
                                       RAC3WEAPONVENDOR.ITEM_AMMO_TEXT_OFFSET)
        self.item_class = self.Property("Class", values[2], 2, RAC3WEAPONVENDOR.ITEM_CLASS_SIZE,
                                        RAC3WEAPONVENDOR.ITEM_CLASS_OFFSET)
        self.free = self.Property("Free?", values[3], 1, RAC3WEAPONVENDOR.ITEM_COST_SIZE,
                                  RAC3WEAPONVENDOR.ITEM_COST_OFFSET)
        self.mega = self.Property("Mega?", values[4], 1, RAC3WEAPONVENDOR.ITEM_MEGA_SIZE,
                                  RAC3WEAPONVENDOR.ITEM_MEGA_OFFSET)
        self.all_ammo = self.Property("All Ammo?", values[5], 1, RAC3WEAPONVENDOR.ITEM_ALL_AMMO_SIZE,
                                      RAC3WEAPONVENDOR.ITEM_ALL_AMMO_OFFSET)
        self.memcard = self.Property("Memory Card?", values[6], 1, RAC3WEAPONVENDOR.ITEM_MEMCARD_SIZE,
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

    def __init__(self, values_list: list[int] | None = None):
        values = [0, 0, 0] if values_list is None else values_list
        self.icon = self.Property("Icon", values[0], 2, RAC3ARMORVENDOR.ITEM_ICON_SIZE, RAC3ARMORVENDOR.ITEM_ICON_OFFSET)
        self.cost = self.Property("Cost", values[1], 0, RAC3ARMORVENDOR.ITEM_COST_SIZE, RAC3ARMORVENDOR.ITEM_COST_OFFSET)
        self.armor_level = self.Property("Armor Level", values[2], 0, RAC3ARMORVENDOR.ITEM_LEVEL_SIZE,
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

    def __init__(self, values_list: list[int] | None = None):
        values = [0, 0, 0, 0, 0, 0, 0, 0, 0] if values_list is None else values_list
        self.icon_id = self.Property("Icon ID", values[0], 2, RAC3SHIPVENDOR.ITEM_ICON_SIZE, RAC3SHIPVENDOR.ITEM_ICON_OFFSET)
        self.cost = self.Property("Cost", values[1], 0, RAC3SHIPVENDOR.ITEM_COST_SIZE, RAC3SHIPVENDOR.ITEM_COST_OFFSET)
        self.highlighted_part = self.Property("Highlighted Part", values[2], 2, RAC3SHIPVENDOR.ITEM_HIGHLIGHTED_PART_SIZE, RAC3SHIPVENDOR.ITEM_HIGHLIGHTED_PART_OFFSET)
        self.color_id = self.Property("Color ID", values[3], 2, RAC3SHIPVENDOR.ITEM_COLOR_ID_SIZE, RAC3SHIPVENDOR.ITEM_COLOR_ID_OFFSET)
        self.ship_config = self.Property("Ship Config", values[4], 2, RAC3SHIPVENDOR.ITEM_SHIP_CONFIG_SIZE, RAC3SHIPVENDOR.ITEM_SHIP_CONFIG_OFFSET)
        self.unlock_id = self.Property("Unlock ID", values[5], 2, RAC3SHIPVENDOR.ITEM_UNLOCK_ID_SIZE, RAC3SHIPVENDOR.ITEM_UNLOCK_ID_OFFSET)
        self.item_name_ptr = self.Property("Item Name Pointer", values[6], 2, RAC3SHIPVENDOR.ITEM_NAME_PTR_SIZE, RAC3SHIPVENDOR.ITEM_NAME_PTR_OFFSET)
        self.icon_color = self.Property("Icon Color", values[7], 2, RAC3SHIPVENDOR.ITEM_ICON_COLOR_SIZE, RAC3SHIPVENDOR.ITEM_ICON_COLOR_OFFSET)
        self.is_equipped = self.Property("Is Equipped?", values[8], 1, RAC3SHIPVENDOR.ITEM_IS_EQUIPPED_SIZE, RAC3SHIPVENDOR.ITEM_IS_EQUIPPED_OFFSET)

    def get_data(self) -> list[RAC3VENDORSLOTDATA.Property]:
        """return a list containing the data of each property this item has"""
        return [self.icon_id, self.cost, self.highlighted_part, self.color_id,
                self.ship_config, self.unlock_id, self.item_name_ptr, self.icon_color, self.is_equipped]

class RAC3SKINVENDORSLOTDATA(RAC3VENDORSLOTDATA):
    cost: RAC3VENDORSLOTDATA.Property
    skin_id: RAC3VENDORSLOTDATA.Property
    description_string_id: RAC3VENDORSLOTDATA.Property

    def __init__(self, values_list: list[int] | None = None):
        values = [0, 0, 0] if values_list is None else values_list
        self.cost = self.Property("Cost", values[0], 0, RAC3SKINVENDOR.ITEM_COST_SIZE, RAC3SKINVENDOR.ITEM_COST_OFFSET)
        self.skin_id = self.Property("Skin ID", values[1], 2, RAC3SKINVENDOR.ITEM_SKIN_ID_SIZE, RAC3SKINVENDOR.ITEM_SKIN_ID_OFFSET)
        self.description_string_id = self.Property("Description String ID", values[2], 2, RAC3SKINVENDOR.ITEM_DESCRIPTION_STRING_ID_SIZE, RAC3SKINVENDOR.ITEM_DESCRIPTION_STRING_ID_OFFSET)

    def get_data(self) -> list[RAC3VENDORSLOTDATA.Property]:
        """return a list containing the data of each property this item has"""
        return [self.cost, self.skin_id, self.description_string_id]

