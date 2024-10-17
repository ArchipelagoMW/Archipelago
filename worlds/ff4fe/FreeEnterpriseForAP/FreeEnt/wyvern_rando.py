from . import databases

POSSIBLE_COMMANDS = {
    '#spell.Hold' : 'random character',
    '#spell.Mute' : 'all characters',
    '#spell.Charm' : 'front row / back row',
    '#spell.Blink' : 'self',
    '#spell.Armor' : 'self',
    '#spell.Shell' : 'self',
    '#spell.Slow' : 'all characters',
    '#spell.Fast' : 'self',
    '#spell.Bersk' : 'front row / back row',
    '#spell.White' : 'all characters',
    '#spell.Size' : 'all characters',
    '#spell.Float' : 'self',
    '#spell.Toad' : 'all characters',
    '#spell.Piggy' : 'all characters',
    '#spell.Venom' : 'all characters',
    '#spell.Fire1' : 'all characters',
    '#spell.Fire2' : 'all characters',
    '#spell.Fire3' : 'all characters',
    '#spell.Ice1' : 'all characters',
    '#spell.Ice2' : 'all characters',
    '#spell.Ice3' : 'all characters',
    '#spell.Lit1' : 'all characters',
    '#spell.Lit2' : 'all characters',
    '#spell.Lit3' : 'all characters',
    '#spell.Virus' : 'all characters',
    '#spell.Weak' : 'all characters',
    '#spell.Sleep' : 'front row / back row',
    '#spell.Stone' : 'random character',
    '#spell.Fatal' : 'random character',
    '#spell.Stop' : 'random character',
    '#spell.Drain' : 'all characters',
    '#spell.Psych' : 'all characters',
    '#spell.Enemy_Gaze' : 'random character',
    '#spell.Enemy_Bluster' : 'random character',
    '#spell.Enemy_Slap' : 'all characters',
    '#spell.Enemy_Powder' : 'all characters',
    '#spell.Enemy_Glance' : 'all characters',
    '#spell.Enemy_Charm' : 'all characters',
    '#spell.Enemy_Tongue' : 'front row / back row',
    '#spell.Enemy_Curse' : 'all characters',
    '#spell.Enemy_Ray' : 'all characters',
    '#spell.Enemy_Count' : 'all characters',
    '#spell.Enemy_Beak' : 'random character',
    '#spell.Enemy_Petrify' : 'front row / back row',
    '#spell.Enemy_Blast' : 'front row / back row',
    '#spell.Enemy_Hug' : 'front row / back row',
    '#spell.Enemy_Breath' : 'all characters',
    '#spell.Enemy_Whisper' : 'all characters',
    '#spell.Enemy_Entangle' : 'front row / back row',
    '#spell.Enemy_WeakEnemy' : 'all characters',
    '#spell.Enemy_ColdMist' : 'all characters',
    '#spell.Enemy_HoldGas' : 'front row / back row',
    '#spell.Enemy_Gas' : 'front row / back row',
    '#spell.Enemy_Poison' : 'all characters',
    '#spell.Enemy_Maser' : 'all characters',
    '#spell.Enemy_Demolish' : 'random character',
    '#spell.Enemy_Disrupt2' : 'random character',
    '#spell.Enemy_Storm' : 'all characters',
    '#spell.Enemy_Magnet' : 'random character',
    '#spell.Enemy_Vampire' : 'all characters',
    '#spell.Enemy_Digest' : 'all characters',
    '#spell.Enemy_Pollen' : 'all characters',
    '#spell.Enemy_Crush' : 'random character',
    '#spell.Enemy_Search' : 'all characters',
    '#spell.Enemy_Fission' : 'front row / back row',
    '#spell.Enemy_Retreat' : 'self',
    '#spell.Enemy_Beam' : 'all characters',
    '#spell.Enemy_Globe199' : 'random character',
    '#spell.Enemy_Fire' : 'all characters',
    '#spell.Enemy_Blaze' : 'all characters',
    '#spell.Enemy_Blitz' : 'all characters',
    '#spell.Enemy_Thunder' : 'all characters',
    '#spell.Enemy_DBreath' : 'all characters',
    '#spell.Enemy_BigWave' : 'all characters',
    '#spell.Enemy_Blizzard' : 'all characters',
    '#spell.Enemy_Wave' : 'all characters',
    '#spell.Enemy_Tornado' : 'all characters',
    '#spell.Enemy_Laser' : 'all characters',
    '#spell.Enemy_Explode2' : 'random character',
    '#spell.Enemy_Emission' : 'all characters',
    '#spell.Enemy_HeatRay' : 'all characters',
    '#spell.Enemy_Glare' : 'all characters',
    '#spell.Enemy_Needle' : 'all characters',
    '#spell.Enemy_Counter' : 'all characters',
    }

UNSAFE_COMMANDS = {
    '#spell.Quake' : 'all characters',
    '#spell.Meteo' : 'all characters',
    '#spell.Enemy_Odin' : 'all characters',
    '#spell.Enemy_BigBang' : 'all characters',
    }

def apply(env):
    if env.options.flags.has('wyvern_no_meganuke'):
        env.add_file('scripts/wyvern_nomeganuke.f4c')

    elif env.options.flags.has('wyvern_random_meganuke'):
        commands = dict(POSSIBLE_COMMANDS)
        if env.options.flags.has('bosses_unsafe'):
            commands.update(UNSAFE_COMMANDS)

        cmd = env.rnd.choice(list(commands))
        target = env.rnd.choice(commands[cmd].split(' / '))
        if target == 'random character':
            script = f'use {cmd}'
        else:
            script = f'target {target} use {cmd}'

        env.add_substitution('wyvern meganuke replacement', script)
        env.add_file('scripts/wyvern_replacemeganuke.f4c')

        env.spoilers.add_table(
            "MISC", 
            [["MegaNuke replacement", databases.get_spell_spoiler_name(cmd)]],
            public = env.options.flags.has_any('-spoil:all', '-spoil:misc')
            )
