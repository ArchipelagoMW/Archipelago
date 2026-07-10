"""
The PINE API.
This is the client side implementation of the PINE protocol.
It allows for a three-way communication between the emulated game, the emulator and an external
tool, using the external tool as a relay for all communication. It is a socket based IPC that
is _very_ fast.

If you want to draw comparisons you can think of this as an equivalent of the BizHawk LUA API,
although with the logic out of the core and in an external tool. While BizHawk would run a lua
script at each frame in the core of the emulator we opt instead to keep the entire logic out of
the emulator to make it more easily extensible, more portable, require less code and be more
performant.
"""
import os
import struct
import socket
from enum import IntEnum
from platform import system


class Pine:
    """ Exposes PS2 memory within a running instance of the PCSX2 emulator using the Pine IPC Protocol. """

    """ Maximum memory used by an IPC message request. Equivalent to 50,000 Write64 requests. """
    MAX_IPC_SIZE: int = 650000

    """ Maximum memory used by an IPC message reply. Equivalent to 50,000 Read64 replies. """
    MAX_IPC_RETURN_SIZE: int = 450000

    """ Maximum number of commands sent in a batch message. """
    MAX_BATCH_REPLY_COUNT: int = 50000

    class IPCResult(IntEnum):
        """ IPC result codes. A list of possible result codes the IPC can send back. Each one of them is what we call an
        "opcode" or "tag" and is the first byte sent by the IPC to differentiate between results.
        """
        IPC_OK = 0,  # IPC command successfully completed.
        IPC_FAIL = 0xFF  # IPC command failed to complete.

    class IPCCommand(IntEnum):
        READ8 = 0,
        READ16 = 1,
        READ32 = 2,
        READ64 = 3,
        WRITE8 = 4,
        WRITE16 = 5,
        WRITE32 = 6,
        WRITE64 = 7,
        VERSION = 8,
        SAVE_STATE = 9,
        LOAD_STATE = 0xA,
        TITLE = 0xB,
        ID = 0xC,
        UUID = 0xD,
        GAME_VERSION = 0xE,
        STATUS = 0xF,
        UNIMPLEMENTED = 0xFF,

    class DataSize(IntEnum):
        INT8 = 1,
        INT16 = 2,
        INT32 = 4,
        INT64 = 8,

    class EmuStatus(IntEnum):
        RUNNING = 0,
        PAUSED = 1,
        SHUTDOWN = 2,

    class ConnectionError(Exception):
        pass

    class DuplicateConnectionError(Exception):
        pass

    def __init__(self, slot: int = 28011):
        if not 0 < slot <= 65536:
            raise ValueError("Provided slot number is outside valid range")
        self._slot: int = slot
        self._sock: socket.socket = socket.socket()
        self._sock_state: bool = False
        # self._init_socket()

    def is_wsl(self) -> bool:
        if system() != "Linux":
            return False
        try:
            with open("/proc/sys/kernel/osrelease", "r") as f:
                return "microsoft" in f.read().lower()
        except Exception:
            return False

    def _init_socket(self) -> bool:
        socket_file_name = "pcsx2.sock" if self._slot == 28011 else f"pcsx2.sock.{self._slot}"
        if system() == "Windows" or self.is_wsl():
            socket_family = socket.AF_INET
            socket_path = ("127.0.0.1", self._slot)
        elif system() == "Linux":
            socket_family = socket.AF_UNIX
            base_path = os.environ.get("XDG_RUNTIME_DIR", "/tmp")

            # Write Permissions are required to connect to Unix Sockets in Linux
            if os.access(os.path.join(base_path, socket_file_name), os.W_OK):
               socket_path = os.path.join(base_path, socket_file_name)
            else:
                # Find the Socket in the Flatpak runtime otherwise
                socket_path = os.path.join(base_path, ".flatpak/net.pcsx2.PCSX2/xdg-run", socket_file_name)
        elif system() == "Darwin":
            socket_family = socket.AF_UNIX
            socket_path = os.path.join(os.environ.get("TMPDIR", "/tmp"), socket_file_name)
        else:
            socket_family = socket.AF_UNIX
            # Other Unix systems may use the XDG spec, so XDG_RUN should also be checked for
            socket_path = os.path.join(os.environ.get("XDG_RUNTIME_DIR", "/tmp"), socket_file_name)

        try:
            self._sock = socket.socket(socket_family, socket.SOCK_STREAM)
            self._sock.settimeout(5.0)
            self._sock.connect(socket_path)
        except socket.error:
            self._sock.close()
            self._sock_state = False
            return False

        self._sock_state = True
        return True

    def connect(self) -> None:
        if not self.is_connected():
            if not self._init_socket():
                raise self.ConnectionError()

            if not self.is_connected():
                raise self.DuplicateConnectionError()

    def disconnect(self) -> None:
        if self._sock_state:
            self._sock.close()
            self._sock_state = False

    def is_connected(self) -> bool:
        try:
            _ = self.get_emu_status()
        except socket.error:
            self._sock_state = False
            self._sock.close()
            return False

        return True

    def read_int8(self, address: int) -> int:
        request = self._create_request(self.IPCCommand.READ8, address, 9)
        return self.from_bytes(self._send_request(request)[-1:])

    def read_int16(self, address) -> int:
        request = self._create_request(self.IPCCommand.READ16, address, 9)
        return self.from_bytes(self._send_request(request)[-2:])

    def read_int32(self, address) -> int:
        request = self._create_request(self.IPCCommand.READ32, address, 9)
        return self.from_bytes(self._send_request(request)[-4:])

    def read_int64(self, address) -> int:
        request = self._create_request(self.IPCCommand.READ64, address, 9)
        return self.from_bytes(self._send_request(request)[-8:])

    def read_bytes(self, address: int, length: int) -> bytes:
        """Careful! This can be quite slow for large reads"""
        data = b''
        while len(data) < length:
            if length - len(data) >= 8:
                data += self._send_request(self._create_request(self.IPCCommand.READ64, address + len(data), 9))[-8:]
            elif length - len(data) >= 4:
                data += self._send_request(self._create_request(self.IPCCommand.READ32, address + len(data), 9))[-4:]
            elif length - len(data) >= 2:
                data += self._send_request(self._create_request(self.IPCCommand.READ16, address + len(data), 9))[-2:]
            elif length - len(data) >= 1:
                data += self._send_request(self._create_request(self.IPCCommand.READ8, address + len(data), 9))[-1:]

        return data

    def write_int8(self, address: int, value: int) -> None:
        request = self._create_request(self.IPCCommand.WRITE8, address, 9 + self.DataSize.INT8)
        request += value.to_bytes(length=1, byteorder="little")
        self._send_request(request)

    def write_int16(self, address: int, value: int) -> None:
        request = self._create_request(self.IPCCommand.WRITE16, address, 9 + self.DataSize.INT16)
        request += value.to_bytes(length=2, byteorder="little")
        self._send_request(request)

    def write_int32(self, address: int, value: int) -> None:
        request = self._create_request(self.IPCCommand.WRITE32, address, 9 + self.DataSize.INT32)
        request += value.to_bytes(length=4, byteorder="little")
        self._send_request(request)

    def write_int64(self, address: int, value: int) -> None:
        request = self._create_request(self.IPCCommand.WRITE64, address, 9 + self.DataSize.INT64)
        request += value.to_bytes(length=8, byteorder="little")
        self._send_request(request)

    def write_float(self, address: int, value: float) -> None:
        request = self._create_request(self.IPCCommand.WRITE32, address, 9 + self.DataSize.INT32)
        request += struct.pack("<f", value)
        self._send_request(request)

    def write_bytes(self, address: int, data: bytes) -> None:
        """Careful! This can be quite slow for large writes"""
        bytes_written = 0
        while bytes_written < len(data):
            if len(data) - bytes_written >= 8:
                request = self._create_request(self.IPCCommand.WRITE64, address + bytes_written, 9 + self.DataSize.INT64)
                request += data[bytes_written:bytes_written + 8]
                self._send_request(request)
                bytes_written += 8
            elif len(data) - bytes_written >= 4:
                request = self._create_request(self.IPCCommand.WRITE32, address + bytes_written, 9 + self.DataSize.INT32)
                request += data[bytes_written:bytes_written + 4]
                self._send_request(request)
                bytes_written += 4
            elif len(data) - bytes_written >= 2:
                request = self._create_request(self.IPCCommand.WRITE16, address + bytes_written, 9 + self.DataSize.INT16)
                request += data[bytes_written:bytes_written + 2]
                self._send_request(request)
                bytes_written += 2
            elif len(data) - bytes_written >= 1:
                request = self._create_request(self.IPCCommand.WRITE8, address + bytes_written, 9 + self.DataSize.INT8)
                request += data[bytes_written:bytes_written + 1]
                self._send_request(request)
                bytes_written += 1

    def write_string(self, address: int, value: str) -> None:
        data = value.encode("ascii") + b'\x00'
        self.write_bytes(address, data)

    def read_string(self, address: int, max_length: int) -> str:
        data = self.read_bytes(address, max_length)
        return data.split(b'\x00', 1)[0].decode("ascii")

    def get_game_id(self) -> str:
        request = self.to_bytes(5, 4) + self.to_bytes(self.IPCCommand.ID, 1)
        response = self._send_request(request)
        return response[9:-1].decode("ascii")

    def get_emu_status(self) -> EmuStatus:
        request = self.to_bytes(5, 4) + self.to_bytes(self.IPCCommand.STATUS, 1)
        response = self._send_request(request)
        return self.EmuStatus(self.from_bytes(response[-4:]))

    def _send_request(self, request: bytes) -> bytes:
        if not self._sock_state:
            self._init_socket()

        try:
            self._sock.sendall(request)
        except socket.error:
            self._sock.close()
            self._sock_state = False
            raise ConnectionError("Lost connection to PCSX2.")

        end_length = 4
        result: bytes = b''
        while len(result) < end_length:
            try:
                response = self._sock.recv(4096)
            except TimeoutError:
                raise TimeoutError("Response timed out. "
                                   "This might be caused by having two PINE connections open on the same slot")

            if len(response) <= 0:
                result = b''
                break

            result += response

            if end_length == 4 and len(response) >= 4:
                end_length = self.from_bytes(result[0:4])
                if end_length > self.MAX_IPC_SIZE:
                    result = b''
                    break

        if len(result) == 0:
            raise ConnectionError("Invalid response from PCSX2.")
        if result[4] == self.IPCResult.IPC_FAIL:
            raise ConnectionError("Failure indicated in PCSX2 response.")

        return result

    @staticmethod
    def _create_request(command: IPCCommand, address: int, size: int = 0) -> bytes:
        ipc = Pine.to_bytes(size, 4)
        ipc += Pine.to_bytes(command, 1)
        ipc += Pine.to_bytes(address, 4)
        return ipc

    @staticmethod
    def to_bytes(value: int, size: int) -> bytes:
        return value.to_bytes(length=size, byteorder="little")

    @staticmethod
    def from_bytes(arr: bytes) -> int:
        return int.from_bytes(arr, byteorder="little")
