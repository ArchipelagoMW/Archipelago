from .bitutil import *

NUM_TILES_PER_TILESET = 0x80

class Tile:
    def __init__(self):
        self.layer1 = False
        self.layer2 = False
        self.bridge_layer = False
        self.save_point = False
        self.closed_door = False
        self.bit5 = False
        self.bit6 = False
        self.bit7 = False
        self.damage = False
        self.bit9 = False
        self.walk_behind = False
        self.bottom_half = False
        self.warp = False
        self.talkover = False
        self.encounters = False
        self.trigger = False

    def encode(self):
        return [
            pack_byte('bbbbbbbb',
                self.layer1, self.layer2, self.bridge_layer, self.save_point,
                self.closed_door, self.bit5, self.bit6, self.bit7),
            pack_byte('bbbbbbbb',
                self.damage, self.bit9, self.walk_behind, self.bottom_half,
                self.warp, self.talkover, self.encounters, self.trigger)
        ]       

    def decode(self, byte_list):
        result = unpack_byte('bbbbbbbb', byte_list[0])
        self.layer1 = result[0]
        self.layer2 = result[1]
        self.bridge_layer = result[2]
        self.save_point = result[3]
        self.closed_door = result[4]
        self.bit5 = result[5]
        self.bit6 = result[6]
        self.bit7 = result[7]

        result = unpack_byte('bbbbbbbb', byte_list[1])
        self.damage = result[0]
        self.bit9 = result[1]
        self.walk_behind = result[2]
        self.bottom_half = result[3]
        self.warp = result[4]
        self.talkover = result[5]
        self.encounters = result[6]
        self.trigger = result[7]

def decode(byte_list):
    tileset = []
    for i in range(NUM_TILES_PER_TILESET):
        tile = Tile()
        tile.decode(byte_list[i * 2 : (i + 1) * 2])
        tileset.append(tile)
    return tileset

def encode_set(self, tileset):
    encoding = []
    for tile in tileset:
        encoding.extend(tile.encode())
    return encoding
