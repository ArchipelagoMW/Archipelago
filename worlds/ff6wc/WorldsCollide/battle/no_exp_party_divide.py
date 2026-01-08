from ..memory.space import Reserve
from ..instruction import asm as asm
from .. import args as args

class _NoExpPartyDivide:
    def __init__(self):
        space = Reserve(0x25de2, 0x25e02, "divide experience by number of surviving party members")
        if args.no_exp_party_divide:
            space.add_label("END", space.end_address + 1)
            space.write(
                # load top 2 bytes of exp (to OR with bottom 2 bytes and check for zero later
                asm.LDA(0x2f36, asm.ABS),
                asm.BRA("END"),
            )
no_exp_party_divide = _NoExpPartyDivide()
