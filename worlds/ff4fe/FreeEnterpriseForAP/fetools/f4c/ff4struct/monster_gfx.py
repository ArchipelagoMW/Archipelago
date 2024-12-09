class MonsterGfx:
    def __init__(self):
        self.size = 0
        self.palette = 0
        self.pointer = 0

    def encode(self):
        return [self.size, self.palette, self.pointer & 0xff, (self.pointer >> 8) & 0xff]

def decode(byte_list):
    mgfx = MonsterGfx()
    mgfx.size = byte_list[0]
    mgfx.palette = byte_list[1]
    mgfx.pointer = byte_list[2] | (byte_list[3] << 8)
    return mgfx
