import argparse
import os
import logging
import random
import urllib.request
import urllib.parse

from EntranceRandomizer import parse_arguments
from Main import main as ERmain

def parse_yaml(txt):
    ret = {}
    indents = {0: ret}
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', help='Path to the weights file to use for rolling game settings, urls are also valid', required=True)
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--multi', default=1, type=lambda value: min(max(int(value), 1), 255))
    parser.add_argument('--names', default='')
    parser.add_argument('--create_spoiler', action='store_true')
    parser.add_argument('--rom')
    parser.add_argument('--enemizercli')
    parser.add_argument('--outputpath')
    args = parser.parse_args()

    try:
        if urllib.parse.urlparse(args.weights).scheme:
            yaml = str(urllib.request.urlopen(args.weights).read(), "utf-8")
        else:
            with open(args.weights, 'rb') as f:
                yaml = str(f.read(), "utf-8")
    except Exception as e:
        print('Failed to read weights (%s)' % e)
        return

    random.seed(args.seed)
    weights = parse_yaml(yaml)
    print(f"Weights: {args.weights} >> {weights['description']}")

    while not gen_mystery(args, weights):
        pass

def gen_mystery(args, weights):
    seed = random.randint(0, 999999999)
    seedname = f'M{random.randint(0, 999999999)}_{os.path.splitext(os.path.basename(args.weights))[0]}'

    print(f"Generating mystery for {args.multi} player{'s' if args.multi > 1 else ''}, {seedname} Seed {seed}")

    choices = {}
    def get_choice(option):
        ret = random.choices(list(map(lambda s: s.strip('\''),weights[option].keys())), weights=list(map(int,weights[option].values())))[0]
        choices[option] = ret
        return ret

    erargs = argparse.Namespace
    erargs.seed = seed
    erargs.multi = args.multi
    erargs.names = args.names
    erargs.create_spoiler = args.create_spoiler
    erargs.race = True
    erargs.outputname = seedname
    erargs.outputpath = args.outputpath

    if args.rom:
        erargs.rom = args.rom
    erargs.enemizercli = args.enemizercli

    logic = get_choice('glitches_required')
    if logic not in ['none', 'no_logic']:
        print("Only NMG and No Logic supported")
        return False
    erargs.logic = {'none': 'noglitches', 'no_logic': 'nologic'}[logic]

    item_placement = get_choice('item_placement')
    # not supported in ER

    dungeon_items = get_choice('dungeon_items')
    if dungeon_items in ['mc', 'mcs', 'full']:
        erargs.mapshuffle = True
        erargs.compassshuffle = True
    if dungeon_items in ['mcs', 'full']:
        erargs.keyshuffle = True
    if dungeon_items in ['full']:
        erargs.bigkeyshuffle = True

    accessibility = get_choice('accessibility')
    erargs.accessibility = accessibility

    entrance_shuffle = get_choice('entrance_shuffle')
    erargs.shuffle = entrance_shuffle if entrance_shuffle != 'none' else 'vanilla'

    goals = get_choice('goals')
    erargs.goal = {'ganon': 'ganon',
                   'fast_ganon': 'crystals',
                   'dungeons': 'dungeons',
                   'pedestal': 'pedestal',
                   'triforce-hunt': 'triforce-hunt'
                   }[goals]
    if goals == 'fast_ganon' and entrance_shuffle == 'none':
        erargs.openpyramid = True

    tower_open = get_choice('tower_open')
    erargs.crystals_gt = tower_open

    ganon_open = get_choice('ganon_open')
    erargs.crystals_ganon = ganon_open

    world_state = get_choice('world_state')
    erargs.mode = world_state
    if world_state == 'retro':
        erargs.mode = 'open'
        erargs.retro = True

    hints = get_choice('hints')
    if hints == 'on':
        erargs.hints = True

    weapons = get_choice('weapons')
    erargs.swords = {'randomized': 'random',
                    'assured': 'assured',
                    'vanilla': 'vanilla',
                    'swordless': 'swordless'
                    }[weapons]

    item_pool = get_choice('item_pool')
    erargs.difficulty = item_pool

    item_functionality = get_choice('item_functionality')
    erargs.item_functionality = item_functionality

    boss_shuffle = get_choice('boss_shuffle')
    erargs.shufflebosses = {'none': 'none',
                            'simple': 'basic',
                            'full': 'normal',
                            'random': 'chaos'
                            }[boss_shuffle]

    enemy_shuffle = get_choice('enemy_shuffle')
    erargs.shuffleenemies = {'none': 'none',
                             'shuffled': 'shuffled',
                             'random': 'chaos'
                             }[enemy_shuffle]

    enemy_damage = get_choice('enemy_damage')
    erargs.enemy_damage = {'default': 'default',
                           'shuffled': 'shuffled',
                           'random': 'chaos'
                           }[enemy_damage]

    enemy_health = get_choice('enemy_health')
    erargs.enemy_health = enemy_health

    for k, v in vars(parse_arguments([])).items():
        if k not in vars(erargs):
            setattr(erargs, k, v)

    # set up logger
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[args.loglevel]
    logging.basicConfig(format='%(message)s', level=loglevel)

    try:
        ERmain(erargs, seed)
    except Exception as e:
        logging.exception(e)
        return False

    return True

if __name__ == '__main__':
    main()
