from ..memory.space import Bank, Reserve, Write, Read

from ..instruction import asm as asm
from ..instruction import f0 as f0
from .. import args as args

from enum import IntFlag

formation_address = 0x3ed4
formation_flags_address = 0x3ecb

class FormationFlag(IntFlag):
    BOSS                = 1 << 0
    DRAGON              = 1 << 1
    FINAL               = 1 << 2
    SKIP_SCALING        = 1 << 3

    BOSS_DRAGON_FINAL   = BOSS | DRAGON | FINAL

class _FormationFlags:
    def __init__(self):
        src = [
            Read(0x22447, 0x22449),

            asm.PHP(),
            asm.AXY8(),

            asm.STZ(formation_flags_address, asm.ABS),  # clear formation flags

            asm.A16(),
            asm.LDA(formation_address, asm.ABS),

            self._check_type(FormationFlag.BOSS, f0.boss_formations, f0.boss_formations_size),
            self._check_type(FormationFlag.DRAGON, f0.dragon_formations, f0.dragon_formations_size),
            self._check_type(FormationFlag.FINAL, f0.final_battle_formations, f0.final_battle_formations_size),

            asm.A8(),
            "TYPE_CHECKED",
            self._check_skip_scaling(),

            "RETURN",
            asm.PLP(),
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "initialize formation flags")
        initialize_formation_flags = space.start_address

        space = Reserve(0x22447, 0x22449, "load formation data", asm.NOP())
        space.write(
            asm.JSR(initialize_formation_flags, asm.ABS),
        )

    def _check_type(self, flag, formations_table, formations_table_size):
        return [
            asm.LDX(0, asm.IMM8),
            f"LOOP_START_{flag.name}",
            asm.CMP(formations_table, asm.LNG_X),       # is this formation in the given table?
            asm.BNE(f"CONTINUE_{flag.name}"),           # branch if not

            asm.A8(),
            asm.LDA(flag, asm.IMM8),
            asm.TSB(formation_flags_address, asm.ABS),  # set flag bit
            asm.BRA("TYPE_CHECKED"),

            f"CONTINUE_{flag.name}",
            asm.INX(),                                  # next formation
            asm.INX(),
            asm.CPX(formations_table_size, asm.IMM8),   # checked all formations in table?
            asm.BLT(f"LOOP_START_{flag.name}"),         # branch if not
        ]

    def _check_skip_scaling(self):
        src = []
        if not args.scale_eight_dragons:
            src += [
                asm.LDA(FormationFlag.DRAGON, asm.IMM8),
                asm.BIT(formation_flags_address, asm.ABS),
                asm.BNE("SET_SKIP_SCALING"),
            ]
        if not args.scale_final_battles:
            src += [
                asm.LDA(FormationFlag.FINAL, asm.IMM8),
                asm.BIT(formation_flags_address, asm.ABS),
                asm.BNE("SET_SKIP_SCALING"),
            ]
        src += [
            asm.BRA("RETURN"),

            "SET_SKIP_SCALING",
            asm.LDA(FormationFlag.SKIP_SCALING, asm.IMM8),
            asm.TSB(formation_flags_address, asm.ABS),
        ]
        return src

formation_flags = _FormationFlags()
