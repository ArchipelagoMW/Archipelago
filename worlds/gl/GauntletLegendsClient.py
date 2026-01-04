import asyncio
import settings
import os
import re
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
    item_ids,
    level_locations,
    sounds,
    colors,
    portals,
    spawner_trap_ids,
    player_compass_index
)
from .Items import ItemData, items_by_id

READ = "READ_CORE_RAM"
WRITE = "WRITE_CORE_RAM"
PLAYER_CLASS = 0xFD30F
PLAYER_COLOR = 0xFD30E
SOUND_ADDRESS = 0xAE740
SOUND_START = 0xEEFC
PLAYER_KILL = 0xFD300
PLAYER_ACTIVE = 0xFD36E
BOSS_GOAL = 0x45D34
BOSS_GOAL_BACKUP = 0x45D3C
LOCATIONS_BASE_ADDRESS = 0x64A68
ZONE_ID = 0x6CA58
LEVEL_ID = 0x6CA5C

MOD_ITEM_ID = 0xD0800
MOD_QUANTITY = 0xD0804
MOD_PLAYER_ID = 0xD0808
MOD_OBELISK_QUANTITY = 0xD07E4
MOD_BOSS_GOAL = 0xD07E5
MOD_PLAYERS_LIST = 0xD07D0
MOD_COMPASS_COUNT = 0xD07D4


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


def message_format(arg: str, params: str) -> str:
    return f"{arg} {params}"


def param_format(adr: int, arr: bytes) -> str:
    return " ".join([hex(adr)] + [f"0x{byte:02X}" for byte in arr])


class GauntletLegendsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_deathlink_toggle(self):
        """Toggle Deathlink on or off"""
        self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
        self.ctx.update_death_link(self.ctx.deathlink_enabled)
        logger.info(f"Deathlink {('Enabled.' if self.ctx.deathlink_enabled else 'Disabled.')}")


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
        self.gl_sync_task = None
        self.glslotdata = None
        self.socket = RetroSocket()
        self.rom_loaded: bool = False
        self.locations_checked: list[int] = []
        self.retro_connected: bool = False
        self.scouted: bool = False
        self.obelisks: list[NetworkItem] = []
        self.item_locations: list[int] = []
        self.obelisk_locations: list[int] = []
        self.chest_locations: list[int] = []
        self.spawner_locations: list[int] = []
        self.item_address: int = 0
        self.chest_address: int = 0
        self.spawner_address: int = 0
        self.vanilla_spawner_count: int = 0
        self.zone: int = 0
        self.level: int = 0
        self.current_zone: int = 0
        self.current_level: int = 0
        self.level_id: int = 0
        self.location_scouts: list[NetworkItem] = []
        self.players: list[int] = []
        self.queued_traps: list[tuple[str, int, bool]] = []

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    async def update_stage(self):
        self.zone = await self._read_ram_int(ZONE_ID, 1)
        self.level = await self._read_ram_int(LEVEL_ID, 1)

    async def check_goal(self) -> bool:
        if self.glslotdata is None:
            return False
        if self.glslotdata["goal"] == 1:
            goal = await self._read_ram_int(BOSS_GOAL, 4)
            backup = await self._read_ram_int(BOSS_GOAL_BACKUP, 4)
            return goal == 0xA or backup == 0xA
        elif self.glslotdata["goal"] == 2:
            goal = await self._read_ram_int(MOD_BOSS_GOAL, 1)
            return goal >= self.glslotdata["boss_goal_count"]

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
        await self._write_ram(MOD_ITEM_ID,
                              int.to_bytes((item_ids[name] if not infinite_count else item_ids[name] & 0xFFFF), 4,
                                           "little"))
        await self._write_ram(MOD_QUANTITY, int.to_bytes(count, 4, "little", signed=True))
        await self._write_ram(MOD_PLAYER_ID, int.to_bytes(player, 4, "little"))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(GauntletLegendsContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.glslotdata = args["slot_data"]
            self.deathlink_enabled = bool(self.glslotdata["death_link"])
            self.update_death_link(self.deathlink_enabled)
        elif cmd == "LocationInfo":
            self.location_scouts = args["locations"]
        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]

    # Update inventory based on items received from server
    # Also adds starting items based on a few yaml options
    async def handle_items(self):
        self.players = list(await self._read_ram(MOD_PLAYERS_LIST, 4))
        players = [player for player in self.players if player != 0]
        for player in players:
            compass = await self._read_ram_int(MOD_COMPASS_COUNT + (2 * player_compass_index[player]), 2)
            if compass - 1 < len(self.items_received):
                for index in range(compass - 1, len(self.items_received)):
                    item = self.items_received[index].item
                    if player != players[0] and item in spawner_trap_ids:
                        continue
                    item_name = items_by_id[item].item_name
                    if self.current_zone in (0x8, 0xE) and item in spawner_trap_ids:
                        if len([trap for trap in self.queued_traps if trap[1] != index]) < 1:
                            self.queued_traps.append((item_name, index, False))
                    await self.give_item(item_name, player)
                    await self.update_item("Compass", 1, player)

    async def give_item(self, item_name: str, player: int):
        await self.wait_for_mod_clear()
        await asyncio.sleep(0.02)
        await self.update_item(item_name, base_count[item_name], player)
        await self.wait_for_mod_clear()
        await asyncio.sleep(0.02)

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
            self.spawner_locations = []
            self.useful = []
            self.obelisks = []
            self.vanilla_spawner_count = 0

            raw_locations = [location for location in level_locations.get(self.level_id, []) if
                             "Mirror" not in location.name and "Skorne" not in location.name]
            scoutable_location_ids = [location.id for location in raw_locations if
                                      location.id in ctx.checked_locations or location.id in self.missing_locations]

            # Scout locations if any exist
            if raw_locations:
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": scoutable_location_ids,
                    "create_as_hint": 0,
                }])
                while not self.location_scouts:
                    await asyncio.sleep(0.1)

            # Build lookup for scouted items by location
            scouted_by_location = {item.location: item for item in self.location_scouts}

            # Categorize scouted locations - mirror ROM's patch_items logic exactly
            for loc in raw_locations:
                scouted_item = scouted_by_location.get(loc.id)
                if not scouted_item:
                    continue  # No item at this location (item[0] == 0 in ROM)

                item_id = scouted_item.item
                item_player = scouted_item.player
                item_data = items_by_id.get(item_id, ItemData())
                is_chest = "Chest" in loc.name or ("Barrel" in loc.name and "Barrel of Gold" not in loc.name)

                # Skip obelisk locations (ROM handles separately with continue)
                if "Obelisk" in loc.name:
                    if "Obelisk" in item_data.item_name and item_player == self.slot:
                        self.obelisk_locations.append(loc.id)
                        self.obelisks.append(scouted_item)
                    # else: obelisk location becomes item, handled below as item_location
                    continue

                # Check spawner (ROM: item[1] == player and item[0] in SPAWNER_TRAP_IDS)
                if item_player == self.slot and item_id in spawner_trap_ids:
                    self.spawner_locations.append(loc.id)
                    continue

                # Check non-local player (ROM: item[1] != player) - stays as item/chest
                if item_player != self.slot:
                    if is_chest:
                        self.chest_locations.append(loc.id)
                    else:
                        self.item_locations.append(loc.id)
                    continue

                # Check obelisk item at non-obelisk location (ROM: "Obelisk" in item_name)
                if "Obelisk" in item_data.item_name:
                    self.obelisk_locations.append(loc.id)
                    self.obelisks.append(scouted_item)
                    continue

                # Check useful/progression chest -> item conversion
                if item_data.progression in (ItemClassification.useful, ItemClassification.progression) and is_chest:
                    self.item_locations.append(loc.id)
                    self.useful.append(scouted_item)
                    continue

                # Regular item/chest
                if is_chest:
                    self.chest_locations.append(loc.id)
                else:
                    self.item_locations.append(loc.id)

            self.scouted = True
        except Exception:
            logger.error(traceback.format_exc())

    async def location_loop(self) -> list[int]:
        if self.current_zone == 0:
            self.current_zone = self.zone
            self.current_level = self.level
            self.level_id = (self.current_zone << 4) + self.current_level

        zone_or_level_changed = self.zone != self.current_zone or self.level != self.current_level
        if zone_or_level_changed:
            if self.current_level & 0x8 == 0x8 and self.level_id != 0x58 and not await self.dead():
                await self.check_locations([loc.id for loc in level_locations[self.level_id]
                                            if "Mirror Shard" in loc.name or "Skorne" in loc.name])
            self.current_zone = self.zone
            self.current_level = self.level
            self.level_id = (self.current_zone << 4) + self.current_level
            self.scouted = False
            await asyncio.sleep(2)

        if self.current_zone in (0x8, 0xE):
            return []

        if not self.scouted:
            await self.scout_locations(self)

        active = await self._read_ram_int(PLAYER_ACTIVE, 1)
        if active == 0:
            return []

        if len(self.queued_traps) > 0:
            for i, trap_name, index, triggered in enumerate(self.queued_traps):
                if not triggered:
                    await self.give_item(trap_name, self.players[0])
                    self.queued_traps[i] = (trap_name, index, True)

            self.queued_traps = []

        locations_address = await self._read_ram_int(LOCATIONS_BASE_ADDRESS, 4) & 0xFFFFFF
        self.item_address = await self._read_ram_int(locations_address + 0x14, 4)
        self.spawner_address = await self._read_ram_int(locations_address + 0x1C, 4)
        self.chest_address = await self._read_ram_int(locations_address + 0x30, 4)

        # Read vanilla spawner count from level header (2 bytes at offset 0x28)
        spawner_count_data = await self._read_ram(locations_address + 0x6, 2)
        if spawner_count_data and not self.vanilla_spawner_count:
            total_spawner_count = int.from_bytes(spawner_count_data, "little")
            # Vanilla count is total minus the ones we added
            self.vanilla_spawner_count = total_spawner_count - len(self.spawner_locations)

        if 0x7FFF0BAD in (self.item_address, self.chest_address, self.spawner_address):
            return []

        self.item_address &= 0xFFFFFF
        self.spawner_address &= 0xFFFFFF
        self.chest_address &= 0xFFFFFF

        acquired = []

        item_section = await self._read_ram(self.item_address, len(self.item_locations) * 0x18)
        for i, loc_id in enumerate(self.item_locations):
            offset = i * 0x18
            active, state = item_section[offset + 0x2], item_section[offset + 0x3]
            if state < 0x7F and active == 1 and state == 0:
                acquired.append(loc_id)

        obelisk = await self._read_ram_int(MOD_OBELISK_QUANTITY, 1)
        for j, loc_id in enumerate(self.obelisk_locations):
            bit = base_count[items_by_id[self.obelisks[j].item].item_name] - 1
            if obelisk & (1 << bit):
                acquired.append(loc_id)

        chest_section = await self._read_ram(self.chest_address, len(self.chest_locations) * 0x18)
        for i, loc_id in enumerate(self.chest_locations):
            offset = i * 0x18
            active, state = chest_section[offset + 0x2], chest_section[offset + 0x3]
            if state < 0x7F and active == 1 and state != 1:
                acquired.append(loc_id)

        # Check spawner locations - these are added after vanilla spawners
        # Read spawners starting after vanilla_spawner_count
        if self.spawner_locations:
            spawner_start = self.spawner_address + (self.vanilla_spawner_count * 0x1C)
            spawner_section = await self._read_ram(spawner_start, len(self.spawner_locations) * 0x1C)
            for i, loc_id in enumerate(self.spawner_locations):
                offset = i * 0x1C
                active, state, hit = spawner_section[offset + 0x2], spawner_section[offset + 0x3], spawner_section[offset + 0x1A]
                if active == 1 and hit == 1:
                    acquired.append(loc_id)

        await self.update_stage()
        return [] if self.zone != self.current_zone or self.level != self.current_level else acquired

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
        try:
            if not ctx.retro_connected:
                logger.info("Attempting to connect to Retroarch...")
                status = await ctx.socket.status()
                ctx.retro_connected = True
                ctx.rom_loaded = "CONTENTLESS" not in status
                logger.info("Connected to Retroarch")
                continue

            if not ctx.rom_loaded:
                status = await ctx.socket.status()
                if "CONTENTLESS" in status:
                    logger.info("No ROM loaded, waiting...")
                    await asyncio.sleep(3)
                    continue
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
            if ctx.zone == 0x10:
                continue

            await ctx.handle_items()
            checking = await ctx.location_loop()
            dead = await ctx.dead()

            if dead and not ctx.ignore_deathlink and not ctx.deathlink_triggered:
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} ran out of food.")
            ctx.deathlink_triggered = False

            if checking:
                ctx.locations_checked += checking
                await ctx.check_locations(checking)

            if ctx.deathlink_pending and ctx.deathlink_enabled:
                ctx.deathlink_pending = False
                await ctx.die()

            if not ctx.finished_game and await ctx.check_goal():
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        except Exception as e:
            logger.error(f"Error: {e}\n{traceback.format_exc()}")
            ctx.socket = RetroSocket()
            ctx.retro_connected = False
            await asyncio.sleep(2)


_original_opt_content: dict[str, str | None] = {}


async def _patch_opt():
    """Create RetroArch core options override for CountPerOp=1."""
    retroarch_path = settings.get_settings().gl_options.retroarch_path
    override_dir = os.path.join(retroarch_path, "config", "Mupen64Plus-Next")
    os.makedirs(override_dir, exist_ok=True)
    override_path = os.path.join(override_dir, "Mupen64Plus-Next.opt")
    target_setting = 'mupen64plus-CountPerOp = "1"'

    if override_path not in _original_opt_content:
        _original_opt_content[override_path] = open(override_path).read() if os.path.exists(override_path) else None

    content = _original_opt_content[override_path] or ""
    if target_setting in content:
        return

    if "mupen64plus-CountPerOp" in content:
        content = re.sub(r'mupen64plus-CountPerOp\s*=\s*"[^"]*"', target_setting, content)
    else:
        content = content.rstrip("\n") + f"\n{target_setting}\n" if content else f"{target_setting}\n"

    with open(override_path, "w") as f:
        f.write(content)


def _restore_opt_files():
    for path, original in _original_opt_content.items():
        try:
            if original is None and os.path.exists(path):
                os.remove(path)
            elif original is not None:
                with open(path, "w") as f:
                    f.write(original)
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
