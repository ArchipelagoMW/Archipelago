# NOTE: for battle event bits: (address - 1dc9) * 0x8 + bit
# e.g. (1dd1 - 1dc9) * 0x8 + 0x3 = 0x43 (enables display of magic points after battle)

DOUBLE_MORPH_DURATION = 0x39
PARTY_ANNIHILATED = 0x40
ENABLE_MORPH_COMMAND = 0x42
MAGIC_POINTS_AFTER_BATTLE = 0x43
DEFEATED_DOOM_GAZE = 0x48

BOSS_DEFEATED_START = 0x68 # start at unused 0x1dd6
BOSS_DEFEATED_BITS = {}
from ..data.bosses import normal_formation_name
for index, formation in enumerate(normal_formation_name):
    BOSS_DEFEATED_BITS[formation] = BOSS_DEFEATED_START + index

DRAGON_DEFEATED_START = BOSS_DEFEATED_START + len(normal_formation_name)
DRAGON_DEFEATED_BITS = {}
from ..data.bosses import dragon_formation_name
for index, formation in enumerate(dragon_formation_name):
    DRAGON_DEFEATED_BITS[formation] = DRAGON_DEFEATED_START + index

def boss_defeated(formation):
    return BOSS_DEFEATED_BITS[formation]

def dragon_defeated(formation):
    return DRAGON_DEFEATED_BITS[formation]

def byte(battle_bit):
    return battle_bit // 8

def bit(battle_bit):
    return battle_bit % 8

def address(battle_bit):
    return 0x1dc9 + byte(battle_bit)

def battle_address(battle_bit):
    # sram battle bits copied at battle start and updated at battle end
    return 0x3eb4 + byte(battle_bit)
