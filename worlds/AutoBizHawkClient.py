from __future__ import annotations
import abc
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Tuple

if TYPE_CHECKING:
    from BizHawkClient import BizHawkClientContext


class AutoBizHawkClientRegister(abc.ABCMeta):
    game_handlers: ClassVar[Dict[str, Dict[str, BizHawkClient]]] = {}

    def __new__(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> AutoBizHawkClientRegister:
        new_class = super().__new__(cls, name, bases, namespace)
        if "system" in namespace:
            if namespace["system"] not in AutoBizHawkClientRegister.game_handlers:
                AutoBizHawkClientRegister.game_handlers[namespace["system"]] = {}

            if "game" in namespace:
                AutoBizHawkClientRegister.game_handlers[namespace["system"]][namespace["game"]] = new_class()

        return new_class

    @staticmethod
    async def get_handler(ctx: BizHawkClientContext, system: str) -> Optional[BizHawkClient]:
        if system in AutoBizHawkClientRegister.game_handlers:
            for handler in AutoBizHawkClientRegister.game_handlers[system].values():
                if await handler.validate_rom(ctx):
                    return handler

        return None


class BizHawkClient(abc.ABC, metaclass=AutoBizHawkClientRegister):
    system: ClassVar[str]
    """The system that the game this client is for runs on"""

    game: ClassVar[str]
    """The game this client is for"""

    @abc.abstractmethod
    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        """Should return whether the currently loaded ROM should be handled by this client. You might read the game name
        from the ROM header, for example. This function will only be asked to validate ROMs from the system set by the
        client class, so you do not need to check the system yourself.

        Once this function has determined that the ROM should be handled by this client, it should also modify `ctx`
        as necessary (such as setting `ctx.game = self.game`, modifying `ctx.items_handling`, etc...)."""
        ...

    @abc.abstractmethod
    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        """Runs on a loop with the approximate interval `ctx.watcher_timeout`. The currently loaded ROM is guaranteed
        to have passed your validator when this function is called, and the emulator is very likely to be connected.
        
        Your client is also expected to send `Connect` from here. Make sure you don't send them repeatedly and check the
        server connection first."""
        ...

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        """For handling packages from the server. Called from `BizHawkClientContext.on_package`."""
        pass
