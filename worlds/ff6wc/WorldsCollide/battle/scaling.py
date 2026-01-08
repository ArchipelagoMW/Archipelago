from ..memory.space import Bank, Reserve, Write, Read
from ..battle.scaling_functions import ScalingFunctions
from ..battle.formation_flags import FormationFlag, formation_flags_address

from ..instruction import asm as asm
from ..instruction import c2 as c2
from .. import args as args

class _Scaling():
    def __init__(self):
        self.scaling_functions = ScalingFunctions()

        self.enemy_level = 0x3b18
        self.level_scale = 0x3ecc
        self.hp_mp_scale = 0x3ecd
        self.xp_gp_scale = 0x3ece

        self.load_scale_levels_mod()
        self.scale_value_mod()

        self.scale_hp_mp_mod()
        self.scale_xp_gp_mod()
        self.scale_distort_level_mod()

    def load_scale_levels_mod(self):
        # at beginning of battle before loading hp/mp/xp/gp (only once, not per enemy)
        # scale enemy level based on given scaling function/factor args

        def scale_level(self, scaling_function, factor, result_address):
            src = [
                asm.A16(),
                asm.JSR(scaling_function, asm.ABS),
            ]
            if scaling_function == self.scaling_functions.time:
                # divide by factor
                src += [
                    asm.ASL(),
                    asm.LDX(int(factor * 2), asm.IMM8),
                    asm.JSR(c2.divide, asm.ABS),
                ]
            else:
                # multiply by factor
                src += [
                    asm.LDX(int(factor * 2), asm.IMM8),
                    asm.STX(0xe8, asm.DIR),
                    asm.JSR(c2.multiply_max_65535, asm.ABS),
                    asm.LSR(),
                ]
            src += [
                asm.JSR(self.scaling_functions.min_max_bound, asm.ABS),
                asm.A8(),
                asm.STA(result_address, asm.ABS),
            ]
            return src

        src = [
            Read(0x2249e, 0x224a0),

            asm.LDA(FormationFlag.SKIP_SCALING, asm.IMM8),
            asm.BIT(formation_flags_address, asm.ABS),
            asm.BNE("RETURN"),
        ]

        if self.scaling_functions.level is not None:
            src += scale_level(self, self.scaling_functions.level, args.level_scaling_factor, self.level_scale),
        if self.scaling_functions.hp_mp is not None:
            src += scale_level(self, self.scaling_functions.hp_mp, args.hp_mp_scaling_factor, self.hp_mp_scale),
        if self.scaling_functions.xp_gp is not None:
            src += scale_level(self, self.scaling_functions.xp_gp, args.xp_gp_scaling_factor, self.xp_gp_scale),

        src += [
            "RETURN",
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "c2 load scale levels")
        load_scale_levels = space.start_address

        if args.level_scaling or args.hp_mp_scaling or args.xp_gp_scaling:
            space = Reserve(0x2249e, 0x224a0, "call scaling functions", asm.NOP())
            space.write(
                asm.JSR(load_scale_levels, asm.ABS),
            )

    def scale_value_mod(self):
        # input: 0xe8 = 24 bit value address, x = 16 bit enemy id * 32, y = 16 bit enemy index
        # output: 16 bit a = (value / original level) * enemy level
        value_ptr_addr = 0xe8

        src = [
            asm.TXA(),                                  # a = enemy id * 32
            asm.CLC(),
            asm.ADC(value_ptr_addr, asm.DIR),           # a = value address + enemy id * 32
            asm.STA(value_ptr_addr, asm.DIR),           # 0xea = address of value for given enemy id

            asm.LDA(FormationFlag.SKIP_SCALING, asm.IMM16),
            asm.BIT(formation_flags_address, asm.ABS),
            asm.BNE("SKIP_SCALE"),

            asm.LDA(0xcf0010, asm.LNG_X),               # a = original enemy level
            asm.AND(0x00ff, asm.IMM16),                 # extract 8 bit level
            asm.CMP(value_ptr_addr, asm.DIR_24),        # compare level to stat value
            asm.BGE("SKIP_SCALE"),                      # branch if level > stat to prevent stat going to zero

            asm.PHX(),
            asm.PHY(),
            asm.TAY(),                                  # y = enemy level
            asm.LDA(value_ptr_addr, asm.DIR_24),        # a = enemy stat value
            asm.TYX(),                                  # x = enemy level
            asm.JSR(c2.divide, asm.ABS),                # a = enemy stat / enemy level
            asm.TAX(),                                  # x = stat / level
            asm.PLY(),
            asm.LDA(self.enemy_level, asm.ABS_Y),       # a = scaled level
            asm.AND(0x00ff, asm.IMM16),                 # extract 8 bit scaled level
            asm.STA(0xe8, asm.DIR),                     # (overwriting value address for multiplication)
            asm.TXA(),                                  # a = stat / level
            asm.JSR(c2.multiply_max_65535, asm.ABS),    # a = (stat / original level) * scaled level
            asm.PLX(),
            asm.RTS(),

            "SKIP_SCALE",
            asm.LDA(value_ptr_addr, asm.DIR_24),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "c2 scale value")
        self.scale_value = space.start_address

    def scale_hp_mp_mod(self):
        # set enemy level to scaled level (based on hp/mp scaling argument calculated in load_scale_levels)
        # call scale value for hp/mp

        hp_address = 0xcf0008
        mp_address = 0xcf000a
        src = [
            asm.A8(),
            asm.LDA(self.hp_mp_scale, asm.ABS),
            asm.STA(self.enemy_level, asm.ABS_Y),
            asm.A16(),

            asm.LDA(mp_address & 0xffff, asm.IMM16),
            asm.STA(0xe8, asm.DIR),
            asm.LDA((mp_address >> 16) & 0xffff, asm.IMM16),
            asm.STA(0xea, asm.DIR),
            asm.JSR(self.scale_value, asm.ABS),

            Read(0x22cc1, 0x22cc6), # store as current and max mp

            asm.LDA(hp_address & 0xffff, asm.IMM16),
            asm.STA(0xe8, asm.DIR),
            asm.LDA((hp_address >> 16) & 0xffff, asm.IMM16),
            asm.STA(0xea, asm.DIR),
            asm.JMP(self.scale_value, asm.ABS),
        ]
        space = Write(Bank.C2, src, "scale hp/mp")
        self.scale_hp_mp = space.start_address

        if args.hp_mp_scaling:
            space = Reserve(0x22cbd, 0x22cca, "load scaled hp/mp", asm.NOP())
            space.write(
                        asm.JSR(self.scale_hp_mp, asm.ABS),
                       )

    def scale_xp_gp_mod(self):
        # set enemy level to scaled level (based on xp/gp scaling argument calculated in load_scale_levels)
        # call scale value for xp/gp

        xp_address = 0xcf000c
        gp_address = 0xcf000e
        src = [
            asm.A8(),
            asm.LDA(self.xp_gp_scale, asm.ABS),
            asm.STA(self.enemy_level, asm.ABS_Y),
            asm.A16(),

            asm.LDA(xp_address & 0xffff, asm.IMM16),
            asm.STA(0xe8, asm.DIR),
            asm.LDA((xp_address >> 16) & 0xffff, asm.IMM16),
            asm.STA(0xea, asm.DIR),
            asm.JSR(self.scale_value, asm.ABS),

            Read(0x22cae, 0x22cb0), # store experience

            asm.LDA(gp_address & 0xffff, asm.IMM16),
            asm.STA(0xe8, asm.DIR),
            asm.LDA((gp_address >> 16) & 0xffff, asm.IMM16),
            asm.STA(0xea, asm.DIR),
            asm.JMP(self.scale_value, asm.ABS),
        ]
        space = Write(Bank.C2, src, "scale hp/mp")
        self.scale_xp_gp = space.start_address

        if args.xp_gp_scaling:
            space = Reserve(0x22caa, 0x22cb4, "load scaled xp/gp", asm.NOP())
            space.write(
                        asm.JSR(self.scale_xp_gp, asm.ABS),
                       )

    def scale_distort_level_mod(self):
        # set enemy level to scaled level (based on level scaling argument calculated in load_scale_levels)
        # apply small distortion to prevent overpowered level-based abilities
        src = [
            asm.LDA(FormationFlag.SKIP_SCALING, asm.IMM8),
            asm.BIT(formation_flags_address, asm.ABS),
            asm.BNE("RETURN"),

            "SCALE_AND_DISTORT",
            asm.LDA(0x04, asm.IMM8),
            asm.JSR(c2.rng_a, asm.ABS),                 # a = random number [0 to 3]
            asm.DEC(),                                  # a in range [-1, to 2]
            asm.CLC(),
            asm.ADC(self.level_scale, asm.ABS),         # a = scaled level + random distortion
            asm.CMP(0x03, asm.IMM8),
            asm.BGE("SAVE_AND_RETURN"),                 # branch if result >= 3
            asm.LDA(0x03, asm.IMM8),                    # else a = 3

            "SAVE_AND_RETURN",
            asm.STA(self.enemy_level, asm.ABS_Y),       # self.enemy_level = scaled level + random distortion

           "RETURN",
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "scale and distort level")
        self.scale_and_distort_level = space.start_address
scaling = _Scaling()
