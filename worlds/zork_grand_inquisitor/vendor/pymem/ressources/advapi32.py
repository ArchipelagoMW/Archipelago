import ctypes

import pymem.ressources.structure

try:
    dll = ctypes.WinDLL('advapi32.dll')
except AttributeError:
    class MockObject:
        def __getattr__(self, item):
            return self

    dll = MockObject()

#: The LookupPrivilegeValue function retrieves the locally unique identifier (LUID) used on a specified system to
#: locally represent the specified privilege name.
#:
#: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-lookupprivilegevaluea
LookupPrivilegeValue = dll.LookupPrivilegeValueW
LookupPrivilegeValue.argtypes = (
    ctypes.c_wchar_p,  # system name
    ctypes.c_wchar_p,  # name
    ctypes.POINTER(pymem.ressources.structure.LUID),
)
LookupPrivilegeValue.restype = ctypes.c_long

#: The LookupPrivilegeName function retrieves the name that corresponds to the privilege represented on a specific
#: system by a specified locally unique identifier (LUID).
#:
#: https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-lookupprivilegenamea
LookupPrivilegeName = dll.LookupPrivilegeNameW
LookupPrivilegeName.argtypes = (
    ctypes.c_wchar_p,  # lpSystemName
    ctypes.POINTER(pymem.ressources.structure.LUID),  # lpLuid
    ctypes.c_wchar_p,  # lpName
    ctypes.POINTER(ctypes.c_ulong),  # cchName
)
LookupPrivilegeName.restype = ctypes.c_long


#: The OpenProcessToken function opens the access token associated with a process.
#:
#: https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken
OpenProcessToken = dll.OpenProcessToken
OpenProcessToken.argtypes = (
    ctypes.c_void_p,
    ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_void_p)
)
OpenProcessToken.restype = ctypes.c_long


#: The AdjustTokenPrivileges function enables or disables privileges in the specified access token.
#: Enabling or disabling privileges in an access token requires TOKEN_ADJUST_PRIVILEGES access.
#:
#: https://docs.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-adjusttokenprivileges
AdjustTokenPrivileges = dll.AdjustTokenPrivileges
AdjustTokenPrivileges.restype = ctypes.c_long
AdjustTokenPrivileges.argtypes = (
    ctypes.c_void_p,  # TokenHandle
    ctypes.c_long,  # DisableAllPrivileges
    pymem.ressources.structure.PTOKEN_PRIVILEGES,  # NewState (optional)
    ctypes.c_ulong,  # BufferLength of PreviousState
    pymem.ressources.structure.PTOKEN_PRIVILEGES,  # PreviousState (out, optional)
    ctypes.POINTER(ctypes.c_ulong),  # ReturnLength
)
