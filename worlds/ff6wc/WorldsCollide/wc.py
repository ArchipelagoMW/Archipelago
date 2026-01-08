from typing import Sequence


class WC():
    def main(self, ap_args: Sequence[str]) -> None:
        from . import args as args
        args.main(ap_args)
        from . import log

        from .memory.memory import Memory
        memory = Memory()

        from .data.data import Data
        data = Data(memory.rom, args)

        from .event.events import Events
        events = Events(memory.rom, args, data)

        from .menus.menus import Menus
        menus = Menus(data.characters, data.dances, data.rages, data.enemies)

        from .battle import Battle
        battle = Battle()

        from .settings import Settings
        settings = Settings()

        from .bug_fixes import BugFixes
        bug_fixes = BugFixes()

        data.write()
        memory.write()