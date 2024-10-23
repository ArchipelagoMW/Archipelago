from . import core_rando
from .boss_rando_formation_data import *
from .palette_wizard import PaletteWizard
from .address import *
from .spoilers import SpoilerRow
import math
from copy import copy

CSV_OUTPUT = False

BOSS_SLOTS = list(core_rando.BOSS_SLOTS)
BOSSES = list(core_rando.BOSSES)

SLOTS_WITH_BOSS_DEATH = [
    'milonz_slot', 'kainazzo_slot', 'valvalis_slot', 'rubicant_slot', 'elements_slot'
    ]

SLOTS_WITH_BACK_ATTACK = [
    'milonz_slot'
    ]

SLOTS_WITH_SPECIAL_MUSIC = {
    'mombomb_slot'          : 'continue',
    'fabulgauntlet_slot'    : 'continue',
    'milonz_slot'           : 'fiend',
    'mirrorcecil_slot'      : 'continue',
    'karate_slot'           : 'continue',
    'guard_slot'            : 'continue',
    'kainazzo_slot'         : 'fiend',
    'darkelf_slot'          : 'continue',
    'valvalis_slot'         : 'fiend',
    'calbrena_slot'         : 'continue',
    'golbez_slot'           : 'continue',
    'lugae_slot'            : 'continue',
    'darkimp_slot'          : 'regular',
    'kingqueen_slot'        : 'continue',
    'rubicant_slot'         : 'continue',
    'evilwall_slot'         : 'continue',
    'elements_slot'         : 'continue',
    'cpu_slot'              : 'continue',
    'paledim_slot'          : 'fiend',
    'wyvern_slot'           : 'fiend',
    'plague_slot'           : 'fiend',
    'dlunar_slot'           : 'fiend',
    'ogopogo_slot'          : 'fiend',
    }

SLOTS_WITH_CONTINUE_MUSIC_AND_FANFARE = [
    'cpu_slot',
    'mombomb_slot',
    'darkelf_slot',
    'calbrena_slot',
    'evilwall_slot',
    'elements_slot',
    'golbez_slot',
    ]

FORMATION_MAP = {
    'dmist' : 0xDE,
    'officer' : 0xED,
    'octomamm' : 0xDF,
    'antlion' : 0xE0,
    'waterhag' : 0xEF,
    'mombomb' : 0xE1,
    'fabulgauntlet' : [0xF7, 0xF8, 0xF7, 0xF9, 0xF8, 0xDA],  # 0xDA is copy of 0xF7 used for music purposes
    'milon' : 0xE2,
    'milonz' : 0xE3,
    'mirrorcecil' : 0xF6,
    'guard' : 0xFA,
    'karate' : 0xF2,
    'baigan' : 0xE4,
    'kainazzo' : 0xE5,
    'darkelf' : 0xE7,
    'magus' : 0xE8,
    'valvalis' : 0xEA,
    'calbrena' : 0x1A7,
    'golbez' : 0x1B6,
    'lugae' : [0x1A9, 0x1B5],
    'darkimp' : 0x100,
    'kingqueen' : 0xFE,
    'rubicant' : 0xFF,
    'evilwall' : 0x1AF,
    'asura' : 0x1B0,
    'leviatan' : 0x1AD,
    'odin' : 0x1AC,
    'bahamut' : 0x1AE,
    'elements' : 0xDC,
    'cpu' : 0xDD,
    'paledim' : 0x1FB,
    'wyvern' : 0x1FC,
    'plague' : 0x1FE,
    'dlunar' : 0x1FD,
    'ogopogo' : 0x1FA,
    }

MONSTER_HP_OFFSETS = {
    0xA4 : 10000,  # Mombomb
    0xA5 : 1000,   # Milon
    0xAC : 20000,  # Dark Elf
    0xB4 : 19000,  # Golbez
    0xC4 : 45600,  # Waterhag :>
    0xB9 : 57000,  # K.Eblan
    0xBA : 57000,  # Q.Eblan
    }

MONSTER_HP_SCALED_THRESHOLDS = {
    0xAA : { 0x02 : 700.0 / 4000.0 },    # Kainazzo
    0xB3 : { 0x04 : 100.0 / 4624.0 },    # Calbrena
    0xBB : { 0x0A : 1000.0 / 25200.0 },  # Rubicant
    0xC1 : { 0x08 : 11000.0 / 57000.0,   # Elements
             0x07 : 40000.0 / 57000.0 }, 
    0xC2 : { 0x09 : 27000.0 / 47000.0 }  # Elements
    }

MONSTER_SCRIPTED_CHANGES = {
    0xC4 : ['waterhag', ('defense', 0x60)],
    0xAA : ['kainazzo', ('defense', 0x7A)],
    0xB1 : ['valvalis',
        ('defense', 0x90), 
        ('magic defense', 0xDE),
        ('defense', 0x60),
        ('magic defense', 0xB0),
        ],  
    0x98 : ['wyvern',
        ('spell power', 12),
        ('spell power', 8),
        ('spell power', 6),
        ]
}

MONSTER_ID_REMAPS = {
    0x55 : 0xD6,  # Bomb
    0x56 : 0xD7,  # GrayBomb
    0x16 : 0xD9,  #Weeper
    0x1B : 0xDA,  #ImpCap
    0x15 : 0xDB,  #WaterHag
    0x25 : 0xDC,  #Gargoyle
    0x3A : 0xDE,  #Guard
    0x18 : 0xDD,  #DarkImp
}

SLOT_NPC_LAYOUTS = {
    'dmist_slot' : [],
    'officer_slot' : [['left', 'up', 'down', 'right'], ['left', 'right']],
    'octomamm_slot' : [['up', 'left', 'right', 'down'], ['up', 'down']],
    'antlion_slot' : ['left', 'right'],
    'mombomb_slot' : ['main'],
    'fabulgauntlet_slot' : ['1', '2', '3'],
    'milon_slot' : ['main'],
    'milonz_slot' : ['main'],
    'mirrorcecil_slot' : ['main'],
    'karate_slot' : ['main'],
    'guard_slot' : ['1', '2'],
    'baigan_slot' : ['main'],
    'kainazzo_slot' : ['main'],
    'darkelf_slot' : ['main'],
    'magus_slot' : ['up', 'left', 'right'],
    'valvalis_slot' : ['main'],
    'calbrena_slot' : ['down', 'left', 'right', 'up'],
    'golbez_slot' : ['main'],
    'lugae_slot' : ['main'],
    'darkimp_slot' : ['up', 'left', 'right'],
    'kingqueen_slot' : ['left', 'right'],
    'rubicant_slot' : ['main'],
    'evilwall_slot' : [],
    'asura_slot' : ['main'],
    'leviatan_slot' : ['main'],
    'odin_slot' : ['main'],
    'bahamut_slot' : ['main'],
    'elements_slot' : [['up', 'left', 'right', 'down'], ['left', 'right']],
    'cpu_slot' : [],
    'paledim_slot' : [],
    'wyvern_slot' : [],
    'plague_slot' : [],
    'dlunar_slot' : [],
    'ogopogo_slot' : [],
    }

BOSS_SPRITES = {
    'dmist' : [
        ['IceWall', 0x05, 2]
        ],
    'officer' : [
        ['Captain', 0x00, 1], 
        ['Soldier', 0x00, 0], 
        ['Soldier', 0x00, 0], 
        ['Soldier', 0x00, 0],
        ],
    'octomamm' : [
        ['OctomammTentacles', 0x00, 0], 
        ['OctomammTentacles', 0x00, 0], 
        ['OctomammTentacles', 0x00, 0], 
        ['OctomammTentacles', 0x00, 0]
        ],
    'antlion' : { 
        'left' : ['AntlionClawLeft', 0x00, 0],
        'right' : ['AntlionClawRight', 0x00, 0]
        },
    'waterhag' : [
        ['HoodedMonster', 0x00, 1],
        ],
    'mombomb' : [
        ['Bomb', 0x00, 0],
        ],
    'fabulgauntlet' : [
        ['HoodedMonster', 0x00, 1], 
        ['HoodedMonster', 0x00, 1], 
        ['HoodedMonster', 0x00, 1],
        ],
    'milon' : [
        ['HoodedMonster', 0x01, 2],
        ],
    'milonz' : [
        ['HoodedMonster', 0x01, 2],
        ],
    'mirrorcecil' : [
        ['DKCecil', 0x00, 0],
        ],
    'guard' : [
        ['Captain', 0x00, 1], 
        ['Captain', 0x00, 1],
        ],
    'karate' : [
        ['Yang', 0x00, 0],
        ],
    'baigan' : [
        ['Captain', 0x00, 0]
        ],
    'kainazzo' : [
        ['Kainazzo', 0x00, 1]
        ],
    'darkelf' : [
        ['DarkElf', 0x00, 1]
        ],
    'magus' : [
        ['MagusSister', 0x01, 2], 
        ['MagusSister', 0x00, 0], 
        ['MagusSister', 0x00, 1]
        ],
    'valvalis' : [
        ['Valvalis', 0x00, 0]
        ],
    'calbrena' : [
        ['Calbrena', 0x00, 0], 
        ['Calbrena', 0x00, 0], 
        ['Calbrena', 0x00, 0], 
        ['Calbrena', 0x00, 0]
        ],
    'golbez' : [
        ['Golbez', 0x00, 1]
        ],
    'lugae' : [
        ['Lugae', 0x01, 3]
        ],
    'darkimp' : [
        ['HoodedMonster', 0x00, 0], 
        ['HoodedMonster', 0x00, 0], 
        ['HoodedMonster', 0x00, 0]
        ],
    'kingqueen' : [
        ['King', 0x00, 1], 
        ['Queen', 0x03, 3]
        ],
    'rubicant' : [
        ['Rubicant', 0x00, 0]
        ],
    'evilwall' : [
        ['DoubleDoor', 0x07, 3]
        ],
    'asura' : [
        ['Queen', 0x00, 1]
        ],
    'leviatan' : [
        ['OldMan', 0x01, 2]
        ],
    'odin' : [
        ['King', 0x00, 0]
        ],
    'bahamut' : [
        ['Bahamut', 0x03, 3]
        ],
    'elements' : {
        'up'     : ['Rubicant', 0x00, 0],
        'left'   : ['Valvalis', 0x00, 0],
        'right'  : ['Kainazzo', 0x00, 1],
        'down'   : ['HoodedMonster', 0x00, 0]
        },
    'cpu' : [
        ['DeathBall', 0x07, 3], 
        ['DeathBall', 0x07, 3], 
        ['DeathBall', 0x07, 3]
        ],
    'paledim' : [
        ['Sparkle', 0x00, 0]
        ],
    'wyvern' : [
        ['Sparkle', 0x00, 0]
        ],
    'plague' : [
        ['Sparkle', 0x00, 0]
        ],
    'dlunar' : [
        ['Sparkle', 0x00, 0]
        ],
    'ogopogo' : [
        ['Sparkle', 0x00, 0]
        ],
}

MULTITARGET_BOSSES = [
    'officer', 'mombomb', 'fabulgauntlet', 'milon', 'guard', 'baigan', 
    'magus', 'calbrena', 'lugae', 'darkimp', 'kingqueen', 'cpu', 'dlunar'
    ]

SLOT_PALETTE_PRESERVATIONS = {
    # values are: [priority, palette-pair index, desired palette index]
    #         or: [priority, [custom palette values], desired palette index]
    'dmist_slot' : {  #actually used for Rubicant in Cave Eblan
        'soldier' : [2, 0x00, 1],
        'fire' : [0, 0x00, 0],
        },
    'octomamm_slot' : {
        'splash' : [0, 0x05, 2]
        },
    'fabulgauntlet_slot' : {
        'monk' : [2, 0x00, 1]
        },
    'mirrorcecil_slot' : {
        'sparkle' : [0, 0x00, 0]
        },
    'karate_slot' : {
        'innkeepergirl' : [2, 0x00, 0],
        'man' : [2, 0x01, 2]
        },
    'guard_slot' : {
        'innkeepergirl' : [2, 0x00, 0],
        'man' : [2, 0x01, 2]
        },
    'baigan_slot' : {
        'soldier' : [2, 0x00, 0]
        },
    'kainazzo_slot' : {
        'king' : [2, 0x00, 0],
        'guard' : [2, 0x00, 1]
        },
    'darkelf_slot' : {
        'crystal' : [2, 0x04, 2],
        'darkelf' : [2, 0x00, 1],
        'harp' : [2, 
            [0x00,0x00,0xff,0x7f,0x9f,0x1f,0x18,0x53,0x31,0x3e,0xad,0x31,0x9e,0x0d,0x08,0x19],
            0],
        },
    'magus_slot' : {
        'teleport' : [0, 0x00, 0]
        },
    'valvalis_slot' : {
        'deathball' : [2, 0x07, 3],
        'tied_up_rosa' : [0, 0x07, 2]
        },
    'calbrena_slot' : {
        'crystal' : [2, 0x04, 2]
        },
    'golbez_slot' : {
        'crystal' : [2, 0x04, 2]
        },
    'lugae_slot' : {
        'teleport' : [0, 0x00, 0]
        },
    'darkimp_slot' : {
        'teleport' : [0, 0x00, 0]
        },
    'rubicant_slot' : {
        'firemagic' : [0, 0x00, 0]
        },
    'evilwall_slot' : { #actually used for Golbez in Zot
        'lightning' : [0, 0x05, 2]
        },
    'asura_slot' : {
        'monster' : [2, 0x00, 0]
        },
    'leviatan_slot' : {     # actually used for Calbrena in throne room
        'giott' : [2, 0x01, 2],
        'luca' : [2, 0x00, 0],
        'dwarf' : [2, 0x00, 1],
        },
    'bahamut_slot' : {
        'children' : [2, 0x03, 3]
        }
}

BOSS_SPOILER_NAMES = {
    'dmist' : 'D.Mist',
    'officer' : 'Kaipo Officer/Soldiers',
    'octomamm' : 'Octomamm',
    'antlion' : 'Antlion',
    'waterhag' : 'WaterHag',
    'mombomb' : 'MomBomb',
    'fabulgauntlet' : 'Fabul gauntlet',
    'milon' : 'Milon',
    'milonz' : 'Milon Z.',
    'mirrorcecil' : 'D.Knight',
    'guard' : 'Baron Inn Guards',
    'karate' : 'Karate',
    'baigan' : 'Baigan',
    'kainazzo' : 'Kainazzo',
    'darkelf' : 'Dark Elf (dragon)',
    'magus' : 'Magus Sisters',
    'valvalis' : 'Valvalis',
    'calbrena' : 'Calbrena',
    'golbez' : 'Golbez',
    'lugae' : 'Lugae',
    'darkimp' : 'Dark Imps',
    'kingqueen' : 'King/Queen Eblan',
    'rubicant' : 'Rubicant',
    'evilwall' : 'EvilWall',
    'asura' : 'Asura',
    'leviatan' : 'Leviatan',
    'odin' : 'Odin',
    'bahamut' : 'Bahamut',
    'elements' : 'Elements',
    'cpu' : 'CPU',
    'paledim' : 'Pale Dim',
    'wyvern' : 'Wyvern',
    'plague' : 'Plague',
    'dlunar' : 'D.Lunars',
    'ogopogo' : 'Ogopogo',
}

BOSS_SLOT_SPOILER_NAMES = { f"{b}_slot": BOSS_SPOILER_NAMES[b] + " position" for b in BOSS_SPOILER_NAMES }

ALT_GAUNTLETS = {
    'dmist_slot' : [0x07, 0x05, 0x08, 0xD0, 0xD1],
    'officer_slot' : [0x0A, 0x06, 0x09, 0x08, 0x0B],
    'octomamm_slot' : [0x18, 0x17, 0x19, 0x1A, 0x1B],
    'antlion_slot' : [0x25, 0x26, 0x27, 0x1F, 0x1E],
    'mombomb_slot' : [0x28, 0x2C, 0x2F, 0x2D, 0x33],
    'fabulgauntlet_slot' : [0x36, 0x2C, 0x2A, 0x2E, 0x37],
    'milon_slot' : [0x33, 0x3C, 0x3D, 0x3E, 0x3F],
    'milonz_slot' : [0x42, 0x43, 0x44, 0x45, 0x3F],
    'mirrorcecil_slot' : [0x47, 0x3F, 0x46, 0x48, 0x49],
    'karate_slot' : [0x4C, 0x4D, 0x4E, 0x4F, 0x50],
    'guard_slot' : [0x4C, 0x4D, 0x4E, 0x4F, 0x50],
    'baigan_slot' : [0x4F, 0x52, 0x50, 0x53, 0x54],
    'kainazzo_slot' : [0x56, 0x51, 0x56, 0x54, 0x57],
    'darkelf_slot' : [0x67, 0x68, 0x69, 0x6A, 0x65],
    'magus_slot' : [0x71, 0x7B, 0x74, 0x79, 0x7F],
    'valvalis_slot' : [0x7D, 0x6D, 0x79, 0x73, 0x7F],
    'calbrena_slot' : [0x103, 0x104, 0x105, 0x106, 0x107],
    'golbez_slot' : [0x103, 0x104, 0x105, 0x106, 0x107],
    'lugae_slot' : [0x11E, 0x120, 0x11F, 0x114, 0x118],
    'darkimp_slot' : [0x119, 0x11A, 0x11B, 0x107, 0x115],
    'kingqueen_slot' : [0xA0, 0x9D, 0xA6, 0xB6, 0xB2],
    'rubicant_slot' : [0xA0, 0xAE, 0xAA, 0xB6, 0xB2],
    'evilwall_slot' : [0x164, 0x167, 0x16A, 0x162, 0x169],
    'asura_slot' : [0x154, 0x155, 0x156, 0x157, 0x15A],
    'leviatan_slot' : [0x150, 0x155, 0x156, 0x157, 0x15B],
    'odin_slot' : [0x153, 0x154, 0x156, 0x157, 0x15A],
    'bahamut_slot' : [0x188, 0x189, 0x185, 0x186, 0x18A],
    'elements_slot' : [0xC9, 0xBF, 0xCA, 0xC7, 0xCE],
    'cpu_slot' : [0xC8, 0xCE, 0xC7, 0xCA, 0xCE],
    'paledim_slot' : [0x188, 0x189, 0x185, 0x186, 0x18A],
    'wyvern_slot' : [0x18D, 0x18B, 0x18A, 0x18E, 0x18F],
    'plague_slot' : [0x191, 0x192, 0x193, 0x194, 0x195],
    'dlunar_slot' : [0x191, 0x192, 0x193, 0x194, 0x195],
    'ogopogo_slot' : [0x197, 0x1A3, 0x197, 0x199, 0x19A],
}

def _is_moon_formation(formation_number):
    if (formation_number >= 0x180 and formation_number <= 0x1A3):
        return True
    elif (formation_number in [0x1AE, 0x1B3, 0x1B4, 0x1B7]):
        return True
    elif (formation_number >= 0x1F0):
        return True
    else:
        return False

def _get_cumulative_formation(formation_data):
    if type(formation_data) is not list:
        formation_data = [formation_data]

    cumulative_formation = {}
    for f in formation_data:
        if type(f) is int:
            if f == 0xDA:  # fabul gauntlet formation remap
                f = FORMATION_DATA[0xF7]
            else:
                f = FORMATION_DATA[f]

        for monster_id in f:
            if monster_id in cumulative_formation:
                cumulative_formation[monster_id]['qty'] += f[monster_id]['qty']
            else:
                cumulative_formation[monster_id] = copy(f[monster_id])
    return cumulative_formation

def _get_total_hp_xp_gp_qty(formation_data):
    total_hp = 0
    total_gp = 0
    total_xp = 0
    total_qty = 0

    for monster_id in _get_cumulative_formation(formation_data):
        monster = formation_data[monster_id]
        hp = monster['hp']
        if monster_id in MONSTER_HP_OFFSETS:
            hp -= MONSTER_HP_OFFSETS[monster_id]
        total_hp += (hp * monster['qty'])
        total_xp += (monster['xp'] * monster['qty'])
        total_gp += (monster['gp'] * monster['qty'])
        total_qty += monster['qty']

    return (total_hp, total_xp, total_gp, total_qty)

def _get_leader(formation_data):
    leader = None
    leader_hp = None
    for monster_id in _get_cumulative_formation(formation_data):
        monster = formation_data[monster_id]
        hp = monster['hp']
        if monster_id in MONSTER_HP_OFFSETS:
            hp -= MONSTER_HP_OFFSETS[monster_id]
        if leader is None or hp > leader_hp:
            leader = monster
            leader_hp = hp
    return leader

def _get_closest_stat(ideal, table, weighting):
    closest = min(table, key = lambda t:
        sum([abs(t[i] - ideal[i]) * weighting[i] for i in range(len(ideal))])
        )

    index = table.index(closest)
    return (index, closest)

def _get_spell_power_ratio(monster1, monster2):
    if monster1['spell power'] is None or monster2['spell power'] is None:
        # heuristically guess a spell power ratio based on ratio of levels
        return monster1['level'] / monster2['level']
    else:
        return monster1['spell power'] / monster2['spell power']


def apply(env):
    # random boss assignments handled in core_rando

    script_lines = []
    palettes = {}

    output_music = {}
    output_formations = {}
    limit_breaks = []

    stat_scaling_reports = []

    assignment = {k : env.assignments[k] for k in env.assignments if k in BOSS_SLOTS}

    for slot in assignment:
        boss = assignment[slot]
        is_alt_gauntlet = (env.options.flags.has('bosses_alt_gauntlet') and boss == 'fabulgauntlet')

        source_formation_id = FORMATION_MAP[slot[:-5]] # remove "_slot" suffix
        target_formation_id = FORMATION_MAP[boss]

        script_lines.append(f'// {slot} <- {boss}')

        source_formation_id_list = (source_formation_id if type(source_formation_id) is list else [source_formation_id])
        target_formation_id_list = (target_formation_id if type(target_formation_id) is list else [target_formation_id])

        if is_alt_gauntlet:
            alt_gauntlet_indicator = 0xFE00
            if slot in SLOTS_WITH_BACK_ATTACK:
                alt_gauntlet_indicator |= 0x0040
            output_formations[slot] = [alt_gauntlet_indicator] + ALT_GAUNTLETS[slot]
        else:
            output_formations[slot] = target_formation_id_list

        output_music[slot] = 0xFF

        palette_slots = [slot]
        if slot == 'leviatan_slot':
            palette_slots = ['asura_slot']
        elif slot == 'dmist_slot' or slot == 'evilwall_slot':
            palette_slots = []

        if slot == 'calbrena_slot':
            # borrow the unused Leviatan slot for the 
            # Calbrena in the Dwarf castle throne room
            palette_slots.append('leviatan_slot')
        elif slot == 'rubicant_slot':
            palette_slots.append('lugae_slot')
            palette_slots.append('dmist_slot') # borrow for Rubicant in Eblan cave
        elif slot == 'golbez_slot':
            palette_slots.append('evilwall_slot') # borrow for Golbez in Zot

        for p in palette_slots:
            if p not in palettes:
                palettes[p] = PaletteWizard()
                if p in SLOT_PALETTE_PRESERVATIONS:
                    preservations = SLOT_PALETTE_PRESERVATIONS[p]
                    for name in preservations:
                        if type(preservations[name][1]) is list:
                            priority, palette_data, index = preservations[name]
                            palettes[p].assign_custom_palette(palette_data, index=index, priority=priority)
                        else:
                            priority, pair_index, index = preservations[name]
                            palettes[p].assign_npc_palette(pair_index, index, index=index, priority=priority, vintage=env.options.flags.has('vintage'))

        handled_formations = set()
        for i,tid in enumerate(target_formation_id_list):
            if tid in handled_formations:
                continue
            handled_formations.add(tid)

            script_lines.append(f'formation(${tid:X}) {{')

            if slot in SLOTS_WITH_BOSS_DEATH and boss not in MULTITARGET_BOSSES:
                script_lines.append('    boss death')
            else:
                script_lines.append('    not boss death')

            if slot in SLOTS_WITH_BACK_ATTACK:
                script_lines.append('    back attack')
            else:
                script_lines.append('    not back attack')

            slot_music = SLOTS_WITH_SPECIAL_MUSIC.get(slot, 'boss')
            if len(target_formation_id_list) == 1:
                script_lines.append(f'    {slot_music} music')
            else:
                script_lines.append('    continue music')
                if i == 0:
                    OUTPUT_MUSIC_MAP = {
                        'regular' : 0x27, # music.Battle
                        'boss' :    0x1A, # music.BossBattle
                        'fiend' :   0x0B, # music.DecisiveBattle
                        'continue': 0xFF
                    }
                    output_music[slot] = OUTPUT_MUSIC_MAP[slot_music]

            script_lines.append('}')

        source_formation = _get_cumulative_formation(source_formation_id_list)
        target_formation = _get_cumulative_formation(target_formation_id_list)

        # get reference stats from original formation in slot
        ref_hp, ref_xp, ref_gp, ref_qty = _get_total_hp_xp_gp_qty(source_formation)
        ref_leader = _get_leader(source_formation)

        # calculate and apply new values for formation going into slot
        total_hp, total_xp, total_gp, total_qty = _get_total_hp_xp_gp_qty(target_formation)
        leader = _get_leader(target_formation)

        env.add_substitution(f'{boss} defaults', '')
        stat_scaling_reports.append(f'{slot} <- {boss}')
        for monster_id in target_formation:
            monster = target_formation[monster_id]
            csv_row = [boss, slot, monster['name']]

            if monster_id in MONSTER_ID_REMAPS:
                script_lines.append(f'monster(${MONSTER_ID_REMAPS[monster_id]:02X}) {{')
            else:
                script_lines.append(f'monster(${monster_id:02X}) {{')

            if env.options.flags.has('no_free_bosses'):
                script_lines.append('    boss')

            hp = monster['hp']
            if monster_id in MONSTER_HP_OFFSETS:
                hp -= MONSTER_HP_OFFSETS[monster_id]
            scaled_hp = int(math.ceil(hp / total_hp * ref_hp))
            if monster_id in MONSTER_HP_OFFSETS:
                restore_threshold = True
                if boss == 'kingqueen':
                    restore_threshold = False
                if env.options.flags.has('no_free_bosses') and boss == 'waterhag':
                    restore_threshold = False
                if restore_threshold:
                    scaled_hp += MONSTER_HP_OFFSETS[monster_id]
            scaled_hp = min(65000, scaled_hp)

            if total_xp == 0:
                scaled_xp = int(ref_xp / total_qty)
            else:
                scaled_xp = int(math.ceil(monster['xp'] / total_xp * ref_xp))

            if total_gp == 0:
                scaled_gp = int(ref_gp / total_qty)
            else:
                scaled_gp = min(65000, int(math.ceil(monster['gp'] / total_gp * ref_gp)))

            scaled_xp_actual = scaled_xp
            if scaled_xp >= 0xFF00:
                # use break limit table
                limit_break_index = len(limit_breaks)
                limit_breaks.append(scaled_xp)
                scaled_xp = 0xFFF0 + limit_break_index
                if scaled_xp > 0xFFFF:
                    raise Exception("Limit break table has too many entries")

            scaled_level = int(math.ceil(monster['level'] * ref_leader['level'] / leader['level']))
            scaled_level = max(1, min(99, scaled_level))

            script_lines.append(f'    level {scaled_level}')
            script_lines.append(f'    hp {scaled_hp}')
            script_lines.append(f'    xp {scaled_xp}')
            script_lines.append(f'    gp {scaled_gp}')

            csv_row.extend([scaled_level, scaled_hp, scaled_xp_actual, scaled_gp])

            monster_scaled_stats = {}
            stat_scaling_reports.append(f'monster(${monster_id:02X})')
            for stats_name in ['attack', 'defense', 'magic defense', 'speed']:
                stat_scaling_reports.append(stats_name)
                stat_scaling_reports.append('monster : ' + str(monster[stats_name]))
                stat_scaling_reports.append('leader  : ' + str(leader[stats_name]))
                if sum(leader[stats_name]) == 0:
                    stats_ratio = [monster['level'] / leader['level']] * len(monster[stats_name])
                else:
                    stats_ratio = [monster[stats_name][i] / max(leader[stats_name][i], 1) for i in range(len(monster[stats_name]))]
                stat_scaling_reports.append('ratio   : ' + str(stats_ratio))
                stat_scaling_reports.append('reflead : ' + str(ref_leader[stats_name]))
                stats_ideal = [ref_leader[stats_name][i] * stats_ratio[i] for i in range(len(stats_ratio))]
                stat_scaling_reports.append('ideal   : ' + str(stats_ideal))
                if stats_name == 'speed':
                    closest_index, closest_value = _get_closest_stat(stats_ideal, SPEED_TABLE, (1.0,1.0))
                else:
                    closest_index, closest_value = _get_closest_stat(stats_ideal, STATS_TABLE, (1.0, 0.1, 1.0))
                stat_scaling_reports.append(f'closest : {closest_value} (${closest_index:02X})')

                script_lines.append(f'    {stats_name} index ${closest_index:02X}  // {closest_value}')
                monster_scaled_stats[stats_name] = closest_value
                csv_row.extend(closest_value)

            if monster['spell power'] is not None:
                scaled_spell_power = min(255, int(math.ceil(monster['spell power'] * _get_spell_power_ratio(ref_leader, leader))))
                script_lines.append(f'    spell power {scaled_spell_power}')
                csv_row.append(scaled_spell_power)
            else:
                csv_row.append('')

            script_lines.append('}')

            if monster_id in MONSTER_HP_SCALED_THRESHOLDS:
                for threshold_id in MONSTER_HP_SCALED_THRESHOLDS[monster_id]:
                    ratio = MONSTER_HP_SCALED_THRESHOLDS[monster_id][threshold_id]
                    scaled_threshold = int(math.ceil(scaled_hp * ratio))
                    script_lines.append('patch(${:X}) {{ {:02X} {:02X} }}  // adjust AI HP threshold to {}'.format(
                        0x76000 + (threshold_id * 2),
                        (scaled_threshold & 0xFF),
                        ((scaled_threshold >> 8) & 0xFF),
                        scaled_threshold
                        ))
                    csv_row.append(f'scriptHP: {scaled_threshold}')

            if monster_id in MONSTER_SCRIPTED_CHANGES:
                monster_name = MONSTER_SCRIPTED_CHANGES[monster_id][0]
                for pair in MONSTER_SCRIPTED_CHANGES[monster_id][1:]:
                    stat, value = pair
                    if stat == 'spell power':
                        scaled_value = str(min(255, int(math.ceil(value * _get_spell_power_ratio(ref_leader, leader)))))
                        env.add_substitution(f'{monster} script spell power change {value}', f'set spell power {scaled_value}')
                        csv_row.append(f'scriptSpellPower: {scaled_value}')
                    else:
                        stats_scripted = (SPEED_TABLE if stat == 'speed' else STATS_TABLE)[value]
                        stats_ratio = [stats_scripted[i] / max(monster[stat][i], 1) for i in range(len(stats_scripted))]
                        stats_ideal = [monster_scaled_stats[stat][i] * stats_ratio[i] for i in range(len(stats_ratio))]
                        if stat == 'speed':
                            closest_index, closest_value = _get_closest_stat(stats_ideal, SPEED_TABLE, (1.0, 1.0))
                        else:
                            closest_index, closest_value = _get_closest_stat(stats_ideal, STATS_TABLE, (1.0, 0.1, 1.0))
                        env.add_substitution(f'{monster_name} script {stat} change ${value:02X}', f'set {stat} index ${closest_index:02X}')
                        csv_row.append(f'script-{stat}: {"-".join([str(v) for v in closest_value])}')

            if CSV_OUTPUT:
                print(','.join([str(v) for v in csv_row]))

        # assign NPC sprites according to slot layout and boss NPC sprites
        layout = SLOT_NPC_LAYOUTS[slot]
        sprites = BOSS_SPRITES[boss]
        if env.meta.get('wacky_challenge', None) == 'enemyunknown':
            sprites = [
                ['Sparkle', 0x00, 1]
                ]

        if layout:
            if type(layout[0]) is list:
                # multiple layouts specified
                max_layout = max(layout, key = len)
                if type(sprites) is dict:
                    # sprites specified directionally
                    layout = max_layout
                else:
                    # sprites specified in priority order, try to find matched length
                    ideal_layouts = [l for l in layout if len(l) == len(sprites)]
                    if ideal_layouts:
                        layout = ideal_layouts[0]
                    else:
                        layout = max_layout
            else:
                max_layout = layout

            layout_assignments = dict()
            if type(sprites) is dict:
                unused_list = []
                for direction in sprites:
                    if direction in layout:
                        layout_assignments[direction] = sprites[direction]
                    else:
                        unused_list.append(sprites[direction])
                # map any unused directional sprites in layout order, if possible
                for direction in layout:
                    if not unused_list:
                        break
                    if direction not in layout_assignments:
                        layout_assignments[direction] = unused_list.pop(0)
            else:
                # directly assign sprites in priority order
                for i in range(min(len(layout), len(sprites))):
                    layout_assignments[layout[i]] = sprites[i]

            # blank out unused layout spaces
            for direction in max_layout:
                if direction not in layout_assignments:
                    layout_assignments[direction] = ['Transparent', None, None]

            # generate substitutions
            for direction in layout_assignments:
                sprite, palette_pair, palette_index = layout_assignments[direction]
                env.add_substitution(f'{slot} sprite {direction}', f'#sprite.{sprite}')
                if palette_pair is not None:
                    for i,p in enumerate(palette_slots):
                        if i == 0:
                            pname = f'{slot} sprite {direction}'
                        else:
                            pname = f'{slot} alt{i} sprite {direction}'
                        palettes[p].assign_npc_palette(palette_pair, palette_index, priority=1, name=pname, vintage=env.options.flags.has('vintage'))

    # output palette data
    script_lines.append('patch($21b000 bus) {')
    for slot in BOSS_SLOTS:
        if slot not in palettes:
            script_lines.append('00 ' * 0x40)
            continue

        data = palettes[slot].get_data()
        script_lines.append(' '.join([f'{b:02X}' for b in data]))

        named_assignments = palettes[slot].get_named_assignments()
        for name in named_assignments:
            env.add_substitution(f'{name} palette', f'palette {named_assignments[name]}')
    script_lines.append('}')

    # need to mark appropriate formations for "continues music but plays fanfare"
    fanfare_formation_ids = set()
    for slot in assignment:
        if assignment[slot] == 'fabulgauntlet' and env.options.flags.has('bosses_alt_gauntlet'):
            if slot in SLOTS_WITH_CONTINUE_MUSIC_AND_FANFARE or SLOTS_WITH_SPECIAL_MUSIC.get(slot, 'boss') != 'continue':
                # mark special bit in sentinel value
                output_formations[slot][0] |= 0x80
        elif len(output_formations[slot]) == 1:
            if slot in SLOTS_WITH_CONTINUE_MUSIC_AND_FANFARE:
                fanfare_formation_ids.add(output_formations[slot][0])
        else:
            if (slot in SLOTS_WITH_CONTINUE_MUSIC_AND_FANFARE) or (slot not in SLOTS_WITH_SPECIAL_MUSIC) or (SLOTS_WITH_SPECIAL_MUSIC[slot] != 'continue'):
                fanfare_formation_ids.add(output_formations[slot][-1])

    fanfare_formation_ids = sorted(fanfare_formation_ids)
    env.add_substitution('randomizer fanfare formations', ' '.join(['{:02X} {:02X}'.format(i & 0xFF, (i >> 8) & 0xFF) for i in fanfare_formation_ids]))

    # output music
    env.blob.add('BossFormations__Music', [output_music[slot] for slot in output_music])

    # output randomized formations
    formation_data = []
    for slot in BOSS_SLOTS:
        fids = []
        for f in output_formations[slot]:
            if f & 0xFF00 == 0xFE00:
                # special code, output it raw
                fids.append(f)
            elif _is_moon_formation(f):
                fids.append(f | 0x8000)
            else:
                fids.append(f)
        if len(fids) < 8:
            fids.append(0xFFFF)
            while len(fids) < 8:
                if env.options.debug:
                    fids.append(0xFFFF)
                else:
                    fids.append(env.rnd.randint(0x0000, 0xFFFF))

        for fid in fids:
            formation_data.append(fid & 0xFF)
            formation_data.append((fid >> 8) & 0xFF)
    
    env.blob.add('BossFormations__Table', formation_data, 
        callback=lambda a: {
            'BossFormations__TablePlus1': a['BossFormations__Table'] + 1,
            'BossFormations__TablePlus3': a['BossFormations__Table'] + 3,
            })

    # create limit break table
    if limit_breaks:
        script_lines.append('patch($21f500 bus) {')
        for xp in limit_breaks:
            script_lines.append('{:02X} {:02X} {:02X} 00'.format(
                xp & 0xFF,
                (xp >> 8) & 0xFF,
                (xp >> 16) & 0xFF
                ))
        script_lines.append('}')

    env.add_file('scripts/randomizer_boss.f4c')

    # special case wyvern
    if assignment['milonz_slot'] == 'wyvern' and not env.options.flags.has('wyvern_no_meganuke') and not env.options.flags.has('wyvern_random_meganuke'):
        env.add_file('scripts/wyvern_slowmeganuke.f4c')

    #print('\n'.join(stat_scaling_reports))

    env.add_script('\n'.join(script_lines))


    # generate spoiler
    boss_spoilers = []
    missing_bosses = set(BOSSES)
    for slot in assignment:
        boss = assignment[slot]
        missing_bosses.remove(boss)
        boss_spoilers.append( SpoilerRow(BOSS_SLOT_SPOILER_NAMES[slot], BOSS_SPOILER_NAMES[boss], obscurable=True) )
    for boss in missing_bosses:
        boss_spoilers.append( SpoilerRow("(not available)", BOSS_SPOILER_NAMES[boss], obscurable=True) )
    env.spoilers.add_table("BOSSES", boss_spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:bosses'))

if __name__ == '__main__':
    from .FreeEnt import FreeEntOptions
    import random

    CSV_OUTPUT = True
    bosses = list(core_rando.BOSSES)

    options = FreeEntOptions()
    options.flags.load('B')

    rnd = random.Random()

    for i in range(len(bosses)):
        assignment = dict(zip(core_rando.BOSS_SLOTS, bosses))
        result = randomize(rnd, options, assignment)
        bosses.append(bosses.pop(0))
    
    #print(result['script'])
    #for k in result['substitutions']:
    #    print('{} -> {}'.format(k, result['substitutions'][k]))


