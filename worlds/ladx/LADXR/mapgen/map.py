import random
from .tileset import solid_tiles, open_tiles
from ..locations.items import *


PRIMARY_ITEMS = [POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA, FEATHER, SHOVEL, MAGIC_POWDER, BOMB, SWORD, FLIPPERS, SONG1]
SECONDARY_ITEMS = [BOOMERANG, RED_TUNIC, BLUE_TUNIC, MAX_POWDER_UPGRADE, MAX_BOMBS_UPGRADE, MAX_ARROWS_UPGRADE, GEL]

HORIZONTAL = 0
VERTICAL = 1


class RoomEdge:
    def __init__(self, direction):
        self.__solid = False
        self.__open_range = None
        self.direction = direction
        self.__open_min = 2 if direction == HORIZONTAL else 1
        self.__open_max = 8 if direction == HORIZONTAL else 7

    def force_solid(self):
        self.__open_min = -1
        self.__open_max = -1
        self.__open_range = None
        self.__solid = True

    def set_open_min(self, value):
        if self.__open_min < 0:
            return
        self.__open_min = max(self.__open_min, value)

    def set_open_max(self, value):
        if self.__open_max < 0:
            return
        self.__open_max = min(self.__open_max, value)

    def set_solid(self):
        self.__open_range = None
        self.__solid = True

    def can_open(self):
        return self.__open_min > -1

    def set_open(self):
        cnt = random.randint(1, self.__open_max - self.__open_min)
        if random.randint(1, 100) < 50:
            cnt = 1
        offset = random.randint(self.__open_min, self.__open_max - cnt)
        self.__open_range = (offset, offset + cnt)
        self.__solid = False

    def is_solid(self):
        return self.__solid

    def get_open_range(self):
        return self.__open_range

    def seed(self, wfc, x, y):
        for offset, cell in self.__cells(wfc, x, y):
            if self.__open_range and self.__open_range[0] <= offset < self.__open_range[1]:
                cell.init_options.intersection_update(open_tiles)
            elif self.__solid:
                cell.init_options.intersection_update(solid_tiles)

    def __cells(self, wfc, x, y):
        if self.direction == HORIZONTAL:
            for n in range(1, 9):
                yield n, wfc.cell_data[(x + n, y)]
        else:
            for n in range(1, 7):
                yield n, wfc.cell_data[(x, y + n)]


class RoomInfo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tileset_id = "basic"
        self.room_type = None
        self.tiles = None
        self.edge_left = None
        self.edge_up = None
        self.edge_right = RoomEdge(VERTICAL)
        self.edge_down = RoomEdge(HORIZONTAL)
        self.room_left = None
        self.room_up = None
        self.room_right = None
        self.room_down = None
        self.locations = []
        self.entities = []

    def __repr__(self):
        return f"Room<{self.x} {self.y}>"


class Map:
    def __init__(self, w, h, tilesets):
        self.w = w
        self.h = h
        self.tilesets = tilesets
        self.__rooms = [RoomInfo(x, y) for y in range(h) for x in range(w)]
        for x in range(w):
            for y in range(h):
                room = self.get(x, y)
                if x == 0:
                    room.edge_left = RoomEdge(VERTICAL)
                else:
                    room.edge_left = self.get(x - 1, y).edge_right
                if y == 0:
                    room.edge_up = RoomEdge(HORIZONTAL)
                else:
                    room.edge_up = self.get(x, y - 1).edge_down
                if x > 0:
                    room.room_left = self.get(x - 1, y)
                if x < w - 1:
                    room.room_right = self.get(x + 1, y)
                if y > 0:
                    room.room_up = self.get(x, y - 1)
                if y < h - 1:
                    room.room_down = self.get(x, y + 1)
        for x in range(w):
            self.get(x, 0).edge_up.set_solid()
            self.get(x, h-1).edge_down.set_solid()
        for y in range(h):
            self.get(0, y).edge_left.set_solid()
            self.get(w-1, y).edge_right.set_solid()

    def __iter__(self):
        return iter(self.__rooms)

    def get(self, x, y) -> RoomInfo:
        assert 0 <= x < self.w and 0 <= y < self.h, f"{x} {y}"
        return self.__rooms[x + y * self.w]

    def get_tile(self, x, y):
        return self.get(x // 10, y // 8).tiles[(x % 10) + (y % 8) * 10]

    def get_item_pool(self):
        item_pool = {}
        for room in self.__rooms:
            for location in room.locations:
                print(room, location.get_item_pool(), location.__class__.__name__)
                for k, v in location.get_item_pool().items():
                    item_pool[k] = item_pool.get(k, 0) + v
        unmapped_count = item_pool.get(None, 0)
        del item_pool[None]
        for item in PRIMARY_ITEMS:
            if item not in item_pool:
                item_pool[item] = 1
                unmapped_count -= 1
        while item_pool[POWER_BRACELET] < 2:
            item_pool[POWER_BRACELET] = item_pool.get(POWER_BRACELET, 0) + 1
            unmapped_count -= 1
        while item_pool[SHIELD] < 2:
            item_pool[SHIELD] = item_pool.get(SHIELD, 0) + 1
            unmapped_count -= 1
        assert unmapped_count >= 0

        for item in SECONDARY_ITEMS:
            if unmapped_count > 0:
                item_pool[item] = item_pool.get(item, 0) + 1
                unmapped_count -= 1

        # Add a heart container per 10 items "spots" left.
        heart_piece_count = unmapped_count // 10
        unmapped_count -= heart_piece_count * 4
        item_pool[HEART_PIECE] = item_pool.get(HEART_PIECE, 0) + heart_piece_count * 4

        # Add the rest as rupees
        item_pool[RUPEES_50] = item_pool.get(RUPEES_50, 0) + unmapped_count
        return item_pool

    def dump(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.get(x, y).edge_right.is_solid():
                    print(" |", end="")
                elif self.get(x, y).edge_right.get_open_range():
                    print("  ", end="")
                else:
                    print(" ?", end="")
            print()
            for x in range(self.w):
                if self.get(x, y).edge_down.is_solid():
                    print("-+", end="")
                elif self.get(x, y).edge_down.get_open_range():
                    print(" +", end="")
                else:
                    print("?+", end="")
            print()
        print()


class MazeGen:
    UP = 0x01
    DOWN = 0x02
    LEFT = 0x04
    RIGHT = 0x08

    def __init__(self, the_map: Map):
        self.map = the_map
        self.visited = set()
        self.visit(0, 0)

    def visit(self, x, y):
        self.visited.add((x, y))
        neighbours = self.get_neighbours(x, y)
        while any((x, y) not in self.visited for x, y, d in neighbours):
            x, y, d = random.choice(neighbours)
            if (x, y) not in self.visited:
                if d == self.RIGHT and self.map.get(x, y).edge_left.can_open():
                    self.map.get(x, y).edge_left.set_open()
                elif d == self.LEFT and self.map.get(x, y).edge_right.can_open():
                    self.map.get(x, y).edge_right.set_open()
                elif d == self.DOWN and self.map.get(x, y).edge_up.can_open():
                    self.map.get(x, y).edge_up.set_open()
                elif d == self.UP and self.map.get(x, y).edge_down.can_open():
                    self.map.get(x, y).edge_down.set_open()
                self.visit(x, y)

    def get_neighbours(self, x, y):
        neighbours = []
        if x > 0:
            neighbours.append((x - 1, y, self.LEFT))
        if x < self.map.w - 1:
            neighbours.append((x + 1, y, self.RIGHT))
        if y > 0:
            neighbours.append((x, y - 1, self.UP))
        if y < self.map.h - 1:
            neighbours.append((x, y + 1, self.DOWN))
        return neighbours
