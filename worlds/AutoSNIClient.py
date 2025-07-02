
from __future__ import annotations
import abc
from bisect import bisect_right
from dataclasses import dataclass
import enum
import logging
from typing import (TYPE_CHECKING, Any, ClassVar, Dict, Generic, Iterable, List,
                    NamedTuple, Optional, Sequence, Tuple, TypeGuard, TypeVar, Union)


from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components

if TYPE_CHECKING:
    from SNIClient import SNIContext

component = Component('SNI Client', 'SNIClient', component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apsoe"),
                      description="A client for connecting to SNES consoles via Super Nintendo Interface.")
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


class Read(NamedTuple):
    """ snes memory read - address and size in bytes """
    address: int
    size: int


@dataclass(frozen=True)
class _MemRead:
    location: Read
    data: bytes


_T_Enum = TypeVar("_T_Enum", bound=enum.Enum)


class SnesData(Generic[_T_Enum]):
    _ranges: Sequence[_MemRead]
    """ sorted by address """

    def __init__(self, ranges: Sequence[tuple[Read, bytes]]) -> None:
        self._ranges = []
        for r, d in ranges:
            self._ranges.append(_MemRead(r, d))

    def get(self, read: _T_Enum) -> bytes:
        assert isinstance(read.value, Read), read.value
        address = read.value.address
        index = bisect_right(self._ranges, address, key=lambda r: r.location.address) - 1
        assert index >= 0, (self._ranges, read.value)
        mem_read = self._ranges[index]
        sub_index = address - mem_read.location.address
        return mem_read.data[sub_index:sub_index + read.value.size]


class SnesReader(Generic[_T_Enum]):
    _ranges: Sequence[Read]
    """ sorted by address """

    def __init__(self, reads: type[_T_Enum]) -> None:
        self._ranges = self._make_ranges(reads)

    @staticmethod
    def _make_ranges(reads: type[enum.Enum]) -> Sequence[Read]:

        unprocessed_reads: list[Read] = []
        for e in reads:
            assert isinstance(e.value, Read), (reads.__name__, e, e.value)
            unprocessed_reads.append(e.value)
        unprocessed_reads.sort()

        ranges: list[Read] = []
        for read in unprocessed_reads:
            #                                      v  end of the previous range
            if len(ranges) == 0 or read.address - (ranges[-1].address + ranges[-1].size) > 255:
                ranges.append(read)
            else:  # combine with previous range
                chunk_address = ranges[-1].address
                assert read.address >= chunk_address, "sort() didn't work? or something"
                original_chunk_size = ranges[-1].size
                new_size = max((read.address + read.size) - chunk_address,
                               original_chunk_size)
                ranges[-1] = Read(chunk_address, new_size)
        logging.debug(f"{len(ranges)=} {max(r.size for r in ranges)=}")
        return ranges

    async def read(self, ctx: "SNIContext") -> SnesData[_T_Enum] | None:
        """
        returns `None` if reading fails,
        otherwise returns the data for the registered `Enum`
        """
        from SNIClient import snes_read

        reads: list[tuple[Read, bytes]] = []
        for r in self._ranges:
            response = await snes_read(ctx, r.address, r.size)
            if response is None:
                return None
            reads.append((r, response))
        return SnesData(reads)
