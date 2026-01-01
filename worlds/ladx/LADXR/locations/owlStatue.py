from .itemInfo import ItemInfo
from .constants import *


class OwlStatue(ItemInfo):
    def configure(self, options):
        if options.owlstatues == "both":
            return
        if options.owlstatues == "dungeon" and self.room >= 0x100:
            return
        if options.owlstatues == "overworld" and self.room < 0x100:
            return
        raise RuntimeError("Tried to configure an owlstatue that was not enabled")
        self.OPTIONS = [RUPEES_20]

    def patch(self, rom, option, *, multiworld=None):
        if option.startswith(MAP) or option.startswith(COMPASS) or option.startswith(STONE_BEAK) or option.startswith(NIGHTMARE_KEY) or option.startswith(KEY):
            if self._location.dungeon == int(option[-1]) and multiworld is not None:
                option = option[:-1]
        rom.banks[0x3E][self.room + 0x3B16] = CHEST_ITEMS[option]

    def read(self, rom):
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x3E][self.room + 0x3B16]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                if k in [MAP, COMPASS, STONE_BEAK, NIGHTMARE_KEY, KEY]:
                    assert self._location.dungeon is not None, "Dungeon item outside of dungeon? %r" % (self)
                    return "%s%d" % (k, self._location.dungeon)
                return k
        raise ValueError("Could not find owl statue contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        if self._location and self._location.dungeon:
            return "%s:%03x:%d" % (self.__class__.__name__, self.room, self._location.dungeon)
        else:
            return "%s:%03x" % (self.__class__.__name__, self.room)
    
    @property
    def nameId(self):
        return "0x%03X-Owl" % self.room
