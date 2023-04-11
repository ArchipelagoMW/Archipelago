from ..assembler import ASM
from ..utils import formatText


def patchRooster(rom):
    # Do not give the rooster
    rom.patch(0x19, 0x0E9D, ASM("ld [$DB7B], a"), "", fill_nop=True)

    # Do not load the rooster sprites
    rom.patch(0x00, 0x2EC7, ASM("jr nz, $08"), "", fill_nop=True)

    # Draw the found item
    rom.patch(0x19, 0x0E4A, ASM("ld hl, $4E37\nld c, $03\ncall $3CE6"), ASM("ld a, $0C\nrst $08"), fill_nop=True)
    rom.patch(0x19, 0x0E7B, ASM("ld hl, $4E37\nld c, $03\ncall $3CE6"), ASM("ld a, $0C\nrst $08"), fill_nop=True)
    # Give the item and message
    rom.patch(0x19, 0x0E69, ASM("ld a, $6D\ncall $2373"), ASM("ld a, $0E\nrst $08"), fill_nop=True)

    # Reuse unused evil eagle text slot for rooster message
    rom.texts[0x0B8] = formatText("Got the {ROOSTER}!")

    # Allow rooster pickup with special rooster item
    rom.patch(0x19, 0x1ABC, ASM("cp $03"), ASM("cp $0F"))
    rom.patch(0x19, 0x1AAE, ASM("cp $03"), ASM("cp $0F"))

    # Ignore the has-rooster flag in the rooster entity (do not despawn)
    rom.patch(0x19, 0x19E0, ASM("jp z, $7E61"), "", fill_nop=True)

    # If we are spawning the rooster, and the rooster is already existing, do not do anything, instead of despawning the rooster.
    rom.patch(0x01, 0x1FEF, ASM("ld [hl], d"), ASM("ret"))
    # Allow rooster to unload when changing rooms
    rom.patch(0x19, 0x19E9, ASM("ld [hl], a"), "", fill_nop=True)

    # Do not take away the rooster after D7
    rom.patch(0x03, 0x1E25, ASM("ld [$DB7B], a"), "", fill_nop=True)

    # Patch the color dungeon entrance not to check for rooster
    rom.patch(0x02, 0x3409, ASM("ld hl, $DB7B\nor [hl]"), "", fill_nop=True)

    # Spawn marin at taltal even with rooster
    rom.patch(0x18, 0x1EE3, ASM("jp nz, $7F08"), "", fill_nop=True)
