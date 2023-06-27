import json
roomAddress = 0xFFF6
mapIdAddress = 0xFFF7
indoorFlagAddress = 0xDBA5
entranceRoomOffset = 0xD800
screenCoordAddress = 0xFFFA

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
    location_changed = False
    screenX = 0
    screenY = 0
    indoors = None

    def __init__(self, gameboy) -> None:
        self.gameboy = gameboy

    async def read_byte(self, b):
        return (await self.gameboy.async_read_memory(b))[0]

    async def read_location(self):
        indoors = await self.read_byte(indoorFlagAddress)

        if indoors != self.indoors and self.indoors != None:
            self.indoorsChanged = True
        
        self.indoors = indoors

        mapId = await self.read_byte(mapIdAddress)
        if mapId not in mapMap:
            print(f'Unknown map ID {hex(mapId)}')
            return

        mapDigit = mapMap[mapId] << 8 if indoors else 0
        last_room = self.room
        self.room = await self.read_byte(roomAddress) + mapDigit

        coords = await self.read_byte(screenCoordAddress)
        self.screenX = coords & 0x0F
        self.screenY = (coords & 0xF0) >> 4

        if (self.room != last_room):
            self.location_changed = True
    
    last_message = {}
    async def send_location(self, socket, diff=False):
        if self.room is None: 
            return
        message = {
            "type":"location",
            "refresh": True,
            "version":"1.0",
            "room": f'0x{self.room:02X}',
            "x": self.screenX,
            "y": self.screenY,
        }
        if message != self.last_message:
            self.last_message = message
            await socket.send(json.dumps(message))
