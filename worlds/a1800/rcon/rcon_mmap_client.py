from CommonClient import logger
from collections import deque
from contextlib import contextmanager
from mmap import mmap
from pathlib import Path
from time import perf_counter, sleep
from typing import Any, Generator, Optional, TypeVar

from .rcon_mmap_file_access import FILE_SIZE, RCONMMapFileAccess
from .rcon_packet import RCONPacket

T = TypeVar("T")


class RCONTimeout(Exception):
    """Connection to RCON file has timed out. Was the file wiped or deleted?"""


class RCONMMapClient:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._id_seq = 0

        self._file_obj = self._file_path.open(mode="rb+")

        self._file_access = RCONMMapFileAccess(mmap(self._file_obj.fileno(), length=FILE_SIZE))

        self._send_queue: deque[RCONPacket] = deque()

        self.connected = False

    def _get_id(self) -> int:
        if self._id_seq == 2**31 - 1:  # signed int32 max
            self._id_seq = 0
        else:
            self._id_seq += 1
        return self._id_seq

    def connect(self) -> bool:
        if self.connected:
            return True
        else:
            if self._file_obj.closed:
                self._file_obj = self._file_path.open(mode="rb+")

            if self._file_access.closed:
                self._file_access = RCONMMapFileAccess(mmap(self._file_obj.fileno(), length=FILE_SIZE))

        if self._file_access.ring_buffer_client.has_request():
            return False

        while self._file_access.ring_buffer_server.get_request():
            pass

        auth_id = self._get_id()
        self._send_packet(auth_id, RCONPacket.SERVERDATA_AUTH, "")

        sleep(0.05)

        try:
            response = self._receive_packet()
        except RCONTimeout:
            return False

        if response.type != RCONPacket.SERVERDATA_RESPONSE_VALUE or response.id != auth_id:
            return False

        try:
            response = self._receive_packet()
        except RCONTimeout:
            return False

        if response.type == RCONPacket.SERVERDATA_AUTH_RESPONSE and response.id == auth_id:
            self.connected = True
        return self.connected

    def _send_packet(self, send_id: int, send_type: int, send_body: str) -> None:
        self._send_queue.append(RCONPacket(id=send_id, type=send_type, body=send_body))
        self._handle_send_queue()

    def _handle_send_queue(self) -> None:
        if len(self._send_queue) == 0:
            return

        packet = self._send_queue[0]
        logger.debug(f"Sending packet {packet.id} {packet.type} {packet.body}")
        if self._file_access.ring_buffer_client.put_request(packet.msg()):
            self._send_queue.popleft()
            self._handle_send_queue()
        else:
            print("Warning: send queue is full!")

    def _receive_packet(self, timeout: int = 1) -> RCONPacket:
        request = self._file_access.ring_buffer_server.get_request()
        start = perf_counter()
        while not request and ((timeout <= 0) or (perf_counter() - start < timeout)):
            sleep(0.01)
            request = self._file_access.ring_buffer_server.get_request()
        if not request:
            self.close()
            raise RCONTimeout()
        p = RCONPacket.from_buffer(request)
        logger.debug(f"Received packet {p.id} {p.type} {p.body}")
        return p
        # return RCONPacket.from_buffer(request)

    def send_command(self, command: str, timeout: int = 1) -> Optional[str]:
        return self.send_commands({"command": command}, timeout)["command"]

    def send_commands(self, commands: dict[T, str], timeout: int = 1) -> dict[T, Optional[str]]:
        id_map: dict[int, T] = {}
        check_id_map: dict[int, tuple[T, int]] = {}
        results: dict[T, Optional[str]] = {}
        for key, value in commands.items():
            packet_id = self._get_id()
            check_id = self._get_id()
            self._send_packet(packet_id, RCONPacket.SERVERDATA_EXECCOMMAND, value)
            self._send_packet(check_id, RCONPacket.SERVERDATA_RESPONSE_VALUE, "")
            id_map[packet_id] = key
            check_id_map[check_id] = (key, packet_id)

        sleep(0.05)

        results: dict[T, Optional[str]] = {}
        while len(id_map.items()) > 0:
            response = self._receive_packet(timeout)
            if response.type != RCONPacket.SERVERDATA_RESPONSE_VALUE:
                continue

            if response.id in check_id_map:
                key, packet_id = check_id_map[response.id]
                if not response.body:
                    if key not in results:
                        results[key] = None
                elif response.body == "\x00\x00\x00\x01\x00\x00\x00\x00":
                    id_map.pop(packet_id, None)
            elif response.id in id_map:
                key = id_map[response.id]
                previous_result = (results[key] or "") if key in results else ""
                results[key] = previous_result + response.body

        return results

    def close(self):
        self.connected = False

        if not self._file_access.closed:
            self._file_access.close()

        if not self._file_obj.closed:
            self._file_obj.close()


@contextmanager
def open_client(file_path: Path,) -> Generator[RCONMMapClient, Any, None]:
    rcon_mmap_client = RCONMMapClient(file_path)
    try:
        yield rcon_mmap_client
    finally:
        rcon_mmap_client.close()
