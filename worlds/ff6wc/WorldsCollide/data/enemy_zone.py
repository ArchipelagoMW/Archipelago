# on world maps enemy zones are regions of world map and contain 4 packs each
# each non-world map corresponds to one enemy zone and has one pack

class EnemyZone():
    ENCOUNTER_RATES = {0 : "Normal", 1 : "Lower", 2 : "Higher"}
    NORMAL_ENCOUNTER_RATE, LOW_ENCOUNTER_RATE, HIGH_ENCOUNTER_RATE = range(3)

    def __init__(self, rom, id):
        self.rom = rom

        self.set_id(id)
        self.read()

    def set_id(self, id):
        self.id = id
        self.data_addr = self.DATA_START + self.id * self.DATA_SIZE

        # encounter rates are 2 bits per pack
        self.rate_addr = self.ENCOUNTER_RATE_START + (self.id // (4 // self.PACK_COUNT))

        # when a zone has 1 pack it only uses 2 bits, so one byte has the rate for 4 zones
        #   e.g. zone 0 rate bits are bits 0 and 1 in byte 0, zone 1 bits 2, 3 in byte 0, ..., zone 4 bits bits 0, 1 in byte 1, etc.
        # when 2 packs in a zone, one byte has the rate for 2 zones
        #   e.g. zone 0 rate bits are bits 0, 1, and 2, 3 in byte 0, zone 1 bits 4, 5, 6, 7 in byte 0, zone 2 bits 0-3 in byte 1, etc.
        # when 4 packs in a zone, one byte is used by the zone
        #   e.g. zone 0 rate bits are bits 0, 1 and 2, 3, and 4, 5 and 6, 7 in byte 0, zone 1 are the same bits in byte 1, etc.
        # therefore, need to take into account zone id for zones with fewer than 4 packs to know which bits to start at
        self.rate_bits_start = (self.id % (4 // self.PACK_COUNT)) * (self.PACK_COUNT * 2)

    def read(self):
        self.packs = []
        self.encounter_rates = []

        rate_byte = self.rom.get_byte(self.rate_addr)
        for x in range(self.PACK_COUNT):
            self.packs.append(self.rom.get_byte(self.data_addr + x))

            rate_bits_start = self.rate_bits_start + x * 2
            self.encounter_rates.append((rate_byte >> rate_bits_start) & 0x3)

    def write(self):
        # TODO write out encounter rate
        for x in range(self.PACK_COUNT):
            self.rom.set_byte(self.data_addr + x, self.packs[x])

    def print(self):
        print(f"{self.id}: ", end = '')
        for x in range(self.PACK_COUNT):
            print(f"{self.packs[x]}", end = ' -> ')
            print(f"{self.ENCOUNTER_RATES[self.encounter_rates[x]]}", end = ", ")
        print()

class WOBZone(EnemyZone):
    DATA_SIZE = 4
    DATA_START = 0xf5400

    ENCOUNTER_RATE_START = 0xf5800

    PACK_COUNT = 4

    WOB = True
    WOR = False
    MAP = False

class WORZone(EnemyZone):
    DATA_SIZE = 4
    DATA_START = 0xf5500

    ENCOUNTER_RATE_START = 0xf5840

    PACK_COUNT = 4

    WOB = False
    WOR = True
    MAP = False

class MapZone(EnemyZone):
    DATA_SIZE = 1
    DATA_START = 0xf5600

    ENCOUNTER_RATE_START = 0xf5880

    PACK_COUNT = 1

    WOB = False
    WOR = False
    MAP = True
