from ..memory.space import Reserve
from ..instruction import asm as asm
from .. import args as args

class Evade:
    def __init__(self):
        if args.fix_evade:
            self.mod()

    def mod(self):
        evade = 0x3b54  # 255 - (evade * 2) + 1
        mblock = 0x3b55 # 255 - (mblock * 2) + 1

        space = Reserve(0x2232d, 0x2232d, "evade bug branch if not image status")
        space.add_label("LOAD_EVADE", 0x22345)
        space.write(
            space.branch_distance("LOAD_EVADE"),    # branch if target does not have image status
        )

        space = Reserve(0x2233f, 0x22349, "evade bug fix")
        space.add_label("APPLY_HIT_RATE", 0x22388)
        space.write(
            asm.LDA(mblock, asm.ABS_Y),
            asm.PHA(),
            asm.BRA("APPLY_HIT_RATE"),

            asm.LDA(evade, asm.ABS_Y),
            asm.PHA(),
            asm.NOP(),
        )
