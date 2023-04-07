from ..assembler import ASM
from ..backgroundEditor import BackgroundEditor


def singleSaveSlot(rom):
    # Do not validate/erase slots 2 and 3 at rom start
    rom.patch(0x01, 0x06B3, ASM("call $4794"), "", fill_nop=True)
    rom.patch(0x01, 0x06B9, ASM("call $4794"), "", fill_nop=True)

    # Patch the code that checks if files have proper filenames to skip file 2/3
    rom.patch(0x01, 0x1DD9, ASM("ld b, $02"), ASM("ret"), fill_nop=True)

    # Remove the part that writes death counters for save2/3 on the file select screen
    rom.patch(0x01, 0x0821, 0x084B, "", fill_nop=True)
    # Remove the call that updates the hearts for save2
    rom.patch(0x01, 0x0800, ASM("call $4DBE"), "", fill_nop=True)
    # Remove the call that updates the hearts for save3
    rom.patch(0x01, 0x0806, ASM("call $4DD6"), "", fill_nop=True)

    # Remove the call that updates the names for save2 and save3
    rom.patch(0x01, 0x0D70, ASM("call $4D94\ncall $4D9D"), "", fill_nop=True)

    # Remove the 2/3 slots from the screen and remove the copy text
    be = BackgroundEditor(rom, 0x03)
    del be.tiles[0x9924]
    del be.tiles[0x9984]
    be.store(rom)
    be = BackgroundEditor(rom, 0x04)
    del be.tiles[0x9924]
    del be.tiles[0x9984]
    for n in range(0x99ED, 0x99F1):
        del be.tiles[n]
    be.store(rom)

    # Do not do left/right for erase/copy selection.
    rom.patch(0x01, 0x092B, ASM("jr z, $0B"), ASM("jr $0B"))
    # Only switch between players
    rom.patch(0x01, 0x08FA, 0x091D, ASM("""
        ld  a, [$DBA7]
        and a
        ld  a, [$DBA6]
        jr  z, skip
        xor $03
skip:
    """), fill_nop=True)

    # On the erase screen, only switch between save 1 and return
    rom.patch(0x01, 0x0E12, ASM("inc a\nand $03"), ASM("xor $03"), fill_nop=True)
    rom.patch(0x01, 0x0E21, ASM("dec a\ncp $ff\njr nz, $02\nld a,$03"), ASM("xor $03"), fill_nop=True)

    be = BackgroundEditor(rom, 0x06)
    del be.tiles[0x9924]
    del be.tiles[0x9984]
    be.store(rom)
