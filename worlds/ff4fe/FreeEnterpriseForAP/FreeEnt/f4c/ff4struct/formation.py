from .bitutil import *

REGULAR_MUSIC = 0
BOSS_MUSIC = 1
FIEND_MUSIC = 2
CONTINUE_MUSIC = 3

class Formation:
    def __init__(self):
        self.gfx_bits = 0
        self.back_attack = False
        self.boss_death = False
        self.eggs = [False, False, False]
        self.monster_types = [0,0,0]
        self.calling = False
        self.transforming = False
        self.monster_qtys = [0,0,0]
        self.arrangement = 0
        self.no_flee = False
        self.no_gameover = False
        self.music = False
        self.character_battle = False
        self.auto_battle = False
        self.floating_enemies = False
        self.transparent = False
        self.cursor_graph_index = 0

    def encode(self):
        encoding = [
            pack_byte('3bbbbb', 
                self.gfx_bits, self.back_attack, 
                self.boss_death, self.eggs[2], self.eggs[1], self.eggs[0]
                ),
            self.monster_types[0],
            self.monster_types[1],
            self.monster_types[2],
            pack_byte('bb222',
                self.calling, self.transforming,
                self.monster_qtys[2],
                self.monster_qtys[1],
                self.monster_qtys[0]
                ),
            self.arrangement,
            pack_byte('bb2bbbb',
                self.no_flee, self.no_gameover, self.music,
                self.character_battle, self.auto_battle, self.floating_enemies, self.transparent
                ),
            self.cursor_graph_index
        ]
        return encoding

def decode(byte_list):
    f = Formation()
    f.gfx_bits, f.back_attack, f.boss_death, f.eggs[2], f.eggs[1], f.eggs[0] = unpack_byte('3bbbbb', byte_list[0])
    f.monster_types = list(byte_list[1:4])
    f.calling, f.transforming, f.monster_qtys[2], f.monster_qtys[1], f.monster_qtys[0] = unpack_byte('bb222', byte_list[4])
    f.arrangement = byte_list[5]
    f.no_flee, f.no_gameover, f.music, f.character_battle, f.auto_battle, f.floating_enemies, f.transparent = unpack_byte('bb2bbbb', byte_list[6])
    f.cursor_graph_index = byte_list[7]
    return f
