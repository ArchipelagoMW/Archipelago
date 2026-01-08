from ..roomEditor import RoomEditor


def desertAccess(rom):
    re = RoomEditor(rom, 0x0FD)
    re.entities = [(6, 2, 0xC4)]
    re.store(rom)
