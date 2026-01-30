"""This module provides data structures for individual items occupying a vendor slot"""
from dataclasses import dataclass

from worlds.rac3.constants.vendors.vendor import RAC3ARMORVENDOR, RAC3WEAPONVENDOR


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

        def read(self):
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

    def __init__(self, values_list: list[int] = None):
        values = [0, 0, 0x0CDB, 0, 0, 0, 0] if values_list is None else values_list
        self.item_id = self.Property('ID', values[0], RAC3WEAPONVENDOR.ITEM_ID_SIZE, RAC3WEAPONVENDOR.ITEM_ID_OFFSET)
        self.ammo_text = self.Property('Ammo text?', values[1], RAC3WEAPONVENDOR.ITEM_AMMO_TEXT_SIZE,
                                       RAC3WEAPONVENDOR.ITEM_AMMO_TEXT_OFFSET)
        self.item_class = self.Property('Class', values[2], RAC3WEAPONVENDOR.ITEM_CLASS_SIZE,
                                        RAC3WEAPONVENDOR.ITEM_CLASS_OFFSET)
        self.free = self.Property('Free?', values[3], RAC3WEAPONVENDOR.ITEM_COST_SIZE,
                                  RAC3WEAPONVENDOR.ITEM_COST_OFFSET)
        self.mega = self.Property('Mega?', values[4], RAC3WEAPONVENDOR.ITEM_MEGA_SIZE,
                                  RAC3WEAPONVENDOR.ITEM_MEGA_OFFSET)
        self.all_ammo = self.Property('All Ammo?', values[5], RAC3WEAPONVENDOR.ITEM_ALL_AMMO_SIZE,
                                      RAC3WEAPONVENDOR.ITEM_ALL_AMMO_OFFSET)
        self.memcard = self.Property('Memory Card?', values[6], RAC3WEAPONVENDOR.ITEM_MEMCARD_SIZE,
                                     RAC3WEAPONVENDOR.ITEM_MEMCARD_OFFSET)

    def get_data(self) -> list[RAC3VENDORSLOTDATA.Property]:
        """return a list containing the data of each property this item has"""
        return [self.item_id, self.ammo_text, self.item_class,
                self.free, self.mega, self.all_ammo, self.memcard]


@dataclass
class RAC3ARMORVENDORSLOTDATA(RAC3VENDORSLOTDATA):
    icon: RAC3VENDORSLOTDATA.Property
    cost: RAC3VENDORSLOTDATA.Property
    level: RAC3VENDORSLOTDATA.Property

    def __init__(self, values_list: list[int] = None):
        values = [0, 0, 0] if values_list is None else values_list
        self.icon = self.Property('Icon', values[0], RAC3ARMORVENDOR.ITEM_ICON_SIZE, RAC3ARMORVENDOR.ITEM_ICON_OFFSET)
        self.cost = self.Property('Cost', values[1], RAC3ARMORVENDOR.ITEM_COST_SIZE, RAC3ARMORVENDOR.ITEM_COST_OFFSET)
        self.level = self.Property('Level', values[2], RAC3ARMORVENDOR.ITEM_LEVEL_SIZE,
                                   RAC3ARMORVENDOR.ITEM_LEVEL_OFFSET)

    def get_data(self) -> list[RAC3VENDORSLOTDATA.Property]:
        """return a list containing the data of each property this item has"""
        return [self.icon, self.cost, self.level]
