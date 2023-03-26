from ..logic import Location, PEGASUS_BOOTS, SHOVEL
from .base import LocationBase
from ..tileset import solid_tiles, open_tiles, walkable_tiles
from ...roomEditor import RoomEditor
from ...assembler import ASM
from ...locations.all import Seashell
import random


class HiddenSeashell(LocationBase):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)
        if room.tiles[x + y * 10] not in (0x20, 0x5C):
            if random.randint(0, 1):
                room.tiles[x + y * 10] = 0x20  # rock
            else:
                room.tiles[x + y * 10] = 0x5C  # bush

    def update_room(self, rom, re: RoomEditor):
        re.entities.append((self.x, self.y, 0x3D))

    def connect_logic(self, logic_location):
        logic_location.add(Seashell(self.room.x + self.room.y * 16))

    def get_item_pool(self):
        return {None: 1}

    @staticmethod
    def check_possible(room, reachable_map):
        # Check if we can potentially place a hidden seashell here
        # First see if we have a nice bush or rock to hide under
        options = []
        for y in range(1, 7):
            for x in range(1, 9):
                if room.tiles[x + y * 10] not in {0x20, 0x5C}:
                    continue
                idx = room.x * 10 + x + (room.y * 8 + y) * reachable_map.w
                if reachable_map.area[idx] == -1:
                    continue
                options.append((reachable_map.distance[idx], x, y))
        if not options:
            # No existing bush, we can always add one. So find a nice spot
            for y in range(1, 7):
                for x in range(1, 9):
                    if room.tiles[x + y * 10] not in walkable_tiles:
                        continue
                    if room.tiles[x + y * 10] == 0x1E:  # ocean edge
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


class DigSeashell(LocationBase):
    MAX_COUNT = 6

    def __init__(self, room, x, y):
        super().__init__(room, x, y)
        if room.tileset_id == "beach":
            room.tiles[x + y * 10] = 0x08
            for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if room.tiles[x + ox + (y + oy) * 10] != 0x1E:
                    room.tiles[x + ox + (y + oy) * 10] = 0x24
        else:
            room.tiles[x + y * 10] = 0x04
            for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                room.tiles[x + ox + (y + oy) * 10] = 0x0A

    def update_room(self, rom, re: RoomEditor):
        re.entities.append((self.x, self.y, 0x3D))
        if rom.banks[0x03][0x2210] == 0xFF:
            rom.patch(0x03, 0x220F, ASM("cp $FF"), ASM(f"cp ${self.room.x | (self.room.y << 4):02x}"))
        elif rom.banks[0x03][0x2214] == 0xFF:
            rom.patch(0x03, 0x2213, ASM("cp $FF"), ASM(f"cp ${self.room.x | (self.room.y << 4):02x}"))
        elif rom.banks[0x03][0x2218] == 0xFF:
            rom.patch(0x03, 0x2217, ASM("cp $FF"), ASM(f"cp ${self.room.x | (self.room.y << 4):02x}"))
        elif rom.banks[0x03][0x221C] == 0xFF:
            rom.patch(0x03, 0x221B, ASM("cp $FF"), ASM(f"cp ${self.room.x | (self.room.y << 4):02x}"))
        elif rom.banks[0x03][0x2220] == 0xFF:
            rom.patch(0x03, 0x221F, ASM("cp $FF"), ASM(f"cp ${self.room.x | (self.room.y << 4):02x}"))
        elif rom.banks[0x03][0x2224] == 0xFF:
            rom.patch(0x03, 0x2223, ASM("cp $FF"), ASM(f"cp ${self.room.x | (self.room.y << 4):02x}"))

    def connect_logic(self, logic_location):
        logic_location.connect(Location().add(Seashell(self.room.x + self.room.y * 16)), SHOVEL)

    def get_item_pool(self):
        return {None: 1}

    @staticmethod
    def check_possible(room, reachable_map):
        options = []
        for y in range(1, 7):
            for x in range(1, 9):
                if room.tiles[x + y * 10] not in walkable_tiles:
                    continue
                if room.tiles[x - 1 + y * 10] not in walkable_tiles:
                    continue
                if room.tiles[x + 1 + y * 10] not in walkable_tiles:
                    continue
                if room.tiles[x + (y - 1) * 10] not in walkable_tiles:
                    continue
                if room.tiles[x + (y + 1) * 10] not in walkable_tiles:
                    continue
                idx = room.x * 10 + x + (room.y * 8 + y) * reachable_map.w
                if reachable_map.area[idx] == -1:
                    continue
                options.append((x, y))
        if not options:
            return None
        return random.choice(options)


class BonkSeashell(LocationBase):
    MAX_COUNT = 2

    def __init__(self, room, x, y):
        super().__init__(room, x, y)
        self.tree_x = x
        self.tree_y = y
        for offsetx, offsety in [(-1, 0), (-1, 1), (2, 0), (2, 1), (0, -1), (1, -1), (0, 2), (1, 2)]:
            if room.tiles[x + offsetx + (y + offsety) * 10] in walkable_tiles:
                self.x += offsetx
                self.y += offsety
                break

    def update_room(self, rom, re: RoomEditor):
        re.entities.append((self.tree_x, self.tree_y, 0x3D))
        if rom.banks[0x03][0x0F04] == 0xFF:
            rom.patch(0x03, 0x0F03, ASM("cp $FF"), ASM(f"cp ${self.room.x|(self.room.y<<4):02x}"))
        elif rom.banks[0x03][0x0F08] == 0xFF:
            rom.patch(0x03, 0x0F07, ASM("cp $FF"), ASM(f"cp ${self.room.x|(self.room.y<<4):02x}"))
        else:
            raise RuntimeError("To many bonk seashells")

    def connect_logic(self, logic_location):
        logic_location.connect(Location().add(Seashell(self.room.x + self.room.y * 16)), PEGASUS_BOOTS)

    def get_item_pool(self):
        return {None: 1}

    @staticmethod
    def check_possible(room, reachable_map):
        # Check if we can potentially place a hidden seashell here
        # Find potential trees
        options = []
        for y in range(1, 6):
            for x in range(1, 8):
                if room.tiles[x + y * 10] != 0x25:
                    continue
                if room.tiles[x + y * 10 + 1] != 0x26:
                    continue
                if room.tiles[x + y * 10 + 10] != 0x27:
                    continue
                if room.tiles[x + y * 10 + 11] != 0x28:
                    continue
                idx = room.x * 10 + x + (room.y * 8 + y) * reachable_map.w
                top_reachable = reachable_map.area[idx - reachable_map.w] != -1 or reachable_map.area[idx - reachable_map.w + 1] != -1
                bottom_reachable = reachable_map.area[idx + reachable_map.w * 2] != -1 or reachable_map.area[idx + reachable_map.w * 2 + 1] != -1
                left_reachable = reachable_map.area[idx - 1] != -1 or reachable_map.area[idx + reachable_map.w - 1] != -1
                right_reachable = reachable_map.area[idx + 2] != -1 or reachable_map.area[idx + reachable_map.w + 2] != -1
                if (top_reachable and bottom_reachable) or (left_reachable and right_reachable):
                    options.append((x, y))
        if not options:
            return None
        return random.choice(options)
