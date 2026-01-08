from .constants import *
from .itemInfo import ItemInfo


class Witch(ItemInfo):
    def __init__(self):
        super().__init__(0x2A2)

    def configure(self, options):
        if not options.witch:
            self.OPTIONS = [MAGIC_POWDER]

    def patch(self, rom, option, *, multiworld=None):
        if multiworld or option != MAGIC_POWDER:
            
            rom.banks[0x3E][self.room + 0x3800] = CHEST_ITEMS[option]
            if multiworld is not None:
                rom.banks[0x3E][0x3300 + self.room] = multiworld
            else:
                rom.banks[0x3E][0x3300 + self.room] = 0
            
            #rom.patch(0x05, 0x08D5, "09", "%02x" % (CHEST_ITEMS[option]))

    def read(self, rom):
        if rom.banks[0x05][0x08EF] != 0x00:
            return MAGIC_POWDER
        value = rom.banks[0x05][0x08D5]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find witch contents in ROM (0x%02x)" % (value))
