from ..memory.space import Bank, Write
from ..instruction import asm as asm
from ..instruction import f0 as f0
from .. import args as args

from .. import objectives as objectives
from ..menus import pregame_track_scroll_area as scroll_area

class Objectives(scroll_area.ScrollArea):
    MENU_NUMBER = 11

    def __init__(self):
        # values in range [special_characters_start, len(objectives)] used as placeholders
        # when value in range found, write number of conditions complete for objective[value - start]
        self.special_characters_start = 1

        self.lines = []
        self.line_color_addresses = []
        for oi, objective in enumerate(objectives):
            result_line = objective.letter + " " + str(objective.result)
            self.lines.append(scroll_area.Line(result_line, f0.set_blue_text_color))

            if len(objective.conditions) == 0:
                self.lines.append(scroll_area.Line(" " + chr(self.special_characters_start + oi) + " required", f0.set_user_text_color))
            else:
                conditions_required = ""
                if objective.conditions_required != 1: # exclude "All 1 of"
                    conditions_required = " All " + str(objective.conditions_required) + " of"
                if objective.conditions_required < len(objective.conditions):
                    conditions_required = " Any " + str(objective.conditions_required) + " of"
                if conditions_required != "":
                    self.lines.append(scroll_area.Line(conditions_required, f0.set_user_text_color))

                for condition in objective.conditions:
                    condition_line = "  " + str(condition)
                    # When you finish a condition, gray it out
                    line_color_address = condition.menu(
                        asm.JMP(f0.set_gray_text_color, asm.ABS),
                        asm.JMP(f0.set_user_text_color, asm.ABS),
                    ).space.start_address
                    self.lines.append(scroll_area.Line(condition_line, line_color_address))

                if conditions_required != "": #exclude "All 1 of"
                    completed_line = " -- " + chr(self.special_characters_start + oi) + " completed --"
                    self.lines.append(scroll_area.Line(completed_line, f0.set_user_text_color))
            self.lines.append(scroll_area.Line("", f0.set_user_text_color))

        if len(self.lines) == 0:
            self.lines.append(scroll_area.Line("No Objectives", f0.set_blue_text_color))
        else:
            del self.lines[-1] # exclude final empty line

        super().__init__()

    def draw_character_mod(self):
        from .. import objectives as objectives
        from ..data.text.text2 import text_value

        if len(objectives) == 0:
            super().draw_character_mod()
            return

        src = []
        for objective in objectives:
            src += [
                (objective.conditions_complete.menu().space.start_address & 0xffff).to_bytes(2, "little"),
            ]
        space = Write(Bank.F0, src, "objectives menu count conditions complete table")
        count_table = space.start_address

        src = []
        for objective in objectives:
            src += [
                objective.conditions_required.to_bytes(1, "little"),
            ]
        space = Write(Bank.F0, src, "objectives menu conditions required table")
        conditions_required_table = space.start_address_snes

        src = [
            asm.CMP(self.special_characters_start, asm.IMM8),
            asm.BLT("WRITE_CHARACTER"), # branch if less than first special character value

            asm.CMP(self.special_characters_start + len(objectives), asm.IMM8),
            asm.BGE("WRITE_CHARACTER"), # branch if greater than last special character value

            asm.PHX(),
            asm.PHY(),
            asm.XY8(),
            asm.SEC(),
            asm.SBC(self.special_characters_start, asm.IMM8),   # a = 0 based objective index
            asm.TAY(),                                          # y = 0 based objective index
            asm.ASL(),                                          # a = objective index * 2
            asm.TAX(),                                          # x = objective index * 2
            asm.JSR(count_table, asm.ABS_X_16),                 # x = number conditions complete
            asm.TXA(),                                          # a = number conditions complete
            asm.TYX(),                                          # x = 0 based objective index
            # when you finish an objective, gray it out
            asm.CMP(conditions_required_table, asm.LNG_X),
            asm.BLT("SKIP_COLOR_CHANGE"),
            asm.PHA(),
            asm.JSR(f0.set_gray_text_color, asm.ABS),
            asm.PLA(),
            "SKIP_COLOR_CHANGE",
            asm.XY16(),
            asm.PLY(),
            asm.PLX(),
            asm.CLC(),
            asm.ADC(text_value['0'], asm.IMM8),                 # a = number conditions complete converted to character

            "WRITE_CHARACTER",
            asm.STA(0x2180, asm.ABS),                           # write character in a register
            asm.RTL(),
        ]
        space = Write(Bank.F0, src, "objectives menu draw character")
        self.draw_character = space.start_address
