# scripts contain most of the cutscene customization, we just
# need to specify the sprites in here because they have to
# sit in a different table.

# note that the individual spell scripts need to properly load
# the name of the relevant spell, as well as do the "give spell"
# command.

from . import databases

HOBS_SPELLS = {
    'Imp'   : ['HoodedMonster'],
    'Bomb'  : ['Fire', 'Bomb'],
    'Cocka' : ['Splash'],
    'Mage'  : ['OldMan', 'FlameBottom', 'FlameBottom', 'FlameBottom'],  # use Rosa ropes as "rings"

    'Shiva' : ['Sylph', 'IceWall', 'IceWall', 'IceWall'],
    'Indra' : ['OldMan', 'Lightning', 'Lightning', 'Lightning'],
    'Jinn'  : ['Dwarf', 'Fire', 'Fire', 'Fire'],
    'Titan' : ['Monk'],
    'Mist'  : ['IceWall'],

    'Sylph' : ['Sylph', 'Sylph'],
    'Odin'  : ['King'],
    'Asura' : ['Woman', 'OldWoman', 'Queen'],
    }

DWARF_CASTLE_SUMMONS_POOL = ['Mist', 'Jinn', 'Indra', 'Shiva', 'Titan', 'Levia', 'Asura', 'Odin', 'Baham', 'Sylph', 'Imp', 'Mage', 'Cocka', 'Bomb']


def apply(env):
    if not env.options.flags.has('vanilla_hobs'):
        apply_hobs_rando(env)

    if not env.options.flags.has('vanilla_dwarf_summons'):
        apply_dwarf_castle_summons_rando(env)


def apply_dwarf_castle_summons_rando(env):
    dwarf_summons = env.rnd.sample(DWARF_CASTLE_SUMMONS_POOL, 5)

    dwarf_summons_script_lines = (
        [f'give spell #RydiaCall #{spell}' for spell in dwarf_summons]
        + [f'[#B #Text_LoadSpellName {index} #spell.{spell}]' for index,spell in enumerate(dwarf_summons)]
        + ['message $11d']
        )
    
    env.add_substitution('dwarf summon rando', '\n'.join(dwarf_summons_script_lines))

    env.spoilers.add_table("MISC", 
        [["Dwarf castle summons", ', '.join([databases.get_spell_spoiler_name(f"#spell.{spell}") for spell in dwarf_summons])]], 
        public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))


def apply_hobs_rando(env):
    spell_name = env.rnd.choice(list(HOBS_SPELLS))
    if 'hobs' in env.options.test_settings:
        for n in HOBS_SPELLS:
            if n.lower() == env.options.test_settings['hobs'].lower():
                spell_name = n
                break

    env.add_substitution('hobs intro', '''
        pause 4
        sound #CallMagic
        batch 10 {
            screen flash
        }
        pause 4
        player invisible
        player visible
        player invisible
        player visible
        player invisible
        player visible
        player invisible
        player visible
        player invisible
        player visible
        player invisible
        toggle tint $E3
        pause 3
        ''')

    env.add_substitution('hobs outro', f'''
        toggle tint $00
        pause 4
        player visible
        player invisible
        player visible
        player invisible
        player visible
        player invisible
        player visible
        player invisible
        player visible
        player invisible
        player visible

        pause 4
        [#B #Text_LoadSpellName 0 #spell.{spell_name}]
        music #CharacterJoined
        map message 5
        give spell #RydiaCall #spell.{spell_name}
        ''')

    for i,sprite in enumerate(HOBS_SPELLS[spell_name]):
        env.add_substitution(f'hobs sprite {i}', f'#sprite.{sprite}')

    env.add_file(f'scripts/hobs_spells/hobs_{spell_name.lower()}.f4c')

    env.spoilers.add_table("MISC", [["Hobs spell", databases.get_spell_spoiler_name(f"#spell.{spell_name}")]], public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))
