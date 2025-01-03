from . import util

_WEIRDER = False

PALETTE_ADDRS = {
    'pc0'           : 0x0d8000,
    'pc1'           : 0x0d8010,
    'pc2'           : 0x0d8020,
    'pc3'           : 0x0d8030,
    'world0'        : 0x0d8040,
    'world1'        : 0x0d8050,
    'world2'        : 0x0d8060,
    'world3'        : 0x0d8070,
    'stone'         : 0x0d80c0,
    'npc_red'       : 0x0d80d0,  # npc palette pair 0
    'npc_blue'      : 0x0d80e0,
    'npc_purple'    : 0x0d80f0,  # npc palette pair 1
    'npc_green'     : 0x0d8100,
    'choco_yellow'  : 0x0d8110,  # npc palette pair 2
    'choco_white'   : 0x0d8120,
    #'npc_????'      : 0x0d8130,  # npc palette pair 3
    'bahamut'       : 0x0d8140,
    'light_crystal' : 0x0d8150,  # npc palette pair 4
    'dark_crystal'  : 0x0d8160,
    'splash'        : 0x0d8170,  # npc palette pair 5
    'tied_up_rosa'  : 0x0d8180,
    'babil_no_bridge' : 0x0d8190,  # npc palette pair 6
    'frog'          : 0x0d81a0,
    'kiss'          : 0x0d81b0,  # npc palette pair 7
    'grayscale'     : 0x0d81c0,
    'blond_kain'    : 0x0d81d0,  # npc palette pair 8
    'choco_black'   : 0x0d81e0,
    'fire'          : 0x0d81f0,  # npc palette pair 9
    'poof'          : 0x0d8200,
    'ocean'         : 0x0d8210,
    'robot?'        : 0x0d8220,
    'giant'         : 0x0d8230,
    }

NPC_STANDARD = ['npc_red', 'npc_blue', 'npc_purple']

SPRITES = [
    {'npc_sprite' : 0x00, 'palettes' : ['pc0']},   #DKCecil
    {'npc_sprite' : 0x01, 'palettes' : ['pc0']},   #Kain
    {'npc_sprite' : 0x02, 'palettes' : ['pc1']},   #CRydia
    {'npc_sprite' : 0x03, 'palettes' : ['pc2']},   #Tellah
    {'npc_sprite' : 0x04, 'palettes' : ['pc2']},   #Edward
    {'npc_sprite' : 0x05, 'palettes' : ['pc2']},   #Rosa
    {'npc_sprite' : 0x06, 'palettes' : ['pc0']},   #Yang
    {'npc_sprite' : 0x07, 'palettes' : ['pc2']},   #Palom
    {'npc_sprite' : 0x08, 'palettes' : ['pc2']},   #Porom
    {'npc_sprite' : 0x09, 'palettes' : ['pc3']},   #PCecil
    {'npc_sprite' : 0x0A, 'palettes' : ['pc0']},   #Cid
    {'npc_sprite' : 0x0B, 'palettes' : ['pc1']},   #ARydia
    {'npc_sprite' : 0x0C, 'palettes' : ['pc0']},   #Edge
    {'npc_sprite' : 0x0D, 'palettes' : ['pc0']},   #Fusoya
    {'npc_sprite' : 0x0E, 'palettes' : NPC_STANDARD},   #Mini
    {'npc_sprite' : 0x0F, 'palettes' : ['frog']},   #Frog
    {'npc_sprite' : 0x10, 'palettes' : ['pc0', 'pc1', 'pc2', 'pc3', 'npc_red']},   #Pig
    {'npc_sprite' : 0x11, 'palettes' : NPC_STANDARD},   #Man
    {'npc_sprite' : 0x12, 'palettes' : NPC_STANDARD},   #Woman
    {'npc_sprite' : 0x13, 'palettes' : NPC_STANDARD},   #Dancer
    {'npc_sprite' : 0x14, 'palettes' : NPC_STANDARD},   #OldMan
    {'npc_sprite' : 0x15, 'palettes' : NPC_STANDARD},   #OldWoman
    {'npc_sprite' : 0x16, 'palettes' : NPC_STANDARD},   #Boy
    {'npc_sprite' : 0x17, 'palettes' : NPC_STANDARD},   #Girl
    {'npc_sprite' : 0x18, 'palettes' : NPC_STANDARD},   #Soldier
    {'npc_sprite' : 0x19, 'palettes' : NPC_STANDARD},   #BeardedMan
    {'npc_sprite' : 0x1A, 'palettes' : NPC_STANDARD},   #Scholar
    {'npc_sprite' : 0x1B, 'palettes' : ['npc_blue']},   #BlackMage
    {'npc_sprite' : 0x1C, 'palettes' : ['npc_red']},   #WhiteMage
    {'npc_sprite' : 0x1D, 'palettes' : ['npc_blue']},   #Engineer
    {'npc_sprite' : 0x1E, 'palettes' : ['choco_yellow', 'choco_white', 'choco_black']},   #Chocobo
    {'npc_sprite' : 0x1F, 'palettes' : ['npc_blue']},   #Monk
    {'npc_sprite' : 0x20, 'palettes' : NPC_STANDARD},   #Captain
    {'npc_sprite' : 0x21, 'palettes' : ['npc_red']},   #Bomb
    {'npc_sprite' : 0x22, 'palettes' : NPC_STANDARD},   #HoodedMonster
    {'npc_sprite' : 0x23, 'palettes' : ['npc_blue']},   #Namingway
    {'npc_sprite' : 0x24, 'palettes' : ['npc_blue']},   #Golbez
    {'npc_sprite' : 0x25, 'palettes' : NPC_STANDARD},   #King
    {'npc_sprite' : 0x26, 'palettes' : ['npc_blue']},   #Elder
    {'npc_sprite' : 0x27, 'palettes' : ['npc_purple']},   #Cleric
    {'npc_sprite' : 0x28, 'palettes' : NPC_STANDARD},   #Dwarf
    {'npc_sprite' : 0x29, 'palettes' : ['npc_red']},   #Calbrena
    {'npc_sprite' : 0x2A, 'palettes' : ['npc_purple']},   #Giott
    {'npc_sprite' : 0x2B, 'palettes' : ['npc_green']},   #Lugae
    {'npc_sprite' : 0x2C, 'palettes' : ['npc_red']},   #Luca
    {'npc_sprite' : 0x2D, 'palettes' : ['npc_blue']},   #GolbezHand
    {'npc_sprite' : 0x2E, 'palettes' : ['kiss']},   #CecilRosaKiss
    {'npc_sprite' : 0x2F, 'palettes' : ['light_crystal', 'dark_crystal']},   #Crystal
    {'npc_sprite' : 0x30, 'palettes' : ['npc_red']},   #HeartBubble
    {'npc_sprite' : 0x31, 'palettes' : ['npc_red']},   #Fire
    {'npc_sprite' : 0x32, 'palettes' : ['npc_red']},   #SleepBubble
    {'npc_sprite' : 0x33, 'palettes' : ['npc_purple']},   #YangWifeWave
    {'npc_sprite' : 0x34, 'palettes' : ['npc_purple']},   #YangWifeSad
    {'npc_sprite' : 0x35, 'palettes' : ['tied_up_rosa']},   #EdwardHarp
    {'npc_sprite' : 0x36, 'palettes' : ['splash']},   #Splash
    {'npc_sprite' : 0x37, 'palettes' : ['npc_red', 'npc_purple']},   #Masamune
    {'npc_sprite' : 0x38, 'palettes' : NPC_STANDARD},   #DancerDress
    {'npc_sprite' : 0x39, 'palettes' : ['npc_red']},   #LegendarySword
    {'npc_sprite' : 0x3A, 'palettes' : ['tied_up_rosa']},   #RosaTiedUpSick
    {'npc_sprite' : 0x3B, 'palettes' : ['npc_red']},   #Rubicant
    {'npc_sprite' : 0x3C, 'palettes' : ['npc_red']},   #Sparkle
    {'npc_sprite' : 0x3D, 'palettes' : ['npc_blue']},   #ElderPraying
    {'npc_sprite' : 0x3E, 'palettes' : ['npc_blue']},   #BlackMagePraying
    {'npc_sprite' : 0x3F, 'palettes' : ['npc_blue']},   #ZemusFallen
    {'npc_sprite' : 0x40, 'palettes' : ['npc_red']},   #WhiteMagePraying
    {'npc_sprite' : 0x41, 'palettes' : ['npc_green']},   #Sylph
    {'npc_sprite' : 0x42, 'palettes' : ['npc_blue']},   #ZeromusFlame
    {'npc_sprite' : 0x43, 'palettes' : ['blond_kain']},   #KainHair
    {'npc_sprite' : 0x44, 'palettes' : ['light_crystal']},   #Lightning
    {'npc_sprite' : 0x45, 'palettes' : ['poof']},   #Teleportation
    #{'npc_sprite' : 0x46, 'palettes' : ['']},   #FatChocobo00
    #{'npc_sprite' : 0x47, 'palettes' : ['']},   #FatChocobo10
    #{'npc_sprite' : 0x48, 'palettes' : ['']},   #FatChocobo01
    #{'npc_sprite' : 0x49, 'palettes' : ['']},   #FatChocobo11
    #{'npc_sprite' : 0x4A, 'palettes' : ['']},   #Namingway00
    #{'npc_sprite' : 0x4B, 'palettes' : ['']},   #Namingway01
    #{'npc_sprite' : 0x4C, 'palettes' : ['']},   #Namingway10
    #{'npc_sprite' : 0x4D, 'palettes' : ['']},   #Namingway11
    {'npc_sprite' : 0x4E, 'palettes' : ['npc_red']},   #Valvalis
    {'npc_sprite' : 0x4F, 'palettes' : ['npc_red']},   #DancerLeg
    {'npc_sprite' : 0x50, 'palettes' : NPC_STANDARD},   #Queen
    {'npc_sprite' : 0x51, 'palettes' : ['npc_blue']},   #Zemus
    {'npc_sprite' : 0x52, 'palettes' : ['npc_red']},   #OctomammTentacles
    {'npc_sprite' : 0x53, 'palettes' : NPC_STANDARD},   #MagusSister
    {'npc_sprite' : 0x54, 'palettes' : ['npc_blue']},   #DarkElf
    {'npc_sprite' : 0x55, 'palettes' : ['bahamut']},   #Bahamut
    {'npc_sprite' : 0x56, 'palettes' : ['npc_blue']},   #Kainazzo
    {'npc_sprite' : 0x57, 'palettes' : NPC_STANDARD},   #Dress
    {'npc_sprite' : 0x58, 'palettes' : ['splash']},   #IceWall
    {'npc_sprite' : 0x59, 'palettes' : ['npc_red']},   #WhiteSpear
    {'npc_sprite' : 0x5A, 'palettes' : NPC_STANDARD},   #WomanLyingDown
    {'npc_sprite' : 0x5B, 'palettes' : ['grayscale']},   #DeathBall
    #{'npc_sprite' : 0x5C, 'palettes' : ['babil_no_bridge']},   #Mist
    {'npc_sprite' : 0x5D, 'palettes' : ['grayscale']},   #DoubleDoor
    {'npc_sprite' : 0x5E, 'palettes' : NPC_STANDARD},   #FallenSoldier
    {'npc_sprite' : 0x5F, 'palettes' : ['npc_red']},   #AntlionClawLeft
    {'npc_sprite' : 0x60, 'palettes' : ['npc_red']},   #AntlionClawRight
    {'npc_sprite' : 0x61, 'palettes' : ['npc_red']},   #Anna
    {'npc_sprite' : 0x62, 'palettes' : ['npc_blue']},   #GolbezFallen
    {'npc_sprite' : 0x63, 'palettes' : ['npc_red']},   #CrystalSword
    {'npc_sprite' : 0x64, 'palettes' : ['npc_red']},   #AnnaFallen
    #{'npc_sprite' : 0x65, 'palettes' : ['']},   #Transparent
    {'npc_sprite' : 0x66, 'palettes' : ['splash']},   #IceMagic
    {'npc_sprite' : 0x67, 'palettes' : ['npc_red']},   #FlameTop << actually harp now
    #{'npc_sprite' : 0x68, 'palettes' : ['npc_red']},   #FlameBottom << currently is ropes pic
    {'npc_sprite' : 0x69, 'palettes' : ['grayscale']},   #StonePalom
    {'npc_sprite' : 0x6A, 'palettes' : ['grayscale']},   #StonePorom
    ]

PC_PALETTES = set(['pc0', 'pc1', 'pc2', 'pc3'])
NON_PLAYER_SPRITES = [s for s in SPRITES if not PC_PALETTES.intersection(s['palettes'])]

def apply(env):
    # replace package sprite and healing pot sprites
    TEST_OVERRIDE_NAMES = [
        'package_sprite'
        ]

    if _WEIRDER:
        TEST_OVERRIDE_NAMES.extend([
            'pot_sprite_0', 
            'pot_sprite_1', 
            'pot_sprite_2', 
            'pot_sprite_3', 
            'pot_sprite_4', 
            'pot_sprite_5', 
            'pot_sprite_6', 
            'pot_sprite_7', 
            ])

    def _find_specified_sprite(name):
        if name in env.options.test_settings:
            for s in SPRITES:
                match = True
                for k in env.options.test_settings[name]:
                    if k not in s or s[k] != env.options.test_settings[name][k]:
                        match = False
                        break

                if match:
                    return s

        return None

    weird_sprite_data = []
    for test_name in TEST_OVERRIDE_NAMES:
        sprite = _find_specified_sprite(test_name)
        if sprite is None:
            sprite = env.rnd.choice(SPRITES)

        if 'npc_sprite' in sprite:
            sprite_id = sprite['npc_sprite']
            source_tile_addr = 0x1b8000
            if sprite_id < 0x11:
                source_tile_addr += (sprite_id) * 8 * 0x60
            elif sprite_id < 0x30:
                source_tile_addr += 0x3300 + (sprite_id - 0x11) * 4 * 0x60
            elif sprite_id < 0x46:
                source_tile_addr += 0x6180 + (sprite_id - 0x30) * 2 * 0x60
            else:
                source_tile_addr += 0x7200 + (sprite_id - 0x46) * 0x60

        palette_addr = PALETTE_ADDRS[env.rnd.choice(sprite['palettes'])]

        weird_sprite_data.append(source_tile_addr)
        weird_sprite_data.append(palette_addr)

    env.add_script('patch ($21f740 bus) {{ {} }}'.format(
        ' '.join([util.value_byte_string(v & 0xFFFF, 2) for v in weird_sprite_data])
        ))

    script_substitution_names = ['palom_statue', 'porom_statue']
    if _WEIRDER:
        script_substitution_names.extend(['ice', 'lightning', 'ball'])

    for name in script_substitution_names:
        sprite = _find_specified_sprite(f'{name}_sprite')
        if sprite is None:
            sprite = env.rnd.choice(NON_PLAYER_SPRITES)

        env.add_substitution(f'weird_sprite {name}', 'sprite ${:02X}'.format(sprite['npc_sprite']))

    env.add_file('scripts/weird_sprites.f4c')

