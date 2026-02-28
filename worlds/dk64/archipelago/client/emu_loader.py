"""Loader script for tracking the success of tests."""

import ctypes
import platform
import os
import glob
from typing import Optional, Set, Tuple, List, Dict, Any
from enum import IntEnum, auto
from archipelago.client.common import DK64MemoryMap
from archipelago.client.ptrace import check_and_fix_ptrace_scope

try:
    from CommonClient import logger
except ImportError:
    import logging

    logger = logging.getLogger(__name__)


def sanitize_and_trim(input_string: str, max_length: int = 0x1F):
    """Sanitize and trim a string for safe memory writing."""
    normalized = input_string.replace("'", "").replace("`", "").replace("'", "").strip()
    sanitized = "".join(e for e in normalized if e.isalnum() or e == " ").strip()
    return sanitized.upper()[:max_length]


# Heavily based on the autoconnector work in GSTHD by JXJacob

# Detect operating system
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Windows API constants and structures
if IS_WINDOWS:
    import ctypes.wintypes

    PROCESS_VM_READ = 0x0010
    PROCESS_VM_WRITE = 0x0020
    PROCESS_VM_OPERATION = 0x0008
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    TH32CS_SNAPMODULE = 0x00000008
    TH32CS_SNAPMODULE32 = 0x00000010
    TH32CS_SNAPPROCESS = 0x00000002
    MAX_PATH = 260

    # Structures for Windows API
    class MODULEENTRY32(ctypes.Structure):
        """Module entry structure for Windows API."""

        _fields_ = [
            ("dwSize", ctypes.wintypes.DWORD),
            ("th32ModuleID", ctypes.wintypes.DWORD),
            ("th32ProcessID", ctypes.wintypes.DWORD),
            ("GlblcntUsage", ctypes.wintypes.DWORD),
            ("ProccntUsage", ctypes.wintypes.DWORD),
            ("modBaseAddr", ctypes.POINTER(ctypes.wintypes.BYTE)),
            ("modBaseSize", ctypes.wintypes.DWORD),
            ("hModule", ctypes.wintypes.HMODULE),
            ("szModule", ctypes.c_char * 256),
            ("szExePath", ctypes.c_char * 260),
        ]

    class PROCESSENTRY32(ctypes.Structure):
        """Process entry structure for Windows API."""

        _fields_ = [
            ("dwSize", ctypes.wintypes.DWORD),
            ("cntUsage", ctypes.wintypes.DWORD),
            ("th32ProcessID", ctypes.wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.POINTER(ctypes.wintypes.ULONG)),
            ("th32ModuleID", ctypes.wintypes.DWORD),
            ("cntThreads", ctypes.wintypes.DWORD),
            ("th32ParentProcessID", ctypes.wintypes.DWORD),
            ("pcPriClassBase", ctypes.wintypes.LONG),
            ("dwFlags", ctypes.wintypes.DWORD),
            ("szExeFile", ctypes.c_char * MAX_PATH),
        ]

    def _get_windows_processes() -> List[Dict[str, Any]]:
        """Get running processes on Windows using native API."""
        processes: List[Dict[str, Any]] = []

        snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snapshot == -1:
            return processes

        try:
            pe32 = PROCESSENTRY32()
            pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)

            if ctypes.windll.kernel32.Process32First(snapshot, ctypes.byref(pe32)):
                while True:
                    try:
                        process_name = pe32.szExeFile.decode("utf-8")
                        processes.append({"name": process_name, "pid": pe32.th32ProcessID})
                    except UnicodeDecodeError:
                        # Skip processes with invalid names
                        pass

                    if not ctypes.windll.kernel32.Process32Next(snapshot, ctypes.byref(pe32)):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snapshot)

        return processes


def get_running_processes() -> List[Dict[str, Any]]:
    """Get list of running processes using native OS methods."""
    processes: List[Dict[str, Any]] = []

    if IS_WINDOWS:
        processes = _get_windows_processes()
    elif IS_LINUX:
        processes = _get_linux_processes()

    return processes


def _get_linux_processes() -> List[Dict[str, Any]]:
    """Get running processes on Linux by reading /proc."""
    processes: List[Dict[str, Any]] = []

    try:
        for pid_dir in glob.glob("/proc/[0-9]*"):
            try:
                pid = int(os.path.basename(pid_dir))

                # Read process name from /proc/pid/comm
                comm_path = os.path.join(pid_dir, "comm")
                if os.path.exists(comm_path):
                    with open(comm_path, "r") as f:
                        process_name = f.read().strip()
                        processes.append({"name": process_name, "pid": pid})
            except (ValueError, OSError, IOError):
                # Skip invalid PIDs or inaccessible processes
                continue
    except OSError:
        pass

    return processes


class ModuleInfo:
    """Info relating to a module in the process."""

    name: str
    lpBaseOfDll: int | None

    def __init__(self, name: str, lpBaseOfDll: int | None):
        """Initialize with the module name and base address."""
        self.name = name
        self.lpBaseOfDll = lpBaseOfDll


class ProcessMemory:
    """Class to handle process memory operations using ctypes on Windows and Linux."""

    def __init__(self, process_name: str):
        """Initialize with the process name."""
        self.process_name = process_name
        self.process_handle = None
        self.process_id = None
        self.mem_fd = None  # File descriptor for Linux /proc/pid/mem
        self._attach_to_process()

    def _attach_to_process(self):
        """Attach to the process by name."""
        processes = get_running_processes()

        for proc in processes:
            if proc["name"] and proc["name"].lower().startswith(self.process_name.lower()):
                self.process_id = proc["pid"]

                if IS_WINDOWS:
                    self.process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION | PROCESS_QUERY_INFORMATION, False, self.process_id)
                    if not self.process_handle:
                        raise Exception(f"Failed to open process {self.process_name}")
                elif IS_LINUX:
                    # On Linux, proactively check ptrace scope before attempting to attach
                    check_and_fix_ptrace_scope()

                    # Open /proc/pid/mem as a file descriptor for atomic pread/pwrite operations
                    try:
                        self.mem_fd = os.open(f"/proc/{self.process_id}/mem", os.O_RDWR)
                    except (OSError, IOError) as e:
                        # Check if this is a permission issue (errno 1=EPERM, errno 13=EACCES)
                        if e.errno in (1, 13):
                            # Try one more time after fixing ptrace scope
                            if check_and_fix_ptrace_scope():
                                try:
                                    self.mem_fd = os.open(f"/proc/{self.process_id}/mem", os.O_RDWR)
                                except (OSError, IOError) as retry_e:
                                    raise Exception(f"Failed to open memory file for process {self.process_name} after fixing ptrace: {retry_e}")
                            else:
                                raise Exception(f"Failed to open memory file for process {self.process_name}: {e}. Ptrace restrictions may be blocking access.")
                        else:
                            raise Exception(f"Failed to open memory file for process {self.process_name}: {e}")
                return
        raise Exception(f"Process {self.process_name} not found")

    def list_modules(self) -> List[ModuleInfo]:
        """List modules in the process."""
        modules: List[ModuleInfo] = []

        if IS_WINDOWS:
            return self._list_modules_windows()
        elif IS_LINUX:
            return self._list_modules_linux()

        return modules

    def _list_modules_windows(self) -> List[ModuleInfo]:
        """List modules on Windows."""
        modules: List[ModuleInfo] = []
        if not self.process_handle or not self.process_id:
            return modules

        snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, self.process_id)

        if snapshot == -1:
            return modules

        try:
            me32 = MODULEENTRY32()
            me32.dwSize = ctypes.sizeof(MODULEENTRY32)

            if ctypes.windll.kernel32.Module32First(snapshot, ctypes.byref(me32)):
                while True:
                    module_info = ModuleInfo(name=me32.szModule.decode("utf-8"), lpBaseOfDll=ctypes.cast(me32.modBaseAddr, ctypes.c_void_p).value)
                    modules.append(module_info)

                    if not ctypes.windll.kernel32.Module32Next(snapshot, ctypes.byref(me32)):
                        break
        finally:
            ctypes.windll.kernel32.CloseHandle(snapshot)

        return modules

    def _list_modules_linux(self) -> List[ModuleInfo]:
        """List modules on Linux by reading /proc/pid/maps."""
        modules: List[ModuleInfo] = []
        if not self.process_id:
            return modules

        try:
            with open(f"/proc/{self.process_id}/maps", "r") as maps_file:
                seen_modules: Set[str] = set()
                for line in maps_file:
                    parts = line.strip().split()
                    if len(parts) >= 6:
                        address_range = parts[0]
                        permissions = parts[1]
                        pathname = parts[5] if len(parts) > 5 else ""

                        # Only include executable mappings with file paths
                        if "x" in permissions and pathname and pathname != "[vdso]" and not pathname.startswith("["):
                            module_name = os.path.basename(pathname)
                            if module_name not in seen_modules:
                                start_addr = int(address_range.split("-")[0], 16)
                                module_info = ModuleInfo(name=module_name, lpBaseOfDll=start_addr)
                                modules.append(module_info)
                                seen_modules.add(module_name)
        except (OSError, IOError):
            pass

        return modules

    def read_bytes(self, address: int, size: int) -> bytes:
        """Read bytes from process memory."""
        if IS_WINDOWS:
            return self._read_bytes_windows(address, size)
        elif IS_LINUX:
            return self._read_bytes_linux(address, size)
        else:
            raise Exception("Unsupported operating system")

    def _read_bytes_windows(self, address: int, size: int) -> bytes:
        """Read bytes from process memory on Windows."""
        if not self.process_handle:
            raise Exception("Process not attached")

        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.wintypes.DWORD(0)

        result = ctypes.windll.kernel32.ReadProcessMemory(self.process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read))

        if not result:
            raise Exception(f"Failed to read memory at address 0x{address:08x}")

        return buffer.raw[: bytes_read.value]

    def _read_bytes_linux(self, address: int, size: int) -> bytes:
        """Read bytes from process memory on Linux."""
        if self.mem_fd is None:
            raise Exception("Process not attached")

        try:
            data = os.pread(self.mem_fd, size, address)
            if len(data) != size:
                raise Exception(f"Failed to read {size} bytes at address 0x{address:08x}")
            return data
        except (OSError, IOError) as e:
            raise Exception(f"Failed to read memory at address 0x{address:08x}: {e}")

    def write_bytes(self, address: int, data: bytes, size: int):
        """Write bytes to process memory."""
        if IS_WINDOWS:
            self._write_bytes_windows(address, data, size)
        elif IS_LINUX:
            self._write_bytes_linux(address, data, size)
        else:
            raise Exception("Unsupported operating system")

    def _write_bytes_windows(self, address: int, data: bytes, size: int):
        """Write bytes to process memory on Windows."""
        if not self.process_handle:
            raise Exception("Process not attached")

        bytes_written = ctypes.wintypes.DWORD(0)

        result = ctypes.windll.kernel32.WriteProcessMemory(self.process_handle, ctypes.c_void_p(address), data, size, ctypes.byref(bytes_written))

        if not result:
            error_code = ctypes.windll.kernel32.GetLastError()
            raise Exception(f"WriteProcessMemory failed at 0x{address:08x}, error: {error_code}")

    def _write_bytes_linux(self, address: int, data: bytes, size: int):
        """Write bytes to process memory on Linux."""
        if self.mem_fd is None:
            raise Exception("Process not attached")

        try:
            written = os.pwrite(self.mem_fd, data[:size], address)
            if written != size:
                raise Exception(f"Failed to write {size} bytes at address 0x{address:08x}")
        except (OSError, IOError) as e:
            raise Exception(f"Failed to write memory at address 0x{address:08x}: {e}")

    def read_int(self, address: int) -> int:
        """Read a 4-byte integer from memory."""
        data = self.read_bytes(address, 4)
        return int.from_bytes(data, "little")

    def read_longlong(self, address: int) -> int:
        """Read an 8-byte long long from memory."""
        data = self.read_bytes(address, 8)
        return int.from_bytes(data, "little")

    def close(self):
        """Close the process handle or file."""
        if IS_WINDOWS and self.process_handle:
            ctypes.windll.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
        elif IS_LINUX and self.mem_fd is not None:
            os.close(self.mem_fd)
            self.mem_fd = None


class Emulators(IntEnum):
    """Emulator enum."""

    Project64 = auto()
    BizHawk = auto()
    Project64_v4 = auto()
    RMG = auto()
    Simple64 = auto()
    ParallelLauncher = auto()
    ParallelLauncher903 = auto()
    RetroArch = auto()


class EmulatorInfo:
    """Class to store emulator information."""

    def __init__(
        self,
        id: Emulators,
        readable_emulator_name: str,
        process_name: str,
        find_dll: bool,
        dll_name: Optional[str],
        additional_lookup: bool,
        lower_offset_range: int,
        upper_offset_range: int,
        range_step: int = 16,
        extra_offset: int = 0,
        linux_dll_name: Optional[str] = None,
    ):
        """Initialize with given parameters."""
        self.id = id
        self.readable_emulator_name = readable_emulator_name
        self.process_name = process_name
        self.find_dll = find_dll
        self.dll_name = dll_name
        self.linux_dll_name = linux_dll_name
        self.additional_lookup = additional_lookup
        self.lower_offset_range = lower_offset_range
        self.upper_offset_range = upper_offset_range
        self.range_step = range_step
        self.extra_offset = extra_offset
        self.connected_process: Optional[ProcessMemory] = None
        self.connected_offset: Optional[int] = None
        self.connection_error: Optional[str] = None
        self.runtime_error: Optional[str] = None

    def get_library_name(self) -> Optional[str]:
        """Get the appropriate library name for the current platform."""
        if IS_LINUX and self.linux_dll_name:
            return self.linux_dll_name
        return self.dll_name

    def get_possible_library_names(self) -> List[str]:
        """Get a list of possible library names to search for."""
        names: List[str] = []
        primary_name = self.get_library_name()
        if primary_name:
            names.append(primary_name)

        # Add common variations on Linux
        if IS_LINUX and self.dll_name:
            # Convert .dll to .so
            if self.dll_name.endswith(".dll"):
                so_name = self.dll_name[:-4] + ".so"
                if so_name not in names:
                    names.append(so_name)

            # Add lib prefix if not present
            if not self.dll_name.startswith("lib"):
                lib_name = "lib" + self.dll_name
                if lib_name not in names:
                    names.append(lib_name)
                # Also try with .so extension
                if lib_name.endswith(".dll"):
                    lib_so_name = lib_name[:-4] + ".so"
                    if lib_so_name not in names:
                        names.append(lib_so_name)

        return [name for name in names if name]  # Filter out None values

    def disconnect(self):
        """Disconnect emulator from process management."""
        if self.connected_process:
            self.connected_process.close()
        self.connected_offset = None
        self.connected_process = None

    def raiseError(self, msg: str):
        """Raise an error and log it."""
        print(msg)
        self.connection_error = msg

    def attach_to_emulator(self) -> Optional[Tuple[ProcessMemory, int]]:
        """Grab  memory addresses of where emulated RDRAM is."""
        # Reset
        self.connected_process = None
        self.connected_offset = None
        # Find process by name
        target_proc = None
        processes = get_running_processes()

        for proc in processes:
            if proc["name"] and proc["name"].lower().startswith(self.process_name.lower()):
                target_proc = proc
                break
        if not target_proc:
            self.raiseError(f"Could not find process '{self.process_name}'")
            return None

        try:
            pm = ProcessMemory(target_proc["name"])
        except Exception as e:
            self.raiseError(f"Failed to attach to process: {str(e)}")
            return None

        address_dll = 0
        if self.find_dll:
            possible_names = self.get_possible_library_names()
            for module in pm.list_modules():
                for lib_name in possible_names:
                    if module.name.lower() == lib_name.lower() and module.lpBaseOfDll:
                        address_dll = module.lpBaseOfDll
                        break
                if address_dll != 0:
                    break

            if address_dll == 0 and self.id == Emulators.BizHawk:
                address_dll = 2024407040  # fallback guess
            elif address_dll == 0:
                searched_names = ", ".join(possible_names)
                self.raiseError(f"Could not find any of [{searched_names}] in {self.readable_emulator_name}")
                return None

        has_seen_nonzero = False
        for pot_off in range(self.lower_offset_range, self.upper_offset_range, self.range_step):
            if self.additional_lookup:
                rom_addr_start = address_dll + pot_off
                try:
                    read_address = pm.read_longlong(rom_addr_start)
                except Exception:
                    continue
                if read_address != 0:
                    has_seen_nonzero = True
            else:
                read_address = address_dll + pot_off

            addr = read_address + self.extra_offset + 0x759290

            try:
                test_value = pm.read_int(addr)
            except Exception:
                continue
            if test_value != 0:
                has_seen_nonzero = True
            if test_value == 0x52414D42:
                self.connected_process = pm
                self.connected_offset = read_address + self.extra_offset
                self.writeBytes(0x807ED6A4, 4, 1)  # Connection validation
                return (pm, read_address + self.extra_offset)

        if not has_seen_nonzero:
            self.raiseError(f"Could not read any data from {self.readable_emulator_name}")

        return None

    def readBytes(self, address: int, size: int) -> int:
        """Read a series of bytes and cast to an int with N64 address fixing."""
        if self.connected_process is None or self.connected_offset is None:
            self.runtime_error = "Not connected to a process, exiting"
            raise Exception(self.runtime_error)
        if address & 0x80000000:
            address &= 0x7FFFFFFF

        # Apply N64 address fixing based on size
        if size == 1:  # 8-bit operation
            remainder = address % 4
            if remainder == 0:
                address += 3
            elif remainder == 1:
                address += 1
            elif remainder == 2:
                address -= 1
            elif remainder == 3:
                address -= 3
        elif size == 2:  # 16-bit operation
            remainder = address % 4
            if remainder in (2, 3):
                address -= 2
            elif remainder in (0, 1):
                address += 2
        # 32-bit operations (size == 4) don't need address fixing

        mem_address = self.connected_offset + address
        data = self.connected_process.read_bytes(mem_address, size)
        value = int.from_bytes(data, "little")
        return value

    def writeBytes(self, address: int, size: int, value: int):
        """Write a series of bytes to memory with N64 address fixing."""
        if self.connected_process is None or self.connected_offset is None:
            self.runtime_error = "Not connected to a process, exiting"
            raise Exception(self.runtime_error)
        if address & 0x80000000:
            address &= 0x7FFFFFFF

        # Apply N64 address fixing based on size
        if size == 1:  # 8-bit operation
            remainder = address % 4
            if remainder == 0:
                address += 3
            elif remainder == 1:
                address += 1
            elif remainder == 2:
                address -= 1
            elif remainder == 3:
                address -= 3
        elif size == 2:  # 16-bit operation
            remainder = address % 4
            if remainder in (2, 3):
                address -= 2
            elif remainder in (0, 1):
                address += 2
        # 32-bit operations (size == 4) don't need address fixing

        mem_address = self.connected_offset + address
        data = value.to_bytes(size, byteorder="little")  # or "big"
        self.connected_process.write_bytes(mem_address, data, size)

    def read_u8(self, address: int) -> int:
        """Read an 8-bit unsigned integer from memory."""
        return self.readBytes(address, 1)

    def read_u16(self, address: int) -> int:
        """Read a 16-bit unsigned integer from memory."""
        return self.readBytes(address, 2)

    def read_u32(self, address: int) -> int:
        """Read a 32-bit unsigned integer from memory."""
        return self.readBytes(address, 4)

    def write_u8(self, address: int, value: int):
        """Write an 8-bit unsigned integer to memory."""
        self.writeBytes(address, 1, value)

    def write_u16(self, address: int, value: int):
        """Write a 16-bit unsigned integer to memory."""
        self.writeBytes(address, 2, value)

    def write_u32(self, address: int, value: int):
        """Write a 32-bit unsigned integer to memory."""
        self.writeBytes(address, 4, value)

    def read_bytestring(self, address: int, length: int) -> str:
        """Read a bytestring from memory."""
        result = ""
        for i in range(length):
            byte_val = self.read_u8(address + i)
            if byte_val == 0:  # Null terminator
                break
            result += chr(byte_val)
        return result

    def write_bytestring(self, address: int, data: str):
        """Write a bytestring to memory."""
        # Always sanitize the input data before writing to memory
        sanitized_data = sanitize_and_trim(data)
        for i, char in enumerate(sanitized_data):
            self.write_u8(address + i, ord(char))
        # Add null terminator
        self.write_u8(address + len(sanitized_data), 0)

    def validate_rom(self) -> bool:
        """Validate the ROM."""
        return (self.read_u8(DK64MemoryMap.rom_flags) & DK64MemoryMap.rom_flag_ap_status) != 0


EMULATOR_CONFIGS = {
    Emulators.Project64_v4: EmulatorInfo(Emulators.Project64_v4, "Project64 4.0", "project64", False, None, False, 0xFDD00000, 0xFE1FFFFF),
    Emulators.BizHawk: EmulatorInfo(Emulators.BizHawk, "Bizhawk", "emuhawk", True, "mupen64plus.dll", False, 0x5A000, 0x5658DF, linux_dll_name="libmupen64plus.so"),
    Emulators.RMG: EmulatorInfo(Emulators.RMG, "Rosalie's Mupen GUI", "rmg", True, "mupen64plus.dll", True, 0x29C15D8, 0x2FC15D8, extra_offset=0x80000000, linux_dll_name="libmupen64plus.so"),
    Emulators.Simple64: EmulatorInfo(Emulators.Simple64, "simple64", "simple64-gui", True, "libmupen64plus.dll", True, 0x1380000, 0x29C95D8, linux_dll_name="libmupen64plus.so"),
    Emulators.ParallelLauncher: EmulatorInfo(
        Emulators.ParallelLauncher, "Parallel Launcher", "retroarch", True, "parallel_n64_next_libretro.dll", True, 0x845000, 0xD56000, linux_dll_name="parallel_n64_next_libretro.so"
    ),
    Emulators.ParallelLauncher903: EmulatorInfo(
        Emulators.ParallelLauncher903, "Parallel Launcher (9.0.3+)", "retroarch", True, "parallel_n64_next_libretro.dll", True, 0x1400000, 0x1800000, linux_dll_name="parallel_n64_next_libretro.so"
    ),
    Emulators.RetroArch: EmulatorInfo(
        Emulators.RetroArch, "RetroArch", "retroarch", True, "mupen64plus_next_libretro.dll", True, 0, 0xFFFFFF, range_step=4, linux_dll_name="mupen64plus_next_libretro.so"
    ),
    Emulators.Project64: EmulatorInfo(Emulators.Project64, "Project64", "project64", False, None, False, 0xDFD00000, 0xE01FFFFF),
}


def attachWrapper(emu: Emulators) -> EmulatorInfo:
    """Wrap function for attaching to an emulator."""
    EMULATOR_CONFIGS[emu].attach_to_emulator()
    return EMULATOR_CONFIGS[emu]


def connect_to_emulator() -> Optional[EmulatorInfo]:
    """Try to connect to any available emulator and return the connected instance."""
    for emu in Emulators:
        try:
            emulator_info = EMULATOR_CONFIGS[emu]
            if emulator_info.attach_to_emulator():
                logger.info(f"Connected to {emulator_info.readable_emulator_name}")
                print(f"Connected to {emulator_info.readable_emulator_name}")
                return emulator_info
        except Exception as e:
            logger.info(f"Failed to connect to {EMULATOR_CONFIGS[emu].readable_emulator_name}: {str(e)}")
            continue
    return None


class EmuLoaderClient:
    """Drop-in replacement client for PJ64Client using direct memory access."""

    def __init__(self):
        """Initialize the EmuLoaderClient."""
        self.emulator_info: Optional[EmulatorInfo] = None
        self.connected = False

    def connect(self) -> bool:
        """Connect to an available emulator."""
        self.emulator_info = connect_to_emulator()
        self.connected = self.emulator_info is not None
        return self.connected

    def disconnect(self):
        """Disconnect from the emulator."""
        if self.emulator_info:
            self.emulator_info.disconnect()
        self.connected = False
        self.emulator_info = None

    def is_connected(self) -> bool:
        """Check if connected to an emulator.

        This serves as a safety check for the memory access methods below, so pyright ignore annotations have been added to them. Be careful if editing this method!
        """
        return self.connected and self.emulator_info is not None

    # Direct memory access methods
    def read_u8(self, address: int) -> int:
        """Read an 8-bit unsigned integer from memory."""
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        return self.emulator_info.read_u8(address)  # pyright: ignore[reportOptionalMemberAccess]

    def read_u16(self, address: int) -> int:
        """Read a 16-bit unsigned integer from memory."""
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        return self.emulator_info.read_u16(address)  # pyright: ignore[reportOptionalMemberAccess]

    def read_u32(self, address: int) -> int:
        """Read a 32-bit unsigned integer from memory."""
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        return self.emulator_info.read_u32(address)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u8(self, address: int, value: int):
        """Write an 8-bit unsigned integer to memory."""
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        self.emulator_info.write_u8(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u16(self, address: int, value: int):
        """Write a 16-bit unsigned integer to memory."""
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        self.emulator_info.write_u16(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def write_u32(self, address: int, value: int):
        """Write a 32-bit unsigned integer to memory."""
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        self.emulator_info.write_u32(address, value)  # pyright: ignore[reportOptionalMemberAccess]

    def read_bytestring(self, address: int, length: int) -> str:
        """Read a bytestring from memory."""
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        return self.emulator_info.read_bytestring(address, length)  # pyright: ignore[reportOptionalMemberAccess]

    def write_bytestring(self, address: int, data: str):
        """Write a bytestring to memory."""
        if not self.is_connected():
            raise Exception("Not connected to emulator")
        self.emulator_info.write_bytestring(address, data)  # pyright: ignore[reportOptionalMemberAccess]

    def validate_rom(self) -> bool:
        """Validate the ROM by checking name and optional memory location."""
        if not self.is_connected():
            return False
        return self.emulator_info.validate_rom()  # pyright: ignore[reportOptionalMemberAccess]


# Example usage and testing code (commented out)
# # Try to connect to each emu type and see if it works
# for emu in Emulators:
#     try:
#         EMULATOR_CONFIGS[emu].attach_to_emulator()
#         if EMULATOR_CONFIGS[emu].connected_process is not None:
#             print(f"Connected to {EMULATOR_CONFIGS[emu].readable_emulator_name}")
#     except Exception as e:
#         print(f"Error connecting to {EMULATOR_CONFIGS[emu].readable_emulator_name}: {str(e)}")
