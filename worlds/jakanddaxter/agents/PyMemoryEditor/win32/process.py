# -*- coding: utf-8 -*-

from ..enums import ScanTypesEnum
from ..process import AbstractProcess
from ..process.errors import ClosedProcess
from .enums import ProcessOperationsEnum

from .functions import (
    CloseProcessHandle,
    GetMemoryRegions,
    GetProcessHandle,
    ReadProcessMemory,
    SearchAddressesByValue,
    SearchValuesByAddresses,
    WriteProcessMemory
)

from typing import Generator, Optional, Sequence, Tuple, Type, TypeVar, Union


T = TypeVar("T")


class WindowsProcess(AbstractProcess):
    """
    Class to open a Windows process for reading, writing and searching at its memory.
    """

    def __init__(
        self,
        *,
        window_title: Optional[str] = None,
        process_name: Optional[str] = None,
        pid: Optional[int] = None,
        permission: ProcessOperationsEnum = ProcessOperationsEnum.PROCESS_ALL_ACCESS
    ):
        """
        :param window_title: window title of the target program.
        :param process_name: name of the target process.
        :param pid: process ID.
        :param permission: access mode to the process.
        """
        super().__init__(
            window_title=window_title,
            process_name=process_name,
            pid=pid
        )
        self.__closed = False

        # Instantiate the permission argument.
        self.__permission = permission

        # Get the process handle.
        self.__process_handle = GetProcessHandle(self.__permission.value, False, self.pid)

    def close(self) -> bool:
        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: return True

        self.__closed = CloseProcessHandle(self.__process_handle) != 0
        return self.__closed

    def get_memory_regions(self) -> Generator[dict, None, None]:
        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()
        return GetMemoryRegions(self.__process_handle)

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

        valid_permissions = [
            ProcessOperationsEnum.PROCESS_ALL_ACCESS.value,
            ProcessOperationsEnum.PROCESS_VM_READ.value
        ]
        if self.__permission.value not in valid_permissions:
            raise PermissionError("The handle does not have permission to read the process memory.")

        return SearchValuesByAddresses(self.__process_handle, pytype, bufflength, addresses, raise_error=raise_error)

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

        valid_permissions = [
            ProcessOperationsEnum.PROCESS_ALL_ACCESS.value,
            ProcessOperationsEnum.PROCESS_VM_READ.value
        ]
        if self.__permission.value not in valid_permissions:
            raise PermissionError("The handle does not have permission to read the process memory.")

        if scan_type in [ScanTypesEnum.VALUE_BETWEEN, ScanTypesEnum.NOT_VALUE_BETWEEN]:
            raise ValueError("Use the method search_by_value_between(...) to search within a range of values.")

        return SearchAddressesByValue(self.__process_handle, pytype, bufflength, value, scan_type, progress_information, writeable_only)

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

        valid_permissions = [
            ProcessOperationsEnum.PROCESS_ALL_ACCESS.value,
            ProcessOperationsEnum.PROCESS_VM_READ.value
        ]
        if self.__permission.value not in valid_permissions:
            raise PermissionError("The handle does not have permission to read the process memory.")

        scan_type = ScanTypesEnum.NOT_VALUE_BETWEEN if not_between else ScanTypesEnum.VALUE_BETWEEN
        return SearchAddressesByValue(self.__process_handle, pytype, bufflength, (start, end), scan_type, progress_information, writeable_only)

    def read_process_memory(
        self,
        address: int,
        pytype: Type[T],
        bufflength: int
    ) -> T:
        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()

        valid_permissions = [
            ProcessOperationsEnum.PROCESS_ALL_ACCESS.value,
            ProcessOperationsEnum.PROCESS_VM_READ.value
        ]
        if self.__permission.value not in valid_permissions:
            raise PermissionError("The handle does not have permission to read the process memory.")

        return ReadProcessMemory(self.__process_handle, address, pytype, bufflength)

    def write_process_memory(
        self,
        address: int,
        pytype: Type[T],
        bufflength: int,
        value: Union[bool, int, float, str, bytes]
    ) -> T:
        # Check the documentation of this method in the AbstractProcess superclass for more information.
        if self.__closed: raise ClosedProcess()

        valid_permissions = [
            ProcessOperationsEnum.PROCESS_ALL_ACCESS.value,
            ProcessOperationsEnum.PROCESS_VM_OPERATION.value | ProcessOperationsEnum.PROCESS_VM_WRITE.value
        ]
        if self.__permission.value not in valid_permissions:
            raise PermissionError("The handle does not have permission to write to the process memory.")

        return WriteProcessMemory(self.__process_handle, address, pytype, bufflength, value)
