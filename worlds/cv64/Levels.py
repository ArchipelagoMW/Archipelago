
from .Names import LocationName


class CV64Level:
    levelIDAddress: int
    startIDAddress: int
    levelID: int
    startID: int
    twoExits: bool
    canBacktrack: bool
    
    def __init__(self, levelIDAddress: int, startIDAddress: int, levelID: int, startID: int, twoExits: bool,
                 canBacktrack: bool):
        self.levelIDAddress = levelIDAddress
        self.startIDAddress = startIDAddress
        self.levelID = levelID
        self.startID = startID
        self.twoExits = twoExits
        self.canBacktrack = canBacktrack


level_dict = {
    LocationName.forest_of_silence:    CV64Level(0x34D19C, 0x34D19D, 0x00, 0x00, False, False),
    LocationName.castle_wall:          CV64Level(0x34D1A7, 0x34D1A8, 0x02, 0x00, False, False),
    LocationName.villa:                CV64Level(0x34D1BD, 0x34D1BE, 0x03, 0x00, True, False),
    LocationName.tunnel:               CV64Level(0x34D1C8, 0x34D1C9, 0x07, 0x00, False, False),
    LocationName.underground_waterway: CV64Level(0x34D1D3, 0x34D1D4, 0x08, 0x00, False, False),
    LocationName.castle_center:        CV64Level(0x34D217, 0x34D218, 0x19, 0x00, True, False),
    LocationName.duel_tower:           CV64Level(0x34D22D, 0x34D22E, 0x13, 0x00, False, True),
    LocationName.tower_of_execution:   CV64Level(0x34D238, 0x34D239, 0x10, 0x00, False, True),
    LocationName.tower_of_science:     CV64Level(0x34D24E, 0x34D24F, 0x12, 0x00, False, True),
    LocationName.tower_of_sorcery:     CV64Level(0x34D264, 0x34D265, 0x11, 0x00, False, True),
    LocationName.room_of_clocks:       CV64Level(0x34D29D, 0x34D29E, 0x1B, 0x00, False, False),
    LocationName.clock_tower:          CV64Level(0x34D2A8, 0x34D2A9, 0x17, 0x00, False, False),
    LocationName.castle_keep:          CV64Level(0x34D2A8, 0x34D2A9, 0x14, 0x02, False, False),
}

level_list = [
    LocationName.forest_of_silence,
    LocationName.castle_wall,
    LocationName.villa,
    LocationName.tunnel,
    LocationName.underground_waterway,
    LocationName.castle_center,
    LocationName.duel_tower,
    LocationName.tower_of_execution,
    LocationName.tower_of_science,
    LocationName.tower_of_sorcery,
    LocationName.room_of_clocks,
    LocationName.clock_tower,
]
