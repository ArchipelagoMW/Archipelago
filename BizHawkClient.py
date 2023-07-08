from __future__ import annotations

import asyncio
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
    watcher_timeout: float = 0.5

    def __init__(self, server_address: Optional[str], password: Optional[str]):
        super().__init__(server_address, password)
        self.client_handler = None
        self.bizhawk_streams = None
        self.bizhawk_connection_status = BizHawkConnectionStatus.NOT_CONNECTED

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
    pass


class NotConnectedError(Exception):
    pass


class BizHawkConnectorError(Exception):
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
    return res["value"]


async def bizhawk_lock(ctx: BizHawkClientContext) -> bool:
    """Locks BizHawk in anticipation of receiving more requests this frame.

    While locked, emulation will halt and the connector will block on incoming
    requests until an UNLOCK request is sent. This is useful if you must guarantee
    multiple commands run during the same frame and the input of one command is
    dependent on the output of a previous command. For example, reading the value of
    a pointer and then reading the value at the address the pointer points to.

    Sending multiple lock commands is the same as sending one.

    Remember to unlock when you're done, or the emulator will appear to freeze.

    Returns True if the connector confirmed the command, False otherwise."""
    res = (await send_requests(ctx, [{"type": "LOCK"}]))[0]
    if res["type"] == "LOCKED":
        return True

    return False


async def bizhawk_unlock(ctx: BizHawkClientContext) -> bool:
    """Unlocks BizHawk to allow it to resume emulation. See bizhawk_lock for more info.

    Sending multiple unlock commands is the same as sending one.

    Returns True if the connector confirmed the command, False otherwise."""
    res = (await send_requests(ctx, [{"type": "UNLOCK"}]))[0]
    if res["type"] == "UNLOCKED":
        return True

    return False


async def bizhawk_display_message(ctx: BizHawkClientContext, message: str) -> bool:
    """Displays the provided message in BizHawk's message queue."""
    res = (await send_requests(ctx, [{"type": "DISPLAY_MESSAGE", "message": message}]))[0]
    if res["type"] == "DISPLAY_MESSAGE_RESPONSE":
        return True

    return False


async def bizhawk_set_message_interval(ctx: BizHawkClientContext, value: float) -> bool:
    """Sets the minimum amount of time in seconds to wait between queued messages.
    The default value of 0 will allow one new message to display per frame."""
    res = (await send_requests(ctx, [{"type": "DISPLAY_MESSAGE", "value": value}]))[0]
    if res["type"] == "DISPLAY_MESSAGE_RESPONSE":
        return True

    return False


async def bizhawk_read_multiple(ctx: BizHawkClientContext, read_list: List[Tuple[int, int, str]]) -> List[bytearray]:
    """Reads an array of bytes at multiple addresses.
    
    Items in read_list should be organized (address, size, domain) where
        address: The address of the first byte of data
        size: The number of bytes to read
        domain: The name of the region of memory the address corresponds to

    Returns a list of bytearrays in the order they were requested"""
    res = await send_requests(ctx, [
        {
            "type": "READ",
            "address": address,
            "size": size,
            "domain": domain
        }
        for address, size, domain in read_list
    ])

    return [bytearray(item["value"]) for item in res]


async def bizhawk_read(ctx: BizHawkClientContext, address: int, size: int, domain: str) -> bytearray:
    """Reads an array of bytes at the specified address.

    address: The address of the first byte of data
    size: The number of bytes to read
    domain: The name of the region of memory the address corresponds to

    Returns a bytearray corresponding to the read data"""
    return (await bizhawk_read_multiple(ctx, [[address, size, domain]]))[0]


async def bizhawk_write_multiple(ctx: BizHawkClientContext, write_list: List[Tuple[int, Iterable[int], str]]) -> bool:
    """Writes bytes at multiple addresses.
    
    Items in write_list should be organized (address, value, domain) where
        address: The address of the first byte of data
        value: A list of bytes to write
        domain: The name of the region of memory the address corresponds to

    Returns True if the connector confirmed the writes, False otherwise"""
    res = await send_requests(ctx, [
        {
            "type": "WRITE",
            "address": address,
            "value": list(value),
            "domain": domain
        }
        for address, value, domain in write_list
    ])

    return all(item["type"] == "WRITE_RESPONSE" for item in res)


async def bizhawk_write(ctx: BizHawkClientContext, address: int, value: Iterable[int], domain: str) -> bool:
    """Writes bytes at the specified address.
    
    address: The address of the first byte of data
    value: A list of bytes to write
    domain: The name of the region of memory the address corresponds to

    Returns True if the connector confirmed the write, False otherwise"""
    return await bizhawk_write_multiple(ctx, [[address, value, domain]])


async def _game_watcher(ctx: BizHawkClientContext):
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), ctx.watcher_timeout)
        except asyncio.TimeoutError:
            pass

        ctx.watcher_event.clear()

        if ctx.bizhawk_streams is None:
            logger.info("Trying to connect to BizHawk...")
            if not await _try_connect(ctx):
                continue

        try:
            await send_requests(ctx, [{"type": "PING"}])

            if ctx.client_handler is None:
                from worlds.AutoBizHawkClient import AutoBizHawkClientRegister

                system = (await send_requests(ctx, [{"type": "SYSTEM"}]))[0]["value"]
                ctx.client_handler = await AutoBizHawkClientRegister.get_handler(ctx, system)

                if ctx.client_handler is None:
                    raise NotImplementedError("No handler was found for this game")
                else:
                    logger.info(f"Running handler for {ctx.client_handler.game}")
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
