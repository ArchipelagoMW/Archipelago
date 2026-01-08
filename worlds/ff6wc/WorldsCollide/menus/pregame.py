from ..memory.space import START_ADDRESS_SNES, Bank, Write, Reserve, Allocate, Read
from ..instruction import asm as asm
from ..instruction import c3 as c3

class PreGameMenu:
    MENU_NUMBER = 9
    INITIALIZE_PREGAME_MENU_COMMAND = 0x2f
    SUSTAIN_PREGAME_MENU_COMMAND = 0x30

    def __init__(self, pregame_track):
        self.common = pregame_track
        self.invoke_flags_submenu = {}
        self.mod()

    def draw_options_mod(self):
        from ..data import text as text

        text_positions = [
            ("New Game", 0x798f),
            ("Objectives", 0x7a0f),
            ("Flags", 0x7a8f),
            ("Config", 0x7b0f),
        ]

        options = []
        option_space = Allocate(Bank.C3, 41, "pregame options")
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
        space = Write(Bank.C3, src, "pregame draw options")
        self.draw_options = space.start_address

    def initialize_mod(self):
        src = [
            asm.JSL(self.common.initialize + START_ADDRESS_SNES),

            asm.JSR(self.draw_options, asm.ABS),
            asm.JSL(self.common.upload_bg123ab + START_ADDRESS_SNES),

            asm.LDA(self.MENU_NUMBER, asm.IMM8),
            asm.STA(0x0200, asm.ABS),

            asm.LDA(self.SUSTAIN_PREGAME_MENU_COMMAND, asm.IMM8),
            asm.STA(0x27, asm.DIR),         # add sustain pregame menu to queue
            asm.LDA(self.common.FADE_IN_COMMAND, asm.IMM8),
            asm.STA(0x26, asm.DIR),         # add fade in pregame menu to queue
            asm.JMP(0x3541, asm.ABS),       # set brightness and refresh screen
        ]
        # called by C3 JSR jump table
        space = Write(Bank.C3, src, "pregame initialize")
        self.initialize = space.start_address

    def invoke_objectives_menu_mod(self):
        src = [
            asm.JSR(0x6a3c, asm.ABS),   # clear BG3 a (workaround for bizhawk snes9x core bug)
            asm.JMP(self.common.invoke_objectives, asm.ABS),
        ]
        space = Write(Bank.C3, src, "pregame invoke objectives")
        self.invoke_objectives = space.start_address

    def invoke_flags_menu_mod(self):
        src = [
            asm.JSR(0x6a3c, asm.ABS),   # clear BG3 a (workaround for bizhawk snes9x core bug)
            asm.JMP(self.common.invoke_flags, asm.ABS),
        ]
        space = Write(Bank.C3, src, "pregame invoke flags")
        self.invoke_flags = space.start_address

    def invoke_flags_submenu_mod(self, submenu_idx):
        src = [
            asm.JSR(0x6a3c, asm.ABS),   # clear BG3 a (workaround for bizhawk snes9x core bug)
            asm.JMP(self.common.invoke_flags_submenu[submenu_idx], asm.ABS),
        ]
        space = Write(Bank.C3, src, "pregame invoke flag submenu")
        self.invoke_flags_submenu[submenu_idx] = space.start_address

    def sustain_mod(self):
        src = [
            asm.JSR(0x2a21, asm.ABS),       # reset game play time
            asm.LDA(0x01, asm.IMM8),        # a = 0x01 (1st save file slot)
            asm.STA(0x0224, asm.ABS),       # store last viewed save file (start next save/load menu on slot 1)
            asm.STZ(0x021f, asm.ABS),       # no save file for this game
            asm.STZ(0x0205, asm.ABS),       # new game flag
            asm.STZ(self.common.MEMORY_CURSOR_POSITION, asm.ABS),       # shared between pregame/track
            asm.STZ(self.common.MEMORY_SCROLL_AREA_NUMBER, asm.ABS),    # shared between pregame/track
            asm.LDA(0xff, asm.IMM8),        # a = exit menu command
            asm.STA(0x27, asm.DIR),         # add exit menu to queue
            asm.LDA(self.common.FADE_OUT_COMMAND, asm.IMM8),
            asm.STA(0x26, asm.DIR),         # add fade out pregame menu to queue
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "pregame new game option clicked")
        new_game = space.start_address

        src = [
            asm.STZ(0x5f, asm.DIR),         # cursor: battle mode (i.e. first config menu option)
            asm.LDA(0x0d, asm.IMM8),        # a = initialize config menu command
            asm.STA(0x27, asm.DIR),         # add initialize config menu to queue
            asm.LDA(self.common.FADE_OUT_COMMAND, asm.IMM8),
            asm.STA(0x26, asm.DIR),         # add fade out pregame menu to queue
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "pregame config option clicked")
        config = space.start_address

        src = [
            (new_game & 0xffff).to_bytes(2, "little"),
            (self.invoke_objectives & 0xffff).to_bytes(2, "little"),
            (self.invoke_flags & 0xffff).to_bytes(2, "little"),
            (config & 0xffff).to_bytes(2, "little"),
        ]
        space = Write(Bank.C3, src, "pregame option click table")
        options_table = space.start_address

        src = [
            asm.JSR(self.common.refresh_sprites, asm.ABS),

            # if in a scroll area, sustain it
            asm.LDA(0x0200, asm.ABS), 
            asm.CMP(self.common.flags.MENU_NUMBER, asm.IMM8),
            asm.BEQ("SUSTAIN_SCROLL_AREA"),
            asm.CMP(self.common.objectives.MENU_NUMBER, asm.IMM8),
            asm.BEQ("SUSTAIN_SCROLL_AREA"),
        ]

        for submenu_idx in self.common.flags.submenus.keys():
            src += [
                asm.CMP(self.common.flags.submenus[submenu_idx].MENU_NUMBER, asm.IMM8),
                asm.BEQ("SUSTAIN_SCROLL_AREA"),
            ]

        src += [
            asm.JSR(0x072d, asm.ABS),       # handle d-pad
            asm.LDY(self.common.cursor_positions, asm.IMM16),
            asm.JSR(0x0640, asm.ABS),       # update cursor position
            asm.LDA(0x4e, asm.ABS),         # a = cursor row
            asm.STA(self.common.MEMORY_CURSOR_POSITION, asm.ABS),

            asm.LDA(0x08, asm.DIR),         # load buttons pressed this frame
            asm.BIT(0x80, asm.IMM8),        # a pressed?
            asm.BNE("A_PRESSED"),           # branch if so
            asm.RTS(),
            "A_PRESSED",
            asm.TDC(),
            asm.JSR(0x0eb2, asm.ABS),       # click sound
            asm.LDA(0x4b, asm.DIR),         # a = cursor index
            asm.ASL(),                      # a = cursor index * 2 (2 bytes per entry in options table)
            asm.TAX(),                      # x = cursor index * 2
            asm.JMP(options_table, asm.ABS_X_16),

            "SUSTAIN_SCROLL_AREA",
            asm.LDA(0x09, asm.DIR),
            asm.BIT(0x80, asm.IMM8),        # b pressed?
            asm.BNE("EXIT_SCROLL_AREA"),    # branch if so

        ]

        for submenu_id in self.common.flags.submenus.keys():
            src.extend(self.common.get_submenu_src(submenu_id, self.invoke_flags_submenu[submenu_id]))

        src += [
            asm.JMP(self.common.sustain_scroll_area, asm.ABS),

            "EXIT_SCROLL_AREA",
        ]
        src.extend(self.common.get_scroll_area_exit_src(self.MENU_NUMBER, self.invoke_flags))
        
        # Called by C3 JSR jump table
        space = Write(Bank.C3, src, "pregame sustain")
        self.sustain = space.start_address

    def initialize_config_menu_mod(self):
        src = [
            c3.eggers_jump(0x352f),         # displaced code: reset
            asm.STZ(0x4A, asm.DIR),         # displaced code: screen 1st
            asm.LDA(0xc0, asm.IMM8),        # hdma channels 6 and 7
            asm.TRB(0x43, asm.DIR),
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "pregame initialize config menu reset uncondense")
        reset_uncondense = space.start_address

        space = Reserve(0x31c7d, 0x31c81, "pregame initialize config menu reset", asm.NOP())
        space.write(
            asm.JSL(reset_uncondense + START_ADDRESS_SNES),
        )

    def exit_config_menu_mod(self):
        # when exiting config menu, check whether to return to pregame or main menu
        src = [
            asm.LDA(0x0200, asm.ABS),       # load menu number
            asm.CMP(self.MENU_NUMBER, asm.IMM8),
            asm.BNE("MAIN_MENU_EXIT"),      # if not in pregame menu, return to main menu
            asm.JSR(0x6a19, asm.ABS),       # clear BG1 b
            asm.JSR(0x0ea9, asm.ABS),       # play cursor sound
            asm.LDA(self.INITIALIZE_PREGAME_MENU_COMMAND, asm.IMM8),
            asm.STA(0x27, asm.DIR),         # add initialize pregame menu to queue
            asm.STZ(0x26, asm.DIR),         # add generic menu fade out to queue
            asm.RTS(),

            "MAIN_MENU_EXIT",
            Read(0x3230c, 0x32315)          # cursor sound, queue main menu, fade out
        ]
        space = Write(Bank.C3, src, "pregame config menu exit check")
        config_menu_exit_check = space.start_address

        space = Reserve(0x3230c, 0x32315, "config menu exit")
        space.write(
            asm.JMP(config_menu_exit_check, asm.ABS),
        )

    def invoke_load_game_mod(self):
        # modify invoke load menu event command to load pregame menu if no saves instead of starting new game
        space = Reserve(0x3017c, 0x301b1, "load pregame menu if no saves else invoke load menu")
        space.add_label("FIELD_MENU_MAIN_LOOP", 0x301ba)
        space.write(
            Read(0x30181, 0x30193),         # play song: the prelude

            asm.JSR(0x7023, asm.ABS),       # test save file validity
            asm.BCC("INVOKE_PREGAME_MENU"), # branch if no valid saves

            asm.LDA(0xff, asm.IMM8),
            asm.STA(0x0205, asm.ABS),       # not a new game
            asm.LDA(0x20, asm.IMM8),        # a = initialize load menu command
            asm.STA(0x26, asm.DIR),         # add initialize load menu to queue
            asm.BRA("FIELD_MENU_MAIN_LOOP"),

            "INVOKE_PREGAME_MENU",
            asm.LDA(self.INITIALIZE_PREGAME_MENU_COMMAND, asm.IMM8),
            asm.STA(0x26, asm.DIR),         # add initialize pregame menu to queue
            asm.BRA("FIELD_MENU_MAIN_LOOP"),
        )

    def menu_commands_jump_table(self):
        space = Reserve(0x30239, 0x3023a, "menu jump table initialize pregame menu")
        space.write((self.initialize & 0xffff).to_bytes(2, "little"))

        space = Reserve(0x3023b, 0x3023c, "menu jump table sustain pregame menu")
        space.write((self.sustain & 0xffff).to_bytes(2, "little"))

    def mod(self):
        self.draw_options_mod()

        self.initialize_mod()
        self.invoke_objectives_menu_mod()
        self.invoke_flags_menu_mod()
        for submenu_idx in self.common.flags.submenus.keys():
            self.invoke_flags_submenu_mod(submenu_idx)
        self.sustain_mod()

        self.initialize_config_menu_mod()
        self.exit_config_menu_mod()
        self.invoke_load_game_mod()
        self.menu_commands_jump_table()
