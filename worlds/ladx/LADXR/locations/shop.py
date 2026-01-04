from .itemInfo import ItemInfo
from .constants import *
from ..utils import formatText
from ..assembler import ASM


class ShopItem(ItemInfo):
    def __init__(self, index):
        self.__index = index
        # pass in the alternate index for shop 2
        # The "real" room is at 0x2A1, but we store the second item data as if link were in 0x2A7
        room = 0x2A1
        if index == 1:
            room = 0x2A7
        super().__init__(room)

    def patch(self, rom, option, *, multiworld=None):
        mw_text = ""
        if multiworld:
            mw_text = f" for player {rom.player_names[multiworld - 1].encode('ascii', 'replace').decode()}"
            # filter out { and } since they cause issues with string.format later on
            mw_text = mw_text.replace("{", "").replace("}", "")
        
        if self.custom_item_name:
            name = self.custom_item_name
        else:
            name = "{"+option+"}"

        if self.__index == 0:
            # Old index, maybe not needed any more
            rom.patch(0x04, 0x37C5, "08", "%02X" % (CHEST_ITEMS[option]))
            rom.texts[0x030] = formatText(f"Deluxe {name} 200 {{RUPEES}}{mw_text}!", ask="Buy  No Way")
            rom.banks[0x3E][0x3800 + 0x2A1] = CHEST_ITEMS[option]
            if multiworld:
                rom.banks[0x3E][0x3300 + 0x2A1] = multiworld
        elif self.__index == 1:
            rom.patch(0x04, 0x37C6, "02", "%02X" % (CHEST_ITEMS[option]))
            rom.texts[0x02C] = formatText(f"{name} only 980 {{RUPEES}}{mw_text}!", ask="Buy  No Way")
            
            rom.banks[0x3E][0x3800 + 0x2A7] = CHEST_ITEMS[option]
            if multiworld:
                rom.banks[0x3E][0x3300 + 0x2A7] = multiworld

    def read(self, rom):
        value = rom.banks[0x04][0x37C5 + self.__index]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find shop item contents in ROM (0x%02x)" % (value))