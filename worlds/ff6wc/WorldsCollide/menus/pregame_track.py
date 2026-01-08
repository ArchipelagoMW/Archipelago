from ..memory.space import Bank, START_ADDRESS_SNES, Reserve, Allocate, Write, Read
from ..instruction import asm as asm
from ..instruction import c3 as c3
from .. import args as args

from ..menus import pregame_track_scroll_area as scroll_area
from ..menus import objectives as objectives
from ..menus import checks as checks
from ..menus import progress as progress
from ..menus import flags as flags

class PreGameTrack:
    # custom fade commands to load hash sprites while fading so sprites do not suddenly appear/disappear
    FADE_IN_COMMAND = 0x31
    FADE_OUT_COMMAND = 0x32
    WAIT_FOR_FADE_COMMAND = 0x44
    MEMORY_CURSOR_POSITION = 0x24e
    MEMORY_SCROLL_AREA_NUMBER = 0x24f

    def __init__(self, characters):
        self.objectives = objectives.Objectives()
        self.checks = checks.Checks()
        self.progress = progress.Progress()
        self.flags = flags.Flags()

        self.invoke_flags_submenu = {}
        self.characters = characters
        self.mod()

    def get_submenu_src(self, submenu_id, invoke_submenu_addr):
        SUBMENU_LABEL = f"SUBMENU_CHECK{submenu_id}"
        SUBMENU_END_LABEL = f"SUBMENU_CHECK{submenu_id}_END"
        HANDLE_SCROLLING_LABEL = f"HANDLE_SCROLLING_{submenu_id}"
        # get the ASM for sustain_mod that checks whether we are in the flags menu
        # and the A button is clicked to launch a submenu.
        src = [
            # if on the flags menu, check A button press
            asm.LDA(0x200, asm.ABS),
            asm.CMP(self.flags.MENU_NUMBER, asm.IMM8), # in Flags menu?
            asm.BNE(HANDLE_SCROLLING_LABEL),               # branch if not
            asm.LDA(0x08, asm.DIR),
            asm.BIT(0x80, asm.IMM8),        # a pressed?
            asm.BEQ(HANDLE_SCROLLING_LABEL),    # branch if not
        ]
        src += [
            SUBMENU_LABEL,
            asm.LDA(0x4b, asm.DIR),         # a = cursor index
            asm.CMP(submenu_id, asm.IMM8), # is the cursor index = this submenu?
            asm.BNE(SUBMENU_END_LABEL),    # branch if not
            asm.TDC(),
            asm.JSR(0x0eb2, asm.ABS),       # click sound
            asm.JSL(self.exit_scroll_area + START_ADDRESS_SNES), # save current submenu position
            asm.JMP(invoke_submenu_addr, asm.ABS), # load the flags submenu
            SUBMENU_END_LABEL,
        ]
        src += [HANDLE_SCROLLING_LABEL]
        return src

    def get_scroll_area_exit_src(self, destination_menu_number, invoke_flags_addr):
        # Get the ASM for sustain_mod that handles exit from a scroll area, either returning to flags if in
        # a flags submenu or to the given destination_menu_number otherwise.
        src = [
            asm.JSR(0x0EA9, asm.ABS),       # cursor sound
            asm.JSL(self.exit_scroll_area + START_ADDRESS_SNES), # save current submenu position
            asm.LDA(0x0200, asm.ABS),
        ]

        for submenu_idx in self.flags.submenus.keys():
            # if current menu is a flags sub-menu, cause it to return to that, rather than main menu
            src += [
                asm.CMP(self.flags.submenus[submenu_idx].MENU_NUMBER, asm.IMM8), # in Flags submenu?
                asm.BEQ("INVOKE_FLAGS"), # branch if so
            ]

        src += [
            asm.LDA(destination_menu_number, asm.IMM8), # queue up this menu
            asm.STA(0x0200, asm.ABS),
            "RETURN",
            asm.RTS(),

            "INVOKE_FLAGS",
            asm.JMP(invoke_flags_addr, asm.ABS),
        ]

        return src

    def draw_layout_mod(self):
        # layouts: 2 bytes for bg/tilemap/position, 1 byte inner width, 1 byte inner height
        # e.g. $5849 is start of bg2 tilemap a, add 0x42 for top left of visible screen area
        #      0x1c, 0x18 is 28x26 inner widthxheight (i.e. does not include borders)
        src = [
            0x8b, 0x58, # top-left to top-right
            0x1c, 0x07, # 28x7
        ]
        # Note: keep in C3 as this is then used by the C3/0341 subroutine called below
        space = Write(Bank.C3, src, "pregame track top window layout")
        top_window_layout = space.start_address

        src = [
            0xcb, 0x5a, # x/y position
            0x1c, 0x0f, # width/height (excluding border)
        ]
        # Note: keep in C3 as this is then used by the C3/0341 subroutine called below
        space = Write(Bank.C3, src, "pregame track bottom window layout")
        bottom_window_layout = space.start_address

        src = [
            c3.eggers_jump(0x6a15), # clear BG1 A
            c3.eggers_jump(0x6a3c), # clear BG3 A
            asm.LDY(top_window_layout, asm.IMM16),
            c3.eggers_jump(0x0341), # draw top window
            asm.LDY(bottom_window_layout, asm.IMM16),
            c3.eggers_jump(0x0341), # draw bottom window
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, "pregame track draw layout")
        self.draw_layout = space.start_address

    def decrease_line_height_mod(self):
        # shift table for top window
        src = [
            0x1f, 0x00, 0x00, # title
            0x0c, 0x08, 0x00, # new game/objectives
            0x0c, 0x0c, 0x00, # objectives/checks
            0x0c, 0x10, 0x00, # flags/progress
            0x0c, 0x14, 0x00, # config/flags
            0x00,             # end
        ]
        # Keep in C3 as it's used by C3 subroutine called below
        space = Write(Bank.C3, src, "pregame track bg3 shift table")
        bg3_shift_table = space.start_address

        src = [
            Read(0x37e2b, 0x37e34),   # 2 bytes to ppu, dma5, dest = 0x2112, bg3
            asm.LDY(bg3_shift_table, asm.IMM16),
            asm.JMP(0x7e38, asm.ABS), # same bg1 scrolling as item menus
        ]
        space = Write(Bank.C3, src, "pregame track decrease line height")
        self.decrease_line_height = space.start_address

    def draw_labels_mod(self):
        from .. import version as version
        from ..data import text as text

        version_string = "v" + version.__version__.split(' ')[0] # remove substrings such as ' (dev)'
        text_positions = [
            ("FFVI Worlds Collide", 0x78cd),
            (f"{version_string}", 0x7905 - len(version_string) * 2),
        ]

        labels = []
        label_space = Allocate(Bank.C3, 32, "pregame track labels")
        for text_position in text_positions:
            labels.append(label_space.next_address)
            label_space.write(
                text_position[1].to_bytes(2, "little"),         # position
                text.get_bytes(text_position[0], text.TEXT3),   # text
                0x00,                                           # end
            )

        src = [
            c3.eggers_jump(0xc2f7),       # set text color to blue
        ]
        for label in labels:
            src += [
                asm.LDY(label, asm.IMM16),
                c3.eggers_jump(0x02f9),   # draw text
            ]
        src += [
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, "pregame track draw labels")
        self.draw_labels = space.start_address

    def draw_entry_mod(self):
        # add current menu check to item list entry draw method
        # draw current objective/flag/item line
        src = [
            asm.LDA(0x0200, asm.ABS),
            asm.CMP(self.objectives.MENU_NUMBER, asm.IMM8),
            asm.BEQ("DRAW_OBJECTIVE"),
            asm.CMP(self.checks.MENU_NUMBER, asm.IMM8),
            asm.BEQ("DRAW_CHECKS"),
            asm.CMP(self.progress.MENU_NUMBER, asm.IMM8),
            asm.BEQ("DRAW_PROGRESS"),
            asm.CMP(self.flags.MENU_NUMBER, asm.IMM8),
            asm.BEQ("DRAW_FLAG"),
        ]

        for submenu_idx in self.flags.submenus.keys():
            src += [
                asm.CMP(self.flags.submenus[submenu_idx].MENU_NUMBER, asm.IMM8),
                asm.BEQ(f"DRAW_FLAGS_SUBMENU{submenu_idx}"),
            ]

        src += [
            "DRAW_ITEM",
            Read(0x37fa1, 0x37fa3),
            asm.JMP(0x7fa4, asm.ABS),

            "DRAW_OBJECTIVE",
            asm.JMP(self.objectives.draw_line, asm.ABS),

            "DRAW_CHECKS",
            asm.JMP(self.checks.draw_line, asm.ABS),

            "DRAW_PROGRESS",
            asm.JMP(self.progress.draw_line, asm.ABS),

            "DRAW_FLAG",
            asm.JMP(self.flags.draw_line, asm.ABS),
        ]

        for submenu_idx in self.flags.submenus.keys():
            src += [
                f"DRAW_FLAGS_SUBMENU{submenu_idx}",
                asm.JMP(self.flags.submenus[submenu_idx].draw_line, asm.ABS),
            ]

        space = Write(Bank.C3, src, "pregame track draw entry")
        draw_entry = space.start_address

        space = Reserve(0x37fa1, 0x37fa3, "pregame track menu draw entry")
        space.write(
            asm.JMP(draw_entry, asm.ABS),
        )

    def upload_bg123ab_mod(self):
        src = [
            c3.eggers_jump(0x0e28), # upload bg1 a+b
            c3.eggers_jump(0x0e52), # upload bg2 a+b
            c3.eggers_jump(0x0e6e), # upload bg3 a+b
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame track upload bg123ab")
        self.upload_bg123ab = space.start_address

    def initialize_cursor_mod(self):
        src = [
            0x08, 0x1d, # new game   / objectives
            0x08, 0x29, # objectives / checks
            0x08, 0x35, # flags      / progress
            0x08, 0x41, # config     / flags
        ]
        # Keep in C3 -- used by subroutines
        space = Write(Bank.C3, src, "pregame track cursor positions")
        self.cursor_positions = space.start_address

        src = [
            0x80, # wrap vertically
            0x00, # initial column
            0x00, # initial row
            0x01, # columns
            0x04, # rows
        ]
        # Keep in C3 -- used by subroutines
        space = Write(Bank.C3, src, "pregame track navigation data")
        navigation_data = space.start_address

        src = [
            asm.LDY(navigation_data, asm.IMM16),
            c3.eggers_jump(0x05fe),   # load navigation data
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, "pregame track update navigation data")
        self.update_navigation_data = space.start_address

        src = [
            asm.LDA(self.MEMORY_CURSOR_POSITION, asm.ABS),
            asm.STA(0x4e, asm.DIR),     # cursor row = saved row
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, "pregame track remember cursor position")
        self.remember_cursor_position = space.start_address

        src = [
            asm.LDY(self.cursor_positions, asm.IMM16),
            c3.eggers_jump(0x0640),   # update cursor position
            c3.eggers_jump(0x07b0),   # add cursor to animation queue
            asm.RTS(),                
        ]
        space = Write(Bank.F0, src, "pregame track update cursor position")
        self.update_cursor_position = space.start_address

        src = [
            asm.JSR(self.update_navigation_data, asm.ABS),
            asm.LDA(0x1d4e, asm.ABS), # load game config
            asm.AND(0x40, asm.IMM8),  # cursor memory enabled?
            asm.BEQ("UPDATE_CURSOR_POSITION"),    # branch if not
            asm.JSR(self.remember_cursor_position, asm.ABS),

            "UPDATE_CURSOR_POSITION",
            asm.JSR(self.update_cursor_position, asm.ABS),
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, "pregame track initialize cursor")
        self.initialize_cursor = space.start_address

    def initialize_scroll_area_mod(self):
        rows = scroll_area.HEIGHT
        cols = 1

        src = []
        if self.objectives.initialize is not None:
            src += [
                asm.JSL(START_ADDRESS_SNES + self.objectives.initialize),
            ]
        if self.checks.initialize is not None:
            src += [
                asm.JSL(START_ADDRESS_SNES + self.checks.initialize),
            ]
        if self.progress.initialize is not None:
            src += [
                asm.JSL(START_ADDRESS_SNES + self.progress.initialize),
            ]
        if self.flags.initialize is not None:
            src+= [
                asm.JSL(START_ADDRESS_SNES + self.flags.initialize),
            ]
        for submenu_idx in self.flags.submenus.keys():
            if self.flags.submenus[submenu_idx].initialize is not None:
                src+= [
                    asm.JSL(START_ADDRESS_SNES + self.flags.submenus[submenu_idx].initialize),
                ]

        src += [
            asm.STZ(0x4a, asm.DIR),     # index of first row displayed
            asm.STZ(0x50, asm.DIR),     # cursor index [0, len(lines))

            asm.LDA(rows, asm.IMM8),
            asm.STA(0x5a, asm.DIR),
            asm.LDA(cols, asm.IMM8),
            asm.STA(0x5b, asm.DIR),
            asm.LDA(self.objectives.number_excess_lines, asm.IMM8),
            asm.STA(0x5c, asm.DIR),

            c3.eggers_jump(0x07b0),   # queue scrollbar animation
            c3.eggers_jump(0x091f),   # create scrollbar
            asm.A16(),
            asm.LDA(self.objectives.scrollbar_speed, asm.IMM16),
            asm.STA(0x7e354a, asm.LNG_X),
            asm.LDA(scroll_area.SCROLLBAR_INITIAL_Y, asm.IMM16),
            asm.STA(0x7e34ca, asm.LNG_X),
            asm.A8(),

            # initialize to objectives menu
            asm.LDA(self.objectives.MENU_NUMBER, asm.IMM8),
            asm.STA(0x0200, asm.ABS),
            asm.STZ(scroll_area.CURRENT_TYPE_ADDR, asm.ABS),

            asm.LDA(0x1d4e, asm.ABS),           # load game config
            asm.AND(0x40, asm.IMM8),            # cursor memory enabled?
            asm.BNE("REMEMBER_SCROLL_AREA"),    # branch if so
            c3.eggers_jump(scroll_area.draw),
            asm.RTS(),

            "REMEMBER_SCROLL_AREA",
            asm.LDA(self.MEMORY_SCROLL_AREA_NUMBER, asm.ABS),

            asm.CMP(self.checks.MENU_NUMBER, asm.IMM8),
            asm.BEQ("REMEMBER_CHECKS"),
            asm.CMP(self.progress.MENU_NUMBER, asm.IMM8),
            asm.BEQ("REMEMBER_PROGRESS"),
            asm.CMP(self.flags.MENU_NUMBER, asm.IMM8),
            asm.BEQ("REMEMBER_FLAGS"),
        ]

        for submenu_idx in self.flags.submenus.keys():
            src += [
                asm.CMP(self.flags.submenus[submenu_idx].MENU_NUMBER, asm.IMM8),
                asm.BEQ(f"REMEMBER_FLAGS_SUBMENU{submenu_idx}"),
            ]

        src += [
            "REMEMBER_OBJECTIVES",
            asm.LDA(self.objectives.MENU_NUMBER, asm.IMM8),     # load objectives menu number
            asm.STA(self.MEMORY_SCROLL_AREA_NUMBER, asm.ABS),   # save in case no scroll area memory
            asm.JMP(self.objectives.remember_draw, asm.ABS),

            "REMEMBER_CHECKS",
            asm.JMP(self.checks.remember_draw, asm.ABS),

            "REMEMBER_PROGRESS",
            asm.JMP(self.progress.remember_draw, asm.ABS),

            "REMEMBER_FLAGS",
            asm.JMP(self.flags.remember_draw, asm.ABS),
        ]

        for submenu_idx in self.flags.submenus.keys():
            src += [
                f"REMEMBER_FLAGS_SUBMENU{submenu_idx}",
                asm.JMP(self.flags.submenus[submenu_idx].remember_draw, asm.ABS),
            ]

        space = Write(Bank.F0, src, "pregame track initialize scroll area")
        self.initialize_scroll_area = space.start_address

    def InvokeScrollArea(self, scroll_area_menu):
        return [
            asm.LDA(scroll_area_menu.MENU_NUMBER, asm.IMM8),
            asm.STA(self.MEMORY_SCROLL_AREA_NUMBER, asm.ABS),
            asm.JSR(scroll_area_menu.invoke, asm.ABS),
            asm.JSR(self.refresh_sprites, asm.ABS), # JSL
            asm.RTS(),
        ]

    def invoke_objectives_mod(self):
        src = [
            self.InvokeScrollArea(self.objectives),
        ]
        space = Write(Bank.C3, src, "pregame track invoke objectives")
        self.invoke_objectives = space.start_address

    def invoke_checks_mod(self):
        src = [
            self.InvokeScrollArea(self.checks),
        ]
        space = Write(Bank.C3, src, "pregame track invoke checks")
        self.invoke_checks = space.start_address

    def invoke_progress_mod(self):
        src = [
            self.InvokeScrollArea(self.progress),
        ]
        space = Write(Bank.C3, src, "pregame track invoke progress")
        self.invoke_progress = space.start_address

    def invoke_flags_mod(self):
        src = [
            self.InvokeScrollArea(self.flags),
        ]
        space = Write(Bank.C3, src, "pregame track invoke flags")
        self.invoke_flags = space.start_address

    def invoke_flags_submenu_mod(self, submenu_idx):
        src = [
            self.InvokeScrollArea(self.flags.submenus[submenu_idx]),
        ]
        space = Write(Bank.C3, src, "pregame track invoke flags submenu")
        self.invoke_flags_submenu[submenu_idx] = space.start_address

    def sustain_scroll_area_mod(self):
        # Called via JMP
        src = [
            asm.TDC(),
            asm.STA(0x2a, asm.DIR),
            asm.JSR(0x0efd, asm.ABS),   # upload bg1 a
            asm.JSR(0x1f64, asm.ABS),   # handle l/r button scrolling
            asm.BGE("RETURN"),          # was l/r button pressed/handled?
            asm.JSR(0x7d22, asm.ABS),   # handle d-pad scrolling

            "RETURN",
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "pregame track sustain scroll area")
        self.sustain_scroll_area = space.start_address

    def exit_scroll_area_mod(self):
        src = [
            # cursor position (reset/memory)
            asm.LDA(0x1d4e, asm.ABS),               # load game config
            asm.AND(0x40, asm.IMM8),                # cursor memory enabled?
            asm.BEQ("UPDATE_PREGAME_TRACK_CURSOR"), # branch if not

            "SAVE_SCROLL_AREA_POSITION",
            asm.LDA(0x0200, asm.ABS),     # a = number of menu being exited
            asm.ASL(),
            asm.CLC(),
            asm.ADC(0x0200, asm.ABS),     # a = a * 3 (3 bytes for cursor and page position per menu)
            asm.A16(),
            asm.AND(0x00ff, asm.IMM16),   # a = exited menu number * 3
            asm.TAY(),
            asm.LDA(0x4f, asm.DIR),       # a = cursor position
            asm.STA(scroll_area.MEMORY_CURSOR_POSITIONS_START_ADDR, asm.ABS_Y),
            asm.A8(),
            asm.LDA(0x4a, asm.DIR),       # a = index of first row displayed (page position)
            asm.STA(scroll_area.MEMORY_PAGE_POSITIONS_START_ADDR, asm.ABS_Y),

            "UPDATE_PREGAME_TRACK_CURSOR",
            asm.JSR(self.update_navigation_data, asm.ABS), 
            asm.JSR(self.remember_cursor_position, asm.ABS), 
            asm.JSR(self.update_cursor_position, asm.ABS),

            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame track exit scroll area")
        self.exit_scroll_area = space.start_address

    def load_sprite_palettes_mod(self):
        # palettes can be customized but only require a small amount of space (32 bytes)
        # copy the original palettes here so the sprite hash is not affected by custom palette changes
        palette_size = 16 * 2               # 16 colors, 2 bytes each
        palettes_size = palette_size * 6    # 6 palettes * 16 colors * 2 bytes
        palette_space = Allocate(Bank.F0, palettes_size, "pregame track palettes")

        palette0_address = palette_space.next_address
        palette_space.write(
            0x42, 0x08, 0x63, 0x0c, 0xff, 0x6f, 0x60, 0x3c,
            0xd8, 0x2a, 0x4f, 0x05, 0x1f, 0x47, 0xb9, 0x1d,
            0x53, 0x27, 0xc6, 0x19, 0x90, 0x6a, 0x4b, 0x45,
            0xe6, 0x1c, 0x46, 0x2d, 0x52, 0x3a, 0x5a, 0x4f,
        )

        palette1_address = palette_space.next_address
        palette_space.write(
            0x00, 0x38, 0x63, 0x0c, 0xff, 0x6f, 0x89, 0x00,
            0x94, 0x3a, 0x2a, 0x1d, 0xff, 0x3e, 0xf9, 0x21,
            0xf3, 0x2d, 0x0f, 0x15, 0x8c, 0x45, 0xe4, 0x30,
            0x95, 0x18, 0xbc, 0x35, 0x5a, 0x4f, 0xff, 0x67,
        )

        palette2_address = palette_space.next_address
        palette_space.write(
            0x00, 0x38, 0x63, 0x0c, 0xff, 0x6f, 0xc0, 0x18,
            0xb0, 0x42, 0x45, 0x1d, 0x1f, 0x47, 0xb9, 0x1d,
            0x57, 0x02, 0x12, 0x00, 0x19, 0x7e, 0x70, 0x6d,
            0xb4, 0x10, 0x1e, 0x2a, 0xee, 0x00, 0xf2, 0x29,
        )

        palette3_address = palette_space.next_address
        palette_space.write(
            0x00, 0x00, 0x63, 0x0c, 0xff, 0x6f, 0x02, 0x0d,
            0xd8, 0x42, 0x4f, 0x21, 0x3f, 0x3f, 0x79, 0x2a,
            0xda, 0x02, 0x72, 0x01, 0x17, 0x00, 0xe0, 0x01,
            0x27, 0x39, 0xce, 0x7d, 0xb7, 0x32, 0xff, 0x63,
        )

        palette4_address = palette_space.next_address
        palette_space.write(
            0x00, 0x38, 0x63, 0x0c, 0xff, 0x6f, 0xa8, 0x40,
            0xd3, 0x52, 0x08, 0x21, 0x3f, 0x43, 0xf8, 0x31,
            0x26, 0x29, 0xc6, 0x18, 0x72, 0x01, 0xcb, 0x5d,
            0xc6, 0x19, 0x53, 0x27, 0x2e, 0x1d, 0x96, 0x3a,
        )

        palette5_address = palette_space.next_address
        palette_space.write(
            0x29, 0x2d, 0x63, 0x0c, 0xff, 0x6f, 0xa0, 0x44,
            0xff, 0x7f, 0x93, 0x66, 0xff, 0x7f, 0x93, 0x66,
            0x5f, 0x5e, 0xff, 0x38, 0xd1, 0x45, 0x53, 0x1d,
            0x51, 0x65, 0xaa, 0x58, 0xb9, 0x02, 0x9f, 0x33,
        )

        palettes = palette_space.start_address

        # normally in menus palette 0 is loaded for config (is it used anywhere?), palette 1 is grayscale
        # and palettes 2-7 correspond to sprite palettes 0-5
        # npc sprites are not in vanilla menus so some colors they use are overwritten
        # the last 4 colors of palette 6 are overwritten for status effect icons (poison/float/...)
        # the last 4 colors of palette 7 are overwritten for cursor/arrow colors
        # pregame menu does not need palette 0 or grayscale but does need full sprite palettes and cursor/arrow colors
        # load the original sprite palettes into 0-5 so they do not conflict with icon/cursor/arrow colors in 6 and 7
        # this leaves the first 12 colors of palettes 6 and 7 available if needed in the future

        src = [
            asm.LDX(0x00, asm.DIR),             # start at color 0
            asm.LDA(0x80, asm.IMM8),
            asm.STA(0x2121, asm.ABS),           # write starting at cgram $100

            "LOAD_COLOR_LOOP_START",
            asm.A16(),
            asm.LDA(palettes + START_ADDRESS_SNES, asm.LNG_X),       # load current color
            asm.STA(0x7e3149, asm.LNG_X),       # store in ram
            asm.A8(),
            asm.STA(0x2122, asm.ABS),           # store low byte in cgram
            asm.XBA(),                          # a = high byte
            asm.STA(0x2122, asm.ABS),           # store high byte in cgram
            asm.INX(),
            asm.INX(),
            asm.CPX(palettes_size, asm.IMM16),  # all colors loaded?
            asm.BNE("LOAD_COLOR_LOOP_START"),   # loop if not

            c3.eggers_jump(0x6ce9),           # load single pose for characters terra, locke, ..., ghost, kefka
            asm.RTS(),
        ]
        space = Write(Bank.F0, src, "pregame track load sprite palettes")
        self.load_sprite_palettes = space.start_address

    def refresh_sprites_mod(self):
        from ..sprite_hash import HASH_CHARACTERS

        x_start = 0x9d
        x_spacing = 0x16

        src = []
        for index in range(len(args.sprite_hash)):
            src += [
                x_start + x_spacing * index,
            ]
        space = Write(Bank.F0, src, "pregame track refresh sprites x positions")
        x_positions_address = space.start_address

        y_start = 0x32 # higher is lower on screen

        src = []
        for entry in args.sprite_hash:
            src += [
                y_start + entry.y_offset * 8,
            ]
        space = Write(Bank.F0, src, "pregame track refresh sprites y positions")
        y_positions_address = space.start_address

        # if not zero, these palettes override sprite oam palettes (at 0xc31324)
        src = [
            0x00, 0x00, 0x00, 0x00,
        ]
        space = Write(Bank.F0, src, "pregame track refresh sprites palettes address")
        palettes_address = space.start_address

        src = [
            HASH_CHARACTERS,
        ]
        space = Write(Bank.F0, src, "pregame track refresh sprites characters address")
        characters_address = space.start_address

        # modified version of c31903 used for save/load menus
        src = [
            asm.LDX(0x00, asm.DIR),

            "SPRITE_LOOP_START",
            asm.PHX(),                      # push current sprite index
            asm.PHX(),                      # push current sprite index
            asm.LDA(0x03, asm.IMM8),        # animation queue index (check 3, then 4, ... until find available)
            asm.LDY(0x19c7, asm.IMM16),     # function address to set animation timer and oam data
            asm.JSR(0x1173, asm.ABS),       # add to animation queue
            asm.TXY(),                      # y = animation queue index
            asm.PLX(),                      # x = current sprite index
            asm.PHB(),                      # push data bank register (0x00)
            asm.LDA(0x7e, asm.IMM8),        # a = desired data bank register
            asm.PHA(),                      # push 0x7e on stack
            asm.PLB(),                      # a = desired data bank register
            asm.LDA(palettes_address + START_ADDRESS_SNES, asm.LNG_X),
            asm.STA(0x3749, asm.ABS_Y),     # store palette for current sprite index
            asm.LDA(0xd8, asm.IMM8),
            asm.STA(0x35ca, asm.ABS_Y),     # store sprite tile data bank
            asm.TDC(),                      # clear a register
            asm.LDA(x_positions_address + START_ADDRESS_SNES, asm.LNG_X),
            asm.STA(0x33ca, asm.ABS_Y),     # store x position for current sprite index
            asm.LDA(y_positions_address + START_ADDRESS_SNES, asm.LNG_X),
            asm.STA(0x344a, asm.ABS_Y),     # store y position for current sprite index
            asm.LDA(characters_address + START_ADDRESS_SNES, asm.LNG_X),
            asm.A16(),
            asm.ASL(),                      # a = character index * 2
            asm.TAX(),                      # x = character index * 2
            asm.LDA(0xd8e917, asm.LNG_X),   # a = address of pointer to oam data for character
            asm.STA(0x32c9, asm.ABS_Y),     # store address of pointer to oam data for character
            asm.A8(),
            asm.PLB(),                      # data bank register = 0x00
            asm.PLX(),                      # x = current sprite index
            asm.INX(),                      # increment current sprite index
            asm.CPX(0x0004, asm.IMM16),     # finished all 4 sprites?
            asm.BNE("SPRITE_LOOP_START"),   # branch if not

            asm.RTS(),
        ]
        # Keep in C3 -- called by JMP methods that are called from C3 JSR jump table
        space = Write(Bank.C3, src, "pregame track refresh sprites")
        self.refresh_sprites = space.start_address

    def hash_characters(self):
        # many npc sprites do not have tiles for an idle left-facing pose, use the middle walking-left pose instead
        # these relative tile pointers are loaded at c36d05 and c36d25
        space = Reserve(0xff8df, 0xff8e4, "menu sprite tile pointers")
        space.write(0xc0, 0x03, # 0x3c0 / 0x20 = 0x1e (tiles 30 and 31) for top row
                    0x00, 0x04, # 0x400 / 0x20 = 0x20 (tiles 32 and 33) for middle row
                    0x40, 0x04) # 0x420 / 0x20 = 0x22 (tiles 34 and 35) for bottom row

        # set sprites/palettes for HASH_CHARACTERS
        from ..sprite_hash import HASH_CHARACTERS
        for index, character in enumerate(HASH_CHARACTERS):
            sprite_address = args.sprite_hash[index].sprite_address
            palette = args.sprite_hash[index].palette

            self.characters.menu_character_sprites.set_sprite_address(character, sprite_address)
            self.characters.menu_character_sprites.standing_sprites[character].set_palette(palette)

    def initialize_mod(self):
        menu_flags = 0x82 # 0x02 = enable main cursor | 0x80 = scrollbar animation index

        # bits 0-1 set size (0 = 32x32, 1 = 64x32, 2 = 32x64, 3 = 64x64) and bits 2-7 set tilemap address
        bg1_size_position = 0x01

        src = [
            asm.LDA(menu_flags, asm.IMM8),
            asm.STA(0x46, asm.DIR),

            c3.eggers_jump(0x352f),               # reset oam/queue/etc.. blank screen
            c3.eggers_jump(0x6904),               # reset BG1-3 x/y
            asm.LDA(bg1_size_position, asm.IMM8),   # a = BG1 size and position
            asm.STA(0x2107, asm.ABS),               # BG1 64x32 at $0000

            asm.LDA(0x1c, asm.IMM8),    # active hdma channels bitmask
            asm.STA(0x43, asm.DIR),     # set active hdma channels

            asm.JSR(self.draw_layout, asm.ABS),
            c3.eggers_jump(self.decrease_line_height),
            asm.JSR(self.initialize_scroll_area, asm.ABS),

            c3.eggers_jump(0x6a19),   # clear BG1 b
            c3.eggers_jump(0x6a3c),   # clear BG3 a
            c3.eggers_jump(0x6a41),   # clear BG3 b 
            c3.eggers_jump(0x6a46),   # clear BG3 c
            c3.eggers_jump(0x6a4b),   # clear BG3 d

            asm.JSR(self.draw_labels, asm.ABS),

            c3.eggers_jump(0x6ca5),   # load cursor colors, skip loading status icon colors at 0x6c84
            asm.JSR(self.load_sprite_palettes, asm.ABS),

            asm.JSR(self.initialize_cursor, asm.ABS),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame track initialize")
        self.initialize = space.start_address

    def wait_for_fade_mod(self):
        src = [
            asm.LDY(0x20, asm.DIR),         # timer, frames left
            asm.BNE("LOAD_SPRITE_DATA"),    # branch if timer not up
            asm.LDA(0x27, asm.DIR),         # load next menu queue entry
            asm.STA(0x26, asm.DIR),         # store as next in queue
            "LOAD_SPRITE_DATA",
            asm.JMP(self.refresh_sprites, asm.ABS),
        ]
        # Keep in C3 -- called by C3 JSR jump table
        space = Write(Bank.C3, src, "pregame track wait for fade")
        self.wait_for_fade = space.start_address

    def fade_in_mod(self):
        src = [
            asm.JSR(0x3056, asm.ABS),       # add generic menu fade in to queue
            asm.LDY(0x0008, asm.IMM16),     # 8 frames
            asm.STY(0x20, asm.DIR),         # fade timer
            asm.LDA(self.WAIT_FOR_FADE_COMMAND, asm.IMM8),
            asm.STA(0x26, asm.DIR),         # add wait for fade to queue
            asm.JMP(self.refresh_sprites, asm.ABS),
        ]
         # Keep in C3 -- called by C3 JSR jump table
        space = Write(Bank.C3, src, "pregame track fade in")
        self.fade_in = space.start_address

    def fade_out_mod(self):
        src = [
            asm.JSR(0x304f, asm.ABS),     # add generic menu fade out to queue
            asm.LDY(0x0008, asm.IMM16),   # 8 frames
            asm.STY(0x20, asm.DIR),       # fade timer
            asm.LDA(self.WAIT_FOR_FADE_COMMAND, asm.IMM8),
            asm.STA(0x26, asm.DIR),       # add wait for fade to queue
            asm.JMP(self.refresh_sprites, asm.ABS),   # refresh sprites
        ]
         # Keep in C3 -- called by C3 JSR jump table
        space = Write(Bank.C3, src, "pregame track fade out")
        self.fade_out = space.start_address

    def menu_commands_jump_table(self):
        space = Reserve(0x3023d, 0x3023e, "pregame track menu commands jump table fade in")
        space.write((self.fade_in & 0xffff).to_bytes(2, "little"))

        space = Reserve(0x3023f, 0x30240, "pregame track menu commands jump table fade out")
        space.write((self.fade_out & 0xffff).to_bytes(2, "little"))

        space = Reserve(0x30263, 0x30264, "pregame track menu commands jump table wait for fade")
        space.write((self.wait_for_fade & 0xffff).to_bytes(2, "little"))

    def mod(self):
        self.draw_layout_mod()
        self.decrease_line_height_mod()
        self.draw_labels_mod()
        self.draw_entry_mod()
        self.upload_bg123ab_mod()
        self.initialize_cursor_mod()

        self.load_sprite_palettes_mod()
        self.refresh_sprites_mod()
        self.hash_characters()

        self.initialize_scroll_area_mod()
        self.invoke_objectives_mod()
        self.invoke_checks_mod()
        self.invoke_progress_mod()
        self.invoke_flags_mod()
        for submenu_idx in self.flags.submenus.keys():
            self.invoke_flags_submenu_mod(submenu_idx)
        self.exit_scroll_area_mod()
        self.sustain_scroll_area_mod()

        self.initialize_mod()
        self.wait_for_fade_mod()
        self.fade_in_mod()
        self.fade_out_mod()
        self.menu_commands_jump_table()
