class Chest():
    EMPTY, MONSTER, ITEM, GOLD, UNUSED = (0x08, 0x20, 0x40, 0x80, 0xfe)
    MAX_GOLD_VALUE = 2 ** 8 - 1 # 1 byte for chest contents, 2^8 - 1 max gold value

    def __init__(self, id, data):
        self.id = id

        self.x          = data[0]
        self.y          = data[1]
        self.bit        = data[2]
        self.bit       |= (data[3] & 0x01) << 8
        self._type      = (data[3] & 0xfe)
        self.contents   = data[4]
        # for monsters, contents = pack id - 256
        # for gold, contents = amount of gp / 100

    def data(self):
        from ..data.chests import Chests
        data = [0x00] * Chests.DATA_SIZE

        data[0]     = self.x
        data[1]     = self.y
        data[2]     = (self.bit & 0xff)
        data[3]     = (self.bit & 0x100) >> 8
        data[3]    |= self.type
        data[4]     = self.contents

        return data

    def randomize_gold(self):
        from random import randint
        self.contents = randint(1, self.MAX_GOLD_VALUE)

    def contains(self, contents_type, contents):
        return self.type == contents_type and self.contents == contents

    @property
    def type(self):
        if self._type == self.UNUSED:
            return self.UNUSED
        if self._type == self.EMPTY:
            return self.EMPTY
        if self._type == self.MONSTER:
            return self.MONSTER
        if self._type == self.ITEM:
            return self.ITEM
        if self._type == self.GOLD:
            return self.GOLD
        raise ValueError(f"Chest.type getter: unknown type {hex(self._type)}")

    @type.setter
    def type(self, value):
        if value not in (self.EMPTY, self.MONSTER, self.ITEM, self.GOLD, self.UNUSED):
            raise ValueError(f"Chest.type setter: unknown type {hex(value)}")
        self._type = value

    def get_type_string(self):
        if self.type == self.EMPTY:
            return "Empty"
        elif self.type == self.GOLD:
            return "Gold"
        elif self.type == self.MONSTER:
            return "Monster"
        elif self.type == self.ITEM:
            return "Item"
        elif self.type == self.UNUSED:
            return "Unused"
        return "Unknown"

    def print(self):
        print("{}: ({}, {}), {}, {}, {}".format(self.id, self.x, self.y, self.bit, hex(self.type), self.contents), end = ' ')
        print(self.get_type_string())
