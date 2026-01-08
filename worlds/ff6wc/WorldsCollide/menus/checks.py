from ..memory.space import Bank, START_ADDRESS_SNES, Write
from ..instruction import asm as asm
from ..instruction import f0 as f0
from .. import args as args

from ..data import event_bit as event_bit
from ..constants.gates import character_checks
from ..constants.objectives import condition_bits as condition_bits
from ..menus import pregame_track_scroll_area as scroll_area

# 0x0002 is not 0xffff after a battle (bug? c2d450), use 0x1202 instead
constant_ffff = 0x1202 # always contains value 0xffff

class Checks(scroll_area.ScrollArea):
    MENU_NUMBER = 13

    def __init__(self):
        self.check_bits = {}
        for name_bit in condition_bits.check_bit:
            self.check_bits[name_bit.name] = name_bit.bit
        self.check_bits["Auction1"] = event_bit.AUCTION_BOUGHT_ESPER1
        self.check_bits["Auction2"] = event_bit.AUCTION_BOUGHT_ESPER2

        if args.character_gating:
            self.character_gating_init()
        else:
            self.open_world_init()

        super().__init__()

    def line_color_function(self, address, bit):
        src = [
            asm.LDA(address, asm.ABS),
            asm.AND(2 ** bit, asm.IMM8),
            asm.BEQ("FALSE"),
            asm.JMP(f0.set_gray_text_color, asm.ABS),

            "FALSE",
            asm.JMP(f0.set_user_text_color, asm.ABS),
        ]
        space = Write(Bank.F0, src, f"menu checks line color function {hex(address)} {hex(bit)}")
        return space.start_address

    def open_world_init(self):
        checks = []
        for group in character_checks.values():
            checks += group
        checks = sorted(checks)

        self.lines = []
        self.line_skip_bits = []
        for check in checks:
            check_address = event_bit.address(self.check_bits[check])
            check_bit = event_bit.bit(self.check_bits[check])
            color_function = self.line_color_function(check_address, check_bit)

            self.lines.append(scroll_area.Line(check, color_function))
            self.line_skip_bits.append((constant_ffff, 0x01))   # never skip

    def character_gating_init(self):
        from ..data.characters import Characters

        self.lines = []
        self.line_skip_bits = []
        for character, checks in character_checks.items():
            if not character:
                character = "Open"
                character_address = constant_ffff   # always 0xffff
                character_bit = 0x01                # any bit
            else:
                character_id = Characters.DEFAULT_NAME.index(character.upper())
                character_event_bit = event_bit.character_recruited(character_id)
                character_address = event_bit.address(character_event_bit)
                character_bit = event_bit.bit(character_event_bit)

            self.lines.append(scroll_area.Line(character, f0.set_blue_text_color))
            self.line_skip_bits.append((character_address, character_bit))

            for check in checks:
                check_address = event_bit.address(self.check_bits[check])
                check_bit = event_bit.bit(self.check_bits[check])
                color_function = self.line_color_function(check_address, check_bit)

                self.lines.append(scroll_area.Line("  " + check, color_function))
                self.line_skip_bits.append((character_address, character_bit))

            self.lines.append(scroll_area.Line("", f0.set_user_text_color))
            self.line_skip_bits.append((character_address, character_bit))

        del self.lines[-1]
        del self.line_skip_bits[-1]

    def initialize_mod(self):
        src = []
        for address_bit in self.line_skip_bits:
            src += [
                address_bit[0].to_bytes(2, "little"),
                2 ** address_bit[1],
            ]
        space = Write(Bank.F0, src, "menu checks post invoke byte bit table")
        byte_bit_table = space.start_address

        # write out which indices of self.lines to display
        # pad end of scroll area with empty lines (represented by index 0xff)
        # NOTE: using 256 bytes of ram starting at 0x7e2000
        src = [
            asm.TDC(),
            asm.LDY(0x0000, asm.IMM16),         # y = self.lines index (character/check line index)
            asm.STY(0xe5, asm.DIR),             # e5 = menu line index, e6 = byte_bit_table index

            "LINE_LOOP_START",
            asm.LDA(0xe6, asm.DIR),             # a = index of event byte address in byte_bit_table
            asm.A16(),
            asm.TAX(),                          # x = index of event byte address in byte_bit_table
            asm.LDA(START_ADDRESS_SNES + byte_bit_table, asm.LNG_X),    # a = event byte address
            asm.TAX(),                          # x = event byte address
            asm.TDC(),
            asm.A8(),
            asm.LDA(0x00, asm.DIR_X),           # a = event byte value

            asm.INC(0xe6, asm.DIR),
            asm.INC(0xe6, asm.DIR),             # e6 = byte_bit_table index of bit (2 byte address, 1 byte event bit)
            asm.LDX(0x00, asm.DIR),             # clear x register
            asm.XY8(),
            asm.LDX(0xe6, asm.DIR),             # x = byte_bit_table index of bit
            asm.XY16(),
            asm.AND(START_ADDRESS_SNES + byte_bit_table, asm.LNG_X),    # is event bit set in event byte?
            asm.BEQ("SKIP_LINE"),               # branch if not

            asm.LDA(0xe5, asm.DIR),             # a = menu line index
            asm.TYX(),                          # x = self.lines index to display at this menu index
            asm.STA(0x7e2000, asm.LNG_X),
            asm.INY(),                          # next self.lines index

            "SKIP_LINE",
            asm.INC(0xe5, asm.DIR),             # next menu line index
            asm.INC(0xe6, asm.DIR),             # next event byte
            asm.LDA(0xe5, asm.DIR),
            asm.CMP(len(self.lines), asm.IMM8), # finished checking every line in self.lines?
            asm.BLT("LINE_LOOP_START"),         # branch if not

            # fill the rest of the menu with empty lines
            asm.LDA(0xff, asm.IMM8),
            asm.TYX(),                          # x = index after last self.lines index written
            "PADDING",
            asm.CPX(len(self.lines), asm.IMM16),
            asm.BGE("RETURN"),
            asm.STA(0x7e2000, asm.LNG_X),
            asm.INX(),
            asm.BRA("PADDING"),

            "RETURN",
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "menu checks initialize store line indices to draw")
        self.initialize = space.start_address

    def initialize_line_mod(self):
        src = [
            asm.LDX(0x0003, asm.IMM16),     # x = 3 (x position to write at)
            asm.JSL(scroll_area.set_line_x_pos),

            asm.TDC(),
            asm.LDA(0xe5, asm.DIR),         # menu line index
            asm.TAX(),
            asm.LDA(0x7e2000, asm.LNG_X),   # look up line to write at current menu line
            asm.TAY(),                      # y = character/check line index
            asm.CMP(0xff, asm.IMM8),        # last line or hidden?
            asm.BEQ("AFTER_SET_COLOR"),     # branch if so

            asm.JSR(self.set_line_color, asm.ABS),

            "AFTER_SET_COLOR",
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "menu checks initialize line set line color")
        self.initialize_line = space.start_address
