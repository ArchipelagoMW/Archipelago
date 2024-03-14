from ..assembler import ASM


def fixInstruments(rom):
    rom.patch(0x03, 0x1EA9, 0x1EAE, "", fill_nop=True)
    rom.patch(0x03, 0x1EB9, 0x1EC8, ASM("""
        ; Render sprite
        ld   a, $05
        rst  8
    """), fill_nop=True)

    # Patch the message and instrument giving code
    rom.patch(0x03, 0x1EE3, 0x1EF6, ASM("""
        ; Handle item effect
        ld   a, $06 ; giveItemMultiworld
        rst  8
        
        ;Show message
        ld   a, $0A ; showMessageMultiworld
        rst  8
    """), fill_nop=True)

    # Color cycle palette 7 instead of 1
    rom.patch(0x36, 0x30F0, ASM("ld de, $DC5C"), ASM("ld de, $DC84"))
