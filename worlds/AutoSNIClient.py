
from __future__ import annotations
import abc
import logging
from typing import TYPE_CHECKING, ClassVar, Dict, Iterable, Tuple, Any, Optional, Union, TypeGuard

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components

if TYPE_CHECKING:
    from SNIClient import SNIContext

component = Component('SNI Client', 'SNIClient', component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apsoe"))
components.append(component)


def valid_patch_suffix(obj: object) -> TypeGuard[Union[str, Iterable[str]]]:
    """ make sure this is a valid value for the class variable `patch_suffix` """

    def valid_individual(one: object) -> TypeGuard[str]:
        """ check an individual suffix """
        # TODO: decide:                 len(one) > 3 and one.startswith(".ap") ?
        # or keep it more general?
        return isinstance(one, str) and len(one) > 1 and one.startswith(".")

    if isinstance(obj, str):
        return valid_individual(obj)
    if not isinstance(obj, Iterable):
        return False
    obj_it: Iterable[object] = obj
    return all(valid_individual(each) for each in obj_it)


class AutoSNIClientRegister(abc.ABCMeta):
    game_handlers: ClassVar[Dict[str, SNIClient]] = {}

    def __new__(cls, name: str, bases: Tuple[type, ...], dct: Dict[str, Any]) -> AutoSNIClientRegister:
        # construct class
        new_class = super().__new__(cls, name, bases, dct)
        if "game" in dct:
            AutoSNIClientRegister.game_handlers[dct["game"]] = new_class()

        if "patch_suffix" in dct:
            patch_suffix = dct["patch_suffix"]
            assert valid_patch_suffix(patch_suffix), f"class {name} defining invalid {patch_suffix=}"

            existing_identifier = component.file_identifier
            assert isinstance(existing_identifier, SuffixIdentifier), f"{existing_identifier=}"
            new_suffixes = [*existing_identifier.suffixes]

            if isinstance(patch_suffix, str):
                new_suffixes.append(patch_suffix)
            else:
                new_suffixes.extend(patch_suffix)

            component.file_identifier = SuffixIdentifier(*new_suffixes)

        return new_class

    @staticmethod
    async def get_handler(ctx: SNIContext) -> Optional[SNIClient]:
        for _game, handler in AutoSNIClientRegister.game_handlers.items():
            try:
                if await handler.validate_rom(ctx):
                    return handler
            except Exception as e:
                text_file_logger = logging.getLogger()
                text_file_logger.exception(e)
        return None


class SNIClient(abc.ABC, metaclass=AutoSNIClientRegister):

    patch_suffix: ClassVar[Union[str, Iterable[str]]] = ()
    """The file extension(s) this client is meant to open and patch (e.g. ".aplttp")"""

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

    def on_package(self, ctx: SNIContext, cmd: str, args: Dict[str, Any]) -> None:
        """ override this with code to handle packages from the server """
        pass
