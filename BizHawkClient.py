from __future__ import annotations

import asyncio
import base64
from enum import IntEnum
import json
import traceback
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional, Tuple, List

from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, server_loop, logger, gui_enabled
import Patch
import Utils
if TYPE_CHECKING:
    from worlds.AutoBizHawkClient import BizHawkClient


BIZHAWK_SOCKET_PORT = 43055
EXPECTED_SCRIPT_VERSION = (1, 0, 0)


class BizHawkConnectionStatus(IntEnum):
    NOT_CONNECTED = 1
    TENTATIVE = 2
    CONNECTED = 3


class BizHawkClientCommandProcessor(ClientCommandProcessor):
    def _cmd_bh(self):
        """Shows the current status of the client's connection to BizHawk"""
        if isinstance(self.ctx, BizHawkClientContext):
            if self.ctx.bizhawk_connection_status == BizHawkConnectionStatus.NOT_CONNECTED:
                logger.info("BizHawk Connection Status: Not Connected")
            elif self.ctx.bizhawk_connection_status == BizHawkConnectionStatus.TENTATIVE:
                logger.info("BizHawk Connection Status: Tentatively Connected")
            elif self.ctx.bizhawk_connection_status == BizHawkConnectionStatus.CONNECTED:
                logger.info("BizHawk Connection Status: Connected")


class BizHawkClientContext(CommonContext):
    command_processor = BizHawkClientCommandProcessor
    client_handler: Optional[BizHawkClient]
    bizhawk_streams: Optional[Tuple[asyncio.StreamReader, asyncio.StreamWriter]]
    bizhawk_connection_status: BizHawkConnectionStatus
    slot_data: Optional[Dict[str, Any]] = None
    rom_hash: Optional[str] = None

    watcher_timeout: float
    """The maximum amount of time the game watcher loop will wait for an update from the server before executing"""

    def __init__(self, server_address: Optional[str], password: Optional[str]):
        super().__init__(server_address, password)
        self.client_handler = None
        self.bizhawk_streams = None
        self.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED
        self.watcher_timeout = 0.5

    def run_gui(self):
        from kvui import GameManager

        class BizHawkManager(GameManager):
            base_title = "Archipelago BizHawk Client"

        self.ui = BizHawkManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd, args):
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None)

        if self.client_handler is not None:
            self.client_handler.on_package(self, cmd, args)


async def _try_connect(ctx: BizHawkClientContext):
    try:
        ctx.bizhawk_streams = await asyncio.open_connection("localhost", BIZHAWK_SOCKET_PORT)
        ctx.bizhawk_connection_status = BizHawkConnectionStatus.TENTATIVE
        return True
    except TimeoutError:
        ctx.bizhawk_streams = None
        ctx.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED
        return False
    except ConnectionRefusedError:
        ctx.bizhawk_streams = None
        ctx.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED
        return False
    except Exception as e:
        logger.error(e)
        ctx.bizhawk_streams = None
        ctx.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED
        return False


class RequestFailedError(Exception):
    """Raised when the connector script did not respond to a request"""
    pass


class NotConnectedError(Exception):
    """Raised when something tries to make a request to the connector script before a connection has been established"""
    pass


class BizHawkConnectorError(Exception):
    """Raised when the connector script encounters an error while processing a request"""
    pass


class BizHawkSyncError(Exception):
    """Raised when the connector script responded with a mismatched response type"""
    pass


async def send_requests(ctx: BizHawkClientContext, req_list: List[Dict[str, Any]]):
    """Sends a list of requests to the BizHawk connector and returns their responses.

    It's likely you want to use the wrapper functions instead of this."""
    if ctx.bizhawk_streams is None:
        raise NotConnectedError("You tried to send a request before a connection to BizHawk was made")

    try:
        reader, writer = ctx.bizhawk_streams
        writer.write(json.dumps(req_list).encode("utf-8") + b"\n")
        await asyncio.wait_for(writer.drain(), timeout=5)

        res = await asyncio.wait_for(reader.readline(), timeout=5)

        if res == b"":
            logger.info("Connection to BizHawk closed")
            writer.close()
            ctx.client_handler = None
            ctx.bizhawk_streams = None
            ctx.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED
            raise RequestFailedError("Connection closed")

        if ctx.bizhawk_connection_status == BizHawkConnectionStatus.TENTATIVE:
            ctx.bizhawk_connection_status = BizHawkConnectionStatus.CONNECTED
            logger.info("Connected to BizHawk")

        ret = json.loads(res.decode("utf-8"))
        for response in ret:
            if response["type"] == "ERROR":
                raise BizHawkConnectorError(response["err"])

        return ret
    except asyncio.TimeoutError:
        logger.info("Connection to BizHawk timed out")
        writer.close()
        ctx.client_handler = None
        ctx.bizhawk_streams = None
        ctx.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED
    except ConnectionResetError:
        logger.info("Connection to BizHawk reset")
        writer.close()
        ctx.client_handler = None
        ctx.bizhawk_streams = None
        ctx.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED

    raise RequestFailedError("Failed to get a response")


async def bizhawk_get_system(ctx: BizHawkClientContext) -> str:
    """Gets the system name for the currently loaded ROM"""
    res = (await send_requests(ctx, [{"type": "SYSTEM"}]))[0]

    if res["type"] != "SYSTEM_RESPONSE":
        raise BizHawkSyncError()

    return res["value"]


async def bizhawk_get_cores(ctx: BizHawkClientContext) -> Dict[str, str]:
    """Gets the preferred cores for systems with multiple cores. Only systems with multiple available cores have
    entries."""
    res = (await send_requests(ctx, [{"type": "PREFERRED_CORES"}]))[0]

    if res["type"] != "PREFERRED_CORES_RESPONSE":
        raise BizHawkSyncError()

    return res["value"]


async def bizhawk_lock(ctx: BizHawkClientContext) -> None:
    """Locks BizHawk in anticipation of receiving more requests this frame.

    Consider using guarded reads and writes instead of locks if possible.

    While locked, emulation will halt and the connector will block on incoming requests until an `UNLOCK` request is
    sent. Remember to unlock when you're done, or the emulator will appear to freeze.

    Sending multiple lock commands is the same as sending one."""
    res = (await send_requests(ctx, [{"type": "LOCK"}]))[0]

    if res["type"] != "LOCKED":
        raise BizHawkSyncError()


async def bizhawk_unlock(ctx: BizHawkClientContext) -> None:
    """Unlocks BizHawk to allow it to resume emulation. See `bizhawk_lock` for more info.

    Sending multiple unlock commands is the same as sending one."""
    res = (await send_requests(ctx, [{"type": "UNLOCK"}]))[0]

    if res["type"] != "UNLOCKED":
        raise BizHawkSyncError()


async def bizhawk_display_message(ctx: BizHawkClientContext, message: str) -> None:
    """Displays the provided message in BizHawk's message queue."""
    res = (await send_requests(ctx, [{"type": "DISPLAY_MESSAGE", "message": message}]))[0]

    if res["type"] != "DISPLAY_MESSAGE_RESPONSE":
        raise BizHawkSyncError()


async def bizhawk_set_message_interval(ctx: BizHawkClientContext, value: float) -> None:
    """Sets the minimum amount of time in seconds to wait between queued messages. The default value of 0 will allow one
    new message to display per frame."""
    res = (await send_requests(ctx, [{"type": "SET_MESSAGE_INTERVAL", "value": value}]))[0]

    if res["type"] != "SET_MESSAGE_INTERVAL_RESPONSE":
        raise BizHawkSyncError()


async def bizhawk_guarded_read(ctx: BizHawkClientContext, read_list: List[Tuple[int, int, str]],
                               guard_list: List[Tuple[int, Iterable[int], str]]) -> Optional[List[bytes]]:
    """Reads an array of bytes at 1 or more addresses if and only if every byte in guard_list matches its expected value.

    Items in read_list should be organized (address, size, domain) where
    - `address` is the address of the first byte of data
    - `size` is the number of bytes to read
    - `domain` is the name of the region of memory the address corresponds to

    Items in `guard_list` should be organized `(address, expected_data, domain)` where
    - `address` is the address of the first byte of data
    - `expected_data` is the bytes that the data starting at this address is expected to match
    - `domain` is the name of the region of memory the address corresponds to

    Returns None if any item in guard_list failed to validate. Otherwise returns a list of bytes in the order they
    were requested."""
    res = await send_requests(ctx, [{
        "type": "GUARD",
        "address": address,
        "expected_data": base64.b64encode(bytes(expected_data)).decode("ascii"),
        "domain": domain
    } for address, expected_data, domain in guard_list] + [{
        "type": "READ",
        "address": address,
        "size": size,
        "domain": domain
    } for address, size, domain in read_list])

    ret: List[bytes] = []
    for item in res:
        if item["type"] == "GUARD_RESPONSE":
            if item["value"] == False:
                return None
        else:
            if not item["type"] == "READ_RESPONSE":
                raise BizHawkSyncError()

            ret.append(base64.b64decode(item["value"]))

    return ret


async def bizhawk_read(ctx: BizHawkClientContext, read_list: List[Tuple[int, int, str]]) -> List[bytes]:
    """Reads data at 1 or more addresses.

    Items in `read_list` should be organized `(address, size, domain)` where
    - `address` is the address of the first byte of data
    - `size` is the number of bytes to read
    - `domain` is the name of the region of memory the address corresponds to

    Returns a list of bytes in the order they were requested."""
    return await bizhawk_guarded_read(ctx, read_list, [])


async def bizhawk_guarded_write(ctx: BizHawkClientContext, write_list: List[Tuple[int, Iterable[int], str]],
                                guard_list: List[Tuple[int, Iterable[int], str]]) -> bool:
    """Writes data to 1 or more addresses if and only if every byte in guard_list matches its expected value.

    Items in `write_list` should be organized `(address, value, domain)` where
    - `address` is the address of the first byte of data
    - `value` is a list of bytes to write, in order, starting at `address`
    - `domain` is the name of the region of memory the address corresponds to

    Items in `guard_list` should be organized `(address, expected_data, domain)` where
    - `address` is the address of the first byte of data
    - `expected_data` is the bytes that the data starting at this address is expected to match
    - `domain` is the name of the region of memory the address corresponds to

    Returns False if any item in guard_list failed to validate. Otherwise returns True."""
    res = await send_requests(ctx, [{
        "type": "GUARD",
        "address": address,
        "expected_data": base64.b64encode(bytes(expected_data)).decode("ascii"),
        "domain": domain
    } for address, expected_data, domain in guard_list] + [{
        "type": "WRITE",
        "address": address,
        "value": base64.b64encode(bytes(value)).decode("ascii"),
        "domain": domain
    } for address, value, domain in write_list])

    for item in res:
        if item["type"] == "GUARD_RESPONSE":
            if item["value"] == False:
                return False
        else:
            if not item["type"] == "WRITE_RESPONSE":
                raise BizHawkSyncError()

    return True


async def bizhawk_write(ctx: BizHawkClientContext, write_list: List[Tuple[int, Iterable[int], str]]) -> None:
    """Writes data to 1 or more addresses.

    Items in write_list should be organized `(address, value, domain)` where
    - `address` is the address of the first byte of data
    - `value` is a list of bytes to write, in order, starting at `address`
    - `domain` is the name of the region of memory the address corresponds to"""
    await bizhawk_guarded_write(ctx, write_list, [])


async def _game_watcher(ctx: BizHawkClientContext):
    showed_connecting_message = False
    showed_no_handler_message = False

    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), ctx.watcher_timeout)
        except asyncio.TimeoutError:
            pass

        ctx.watcher_event.clear()

        if ctx.bizhawk_streams is None:
            if not showed_connecting_message:
                logger.info("Waiting to connect to BizHawk...")
                showed_connecting_message = True

            if not await _try_connect(ctx):
                continue

            script_version = (await send_requests(ctx, [{"type": "SCRIPT_VERSION"}]))[0]["value"]

            if script_version[0] != EXPECTED_SCRIPT_VERSION[0] or script_version[1] < EXPECTED_SCRIPT_VERSION[1]:
                script_version_str = f"v{script_version[0]}.{script_version[1]}.{script_version[2]}"
                expected_script_version_str = f"v{EXPECTED_SCRIPT_VERSION[0]}.{EXPECTED_SCRIPT_VERSION[1]}.{EXPECTED_SCRIPT_VERSION[2]}"
                logger.info(f"Connector script is incompatible. Expected version {expected_script_version_str} but got {script_version_str}. Disconnecting.")

                ctx.bizhawk_streams[1].close()
                ctx.bizhawk_streams = None
                ctx.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED

                continue

        showed_connecting_message = False
        try:
            await send_requests(ctx, [{"type": "PING"}])

            if ctx.client_handler is None:
                from worlds.AutoBizHawkClient import AutoBizHawkClientRegister

                system = (await send_requests(ctx, [{"type": "SYSTEM"}]))[0]["value"]
                ctx.client_handler = await AutoBizHawkClientRegister.get_handler(ctx, system)

                if ctx.client_handler is None:
                    if not showed_no_handler_message:
                        logger.info("No handler was found for this game")
                        showed_no_handler_message = True
                    continue
                else:
                    showed_no_handler_message = False
                    logger.info(f"Running handler for {ctx.client_handler.game}")

                rom_hash = (await send_requests(ctx, [{"type": "HASH"}]))[0]["value"]
                if ctx.rom_hash is not None and ctx.rom_hash != rom_hash:
                    if ctx.server is not None:
                        logger.info(f"ROM changed. Disconnecting from server.")
                        await ctx.disconnect(True)

                    ctx.auth = None
                    ctx.username = None

                ctx.rom_hash = rom_hash
        except RequestFailedError:
            continue

        await ctx.client_handler.game_watcher(ctx)


async def _run_game(rom: str):
    import webbrowser
    webbrowser.open(rom)


async def _patch_and_run_game(patch_file: str):
    metadata, output_file = Patch.create_rom_file(patch_file)
    Utils.async_start(_run_game(output_file))


async def _main():
    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an Archipelago patch file")
    args = parser.parse_args()

    ctx = BizHawkClientContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    if args.patch_file is not None:
        Utils.async_start(_patch_and_run_game(args.patch_file))

    watcher_task = asyncio.create_task(_game_watcher(ctx), name="GameWatcher")

    try:
        await watcher_task
    except Exception as e:
        logger.error("".join(traceback.format_exception(e)))

    await ctx.exit_event.wait()
    await ctx.shutdown()


if __name__ == "__main__":
    import colorama
    colorama.init()
    asyncio.run(_main())
    colorama.deinit()
