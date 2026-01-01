from ..assembler import ASM
from ..utils import formatText
from ..locations.constants import CHEST_ITEMS


def fixChests(rom):
    # Patch the chest code, so it can give a lvl1 sword.
    # Normally, there is some code related to the owl event when getting the tail key,
    # as we patched out the owl. We use it to jump to our custom code in bank $3E to handle getting the item
    rom.patch(0x03, 0x109C, ASM("""
        cp $11 ; if not tail key, skip
        jr nz, end
        push af
        ld   a, [$C501]
        ld   e, a
        ld   hl, $C2F0
        add  hl, de
        ld   [hl], $38
        pop af
    end:
        ld   e, a
        cp   $21 ; if is message chest or higher number, next instruction is to skip giving things.
    """), ASM("""
        ld   a, $06 ; GiveItemMultiworld
        rst  8

        and  a   ; clear the carry flag to always skip giving stuff.
    """), fill_nop=True)

    # Instead of the normal logic to on which sprite data to show, we jump to our custom code in bank 3E.
    rom.patch(0x07, 0x3C36, None, ASM("""
        ld   a, $01
        rst  8
        jp $7C5E
    """), fill_nop=True)

    # Instead of the normal logic of showing the proper dialog, we jump to our custom code in bank 3E.
    rom.patch(0x07, 0x3C9C, None, ASM("""
        ld   a, $0A ; showItemMessageMultiworld
        rst  8
        jp $7CE9
    """))

    # Sound to play is normally loaded from a table, which is no longer big enough. So always use the same sound.
    rom.patch(0x07, 0x3C81, ASM("""
        add  hl, de
        ld   a, [hl]
    """), ASM("ld a, $01"), fill_nop=True)

    # Always spawn seashells even if you have the L2 sword
    rom.patch(0x14, 0x192F, ASM("ld a, $1C"), ASM("ld a, $20"))

    rom.texts[0x9A] = formatText("You found 10 {BOMB}!")


def setMultiChest(rom, option):
    room = 0x2F2
    addr = room + 0x560
    rom.banks[0x14][addr] = CHEST_ITEMS[option]
