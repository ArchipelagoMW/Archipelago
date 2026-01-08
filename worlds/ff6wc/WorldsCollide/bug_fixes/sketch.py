from ..memory.space import Reserve
from ..instruction import asm as asm
from .. import args as args

class Sketch:
    def __init__(self):
        if args.fix_sketch:
            self.mod()

    def mod(self):
        # assassin, main page: http://assassin17.brinkster.net/
        # masterzed, http://masterzed.cavesofnarshe.com/hostedpatches/sketchfix.zip
        space = Reserve(0x2f5c6, 0x2f5ce, "sketch bug fix reuse code at c2f592", asm.NOP())
        space.add_label("SAME_CODE", 0x2f592)
        space.write(
            asm.BRA("SAME_CODE"),       # branch to same code in another location to free space
        )
        # 7 free bytes

        # this jmp does not fit at c2f5f6 so put it here and branch to it
        space = Reserve(0x2f5cf, 0x2f5d1, "sketch bug fix c2f809 jmp")
        space.write(
            asm.JMP(0xf809, asm.ABS),
        )

        space = Reserve(0x2f5d9, 0x2f5f7, "sketch bug fix monster sprite data lookup")
        space.add_label("JMP", 0x2f5cf),
        space.write(
            asm.LDA(0x01, asm.IMM8),
            asm.TRB(0x898d, asm.ABS),
            asm.LDY(0x0003, asm.IMM16),
            asm.LDA(0x76, asm.DIR_16_Y),# if sketch misses, can load 0xff into a
            asm.ASL(),                  # if a was 0xff, then a = 0xfe and carry bit set
            asm.TAX(),
            asm.A16(),
            asm.LDA(0x2001, asm.ABS_X), # if a = 0xfe, then incorrectly loads from 7e20ff (magic list/aiming)
            asm.BCC("ORIGINAL_SKETCH"), # branch if carry clear, otherwise fix invalid value
            asm.TDC(),                  # a = 0x0000, clear the invalid value loaded
            asm.DEC(),                  # a = 0xffff, transfer 0xffff to x instead

            "ORIGINAL_SKETCH",
            asm.TAX(),                  # transfer a to x to be stored at $10 and used later at c124f7
            asm.TDC(),
            asm.A8(),
            asm.JSL(0xc124d1),
            asm.BRA("JMP"),             # branch to jmp because jmp does not fit here
        )
