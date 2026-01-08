from ..assembler import ASM
from ..utils import formatText


def updateTarin(rom):
    # Do not give the shield.
    rom.patch(0x05, 0x0CD0, ASM("""
        ld   d, $04
        call $5321
        ld   a, $01
        ld   [$DB44], a
    """), "", fill_nop=True)

    # Instead of showing the usual "your shield back" message, give the proper message and give the item.
    rom.patch(0x05, 0x0CDE, ASM("""
        ld   a, $91
        call $2385
    """), ASM("""
        ld   a, $0B ; GiveItemAndMessageForRoom
        rst  8
    """), fill_nop=True)

    rom.patch(0x05, 0x0CF0, ASM("""
        xor  a
        ldh  [$FFF1], a
        ld   de, $4CC6
        call $3C77
    """), ASM("""
        ld   a, $0C ; RenderItemForRoom
        rst  8
        xor  a
        ldh  [$FFF1], a
    """), fill_nop=True)

    # Set the room status to finished. (replaces a GBC check)
    rom.patch(0x05, 0x0CAB, 0x0CB0, ASM("""
        ld a, $20
        call $36C4
    """), fill_nop=True)

    # Instead of checking for the shield level to put you in the bed, check the room flag.
    rom.patch(0x05, 0x1202, ASM("ld a, [$DB44]\nand a"), ASM("ldh a, [$FFF8]\nand $20"))
    rom.patch(0x05, 0x0C6D, ASM("ld a, [$DB44]\nand a"), ASM("ldh a, [$FFF8]\nand $20"))

    # If the starting item is picked up, load the right palette when entering the room
    rom.patch(0x21, 0x0176, ASM("ld a, [$DB48]\ncp $01"), ASM("ld a, [$DAA3]\ncp $A1"), fill_nop=True)
    rom.patch(0x05, 0x0C94, "FF473152C5280000", "FD2ED911CE100000")
    rom.patch(0x05, 0x0CB0, ASM("ld hl, $DC88"), ASM("ld hl, $DC80"))

    # Patch the text that Tarin uses to give your shield back.
    rom.texts[0x54] = formatText("#####, it is dangerous to go alone!\nTake this!")
