'''
A BytesPatch object is like a patch() block, except instead of reading
the patch data hex codes from text, it uses a provided bytes object,
mainly so that scripts using F4C as a module do not necessarily have
to encode a raw patch into a string to pass to F4C just so that F4C
can convert it back to bytes.
'''

from . import compile_common

class BytesPatch:
    def __init__(self, data, *, unheadered_address=None, headered_address=None, bus_address=None):
        self.data = data
        self.unheadered_address = unheadered_address
        self.headered_address = headered_address
        self.bus_address = bus_address

        if unheadered_address is None and headered_address is None and bus_address is None:
            raise compile_common.BuildError('BytesPatch requires a rom address to be specified')

    def get_unheadered_address(self):
        if self.unheadered_address is not None:
            addr = self.unheadered_address
        elif self.headered_address is not None:
            addr = self.headered_address - 0x200
        elif self.bus_address is not None:
            addr = compile_common.snes_to_rom_address(self.bus_address)
        else:
            raise compile_common.BuildError('BytesPatch requires a rom address to be specified')

        return addr
