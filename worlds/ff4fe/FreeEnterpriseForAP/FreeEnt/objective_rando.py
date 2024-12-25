from .address import *
from .objective_data import *
from .errors import *
from . import util
from .spoilers import SpoilerRow

MODES = {
    'Omode:classicforge'  : ['quest_forge'],
    'Omode:classicgiant'  : ['quest_giant'],
    'Omode:fiends'        : ['boss_milon', 'boss_milonz', 'boss_kainazzo', 'boss_valvalis', 'boss_rubicant', 'boss_elements'],
    'Omode:dkmatter'      : ['internal_dkmatter'],
}

OBJECTIVE_SLUGS_TO_IDS = {}
for objective_id in OBJECTIVES:
    OBJECTIVE_SLUGS_TO_IDS[OBJECTIVES[objective_id]['slug']] = objective_id

CHAR_OBJECTIVE_PREFIX = "char_"
BOSS_OBJECTIVE_PREFIX = "boss_"
INTERNAL_OBJECTIVE_PREFIX = "internal_"

CUSTOM_OBJECTIVE_COUNT = 16

MAX_OBJECTIVE_COUNT = 0x20

RANDOM_CATEGORY_WEIGHTS = {
    'char' : 20,
    'boss' : 20,
    'quest' : 60,
    }

TOUGH_QUEST_OBJECTIVES_EXCLUDED = [
    'quest_mistcave',
    'quest_waterfall',
    'quest_antlionnest',
    'quest_hobs',
    'quest_fabul',
    'quest_ordeals',
    'quest_baroninn',
    'quest_pass',
    'quest_dwarfcastle',
    'quest_lowerbabil',
    'quest_unlocksewer',
    'quest_music',
    'quest_toroiatreasury',
    'quest_magma',
    'quest_unlocksealedcave',
    'quest_bigwhale',
    'quest_wakeyang',
]

TOUGH_QUEST_OBJECTIVES_WEIGHTED = [
    'quest_monsterking',
    'quest_monsterqueen',
    'quest_cavebahamut',
    'quest_murasamealtar',
    'quest_crystalaltar',
    'quest_whitealtar',
    'quest_ribbonaltar',
    'quest_masamunealtar'
]


def _split_lines(text, line_length=24):
    pieces = text.split()
    lines = []
    while pieces:
        if len(pieces[0]) > line_length:
            lines.append(pieces[0][:line_length])
            pieces[0] = pieces[0][line_length:]
        elif not lines or len(lines[-1] + ' ' + pieces[0]) > line_length:
            lines.append(pieces[0])
            pieces.pop(0)
        else:
            lines[-1] += ' ' + pieces[0]
            pieces.pop(0)
    return lines


def setup(env):
    env.meta['has_objectives'] = False
    env.meta['zeromus_required'] = True
    env.meta.setdefault('objectives_from_flags', [])
    env.meta.setdefault('objective_required_characters', set())
    env.meta.setdefault('objective_required_bosses', set())
    env.meta.setdefault('objective_required_key_items', set())
    env.meta.setdefault('required_treasures', {})

    if not env.options.flags.has('objective_none'):
        env.meta['has_objectives'] = True
        env.meta['zeromus_required'] = env.options.flags.has("objective_zeromus")

        specified_objectives = dict()
        for i in range(CUSTOM_OBJECTIVE_COUNT):
            slug = env.options.flags.get_suffix(f"O{i+1}:")
            env.meta['objectives_from_flags'].append(slug)
            specified_objectives[slug] = True            

        for mode in MODES:
            if env.options.flags.has(mode):
                for slug in MODES[mode]:
                    specified_objectives[slug] = True

        for objective_id in OBJECTIVES:
            objective = OBJECTIVES[objective_id]
            slug = objective['slug']
            if specified_objectives.get(slug, False):
                if slug.startswith(CHAR_OBJECTIVE_PREFIX):
                    env.meta['objective_required_characters'].add(slug[len(CHAR_OBJECTIVE_PREFIX):])
                elif slug.startswith(BOSS_OBJECTIVE_PREFIX):
                    env.meta['objective_required_bosses'].add(slug[len(BOSS_OBJECTIVE_PREFIX):])
                elif slug == 'quest_tradepink':
                    env.meta['objective_required_key_items'].add('#item.Pink')

        if env.options.flags.has('objective_mode_dkmatter'):
            env.meta['required_treasures'].setdefault('#item.DkMatter', 0)
            env.meta['required_treasures']['#item.DkMatter'] += 45


def apply(env):
    if not env.meta['has_objectives']:
        return

    env.add_substitution('intro disable', '')
    if not env.meta['zeromus_required']:
        env.add_file('scripts/zeromus_trigger_reassign.f4c')

    objective_ids = []

    # apply objectives from modes
    for objective_flag in MODES:
        if env.options.flags.has(objective_flag):
            objective_ids.extend([OBJECTIVE_SLUGS_TO_IDS[q] for q in MODES[objective_flag]])

    # custom objectives from flags
    for objective_id in OBJECTIVES:
        if OBJECTIVES[objective_id]['slug'] in env.meta['objectives_from_flags']:
            objective_ids.append(objective_id)

    # remove duplicates
    objective_ids = sorted(list(set(objective_ids)), key = lambda oid: objective_ids.index(oid))

    # generate random objectives
    random_objective_count = 0
    for f in env.options.flags.get_list(r'^Orandom:\d'):
        random_objective_count = int(f[len('Orandom:'):])

    random_objective_allowed_types = set()
    tough_quests_only = False
    for f in env.options.flags.get_list(r'^Orandom:[^\d]'):
        allowed_type = f[len('Orandom:'):]
        if (allowed_type == 'tough_quest'):
            allowed_type = 'quest'
            tough_quests_only = True
        random_objective_allowed_types.add(allowed_type)

    random_objective_pool = {}
    for objective_id in OBJECTIVES:
        obj = OBJECTIVES[objective_id]
        category = obj['slug'].split('_')[0]

        if (not random_objective_allowed_types) or (category in random_objective_allowed_types):
            if (category != 'quest') or (not tough_quests_only) or (obj['slug'] not in TOUGH_QUEST_OBJECTIVES_EXCLUDED):
                if obj['slug'] in TOUGH_QUEST_OBJECTIVES_WEIGHTED and env.rnd.random() < 0.40:
                    continue
                random_objective_pool.setdefault(category, []).append(objective_id)

    random_category_weights = RANDOM_CATEGORY_WEIGHTS
    if random_objective_allowed_types:
        random_category_weights = { k : RANDOM_CATEGORY_WEIGHTS[k] for k in RANDOM_CATEGORY_WEIGHTS if k in random_objective_allowed_types }
    random_category_distribution = util.Distribution(**random_category_weights)

    for i in range(random_objective_count):
        while True:
            category = random_category_distribution.choose(env.rnd)
            q = env.rnd.choice(random_objective_pool[category])
            if q in objective_ids:
                continue
            
            slug = OBJECTIVES[q]['slug']
            if slug.startswith(CHAR_OBJECTIVE_PREFIX):
                char = slug[len(CHAR_OBJECTIVE_PREFIX):]
                if char not in env.meta['available_nonstarting_characters']:
                    continue
            elif slug.startswith(BOSS_OBJECTIVE_PREFIX):
                boss = slug[len(BOSS_OBJECTIVE_PREFIX):]
                if boss not in env.meta['available_bosses']:
                    continue
            elif slug == 'quest_tradepink':
                if '#item.Pink' not in env.meta['available_key_items']:
                    continue
            elif slug == 'quest_pass':
                if env.options.flags.has('pass_none'):
                    continue
            elif slug.startswith(INTERNAL_OBJECTIVE_PREFIX):
                # don't allow internal objectives to be selected as random ones
                continue

            break

        objective_ids.append(q)

    if env.options.test_settings.get('objectives'):
        objective_ids = [OBJECTIVE_SLUGS_TO_IDS[s.strip()] for s in env.options.test_settings.get('objectives').split(',')]

    if len(objective_ids) > MAX_OBJECTIVE_COUNT:
        reduced_objective_ids = env.rnd.sample(objective_ids, MAX_OBJECTIVE_COUNT)
        objective_ids = sorted(reduced_objective_ids, key = objective_ids.index)

    # write list of objective IDs and thresholds
    total_objective_count = len(objective_ids)
    env.add_substitution('objective count', f'{total_objective_count:02X}')
    objective_ids.extend([0x00] * (MAX_OBJECTIVE_COUNT - len(objective_ids)))
    env.add_substitution('objective ids', ' '.join([f'{b:02X}' for b in objective_ids]))
    env.add_substitution('objective thresholds', ' '.join([('00' if b == 0xFF else '01') for b in objective_ids]))

    # handle changes for partial objectives
    required_objective_count = env.options.flags.get_suffix('Oreq:')
    if required_objective_count == 'all' or required_objective_count is None:
        required_objective_count = total_objective_count
    else:
        required_objective_count = int(required_objective_count)
    env.add_substitution('objective required count', f'{required_objective_count:02X}')

    if required_objective_count > total_objective_count:
        raise BuildError(f"Flags stipulate that {required_objective_count} objectives must be completed, but there are only {total_objective_count} objectives specified.")
    elif required_objective_count < total_objective_count:
        required_objective_count_text = f'{required_objective_count} objective{"s" if required_objective_count > 1 else ""}'
        env.add_substitution('completion objective count text', required_objective_count_text)
    else:
        required_objective_count_text = 'all objectives'
        env.add_substitution('completion objective count text', 'All objectives')

    if env.options.hide_flags:
        required_objective_count_text = 'objectives'

    env.add_substitution('required objective count text', required_objective_count_text)

    # write objective descriptions and compile spoilers
    spoilers = []
    pregame_text_lines = []
    for i,objective_id in enumerate(objective_ids):
        if objective_id == 0x00:
            continue

        text = OBJECTIVES[objective_id]['desc']
        env.meta.setdefault('objective_descriptions', []).append(text)
        spoilers.append( SpoilerRow(f"{i+1}. {text}") )
        lines = _split_lines(text)
        if len(lines) > 2:
            raise ValueError(f"Objective text cannot fit on 2 lines; text is {text}")
        while len(lines) < 2:
            lines.append('')

        for j,line in enumerate(lines):
            addr = 0x23C000 + (i * 0x40) + (j * 0x20)
            env.add_binary(BusAddress(addr), [len(line)], as_script=True)
            encoded_line = line.replace('(', '[$cc]').replace(')', '[$cd]')
            env.add_script(f'text(${addr + 1:06X} bus) {{{encoded_line}}}')

            if line.strip():
                prefix = f"{i+1}." + (" " if i < 9 else "")
                if j > 0:
                    prefix = " " * len(prefix)
                pregame_text_lines.append(prefix + line)
        pregame_text_lines.append("")

    completion_reward_text = 'the Crystal' if env.options.flags.has('objective_zeromus') else 'the game'
    pregame_text_lines.append(" Complete " + required_objective_count_text)
    pregame_text_lines.append(" to win " + completion_reward_text)

    env.spoilers.add_table("OBJECTIVES", spoilers, public=env.options.flags.has_any('-spoil:all', '-spoil:misc'))
    env.add_pregame_text("OBJECTIVES", "\n".join(pregame_text_lines), center=False)

    # apply additional objective needs
    if OBJECTIVE_SLUGS_TO_IDS['internal_dkmatter'] in objective_ids:
        env.add_file('scripts/dark_matter_hunt.f4c')
        


if __name__ == '__main__':
    print("Checking line lengths")
    for q in OBJECTIVES:
        desc = OBJECTIVES[q]['desc']
        lines = _split_lines(desc)
        if len(lines) > 2:
            print(f"Too long: {desc}")
