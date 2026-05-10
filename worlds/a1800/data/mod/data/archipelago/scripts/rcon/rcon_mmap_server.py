from collections import deque
from contextlib import contextmanager
from mmap import mmap
from pathlib import Path
from typing import Any, Callable, Generator

from .rcon_mmap_file_access import FILE_SIZE, RCONMMapFileAccess
from .rcon_packet import RCONPacket
from .rcon_message import RCONMessage


class RCONMMapServer:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        self._file_obj = self._file_path.open(mode="wb+")
        self._file_obj.write(bytes(FILE_SIZE))
        self._file_obj.flush()

        self._file_access = RCONMMapFileAccess(mmap(self._file_obj.fileno(), length=FILE_SIZE))

        # Typing fix for python 3.5
        self._receive_queue = deque([RCONPacket(0, 0, "")])
        self._receive_queue.pop()

        # Typing fix for python 3.5
        self._send_queue = deque([RCONPacket(0, 0, "")])
        self._send_queue.pop()

        self._callbacks = {
            "/print": _handle_print
        }

    def register_handler(self, command: str, handler: Callable[["RCONMMapServer", RCONPacket, str], None]) -> None:
        self._callbacks[command] = handler  # pyright: ignore[reportArgumentType]

    def _handle_receive_queue(self) -> None:
        if len(self._receive_queue) == 0:
            return

        packet = self._receive_queue.popleft()

        if packet.type == RCONPacket.SERVERDATA_AUTH:
            self.send_message(packet.id, RCONPacket.SERVERDATA_RESPONSE_VALUE, "")
            self.send_message(packet.id, RCONPacket.SERVERDATA_AUTH_RESPONSE, "")
        elif packet.type == RCONPacket.SERVERDATA_RESPONSE_VALUE and not packet.body:
            self.send_message(packet.id, RCONPacket.SERVERDATA_RESPONSE_VALUE, "")
            self.send_message(packet.id, RCONPacket.SERVERDATA_RESPONSE_VALUE, "\x00\x00\x00\x01\x00\x00\x00\x00")
        elif packet.type == RCONPacket.SERVERDATA_EXECCOMMAND:
            body = packet.body.split(maxsplit=1)

            if body[0] in self._callbacks:
                self._callbacks[body[0]](self, packet, body[1] if len(body) > 1 else "")
            else:
                print("Invalid command: {}".format(body[0]))

        self._handle_receive_queue()

    def _handle_send_queue(self) -> None:
        if len(self._send_queue) == 0:
            return

        packet = self._send_queue[0]
        if self._file_access.ring_buffer_server.put_request(packet.msg()):
            self._send_queue.popleft()
            self._handle_send_queue()
        else:
            print("Warning: send queue is full!")

    def send_message(self, send_id: int, send_type: int, send_body: str) -> None:
        message = RCONMessage(id=send_id, type=send_type, body=send_body)
        self._send_queue += message.packets

    def listen(self) -> None:
        request = self._file_access.ring_buffer_client.get_request()
        while request:
            self._receive_queue.append(RCONPacket.from_buffer(request))

            request = self._file_access.ring_buffer_client.get_request()

        self._handle_receive_queue()
        self._handle_send_queue()

    def close(self):
        if not self._file_access.closed:
            self._file_access.close()

        if not self._file_obj.closed:
            self._file_obj.close()

        try:
            self._file_path.unlink()
        except FileNotFoundError:
            pass


def _handle_print(_server: RCONMMapServer, _packet: RCONPacket, body: str) -> None:
    if body:
        print(body)
    else:
        print("Missing argument for /print")


@contextmanager
def open_rcon_mmap_server(file_path: Path) -> Generator[RCONMMapServer, Any, None]:
    rcon_mmap_server = RCONMMapServer(file_path)
    try:
        yield rcon_mmap_server
    finally:
        rcon_mmap_server.close()
