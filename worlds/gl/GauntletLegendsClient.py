import asyncio
import socket
import traceback
from typing import List, Optional

import Patch
import Utils
from BaseClasses import ItemClassification
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import ClientStatus, NetworkItem

from .Arrays import (
    base_count,
    boss_level,
    castle_id,
    characters,
    difficulty_convert,
    inv_dict,
    level_locations,
    mirror_levels,
    spawners,
    timers, sounds, colors, vanilla,
)
from .Items import ItemData, items_by_id
from .Locations import LocationData

READ = "READ_CORE_RAM"
WRITE = "WRITE_CORE_RAM"
INV_ADDR = 0xC5BF0
OBJ_ADDR = 0xBC22C
INV_UPDATE_ADDR = 0x56094
INV_LAST_ADDR = 0x56084
ACTIVE_POTION = 0xFD313
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

BOSS_ADDR = 0x289C08
TIME = 0xC5B1C
INPUT = 0xC5BCD


class RetroSocket:
    def __init__(self):
        self.host = "localhost"
        self.port = 55355
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    async def write(self, message: str):
        await asyncio.sleep(0)
        self.socket.sendto(message.encode(), (self.host, self.port))

    async def read(self, message) -> Optional[bytes]:
        await asyncio.sleep(0)
        self.socket.sendto(message.encode(), (self.host, self.port))

        self.socket.settimeout(2)
        try:
            data, addr = self.socket.recvfrom(30000)
        except socket.timeout:
            raise Exception("Socket receive timed out. No data received within the specified timeout.")
        except ConnectionResetError:
            raise Exception("Retroarch is not open. Please open Retroarch and load the correct ROM.")
        response = data.decode().split(" ")
        b = b""
        for s in response[2:]:
            if "-1" in s:
                logger.info("-1 response")
                raise Exception("Client tried to read from an invalid address or could not successfully make a connection to Retroarch.")
            b += bytes.fromhex(s)
        return b

    def status(self) -> bool:
        message = "GET_STATUS"
        self.socket.sendto(message.encode(), (self.host, self.port))
        try:
            data, addr = self.socket.recvfrom(1000)
        except ConnectionResetError:
            raise Exception("Retroarch not detected. Please make sure your ROM is open in Retroarch.")
        return True


class RamChunk:
    def __init__(self, arr: bytes):
        self.raw = arr
        self.split = []

    def iterate(self, length: int):
        self.split = [self.raw[i: i + length] for i in range(0, len(self.raw), length)]


def type_to_name(arr) -> str:
    target_tuple = tuple(arr)
    return inv_dict.get(target_tuple, None)


def name_to_type(name) -> bytes:
    if name == "Fruit" or name == "Meat":
        return bytes([0x0, 0x1, 0x0])
    for key, value in inv_dict.items():
        if value == name:
            return bytes(key)
    logger.info(f"Invalid Item: {name}")
    raise ValueError("Value not found in the dictionary")


class InventoryEntry:
    def __init__(self, arr=None, index=None, player=None):
        if arr is not None:
            self.raw = arr
            self.addr = 0xC5BF0 + (0x400 * player) + (index * 0x10)
            self.on: int = arr[0]
            self.type: bytes = arr[1:4]
            self.name = type_to_name(self.type)
            self.count: int = int.from_bytes(arr[4:8], "little")
            self.n_addr: int = int.from_bytes(arr[12:15], "little")
            self.p_addr: int = int.from_bytes(arr[8:11], "little")
        else:
            self.raw: bytes
            self.addr: int
            self.on = 0
            self.type: bytes
            self.name = ""
            self.count: int
            self.n_addr: int
            self.p_addr: int


class ObjectEntry:
    def __init__(self, arr=None):
        if arr is not None:
            self.raw = arr
        else:
            self.raw: bytes


def message_format(arg: str, params: str) -> str:
    return f"{arg} {params}"


def param_format(adr: int, arr: bytes) -> str:
    return " ".join([hex(adr)] + [f"0x{byte:02X}" for byte in arr])


class GauntletLegendsCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_connected(self):
        logger.info(f"Retroarch Status: {self.ctx.retro_connected}")

    def _cmd_deathlink_toggle(self):
        self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
        logger.info(f"Deathlink {'Enabled.' if self.ctx.deathlink_enabled else 'Disabled.'}")

    def _cmd_players(self, value: int):
        """Set number of local players"""
        value = int(value)
        logger.info(f"Players set from {self.ctx.players} to {min(value, 4)}.")
        self.ctx.players = min(value, 4)


class GauntletLegendsContext(CommonContext):
    command_processor = GauntletLegendsCommandProcessor
    game = "Gauntlet Legends"
    items_handling = 0b101

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.useful: List[NetworkItem] = []
        self.deathlink_pending: bool = False
        self.deathlink_enabled: bool = False
        self.deathlink_triggered: bool = False
        self.ignore_deathlink: bool = False
        self.difficulty: int = 0
        self.players: int = 1
        self.gl_sync_task = None
        self.received_index: int = 0
        self.glslotdata = None
        self.crc32 = None
        self.socket = RetroSocket()
        self.locations_checked: List[int] = []
        self.inventory: List[List[InventoryEntry]] = []
        self.inventory_raw: List[RamChunk] = []
        self.item_objects: List[ObjectEntry] = []
        self.obelisk_objects: List[ObjectEntry] = []
        self.chest_objects: List[ObjectEntry] = []
        self.retro_connected: bool = False
        self.level_loading: bool = False
        self.in_game: bool = False
        self.objects_loaded: bool = False
        self.obelisks: List[NetworkItem] = []
        self.item_locations: List[LocationData] = []
        self.obelisk_locations: List[LocationData] = []
        self.chest_locations: List[LocationData] = []
        self.extra_items: int = 0
        self.extra_spawners: int = 0
        self.limbo: bool = False
        self.in_portal: bool = False
        self.scaled: bool = False
        self.offset: int = -1
        self.clear_counts = None
        self.current_level: bytes = b""
        self.movement: int = 0
        self.init_refactor: bool = False
        self.location_scouts: list[NetworkItem] = []
        self.character_loaded: bool = False

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)

    # Return number of items in inventory
    def inv_count(self, player: int) -> int:
        return len(self.inventory[player])

    # Update self.inventory to current in-game values
    async def inv_read(self):
        self.inventory = []
        self.inventory_raw = []
        for player in range(self.players):
            _inv: List[InventoryEntry] = []
            b = RamChunk(await self.socket.read(message_format(READ, f"0x{format(INV_ADDR + (0x400 * player), 'x')} 1008")))
            if b is None:
                return
            b.iterate(0x10)
            self.inventory_raw += [b]
            for i, arr in enumerate(b.split):
                _inv += [InventoryEntry(arr, i, player)]
            for i in range(len(_inv)):
                if _inv[i].p_addr == 0:
                    _inv = _inv[i:]
                    break
            new_inv: List[InventoryEntry] = []
            new_inv += [_inv[0]]
            addr = new_inv[0].n_addr
            while True:
                if addr == 0:
                    break
                new_inv += [inv for inv in _inv if inv.addr == addr]
                addr = new_inv[-1].n_addr
            self.inventory += [new_inv]

    # Return InventoryEntry if item of name is in inv, else return None
    async def item_from_name(self, name: str, player: int) -> InventoryEntry | None:
        await self.inv_read()
        for i in range(0, self.inv_count(player)):
            if self.inventory[player][i].name == name:
                return self.inventory[player][i]
        return None

    # Return True if bitwise and evaluates to non-zero value
    async def inv_bitwise(self, name: str, bit: int, player: int) -> bool:
        item = await self.item_from_name(name, player)
        if item is None:
            return False
        return (item.count & bit) != 0

    # Return pointer of object section of RAM
    async def get_obj_addr(self) -> int:
        return (
            int.from_bytes(await self.socket.read(message_format(READ, f"0x{format(OBJ_ADDR, 'x')} 4")), "little")
        ) & 0xFFFFF

    # Read a subsection of the objects loaded into RAM
    # Objects are 0x3C bytes long
    # Modes: 0 = items, 1 = chests/barrels
    async def obj_read(self, mode=0):
        _obj = []
        b: RamChunk
        if mode == 0:
            while True:
                b = RamChunk(
                    await self.socket.read(
                        message_format(
                            READ,
                            f"0x{format(OBJ_ADDR, 'x')} {(len(self.item_locations) + self.extra_items) * 0x3C}",
                        ),
                    ),
                )
                b.iterate(0x3C)
                count = 0
                for obj in b.split:
                    if obj[0] == 0xFF and obj[1] == 0xFF:
                        count += 1
                count -= self.extra_items
                if count <= 0:
                    break
                self.extra_items = count
        else:
            spawner_count = len([spawner for spawner in spawners[(self.current_level[1] << 4) + (
                self.current_level[0] if self.current_level[1] != 1 else castle_id.index(self.current_level[0]) + 1)] if
                                 self.difficulty >= spawner])
            if self.extra_spawners == 0:
                count = 0
                for i in range((spawner_count + 99) // 100):
                    b = RamChunk(
                        await self.socket.read(
                            message_format(
                                READ,
                                f"0x{format(OBJ_ADDR + ((len(self.item_locations) + self.extra_items + (i * 100)) * 0x3C), 'x')} {min((spawner_count - (100 * i)), 100) * 0x3C}",
                            ),
                        ),
                    )
                    b.iterate(0x3C)
                    for obj in b.split:
                        if obj[0] == 0xFF and obj[1] == 0xFF:
                            count += 1
                self.extra_spawners += count
            b = RamChunk(
                await self.socket.read(
                    message_format(
                        READ,
                        f"0x{format(OBJ_ADDR + ((len(self.item_locations) + self.extra_items + self.extra_spawners + spawner_count) * 0x3C), 'x')} {(len(self.chest_locations) + 2) * 0x3C}",
                    ),
                ),
            )
            b.iterate(0x3C)
        for arr in b.split:
            _obj += [ObjectEntry(arr)]
        _obj = [obj for obj in _obj if obj.raw[0] != 0xFF and obj.raw[1] != 0xFF]
        if mode == 1:
            self.chest_objects = _obj[:len(self.chest_locations)]
        else:
            self.item_objects = _obj[:len(self.item_locations)]

    # Update item count of an item.
    # If the item is new, add it to your inventory
    async def inv_update(self, name: str, count: int, one=None):
        await self.inv_read()
        if "Runestone" in name:
            name = "Runestone"
        if "Fruit" in name or "Meat" in name:
            name = "Health"
        if "Obelisk" in name:
            name = "Obelisk"
        if "Mirror" in name:
            name = "Mirror Shard"
        zero = False
        if one is None:
            for player in range(self.players):
                added = False
                for item in self.inventory[player]:
                    if item.name == name:
                        zero = (item.count == 0 and "Health" not in name)
                        if name in timers:
                            count *= 96
                        if "Compass" in name:
                            item.count = count
                        elif "Health" in name:
                            max_health = await self.item_from_name("Max", player)
                            item.count = min(max(item.count + count, 0), max_health.count)
                        elif "Runestone" in name or "Mirror" in name or "Obelisk" in name:
                            item.count |= count
                        else:
                            item.count += count
                        await self.write_item(item)
                        added = True
                if not added:
                    await self.inv_add(name, count, player)
            if zero:
                await self.inv_refactor()
        else:
            for item in self.inventory[one]:
                if item.name == name:
                    zero = item.count == 0
                    if name in timers:
                        count *= 96
                    if "Compass" in name:
                        item.count = count
                    elif "Health" in name:
                        max_health = await self.item_from_name("Max", one)
                        item.count = min(max(item.count + count, 0), max_health.count)
                    elif "Runestone" in name or "Mirror" in name or "Obelisk" in name:
                        item.count |= count
                    else:
                        item.count += count
                    await self.write_item(item)
                    if zero:
                        await self.inv_refactor()
                    return
            await self.inv_add(name, count, one)

    # Rewrite entire inventory in RAM.
    # This is necessary since item entries are not cleared after full use until a level is completed.
    async def inv_refactor(self, new=None, one=None):
        await self.inv_read()
        if new is not None:
            if one is None:
                for player in range(self.players):
                    self.inventory[player] += [new]
            else:
                self.inventory[one] += [new]
        for player in range(self.players):
            for i, item in enumerate(self.inventory[player]):
                if item.name is not None:
                    if "Potion" in item.name and item.count != 0:
                        await self.socket.write(
                            message_format(
                                WRITE, param_format(ACTIVE_POTION + (0x1F0 * player), int.to_bytes(item.type[2] // 0x10, 1, "little")),
                            ),
                        )
                if i == 0:
                    item.p_addr = 0
                    item.addr = INV_ADDR + (0x400 * player)
                    item.n_addr = item.addr + 0x10
                    self.inventory[player][i] = item
                    continue
                item.addr = INV_ADDR + (0x400 * player) + (0x10 * i)
                item.p_addr = item.addr - 0x10
                if i == (len(self.inventory[player]) - 1):
                    item.n_addr = 0
                    self.inventory[player][i] = item
                    break
                item.n_addr = item.addr + 0x10
                self.inventory[player][i] = item

            for item in self.inventory[player]:
                await self.write_item(item)

            for i, raw in enumerate(self.inventory_raw[player].split[len(self.inventory[player]):], len(self.inventory[player])):
                item = InventoryEntry(raw, i, player)
                if item.type != bytes([0, 0, 0]):
                    await self.write_item(
                        InventoryEntry(
                            bytes([0, 0, 0, 0, 0, 0, 0, 0])
                            + int.to_bytes(item.addr + 0x10, 3, "little")
                            + bytes([0xE0, 0, 0, 0, 0]),
                            i,
                        player),
                    )

            await self.socket.write(
                message_format(WRITE, param_format(INV_UPDATE_ADDR + (4 * player), int.to_bytes(self.inventory[player][-1].addr, 3, "little"))),
            )
            await self.socket.write(
                message_format(WRITE,
                               param_format(INV_LAST_ADDR + (4 * player), int.to_bytes(self.inventory[player][-1].addr + 0x10, 3, "little"))),
            )

            await self.socket.write(f"{WRITE} 0x{format(0xC6BF0 + (4 * player), 'x')} 0x{format(self.inv_count(player), 'x')}")

    # Add new item to inventory
    # Call refactor at the end to write it into ram correctly
    async def inv_add(self, name: str, count: int, one=None):
        new = InventoryEntry()
        new.name = name
        if name == "Key":
            new.on = 1
        new.count = count
        if name in timers:
            new.count *= 0x96
        new.type = name_to_type(name)
        await self.inv_refactor(new, one)

    # Write a single item entry into RAM
    async def write_item(self, item: InventoryEntry):
        b = (
                int.to_bytes(item.on, 1)
                + item.type
                + int.to_bytes(item.count, 4, "little")
                + int.to_bytes(item.p_addr, 3, "little")
                + (int.to_bytes(0xE0) if item.p_addr != 0 else int.to_bytes(0x0))
                + int.to_bytes(item.n_addr, 3, "little")
                + (int.to_bytes(0xE0) if item.n_addr != 0 else int.to_bytes(0x0))
        )
        await self.socket.write(message_format(WRITE, param_format(item.addr, b)))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(GauntletLegendsContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.retro_connected = False
        await self.var_reset()
        await super(GauntletLegendsContext, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.retro_connected = False
        await self.var_reset()
        await super(GauntletLegendsContext, self).disconnect()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.slot = args["slot"]
            self.glslotdata = args["slot_data"]
            self.players = self.glslotdata["players"]
            logger.info(f"Players set to {self.players}.")
            if self.socket.status():
                self.retro_connected = True
                self.deathlink_enabled = self.glslotdata["death_link"]
            else:
                raise Exception("Retroarch not detected. Please open you patched ROM in Retroarch.")
        elif cmd == "Retrieved":
            if "keys" not in args:
                logger.warning(f"invalid Retrieved packet to GLClient: {args}")
                return
            cc = None
            try:
                cc = self.stored_data.get(f"gl_cc_T{self.team}_P{self.slot}", None)
            except Exception:
                logger.info(traceback.format_exc())
            if cc is not None:
                logger.info("Received clear counts from server")
                self.clear_counts = cc
            else:
                self.clear_counts = {}
        elif cmd == "LocationInfo":
            self.location_scouts = args["locations"]

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
                        await self.inv_update(characters[self.glslotdata["characters"][player] - 1], 50, player)
                temp = await self.item_from_name("Key", player)
                if temp is None and self.glslotdata["keys"] == 1:
                    await self.inv_update("Key", 9000, player)
                temp = await self.item_from_name("Speed Boots", player)
                if temp is None and self.glslotdata["speed"] == 1:
                    await self.inv_update("Speed Boots", 2000, player)
            i = compass.count
            if i - 1 < len(self.items_received):
                for index in range(i - 1, len(self.items_received)):
                    item = self.items_received[index].item
                    if items_by_id[item].item_name == "Death":
                        continue
                    await self.inv_update(items_by_id[item].item_name, base_count[items_by_id[item].item_name])
            await self.inv_update("Compass", len(self.items_received) + 1)

    # Read current timer in RAM
    async def read_time(self) -> int:
        return int.from_bytes(await self.socket.read(message_format(READ, f"0x{format(TIME, 'x')} 2")), "little")

    # Read currently loaded level in RAM
    async def read_level(self) -> bytes:
        level = await self.socket.read(message_format(READ, f"0x{format(ACTIVE_LEVEL, 'x')} 2"))
        return level

    # Read value that is 1 while a level is currently loading
    async def check_loading(self) -> bool:
        if self.in_portal or self.level_loading:
            time = await self.read_time()
            return time == 0
        return False

    # Read number of loaded players in RAM
    async def active_players(self) -> int:
        temp = await self.socket.read(message_format(READ, f"0x{format(PLAYER_COUNT, 'x')} 1"))
        return temp[0]

    # Read level of player 1 in RAM
    async def player_level(self) -> int:
        temp = await self.socket.read(message_format(READ, f"0x{format(PLAYER_LEVEL, 'x')} 1"))
        return temp[0]

    # Update value at player count address
    # This directly impacts the difficulty of the level when it is loaded
    async def scale(self):
        level = await self.read_level()
        if self.movement != 0x12:
            level = [0x1, 0xF]
        players = await self.active_players()
        player_level = await self.player_level()
        max_value: int = max(self.glslotdata["max"], self.players)
        scale_value = min(max(((player_level - difficulty_convert[level[1]]) // 5), 0), 3)
        if self.glslotdata["instant_max"] == 1:
            scale_value = max_value
        # mountain_value = min(player_level // 10, 3)
        await self.socket.write(
            message_format(WRITE, f"0x{format(PLAYER_COUNT, 'x')} 0x{format(min(players + scale_value, max_value), 'x')}"),
        )
        self.scaled = True

    # Prepare locations that are going to be in the currently loading level
    async def scout_locations(self, ctx: "GauntletLegendsContext") -> None:
        level = await self.read_level()
        if level in boss_level:
            for i in range(4):
                await self.socket.write(
                    message_format(
                        WRITE,
                        param_format(
                            BOSS_ADDR, bytes([self.glslotdata["shards"][i][1], 0x0, self.glslotdata["shards"][i][0]]),
                        ),
                    ),
                )
        if self.movement != 0x12:
            level = [0x1, 0xF]
        self.current_level = level
        players = await self.active_players()
        player_level = await self.player_level()
        if self.clear_counts.get(str(level), 0) != 0:
            self.difficulty = min(players + (min(player_level // vanilla[level[1]], 3)), 4)
        else:
            self.difficulty = players
        _id = level[0]
        if level[1] == 1:
            _id = castle_id.index(level[0]) + 1
        raw_locations = []
        for location in [location for location in level_locations.get((level[1] << 4) + _id, []) if self.difficulty >= location.difficulty]:
            if "Chest" in location.name:
                if self.glslotdata["chests"]:
                    raw_locations += [location]
            elif "Barrel" in location.name and "Barrel of Gold" not in location.name:
                if self.glslotdata["barrels"]:
                    raw_locations += [location]
            else:
                raw_locations += [location]
        await ctx.send_msgs(
            [
                {
                    "cmd": "LocationScouts",
                    "locations": [
                        location.id
                        for location in [location for location in raw_locations if min(self.difficulty, self.glslotdata["max"]) >= location.difficulty]
                    ],
                    "create_as_hint": 0,
                },
            ],
        )
        while len(self.location_scouts) == 0:
            await asyncio.sleep(0.1)
        self.obelisks = [
            item
            for item in self.location_scouts
            if "Obelisk" in items_by_id.get(item.item, ItemData(0, "", ItemClassification.filler)).item_name
               and item.player == self.slot
        ]
        self.useful = [
            item
            for item in self.location_scouts
            if "Obelisk" not in items_by_id.get(item.item, ItemData(0, "", ItemClassification.filler)).item_name
                and (items_by_id.get(item.item, ItemData(0, "", ItemClassification.filler)).progression == ItemClassification.useful
                or items_by_id.get(item.item, ItemData(0, "", ItemClassification.filler)).progression == ItemClassification.progression)
                and item.player == self.slot
        ]
        self.obelisk_locations = [
            location for location in raw_locations if location.id in [item.location for item in self.obelisks]
        ]
        self.item_locations = [
            location for location in raw_locations
            if ("Chest" not in location.name
                and ("Barrel" not in location.name or "Barrel of Gold" in location.name))
                and location not in self.obelisk_locations
                or location.id in [item.location for item in self.useful]
        ]
        self.chest_locations = [
            location for location in raw_locations
            if location not in self.obelisk_locations and location not in self.item_locations]
        max_value: int = self.glslotdata['max']
        logger.info(f"Items: {len(self.item_locations)} Chests: {len(self.chest_locations)} Obelisks: {len(self.obelisk_locations)}")
        logger.info(
            f"Locations: {len([location for location in self.obelisk_locations + self.item_locations + self.chest_locations if location.difficulty <= max_value and location.id not in self.locations_checked])} Difficulty: { max_value if self.glslotdata['instant_max'] else self.difficulty}",
        )

    # Compare values of loaded objects to see if they have been collected
    # Sends locations out to server based on object lists read in obj_read()
    # Local obelisks and mirror shards have special cases
    async def location_loop(self) -> List[int]:
        await self.obj_read()
        await self.obj_read(1)
        acquired = []
        for i, obj in enumerate(self.item_objects):
            if obj.raw[24] != 0x0:
                if self.item_locations[i].id not in self.locations_checked:
                    acquired += [self.item_locations[i].id]
        for j in range(len(self.obelisk_locations)):
            ob = await self.inv_bitwise("Obelisk", base_count[items_by_id[self.obelisks[j].item].item_name], 0)
            if ob:
                acquired += [self.obelisk_locations[j].id]
        for k, obj in enumerate(self.chest_objects):
            if "Chest" in self.chest_locations[k].name:
                if obj.raw[24] != 0x0:
                    if self.chest_locations[k].id not in self.locations_checked:
                        acquired += [self.chest_locations[k].id]
            else:
                if obj.raw[0x33] != 0:
                    if self.chest_locations[k].id not in self.locations_checked:
                        acquired += [self.chest_locations[k].id]
        dead = await self.dead()
        if dead:
            return []
        return acquired

    # Returns 1 if players are spinning in a portal
    async def portaling(self) -> int:
        temp = await self.socket.read(message_format(READ, f"0x{format(PLAYER_PORTAL, 'x')} 1"))
        return temp[0]

    # Returns a number that shows if the player currently has control or not
    async def limbo_check(self, offset=0) -> int:
        temp = await self.socket.read(message_format(READ, f"0x{format(PLAYER_MOVEMENT + offset, 'x')} 1"))
        return temp[0]

    # Returns True of the player is dead
    async def dead(self) -> bool:
        temp = await self.socket.read(message_format(READ, f"0x{format(PLAYER_KILL, 'x')} 1"))
        if (temp[0] & 0xF) == 0x1:
            self.ignore_deathlink = True
        return ((temp[0] & 0xF) == 0x8) or ((temp[0] & 0xF) == 0x1)

    # Returns a number that tells if the player is fighting a boss currently
    async def boss(self) -> int:
        temp = await self.socket.read(message_format(READ, f"0x{format(PLAYER_BOSSING, 'x')} 1"))
        return temp[0]

    # Checks if a player is currently exiting a level
    # Checks for both death and completion
    # Resets values since level is no longer being played
    async def level_status(self, ctx: "GauntletLegendsContext") -> bool:
        portaling = await self.portaling()
        dead = await self.dead()
        boss = await self.boss()
        if portaling or dead or (self.current_level in boss_level and boss == 0):
            if self.in_game:
                if portaling or (self.current_level in boss_level and boss == 0):
                    self.clear_counts[str(self.current_level)] = self.clear_counts.get(str(self.current_level), 0) + 1
                    if self.current_level in mirror_levels:
                        await ctx.send_msgs(
                            [
                                {
                                    "cmd": "LocationChecks",
                                    "locations": [
                                        location.id
                                        for location in level_locations[
                                            (self.current_level[1] << 4) + self.current_level[0]
                                            ]
                                        if "Mirror" in location.name
                                    ],
                                },
                            ],
                        )
                if dead and not (self.current_level in boss_level and boss == 0):
                    if self.deathlink_triggered:
                        self.deathlink_triggered = False
                    elif self.ignore_deathlink:
                        self.ignore_deathlink = False
                    else:
                        if self.deathlink_enabled:
                            await ctx.send_death(f"{ctx.auth} didn't eat enough meat.")
            await self.var_reset()
            return True
        return False

    async def var_reset(self):
        self.objects_loaded = False
        self.extra_items = 0
        self.item_locations = []
        self.item_objects = []
        self.chest_locations = []
        self.chest_objects = []
        self.obelisk_locations = []
        self.obelisks = []
        self.in_game = False
        self.level_loading = False
        self.scaled = False
        self.offset = -1
        self.movement = 0
        self.difficulty = 0
        self.location_scouts = []
        self.ignore_deathlink = False

    # Prep arrays with locations and objects
    async def load_objects(self, ctx: "GauntletLegendsContext"):
        await self.scout_locations(ctx)
        await self.obj_read()
        await self.obj_read(1)
        self.objects_loaded = True

    async def die(self):
        self.deathlink_triggered = True
        char = await self.socket.read(message_format(READ, f"0x{format(PLAYER_CLASS, 'x')} 1"))
        char = char[0]
        color = await self.socket.read(message_format(READ, f"0x{format(PLAYER_COLOR, 'x')} 1"))
        color = color[0]
        await self.socket.write(message_format(WRITE, param_format(SOUND_ADDRESS, int.to_bytes(colors[color], 4, "little") + int.to_bytes(sounds[char], 4, "little") + int.to_bytes(0xBB, 4, "little"))))
        await self.socket.write(message_format(WRITE, param_format(SOUND_START, int.to_bytes(0xE00AE718, 4, "little"))))
        await asyncio.sleep(2)
        await self.socket.write(message_format(WRITE, param_format(SOUND_START, int.to_bytes(0x0, 4, "little"))))
        await self.socket.write(message_format(WRITE, param_format(PLAYER_KILL, int.to_bytes(0x7, 1, "little"))))

    def run_gui(self):
        from kvui import GameManager

        class GLManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago Gauntlet Legends Client"

        self.ui = GLManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def _patch_and_run_game(patch_file: str):
    metadata, output_file = Patch.create_rom_file(patch_file)


# Sends player items from server
# Checks for player status to see if they are in/loading a level
# Checks location status inside of levels
async def gl_sync_task(ctx: GauntletLegendsContext):
    logger.info("Starting N64 connector...")
    logger.info("Use /players to set the number of people playing locally. This is required for the client to function.")
    while not ctx.exit_event.is_set():
        if ctx.retro_connected:
            cc_str: str = f"gl_cc_T{ctx.team}_P{ctx.slot}"
            pl_str: str = f"gl_pl_T{ctx.team}_P{ctx.slot}"
            try:
                ctx.set_notify(cc_str)
                if not ctx.auth:
                    ctx.retro_connected = False
                    continue
            except Exception:
                logger.info(traceback.format_exc())
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
            if ctx.limbo:
                try:
                    limbo = await ctx.limbo_check(0x78)
                    if limbo:
                        ctx.limbo = False
                        await asyncio.sleep(4)
                    else:
                        await asyncio.sleep(0.05)
                        continue
                except Exception:
                    logger.info(traceback.format_exc())
            try:
                await ctx.handle_items()
                if ctx.deathlink_pending and ctx.deathlink_enabled:
                    ctx.deathlink_pending = False
                    await ctx.die()
            except Exception:
                logger.info(traceback.format_exc())
            if not ctx.level_loading and not ctx.in_game:
                try:
                    if not ctx.in_portal:
                        ctx.in_portal = await ctx.portaling()
                    if ctx.in_portal and not ctx.init_refactor:
                        await asyncio.sleep(0.1)
                        ctx.movement = await ctx.limbo_check()
                        await ctx.inv_refactor()
                        ctx.init_refactor = True
                    ctx.level_loading = await ctx.check_loading()
                except Exception:
                    logger.info(traceback.format_exc())
            if ctx.level_loading:
                try:
                    ctx.in_portal = False
                    ctx.init_refactor = False
                    if not ctx.scaled:
                        logger.info("Scaling level...")
                        await asyncio.sleep(0.2)
                        await ctx.scale()
                    ctx.in_game = not await ctx.check_loading()
                except Exception:
                    logger.info(traceback.format_exc())
                    await ctx.var_reset()
            if ctx.in_game:
                ctx.level_loading = False
                try:
                    if not ctx.objects_loaded:
                        logger.info("Loading Objects...")
                        await ctx.load_objects(ctx)
                        await asyncio.sleep(1)
                    if await ctx.level_status(ctx):
                        try:
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
                        except Exception:
                            logger.info(traceback.format_exc())
                        ctx.limbo = True
                        await asyncio.sleep(0.05)
                        continue
                    await asyncio.sleep(0.1)
                    checking = await ctx.location_loop()
                    if len(checking) > 0:
                        ctx.locations_checked += checking
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checking}])
                    bitwise = await ctx.inv_bitwise("Hell", 0x100, 0)
                    if not ctx.finished_game and bitwise:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                except Exception:
                    logger.info(traceback.format_exc())
            await asyncio.sleep(0.1)
        else:
            await asyncio.sleep(1)
            continue


def launch():
    Utils.init_logging("GauntletLegendsClient", exception_logger="Client")

    async def main():
        parser = get_base_parser()
        parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APGL file")
        args = parser.parse_args()
        if args.patch_file:
            await asyncio.create_task(_patch_and_run_game(args.patch_file))
        ctx = GauntletLegendsContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        ctx.gl_sync_task = asyncio.create_task(gl_sync_task(ctx), name="Gauntlet Legends Sync Task")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()
