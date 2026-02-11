import os
import time
from typing import Dict, List, Tuple

import ModuleUpdate
from Utils import async_start

import asyncio
from pymem import pymem

from NetUtils import ClientStatus, NetworkItem
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop, ClientCommandProcessor, handle_url_arg

from .Items import item_data_table, inv_item_table
from .Locations import location_data_table, FF12OpenWorldLocationData

tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor
    CommonContext = TrackerGameContext
    ClientCommandProcessor = TrackerCommandProcessor
    tracker_loaded = True
except ModuleNotFoundError:
    pass

ModuleUpdate.update()

sort_start_addresses = [
    0x204FD4C,  # Items
    0x204FDCC,  # Weapons
    0x204FF5C,  # Armor
    0x2050074,  # Accessories
    0x20500D4,  # Ammo
    0x2050364,  # Technicks
    0x2050394,  # Magicks
    0x2050436,  # Key Items
    0x2050836,  # Loot
]

sort_count_addresses = [
    0x2050C38,  # Items
    0x2050C3C,  # Weapons
    0x2050C40,  # Armor
    0x2050C44,  # Accessories
    0x2050C48,  # Ammo
    0x2050C58,  # Technicks
    0x2050C5C,  # Magicks
    0x2050C60,  # Key Items
    0x2050C64,  # Loot
]

MAX_PARTY_MEMBERS = 12


class FF12StateCache:
    SAVE_DATA_LENGTH = 0xE200
    ITEM_SECTION_LENGTH = 0x2000
    BITFIELD_SECTION_LENGTH = 0x200

    def __init__(self):
        self.save_data_base: int = 0
        self.save_data: bytes = b""
        self.extra_segments: List[Tuple[int, bytes]] = []
        self.party_address: int = 0
        self.scenario_flag: int = -1
        self.current_map: int = -1
        self.current_game_state: int = -1
        self.party_members: set[int] = set()
        self.inventory_by_code: Dict[int, int] = {}
        self.inventory_by_name: Dict[str, int] = {}
        self.leviathan_progress: int = 0
        self.escape_progress: int = 0
        self.draklor_progress: int = 0

    def read_range(self, absolute_address: int, size: int):
        if self.save_data and self.save_data_base <= absolute_address and \
                absolute_address + size <= self.save_data_base + len(self.save_data):
            offset = absolute_address - self.save_data_base
            return self.save_data[offset:offset + size]

        for base, data in self.extra_segments:
            if base <= absolute_address and absolute_address + size <= base + len(data):
                offset = absolute_address - base
                return data[offset:offset + size]
        return None

    def add_extra_segment(self, base: int, data: bytes):
        if data:
            self.extra_segments.append((base, data))

    def save_byte(self, offset: int) -> int:
        if 0 <= offset < len(self.save_data):
            return self.save_data[offset]
        return 0

    def save_short(self, offset: int) -> int:
        if 0 <= offset + 1 < len(self.save_data):
            return int.from_bytes(self.save_data[offset:offset + 2], "little")
        return 0

    def save_bit(self, offset: int, bit: int) -> bool:
        byte = self.save_byte(offset)
        return ((byte >> bit) & 1) != 0


class FF12OpenWorldCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_list_processes(self):
        """List all processes found by pymem."""
        for process in pymem.process.list_processes():
            self.output(f"{process.szExeFile}: {process.th32ProcessID}")

    def _cmd_set_process_by_id(self, process_id: str):
        """Set the process by ID (int)."""
        int_id = int(process_id)
        try:
            self.ctx.ff12 = pymem.Pymem().open_process_from_id(int_id)
            logger.info("You are now auto-tracking")
            self.ctx.ff12connected = True
        except Exception as e:
            if self.ctx.ff12connected:
                self.ctx.ff12connected = False
            logger.info("Failed to set process by ID.")
            logger.info(e)


# Copied from KH2 Client
class FF12OpenWorldContext(CommonContext):
    command_processor = FF12OpenWorldCommandProcessor
    game = "Final Fantasy 12 Open World"
    items_handling = 0b111  # Indicates you get items sent from other worlds.
    tags = ["AP"]

    def __init__(self, server_address, password):
        super(FF12OpenWorldContext, self).__init__(server_address, password)

        self.last_big_batch_time = None
        self.ff12_items_received: List[NetworkItem] = []
        self.sending: List[int] = []
        self.ff12slotdata = None
        self.server_connected = False
        self.ff12connected = False
        self.stored_map_id = 0
        self.hunt_progress = {}
        self.hunt_progress_changed = False
        # hooked object
        self.ff12 = None
        self.game_state_cache = FF12StateCache()
        self.item_lock = asyncio.Lock()
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%\FF12OpenWorldAP")
        else:
            logger.info("Could not find localappdata environment variable")
            self.game_communication_path = None
        self.delete_communication_files()

    async def get_username(self):
        if not self.auth:
            self.auth = self.username
            if not self.auth:
                logger.info('Enter slot name:')
                self.auth = await self.console_input()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(FF12OpenWorldContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.ff12connected = False
        self.server_connected = False
        self.delete_communication_files()
        self.ff12_items_received.clear()
        self.game_state_cache = FF12StateCache()
        await super(FF12OpenWorldContext, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.ff12connected = False
        self.server_connected = False
        self.delete_communication_files()
        self.ff12_items_received.clear()
        self.game_state_cache = FF12StateCache()
        await super(FF12OpenWorldContext, self).disconnect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(FF12OpenWorldContext, self).shutdown()

    def ff12_story_address(self):
        return self.ff12.base_address

    def _compute_save_data_address(self) -> int:
        if not self.ff12:
            return 0
        return self.ff12.base_address + 0x02044480

    def _read_bytes(self, address: int, length: int, use_base: bool = True) -> bytes:
        if not self.ff12:
            raise RuntimeError("FF12 process not attached")
        absolute = self.ff12.base_address + address if use_base else address
        cached = self.game_state_cache.read_range(absolute, length)
        if cached is not None and len(cached) == length:
            return cached
        return self.ff12.read_bytes(absolute, length)

    def ff12_read_byte(self, address, use_base=True):
        return int.from_bytes(self._read_bytes(address, 1, use_base), "little")

    def ff12_read_bit(self, address, bit, use_base=True) -> bool:
        return (self.ff12_read_byte(address, use_base) >> bit) & 1 == 1

    def ff12_read_short(self, address, use_base=True):
        return int.from_bytes(self._read_bytes(address, 2, use_base), "little")

    def ff12_read_int(self, address, use_base=True):
        return int.from_bytes(self._read_bytes(address, 4, use_base), "little")

    def on_package(self, cmd: str, args: dict):

        if cmd in {"Connected"}:
            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Final Fantasy 12 Open World"]}]))
            self.ff12slotdata = args['slot_data']
            self.locations_checked = set(args["checked_locations"])

        if cmd in {"ReceivedItems"}:
            self.find_game()
            if self.server_connected:
                # Get the items past the start index in args items
                for index, item in enumerate(args["items"], start=args["index"]):
                    if index >= len(self.ff12_items_received):
                        self.ff12_items_received.append(item)
                    else:
                        self.ff12_items_received[index] = item

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.locations_checked |= new_locations

        if cmd in {"DataPackage"}:
            self.find_game()
            self.server_connected = True
            self.delete_communication_files()
            asyncio.create_task(self.send_msgs([{'cmd': 'Sync'}]))

        if cmd in {"RoomInfo"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)

        super(FF12OpenWorldContext, self).on_package(cmd, args)

    def find_game(self):
        if not self.ff12connected:
            try:
                self.ff12 = pymem.Pymem(process_name="FFXII_TZA")
                logger.info("You are now auto-tracking")
                self.ff12connected = True
            except Exception:
                if self.ff12connected:
                    self.ff12connected = False
                logger.info("Game is not open (Try running the client as an admin).")

    def delete_communication_files(self):
        if os.path.exists(self.game_communication_path):
            for filename in os.listdir(self.game_communication_path):
                file_path = os.path.join(self.game_communication_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    logger.info(e)

    async def update_game_state_cache(self):
        if not self.ff12connected or not self.ff12:
            return

        new_cache = FF12StateCache()
        try:
            save_addr = self._compute_save_data_address()
            if not save_addr:
                return

            new_cache.save_data_base = save_addr
            new_cache.save_data = self.ff12.read_bytes(save_addr, FF12StateCache.SAVE_DATA_LENGTH)
            if not new_cache.save_data:
                return
            new_cache.scenario_flag = int.from_bytes(new_cache.save_data[0:2], "little")

            base = self.ff12.base_address

            def capture_segment(offset: int, length: int) -> bytes:
                data = self.ff12.read_bytes(base + offset, length)
                new_cache.add_extra_segment(base + offset, data)
                return data

            normal_items = capture_segment(0x02097054, FF12StateCache.ITEM_SECTION_LENGTH)
            equipment_items = capture_segment(0x020970D4, FF12StateCache.ITEM_SECTION_LENGTH)
            loot_items = capture_segment(0x0209741C, FF12StateCache.ITEM_SECTION_LENGTH)
            key_item_bits = capture_segment(0x0209784C, FF12StateCache.BITFIELD_SECTION_LENGTH)
            esper_bits = capture_segment(0x0209788C, FF12StateCache.BITFIELD_SECTION_LENGTH)
            magick_bits = capture_segment(0x0209781C, FF12StateCache.BITFIELD_SECTION_LENGTH)
            technick_bits = capture_segment(0x02097828, FF12StateCache.BITFIELD_SECTION_LENGTH)

            party_ptr = int.from_bytes(
                self.ff12.read_bytes(self.ff12.base_address + 0x02D9F190, 4), "little")
            new_cache.party_address = party_ptr + 0x08 if party_ptr else 0

            pointer1 = int.from_bytes(
                self.ff12.read_bytes(self.ff12.base_address + 0x01E5FFE0, 4), "little")
            if pointer1:
                new_cache.current_game_state = int.from_bytes(
                    self.ff12.read_bytes(pointer1 + 0x3A, 1), "little")
            new_cache.current_map = int.from_bytes(
                self.ff12.read_bytes(self.ff12.base_address + 0x020454C4, 2), "little")

            def read_short_from(data: bytes, offset: int) -> int:
                if 0 <= offset + 1 < len(data):
                    return int.from_bytes(data[offset:offset + 2], "little")
                return 0

            def read_flag_from(data: bytes, index: int) -> int:
                byte_index = index // 8
                bit_index = index % 8
                if 0 <= byte_index < len(data):
                    return (data[byte_index] >> bit_index) & 1
                return 0

            inventory_by_code: Dict[int, int] = {}
            inventory_by_name: Dict[str, int] = {}
            for name, item in item_data_table.items():
                code = item.code - 1
                count = 0
                if code < 0x1000:
                    count = read_short_from(normal_items, code * 2)
                elif code < 0x2000:
                    count = read_short_from(equipment_items, (code - 0x1000) * 2)
                elif 0x2000 <= code < 0x3000:
                    count = read_short_from(loot_items, (code - 0x2000) * 2)
                elif 0x8000 <= code < 0x9000:
                    count = read_flag_from(key_item_bits, code - 0x8000)
                elif 0xC000 <= code < 0xD000:
                    count = read_flag_from(esper_bits, code - 0xC000)
                elif 0x3000 <= code < 0x4000:
                    count = read_flag_from(magick_bits, code - 0x3000)
                elif 0x4000 <= code < 0x5000:
                    count = read_flag_from(technick_bits, code - 0x4000)
                inventory_by_code[code] = count
                inventory_by_name[name] = count
            new_cache.inventory_by_code = inventory_by_code
            new_cache.inventory_by_name = inventory_by_name

            party_members = set()
            if new_cache.party_address:
                try:
                    party_blob = self.ff12.read_bytes(new_cache.party_address, 0x1C8 * MAX_PARTY_MEMBERS)
                    for chara in range(MAX_PARTY_MEMBERS):
                        base_index = chara * 0x1C8
                        if base_index < len(party_blob) and party_blob[base_index] & 0x10:
                            party_members.add(chara)
                except Exception:
                    pass
            new_cache.party_members = party_members

            scenario_flag = new_cache.scenario_flag
            if 0x37A <= scenario_flag <= 0x44C:
                new_cache.leviathan_progress = scenario_flag
            else:
                lev_flag = new_cache.save_short(0xDFF7)
                if lev_flag > 10000:
                    new_cache.leviathan_progress = lev_flag - 10000
                elif lev_flag == 0:
                    new_cache.leviathan_progress = 0
                else:
                    new_cache.leviathan_progress = lev_flag

            esc_flag = new_cache.save_short(0xDFF4)
            if new_cache.save_byte(0xA04) >= 2:
                new_cache.escape_progress = 0x208
            elif 0x11D < scenario_flag < 0x208:
                new_cache.escape_progress = scenario_flag
            elif 0x11D < esc_flag < 0x208:
                new_cache.escape_progress = esc_flag
            elif new_cache.save_byte(0xA06) >= 2:
                new_cache.escape_progress = 0x11D
            elif 6110 < scenario_flag <= 6110 + 70:
                new_cache.escape_progress = scenario_flag - 6110
            elif 6110 < esc_flag <= 6110 + 70:
                new_cache.escape_progress = esc_flag - 6110
            else:
                new_cache.escape_progress = 0

            if 0xD48 <= scenario_flag <= 0x1036:
                new_cache.draklor_progress = scenario_flag
            else:
                darklor_flag = new_cache.save_short(0xDFF9)
                new_cache.draklor_progress = 0 if darklor_flag == 0 else darklor_flag

            self.game_state_cache = new_cache
        except Exception as e:
            if self.ff12connected:
                self.ff12connected = False
            logger.info(e)

    def get_party_address(self) -> int:
        if self.game_state_cache.party_address:
            return self.game_state_cache.party_address
        return self.ff12_read_int(0x02D9F190) + 0x08

    def get_save_data_address(self) -> int:
        if self.game_state_cache.save_data_base:
            return self.game_state_cache.save_data_base
        return self._compute_save_data_address()

    def get_scenario_flag(self) -> int:
        if self.game_state_cache.scenario_flag >= 0:
            return self.game_state_cache.scenario_flag
        return self.ff12_read_short(0x02044480)

    def get_item_count_received(self, item_name: str) -> int:
        return len([item for item in self.ff12_items_received[:self.get_item_index()] if
                    item.item == item_data_table[item_name].code])

    def get_item_index(self) -> int:
        return self.ff12_read_int(self.get_save_data_address() + 0x696, use_base=False)

    def has_item_received(self, item_name: str) -> bool:
        return self.get_item_count_received(item_name) > 0

    def inventory_count(self, item_name: str) -> int:
        return self.game_state_cache.inventory_by_name.get(item_name, 0)

    def inventory_has(self, item_name: str) -> bool:
        return self.inventory_count(item_name) > 0

    def get_current_map(self) -> int:
        if self.game_state_cache.current_map >= 0:
            return self.game_state_cache.current_map
        return self.ff12_read_short(0x20454C4)

    def get_current_game_state(self) -> int:
        if self.game_state_cache.current_game_state >= 0:
            return self.game_state_cache.current_game_state
        pointer1 = self.ff12_read_int(0x01E5FFE0)
        return self.ff12_read_byte(pointer1 + 0x3A, False)

    async def ff12_check_locations(self):
        try:
            self.sending.clear()
            index = 0
            for location_name, data in location_data_table.items():
                index += 1
                if data.address in self.locations_checked:
                    continue

                # Check if the game is in a state where the location can be checked
                map_id = self.get_current_map()
                game_state = self.get_current_game_state()
                scenario_flag = self.get_scenario_flag()
                if (map_id == 0 or map_id > 0xFFFF or map_id <= 12 or
                        map_id == 274 or game_state != 0 or scenario_flag < 45):
                    break

                if data.type == "inventory":
                    if int(data.str_id) in self.game_state_cache.party_members:
                        self.sending.append(data.address)
                elif data.type == "reward":
                    if self.is_reward_met(data):
                        self.sending.append(data.address)
                elif data.type == "treasure":
                    treasures: list[str] = self.ff12slotdata["treasures"]
                    if location_name not in treasures:
                        continue
                    treasure_index = treasures.index(location_name)
                    byte_index = treasure_index // 8
                    bit_index = treasure_index % 8
                    treasure_byte = self.game_state_cache.save_byte(0x14B4 + byte_index)
                    if (treasure_byte >> bit_index) & 1:
                        self.sending.append(data.address)

            self.locations_checked |= set(self.sending)

            # Victory, Final Boss
            if self.game_state_cache.save_byte(0xA2E) >= 2 and not self.finished_game:
                await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                self.finished_game = True

            if len(self.sending) > 0:
                message = [{"cmd": 'LocationChecks', "locations": self.sending}]
                await self.send_msgs(message)

            # Poptracker stuff
            map_id = self.get_current_map()
            if map_id != self.stored_map_id and map_id > 12 and map_id < 0xFFFF and map_id != 274:
                # Send Bounce with new ID
                self.stored_map_id = map_id
                await self.send_msgs([{
                    "cmd": "Bounce",
                    "slots": [self.slot],
                    "data": {
                        "type": "MapUpdate",
                        "mapId": map_id,
                    },
                }])

            if self.hunt_progress_changed:
                self.hunt_progress_changed = False
                await self.send_msgs(
                    [
                        {
                            "cmd": "Set",
                            "key": f"ffxiiow_hunts_{self.team}_{self.slot}",
                            "default": {},
                            "want_reply": False,
                            "operations": [{"operation": "update", "value": self.hunt_progress}],
                        }
                    ]
                )

        except Exception as e:
            if self.ff12connected:
                self.ff12connected = False
            logger.info(e)

    def is_reward_met(self, location_data: FF12OpenWorldLocationData):
        save = self.game_state_cache
        scen = self.get_scenario_flag()

        if location_data.str_id == "9000" or \
                location_data.str_id == "916B" or \
                location_data.str_id == "916C":  # Tomaj Checks
            return scen >= 6110
        elif location_data.str_id == "9002":  # Shadestone check
            return save.save_bit(0xA42, 0)
        elif location_data.str_id == "9001":  # Sunstone check (if received Shadestone but the item is lost)
            return self.has_item_received("Shadestone") and not self.inventory_has("Shadestone")
        elif location_data.str_id == "905E":  # Crescent Stone (if received Sunstone but the item is lost)
            return self.has_item_received("Sunstone") and not self.inventory_has("Sunstone")
        elif location_data.str_id == "905F":  # Dalan SotO
            return save.save_bit(0xA42, 1)
        elif location_data.str_id == "911E":  # SotO turn in
            return self.has_item_received("Sword of the Order") and not self.inventory_has("Sword of the Order")
        elif location_data.str_id == "9060":  # Judges Boss
            return save.save_byte(0xA27) >= 2
        elif location_data.str_id == "9061":  # Systems Access Key
            return save.save_bit(0x14D4 + 4, 0)
        elif location_data.str_id == "912C":  # Manufacted Nethicite
            return self.game_state_cache.leviathan_progress >= 0x3E8
        elif location_data.str_id == "912D":  # Eksir Berries
            return save.save_bit(0xA42, 2)
        elif location_data.str_id == "9190":  # Belias Boss
            return save.save_byte(0xA19) >= 2
        elif location_data.str_id == "912E":  # Dawn Shard
            return save.save_bit(0xA42, 3)
        elif location_data.str_id == "918E":  # Vossler Boss
            return save.save_byte(0xA3B) >= 2
        elif location_data.str_id == "912F":  # Goddess's Magicite
            return self.game_state_cache.escape_progress >= 15
        elif location_data.str_id == "9130":  # Tube Fuse
            return self.game_state_cache.escape_progress >= 0x13F
        elif location_data.str_id == "911F":  # Garif Reward
            return save.save_bit(0xA42, 4)
        elif location_data.str_id == "9131":  # Lente's Tear (Tiamat Boss)
            return save.save_byte(0xA08) >= 2
        elif location_data.str_id == "9191":  # Mateus Boss
            return save.save_byte(0xA21) >= 2
        elif location_data.str_id == "9132":  # Sword of Kings
            return save.save_bit(0xA42, 6)
        elif location_data.str_id == "9133":  # Start Mandragoras
            # Kid or Dad
            return self.game_state_cache.save_byte(0x684) == 1 or \
                self.game_state_cache.save_byte(0x681) == 1
        elif location_data.str_id == "9052":  # Turn in Mandragoras
            return self.game_state_cache.save_byte(0x683) == 1
        elif location_data.str_id == "918D":  # Cid 1 Boss
            return self.game_state_cache.save_byte(0xA29) >= 2
        elif 0x9134 <= int(location_data.str_id, 16) <= 0x914F:  # Pinewood Chops
            return (save.save_byte(0xDFF6) >
                    int(location_data.str_id, 16) - 0x9134)
        elif location_data.str_id == "9150":  # Sandalwood Chop
            return save.save_bit(0xA42, 7)
        elif location_data.str_id == "9151":  # Lab Access Card
            return self.game_state_cache.draklor_progress >= 0xD48
        elif location_data.str_id == "9192":  # Shemhazai Boss
            return self.game_state_cache.save_byte(0xA20) >= 2
        elif location_data.str_id == "9152":  # Treaty Blade
            return save.save_bit(0xDFFB, 0)
        elif 0x9153 <= int(location_data.str_id, 16) <= 0x916A:  # Black Orbs
            return (save.save_byte(0xDFFC) >
                    int(location_data.str_id, 16) - 0x9153)
        elif location_data.str_id == "9193":  # Hashmal Boss
            return self.game_state_cache.save_byte(0xA1F) >= 2
        elif location_data.str_id == "918F":  # Cid 2 Boss
            return self.game_state_cache.save_byte(0xA2A) >= 2
        elif location_data.str_id == "9003":  # Hunt 1
            return self.read_hunt_progress(0) >= 70
        elif location_data.str_id == "9004":  # Hunt 2
            return self.read_hunt_progress(1) >= 70
        elif location_data.str_id == "9005":  # Hunt 3
            return self.read_hunt_progress(2) >= 90
        elif location_data.str_id == "9006":  # Hunt 4
            return self.read_hunt_progress(3) >= 100
        elif location_data.str_id == "9007":  # Hunt 5
            return self.read_hunt_progress(4) >= 90
        elif location_data.str_id == "9008":  # Hunt 6
            return self.read_hunt_progress(5) >= 100
        elif location_data.str_id == "9009":  # Hunt 7
            return self.read_hunt_progress(6) >= 100
        elif location_data.str_id == "900A":  # Hunt 8
            return self.read_hunt_progress(7) >= 100
        elif location_data.str_id == "900B":  # Hunt 9
            return self.read_hunt_progress(8) >= 100
        elif location_data.str_id == "900C":  # Hunt 10
            return self.read_hunt_progress(9) >= 100
        elif location_data.str_id == "900D":  # Hunt 11
            return self.read_hunt_progress(10) >= 100
        elif location_data.str_id == "900E":  # Hunt 12
            return self.read_hunt_progress(11) >= 100
        elif location_data.str_id == "900F":  # Hunt 13
            return self.read_hunt_progress(12) >= 90
        elif location_data.str_id == "9010":  # Hunt 14
            return self.read_hunt_progress(13) >= 100
        elif location_data.str_id == "9011":  # Hunt 15
            return self.read_hunt_progress(14) >= 100
        elif location_data.str_id == "9012":  # Hunt 16
            return self.read_hunt_progress(15) >= 90
        elif location_data.str_id == "9013":  # Hunt 17
            return self.read_hunt_progress(16) >= 50
        elif location_data.str_id == "9014":  # Hunt 18
            return self.read_hunt_progress(17) >= 50
        elif location_data.str_id == "9015":  # Hunt 19
            return self.read_hunt_progress(18) >= 100
        elif location_data.str_id == "9016":  # Hunt 20
            return self.read_hunt_progress(19) >= 150
        elif location_data.str_id == "9017":  # Hunt 21
            return self.read_hunt_progress(20) >= 150
        elif location_data.str_id == "9018":  # Hunt 22
            return self.read_hunt_progress(21) >= 150
        elif location_data.str_id == "9019":  # Hunt 23
            return self.read_hunt_progress(22) >= 150
        elif location_data.str_id == "901A":  # Hunt 24
            return self.read_hunt_progress(23) >= 50
        elif location_data.str_id == "901B":  # Hunt 25
            return self.read_hunt_progress(24) >= 50
        elif location_data.str_id == "901C":  # Hunt 26
            return self.read_hunt_progress(25) >= 90
        elif location_data.str_id == "901D":  # Hunt 27
            return self.read_hunt_progress(26) >= 90
        elif location_data.str_id == "901E":  # Hunt 28
            return self.read_hunt_progress(27) >= 90
        elif location_data.str_id == "901F":  # Hunt 29
            return self.read_hunt_progress(28) >= 100
        elif location_data.str_id == "9020":  # Hunt 30
            return self.read_hunt_progress(29) >= 100
        elif location_data.str_id == "9021":  # Hunt 31
            return self.read_hunt_progress(30) >= 90
        elif location_data.str_id == "9022":  # Hunt 32
            return self.read_hunt_progress(31) >= 150
        elif location_data.str_id == "9023":  # Hunt 33
            return self.read_hunt_progress(32) >= 100
        elif location_data.str_id == "9024":  # Hunt 34
            return self.read_hunt_progress(33) >= 90
        elif location_data.str_id == "9025":  # Hunt 35
            return self.read_hunt_progress(34) >= 100
        elif location_data.str_id == "9026":  # Hunt 36
            return self.read_hunt_progress(35) >= 100
        elif location_data.str_id == "9027":  # Hunt 37
            return self.read_hunt_progress(36) >= 90
        elif location_data.str_id == "9028":  # Hunt 38
            return self.read_hunt_progress(37) >= 110
        elif location_data.str_id == "9029":  # Hunt 39
            return self.read_hunt_progress(38) >= 50
        elif location_data.str_id == "902A":  # Hunt 40
            return self.read_hunt_progress(39) >= 130
        elif location_data.str_id == "902B":  # Hunt 42
            return self.read_hunt_progress(40) >= 100
        elif location_data.str_id == "902C":  # Hunt 43
            return self.read_hunt_progress(41) >= 150
        elif location_data.str_id == "902D":  # Hunt 44
            return self.read_hunt_progress(42) >= 100
        elif location_data.str_id == "902E":  # Hunt 45
            return self.read_hunt_progress(43) >= 100
        elif location_data.str_id == "9122":  # Hunt 41
            return self.read_hunt_progress(44) >= 100
        elif 0x902F <= int(location_data.str_id, 16) <= 0x903A:  # Clan Rank Rewards
            return (self.game_state_cache.save_byte(0x418) >
                    int(location_data.str_id, 16) - 0x902F)
        elif location_data.str_id == "903B":  # Clan Boss Flans
            return self.game_state_cache.save_bit(0x419, 0)
        elif location_data.str_id == "903C":  # Clan Boss Firemane
            return self.game_state_cache.save_bit(0x419, 1)
        elif location_data.str_id == "903D":  # Clan Boss Earth Tyrant
            return self.game_state_cache.save_bit(0x419, 2)
        elif location_data.str_id == "903E":  # Clan Boss Mimic Queen
            return self.game_state_cache.save_bit(0x419, 3)
        elif location_data.str_id == "903F":  # Clan Boss Demon Wall 1
            return self.game_state_cache.save_bit(0x419, 4)
        elif location_data.str_id == "9040":  # Clan Boss Demon Wall 2
            return self.game_state_cache.save_bit(0x419, 5)
        elif location_data.str_id == "9041":  # Clan Boss Elder Wyrm
            return self.game_state_cache.save_bit(0x419, 6)
        elif location_data.str_id == "9042":  # Clan Boss Tiamat
            return self.game_state_cache.save_bit(0x419, 7)
        elif location_data.str_id == "9043":  # Clan Boss Vinuskar
            return self.game_state_cache.save_bit(0x41A, 0)
        elif location_data.str_id == "9044":  # Clan Boss King Bomb
            return self.game_state_cache.save_bit(0x41A, 1)
        elif location_data.str_id == "9045":  # Clan Boss Mandragoras
            return self.game_state_cache.save_bit(0x41A, 3)
        elif location_data.str_id == "9046":  # Clan Boss Ahriman
            return self.game_state_cache.save_bit(0x41A, 2)
        elif location_data.str_id == "9047":  # Clan Boss Hell Wyrm
            return self.game_state_cache.save_bit(0x41A, 4)
        elif location_data.str_id == "9048":  # Clan Boss Rafflesia
            return self.game_state_cache.save_bit(0x41A, 5)
        elif location_data.str_id == "9049":  # Clan Boss Daedalus
            return self.game_state_cache.save_bit(0x41A, 6)
        elif location_data.str_id == "904A":  # Clan Boss Tyrant
            return self.game_state_cache.save_bit(0x41A, 7)
        elif location_data.str_id == "904B":  # Clan Boss Hydro
            return self.game_state_cache.save_bit(0x41B, 0)
        elif location_data.str_id == "904C":  # Clan Boss Humbaba Mistant
            return self.game_state_cache.save_bit(0x41B, 1)
        elif location_data.str_id == "904D":  # Clan Boss Fury
            return self.game_state_cache.save_bit(0x41B, 2)
        elif location_data.str_id == "905A":  # Clan Boss Omega Mark XII
            return self.game_state_cache.save_bit(0x41B, 3)
        elif 0x904E <= int(location_data.str_id, 16) <= 0x9051:  # Clan Espers (1,4,8,13)
            return (self.game_state_cache.save_byte(0x41C) >
                    int(location_data.str_id, 16) - 0x904E)
        elif location_data.str_id == "916D":  # Flowering Cactoid Drop
            return self.game_state_cache.save_byte(0x1064 + 130) >= 70
        elif location_data.str_id == "916E":  # Barheim Key
            return self.game_state_cache.save_byte(0x68B) >= 11
        elif location_data.str_id == "9081":  # Deliver Cactus Flower
            return self.game_state_cache.save_byte(0x68B) >= 3
        elif location_data.str_id == "908A":  # Cactus Family
            return self.game_state_cache.save_byte(0x686) >= 7
        elif location_data.str_id == "916F":  # Get Stone of the Condemner
            return self.game_state_cache.save_byte(0x680) >= 1
        elif location_data.str_id == "9170":  # Get Wind Globe
            return self.game_state_cache.save_byte(0x1064 + 53) >= 50
        elif location_data.str_id == "9171":  # Get Windvane
            return self.game_state_cache.save_byte(0x1064 + 53) >= 60
        elif location_data.str_id == "9172":  # White Mousse Drop
            return self.game_state_cache.save_byte(0x1064 + 133) >= 50
        elif location_data.str_id == "9173":  # Sluice Gate Key
            return self.game_state_cache.save_byte(0x1064 + 133) >= 120
        elif location_data.str_id == "9174":  # Enkelados Drop
            return self.game_state_cache.save_byte(0x1064 + 137) >= 50
        elif location_data.str_id == "9062":  # Give Errmonea Leaf
            return self.game_state_cache.save_byte(0x4AE) >= 1
        elif location_data.str_id == "9175":  # Merchant's Armband
            return self.game_state_cache.save_byte(0x6FD) >= 2
        elif location_data.str_id == "9176":  # Get Pilika's Diary
            return self.game_state_cache.save_byte(0x6FD) >= 3
        elif location_data.str_id == "908D":  # Give Pilika's Diary
            return self.game_state_cache.save_byte(0x6FD) >= 4
        elif location_data.str_id == "9177":  # Vorpal Bunny Drop
            return self.game_state_cache.save_byte(0x1064 + 141) >= 50
        elif location_data.str_id == "9178":  # Croakadile Drop
            return self.game_state_cache.save_byte(0x1064 + 138) >= 50
        elif location_data.str_id == "9179":  # Lindwyrm Drop
            return self.game_state_cache.save_byte(0x1064 + 149) >= 100
        elif location_data.str_id == "917A":  # Get Silent Urn
            return self.game_state_cache.save_byte(0x1064 + 163) >= 50
        elif location_data.str_id == "917B":  # Orthros Drop
            return self.game_state_cache.save_byte(0x1064 + 162) >= 70
        elif location_data.str_id == "917D":  # Site 3 Key
            return self.game_state_cache.save_byte(0x1064 + 165) >= 50
        elif location_data.str_id == "917E":  # Site 11 Key
            return self.game_state_cache.save_bit(0xDFFB, 2)
        elif location_data.str_id == "917F":  # Fafnir Drop
            return self.game_state_cache.save_byte(0x1064 + 158) >= 70
        elif location_data.str_id == "9180":  # Marilith Drop
            return self.game_state_cache.save_byte(0x1064 + 136) >= 70
        elif location_data.str_id == "9181":  # Vyraal Drop
            return self.game_state_cache.save_byte(0x1064 + 148) >= 100
        elif location_data.str_id == "9182":  # Dragon Scale
            return self.game_state_cache.save_byte(0x1064 + 148) >= 150
        elif location_data.str_id == "9183":  # Ageworn Key check (if received Dragon Scale but the item is lost)
            return self.has_item_received("Dragon Scale") and not self.inventory_has("Dragon Scale")
        elif location_data.str_id == "9184":  # Ann's Letter
            return self.game_state_cache.save_byte(0x5A6) >= 1
        elif location_data.str_id == "906C":  # Ann's Sisters
            return self.game_state_cache.save_byte(0x5A6) >= 7
        elif location_data.str_id == "9185":  # Dusty Letter
            return self.game_state_cache.save_bit(0x423, 2)
        elif location_data.str_id == "917C":  # Blackened Fragment
            return self.game_state_cache.save_byte(0x1064 + 162) >= 100
        elif location_data.str_id == "9186":  # Dull Fragment
            return self.game_state_cache.save_bit(0x423, 1)
        elif location_data.str_id == "9187":  # Grimy Fragment
            return self.game_state_cache.save_byte(0x416) >= 7
        elif location_data.str_id == "9188":  # Moonsilver Medallion
            return self.game_state_cache.save_byte(0x1064 + 59) >= 20
        elif location_data.str_id == "9189" or \
                location_data.str_id == "918A" or \
                location_data.str_id == "918B":  # Nabreus Medallions
            return self.game_state_cache.save_byte(0x1064 + 57) >= 100
        elif location_data.str_id == "918C":  # Medallion of Might (Humbaba Mistant and Fury bosses)
            return self.game_state_cache.save_byte(0xA0F) >= 2 and \
                self.game_state_cache.save_byte(0xA10) >= 2
        elif location_data.str_id == "9056":  # Viera Rendevous
            return self.game_state_cache.save_byte(0x40E) >= 6
        elif location_data.str_id == "9058":  # Ktjn Reward
            return self.game_state_cache.save_bit(0x409, 0)
        elif location_data.str_id == "906A":  # Jovy Reward
            return self.game_state_cache.save_byte(0x5B8) >= 6
        elif location_data.str_id == "906E":  # Outpost Glint 1
            return self.game_state_cache.save_byte(0x691) >= 1
        elif location_data.str_id == "906F":  # Outpost Glint 2
            return self.game_state_cache.save_byte(0x692) >= 1
        elif location_data.str_id == "9057":  # Outpost Glint 3
            return self.game_state_cache.save_byte(0x693) >= 1
        elif location_data.str_id == "9070":  # Outpost Glint 4
            return self.game_state_cache.save_byte(0x694) >= 1
        elif location_data.str_id == "9059":  # Outpost Glint 5
            return self.game_state_cache.save_byte(0x695) >= 1
        elif location_data.str_id == "908F":  # Footrace
            return self.game_state_cache.save_byte(0x73D) >= 1
        elif location_data.str_id == "9194":  # Adrammelech Boss
            return save.save_byte(0xA25) >= 2
        elif location_data.str_id == "9195":  # Zalera Boss
            return save.save_byte(0xA1D) >= 2
        elif location_data.str_id == "9196":  # Cuchulainn Boss
            return save.save_byte(0xA1C) >= 2
        elif location_data.str_id == "9197":  # Zeromus Boss
            return save.save_byte(0xA22) >= 2
        elif location_data.str_id == "9198":  # Exodus Boss
            return save.save_byte(0xA23) >= 2
        elif location_data.str_id == "9199":  # Chaos Boss
            return save.save_byte(0xA1A) >= 2
        elif location_data.str_id == "919A":  # Ultima Boss
            return save.save_byte(0xA24) >= 2
        elif location_data.str_id == "919B":  # Zodiark Boss
            return save.save_byte(0xA1B) >= 2
        elif 0x9090 <= int(location_data.str_id, 16) <= 0x90AE:  # Trophy Drops
            trophy_index = int(location_data.str_id, 16) - 0x9090
            return save.save_byte(0xC90 + trophy_index) >= 2
        elif 0x90F9 <= int(location_data.str_id, 16) <= 0x90FE:  # Rare Game Defeats (5,10,15,20,25,30)
            return save.save_byte(0x725) > \
                (int(location_data.str_id, 16) - 0x90F9) + 1
        elif location_data.str_id == "90F3":  # Atak >=16
            if save.save_byte(0x1064 + 71) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return save.save_byte(0xB14) == max_trophies and \
                max_trophies >= 16
        elif location_data.str_id == "90F4":  # Atak <16
            if save.save_byte(0x1064 + 71) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return save.save_byte(0xB14) == max_trophies and \
                max_trophies < 16
        elif location_data.str_id == "90F5":  # Blok >=16
            if save.save_byte(0x1064 + 71) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return save.save_byte(0xB15) == max_trophies and \
                max_trophies >= 16
        elif location_data.str_id == "90F6":  # Blok <16
            if save.save_byte(0x1064 + 71) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return save.save_byte(0xB15) == max_trophies and \
                max_trophies < 16
        elif location_data.str_id == "90F7":  # Stok >=16
            if save.save_byte(0x1064 + 71) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return save.save_byte(0xB16) == max_trophies and \
                max_trophies >= 16
        elif location_data.str_id == "90F8":  # Stok <16
            if save.save_byte(0x1064 + 71) < 170:
                return False
            max_trophies = self.get_max_trophies()
            return save.save_byte(0xB16) == max_trophies and \
                max_trophies < 16
        elif 0x90FF <= int(location_data.str_id, 16) <= 0x911D:  # Hunt Club Outfitters
            outfitter_index = int(location_data.str_id, 16) - 0x90FF
            return save.save_byte(0xAF2 + outfitter_index) >= 1

    def read_hunt_progress(self, hunt_id: int) -> int:
        value = self.game_state_cache.save_byte(0x1064 + 128 + hunt_id)
        if self.hunt_progress.get(hunt_id) != value:
            print("[Debug] Hunt Progress: Hunt %d: %d -> %d" % (hunt_id, self.hunt_progress.get(hunt_id, 0), value))
            self.hunt_progress[hunt_id] = value
            self.hunt_progress_changed = True
        return value

    def get_max_trophies(self):
        return max(
            self.game_state_cache.save_byte(0xB14),
            self.game_state_cache.save_byte(0xB15),
            self.game_state_cache.save_byte(0xB16))

    async def give_items(self):
        try:
            # Write obtained items to txt files in the communication folder in format items_received_####.txt
            cur_index = 0
            for item in self.ff12_items_received:
                file_path = os.path.join(
                    self.game_communication_path,
                    f"items_received_{cur_index:04d}.txt")
                with open(file_path, "w") as f:
                    # Write the item ID and the amount of the item on new lines
                    item_id = item.item - 1
                    if item.item >= 1 + 98304:  # Gil
                        item_id = 0xFFFE
                    item_count = item_data_table[inv_item_table[item.item]].amount
                    f.write(f"{item_id}\n{item_count}\n")
                cur_index += 1
        except Exception as e:
            if self.ff12connected:
                self.ff12connected = False
            logger.info(e)

    def make_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        ui = super().make_gui()

        class FF12OpenWorldManager(ui):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago FF12 Open World Client"

        return FF12OpenWorldManager


async def ff12_watcher(ctx: FF12OpenWorldContext):
    while not ctx.exit_event.is_set():
        try:
            if ctx.ff12connected and ctx.server_connected:
                await ctx.update_game_state_cache()
                await ctx.ff12_check_locations()
                await ctx.give_items()
            elif not ctx.ff12connected and ctx.server_connected:
                ctx.ff12 = None
                last_check = time.time()
                while not ctx.ff12connected and ctx.server_connected and not ctx.exit_event.is_set():
                    if time.time() - last_check > 15:
                        logger.info("Game Connection lost. Waiting 15 seconds until trying to reconnect.")
                        ctx.find_game()
                        last_check = time.time()
                    await asyncio.sleep(0.5)
        except Exception as e:
            if ctx.ff12connected:
                ctx.ff12connected = False
            logger.info(e)
        await asyncio.sleep(0.5)


def launch(*launch_args):
    async def main(args_in):
        ctx = FF12OpenWorldContext(args_in.connect, args_in.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            ff12_watcher(ctx), name="FF12ProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="FF12 Open World Client, for text interfacing.")
    parser.add_argument("url", default="", type=str, nargs="?", help="Archipelago connection url")

    args, rest = parser.parse_known_args(launch_args)
    args = handle_url_arg(args, parser)
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
