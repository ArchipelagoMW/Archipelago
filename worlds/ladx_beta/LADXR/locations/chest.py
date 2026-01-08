from .itemInfo import ItemInfo
from .constants import *
from ..assembler import ASM


class Chest(ItemInfo):
    def __init__(self, room):
        super().__init__(room)
        self.addr = room + 0x560

    def patch(self, rom, option, *, multiworld=None):
        rom.banks[0x14][self.addr] = CHEST_ITEMS[option]

        if self.room == 0x1B6:
            # Patch the code that gives the nightmare key when you throw the pot at the chest in dungeon 6
            # As this is hardcoded for a specific chest type
            rom.patch(3, 0x145D, ASM("ld a, $19"), ASM("ld a, $%02x" % (CHEST_ITEMS[option])))
        if multiworld is not None:
            rom.banks[0x3E][0x3300 + self.room] = multiworld

    def read(self, rom):
        value = rom.banks[0x14][self.addr]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find chest contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        return "%s:%03x" % (self.__class__.__name__, self.room)


class DungeonChest(Chest):
    def patch(self, rom, option, *, multiworld=None):
        if (option.startswith(MAP) and option != MAP) \
                or (option.startswith(COMPASS)  and option != COMPASS) \
                or (option.startswith(STONE_BEAK) and option != STONE_BEAK) \
                    or (option.startswith(NIGHTMARE_KEY) and option != NIGHTMARE_KEY) \
                    or (option.startswith(KEY) and option != KEY):
            if self._location.dungeon == int(option[-1]) and multiworld is None:
                option = option[:-1]
        super().patch(rom, option, multiworld=multiworld)

    def read(self, rom):
        result = super().read(rom)
        if result in [MAP, COMPASS, STONE_BEAK, NIGHTMARE_KEY, KEY]:
            return "%s%d" % (result, self._location.dungeon)
        return result

    def __repr__(self):
        return "%s:%03x:%d" % (self.__class__.__name__, self.room, self._location.dungeon)
