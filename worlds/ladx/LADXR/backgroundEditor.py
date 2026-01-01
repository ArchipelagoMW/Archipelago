
class BackgroundEditor:
    def __init__(self, rom, index, *, attributes=False):
        self.__index = index
        self.__is_attributes = attributes

        self.tiles = {}
        if attributes:
            data = rom.background_attributes[index]
        else:
            data = rom.background_tiles[index]
        idx = 0
        while data[idx] != 0x00:
            addr = data[idx] << 8 | data[idx + 1]
            amount = (data[idx + 2] & 0x3F) + 1
            repeat = (data[idx + 2] & 0x40) == 0x40
            vertical = (data[idx + 2] & 0x80) == 0x80
            idx += 3
            for n in range(amount):
                self.tiles[addr] = data[idx]
                if not repeat:
                    idx += 1
                addr += 0x20 if vertical else 0x01
            if repeat:
                idx += 1

    def dump(self):
        if not self.tiles:
            return
        low = min(self.tiles.keys()) & 0xFFE0
        high = (max(self.tiles.keys()) | 0x001F) + 1
        print("0x%02x " % (self.__index) + "".join(map(lambda n: "%2X" % (n), range(0x20))))
        for addr in range(low, high, 0x20):
            print("%04x " % (addr) + "".join(map(lambda n: ("%02X" % (self.tiles[addr + n])) if addr + n in self.tiles else "  ", range(0x20))))

    def store(self, rom):
        # NOTE: This is not a very good encoder, but the background back has so much free space that we really don't care.
        # Improvements can be done to find long sequences of bytes and store those as repeated.
        result = bytearray()
        low = min(self.tiles.keys())
        high = max(self.tiles.keys()) + 1
        while low < high:
            if low not in self.tiles:
                low += 1
                continue
            different_count = 1
            while low + different_count in self.tiles and different_count < 0x40:
                different_count += 1
            same_count = 1
            while low + same_count in self.tiles and self.tiles[low] == self.tiles[low + same_count] and same_count < 0x40:
                same_count += 1
            if same_count > different_count - 4 and same_count > 2:
                result.append(low >> 8)
                result.append(low & 0xFF)
                result.append((same_count - 1) | 0x40)
                result.append(self.tiles[low])
                low += same_count
            else:
                result.append(low >> 8)
                result.append(low & 0xFF)
                result.append(different_count - 1)
                for n in range(different_count):
                    result.append(self.tiles[low + n])
                low += different_count
        result.append(0x00)
        if self.__is_attributes:
            rom.background_attributes[self.__index] = result
        else:
            rom.background_tiles[self.__index] = result
