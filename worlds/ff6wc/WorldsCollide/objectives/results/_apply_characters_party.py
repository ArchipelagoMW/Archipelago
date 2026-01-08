from ...instruction import asm as asm
character_data_size = 37

def ApplyToCharacters(instructions):
    from ...constants.entities import CHARACTER_COUNT

    return [
        asm.PHP(),
        asm.XY16(),

        asm.LDX(0x0000, asm.IMM16),                 # x = character index
        asm.LDY(0x0000, asm.IMM16),                 # y = character data offset

        "CHARACTER_LOOP_START",

        instructions,

        asm.A16(),
        asm.TYA(),                                  # a = character data offset
        asm.CLC(),
        asm.ADC(character_data_size, asm.IMM16),    # next character's data block
        asm.TAY(),                                  # y = next character's data offset
        asm.A8(),

        asm.INX(),                                  # next character's party bits
        asm.CPX(CHARACTER_COUNT, asm.IMM16),        # all character's checked?
        asm.BLT("CHARACTER_LOOP_START"),            # branch if not

        asm.PLP(),
    ]

def ApplyToCharacter(character, instructions):
    return [
        asm.PHP(),
        asm.XY16(),

        asm.LDY(character * character_data_size, asm.IMM16),    # y = character data offset
        instructions,

        asm.PLP(),
    ]

def ApplyToParty(instructions):
    character_party_start = 0x1850
    current_party = 0x1a6d

    return ApplyToCharacters([
        asm.LDA(character_party_start, asm.ABS_X),  # a = character party (and visible/enabled/...)
        asm.AND(current_party, asm.ABS),            # is character in current party?
        asm.BEQ("NEXT_CHARACTER"),                  # branch if not

        instructions,

        "NEXT_CHARACTER",
    ])
