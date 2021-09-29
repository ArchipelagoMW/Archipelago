import argparse
import atexit
exit_func = atexit.register(input, "Press enter to close.")
import threading
import time
import sys
import multiprocessing
import os
import subprocess
import base64
import shutil
import logging
import asyncio
from json import loads, dumps

from Utils import get_item_name_from_id


import ModuleUpdate

ModuleUpdate.update()

import colorama

from NetUtils import *

import Utils
from CommonClient import CommonContext, server_loop, console_loop, ClientCommandProcessor

snes_logger = logging.getLogger("SNES")

from MultiServer import mark_raw

os.makedirs("logs", exist_ok=True)

# Log to file in gui case
if getattr(sys, "frozen", False) and not "--nogui" in sys.argv:
    logging.basicConfig(format='[%(name)s]: %(message)s', level=logging.INFO,
                        filename=os.path.join("logs", "SmClient.txt"), filemode="w", force=True)
else:
    logging.basicConfig(format='[%(name)s]: %(message)s', level=logging.INFO, force=True)
    logging.getLogger().addHandler(logging.FileHandler(os.path.join("logs", "SmClient.txt"), "w"))


class SmCommandProcessor(ClientCommandProcessor):
    def _cmd_slow_mode(self, toggle: str = ""):
        """Toggle slow mode, which limits how fast you send / receive items."""
        if toggle:
            self.ctx.slow_mode = toggle.lower() in {"1", "true", "on"}
        else:
            self.ctx.slow_mode = not self.ctx.slow_mode

        self.output(f"Setting slow mode to {self.ctx.slow_mode}")

    @mark_raw
    def _cmd_snes(self, snes_options: str = "") -> bool:
        """Connect to a snes. Optionally include network address of a snes to connect to, otherwise show available devices; and a SNES device number if more than one SNES is detected"""
        
        snes_address = self.ctx.snes_address
        snes_device_number = -1
        
        options = snes_options.split()
        num_options = len(options)
        
        if num_options > 0:
            snes_address = options[0]
            
        if num_options > 1:
            try:
                snes_device_number = int(options[1])
            except:
                pass

        self.ctx.snes_reconnect_address = None
        asyncio.create_task(snes_connect(self.ctx, snes_address, snes_device_number))
        return True

    def _cmd_snes_close(self) -> bool:
        """Close connection to a currently connected snes"""
        self.ctx.snes_reconnect_address = None
        if self.ctx.snes_socket is not None and not self.ctx.snes_socket.closed:
            asyncio.create_task(self.ctx.snes_socket.close())
            return True
        else:
            return False

class Context(CommonContext):
    command_processor = SmCommandProcessor
    game = "Super Metroid"

    def __init__(self, snes_address, server_address, password):
        super(Context, self).__init__(server_address, password)

        # snes stuff
        self.snes_address = snes_address
        self.snes_socket = None
        self.snes_state = SNESState.SNES_DISCONNECTED
        self.snes_attached_device = None
        self.snes_reconnect_address = None
        self.snes_recv_queue = asyncio.Queue()
        self.snes_request_lock = asyncio.Lock()
        self.snes_write_buffer = []
        self.snes_connector_lock = threading.Lock()

        self.awaiting_rom = False
        self.rom = None
        self.prev_rom = None

    async def connection_closed(self):
        await super(Context, self).connection_closed()
        self.awaiting_rom = False

    def event_invalid_slot(self):
        if self.snes_socket is not None and not self.snes_socket.closed:
            asyncio.create_task(self.snes_socket.close())
        raise Exception('Invalid ROM detected, '
                        'please verify that you have loaded the correct rom and reconnect your snes (/snes)')

    async def server_auth(self, password_requested):
        if password_requested and not self.password:
            await super(Context, self).server_auth(password_requested)
        if self.rom is None:
            self.awaiting_rom = True
            snes_logger.info(
                'No ROM detected, awaiting snes connection to authenticate to the multiworld server (/snes)')
            return
        self.awaiting_rom = False
        self.auth = self.rom
        auth = base64.b64encode(self.rom).decode()
        await self.send_msgs([{"cmd": 'Connect',
                              'password': self.password, 'name': auth, 'version': Utils.version_tuple,
                              'tags': get_tags(self),
                              'uuid': Utils.get_unique_identifier(), 'game': "Super Metroid"
                              }])


def color_item(item_id: int, green: bool = False) -> str:
    item_name = get_item_name_from_id(item_id)
    item_colors = ['green' if green else 'cyan']
    return color(item_name, *item_colors)


SNES_RECONNECT_DELAY = 5

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

ROMNAME_START = 0x1C4F00
ROMNAME_SIZE = 0x15

INGAME_MODES = {0x07, 0x09, 0x0b}
ENDGAME_MODES = {0x26, 0x27}

SAVEDATA_START = WRAM_START + 0xF000
SAVEDATA_SIZE = 0x500

RECV_PROGRESS_ADDR = SRAM_START + 0x2000            # 2 bytes
RECV_ITEM_ADDR = SAVEDATA_START + 0x4D2             # 1 byte
RECV_ITEM_PLAYER_ADDR = SAVEDATA_START + 0x4D3      # 1 byte

class SNESState(enum.IntEnum):
    SNES_DISCONNECTED = 0
    SNES_CONNECTING = 1
    SNES_CONNECTED = 2
    SNES_ATTACHED = 3


def launch_sni(ctx: Context):
    sni_path = Utils.get_options()["sm_options"]["sni"]

    if not os.path.isdir(sni_path):
        sni_path = Utils.local_path(sni_path)
    if os.path.isdir(sni_path):
        for file in os.listdir(sni_path):
            if file.startswith("sni.") and not file.endswith(".proto"):
                sni_path = os.path.join(sni_path, file)

    if os.path.isfile(sni_path):
        snes_logger.info(f"Attempting to start {sni_path}")
        import subprocess
        if Utils.is_frozen(): # if it spawns a visible console, may as well populate it
            subprocess.Popen(sni_path, cwd=os.path.dirname(sni_path))
        else:
            subprocess.Popen(sni_path, cwd=os.path.dirname(sni_path), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        snes_logger.info(
            f"Attempt to start SNI was aborted as path {sni_path} was not found, "
            f"please start it yourself if it is not running")


async def _snes_connect(ctx: Context, address: str):
    address = f"ws://{address}" if "://" not in address else address
    snes_logger.info("Connecting to SNI at %s ..." % address)
    seen_problems = set()
    succesful = False
    while not succesful:
        try:
            snes_socket = await websockets.connect(address, ping_timeout=None, ping_interval=None)
            succesful = True
        except Exception as e:
            problem = "%s" % e
            # only tell the user about new problems, otherwise silently lay in wait for a working connection
            if problem not in seen_problems:
                seen_problems.add(problem)
                snes_logger.error(f"Error connecting to SNI ({problem})")

                if len(seen_problems) == 1:
                    # this is the first problem. Let's try launching SNI if it isn't already running
                    launch_sni(ctx)

            await asyncio.sleep(1)
        else:
            return snes_socket


async def get_snes_devices(ctx: Context):
    socket = await _snes_connect(ctx, ctx.snes_address)  # establish new connection to poll
    DeviceList_Request = {
        "Opcode": "DeviceList",
        "Space": "SNES"
    }
    await socket.send(dumps(DeviceList_Request))

    reply = loads(await socket.recv())
    devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else None

    if not devices:
        snes_logger.info('No SNES device found. Please connect a SNES device to SNI.')
        while not devices:
            await asyncio.sleep(1)
            await socket.send(dumps(DeviceList_Request))
            reply = loads(await socket.recv())
            devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else None


    await socket.close()
    return devices


async def snes_connect(ctx: Context, address, deviceIndex = -1):
    global SNES_RECONNECT_DELAY
    if ctx.snes_socket is not None and ctx.snes_state == SNESState.SNES_CONNECTED:
        if ctx.rom:
            snes_logger.error('Already connected to SNES, with rom loaded.')
        else:
            snes_logger.error('Already connected to SNI, likely awaiting a device.')
        return

    device = None
    recv_task = None
    ctx.snes_state = SNESState.SNES_CONNECTING
    socket = await _snes_connect(ctx, address)
    ctx.snes_socket = socket
    ctx.snes_state = SNESState.SNES_CONNECTED

    try:
        devices = await get_snes_devices(ctx)
        numDevices = len(devices)

        if numDevices == 1:
            device = devices[0]
        elif ctx.snes_reconnect_address:
            if ctx.snes_attached_device[1] in devices:
                device = ctx.snes_attached_device[1]
            else:
                device = devices[ctx.snes_attached_device[0]]
        elif numDevices > 1:
            if deviceIndex == -1:
                snes_logger.info("Found " + str(numDevices) + " SNES devices; connect to one with /snes <address> <device number>:")

                for idx, availableDevice in enumerate(devices):
                    snes_logger.info(str(idx + 1) + ": " + availableDevice)

            elif (deviceIndex < 0) or (deviceIndex - 1) > numDevices:
                snes_logger.warning("SNES device number out of range")

            else:
                device = devices[deviceIndex - 1]
            
        if device is None:
            await snes_disconnect(ctx)
            return

        snes_logger.info("Attaching to " + device)

        Attach_Request = {
            "Opcode": "Attach",
            "Space": "SNES",
            "Operands": [device]
        }
        await ctx.snes_socket.send(dumps(Attach_Request))
        ctx.snes_state = SNESState.SNES_ATTACHED
        ctx.snes_attached_device = (devices.index(device), device)
        ctx.snes_reconnect_address = address
        recv_task = asyncio.create_task(snes_recv_loop(ctx))
        SNES_RECONNECT_DELAY = ctx.starting_reconnect_delay
        snes_logger.info(f"Attached to {device}")

    except Exception as e:
        if recv_task is not None:
            if not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
        else:
            if ctx.snes_socket is not None:
                if not ctx.snes_socket.closed:
                    await ctx.snes_socket.close()
                ctx.snes_socket = None
            ctx.snes_state = SNESState.SNES_DISCONNECTED
        if not ctx.snes_reconnect_address:
            snes_logger.error("Error connecting to snes (%s)" % e)
        else:
            snes_logger.error(f"Error connecting to snes, attempt again in {SNES_RECONNECT_DELAY}s")
            asyncio.create_task(snes_autoreconnect(ctx))
        SNES_RECONNECT_DELAY *= 2


async def snes_disconnect(ctx: Context):
    if ctx.snes_socket:
        if not ctx.snes_socket.closed:
            await ctx.snes_socket.close()
        ctx.snes_socket = None


async def snes_autoreconnect(ctx: Context):
    # unfortunately currently broken. See: https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1033
    # with prompt_toolkit.shortcuts.ProgressBar() as pb:
    #    for _ in pb(range(100)):
    #        await asyncio.sleep(RECONNECT_DELAY/100)

    await asyncio.sleep(SNES_RECONNECT_DELAY)
    if ctx.snes_reconnect_address and ctx.snes_socket is None:
        await snes_connect(ctx, ctx.snes_reconnect_address)


async def snes_recv_loop(ctx: Context):
    try:
        async for msg in ctx.snes_socket:
            ctx.snes_recv_queue.put_nowait(msg)
        snes_logger.warning("Snes disconnected")
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            snes_logger.exception(e)
        snes_logger.error("Lost connection to the snes, type /snes to reconnect")
    finally:
        socket, ctx.snes_socket = ctx.snes_socket, None
        if socket is not None and not socket.closed:
            await socket.close()

        ctx.snes_state = SNESState.SNES_DISCONNECTED
        ctx.snes_recv_queue = asyncio.Queue()
        ctx.hud_message_queue = []

        ctx.rom = None

        if ctx.snes_reconnect_address:
            snes_logger.info(f"...reconnecting in {SNES_RECONNECT_DELAY}s")
            asyncio.create_task(snes_autoreconnect(ctx))


async def snes_read(ctx: Context, address, size):
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNESState.SNES_ATTACHED or ctx.snes_socket is None or not ctx.snes_socket.open or ctx.snes_socket.closed:
            return None

        GetAddress_Request = {
            "Opcode": "GetAddress",
            "Space": "SNES",
            "Operands": [hex(address)[2:], hex(size)[2:]]
        }
        try:
            await ctx.snes_socket.send(dumps(GetAddress_Request))
        except websockets.ConnectionClosed:
            return None

        data = bytes()
        while len(data) < size:
            try:
                data += await asyncio.wait_for(ctx.snes_recv_queue.get(), 5)
            except asyncio.TimeoutError:
                break

        if len(data) != size:
            snes_logger.error('Error reading %s, requested %d bytes, received %d' % (hex(address), size, len(data)))
            if len(data):
                snes_logger.error(str(data))
                snes_logger.warning('Communication Failure with SNI')
            if ctx.snes_socket is not None and not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
            return None

        return data
    finally:
        ctx.snes_request_lock.release()


async def snes_write(ctx: Context, write_list):
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNESState.SNES_ATTACHED or ctx.snes_socket is None or \
                not ctx.snes_socket.open or ctx.snes_socket.closed:
            return False

        PutAddress_Request = {"Opcode": "PutAddress", "Operands": [], 'Space': 'SNES'}
        try:
            for address, data in write_list:
                PutAddress_Request['Operands'] = [hex(address)[2:], hex(len(data))[2:]]
                if ctx.snes_socket is not None:
                    await ctx.snes_socket.send(dumps(PutAddress_Request))
                    await ctx.snes_socket.send(data)
                else:
                    snes_logger.warning(f"Could not send data to SNES: {data}")
        except websockets.ConnectionClosed:
            return False

        return True
    finally:
        ctx.snes_request_lock.release()


def snes_buffered_write(ctx: Context, address, data):
    if ctx.snes_write_buffer and (ctx.snes_write_buffer[-1][0] + len(ctx.snes_write_buffer[-1][1])) == address:
        # append to existing write command, bundling them
        ctx.snes_write_buffer[-1] = (ctx.snes_write_buffer[-1][0], ctx.snes_write_buffer[-1][1] + data)
    else:
        ctx.snes_write_buffer.append((address, data))


async def snes_flush_writes(ctx: Context):
    if not ctx.snes_write_buffer:
        return

    # swap buffers
    ctx.snes_write_buffer, writes = [], ctx.snes_write_buffer
    await snes_write(ctx, writes)


# kept as function for easier wrapping by plugins
def get_tags(ctx: Context):
    tags = ['AP']
    return tags


async def game_watcher(ctx: Context):
    prev_game_timer = 0
    perf_counter = time.perf_counter()
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()

        if not ctx.rom:
            ctx.finished_game = False
            rom = await snes_read(ctx, ROMNAME_START, ROMNAME_SIZE)
            if rom is None or rom == bytes([0] * ROMNAME_SIZE):
                continue

            ctx.rom = rom
            if not ctx.prev_rom or ctx.prev_rom != ctx.rom:
                ctx.locations_checked = set()
                ctx.locations_scouted = set()
            ctx.prev_rom = ctx.rom

            if ctx.awaiting_rom:
                await ctx.server_auth(False)

        if ctx.auth and ctx.auth != ctx.rom:
            snes_logger.warning("ROM change detected, please reconnect to the multiworld server")
            await ctx.disconnect()

        gamemode = await snes_read(ctx, WRAM_START + 0x0998, 1)
        if gamemode is not None and gamemode[0] in ENDGAME_MODES:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True
            continue

        data = await snes_read(ctx, RECV_PROGRESS_ADDR + 0x680, 4)
        if data is None:
            continue

        recv_index = data[0] | (data[1] << 8)
        recv_item = data[2] | (data[3] << 8)

        while (recv_index < recv_item):
            itemAdress = recv_index * 8
            message = await snes_read(ctx, RECV_PROGRESS_ADDR + 0x700 + itemAdress, 8)
            worldId = message[0] | (message[1] << 8)
            itemId = message[2] | (message[3] << 8)
            itemIndex = (message[4] | (message[5] << 8)) >> 3
            seq = recv_index

            recv_index += 1
            snes_buffered_write(ctx, RECV_PROGRESS_ADDR + 0x680, bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))

            from worlds.sm.Locations import locations_start_id
            location_id = locations_start_id + itemIndex

            ctx.locations_checked.add(location_id)
            location = ctx.location_name_getter(location_id)
            snes_logger.info(f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])

        data = await snes_read(ctx, RECV_PROGRESS_ADDR + 0x600, 4)
        if data is None:
            continue

        recv_itemOutPtr = data[0] | (data[1] << 8)
        itemOutPtr = data[2] | (data[3] << 8)

        from worlds.sm.Items import items_start_id
        if itemOutPtr < len(ctx.items_received):
            item = ctx.items_received[itemOutPtr]
            itemId = item.item - items_start_id

            playerID = (item.player-1) if item.player != 0 else (len(ctx.player_names)-1)
            snes_buffered_write(ctx, RECV_PROGRESS_ADDR + itemOutPtr * 4, bytes([playerID & 0xFF, (playerID >> 8) & 0xFF, itemId & 0xFF, (itemId >> 8) & 0xFF]))
            itemOutPtr += 1
            snes_buffered_write(ctx, RECV_PROGRESS_ADDR + 0x602, bytes([itemOutPtr & 0xFF, (itemOutPtr >> 8) & 0xFF]))
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_name_getter(item.item), 'red', 'bold'), color(ctx.player_names[item.player], 'yellow'),
                ctx.location_name_getter(item.location), itemOutPtr, len(ctx.items_received)))
        await snes_flush_writes(ctx)

async def run_game(romfile):
    auto_start = Utils.get_options()["sm_options"].get("rom_start", True)
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def main():
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser()
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a Archipelago Binary Patch file')
    parser.add_argument('--snes', default='localhost:8080', help='Address of the SNI server.')
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    parser.add_argument('--founditems', default=False, action='store_true',
                        help='Show items found by other players for themselves.')
    if not Utils.is_frozen():  # Frozen state has no cmd window in the first place
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")
    args = parser.parse_args()
    logging.basicConfig(format='%(message)s', level=getattr(logging, args.loglevel.upper(), logging.INFO))
    if args.diff_file:
        import Patch
        logging.info("Patch file was supplied. Creating sfc rom..")
        meta, romfile = Patch.create_rom_file(args.diff_file)
        args.connect = meta["server"]
        logging.info(f"Wrote rom file to {romfile}")
        adjustedromfile, adjusted = Utils.get_adjuster_settings(romfile)
        if adjusted:
            try:
                shutil.move(adjustedromfile, romfile)
                adjustedromfile = romfile
            except Exception as e:
                logging.exception(e)
        asyncio.create_task(run_game(adjustedromfile if adjusted else romfile))

    ctx = Context(args.snes, args.connect, args.password)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if Utils.is_frozen() or "--nogui" not in sys.argv:
        input_task = None
        from kvui import LttPManager
        ctx.ui = LttPManager(ctx)
        ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
    else:
        input_task = asyncio.create_task(console_loop(ctx), name="Input")
        ui_task = None

    snes_connect_task = asyncio.create_task(snes_connect(ctx, ctx.snes_address))
    watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

    await ctx.exit_event.wait()
    if snes_connect_task:
        snes_connect_task.cancel()
    ctx.server_address = None
    ctx.snes_reconnect_address = None

    await watcher_task

    if ctx.server and not ctx.server.socket.closed:
        await ctx.server.socket.close()
    if ctx.server_task:
        await ctx.server_task

    if ctx.snes_socket is not None and not ctx.snes_socket.closed:
        await ctx.snes_socket.close()

    while ctx.input_requests > 0:
        ctx.input_queue.put_nowait(None)
        ctx.input_requests -= 1

    if ui_task:
        await ui_task

    if input_task:
        input_task.cancel()


if __name__ == '__main__':
    colorama.init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    colorama.deinit()
    atexit.unregister(exit_func)
