# a tile is 32 bytes representing an 8x8 array of palette color indices

# tile layout example:
# 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
# 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f

# row 1 of the tile are bytes:
# 0x02, 0x03
# 0x12, 0x13

# 0x02 = 0000 0010
# 0x03 = 0000 0011
# 0x12 = 0001 0010
# 0x13 = 0001 0011

# 0101 = 5
# 1111 = 15
# 0000 = 0
# 0000 = 0

# 0011 = 3
# 0000 = 0
# 0000 = 0
# 0000 = 0

# row 1 of the tile is color ids: 5 15 0 0 3 0 0 0

# 1100 1000 = 0xc8
# 0100 1000 = 0x48
# 1100 0000
# 0100 0000

# row 0 is bytes 0x00, 0x01, 0x10, 0x11
# row 2 is bytes 0x04, 0x05, 0x14, 0x15
# etc...

class SpriteTile:
    ROW_COUNT = 8
    COL_COUNT = 8
    DATA_SIZE = 32

    row_offsets = [
        0,
        1,
        (DATA_SIZE // 2),
        (DATA_SIZE // 2) + 1,
    ]

    def __init__(self, data = None):
        self.colors = [[0 for x in range(self.COL_COUNT)] for y in range(self.ROW_COUNT)]
        if data is not None:
            self.data = data

    @property
    def data(self):
        tile_bytes = [0x00] * self.DATA_SIZE

        for row_index in range(self.ROW_COUNT):
            for col_index in range(self.COL_COUNT):
                color = self.colors[row_index][col_index]
                dest_bit = (self.COL_COUNT - col_index) - 1

                for byte_index in range(len(self.row_offsets)):
                    tile_bytes[row_index * 2 + self.row_offsets[byte_index]] |= (((color >> byte_index) & 1) << dest_bit)

        return tile_bytes

    @data.setter
    def data(self, new_data):
        for row_index in range(self.ROW_COUNT):
            row_bytes = []
            for byte_index in range(len(self.row_offsets)):
                row_bytes.append(new_data[row_index * 2 + self.row_offsets[byte_index]])

            for col_index in range(self.COL_COUNT):
                color = 0x00
                source_bit = (self.COL_COUNT - col_index) - 1

                for bit_index, byte in enumerate(row_bytes):
                    self.colors[row_index][col_index] |= (((byte >> source_bit) & 1) << bit_index)

    def color(self, x, y):
        # (0, 0) is top left of tile
        return self.colors[y][x]

    def __str__(self):
        result = ""
        for row in self.colors:
            result += "["
            for color in row:
                result += f"{color:>2},"
            result = result[:-1] + "]\n"
        return result[:-1]
