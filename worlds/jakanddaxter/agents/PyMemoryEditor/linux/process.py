# -*- coding: utf-8 -*-

from ..enums import ScanTypesEnum
from ..process import AbstractProcess
from ..process.errors import ClosedProcess
from .functions import (
    get_memory_regions,
    read_process_memory,
    search_addresses_by_value,
    search_values_by_addresses,
    write_process_memory
)
from typing import Generator, Optional, Sequence, Tuple, Type, TypeVar, Union


T = TypeVar("T")


class LinuxProcess(AbstractProcess):
    """
    Class to open a Linux process for reading, writing and searching at its memory.
    """

    def __init__(
        self,
        *,
        window_title: Optional[str] = None,
        process_name: Optional[str] = None,
        pid: Optional[int] = None,
        **kwargs
    ):
        """
        :param window_title: window title of the target program.
        :param process_name: name of the target process.
        :param pid: process ID.
        """
        super().__init__(
            window_title=window_title,
            process_name=process_name,
            pid=pid
        )
        self.__closed = False

    def close(self) -> bool:
        # Check the documentation of this method in the AbstractProcess superclass for more information.
        self.__closed = True
        return True

    def get_memory_regions(self) -> Generator[dict, None, None]:
        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()
        return get_memory_regions(self.pid)

    def read_process_memory(
        self,
        address: int,
        pytype: Type[T],
        bufflength: int
    ) -> T:
        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()
        return read_process_memory(self.pid, address, pytype, bufflength)

    def search_by_addresses(
        self,
        pytype: Type[T],
        bufflength: int,
        addresses: Sequence[int],
        *,
        raise_error: bool = False,
    ) -> Generator[Tuple[int, Optional[T]], None, None]:

        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()
        return search_values_by_addresses(self.pid, pytype, bufflength, addresses, raise_error=raise_error)

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

        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()

        if scan_type in [ScanTypesEnum.VALUE_BETWEEN, ScanTypesEnum.NOT_VALUE_BETWEEN]:
            raise ValueError("Use the method search_by_value_between(...) to search within a range of values.")

        return search_addresses_by_value(self.pid, pytype, bufflength, value, scan_type, progress_information, writeable_only)

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

        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()

        scan_type = ScanTypesEnum.NOT_VALUE_BETWEEN if not_between else ScanTypesEnum.VALUE_BETWEEN
        return search_addresses_by_value(self.pid, pytype, bufflength, (start, end), scan_type, progress_information, writeable_only)

    def write_process_memory(
        self,
        address: int,
        pytype: Type[T],
        bufflength: int,
        value: Union[bool, int, float, str, bytes]
    ) -> T:
        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()
        return write_process_memory(self.pid, address, pytype, bufflength, value)
