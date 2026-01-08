from ..memory.space import Bank, Reserve, Allocate
from ..instruction import asm as asm
from .. import args as args

class DanceMenu:
    def __init__(self, dances):
        self.free_space = Allocate(Bank.C3, 112, "dance menu")
        self.dances = dances

        self.mod()

    def draw_ability_names_mod(self):
        from ..data import text as text
        dance_data_address = self.dances.DATA_START + 0xc00000

        comma_value = int.from_bytes(text.get_bytes(',', text.TEXT3), "little")
        space_value = int.from_bytes(text.get_bytes(' ', text.TEXT3), "little")
        line_value = int.from_bytes(text.get_bytes("<line>", text.TEXT3), "little")

        draw_comma_space = self.free_space.next_address
        self.free_space.write(
            asm.LDA(comma_value, asm.IMM8), # load ',' character
            asm.STA(0x2180, asm.ABS),       # add ',' to string
            asm.LDA(space_value, asm.IMM8), # load ' ' character
            asm.STA(0x2180, asm.ABS),       # add ' ' to string
            asm.RTS(),
        )

        # argument: x = dance data index
        draw_ability_name = self.free_space.next_address
        self.free_space.write(
            asm.PHX(),
            asm.PHY(),
            asm.LDA(dance_data_address, asm.LNG_X),   # a = ability id
            asm.SEC(),
            asm.SBC(0x65, asm.IMM8),    # a = dance ability index (dance names start at 0x65)
            asm.STA(0x4202, asm.ABS),   # $4202 = dance ability index
            asm.LDY(self.dances.ABILITY_NAME_SIZE, asm.IMM16),
            asm.STY(0x4203, asm.ABS),   # $4203 = ability name length
            asm.NOP(),                  # wait for multiplication...
            asm.NOP(),
            asm.NOP(),
            asm.NOP(),
            asm.LDX(0x4216, asm.ABS),   # x = ability index * ability name length

            "ABILITY_NAME_LOOP_START",
            asm.LDA(self.dances.ABILITY_NAMES_START, asm.LNG_X),  # a = current char in ability name
            asm.CMP(space_value, asm.IMM8),         # compare with character ' ' which pads end of ability names
            asm.BEQ("DRAW_ABILITY_NAME_RETURN"),    # branch if reached end of ability name
            asm.STA(0x2180, asm.ABS),               # add character to string
            asm.INX(),                              # next character in ability name
            asm.DEY(),                              # decrement ability name character index
            asm.BNE("ABILITY_NAME_LOOP_START"),     # branch if not zero

            "DRAW_ABILITY_NAME_RETURN",
            asm.PLY(),
            asm.PLX(),
            asm.RTS(),
        )

        draw_ability_name_row = self.free_space.next_address
        self.free_space.write(
            asm.JSR(draw_ability_name, asm.ABS),    # draw current dance ability
            asm.JSR(draw_comma_space, asm.ABS),     # draw ', ' separator
            asm.INX(),                              # next dance ability
            asm.JSR(draw_ability_name, asm.ABS),    # draw current dance ability
            asm.RTS(),
        )

        draw_ability_names = self.free_space.next_address
        self.free_space.write(
            asm.LDX(0x9ec9, asm.IMM16),     # dest WRAM LBs
            asm.STX(0x2181, asm.ABS),       # store dest WRAM LBs

            asm.TDC(),                      # a = 0x0000
            asm.LDA(0x4b, asm.DIR),         # a = cursor index (dance index)
            asm.TAX(),                      # x = cursor index (dance index)
            asm.LDA(0x7e9d89, asm.LNG_X),   # a = dance at cursor index
            asm.CMP(0xff, asm.IMM8),        # compare with no dance
            asm.BEQ("END_STRING_RETURN"),   # branch if dance at cursor index not learned

            asm.ASL(),
            asm.ASL(),                      # a = dance index * 4 (4 abilities per dance)
            asm.TAX(),                      # x = dance index * 4 (dance ability data index)
            asm.JSR(draw_ability_name_row, asm.ABS),  # draw first row of dance abilities

            asm.LDA(line_value, asm.IMM8),  # load newline character
            asm.STA(0x2180, asm.ABS),       # add newline character to string

            asm.INX(),                      # next dance ability
            asm.JSR(draw_ability_name_row, asm.ABS),  # draw second row of dance abilities

            "END_STRING_RETURN",
            asm.STZ(0x2180, asm.ABS),       # end string
            asm.RTS(),
        )

        sustain_replace = 0x328ad   # handle d-pad
        replace_size = 3            # replacing jsr instructions

        sustain_dance_list = self.free_space.next_address
        self.free_space.write(
            asm.LDA(0x10, asm.IMM8),# enable description menu flag bitmask
            asm.TRB(0x45, asm.DIR), # enable descriptions
        )
        self.free_space.copy_from(sustain_replace, sustain_replace + replace_size - 1) # handle d-pad
        self.free_space.write(
            asm.JMP(draw_ability_names, asm.ABS),
        )

        space = Reserve(sustain_replace, sustain_replace + replace_size - 1, "dance menu sustain handle d-pad")
        space.write(
            asm.JSR(sustain_dance_list, asm.ABS),
        )

    def mod(self):
        if args.dances_display_abilities:
            self.draw_ability_names_mod()
