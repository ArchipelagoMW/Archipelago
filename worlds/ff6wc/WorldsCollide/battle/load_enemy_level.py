from ..memory.space import Bank, START_ADDRESS_SNES, Reserve, Write, Read
from ..instruction import asm as asm

from ..battle.scaling import scaling
from ..battle.formation_flags import FormationFlag, formation_flags_address

from ..data import event_bit as event_bit
from .. import objectives as objectives
from .. import args as args

enemy_level_address = 0x3b18

class _LoadEnemyLevel:
    def __init__(self):
        add_enemy_levels = self._add_objective_levels_mod("Add Enemy Levels", FormationFlag.BOSS_DRAGON_FINAL, asm.BEQ)
        add_boss_levels = self._add_objective_levels_mod("Add Boss Levels", FormationFlag.BOSS, asm.BNE)
        add_dragon_levels = self._add_objective_levels_mod("Add Dragon Levels", FormationFlag.DRAGON, asm.BNE)
        add_final_levels = self._add_objective_levels_mod("Add Final Levels", FormationFlag.FINAL, asm.BNE)

        src = [
            Read(0x22d1e, 0x22d24), # unscaled enemy level
        ]
        if args.level_scaling:
            src += [
                asm.JSR(scaling.scale_and_distort_level, asm.ABS),
            ]

        src += [
            asm.JSL(START_ADDRESS_SNES + add_enemy_levels),
            asm.JSL(START_ADDRESS_SNES + add_boss_levels),
            asm.JSL(START_ADDRESS_SNES + add_dragon_levels),
            asm.JSL(START_ADDRESS_SNES + add_final_levels),

            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "load enemy level")
        load_enemy_level = space.start_address

        space = Reserve(0x22d1e, 0x22d24, "call load enemy level", asm.NOP())
        space.write(
            asm.JSR(load_enemy_level, asm.ABS),
        )

    def _add_objective_levels_mod(self, result_name, formation_flag, branch_instr):
        # Note: branch instruction is inverted to avoid trying to branch > 127 bytes.
        src = [
            asm.LDA(formation_flag, asm.IMM8),
            asm.BIT(formation_flags_address, asm.ABS),
            branch_instr(f"DO_{result_name}"),
            asm.RTL(),
            f"DO_{result_name}",
        ]
        if result_name in objectives.results:
            for objective in objectives.results[result_name]:
                objective_event_bit = event_bit.objective(objective.id)
                bit = event_bit.bit(objective_event_bit)
                address = event_bit.address(objective_event_bit)

                src += [
                    asm.LDA(address, asm.ABS),
                    asm.AND(2 ** bit, asm.IMM8),
                    asm.BEQ(f"SKIP_{objective.letter}"),

                    asm.LDA(objective.result.levels, asm.IMM8),
                    asm.CLC(),
                    asm.ADC(enemy_level_address, asm.ABS_Y),
                    asm.STA(enemy_level_address, asm.ABS_Y),

                    f"SKIP_{objective.letter}",
                ]
        src += [
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, f"{result_name} objectives")
        return space.start_address

load_enemy_level = _LoadEnemyLevel()
