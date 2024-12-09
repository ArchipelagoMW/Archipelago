import math

TRAPDOORS = ['DoubleDoor{}'.format(n) for n in range(2,17)]
BEHEMOTHS = ['behemoth1','behemoth2','behemoth3']

def apply(env):
    doors_to_disable = []
    behemoths_to_disable = []

    env.add_file('scripts/encounter_reduction.f4c')

    if not env.options.flags.has('encounter_keep_doors'):
        if env.options.flags.has('encounter_reduction'):
            # only disable half the trapdoors
            doors_to_disable = env.rnd.sample(TRAPDOORS, math.ceil(len(TRAPDOORS) * 0.6))
        elif env.options.flags.has('encounter_off'):
            # disable all trapdoors
            doors_to_disable = TRAPDOORS

        for d in doors_to_disable:
            env.add_substitution(f'trapdoor {d}', 'set #Temp')
    else:
        for d in TRAPDOORS:
            env.add_substitution(f'trapdoor {d}', 'clear #Temp')

    if not env.options.flags.has('encounter_keep_behemoths'):
        if env.options.flags.has('encounter_reduction'):
            # each behemoth has a 50/50 chance of being disabled
            behemoths_to_disable = [i for i in BEHEMOTHS if env.rnd.random() < 0.5]
        elif env.options.flags.has('encounter_off'):
            # disable all behemoths
            behemoths_to_disable = BEHEMOTHS

        if behemoths_to_disable:
            env.add_file('scripts/bahamut_no_behemoths.f4c')
            for b in BEHEMOTHS:
                if b not in behemoths_to_disable:
                    env.add_substitution(f'{b} disable', '')
    else:
        env.add_substitution('behemoth use toggle', '')

    if env.options.flags.has('encounter_toggle'):
        env.add_file('scripts/encounter_toggle.f4c')
    
    if env.options.flags.has('encounter_dangerous') and env.options.flags.has_any('encounter_toggle', 'encounter_off'):
        env.add_file('scripts/encounter_dangerous.f4c')
    else:
        env.add_substitution('encounter dangerous on', '')

    if not env.options.flags.has_any('encounter_toggle', 'encounter_off'):
        env.add_substitution('encounter default off', '')

    if not env.options.flags.has('encounter_reduction'):
        env.add_substitution('encounter reduction', '')

    if env.options.flags.has('encounter_cant_run'):
        env.add_file('scripts/cant_run.f4c')
