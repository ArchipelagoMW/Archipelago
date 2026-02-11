# Char  | Byte order    | Size     | Alignment
#- @    | native        | native   | native
#- =    | native        | standard | none
#- <    | little-endian | standard | none
#- >    | big-endian    | standard | none
#- !    | network       | standard | none

from collections import namedtuple
import logging
import struct
import typing
logger = logging.getLogger("Client")

class ParseField(object):
    count = 1
    field_type = 'B'
    def __init__(self, format_str, count=1):
        if len(format_str) > 1:
            self.field_type= format_str[-1]
            self.count = int(format_str[:-1])
        else:
            self.field_type = format_str
            self.count = count

FieldRecord = namedtuple('FieldRecord',['name', 'type', 'index', 'count', 'length', 'offset'])

class _array_proxy(object):
    _sram: 'SegaSRAM'
    _fr: FieldRecord
    def __init__(self, sram, fr):
        super().__setattr__("_sram", sram)
        super().__setattr__("_fr", fr)

    def __getitem__(self, key) -> typing.Any:
        assert(self._fr.count > key)
        return self._sram._fields[self._fr.offset+key]

    def __setitem__(self, key, value):
        assert(self._fr.count > key)
        self._sram.stage(self._fr.offset+key, [value])

class _fields_proxy(object):
    _sram: 'SegaSRAM'
    def __init__(self, sram):
        super().__setattr__("_sram", sram)

    def __getattribute__(self, name) -> typing.Any|list:
        sram = object.__getattribute__(self, '_sram')
        if name == '_sram':
            return sram
        if name in sram.field_map:
            k = sram.field_map[name]
            if k.count == 1:
                return sram._fields[k.offset]
            else:
                return _array_proxy(sram, k)
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        k = self._sram.field_map[name]
        assert(k.count == 1)
        self._sram.stage(k.offset, [value])

    def __getitem__(self, key):
        if isinstance(key,int):
            return self.__getattribute__(self._sram.field_table[key].name)
        else:
            return self.__getattribute__(self._sram.field_map[key].name)

    def __setitem__(self, key, value):
        if isinstance(key,int):
            return self.__setattr__(self._sram.field_table[key].name, value)
        else:
            return self.__setattr__(self._sram.field_map[key].name, value)

class DataOrder(_fields_proxy):
    pass

class BigEndian(DataOrder):
    pass

class LittleEndian(DataOrder):
    pass

class NetworkEndian(DataOrder):
    pass

class SegaSRAM(object):
    _raw: typing.List[bytes]
    clean_data: bytes
    byte_count: int
    ram_type = 0
    format: str = ""
    _fields = ()
    _fieldproxy: DataOrder
    staged: typing.List[typing.Tuple]
    extra_addresses: typing.List[typing.Tuple[int,int,str]]
    extra_data: typing.List[bytes]
    field_table: list[FieldRecord]
    field_map: dict[str,FieldRecord]
    _read_callable: typing.Callable
    _write_callable: typing.Callable

    _struct_type_map = {'x': None, 'c': int, 'b': int, 'B': int, '?': bool,
    'h': int, 'H': int, 'i': int, 'I': int, 'l': int, 'L': int, 'q': int, 'Q': int,
    'n': int, 'N': int, 'e': float, 'f': float, 'd': float, 's': bytes, 'p': bytes, 'P': int}

    def __init__(self, read_callable, write_callable, ram_type=0):
        '''Ram_type 0 for even addresses (FF__), 1 for odd addresses (__FF), 2 for both (FFFF)'''
        self._raw = []
        self.ram_type = ram_type
        self.staged = []
        self.extra_addresses = []
        self.extra_data = []
        self._fieldproxy = _fields_proxy(self)
        self._read_callable = read_callable
        self._write_callable = write_callable

    @property
    def fields(self):
        return self._fieldproxy

    @fields.setter
    def fields(self, format: type[DataOrder]):
        logger.info(f"Setting {format=}")
        newformat = ""
        newtable = []
        # So, first the endian
        assert(issubclass(format, DataOrder))
        match format.__class__:
            case BigEndian():
                newformat += ">"
            case LittleEndian():
                newformat += "<"
            case NetworkEndian():
                newformat += "!"
        offset = 0
        i = 0
        for k,v in format.__dict__.items():
            if isinstance(v, ParseField):
                #logger.info(f"{k} is {v}")
                if v.field_type in 'sp':
                    fr = FieldRecord(k, self._struct_type_map[v.field_type], i, 1, v.count, offset)
                    offset += 1
                else:
                    fr = FieldRecord(k, self._struct_type_map[v.field_type], i, v.count, 1, offset)
                    offset += v.count
                i += 1
                newformat += f"{v.count if v.count > 1 else ''}{v.field_type}"
                newtable.append(fr)
        self.format = newformat
        self.layout = format
        self._fieldproxy = format(self)
        self.field_table = newtable
        self.field_map = {i.name:i for i in newtable}
        self.byte_count = struct.calcsize(newformat)*(1 if self.ram_type in [2,3] else 2)

    async def detect_type(self, ctx, magic: bytes, address=0x0):
        '''Magic is the sequence of bytes to look for at the address'''
        tests = []
        addresses = []
        magic_odd = len(magic)%2
        address_odd = address%2
        # First assume the address is console side, including the dead bytes
        magic_len = len(magic)*2 # Double length for dead bytes
        addresses.append((address-address_odd, magic_len, "SRAM"))
        # We'll do that again, only this time we'll assume the address excludes the dead bytes
        addresses.append((address*2, magic_len, "SRAM"))
        # Maybe it's 16-bit?
        addresses.append((address-address_odd, len(magic)+address_odd+magic_odd, "SRAM"))
        data = await self._read_callable(ctx.bizhawk_ctx, addresses)
        # Now to test ways of mangling that
        tests.append((bytes([data[0][i] for i in range(0,len(data[0]), 2)]), 0)) # even bytes, include dead
        tests.append((bytes([data[0][i] for i in range(1,len(data[0]), 2)]), 1)) # odd bytes, include dead
        tests.append((bytes([data[1][i] for i in range(0,len(data[1]), 2)]), 0)) # even bytes, exclude dead
        tests.append((bytes([data[1][i] for i in range(1,len(data[1]), 2)]), 1)) # odd bytes, exclude dead
        tests.append((data[2][address_odd:len(magic)+address_odd], 2)) # both bytes, correct order
        swapped = [] # Both bytes, byte swapped... we don't actually support that right now.
        for i in range(0,len(data[2]), 2):
            swapped.extend([data[2][i+1],data[2][i]])
        if address_odd == 1:
            swapped.pop(0)
        tests.append((bytes(swapped[:len(magic)]),3))

        self.ram_type = -1 # So we can test detection failures
        for (test,result) in tests:
            #logger.info(f"{test=} {result=}")
            if test == magic:
                self.ram_type = result
                if self._fieldproxy is not None:
                    self.byte_count = struct.calcsize(self.format)*(1 if self.ram_type in [2,3] else 2)
                return

    async def read_bytes(self, ctx, clear_stage=True):
        if clear_stage:
            self.staged = []
        data = await self._read_callable(ctx.bizhawk_ctx, [(0x0, self.byte_count, "SRAM"),]+self.extra_addresses)
        self._raw = data[0]
        self.extra_data = data[1:]
        # Because of 8bit sram stupidity, we're probably going to need to unpack this by dropping every other byte.
        # So:
        if self.ram_type == 0:
          self.clean_data = bytes([data[0][i] for i in range(0,len(data[0]), 2)])
        elif self.ram_type == 1:
          self.clean_data = bytes([data[0][i] for i in range(1,len(data[0]), 2)])
        elif self.ram_type == 2:
          self.clean_data = data[0]
        elif self.ram_type == 3:
          # I hate this so much.  This will likely fail if your data and format aren't properly word aligned
          tdata = []
          for i in range(0,len(data[0]), 2):
            tdata.extend([data[0][i+1],data[0][i]])
          self.clean_data = bytes(tdata)
        self._fields = struct.unpack(self.format,self.clean_data)
        #seed_name = ''.join([chr(c) for c in clean_data[-20:]])
        #logger.info(f"Data... {clean_data=} ({len(clean_data)=}) {seed_name=} {len(seed_name)=}")
        # We're only caring about the seed in the start.

    async def full_write(self, ctx, data, clear_stage=True):
        if clear_stage:
            self.staged = []
        self._fields = tuple(data)
        self.clean_data = struct.pack(self.format, *data)
        wrdata = []
        if self.ram_type == 0:
            for b in self.clean_data:
                wrdata.extend([b,0x0])
        elif self.ram_type == 1:
            for b in self.clean_data:
                wrdata.extend([0x0,b])
        elif self.ram_type == 2:
            wrdata = self.clean_data
        elif self.ram_type == 3:
            # I hate this so much.  This will likely fail if your data and format aren't properly word aligned
            wrdata = []
            for i in range(0,len(self.clean_data), 2):
              wrdata.extend([self.clean_data[i+1],self.clean_data[i]])
        self._raw = bytes(wrdata)
        await self._write_callable(ctx.bizhawk_ctx, [(0, wrdata, "SRAM")])

    def stage(self, offset, data):
        for i in range(0,len(data)):
            if self._fields[offset+i] != data[i]:
                self.staged.append((offset+i, data[i]))

    async def commit(self, ctx):
        if len(self.staged) > 0:
          out = list(self._fields)
          while len(self.staged):
              u = self.staged.pop(0)
              out[u[0]] = u[1]
          self._fields = tuple(out)
          self.clean_data = struct.pack(self.format, *out)
          wrdata = []
          if self.ram_type == 0:
              for b in self.clean_data:
                  wrdata.extend([b,0x0])
          elif self.ram_type == 1:
              for b in self.clean_data:
                  wrdata.extend([0x0,b])
          elif self.ram_type == 2:
              wrdata = self.clean_data
          elif self.ram_type == 3:
              # I hate this so much.  This will likely fail if your data and format aren't properly word aligned
              wrdata = []
              for i in range(0,len(self.clean_data), 2):
                  wrdata.extend([self.clean_data[i+1],self.clean_data[i]])
          tempraw = bytes(wrdata)
          patches = []
          for i,bs in enumerate(zip(self._raw, tempraw)):
              if bs[0] != bs[1]:
                  logger.debug(f"{i=} {bs=}")
                  patches.append([i,[bs[1]], "SRAM"])
          self._raw = tempraw
          await self._write_callable(ctx.bizhawk_ctx,patches)
