from . import databases

STARTING_WHITE = [
    '#Hold', '#Mute', '#Charm', '#Blink',
    '#Fast', '#Peep', '#Cure1', '#Cure2',
    '#Heal', '#Life1', '#Size', '#Exit',
    '#Sight', '#Float'
    ]

STARTING_WHITE_JAPANESE = [
    '#Armor', '#Shell', '#Dspel'
    ]

STARTING_BLACK = [
    '#Toad', '#Piggy', '#Warp', '#Venom',
    '#Fire1', '#Fire2', '#Ice1', '#Ice2',
    '#Lit1', '#Lit2', '#Sleep', '#Stone',
    '#Drain', '#Psych'
    ]

JAPANESE_EXCLUSIVE_SPELLS = [
    '#spell.Armor', '#spell.Shell', '#spell.Dspel'
    ]

ALL_SPELLS_BY_LEVEL = {
    '#spell.Ice1'  : 1,
    '#spell.Cure1' : 0,
    '#spell.Sight' : 0,
    '#spell.Lit1'  : 1,
    '#spell.Peep'  : 0,
    '#spell.Fire1' : 1,
    '#spell.Hold'  : 0,
    '#spell.Sleep' : 1,
    '#spell.Slow'  : 0,
    '#spell.Venom' : 1,
    '#spell.Ice2'  : 1,
    '#spell.Life1' : 0,
    '#spell.Piggy' : 1,
    '#spell.Armor' : 0,
    '#spell.Fire2' : 1,
    '#spell.Cure2' : 0,
    '#spell.Lit2'  : 1,
    '#spell.Stop'  : 1,
    '#spell.Mute'  : 0,
    '#spell.Bersk' : 0,
    '#spell.Exit'  : 0,
    '#spell.Virus' : 1,
    '#spell.Heal'  : 0,
    '#spell.Toad'  : 1,
    '#spell.Blink' : 0,
    '#spell.Quake' : 1,
    '#spell.Charm' : 0,
    '#spell.Drain' : 1,
    '#spell.Shell' : 0,
    '#spell.Warp'  : 1,
    '#spell.Dspel' : 0,
    '#spell.Size'  : 0,
    '#spell.Ice3'  : 1,
    '#spell.Cure3' : 0,
    '#spell.Fire3' : 1,
    '#spell.Lit3'  : 1,
    '#spell.Stone' : 1,
    '#spell.Fast'  : 0,
    '#spell.Float' : 0,
    '#spell.Cure4' : 0,
    '#spell.Psych' : 1,
    '#spell.Wall'  : 0,
    '#spell.Life2' : 0,
    '#spell.Fatal' : 1,
    '#spell.Weak'  : 1,
    '#spell.White' : 0,
    '#spell.Meteo' : 1,
    '#spell.Nuke'  : 1,
    }

ALL_SPELLS_BY_GOODNESS = {
    '#spell.Sight' : 0,
    '#spell.Peep'  : 0,
    '#spell.Cure1' : 0,
    '#spell.Venom' : 1,
    '#spell.Toad'  : 1,
    '#spell.Piggy' : 1,
    '#spell.Ice1'  : 1,
    '#spell.Lit1'  : 1,
    '#spell.Fire1' : 1,
    '#spell.Sleep' : 1,
    '#spell.Charm' : 0,
    '#spell.Drain' : 1,
    '#spell.Shell' : 0,
    '#spell.Psych' : 1,
    '#spell.Mute'  : 0,
    '#spell.Size'  : 0,
    '#spell.Armor' : 0,
    '#spell.Dspel' : 0,

    '#spell.Slow'  : 0,
    '#spell.Cure2' : 0,
    '#spell.Float' : 0,
    '#spell.Hold'  : 0,
    '#spell.Blink' : 0,
    '#spell.Ice2'  : 1,
    '#spell.Life1' : 0,
    '#spell.Fire2' : 1,
    '#spell.Lit2'  : 1,
    '#spell.Stop'  : 1,
    '#spell.Exit'  : 0,
    '#spell.Heal'  : 0,
    '#spell.Warp'  : 1,
    '#spell.Cure3' : 0,
    '#spell.Stone' : 1,
    '#spell.Fast'  : 0,
    '#spell.Wall'  : 0,

    '#spell.Virus' : 1,
    '#spell.Fire3' : 1,
    '#spell.Ice3'  : 1,
    '#spell.Lit3'  : 1,
    '#spell.Quake' : 1,
    '#spell.Bersk' : 0,
    '#spell.Cure4' : 0,
    '#spell.Life2' : 0,
    '#spell.Fatal' : 1,
    '#spell.Weak'  : 1,
    '#spell.Meteo' : 1,
    '#spell.White' : 0,
    '#spell.Nuke'  : 1,
    }


def apply(env):
    if not env.options.flags.has('vanilla_fusoya'):
        ranked_spells = []
        for i,spell in enumerate(ALL_SPELLS_BY_GOODNESS):
            if spell in JAPANESE_EXCLUSIVE_SPELLS and not env.options.flags.has('japanese_spells'):
                continue
            position = float(i) / len(ALL_SPELLS_BY_GOODNESS)
            #position += (env.rnd.random() - 0.5) * 0.5
            position += (env.rnd.random() - 0.5)
            #position = max(0.0, min(1.0, position))
            ranked_spells.append( (position, spell) )

        ranked_spells.sort()
        initial_spells = [p[1] for p in ranked_spells[:6]]
        learned_spells = [p[1] for p in ranked_spells[6:]]

        white = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 0]
        black = [s for s in initial_spells if ALL_SPELLS_BY_GOODNESS[s] == 1]

        env.add_substitution('fusoya initial spells', '')
        env.add_substitution('fusoya challenge spells', '\n'.join(learned_spells))

        env.add_scripts(
            'spellset(#FusoyaWhite) {{ initial {{ {} }} }}'.format(' '.join(white)),
            'spellset(#FusoyaBlack) {{ initial {{ {} }} }}'.format(' '.join(black))
            )

        spoilers = []
        spoilers.append( ("Initial spells", ', '.join([databases.get_spell_spoiler_name(s) for s in initial_spells])) )
        for i in range(0, len(learned_spells), 3):
            boss_number = (i // 3) + 1
            level_spells = learned_spells[i:i+3]
            spoilers.append( (f"Boss {boss_number}", ', '.join([databases.get_spell_spoiler_name(s) for s in level_spells])) )
        env.spoilers.add_table("FUSOYA SPELLS", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'), ditto_depth=1)
