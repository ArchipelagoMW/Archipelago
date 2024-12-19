import time
import json

class Consts:
    room = 0xFFF6
    mapId = 0xFFF7
    indoorFlag = 0xDBA5
    spawnMap = 0xDB60
    spawnRoom = 0xDB61
    spawnX = 0xDB62
    spawnY = 0xDB63
    entranceRoomOffset = 0xD800
    transitionState = 0xC124
    transitionTargetX = 0xC12C
    transitionTargetY = 0xC12D
    transitionScrollX = 0xFF96
    transitionScrollY = 0xFF97
    linkMotionState = 0xC11C
    transitionSequence = 0xC16B 
    screenCoord = 0xFFFA

mapMap = {
    0x00: 0x01,
    0x01: 0x01,
    0x02: 0x01,
    0x03: 0x01,
    0x04: 0x01,
    0x05: 0x01,
    0x06: 0x02,
    0x07: 0x02,
    0x08: 0x02,
    0x09: 0x02,
    0x0A: 0x02,
    0x0B: 0x02,
    0x0C: 0x02,
    0x0D: 0x02,
    0x0E: 0x02,
    0x0F: 0x02,
    0x10: 0x02,
    0x11: 0x02,
    0x12: 0x02,
    0x13: 0x02,
    0x14: 0x02,
    0x15: 0x02,
    0x16: 0x02,
    0x17: 0x02,
    0x18: 0x02,
    0x19: 0x02,
    0x1D: 0x01,
    0x1E: 0x01,
    0x1F: 0x01,
    0xFF: 0x03,
}

class GpsTracker:
    room = None
    last_room = None
    last_different_room = None
    room_same_for = 0
    room_changed = False
    location_changed = False
    screen_x = 0
    screen_y = 0
    spawn_x = 0
    spawn_y = 0
    indoors = None
    indoors_changed = False
    spawn_map = None
    spawn_room = None
    spawn_changed = False
    spawn_same_for = 0

    def __init__(self, gameboy) -> None:
        self.gameboy = gameboy

        self.gameboy.set_location_range(
            Consts.linkMotionState,
            Consts.transitionSequence - Consts.linkMotionState,
            [Consts.transitionState]
        )

    async def read_byte(self, b):
        return (await self.gameboy.async_read_memory(b))[0]

    lastTime = time.time()
    async def read_location(self):
        now = time.time()
        print(f"reading location after {now - self.lastTime}")

        self.lastTime = now

        transitionState = await self.read_byte(Consts.transitionState)
        transitionTargetX = await self.read_byte(Consts.transitionTargetX)
        transitionTargetY = await self.read_byte(Consts.transitionTargetY)
        transitionScrollX = await self.read_byte(Consts.transitionScrollX)
        transitionScrollY = await self.read_byte(Consts.transitionScrollY)
        transitionSequence = await self.read_byte(Consts.transitionSequence)
        motionState = await self.read_byte(Consts.linkMotionState)
        if (transitionState != 0
            or transitionTargetX != transitionScrollX
            or transitionTargetY != transitionScrollY
            or transitionSequence != 0x04):
            return

        indoors = await self.read_byte(Consts.indoorFlag)

        if indoors != self.indoors and self.indoors != None:
            self.indoors_changed = True

        self.indoors = indoors
        
        spawnMap = await self.read_byte(Consts.spawnMap)
        mapDigit = mapMap[spawnMap] << 8 if self.spawn_map else 0
        spawnRoom = await self.read_byte(Consts.spawnRoom) + mapDigit
        spawnX = await self.read_byte(Consts.spawnX)
        spawnY = await self.read_byte(Consts.spawnY)

        if ((spawnRoom != self.spawn_room and self.spawn_room != None)
            or (spawnMap != self.spawn_map and self.spawn_map != None)
            or (spawnX != self.spawn_x and self.spawn_x != None)
            or (spawnY != self.spawn_y and self.spawn_y != None)):
            self.spawn_changed = True
            self.spawn_same_for = 0
        else:
            self.spawn_same_for += 1
        
        self.spawn_map = spawnMap
        self.spawn_room = spawnRoom
        self.spawn_x = spawnX
        self.spawn_y = spawnY

        mapId = await self.read_byte(Consts.mapId)
        if mapId not in mapMap:
            print(f'Unknown map ID {hex(mapId)}')
            return

        mapDigit = mapMap[mapId] << 8 if indoors else 0
        self.last_room = self.room
        self.room = await self.read_byte(Consts.room) + mapDigit

        if self.last_room != self.room:
            self.room_same_for = 0
            self.room_changed = True
            self.last_different_room = self.last_room
        else:
            self.room_same_for += 1

        if motionState in [0, 1]:
            oldX = self.screen_x
            oldY = self.screen_y

            coords = await self.read_byte(Consts.screenCoord)
            self.screen_x = coords & 0x0F
            self.screen_y = (coords & 0xF0) >> 4

            if (self.room != self.last_room
                or oldX != self.screen_x
                or oldY != self.screen_y):
                self.location_changed = True
        # indoors = await self.read_byte(Consts.indoorFlag)

        # if indoors != self.indoors and self.indoors != None:
        #     self.indoorsChanged = True
        
        # self.indoors = indoors

        # mapId = await self.read_byte(Consts.mapId)
        # if mapId not in mapMap:
        #     print(f'Unknown map ID {hex(mapId)}')
        #     return

        # mapDigit = mapMap[mapId] << 8 if indoors else 0
        # last_room = self.room
        # self.room = await self.read_byte(Consts.room) + mapDigit

        # coords = await self.read_byte(Consts.screenCoord)
        # self.screenX = coords & 0x0F
        # self.screenY = (coords & 0xF0) >> 4

        # if (self.room != last_room):
        #     self.location_changed = True
    
    last_message = {}
    async def send_location(self, socket, diff=False):
        if self.room is None: 
            return

        message = {
            "type":"location",
            "refresh": True,
            "room": f'0x{self.room:02X}',
            "x": self.screen_x,
            "y": self.screen_y,
            "drawFine": True,
        }

        if message != self.last_message:
            self.last_message = message
            await socket.send(json.dumps(message))
