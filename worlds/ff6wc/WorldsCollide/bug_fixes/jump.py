from ..memory.space import Bank, Reserve, Allocate
from ..instruction import asm as asm
from .. import args as args

class Jump:
    def __init__(self):
        if args.fix_jump:
            self.mod()

    def mod(self):
        # http://assassin17.brinkster.net/patches.htm#anchor5
        # this does not apply the space optimization or shifting in assassin's patch (spend 8 bytes instead)

        space = Allocate(Bank.C2, 8, "jump super ball launcher bug fix", asm.NOP())
        space.write(
            # $3405 = number of hits and is decremented for each target chosen
            # if no valid targets, 3405 needs to be reset to 0xff so normal combat routine is not skipped
            asm.INY(),                  # y = 0xff
            asm.STY(0x3405, asm.ABS),   # counter = 0xff (null, no targets found)

            asm.LDA(0x0010, asm.IMM16), # original code replaced with calling this function
            asm.RTS(),
        )
        reset_counter = space.start_address

        space = Reserve(0x23515, 0x23517, "call jump super ball launcher bug fix")#, asm.NOP())
        space.write(
            asm.JSR(reset_counter, asm.ABS),
        )

