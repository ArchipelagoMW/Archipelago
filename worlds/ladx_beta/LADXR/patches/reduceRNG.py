from ..assembler import ASM


def slowdownThreeOfAKind(rom):
    rom.patch(0x06, 0x096B, ASM("ldh a, [$FFE7]\nand $0F"), ASM("ldh a, [$FFE7]\nand $3F"))


def fixHorseHeads(rom):
    rom.patch(0x07, 0x3653, "00010400", "00010000")
