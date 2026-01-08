import bsdiff4

class ROM():
    SHORT_PTR_SIZE = 2  # short ptr (16-bit)
    LONG_PTR_SIZE = 3   # long ptr  (24-bit)

    def __init__(self, file_name):
        from ..valid_rom_file import valid_rom_file
        if not valid_rom_file(file_name):
            raise ValueError("Invalid ROM File")

        with open(file_name, "rb") as rom_file:
            self.data = list(rom_file.read())

        self.expand()

    def size(self):
        return len(self.data)

    def expand(self):
        expanded_size = 4 * 2 ** 20 # 4 mb
        self.data.extend([0xff] * (expanded_size - len(self.data)))

    def write(self, file_name):
        with open(file_name, "wb") as out_file:
            out_file.write(bytearray(self.data))

    def write_patch(self, base_rom, modified_rom):
        patch = bsdiff4.diff(base_rom, bytes(self.data))
        with open(modified_rom, "wb") as output_patch:
            output_patch.write(bytearray(patch))

    def get_bits(self, address, mask):
        return self.data[address] & mask

    def get_byte(self, address):
        return self.data[address]

    def get_short(self, address):
        return int.from_bytes(self.get_bytes(address, 2), byteorder='little')

    def get_bytes(self, address, count):
        return self.data[address : address + count]

    def get_bytes_endian_swap(self, address, count):
        return self.get_bytes(address, count)[::-1]

    def set_bits(self, address, mask, value):
        not_mask = 0xff - mask # be careful of signed values
        self.data[address] = (value & mask) | (self.data[address] & not_mask)

    def set_bit_num(self, address, bit_num, value):
        # set bit_num starting at address, e.g. bit_num = 12 address = 0xa0000, sets bit 4 in byte 0xa0001
        byte = bit_num // 8
        bit = bit_num % 8

        if value:
            self.data[address + byte] = self.data[address + byte] | (1 << bit)
        else:
            self.data[address + byte] = self.data[address + byte] & ~(1 << bit)

    def set_byte(self, address, value):
        self.data[address] = value

    def set_short(self, address, value):
        self.set_bytes(address, value.to_bytes(2, 'little'))

    def set_bytes(self, address, values):
        self.data[address : address + len(values)] = values
        return address + len(values)

    def set_bytes_endian_swap(self, address, values):
        return self.set_bytes(address, values[::-1])

    def print_byte(self, address, decimal = False):
        if decimal:
            print(self.get_byte(address))
        else:
            print('0x{:02x}'.format(self.get_byte(address)))

    def print_bytes(self, address, count, decimal = False):
        if decimal:
            print(' '.join(str(byte) for byte in self.get_bytes(address, count)))
        else:
            print(' '.join("0x{:02x}".format(byte) for byte in self.get_bytes(address, count)))

    def print_addresses(self, address, count):
        for offset, byte in enumerate(self.get_bytes(address, count)):
            print(hex(address + offset) + ": " + hex(byte))
