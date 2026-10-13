# All the write functions return a bool for has written it but there isnt a use case for that I've found
def kh2_read_short(self, address) -> int:
    """Reads 2 bytes"""
    return self.kh2.read_short(self.kh2.base_address + address)


def kh2_write_short(self, address, value) -> None:
    """Writes 2 bytes"""
    self.kh2.write_short(self.kh2.base_address + address, value)


def kh2_write_byte(self, address, value):
    """Writes 1 byte"""
    return self.kh2.write_bytes(self.kh2.base_address + address, value.to_bytes(1, 'big'), 1)


def kh2_read_byte(self, address):
    """Reads 1 byte"""
    return int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + address, 1))


def kh2_read_int(self, address):
    """Reads 4 bytes"""
    return self.kh2.read_int(self.kh2.base_address + address)


def kh2_write_int(self, address, value):
    """Writes 4 bytes"""
    self.kh2.write_int(self.kh2.base_address + address, value)


def kh2_read_longlong(self, address):
    """Reads 8 bytes"""
    return self.kh2.read_longlong(self.kh2.base_address + address)


def kh2_read_string(self, address, length):
    """Reads length amount of bytes"""
    return self.kh2.read_string(self.kh2.base_address + address, length)


def kh2_write_bytes(self, address, value):
    return self.kh2.write_bytes(self.kh2.base_address + address, bytes(value), len(value))


def kh2_return_base_address(self):
    return self.kh2.base_address
