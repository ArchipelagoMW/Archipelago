from .bitutil import *

class NpcPlacement:
    def __init__(self):
        self.npc = 0
        self.x = 0
        self.y = 0
        self.walks = False
        self.intangible = False
        self.facing = 0
        self.palette = 0
        self.turns = False
        self.marches = False
        self.speed = 0

        self.bit13 = False
        self.bit14 = False
        self.bit21 = False
        self.bit22 = False

    def encode(self):
        encoding = [0, 0, 0, 0]

        encoding[0] = self.npc
        encoding[1] = pack_byte('5bbb', self.x, self.bit13, self.bit14, self.walks)
        encoding[2] = pack_byte('5bbb', self.y, self.bit21, self.bit22, self.intangible)
        encoding[3] = pack_byte('22bb2', self.facing, self.palette, self.turns, self.marches, self.speed)

        return encoding

def decode(byte_list):
    p = NpcPlacement()
    
    p.npc = byte_list[0]
    p.x, p.bit13, p.bit14, p.walks = unpack_byte('5bbb', byte_list[1])
    p.y, p.bit21, p.bit22, p.intangible = unpack_byte('5bbb', byte_list[2])
    p.facing, p.palette, p.turns, p.marches, p.speed = unpack_byte('22bb2', byte_list[3])

    return p

def decode_set(byte_list):
    results = []
    for i in range(0, 48, 4):
        if i >= len(byte_list):
            break
        if byte_list[i] == 0:
            break
        results.append(decode(byte_list[i:i+4]))
    return results

def encode_set(placement_list):
    byte_list = []
    for placement in placement_list:
        byte_list.extend(placement.encode())
    byte_list.append(0x00)
    return byte_list
