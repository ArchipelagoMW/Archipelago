from ..menus import pregame_track as pregame_track
from ..menus import pregame as pregame
from ..menus import track as track
from ..menus import dance as dance
from ..menus import rage as rage
from ..menus import status as status
from ..menus import final_lineup as final_lineup
from ..menus import coliseum as coliseum
from ..menus import sell as sell
from ..menus import magic as magic

class Menus:
    def __init__(self, characters, dances, rages, enemies):
        self.characters = characters
        self.dances = dances
        self.rages = rages
        self.enemies = enemies

        self.pregame_track = pregame_track.PreGameTrack(self.characters)
        self.pregame_menu = pregame.PreGameMenu(self.pregame_track)
        self.track_menu = track.TrackMenu(self.pregame_track)
        self.dance_menu = dance.DanceMenu(self.dances)
        self.rage_menu = rage.RageMenu(self.rages, self.enemies)
        self.status_menu = status.StatusMenu(self.characters)
        self.final_lineup_menu = final_lineup.FinalLineupMenu(self.characters)
        self.coliseum_menu = coliseum.ColiseumMenu()
        self.sell_menu = sell.SellMenu()
        self.magic_menu = magic.MagicMenu()

        self.scrollbar_bugfix()

    def scrollbar_bugfix(self):
        from ..memory.space import Reserve
        from ..instruction import asm as asm

        # square hardcoded the vertical scrollbar speed here (0x0070 is the speed for menus with 256 rows, e.g. items)
        # as a result, the scrollbar does not work correctly in menus with between roughly 140 to 230 rows
        # fix this by adding the vertical scrollbar speed from memory to handle menus with custom number of rows
        space = Reserve(0x309b1, 0x309b3, "menus scrollbar bugfix")
        space.write(
            asm.ADC(0x354a, asm.ABS_X), # add scrollbar vertical speed
        )
