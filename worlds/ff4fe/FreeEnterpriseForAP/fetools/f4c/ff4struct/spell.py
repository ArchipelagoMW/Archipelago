from .bitutil import *

class Spell:
    def __init__(self):
        self.casting_time = 0
        self.target = 0
        self.param = 0
        self.hit = 0
        self.boss = False
        self.effect = 0
        self.damage = False
        self.element = 0
        self.impact = False
        self.mp_cost = 0
        self.ignore_wall = False
        #self.colors = 0
        #self.sprites = 0
        #self.visual1 = 0
        #self.visual2 = 0
        #self.sound = 0

def decode(byte_list):
    s = Spell()
    s.casting_time, s.target = unpack_byte('53', byte_list[0])
    s.param = byte_list[1]
    s.hit, s.boss = unpack_byte('7b', byte_list[2])
    s.effect, s.damage = unpack_byte('7b', byte_list[3])
    s.element, s.impact = unpack_byte('7b', byte_list[4])
    s.mp_cost, s.ignore_wall = unpack_byte('7b', byte_list[5])
    return s
