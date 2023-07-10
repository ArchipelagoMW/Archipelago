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
    @abc.abstractmethod
    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        ...

    @abc.abstractmethod
    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        ...

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        pass
