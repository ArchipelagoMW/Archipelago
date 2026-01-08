from ..memory.space import START_ADDRESS_SNES, Bank, Reserve, Write, Read
from ..instruction import asm as asm
from .. import args as args

class InitialSpells:
    def __init__(self):
        from ..data.spell_names import name_id

        self.initial_spells = []
        if args.scan_all:
            self.initial_spells.append(name_id["Scan"])

        if args.warp_all:
            self.initial_spells.append(name_id["Warp"])

        if len(self.initial_spells) > 0:
            self.teach_spells()

    def teach_spells(self):
        from ..data.spells import Spells
        from ..data.characters import Characters

        learned_spells_start = 0x1a6e
        learner_count = Characters.CHARACTER_COUNT - 2 # no gogo/umaro
        last_offset = Spells.SPELL_COUNT * learner_count

        src = [
            Read(0x0bdcc, 0x0bdd6),                 # initialize spells to 0% learned

            asm.PHY(),
            asm.LDX(0x00, asm.DIR), # x = 0x0000

            "CHARACTER_LOOP_START",
        ]
        for spell_id in self.initial_spells:
            src += [
                # Put spell offset from learned_spells_start in Y (X [character offset] + spell_id)
                asm.A16(),
                asm.TXA(),
                asm.CLC(),
                asm.ADC(spell_id, asm.IMM16),
                asm.TAY(),
                asm.A8(),
                # Write 0xff to the learned_spells_start + Y to initialize it as learned
                asm.LDA(0xff, asm.IMM8),                   # a = 0xff (spell learned value)
                asm.STA(learned_spells_start, asm.ABS_Y),  # set spell learned for current character
            ]
        src += [
            asm.A16(),
            asm.TXA(),                              # a = spell address offset for current character
            asm.CLC(),
            asm.ADC(Spells.SPELL_COUNT, asm.IMM16), # go to next character
            asm.TAX(),                              # x = spell address offset for next character
            asm.A8(),
            asm.CPX(last_offset, asm.IMM16),        # all characters done?
            asm.BLT("CHARACTER_LOOP_START"),        # branch if not

            asm.PLY(),
            asm.TDC(),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "scan all learn_scan")
        learn_spells_snes = space.start_address_snes

        space = Reserve(0x0bdcc, 0x0bdd6, "initialize spells and learn initial", asm.NOP())
        space.write(
            asm.JSL(learn_spells_snes),
        )
