from ..memory.space import Bank, Reserve, Allocate
from ..instruction import asm as asm
from .. import args as args

class StatusMenu:
    def __init__(self, characters):
        self.free_space = Allocate(Bank.C3, 61, "status menu")
        self.characters = characters

        self.mod()

    def mod_natural_magic(self):
        from ..data import text as text

        natural_magic_learners = []
        if self.characters.natural_magic.learner1 is not None:
            natural_magic_learners.append(self.characters.natural_magic.learner1)
        if self.characters.natural_magic.learner2 is not None:
            natural_magic_learners.append(self.characters.natural_magic.learner2)

        if not natural_magic_learners:
            return

        empty_position_text = self.free_space.next_address
        self.free_space.write(
            0xb7, 0x3a, # x/y position
            text.get_bytes("       ", text.TEXT3),
            0x00,       # end
        )

        natural_position_text = self.free_space.next_address
        self.free_space.write(
            0xb7, 0x3a, # x/y position
            text.get_bytes("Natural", text.TEXT3),
            0x00,       # end
        )

        draw_lv_hp_mp_natural = self.free_space.next_address
        self.free_space.copy_from(0x35d58, 0x35d5a) # call draw LV/HP/MP

        # status menu and lineup store character data/slots in ram differently
        # status menu can also be reached from main menu or L/R switching
        self.free_space.write(
            asm.LDA(0x25, asm.DIR),     # a = main menu cursor pos (set to zero for lineup at c36328)
            asm.CMP(0x04, asm.IMM8),    # status menu reached from main menu?
            asm.BNE("LINEUP_MENU"),     # branch if not

            asm.XY8(),
            asm.LDX(0x28, asm.DIR),     # x = character slot
            asm.LDA(0x69, asm.DIR_X),   # a = character id
            asm.XY16(),
            asm.BRA("LEARNER_CHECK"),

            "LINEUP_MENU",
            asm.LDA(0xc9, asm.DIR),     # load character id

            "LEARNER_CHECK",
        )
        for learner in natural_magic_learners:
            self.free_space.write(
                asm.CMP(learner, asm.IMM8), # compare character with learner
                asm.BEQ("DRAW_NATURAL"),
            )

        # if not a natural magic learner, write spaces to cover up "Natural" in case switching characters using L/R
        # this is also how MP display is handled (c30cba)
        self.free_space.write(
            "DRAW_EMPTY",
            asm.LDY(empty_position_text, asm.IMM16),
            asm.BRA("DRAW_TEXT_RETURN"),

            "DRAW_NATURAL",
            asm.LDY(natural_position_text, asm.IMM16),

            "DRAW_TEXT_RETURN",
            asm.JSR(0x02f9, asm.ABS),   # call draw text
            asm.RTS(),
        )

        space = Reserve(0x35d58, 0x35d5a, "status draw LV/HP/MP and Natural", asm.NOP())
        space.write(
            asm.JSR(draw_lv_hp_mp_natural, asm.ABS),
        )

    def mod(self):
        if args.natural_magic_menu_indicator:
            self.mod_natural_magic()
