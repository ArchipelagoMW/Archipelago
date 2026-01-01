from .itemInfo import ItemInfo
from .constants import *


class MadBatter(ItemInfo):
    def configure(self, options):
        return

    def patch(self, rom, option, *, multiworld=None):
        rom.banks[0x18][0x0F90 + (self.room & 0x0F)] = CHEST_ITEMS[option]
        if multiworld is not None:
            rom.banks[0x3E][0x3300 + self.room] = multiworld

    def read(self, rom):
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x18][0x0F90 + (self.room & 0x0F)]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find mad batter contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        return "%s:%03x" % (self.__class__.__name__, self.room)
