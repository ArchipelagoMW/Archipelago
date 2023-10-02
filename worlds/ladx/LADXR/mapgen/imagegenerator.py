from .tileset import open_tiles, solid_tiles


def tx(x):
    return x * 16 + x // 10


def ty(y):
    return y * 16 + y // 8


class ImageGen:
    def __init__(self, tilesets, the_map, rom):
        self.tilesets = tilesets
        self.map = the_map
        self.rom = rom
        self.image = None
        self.draw = None
        self.count = 0
        self.enabled = False
        self.__tile_cache = {}

    def on_step(self, wfc, cur=None, err=None):
        if not self.enabled:
            return
        if self.image is None:
            import PIL.Image
            import PIL.ImageDraw
            self.image = PIL.Image.new("RGB", (self.map.w * 161, self.map.h * 129))
            self.draw = PIL.ImageDraw.Draw(self.image)
        self.image.paste(0, (0, 0, wfc.w * 16, wfc.h * 16))
        for y in range(wfc.h):
            for x in range(wfc.w):
                cell = wfc.cell_data[(x, y)]
                if len(cell.options) == 1:
                    tile_id = next(iter(cell.options))
                    room = self.map.get(x//10, y//8)
                    tile = self.get_tile(room.tileset_id, tile_id)
                    self.image.paste(tile, (tx(x), ty(y)))
                else:
                    self.draw.text((tx(x) + 3, ty(y) + 3), f"{len(cell.options):2}", (255, 255, 255))
                    if cell.options.issubset(open_tiles):
                        self.draw.rectangle((tx(x), ty(y), tx(x) + 15, ty(y) + 15), outline=(0, 128, 0))
                    elif cell.options.issubset(solid_tiles):
                        self.draw.rectangle((tx(x), ty(y), tx(x) + 15, ty(y) + 15), outline=(0, 0, 192))
        if cur:
            self.draw.rectangle((tx(cur[0]),ty(cur[1]),tx(cur[0])+15,ty(cur[1])+15), outline=(0, 255, 0))
        if err:
            self.draw.rectangle((tx(err[0]),ty(err[1]),tx(err[0])+15,ty(err[1])+15), outline=(255, 0, 0))
        self.image.save(f"_map/tmp{self.count:08}.png")
        self.count += 1

    def get_tile(self, tileset_id, tile_id):
        tile = self.__tile_cache.get((tileset_id, tile_id), None)
        if tile is not None:
            return tile
        import PIL.Image
        tile = PIL.Image.new("L", (16, 16))
        tileset = self.get_tileset(tileset_id)
        metatile = self.rom.banks[0x1A][0x2749 + tile_id * 4:0x2749 + tile_id * 4+4]

        def draw(ox, oy, t):
            addr = (t & 0x3FF) << 4
            tile_data = self.rom.banks[t >> 10][addr:addr+0x10]
            for y in range(8):
                a = tile_data[y * 2]
                b = tile_data[y * 2 + 1]
                for x in range(8):
                    v = 0
                    bit = 0x80 >> x
                    if a & bit:
                        v |= 0x01
                    if b & bit:
                        v |= 0x02
                    tile.putpixel((ox+x,oy+y), (255, 192, 128, 32)[v])
        draw(0, 0, tileset[metatile[0]])
        draw(8, 0, tileset[metatile[1]])
        draw(0, 8, tileset[metatile[2]])
        draw(8, 8, tileset[metatile[3]])
        self.__tile_cache[(tileset_id, tile_id)] = tile
        return tile

    def get_tileset(self, tileset_id):
        subtiles = [0] * 0x100
        for n in range(0, 0x20):
            subtiles[n] = (0x0F << 10) + (self.tilesets[tileset_id].main_id << 4) + n
        for n in range(0x20, 0x80):
            subtiles[n] = (0x0C << 10) + 0x100 + n
        for n in range(0x80, 0x100):
            subtiles[n] = (0x0C << 10) + n

        addr = (0x000, 0x000, 0x2B0, 0x2C0, 0x2D0, 0x2E0, 0x2F0, 0x2D0, 0x300, 0x310, 0x320, 0x2A0, 0x330, 0x350, 0x360, 0x340, 0x370)[self.tilesets[tileset_id].animation_id or 3]
        for n in range(0x6C, 0x70):
            subtiles[n] = (0x0C << 10) + addr + n - 0x6C
        return subtiles
