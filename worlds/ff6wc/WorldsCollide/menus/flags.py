from ..memory.space import START_ADDRESS_SNES, Bank, Reserve, Allocate, Write
from ..instruction import asm as asm
from ..instruction import f0 as f0
from .. import args as args

from ..menus import pregame_track_scroll_area as scroll_area
from ..data.text.text2 import text_value

class Flags(scroll_area.ScrollArea):
    MENU_NUMBER = 12

    def __init__(self):
        self.lines = []
        self.submenus = {} # dictionary of submenus. key = line number, value = ScrollArea derived class
        if args.hide_flags:
            self.lines.append(scroll_area.Line("Flags Hidden", f0.set_blue_text_color))
        else:
            for _, group in args.group_modules.items():
                if hasattr(group, "menu"):
                    name, options = group.menu(args)

                    self.lines.append(scroll_area.Line(name, f0.set_blue_text_color))
                    for option in options:
                        key = option[0]
                        value = option[1]


                        key = "  " + key.replace("&", "+")

                        # if we're given a scroll area, save it as a sub-menu with a value of X …, where X is the number of items in the sub-menu
                        if isinstance(value, scroll_area.ScrollArea):
                            self.submenus[len(self.lines)] = value
                            value = f"{value.number_items} {chr(text_value['…'])}"

                        value = str(value)
                        if value == "True":
                            value = "T"
                        elif value == "False":
                            value = "F"

                        padding = scroll_area.WIDTH - (len(key) + len(value))
                        self.lines.append(scroll_area.Line(f"{key}{' ' * padding}{value}", f0.set_user_text_color))

                    self.lines.append(scroll_area.Line("", f0.set_user_text_color))
            del self.lines[-1] # exclude final empty line

        super().__init__()
