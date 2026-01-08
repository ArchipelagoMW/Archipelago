class Block:
    def __init__(self, start, end):
        if start > end:
            self._start = end
            self._end = start
        else:
            self._start = start
            self._end = end
        self._size = self._end - self._start + 1

    @property
    def size(self):
        return self._size

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, new_start):
        self._start = new_start
        self._size = self._end - self._start + 1

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, new_end):
        self._end = new_end
        self._size = self._end - self._start + 1

class Heap:
    def __init__(self):
        self.blocks = []
        self._available = 0

    def allocate(self, size):
        def find_best_fit(size):
            best_block = None
            if not self.blocks:
                return None

            best_diff = self._available
            for block in self.blocks:
                diff = block.size - size
                if diff == 0:
                    return block
                elif diff > 0 and diff < best_diff:
                    best_block = block
                    best_diff = diff
            return best_block

        block = find_best_fit(size)
        if block is None:
            raise MemoryError(f"Unable to allocate block of size {size}")

        start = block.start
        block.start += size
        if block.size == 0:
            self.blocks.remove(block)
        self._available -= size
        return start

    def free(self, start, end):
        new_block = Block(start, end)

        overlaps = set()
        for block in self.blocks:
            if block.start >= new_block.start and block.start <= new_block.end + 1:
                if block.end > new_block.end:
                    new_block.end = block.end
                overlaps.add(block)
            elif block.end <= new_block.end and block.end >= new_block.start - 1:
                if block.start < new_block.start:
                    new_block.start = block.start
                overlaps.add(block)
            elif block.start < new_block.start and block.end > new_block.end:
                return # new block is already encompassed by a single existing free block

        new_blocks = [new_block]
        self._available = new_block.size
        for block in self.blocks:
            if block not in overlaps:
                new_blocks.append(block)
                self._available += block.size
        self.blocks = new_blocks

    def reserve(self, start, end):
        reserved = Block(start, end)

        overlaps = set()
        for block in self.blocks:
            if block.start >= reserved.start and block.start <= reserved.end:
                if block.end > reserved.end:
                    block.start = reserved.end + 1
                else:
                    overlaps.add(block)
            elif block.end <= reserved.end and block.end >= reserved.start:
                if block.start < reserved.start:
                    block.end = reserved.start - 1
                else:
                    overlaps.add(block)
            elif block.start < reserved.start and block.end > reserved.end:
                # reserved is encompassed by a single exsting free block
                # split block into two blocks which don't overlap reserved
                self.blocks.append(Block(reserved.end + 1, block.end))
                block.end = reserved.start - 1
                self._available -= (end - start) + 1
                return

        new_blocks = []
        self._available = 0
        for block in self.blocks:
            if block not in overlaps:
                new_blocks.append(block)
                self._available += block.size
        self.blocks = new_blocks

    @property
    def available(self):
        return self._available

    def __str__(self):
        return f"{self.available} bytes available in {len(self.blocks)} blocks"

    def __repr__(self):
        result = f"{str(self)}\n"
        for block in self.blocks:
            result += f"  [0x{block.start:06x} - 0x{block.end:06x}] {block.size} bytes\n"
        return result[:-1]

    def print(self):
        print(str(self))

    def printr(self):
        print(repr(self))
