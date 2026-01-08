class ShortMapExit():
    DATA_SIZE = 0x06

    def __init__(self):
        self.x = 0
        self.y = 0

    def from_data(self, data):
        assert(len(data) == self.DATA_SIZE)

        self.x = data[0]
        self.y = data[1]
        self.dest_map = data[2] | (data[3] & 0x01) << 8
        self.unknown = data[3] & 0xfe
        self.dest_x = data[4]
        self.dest_y = data[5]

    def to_data(self):
        data = [0x00] * self.DATA_SIZE

        data[0] = self.x
        data[1] = self.y
        data[2] = self.dest_map & 0xff
        data[3] = ((self.dest_map & 0x100) >> 8) | self.unknown
        data[4] = self.dest_x
        data[5] = self.dest_y

        return data

    def print(self):
        print("{}, {} -> {}: {}, {} ({})".format(self.x, self.y, hex(self.dest_map), self.dest_x, self.dest_y, hex(self.unknown)))

class LongMapExit():
    DATA_SIZE = 0x07

    def __init__(self):
        self.x = 0
        self.y = 0

    def from_data(self, data):
        assert(len(data) == self.DATA_SIZE)

        self.x = data[0]
        self.y = data[1]
        self.size = data[2] & 0x7f
        self.direction = data[2] & 0x80 # horizontal/vertical
        self.dest_map = data[3] | (data[4] & 0x01) << 8
        self.unknown = data[4] & 0xfe
        self.dest_x = data[5]
        self.dest_y = data[6]

    def to_data(self):
        data = [0x00] * self.DATA_SIZE

        data[0] = self.x
        data[1] = self.y
        data[2] = self.size | self.direction
        data[3] = self.dest_map & 0xff
        data[4] = ((self.dest_map & 0x100) >> 8) | self.unknown
        data[5] = self.dest_x
        data[6] = self.dest_y

        return data

    def print(self):
        print("{}, {} {}, {} -> {}: {}, {}".format(self.x, self.y, self.size, self.direction, hex(self.dest_map), self.dest_x, self.dest_y))
