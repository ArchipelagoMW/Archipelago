from ..roomEditor import RoomEditor, ObjectWarp, ObjectVertical


def tweakMap(rom):
    # 5 holes at the castle, reduces to 3
    re = RoomEditor(rom, 0x078)
    re.objects[-1].count = 3
    re.overlay[7 + 6 * 10] = re.overlay[9 + 6 * 10]
    re.overlay[8 + 6 * 10] = re.overlay[9 + 6 * 10]
    re.store(rom)


def addBetaRoom(rom):
    re = RoomEditor(rom, 0x1FC)
    re.objects[-1].target_y -= 0x10
    re.store(rom)
    re = RoomEditor(rom, 0x038)
    re.changeObject(5, 1, 0xE1)
    re.removeObject(0, 0)
    re.removeObject(0, 1)
    re.removeObject(0, 2)
    re.removeObject(6, 1)
    re.objects.append(ObjectVertical(0, 0, 0x38, 3))
    re.objects.append(ObjectWarp(1, 0x1F, 0x1FC, 0x50, 0x7C))
    re.store(rom)

    rom.room_sprite_data_indoor[0x0FC] = rom.room_sprite_data_indoor[0x1A1]


def tweakBirdKeyRoom(rom):
    # Make the bird key accessible without the rooster
    re = RoomEditor(rom, 0x27A)
    re.removeObject(1, 6)
    re.removeObject(2, 6)
    re.removeObject(3, 5)
    re.removeObject(3, 6)
    re.moveObject(1, 5, 2, 6)
    re.moveObject(2, 5, 3, 6)
    re.addEntity(3, 5, 0x9D)
    re.store(rom)


def openMabe(rom):
    # replaces rocks on east side of Mabe Village with bushes
    re = RoomEditor(rom, 0x094)
    re.changeObject(5, 1, 0x5C)
    re.overlay[5 + 1 * 10] = 0x5C
    re.overlay[5 + 2 * 10] = 0x5C
    re.store(rom)
