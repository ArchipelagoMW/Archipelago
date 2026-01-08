from ..utils import formatText
from ..assembler import ASM


def upgradeTunicFairy(rom):
    rom.texts[0x268] = formatText("Welcome, #####. I admire you for coming this far.")
    rom.texts[0x0CC] = formatText("Got the {RED_TUNIC}! You can change Tunics at the phone booths.")
    rom.texts[0x0CD] = formatText("Got the {BLUE_TUNIC}! You can change Tunics at the phone booths.")

    rom.patch(0x36, 0x111C, 0x1133, ASM("""
        call $3B12
        ld  a, [$DDE1]
        and $10
        jr  z, giveItems
        ld   [hl], $09
        ret

giveItems:
        ld  a, [$DDE1]
        or  $10
        ld  [$DDE1], a
    """), fill_nop=True)
    rom.patch(0x36, 0x1139, 0x1144, ASM("""
        ld  a, $04
        ldh [$FFF6], a
        ld  a, $0E
        rst 8
    """), fill_nop=True)

    rom.patch(0x36, 0x1162, 0x1192, ASM("""
        ld  a, $01
        ldh [$FFF6], a
        ld  a, $0E
        rst 8
    """), fill_nop=True)

    rom.patch(0x36, 0x119D, 0x11A2, "", fill_nop=True)
    rom.patch(0x36, 0x11B5, 0x11BE, ASM("""
        ; Skip to the end ignoring all the tunic giving animation.
        call $3B12
        ld   [hl], $09
    """), fill_nop=True)

    rom.banks[0x36][0x11BF] = 0x87
    rom.banks[0x36][0x11C0] = 0x88
