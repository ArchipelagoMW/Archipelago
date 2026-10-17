"""Memory transports used by the TWW client. All game addresses are PPC addresses."""

import importlib
import math
import secrets
import socket
import struct
from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from types import ModuleType

GAME_ID_ADDRESS = 0x80000000
GAME_ID = b"GZLE99"
MEM1_END = 0x81800000
AP_BRIDGE_PORT = 55000
AP_BRIDGE_MAX_SIZE = 256
AP_BRIDGE_READ_ATTEMPTS = 3
AP_BRIDGE_WRITE_ATTEMPTS = 3


class ConsoleMemory(ABC):
    name: str

    @property
    def description(self) -> str:
        return self.name

    @abstractmethod
    def hook(self) -> None:
        pass

    @abstractmethod
    def un_hook(self) -> None:
        pass

    @abstractmethod
    def is_hooked(self) -> bool:
        pass

    @abstractmethod
    def read_bytes(self, address: int, length: int) -> bytes:
        pass

    @abstractmethod
    def write_bytes(self, address: int, data: bytes) -> None:
        pass

    def read_byte(self, address: int) -> int:
        return self.read_bytes(address, 1)[0]

    def read_word(self, address: int) -> int:
        return int.from_bytes(self.read_bytes(address, 4), "big")

    def write_byte(self, address: int, value: int) -> None:
        self.write_bytes(address, bytes([value]))


class DolphinMemory(ConsoleMemory):
    """Keep Dolphin's native operations and load its dependency only when selected."""

    name = "Dolphin"

    def __init__(self) -> None:
        self._engine: ModuleType | None = None

    @property
    def engine(self) -> ModuleType:
        if self._engine is None:
            self._engine = importlib.import_module("dolphin_memory_engine")
        return self._engine

    def hook(self) -> None:
        self.engine.hook()

    def un_hook(self) -> None:
        if self._engine is not None:
            self._engine.un_hook()

    def is_hooked(self) -> bool:
        return self._engine is not None and self._engine.is_hooked()

    def read_bytes(self, address: int, length: int) -> bytes:
        return self.engine.read_bytes(address, length)

    def read_byte(self, address: int) -> int:
        return self.engine.read_byte(address)

    def read_word(self, address: int) -> int:
        return self.engine.read_word(address)

    def write_bytes(self, address: int, data: bytes) -> None:
        self.engine.write_bytes(address, data)

    def write_byte(self, address: int, value: int) -> None:
        self.engine.write_byte(address, value)


class APBridgeError(RuntimeError):
    """A local validation, transport, probe, or protocol failure."""


class APBridgeTimeoutError(APBridgeError):
    """An exchange timed out; WRTX retries require a completed send."""

    def __init__(self, message: str, *, waiting_for_reply: bool) -> None:
        super().__init__(message)
        self.waiting_for_reply = waiting_for_reply


class APBridgeRemoteError(APBridgeError):
    """A fully validated ERR! reply rejecting the request."""

    def __init__(self, code: int, address: int, length: int) -> None:
        self.code = code
        reasons = {
            1: "invalid length",
            2: "invalid MEM1 address/range",
            3: "reserved field nonzero",
            4: "WRITE payload size mismatch",
            5: "invalid transaction ID",
            6: "transaction ID conflict",
        }
        super().__init__(f"Wii AP Bridge ERR! {code} ({reasons[code]}) at 0x{address:08X}, length {length}")


class APBridgeWriteUncertainError(APBridgeError):
    """A write's result is unknown. Replaying it as a new transaction may duplicate an item."""


class WiiMemory(ConsoleMemory):
    """One connected UDP socket and one outstanding request at a time.

    Calls are synchronous and must be serialized by the client's event loop. The
    READ has no transaction IDs, so timeouts retry on fresh sockets only. WRTX
    reply timeouts also use fresh sockets, retaining the same transaction ID.
    Other failures close the socket without retrying. Legacy WRIT is never sent.
    """

    name = "Wii AP Bridge"

    def __init__(self, host: str, port: int = AP_BRIDGE_PORT, timeout: float = 0.5) -> None:
        self.host = str(IPv4Address(host))
        if not 1 <= port <= 65535:
            raise ValueError("Wii AP Bridge port must be between 1 and 65535")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("Wii AP Bridge timeout must be finite and positive")
        self.port = port
        self.timeout = timeout
        self._socket: socket.socket | None = None
        self._connected = False

    @property
    def description(self) -> str:
        return f"{self.name} ({self.host}:{self.port})"

    def hook(self) -> None:
        self.un_hook()
        try:
            self._open_socket()
            if self._exchange(b"HELLO") != b"NIN-AP":
                raise APBridgeError("Wii AP Bridge expected exactly NIN-AP in reply to HELLO")
            if self.read_bytes(GAME_ID_ADDRESS, len(GAME_ID)) != GAME_ID:
                raise APBridgeError("Wii AP Bridge requires a randomized The Wind Waker game (GZLE99)")
            self._connected = True
        except (OSError, APBridgeError) as error:
            self.un_hook()
            if isinstance(error, APBridgeError):
                raise
            raise APBridgeError(f"Could not connect to {self.description}: {error}") from error

    def _open_socket(self, excluded_ports: set[int] | None = None) -> None:
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.settimeout(self.timeout)
            self._socket.connect((self.host, self.port))
        except OSError as error:
            raise APBridgeError(f"Could not connect to {self.description}: {error}") from error
        # A new socket must not accidentally reuse a timed-out request's source
        # port, where a late reply could still arrive from the network.
        if excluded_ports and self._socket.getsockname()[1] in excluded_ports:
            raise APBridgeError("Wii AP Bridge could not obtain a fresh UDP source port for retry")

    def un_hook(self) -> None:
        self._connected = False
        if self._socket is not None:
            self._socket.close()
            self._socket = None

    def is_hooked(self) -> bool:
        return self._connected

    @staticmethod
    def _validate_range(address: int, length: int) -> None:
        if not isinstance(length, int) or not 1 <= length <= AP_BRIDGE_MAX_SIZE:
            raise APBridgeError("Wii AP Bridge operations require 1..256 bytes")
        if not isinstance(address, int) or not GAME_ID_ADDRESS <= address < address + length <= MEM1_END:
            raise APBridgeError("Wii AP Bridge operation must lie entirely within MEM1 (0x80000000..0x817FFFFF)")

    def _exchange(self, request: bytes) -> bytes:
        if self._socket is None:
            raise APBridgeError("Wii AP Bridge is disconnected")
        waiting_for_reply = False
        try:
            if self._socket.send(request) != len(request):
                raise APBridgeError("Wii AP Bridge could not send the complete datagram")
            waiting_for_reply = True
            # Read the entire datagram so extra bytes cannot be silently truncated.
            return self._socket.recv(65535)
        except TimeoutError as error:
            raise APBridgeTimeoutError(
                f"{self.description} timed out during {request[:4]!r} exchange",
                waiting_for_reply=waiting_for_reply,
            ) from error
        except OSError as error:
            raise APBridgeError(f"{self.description} UDP exchange failed: {error}") from error

    @staticmethod
    def _validate_reply(reply: bytes, magic: bytes, address: int, length: int, size: int) -> None:
        if len(reply) < 12:
            raise APBridgeError("Wii AP Bridge reply is shorter than its 12-byte header")
        actual_magic, actual_address, actual_length, reserved = struct.unpack(">4sIHH", reply[:12])
        if actual_magic not in (magic, b"ERR!"):
            raise APBridgeError(f"Wii AP Bridge unexpected reply magic {actual_magic!r}, expected {magic!r}")
        expected_size = 12 if actual_magic == b"ERR!" else size
        if len(reply) != expected_size:
            raise APBridgeError(f"Wii AP Bridge reply size {len(reply)}, expected {expected_size}")
        if actual_address != address:
            raise APBridgeError(f"Wii AP Bridge echoed address 0x{actual_address:08X}, expected 0x{address:08X}")
        if actual_length != length:
            raise APBridgeError(f"Wii AP Bridge echoed length {actual_length}, expected {length}")
        if actual_magic == b"ERR!":
            if reply[11] != 0:
                raise APBridgeError("Wii AP Bridge ERR! reserved byte is nonzero")
            if reply[10] not in (1, 2, 3, 4):
                raise APBridgeError(f"Wii AP Bridge unknown error code {reply[10]}")
            raise APBridgeRemoteError(reply[10], address, length)
        if reserved != 0:
            raise APBridgeError("Wii AP Bridge reserved response bytes are nonzero")

    def read_bytes(self, address: int, length: int) -> bytes:
        self._validate_range(address, length)
        request = struct.pack(">4sIHH", b"READ", address, length, 0)
        was_connected = self._connected
        excluded_ports: set[int] = set()
        attempt = 1
        try:
            while True:
                try:
                    reply = self._exchange(request)
                except APBridgeTimeoutError as error:
                    assert self._socket is not None
                    excluded_ports.add(self._socket.getsockname()[1])
                    self.un_hook()
                    if attempt == AP_BRIDGE_READ_ATTEMPTS:
                        raise APBridgeError(
                            f"{self.description} READ at 0x{address:08X}, length {length} "
                            f"timed out after {attempt} attempts"
                        ) from error
                    # AP Bridge is stateless: resend this READ directly, without
                    # HELLO or any writes, and retain the new socket on success.
                    self._open_socket(excluded_ports)
                    attempt += 1
                    continue
                self._validate_reply(reply, b"DATA", address, length, 12 + length)
                self._connected = was_connected
                return reply[12:]
        except APBridgeError:
            self.un_hook()
            raise

    def write_bytes(self, address: int, data: bytes) -> None:
        self._validate_range(address, len(data))
        if self._socket is None:
            raise APBridgeError("Wii AP Bridge is disconnected")
        txid = secrets.randbits(64)
        while txid == 0:
            txid = secrets.randbits(64)
        # Pack once: every retry is the same logical write, even if the first
        # request already executed and only its acknowledgment was lost.
        request = struct.pack(">4sIHHQ", b"WRTX", address, len(data), 0, txid) + data
        was_connected = self._connected
        excluded_ports: set[int] = set()
        attempt = 1
        try:
            while True:
                try:
                    reply = self._exchange(request)
                except APBridgeTimeoutError as error:
                    if not error.waiting_for_reply:
                        raise
                    assert self._socket is not None
                    excluded_ports.add(self._socket.getsockname()[1])
                    self.un_hook()
                    if attempt == AP_BRIDGE_WRITE_ATTEMPTS:
                        raise APBridgeError(
                            f"{self.description} WRTX timed out after {attempt} attempts"
                        ) from error
                    # The bridge's recent transaction cache is global across
                    # peers. Do not probe or generate another txid here.
                    self._open_socket(excluded_ports)
                    attempt += 1
                    continue
                self._validate_write_reply(reply, address, len(data), txid)
                self._connected = was_connected
                return
        except APBridgeRemoteError:
            self.un_hook()
            raise
        except APBridgeError as error:
            self.un_hook()
            raise APBridgeWriteUncertainError(
                f"{error}. WRTX at 0x{address:08X}, transaction 0x{txid:016X}, may have succeeded; "
                "no further retries will be made."
            ) from error

    @staticmethod
    def _validate_write_reply(reply: bytes, address: int, length: int, txid: int) -> None:
        if len(reply) != 20:
            raise APBridgeError(f"Wii AP Bridge WRTX reply size {len(reply)}, expected 20")
        magic, actual_address, actual_length, status, reserved, actual_txid = struct.unpack(">4sIHBBQ", reply)
        if magic not in (b"WROK", b"ERR!"):
            raise APBridgeError(f"Wii AP Bridge unexpected WRTX reply magic {magic!r}")
        if actual_address != address:
            raise APBridgeError(f"Wii AP Bridge echoed address 0x{actual_address:08X}, expected 0x{address:08X}")
        if actual_length != length:
            raise APBridgeError(f"Wii AP Bridge echoed length {actual_length}, expected {length}")
        if reserved != 0:
            raise APBridgeError("Wii AP Bridge WRTX reserved response byte is nonzero")
        if actual_txid != txid:
            raise APBridgeError(
                f"Wii AP Bridge echoed transaction ID 0x{actual_txid:016X}, expected 0x{txid:016X}"
            )
        if magic == b"ERR!":
            if status not in (1, 2, 3, 4, 5, 6):
                raise APBridgeError(f"Wii AP Bridge unknown WRTX error code {status}")
            raise APBridgeRemoteError(status, address, length)
        if status != 0:
            raise APBridgeError("Wii AP Bridge WROK status byte is nonzero")
