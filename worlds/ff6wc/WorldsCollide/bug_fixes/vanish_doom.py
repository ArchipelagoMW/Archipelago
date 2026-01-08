from ..memory.space import Reserve
from ..instruction import asm as asm
from .. import args as args

class VanishDoom:
    def __init__(self):
        if args.fix_vanish_doom:
            self.mod()

    def mod(self):
        # copy original code down and overwrite previous instant death protection check
        space = Reserve(0x22223, 0x22258, "vanish/doom bug fix normal checks")
        space.copy_from(0x22215, 0x2224a)

        # add original instant death protection to the beginning of where original code used to be
        space = Reserve(0x22215, 0x22222, "vanish/doom bug fix death check")
        space.add_label("MISS", 0x22291),
        space.write(
            asm.LDA(0x11a2, asm.ABS),
            asm.BIT(0x02, asm.IMM8),    # instant death spell bit?
            asm.BEQ("CONTINUE"),        # if not, skip checking instant death protection
            asm.LDA(0x3aa1, asm.ABS_Y),
            asm.BIT(0x04, asm.IMM8),    # protection from instant death bit?
            asm.BNE("MISS"),            # if so, miss
            "CONTINUE",
        )
