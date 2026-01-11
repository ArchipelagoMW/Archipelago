from ..memory.space import Write, Bank, Reserve
from ..instruction import asm as asm
from .. import args as args

class MagicMenu:
    def __init__(self):
        self.mod()

    def draw_three_digits(self):
        # Enable drawing of 3 digits
        # Create string function
        STRING_DRAW_ADDR = 0x2180 # Where to write strings to be written
        src = [
            asm.LDA(0xF7, asm.DIR),             # Hundreds digit
            asm.STA(STRING_DRAW_ADDR, asm.ABS), # Add to string
            # displaced vanilla logic, from C3/51E9 - 51ED 
            asm.LDA(0xF8, asm.DIR),             # Tens digit
            asm.STA(STRING_DRAW_ADDR, asm.ABS), # Add to string
            asm.RTL()
        ]
        space = Write(Bank.F0, src, "Create MP Cost string")
        create_string = space.start_address_snes

        space = Reserve(0x351e9, 0x351ed, "Call create_string", asm.NOP())
        space.write(
            asm.JSL(create_string),
        )

        # Move where MP gets written 1 space to the left, 
        # to avoid having the number show up at the top of the "Espers" menu
        space = Reserve(0x351cd, 0x351cd, "MP String location")
        space.write(0xbd) #original: 0xbf (each text space is a value of 2)

    def fix_in_battle_mp_tens_digit(self):
        # Fix Vanilla in-battle MP listing in which the ten's digit is blanked
        # if it is 0 but the hundreds digit is not
        space = Reserve(0x1057b, 0x1057b, "MP Hundreds non-zero BNE offset")
        space.write(0x14) # original: 0x08; 0x14 causes it to jump to RTS if the hundreds place is non-zero

    def mod(self):
        self.draw_three_digits()
        self.fix_in_battle_mp_tens_digit()
