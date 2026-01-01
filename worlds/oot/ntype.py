# Written by mzxrules

import struct


class uint16:
    _struct = struct.Struct('>H')
    def write(buffer, address, value): 
        struct.pack_into('>H', buffer, address, value)

    def read(buffer, address=0): 
        return uint16._struct.unpack_from(buffer, address)[0]

    def bytes(value):
        value = value & 0xFFFF
        return [(value >> 8) & 0xFF, value & 0xFF]

    def value(values):
        return (values[0] << 8) | values[1]


class uint32:
    _struct = struct.Struct('>I')
    def write(buffer, address, value): 
        struct.pack_into('>I', buffer, address, value)

    def read(buffer, address=0): 
        return uint32._struct.unpack_from(buffer, address)[0]

    def bytes(value):
        value = value & 0xFFFFFFFF
        return [(value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]

    def value(values):
        return (values[0] << 24) | (values[1] << 16) | (values[2] << 8) | values[3]


class int32:
    _struct = struct.Struct('>i')
    def write(buffer, address, value): 
        struct.pack_into('>i', buffer, address, value)

    def read(buffer, address=0): 
        return int32._struct.unpack_from(buffer, address)[0]

    def bytes(value):
        value = value & 0xFFFFFFFF
        return [(value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]

    def value(values):
        value = (values[0] << 24) | (values[1] << 16) | (values[2] << 8) | values[3]
        if value >= 0x80000000:
            value ^= 0xFFFFFFFF
            value += 1
        return value


class uint24:
    def write(buffer, address, value): 
        byte_arr = bytes(value)
        buffer[address:address + 3] = byte_arr[0:3]

    def read(buffer, address=0): 
        return (buffer[address+0] << 16) | (buffer[address+1] << 8) | buffer[address+2]

    def bytes(value):
        value = value & 0xFFFFFF
        return [(value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]

    def value(values):
        return (values[0] << 16) | (values[1] << 8) | values[2]


class BigStream(object):

    def __init__(self, buffer:bytearray):
        self.last_address = 0
        self.buffer = buffer


    def seek_address(self, address=None, delta=None):
        if delta is None:
            self.last_address = address
        else:
            self.last_address += delta


    def eof(self):
        return self.last_address >= len(self.buffer)


    def read_byte(self, address=None):
        if address == None:
            address = self.last_address
        self.last_address = address + 1
        return self.buffer[address]


    def read_bytes(self, address=None, length=1):
        if address == None:
            address = self.last_address
        self.last_address = address + length
        return self.buffer[address : address + length]


    def read_int16(self, address=None):
        if address == None:
            address = self.last_address
        return uint16.value(self.read_bytes(address, 2))


    def read_int24(self, address=None):
        if address == None:
            address = self.last_address
        return uint24.value(self.read_bytes(address, 3))


    def read_int32(self, address=None):
        if address == None:
            address = self.last_address
        return uint32.value(self.read_bytes(address, 4))


    def write_byte(self, address, value):
        if address == None:
            address = self.last_address
        self.buffer[address] = value
        self.last_address = address + 1


    def write_sbyte(self, address, value):
        if address == None:
            address = self.last_address
        self.write_bytes(address, struct.pack('b', value))


    def write_int16(self, address, value):
        if address == None:
            address = self.last_address
        self.write_bytes(address, uint16.bytes(value))


    def write_int24(self, address, value):
        if address == None:
            address = self.last_address
        self.write_bytes(address, uint24.bytes(value))


    def write_int32(self, address, value):
        if address == None:
            address = self.last_address
        self.write_bytes(address, uint32.bytes(value))


    def write_f32(self, address, value:float):
        if address == None:
            address = self.last_address
        self.write_bytes(address, struct.pack('>f', value))


    def write_bytes(self, startaddress, values):
        if startaddress == None:
            startaddress = self.last_address
        self.last_address = startaddress + len(values)
        self.buffer[startaddress:startaddress + len(values)] = values


    def write_int16s(self, startaddress, values):
        if startaddress == None:
            startaddress = self.last_address
        for i, value in enumerate(values):
            self.write_int16(startaddress + (i * 2), value)


    def write_int24s(self, startaddress, values):
        if startaddress == None:
            startaddress = self.last_address
        for i, value in enumerate(values):
            self.write_int24(startaddress + (i * 3), value)


    def write_int32s(self, startaddress, values):
        if startaddress == None:
            startaddress = self.last_address
        for i, value in enumerate(values):
            self.write_int32(startaddress + (i * 4), value)


    def append_byte(self, value):
        self.buffer.append(value)


    def append_sbyte(self, value):
        self.append_bytes(struct.pack('b', value))


    def append_int16(self, value):
        self.append_bytes(uint16.bytes(value))


    def append_int24(self, value):
        self.append_bytes(uint24.bytes(value))


    def append_int32(self, value):
        self.append_bytes(uint32.bytes(value))


    def append_f32(self, value:float):
        self.append_bytes(struct.pack('>f', value))


    def append_bytes(self, values):
        for value in values:
            self.append_byte(value)


    def append_int16s(self, values):
        for value in values:
            self.append_int16(value)


    def append_int24s(self, values):
        for value in values:
            self.append_int24(value)


    def append_int32s(self, values):
        for value in values:
            self.append_int32(value)
