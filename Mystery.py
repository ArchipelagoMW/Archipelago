import argparse
import logging
import random
import urllib.request
import urllib.parse
import functools

import ModuleUpdate

ModuleUpdate.update()

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from EntranceRandomizer import parse_arguments
from Main import main as ERmain

parse_yaml = functools.partial(load, Loader=Loader)


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--multi', default=1, type=lambda value: min(max(int(value), 1), 255))
    multiargs, _ = parser.parse_known_args()

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights',
                        help='Path to the weights file to use for rolling game settings, urls are also valid')
    parser.add_argument('--samesettings', help='Rolls settings per weights file rather than per player',
                        action='store_true')
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--multi', default=1, type=lambda value: min(max(int(value), 1), 255))
    parser.add_argument('--names', default='')
    parser.add_argument('--teams', default=1, type=lambda value: max(int(value), 1))
    parser.add_argument('--create_spoiler', action='store_true')
    parser.add_argument('--rom')
    parser.add_argument('--enemizercli')
    parser.add_argument('--outputpath')
    parser.add_argument('--race', action='store_true')
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
                try:
                    weights_cache[path] = get_weights(path)
                except:
                    raise ValueError(f"File {path} is destroyed. Please fix your yaml.")
            print(f"P{player} Weights: {path} >> {weights_cache[path]['description']}")

    erargs = parse_arguments(['--multi', str(args.multi)])
    erargs.seed = seed
    erargs.names = args.names
    erargs.create_spoiler = args.create_spoiler
    erargs.race = args.race
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
            try:
                settings = settings_cache[path] if settings_cache[path] else roll_settings(weights_cache[path])
                for k, v in vars(settings).items():
                    if v is not None:
                        getattr(erargs, k)[player] = v
            except:
                raise ValueError(f"File {path} is destroyed. Please fix your yaml.")
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


def interpret_on_off(value):
    return {"on": True, "off": False}.get(value, value)

def convert_to_on_off(value):
    return {True: "on", False: "off"}.get(value, value)

def roll_settings(weights):
    def get_choice(option, root=weights):
        if option not in root:
            return None
        if type(root[option]) is not dict:
            return interpret_on_off(root[option])
        if not root[option]:
            return None
        return interpret_on_off(
            random.choices(list(root[option].keys()), weights=list(map(int, root[option].values())))[0])

    ret = argparse.Namespace()

    glitches_required = get_choice('glitches_required')
    if glitches_required not in ['none', 'no_logic']:
        print("Only NMG and No Logic supported")
        glitches_required = 'none'
    ret.logic = {'none': 'noglitches', 'no_logic': 'nologic'}[glitches_required]

    # item_placement = get_choice('item_placement')
    # not supported in ER

    dungeon_items = get_choice('dungeon_items')
    if dungeon_items == 'full':
        dungeon_items = 'mcsb'
    ret.mapshuffle = get_choice('map_shuffle') if 'map_shuffle' in weights else 'm' in dungeon_items
    ret.compassshuffle = get_choice('compass_shuffle') if 'compass_shuffle' in weights else 'c' in dungeon_items
    ret.keyshuffle = get_choice('smallkey_shuffle') if 'smallkey_shuffle' in weights else 's' in dungeon_items
    ret.bigkeyshuffle = get_choice('bigkey_shuffle') if 'bigkey_shuffle' in weights else 'b' in dungeon_items

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

    ret.crystals_ganon = get_choice('ganon_open')

    ret.mode = get_choice('world_state')
    if ret.mode == 'retro':
        ret.mode = 'open'
        ret.retro = True

    ret.hints = get_choice('hints')

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

    ret.shufflepots = get_choice('pot_shuffle')

    ret.beemizer = int(get_choice('beemizer')) if 'beemizer' in weights else 0

    ret.progressive = convert_to_on_off(get_choice('progressive')) if "progressive" in weights else 'on'
    inventoryweights = weights.get('startinventory', {})
    startitems = []
    for item in inventoryweights.keys():
        itemvalue = get_choice(item, inventoryweights)
        if item.startswith(('Progressive ', 'Small Key ', 'Rupee', 'Piece of Heart', 'Boss Heart Container', 'Sanctuary Heart Container', 'Arrow', 'Bombs ', 'Bomb ', 'Bottle')) and isinstance(itemvalue, int):
            for i in range(int(itemvalue)):
                startitems.append(item)
        elif itemvalue:
            startitems.append(item)
    if glitches_required in ['no_logic'] and 'Pegasus Boots' not in startitems:
        startitems.append('Pegasus Boots')
    ret.startinventory = ','.join(startitems)

    if 'rom' in weights:
        romweights = weights['rom']
        ret.sprite = get_choice('sprite', romweights)
        ret.disablemusic = get_choice('disablemusic', romweights)
        ret.extendedmsu = get_choice('extendedmsu', romweights)
        ret.quickswap = get_choice('quickswap', romweights)
        ret.fastmenu = get_choice('menuspeed', romweights)
        ret.heartcolor = get_choice('heartcolor', romweights)
        ret.heartbeep = convert_to_on_off(get_choice('heartbeep', romweights))
        ret.ow_palettes = get_choice('ow_palettes', romweights)
        ret.uw_palettes = get_choice('uw_palettes', romweights)

    return ret

if __name__ == '__main__':
    main()
