from ..memory.space import Reserve
from ..instruction import asm as asm
from .. import args as args

class SellMenu:
    def __init__(self):
        self.mod()

    def sell_zero(self):
        space = Reserve(0x3bb75, 0x3bb7b, "shop menu cut price in half", asm.NOP())
        space.write(
            asm.STZ(0xf1, asm.DIR),     # sell items for zero
        )

    def sell_fraction(self):
        # there is an unnecessary jmp/lda here we can replace to not use any extra space
        space = Reserve(0x3bb7a, 0x3bb82, "shop menu calculate and store sell value", asm.NOP())

        # a register = item price
        if args.shop_sell_fraction4 or args.shop_sell_fraction8:
            space.write(
                asm.LSR(),              # cut price in half (1/4)
            )
        if args.shop_sell_fraction8:
            space.write(
                asm.LSR(),              # cut price in half (1/8)
            )
        space.write(
            asm.STA(0xf1, asm.DIR),     # save sell price
            asm.A8(),
        )

    def mod(self):
        if args.shop_sell_fraction0:
            self.sell_zero()
        elif args.shop_sell_fraction4 or args.shop_sell_fraction8:
            self.sell_fraction()
