from ..memory.space import Bank, START_ADDRESS_SNES, Write
from ..instruction import asm as asm
from ..instruction import f0 as f0
from .. import args as args

from ..menus import pregame_track_scroll_area as scroll_area

# 0x0002 is not 0xffff after a battle (bug? c2d450), use 0x1202 instead
constant_ffff = 0x1202 # always contains value 0xffff

class Progress(scroll_area.ScrollArea):
    MENU_NUMBER = 14

    def __init__(self):
        # values in range [special_characters_start, len(event_words to display)] used as placeholders
        # when value in range found, write value of event_word[index - start]
        self.special_characters_start = 1

        labels = [
            "Checks Complete",
            "Characters Available",
            "Espers Found",
            "Dragons Defeated",
            "Bosses Defeated",
        ]

        self.lines = []
        for index, label in enumerate(labels):
            self.lines.append(scroll_area.Line(label, f0.set_user_text_color))
            self.lines.append(scroll_area.Line("", f0.set_user_text_color))
        del self.lines[-1] # exclude final empty line

        super().__init__()

    def initialize_line_mod(self):
        from ..data import event_word as event_word
        event_words = [
            event_word.CHECKS_COMPLETE,
            event_word.CHARACTERS_AVAILABLE,
            event_word.ESPERS_FOUND,
            event_word.DRAGONS_DEFEATED,
            event_word.BOSSES_DEFEATED,
        ]

        addresses = []
        for word in event_words:
            addresses += [
                event_word.address(word),
                constant_ffff,
            ]

        # ensure there is an address for each line
        for _ in range(len(addresses), len(self.lines)):
            addresses.append(constant_ffff)

        value_functions = []
        for address in addresses:
            src = [
                asm.LDA(address, asm.ABS),
                asm.RTS(),
            ]
            space = Write(Bank.F0, src, "progress menu load value at {hex(address)}")
            value_functions.append(space.start_address)

        src = []
        for function in value_functions:
            src += [
                (function & 0xffff).to_bytes(2, "little"),
            ]
        space = Write(Bank.F0, src, "progress menu value functions table")
        value_functions_table = space.start_address

        src = [
            asm.JSR(0x04e0, asm.ABS),   # convert value in a to text
            asm.LDA(0xe6, asm.DIR),     # a = bg1 row
            asm.INC(),
            asm.LDX(0x0003, asm.IMM16), # x = x position to write at
            asm.JSR(0x809f, asm.ABS),   # x/y position in bg1 a
            asm.JSR(0x04b6, asm.ABS),   # draw 2 digit number
            asm.RTL(),
        ]
        space = Write(Bank.C3, src, "draw 2 digit number long function")
        draw_2_digit_number = space.start_address

        src = [
            asm.LDX(0x0006, asm.IMM16),  # x = 3 (x position to write at)
            asm.JSL(scroll_area.set_line_x_pos),

            asm.JSR(self.set_line_color, asm.ABS),

            asm.JSR(value_functions_table, asm.ABS_X_16),
            asm.CMP(100, asm.IMM8),     # if more than 2 digits, do not show anything
            asm.BGE("RETURN"),

            asm.PHY(),
            asm.JSL(START_ADDRESS_SNES + draw_2_digit_number),
            asm.PLY(),

            "RETURN",
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "progress menu initialize line")
        self.initialize_line = space.start_address
