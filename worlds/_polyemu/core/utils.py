class Buffer:
    _buffer: bytes
    _cursor: int

    def __init__(self, data: bytes):
        self._buffer = data
        self._cursor = 0

    def reached_end(self):
        return self._cursor >= len(self._buffer)

    def consume_bytes(self, size: int) -> bytes:
        ret = self._buffer[self._cursor:self._cursor + size]
        self._cursor = self._cursor + size
        return ret

    def consume_int(self, size: int) -> int:
        ret = int.from_bytes(self._buffer[self._cursor:self._cursor + size], "big")
        self._cursor = self._cursor + size
        return ret

    def __str__(self):
        byte_strs = [hex(d) for d in self._buffer]
        byte_strs = [b[b.find("x") + 1:].rjust(2, "0") for b in byte_strs]
        byte_strs = [f"[{b}]" if i == self._cursor else b for i, b in enumerate(byte_strs)]
        return " ".join(byte_strs)
