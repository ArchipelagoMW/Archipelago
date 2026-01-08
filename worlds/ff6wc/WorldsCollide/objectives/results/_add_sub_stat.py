from ...memory.space import Bank, Write
from ...instruction import asm as asm
from ...instruction import field as field

from ...objectives.results._apply_characters_party import ApplyToCharacter, ApplyToCharacters

def AddStat(stat_address):
    MAX_STAT = 0x80
    return [
        asm.LDA(stat_address, asm.ABS_Y),
        asm.CLC(),
        asm.ADC(field.LongCall.ARG_ADDRESS, asm.DIR),
        asm.CMP(MAX_STAT, asm.IMM8),
        asm.BLT("STORE"),             # If < 128, skip to STORE
        asm.LDA(MAX_STAT, asm.IMM8),  # Else, cap at 128
        "STORE",
        asm.STA(stat_address, asm.ABS_Y),
    ]

def SubStat(stat_address):
    return [
        asm.LDA(stat_address, asm.ABS_Y),
        asm.SEC(),
        asm.SBC(field.LongCall.ARG_ADDRESS, asm.DIR),
        asm.BCC("MINIMUM"),
        asm.BRA("STORE"),

        "MINIMUM",
        asm.LDA(0, asm.IMM8),

        "STORE",
        asm.STA(stat_address, asm.ABS_Y),
    ]

def add_stat_all(stat_address, stat_string):
    src = ApplyToCharacters(AddStat(stat_address))
    src += [
        asm.RTL(),
    ]

    space = Write(Bank.F0, src, f"add {stat_string} all")
    return space.start_address

def sub_stat_all(stat_address, stat_string):
    src = ApplyToCharacters(SubStat(stat_address))
    src += [
        asm.RTL(),
    ]

    space = Write(Bank.F0, src, f"sub {stat_string} all")
    return space.start_address

def add_stat_character(character, stat_address, stat_string):
    src = ApplyToCharacter(character, AddStat(stat_address))
    src += [
        asm.RTL(),
    ]

    space = Write(Bank.F0, src, f"add {stat_string} {character}")
    return space.start_address

def sub_stat_character(character, stat_address, stat_string):
    src = ApplyToCharacter(character, SubStat(stat_address))
    src += [
        asm.RTL(),
    ]

    space = Write(Bank.F0, src, f"sub {stat_string} {character}")
    return space.start_address
