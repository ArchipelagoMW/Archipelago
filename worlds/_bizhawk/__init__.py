"""
A module for interacting with BizHawk through `connector_bizhawk_generic.lua`.

Any mention of `domain` in this module refers to the names BizHawk gives to memory domains in its own lua api. They are
naively passed to BizHawk without validation or modification.
"""

import asyncio
import base64
import enum
import json
import typing


BIZHAWK_SOCKET_PORT = 43055


class ConnectionStatus(enum.IntEnum):
    NOT_CONNECTED = 1
    TENTATIVE = 2
    CONNECTED = 3


class NotConnectedError(Exception):
    """Raised when something tries to make a request to the connector script before a connection has been established"""
    pass


class RequestFailedError(Exception):
    """Raised when the connector script did not respond to a request"""
    pass


class ConnectorError(Exception):
    """Raised when the connector script encounters an error while processing a request"""
    pass


class SyncError(Exception):
    """Raised when the connector script responded with a mismatched response type"""
    pass


class BizHawkContext:
    streams: typing.Optional[typing.Tuple[asyncio.StreamReader, asyncio.StreamWriter]]
    connection_status: ConnectionStatus
    _lock: asyncio.Lock

    def __init__(self) -> None:
        self.streams = None
        self.connection_status = ConnectionStatus.NOT_CONNECTED
        self._lock = asyncio.Lock()

    async def _send_message(self, message: str):
        async with self._lock:
            if self.streams is None:
                raise NotConnectedError("You tried to send a request before a connection to BizHawk was made")

            try:
                reader, writer = self.streams
                writer.write(message.encode("utf-8") + b"\n")
                await asyncio.wait_for(writer.drain(), timeout=5)

                res = await asyncio.wait_for(reader.readline(), timeout=5)

                if res == b"":
                    writer.close()
                    self.streams = None
                    self.connection_status = ConnectionStatus.NOT_CONNECTED
                    raise RequestFailedError("Connection closed")

                if self.connection_status == ConnectionStatus.TENTATIVE:
                    self.connection_status = ConnectionStatus.CONNECTED

                return res.decode("utf-8")
            except asyncio.TimeoutError as exc:
                writer.close()
                self.streams = None
                self.connection_status = ConnectionStatus.NOT_CONNECTED
                raise RequestFailedError("Connection timed out") from exc
            except ConnectionResetError as exc:
                writer.close()
                self.streams = None
                self.connection_status = ConnectionStatus.NOT_CONNECTED
                raise RequestFailedError("Connection reset") from exc


async def connect(ctx: BizHawkContext) -> bool:
    """Attempts to establish a connection with the connector script. Returns True if successful."""
    try:
        ctx.streams = await asyncio.open_connection("localhost", BIZHAWK_SOCKET_PORT)
        ctx.connection_status = ConnectionStatus.TENTATIVE
        return True
    except (TimeoutError, ConnectionRefusedError):
        ctx.streams = None
        ctx.connection_status = ConnectionStatus.NOT_CONNECTED
        return False


def disconnect(ctx: BizHawkContext) -> None:
    """Closes the connection to the connector script."""
    if ctx.streams is not None:
        ctx.streams[1].close()
        ctx.streams = None
    ctx.connection_status = ConnectionStatus.NOT_CONNECTED


async def get_script_version(ctx: BizHawkContext) -> int:
    return int(await ctx._send_message("VERSION"))


async def send_requests(ctx: BizHawkContext, req_list: typing.List[typing.Dict[str, typing.Any]]) -> typing.List[typing.Dict[str, typing.Any]]:
    """Sends a list of requests to the BizHawk connector and returns their responses.

    It's likely you want to use the wrapper functions instead of this."""
    return json.loads(await ctx._send_message(json.dumps(req_list)))


async def ping(ctx: BizHawkContext) -> None:
    """Sends a PING request and receives a PONG response."""
    res = (await send_requests(ctx, [{"type": "PING"}]))[0]

    if res["type"] != "PONG":
        raise SyncError(f"Expected response of type PONG but got {res['type']}")


async def get_hash(ctx: BizHawkContext) -> str:
    """Gets the system name for the currently loaded ROM"""
    res = (await send_requests(ctx, [{"type": "HASH"}]))[0]

    if res["type"] != "HASH_RESPONSE":
        raise SyncError(f"Expected response of type HASH_RESPONSE but got {res['type']}")

    return res["value"]


async def get_system(ctx: BizHawkContext) -> str:
    """Gets the system name for the currently loaded ROM"""
    res = (await send_requests(ctx, [{"type": "SYSTEM"}]))[0]

    if res["type"] != "SYSTEM_RESPONSE":
        raise SyncError(f"Expected response of type SYSTEM_RESPONSE but got {res['type']}")

    return res["value"]


async def get_cores(ctx: BizHawkContext) -> typing.Dict[str, str]:
    """Gets the preferred cores for systems with multiple cores. Only systems with multiple available cores have
    entries."""
    res = (await send_requests(ctx, [{"type": "PREFERRED_CORES"}]))[0]

    if res["type"] != "PREFERRED_CORES_RESPONSE":
        raise SyncError(f"Expected response of type PREFERRED_CORES_RESPONSE but got {res['type']}")

    return res["value"]


async def lock(ctx: BizHawkContext) -> None:
    """Locks BizHawk in anticipation of receiving more requests this frame.

    Consider using guarded reads and writes instead of locks if possible.

    While locked, emulation will halt and the connector will block on incoming requests until an `UNLOCK` request is
    sent. Remember to unlock when you're done, or the emulator will appear to freeze.

    Sending multiple lock commands is the same as sending one."""
    res = (await send_requests(ctx, [{"type": "LOCK"}]))[0]

    if res["type"] != "LOCKED":
        raise SyncError(f"Expected response of type LOCKED but got {res['type']}")


async def unlock(ctx: BizHawkContext) -> None:
    """Unlocks BizHawk to allow it to resume emulation. See `lock` for more info.

    Sending multiple unlock commands is the same as sending one."""
    res = (await send_requests(ctx, [{"type": "UNLOCK"}]))[0]

    if res["type"] != "UNLOCKED":
        raise SyncError(f"Expected response of type UNLOCKED but got {res['type']}")


async def display_message(ctx: BizHawkContext, message: str) -> None:
    """Displays the provided message in BizHawk's message queue."""
    res = (await send_requests(ctx, [{"type": "DISPLAY_MESSAGE", "message": message}]))[0]

    if res["type"] != "DISPLAY_MESSAGE_RESPONSE":
        raise SyncError(f"Expected response of type DISPLAY_MESSAGE_RESPONSE but got {res['type']}")


async def set_message_interval(ctx: BizHawkContext, value: float) -> None:
    """Sets the minimum amount of time in seconds to wait between queued messages. The default value of 0 will allow one
    new message to display per frame."""
    res = (await send_requests(ctx, [{"type": "SET_MESSAGE_INTERVAL", "value": value}]))[0]

    if res["type"] != "SET_MESSAGE_INTERVAL_RESPONSE":
        raise SyncError(f"Expected response of type SET_MESSAGE_INTERVAL_RESPONSE but got {res['type']}")


async def guarded_read(ctx: BizHawkContext, read_list: typing.List[typing.Tuple[int, int, str]],
                       guard_list: typing.List[typing.Tuple[int, typing.Iterable[int], str]]) -> typing.Optional[typing.List[bytes]]:
    """Reads an array of bytes at 1 or more addresses if and only if every byte in guard_list matches its expected
    value.

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

    ret: typing.List[bytes] = []
    for item in res:
        if item["type"] == "GUARD_RESPONSE":
            if not item["value"]:
                return None
        else:
            if item["type"] != "READ_RESPONSE":
                raise SyncError(f"Expected response of type READ_RESPONSE or GUARD_RESPONSE but got {res['type']}")

            ret.append(base64.b64decode(item["value"]))

    return ret


async def read(ctx: BizHawkContext, read_list: typing.List[typing.Tuple[int, int, str]]) -> typing.List[bytes]:
    """Reads data at 1 or more addresses.

    Items in `read_list` should be organized `(address, size, domain)` where
    - `address` is the address of the first byte of data
    - `size` is the number of bytes to read
    - `domain` is the name of the region of memory the address corresponds to

    Returns a list of bytes in the order they were requested."""
    return await guarded_read(ctx, read_list, [])


async def guarded_write(ctx: BizHawkContext, write_list: typing.List[typing.Tuple[int, typing.Iterable[int], str]],
                        guard_list: typing.List[typing.Tuple[int, typing.Iterable[int], str]]) -> bool:
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
            if not item["value"]:
                return False
        else:
            if item["type"] != "WRITE_RESPONSE":
                raise SyncError(f"Expected response of type WRITE_RESPONSE or GUARD_RESPONSE but got {res['type']}")

    return True


async def write(ctx: BizHawkContext, write_list: typing.List[typing.Tuple[int, typing.Iterable[int], str]]) -> None:
    """Writes data to 1 or more addresses.

    Items in write_list should be organized `(address, value, domain)` where
    - `address` is the address of the first byte of data
    - `value` is a list of bytes to write, in order, starting at `address`
    - `domain` is the name of the region of memory the address corresponds to"""
    await guarded_write(ctx, write_list, [])
