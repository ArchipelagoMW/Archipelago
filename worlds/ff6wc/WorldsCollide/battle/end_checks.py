from ..memory.space import Bank, Reserve, Write
from ..instruction import asm as asm
from ..instruction import c2 as c2

from ..battle.check_dragon_boss import CheckDragonBoss
from ..battle.check_objectives import CheckObjectives

class _EndChecks:
    def __init__(self):
        src = [
            # replaced code
            asm.JSR(0x4936, asm.ABS),   # copy battle data to sram, update characters/enemies, ...

            asm.LDA(0x01, asm.IMM8),
            asm.BIT(0x3ebc, asm.ABS),   # was party annihilated?
            asm.BNE("AFTER_CHECKS"),    # if annihilated, skip checks

            CheckDragonBoss(),
            CheckObjectives(),

            "AFTER_CHECKS",
            asm.RTS(),
        ]
        space = Write(Bank.C2, src, "battle end checks")
        end_checks = space.start_address

        space = Reserve(0x2488f, 0x24891, "call battle end checks", asm.NOP())
        space.write(
            asm.JSR(end_checks, asm.ABS),
        )
end_checks = _EndChecks()
