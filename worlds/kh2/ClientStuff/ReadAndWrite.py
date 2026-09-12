from PyMemoryEditor import OpenProcess, ProcessNotFoundError

KH2_PROCESS_NAME = "KINGDOM HEARTS II FINAL MIX"


def kh2_open_process(self) -> None:
    """Opens the game's process and caches the base address of its executable"""
    # exact_match is off so the name also matches "KINGDOM HEARTS II FINAL MIX.exe"
    self.kh2 = OpenProcess(name=KH2_PROCESS_NAME, exact_match=False)

    # The first module of a process is its own executable, which is what every address here is relative to
    main_module = next(self.kh2.get_modules(), None)
    if main_module is None:
        self.kh2_close_process()
        raise ProcessNotFoundError(KH2_PROCESS_NAME)
    self.kh2_base_address = main_module.base_address


def kh2_close_process(self) -> None:
    """Closes the handle of the game's process if it is open"""
    if self.kh2 is not None:
        try:
            self.kh2.close()
        except OSError:
            pass
    self.kh2 = None
    self.kh2_base_address = None


# All the write functions return a bool for has written it but there isnt a use case for that I've found
def kh2_read_short(self, address) -> int:
    """Reads 2 bytes"""
    return self.kh2.read_short(self.kh2_base_address + address)


def kh2_write_short(self, address, value) -> None:
    """Writes 2 bytes"""
    self.kh2.write_short(self.kh2_base_address + address, value)


def kh2_write_byte(self, address, value):
    """Writes 1 byte"""
    return self.kh2.write_uchar(self.kh2_base_address + address, value)


def kh2_read_byte(self, address):
    """Reads 1 byte"""
    return self.kh2.read_uchar(self.kh2_base_address + address)


def kh2_read_int(self, address):
    """Reads 4 bytes"""
    return self.kh2.read_int(self.kh2_base_address + address)


def kh2_write_int(self, address, value):
    """Writes 4 bytes"""
    self.kh2.write_int(self.kh2_base_address + address, value)


def kh2_read_longlong(self, address):
    """Reads 8 bytes"""
    return self.kh2.read_longlong(self.kh2_base_address + address)


def kh2_read_string(self, address, length):
    """Reads length amount of bytes"""
    return self.kh2.read_string(self.kh2_base_address + address, length)


def kh2_write_bytes(self, address, value):
    return self.kh2.write_bytes(self.kh2_base_address + address, bytes(value))


def kh2_return_base_address(self):
    return self.kh2_base_address
