from ..roomEditor import RoomEditor, Object
from ..assembler import ASM


def fixAll(rom):
    # Prevent soft locking in the first mountain cave if we do not have a feather
    re = RoomEditor(rom, 0x2B7)
    re.removeObject(3, 3)
    re.store(rom)

    # Prevent getting stuck in the sidescroll room in the beginning of dungeon 5
    re = RoomEditor(rom, 0x1A9)
    re.objects[6].count = 7
    re.store(rom)

    # Cave that allows you to escape from D4 without flippers, make it no longer require a feather
    re = RoomEditor(rom, 0x1EA)
    re.objects[9].count = 8
    re.removeObject(5, 4)
    re.moveObject(4, 4, 7, 5)
    re.store(rom)

    # D3 west side room requires feather to get the key. But feather is not required to unlock the door, potentially softlocking you.
    re = RoomEditor(rom, 0x155)
    re.changeObject(4, 1, 0xcf)
    re.changeObject(4, 6, 0xd0)
    re.store(rom)

    # D3 boots room requires boots to escape
    re = RoomEditor(rom, 0x146)
    re.removeObject(5, 6)
    re.store(rom)

    allowRaftGameWithoutFlippers(rom)
    # We cannot access thes holes in logic:
    # removeBirdKeyHoleDrop(rom)
    fixDoghouse(rom)
    flameThrowerShieldRequirement(rom)
    fixLessThen3MaxHealth(rom)

def fixDoghouse(rom):
    # Fix entering the dog house from the back, and ending up out of bounds.
    re = RoomEditor(rom, 0x0A1)
    re.objects.append(Object(6, 2, 0x0E2))
    re.objects.append(re.objects[20])  # Move the flower patch after the warp entry definition so it overrules the tile
    re.objects.append(re.objects[3])

    re.objects.pop(22)
    re.objects.pop(21)
    re.objects.pop(20)  # Remove the flower patch at the normal entry index
    re.objects.pop(11)  # Duplicate object, we can just remove it, gives room for our custom entry door
    re.store(rom)

def allowRaftGameWithoutFlippers(rom):
    # Allow jumping down the waterfall in the raft game without the flippers.
    rom.patch(0x02, 0x2E8F, ASM("ld a, [$DB0C]"), ASM("ld a, $01"), fill_nop=True)
    # Change the room that goes back up to the raft game from the bottom, so we no longer need flippers
    re = RoomEditor(rom, 0x1F7)
    re.changeObject(3, 2, 0x1B)
    re.changeObject(2, 3, 0x1B)
    re.changeObject(3, 4, 0x1B)
    re.changeObject(4, 5, 0x1B)
    re.changeObject(6, 6, 0x1B)
    re.store(rom)

def removeBirdKeyHoleDrop(rom):
    # Prevent the cave with the bird key from dropping you in the water
    # (if you do not have flippers this would softlock you)
    rom.patch(0x02, 0x1176, ASM("""
        ldh a, [$FFF7]
        cp $0A
        jr nz, $30
    """), ASM("""
        nop
        nop
        nop
        nop
        jr $30
    """))
    # Remove the hole that drops you all the way from dungeon7 entrance to the water in the cave
    re = RoomEditor(rom, 0x01E)
    re.removeObject(5, 4)
    re.store(rom)

def flameThrowerShieldRequirement(rom):
    # if you somehow get a lvl3 shield or higher, it no longer works against the flamethrower, easy fix.
    rom.patch(0x03, 0x2EBA,
        ASM("ld a, [$DB44]\ncp $02\nret nz"),  # if not shield level 2
        ASM("ld a, [$DB44]\ncp $02\nret c"))  # if not shield level 2 or higher

def fixLessThen3MaxHealth(rom):
    # The table that starts your start HP when you die is not working for less then 3 HP, and locks the game.
    rom.patch(0x01, 0x1295, "18181818", "08081018")
