# CR cam: why are we rolling our own transport layer

import struct
import asyncio
from collections import defaultdict, abc
from typing import NewType, DefaultDict

MsgId = NewType("MsgId", int)

# Both are unsigned 4-byte header fields.
MAX_MSG_SIZE = (1 << 32) - 1
MAX_ID = 1 << 32

# > = big endian
# L = 4 bytes, unsigned (size)
# L = 4 bytes, unsigned (id)
# b = 1 byte (more?)
HEADER_FORMAT = ">LLb"
HEADER_SIZE = 4 + 4 + 1

STRING_ENCODING = "utf8"

# Format header data as bytes according to HEADER_FORMAT
def format_header(*, size: int, id: MsgId, more: bool):
    return struct.pack(HEADER_FORMAT, size, id, more)


# Calculate the next message ID
def increment_msgid(id: MsgId) -> MsgId:
    return MsgId((id + 1) % MAX_ID)


# This session class handles low-level byte transfer
class Session(abc.AsyncIterator[bytes]):
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    curr_id: MsgId

    # In a real, concurrent system, we'd want to protect this dictionary with
    # some sort of lock. However, async/await means that the write access to
    # [self.pending_msgs] is safe provided that we don't [await] while the
    # dictionary is in some intermediate state. Also, dictionaries should have
    # atomic operations when used with primitive keys, so it'd be fine anyway.
    pending_msgs: DefaultDict[MsgId, bytes]

    # Initialize session
    def __init__(self, reader, writer):
        self.curr_id = MsgId(0)
        self.reader = reader
        self.writer = writer
        self.pending_msgs = defaultdict(bytes)

    # Get the next fresh message ID in this session
    def fresh_id(self) -> MsgId:
        prev = self.curr_id
        self.curr_id = increment_msgid(self.curr_id)
        return prev

    # Send a single message (s) in bytes
    # by breaking down the message into packets
    # and sending each packet in order
    async def send(self, s: bytes) -> None:
        # generate a new ID for this message
        msg_id = self.fresh_id()

        # for each chunk of the message,
        # assemble a packet with the corresponding header and send it
        for i in range(0, len(s), MAX_MSG_SIZE):
            chunk = s[i : i + MAX_MSG_SIZE]
            more = bool(s[i + MAX_MSG_SIZE :])
            header = format_header(size=len(chunk), id=msg_id, more=more)
            packet = header + chunk
            self.writer.write(packet)
            await self.writer.drain()

    # Receive a single message in bytes
    async def recv_single(self) -> bytes:
        # loop to receive all incoming packets
        while True:
            # for each packet, read and unpack header, then read chunk
            header = await self.reader.readexactly(HEADER_SIZE)
            size, id, more = struct.unpack(HEADER_FORMAT, header)
            chunk = await self.reader.readexactly(size)
            id = MsgId(id)
            # add this chunk to the corresponding pending message by id
            self.pending_msgs[id] += chunk
            # if this is the last chunk, the message is fully received
            if not more:
                payload = self.pending_msgs[id]
                # delete from pending and return full message
                del self.pending_msgs[id]
                return payload

    # Initialize iterator for session
    def __aiter__(self) -> abc.AsyncIterator[bytes]:
        return self

    # Iterator function to receive the next message
    async def __anext__(self) -> bytes:
        try:
            return await self.recv_single()
        except (EOFError, asyncio.CancelledError, struct.error):
            raise StopAsyncIteration
