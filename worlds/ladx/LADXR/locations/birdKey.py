from .droppedKey import DroppedKey
from ..roomEditor import RoomEditor
from ..assembler import ASM


class BirdKey(DroppedKey):
    def __init__(self):
        super().__init__(0x27A)

    def patch(self, rom, option, *, multiworld=None):
        super().patch(rom, option, multiworld=multiworld)

        re = RoomEditor(rom, self.room)

        # Make the bird key accessible without the rooster
        re.removeObject(1, 6)
        re.removeObject(2, 6)
        re.removeObject(3, 5)
        re.removeObject(3, 6)
        re.moveObject(1, 5, 2, 6)
        re.moveObject(2, 5, 3, 6)
        re.addEntity(3, 5, 0x9D)
        re.store(rom)
