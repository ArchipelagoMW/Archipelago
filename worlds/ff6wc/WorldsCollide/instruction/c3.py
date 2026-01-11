from ..memory.space import Bank, START_ADDRESS_SNES, Space, Reserve, Allocate, Free, Write
from ..instruction import asm as asm

# Allow Eggers jumps into C3 -- that is, enable calls to JSR routines from other banks
# Ref: https://www.ff6hacking.com/forums/thread-2301.html
def _eggers_jump_return_mod():
    src = [
        asm.RTS(),
        asm.RTL()
    ]
    space =  Write(Bank.C3, src, "C3 eggers jump return")
    return space.start_address
eggers_jump_return = _eggers_jump_return_mod()

# Eggers jump src to jump to the specified C3 subroutine and successfully return to another bank
def eggers_jump(c3addr):
    src = [
        asm.PHK(),
        asm.PER(0x0009),
        asm.PEA(eggers_jump_return),
        asm.PEA(c3addr-1), # return after execution
        asm.JMP(eggers_jump_return + START_ADDRESS_SNES, asm.LNG),
    ]
    return src