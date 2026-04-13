"""This module provides constant address offsets, for use when reading data regarding Vendor contents"""

from worlds.rac3.constants.region import PLANET_VENDOR_OFFSET
from worlds.rac3.constants.status import RAC3STATUS
from worlds.rac3.constants.vendors.type import RAC3VENDORTYPE


class RAC3VENDOR:
    """Base struct for Vendor data, containing common address offsets"""
    CURSOR_OFFSET: int = -0xC0
    SUBMENU_OFFSET: int = -0xBC
    MODEL_UPDATE_OFFSET: int = -0xB0
    SLOT_COUNT_OFFSET: int = 0x600
    NEW_ARMOR_OFFSET: int = 0x628
    VENDOR_TYPE_OFFSET: int = -0xF0
    IS_PDA_OFFSET: int = -0xE4
    SLOT_SIZE: int = 0
    NO_ITEMS_AVAILABLE_LOC_KEY: str = "NO_VENDOR_ITEMS"
    NO_ITEMS_AVAILABLE_MSG: str = "No items available. 1 infobot = 3 items in stock!"

    @staticmethod
    def get_vendor_property_address(planet: str, vendor_prop: int) -> int:
        """Provides the vendor property address for reading data"""
        return RAC3STATUS.VENDOR_BASE + PLANET_VENDOR_OFFSET[planet] + vendor_prop

    @staticmethod
    def get_vendor_item_property_address(planet: str, slot: int, item_prop_offset: int, slot_size: int) -> int:
        """
        Provides the item property address for reading vendor item data,
        using the correct slot size for the vendor type.
        """
        return RAC3VENDOR.get_vendor_property_address(planet, 0) + (slot * slot_size) + item_prop_offset


class RAC3WEAPONVENDOR(RAC3VENDOR):
    """Struct for Weapon Vendor data, with weapon-specific slot size and offsets"""
    VENDOR_WEAPON_TYPE_OFFSET: int = 0x604  # 0 = Normal, 1 = Slim Cognito
    SLOT_SIZE: int = 0x14

    ITEM_ID_OFFSET: int = 0x00
    ITEM_ID_SIZE: int = 4  # Bytes
    ITEM_AMMO_TEXT_OFFSET: int = 0x04  # 0 = No Text + Not Shifted, 1 = Ammo Text + Shifted Up, 2 = No Text + Shifted Up
    ITEM_AMMO_TEXT_SIZE: int = 1
    ITEM_CLASS_OFFSET: int = 0x0C  # Items = 0x0CDB
    ITEM_CLASS_SIZE: int = 2
    ITEM_COST_OFFSET: int = 0x10  # 0 = Normal price, 1 = Free
    ITEM_COST_SIZE: int = 1
    ITEM_MEGA_OFFSET: int = 0x11  # 0 = Normal, 1 = Mega
    ITEM_MEGA_SIZE: int = 1
    ITEM_ALL_AMMO_OFFSET: int = 0x12  # 0 = Normal, 1 = All Ammo
    ITEM_ALL_AMMO_SIZE: int = 1
    ITEM_MEMCARD_OFFSET: int = 0x13  # 0 = Normal, 1 = Memory Card Check
    ITEM_MEMCARD_SIZE: int = 1


class RAC3ARMORVENDOR(RAC3VENDOR):
    """Struct for Armor Vendor data, with armor-specific slot size and offsets"""
    SLOT_SIZE: int = 0x10

    ITEM_ICON_OFFSET: int = 0x00
    ITEM_ICON_SIZE: int = 2
    ITEM_COST_OFFSET: int = 0x04
    ITEM_COST_SIZE: int = 4
    ITEM_LEVEL_OFFSET: int = 0x08
    ITEM_LEVEL_SIZE: int = 1

class RAC3SHIPVENDOR(RAC3VENDOR):
    """Struct for Ship Vendor data, with ship-specific slot size and offsets"""
    SLOT_SIZE: int = 0x24

    ITEM_ICON_OFFSET: int = 0x00
    ITEM_ICON_SIZE: int = 4
    ITEM_COST_OFFSET: int = 0x04
    ITEM_COST_SIZE: int = 4
    ITEM_HIGHLIGHTED_PART_OFFSET: int = 0x08
    ITEM_HIGHLIGHTED_PART_SIZE: int = 4
    ITEM_SHIP_CONFIG_OFFSET: int = 0x0C
    ITEM_SHIP_CONFIG_SIZE: int = 2
    ITEM_COLOR_ID_OFFSET: int = 0x0E
    ITEM_COLOR_ID_SIZE: int = 2
    ITEM_UNLOCK_ID_OFFSET: int = 0x10
    ITEM_UNLOCK_ID_SIZE: int = 4
    ITEM_NAME_PTR_OFFSET: int = 0x14
    ITEM_NAME_PTR_SIZE: int = 4
    ITEM_ICON_COLOR_OFFSET: int = 0x1C
    ITEM_ICON_COLOR_SIZE: int = 4
    ITEM_IS_EQUIPPED_OFFSET: int = 0x20 
    ITEM_IS_EQUIPPED_SIZE: int = 1

class RAC3SKINVENDOR(RAC3VENDOR):
    """Struct for Skin Vendor data, with skin-specific slot size and offsets"""
    SLOT_SIZE: int = 0xF

    ITEM_COST_OFFSET: int = 0x04
    ITEM_COST_SIZE: int = 4
    ITEM_SKIN_ID_OFFSET: int = 0x08
    ITEM_SKIN_ID_SIZE: int = 4
    ITEM_DESCRIPTION_STRING_ID_OFFSET: int = 0x0C
    ITEM_DESCRIPTION_STRING_ID_SIZE: int = 4

VENDORTYPE_TO_SLOT_SIZE: dict[int, int] = {
    RAC3VENDORTYPE.WEAPON: 0x14,
    RAC3VENDORTYPE.ARMOR: 0x10,
    RAC3VENDORTYPE.SHIP: 0x24,
    RAC3VENDORTYPE.SKIN: 0x0F,
}
