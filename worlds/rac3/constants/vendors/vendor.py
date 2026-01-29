from worlds.rac3.client.rac3_interface import Rac3Interface
from worlds.rac3.constants.vendors.mode import RAC3VENDORMODE
from worlds.rac3.constants.vendors.vendorslot import RAC3VENDORSLOT


class RAC3VENDOR:
    CURSOR_OFFSET: int = -0xC0
    SUBMENU_OFFSET: int = -0xBC
    MODEL_UPDATE_OFFSET: int = -0xB0
    SLOT_COUNT_OFFSET: int = 0x600
    VENDOR_TYPE_OFFSET: int = -0xF0
    VENDOR_WEAPON_TYPE_OFFSET: int = 0x604 # 0 = Normal, 1 = Slim Cognito
    SLOT_SIZE: int = 0x18

    def __init__(self, interface: "Rac3Interface"):
        self.mode: RAC3VENDORMODE = RAC3VENDORMODE.CLOSED
        self.interface: Rac3Interface = interface
        self.slots: list[RAC3VENDORSLOT] = []
        self.recently_bought_locations: list[int] = []