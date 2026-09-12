#!/usr/bin/env python3
"""
Ys I Chronicles Archipelago Client

Connects to the PC game (ys1plus.exe) via memory read/write tools and
to the Archipelago server for multiworld randomizer functionality.

Supports:
- macOS via CrossOver/Wine (subprocess to mem_read.exe/mem_write.exe)
- Windows native (ctypes ReadProcessMemory/WriteProcessMemory)
"""

import abc
import asyncio
import hashlib
import os
import platform
import struct
import tempfile
from typing import Optional, Dict, Set, List

# Archipelago imports
try:
    from CommonClient import CommonContext, server_loop, get_base_parser, gui_enabled
    from NetUtils import ClientStatus
    import Utils
    ARCHIPELAGO_AVAILABLE = True
except ImportError:
    ARCHIPELAGO_AVAILABLE = False

from .items import YS1_ITEMS, YS1_BASE_ID, AP_CODE_TO_GAME_ID, GAME_ID_TO_AP_NAME
from .locations import YS1_LOCATIONS, FLAG_TO_LOCATION, REVERSE_FLAG_LOCATIONS


# =============================================================================
# Constants
# =============================================================================

POLL_INTERVAL = 0.5
GAME_ITEM_COUNT = 52


# =============================================================================
# PC Memory Addresses
# =============================================================================

class PCAddresses:
    """Absolute memory addresses for ys1plus.exe (PC version)."""

    # Player stats
    HP          = 0x5317FC
    MAX_HP      = 0x531800
    STR         = 0x531804
    DEF         = 0x531808
    GOLD        = 0x53180C
    EXP         = 0x531810
    LEVEL       = 0x531814

    # Item arrays
    ITEM_ARRAY_1_BASE = 0x531990   # Ownership, DWORD[52]
    ITEM_ARRAY_2_BASE = 0x53207C   # Visibility, DWORD[52]

    # Boss flags
    BOSS_JENOCRES           = 0x531950
    BOSS_NYGTILGER          = 0x531958
    BOSS_VAGULLION          = 0x531AC0
    BOSS_PICTIMOS           = 0x531968
    BOSS_KHONSCLARD         = 0x531978
    BOSS_YOGLEKS_OMULGUN    = 0x531ACC
    BOSS_DARK_FACT          = 0x531A98

    @classmethod
    def item_array1_addr(cls, game_id: int) -> int:
        return cls.ITEM_ARRAY_1_BASE + game_id * 4

    @classmethod
    def item_array2_addr(cls, game_id: int) -> int:
        return cls.ITEM_ARRAY_2_BASE + game_id * 4


# =============================================================================
# Memory Interface (Abstract)
# =============================================================================

class MemoryInterface(abc.ABC):
    @abc.abstractmethod
    async def connect(self) -> bool: ...

    @abc.abstractmethod
    async def read_u32(self, address: int) -> int: ...

    @abc.abstractmethod
    async def write_u32(self, address: int, value: int) -> bool: ...

    @abc.abstractmethod
    async def read_u32_batch(self, address: int, count: int) -> List[int]: ...

    @abc.abstractmethod
    async def is_connected(self) -> bool: ...


# =============================================================================
# Wine/CrossOver Memory Interface (macOS)
# =============================================================================

class WineMemoryInterface(MemoryInterface):
    """Memory access via Wine + mem_read.exe/mem_write.exe subprocess calls."""

    def __init__(
        self,
        wine_path: Optional[str] = None,
        wineprefix: Optional[str] = None,
        mem_read: str = "C:\\mem_read.exe",
        mem_write: str = "C:\\mem_write.exe",
    ):
        self.wine_path = wine_path or os.environ.get(
            "WINE_PATH",
            "/Users/luis/Applications/CrossOver.app/Contents/SharedSupport/"
            "CrossOver/lib/wine/x86_64-unix/wine"
        )
        self.wineprefix = wineprefix or os.environ.get(
            "WINEPREFIX",
            os.path.expanduser(
                "~/Library/Application Support/CrossOver/Bottles/Steam"
            )
        )
        self.mem_read = mem_read
        self.mem_write = mem_write
        self._connected = False

    def _env(self) -> dict:
        return {
            "WINEPREFIX": self.wineprefix,
            "WINEDEBUG": "-all",
            "WINEMSYNC": "1",
            "PATH": os.environ.get("PATH", ""),
        }

    async def connect(self) -> bool:
        """Test connection by reading HP."""
        try:
            hp = await self.read_u32(PCAddresses.HP)
            self._connected = True
            return True
        except Exception:
            self._connected = False
            return False

    async def is_connected(self) -> bool:
        return self._connected

    async def read_u32(self, address: int) -> int:
        result = await asyncio.create_subprocess_exec(
            self.wine_path, self.mem_read, f"0x{address:X}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self._env(),
        )
        stdout, _ = await result.communicate()
        output = stdout.decode().replace('\r', '')
        for line in output.strip().split('\n'):
            if ':' in line:
                value_str = line.split(':')[-1].strip()
                return int(value_str)
        raise RuntimeError(f"Failed to read 0x{address:X}: {output}")

    async def read_u32_batch(self, address: int, count: int) -> List[int]:
        """Read multiple consecutive DWORDs using mem_read.exe count param."""
        result = await asyncio.create_subprocess_exec(
            self.wine_path, self.mem_read, f"0x{address:X}", str(count),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self._env(),
        )
        stdout, _ = await result.communicate()
        output = stdout.decode().replace('\r', '')
        values = []
        for line in output.strip().split('\n'):
            if ':' in line:
                value_str = line.split(':')[-1].strip()
                values.append(int(value_str))
        if len(values) != count:
            raise RuntimeError(
                f"Expected {count} values from 0x{address:X}, got {len(values)}"
            )
        return values

    async def write_u32(self, address: int, value: int) -> bool:
        result = await asyncio.create_subprocess_exec(
            self.wine_path, self.mem_write, f"0x{address:X}", str(value),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=self._env(),
        )
        await result.communicate()
        return result.returncode == 0


# =============================================================================
# Windows Native Memory Interface
# =============================================================================

class WindowsMemoryInterface(MemoryInterface):
    """Direct memory access on Windows using ctypes."""

    def __init__(self):
        self.process_handle = None
        self._pid = None

    async def connect(self) -> bool:
        try:
            import ctypes
            import ctypes.wintypes
            self.kernel32 = ctypes.windll.kernel32

            # Find ys1plus.exe
            pid = self._find_process("ys1plus.exe")
            if not pid:
                return False

            PROCESS_VM_READ = 0x0010
            PROCESS_VM_WRITE = 0x0020
            PROCESS_VM_OPERATION = 0x0008
            self.process_handle = self.kernel32.OpenProcess(
                PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION,
                False, pid
            )
            self._pid = pid
            return self.process_handle is not None and self.process_handle != 0
        except Exception:
            return False

    async def is_connected(self) -> bool:
        if not self.process_handle:
            return False
        # Check if process still exists
        import ctypes
        exit_code = ctypes.wintypes.DWORD()
        self.kernel32.GetExitCodeProcess(
            self.process_handle, ctypes.byref(exit_code)
        )
        return exit_code.value == 259  # STILL_ACTIVE

    def _find_process(self, name: str) -> Optional[int]:
        import ctypes
        import ctypes.wintypes

        TH32CS_SNAPPROCESS = 0x00000002
        snap = self.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

        class PROCESSENTRY32(ctypes.Structure):
            _fields_ = [
                ("dwSize", ctypes.wintypes.DWORD),
                ("cntUsage", ctypes.wintypes.DWORD),
                ("th32ProcessID", ctypes.wintypes.DWORD),
                ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
                ("th32ModuleID", ctypes.wintypes.DWORD),
                ("cntThreads", ctypes.wintypes.DWORD),
                ("th32ParentProcessID", ctypes.wintypes.DWORD),
                ("pcPriClassBase", ctypes.c_long),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("szExeFile", ctypes.c_char * 260),
            ]

        pe = PROCESSENTRY32()
        pe.dwSize = ctypes.sizeof(PROCESSENTRY32)

        if self.kernel32.Process32First(snap, ctypes.byref(pe)):
            while True:
                if pe.szExeFile.decode().lower() == name.lower():
                    pid = pe.th32ProcessID
                    self.kernel32.CloseHandle(snap)
                    return pid
                if not self.kernel32.Process32Next(snap, ctypes.byref(pe)):
                    break

        self.kernel32.CloseHandle(snap)
        return None

    async def read_u32(self, address: int) -> int:
        import ctypes
        buf = ctypes.c_uint32()
        bytes_read = ctypes.c_size_t()
        self.kernel32.ReadProcessMemory(
            self.process_handle, ctypes.c_void_p(address),
            ctypes.byref(buf), 4, ctypes.byref(bytes_read)
        )
        return buf.value

    async def read_u32_batch(self, address: int, count: int) -> List[int]:
        import ctypes
        buf = (ctypes.c_uint32 * count)()
        bytes_read = ctypes.c_size_t()
        self.kernel32.ReadProcessMemory(
            self.process_handle, ctypes.c_void_p(address),
            ctypes.byref(buf), count * 4, ctypes.byref(bytes_read)
        )
        return list(buf)

    async def write_u32(self, address: int, value: int) -> bool:
        import ctypes
        buf = ctypes.c_uint32(value)
        bytes_written = ctypes.c_size_t()
        return bool(self.kernel32.WriteProcessMemory(
            self.process_handle, ctypes.c_void_p(address),
            ctypes.byref(buf), 4, ctypes.byref(bytes_written)
        ))


# =============================================================================
# Platform Detection
# =============================================================================

def create_memory_interface() -> MemoryInterface:
    if platform.system() == "Darwin":
        return WineMemoryInterface()
    elif platform.system() == "Windows":
        return WindowsMemoryInterface()
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")


# =============================================================================
# Game State Tracking
# =============================================================================

class YsGameState:
    """Tracks Ys I game state by polling memory."""

    # Path to the permitted items file read by itemhook.dll
    PERMIT_FILE = "C:\\ap_items.txt"

    def __init__(self, mem: MemoryInterface, wineprefix: Optional[str] = None):
        self.mem = mem

        # Flag tracking
        self.prev_flags: Dict[int, int] = {}
        self.checked_locations: Set[int] = set()

        # Item tracking for AP
        self.ap_received_items: Set[int] = set()  # game_ids received from AP
        self.permitted_ids: Set[int] = set()       # game_ids permitted by itemhook
        self.received_item_index: int = 0

        # Save/load detection
        self.last_item_checksum: Optional[str] = None

        # Death link / multiplier tracking
        self.last_hp: int = 0
        self.last_exp: int = 0
        self.last_gold: int = 0

        # Resolve native paths
        if wineprefix:
            drive_c = os.path.join(wineprefix, "drive_c")
        elif platform.system() == "Windows":
            drive_c = "C:\\"
        else:
            drive_c = os.path.expanduser(
                "~/Library/Application Support/CrossOver/Bottles/Steam/drive_c"
            )
        self._permit_path = os.path.join(drive_c, "ap_items.txt")

    def write_permitted_file(self):
        """Write permitted item IDs to C:\\ap_items.txt atomically."""
        dir_path = os.path.dirname(self._permit_path)
        try:
            fd, tmp = tempfile.mkstemp(dir=dir_path, suffix=".tmp")
            with os.fdopen(fd, 'w') as f:
                for gid in sorted(self.permitted_ids):
                    f.write(f"{gid}\n")
            if platform.system() == "Windows":
                try:
                    os.remove(self._permit_path)
                except OSError:
                    pass
            os.rename(tmp, self._permit_path)
        except Exception as e:
            print(f"Failed to write permitted file: {e}")

    async def is_in_game(self) -> bool:
        """Check if the player is actively in Ys I gameplay."""
        try:
            hp = await self.mem.read_u32(PCAddresses.MAX_HP)
            return 0 < hp < 1000
        except Exception:
            return False

    # ----- Location Polling -----

    async def poll_locations(self) -> Set[int]:
        """Check all location flags for new checks. Returns new AP location codes."""
        new_checks: Set[int] = set()

        for flag_addr, ap_loc_code in FLAG_TO_LOCATION.items():
            if ap_loc_code in self.checked_locations:
                continue

            try:
                value = await self.mem.read_u32(flag_addr)
            except Exception:
                continue

            if flag_addr in REVERSE_FLAG_LOCATIONS:
                # Reverse flag: starts at 1, goes to 0 when claimed
                if value == 0 and self.prev_flags.get(flag_addr, 1) != 0:
                    new_checks.add(ap_loc_code)
                    self.checked_locations.add(ap_loc_code)
            else:
                # Normal flag: 0→1 when checked
                if value != 0 and self.prev_flags.get(flag_addr, 0) == 0:
                    new_checks.add(ap_loc_code)
                    self.checked_locations.add(ap_loc_code)

            self.prev_flags[flag_addr] = value

        return new_checks

    # ----- Item Give/Remove -----

    async def give_item(self, game_id: int) -> bool:
        """Give an item. Permits it in itemhook, then sets both arrays."""
        try:
            # Permit first so the DLL won't suppress the write
            self.permitted_ids.add(game_id)
            self.write_permitted_file()

            addr1 = PCAddresses.item_array1_addr(game_id)
            addr2 = PCAddresses.item_array2_addr(game_id)
            ok1 = await self.mem.write_u32(addr1, 1)
            ok2 = await self.mem.write_u32(addr2, 1)
            if ok1 and ok2:
                self.ap_received_items.add(game_id)
            return ok1 and ok2
        except Exception as e:
            print(f"give_item({game_id}) error: {e}")
            return False

    async def remove_item(self, game_id: int) -> bool:
        """Remove an item. Revoke permit, then DLL handles zeroing."""
        try:
            self.permitted_ids.discard(game_id)
            self.write_permitted_file()
            # DLL will zero the arrays on next poll (~16ms)
            return True
        except Exception as e:
            print(f"remove_item({game_id}) error: {e}")
            return False

    # ----- Save/Load Detection -----

    async def read_item_ownership(self) -> List[int]:
        """Read all item ownership values as a list."""
        try:
            return await self.mem.read_u32_batch(
                PCAddresses.ITEM_ARRAY_1_BASE, GAME_ITEM_COUNT
            )
        except Exception:
            return []

    def compute_item_checksum(self, items: List[int]) -> str:
        bits = ''.join('1' if v else '0' for v in items)
        return hashlib.md5(bits.encode()).hexdigest()[:16]

    async def check_save_load(self) -> bool:
        """Detect save load by checking if AP-given items disappeared."""
        if not self.ap_received_items:
            return False

        items = await self.read_item_ownership()
        if not items:
            return False

        checksum = self.compute_item_checksum(items)
        if checksum == self.last_item_checksum:
            return False

        # Check if any AP items are missing
        missing = False
        for game_id in self.ap_received_items:
            if game_id < len(items) and items[game_id] == 0:
                missing = True
                break

        if missing:
            print(f"Save load detected — re-applying {len(self.ap_received_items)} AP items")
            for game_id in self.ap_received_items:
                await self.give_item(game_id)
            items = await self.read_item_ownership()
            if items:
                self.last_item_checksum = self.compute_item_checksum(items)
            return True

        self.last_item_checksum = checksum
        return False

    # ----- Tower Entry Guard -----

    # Goban interaction flags — triggers tower entry cutscene
    GOBAN_FLAGS = [0x531CE4, 0x531CE8, 0x531CEC]

    async def guard_tower_entry(self, tower_items_in_overworld: List[int]):
        """Block Goban's tower entry if player is missing tower items
        that were randomized to overworld locations."""
        if not tower_items_in_overworld:
            return

        # Check if Goban interaction just triggered
        try:
            goban_triggered = False
            for flag_addr in self.GOBAN_FLAGS:
                val = await self.mem.read_u32(flag_addr)
                if val != 0:
                    goban_triggered = True
                    break

            if not goban_triggered:
                return

            # Check if player has all required items
            missing = []
            for game_id in tower_items_in_overworld:
                addr = PCAddresses.item_array1_addr(game_id)
                val = await self.mem.read_u32(addr)
                if val == 0:
                    missing.append(game_id)

            if missing:
                # Suppress Goban — zero all flags back
                for flag_addr in self.GOBAN_FLAGS:
                    await self.mem.write_u32(flag_addr, 0)
                print("Tower entry blocked! You are missing required items.")
        except Exception:
            pass

    # ----- Death Link -----

    async def check_death(self) -> bool:
        """Check if player died (HP went to 0)."""
        try:
            hp = await self.mem.read_u32(PCAddresses.HP)
            died = (hp == 0 and self.last_hp > 0)
            self.last_hp = hp
            return died
        except Exception:
            return False

    async def kill_player(self):
        """Kill the player for death link."""
        await self.mem.write_u32(PCAddresses.HP, 0)

    # ----- EXP/Gold Multipliers -----

    async def apply_multipliers(self, exp_mult: float, gold_mult: float):
        """Apply EXP and Gold multipliers by adjusting deltas."""
        try:
            exp = await self.mem.read_u32(PCAddresses.EXP)
            gold = await self.mem.read_u32(PCAddresses.GOLD)

            if exp_mult != 1.0 and self.last_exp > 0:
                diff = exp - self.last_exp
                if diff > 0:
                    adjusted = self.last_exp + int(diff * exp_mult)
                    await self.mem.write_u32(PCAddresses.EXP, adjusted)
                    exp = adjusted

            if gold_mult != 1.0 and self.last_gold > 0:
                diff = gold - self.last_gold
                if diff > 0:
                    adjusted = self.last_gold + int(diff * gold_mult)
                    await self.mem.write_u32(PCAddresses.GOLD, adjusted)
                    gold = adjusted

            self.last_exp = exp
            self.last_gold = gold
        except Exception:
            pass

    # ----- Goal Completion -----

    async def check_goal(self, goal: int) -> bool:
        """Check if the goal condition is met."""
        try:
            if goal == 0:  # Dark Fact
                val = await self.mem.read_u32(PCAddresses.BOSS_DARK_FACT)
                return val != 0

            elif goal == 1:  # All Books
                val = await self.mem.read_u32(PCAddresses.BOSS_DARK_FACT)
                if val == 0:
                    return False
                # Check all 6 books (game_id 20-25) in Array 1
                books = await self.mem.read_u32_batch(
                    PCAddresses.item_array1_addr(20), 6
                )
                return all(b != 0 for b in books)

            elif goal == 2:  # All Bosses
                boss_flags = [
                    PCAddresses.BOSS_JENOCRES,
                    PCAddresses.BOSS_NYGTILGER,
                    PCAddresses.BOSS_VAGULLION,
                    PCAddresses.BOSS_PICTIMOS,
                    PCAddresses.BOSS_KHONSCLARD,
                    PCAddresses.BOSS_YOGLEKS_OMULGUN,
                    PCAddresses.BOSS_DARK_FACT,
                ]
                for flag in boss_flags:
                    val = await self.mem.read_u32(flag)
                    if val == 0:
                        return False
                return True

        except Exception:
            pass
        return False


# =============================================================================
# Archipelago Client Context
# =============================================================================

if ARCHIPELAGO_AVAILABLE:
    class YsChroniclesContext(CommonContext):
        """Archipelago client context for Ys Chronicles."""

        game = "Ys I Chronicles"
        command_processor = 0
        items_handling = 0b111  # Full item handling

        def __init__(self, server_address: Optional[str], password: Optional[str]):
            super().__init__(server_address, password)
            self.mem: Optional[MemoryInterface] = None
            self.game_state: Optional[YsGameState] = None
            self.slot_data: Dict = {}
            self.mem_connected = False
            self.dll_injected = False
            self.game_poll_task: Optional[asyncio.Task] = None

        async def server_auth(self, password_requested: bool = False):
            if password_requested and not self.password:
                await super().server_auth(password_requested)
            await self.get_username()
            await self.send_connect()

        def on_package(self, cmd: str, args: dict):
            if cmd == "Connected":
                self.slot_data = args.get("slot_data", {})
                checked = args.get("checked_locations", [])
                if self.game_state:
                    self.game_state.checked_locations = set(checked)
                print(f"Connected to AP server. Slot data: {self.slot_data}")

            elif cmd == "ReceivedItems":
                if not self.game_state:
                    return
                items: List = args.get("items", [])
                start_index = args.get("index", 0)
                asyncio.create_task(
                    self._process_received_items(items, start_index)
                )

            elif cmd == "RoomUpdate":
                checked = args.get("checked_locations", [])
                if checked and self.game_state:
                    self.game_state.checked_locations.update(checked)

        async def _inject_itemhook(self):
            """Inject itemhook.dll into the game process."""
            try:
                if isinstance(self.mem, WineMemoryInterface):
                    result = await asyncio.create_subprocess_exec(
                        self.mem.wine_path, "C:\\inject.exe", "C:\\itemhook.dll",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        env=self.mem._env(),
                    )
                    stdout, stderr = await result.communicate()
                    if result.returncode == 0:
                        print("Injected itemhook.dll")
                    else:
                        print(f"itemhook injection failed: {stderr.decode().strip()}")
                else:
                    # Windows native
                    result = await asyncio.create_subprocess_exec(
                        "inject.exe", "C:\\itemhook.dll",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await result.communicate()
                    if result.returncode == 0:
                        print("Injected itemhook.dll")
                    else:
                        print(f"itemhook injection failed: {stderr.decode().strip()}")
            except Exception as e:
                print(f"itemhook injection error: {e}")

        async def _process_received_items(self, items: list, start_index: int):
            """Process received items and inject them into the game."""
            if not self.game_state:
                return

            for i, item in enumerate(items):
                idx = start_index + i
                if idx < self.game_state.received_item_index:
                    continue

                self.game_state.received_item_index = idx + 1

                # Get AP item code
                if isinstance(item, dict):
                    ap_code = item.get("item", 0)
                else:
                    ap_code = item.item if hasattr(item, "item") else 0

                # Convert AP code to game_id
                game_id = AP_CODE_TO_GAME_ID.get(ap_code)
                if game_id is not None:
                    success = await self.game_state.give_item(game_id)
                    item_name = GAME_ID_TO_AP_NAME.get(game_id, f"id:{game_id}")
                    if success:
                        print(f"Received: {item_name}")
                    else:
                        print(f"Failed to give: {item_name}")
                else:
                    print(f"Unknown AP item code {ap_code:#x}")

        async def game_poll_loop(self):
            """Main game polling loop."""
            while not self.exit_event.is_set():
                try:
                    # Ensure memory connection
                    if not self.mem_connected:
                        self.mem = create_memory_interface()
                        if await self.mem.connect():
                            wineprefix = getattr(self.mem, 'wineprefix', None)
                            self.game_state = YsGameState(self.mem, wineprefix=wineprefix)
                            self.mem_connected = True
                            print("Connected to ys1plus.exe!")

                            # Initialize permitted file and inject itemhook DLL
                            if not self.dll_injected:
                                self.game_state.write_permitted_file()
                                await self._inject_itemhook()
                                self.dll_injected = True
                        else:
                            await asyncio.sleep(5)
                            continue

                    # Ensure game is active
                    if not await self.game_state.is_in_game():
                        await asyncio.sleep(1)
                        continue

                    # 1. Save/load detection
                    await self.game_state.check_save_load()

                    # 2. Poll locations
                    new_checks = await self.game_state.poll_locations()
                    if new_checks and self.server and self.server.socket:
                        await self.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": list(new_checks),
                        }])
                        print(f"Sent {len(new_checks)} location checks")

                    # 3. Tower entry guard
                    tower_items = self.slot_data.get("tower_items_in_overworld", [])
                    if tower_items:
                        await self.game_state.guard_tower_entry(tower_items)

                    # 4. EXP/Gold multipliers
                    exp_mult = self.slot_data.get("experience_multiplier", 100) / 100.0
                    gold_mult = self.slot_data.get("gold_multiplier", 100) / 100.0
                    if exp_mult != 1.0 or gold_mult != 1.0:
                        await self.game_state.apply_multipliers(exp_mult, gold_mult)

                    # 5. Death link
                    if self.slot_data.get("death_link", False):
                        if await self.game_state.check_death():
                            await self.send_death()

                    # 6. Goal check
                    goal = self.slot_data.get("goal", 0)
                    if not self.finished_game and await self.game_state.check_goal(goal):
                        await self.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL,
                        }])
                        self.finished_game = True
                        print("Goal complete!")

                except Exception as e:
                    print(f"Poll error: {e}")
                    self.mem_connected = False

                await asyncio.sleep(POLL_INTERVAL)

        async def send_death(self):
            """Send death link to server."""
            await self.send_msgs([{
                "cmd": "Bounce",
                "tags": ["DeathLink"],
                "data": {
                    "time": asyncio.get_event_loop().time(),
                    "source": self.slot_info[self.slot].name
                    if self.slot_info else "Ys I",
                    "cause": "Adol fell in battle",
                },
            }])

        def on_deathlink(self, data: dict):
            """Handle incoming death link."""
            if self.game_state:
                asyncio.create_task(self.game_state.kill_player())
                source = data.get("source", "someone")
                print(f"Death link from {source}!")


# =============================================================================
# Main Entry Points
# =============================================================================

async def main_standalone():
    """Standalone client loop (without Archipelago)."""
    print("=" * 50)
    print("Ys I Chronicles - AP Client (Standalone)")
    print("=" * 50)

    mem = create_memory_interface()
    if not await mem.connect():
        print("Could not connect to ys1plus.exe.")
        print("Make sure the game is running.")
        return

    game_state = YsGameState(mem)

    if not await game_state.is_in_game():
        print("Could not detect active gameplay.")
        return

    print("Connected to Ys I!")

    # Read initial stats
    try:
        hp = await mem.read_u32(PCAddresses.HP)
        max_hp = await mem.read_u32(PCAddresses.MAX_HP)
        level = await mem.read_u32(PCAddresses.LEVEL)
        print(f"HP: {hp}/{max_hp}  Level: {level}")
    except Exception as e:
        print(f"Stats read error: {e}")

    # Initialize item state
    items = await game_state.read_item_ownership()
    if items:
        game_state.last_item_checksum = game_state.compute_item_checksum(items)

    print("\n[Monitoring for changes — press Ctrl+C to exit]")

    try:
        while True:
            await asyncio.sleep(POLL_INTERVAL)

            save_loaded = await game_state.check_save_load()
            if save_loaded:
                print("  State restored after save load")

            new_checks = await game_state.poll_locations()
            for loc_code in new_checks:
                print(f"  Location check: {loc_code:#x}")

    except KeyboardInterrupt:
        print("\nShutting down...")


async def main_archipelago(args):
    """Archipelago-integrated client loop."""
    ctx = YsChroniclesContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # Start game polling
    ctx.game_poll_task = asyncio.create_task(
        ctx.game_poll_loop(), name="game poll"
    )

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    """Entry point for Archipelago launcher."""
    if ARCHIPELAGO_AVAILABLE:
        parser = get_base_parser()
        args = parser.parse_args()
        asyncio.run(main_archipelago(args))
    else:
        asyncio.run(main_standalone())


if __name__ == "__main__":
    launch()
