from .bitutil import *

EVENT = 1
TREASURE = 2
TELEPORT = 3

class Trigger:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = EVENT
        self.event_call = 0
        self.formation = 0
        self.is_miab = False
        self.item = None
        self.gp = None
        self.map = 0
        self.target_x = 0
        self.target_y = 0
        self.target_facing = 0

    def encode(self):
        encoding = [self.x, self.y, 0, 0, 0]

        if self.type == EVENT:
            encoding[2] = 0xFF
            encoding[3] = self.event_call
        elif self.type == TREASURE:
            encoding[2] = 0xFE
            encoding[3] = pack_byte('6bb', self.formation, self.is_miab, (self.item is not None))
            if self.item is not None:
                encoding[4] = self.item                
            elif self.gp < 1280:
                encoding[4] = int(self.gp / 10)
            else:
                encoding[4] = 0x80 + int(self.gp / 1000)
        elif self.type == TELEPORT:
            encoding[2] = self.map
            if self.target_facing is None:
                encoding[3] = self.target_x
            else:
                encoding[3] = pack_byte('62', self.target_x, self.target_facing)
            encoding[4] = self.target_y

        return encoding

def decode(byte_list):
    t = Trigger()
    t.x = byte_list[0]
    t.y = byte_list[1]
    if byte_list[2] == 0xFF:
        t.type = EVENT
        t.event_call = byte_list[3]
    elif byte_list[2] == 0xFE:
        t.type = TREASURE
        t.formation, t.is_miab, contains_item = unpack_byte('6bb', byte_list[3])
        if contains_item:
            t.item = byte_list[4]
        elif byte_list[4] >= 0x80:
            t.gp = (byte_list[4] - 0x80) * 1000
        else:
            t.gp = byte_list[4] * 10
    else:
        t.type = TELEPORT
        t.map = byte_list[2]
        if t.map >= 251 and t.map <= 253:
            t.target_x = byte_list[3]
            t.target_facing = None
        else:
            t.target_x, t.target_facing = unpack_byte('62', byte_list[3])
        t.target_y = byte_list[4]

    return t

def decode_set(byte_list):
    results = []
    for i in range(0, len(byte_list), 5):
        data = byte_list[i:i+5]
        results.append(decode(data))
    return results

def encode_set(trigger_set):
    encoding = []
    for t in trigger_set:
        encoding.extend(t.encode())
    return encoding
