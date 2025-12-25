import asyncio
import settings
import os
import socket
import traceback
import subprocess
from typing import Optional

import Patch
from BaseClasses import ItemClassification
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from .Data import (
    base_count,
    boss_level,
    castle_id,
    characters,
    difficulty_convert,
    item_ids,
    level_locations,
    sounds,
    colors,
    vanilla,
    portals
)
from .Items import ItemData, items_by_id
from .Locations import LocationData

READ = "READ_CORE_RAM"
WRITE = "WRITE_CORE_RAM"
INV_ADDR = 0xC5BF0
ACTIVE_LEVEL = 0x4EFC0
PLAYER_COUNT = 0x127764
PLAYER_LEVEL = 0xFD31B
PLAYER_ALIVE = 0xFD2EB
PLAYER_CLASS = 0xFD30F
PLAYER_COLOR = 0xFD30E
PLAYER_PORTAL = 0x64A50
PLAYER_BOSSING = 0x64A54
PLAYER_MOVEMENT = 0xFD307
SOUND_ADDRESS = 0xAE740
SOUND_START = 0xEEFC
PLAYER_KILL = 0xFD300
PAUSED = 0xC5B18
LOCATIONS_BASE_ADDRESS = 0x64A68

BOSS_ADDR = 0x289C08
TIME = 0xC5B1C
INPUT = 0xC5BCD

MOD_ITEM_ID = 0xD0800
MOD_QUANTITY = 0xD0804
MOD_PLAYER_ID = 0xD0808


class RetroSocket:
    def __init__(self):
        self.host = "localhost"
        self.port = 55355
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)

    def send(self, message: str):
        try:
            self.socket.sendto(message.encode(), (self.host, self.port))
        except Exception as e:
            raise Exception("An error occurred while sending a message.")

    async def read(self, message: str) -> Optional[bytes]:
        self.send(message)
        try:
            response = await asyncio.wait_for(asyncio.get_event_loop().sock_recv(self.socket, 30000), 1.0)
            data = response.decode().strip("\n").split(" ")
            b = b""
            for s in data[2:]:
                if "-1" in s:
                    raise Exception("Client tried to read from an invalid address or ROM is not open.")
                b += bytes.fromhex(s)
            return b
        except asyncio.TimeoutError:
            logger.error("Timeout while waiting for socket response")
            return None

    async def status(self) -> str:
        message = "GET_STATUS"
        self.send(message)
        data = await asyncio.wait_for(asyncio.get_event_loop().sock_recv(self.socket, 4096), 1.0)
        return data.decode()


class RamChunk:
    def __init__(self, arr: bytes):
        self.raw = arr
        self.split = []

    def iterate(self, length: int):
        self.split = [self.raw[i: i + length] for i in range(0, len(self.raw), length)]


item_names: dict[int, str] = {v & 0xFFFF: k for k, v in item_ids.items()}


def type_to_name(arr) -> str:
    packed = int.from_bytes(arr[1:3], "little")
    return item_names.get(packed, None)


class InventoryEntry:
    def __init__(self, arr: bytes, index: int, player: int):
        self.name = type_to_name(arr[1:4])
        self.count: int = int.from_bytes(arr[4:8], "little")
        self.addr = INV_ADDR + (0x400 * player) + (index * 0x10)
        self.n_addr: int = int.from_bytes(arr[12:15], "little")
        self.p_addr: int = int.from_bytes(arr[8:11], "little")


class ObjectEntry:
    def __init__(self, arr: bytes = None):
        self.raw = arr if arr is not None else bytes()


def message_format(arg: str, params: str) -> str:
    return f"{arg} {params}"


def param_format(adr: int, arr: bytes) -> str:
    return " ".join([hex(adr)] + [f"0x{byte:02X}" for byte in arr])


class GauntletLegendsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_connected(self):
        logger.info(f"Retroarch Connected Status: {self.ctx.retro_connected}")

    def _cmd_deathlink_toggle(self):
        self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
        self.ctx.update_death_link(self.ctx.deathlink_enabled)
        logger.info(f"Deathlink {('Enabled.' if self.ctx.deathlink_enabled else 'Disabled.')}")

    def _cmd_instantmax_toggle(self):
        if not self.ctx.glslotdata:
            logger.info("Cannot toggle InstantMax: slot data not initialized.")
            return
        self.ctx.glslotdata["instant_max"] = not self.ctx.glslotdata["instant_max"]
        logger.info(f"InstantMax {('Enabled.' if self.ctx.glslotdata['instant_max'] else 'Disabled.')}")

    def _cmd_players(self, value: int):
        value = int(value)
        logger.info(f"Players set from {self.ctx.players} to {min(value, 4)}.")
        self.ctx.players = min(value, 4)


class GauntletLegendsContext(CommonContext):
    command_processor = GauntletLegendsCommandProcessor
    game = "Gauntlet Legends"
    items_handling = 0b101

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.useful: list[NetworkItem] = []
        self.deathlink_pending: bool = False
        self.deathlink_enabled: bool = False
        self.deathlink_triggered: bool = False
        self.ignore_deathlink: bool = False
        self.difficulty: int = 0
        self.players: int = 1
        self.gl_sync_task = None
        self.glslotdata = None
        self.socket = RetroSocket()
        self.rom_loaded: bool = False
        self.locations_checked: list[int] = []
        self.inventory: list[list[InventoryEntry]] = []
        self.retro_connected: bool = False
        self.level_loading: bool = False
        self.in_game: bool = False
        self.scouted: bool = False
        self.obelisks: list[NetworkItem] = []
        self.item_locations: list[LocationData] = []
        self.obelisk_locations: list[LocationData] = []
        self.chest_locations: list[LocationData] = []
        self.item_address: int = 0
        self.chest_address: int = 0
        self.limbo: bool = False
        self.in_portal: bool = False
        self.scaled: bool = False
        self.offset: int = -1
        self.clear_counts = None
        self.current_level: bytes = b""
        self.output_file: str = ""
        self.movement: int = 0
        self.init_refactor: bool = False
        self.location_scouts: list[NetworkItem] = []

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    def inv_count(self, player: int) -> int:
        return len(self.inventory[player])

    async def inv_read(self):
        self.inventory = []
        for player in range(self.players):
            _inv: list[InventoryEntry] = []
            b = RamChunk(
                await self.socket.read(message_format(READ, f"0x{format(INV_ADDR + (0x400 * player), 'x')} 1008")))
            if b is None:
                return
            b.iterate(0x10)
            for i, arr in enumerate(b.split):
                _inv += [InventoryEntry(arr, i, player)]
            for i in range(len(_inv)):
                if _inv[i].p_addr == 0:
                    _inv = _inv[i:]
                    break
            new_inv: list[InventoryEntry] = []
            new_inv += [_inv[0]]
            addr = new_inv[0].n_addr
            visited = {new_inv[0].addr}  # Track visited addresses to detect cycles
            while True:
                if addr == 0:
                    break
                if addr in visited:  # Circular reference detected
                    logger.warning(f"Circular reference detected in inventory chain at {addr:#x}")
                    break
                matching = [inv for inv in _inv if inv.addr == addr]
                if not matching:  # Broken chain - address not found
                    logger.warning(f"Broken inventory chain: addr {addr:#x} not found in inventory data")
                    break
                new_inv += matching
                visited.add(addr)
                addr = new_inv[-1].n_addr
            self.inventory += [new_inv]

    async def item_from_name(self, name: str, player: int) -> InventoryEntry | None:
        await self.inv_read()
        for i in range(0, self.inv_count(player)):
            if self.inventory[player][i].name == name:
                return self.inventory[player][i]
        return None

    async def inv_bitwise(self, name: str, bit: int, player: int) -> bool:
        item = await self.item_from_name(name, player)
        if item is None:
            return False
        return (item.count & bit) != 0

    def _normalize_item_name(self, name: str) -> str:
        if "Runestone" in name:
            return "Runestone"
        if "Fruit" in name or "Meat" in name:
            return "Health"
        if "Obelisk" in name:
            return "Obelisk"
        if "Mirror" in name:
            return "Mirror Shard"
        if portals.get(name, False):
            return portals[name]
        return name

    async def update_item(self, name: str, count: int, player: int = None, infinite_count: bool = False):
        name = self._normalize_item_name(name)
        players_to_update = range(self.players) if player is None else [player]

        for p in players_to_update:
            player_id = p + 1
            await self._write_ram(MOD_ITEM_ID, int.to_bytes((item_ids[name] if not infinite_count else item_ids[name] & 0xFFFF), 4, "little"))
            await self._write_ram(MOD_QUANTITY, int.to_bytes(count, 4, "little", signed=True))
            await self._write_ram(MOD_PLAYER_ID, int.to_bytes(player_id, 4, "little"))
            await asyncio.sleep(0.05)

    async def set_item(self, name: str, value: int, player: int = None):
        players_to_update = range(self.players) if player is None else [player]
        for p in players_to_update:
            current = await self.item_from_name(name, p)
            diff = value - (current.count if current else 0)
            if diff != 0:
                await self.update_item(name, diff, p)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(GauntletLegendsContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.glslotdata = args["slot_data"]
            self.players = self.glslotdata["players"]
            if self.players is None:
                self.players = 1
            self.deathlink_enabled = self.glslotdata["death_link"]
            self.update_death_link(self.deathlink_enabled)
            self.var_reset()
            logger.info(f"Players set to {self.players}.")
            logger.info("If this is incorrect, Use /players to set the number of people playing locally.")
        elif cmd == "Retrieved":
            if "keys" not in args:
                logger.warning(f"invalid Retrieved packet to GLClient: {args}")
                return
            cc = self.stored_data.get(f"gl_cc_T{self.team}_P{self.slot}", None)
            if cc is not None:
                logger.info("Received clear counts from server")
                self.clear_counts = cc
            else:
                self.clear_counts = {}
        elif cmd == "LocationInfo":
            self.location_scouts = args["locations"]
        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]

    # Update inventory based on items received from server
    # Also adds starting items based on a few yaml options
    async def handle_items(self):
        compass = None
        for player in range(self.players):
            compass = await self.item_from_name("Compass", player)
            if compass is None:
                break
        if compass is not None:
            for player in range(self.players):
                if self.glslotdata["characters"][player] != 0:
                    temp = await self.item_from_name(characters[self.glslotdata["characters"][player] - 1], player)
                    if temp is None:
                        await self.wait_for_mod_clear()
                        await self.update_item(characters[self.glslotdata["characters"][player] - 1], 50, player)

                temp = await self.item_from_name("Key", player)
                if temp is None and self.glslotdata["keys"] == 1:
                    await self.wait_for_mod_clear()
                    await self.update_item("Key", 9000, player)

                temp = await self.item_from_name("Speed Boots", player)
                if temp is None and self.glslotdata["speed"] == 1:
                    await self.wait_for_mod_clear()
                    await self.update_item("Speed Boots", 1, player, True)

            i = compass.count
            if i - 1 < len(self.items_received):
                for index in range(i - 1, len(self.items_received)):
                    item = self.items_received[index].item
                    item_name = items_by_id[item].item_name

                    if item_name == "Death":
                        continue

                    await self.wait_for_mod_clear()
                    await asyncio.sleep(0.05)
                    await self.update_item(item_name, base_count[item_name])

            await self.wait_for_mod_clear()
            await asyncio.sleep(0.05)
            await self.set_item("Compass", len(self.items_received) + 1)

    async def wait_for_mod_clear(self, poll_interval: float = 0.05):
        while True:
            mod_data = await self.socket.read(message_format(READ, f"0x{MOD_ITEM_ID:x} 12"))
            if mod_data and all(byte == 0 for byte in mod_data):
                return True
            await asyncio.sleep(poll_interval)

    async def _read_ram(self, address: int, size: int) -> bytes:
        return await self.socket.read(message_format(READ, f"0x{address:x} {size}"))

    async def _read_ram_int(self, address: int, size: int, signed: bool = False) -> int:
        data = await self._read_ram(address, size)
        return int.from_bytes(data, "little", signed=signed) if data else 0

    async def _write_ram(self, address: int, data: bytes):
        self.socket.send(message_format(WRITE, param_format(address, data)))

    async def read_time(self) -> int:
        return await self._read_ram_int(TIME, 2)

    async def read_level(self) -> bytes:
        return await self._read_ram(ACTIVE_LEVEL, 2)

    async def check_loading(self) -> bool:
        if self.in_portal or self.level_loading:
            return await self.read_time() == 0
        return False

    async def active_players(self) -> int:
        return await self._read_ram_int(PLAYER_COUNT, 1)

    async def player_level(self) -> int:
        return await self._read_ram_int(PLAYER_LEVEL, 1)

    async def portaling(self) -> int:
        return await self._read_ram_int(PLAYER_PORTAL, 1)

    async def limbo_check(self, offset=0) -> int:
        return await self._read_ram_int(PLAYER_MOVEMENT + offset, 1)

    async def dead(self) -> bool:
        val = await self._read_ram_int(PLAYER_KILL, 1)
        if (val & 0xF) == 0x1:
            self.ignore_deathlink = True
        return ((val & 0xF) == 0x8) or ((val & 0xF) == 0x1)

    async def boss(self) -> int:
        return await self._read_ram_int(PLAYER_BOSSING, 1)

    async def paused(self) -> int:
        val = await self._read_ram_int(PAUSED, 1)
        return val != 0x3

    async def scale(self):
        level = await self.read_level()
        if self.movement != 0x12:
            level = [0x1, 0xF]

        players = await self.active_players()
        player_level = await self.player_level()
        max_value = max(self.glslotdata["max"], self.players)

        scale_value = (max_value if self.glslotdata["instant_max"] == 1
                       else min(max((player_level - difficulty_convert[level[1]]) // 5, 0), 3))

        await self._write_ram(PLAYER_COUNT, int.to_bytes(min(players + scale_value, max_value), 1, "little"))
        self.scaled = True

    def _get_level_id(self, level: bytes) -> int:
        _id = level[0]
        if level[1] == 1:
            _id = castle_id.index(level[0]) + 1
        return (level[1] << 4) + _id

    async def get_seed_name(self) -> str:
        seed_name = await self._read_ram(0xD07F0, 0x10)
        return seed_name.decode("utf-8").strip()

    async def scout_locations(self, ctx: "GauntletLegendsContext") -> None:
        try:
            level = await self.read_level()

            # Handle special movement case
            if self.movement != 0x12:
                level = [0x1, 0xF]

            self.current_level = level
            players = await self.active_players()
            player_level = await self.player_level()

            # Determine difficulty
            self.difficulty = (min(players + (min(player_level // vanilla[level[1]], 3)), 4)
                               if self.clear_counts.get(str(level), 0) != 0 else players)

            # Filter locations by difficulty and settings
            level_id = self._get_level_id(level)

            locations_address = await self._read_ram_int(LOCATIONS_BASE_ADDRESS, 4) & 0xFFFFFF
            self.item_address = await self._read_ram_int(locations_address + 0x14, 4) & 0xFFFFFF
            self.chest_address = await self._read_ram_int(locations_address + 0x30, 4) & 0xFFFFFF

            raw_locations = [location for location in level_locations.get(level_id, []) if "Mirror" not in location.name and "Skorne" not in location.name]

            # Scout locations if any exist
            if raw_locations:
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": [loc.id for loc in raw_locations],
                    "create_as_hint": 0,
                }])
                while not self.location_scouts:
                    await asyncio.sleep(0.1)

            # Categorize scouted locations
            self.obelisks = [
                item for item in self.location_scouts
                if "Obelisk" in items_by_id.get(item.item, ItemData(0, "", "filler")).item_name
                   and item.player == self.slot
            ]

            self.useful = [
                item for item in self.location_scouts
                if "Obelisk" not in items_by_id.get(item.item, ItemData(0, "", "filler")).item_name
                   and items_by_id.get(item.item, ItemData(0, "", "filler")).progression in
                   [ItemClassification.useful, ItemClassification.progression]
                   and item.player == self.slot
            ]

            obelisk_ids = {item.location for item in self.obelisks}
            useful_ids = {item.location for item in self.useful}

            self.obelisk_locations = [loc for loc in raw_locations if loc.id in obelisk_ids]
            self.item_locations = [
                loc for loc in raw_locations
                if (("Chest" not in loc.name and
                     ("Barrel" not in loc.name or "Barrel of Gold" in loc.name) and
                     loc not in self.obelisk_locations) or loc.id in useful_ids)
            ]
            self.chest_locations = [
                loc for loc in raw_locations
                if loc not in self.obelisk_locations and loc not in self.item_locations
            ]

            self.scouted = True
        except Exception:
            logger.error(traceback.format_exc())

    async def location_loop(self) -> list[int]:
        acquired = []
        item_section = await self._read_ram(self.item_address, (len(self.item_locations) * 0x18))
        for i in range(len(self.item_locations)):
            active = item_section[i * 0x18 + 0x2]
            state = item_section[i * 0x18 + 0x3]
            if state >= 0x7F:
                continue
            if active == 1 and state == 0:
                acquired += [self.item_locations[i].id]

        for j in range(len(self.obelisk_locations)):
            ob = await self.inv_bitwise("Obelisk", (1 << (base_count[items_by_id[self.obelisks[j].item].item_name] - 1)), 0)
            if ob:
                acquired += [self.obelisk_locations[j].id]

        chest_section = await self._read_ram(self.chest_address, (len(self.chest_locations) * 0x18))
        for i in range(len(self.chest_locations)):
            active = chest_section[i * 0x18 + 0x2]
            state = chest_section[i * 0x18 + 0x3]
            if state >= 0x7F:
                continue
            if active == 1 and state != 1:
                acquired += [self.chest_locations[i].id]

        paused = await self.paused()
        dead = await self.dead()
        if paused or dead:
            return []
        return acquired

    async def level_status(self, ctx: "GauntletLegendsContext") -> bool:
        portaling = await self.portaling()
        dead = await self.dead()
        boss = await self.boss()
        if portaling or dead or (self.current_level in boss_level and boss == 0):
            if portaling or (self.current_level in boss_level and boss == 0):
                self.clear_counts[str(self.current_level)] = self.clear_counts.get(str(self.current_level), 0) + 1
                if self.current_level in boss_level:
                    await ctx.send_msgs(
                        [
                            {
                                "cmd": "LocationChecks",
                                "locations": [
                                    location.id
                                    for location in level_locations[
                                        (self.current_level[1] << 4) + self.current_level[0]
                                        ]
                                    if "Mirror" in location.name or "Skorne" in location.name
                                ],
                            },
                        ],
                    )
            if dead and not (self.current_level in boss_level and boss == 0):
                if self.deathlink_triggered:
                    self.deathlink_triggered = False
                elif self.ignore_deathlink:
                    self.ignore_deathlink = False
                elif self.deathlink_enabled:
                    await ctx.send_death(f"{ctx.auth} didn't eat enough meat.")
            self.var_reset()
            return True
        return False

    def var_reset(self):
        self.output_file = ""
        self.item_locations = []
        self.chest_locations = []
        self.obelisk_locations = []
        self.obelisks = []
        self.useful = []
        self.in_game = False
        self.level_loading = False
        self.scaled = False
        self.offset = -1
        self.movement = 0
        self.difficulty = 0
        self.location_scouts = []
        self.ignore_deathlink = False
        self.item_address = 0
        self.chest_address = 0
        self.scouted = False

    async def die(self):
        """Trigger deathlink death with character-specific death sound."""
        self.deathlink_triggered = True
        char = await self._read_ram_int(PLAYER_CLASS, 1)
        color = await self._read_ram_int(PLAYER_COLOR, 1)

        # Play death sound
        sound_data = (int.to_bytes(colors[color], 4, "little") +
                      int.to_bytes(sounds[char], 4, "little") +
                      int.to_bytes(0xBB, 4, "little"))
        await self._write_ram(SOUND_ADDRESS, sound_data)
        await self._write_ram(SOUND_START, int.to_bytes(0xE00AE718, 4, "little"))
        await asyncio.sleep(2)

        # Stop sound and kill player
        await self._write_ram(SOUND_START, int.to_bytes(0x0, 4, "little"))
        await self._write_ram(PLAYER_KILL, int.to_bytes(0x7, 1, "little"))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Archipelago Gauntlet Legends Client"
        return ui


# Store original file content for restoration
_original_opt_content: dict[str, str | None] = {}


async def _patch_opt():
    """
    Create RetroArch core options override for CountPerOp=1.
    Backs up existing content for restoration on close.
    """
    retroarch_path = settings.get_settings().gl_options.retroarch_path

    override_dir = os.path.join(retroarch_path, "config", "Mupen64Plus-Next")
    os.makedirs(override_dir, exist_ok=True)
    override_path = os.path.join(override_dir, f"Mupen64Plus-Next.opt")

    logger.info(f"Override path: {override_path}")
    logger.info(f"File exists: {os.path.exists(override_path)}")

    # Store original content for restoration (None if file didn't exist)
    if override_path not in _original_opt_content:
        if os.path.exists(override_path):
            with open(override_path, "r") as f:
                _original_opt_content[override_path] = f.read()
        else:
            _original_opt_content[override_path] = None

    if os.path.exists(override_path):
        with open(override_path, "r") as f:
            content = f.read()

        logger.info(f"Current content length: {len(content)}")
        logger.info(f"CountPerOp in content: {'mupen64plus-CountPerOp' in content}")

        if 'mupen64plus-CountPerOp = "1"' in content:
            logger.info(f"CountPerOp=1 already set in: {override_path}")
            return

        # Check if CountPerOp exists with different value - replace it
        import re
        if 'mupen64plus-CountPerOp' in content:
            logger.info("Replacing existing CountPerOp value")
            content = re.sub(
                r'mupen64plus-CountPerOp\s*=\s*"[^"]*"',
                'mupen64plus-CountPerOp = "1"',
                content
            )
        else:
            logger.info("Appending CountPerOp")
            if not content.endswith("\n"):
                content += "\n"
            content += 'mupen64plus-CountPerOp = "1"\n'
    else:
        logger.info("Creating new file")
        content = 'mupen64plus-CountPerOp = "1"\n'

    logger.info(f"Writing content: {content[:100]}...")
    with open(override_path, "w") as f:
        f.write(content)

    # Verify write
    with open(override_path, "r") as f:
        verify = f.read()
    logger.info(f"Verified content: {verify[:100]}...")

    logger.info(f"Created CountPerOp override at: {override_path}")


def _restore_opt_files():
    """
    Restore original .opt files on application close.
    Call this from shutdown/cleanup.
    """
    for path, original_content in _original_opt_content.items():
        try:
            if original_content is None:
                # File didn't exist before, delete it
                if os.path.exists(path):
                    os.remove(path)
                    logger.info(f"Removed override file: {path}")
            else:
                # Restore original content
                with open(path, "w") as f:
                    f.write(original_content)
                logger.info(f"Restored override file: {path}")
        except Exception as e:
            logger.error(f"Failed to restore {path}: {e}")

    _original_opt_content.clear()


async def _launch_retroarch(rom_path: str):
    """
    Launch RetroArch with the ROM.
    """
    retroarch_path = settings.get_settings().gl_options.retroarch_path
    retroarch_exe = os.path.join(retroarch_path, "retroarch.exe")
    core_path = os.path.join(retroarch_path, "cores", "mupen64plus_next_libretro.dll")

    if not os.path.exists(retroarch_exe):
        logger.error(f"RetroArch not found at: {retroarch_exe}")
        return

    if not os.path.exists(core_path):
        logger.error(f"Mupen64Plus core not found at: {core_path}")
        return

    subprocess.Popen([retroarch_exe, "-L", core_path, rom_path])
    logger.info(f"Launched RetroArch with ROM: {rom_path}")

    # Wait for RetroArch to start up
    await asyncio.sleep(2)

# Update _patch_game to call _patch_crc:
async def _patch_and_launch_game(patch_file: str):
    metadata, output_file = Patch.create_rom_file(patch_file)
    await _patch_opt()
    await _launch_retroarch(output_file)




async def gl_sync_task(ctx: GauntletLegendsContext):
    logger.info("Starting N64 connector...")
    while not ctx.exit_event.is_set():
        if ctx.retro_connected:
            try:
                if not ctx.rom_loaded:
                    status = await ctx.socket.status()
                    status = status.split(" ")
                    if status[1] == "CONTENTLESS":
                        logger.info("No ROM loaded, waiting...")
                        await asyncio.sleep(3)
                        continue
                    else:
                        logger.info("ROM Loaded")
                        ctx.rom_loaded = True
                cc_str: str = f"gl_cc_T{ctx.team}_P{ctx.slot}"
                pl_str: str = f"gl_pl_T{ctx.team}_P{ctx.slot}"
                ctx.set_notify(cc_str)
                if not ctx.auth:
                    await asyncio.sleep(1)
                    continue
                seed_name = await ctx.get_seed_name()
                if seed_name != ctx.seed_name[0:16]:
                    logger.info(f"ROM seed does not match room seed ({seed_name} != {ctx.seed_name}), "
                                f"please load the correct ROM.")
                    await ctx.disconnect()
                    continue
                player_level = await ctx.player_level()
                await ctx.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": pl_str,
                            "default": {},
                            "want_reply": True,
                            "operations": [
                                {
                                    "operation": "replace",
                                    "value": player_level,
                                },
                            ],
                        },
                    ],
                )
                bitwise = await ctx.inv_bitwise("Hell", 0x100, 0)
                if not ctx.finished_game and bitwise:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
                if ctx.limbo:
                    limbo = await ctx.limbo_check(0x78)
                    if limbo:
                        ctx.limbo = False
                        await asyncio.sleep(3)
                    else:
                        await asyncio.sleep(0.05)
                        continue
                await ctx.handle_items()
                if ctx.deathlink_pending and ctx.deathlink_enabled:
                    ctx.deathlink_pending = False
                    await ctx.die()
                if not ctx.level_loading and not ctx.in_game:
                    if not ctx.in_portal:
                        ctx.in_portal = bool(await ctx.portaling())
                    if ctx.in_portal:
                        await asyncio.sleep(0.1)
                        if ctx.movement == 0:
                            ctx.movement = await ctx.limbo_check()
                    ctx.level_loading = await ctx.check_loading()
                if ctx.level_loading:
                    ctx.in_portal = False
                    if not ctx.scaled:
                        await asyncio.sleep(0.2)
                        await ctx.scale()
                    ctx.in_game = not await ctx.check_loading()
                if ctx.in_game:
                    ctx.level_loading = False
                    if not ctx.scouted:
                        await ctx.scout_locations(ctx)
                        await asyncio.sleep(1)
                    status = await ctx.level_status(ctx)
                    if status:
                        await ctx.send_msgs(
                            [
                                {
                                    "cmd": "Set",
                                    "key": cc_str,
                                    "default": {},
                                    "want_reply": True,
                                    "operations": [
                                        {
                                            "operation": "replace",
                                            "value": ctx.clear_counts,
                                        },
                                    ],
                                },
                            ],
                        )
                        ctx.limbo = True
                        await asyncio.sleep(0.05)
                        continue
                    await asyncio.sleep(0.1)
                    checking = await ctx.location_loop()
                    if len(checking) > 0:
                        ctx.locations_checked += checking
                        await ctx.check_locations(checking)
                await asyncio.sleep(0.1)
            except (TimeoutError, ConnectionResetError, ConnectionRefusedError) as e:
                error_type = type(e).__name__
                logger.info(f"{error_type.replace('Error', ' ')}, Reconnecting")
                ctx.socket = RetroSocket()
                ctx.retro_connected = False
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Unknown Error Occurred: {e}")
                logger.info(traceback.format_exc())
                ctx.socket = RetroSocket()
                ctx.retro_connected = False
                await asyncio.sleep(2)
        else:
            try:
                logger.info("Attempting to connect to Retroarch...")
                status = await ctx.socket.status()
                ctx.retro_connected = True
                status = status.split(" ")
                if status[1] == "CONTENTLESS":
                    ctx.rom_loaded = False
                logger.info("Connected to Retroarch")
                continue
            except (TimeoutError, ConnectionRefusedError, ConnectionResetError) as e:
                error_type = type(e).__name__
                logger.info(f"{error_type.replace('Error', ' ')}, Trying Again")
                logger.info(traceback.format_exc())
                await asyncio.sleep(2)
                continue
            except Exception as e:
                logger.error(f"Unknown Error Occurred: {e}")
                logger.info(traceback.format_exc())
                await asyncio.sleep(2)
                continue


def launch(*args):
    async def main(args):
        if args.patch_file:
            await asyncio.create_task(_patch_and_launch_game(args.patch_file))
        ctx = GauntletLegendsContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.gl_sync_task = asyncio.create_task(gl_sync_task(ctx), name="Gauntlet Legends Sync Task")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        # Restore original .opt files on exit
        _restore_opt_files()

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APGL file")
    args = parser.parse_args(args)

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
