from ..data import event_bit as event_bit
from ..instruction import asm as asm

def ram_event_byte(event):
    return 0x1e80 + event_bit.byte(event)

def ram_event_bit(event):
    return 1 << event_bit.bit(event)

def char_recruited_event_byte(char):
    return ram_event_byte(event_bit.character_recruited(char))

def char_recruited_event_bit(char):
    return ram_event_bit(event_bit.character_recruited(char))

def char_available_event_byte(char):
    return ram_event_byte(event_bit.character_available(char))

def char_available_event_bit(char):
    return ram_event_bit(event_bit.character_available(char))

def esper_available_byte(esper):
    return 0x1a69 + esper // 8

def esper_available_bit(esper):
    return 1 << (esper % 8)

def branch_if_char_recruited(char, dest):
    return [
        asm.LDA(char_recruited_event_byte(char), asm.ABS),
        asm.BIT(char_recruited_event_bit(char), asm.IMM8),
        asm.BNE(dest),
    ]

def branch_if_char_not_recruited(char, dest):
    return [
        asm.LDA(char_recruited_event_byte(char), asm.ABS),
        asm.BIT(char_recruited_event_bit(char), asm.IMM8),
        asm.BEQ(dest),
    ]

def branch_if_char_available(char, dest):
    return [
        asm.LDA(char_available_event_byte(char), asm.ABS),
        asm.BIT(char_available_event_bit(char), asm.IMM8),
        asm.BNE(dest),
    ]

def branch_if_char_not_available(char, dest):
    return [
        asm.LDA(char_available_event_byte(char), asm.ABS),
        asm.BIT(char_available_event_bit(char), asm.IMM8),
        asm.BEQ(dest),
    ]

def branch_if_event_bit_set(event, dest):
    return [
        asm.LDA(ram_event_byte(event), asm.ABS),
        asm.BIT(ram_event_bit(event), asm.IMM8),
        asm.BNE(dest),
    ]

def branch_if_event_bit_clear(event, dest):
    return [
        asm.LDA(ram_event_byte(event), asm.ABS),
        asm.BIT(ram_event_bit(event), asm.IMM8),
        asm.BEQ(dest),
    ]
