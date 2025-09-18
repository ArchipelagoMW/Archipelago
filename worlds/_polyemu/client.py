from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, ClassVar, Sequence

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from .core import PLATFORMS

if TYPE_CHECKING:
    from .context import PolyEmuClientContext


__all__ = [
    "AutoPolyEmuClientRegister", "PolyEmuClient",
]


def launch_client(*args) -> None:
    from .context import launch
    launch_subprocess(launch, name="PolyEmuClient", args=args)


client_component = Component("PolyEmu Client", "PolyEmuClient", component_type=Type.CLIENT, func=launch_client,
                             file_identifier=SuffixIdentifier())
components.append(client_component)


class AutoPolyEmuClientRegister(abc.ABCMeta):
    game_handlers: ClassVar[dict[tuple[int, ...], dict[str, PolyEmuClient]]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoPolyEmuClientRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register handler
        if "platform" in namespace:
            platforms = namespace["platform"] if isinstance(namespace["platform"], Sequence) else (namespace["platform"],)
            platforms = tuple(PLATFORMS.cast_to_int(p) for p in platforms)
            if platforms not in AutoPolyEmuClientRegister.game_handlers:
                AutoPolyEmuClientRegister.game_handlers[platforms] = {}

            if "game" in namespace:
                AutoPolyEmuClientRegister.game_handlers[platforms][namespace["game"]] = new_class()

        # Update launcher component's suffixes
        if "patch_suffix" in namespace:
            if namespace["patch_suffix"] is not None:
                existing_identifier: SuffixIdentifier = client_component.file_identifier
                new_suffixes = [*existing_identifier.suffixes]

                if type(namespace["patch_suffix"]) is str:
                    new_suffixes.append(namespace["patch_suffix"])
                else:
                    new_suffixes.extend(namespace["patch_suffix"])

                client_component.file_identifier = SuffixIdentifier(*new_suffixes)

        return new_class

    @staticmethod
    async def get_handler(ctx: "PolyEmuClientContext", system: str) -> PolyEmuClient | None:
        # TODO: Get clients to register the request types they need, and check
        # whether the device can fulfill the requests a handler uses.
        for systems, handlers in AutoPolyEmuClientRegister.game_handlers.items():
            if system in systems:
                for handler in handlers.values():
                    if await handler.validate_rom(ctx):
                        return handler

        return None


class PolyEmuClient(abc.ABC, metaclass=AutoPolyEmuClientRegister):
    platform: ClassVar[int | tuple[int, ...]]
    """The platform(s) that the game this client is for runs on"""

    game: ClassVar[str]
    """The game this client is for"""

    patch_suffix: ClassVar[str | tuple[str, ...] | None]
    """The file extension(s) this client is meant to open and patch (e.g. ".apz3")"""

    @abc.abstractmethod
    async def validate_rom(self, ctx: "PolyEmuClientContext") -> bool:
        """Should return whether the currently loaded ROM should be handled by this client. You might read the game name
        from the ROM header, for example. This function will only be asked to validate ROMs from the system set by the
        client class, so you do not need to check the system yourself.

        Once this function has determined that the ROM should be handled by this client, it should also modify `ctx`
        as necessary (such as setting `ctx.game = self.game`, modifying `ctx.items_handling`, etc...)."""
        ...

    async def set_auth(self, ctx: "PolyEmuClientContext") -> None:
        """Should set ctx.auth in anticipation of sending a `Connected` packet. You may override this if you store slot
        name in your patched ROM. If ctx.auth is not set after calling, the player will be prompted to enter their
        username."""
        pass

    @abc.abstractmethod
    async def game_watcher(self, ctx: "PolyEmuClientContext") -> None:
        """Runs on a loop with the approximate interval `ctx.watcher_timeout`. The currently loaded ROM is guaranteed
        to have passed your validator when this function is called, and the emulator is very likely to be connected."""
        ...

    def on_package(self, ctx: "PolyEmuClientContext", cmd: str, args: dict) -> None:
        """For handling packages from the server. Called from `PolyEmuClientContext.on_package`."""
        pass
