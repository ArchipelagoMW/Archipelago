import argparse
import logging
import random
import urllib.request
import urllib.parse

from EntranceRandomizer import parse_arguments
from Main import main as ERmain

def parse_yaml(txt):
    ret = {}
    indents = {len(txt) - len(txt.lstrip(' ')): ret}
    for line in txt.splitlines():
        if not line:
            continue
        name, val = line.split(':', 1)
        val = val.strip()
        spaces = len(name) - len(name.lstrip(' '))
        name = name.strip()
        if val:
            indents[spaces][name] = val
        else:
            newdict = {}
            indents[spaces][name] = newdict
            indents[spaces+2] = newdict
    return ret

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--multi', default=1, type=lambda value: min(max(int(value), 1), 255))
    multiargs, _ = parser.parse_known_args()

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', help='Path to the weights file to use for rolling game settings, urls are also valid')
    parser.add_argument('--samesettings', help='Rolls settings per weights file rather than per player', action='store_true')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--multi', default=1, type=lambda value: min(max(int(value), 1), 255))
    parser.add_argument('--names', default='')
    parser.add_argument('--create_spoiler', action='store_true')
    parser.add_argument('--rom')
    parser.add_argument('--enemizercli')
    parser.add_argument('--outputpath')
    for player in range(1, multiargs.multi + 1):
        parser.add_argument(f'--p{player}', help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.seed is None:
        random.seed(None)
        seed = random.randint(0, 999999999)
    else:
        seed = args.seed
    random.seed(seed)

    seedname = f'M{random.randint(0, 999999999)}'
    print(f"Generating mystery for {args.multi} player{'s' if args.multi > 1 else ''}, {seedname} Seed {seed}")

    weights_cache = {}
    if args.weights:
        weights_cache[args.weights] = get_weights(args.weights)
        print(f"Weights: {args.weights} >> {weights_cache[args.weights]['description']}")
    for player in range(1, args.multi + 1):
        path = getattr(args, f'p{player}')
        if path:
            if path not in weights_cache:
                weights_cache[path] = get_weights(path)
            print(f"P{player} Weights: {path} >> {weights_cache[path]['description']}")

    erargs = parse_arguments(['--multi', str(args.multi)])
    erargs.seed = seed
    erargs.names = args.names
    erargs.create_spoiler = args.create_spoiler
    erargs.race = True
    erargs.outputname = seedname
    erargs.outputpath = args.outputpath

    if args.rom:
        erargs.rom = args.rom
    erargs.enemizercli = args.enemizercli

    settings_cache = {k: (roll_settings(v) if args.samesettings else None) for k, v in weights_cache.items()}

    for player in range(1, args.multi + 1):
        path = getattr(args, f'p{player}') if getattr(args, f'p{player}') else args.weights
        if path:
            settings = settings_cache[path] if settings_cache[path] else roll_settings(weights_cache[path])
            for k, v in vars(settings).items():
                getattr(erargs, k)[player] = v
        else:
            raise RuntimeError(f'No weights specified for player {player}')

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[erargs.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    ERmain(erargs, seed)

def get_weights(path):
    try:
        if urllib.parse.urlparse(path).scheme:
            yaml = str(urllib.request.urlopen(path).read(), "utf-8")
        else:
            with open(path, 'rb') as f:
                yaml = str(f.read(), "utf-8")
    except Exception as e:
        print('Failed to read weights (%s)' % e)
        return

    return parse_yaml(yaml)

def roll_settings(weights):
    def get_choice(option):
        return random.choices(list(weights[option].keys()), weights=list(map(int,weights[option].values())))[0].replace('"','').replace("'",'')

    ret = argparse.Namespace()

    glitches_required = get_choice('glitches_required')
    if glitches_required not in ['none', 'no_logic']:
        print("Only NMG and No Logic supported")
        glitches_required = 'none'
    ret.logic = {'none': 'noglitches', 'no_logic': 'nologic'}[glitches_required]

    item_placement = get_choice('item_placement')
    # not supported in ER

    if {'map_shuffle', 'compass_shuffle', 'smallkey_shuffle', 'bigkey_shuffle'}.issubset(weights.keys()):
        ret.mapshuffle = get_choice('map_shuffle') == 'on'
        ret.compassshuffle = get_choice('compass_shuffle') == 'on'
        ret.keyshuffle = get_choice('smallkey_shuffle') == 'on'
        ret.bigkeyshuffle = get_choice('bigkey_shuffle') == 'on'
    else:
        dungeon_items = get_choice('dungeon_items')
        ret.mapshuffle = dungeon_items in ['mc', 'mcs', 'full']
        ret.compassshuffle = dungeon_items in ['mc', 'mcs', 'full']
        ret.keyshuffle = dungeon_items in ['mcs', 'full']
        ret.bigkeyshuffle = dungeon_items in ['full']

    accessibility = get_choice('accessibility')
    ret.accessibility = accessibility

    entrance_shuffle = get_choice('entrance_shuffle')
    ret.shuffle = entrance_shuffle if entrance_shuffle != 'none' else 'vanilla'

    goals = get_choice('goals')
    ret.goal = {'ganon': 'ganon',
                'fast_ganon': 'crystals',
                'dungeons': 'dungeons',
                'pedestal': 'pedestal',
                'triforce-hunt': 'triforcehunt'
                }[goals]
    ret.openpyramid = goals == 'fast_ganon'

    tower_open = get_choice('tower_open')
    ret.crystals_gt = tower_open

    ganon_open = get_choice('ganon_open')
    ret.crystals_ganon = ganon_open

    world_state = get_choice('world_state')
    ret.mode = world_state
    if world_state == 'retro':
        ret.mode = 'open'
        ret.retro = True

    hints = get_choice('hints')
    ret.hints = hints == 'on'

    weapons = get_choice('weapons')
    ret.swords = {'randomized': 'random',
                  'assured': 'assured',
                  'vanilla': 'vanilla',
                  'swordless': 'swordless'
                  }[weapons]

    item_pool = get_choice('item_pool')
    ret.difficulty = item_pool

    item_functionality = get_choice('item_functionality')
    ret.item_functionality = item_functionality

    boss_shuffle = get_choice('boss_shuffle')
    ret.shufflebosses = {'none': 'none',
                         'simple': 'basic',
                         'full': 'normal',
                         'random': 'chaos'
                         }[boss_shuffle]

    enemy_shuffle = get_choice('enemy_shuffle')
    ret.shuffleenemies = {'none': 'none',
                          'shuffled': 'shuffled',
                          'random': 'chaos'
                          }[enemy_shuffle]

    enemy_damage = get_choice('enemy_damage')
    ret.enemy_damage = {'default': 'default',
                        'shuffled': 'shuffled',
                        'random': 'chaos'
                        }[enemy_damage]

    enemy_health = get_choice('enemy_health')
    ret.enemy_health = enemy_health

    ret.beemizer = int(get_choice('beemizer')) if 'beemizer' in weights.keys() else 1 # suck it :)

    return ret

if __name__ == '__main__':
    main()
