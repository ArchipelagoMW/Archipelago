import os

from . import databases
from .address import *
from .core_rando import BOSS_SLOTS

WACKY_CHALLENGES = {
    'musical'           : 'Final Fantasy IV:\nThe Musical',
    'bodyguard'         : 'The Bodyguard',
    'fistfight'         : 'Fist Fight',
    'omnidextrous'      : 'Omnidextrous',
    'biggermagnet'      : 'A Much\nBigger Magnet',
    'sixleggedrace'     : 'Six-Legged Race',
    'floorislava'       : 'The Floor Is\nMade Of Lava',
    'neatfreak'         : 'Neat Freak',
    'timeismoney'       : 'Time is Money',
    'nightmode'         : 'Night Mode',
    'mysteryjuice'      : 'Mystery Juice',
    'misspelled'        : 'Misspelled',
    'enemyunknown'      : 'Enemy Unknown',
    'kleptomania'       : 'Kleptomania',
    'darts'             : 'World Championship\nof Darts',
    'unstackable'       : 'Unstackable',
    'menarepigs'        : 'Men Are Pigs',
    'skywarriors'       : 'The Sky Warriors',
    'zombies'           : 'Zombies!!!',
    'afflicted'         : 'Afflicted',
    'batman'            : 'Holy Onomatopoeias,\nBatman!',
    'battlescars'       : 'Battle Scars',
    'imaginarynumbers'  : 'Imaginary Numbers',
    'tellahmaneuver'    : 'The Tellah\nManeuver',
    '3point'            : 'The 3-Point System',
    'friendlyfire'      : 'Friendly Fire',
    'payablegolbez'     : 'Payable Golbez',
    'gottagofast'       : 'Gotta Go Fast',
    'worthfighting'     : 'Something Worth\nFighting For',
    'saveusbigchocobo'  : 'Save Us,\nBig Chocobo!',
    'isthisrandomized'  : 'Is This Even\nRandomized?',
    'forwardisback'     : 'Forward is\nthe New Back',
}

WACKY_ROM_ADDRESS = BusAddress(0x268000)
WACKY_RAM_ADDRESS = BusAddress(0x7e1660)

def setup(env):
    wacky_challenge = None
    if env.options.test_settings.get('wacky', None):
        wacky_challenge = env.options.test_settings['wacky']
    elif env.options.flags.has('-wacky:random'):
        wacky_challenge = env.rnd.choice(list(WACKY_CHALLENGES))
    else:
        wacky_challenge = env.options.flags.get_suffix('-wacky:')

    if wacky_challenge:
        env.meta['wacky_challenge'] = wacky_challenge
        setup_func = globals().get(f'setup_{wacky_challenge}')
        if setup_func:
            setup_func(env)

def apply(env):
    wacky_challenge = env.meta.get('wacky_challenge', None)
    if wacky_challenge:
        env.add_file('scripts/wacky/wacky_common.f4c')

        # apply script of the same name, if it exists
        script_filename = f'scripts/wacky/{wacky_challenge}.f4c'
        if os.path.isfile(os.path.join(os.path.dirname(__file__), script_filename)):
            env.add_file(script_filename)

        apply_func = globals().get(f'apply_{wacky_challenge}', None)
        if apply_func:
            apply_func(env)

        env.add_substitution('intro disable', '')

        text = WACKY_CHALLENGES[wacky_challenge]
        centered_text = '\n'.join([line.center(26).upper().rstrip() for line in text.split('\n')])
        env.add_substitution('wacky challenge title', centered_text)
        env.add_substitution('wacky_rom_data_addr', f'{WACKY_ROM_ADDRESS.get_bus():06X}')
        env.add_toggle('wacky_challenge_enabled')

        env.add_script(f'''
            msfpatch {{ 
                .def Wacky__ROMData ${WACKY_ROM_ADDRESS.get_bus():06x} 
                .def Wacky__RAM     ${WACKY_RAM_ADDRESS.get_bus():06x}
                }}
        ''')

        env.spoilers.add_table('WACKY CHALLENGE', [[text.replace('\n', ' ')]], public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))


def apply_musical(env):
    env.add_substitution('wacky_fightcommandreplacement', '#$08')

def apply_bodyguard(env):
    # need substitution to mark all characters as cover-capable
    env.add_toggle('wacky_all_characters_cover')
    env.add_toggle('wacky_cover_check')

def apply_fistfight(env):
    env.add_toggle('wacky_all_characters_ambidextrous')
    # change claws to be universally equippable, all other weapons not
    for item_id in range(0x01, 0x60):
        if item_id < 0x07:
            # is claw
            eqp_byte = 0x00
        elif item_id not in [0x3E, 0x46]: # ignore Spoon and custom weapon
            eqp_byte = 0x1F
        else:
            eqp_byte = None

        if eqp_byte is not None:
            env.add_binary(UnheaderedAddress(0x79106 + (0x08 * item_id)), [eqp_byte], as_script=True)

def apply_omnidextrous(env):
    env.add_toggle('wacky_all_characters_ambidextrous')
    env.add_toggle('wacky_omnidextrous')

def apply_sixleggedrace(env):
    env.add_toggle('wacky_challenge_show_detail')

def apply_neatfreak(env):
    env.add_toggle('wacky_neatfreak')

def apply_timeismoney(env):
    env.add_file('scripts/sell_zero.f4c')

def setup_mysteryjuice(env):
    juices = '''
        Sweet Sour Bitter Salty Spicy Fruity Minty Milky Creamy Meaty Tart Savory Buttery Purple Green Brown Clear Glowing Hot Cold Lukewarm Slushy Cloudy Smooth Gooey Lumpy Juicy Crunchy Chunky Muddy Runny Chewy Steamy Frothy Inky Murky Tasty Fancy Foamy Zesty Smoky Dry Wet Bubbly Fizzy Pungent Chalky Stringy Thick Gritty Gross Neon Bold Simple Shiny
        '''.split()
    env.rnd.shuffle(juices)
    
    JUICE_ITEMS = list(range(0xB0, 0xE2)) + [0xE4, 0xE5, 0xEB, 0xED]
    juice_mapping = {}
    juice_prices = env.meta.setdefault('altered_item_prices', {})
    for item_id in JUICE_ITEMS:
        juice_mapping[item_id] = '[potion]' + juices.pop()
        juice_prices[item_id] = 1000

    env.meta.setdefault('altered_item_names', {}).update(juice_mapping)
    env.meta['wacky_juices'] = juice_mapping

def apply_mysteryjuice(env):
    ITEM_DESCRIPTION = (
        [0x00, 0xFA] + ([0xFF] * 27) + [0xFB, 0x00, 0x00] +
        [0x00, 0xFA] + ([0xFF] * 12) + ([0xC5] * 3) + ([0xFF] * 12) + [0xFB, 0x00, 0x00] +
        [0x00, 0xFA] + ([0xFF] * 27) + [0xFB, 0x00, 0x00] +
        [0x00, 0xFA] + ([0xFF] * 27) + [0xFB, 0x00, 0x00]
        )
    for item_id in env.meta['wacky_juices']:
        env.add_script(f'''
            text(item name ${item_id:02X}) {{{env.meta['wacky_juices'][item_id]}}}
        ''')
        env.meta.setdefault('item_description_overrides', {})[item_id] = ITEM_DESCRIPTION

def apply_misspelled(env):
    spells_dbview = databases.get_spells_dbview()
    remappable_spells = spells_dbview.find_all(lambda sp: (sp.code >= 0x01 and sp.code <= 0x47 and sp.code not in [0x40,0x41]))
    shuffled_spells = list(remappable_spells)
    env.rnd.shuffle(shuffled_spells)

    # get summon effects and pair them with their summon spell
    raw_summon_effects = spells_dbview.find_all(lambda sp: (sp.code >=0x4D and sp.code <= 0x5D))
    summon_effects_list = list(raw_summon_effects)
    summon_effects_linked = {}
    for effect in summon_effects_list:
        # three Asuna effects
        if (effect.code in [0x5A, 0x5B, 0x5C]):
            try:
                summon_effects_linked[0x3E].append(effect)
            except:
                summon_effects_linked[0x3E] = [effect]
        # bahamut
        elif (effect.code == 0x5D):
            summon_effects_linked[0x3F] = effect
        else:
            summon_effects_linked[effect.code - 0x1C] = effect


    pairings = zip(remappable_spells, shuffled_spells)
    remap_data = [0x00] * 0x100
    for pair in pairings:
        remap_data[pair[0].code] = pair[1].code
        env.add_script(f'''
            text(spell name {pair[1].const}) {{{pair[0].name}}}
        ''')
        # rename effects of summon spells as well
        if (pair[1].code >= 0x31 and pair[1].code <= 0x3D):
            env.add_script(f'''
                text(spell name ${pair[1].code + 0x1C:02X}) {{{pair[0].name}}}
            ''')
        elif (pair[1].code == 0x3E):
            # three Asura effects
            env.add_script(f'''
                text(spell name $5A) {{{pair[0].name}}}
                text(spell name $5B) {{{pair[0].name}}}
                text(spell name $5C) {{{pair[0].name}}}
            ''')
        elif (pair[1].code == 0x3F):
            # bahamut
            env.add_script(f'''
                text(spell name $5D) {{{pair[0].name}}}
            ''')
        
        # trade MP costs
        env.add_binary(
            BusAddress(0xF97A5 + (0x06 * pair[1].code)),
            [(pair[0].data[5] & 0x7F) | (pair[1].data[5] & 0x80)],
            as_script=True
        )

        # trade summon effect MP costs as well
        if (pair[1].code >= 0x31 and pair[1].code <= 0x3D):
            env.add_binary(
                BusAddress(0xF97A5 + (0x06 * (pair[1].code + 0x1C))),
                [(pair[0].data[5] & 0x7F) | (summon_effects_linked[pair[1].code].data[5] & 0x80)],
                as_script=True
            )
        elif (pair[1].code == 0x3E):
            # three Asuna effects
            env.add_binary(
                BusAddress(0xF97A5 + (0x06 * 0x5A)),
                [(pair[0].data[5] & 0x7F) | (summon_effects_linked[0x3E][0].data[5] & 0x80)],
                as_script=True
            )
            env.add_binary(
                BusAddress(0xF97A5 + (0x06 * 0x5B)),
                [(pair[0].data[5] & 0x7F) | (summon_effects_linked[0x3E][1].data[5] & 0x80)],
                as_script=True
            )
            env.add_binary(
            BusAddress(0xF97A5 + (0x06 * 0x5C)),
            [(pair[0].data[5] & 0x7F) | (summon_effects_linked[0x3E][2].data[5] & 0x80)],
            as_script=True
            )
        elif (pair[1].code == 0x3F):
            # bahamut
            env.add_binary(
            BusAddress(0xF97A5 + (0x06 * 0x5D)),
            [(pair[0].data[5] & 0x7F) | (summon_effects_linked[0x3F].data[5] & 0x80)],
            as_script=True
            )   

    

    env.add_binary(WACKY_ROM_ADDRESS, remap_data, as_script=True)
    env.add_toggle('wacky_misspelled')

def apply_kleptomania(env):
    VANILLA_MONSTER_LEVELS = [3,5,5,4,5,20,19,4,6,5,5,6,6,6,6,6,7,23,7,7,8,8,9,36,16,25,12,9,21,9,11,14,97,19,10,10,11,12,23,48,15,8,8,16,12,15,16,13,16,31,17,20,20,79,17,17,15,18,18,34,20,20,35,15,27,20,20,21,21,41,22,22,41,25,44,49,27,26,35,32,28,79,28,29,39,14,14,28,25,29,29,32,32,33,34,43,26,27,34,32,30,31,53,31,50,33,39,96,40,35,67,42,23,36,37,45,43,23,39,32,40,48,26,58,40,40,44,48,98,30,50,98,36,37,96,16,60,60,61,34,97,40,45,54,99,61,97,32,99,99,30,71,99,61,62,98,97,54,98,99,99,10,10,2,15,15,15,9,9,9,16,15,15,16,16,16,26,36,31,47,31,7,32,32,25,15,15,50,53,79,47,37,63,79,79,19,5,48,48,63,96,96,47,5,31,17,1,1,1,1,15,15,47,79,63,63,63,1,31,31,31,31,1,3]
    items_dbview = databases.get_items_dbview()
    available_weapons = items_dbview.find_all(lambda it: it.category == 'weapon' and it.tier >= 2 and it.tier <= 8)
    available_armor = items_dbview.find_all(lambda it: it.category == 'armor' and it.tier >= 1 and it.tier <= 8)
    available_weapons.sort(key=lambda it: it.tier)
    available_armor.sort(key=lambda it: it.tier)

    is_armor_queue = [bool((i % 5) < 2) for i in range(len(VANILLA_MONSTER_LEVELS))]
    env.rnd.shuffle(is_armor_queue)

    equipment_bytes = []
    VARIATION = 0.05
    for monster_id,monster_level in enumerate(VANILLA_MONSTER_LEVELS):
        if is_armor_queue[monster_id]:
            available_items = available_armor
            scale = 30.0
        else:
            available_items = available_weapons
            scale = 50.0
        normalized_level = max(VARIATION, min(1.0 - VARIATION, monster_level / scale))

        variated_level = normalized_level + (env.rnd.random() - 0.50) * (VARIATION * 2.0)
        index = max(0, min(len(available_items) - 1, int(len(available_items) * variated_level)))
        item = available_items[index]
        equipment_bytes.append(item.code)

    env.add_binary(WACKY_ROM_ADDRESS, equipment_bytes, as_script=True)        

def apply_darts(env):
    env.add_substitution('wacky_fightcommandreplacement', '#$16')

def apply_unstackable(env):
    env.add_toggle('wacky_unstackable')
    env.add_toggle('wacky_initialize_axtor_hook')

def apply_menarepigs(env):
    env.add_toggle('wacky_initialize_axtor_hook')
    env.add_file('scripts/wacky/status_enforcement.f4c')
    env.add_toggle('wacky_status_enforcement_uses_job')

def apply_skywarriors(env):
    env.add_toggle('wacky_initialize_axtor_hook')
    env.add_file('scripts/wacky/status_enforcement.f4c')

def apply_zombies(env):
    env.add_file('scripts/wacky/status_enforcement.f4c')
    env.add_toggle('wacky_initialize_axtor_hook')
    env.add_toggle('wacky_status_enforcement_uses_slot')
    env.add_toggle('wacky_status_enforcement_uses_battleinit_context')
    env.add_toggle('wacky_status_enforcement_uses_battle_context')
    env.add_toggle('wacky_post_battle_hook')

def apply_afflicted(env):
    env.add_file('scripts/wacky/status_enforcement.f4c')
    env.add_toggle('wacky_initialize_axtor_hook')
    env.add_toggle('wacky_status_enforcement_uses_axtor')
    env.add_toggle('wacky_status_enforcement_uses_battleinit_context')
    env.add_toggle('wacky_spell_filter_hook')
    env.add_toggle('wacky_post_battle_hook')

    STATUSES = {
        'poison'  : [0x01, 0x00, 0x00, 0x00],
        'blind'   : [0x02, 0x00, 0x00, 0x00],
        'mute'    : [0x04, 0x00, 0x00, 0x00],
        'piggy'   : [0x08, 0x00, 0x00, 0x00],
        'mini'    : [0x10, 0x00, 0x00, 0x00],
        'toad'    : [0x20, 0x00, 0x00, 0x00],
        #'stone'   : [0x40, 0x00, 0x00, 0x00],
        'calcify' : [0x00, 0x01, 0x00, 0x00],
        'calcify2': [0x00, 0x02, 0x00, 0x00],
        'berserk' : [0x00, 0x04, 0x00, 0x00],
        'charm'   : [0x00, 0x08, 0x00, 0x00],
        #'sleep'   : [0x00, 0x10, 0x00, 0x00],
        #'stun'    : [0x00, 0x20, 0x00, 0x00],
        'float'   : [0x00, 0x40, 0x00, 0x00],
        'curse'   : [0x00, 0x80, 0x00, 0x00],
        'blink1'  : [0x00, 0x00, 0x00, 0x04],
        'blink2'  : [0x00, 0x00, 0x00, 0x08],
        'armor'   : [0x00, 0x00, 0x00, 0x10],
        'wall'    : [0x00, 0x00, 0x00, 0x20],
    }

    status_bytes = []
    for status in STATUSES:
        status_bytes.extend(STATUSES[status])    
    env.add_binary(WACKY_ROM_ADDRESS, status_bytes, as_script=True)

    rng_table = [env.rnd.randint(0, len(STATUSES) - 1) for i in range(0x200)]
    env.add_binary(WACKY_ROM_ADDRESS.offset(0x100), rng_table, as_script=True)


'''
def apply_afflicted_legacyversion(env):
    env.add_toggle('wacky_initialize_axtor_hook')
    env.add_file('scripts/wacky/status_enforcement.f4c')
    env.add_toggle('wacky_status_enforcement_uses_axtor')

    STATUSES = {
        'poison'  : [0x01, 0x00, 0x00, 0x00],
        'blind'   : [0x02, 0x00, 0x00, 0x00],
        'mute'    : [0x04, 0x00, 0x00, 0x00],
        'piggy'   : [0x08, 0x00, 0x00, 0x00],
        'mini'    : [0x10, 0x00, 0x00, 0x00],
        'toad'    : [0x20, 0x00, 0x00, 0x00],
        'calcify' : [0x00, 0x01, 0x00, 0x00],
        'calcify2': [0x00, 0x02, 0x00, 0x00],
        'berserk' : [0x00, 0x04, 0x00, 0x00],
        #'sleep'   : [0x00, 0x10, 0x00, 0x00],
        'float'   : [0x00, 0x40, 0x00, 0x00],
        'curse'   : [0x00, 0x80, 0x00, 0x00],
        'blink'   : [0x00, 0x00, 0x00, 0x08],
        'wall'    : [0x00, 0x00, 0x00, 0x20],
    }

    status_names = list(STATUSES)
    status_bytes = []
    for axtor_id in range(0x20):
        status = env.rnd.choice(status_names)
        status_bytes.extend(STATUSES[status])
    
    env.add_binary(WACKY_ROM_ADDRESS, status_bytes, as_script=True)
'''

def apply_battlescars(env):
    env.add_toggle('wacky_initialize_axtor_hook')
    env.add_toggle('wacky_post_battle_hook')

def apply_tellahmaneuver(env):
    env.add_toggle('wacky_omit_mp')

    # precalculate MP costs times 10
    spells_dbview = databases.get_spells_dbview()
    data = [0x00] * 0x400
    for spell_id in range(0x48):
        mp_cost = 10 * spells_dbview.find_one(lambda sp: sp.code == spell_id).mp
        data[spell_id] = mp_cost & 0xFF
        data[spell_id + 0x100] = (mp_cost >> 8) & 0xFF

    # also precalculate number * 10 in general
    for v in range(0x100):
        data[v + 0x200] = ((v * 10) & 0xFF)
        data[v + 0x300] = ((v * 10) >> 8) & 0xFF
    
    env.add_binary(WACKY_ROM_ADDRESS, data, as_script=True)

def apply_3point(env):
    env.add_toggle('wacky_initialize_axtor_hook')

    # change all MP costs to 1
    spells_dbview = databases.get_spells_dbview()
    for spell_id in range(0x48):
        spell = spells_dbview.find_one(lambda sp: sp.code == spell_id)
        if spell.mp > 0:
            env.add_binary(
                BusAddress(0xF97A5 + (0x06 * spell_id)),
                [(spell.data[5] & 0x80) | 0x01],
                as_script=True
            )
    for spell_id in range(0x4D, 0x5E):
        spell = spells_dbview.find_one(lambda sp: sp.code == spell_id)
        env.add_binary(
            BusAddress(0xF97A5 + (0x06 * spell_id)),
            [(spell.data[5] & 0x80) | 0x01],
            as_script=True
        )

def apply_friendlyfire(env):
    env.add_toggle('wacky_spell_filter_hook')
    env.add_file('scripts/wacky/spell_filter_hook.f4c')

def apply_payablegolbez(env):
    BOSS_SLOT_HPS = {
        'antlion_slot' : 1000,
        'asura_slot' : 23000,
        'bahamut_slot' : 37000,
        'baigan_slot' : 4200,
        'calbrena_slot' : 8524,
        'cpu_slot' : 24000,
        'darkelf_slot' : 5000,
        'darkimp_slot' : 597,
        'dlunar_slot' : 42000,
        'dmist_slot' : 465,
        'elements_slot' : 65000,
        'evilwall_slot' : 19000,
        'fabulgauntlet_slot' : 1880,
        'golbez_slot' : 3002,
        'guard_slot' : 400,
        'kainazzo_slot' : 4000,
        'karate_slot' : 4000,
        'kingqueen_slot' : 6000,
        'leviatan_slot' : 35000,
        'lugae_slot' : 18943,
        'magus_slot' : 9000,
        'milon_slot' : 2780,
        'milonz_slot' : 3000,
        'mirrorcecil_slot' : 1000,
        'mombomb_slot' : 1250,
        'octomamm_slot' : 2350,
        'odin_slot' : 20500,
        'officer_slot' : 302,
        'ogopogo_slot' : 37000,
        'paledim_slot' : 27300,
        'plague_slot' : 28000,
        'rubicant_slot' : 25200,
        'valvalis_slot' : 6000,
        'wyvern_slot' : 25000,
    }
    bribe_values = []
    for slot in BOSS_SLOTS:
        bribe = BOSS_SLOT_HPS[slot] * 5
        bribe_values.extend([
            ((bribe >> (i * 8)) & 0xFF) for i in range(4)
        ])

    env.add_binary(WACKY_ROM_ADDRESS, bribe_values, as_script=True)
    env.add_toggle('allow_boss_bypass')
    env.add_toggle('wacky_boss_skip_hook')

def apply_gottagofast(env):
    env.add_toggle('wacky_sprint')

def apply_worthfighting(env):
    env.add_toggle('wacky_post_treasure_hook')
    env.add_toggle('wacky_post_battle_hook')

def setup_saveusbigchocobo(env):
    env.meta['wacky_starter_kit'] = [( 'Carrot', [5] )]
