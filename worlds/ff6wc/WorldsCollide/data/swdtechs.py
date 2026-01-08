from ..data.swdtech import SwdTech
from ..data.structures import DataArray

from ..memory.space import Bank, Reserve, Allocate, Write
from ..instruction import asm as asm

class SwdTechs:
    NAMES_START = 0x0f3c40
    NAMES_END = 0x0f3c9f

    def __init__(self, rom, args, characters):
        self.rom = rom
        self.args = args
        self.characters = characters

        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, SwdTech.NAME_SIZE)

        self.swdtechs = []
        for swdtech_index in range(len(self.name_data)):
            swdtech = SwdTech(swdtech_index, self.name_data[swdtech_index])
            self.swdtechs.append(swdtech)

    def write_learners_table(self):
        self.learners = self.characters.get_characters_with_command("SwdTech")

        space = Allocate(Bank.CF, self.characters.CHARACTER_COUNT, "swdtech learners")
        space.write(self.learners)

        self.learners_table = space.start_address
        self.learners_table_end = self.learners_table + len(self.learners)

    def write_is_learner(self):
        from ..instruction import c0 as c0

        src = [
            asm.PHY(),
            asm.LDX(self.learners_table_end, asm.IMM16),# offset in bank to last learner in table + 1
            asm.LDY(len(self.learners), asm.IMM16),     # learners table size
            asm.JSR(c0.is_skill_learner, asm.ABS),
            asm.PLY(),
            asm.RTL(),
        ]
        space = Write(Bank.C0, src, "swdtech is learner")
        self.is_learner_function = space.start_address_snes

    def event_check_mod(self):
        from ..memory.space import START_ADDRESS_SNES
        from ..instruction import c0 as c0

        learn_swdtechs = 0x0a1da
        character_recruited = c0.character_recruited + START_ADDRESS_SNES

        space = Allocate(Bank.C0, 24, "swdtech event check", asm.NOP())
        space.write(
            asm.PHA(),
            asm.JSL(character_recruited),
            asm.CMP(0x00, asm.IMM8),        # compare result with 0
            asm.BEQ("RETURN"),              # branch if character not recruited
        )
        if not self.args.swdtechs_everyone_learns:
            space.write(
                asm.PLA(),
                asm.PHA(),
                asm.JSL(self.is_learner_function),
                asm.CMP(0x00, asm.IMM8),    # compare result with 0
                asm.BEQ("RETURN"),          # branch if character not learner
            )
        space.write(
            asm.JSR(learn_swdtechs, asm.ABS),

            "RETURN",
            asm.PLA(),
            asm.RTS(),
        )
        check_swdtechs = space.start_address

        space = Reserve(0x0a18a, 0x0a18d, "event check cyan learn swdtechs", asm.NOP())
        if self.learners:
            space.write(
                asm.JSR(check_swdtechs, asm.ABS),
            )

    def after_battle_check_mod(self):
        learn_swdtechs = 0x261cb

        space = Allocate(Bank.C2, 31, "swdtech check after battle", asm.NOP())
        space.write(
            asm.A16(),
            asm.PHA(),
            asm.A8(),
        )
        if not self.args.swdtechs_everyone_learns:
            space.write(
                asm.JSL(self.is_learner_function),
                asm.CMP(0x00, asm.IMM8),    # compare result with 0
                asm.BEQ("RETURN"),          # branch if character not learner
                asm.A16(),
                asm.PLA(),
                asm.PHA(),
                asm.A8(),
            )
        space.write(
            asm.LDX(0x0000, asm.IMM16),
            asm.JSR(learn_swdtechs, asm.ABS),

            "RETURN",
            asm.A16(),
            asm.PLA(),
            asm.A8(),
            asm.RTS(),
        )
        check_swdtechs = space.start_address

        if self.learners:
            space = Reserve(0x261c4, 0x261c8, "battle check cyan learn swdtechs", asm.NOP())
            space.write(
                asm.JSR(check_swdtechs, asm.ABS),
            )
        else:
            space = Reserve(0x261c7, 0x261c8, "battle check cyan learn swdtechs", asm.NOP())

        space = Reserve(0x261c9, 0x261c9, "battle always check learn blitzes")
        space.write(0x80) # change bne to bra to always check for learning blitzes after swdtech

    def enable_fast_swdtech(self):
        # bitwise and the frame counter with this byte, if result is 0 then swdtech bar is not incremented
        # every 32 increments is a new swdtech, 8 swdtechs so bar is full and resets after 256 increments
        # 0 is fastest speed possible which increments every frame, at 60fps that is 32/60 = 0.53 seconds per swdtech
        space = Reserve(0x17d87, 0x17d87, "swdtech speed")
        space.write(0x00)

    def mod(self):
        self.write_learners_table()
        self.write_is_learner()

        self.event_check_mod()
        self.after_battle_check_mod()

        if self.args.fast_swdtech:
            self.enable_fast_swdtech()

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for swdtech_index, swdtech in enumerate(self.swdtechs):
            self.name_data[swdtech_index] = swdtech.name_data()

        self.name_data.write()

    def log(self):
        pass

    def print(self):
        for swdtech in self.swdtechs:
            swdtech.print()
