from ..memory.space import START_ADDRESS_SNES, Bank, Write
from ..instruction import asm as asm
from ..instruction import f0 as f0
from ..instruction import c3 as c3

from enum import IntEnum
from collections import namedtuple

WIDTH = 26  # max characters per row
HEIGHT = 10 # rows visible on screen

ROWS = 10   # scrollable rows (same as height)
COLS = 1    # scrollable cols

SCROLLBAR_INITIAL_Y = 0x58
SCROLLBAR_INDEX = 0x30 # always the same because remove old one before creating new one

CURRENT_TYPE_ADDR = 0x0204  # address to store currently displayed scroll area type

Line = namedtuple("Line", ["text", "color_function"])

def _draw_mod():
    src = [
        asm.JSR(0x7e0d, asm.ABS),   # clear bg1 a, draw list
        asm.JSR(0x7e01, asm.ABS),   # upload bg1 abc, bg3 abcd
        asm.RTS(),
    ]
    space = Write(Bank.C3, src, "pregame track scroll area draw")
    return space.start_address
draw = _draw_mod()

def _set_line_x_pos_mod():
    src = [
        asm.TDC(),                  # clear a
        asm.LDA(0xe6, asm.DIR),     # a = bg1 row
        asm.INC(),                  # increment row
        asm.JSR(0x809f, asm.ABS),   # calculate x/y position in bg1 a
        asm.A16(),
        asm.TXA(),
        asm.STA(0x7e9e89, asm.LNG), # store position
        asm.A8(),
        asm.TDC(),
        asm.LDA(0xe5, asm.DIR),     # a = line index
        asm.TAY(),
        asm.RTL(),
    ]
    space = Write(Bank.C3, src, "pregame track scroll area set line x position")
    return space.start_address
set_line_x_pos = _set_line_x_pos_mod()

# 2 bytes to store cursor position + 1 byte to store page position
# addresses >= 0x250 and < 0x300 in menu ram seem available
# first custom scroll area menu number is 11, 0x22f + 0xb * 3 = 0x250
MEMORY_CURSOR_POSITIONS_START_ADDR = 0x22f
MEMORY_PAGE_POSITIONS_START_ADDR = 0x231
def memory_cursor_position(menu_number):
    return MEMORY_CURSOR_POSITIONS_START_ADDR + menu_number * 3
def memory_page_position(menu_number):
    return MEMORY_PAGE_POSITIONS_START_ADDR + menu_number * 3

class ScrollArea:
    def __init__(self):
        # fill out entire scroll area so everything in window is overwritten when switching menus
        for _ in range(len(self.lines), HEIGHT):
            self.lines.append(Line("", f0.set_user_text_color))

        line_color_addresses = []
        for li in range(len(self.lines)):
            line_color_addresses.extend((self.lines[li].color_function & 0xffff).to_bytes(2, "little"))
            self.lines[li] = Line(self.lines[li].text.ljust(WIDTH), self.lines[li].color_function)

        space = Write(Bank.F0, line_color_addresses, "pregame track scroll area line colors table")
        self.line_colors_table = space.start_address

        self.number_excess_lines = max(len(self.lines) - HEIGHT, 0)
        assert self.number_excess_lines <= 256
        if self.number_excess_lines > 0:
            # this seems to match scrollable area and rows well enough
            self.scrollbar_speed = int(27000 * self.number_excess_lines ** -1.0)
        else:
            self.scrollbar_speed = 0

        self.memory_cursor_position = memory_cursor_position(self.MENU_NUMBER)
        self.memory_page_position = memory_page_position(self.MENU_NUMBER)

        self.mod()

    def initialize_mod(self):
        self.initialize = None

    def invoke_mod(self):
        visible_scrollbar = 0xc0    # $46 mask for show/hide scrollbar
        src = [
            asm.LDA(self.MENU_NUMBER, asm.IMM8),
            asm.STA(0x0200, asm.ABS),
            asm.CMP(CURRENT_TYPE_ADDR, asm.ABS),
            asm.BEQ("CURRENT_TYPE_SHOWING"),
            asm.STA(CURRENT_TYPE_ADDR, asm.ABS),

            asm.LDX(SCROLLBAR_INDEX, asm.IMM16),# x = scrollbar index

            asm.A16(),
            asm.LDA(0x0000, asm.IMM16),
            asm.STA(0x7e3249, asm.LNG_X),       # remove old scrollbar
            asm.A8(),

            asm.LDA(self.number_excess_lines, asm.IMM8),
            asm.STA(0x5c, asm.DIR),
            asm.CMP(0x00, asm.IMM8),            # does this menu have excess lines? (i.e. need scrollbar?)
            asm.BNE("CREATE_SCROLLBAR"),        # branch if so

            asm.LDA(visible_scrollbar, asm.IMM8),
            asm.TRB(0x46, asm.DIR),             # hide scrollbar
            asm.BRA("UPDATE_SCROLLBAR"),

            "CREATE_SCROLLBAR",
            asm.JSR(0x091f, asm.ABS),           # create scrollbar, x = scrollbar index
            asm.LDA(visible_scrollbar, asm.IMM8),
            asm.TSB(0x46, asm.DIR),             # show scrollbar

            "UPDATE_SCROLLBAR",
            asm.STZ(0x4a, asm.DIR),             # index of first row displayed
            asm.STZ(0x50, asm.DIR),             # cursor index [0, len(lines))

            asm.A16(),
            asm.LDA(SCROLLBAR_INITIAL_Y, asm.IMM16),
            asm.STA(0x7e34ca, asm.LNG_X),
            asm.LDA(self.scrollbar_speed, asm.IMM16),
            asm.STA(0x7e354a, asm.LNG_X),
            asm.A8(),

            "CURRENT_TYPE_SHOWING",
            asm.JSR(0x7d1c, asm.ABS),           # load navigation data

            # cursor position (reset/memory)
            asm.LDA(0x1d4e, asm.ABS),           # load game config
            asm.AND(0x40, asm.IMM8),            # cursor memory enabled?
            asm.BEQ("UPDATE_CURSOR"),           # branch if not

            asm.JSL(self.remember_cursor + START_ADDRESS_SNES),

            "UPDATE_CURSOR",
            asm.JSR(0x7d25, asm.ABS),           # update cursor

            asm.JSR(draw, asm.ABS),             # draw scroll area
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "pregame track scroll area invoke")
        self.invoke = space.start_address

    def set_line_color_mod(self):
        src = [
            asm.A16(),
            asm.TYA(),                  # a = line index
            asm.ASL(),                  # a = line index * 2
            asm.TAX(),                  # x = line index * 2 (2 bytes per entry in line colors table)
            asm.A8(),
            asm.JSR(self.line_colors_table, asm.ABS_X_16),  # set line color
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, "pregame track scroll area set line color")
        self.set_line_color = space.start_address

    def initialize_line_mod(self):
        src = [
            asm.LDX(0x0003, asm.IMM16), # x = 3 (x position to write at)
            asm.JSL(set_line_x_pos),

            asm.JSR(self.set_line_color, asm.ABS),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame track scroll area set line color")
        self.initialize_line = space.start_address

    def draw_character_mod(self):
        src = [
            asm.STA(0x2180, asm.ABS),   # write current character
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame track scroll area draw character")
        self.draw_character = space.start_address

    def draw_line_mod(self):
        from ..data.text.text2 import text_value

        src = []
        for line in self.lines:
            for index, character in enumerate(line.text):
                if character not in text_value:
                    src.append(ord(character)) # assume special character
                else:
                    src.append(text_value[character])
        space = Write(Bank.F0, src, "pregame track scroll area lines table")
        lines_table = space.start_address + START_ADDRESS_SNES

        src = [
            asm.LDX(0x9e8b, asm.IMM16), # wram LBs
            asm.STX(0x2181, asm.ABS),   # store wram LBs

            "H_BLANK_CHECK",
            asm.LDA(0x4212, asm.ABS),   # PPU status
            asm.AND(0x40, asm.IMM8),    # h-blank?
            asm.BEQ("H_BLANK_CHECK"),

            asm.TYA(),                  # a = line index
            asm.CMP(len(self.lines), asm.IMM8),
            asm.BGE("WRITE_BLANK_LINE"),# if hidden, draw empty line

            asm.STA(0x211b, asm.ABS),   # matrix a LB
            asm.STZ(0x211b, asm.ABS),   # matrix a HB
            asm.LDA(WIDTH, asm.IMM8),
            asm.STA(0x211c, asm.ABS),   # matrix b LB
            asm.STA(0x211c, asm.ABS),   # matrix b HB
            asm.LDX(0x2134, asm.ABS),   # x = line index * characters per line

            asm.LDY(WIDTH, asm.IMM16),  # y = characters per line
            "LOOP_START",
            asm.LDA(lines_table, asm.LNG_X),
            asm.JSL(START_ADDRESS_SNES + self.draw_character),

            asm.INX(),                  # next character
            asm.DEY(),                  # decrement count
            asm.BNE("LOOP_START"),      # branch if more characters in line
            asm.STZ(0x2180, asm.ABS),   # write end of string
            asm.RTL(),

            "WRITE_BLANK_LINE",
            asm.LDY(WIDTH, asm.IMM16),
            asm.LDA(text_value[' '], asm.IMM8),
            "WRITE_BLANK_LINE_LOOP",
            asm.STA(0x2180, asm.ABS),
            asm.DEY(),
            asm.BNE("WRITE_BLANK_LINE_LOOP"),
            asm.STZ(0x2180, asm.ABS),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame track scroll area write line")
        write_line = space.start_address

        src = [
            asm.JSL(START_ADDRESS_SNES + self.initialize_line),
            asm.JSL(START_ADDRESS_SNES + write_line),
            asm.JSR(0x37fd9, asm.ABS),  # draw line
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "pregame track scroll area draw line")
        self.draw_line = space.start_address

    def remember_cursor_mod(self):
        src = [
            asm.LDY(self.memory_cursor_position, asm.ABS),
            asm.STY(0x4f, asm.DIR),
            asm.LDA(0x4f, asm.DIR),
            asm.STA(0x4d, asm.DIR),
            asm.LDA(self.memory_page_position, asm.ABS),
            c3.eggers_jump(0x0e1e),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame track scroll area remember cursor")
        self.remember_cursor = space.start_address

    def remember_scrollbar_mod(self):
        src = [
            asm.LDA(self.number_excess_lines, asm.IMM8),
            asm.STA(0x5c, asm.DIR),

            asm.A16(),
            asm.LDA(self.scrollbar_speed, asm.IMM16),
            asm.STA(0x7e354a, asm.LNG_X),
            asm.A8(),

            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame track scroll area remember scrollbar")
        self.remember_scrollbar = space.start_address

    def remember_draw_mod(self):
        src = [
            asm.LDA(self.MENU_NUMBER, asm.IMM8),
            asm.STA(0x0200, asm.ABS),

            asm.JSL(self.remember_cursor + START_ADDRESS_SNES),
            asm.JSL(self.remember_scrollbar + START_ADDRESS_SNES),

            c3.eggers_jump(draw),
            asm.RTS(), 
        ]
        space = Write(Bank.F0, src, "pregame track scroll area remember draw")
        self.remember_draw = space.start_address

    def mod(self):
        self.remember_cursor_mod()
        self.remember_scrollbar_mod()
        self.remember_draw_mod()

        self.initialize_mod()
        self.invoke_mod()
        self.set_line_color_mod()
        self.initialize_line_mod()
        self.draw_character_mod()
        self.draw_line_mod()
