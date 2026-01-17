from typing import Optional
import socket
import struct
import asyncio

class CitraException(Exception):
    pass

class CitraInterface:
    PACKET_VERSION: int = 1
    TYPE_NONE: int = 0
    TYPE_READ: int = 1
    TYPE_WRITE: int = 2
    HEADER_SIZE: int = 16
    MAX_READ_SIZE: int = 32
    MAX_WRITE_SIZE: int = 24

    socket: socket.socket

    async def connect(self) -> bool:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect(("127.0.0.1", 45987))
        self.socket.settimeout(1)
        try:
            packet = struct.pack("=IIII", self.PACKET_VERSION, 0, self.TYPE_NONE, 0)
            self.socket.sendall(packet)
            self.socket.recv(self.HEADER_SIZE)
            return True
        except:
            return False
    
    def _read_single(self, address: int, size: int) -> bytes:
        out_packet = struct.pack("=IIIIII", self.PACKET_VERSION, 0, self.TYPE_READ, 8, address, size)
        self.socket.sendall(out_packet)
        in_packet = self.socket.recv(self.HEADER_SIZE + self.MAX_READ_SIZE)
        if in_packet and len(in_packet) == self.HEADER_SIZE + size:
            return in_packet[self.HEADER_SIZE:]
        else:
            raise Exception("Did not receive packet of expected size.")
    
    async def read(self, address: int, size: int) -> bytes:
        try:
            mem = b""
            while size > 0:
                request_size = min(size, self.MAX_READ_SIZE)
                mem += self._read_single(address, request_size)
                address += request_size
                size -= request_size
            return mem
        except Exception as e:
            raise CitraException(f"Lost connection to emulator ({str(e)})")
    
    async def read_u32(self, address: int) -> int:
        return int.from_bytes(await self.read(address, 4), "little")

    def _write_single(self, address: int, data: bytes) -> None:
        out_packet = struct.pack("=IIIIII", self.PACKET_VERSION, 0, self.TYPE_WRITE, 8 + len(data), address, len(data))
        out_packet += data
        self.socket.sendall(out_packet)
        self.socket.recv(self.HEADER_SIZE)

    async def write(self, address: int, data: bytes) -> None:
        try:
            start = 0
            while start < len(data):
                end = min(start + self.MAX_WRITE_SIZE, len(data))
                self._write_single(address + start, data[start:end])
                start += self.MAX_WRITE_SIZE
        except Exception as e:
            raise CitraException(f"Lost connection to emulator ({str(e)})")

    async def write_u32(self, address: int, value: int) -> None:
        await self.write(address, value.to_bytes(4, "little"))