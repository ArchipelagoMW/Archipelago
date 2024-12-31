from ..assembler import ASM


def fixGoldenLeaf(rom):
    # Patch the golden leaf code so it jumps to the dropped key handling in bank 3E
    rom.patch(3, 0x2007, ASM("""
        ld   de, $5FFB
        call $3C77 ; RenderActiveEntitySprite
    """), ASM("""
        ld   a, $04
        rst  8
    """), fill_nop=True)
    rom.patch(3, 0x2018, None, ASM("""
        ld   a, $06 ; giveItemMultiworld
        rst  8
        jp   $602F
    """))
    rom.patch(3, 0x2037, None, ASM("""
        ld   a, $0a ; showMessageMultiworld
        rst  8
        jp   $604B
    """))

    # Patch all over the place to move the golden leafs to a different memory location.
    # We use $DB6D (dungeon 9 status), but we could also use $DB7A (which is only used by the ghost)
    rom.patch(0x00, 0x2D17, ASM("ld a, [$DB15]"), ASM("ld a, $06"), fill_nop=True)  # Always load the slime tiles
    rom.patch(0x02, 0x3005, ASM("cp $06"), ASM("cp $01"), fill_nop=True)  # Instead of checking for 6 leaves a the keyhole, just check for the key
    rom.patch(0x20, 0x1AD1, ASM("ld a, [$DB15]"), ASM("ld a, [wGoldenLeaves]"))  # For the status screen, load the number of leafs from the proper memory
    rom.patch(0x03, 0x0980, ASM("ld a, [$DB15]"), ASM("ld a, [wGoldenLeaves]"))  # If leaves >= 6 move richard
    rom.patch(0x06, 0x0059, ASM("ld a, [$DB15]"), ASM("ld a, [wGoldenLeaves]"))  # If leaves >= 6 move richard
    rom.patch(0x06, 0x007D, ASM("ld a, [$DB15]"), ASM("ld a, [wGoldenLeaves]"))  # Richard message if no leaves
    rom.patch(0x06, 0x00B6, ASM("ld a, $FF"), ASM("ld a, $06"))
    rom.patch(0x06, 0x00B8, ASM("ld [$DB15], a"), ASM("ld [wGoldenLeaves], a"))  # Stores 6 in the leaf counter if we opened the path (instead of FF, so that nothing breaks if we get more for some reason)
    # 6:40EE uses leaves == 6 to check if we have collected the key, but only to change the message.
    # rom.patch(0x06, 0x2AEF, ASM("ld a, [$DB15]"), ASM("ld a, [wGoldenLeaves]"))  # Telephone message handler
