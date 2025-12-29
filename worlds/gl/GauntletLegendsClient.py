import asyncio
import settings
import os
import socket
import traceback
import subprocess
import Patch

from typing import Optional
from BaseClasses import ItemClassification
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from .Data import (
    base_count,
    characters,
    item_ids,
    level_locations,
    sounds,
    colors,
    portals
)
from .Items import ItemData, items_by_id
from .Locations import LocationData

READ = "READ_CORE_RAM"
WRITE = "WRITE_CORE_RAM"
INV_ADDR = 0xC5BF0
PLAYER_CLASS = 0xFD30F
PLAYER_COLOR = 0xFD30E
SOUND_ADDRESS = 0xAE740
SOUND_START = 0xEEFC
PLAYER_KILL = 0xFD300
BOSS_GOAL = 0x45D34
BOSS_GOAL_BACKUP = 0x45D3C
LEVEL_LOADING = 0x64A50
LOCATIONS_BASE_ADDRESS = 0x64A68
ZONE_ID = 0x6CA58
LEVEL_ID = 0x6CA5C

MOD_ITEM_ID = 0xD0800
MOD_QUANTITY = 0xD0804
MOD_PLAYER_ID = 0xD0808
MOD_OBELISK_QUANTITY = 0xD07E7


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
        self.p_addr: int = int.from_bytes(arr[8:12], "little") & 0x00FFFFFF
        self.n_addr: int = int.from_bytes(arr[12:16], "little") & 0x00FFFFFF


def message_format(arg: str, params: str) -> str:
    return f"{arg} {params}"


def param_format(adr: int, arr: bytes) -> str:
    return " ".join([hex(adr)] + [f"0x{byte:02X}" for byte in arr])


class GauntletLegendsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_connected(self):
        """Show Retroarch connection status"""
        logger.info(f"Retroarch Connected Status: {self.ctx.retro_connected}")

    def _cmd_deathlink_toggle(self):
        """Toggle Deathlink on or off"""
        self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
        self.ctx.update_death_link(self.ctx.deathlink_enabled)
        logger.info(f"Deathlink {('Enabled.' if self.ctx.deathlink_enabled else 'Disabled.')}")

    def _cmd_instantmax_toggle(self):
        """Toggle InstantMax on or off"""
        if not self.ctx.glslotdata:
            logger.info("Cannot toggle InstantMax: slot data not initialized.")
            return
        self.ctx.glslotdata["instant_max"] = not self.ctx.glslotdata["instant_max"]
        logger.info(f"InstantMax {('Enabled.' if self.ctx.glslotdata['instant_max'] else 'Disabled.')}")

    def _cmd_players(self, value: int):
        """Set number of local players (max 4)"""
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
        self.players: int = 1
        self.gl_sync_task = None
        self.glslotdata = None
        self.socket = RetroSocket()
        self.rom_loaded: bool = False
        self.locations_checked: list[int] = []
        self.inventory: list[list[InventoryEntry]] = []
        self.retro_connected: bool = False
        self.scouted: bool = False
        self.obelisks: list[NetworkItem] = []
        self.item_locations: list[int] = []
        self.obelisk_locations: list[int] = []
        self.chest_locations: list[int] = []
        self.item_address: int = 0
        self.chest_address: int = 0
        self.zone: int = 0
        self.level: int = 0
        self.current_zone: int = 0
        self.current_level: int = 0
        self.level_id: int = 0
        self.output_file: str = ""
        self.location_scouts: list[NetworkItem] = []

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    async def update_stage(self):
        self.zone = await self._read_ram_int(ZONE_ID, 1)
        self.level = await self._read_ram_int(LEVEL_ID, 1)

    async def check_goal(self) -> bool:
        goal = await self._read_ram_int(BOSS_GOAL, 4)
        backup = await self._read_ram_int(BOSS_GOAL_BACKUP, 4)
        return goal == 0xA or backup == 0xA

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
            start_entry = None
            for entry in _inv:
                if entry.p_addr == 0:
                    start_entry = entry
                    break
            if start_entry is None:
                self.inventory += [[]]
                continue
            new_inv: list[InventoryEntry] = []
            new_inv += [start_entry]
            addr = start_entry.n_addr
            visited = {start_entry.addr}
            while True:
                if addr == 0:
                    break
                if addr in visited:
                    break
                matching = [inv for inv in _inv if inv.addr == addr]
                if not matching:
                    logger.warning(f"Broken inventory chain: addr {addr:#x} not found in inventory data")
                    break
                new_inv += matching
                visited.add(addr)
                addr = new_inv[-1].n_addr
            self.inventory += [new_inv]

    async def item_from_name(self, name: str, player: int) -> InventoryEntry | None:
        await self.inv_read()
        for i in range(0, len(self.inventory[player])):
            if self.inventory[player][i].name == name:
                return self.inventory[player][i]
        return None

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
            logger.info(f"Players set to {self.players}.")
            logger.info("If this is incorrect, Use /players to set the number of people playing locally.")
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
                    await asyncio.sleep(0.02)
                    await self.update_item(item_name, base_count[item_name])
                    await self.wait_for_mod_clear()
                    await asyncio.sleep(0.02)
                    await self.update_item("Compass", 1)

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

    async def dead(self) -> bool:
        val = await self._read_ram_int(PLAYER_KILL, 1)
        if (val & 0xF) == 0x1:
            self.ignore_deathlink = True
        return ((val & 0xF) == 0x8) or ((val & 0xF) == 0x1)

    async def get_seed_name(self) -> str:
        seed_name = await self._read_ram(0xD07F0, 0x10)
        return seed_name.decode("utf-8").strip()

    async def scout_locations(self, ctx: "GauntletLegendsContext") -> None:
        try:
            self.location_scouts = []
            self.obelisk_locations = []
            self.item_locations = []
            self.chest_locations = []
            self.useful = []
            self.obelisks = []

            raw_locations = [location for location in level_locations.get(self.level_id, []) if "Mirror" not in location.name and "Skorne" not in location.name]
            scoutable_location_ids = [location.id for location in raw_locations if location.id in ctx.checked_locations or location.id in self.missing_locations]

            # Scout locations if any exist
            if raw_locations:
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": scoutable_location_ids,
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

            self.obelisk_locations = [loc.id for loc in raw_locations if loc.id in obelisk_ids]
            self.item_locations = [
                loc.id for loc in raw_locations
                if (("Chest" not in loc.name and
                     ("Barrel" not in loc.name or "Barrel of Gold" in loc.name) and
                     loc.id not in self.obelisk_locations) or loc.id in useful_ids)
            ]
            self.chest_locations = [
                loc.id for loc in raw_locations
                if loc.id not in self.obelisk_locations and loc.id not in self.item_locations
            ]
            self.scouted = True
        except Exception:
            logger.error(traceback.format_exc())

    async def location_loop(self) -> list[int]:
        if self.current_zone == 0:
            self.current_zone = self.zone
            self.current_level = self.level
            self.level_id = (self.current_zone << 4) + self.current_level
        if self.zone != self.current_zone or self.level != self.current_level:
            if self.current_level & 0x8 == 0x8:
                dead = await self.dead()
                if not dead and self.level_id != 0x58:
                    await self.check_locations([location.id for location in level_locations[self.level_id]
                                                if "Mirror Shard" in location.name or "Skorne" in location.name])
            self.current_zone = self.zone
            self.current_level = self.level
            self.level_id = (self.current_zone << 4)  + self.current_level
            self.scouted = False
            await asyncio.sleep(2)
        if self.current_zone == 0x8 or self.current_zone == 0xE:
            return []

        if not self.scouted:
            await self.scout_locations(self)

        loading = await self._read_ram_int(LEVEL_LOADING, 1)
        if loading == 1:
            return []

        locations_address = await self._read_ram_int(LOCATIONS_BASE_ADDRESS, 4) & 0xFFFFFF
        self.item_address = await self._read_ram_int(locations_address + 0x14, 4)
        self.chest_address = await self._read_ram_int(locations_address + 0x30, 4)
        if self.item_address == 0x7FFF0BAD or self.chest_address == 0x7FFF0BAD:
            return []

        self.item_address &= 0xFFFFFF
        self.chest_address &= 0xFFFFFF

        acquired = []
        item_section = await self._read_ram(self.item_address, (len(self.item_locations) * 0x18))
        for i in range(len(self.item_locations)):
            active = item_section[i * 0x18 + 0x2]
            state = item_section[i * 0x18 + 0x3]
            if state >= 0x7F:
                continue
            if active == 1 and state == 0:
                acquired += [self.item_locations[i]]

        for j in range(len(self.obelisk_locations)):
            obelisk = await self._read_ram_int(MOD_OBELISK_QUANTITY, 1)
            if obelisk & (1 << (base_count[items_by_id[self.obelisks[j].item].item_name] - 1)) != 0:
                acquired += [self.obelisk_locations[j]]

        chest_section = await self._read_ram(self.chest_address, (len(self.chest_locations) * 0x18))
        for i in range(len(self.chest_locations)):
            active = chest_section[i * 0x18 + 0x2]
            state = chest_section[i * 0x18 + 0x3]
            if state >= 0x7F:
                continue
            if active == 1 and state != 1:
                acquired += [self.chest_locations[i]]

        await self.update_stage()
        if self.zone != self.current_zone or self.level != self.current_level:
            return []
        return acquired

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
                if not ctx.auth:
                    await asyncio.sleep(1)
                    continue
                seed_name = await ctx.get_seed_name()
                if seed_name != ctx.seed_name[0:16]:
                    logger.info(f"ROM seed does not match room seed ({seed_name} != {ctx.seed_name}), "
                                f"please load the correct ROM.")
                    await ctx.disconnect()
                    continue
                await ctx.update_stage()
                if ctx.zone != 0x10:
                    await ctx.handle_items()
                    checking = await ctx.location_loop()
                    dead = await ctx.dead()
                    if dead and not ctx.ignore_deathlink:
                        if ctx.deathlink_triggered:
                            ctx.deathlink_triggered = False
                        else:
                            await ctx.send_death(f"{ctx.player_names[ctx.slot]} ran out of food.")
                    if len(checking) > 0:
                        ctx.locations_checked += checking
                        await ctx.check_locations(checking)

                    if ctx.deathlink_pending and ctx.deathlink_enabled:
                        ctx.deathlink_pending = False
                        await ctx.die()

                    goal = await ctx.check_goal()
                    if not ctx.finished_game and goal:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
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
            except Exception as e:
                logger.error(f"Unknown Error Occurred: {e}")
                logger.info(traceback.format_exc())
                await asyncio.sleep(2)
                continue




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


async def _patch_and_launch_game(patch_file: str):
    metadata, output_file = Patch.create_rom_file(patch_file)
    await _patch_opt()
    await _launch_retroarch(output_file)


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

        _restore_opt_files()

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APGL file")
    args = parser.parse_args(args)

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
