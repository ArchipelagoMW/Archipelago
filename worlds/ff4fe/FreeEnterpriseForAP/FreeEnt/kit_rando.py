from . import databases
import re


KIT_SPECS = {
    'basic' : [
        ( 'Life',       [(10, 15)] ),
        ( 'Cure2',      [(10, 15)] ),
        ( 'StarVeil',   [(2, 4)]   ),
        ( 'Tent',       [(3, 5)]   ),
        ],

    'better' : [
        ( 'Life',       [(10, 15)] ),
        ( 'Cure2',      [(10, 15)] ),
        ( 'StarVeil',   [(2, 4)]   ),
        ( 'Tent',       [(3, 5)]   ),
        ( [
            'Exit',
            'ThorRage',
            'SilkWeb',
            'Kamikaze',
            'Heal',
            'Ether1',
            'FireBomb',
            'Blizzard',
            'LitBolt',
            'Cabin',
            'Cure3'
          ], [(1,3), (0,2)]              ),
        ( [
            'Vampire',
            'SomaDrop',
            'GaiaDrum',
            'Grimoire',
            'Stardust',
            'BigBomb',
            'Boreas',
            'ZeusRage',
            'Illusion',
            'Siren',
            'HrGlass1',
            'HrGlass2',
            'HrGlass3',
            'Bacchus',
            'Coffin',
            'Elixir',
            'MoonVeil',
            'Sylph',
          ], [(1,2), (0,1)]              ),
        ],

    'loaded' : [
        ( 'Cure2',      [20]       ),
        ( 'Life',       [20]       ),
        ( 'Exit',       [5]        ),
        ( 'Ether2',     [3]        ),
        ( 'StarVeil',   [10]       ),
        ( 'HrGlass1',   [(3,5)]    ),
        ( 'Cabin',      [(3,5)]    ),
        ( [
            'Vampire',
            'SomaDrop',
            'GaiaDrum',
            'Grimoire',
            'Stardust',
            'BigBomb',
            'Boreas',
            'ZeusRage',
            'Illusion',
            'Bacchus',
            'Coffin',
            'Elixir',
            'MoonVeil',
            'Sylph',
          ], [(1,2), (1,2)] ),
        ],

    'cata' : [
        ( 'Life',       [3]        ),
        ( 'StarVeil',   [1]        ),
        ],

    'freedom' : [
        ( 'Life',       [10]       ),
        ( 'StarVeil',   [(3, 5)]   ),
        ( 'Siren',      [(1, 2)]   ),
        ( 'ThorRage',   [10]       ),
        ],

    'cid' : [
        ( 'Cure2',      [5] ),
        ( 'Bacchus',    [1] ),
        ( 'Unihorn',    [1] ),
        ( ['Dwarf', 'Ogre', 'PoisonAxe', 'RuneAxe'],  [1] ),
        ],

    'yang' : [
        ( 'CatClaw',    [2] ),
        ],

    'money' : [
        ( 'GP',         [(20000, 80000)] ),
        ],

    'grabbag' : None,  # special case handling

    'miab' : [
        ( 'HrGlass2',   [3] ),
        ( 'MuteBell',   [3] ),
        ( 'Assassin',   [1] ),
        ],

    'archer' : [
        ( ['ElvenBow', 'SamuraiBow', 'ArtemisBow'],  [1] ),
        ( ['PoisonArrow', 'MuteArrow', 'CharmArrow', 'SamuraiArrow'],  [20] ),
        ],

    'fabul' : [
        ( 'BlackSword', [1] ),
        ],

    'castlevania' : [
        ( ['Blitz', 'FlameWhip', 'DragonWhip'],  [1] ),
        ( 'Cross', [3] )
        ],

    'summon' : [
        ( ['Sylph', 'Odin', 'Levia', 'Asura', 'Baham'], [1] )
        ],

    'notdeme' : [
        ( 'Cure3',      [3] ),
        ( 'Elixir',     [2] ),
        ( 'Illusion',   [1] ),
        ],

    'meme' : [
        ( 'NinjaArmor', [1] ),
        ( 'DrainSpear', [1] ),
        ],

    'defense' : [
        ( 'DragonArmor', [1] ),
        ( 'DiamondHelm', [1] ),
        ],

    'mist' : [
        ( 'Dancing',    [10] ),
        ( 'Tiara',      [1]  ),
        ( 'Change',     [1]  )
        ],

    'mysidia' : [
        ( 'Cure2',         [70] ),
        ( 'Life',          [70] ),
        ( 'Heal',          [70] ),
        ( 'Ether1',        [70] ),
        ( 'GaeaHat',       [1]  ),
        ( 'PaladinShield', [1]  ),
        ( 'SilverRing',    [1]  ),
        ],

    'baron' : [
        ( 'Headband',    [10] ),
        ( 'Karate',      [10] ),
        ( 'ThunderClaw', [1]  ),
        ( 'ThunderRod',  [1]  ),
        ],

    'dwarf' : [
        ( 'WizardHat',   [1]  ),
        ( 'WizardArmor', [1]  ),
        ( 'Rune',        [10] ),
        ( 'Dwarf',       [1]  ),
        ( 'Elixir',      [1]  ),
        ( 'Strength',    [1]  ),
        ],

    'eblan' : [
        ( 'IceBrand',      [1] ),
        ( 'BlizzardSpear', [1] ),
        ],

    'libra' : [
        ( 'Bestiary',      [50] )
    ],

    '99' : None,  # special case handling

    'green' : [
        ( ['Glass','NinjaHelm'],   [1] ),   # b0ard
        ( ['Heroine', 'Carrot'],   [1] ),   # rivers
        ( ['Tiara', 'Grimoire'],   [1] ),   # schala
        ( ['RubyRing', 'CharmHarp'],   [1] ),   # zoe
    ]
}



def apply(env):
    kits = []
    items_dbview = databases.get_items_dbview()

    kit_names = []
    for flag_prefix in ['-kit:', '-kit2:', '-kit3:']:
        kit_name = env.options.flags.get_suffix(flag_prefix)
        if kit_name in KIT_SPECS:
            kit_names.append(kit_name)
        elif kit_name == 'random':
            kit_names.append(env.rnd.choice(list(KIT_SPECS)))

    if env.meta.get('wacky_starter_kit'):
        kit_names.append('wacky_challenge')

    for kit_name in kit_names:
        if kit_name == 'grabbag':
            kit_spec = [
                ( items_dbview.find_all(lambda it: it.tier >= 1 and it.tier <= 5), [1] * 8 )
                ]
        elif kit_name == '99':
            kit_spec = [
                ( items_dbview.find_all(lambda it: it.tier >= 1 and it.tier <= 8), [99] )
                ]
        elif kit_name == 'wacky_challenge':
            kit_spec = env.meta['wacky_starter_kit']
        else:
            kit_spec = KIT_SPECS[kit_name]

        kit = []
        for entry in kit_spec:
            item_set = entry[0]
            if type(item_set) is str:
                item_set = [item_set]

            if env.meta.get('wacky_challenge') == '3point':
                item_set = list(filter(lambda i: i != 'SomaDrop', item_set))

            qty_list = entry[1]
            items = env.rnd.sample(item_set, len(qty_list))
            for i,qty_spec in enumerate(qty_list):
                if type(qty_spec) is int:
                    qty = qty_spec
                else:
                    qty = env.rnd.randint(*qty_spec)

                item = items.pop(0)
                if qty > 0:
                    if item == 'GP':
                        qty = 1000 * round(qty / 1000)
                        kit.append( ('GP', qty) )
                    else:
                        item_const = (f'#item.{item}' if type(item) is str else item.const)
                        if kit_name == 'grabbag' and item.subtype == 'arrow':
                            qty = env.rnd.randint(1,10)
                        if env.meta.get('wacky_challenge') == 'unstackable':
                            qty = 1
                        kit.append( (items_dbview.find_one(lambda it: it.const == item_const), qty) )

        if kit:
            kits.append(kit)

    patch_lines = []

    altered_item_names = env.meta.get('altered_item_names', {})
    for i in range(4):
        if not kits:
            env.add_substitution(f'starterkit{i} message enable', '')
        else:        
            kit = kits.pop(0)

            message_lines = []
            spoiler_rows = []

            message_lines.append('Received supplies:')
            for entry in kit:
                item,qty = entry
                if (item == 'GP'):
                    message_lines.append(f'    {qty} GP')
                    patch_lines.append(f'FE {qty & 0xFF:02X} {(qty >> 8) & 0xFF:02X} {(qty >> 16) & 0xFF:02X}')
                    spoiler_rows.append( (str(qty), 'GP') )
                else:
                    item_name = altered_item_names.get(item.code, item.name)
                    message_lines.append(f'    {qty:>2} {item_name}')
                    patch_lines.append(f'{item.const} {qty:02X}')
                    spoiler_rows.append( (str(qty), databases.get_item_spoiler_name(item)) )

            env.add_substitution(f'starterkit{i} message text', '\n'.join(message_lines))

            env.spoilers.add_table(f'STARTER KIT {i+1}', spoiler_rows, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))


    env.add_script('patch($21dd00 bus) {\n' + '\n'.join(patch_lines) + '\nFF FF\n}')
