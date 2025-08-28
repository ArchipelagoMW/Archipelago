# -*- coding: utf-8 -*-
from enum import Enum


class ProcessOperationsEnum(Enum):
    """
    Enum with all permissions and operations you can do to a process.
    """
    # All possible access rights for a process object.Windows Server 2003 and Windows XP: The size of
    # the PROCESS_ALL_ACCESS flag increased on Windows Server 2008 and Windows Vista. If an application
    # compiled for Windows Server 2008 and Windows Vista is run on Windows Server 2003 or Windows XP,
    # the PROCESS_ALL_ACCESS flag is too large and the function specifying this flag fails with
    # ERROR_ACCESS_DENIED. To avoid this problem, specify the minimum set of access rights required for
    # the operation. If PROCESS_ALL_ACCESS must be used, set _WIN32_WINNT to the minimum operating
    # system targeted by your application (for example, #define _WIN32_WINNT _WIN32_WINNT_WINXP). For
    # more information, see Using the Windows Headers.
    PROCESS_ALL_ACCESS = 0x1f0fff

    # Required to create a process.
    PROCESS_CREATE_PROCESS = 0x0080

    # Required to create a thread.
    PROCESS_CREATE_THREAD = 0x0002

    # Required to duplicate a handle using DuplicateHandle.
    PROCESS_DUP_HANDLE = 0x0040

    # Required to retrieve certain information about a process, such as its token, exit code, and priority
    # class (see OpenProcessToken).
    PROCESS_QUERY_INFORMATION = 0x0400

    # Required to retrieve certain information about a process (see GetExitCodeProcess, GetPriorityClass,
    # IsProcessInJob, QueryFullProcessImageName). A handle that has the PROCESS_QUERY_INFORMATION access right
    # is automatically granted PROCESS_QUERY_LIMITED_INFORMATION.Windows Server 2003 and Windows XP: This
    # access right is not supported.
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

    # Required to set certain information about a process, such as its priority class (see SetPriorityClass).
    PROCESS_SET_INFORMATION = 0x0200
    PROCESS_SET_LIMITED_INFORMATION = 0x2000

    # Required to set memory limits using SetProcessWorkingSetSize.
    PROCESS_SET_QUOTA = 0x0100

    # Required to suspend or resume a process.
    PROCESS_SUSPEND_RESUME = 0x0800

    # Required to terminate a process using TerminateProcess.
    PROCESS_TERMINATE = 0x0800

    # Required to perform an operation on the address space of a process (see VirtualProtectEx and WriteProcessMemory).
    PROCESS_VM_OPERATION = 0x0008

    # Required to read memory in a process using ReadProcessMemory.
    PROCESS_VM_READ = 0x0010

    # Required to write to memory in a process using WriteProcessMemory.
    PROCESS_VM_WRITE = 0x0020
