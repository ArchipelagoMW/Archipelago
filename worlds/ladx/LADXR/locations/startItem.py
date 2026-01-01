from .itemInfo import ItemInfo
from .constants import *
from .droppedKey import DroppedKey
from ..assembler import ASM
from ..utils import formatText
from ..roomEditor import RoomEditor


class StartItem(DroppedKey):
    MULTIWORLD = False

    def __init__(self):
        super().__init__(0x2A3)
        self.give_bowwow = False

    def patch(self, rom, option, *, multiworld=None):
        assert multiworld is None

        if self.give_bowwow:
            option = BOWWOW
            rom.texts[0xC8] = formatText("Got BowWow!")

        if option != SHIELD:
            rom.patch(5, 0x0CDA, ASM("ld a, $22"), ASM("ld a, $00"))  # do not change links sprite into the one with a shield

        super().patch(rom, option)
