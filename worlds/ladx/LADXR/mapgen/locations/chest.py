from .base import LocationBase
from ..tileset import solid_tiles, open_tiles, walkable_tiles
from ...roomEditor import RoomEditor
from ...locations.all import HeartPiece, Chest as ChestLocation
import random


class Chest(LocationBase):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)
        room.tiles[x + y * 10] = 0xA0

    def connect_logic(self, logic_location):
        logic_location.add(ChestLocation(self.room.x + self.room.y * 16))

    def get_item_pool(self):
        return {None: 1}

    @staticmethod
    def check_possible(room, reachable_map):
        # Check if we can potentially place a chest here, and what the best spot would be.
        options = []
        for y in range(1, 6):
            for x in range(1, 9):
                if room.tiles[x + y * 10 - 10] not in solid_tiles: # Chest needs to be against a "wall" at the top
                    continue
                if room.tiles[x + y * 10] not in walkable_tiles or room.tiles[x + y * 10 + 10] not in walkable_tiles:
                    continue
                if room.tiles[x - 1 + y * 10] not in solid_tiles and room.tiles[x - 1 + y * 10 + 10] not in open_tiles:
                    continue
                if room.tiles[x + 1 + y * 10] not in solid_tiles and room.tiles[x + 1 + y * 10 + 10] not in open_tiles:
                    continue
                idx = room.x * 10 + x + (room.y * 8 + y) * reachable_map.w
                if reachable_map.area[idx] == -1:
                    continue
                options.append((reachable_map.distance[idx], x, y))
        if not options:
            return None
        options.sort(reverse=True)
        options = [(x, y) for d, x, y in options if d > options[0][0] - 4]
        return random.choice(options)


class FloorItem(LocationBase):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)

    def update_room(self, rom, re: RoomEditor):
        re.entities.append((self.x, self.y, 0x35))

    def connect_logic(self, logic_location):
        logic_location.add(HeartPiece(self.room.x + self.room.y * 16))

    def get_item_pool(self):
        return {None: 1}

    @staticmethod
    def check_possible(room, reachable_map):
        # Check if we can potentially place a floor item here, and what the best spot would be.
        options = []
        for y in range(1, 7):
            for x in range(1, 9):
                if room.tiles[x + y * 10] not in walkable_tiles:
                    continue
                idx = room.x * 10 + x + (room.y * 8 + y) * reachable_map.w
                if reachable_map.area[idx] == -1:
                    continue
                options.append((reachable_map.distance[idx], x, y))
        if not options:
            return None
        options.sort(reverse=True)
        options = [(x, y) for d, x, y in options if d > options[0][0] - 4]
        return random.choice(options)
