from __future__ import annotations

import sys
import threading
import time
import multiprocessing
import os
import subprocess
import base64
import logging
import asyncio
import enum
import typing

from json import loads, dumps

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser

import Utils
from Utils import async_start
from MultiServer import mark_raw
if typing.TYPE_CHECKING:
    from worlds.AutoSNIClient import SNIClient

if __name__ == "__main__":
    Utils.init_logging("SNIClient", exception_logger="Client")

import colorama
from websockets.client import connect as websockets_connect, WebSocketClientProtocol
from websockets.exceptions import WebSocketException, ConnectionClosed

snes_logger = logging.getLogger("SNES")


class DeathState(enum.IntEnum):
    killing_player = 1
    alive = 2
    dead = 3


class SNIClientCommandProcessor(ClientCommandProcessor):
    ctx: SNIContext

    def _cmd_slow_mode(self, toggle: str = "") -> None:
        """Toggle slow mode, which limits how fast you send / receive items."""
        if toggle:
            self.ctx.slow_mode = toggle.lower() in {"1", "true", "on"}
        else:
            self.ctx.slow_mode = not self.ctx.slow_mode

        self.output(f"Setting slow mode to {self.ctx.slow_mode}")

    @mark_raw
    def _cmd_snes(self, snes_options: str = "") -> bool:
        """Connect to a snes. Optionally include network address of a snes to connect to,
        otherwise show available devices; and a SNES device number if more than one SNES is detected.
        Examples: "/snes", "/snes 1", "/snes localhost:23074 1" """
        if self.ctx.snes_state in {SNESState.SNES_ATTACHED, SNESState.SNES_CONNECTED, SNESState.SNES_CONNECTING}:
            self.output("Already connected to SNES. Disconnecting first.")
            self._cmd_snes_close()
        return self.connect_to_snes(snes_options)

    def connect_to_snes(self, snes_options: str = "") -> bool:
        snes_address = self.ctx.snes_address
        snes_device_number = -1

        options = snes_options.split()
        num_options = len(options)

        if num_options > 1:
            snes_address = options[0]
            snes_device_number = int(options[1])
        elif num_options > 0:
            snes_device_number = int(options[0])

        self.ctx.snes_reconnect_address = None
        if self.ctx.snes_connect_task:
            self.ctx.snes_connect_task.cancel()
        self.ctx.snes_connect_task = asyncio.create_task(snes_connect(self.ctx, snes_address, snes_device_number),
                                                         name="SNES Connect")
        return True

    def _cmd_snes_close(self) -> bool:
        """Close connection to a currently connected snes"""
        self.ctx.snes_reconnect_address = None
        self.ctx.cancel_snes_autoreconnect()
        self.ctx.snes_state = SNESState.SNES_DISCONNECTED
        if self.ctx.snes_socket and not self.ctx.snes_socket.closed:
            async_start(self.ctx.snes_socket.close())
            return True
        else:
            return False

    # Left here for quick re-addition for debugging.
    # def _cmd_snes_write(self, address, data):
    #     """Write the specified byte (base10) to the SNES' memory address (base16)."""
    #     if self.ctx.snes_state != SNESState.SNES_ATTACHED:
    #         self.output("No attached SNES Device.")
    #         return False
    #     snes_buffered_write(self.ctx, int(address, 16), bytes([int(data)]))
    #     async_start(snes_flush_writes(self.ctx))
    #     self.output("Data Sent")
    #     return True

    # def _cmd_snes_read(self, address, size=1):
    #     """Read the SNES' memory address (base16)."""
    #     if self.ctx.snes_state != SNESState.SNES_ATTACHED:
    #         self.output("No attached SNES Device.")
    #         return False
    #     data = await snes_read(self.ctx, int(address, 16), size)
    #     self.output(f"Data Read: {data}")
    #     return True


class SNIContext(CommonContext):
    command_processor: typing.Type[SNIClientCommandProcessor] = SNIClientCommandProcessor
    game: typing.Optional[str] = None  # set in validate_rom
    items_handling: typing.Optional[int] = None  # set in game_watcher
    snes_connect_task: "typing.Optional[asyncio.Task[None]]" = None
    snes_autoreconnect_task: typing.Optional["asyncio.Task[None]"] = None

    snes_address: str
    snes_socket: typing.Optional[WebSocketClientProtocol]
    snes_state: SNESState
    snes_attached_device: typing.Optional[typing.Tuple[int, str]]
    snes_reconnect_address: typing.Optional[str]
    snes_recv_queue: "asyncio.Queue[bytes]"
    snes_request_lock: asyncio.Lock
    snes_write_buffer: typing.List[typing.Tuple[int, bytes]]
    snes_connector_lock: threading.Lock
    death_state: DeathState
    killing_player_task: "typing.Optional[asyncio.Task[None]]"
    allow_collect: bool
    slow_mode: bool

    client_handler: typing.Optional[SNIClient]
    awaiting_rom: bool
    rom: typing.Optional[bytes]
    prev_rom: typing.Optional[bytes]

    hud_message_queue: typing.List[str]  # TODO: str is a guess, is this right?
    death_link_allow_survive: bool

    def __init__(self, snes_address: str, server_address: str, password: str) -> None:
        super(SNIContext, self).__init__(server_address, password)

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
        self.death_state = DeathState.alive  # for death link flop behaviour
        self.killing_player_task = None
        self.allow_collect = False
        self.slow_mode = False

        self.client_handler = None
        self.awaiting_rom = False
        self.rom = None
        self.prev_rom = None

    async def connection_closed(self) -> None:
        await super(SNIContext, self).connection_closed()
        self.awaiting_rom = False

    def event_invalid_slot(self) -> typing.NoReturn:
        if self.snes_socket is not None and not self.snes_socket.closed:
            async_start(self.snes_socket.close())
        raise Exception("Invalid ROM detected, "
                        "please verify that you have loaded the correct rom and reconnect your snes (/snes)")

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(SNIContext, self).server_auth(password_requested)
        if self.rom is None:
            self.awaiting_rom = True
            snes_logger.info(
                "No ROM detected, awaiting snes connection to authenticate to the multiworld server (/snes)")
            return
        self.awaiting_rom = False
        # TODO: This looks kind of hacky...
        # Context.auth is meant to be the "name" parameter in send_connect,
        # which has to be a str (bytes is not json serializable).
        # But here, Context.auth is being used for something else
        # (where it has to be bytes because it is compared with rom elsewhere).
        # If we need to save something to compare with rom elsewhere,
        # it should probably be in a different variable,
        # and let auth be used for what it's meant for.
        self.auth = self.rom
        auth = base64.b64encode(self.rom).decode()
        await self.send_connect(name=auth)

    def cancel_snes_autoreconnect(self) -> bool:
        if self.snes_autoreconnect_task:
            self.snes_autoreconnect_task.cancel()
            self.snes_autoreconnect_task = None
            return True
        return False

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        if not self.killing_player_task or self.killing_player_task.done():
            self.killing_player_task = asyncio.create_task(deathlink_kill_player(self))
        super(SNIContext, self).on_deathlink(data)

    async def handle_deathlink_state(self, currently_dead: bool, death_text: str = "") -> None:
        # in this state we only care about triggering a death send
        if self.death_state == DeathState.alive:
            if currently_dead:
                self.death_state = DeathState.dead
                await self.send_death(death_text)
        # in this state we care about confirming a kill, to move state to dead
        elif self.death_state == DeathState.killing_player:
            # this is being handled in deathlink_kill_player(ctx) already
            pass
        # in this state we wait until the player is alive again
        elif self.death_state == DeathState.dead:
            if not currently_dead:
                self.death_state = DeathState.alive

    async def shutdown(self) -> None:
        await super(SNIContext, self).shutdown()
        self.cancel_snes_autoreconnect()
        if self.snes_connect_task:
            try:
                await asyncio.wait_for(self.snes_connect_task, 1)
            except asyncio.TimeoutError:
                self.snes_connect_task.cancel()

    def on_package(self, cmd: str, args: typing.Dict[str, typing.Any]) -> None:
        if cmd in {"Connected", "RoomUpdate"}:
            if "checked_locations" in args and args["checked_locations"]:
                new_locations = set(args["checked_locations"])
                self.checked_locations |= new_locations
                self.locations_scouted |= new_locations
                # Items belonging to the player should not be marked as checked in game,
                # since the player will likely need that item.
                # Once the games handled by SNIClient gets made to be remote items,
                # this will no longer be needed.
                async_start(self.send_msgs([{"cmd": "LocationScouts", "locations": list(new_locations)}]))
                
        if self.client_handler is not None:
            self.client_handler.on_package(self, cmd, args)

    def run_gui(self) -> None:
        from kvui import GameManager

        class SNIManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("SNES", "SNES"),
            ]
            base_title = "Archipelago SNI Client"

        self.ui = SNIManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")  # type: ignore


async def deathlink_kill_player(ctx: SNIContext) -> None:
    ctx.death_state = DeathState.killing_player
    while ctx.death_state == DeathState.killing_player and \
            ctx.snes_state == SNESState.SNES_ATTACHED:

        if ctx.client_handler is None:
            continue

        await ctx.client_handler.deathlink_kill_player(ctx)

        ctx.last_death_link = time.time()


_global_snes_reconnect_delay = 5


class SNESState(enum.IntEnum):
    SNES_DISCONNECTED = 0
    SNES_CONNECTING = 1
    SNES_CONNECTED = 2
    SNES_ATTACHED = 3


def launch_sni() -> None:
    sni_path = Utils.get_settings()["sni_options"]["sni_path"]

    if not os.path.isdir(sni_path):
        sni_path = Utils.local_path(sni_path)
    if os.path.isdir(sni_path):
        dir_entry: "os.DirEntry[str]"
        for dir_entry in os.scandir(sni_path):
            if dir_entry.is_file():
                lower_file = dir_entry.name.lower()
                if (lower_file.startswith("sni.") and not lower_file.endswith(".proto")) or (lower_file == "sni"):
                    sni_path = dir_entry.path
                    break

    if os.path.isfile(sni_path):
        snes_logger.info(f"Attempting to start {sni_path}")
        import sys
        if not sys.stdout:  # if it spawns a visible console, may as well populate it
            subprocess.Popen(os.path.abspath(sni_path), cwd=os.path.dirname(sni_path))
        else:
            proc = subprocess.Popen(os.path.abspath(sni_path), cwd=os.path.dirname(sni_path),
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                proc.wait(.1)  # wait a bit to see if startup fails (missing dependencies)
                snes_logger.info('Failed to start SNI. Try running it externally for error output.')
            except subprocess.TimeoutExpired:
                pass  # seems to be running

    else:
        snes_logger.info(
            f"Attempt to start SNI was aborted as path {sni_path} was not found, "
            f"please start it yourself if it is not running")


async def _snes_connect(ctx: SNIContext, address: str, retry: bool = True) -> WebSocketClientProtocol:
    address = f"ws://{address}" if "://" not in address else address
    snes_logger.info("Connecting to SNI at %s ..." % address)
    seen_problems: typing.Set[str] = set()
    while True:
        try:
            snes_socket = await websockets_connect(address, ping_timeout=None, ping_interval=None)
        except Exception as e:
            problem = "%s" % e
            # only tell the user about new problems, otherwise silently lay in wait for a working connection
            if problem not in seen_problems:
                seen_problems.add(problem)
                snes_logger.error(f"Error connecting to SNI ({problem})")

                if len(seen_problems) == 1:
                    # this is the first problem. Let's try launching SNI if it isn't already running
                    launch_sni()

            await asyncio.sleep(1)
        else:
            return snes_socket
        if not retry:
            break


class SNESRequest(typing.TypedDict):
    Opcode: str
    Space: str
    Operands: typing.List[str]
    # TODO: When Python 3.11 is the lowest version supported, `Operands` can use `typing.NotRequired` (pep-0655)
    # Then the `Operands` key doesn't need to be given for opcodes that don't use it.


async def get_snes_devices(ctx: SNIContext) -> typing.List[str]:
    socket = await _snes_connect(ctx, ctx.snes_address)  # establish new connection to poll
    DeviceList_Request: SNESRequest = {
        "Opcode": "DeviceList",
        "Space": "SNES",
        "Operands": []
    }
    await socket.send(dumps(DeviceList_Request))

    reply: typing.Dict[str, typing.Any] = loads(await socket.recv())
    devices: typing.List[str] = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else []

    if not devices:
        snes_logger.info('No SNES device found. Please connect a SNES device to SNI.')
        while not devices and not ctx.exit_event.is_set():
            await asyncio.sleep(0.1)
            await socket.send(dumps(DeviceList_Request))
            reply = loads(await socket.recv())
            devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else []
    if devices:
        await verify_snes_app(socket)
    await socket.close()
    return sorted(devices)


async def verify_snes_app(socket: WebSocketClientProtocol) -> None:
    AppVersion_Request = {
        "Opcode": "AppVersion",
    }
    await socket.send(dumps(AppVersion_Request))

    app: str = loads(await socket.recv())["Results"][0]
    if "SNI" not in app:
        snes_logger.warning(f"Warning: Did not find SNI as the endpoint, instead {app} was found.")


async def snes_connect(ctx: SNIContext, address: str, deviceIndex: int = -1) -> None:
    global _global_snes_reconnect_delay
    if ctx.snes_socket is not None and ctx.snes_state == SNESState.SNES_CONNECTED:
        if ctx.rom:
            snes_logger.error('Already connected to SNES, with rom loaded.')
        else:
            snes_logger.error('Already connected to SNI, likely awaiting a device.')
        return

    ctx.cancel_snes_autoreconnect()

    device = None
    recv_task = None
    ctx.snes_state = SNESState.SNES_CONNECTING
    socket = await _snes_connect(ctx, address)
    ctx.snes_socket = socket
    ctx.snes_state = SNESState.SNES_CONNECTED

    try:
        devices = await get_snes_devices(ctx)
        device_count = len(devices)

        if device_count == 1:
            device = devices[0]
        elif ctx.snes_reconnect_address:
            assert ctx.snes_attached_device
            if ctx.snes_attached_device[1] in devices:
                device = ctx.snes_attached_device[1]
            else:
                device = devices[ctx.snes_attached_device[0]]
        elif device_count > 1:
            if deviceIndex == -1:
                snes_logger.info(f"Found {device_count} SNES devices. "
                                 f"Connect to one with /snes <address> <device number>. For example /snes {address} 1")

                for idx, availableDevice in enumerate(devices):
                    snes_logger.info(str(idx + 1) + ": " + availableDevice)

            elif (deviceIndex < 0) or (deviceIndex - 1) > device_count:
                snes_logger.warning("SNES device number out of range")

            else:
                device = devices[deviceIndex - 1]

        if device is None:
            await snes_disconnect(ctx)
            return

        snes_logger.info("Attaching to " + device)

        Attach_Request: SNESRequest = {
            "Opcode": "Attach",
            "Space": "SNES",
            "Operands": [device]
        }
        await ctx.snes_socket.send(dumps(Attach_Request))
        ctx.snes_state = SNESState.SNES_ATTACHED
        ctx.snes_attached_device = (devices.index(device), device)
        ctx.snes_reconnect_address = address
        recv_task = asyncio.create_task(snes_recv_loop(ctx))

    except Exception as e:
        ctx.snes_state = SNESState.SNES_DISCONNECTED
        if task_alive(recv_task):
            if not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
        else:
            if ctx.snes_socket is not None:
                if not ctx.snes_socket.closed:
                    await ctx.snes_socket.close()
                ctx.snes_socket = None
        snes_logger.error(f"Error connecting to snes ({e}), retrying in {_global_snes_reconnect_delay} seconds")
        ctx.snes_autoreconnect_task = asyncio.create_task(snes_autoreconnect(ctx), name="snes auto-reconnect")
        _global_snes_reconnect_delay *= 2
    else:
        _global_snes_reconnect_delay = ctx.starting_reconnect_delay
        snes_logger.info(f"Attached to {device}")


async def snes_disconnect(ctx: SNIContext) -> None:
    if ctx.snes_socket:
        if not ctx.snes_socket.closed:
            await ctx.snes_socket.close()
        ctx.snes_socket = None


def task_alive(task: typing.Optional[asyncio.Task]) -> bool:
    if task:
        return not task.done()
    return False


async def snes_autoreconnect(ctx: SNIContext) -> None:
    await asyncio.sleep(_global_snes_reconnect_delay)
    if not ctx.snes_socket and not task_alive(ctx.snes_connect_task):
        address = ctx.snes_reconnect_address if ctx.snes_reconnect_address else ctx.snes_address
        ctx.snes_connect_task = asyncio.create_task(snes_connect(ctx, address), name="SNES Connect")


async def snes_recv_loop(ctx: SNIContext) -> None:
    try:
        if ctx.snes_socket is None:
            raise Exception("invalid context state - snes_socket not connected")
        async for msg in ctx.snes_socket:
            ctx.snes_recv_queue.put_nowait(typing.cast(bytes, msg))
        snes_logger.warning("Snes disconnected")
    except Exception as e:
        if not isinstance(e, WebSocketException):
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
            snes_logger.info(f"... automatically reconnecting to snes in {_global_snes_reconnect_delay} seconds")
            assert ctx.snes_autoreconnect_task is None
            ctx.snes_autoreconnect_task = asyncio.create_task(snes_autoreconnect(ctx), name="snes auto-reconnect")


async def snes_read(ctx: SNIContext, address: int, size: int) -> typing.Optional[bytes]:
    try:
        await ctx.snes_request_lock.acquire()

        if (
            ctx.snes_state != SNESState.SNES_ATTACHED or
            ctx.snes_socket is None or
            not ctx.snes_socket.open or
            ctx.snes_socket.closed
        ):
            return None

        GetAddress_Request: SNESRequest = {
            "Opcode": "GetAddress",
            "Space": "SNES",
            "Operands": [hex(address)[2:], hex(size)[2:]]
        }
        try:
            await ctx.snes_socket.send(dumps(GetAddress_Request))
        except ConnectionClosed:
            return None

        data: bytes = bytes()
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


async def snes_write(ctx: SNIContext, write_list: typing.List[typing.Tuple[int, bytes]]) -> bool:
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNESState.SNES_ATTACHED or ctx.snes_socket is None or \
                not ctx.snes_socket.open or ctx.snes_socket.closed:
            return False

        PutAddress_Request: SNESRequest = {"Opcode": "PutAddress", "Operands": [], 'Space': 'SNES'}
        try:
            for address, data in write_list:
                PutAddress_Request['Operands'] = [hex(address)[2:], hex(len(data))[2:]]
                if ctx.snes_socket is not None:
                    await ctx.snes_socket.send(dumps(PutAddress_Request))
                    await ctx.snes_socket.send(data)
                else:
                    snes_logger.warning(f"Could not send data to SNES: {data}")
        except ConnectionClosed:
            return False

        return True
    finally:
        ctx.snes_request_lock.release()


def snes_buffered_write(ctx: SNIContext, address: int, data: bytes) -> None:
    if ctx.snes_write_buffer and (ctx.snes_write_buffer[-1][0] + len(ctx.snes_write_buffer[-1][1])) == address:
        # append to existing write command, bundling them
        ctx.snes_write_buffer[-1] = (ctx.snes_write_buffer[-1][0], ctx.snes_write_buffer[-1][1] + data)
    else:
        ctx.snes_write_buffer.append((address, data))


async def snes_flush_writes(ctx: SNIContext) -> None:
    if not ctx.snes_write_buffer:
        return

    # swap buffers
    ctx.snes_write_buffer, writes = [], ctx.snes_write_buffer
    await snes_write(ctx, writes)


async def game_watcher(ctx: SNIContext) -> None:
    perf_counter = time.perf_counter()
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()

        if not ctx.rom or not ctx.client_handler:
            ctx.finished_game = False
            ctx.death_link_allow_survive = False

            from worlds.AutoSNIClient import AutoSNIClientRegister
            ctx.client_handler = await AutoSNIClientRegister.get_handler(ctx)

            if not ctx.client_handler:
                continue

            if not ctx.rom:
                continue

            if not ctx.prev_rom or ctx.prev_rom != ctx.rom:
                ctx.locations_checked = set()
                ctx.locations_scouted = set()
                ctx.locations_info = {}
            ctx.prev_rom = ctx.rom

            if ctx.awaiting_rom:
                await ctx.server_auth(False)
            elif ctx.server is None:
                snes_logger.warning("ROM detected but no active multiworld server connection. " +
                                    "Connect using command: /connect server:port")

        if not ctx.client_handler:
            continue

        try:
            rom_validated = await ctx.client_handler.validate_rom(ctx)
        except Exception as e:
            snes_logger.error(f"An error occurred, see logs for details: {e}")
            text_file_logger = logging.getLogger()
            text_file_logger.exception(e)
            rom_validated = False

        if not rom_validated or (ctx.auth and ctx.auth != ctx.rom):
            snes_logger.warning("ROM change detected, please reconnect to the multiworld server")
            await ctx.disconnect(allow_autoreconnect=True)
            ctx.client_handler = None
            ctx.rom = None
            ctx.command_processor(ctx).connect_to_snes()
            continue

        delay = 7 if ctx.slow_mode else 0
        if time.perf_counter() - perf_counter < delay:
            continue

        perf_counter = time.perf_counter()

        try:
            await ctx.client_handler.game_watcher(ctx)
        except Exception as e:
            snes_logger.error(f"An error occurred, see logs for details: {e}")
            text_file_logger = logging.getLogger()
            text_file_logger.exception(e)
            await snes_disconnect(ctx)


async def run_game(romfile: str) -> None:
    auto_start = typing.cast(typing.Union[bool, str],
                             Utils.get_settings()["sni_options"].get("snes_rom_start", True))
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif isinstance(auto_start, str) and os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def main() -> None:
    multiprocessing.freeze_support()
    parser = get_base_parser()
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a Archipelago Binary Patch file')
    parser.add_argument('--snes', default='localhost:23074', help='Address of the SNI server.')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    args = parser.parse_args()

    if args.diff_file:
        import Patch
        logging.info("Patch file was supplied. Creating sfc rom..")
        try:
            meta, romfile = Patch.create_rom_file(args.diff_file)
        except Exception as e:
            Utils.messagebox('Error', str(e), True)
            raise
        args.connect = meta["server"]
        logging.info(f"Wrote rom file to {romfile}")
        if args.diff_file.endswith(".apsoe"):
            import webbrowser
            async_start(run_game(romfile))
            await _snes_connect(SNIContext(args.snes, args.connect, args.password), args.snes, False)
            webbrowser.open(f"http://www.evermizer.com/apclient/#server={meta['server']}")
            logging.info("Starting Evermizer Client in your Browser...")
            import time
            time.sleep(3)
            sys.exit()
        elif args.diff_file.endswith(".aplttp"):
            from worlds.alttp.Client import get_alttp_settings
            adjustedromfile, adjusted = get_alttp_settings(romfile)
            async_start(run_game(adjustedromfile if adjusted else romfile))
        else:
            async_start(run_game(romfile))

    ctx = SNIContext(args.snes, args.connect, args.password)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    ctx.snes_connect_task = asyncio.create_task(snes_connect(ctx, ctx.snes_address), name="SNES Connect")
    watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

    await ctx.exit_event.wait()

    ctx.server_address = None
    ctx.snes_reconnect_address = None
    if ctx.snes_socket is not None and not ctx.snes_socket.closed:
        await ctx.snes_socket.close()
    await watcher_task
    await ctx.shutdown()


if __name__ == '__main__':
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
