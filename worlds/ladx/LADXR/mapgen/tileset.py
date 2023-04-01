from typing import Dict, Set
from ..roomEditor import RoomEditor


animated_tiles = {0x0E, 0x1B, 0x1E, 0x1F, 0x44, 0x91, 0xCF, 0xD0, 0xD1, 0xD2, 0xD9, 0xDC, 0xE9, 0xEB, 0xEC, 0xED, 0xEE, 0xEF}
entrance_tiles = {0xE1, 0xE2, 0xE3, 0xBA, 0xC6}

solid_tiles = set()
open_tiles = set()
walkable_tiles = set()
vertical_edge_tiles = set()
horizontal_edge_tiles = set()


class TileInfo:
    def __init__(self, key):
        self.key = key
        self.up = set()
        self.right = set()
        self.down = set()
        self.left = set()
        self.up_freq = {}
        self.right_freq = {}
        self.down_freq = {}
        self.left_freq = {}
        self.frequency = 0

    def copy(self):
        result = TileInfo(self.key)
        result.up = self.up.copy()
        result.right = self.right.copy()
        result.down = self.down.copy()
        result.left = self.left.copy()
        result.up_freq = self.up_freq.copy()
        result.right_freq = self.right_freq.copy()
        result.down_freq = self.down_freq.copy()
        result.left_freq = self.left_freq.copy()
        result.frequency = self.frequency
        return result

    def remove(self, tile_id):
        if tile_id in self.up:
            self.up.remove(tile_id)
            del self.up_freq[tile_id]
        if tile_id in self.down:
            self.down.remove(tile_id)
            del self.down_freq[tile_id]
        if tile_id in self.left:
            self.left.remove(tile_id)
            del self.left_freq[tile_id]
        if tile_id in self.right:
            self.right.remove(tile_id)
            del self.right_freq[tile_id]

    def update(self, other: "TileInfo", tile_filter: Set[int]):
        self.frequency += other.frequency
        self.up.update(other.up.intersection(tile_filter))
        self.down.update(other.down.intersection(tile_filter))
        self.left.update(other.left.intersection(tile_filter))
        self.right.update(other.right.intersection(tile_filter))
        for k, v in other.up_freq.items():
            if k not in tile_filter:
                continue
            self.up_freq[k] = self.up_freq.get(k, 0) + v
        for k, v in other.down_freq.items():
            if k not in tile_filter:
                continue
            self.down_freq[k] = self.down_freq.get(k, 0) + v
        for k, v in other.left_freq.items():
            if k not in tile_filter:
                continue
            self.left_freq[k] = self.left_freq.get(k, 0) + v
        for k, v in other.down_freq.items():
            if k not in tile_filter:
                continue
            self.right_freq[k] = self.right_freq.get(k, 0) + v

    def __repr__(self):
        return f"<{self.key}>\n U{[f'{n:02x}' for n in self.up]}\n R{[f'{n:02x}' for n in self.right]}\n D{[f'{n:02x}' for n in self.down]}\n L{[f'{n:02x}' for n in self.left]}>"


class TileSet:
    def __init__(self, *, main_id=None, animation_id=None):
        self.main_id = main_id
        self.animation_id = animation_id
        self.palette_id = None
        self.attr_bank = None
        self.attr_addr = None
        self.tiles: Dict[int, "TileInfo"] = {}
        self.all: Set[int] = set()

    def copy(self) -> "TileSet":
        result = TileSet(main_id=self.main_id, animation_id=self.animation_id)
        for k, v in self.tiles.items():
            result.tiles[k] = v.copy()
        result.all = self.all.copy()
        return result

    def remove(self, tile_id):
        self.all.remove(tile_id)
        del self.tiles[tile_id]
        for k, v in self.tiles.items():
            v.remove(tile_id)

    # Look at the "other" tileset and merge information about tiles known in this tileset
    def learn_from(self, other: "TileSet"):
        for key, other_info in other.tiles.items():
            if key not in self.all:
                continue
            self.tiles[key].update(other_info, self.all)

    def combine(self, other: "TileSet"):
        if other.main_id and not self.main_id:
            self.main_id = other.main_id
        if other.animation_id and not self.animation_id:
            self.animation_id = other.animation_id
        for key, other_info in other.tiles.items():
            if key not in self.all:
                self.tiles[key] = other_info.copy()
            else:
                self.tiles[key].update(other_info, self.all)
        self.all.update(other.all)


def loadTileInfo(rom) -> Dict[str, TileSet]:
    for n in range(0x100):
        physics_flag = rom.banks[8][0x0AD4 + n]
        if n == 0xEF:
            physics_flag = 0x01  # One of the sky tiles is marked as a pit instead of solid, which messes with the generation of sky
        if physics_flag in {0x00, 0x05, 0x06, 0x07}:
            open_tiles.add(n)
            walkable_tiles.add(n)
            vertical_edge_tiles.add(n)
            horizontal_edge_tiles.add(n)
        elif physics_flag in {0x01, 0x04, 0x60}:
            solid_tiles.add(n)
            vertical_edge_tiles.add(n)
            horizontal_edge_tiles.add(n)
        elif physics_flag in {0x08}:  # Bridge
            open_tiles.add(n)
            walkable_tiles.add(n)
        elif physics_flag in {0x02}:  # Stairs
            open_tiles.add(n)
            walkable_tiles.add(n)
            horizontal_edge_tiles.add(n)
        elif physics_flag in {0x03}:  # Entrances
            open_tiles.add(n)
        elif physics_flag in {0x30}:  # bushes/rocks
            open_tiles.add(n)
        elif physics_flag in {0x50}:  # pits
            open_tiles.add(n)
    world_tiles = {}
    for ry in range(0, 16):
        for rx in range(0, 16):
            tileset_id = rom.banks[0x3F][0x3F00 + rx + (ry << 4)]
            re = RoomEditor(rom, rx | (ry << 4))
            tiles = re.getTileArray()
            for y in range(8):
                for x in range(10):
                    tile_id = tiles[x+y*10]
                    world_tiles[(rx*10+x, ry*8+y)] = (tile_id, tileset_id, re.animation_id | 0x100)

    # Fix up wrong tiles
    world_tiles[(150, 24)] = (0x2A, world_tiles[(150, 24)][1], world_tiles[(150, 24)][2])  # Left of the raft house, a tree has the wrong tile.

    rom_tilesets: Dict[int, TileSet] = {}
    for (x, y), (key, tileset_id, animation_id) in world_tiles.items():
        if key in animated_tiles:
            if animation_id not in rom_tilesets:
                rom_tilesets[animation_id] = TileSet(animation_id=animation_id&0xFF)
            tileset = rom_tilesets[animation_id]
        else:
            if tileset_id not in rom_tilesets:
                rom_tilesets[tileset_id] = TileSet(main_id=tileset_id)
            tileset = rom_tilesets[tileset_id]
        tileset.all.add(key)
        if key not in tileset.tiles:
            tileset.tiles[key] = TileInfo(key)
        ti = tileset.tiles[key]
        ti.frequency += 1
        if (x, y - 1) in world_tiles:
            tile_id = world_tiles[(x, y - 1)][0]
            ti.up.add(tile_id)
            ti.up_freq[tile_id] = ti.up_freq.get(tile_id, 0) + 1
        if (x + 1, y) in world_tiles:
            tile_id = world_tiles[(x + 1, y)][0]
            ti.right.add(tile_id)
            ti.right_freq[tile_id] = ti.right_freq.get(tile_id, 0) + 1
        if (x, y + 1) in world_tiles:
            tile_id = world_tiles[(x, y + 1)][0]
            ti.down.add(tile_id)
            ti.down_freq[tile_id] = ti.down_freq.get(tile_id, 0) + 1
        if (x - 1, y) in world_tiles:
            tile_id = world_tiles[(x - 1, y)][0]
            ti.left.add(tile_id)
            ti.left_freq[tile_id] = ti.left_freq.get(tile_id, 0) + 1

    tilesets = {
        "basic": rom_tilesets[0x0F].copy()
    }
    for key, tileset in rom_tilesets.items():
        tilesets["basic"].learn_from(tileset)
    tilesets["mountains"] = rom_tilesets[0x3E].copy()
    tilesets["mountains"].combine(rom_tilesets[0x10B])
    tilesets["mountains"].remove(0xB6)  # Remove the raft house roof
    tilesets["mountains"].remove(0xB7)  # Remove the raft house roof
    tilesets["mountains"].remove(0x66)  # Remove the raft house roof
    tilesets["mountains"].learn_from(rom_tilesets[0x1C])
    tilesets["mountains"].learn_from(rom_tilesets[0x3C])
    tilesets["mountains"].learn_from(rom_tilesets[0x30])
    tilesets["mountains"].palette_id = 0x15
    tilesets["mountains"].attr_bank = 0x27
    tilesets["mountains"].attr_addr = 0x5A20

    tilesets["egg"] = rom_tilesets[0x3C].copy()
    tilesets["egg"].combine(tilesets["mountains"])
    tilesets["egg"].palette_id = 0x13
    tilesets["egg"].attr_bank = 0x27
    tilesets["egg"].attr_addr = 0x5620

    tilesets["forest"] = rom_tilesets[0x20].copy()
    tilesets["forest"].palette_id = 0x00
    tilesets["forest"].attr_bank = 0x25
    tilesets["forest"].attr_addr = 0x4000

    tilesets["town"] = rom_tilesets[0x26].copy()
    tilesets["town"].combine(rom_tilesets[0x103])
    tilesets["town"].palette_id = 0x03
    tilesets["town"].attr_bank = 0x25
    tilesets["town"].attr_addr = 0x4C00

    tilesets["swamp"] = rom_tilesets[0x36].copy()
    tilesets["swamp"].combine(rom_tilesets[0x103])
    tilesets["swamp"].palette_id = 0x0E
    tilesets["swamp"].attr_bank = 0x22
    tilesets["swamp"].attr_addr = 0x7400

    tilesets["beach"] = rom_tilesets[0x22].copy()
    tilesets["beach"].combine(rom_tilesets[0x102])
    tilesets["beach"].palette_id = 0x01
    tilesets["beach"].attr_bank = 0x22
    tilesets["beach"].attr_addr = 0x5000

    tilesets["water"] = rom_tilesets[0x3E].copy()
    tilesets["water"].combine(rom_tilesets[0x103])
    tilesets["water"].learn_from(tilesets["basic"])
    tilesets["water"].remove(0x7A)
    tilesets["water"].remove(0xC8)
    tilesets["water"].palette_id = 0x09
    tilesets["water"].attr_bank = 0x22
    tilesets["water"].attr_addr = 0x6400

    return tilesets
