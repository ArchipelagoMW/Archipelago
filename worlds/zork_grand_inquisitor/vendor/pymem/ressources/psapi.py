import ctypes

try:
    dll = ctypes.WinDLL('psapi.dll')
except AttributeError:
    class MockObject:
        def __getattr__(self, item):
            return self

    dll = MockObject()

#: Retrieves a handle for each module in the specified process that meets the specified filter criteria.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms682633(v=vs.85).aspx
EnumProcessModulesEx = dll.EnumProcessModulesEx
EnumProcessModulesEx.restype = ctypes.c_bool


#: Retrieves a handle for each module in the specified process that meets the specified filter criteria.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms683196(v=vs.85).aspx
GetModuleBaseNameA = dll.GetModuleBaseNameA
GetModuleBaseNameA.restype = ctypes.c_ulonglong


#: Retrieves information about the specified module in the MODULEINFO structure.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms683201(v=vs.85).aspx
GetModuleInformation = dll.GetModuleInformation
GetModuleInformation.restype = ctypes.c_bool

#: Retrieves information about the specified module in the MODULEINFO structure.
#:
#: https://msdn.microsoft.com/en-us/library/windows/desktop/ms683198(v=vs.85).aspx
GetModuleFileNameExA = dll.GetModuleFileNameExA
GetModuleFileNameExA.restype = ctypes.c_ulong
