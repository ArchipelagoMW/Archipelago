
from __future__ import annotations
import abc
from typing import TYPE_CHECKING, ClassVar, Dict, Tuple, Any, Optional

if TYPE_CHECKING:
    from SNIClient import SNIContext


class AutoSNIClientRegister(abc.ABCMeta):
    game_handlers: ClassVar[Dict[str, SNIClient]] = {}

    def __new__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoSNIClientRegister:
        # construct class
        new_class = super().__new__(cls, name, bases, dct)
        if "game" in dct:
            AutoSNIClientRegister.game_handlers[dct["game"]] = new_class()
        return new_class

    @staticmethod
    async def get_handler(ctx: SNIContext) -> Optional[SNIClient]:
        for _game, handler in AutoSNIClientRegister.game_handlers.items():
            if await handler.validate_rom(ctx):
                return handler
        return None


class SNIClient(abc.ABC, metaclass=AutoSNIClientRegister):

    @abc.abstractmethod
    async def validate_rom(self, ctx: SNIContext) -> bool:
        """ TODO: interface documentation here """
        ...

    @abc.abstractmethod
    async def game_watcher(self, ctx: SNIContext) -> None:
        """ TODO: interface documentation here """
        ...

    async def deathlink_kill_player(self, ctx: SNIContext) -> None:
        """ override this with implementation to kill player """
        pass
