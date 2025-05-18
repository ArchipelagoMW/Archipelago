


class LocalRom:

    def __init__(self, file, name=None, hash=None):
        self.name = name
        self.hash = hash

        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())

    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytearray:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        pass
        self.buffer[startaddress:startaddress + len(values)] = values
        pass

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())

    def find_free_space(self, start, size):
        for i in range(start, 0xffff - size + 1):
            found = True
            if self.read_bytes(i, size) != bytearray([0xff] * size):
                found = False
                break

            if found:
                return i
        return -1


