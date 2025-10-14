import ModuleUpdate
ModuleUpdate.update()

import Utils

import asyncio
import base64
import binascii
import colorama
import io
import os
import re
import select
import shlex
import socket
import struct
import sys
import subprocess
import time
import typing
from enum import IntEnum


from CommonClient import (CommonContext, ClientCommandProcessor, get_base_parser, gui_enabled, logger, server_loop)
from NetUtils import ClientStatus
from . import LinksAwakeningWorld
from . import Common
from .GpsTracker import GpsTracker
from .TrackerConsts import storage_key
from .ItemTracker import ItemTracker
from .Locations import links_awakening_location_meta_to_id
from .Tracker import LocationTracker, MagpieBridge, Check

links_awakening_location_id_to_meta = {v:k for k,v in links_awakening_location_meta_to_id.items()}


class GameboyException(Exception):
    pass


class RetroArchDisconnectError(GameboyException):
    pass


class InvalidEmulatorStateError(GameboyException):
    pass


class BadRetroArchResponse(GameboyException):
    pass


def clamp(minimum, number, maximum):
    return max(minimum, min(maximum, number))


class LAClientConstants:
    # Memory locations
    ROMGameID = 0x0051  # 4 bytes
    SlotName = 0x0134
    wGameplayType = 0xDB95
    wHealth = 0xDB5A

    wMWRecvIndexHi = 0xDDF6   # RO: The index of the next item to receive.
    wMWRecvIndexLo = 0xDDF7   #     If given something different it will be ignored.
    wMWCommand = 0xDDF8       # RW: See MWCommands
    wMWItemCode = 0xDDF9      # RW: Item code to give the player
    wMWItemSenderHi = 0xDDFA  # RW: Unused, but maybe will set up more rom banks in the future
    wMWItemSenderLo = 0xDDFB  # RW: ID for sending player
    wMWMultipurposeC = 0xDDFC # RW
    wMWMultipurposeD = 0xDDFD # RW
    wMWMultipurposeE = 0xDDFE # RW
    wMWMultipurposeF = 0xDDFF # RW

    wCheckAddress = 0xC0FF - 0x4
    WRamCheckSize = 0x4
    WRamSafetyValue = bytearray([0]*WRamCheckSize)

    wRamStart = 0xC000
    hRamStart = 0xFF80
    hRamSize = 0x80

    MinGameplayValue = 0x06
    MaxGameplayValue = 0x1A
    VictoryGameplayAndSub = 0x0102


class MWCommands(IntEnum):
    # bit 0: send item
    # bit 1: consider receive index for item send and tick up
    # bit 2: collect location
    # bit 3: send death link
    # bit 4,5: clear trade item (bit in wMWMultipurposeF)
    # bit 7: no commands happen unless this is set, the gb will unset this bit
    #        after executing the command allowing for confirmation in client
    NONE =              0b00000000
    SEND_ITEM_SPECIAL = 0b00000001
    SEND_ITEM =         0b00000011
    COLLECT =           0b00000100
    COLLECT_WITH_ITEM = 0b00000101
    DEATH_LINK =        0b00001000
    CLEAR_TRADE_1 =     0b00010000
    CLEAR_TRADE_2 =     0b00100000
    EXECUTE_COMMAND =   0b10000000


class DeathLinkStatus(IntEnum):
    NONE = 0
    PENDING = 1
    DYING = 2


class RAGameboy():
    cache = []
    last_cache_read = None
    socket = None

    def __init__(self, address, port) -> None:
        self.cache_start = LAClientConstants.wRamStart
        self.cache_size = LAClientConstants.hRamStart + LAClientConstants.hRamSize - LAClientConstants.wRamStart

        self.address = address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        assert (self.socket)
        self.socket.setblocking(False)

    async def send_command(self, command, timeout=1.0):
        self.send(f'{command}\n')
        response_str = await self.async_recv()
        self.check_command_response(command, response_str)
        return response_str.rstrip()

    async def get_retroarch_version(self):
        return await self.send_command("VERSION")

    async def get_retroarch_status(self):
        return await self.send_command("GET_STATUS")

    def set_checks_range(self, checks_start, checks_size):
        self.checks_start = checks_start
        self.checks_size = checks_size

    def set_location_range(self, location_start, location_size, critical_addresses):
        self.location_start = location_start
        self.location_size = location_size
        self.critical_location_addresses = critical_addresses

    def send(self, b):
        if type(b) is str:
            b = b.encode('ascii')
        self.socket.sendto(b, (self.address, self.port))

    def recv(self):
        select.select([self.socket], [], [])
        response, _ = self.socket.recvfrom(4096)
        return response

    async def async_recv(self, timeout=1.0):
        response = await asyncio.wait_for(asyncio.get_event_loop().sock_recv(self.socket, 4096), timeout)
        return response

    async def check_safe_gameplay(self, throw=True):
        async def check_wram():
            check_values = await self.async_read_memory(LAClientConstants.wCheckAddress, LAClientConstants.WRamCheckSize)

            if check_values != LAClientConstants.WRamSafetyValue:
                if throw:
                    raise InvalidEmulatorStateError()
                return False
            return True

        if not await check_wram():
            if throw:
                raise InvalidEmulatorStateError()
            return False

        gameplay_value = await self.async_read_memory(LAClientConstants.wGameplayType)
        gameplay_value = gameplay_value[0]
        # In gameplay or credits
        if not (LAClientConstants.MinGameplayValue <= gameplay_value <= LAClientConstants.MaxGameplayValue) and gameplay_value != 0x1:
            if throw:
                logger.info("invalid emu state")
                raise InvalidEmulatorStateError()
            return False
        if not await check_wram():
            if throw:
                raise InvalidEmulatorStateError()
            return False
        return True

    # We're sadly unable to update the whole cache at once
    # as RetroArch only gives back some number of bytes at a time
    # So instead read as big as chunks at a time as we can manage
    async def update_cache(self):
        # First read the safety address - if it's invalid, bail
        self.cache = []

        if not await self.check_safe_gameplay():
            return

        attempts = 0
        while True:
            # RA doesn't let us do an atomic read of a large enough block of RAM
            # Some bytes can't change in between reading location_block and hram_block
            location_block = await self.read_memory_block(self.location_start, self.location_size)
            hram_block = await self.read_memory_block(LAClientConstants.hRamStart, LAClientConstants.hRamSize)
            verification_block = await self.read_memory_block(self.location_start, self.location_size)

            valid = True
            for address in self.critical_location_addresses:
                if location_block[address - self.location_start] != verification_block[address - self.location_start]:
                    valid = False

            if valid:
                break

            attempts += 1

            # Shouldn't really happen, but keep it from choking
            if attempts > 5:
                return

        checks_block = await self.read_memory_block(self.checks_start, self.checks_size)

        if not await self.check_safe_gameplay():
            return

        self.cache = bytearray(self.cache_size)

        start = self.checks_start - self.cache_start
        self.cache[start:start + len(checks_block)] = checks_block

        start = self.location_start - self.cache_start
        self.cache[start:start + len(location_block)] = location_block

        start = LAClientConstants.hRamStart - self.cache_start
        self.cache[start:start + len(hram_block)] = hram_block

        self.last_cache_read = time.time()

    async def read_memory_block(self, address: int, size: int):
        block = bytearray()
        remaining_size = size
        while remaining_size:
            chunk = await self.async_read_memory(address + len(block), remaining_size)
            remaining_size -= len(chunk)
            block += chunk

        return block

    async def read_memory_cache(self, addresses):
        if not self.last_cache_read or self.last_cache_read + 0.1 < time.time():
            await self.update_cache()
        if not self.cache:
            return None
        assert (len(self.cache) == self.cache_size)
        for address in addresses:
            assert self.cache_start <= address <= self.cache_start + self.cache_size
        r = {address: self.cache[address - self.cache_start]
             for address in addresses}
        return r

    async def async_read_memory_safe(self, address, size=1):
        # whenever we do a read for a check, we need to make sure that we aren't reading
        # garbage memory values - we also need to protect against reading a value, then the emulator resetting
        #
        # ...actually, we probably _only_ need the post check

        # Check before read
        if not await self.check_safe_gameplay():
            return None

        # Do read
        r = await self.async_read_memory(address, size)

        # Check after read
        if not await self.check_safe_gameplay():
            return None

        return r

    def check_command_response(self, command: str, response: bytes):
        if command == "VERSION":
            ok = re.match(r"\d+\.\d+\.\d+", response.decode('ascii')) is not None
        else:
            ok = response.startswith(command.encode())
        if not ok:
            logger.warning(f"Bad response to command {command} - {response}")
            raise BadRetroArchResponse()

    def read_memory(self, address, size=1):
        command = "READ_CORE_MEMORY"

        self.send(f'{command} {hex(address)} {size}\n')
        response = self.recv()

        self.check_command_response(command, response)

        splits = response.decode().split(" ", 2)
        # Ignore the address for now
        if splits[2][:2] == "-1":
            raise BadRetroArchResponse()

        # TODO: check response address, check hex behavior between RA and BH

        return bytearray.fromhex(splits[2])

    async def async_read_memory(self, address, size=1):
        command = "READ_CORE_MEMORY"

        self.send(f'{command} {hex(address)} {size}\n')
        response = await self.async_recv()
        self.check_command_response(command, response)
        response = response[:-1]
        splits = response.decode().split(" ", 2)
        try:
            response_addr = int(splits[1], 16)
        except ValueError:
            raise BadRetroArchResponse()

        if response_addr != address:
            raise BadRetroArchResponse()

        ret = bytearray.fromhex(splits[2])
        if len(ret) > size:
            raise BadRetroArchResponse()
        return ret

    def write_memory(self, address, bytes):
        command = "WRITE_CORE_MEMORY"

        self.send(f'{command} {hex(address)} {" ".join(hex(b) for b in bytes)}')
        select.select([self.socket], [], [])
        response, _ = self.socket.recvfrom(4096)
        self.check_command_response(command, response)
        splits = response.decode().split(" ", 3)

        assert (splits[0] == command)

        if splits[2] == "-1":
            logger.info(splits[3])

    def send_mw_command(self, command, item_code=0xFF, item_sender=0x0000,
                        mp_c=0x00, mp_d=0x00, mp_e=0x00, mp_f=0x00,
                        mp_cd=0x0000, mp_ef=0x0000):
        command |= MWCommands.EXECUTE_COMMAND
        [sender_high, sender_low] = struct.pack('>H', item_sender)
        if mp_cd:
            [mp_c, mp_d] = struct.pack('>H', mp_cd)
        if mp_ef:
            [mp_e, mp_f] = struct.pack('>H', mp_ef)
        msg = [command, item_code, sender_high, sender_low, mp_c, mp_d, mp_e, mp_f]
        self.write_memory(LAClientConstants.wMWCommand, msg)


class LinksAwakeningClient():
    socket = None
    gameboy = None
    tracker = None
    auth = None
    game_crc = None
    collect_enabled = True
    death_link_status = DeathLinkStatus.DYING # avoids sending a death if player is dead when client connects
    retroarch_address = None
    retroarch_port = None
    gameboy = None

    def __init__(self, retroarch_address="127.0.0.1", retroarch_port=55355):
        self.retroarch_address = retroarch_address
        self.retroarch_port = retroarch_port
        pass

    stop_bizhawk_spam = False
    async def wait_for_retroarch_connection(self):
        if not self.stop_bizhawk_spam:
            logger.info("Waiting on connection to Retroarch...")
            self.stop_bizhawk_spam = True
        self.gameboy = RAGameboy(self.retroarch_address, self.retroarch_port)

        while True:
            try:
                version = await self.gameboy.get_retroarch_version()
                NO_CONTENT = b"GET_STATUS CONTENTLESS"
                status = NO_CONTENT
                core_type = None
                GAME_BOY = b"game_boy"
                while status == NO_CONTENT or core_type != GAME_BOY:
                    status = await self.gameboy.get_retroarch_status()
                    if status.count(b" ") < 2:
                        await asyncio.sleep(1.0)
                        continue
                    GET_STATUS, PLAYING, info = status.split(b" ", 2)
                    if status.count(b",") < 2:
                        await asyncio.sleep(1.0)
                        continue
                    core_type, rom_name, self.game_crc = info.split(b",", 2)
                    if core_type != GAME_BOY:
                        logger.info(
                            f"Core type should be '{GAME_BOY}', found {core_type} instead - wrong type of ROM?")
                        await asyncio.sleep(1.0)
                        continue
                self.stop_bizhawk_spam = False
                logger.info(f"Connected to Retroarch {version.decode('ascii', errors='replace')} "
                            f"running {rom_name.decode('ascii', errors='replace')}")
                return
            except (BlockingIOError, TimeoutError, ConnectionResetError):
                await asyncio.sleep(1.0)
                pass

    async def reset_auth(self):
        auth = binascii.hexlify(await self.gameboy.async_read_memory(LAClientConstants.SlotName, 12)).decode()
        self.auth = auth

    async def wait_and_init_tracker(self, magpie: MagpieBridge):
        await self.wait_for_game_ready()
        self.tracker = LocationTracker(self.gameboy)
        self.item_tracker = ItemTracker(self.gameboy)
        self.gps_tracker = GpsTracker(self.gameboy)
        magpie.gps_tracker = self.gps_tracker

    # The key location is blocked from collection unless the value location
    # has also been checked.
    dependent_location_meta_ids = {
        "0x301-0": "0x301-1", # Tunic Fairy Item 1 -> Tunic Fairy Item 2
        "0x301-1": "0x301-0", # Tunic Fairy Item 2 -> Tunic Fairy Item 1
        "0x106": "0x102",     # Moldorm Heart Container -> Full Moon Cello
        "0x12B": "0x12A",     # Genie Heart Container -> Conch Horn
        "0x15A": "0x159",     # Slime Eye Heart Container -> Sea Lily's Bell
        "0x166": "0x162",     # Angler Fish Heart Container -> Surf Harp
        "0x185": "0x182",     # Slime Eel Heart Container -> Wind Marimba
        "0x1BC": "0x1B5",     # Facade Heart Container -> Coral Triangle
        "0x223": "0x22C",     # Evil Eagle Heart Container -> Organ of Evening Calm
        "0x234": "0x230",     # Hot Head Heart Container -> Thunder Drum
    }
    dependent_location_ids = {
        links_awakening_location_meta_to_id[k]: links_awakening_location_meta_to_id[v]
        for k, v in dependent_location_meta_ids.items()}

    # for these locations, only collect if the player has the trade item, and then take the trade item
    restricted_trades = {
        "0x2A6-Trade": {"cmd": MWCommands.CLEAR_TRADE_1, "mask": ~(1<<0)&0xFF, "item": "TRADING_ITEM_YOSHI_DOLL" },
        "0x2B2-Trade": {"cmd": MWCommands.CLEAR_TRADE_1, "mask": ~(1<<1)&0xFF, "item": "TRADING_ITEM_RIBBON" },
        "0x2FE-Trade": {"cmd": MWCommands.CLEAR_TRADE_1, "mask": ~(1<<2)&0xFF, "item": "TRADING_ITEM_DOG_FOOD" },
        "0x07B-Trade": {"cmd": MWCommands.CLEAR_TRADE_1, "mask": ~(1<<3)&0xFF, "item": "TRADING_ITEM_BANANAS" },
        "0x087-Trade": {"cmd": MWCommands.CLEAR_TRADE_1, "mask": ~(1<<4)&0xFF, "item": "TRADING_ITEM_STICK" },
        "0x2D7-Trade": {"cmd": MWCommands.CLEAR_TRADE_1, "mask": ~(1<<5)&0xFF, "item": "TRADING_ITEM_HONEYCOMB" },
        "0x019-Trade": {"cmd": MWCommands.CLEAR_TRADE_1, "mask": ~(1<<6)&0xFF, "item": "TRADING_ITEM_PINEAPPLE" },
        "0x2D9-Trade": {"cmd": MWCommands.CLEAR_TRADE_1, "mask": ~(1<<7)&0xFF, "item": "TRADING_ITEM_HIBISCUS" },
        "0x2A8-Trade": {"cmd": MWCommands.CLEAR_TRADE_2, "mask": ~(1<<0)&0xFF, "item": "TRADING_ITEM_LETTER" },
        "0x0CD-Trade": {"cmd": MWCommands.CLEAR_TRADE_2, "mask": ~(1<<1)&0xFF, "item": "TRADING_ITEM_BROOM" },
        "0x2F5-Trade": {"cmd": MWCommands.CLEAR_TRADE_2, "mask": ~(1<<2)&0xFF, "item": "TRADING_ITEM_FISHING_HOOK" },
        "0x0C9-Trade": {"cmd": MWCommands.CLEAR_TRADE_2, "mask": ~(1<<3)&0xFF, "item": "TRADING_ITEM_NECKLACE" },
    }

    async def collect(self, ctx):
        if not self.gps_tracker.room or self.gps_tracker.is_transitioning:
            return
        current_room = '0x' + hex(self.gps_tracker.room)[2:].zfill(3).upper()
        for id in ctx.checked_locations:
            meta_id = links_awakening_location_id_to_meta[id]
            is_checked = next(x for x in self.tracker.all_checks if x.id == meta_id).value
            trade = self.restricted_trades.get(meta_id)
            if(is_checked
               or current_room == meta_id[:5] # player is in the location room
               or id not in ctx.locations_info # location scout data not in yet
               or (trade and not self.item_tracker.itemDict[trade["item"]].value) # restricted trade not met
               or (id in self.dependent_location_ids
                   and self.dependent_location_ids.get(id) not in ctx.checked_locations)): # location dependency not met
                continue
            check = self.tracker.meta_to_check[meta_id]
            item = ctx.locations_info[id]
            args = {
                "command": MWCommands.COLLECT,
                "mp_cd": check.address,
                "mp_e": check.mask,
            }
            if item.player == ctx.slot:
                args["command"] |= MWCommands.SEND_ITEM_SPECIAL
                args["item_code"] = item.item - Common.BASE_ID
                args["item_sender"] = clamp(0, ctx.slot, 101)
            if trade:
                args["command"] |= trade["cmd"]
                args["mp_f"] = trade["mask"]
            self.gameboy.send_mw_command(**args)
            break # one per cycle
        locations_to_scout = ctx.checked_locations - ctx.scouted_locations
        if len(locations_to_scout):
            await ctx.send_msgs([{
                "cmd": "LocationScouts",
                "locations": locations_to_scout
            }])
            ctx.scouted_locations.update(locations_to_scout)

    should_reset_auth = False
    async def wait_for_game_ready(self):
        logger.info("Waiting on game to be in valid state...")
        while not await self.gameboy.check_safe_gameplay(throw=False):
            if self.should_reset_auth:
                self.should_reset_auth = False
                raise GameboyException("Resetting due to wrong archipelago server")
        logger.info("Game connection ready!")

    async def main_tick(self, ctx, item_get_cb, win_cb, death_link_cb):
        await self.gameboy.update_cache()

        await self.tracker.readChecks(item_get_cb)
        await self.item_tracker.readItems()
        await self.gps_tracker.read_location()
        await self.gps_tracker.read_entrances()

        if not ctx.slot or not self.tracker.has_start_item():
            return

        wGameplayType = (await self.gameboy.async_read_memory(LAClientConstants.wGameplayType))[0]
        wHealth = (await self.gameboy.async_read_memory(LAClientConstants.wHealth))[0]
        cmd_block = await self.gameboy.async_read_memory(LAClientConstants.wMWRecvIndexHi, 3)
        if not await self.gameboy.check_safe_gameplay():
            return

        [wMWRecvIndexHi, wMWRecvIndexLo, wMWCommand] = cmd_block

        if wGameplayType == 1: # Credits
            await win_cb()

        if self.death_link_status == DeathLinkStatus.NONE:
            if not wHealth: # natural death
                await death_link_cb()
                self.death_link_status = DeathLinkStatus.DYING
        elif self.death_link_status == DeathLinkStatus.PENDING:
            if wMWCommand & MWCommands.DEATH_LINK:
                if not wMWCommand & MWCommands.EXECUTE_COMMAND:
                    self.death_link_status = DeathLinkStatus.DYING
                    self.gameboy.send_mw_command(command=MWCommands.NONE)
            else:
                self.gameboy.send_mw_command(command=MWCommands.DEATH_LINK)
        elif self.death_link_status == DeathLinkStatus.DYING:
            if wHealth:
                self.death_link_status = DeathLinkStatus.NONE

        if wMWCommand & MWCommands.EXECUTE_COMMAND or self.death_link_status:
            return

        recv_index = wMWRecvIndexHi << 8 | wMWRecvIndexLo
        if recv_index in ctx.recvd_checks:
            item = ctx.recvd_checks[recv_index]
            self.gameboy.send_mw_command(command=MWCommands.SEND_ITEM,
                                         item_code=item.item - Common.BASE_ID,
                                         item_sender=clamp(0, item.player, 101),
                                         mp_cd=recv_index)
            return

        if self.collect_enabled:
            await self.collect(ctx)

all_tasks = set()

def create_task_log_exception(awaitable) -> asyncio.Task:
    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:
            logger.exception(e)
            pass
        finally:
            all_tasks.remove(task)
    task = asyncio.create_task(_log_exception(awaitable))
    all_tasks.add(task)


class LinksAwakeningCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_toggle_collect(self):
        """Toggles collect."""
        if isinstance(self.ctx, LinksAwakeningContext):
            self.ctx.client.collect_enabled = not self.ctx.client.collect_enabled
            if self.ctx.client.collect_enabled:
                logger.info("Collect enabled")
            else:
                logger.info("Collect disabled")

    def _cmd_death_link(self):
        """Toggles death link."""
        if isinstance(self.ctx, LinksAwakeningContext):
            Utils.async_start(self.ctx.update_death_link("DeathLink" not in self.ctx.tags))

    def _cmd_die(self):
        """Simulate received death link."""
        if isinstance(self.ctx, LinksAwakeningContext):
            self.ctx.client.death_link_status = DeathLinkStatus.PENDING


class LinksAwakeningContext(CommonContext):
    tags = {"AP"}
    game = Common.LINKS_AWAKENING
    command_processor = LinksAwakeningCommandProcessor
    items_handling = 0b101
    want_slot_data = True
    la_task = None
    client = None
    found_checks = set()
    scouted_locations = set()
    recvd_checks = {}
    last_resend = time.time()

    magpie_enabled = False
    magpie = None
    magpie_task = None
    won = False

    @property
    def slot_storage_key(self):
        return f"{self.slot_info[self.slot].name}_{storage_key}"

    def __init__(self, server_address: str | None, password: str | None, magpie: bool) -> None:
        self.client = LinksAwakeningClient()
        self.slot_data = {}

        if magpie:
            self.magpie_enabled = True
            self.magpie = MagpieBridge()
        super().__init__(server_address, password)

    def run_gui(self) -> None:
        import webbrowser
        from kvui import GameManager
        from kivy.metrics import dp
        from kivymd.uix.button import MDButton, MDButtonText

        class LADXManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("Tracker", "Tracker"),
            ]
            base_title = "Archipelago Links Awakening DX Client"

            def build(self):
                b = super().build()

                if self.ctx.magpie_enabled:
                    button = MDButton(MDButtonText(text="Open Tracker"), style="filled", size=(dp(100), dp(70)), radius=5,
                                      size_hint_x=None, size_hint_y=None, pos_hint={"center_y": 0.55},
                                      on_press=lambda _: webbrowser.open('https://magpietracker.us/?enable_autotracker=1'))
                    button.height = self.server_connect_bar.height
                    self.connect_layout.add_widget(button)

                return b

        self.ui = LADXManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def send_new_entrances(self, entrances: typing.Dict[str, str]):
        # Store the entrances we find on the server for future sessions
        message = [{
            "cmd": "Set",
            "key": self.slot_storage_key,
            "default": {},
            "want_reply": False,
            "operations": [{"operation": "update", "value": entrances}],
        }]

        await self.send_msgs(message)

    had_invalid_slot_data = None
    def event_invalid_slot(self):
        # The next time we try to connect, reset the game loop for new auth
        self.had_invalid_slot_data = True
        self.auth = None
        # Don't try to autoreconnect, it will just fail
        self.disconnected_intentionally = True
        CommonContext.event_invalid_slot(self)

    async def send_death_link(self):
        if "DeathLink" in self.tags:
            logger.info("DeathLink: Sending death to your friends...")
            self.last_death_link = time.time()
            await self.send_msgs([{
                "cmd": "Bounce", "tags": ["DeathLink"],
                "data": {
                    "time": self.last_death_link,
                    "source": self.slot_info[self.slot].name,
                    "cause": self.slot_info[self.slot].name + " had a nightmare."
                }
            }])

    async def send_victory(self):
        if not self.won:
            message = [{"cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL}]
            logger.info("victory!")
            await self.send_msgs(message)
            self.won = True

    async def request_found_entrances(self):
        await self.send_msgs([{"cmd": "Get", "keys": [self.slot_storage_key]}])

        # Ask for updates so that players can co-op entrances in a seed
        await self.send_msgs([{"cmd": "SetNotify", "keys": [self.slot_storage_key]}])

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        self.client.death_link_status = DeathLinkStatus.PENDING
        super(LinksAwakeningContext, self).on_deathlink(data)

    def new_checks(self, item_ids, ladxr_ids):
        self.found_checks.update(item_ids)
        create_task_log_exception(self.check_locations(self.found_checks))
        if self.magpie_enabled:
            create_task_log_exception(self.magpie.send_new_checks(ladxr_ids))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(LinksAwakeningContext, self).server_auth(password_requested)

        if self.had_invalid_slot_data:
            # We are connecting when previously we had the wrong ROM or server - just in case
            # re-read the ROM so that if the user had the correct address but wrong ROM, we
            # allow a successful reconnect
            self.client.should_reset_auth = True
            self.had_invalid_slot_data = False

        while self.client.auth == None:
            await asyncio.sleep(0.1)

            # Just return if we're closing
            if self.exit_event.is_set():
                return
        self.auth = self.client.auth
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
            self.slot_data = args.get("slot_data", {})
            # This is sent to magpie over local websocket to make its own connection
            self.slot_data.update({
                "server_address": self.server_address,
                "slot_name": self.player_names[self.slot],
                "password": self.password,
            })
            if self.slot_data.get("death_link"):
                Utils.async_start(self.update_death_link(True))

            # We can process linked items on already-checked checks now that we have slot_data
            if self.client.tracker:
                checked_checks = set(self.client.tracker.all_checks) - set(self.client.tracker.remaining_checks)
                self.add_linked_items(checked_checks)

        # TODO - use watcher_event
        if cmd == "ReceivedItems":
            for index, item in enumerate(args["items"], start=args["index"]):
                self.recvd_checks[index] = item

        if cmd == "Retrieved" and self.magpie_enabled and self.slot_storage_key in args["keys"]:
            self.client.gps_tracker.receive_found_entrances(args["keys"][self.slot_storage_key])

        if cmd == "SetReply" and self.magpie_enabled and args["key"] == self.slot_storage_key:
            self.client.gps_tracker.receive_found_entrances(args["value"])

    async def sync(self):
        sync_msg = [{'cmd': 'Sync'}]
        await self.send_msgs(sync_msg)

    def add_linked_items(self, checks: typing.List[Check]):
        for check in checks:
            if check.value and check.linkedItem:
                linkedItem = check.linkedItem
                if 'condition' not in linkedItem or (self.slot_data and linkedItem['condition'](self.slot_data)):
                    self.client.item_tracker.setExtraItem(check.linkedItem['item'], check.linkedItem['qty'])

    async def run_game_loop(self):
        def on_item_get(ladxr_checks):
            checks = [links_awakening_location_meta_to_id[check.id] for check in ladxr_checks]
            self.new_checks(checks, [check.id for check in ladxr_checks])

            self.add_linked_items(ladxr_checks)

        async def victory():
            await self.send_victory()

        async def death_link():
            await self.send_death_link()

        if self.magpie_enabled:
            self.magpie_task = asyncio.create_task(self.magpie.serve())

        # yield to allow UI to start
        await asyncio.sleep(0)

        while True:
            try:
                # TODO: cancel all client tasks
                if not self.client.stop_bizhawk_spam:
                    logger.info("(Re)Starting game loop")
                self.found_checks.clear()
                # On restart of game loop, clear all checks, just in case we swapped ROMs
                # this isn't totally neccessary, but is extra safety against cross-ROM contamination
                self.recvd_checks.clear()
                await self.client.wait_for_retroarch_connection()
                await self.client.reset_auth()
                # If we find ourselves with new auth after the reset, reconnect
                if self.auth and self.client.auth != self.auth:
                    # It would be neat to reconnect here, but connection needs this loop to be running
                    logger.info("Detected new ROM, disconnecting...")
                    await self.disconnect()
                    continue

                if not self.recvd_checks:
                    await self.sync()

                await self.client.wait_and_init_tracker(self.magpie)

                min_tick_duration = 0.1
                last_tick = time.time()
                while True:
                    await self.client.main_tick(self, on_item_get, victory, death_link)

                    now = time.time()
                    tick_duration = now - last_tick
                    sleep_duration = max(min_tick_duration - tick_duration, 0)
                    await asyncio.sleep(sleep_duration)

                    last_tick = now

                    if self.last_resend + 5.0 < now:
                        self.last_resend = now
                        await self.check_locations(self.found_checks)
                    if self.magpie_enabled:
                        try:
                            self.magpie.set_checks(self.client.tracker.all_checks)
                            await self.magpie.set_item_tracker(self.client.item_tracker)
                            if self.slot_data and "slot_data" in self.magpie.features and not self.magpie.has_sent_slot_data:
                                self.magpie.slot_data = self.slot_data
                                await self.magpie.send_slot_data()

                            if self.client.gps_tracker.needs_found_entrances:
                                await self.request_found_entrances()
                                self.client.gps_tracker.needs_found_entrances = False

                            new_entrances = await self.magpie.send_gps(self.client.gps_tracker)
                            if new_entrances:
                                await self.send_new_entrances(new_entrances)
                        except Exception:
                            # Don't let magpie errors take out the client
                            pass
                    if self.client.should_reset_auth:
                        self.client.should_reset_auth = False
                        raise GameboyException("Resetting due to wrong archipelago server")
            except (GameboyException, asyncio.TimeoutError, TimeoutError, ConnectionResetError):
                await asyncio.sleep(1.0)

def run_game(romfile: str) -> None:
    auto_start = LinksAwakeningWorld.settings.rom_start

    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif isinstance(auto_start, str):
        args = shlex.split(auto_start)
        # Specify full path to ROM as we are going to cd in popen
        full_rom_path = os.path.realpath(romfile)
        args.append(full_rom_path)
        try:
            # set cwd so that paths to lua scripts are always relative to our client
            if getattr(sys, 'frozen', False):
                # The application is frozen
                script_dir = os.path.dirname(sys.executable)
            else:
                script_dir = os.path.dirname(os.path.realpath(__file__))

            subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=script_dir)
        except FileNotFoundError:
            logger.error(f"Couldn't launch ROM, {args[0]} is missing")

def launch(*launch_args):
    async def main():
        parser = get_base_parser(description="Link's Awakening Client.")
        parser.add_argument("--url", help="Archipelago connection url")
        parser.add_argument("--no-magpie", dest='magpie', default=True, action='store_false', help="Disable magpie bridge")
        parser.add_argument('diff_file', default="", type=str, nargs="?",
                            help='Path to a .apladx Archipelago Binary Patch file')

        args = parser.parse_args(launch_args)

        if args.diff_file:
            import Patch
            logger.info("patch file was supplied - creating rom...")
            meta, rom_file = Patch.create_rom_file(args.diff_file)
            if "server" in meta and not args.connect:
                args.connect = meta["server"]
            logger.info(f"wrote rom file to {rom_file}")


        ctx = LinksAwakeningContext(args.connect, args.password, args.magpie)

        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        # TODO: nothing about the lambda about has to be in a lambda
        ctx.la_task = create_task_log_exception(ctx.run_game_loop())
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        # Down below run_gui so that we get errors out of the process
        if args.diff_file:
            run_game(rom_file)

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("LinksAwakeningContext", exception_logger="Client")

    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
