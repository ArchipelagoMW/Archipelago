
# Map grids are indexed like so: map_grid[x][y]

class MapGrid:
    def __init__(self, linear_tiles):
        self._grid = []
        for x in range(32):
            column = [linear_tiles[i] for i in range(x, len(linear_tiles), 32)]
            self._grid.append(column)

    def __getitem__(self, k):
        return self._grid[k]

    def encode(self):
        runs = []
        for y in range(32):
            for x in range(32):
                tile = self[x][y]
                if not runs or runs[-1][0] != tile or runs[-1][1] == 0xFF:
                    runs.append([tile, 1])
                else:
                    runs[-1][1] += 1

        byte_list = []
        for run in runs:
            if run[1] > 1:
                byte_list.append(run[0] | 0x80)
                byte_list.append(run[1] - 1)
            else:
                byte_list.append(run[0])

        return byte_list

def decode(byte_list):
    byte_list = list(byte_list)
    linear_tiles = []
    while(byte_list):
        b = byte_list.pop(0)
        if b & 0x80:
            length = byte_list.pop(0) + 1
            linear_tiles.extend([b & 0x7F] * length)
        else:
            linear_tiles.append(b)

    linear_tiles = linear_tiles[:0x400]
    return MapGrid(linear_tiles)

