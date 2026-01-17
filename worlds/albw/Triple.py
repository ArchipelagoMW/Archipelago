from typing import Optional
import socket
import struct
import asyncio

from CommonClient import logger

class TripleException(Exception):
    pass

class TripleInterface:
    PACKET_VERSION: int = 1
    TYPE_NONE: int = 0
    TYPE_READ: int = 1
    TYPE_WRITE: int = 2
    HEADER_SIZE: int = 16
    MAX_READ_SIZE: int = 32
    MAX_WRITE_SIZE: int = 24

    tries_to_timeout: int = 200000
    socket: socket.socket

    async def connect(self, address) -> bool:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((address, 45987))
        self.socket.setblocking(0)
        self.socket.settimeout(0)
        try:
            packet = struct.pack("=IIII", self.PACKET_VERSION, 0, self.TYPE_NONE, 0)
            await self._send(packet)
            await self._recv(self.HEADER_SIZE)
            return True
        except:
            return False
    
    def disconnect(self):
        if hasattr(self, 'socket'):
            self.socket.close()
    
    def set_timeout(self, timeout):
        try:
            self.tries_to_timeout = int(timeout)
            return True
        except ValueError as e:
            return False
    
    async def _recv(self, length) -> bytes:
        tries = 0
        while True:
            if tries > self.tries_to_timeout:
                raise TripleException("")
            try:
                in_packet = self.socket.recv(length)
                return in_packet
            except Exception as e:
                await asyncio.sleep(0)
                tries += 1
    
    async def _send(self, packet):
        tries = 0
        bytes_sent = 0
        while True:
            if tries > self.tries_to_timeout:
                raise TripleException("")
            try:
                bytes_sent += self.socket.send(packet)
                if bytes_sent == len(packet):
                    break
            except Exception as e:
                await asyncio.sleep(0)
                tries += 1
    
    async def _read_single(self, address: int, size: int) -> bytes:
        out_packet = struct.pack("=IIIIII", self.PACKET_VERSION, 0, self.TYPE_READ, 8, address, size)
        await self._send(out_packet)
        in_packet = await self._recv(self.HEADER_SIZE + self.MAX_READ_SIZE)
        if in_packet and len(in_packet) == self.HEADER_SIZE + size:
            return in_packet[self.HEADER_SIZE:]
        else:
            raise Exception("Did not receive packet of expected size.")
    
    async def read(self, address: int, size: int) -> bytes:
        try:
            mem = b""
            while size > 0:
                request_size = min(size, self.MAX_READ_SIZE)
                mem += await self._read_single(address, request_size)
                address += request_size
                size -= request_size
            return mem
        except Exception as e:
            if str(e) == "":
                raise TripleException("")
            raise TripleException(f"Lost connection to 3ds ({str(e)})")
    
    async def read_u32(self, address: int) -> int:
        return int.from_bytes(await self.read(address, 4), "little")

    async def _write_single(self, address: int, data: bytes) -> None:
        out_packet = struct.pack("=IIIIII", self.PACKET_VERSION, 0, self.TYPE_WRITE, 8 + len(data), address, len(data))
        out_packet += data
        await self._send(out_packet)
        await self._recv(self.HEADER_SIZE)

    async def write(self, address: int, data: bytes) -> None:
        try:
            start = 0
            while start < len(data):
                end = min(start + self.MAX_WRITE_SIZE, len(data))
                await self._write_single(address + start, data[start:end])
                start += self.MAX_WRITE_SIZE
        except Exception as e:
            if str(e) == "":
                raise TripleException("")
            raise TripleException(f"Lost connection to 3ds ({str(e)})")

    async def write_u32(self, address: int, value: int) -> None:
        await self.write(address, value.to_bytes(4, "little"))