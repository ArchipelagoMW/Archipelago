import json
from . import entityData


WARP_TYPE_IDS = {0xE1, 0xE2, 0xE3, 0xBA, 0xA8, 0xBE, 0xCB, 0xC2, 0xC6}
ALT_ROOM_OVERLAYS = {"Alt06": 0x1040, "Alt0E": 0x1090, "Alt1B": 0x10E0, "Alt2B": 0x1130, "Alt79": 0x1180, "Alt8C": 0x11D0}


class RoomEditor:
    def __init__(self, rom, room=None):
        assert room is not None
        self.room = room
        self.entities = []
        self.objects = []
        self.tileset_index = None
        self.palette_index = None
        self.attribset = None

        if isinstance(room, int):
            entities_raw = rom.entities[room]
            idx = 0
            while entities_raw[idx] != 0xFF:
                x = entities_raw[idx] & 0x0F
                y = entities_raw[idx] >> 4
                id = entities_raw[idx + 1]
                self.entities.append((x, y, id))
                idx += 2
            assert idx == len(entities_raw) - 1

        if isinstance(room, str):
            if room in rom.rooms_overworld_top:
                objects_raw = rom.rooms_overworld_top[room]
            elif room in rom.rooms_overworld_bottom:
                objects_raw = rom.rooms_overworld_bottom[room]
            elif room in rom.rooms_indoor_a:
                objects_raw = rom.rooms_indoor_a[room]
            else:
                assert False, "Failed to find alt room: %s" % (room)
        else:
            if room < 0x080:
                objects_raw = rom.rooms_overworld_top[room]
            elif room < 0x100:
                objects_raw = rom.rooms_overworld_bottom[room - 0x80]
            elif room < 0x200:
                objects_raw = rom.rooms_indoor_a[room - 0x100]
            elif room < 0x300:
                objects_raw = rom.rooms_indoor_b[room - 0x200]
            else:
                objects_raw = rom.rooms_color_dungeon[room - 0x300]

        self.animation_id = objects_raw[0]
        self.floor_object = objects_raw[1]
        idx = 2
        while objects_raw[idx] != 0xFE:
            x = objects_raw[idx] & 0x0F
            y = objects_raw[idx] >> 4
            if y == 0x08:  # horizontal
                count = x
                x = objects_raw[idx + 1] & 0x0F
                y = objects_raw[idx + 1] >> 4
                self.objects.append(ObjectHorizontal(x, y, objects_raw[idx + 2], count))
                idx += 3
            elif y == 0x0C: # vertical
                count = x
                x = objects_raw[idx + 1] & 0x0F
                y = objects_raw[idx + 1] >> 4
                self.objects.append(ObjectVertical(x, y, objects_raw[idx + 2], count))
                idx += 3
            elif y == 0x0E:  # warp
                self.objects.append(ObjectWarp(objects_raw[idx] & 0x0F, objects_raw[idx + 1], objects_raw[idx + 2], objects_raw[idx + 3], objects_raw[idx + 4]))
                idx += 5
            else:
                self.objects.append(Object(x, y, objects_raw[idx + 1]))
                idx += 2
        if room is not None:
            assert idx == len(objects_raw) - 1

        if isinstance(room, int) and room < 0x0CC:
            self.overlay = rom.banks[0x26][room * 80:room * 80+80]
        elif isinstance(room, int) and room < 0x100:
            self.overlay = rom.banks[0x27][(room - 0xCC) * 80:(room - 0xCC) * 80 + 80]
        elif room in ALT_ROOM_OVERLAYS:
            self.overlay = rom.banks[0x27][ALT_ROOM_OVERLAYS[room]:ALT_ROOM_OVERLAYS[room] + 80]
        else:
            self.overlay = None

    def store(self, rom, new_room_nr=None):
        if new_room_nr is None:
            new_room_nr = self.room
        objects_raw = bytearray([self.animation_id, self.floor_object])
        for obj in self.objects:
            objects_raw += obj.export()
        objects_raw += bytearray([0xFE])

        if isinstance(new_room_nr, str):
            if new_room_nr in rom.rooms_overworld_top:
                rom.rooms_overworld_top[new_room_nr] = objects_raw
            elif new_room_nr in rom.rooms_overworld_bottom:
                rom.rooms_overworld_bottom[new_room_nr] = objects_raw
            elif new_room_nr in rom.rooms_indoor_a:
                rom.rooms_indoor_a[new_room_nr] = objects_raw
            else:
                assert False, "Failed to find alt room: %s" % (new_room_nr)
        elif new_room_nr < 0x080:
            rom.rooms_overworld_top[new_room_nr] = objects_raw
        elif new_room_nr < 0x100:
            rom.rooms_overworld_bottom[new_room_nr - 0x80] = objects_raw
        elif new_room_nr < 0x200:
            rom.rooms_indoor_a[new_room_nr - 0x100] = objects_raw
        elif new_room_nr < 0x300:
            rom.rooms_indoor_b[new_room_nr - 0x200] = objects_raw
        else:
            rom.rooms_color_dungeon[new_room_nr - 0x300] = objects_raw

        if isinstance(new_room_nr, int) and new_room_nr < 0x100:
            if self.tileset_index is not None:
                rom.banks[0x3F][0x3F00 + new_room_nr] = self.tileset_index & 0xFF
            if self.attribset is not None:
                # With a tileset, comes metatile gbc data that we need to store a proper bank+pointer.
                rom.banks[0x1A][0x2476 + new_room_nr] = self.attribset[0]
                rom.banks[0x1A][0x1E76 + new_room_nr*2] = self.attribset[1] & 0xFF
                rom.banks[0x1A][0x1E76 + new_room_nr*2+1] = self.attribset[1] >> 8
            if self.palette_index is not None:
                rom.banks[0x21][0x02ef + new_room_nr] = self.palette_index

        if isinstance(new_room_nr, int):
            entities_raw = bytearray()
            for entity in self.entities:
                entities_raw += bytearray([entity[0] | entity[1] << 4, entity[2]])
            entities_raw += bytearray([0xFF])
            rom.entities[new_room_nr] = entities_raw

            if new_room_nr < 0x0CC:
                rom.banks[0x26][new_room_nr * 80:new_room_nr * 80 + 80] = self.overlay
            elif new_room_nr < 0x100:
                rom.banks[0x27][(new_room_nr - 0xCC) * 80:(new_room_nr - 0xCC) * 80 + 80] = self.overlay
        elif new_room_nr in ALT_ROOM_OVERLAYS:
            rom.banks[0x27][ALT_ROOM_OVERLAYS[new_room_nr]:ALT_ROOM_OVERLAYS[new_room_nr] + 80] = self.overlay

    def addEntity(self, x, y, type_id):
        self.entities.append((x, y, type_id))

    def removeEntities(self, type_id):
        self.entities = list(filter(lambda e: e[2] != type_id, self.entities))

    def hasEntity(self, type_id):
        return any(map(lambda e: e[2] == type_id, self.entities))

    def changeObject(self, x, y, new_type):
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                obj.type_id = new_type
                if self.overlay is not None:
                    self.overlay[x + y * 10] = new_type

    def removeObject(self, x, y):
        self.objects = list(filter(lambda obj: obj.x != x or obj.y != y, self.objects))

    def moveObject(self, x, y, new_x, new_y):
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                if self.overlay is not None:
                    self.overlay[x + y * 10] = self.floor_object
                    self.overlay[new_x + new_y * 10] = obj.type_id
                obj.x = new_x
                obj.y = new_y

    def getWarps(self):
        return list(filter(lambda obj: isinstance(obj, ObjectWarp), self.objects))

    def updateOverlay(self, preserve_floor=False):
        if self.overlay is None:
            return
        if not preserve_floor:
            for n in range(80):
                self.overlay[n] = self.floor_object
        for obj in self.objects:
            if isinstance(obj, ObjectHorizontal):
                for n in range(obj.count):
                    self.overlay[obj.x + n + obj.y * 10] = obj.type_id
            elif isinstance(obj, ObjectVertical):
                for n in range(obj.count):
                    self.overlay[obj.x + n * 10 + obj.y * 10] = obj.type_id
            elif not isinstance(obj, ObjectWarp):
                self.overlay[obj.x + obj.y * 10] = obj.type_id

    def loadFromJson(self, filename):
        self.objects = []
        self.entities = []
        self.animation_id = 0
        self.tileset_index = 0x0F
        self.palette_index = 0x01
        
        data = json.load(open(filename))
        
        for prop in data.get("properties", []):
            if prop["name"] == "palette":
                self.palette_index = int(prop["value"], 16)
            elif prop["name"] == "tileset":
                self.tileset_index = int(prop["value"], 16)
            elif prop["name"] == "animationset":
                self.animation_id = int(prop["value"], 16)
            elif prop["name"] == "attribset":
                bank, _, addr = prop["value"].partition(":")
                self.attribset = (int(bank, 16), int(addr, 16) + 0x4000)

        tiles = [0] * 80
        for layer in data["layers"]:
            if "data" in layer:
                for n in range(80):
                    if layer["data"][n] > 0:
                        tiles[n] = (layer["data"][n] - 1) & 0xFF
            if "objects" in layer:
                for obj in layer["objects"]:
                    x = int((obj["x"] + obj["width"] / 2) // 16)
                    y = int((obj["y"] + obj["height"] / 2) // 16)
                    if obj["type"] == "warp":
                        warp_type, map_nr, room, x, y = obj["name"].split(":")
                        self.objects.append(ObjectWarp(int(warp_type), int(map_nr, 16), int(room, 16) & 0xFF, int(x, 16), int(y, 16)))
                    elif obj["type"] == "entity":
                        type_id = entityData.NAME.index(obj["name"])
                        self.addEntity(x, y, type_id)
                    elif obj["type"] == "hidden_tile":
                        self.objects.append(Object(x, y, int(obj["name"], 16)))
        self.buildObjectList(tiles, reduce_size=True)
        return data

    def getTileArray(self):
        if self.room < 0x100:
            tiles = [self.floor_object] * 80
        else:
            tiles = [self.floor_object & 0x0F] * 80
        def objHSize(type_id):
            if type_id == 0xF5:
                return 2
            return 1
        def objVSize(type_id):
            if type_id == 0xF5:
                return 2
            return 1
        def getObject(x, y):
            x, y = (x & 15), (y & 15)
            if x < 10 and y < 8:
                return tiles[x + y * 10]
            return 0
        if self.room < 0x100:
            def placeObject(x, y, type_id):
                if type_id == 0xF5:
                    if getObject(x, y) in (0x1B, 0x28, 0x29, 0x83, 0x90):
                        placeObject(x, y, 0x29)
                    else:
                        placeObject(x, y, 0x25)
                    if getObject(x + 1, y) in (0x1B, 0x27, 0x82, 0x86, 0x8A, 0x90, 0x2A):
                        placeObject(x + 1, y, 0x2A)
                    else:
                        placeObject(x + 1, y, 0x26)
                    if getObject(x, y + 1) in (0x26, 0x2A):
                        placeObject(x, y + 1, 0x2A)
                    elif getObject(x, y + 1) == 0x90:
                        placeObject(x, y + 1, 0x82)
                    else:
                        placeObject(x, y + 1, 0x27)
                    if getObject(x + 1, y + 1) in (0x25, 0x29):
                        placeObject(x + 1, y + 1, 0x29)
                    elif getObject(x + 1, y + 1) == 0x90:
                        placeObject(x + 1, y + 1, 0x83)
                    else:
                        placeObject(x + 1, y + 1, 0x28)
                elif type_id == 0xF6:  # two door house
                    placeObject(x + 0, y, 0x55)
                    placeObject(x + 1, y, 0x5A)
                    placeObject(x + 2, y, 0x5A)
                    placeObject(x + 3, y, 0x5A)
                    placeObject(x + 4, y, 0x56)
                    placeObject(x + 0, y + 1, 0x57)
                    placeObject(x + 1, y + 1, 0x59)
                    placeObject(x + 2, y + 1, 0x59)
                    placeObject(x + 3, y + 1, 0x59)
                    placeObject(x + 4, y + 1, 0x58)
                    placeObject(x + 0, y + 2, 0x5B)
                    placeObject(x + 1, y + 2, 0xE2)
                    placeObject(x + 2, y + 2, 0x5B)
                    placeObject(x + 3, y + 2, 0xE2)
                    placeObject(x + 4, y + 2, 0x5B)
                elif type_id == 0xF7:  # large house
                    placeObject(x + 0, y, 0x55)
                    placeObject(x + 1, y, 0x5A)
                    placeObject(x + 2, y, 0x56)
                    placeObject(x + 0, y + 1, 0x57)
                    placeObject(x + 1, y + 1, 0x59)
                    placeObject(x + 2, y + 1, 0x58)
                    placeObject(x + 0, y + 2, 0x5B)
                    placeObject(x + 1, y + 2, 0xE2)
                    placeObject(x + 2, y + 2, 0x5B)
                elif type_id == 0xF8:  # catfish
                    placeObject(x + 0, y, 0xB6)
                    placeObject(x + 1, y, 0xB7)
                    placeObject(x + 2, y, 0x66)
                    placeObject(x + 0, y + 1, 0x67)
                    placeObject(x + 1, y + 1, 0xE3)
                    placeObject(x + 2, y + 1, 0x68)
                elif type_id == 0xF9:  # palace door
                    placeObject(x + 0, y, 0xA4)
                    placeObject(x + 1, y, 0xA5)
                    placeObject(x + 2, y, 0xA6)
                    placeObject(x + 0, y + 1, 0xA7)
                    placeObject(x + 1, y + 1, 0xE3)
                    placeObject(x + 2, y + 1, 0xA8)
                elif type_id == 0xFA:  # stone pig head
                    placeObject(x + 0, y, 0xBB)
                    placeObject(x + 1, y, 0xBC)
                    placeObject(x + 0, y + 1, 0xBD)
                    placeObject(x + 1, y + 1, 0xBE)
                elif type_id == 0xFB:  # palmtree
                    if x == 15:
                        placeObject(x + 1, y + 1, 0xB7)
                        placeObject(x + 1, y + 2, 0xCE)
                    else:
                        placeObject(x + 0, y, 0xB6)
                        placeObject(x + 0, y + 1, 0xCD)
                        placeObject(x + 1, y + 0, 0xB7)
                        placeObject(x + 1, y + 1, 0xCE)
                elif type_id == 0xFC:  # square "hill with hole" (seen near lvl4 entrance)
                    placeObject(x + 0, y, 0x2B)
                    placeObject(x + 1, y, 0x2C)
                    placeObject(x + 2, y, 0x2D)
                    placeObject(x + 0, y + 1, 0x37)
                    placeObject(x + 1, y + 1, 0xE8)
                    placeObject(x + 2, y + 1, 0x38)
                    placeObject(x - 1, y + 2, 0x0A)
                    placeObject(x + 0, y + 2, 0x33)
                    placeObject(x + 1, y + 2, 0x2F)
                    placeObject(x + 2, y + 2, 0x34)
                    placeObject(x + 0, y + 3, 0x0A)
                    placeObject(x + 1, y + 3, 0x0A)
                    placeObject(x + 2, y + 3, 0x0A)
                    placeObject(x + 3, y + 3, 0x0A)
                elif type_id == 0xFD:  # small house
                    placeObject(x + 0, y, 0x52)
                    placeObject(x + 1, y, 0x52)
                    placeObject(x + 2, y, 0x52)
                    placeObject(x + 0, y + 1, 0x5B)
                    placeObject(x + 1, y + 1, 0xE2)
                    placeObject(x + 2, y + 1, 0x5B)
                else:
                    x, y = (x & 15), (y & 15)
                    if x < 10 and y < 8:
                        tiles[x + y * 10] = type_id
        else:
            def placeObject(x, y, type_id):
                x, y = (x & 15), (y & 15)
                if type_id == 0xEC:  # key door
                    placeObject(x, y, 0x2D)
                    placeObject(x + 1, y, 0x2E)
                elif type_id == 0xED:
                    placeObject(x, y, 0x2F)
                    placeObject(x + 1, y, 0x30)
                elif type_id == 0xEE:
                    placeObject(x, y, 0x31)
                    placeObject(x, y + 1, 0x32)
                elif type_id == 0xEF:
                    placeObject(x, y, 0x33)
                    placeObject(x, y + 1, 0x34)
                elif type_id == 0xF0:  # closed door
                    placeObject(x, y, 0x35)
                    placeObject(x + 1, y, 0x36)
                elif type_id == 0xF1:
                    placeObject(x, y, 0x37)
                    placeObject(x + 1, y, 0x38)
                elif type_id == 0xF2:
                    placeObject(x, y, 0x39)
                    placeObject(x, y + 1, 0x3A)
                elif type_id == 0xF3:
                    placeObject(x, y, 0x3B)
                    placeObject(x, y + 1, 0x3C)
                elif type_id == 0xF4:  # open door
                    placeObject(x, y, 0x43)
                    placeObject(x + 1, y, 0x44)
                elif type_id == 0xF5:
                    placeObject(x, y, 0x8C)
                    placeObject(x + 1, y, 0x08)
                elif type_id == 0xF6:
                    placeObject(x, y, 0x09)
                    placeObject(x, y + 1, 0x0A)
                elif type_id == 0xF7:
                    placeObject(x, y, 0x0B)
                    placeObject(x, y + 1, 0x0C)
                elif type_id == 0xF8:  # boss door
                    placeObject(x, y, 0xA4)
                    placeObject(x + 1, y, 0xA5)
                elif type_id == 0xF9:  # stairs door
                    placeObject(x, y, 0xAF)
                    placeObject(x + 1, y, 0xB0)
                elif type_id == 0xFA:  # flipwall
                    placeObject(x, y, 0xB1)
                    placeObject(x + 1, y, 0xB2)
                elif type_id == 0xFB:  # one way arrow
                    placeObject(x, y, 0x45)
                    placeObject(x + 1, y, 0x46)
                elif type_id == 0xFC:  # entrance
                    placeObject(x + 0, y, 0xB3)
                    placeObject(x + 1, y, 0xB4)
                    placeObject(x + 2, y, 0xB4)
                    placeObject(x + 3, y, 0xB5)
                    placeObject(x + 0, y + 1, 0xB6)
                    placeObject(x + 1, y + 1, 0xB7)
                    placeObject(x + 2, y + 1, 0xB8)
                    placeObject(x + 3, y + 1, 0xB9)
                    placeObject(x + 0, y + 2, 0xBA)
                    placeObject(x + 1, y + 2, 0xBB)
                    placeObject(x + 2, y + 2, 0xBC)
                    placeObject(x + 3, y + 2, 0xBD)
                elif type_id == 0xFD:  # entrance
                    placeObject(x, y, 0xC1)
                    placeObject(x + 1, y, 0xC2)
                else:
                    if x < 10 and y < 8:
                        tiles[x + y * 10] = type_id

            def addWalls(flags):
                for x in range(0, 10):
                    if flags & 0b0010:
                        placeObject(x, 0, 0x21)
                    if flags & 0b0001:
                        placeObject(x, 7, 0x22)
                for y in range(0, 8):
                    if flags & 0b1000:
                        placeObject(0, y, 0x23)
                    if flags & 0b0100:
                        placeObject(9, y, 0x24)
                if flags & 0b1000 and flags & 0b0010:
                    placeObject(0, 0, 0x25)
                if flags & 0b0100 and flags & 0b0010:
                    placeObject(9, 0, 0x26)
                if flags & 0b1000 and flags & 0b0001:
                    placeObject(0, 7, 0x27)
                if flags & 0b0100 and flags & 0b0001:
                    placeObject(9, 7, 0x28)

            if self.floor_object & 0xF0 == 0x00:
                addWalls(0b1111)
            if self.floor_object & 0xF0 == 0x10:
                addWalls(0b1101)
            if self.floor_object & 0xF0 == 0x20:
                addWalls(0b1011)
            if self.floor_object & 0xF0 == 0x30:
                addWalls(0b1110)
            if self.floor_object & 0xF0 == 0x40:
                addWalls(0b0111)
            if self.floor_object & 0xF0 == 0x50:
                addWalls(0b1001)
            if self.floor_object & 0xF0 == 0x60:
                addWalls(0b0101)
            if self.floor_object & 0xF0 == 0x70:
                addWalls(0b0110)
            if self.floor_object & 0xF0 == 0x80:
                addWalls(0b1010)
        for obj in self.objects:
            if isinstance(obj, ObjectWarp):
                pass
            elif isinstance(obj, ObjectHorizontal):
                for n in range(0, obj.count):
                    placeObject(obj.x + n * objHSize(obj.type_id), obj.y, obj.type_id)
            elif isinstance(obj, ObjectVertical):
                for n in range(0, obj.count):
                    placeObject(obj.x, obj.y + n * objVSize(obj.type_id), obj.type_id)
            else:
                placeObject(obj.x, obj.y, obj.type_id)
        return tiles

    def buildObjectList(self, tiles, *, reduce_size=False):
        self.objects = [obj for obj in self.objects if isinstance(obj, ObjectWarp)]
        tiles = tiles.copy()
        if self.overlay:
            for n in range(80):
                self.overlay[n] = tiles[n]
                if reduce_size:
                    if tiles[n] in {0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F,
                                    0x33, 0x34, 0x37, 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F,
                                    0x48, 0x49, 0x4B, 0x4C, 0x4E,
                                    0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F}:
                        tiles[n] = 0x3A  # Solid tiles
                    if tiles[n] in {0x08, 0x09, 0x0C, 0x44,
                                    0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF}:
                        tiles[n] = 0x04  # Open tiles

        is_overworld = isinstance(self.room, str) or self.room < 0x100
        counts = {}
        for n in tiles:
            if n < 0x0F or is_overworld:
                counts[n] = counts.get(n, 0) + 1
        self.floor_object = max(counts, key=counts.get)
        for y in range(8) if is_overworld else range(1, 7):
            for x in range(10) if is_overworld else range(1, 9):
                if tiles[x + y * 10] == self.floor_object:
                    tiles[x + y * 10] = -1
        for y in range(8):
            for x in range(10):
                obj = tiles[x + y * 10]
                if obj == -1:
                    continue
                w = 1
                h = 1
                while x + w < 10 and tiles[x + w + y * 10] == obj:
                    w += 1
                while y + h < 8 and tiles[x + (y + h) * 10] == obj:
                    h += 1
                if obj in {0xE1, 0xE2, 0xE3, 0xBA, 0xC6}:  # Entrances should never be horizontal/vertical lists
                    w = 1
                    h = 1
                if w > h:
                    for n in range(w):
                        tiles[x + n + y * 10] = -1
                    self.objects.append(ObjectHorizontal(x, y, obj, w))
                elif h > 1:
                    for n in range(h):
                        tiles[x + (y + n) * 10] = -1
                    self.objects.append(ObjectVertical(x, y, obj, h))
                else:
                    self.objects.append(Object(x, y, obj))


class Object:
    def __init__(self, x, y, type_id):
        self.x = x
        self.y = y
        self.type_id = type_id

    def export(self):
        return bytearray([self.x | (self.y << 4), self.type_id])

    def __repr__(self):
        return "%s:%d,%d:%02X" % (self.__class__.__name__, self.x, self.y, self.type_id)


class ObjectHorizontal(Object):
    def __init__(self, x, y, type_id, count):
        super().__init__(x, y, type_id)
        self.count = count

    def export(self):
        return bytearray([0x80 | self.count, self.x | (self.y << 4), self.type_id])

    def __repr__(self):
        return "%s:%d,%d:%02Xx%d" % (self.__class__.__name__, self.x, self.y, self.type_id, self.count)


class ObjectVertical(Object):
    def __init__(self, x, y, type_id, count):
        super().__init__(x, y, type_id)
        self.count = count

    def export(self):
        return bytearray([0xC0 | self.count, self.x | (self.y << 4), self.type_id])

    def __repr__(self):
        return "%s:%d,%d:%02Xx%d" % (self.__class__.__name__, self.x, self.y, self.type_id, self.count)


class ObjectWarp(Object):
    def __init__(self, warp_type, map_nr, room_nr, target_x, target_y):
        super().__init__(None, None, None)
        if warp_type > 0:
            # indoor map
            if map_nr == 0xff:
                room_nr += 0x300  # color dungeon
            elif 0x06 <= map_nr < 0x1A:
                room_nr += 0x200  # indoor B
            else:
                room_nr += 0x100  # indoor A
        self.warp_type = warp_type
        self.room = room_nr
        self.map_nr = map_nr
        self.target_x = target_x
        self.target_y = target_y

    def export(self):
        return bytearray([0xE0 | self.warp_type, self.map_nr, self.room & 0xFF, self.target_x, self.target_y])

    def copy(self):
        return ObjectWarp(self.warp_type, self.map_nr, self.room & 0xFF, self.target_x, self.target_y)

    def __repr__(self):
        return "%s:%d:%03x:%02x:%d,%d" % (self.__class__.__name__, self.warp_type, self.room, self.map_nr, self.target_x, self.target_y)
