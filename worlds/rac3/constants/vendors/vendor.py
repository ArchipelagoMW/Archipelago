"""This module provides constant address offsets, for use when reading data regarding Vendor contents"""

from worlds.rac3.constants.region import PLANET_VENDOR_OFFSET
from worlds.rac3.constants.status import RAC3STATUS


class RAC3VENDOR:
    """Struct for the Vendor data, containing address offsets for where data can be read"""
    CURSOR_OFFSET: int = -0xC0
    SUBMENU_OFFSET: int = -0xBC
    MODEL_UPDATE_OFFSET: int = -0xB0
    SLOT_COUNT_OFFSET: int = 0x600
    VENDOR_TYPE_OFFSET: int = -0xF0
    VENDOR_WEAPON_TYPE_OFFSET: int = 0x604  # 0 = Normal, 1 = Slim Cognito

    SLOT_SIZE: int = 0x14

    ITEM_ID_OFFSET: int = 0x00  # 4 Bytes
    ITEM_AMMO_TEXT_OFFSET: int = 0x04
    # 1 Byte, 0 = No Text + Not Shifted, 1 = Ammo Text + Shifted Up, 2 = No Text + Shifted Up
    ITEM_CLASS_OFFSET: int = 0x0C  # 2 Byte, Items = 0x0CDB
    ITEM_COST_OFFSET: int = 0x10  # 1 Byte, 0 = Normal price, 1 = Free
    ITEM_MEGA_OFFSET: int = 0x11  # 1 Byte, 0 = Normal, 1 = Mega
    ITEM_ALL_AMMO_OFFSET: int = 0x12  # 1 Byte, 0 = Normal, 1 = All Ammo
    ITEM_MEMCARD_OFFSET: int = 0x13  # 1 Byte, 0 = Normal, 1 = Memory Card Check

    @staticmethod
    def get_vendor_item_property_address(planet: str, slot: int, item_prop_offset: int):
        """Provides the item property address for reading data"""
        return RAC3VENDOR.get_vendor_property_address(planet, 0) + (slot * RAC3VENDOR.SLOT_SIZE) + item_prop_offset

    @staticmethod
    def get_vendor_property_address(planet, vendor_prop):
        """Provides the vendor property address for reading data"""
        return RAC3STATUS.VENDOR_BASE + PLANET_VENDOR_OFFSET[planet] + vendor_prop
