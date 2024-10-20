from .bitutil import *

def _set_to_bits(s):
    val = 0
    for i in s:
        val |= (1 << i)
    return val

def _bits_to_set(val):
    s = set()
    for i in range(16):
        if val & (1 << i):
            s.add(i)
    return s

class Monster:
    def __init__(self):
        self.boss = False
        self.level = 0
        self.hp = 0
        self.attack_index = 0
        self.defense_index = 0
        self.magic_defense_index = 0
        self.speed_index = 0
        self.drop_index = 0
        self.drop_rate = 0
        self.attack_sequence = 0
        self.attack_elements = set()
        self.attack_statuses = set()
        self.resist_elements = set()
        self.resist_statuses = set()
        self.weak_elements = set()
        self.spell_power = None
        self.races = set()
        self.reaction_sequence = None
        self.bit72 = False
        self.bit73 = False

    def encode(self):
        encoded = [
            pack_byte('7b', self.level, self.boss),
            self.hp & 0xff,
            (self.hp >> 8) & 0xff,
            self.attack_index,
            self.defense_index,
            self.magic_defense_index,
            self.speed_index,
            pack_byte('62', self.drop_index, self.drop_rate),
            self.attack_sequence,
            pack_byte('bbbbbbbb',
                self.bit72,
                self.bit73,
                (self.reaction_sequence is not None),
                bool(self.races),
                (self.spell_power is not None),
                bool(self.weak_elements),
                bool(self.resist_elements) or bool(self.resist_statuses),
                bool(self.attack_elements) or bool(self.attack_statuses)
                )
            ]

        if self.attack_elements or self.attack_statuses:
            if self.attack_elements:
                encoded.append(_set_to_bits(self.attack_elements))
            else:
                encoded.append(0)

            if self.attack_statuses:
                val = _set_to_bits(self.attack_statuses)
                encoded.append(val & 0xff)
                encoded.append((val >> 8) & 0xff)
            else:
                encoded.extend([0,0])
        if self.resist_elements or self.resist_statuses:
            if self.resist_elements:
                encoded.append(_set_to_bits(self.resist_elements))
            else:
                encoded.append(0)

            if self.resist_statuses:
                val = _set_to_bits(self.resist_statuses)
                encoded.append(val & 0xff)
                encoded.append((val >> 8) & 0xff)
            else:
                encoded.extend([0,0])
        if self.weak_elements:
            encoded.append(_set_to_bits(self.weak_elements))
        if self.spell_power is not None:
            encoded.append(self.spell_power)
        if self.races:
            encoded.append(_set_to_bits(self.races))
        if self.reaction_sequence is not None:
            encoded.append(self.reaction_sequence)

        return encoded

def decode(byte_list):
    m = Monster()
    m.level, m.boss = unpack_byte('7b', byte_list[0])
    m.hp = byte_list[1] | (byte_list[2] << 8)
    m.attack_index = byte_list[3]
    m.defense_index = byte_list[4]
    m.magic_defense_index = byte_list[5]
    m.speed_index = byte_list[6]
    m.drop_index, m.drop_rate = unpack_byte('62', byte_list[7])
    m.attack_sequence = byte_list[8]

    flags = list(unpack_byte('bbbbbbbb', byte_list[9]))
    byte_list = byte_list[10:]

    if flags.pop():
        m.attack_elements = _bits_to_set(byte_list.pop(0))
        m.attack_statuses = _bits_to_set(byte_list[0] | (byte_list[1] << 8))
        byte_list = byte_list[2:]

    if flags.pop():
        m.resist_elements = _bits_to_set(byte_list.pop(0))
        m.resist_statuses = _bits_to_set(byte_list[0] | (byte_list[1] << 8))
        byte_list = byte_list[2:]

    if flags.pop():
        m.weak_elements = _bits_to_set(byte_list.pop(0))

    if flags.pop():
        m.spell_power = byte_list.pop(0)

    if flags.pop():
        m.races = _bits_to_set(byte_list.pop(0))

    if flags.pop():
        m.reaction_sequence = byte_list.pop(0)

    m.bit73 = flags.pop()
    m.bit72 = flags.pop()

    return m
