from ..data import direction as direction

class NPC():
    DATA_SIZE = 0x09

    NO_MOVE, SCRIPT_MOVE, PLAYER_MOVE, RANDOM_MOVE, ACTIVATED_MOVE = range(5)
    SLOWEST, SLOW, FAST, FASTEST = range(4)

    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = direction.UP
        self.no_face_on_trigger = 0

        self.speed = 0
        self.movement = 0

        self.sprite = 0
        self.split_sprite = 0
        self.const_sprite = 0
        self.palette = 0
        self.vehicle = 0

        self.event_byte = 0
        self.event_bit = 0
        self.event_address = 0x5eb3 # event that just returns

        self.map_layer = 0
        self.background_scrolls = 0
        self.background_layer = 0

        self.unknown1 = 0
        self.unknown2 = 0

    def from_data(self, data):
        assert(len(data) == self.DATA_SIZE)

        event_addr = data[0] + (data[1] << 8) + ((data[2] & 0x03) << 16)
        self.event_address = event_addr

        self.palette = (data[2] & 0x1c) >> 2
        self.background_scrolls = (data[2] & 0x20) >> 5
        self.event_bit = (data[2] & 0xc0) >> 6
        self.event_bit += (data[3] & 0x01) << 2
        self.event_byte = (data[3] & 0xfe) >> 1
        self.x = data[4] & 0x7f
        self.no_face_on_trigger = (data[4] & 0x80) >> 7
        self.y = data[5] & 0x3f
        self.speed = (data[5] & 0xc0) >> 6
        self.sprite = data[6]
        self.movement = data[7] & 0x0f
        self.map_layer = (data[7] & 0x30) >> 4
        self.vehicle = (data[7] & 0xc0) >> 6
        self.direction = data[8] & 0x03
        self.const_sprite = (data[8] & 0x04) >> 2
        self.background_layer = (data[8] & 0x18) >> 3
        self.unknown1 = (data[8] & 0x20) >> 5
        self.split_sprite = (data[8] & 0x40) >> 6
        self.unknown2 = (data[8] & 0x80) >> 7

    def to_data(self):
        data = [0x00] * self.DATA_SIZE

        data[0] = self.event_address & 0xff

        data[1] = (self.event_address & 0xff00) >> 8

        data[2] = (self.event_address & 0x030000) >> 16
        data[2] |= self.palette << 2
        data[2] |= self.background_scrolls << 5
        data[2] |= (self.event_bit & 0x03) << 6

        data[3] = (self.event_bit & 0x04) >> 2
        data[3] |= self.event_byte << 1

        data[4] = self.x
        data[4] |= self.no_face_on_trigger << 7

        data[5] = self.y
        data[5] |= self.speed << 6

        data[6] = self.sprite

        data[7] = self.movement
        data[7] |= self.map_layer << 4
        data[7] |= self.vehicle << 6

        data[8] = self.direction
        data[8] |= self.const_sprite << 2
        data[8] |= self.background_layer << 3
        data[8] |= self.unknown1 << 5
        data[8] |= self.split_sprite << 6
        data[8] |= self.unknown2 << 7

        return data

    def set_event_address(self, address):
        from ..instruction.event import EVENT_CODE_START
        self.event_address = address - EVENT_CODE_START

    def print(self):
        print(" ".join("{}: {}".format(k, v) for k, v in vars(self).items()))
