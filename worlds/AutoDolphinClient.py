from __future__ import annotations
import abc
from typing import TYPE_CHECKING, ClassVar, Dict, Tuple, Any, Optional

if TYPE_CHECKING:
    from DolphinClient import DolphinContext


class AutoDolphinClientRegister(abc.ABCMeta):
    game_handlers: ClassVar[Dict[str, DolphinClient]] = {}

    def __new__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoDolphinClientRegister:
        # construct class
        new_class = super().__new__(cls, name, bases, dct)
        if "game" in dct:
            AutoDolphinClientRegister.game_handlers[dct["game"]] = new_class()
        return new_class

    @staticmethod
    async def get_handler(ctx: DolphinContext) -> Optional[DolphinClient]:
        for _game, handler in AutoDolphinClientRegister.game_handlers.items():
            if await handler.validate_rom(ctx):
                return handler
        return None


class DolphinClient(abc.ABC, metaclass=AutoDolphinClientRegister):

    @abc.abstractmethod
    async def validate_rom(self, ctx: DolphinContext) -> bool:
        """ TODO: interface documentation here """
        ...

    @abc.abstractmethod
    async def game_watcher(self, ctx: DolphinContext) -> None:
        """ TODO: interface documentation here """
        ...

    async def deathlink_kill_player(self, ctx: DolphinContext) -> None:
        """ TODO: override this with implementation to kill player """
        pass
