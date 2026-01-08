from ..memory.space import Bank, Reserve, Write
from ..instruction import asm as asm
from ..instruction import c2 as c2
from .. import args as args

class Multipliers():
    def __init__(self):
        if args.xp_mult != 1:
            self.set_xp_multiplier(args.xp_mult)

        if args.gp_mult != 1:
            self.set_gp_multiplier(args.gp_mult)

        if args.mp_mult != 1:
            self.set_mp_multiplier(args.mp_mult)

    def set_xp_multiplier(self, multiplier):
        src = [
            asm.A8(),
            asm.LDA(multiplier, asm.IMM8),
            asm.STA(0xe8, asm.DIR),                     # $e8 = given multiplier
            asm.A16(),
            asm.LDA(0x3d8c, asm.ABS_X),                 # a = enemy exp
            asm.JSR(c2.multiply_max_65535, asm.ABS),    # a = enemy exp * multiplier
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "exp multiply function")
        multiply_exp = space.start_address

        # multiply each enemies exp at end of battle by given multiplier (applied after enemy scaling)
        # NOTE: max exp each enemy can give is 65535 (2 bytes per enemy)
        #       but the overall battle total can be higher (3 bytes)
        #       so if two enemies max out their exp and third enemy gives 100 exp:
        #           total battle exp will be (65535 + 65535 + 100) / number of party members
        space = Reserve(0x25dc1, 0x25dc3, "call exp multiply function")
        space.write(
            asm.JSR(multiply_exp, asm.ABS),
        )

    def set_gp_multiplier(self, multiplier):
        src = [
            asm.A8(),
            asm.LDA(multiplier, asm.IMM8),
            asm.STA(0xe8, asm.DIR),                     # $e8 = given multiplier
            asm.A16(),
            asm.LDA(0x3da0, asm.ABS_X),                 # a = enemy gp
            asm.JSR(c2.multiply_max_65535, asm.ABS),    # a = enemy gp * multiplier
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "gp multiply function")
        multiply_gp = space.start_address

        # multiply each enemies gp at end of battle by given multiplier (applied after enemy scaling)
        # NOTE: max gp each enemy can give is 65535 (2 bytes per enemy)
        #       but the overall battle total can be higher (3 bytes)
        #       so if two enemies max out their gp and third enemy gives 100 gp:
        #           total battle gp will be (65535 + 65535 + 100)
        space = Reserve(0x25dd0, 0x25dd2, "call gp multiply function")
        space.write(
            asm.JSR(multiply_gp, asm.ABS),
        )

    def set_mp_multiplier(self, multiplier):
        src = [
            asm.LDA(0xdfb400, asm.LNG_X),               # a = formation magic points (instruction replaced)
            asm.XBA(),
            asm.LDA(multiplier, asm.IMM8),              # a = given multiplier
            asm.JSR(c2.multiply_max_255, asm.ABS),      # a = multiplier * magic points
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "magic points multiply function")
        multiply_mp = space.start_address

        # NOTE: max magic points battle can give is 255 (1 byte)
        space = Reserve(0x25d9c, 0x25d9f, "call magic points multiply function", asm.NOP())
        space.write(
            asm.JSR(multiply_mp, asm.ABS),
        )

        # protect against overflow, if multiplying magic points by learn rate > 100, cap it at 100
        space = Reserve(0x26050, 0x26052, "scaling multiply magic points by learn rate")
        space.write(
            asm.JSR(c2.multiply_max_100, asm.ABS),
        )

        src = [
            asm.LDX(multiplier, asm.IMM16),  # x = given multiplier
            asm.A16(),
            asm.AND(0x00ff, asm.IMM16),      # a = morph time
            asm.JSR(c2.divide, asm.ABS),     # a = morph time / multiplier
            asm.A8(),
            asm.CLC(),
            asm.ADC(0x1cf6, asm.ABS),        # add morph time to existing morph time
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "divide gained morph time by magic points multiplier")
        add_morph_time = space.start_address

        space = Reserve(0x25e3f, 0x25e41, "call add_morph_time", asm.NOP())
        space.write(
            asm.JSR(add_morph_time, asm.ABS),
        )
