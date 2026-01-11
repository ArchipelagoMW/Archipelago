from types import SimpleNamespace

targeting_table = {
    0x00: 'MARIO',
    0x01: 'TOADSTOOL',
    0x02: 'BOWSER',
    0x03: 'GENO',
    0x04: 'MALLOW',
    0x10: 'SLOT_1',
    0x11: 'SLOT_2',
    0x12: 'SLOT_3',
    0x13: 'MONSTER_1',
    0x14: 'MONSTER_2',
    0x15: 'MONSTER_3',
    0x16: 'MONSTER_4',
    0x17: 'MONSTER_5',
    0x18: 'MONSTER_6',
    0x19: 'MONSTER_7',
    0x1A: 'MONSTER_8',
    0x1B: 'SELF',
    0x1C: 'ALL_ALLIES_EXCLUDING_SELF',
    0x1D: 'RANDOM_ALLY_EXCLUDING_SELF_OPPONENT_IF_SOLO',
    0x1E: 'ALL_ALLIES_AND_SELF',
    0x1F: 'RANDOM_ALLY_OR_SELF',
    0x23: 'ALL_OPPONENTS',
    0x24: 'AT_LEAST_ONE_OPPONENT',
    0x25: 'RANDOM_OPPONENT',
    0x27: 'AT_LEAST_ONE_ALLY',
    0x28: 'MONSTER_1_D',
    0x29: 'MONSTER_2_D',
    0x2A: 'MONSTER_3_D',
    0x2B: 'MONSTER_4_D',
    0x2C: 'MONSTER_5_D',
    0x2D: 'MONSTER_6_D',
    0x2E: 'MONSTER_7_D',
    0x2F: 'MONSTER_8_D',
}

Targets = SimpleNamespace()
for i in targeting_table:
  setattr(Targets, targeting_table[i], i)


monsters_table = {
    0x00: 'SELF',
    0x01: 'MONSTER_1',
    0x02: 'MONSTER_2',
    0x03: 'MONSTER_3',
    0x04: 'MONSTER_4',
    0x05: 'MONSTER_5',
    0x06: 'MONSTER_6',
    0x07: 'MONSTER_7',
    0x08: 'MONSTER_8',
}

Monsters = SimpleNamespace()
for i in monsters_table:
  setattr(Monsters, monsters_table[i], i)

