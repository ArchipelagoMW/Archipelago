
from __future__ import annotations
import abc
from dataclasses import dataclass
import enum
import logging
import sys
from typing import (TYPE_CHECKING, Any, ClassVar, Dict, Generic, Iterable, List,
                    NamedTuple, Optional, Sequence, Tuple, TypeVar, Union)

from typing_extensions import TypeGuard

# TODO: get rid of python version check when < 3.10 is gone
if sys.version_info.major == 3 and sys.version_info.minor < 10:
    from Utils import bisect_right
else:
    from bisect import bisect_right

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
            if await handler.validate_rom(ctx):
                return handler
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


class Read(NamedTuple):
    """ snes memory read - address and size in bytes """
    address: int
    size: int


@dataclass
class _MemRead:
    location: Read
    data: bytes


_T_Enum = TypeVar("_T_Enum", bound=enum.Enum)


class SnesReader(Generic[_T_Enum]):
    _ranges: Sequence[_MemRead]
    """ sorted by address """
    _ctx: "SNIContext"

    def __init__(self, reads: type[_T_Enum], ctx: "SNIContext") -> None:
        self._ranges = self._make_ranges(reads)
        self._ctx = ctx

    @staticmethod
    def _make_ranges(reads: type[enum.Enum]) -> Sequence[_MemRead]:

        unprocessed_reads: List[Read] = []
        for e in reads:
            assert isinstance(e.value, Read), f"{reads.__name__} {e=} {type(e.value)=}"
            unprocessed_reads.append(e.value)
        unprocessed_reads.sort()

        ranges: List[_MemRead] = []
        for read in unprocessed_reads:
            #                                      v  end of the previous range
            if len(ranges) == 0 or read.address - (ranges[-1].location.address + ranges[-1].location.size) > 255:
                ranges.append(_MemRead(read, bytes([0 for _ in range(read.size)])))
            else:  # combine with previous range
                chunk_address = ranges[-1].location.address
                assert read.address >= chunk_address, "sort() didn't work? or something"
                original_chunk_size = ranges[-1].location.size
                new_size = max((read.address + read.size) - chunk_address,
                               original_chunk_size)
                ranges[-1] = _MemRead(Read(chunk_address, new_size), bytes([0 for _ in range(new_size)]))
        logging.debug(f"{len(ranges)=} {max(r.location.size for r in ranges)=}")
        return ranges

    async def read(self) -> bool:
        """ returns `True` if all the reads succeeded, `False` if any failed """
        from SNIClient import snes_read

        # To keep things better synced, we don't update any unless we read all successfully.
        to_place: List[Tuple[_MemRead, bytes]] = []
        for rr in self._ranges:
            response = await snes_read(self._ctx, rr.location.address, rr.location.size)
            if response is None:
                return False
            to_place.append((rr, response))
        for rr, r in to_place:
            rr.data = r
        return True

    def get(self, read: _T_Enum) -> bytes:
        """
        `read` should be called before this (and it should return `True`)
        to make this data up-to-date and valid
        """
        address: int = read.value.address
        size: int = read.value.size
        index = bisect_right(self._ranges, address, key=lambda r: r.location.address) - 1
        assert index >= 0, f"{self._ranges=} {read.value=}"
        mem_read = self._ranges[index]
        sub_index = address - mem_read.location.address
        return mem_read.data[sub_index:sub_index + size]
