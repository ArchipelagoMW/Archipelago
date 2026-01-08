from ..assembler import ASM


def onlyDropBombsWhenHaveBombs(rom):
    rom.patch(0x03, 0x1FC5, ASM("call $608C"), ASM("call $50B2"))
    # We use some of the unused chest code space here to remove the bomb if you do not have bombs in your inventory.
    rom.patch(0x03, 0x10B2, 0x112A, ASM("""
        ld   e, INV_SIZE
        ld   hl, $DB00
        ld   a, $02
loop:
        cp   [hl]
        jr   z, resume
        dec  e
        inc  hl
        jr   nz, loop
        jp   $3F8D ; unload entity
resume:
        jp   $608C
    """), fill_nop=True)