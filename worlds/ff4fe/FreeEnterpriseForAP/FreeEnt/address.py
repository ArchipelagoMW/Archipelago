class MemoryAddress:
    def __init__(self, snes_address):
        self._snes_address = snes_address
    
    def get_bus(self):
        return self._snes_address
    
    def get_unheadered(self):
        bank = (self._snes_address >> 16) & 0xFF
        addr = (self._snes_address & 0xFFFF)
        if bank == 0x7E or bank == 0x7F:
            raise ValueError("Cannot convert SNES address {:X} to ROM address : address is WRAM".format(self._snes_address))
        if bank >= 0x80:
            bank -= 0x80
        if addr < 0x8000:
            if bank >= 0x40 and bank <= 0x6F:
                addr += 0x8000
            else:
                raise ValueError("Cannot convert SNES address {:X} to ROM address : this address does not map to ROM".format(self._snes_address))
        if not (bank & 0x01):
            addr -= 0x8000
        bank = (bank >> 1)
        return ((bank << 16) | addr)
    
    def get_headered(self):
        return self.get_unheadered_address() + 0x200

    def offset(self, offset):
        # NOTE: naive; will not support crossing bank boundary
        return MemoryAddress(self._snes_address + offset)

    def __repr__(self):
        return f'MemoryAddress({self._snes_address >> 16:02X}:{self._snes_address & 0xFFFF:04X})'

def BusAddress(address):
    return MemoryAddress(address)

def UnheaderedAddress(address):
    bank = address >> 15
    addr = (address & 0x7FFF) + 0x8000
    return MemoryAddress((bank << 16) + addr)

def HeaderedAddress(address):
    return UnheaderedAddress(address - 0x200)
