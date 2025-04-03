import ModuleUpdate
ModuleUpdate.update()

import Utils

if __name__ == "__main__":
    Utils.init_logging("LinksAwakeningContext", exception_logger="Client")

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


from CommonClient import (CommonContext, get_base_parser, gui_enabled, logger,
                          server_loop)
from NetUtils import ClientStatus
from worlds.ladx.Common import BASE_ID as LABaseID
from worlds.ladx.GpsTracker import GpsTracker
from worlds.ladx.TrackerConsts import storage_key
from worlds.ladx.ItemTracker import ItemTracker
from worlds.ladx.LADXR.checkMetadata import checkMetadataTable
from worlds.ladx.Locations import get_locations_to_id, meta_to_name
from worlds.ladx.Tracker import LocationTracker, MagpieBridge


class GameboyException(Exception):
    pass


class RetroArchDisconnectError(GameboyException):
    pass


class InvalidEmulatorStateError(GameboyException):
    pass


class BadRetroArchResponse(GameboyException):
    pass


def magpie_logo():
    from kivy.uix.image import CoreImage
    binary_data = """
iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAAXN
SR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA
7DAcdvqGQAAADGSURBVDhPhVLBEcIwDHOYhjHCBuXHj2OTbAL8+
MEGZIxOQ1CinOOk0Op0bmo7tlXXeR9FJMYDLOD9mwcLjQK7+hSZ
wgcWMZJOAGeGKtChNHFL0j+FZD3jSCuo0w7l03wDrWdg00C4/aW
eDEYNenuzPOfPspBnxf0kssE80vN0L8361j10P03DK4x6FHabuV
ear8fHme+b17rwSjbAXeUMLb+EVTV2QHm46MWQanmnydA98KsVS
XkV+qFpGQXrLhT/fqraQeQLuplpNH5g+WkAAAAASUVORK5CYII="""
    binary_data = base64.b64decode(binary_data)
    data = io.BytesIO(binary_data)
    return CoreImage(data, ext="png").texture


class LAClientConstants:
    # Connector version
    VERSION = 0x01
    #
    # Memory locations of LADXR
    ROMGameID = 0x0051  # 4 bytes
    SlotName = 0x0134
    # Unused
    # ROMWorldID = 0x0055
    # ROMConnectorVersion = 0x0056
    # RO: We should only act if this is higher then 6, as it indicates that the game is running normally
    wGameplayType = 0xDB95
    # RO: Starts at 0, increases every time an item is received from the server and processed
    wLinkSyncSequenceNumber = 0xDDF6
    wLinkStatusBits = 0xDDF7          # RW:
    #      Bit0: wLinkGive* contains valid data, set from script cleared from ROM.
    wLinkHealth = 0xDB5A
    wLinkGiveItem = 0xDDF8  # RW
    wLinkGiveItemFrom = 0xDDF9  # RW
    # All of these six bytes are unused, we can repurpose
    # wLinkSendItemRoomHigh = 0xDDFA  # RO
    # wLinkSendItemRoomLow = 0xDDFB  # RO
    # wLinkSendItemTarget = 0xDDFC  # RO
    # wLinkSendItemItem = 0xDDFD  # RO
    # wLinkSendShopItem = 0xDDFE # RO, which item to send (1 based, order of the shop items)
    # RO, which player to send to, but it's just the X position of the NPC used, so 0x18 is player 0
    # wLinkSendShopTarget = 0xDDFF


    wRecvIndex = 0xDDFD # Two bytes
    wCheckAddress = 0xC0FF - 0x4
    WRamCheckSize = 0x4
    WRamSafetyValue = bytearray([0]*WRamCheckSize)

    wRamStart = 0xC000
    hRamStart = 0xFF80
    hRamSize = 0x80

    MinGameplayValue = 0x06
    MaxGameplayValue = 0x1A
    VictoryGameplayAndSub = 0x0102

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


class LinksAwakeningClient():
    socket = None
    gameboy = None
    tracker = None
    auth = None
    game_crc = None
    pending_deathlink = False
    deathlink_debounce = True
    recvd_checks = {}
    retroarch_address = None
    retroarch_port = None
    gameboy = None

    def msg(self, m):
        logger.info(m)
        s = f"SHOW_MSG {m}\n"
        self.gameboy.send(s)

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
        auth = binascii.hexlify(await self.gameboy.async_read_memory(0x0134, 12)).decode()
        self.auth = auth

    async def wait_and_init_tracker(self, magpie: MagpieBridge):
        await self.wait_for_game_ready()
        self.tracker = LocationTracker(self.gameboy)
        self.item_tracker = ItemTracker(self.gameboy)
        self.gps_tracker = GpsTracker(self.gameboy)
        magpie.gps_tracker = self.gps_tracker

    async def recved_item_from_ap(self, item_id, from_player, next_index):
        # Don't allow getting an item until you've got your first check
        if not self.tracker.has_start_item():
            return

        # Spin until we either:
        # get an exception from a bad read (emu shut down or reset)
        # beat the game
        # the client handles the last pending item
        status = (await self.gameboy.async_read_memory_safe(LAClientConstants.wLinkStatusBits))[0]
        while not (await self.is_victory()) and status & 1 == 1:
            time.sleep(0.1)
            status = (await self.gameboy.async_read_memory_safe(LAClientConstants.wLinkStatusBits))[0]

        item_id -= LABaseID
        # The player name table only goes up to 100, so don't go past that
        # Even if it didn't, the remote player _index_ byte is just a byte, so 255 max
        if from_player > 100:
            from_player = 100

        next_index += 1
        self.gameboy.write_memory(LAClientConstants.wLinkGiveItem, [
                                  item_id, from_player])
        status |= 1
        status = self.gameboy.write_memory(LAClientConstants.wLinkStatusBits, [status])
        self.gameboy.write_memory(LAClientConstants.wRecvIndex, struct.pack(">H", next_index))

    should_reset_auth = False
    async def wait_for_game_ready(self):
        logger.info("Waiting on game to be in valid state...")
        while not await self.gameboy.check_safe_gameplay(throw=False):
            if self.should_reset_auth:
                self.should_reset_auth = False
                raise GameboyException("Resetting due to wrong archipelago server")
        logger.info("Game connection ready!")

    async def is_victory(self):
        return (await self.gameboy.read_memory_cache([LAClientConstants.wGameplayType]))[LAClientConstants.wGameplayType] == 1

    async def main_tick(self, item_get_cb, win_cb, deathlink_cb):
        await self.gameboy.update_cache()
        await self.tracker.readChecks(item_get_cb)
        await self.item_tracker.readItems()
        await self.gps_tracker.read_location()
        await self.gps_tracker.read_entrances()

        current_health = (await self.gameboy.read_memory_cache([LAClientConstants.wLinkHealth]))[LAClientConstants.wLinkHealth]
        if self.deathlink_debounce and current_health != 0:
            self.deathlink_debounce = False
        elif not self.deathlink_debounce and current_health == 0:
            # logger.info("YOU DIED.")
            await deathlink_cb()
            self.deathlink_debounce = True

        if self.pending_deathlink:
            logger.info("Got a deathlink")
            self.gameboy.write_memory(LAClientConstants.wLinkHealth, [0])
            self.pending_deathlink = False
            self.deathlink_debounce = True

        if await self.is_victory():
            await win_cb()

        recv_index = struct.unpack(">H", await self.gameboy.async_read_memory(LAClientConstants.wRecvIndex, 2))[0]

        # Play back one at a time
        if recv_index in self.recvd_checks:
            item = self.recvd_checks[recv_index]
            await self.recved_item_from_ap(item.item, item.player, recv_index)


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


class LinksAwakeningContext(CommonContext):
    tags = {"AP"}
    game = "Links Awakening DX"
    items_handling = 0b101
    want_slot_data = True
    la_task = None
    client = None
    # TODO: does this need to re-read on reset?
    found_checks = set()
    last_resend = time.time()

    magpie_enabled = False
    magpie = None
    magpie_task = None
    won = False

    @property 
    def slot_storage_key(self): 
        return f"{self.slot_info[self.slot].name}_{storage_key}"

    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str], magpie: typing.Optional[bool]) -> None:
        self.client = LinksAwakeningClient()
        self.slot_data = {}

        if magpie:
            self.magpie_enabled = True
            self.magpie = MagpieBridge()
        super().__init__(server_address, password)

    def run_gui(self) -> None:
        import webbrowser
        import kvui
        from kvui import Button, GameManager
        from kivy.uix.image import Image

        class LADXManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("Tracker", "Tracker"),
            ]
            base_title = "Archipelago Links Awakening DX Client"

            def build(self):
                b = super().build()

                if self.ctx.magpie_enabled:
                    button = Button(text="", size=(30, 30), size_hint_x=None,
                                    on_press=lambda _: webbrowser.open('https://magpietracker.us/?enable_autotracker=1'))
                    image = Image(size=(16, 16), texture=magpie_logo())
                    button.add_widget(image)

                    def set_center(_, center):
                        image.center = center
                    button.bind(center=set_center)

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

    ENABLE_DEATHLINK = False
    async def send_deathlink(self):
        if self.ENABLE_DEATHLINK:
            message = [{"cmd": 'Deathlink',
                        'time': time.time(),
                        'cause': 'Had a nightmare',
                        # 'source': self.slot_info[self.slot].name,
                        }]
            await self.send_msgs(message)

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

    async def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        if self.ENABLE_DEATHLINK:
            self.client.pending_deathlink = True

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
            
        # TODO - use watcher_event
        if cmd == "ReceivedItems":
            for index, item in enumerate(args["items"], start=args["index"]):
                self.client.recvd_checks[index] = item
        
        if cmd == "Retrieved" and self.magpie_enabled and self.slot_storage_key in args["keys"]:
            self.client.gps_tracker.receive_found_entrances(args["keys"][self.slot_storage_key])

        if cmd == "SetReply" and self.magpie_enabled and args["key"] == self.slot_storage_key:
            self.client.gps_tracker.receive_found_entrances(args["value"])

    async def sync(self):
        sync_msg = [{'cmd': 'Sync'}]
        await self.send_msgs(sync_msg)

    item_id_lookup = get_locations_to_id()

    async def run_game_loop(self):
        def on_item_get(ladxr_checks):
            checks = [self.item_id_lookup[meta_to_name(
                checkMetadataTable[check.id])] for check in ladxr_checks]
            self.new_checks(checks, [check.id for check in ladxr_checks])

            for check in ladxr_checks:
                if check.value and check.linkedItem:
                    linkedItem = check.linkedItem
                    if 'condition' not in linkedItem or linkedItem['condition'](self.slot_data):
                        self.client.item_tracker.setExtraItem(check.linkedItem['item'], check.linkedItem['qty'])

        async def victory():
            await self.send_victory()

        async def deathlink():
            await self.send_deathlink()

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
                self.client.recvd_checks.clear()
                await self.client.wait_for_retroarch_connection()
                await self.client.reset_auth()
                # If we find ourselves with new auth after the reset, reconnect
                if self.auth and self.client.auth != self.auth:
                    # It would be neat to reconnect here, but connection needs this loop to be running
                    logger.info("Detected new ROM, disconnecting...")
                    await self.disconnect()
                    continue

                if not self.client.recvd_checks:
                    await self.sync()

                await self.client.wait_and_init_tracker(self.magpie)

                min_tick_duration = 0.1
                last_tick = time.time()
                while True:
                    await self.client.main_tick(on_item_get, victory, deathlink)

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
                            self.magpie.slot_data = self.slot_data
                            
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
    auto_start = typing.cast(typing.Union[bool, str],
                            Utils.get_options()["ladx_options"].get("rom_start", True))
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

async def main():
    parser = get_base_parser(description="Link's Awakening Client.")
    parser.add_argument("--url", help="Archipelago connection url")
    parser.add_argument("--no-magpie", dest='magpie', default=True, action='store_false', help="Disable magpie bridge")
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a .apladx Archipelago Binary Patch file')

    args = parser.parse_args()

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

if __name__ == '__main__':
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
