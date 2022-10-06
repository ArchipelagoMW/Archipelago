
from __future__ import annotations
from typing import ClassVar, Dict, Tuple, Any, Optional


class AutoSNIClientRegister(type):
    game_handlers: ClassVar[Dict[str, AutoSNIClientRegister]] = {}

    def __new__(mcs, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoSNIClientRegister:
        # construct class
        new_class = super().__new__(mcs, name, bases, dct)
        if "game" in dct:
            AutoSNIClientRegister.game_handlers[dct["game"]] = new_class()
        return new_class

    @staticmethod
    async def get_handler(ctx) -> Optional[SNIClient]:
        for game, handler in AutoSNIClientRegister.game_handlers.items():
            if await handler.rom_init(ctx):
                return handler
        return None


class SNIClient(metaclass=AutoSNIClientRegister):

    async def rom_init(self, ctx):
        raise NotImplementedError

    async def game_watcher(self, ctx):
        raise NotImplementedError

    async def deathlink_kill_player(self, ctx):
        pass
