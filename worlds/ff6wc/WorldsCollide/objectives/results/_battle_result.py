from ...memory.space import Bank, START_ADDRESS_SNES, Write
from ...instruction import asm as asm
from ...objectives._cached_function import _CachedFunction

class Result(_CachedFunction, asm.JSR):
    def __init__(self, *args, **kwargs):
        _CachedFunction.__init__(self, *args, **kwargs)
        asm.JSR.__init__(self, self.address(*args, **kwargs), asm.ABS)

    def write(self, *args, **kwargs):
        src = [
            self.src(*args, **kwargs),
            asm.RTS(),
        ]
        return Write(Bank.F0, src, f"battle result {type(self).__name__} {self.arg_string}")

def SetBit(address, bit):
    bitmask = 2 ** (bit % 8)
    return [
        asm.LDA(bitmask, asm.IMM8),
        asm.TSB(address, asm.ABS),
    ]

def AddItem(item_id):
    from ...instruction.c0 import add_item
    return [
        asm.PHP(),
        asm.A8(),
        asm.XY16(),

        asm.LDA(item_id, asm.IMM8),
        asm.JSL(START_ADDRESS_SNES + add_item),

        asm.PLP(),
    ]
