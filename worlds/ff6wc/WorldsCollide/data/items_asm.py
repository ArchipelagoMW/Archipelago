from ..memory.space import Bank, Reserve, Write, Read
from ..instruction import asm as asm

from ..data.item_names import name_id
import random

def stronger_atma_weapon():
    space = Reserve(0x20e59, 0x20e59, "atma weapon divisor exponent")
    space.write(4) # change modifier from 2^(5+1) to 2^(4+1)

def cursed_shield_mod(battles):
    src = [
        asm.LDA(battles, asm.IMM8),                 # a = battles required
        asm.INC(0x3ec0, asm.ABS),                   # increment cursed shield battle count
        asm.CMP(0x3ec0, asm.ABS),                   # compare battle count with battles required
        asm.BNE("NOT_UNCURSED"),                    # branch if count != required

        asm.STZ(0x3ec0, asm.ABS),                   # reset count back to zero
        Read(0x26003, 0x2600b),                     # set uncursed flag and change item to paladin shield
        asm.RTS(),

        "NOT_UNCURSED",
        asm.LDA(name_id["Cursed Shld"], asm.IMM8),  # a = cursed shield id
        asm.RTS(),
    ]
    space = Write(Bank.C2, src, "cursed shield uncursed check")
    uncurse_shield_check = space.start_address

    space = Reserve(0x25ffe, 0x2600b, "cursed shield battles increment", asm.NOP())
    space.write(
        asm.JSR(uncurse_shield_check, asm.ABS),
    )
