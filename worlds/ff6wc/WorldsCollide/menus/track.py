from ..memory.space import START_ADDRESS_SNES, Bank, Write, Reserve, Allocate, Read
from ..instruction import asm as asm
from ..instruction import c3 as c3

class TrackMenu:
    MENU_NUMBER = 10
    INITIALIZE_TRACK_MENU_COMMAND = 0x45
    SUSTAIN_TRACK_MENU_COMMAND = 0x46

    def __init__(self, pregame_track):
        self.common = pregame_track
        self.mod()

    def time_steps_gp_layout_mod(self):
        space = Reserve(0x331bf, 0x331c2, "time submenu layout")
        space.clear(0x00)   # clear time submenu layout entry

        space = Reserve(0x33175, 0x3317a, "draw time submenu", asm.NOP())

        # increase steps/gp submenu size to allow time to fit
        space = Reserve(0x331c3, 0x331c6, "steps/gp submenu layout")
        space.write(
            0xf5, 0x5c,     # move y-coordinate higher
            0x07, 0x07,     # increase height
        )

        # shift time down into steps/gp submenu
        space = Reserve(0x33804, 0x33805, "'Time' text position")
        space.write(
            0x37, 0x7d,
        )
        space = Reserve(0x332a0, 0x332a1, "time hours value text position")
        space.write(
            0x7b, 0x7d,
        )
        space = Reserve(0x332ac, 0x332ad, "time minutes value text position")
        space.write(
            0x81, 0x7d,
        )
        space = Reserve(0x3380b, 0x3380c, "time colon character position")
        space.write(
            0x7f, 0x7d,
        )

        # shift steps down
        space = Reserve(0x3380f, 0x33810, "'Steps' text position")
        space.write(
            0xf7, 0x7d,
        )
        space = Reserve(0x33253, 0x33254, "steps value text position")
        space.write(
            0x37, 0x7e,
        )

    def main_menu_mod(self):
        from ..data import text as text

        # increase main menu options submenu size to allow track to fit
        space = Reserve(0x331bb, 0x331be, "main menu options submenu layout")
        space.write(
            0xb7, 0x58,
            0x06, 0x0f,
        )

        # shift config/save down
        space = Reserve(0x337f4, 0x337f5, "'Config' option text position")
        space.write(
            0x39, 0x7c,
        )
        space = Reserve(0x337fd, 0x337fe, "'Save' option text position")
        space.write(
            0xb9, 0x7c,
        )
        space = Reserve(0x336da, 0x336df, "main menu save entry offset")
        space.write(
            0x0f, 0x0a, 0x00,   # save
            0x07, 0x08, 0x00,   # empty
        )

        # draw "Track" in main menu options
        options = []
        option_space = Allocate(Bank.C3, 25, "track main menu options")

        options.append(option_space.next_address)
        option_space.write(
            Read(0x337db, 0x337e2)  # equip
        )
        options.append(option_space.next_address)
        option_space.write(
            0xb9, 0x7b,                             # position
            text.get_bytes("Track", text.TEXT3),    # text
            0x00,                                   # end
        )
        options.append(option_space.next_address)
        option_space.write(
            Read(0x337f4, 0x337fc)  # config
        )

        src = []
        for option in options:
            src += [
                (option & 0xffff).to_bytes(2, "little"),
            ]
        space = Write(Bank.C3, src, "track main menu option table")
        option_table = space.start_address

        space = Reserve(0x33204, 0x33209, "draw equip, track, config menu options", asm.NOP())
        space.write(
            asm.LDX(option_table, asm.IMM16),       # x = address of pointers to positioned text
            asm.LDY(len(options) * 2, asm.IMM16),   # y = number of strings to draw * pointer size
        )

        # cursor positions
        src = [
            Read(0x32f8a, 0x32f93),     # item/skills/equip/relic/status

            0xaf, 0x5d,                 # tracker
            0xaf, 0x6c,                 # config
            0xaf, 0x7b,                 # save
        ]
        space = Write(Bank.C3, src, "track main menu cursor positions")
        cursor_positions = space.start_address

        space = Reserve(0x32f66, 0x32f67, "main menu initialize cursor position")
        space.write(
            (cursor_positions & 0xffff).to_bytes(2, "little"),
        )
        space = Reserve(0x32f77, 0x32f78, "main menu update cursor position")
        space.write(
            (cursor_positions & 0xffff).to_bytes(2, "little"),
        )

        space = Reserve(0x32f89, 0x32f89, "main menu number of rows")
        space.write(8)

    def draw_options_mod(self):
        from ..data import text as text

        text_positions = [
            ("Objectives", 0x798f),
            ("Checks", 0x7a0f),
            ("Progress", 0x7a8f),
            ("Flags", 0x7b0f),
        ]

        options = []
        option_space = Allocate(Bank.C3, 41, "track options")
        for text_position in text_positions:
            options.append(option_space.next_address)
            option_space.write(
                text_position[1].to_bytes(2, "little"),         # position
                text.get_bytes(text_position[0], text.TEXT3),   # text
                0x00,                                           # end
            )

        src = [
            asm.JSR(0xc2f2, asm.ABS),       # set text color to user config choice
        ]
        for option in options:
            src += [
                asm.LDY(option, asm.IMM16),
                asm.JSR(0x02f9, asm.ABS),   # draw text
            ]
        src += [
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "track draw options")
        self.draw_options = space.start_address

    def invoke_mod(self):
        src = [
            asm.JSR(0x0eb2, asm.ABS),   # click sound
            asm.STZ(0x26, asm.DIR),     # add fade out to queue
            asm.LDA(self.INITIALIZE_TRACK_MENU_COMMAND, asm.IMM8),
            asm.STA(0x27, asm.DIR),     # add initialize track menu to queue
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "track invoke")
        invoke = space.start_address

        src = [
            Read(0x32e6c, 0x32e75),     # item/skills/equip/relic/status
            (invoke & 0xffff).to_bytes(2, "little"),
            Read(0x32e76, 0x32e79),     # config/save
        ]
        space = Write(Bank.C3, src, "track invoke option table")
        option_table = space.start_address

        space = Reserve(0x32e6a, 0x32e6b, "track main menu options jump table address")
        space.write(
            (option_table & 0xffff).to_bytes(2, "little"),
        )

    def initialize_mod(self):
        src = [
            asm.JSL(self.common.initialize + START_ADDRESS_SNES),

            asm.JSR(self.draw_options, asm.ABS),
            asm.JSL(self.common.upload_bg123ab + START_ADDRESS_SNES),

            asm.LDA(self.MENU_NUMBER, asm.IMM8),
            asm.STA(0x0200, asm.ABS),

            asm.LDA(self.SUSTAIN_TRACK_MENU_COMMAND, asm.IMM8),
            asm.STA(0x27, asm.DIR),     # add sustain track menu to queue
            asm.LDA(self.common.FADE_IN_COMMAND, asm.IMM8),
            asm.STA(0x26, asm.DIR),     # add fade in menu to queue
            asm.JMP(0x3541, asm.ABS),   # set brightness and refresh screen
        ]
        # called by C3 JSR jump table
        space = Write(Bank.C3, src, "track initialize")
        self.initialize = space.start_address

    def sustain_mod(self):
        src = [
            (self.common.invoke_objectives & 0xffff).to_bytes(2, "little"),
            (self.common.invoke_checks & 0xffff).to_bytes(2, "little"),
            (self.common.invoke_progress & 0xffff).to_bytes(2, "little"),
            (self.common.invoke_flags & 0xffff).to_bytes(2, "little"),
        ]
        space = Write(Bank.C3, src, "track option click table")
        options_table = space.start_address

        src = [
            asm.JSR(self.common.refresh_sprites, asm.ABS),

            # if in a scroll-area menu, sustain the scroll area
            asm.LDA(0x0200, asm.ABS), 
            asm.CMP(self.common.objectives.MENU_NUMBER, asm.IMM8),
            asm.BEQ("SUSTAIN_SCROLL_AREA"),
            asm.CMP(self.common.checks.MENU_NUMBER, asm.IMM8),
            asm.BEQ("SUSTAIN_SCROLL_AREA"),
            asm.CMP(self.common.progress.MENU_NUMBER, asm.IMM8),
            asm.BEQ("SUSTAIN_SCROLL_AREA"),
            asm.CMP(self.common.flags.MENU_NUMBER, asm.IMM8),
            asm.BEQ("SUSTAIN_SCROLL_AREA"),
        ]

        for submenu_idx in self.common.flags.submenus.keys():
            src += [
                asm.CMP(self.common.flags.submenus[submenu_idx].MENU_NUMBER, asm.IMM8),
                asm.BEQ("SUSTAIN_SCROLL_AREA"),
            ]

        src += [
            asm.JSR(0x072d, asm.ABS),   # handle d-pad
            asm.LDY(self.common.cursor_positions, asm.IMM16),
            asm.JSR(0x0640, asm.ABS),   # update cursor position
            asm.LDA(0x4e, asm.DIR),     # a = cursor row
            asm.STA(self.common.MEMORY_CURSOR_POSITION, asm.ABS),

            asm.LDA(0x08, asm.DIR),     # load buttons pressed this frame
            asm.BIT(0x80, asm.IMM8),    # a pressed?
            asm.BEQ("HANDLE_B"),        # branch if not

            asm.TDC(),
            asm.JSR(0x0eb2, asm.ABS),   # click sound
            asm.LDA(0x4b, asm.DIR),     # a = cursor index
            asm.ASL(),                  # a = cursor index * 2 (2 bytes per entry in options table)
            asm.TAX(),                  # x = cursor index * 2
            asm.JMP(options_table, asm.ABS_X_16),

            "HANDLE_B",
            asm.LDA(0x09, asm.DIR),     # load buttons pressed this frame
            asm.BIT(0x80, asm.IMM8),    # b pressed?
            asm.BNE("B_PRESSED"),       # return if not
            asm.RTS(),
            "B_PRESSED",
            asm.LDA(0x04, asm.IMM8),    # a = initialize main menu command
            asm.STA(0x27, asm.DIR),     # add initialize main menu to queue
            asm.LDA(self.common.FADE_OUT_COMMAND, asm.IMM8),
            asm.STA(0x26, asm.DIR),     # add fade out menu to queue
            asm.RTS(),

            "SUSTAIN_SCROLL_AREA",
            asm.LDA(0x09, asm.DIR),
            asm.BIT(0x80, asm.IMM8),     # b pressed?
            asm.BNE("EXIT_SCROLL_AREA"), # branch if so
        ]

        for submenu_idx in self.common.flags.submenus.keys():
            src.extend(self.common.get_submenu_src(submenu_idx, self.common.invoke_flags_submenu[submenu_idx]))

        src += [
            asm.JMP(self.common.sustain_scroll_area, asm.ABS),

            "EXIT_SCROLL_AREA",
        ]

        src.extend(self.common.get_scroll_area_exit_src(self.MENU_NUMBER, self.common.invoke_flags))

        # Called by C3 JSR jump table
        space = Write(Bank.C3, src, "track sustain")
        self.sustain = space.start_address

    def menu_commands_jump_table(self):
        space = Reserve(0x30265, 0x30266, "menu jump table initialize track menu")
        space.write((self.initialize & 0xffff).to_bytes(2, "little"))

        space = Reserve(0x30267, 0x30268, "menu jump table sustain track menu")
        space.write((self.sustain & 0xffff).to_bytes(2, "little"))

    def mod(self):
        self.time_steps_gp_layout_mod()
        self.main_menu_mod()

        self.draw_options_mod()
        self.invoke_mod()
        self.initialize_mod()
        self.sustain_mod()

        self.menu_commands_jump_table()
