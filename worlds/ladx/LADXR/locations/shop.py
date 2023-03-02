from .itemInfo import ItemInfo
from .constants import *
from ..utils import formatText
from ..assembler import ASM


class ShopItem(ItemInfo):
    def __init__(self, index):
        self.__index = index
        # TODO: pass in the alternate index for shop 2
        super().__init__(0x2A1)

    def patch(self, rom, option, *, multiworld=None):
        mw_text = ""
        if multiworld:
            mw_text = f" for player {rom.player_names[multiworld - 1]}"

        if self.__index == 0:
            # Old index, maybe not needed any more
            rom.patch(0x04, 0x37C5, "08", "%02X" % (CHEST_ITEMS[option]))
            rom.texts[0x030] = formatText(f"Deluxe {{%s}} 200 {{RUPEES}}{mw_text}!" % (option), ask="Buy  No Way")
            rom.banks[0x3E][0x3800 + 0x2A1] = CHEST_ITEMS[option]
            if multiworld:
                rom.banks[0x3E][0x3300 + 0x2A1] = multiworld
        elif self.__index == 1:
            rom.patch(0x04, 0x37C6, "02", "%02X" % (CHEST_ITEMS[option]))
            rom.texts[0x02C] = formatText(f"{{%s}} Only 980 {{RUPEES}}{mw_text}!" % (option), ask="Buy  No Way")
            
            rom.banks[0x3E][0x3800 + 0x2A7] = CHEST_ITEMS[option]
            if multiworld:
                rom.banks[0x3E][0x3300 + 0x2A7] = multiworld

    def read(self, rom):
        value = rom.banks[0x04][0x37C5 + self.__index]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find shop item contents in ROM (0x%02x)" % (value))

    @property
    def nameId(self):
        return "0x%03X-%s" % (self.room, self.__index)

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.__index)
