# world map event modifications change the world map if an event bit is set
# e.g. if event bit 0x9e (floating continent) is set the sealed gate is removed

class WorldMapEventModification:
    DATA_SIZE = 0x04
    DATA_START_ADDR = 0xef600

    def __init__(self, rom, id):
        self.rom = rom

        self.set_id(id)
        self.read()

    def set_id(self, id):
        self.id = id
        self.data_addr = self.DATA_START_ADDR + self.id * self.DATA_SIZE

    def read(self):
        data = self.rom.get_bytes(self.data_addr, self.DATA_SIZE)
        self.event_bit = int.from_bytes(data[:2], "little")
        self.chunk_addr = int.from_bytes(data[2:], "little") # offset from 0xcef600

    def write(self):
        data = [0x00] * self.DATA_SIZE
        data[:2] = self.event_bit.to_bytes(2, "little")
        data[2:] = self.chunk_addr.to_bytes(2, "little")
        self.rom.set_bytes(self.data_addr, data)

    def print(self):
        print(f"{self.id:2} event bit: 0x{self.event_bit:04x} chunk addr: 0x{self.DATA_START_ADDR + self.chunk_addr:x}")
