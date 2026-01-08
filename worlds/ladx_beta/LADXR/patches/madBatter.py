from ..assembler import ASM
from ..utils import formatText


def upgradeMadBatter(rom):
    # Normally the madbatter won't do anything if you have full capacity. Remove that check.
    rom.patch(0x18, 0x0F05, 0x0F1D, "", fill_nop=True)
    # Remove the code that finds which upgrade to apply,
    rom.patch(0x18, 0x0F9E, 0x0FC4, "", fill_nop=True)
    rom.patch(0x18, 0x0FD2, 0x0FD8, "", fill_nop=True)

    # Finally, at the last step, give the item and the item message.
    rom.patch(0x18, 0x1016, 0x101B, "", fill_nop=True)
    rom.patch(0x18, 0x101E, 0x1051, ASM("""
        ; Mad batter rooms are E0,E1 and E2, load the item type from a table in the rom
        ; which only has 3 entries, and store it where bank 3E wants it.
        ldh a, [$FFF6] ; current room
        and $0F
        ld  d, $00
        ld  e, a
        ld  hl, $4F90
        add hl, de
        ld  a, [hl]
        ldh [$FFF1], a
    
        ; Give item
        ld  a, $06 ; giveItemMultiworld
        rst 8
        ; Message
        ld  a, $0A ; showMessageMultiworld
        rst 8
        ; Force the dialog at the bottom
        ld  a, [$C19F]
        or  $80
        ld  [$C19F], a
    """), fill_nop=True)
    # Setup the default items
    rom.patch(0x18, 0x0F90, "406060", "848586")

    rom.texts[0xE2] = formatText("You can now carry more Magic Powder!")
    rom.texts[0xE3] = formatText("You can now carry more Bombs!")
    rom.texts[0xE4] = formatText("You can now carry more Arrows!")
