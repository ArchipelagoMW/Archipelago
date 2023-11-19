import enum
import locale
import struct
import ctypes
# these are available on linux also (doc ci building)
import ctypes.wintypes

import pymem.ressources.psapi
import pymem.ressources.ntdll


class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", ctypes.c_ulong),
        ("HighPart", ctypes.c_long)
    ]


class LUID_AND_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ("Luid", LUID),
        ("Attributes", ctypes.c_ulong),
    ]

    def is_enabled(self):
        return bool(self.attributes & SE_TOKEN_PRIVILEGE.SE_PRIVILEGE_ENABLED)

    def enable(self):
        self.attributes |= SE_TOKEN_PRIVILEGE.SE_PRIVILEGE_ENABLED

    def get_name(self):
        import pymem.ressources.advapi32

        size = ctypes.c_ulong(10240)
        buf = ctypes.create_unicode_buffer(size.value)
        res = pymem.ressources.advapi32.LookupPrivilegeName(None, self.LUID, buf, size)
        if res == 0:
            raise RuntimeError("Could not LookupPrivilegeName")
        return buf[:size.value]

    def __str__(self):
        res = self.get_name()
        if self.is_enabled():
            res += ' (enabled)'
        return res


class TOKEN_PRIVILEGES(ctypes.Structure):
    _fields_ = [
        ("count", ctypes.c_ulong),
        ("Privileges", LUID_AND_ATTRIBUTES * 0)
    ]

    def get_array(self):
        array_type = LUID_AND_ATTRIBUTES * self.count
        privileges = ctypes.cast(self.Privileges, ctypes.POINTER(array_type)).contents
        return privileges

    def __iter__(self):
        return iter(self.get_array())


PTOKEN_PRIVILEGES = ctypes.POINTER(TOKEN_PRIVILEGES)

MAX_MODULE_NAME32 = 255


class ModuleEntry32(ctypes.Structure):
    """Describes an entry from a list of the modules belonging to the specified process.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms684225%28v=vs.85%29.aspx
    """
    _fields_ = [
        ('dwSize', ctypes.c_ulong),
        ('th32ModuleID', ctypes.c_ulong),
        ('th32ProcessID', ctypes.c_ulong),
        ('GlblcntUsage', ctypes.c_ulong),
        ('ProccntUsage', ctypes.c_ulong),
        ('modBaseAddr', ctypes.POINTER(ctypes.c_ulonglong)),
        ('modBaseSize', ctypes.c_ulong),
        ('hModule', ctypes.c_ulong),
        ('szModule', ctypes.c_char * (MAX_MODULE_NAME32 + 1)),
        ('szExePath', ctypes.c_char * ctypes.wintypes.MAX_PATH)
    ]

    def __init__(self, *args, **kwds):
        super(ModuleEntry32, self).__init__(*args, **kwds)
        self.dwSize = ctypes.sizeof(self)

    @property
    def base_address(self):
        return ctypes.addressof(self.modBaseAddr.contents)

    @property
    def name(self):
        return self.szModule.decode(locale.getpreferredencoding())


LPMODULEENTRY32 = ctypes.POINTER(ModuleEntry32)


class ProcessEntry32(ctypes.Structure):
    """Describes an entry from a list of the processes residing in the system address space when a snapshot was taken.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms684839(v=vs.85).aspx
    """
    _fields_ = [
        ('dwSize', ctypes.c_ulong),
        ('cntUsage', ctypes.c_ulong),
        ('th32ProcessID', ctypes.c_ulong),
        ('th32DefaultHeapID', ctypes.POINTER(ctypes.c_ulong)),
        ('th32ModuleID', ctypes.c_ulong),
        ('cntThreads', ctypes.c_ulong),
        ('th32ParentProcessID', ctypes.c_ulong),
        ('pcPriClassBase', ctypes.c_ulong),
        ('dwFlags', ctypes.c_ulong),
        ('szExeFile', ctypes.c_char * ctypes.wintypes.MAX_PATH)
    ]

    @property
    def szExeFile(self):
        return self.szExeFile.decode(locale.getpreferredencoding())

    def __init__(self, *args, **kwds):
        super(ProcessEntry32, self).__init__(*args, **kwds)
        self.dwSize = ctypes.sizeof(self)


class FILETIME(ctypes.Structure):
    _fields_ = [
        ("dwLowDateTime", ctypes.c_ulong),
        ("dwHighDateTime", ctypes.c_ulong)
    ]

    @property
    def value(self):
        v = struct.unpack('>Q', struct.pack('>LL', self.dwHighDateTime, self.dwLowDateTime))
        v = v[0]
        return v


class ThreadEntry32(ctypes.Structure):
    """Describes an entry from a list of the threads executing in the system when a snapshot was taken.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms686735(v=vs.85).aspx
    """

    _fields_ = [
        ('dwSize', ctypes.c_ulong),
        ("cntUsage", ctypes.c_ulong),
        ("th32ThreadID", ctypes.c_ulong),
        ("th32OwnerProcessID", ctypes.c_ulong),
        ("tpBasePri", ctypes.c_ulong),
        ("tpDeltaPri", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong)
    ]

    @property
    def szExeFile(self):
        return self.szExeFile.decode(locale.getpreferredencoding())

    # XXX: save it somehow
    @property
    def creation_time(self):
        THREAD_QUERY_INFORMATION = 0x0040
        handle = pymem.ressources.kernel32.OpenThread(
            THREAD_QUERY_INFORMATION, False, self.th32ThreadID
        )

        ctime = FILETIME()
        etime = FILETIME()
        ktime = FILETIME()
        utime = FILETIME()

        pymem.ressources.kernel32.GetThreadTimes(
            handle, ctypes.pointer(ctime), ctypes.pointer(etime), ctypes.pointer(ktime), ctypes.pointer(utime)
        )
        pymem.ressources.kernel32.CloseHandle(handle)
        return ctime.value

    def __init__(self, *args, **kwds):
        super(ThreadEntry32, self).__init__(*args, **kwds)
        self.dwSize = ctypes.sizeof(self)


class PROCESS(enum.IntEnum):
    """Process manipulation flags"""

    #: Required to create a process.
    PROCESS_CREATE_PROCESS = 0x0080
    #: Required to create a thread.
    PROCESS_CREATE_THREAD = 0x0002
    #: PROCESS_DUP_HANDLE
    PROCESS_DUP_HANDLE = 0x0040
    #: Required to retrieve certain information about a process, such as its token, exit code,
    # and priority class (see OpenProcessToken).
    PROCESS_QUERY_INFORMATION = 0x0400
    #: Required to retrieve certain information about a process
    # (see GetExitCodeProcess, GetPriorityClass, IsProcessInJob, QueryFullProcessImageName).
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    #: Required to set certain information about a process, such as its priority class (see SetPriorityClass).
    PROCESS_SET_INFORMATION = 0x0200
    #: Required to set memory limits using SetProcessWorkingSetSize.
    PROCESS_SET_QUOTA = 0x0100
    #: Required to suspend or resume a process.
    PROCESS_SUSPEND_RESUME = 0x0800
    #: Required to terminate a process using TerminateProcess.
    PROCESS_TERMINATE = 0x0001
    #: Required to perform an operation on the address space of a process (see VirtualProtectEx and WriteProcessMemory).
    PROCESS_VM_OPERATION = 0x0008
    #: Required to read memory in a process using ReadProcessMemory.
    PROCESS_VM_READ = 0x0010
    #: Required to write to memory in a process using WriteProcessMemory.
    PROCESS_VM_WRITE = 0x0020
    #: Required to wait for the process to terminate using the wait functions.
    SYNCHRONIZE = 0x00100000
    #: Combines DELETE, READ_CONTROL, WRITE_DAC, and WRITE_OWNER access.
    STANDARD_RIGHTS_REQUIRED = 0x000F0000
    #: All possible access rights for a process object.
    PROCESS_ALL_ACCESS = (
            STANDARD_RIGHTS_REQUIRED | SYNCHRONIZE | 0xFFF
    )
    #: Required to delete the object.
    DELETE = 0x00010000
    #: Required to read information in the security descriptor for the object, not including the information in the
    #: SACL. To read or write the SACL, you must request the ACCESS_SYSTEM_SECURITY access right. For more information
    #: see SACL Access Right.
    READ_CONTROL = 0x00020000
    #: Required to modify the DACL in the security descriptor for the object.
    WRITE_DAC = 0x00040000
    #: Required to change the owner in the security descriptor for the object.
    WRITE_OWNER = 0x00080000


class TOKEN(enum.IntEnum):
    STANDARD_RIGHTS_REQUIRED = 0x000F0000
    TOKEN_ASSIGN_PRIMARY = 0x0001
    TOKEN_DUPLICATE = 0x0002
    TOKEN_IMPERSONATE = 0x0004
    TOKEN_QUERY = 0x0008
    TOKEN_QUERY_SOURCE = 0x0010
    TOKEN_ADJUST_PRIVILEGES = 0x0020
    TOKEN_ADJUST_GROUPS = 0x0040
    TOKEN_ADJUST_DEFAULT = 0x0080
    TOKEN_ADJUST_SESSIONID = 0x0100
    TOKEN_ALL_ACCESS = (
            STANDARD_RIGHTS_REQUIRED |
            TOKEN_ASSIGN_PRIMARY |
            TOKEN_DUPLICATE |
            TOKEN_IMPERSONATE |
            TOKEN_QUERY |
            TOKEN_QUERY_SOURCE |
            TOKEN_ADJUST_PRIVILEGES |
            TOKEN_ADJUST_GROUPS |
            TOKEN_ADJUST_DEFAULT
    )


class SE_TOKEN_PRIVILEGE(enum.IntEnum):
    """An access token contains the security information for a logon session.
    The system creates an access token when a user logs on, and every process executed on behalf of the user has a copy
    of the token.
    """

    SE_PRIVILEGE_ENABLED_BY_DEFAULT = 0x00000001
    SE_PRIVILEGE_ENABLED = 0x00000002
    SE_PRIVILEGE_REMOVED = 0x00000004
    SE_PRIVILEGE_USED_FOR_ACCESS = 0x80000000


class MEMORY_STATE(enum.IntEnum):
    """The type of memory allocation"""
    #: Allocates memory charges (from the overall size of memory and the paging files on disk)
    # for the specified reserved memory pages. The function also guarantees that when the caller later
    # initially accesses the memory, the contents will be zero.
    # Actual physical pages are not allocated unless/until the virtual addresses are actually accessed.
    MEM_COMMIT = 0x1000
    #: XXX
    MEM_FREE = 0x10000
    #: XXX
    MEM_RESERVE = 0x2000
    #: Decommits the specified region of committed pages. After the operation, the pages are in the reserved state.
    #: https://msdn.microsoft.com/en-us/library/windows/desktop/aa366894(v=vs.85).aspx
    MEM_DECOMMIT = 0x4000
    #: Releases the specified region of pages. After the operation, the pages are in the free state.
    #: https://msdn.microsoft.com/en-us/library/windows/desktop/aa366894(v=vs.85).aspx
    MEM_RELEASE = 0x8000


class MEMORY_TYPES(enum.IntEnum):
    #: XXX
    MEM_IMAGE = 0x1000000
    #: XXX
    MEM_MAPPED = 0x40000
    #: XXX
    MEM_PRIVATE = 0x20000


class MEMORY_PROTECTION(enum.IntEnum):
    """The following are the memory-protection options;
    you must specify one of the following values when allocating or protecting a page in memory
    https://msdn.microsoft.com/en-us/library/windows/desktop/aa366786(v=vs.85).aspx"""

    #: Enables execute access to the committed region of pages.
    # An attempt to write to the committed region results in an access violation.
    PAGE_EXECUTE = 0x10
    #: Enables execute or read-only access to the committed region of pages.
    # An attempt to write to the committed region results in an access violation.
    PAGE_EXECUTE_READ = 0x20
    #: Enables execute, read-only, or read/write access to the committed region of pages.
    PAGE_EXECUTE_READWRITE = 0x40
    #: Enables execute, read-only, or copy-on-write access to a mapped view of a file mapping object.
    # An attempt to write to a committed copy-on-write page results in a private
    # copy of the page being made for the process.
    # The private page is marked as PAGE_EXECUTE_READWRITE, and the change is written to the new page.
    PAGE_EXECUTE_WRITECOPY = 0x80
    #: Disables all access to the committed region of pages.
    # An attempt to read from, write to, or execute the committed region results in an access violation.
    PAGE_NOACCESS = 0x01
    #: Enables read-only access to the committed region of pages.
    # An attempt to write to the committed region results in an access violation.
    # If Data Execution Prevention is enabled,
    # an attempt to execute code in the committed region results in an access violation.
    PAGE_READONLY = 0x02
    #: Enables read-only or read/write access to the committed region of pages.
    # If Data Execution Prevention is enabled, attempting to execute code in the
    # committed region results in an access violation.
    PAGE_READWRITE = 0x04
    #: Enables read-only or copy-on-write access to a mapped view of a file mapping object.
    # An attempt to write to a committed copy-on-write page results in a private copy of
    # the page being made for the process. The private page is marked as PAGE_READWRITE,
    # and the change is written to the new page. If Data Execution Prevention is enabled,
    # attempting to execute code in the committed region results in an access violation.
    PAGE_WRITECOPY = 0x08
    #: Pages in the region become guard pages.
    # Any attempt to access a guard page causes the system to
    # raise a STATUS_GUARD_PAGE_VIOLATION exception and turn off the guard page status.
    # Guard pages thus act as a one-time access alarm. For more information, see Creating Guard Pages.
    PAGE_GUARD = 0x100
    #: Sets all pages to be non-cachable.
    # Applications should not use this attribute except when explicitly required for a device.
    # Using the interlocked functions with memory that is mapped with
    # SEC_NOCACHE can result in an EXCEPTION_ILLEGAL_INSTRUCTION exception.
    PAGE_NOCACHE = 0x200
    #: Sets all pages to be write-combined.
    #: Applications should not use this attribute except when explicitly required for a device.
    # Using the interlocked functions with memory that is mapped as write-combined can result in an
    # EXCEPTION_ILLEGAL_INSTRUCTION exception.
    PAGE_WRITECOMBINE = 0x400


SIZE_OF_80387_REGISTERS = 80


class FLOATING_SAVE_AREA(ctypes.Structure):
    """Undocumented ctypes.Structure used for ThreadContext."""
    _fields_ = [
        ('ControlWord', ctypes.c_uint),
        ('StatusWord', ctypes.c_uint),
        ('TagWord', ctypes.c_uint),
        ('ErrorOffset', ctypes.c_uint),
        ('ErrorSelector', ctypes.c_uint),
        ('DataOffset', ctypes.c_uint),
        ('DataSelector', ctypes.c_uint),
        ('RegisterArea', ctypes.c_byte * SIZE_OF_80387_REGISTERS),
        ('Cr0NpxState', ctypes.c_uint)
    ]


MAXIMUM_SUPPORTED_EXTENSION = 512


class ThreadContext(ctypes.Structure):
    """Represents a thread context"""

    _fields_ = [
        ('ContextFlags', ctypes.c_uint),
        ('Dr0', ctypes.c_uint),
        ('Dr1', ctypes.c_uint),
        ('Dr2', ctypes.c_uint),
        ('Dr3', ctypes.c_uint),
        ('Dr6', ctypes.c_uint),
        ('Dr7', ctypes.c_uint),
        ('FloatSave', FLOATING_SAVE_AREA),
        ('SegGs', ctypes.c_uint),
        ('SegFs', ctypes.c_uint),
        ('SegEs', ctypes.c_uint),
        ('SegDs', ctypes.c_uint),
        ('Edi', ctypes.c_uint),
        ('Esi', ctypes.c_uint),
        ('Ebx', ctypes.c_uint),
        ('Edx', ctypes.c_uint),
        ('Ecx', ctypes.c_uint),
        ('Eax', ctypes.c_uint),
        ('Ebp', ctypes.c_uint),
        ('Eip', ctypes.c_uint),
        ('SegCs', ctypes.c_uint),
        ('EFlags', ctypes.c_uint),
        ('Esp', ctypes.c_uint),
        ('SegSs', ctypes.c_uint),
        ('ExtendedRegisters', ctypes.c_byte * MAXIMUM_SUPPORTED_EXTENSION)
    ]


class MODULEINFO(ctypes.Structure):
    """Contains the module load address, size, and entry point.

    attributes:
      lpBaseOfDll
      SizeOfImage
      EntryPoint

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms684229(v=vs.85).aspx
    """

    _fields_ = [
        ("lpBaseOfDll", ctypes.c_void_p),  # remote pointer
        ("SizeOfImage", ctypes.c_ulong),
        ("EntryPoint", ctypes.c_void_p),  # remote pointer
    ]

    def __init__(self, handle):
        self.process_handle = handle

    @property
    def name(self):
        modname = ctypes.c_buffer(ctypes.wintypes.MAX_PATH)
        pymem.ressources.psapi.GetModuleBaseNameA(
            self.process_handle,
            ctypes.c_void_p(self.lpBaseOfDll),
            modname,
            ctypes.sizeof(modname)
        )
        return modname.value.decode(locale.getpreferredencoding())

    @property
    def filename(self):
        _filename = ctypes.c_buffer(ctypes.wintypes.MAX_PATH)
        pymem.ressources.psapi.GetModuleFileNameExA(
            self.process_handle,
            ctypes.c_void_p(self.lpBaseOfDll),
            _filename,
            ctypes.sizeof(_filename)
        )
        return _filename.value.decode(locale.getpreferredencoding())


class SYSTEM_INFO(ctypes.Structure):
    """Contains information about the current computer system.
    This includes the architecture and type of the processor, the number
    of processors in the system, the page size, and other such information.

    https://msdn.microsoft.com/en-us/library/windows/desktop/ms724958(v=vs.85).aspx
    """

    _fields_ = [
        ("wProcessorArchitecture", ctypes.c_ushort),
        ("wReserved", ctypes.c_ushort),
        ("dwPageSize", ctypes.c_ulong),
        ("lpMinimumApplicationAddress", ctypes.c_ulong),
        ("lpMaximumApplicationAddress", ctypes.c_ulonglong),
        ("dwActiveProcessorMask", ctypes.c_ulong),
        ("dwNumberOfProcessors", ctypes.c_ulong),
        ("dwProcessorType", ctypes.c_ulong),
        ("dwAllocationGranularity", ctypes.c_ulong),
        ("wProcessorLevel", ctypes.c_ushort),
        ("wProcessorRevision", ctypes.c_ushort)
    ]


class MEMORY_BASIC_INFORMATION32(ctypes.Structure):
    """Contains information about a range of pages in the virtual address space of a process.
    The VirtualQuery and VirtualQueryEx functions use this structure.

    https://msdn.microsoft.com/en-us/library/windows/desktop/aa366775(v=vs.85).aspx
    """
    _fields_ = [
        ("BaseAddress", ctypes.c_ulong),
        ("AllocationBase", ctypes.c_ulong),
        ("AllocationProtect", ctypes.c_ulong),
        ("RegionSize", ctypes.c_ulong),
        ("State", ctypes.c_ulong),
        ("Protect", ctypes.c_ulong),
        ("Type", ctypes.c_ulong)
    ]

    @property
    def type(self):
        enum_type = [e for e in MEMORY_TYPES if e.value == self.Type] or None
        enum_type = enum_type[0] if enum_type else None
        return enum_type

    @property
    def state(self):
        enum_type = [e for e in MEMORY_STATE if e.value == self.State] or None
        enum_type = enum_type[0] if enum_type else None
        return enum_type

    @property
    def protect(self):
        enum_type = [e for e in MEMORY_PROTECTION if e.value == self.Protect]
        enum_type = enum_type[0] if enum_type else None
        return enum_type


class MEMORY_BASIC_INFORMATION64(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_ulonglong),
        ("AllocationBase", ctypes.c_ulonglong),
        ("AllocationProtect", ctypes.c_ulong),
        ("__alignment1", ctypes.c_ulong),
        ("RegionSize", ctypes.c_ulonglong),
        ("State", ctypes.c_ulong),
        ("Protect", ctypes.c_ulong),
        ("Type", ctypes.c_ulong),
        ("__alignment2", ctypes.c_ulong),
    ]

    @property
    def type(self):
        enum_type = [e for e in MEMORY_TYPES if e.value == self.Type] or None
        enum_type = enum_type[0] if enum_type else None
        return enum_type

    @property
    def state(self):
        enum_type = [e for e in MEMORY_STATE if e.value == self.State] or None
        enum_type = enum_type[0] if enum_type else None
        return enum_type

    @property
    def protect(self):
        enum_type = [e for e in MEMORY_PROTECTION if e.value == self.Protect]
        enum_type = enum_type[0] if enum_type else None
        return enum_type


PTR_SIZE = ctypes.sizeof(ctypes.c_void_p)
if PTR_SIZE == 8:  # 64-bit python
    MEMORY_BASIC_INFORMATION = MEMORY_BASIC_INFORMATION64
elif PTR_SIZE == 4:  # 32-bit python
    MEMORY_BASIC_INFORMATION = MEMORY_BASIC_INFORMATION32


class EnumProcessModuleEX(object):
    """The following are the EnumProcessModuleEX flags

    https://msdn.microsoft.com/ru-ru/library/windows/desktop/ms682633(v=vs.85).aspx
    """
    #: List the 32-bit modules
    LIST_MODULES_32BIT = 0x01
    #: List the 64-bit modules.
    LIST_MODULES_64BIT = 0x02
    #: List all modules.
    LIST_MODULES_ALL = 0x03
    #: Use the default behavior.
    LIST_MODULES_DEFAULT = 0x00


class SECURITY_ATTRIBUTES(ctypes.Structure):
    """The SECURITY_ATTRIBUTES structure contains the security descriptor for an
    object and specifies whether the handle retrieved by specifying this structure
    is inheritable.

    https://msdn.microsoft.com/en-us/library/windows/desktop/aa379560(v=vs.85).aspx
    """
    _fields_ = [('nLength', ctypes.c_ulong),
                ('lpSecurityDescriptor', ctypes.c_void_p),
                ('bInheritHandle', ctypes.c_long)
                ]


LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)


class CLIENT_ID(ctypes.Structure):
    #: http://terminus.rewolf.pl/terminus/structures/ntdll/_CLIENT_ID64_x64.html
    _fields_ = [
        ("UniqueProcess", ctypes.c_void_p),
        ("UniqueThread", ctypes.c_void_p),
    ]


class THREAD_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ExitStatus", pymem.ressources.ntdll.NTSTATUS),
        ("TebBaseAddress", ctypes.c_void_p),
        ("ClientId", CLIENT_ID),
        ("AffinityMask", ctypes.c_long),
        ("Priority", ctypes.c_long),
        ("BasePriority", ctypes.c_long)
    ]


# TEB
class TIB_UNION(ctypes.Union):
    _fields_ = [
        ("FiberData", ctypes.c_void_p),
        ("Version", ctypes.c_ulong),
    ]


class NT_TIB(ctypes.Structure):
    _fields_ = [
        ("ExceptionList", ctypes.c_void_p),  # PEXCEPTION_REGISTRATION_RECORD
        ("StackBase", ctypes.c_void_p),
        ("StackLimit", ctypes.c_void_p),
        ("SubSystemTib", ctypes.c_void_p),
        ("u", TIB_UNION),
        ("ArbitraryUserPointer", ctypes.c_void_p),
        ("Self", ctypes.c_void_p),  # PNTTIB
    ]


class SMALL_TEB(ctypes.Structure):
    _pack_ = 1

    _fields_ = [
        ("NtTib", NT_TIB),
        ("EnvironmentPointer", ctypes.c_void_p),
        ("ClientId", CLIENT_ID),
        ("ActiveRpcHandle", ctypes.c_void_p),
        ("ThreadLocalStoragePointer", ctypes.c_void_p)
    ]
