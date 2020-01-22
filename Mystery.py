import argparse
import logging
import random
import urllib.request
import urllib.parse

from EntranceRandomizer import parse_arguments
from Main import main as ERmain

def parse_yaml(txt):
    def strip(s):
        s = s.strip()
        return '' if not s else s.strip('"') if s[0] == '"' else s.strip("'") if s[0] == "'" else s
    ret = {}
    indents = {len(txt) - len(txt.lstrip(' ')): ret}
    for line in txt.splitlines():
        if not line:
            continue
        name, val = line.split(':', 1)
        val = strip(val)
        spaces = len(name) - len(name.lstrip(' '))
        name = strip(name)
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
    parser.add_argument('--teams', default=1, type=lambda value: max(int(value), 1))
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
    if args.enemizercli:
        erargs.enemizercli = args.enemizercli

    settings_cache = {k: (roll_settings(v) if args.samesettings else None) for k, v in weights_cache.items()}

    for player in range(1, args.multi + 1):
        path = getattr(args, f'p{player}') if getattr(args, f'p{player}') else args.weights
        if path:
            settings = settings_cache[path] if settings_cache[path] else roll_settings(weights_cache[path])
            for k, v in vars(settings).items():
                if v is not None:
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
    def get_choice(option, root=weights):
        if option not in root:
            return None
        if type(root[option]) is not dict:
            return root[option]
        if not root[option]:
            return None
        return random.choices(list(root[option].keys()), weights=list(map(int,root[option].values())))[0]

    ret = argparse.Namespace()

    glitches_required = get_choice('glitches_required')
    if glitches_required not in ['none', 'no_logic', 'overworld_glitches']:
        print("Only NMG, OWG and No Logic supported")
        glitches_required = 'none'
    ret.logic = {'none': 'noglitches', 'no_logic': 'nologic', 'overworld_glitches': 'owglitches'}[glitches_required]

    item_placement = get_choice('item_placement')
    # not supported in ER

    dungeon_items = get_choice('dungeon_items')
    ret.mapshuffle = get_choice('map_shuffle') == 'on' if 'map_shuffle' in weights else dungeon_items in ['mc', 'mcs', 'full']
    ret.compassshuffle = get_choice('compass_shuffle') == 'on' if 'compass_shuffle' in weights else dungeon_items in ['mc', 'mcs', 'full']
    ret.keyshuffle = get_choice('smallkey_shuffle') == 'on' if 'smallkey_shuffle' in weights else dungeon_items in ['mcs', 'full']
    ret.bigkeyshuffle = get_choice('bigkey_shuffle') == 'on' if 'bigkey_shuffle' in weights else dungeon_items in ['full']

    ret.accessibility = get_choice('accessibility')

    entrance_shuffle = get_choice('entrance_shuffle')
    ret.shuffle = entrance_shuffle if entrance_shuffle != 'none' else 'vanilla'

    goal = get_choice('goals')
    ret.goal = {'ganon': 'ganon',
                'fast_ganon': 'crystals',
                'dungeons': 'dungeons',
                'pedestal': 'pedestal',
                'triforce-hunt': 'triforcehunt'
                }[goal]
    ret.openpyramid = goal == 'fast_ganon'

    ret.crystals_gt = get_choice('tower_open')

    ret.crystals_ganon =  get_choice('ganon_open')

    ret.mode = get_choice('world_state')
    if ret.mode == 'retro':
        ret.mode = 'open'
        ret.retro = True

    ret.hints = get_choice('hints') == 'on'

    ret.swords = {'randomized': 'random',
                  'assured': 'assured',
                  'vanilla': 'vanilla',
                  'swordless': 'swordless'
                  }[get_choice('weapons')]

    ret.difficulty = get_choice('item_pool')

    ret.item_functionality = get_choice('item_functionality')

    ret.shufflebosses = {'none': 'none',
                         'simple': 'basic',
                         'full': 'normal',
                         'random': 'chaos'
                         }[get_choice('boss_shuffle')]

    ret.shuffleenemies = {'none': 'none',
                          'shuffled': 'shuffled',
                          'random': 'chaos'
                          }[get_choice('enemy_shuffle')]

    ret.enemy_damage = {'default': 'default',
                        'shuffled': 'shuffled',
                        'random': 'chaos'
                        }[get_choice('enemy_damage')]

    ret.enemy_health = get_choice('enemy_health')

    ret.shufflepots = get_choice('pot_shuffle') == 'on'

    ret.beemizer = int(get_choice('beemizer')) if 'beemizer' in weights else 0

    inventoryweights = weights.get('startinventory', {})
    startitems = []
    for item in inventoryweights.keys():
        if get_choice(item, inventoryweights) == 'on':
            startitems.append(item)
    ret.startinventory = ','.join(startitems)

    if 'rom' in weights:
        romweights = weights['rom']
        ret.sprite = get_choice('sprite', romweights)
        ret.disablemusic = get_choice('disablemusic', romweights) == 'on'
        ret.quickswap = get_choice('quickswap', romweights) == 'on'
        ret.fastmenu = get_choice('menuspeed', romweights)
        ret.heartcolor = get_choice('heartcolor', romweights)
        ret.heartbeep = get_choice('heartbeep', romweights)
        ret.ow_palettes = get_choice('ow_palettes', romweights)
        ret.uw_palettes = get_choice('uw_palettes', romweights)

    return ret

if __name__ == '__main__':
    main()
