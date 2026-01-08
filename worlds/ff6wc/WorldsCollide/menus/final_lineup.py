from ..memory.space import Bank, START_ADDRESS_SNES, Reserve, Allocate
from ..instruction import asm as asm
from .. import args as args

class FinalLineupMenu:
    LINEUP_SIZE = 12 # number of characters listed in lineup

    def __init__(self, characters):
        self.free_space = Allocate(Bank.C3, 175, "final lineup")
        self.characters = characters

        self.mod()

    def original_names_mod(self):
        from ..data import text as text

        # shift left list further left and right list further right to make room for default names
        space = Reserve(0x3ac8a, 0x3ac8b, "final lineup menu 'End' text position")
        space.write(0x0f, 0x40)

        space = Reserve(0x3ac90, 0x3ac91, "final lineup menu 'Reset' text position")
        space.write(0x8f, 0x39)

        space = Reserve(0x3ac1e, 0x3ac1f, "final lineup menu left column numbers position")
        space.write(0x0d, 0x3a)

        space = Reserve(0x3ac2f, 0x3ac30, "final lineup menu right column numbers position")
        space.write(0x33, 0x3a)

        space = Reserve(0x3ab8a, 0x3ab8b, "final lineup menu left column names position")
        space.write(0x13, 0x3a)

        space = Reserve(0x3abb9, 0x3abba, "final lineup menu right column names position")
        space.write(0x39, 0x3a)

        space = Reserve(0x3ac68, 0x3ac83, "final lineup menu cursor positions")
        space.write(
            0x08, 0x20, # 'Reset' cursor position
        )

        first_name_position = 0x2c18
        row_size = 0xc00
        for index in range(self.LINEUP_SIZE):
            space.write(
                (first_name_position + row_size * index).to_bytes(2, "little"),
            )

        space.write(
            0x08, 0xbc, # 'End' cursor position
        )

        original_name_length = 8 # 6 for name + 2 for parenthesis
        original_names = self.free_space.next_address

        for default_name in self.characters.DEFAULT_NAME:
            self.free_space.write(
                text.get_bytes(("(" + default_name + ")").ljust(original_name_length), text.TEXT3),
            )

        draw_left_column_names = self.free_space.next_address
        self.free_space.copy_from(0x3aba1, 0x3aba3) # call draw name
        self.free_space.write(
            # pull current slot index from stack and restore stack to previous state
            asm.PLY(),                      # pull return address
            asm.PLX(),                      # pull slot index
            asm.PHX(),                      # push slot index
            asm.PHY(),                      # push return address

            # push current position and set new position to draw text
            asm.A16(),
            asm.LDA(0xf5, asm.DIR),         # a = current text position
            asm.PHA(),
            asm.ADC(0x000e, asm.IMM16),     # add x offset to current position
            asm.STA(0xf5, asm.DIR),         # $f5 = position to draw original name
            asm.JSR(0xabdc, asm.ABS),       # call update position
            asm.A16(),

            # draw original name
            asm.LDA(0x7e9d8a, asm.LNG_X),   # a = index of character in current slot
            asm.AND(0x00ff, asm.IMM16),     # clear high byte
            asm.ASL(),
            asm.ASL(),
            asm.ASL(),                      # a = character index * 8
            asm.TAX(),                      # x = character index * 8 (string length)
            asm.LDY(original_name_length, asm.IMM16),
            asm.A8(),

            "DRAW_NAME_LOOP_START",
            asm.LDA(START_ADDRESS_SNES + original_names, asm.LNG_X),
            asm.STA(0x2180, asm.ABS),       # write next character in string to draw
            asm.INX(),                      # next character in string
            asm.DEY(),                      # decrement string length counter
            asm.BNE("DRAW_NAME_LOOP_START"),# branch if not zero
            asm.STZ(0x2180, asm.ABS),       # write end of character to draw
            asm.JSR(0x7fd9, asm.ABS),       # call draw string

            # restore position to draw text
            asm.A16(),
            asm.PLA(),                      # pull current text position
            asm.STA(0xf5, asm.DIR),
            asm.A8(),
            asm.RTS(),
        )

        space = Reserve(0x3aba1, 0x3aba3, "final lineup menu left column call draw name")
        space.write(
            asm.JSR(draw_left_column_names, asm.ABS),
        )

        # draw original_name_length spaces instead of just 6
        # because original_name_length characters were written to $2180 which need to be overwritten (erased)
        space = Reserve(0x3ac0c, 0x3ac0c, "final lineup menu empty character name length")
        space.write(original_name_length)

    def mod(self):
        if args.original_name_display:
            self.original_names_mod()
