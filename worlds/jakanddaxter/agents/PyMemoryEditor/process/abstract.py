# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Generator, Optional, Sequence, Tuple, Type, TypeVar, Union

from ..enums import ScanTypesEnum
from ..process.info import ProcessInfo


T = TypeVar("T")


class AbstractProcess(ABC):
    """
    Abstract class to represent a process.
    """

    @abstractmethod
    def __init__(self, *, window_title: Optional[str] = None, process_name: Optional[str] = None, pid: Optional[int] = None):
        """
        :param window_title: window title of the target program.
        :param process_name: name of the target process.
        :param pid: process ID.
        """
        self._process_info = ProcessInfo()

        # Set the attributes to the process.
        if pid:
            self._process_info.pid = pid

        elif window_title:
            self._process_info.window_title = window_title

        elif process_name:
            self._process_info.process_name = process_name

        else:
            raise TypeError("You must pass an argument to one of these parameters (window_title, process_name, pid).")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    @property
    def pid(self) -> int:
        return self._process_info.pid

    @abstractmethod
    def close(self) -> bool:
        """
        Close the process handle.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_memory_regions(self) -> Generator[dict, None, None]:
        """
        Generates dictionaries with the address, size and other
        information of each memory region used by the process.
        """
        raise NotImplementedError()

    @abstractmethod
    def search_by_addresses(
        self,
        pytype: Type[T],
        bufflength: int,
        addresses: Sequence[int],
        *,
        raise_error: bool = False,
    ) -> Generator[Tuple[int, Optional[T]], None, None]:
        """
        Search the whole memory space, accessible to the process,
        for the provided list of addresses, returning their values.
        """
        raise NotImplementedError()

    @abstractmethod
    def search_by_value(
        self,
        pytype: Type[T],
        bufflength: int,
        value: Union[bool, int, float, str, bytes],
        scan_type: ScanTypesEnum = ScanTypesEnum.EXACT_VALUE,
        *,
        progress_information: bool = False,
        writeable_only: bool = False,
    ) -> Generator[Union[int, Tuple[int, dict]], None, None]:
        """
        Search the whole memory space, accessible to the process,
        for the provided value, returning the found addresses.

        :param pytype: type of value to be queried (bool, int, float, str or bytes).
        :param bufflength: value size in bytes (1, 2, 4, 8).
        :param value: value to be queried (bool, int, float, str or bytes).
        :param scan_type: the way to compare the values.
        :param progress_information: if True, a dictionary with the progress information will be return.
        :param writeable_only: if True, search only at writeable memory regions.
        """
        raise NotImplementedError()

    def search_by_value_between(
        self,
        pytype: Type[T],
        bufflength: int,
        start: Union[bool, int, float, str, bytes],
        end: Union[bool, int, float, str, bytes],
        *,
        not_between: bool = False,
        progress_information: bool = False,
        writeable_only: bool = False,
    ) -> Generator[Union[int, Tuple[int, dict]], None, None]:
        """
        Search the whole memory space, accessible to the process,
        for a value within the provided range, returning the found addresses.

        :param pytype: type of value to be queried (bool, int, float, str or bytes).
        :param bufflength: value size in bytes (1, 2, 4, 8).
        :param start: minimum inclusive value to be queried (bool, int, float, str or bytes).
        :param end: maximum inclusive value to be queried (bool, int, float, str or bytes).
        :param not_between: if True, return only addresses of values that are NOT within the range.
        :param progress_information: if True, a dictionary with the progress information will be return.
        :param writeable_only: if True, search only at writeable memory regions.
        """
        raise NotImplementedError()

    @abstractmethod
    def read_process_memory(
        self,
        address: int,
        pytype: Type[T],
        bufflength: int
    ) -> T:
        """
        Return a value from a memory address.

        :param address: target memory address (ex: 0x006A9EC0).
        :param pytype: type of the value to be received (bool, int, float, str or bytes).
        :param bufflength: value size in bytes (1, 2, 4, 8).
        """
        raise NotImplementedError()

    @abstractmethod
    def write_process_memory(
        self,
        address: int,
        pytype: Type[T],
        bufflength: int,
        value: Union[bool, int, float, str, bytes]
    ) -> T:
        """
        Write a value to a memory address.

        :param address: target memory address (ex: 0x006A9EC0).
        :param pytype: type of value to be written into memory (bool, int, float, str or bytes).
        :param bufflength: value size in bytes (1, 2, 4, 8).
        :param value: value to be written (bool, int, float, str or bytes).
        """
        raise NotImplementedError()
