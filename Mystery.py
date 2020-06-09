import argparse
import logging
import random
import urllib.request
import urllib.parse
import typing
import os

import ModuleUpdate

ModuleUpdate.update()

from Utils import parse_yaml
from Rom import get_sprite_from_name
from EntranceRandomizer import parse_arguments
from Main import main as ERmain
from Items import item_name_groups, item_table



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
    parser.add_argument('--teams', default=1, type=lambda value: max(int(value), 1))
    parser.add_argument('--create_spoiler', action='store_true')
    parser.add_argument('--skip_playthrough', action='store_true')
    parser.add_argument('--rom')
    parser.add_argument('--enemizercli')
    parser.add_argument('--outputpath')
    parser.add_argument('--race', action='store_true')
    parser.add_argument('--meta', default=None)
    parser.add_argument('--log_output_path', help='Path to store output log')
    parser.add_argument('--loglevel', default='info', help='Sets log level')
    parser.add_argument('--yaml_output', default=0, type=lambda value: min(max(int(value), 0), 255),
                        help='Output rolled mystery results to yaml up to specified number (made for async multiworld)')

    for player in range(1, multiargs.multi + 1):
        parser.add_argument(f'--p{player}', help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.seed is None:
        random.seed(None)
        seed = random.randint(0, 999999999)
    else:
        seed = args.seed
    random.seed(seed)

    seedname = "M"+(f"{random.randint(0, 999999999)}".zfill(9))
    print(f"Generating mystery for {args.multi} player{'s' if args.multi > 1 else ''}, {seedname} Seed {seed}")

    weights_cache = {}
    if args.weights:
        try:
            weights_cache[args.weights] = get_weights(args.weights)
        except Exception as e:
            raise ValueError(f"File {args.weights} is destroyed. Please fix your yaml.") from e
        print(f"Weights: {args.weights} >> {weights_cache[args.weights]['description']}")
    if args.meta:
        try:
            weights_cache[args.meta] = get_weights(args.meta)
        except Exception as e:
            raise ValueError(f"File {args.meta} is destroyed. Please fix your yaml.") from e
        meta_weights = weights_cache[args.meta]
        print(f"Meta: {args.meta} >> {meta_weights['meta_description']}")
        if args.samesettings:
            raise Exception("Cannot mix --samesettings with --meta")

    for player in range(1, args.multi + 1):
        path = getattr(args, f'p{player}')
        if path:
            try:
                if path not in weights_cache:
                    weights_cache[path] = get_weights(path)
                print(f"P{player} Weights: {path} >> {weights_cache[path]['description']}")

            except Exception as e:
                raise ValueError(f"File {path} is destroyed. Please fix your yaml.") from e
    erargs = parse_arguments(['--multi', str(args.multi)])
    erargs.seed = seed
    erargs.name = {x: "" for x in range(1, args.multi + 1)} # only so it can be overwrittin in mystery
    erargs.create_spoiler = args.create_spoiler
    erargs.race = args.race
    erargs.skip_playthrough = args.skip_playthrough
    erargs.outputname = seedname
    erargs.outputpath = args.outputpath
    erargs.teams = args.teams
    erargs.progression_balancing = {}

    # set up logger
    if args.loglevel:
        erargs.loglevel = args.loglevel
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[erargs.loglevel]

    import sys
    class LoggerWriter(object):
        def __init__(self, writer):
            self._writer = writer
            self._msg = ''

        def write(self, message):
            self._msg = self._msg + message
            while '\n' in self._msg:
                pos = self._msg.find('\n')
                self._writer(self._msg[:pos])
                self._msg = self._msg[pos + 1:]

        def flush(self):
            if self._msg != '':
                self._writer(self._msg)
                self._msg = ''

    if args.log_output_path:
        log = logging.getLogger("stderr")
        log.addHandler(logging.StreamHandler())
        sys.stderr = LoggerWriter(log.error)
        os.makedirs(args.log_output_path, exist_ok=True)
        logging.basicConfig(format='%(message)s', level=loglevel, filename=os.path.join(args.log_output_path, f"{seed}.log"))
    else:
        logging.basicConfig(format='%(message)s', level=loglevel)
    if args.rom:
        erargs.rom = args.rom

    if args.enemizercli:
        erargs.enemizercli = args.enemizercli

    settings_cache = {k: (roll_settings(v) if args.samesettings else None) for k, v in weights_cache.items()}
    player_path_cache = {}
    for player in range(1, args.multi + 1):
        player_path_cache[player] = getattr(args, f'p{player}') if getattr(args, f'p{player}') else args.weights

    if args.meta:
        for player, path in player_path_cache.items():
            weights_cache[path].setdefault("meta_ignore", [])
        meta_weights = weights_cache[args.meta]
        for key in meta_weights:
            option = get_choice(key, meta_weights)
            if option is not None:
                for player, path in player_path_cache.items():
                    players_meta = weights_cache[path].get("meta_ignore", [])
                    if key not in players_meta:
                        weights_cache[path][key] = option
                    elif type(players_meta) == dict and players_meta[key] and option not in players_meta[key]:
                        weights_cache[path][key] = option

    for player in range(1, args.multi + 1):
        path = player_path_cache[player]
        if path:
            try:
                settings = settings_cache[path] if settings_cache[path] else roll_settings(weights_cache[path])
                if settings.sprite is not None and not os.path.isfile(settings.sprite) and not get_sprite_from_name(settings.sprite):
                    logging.warning(
                        f"Warning: The chosen sprite, \"{settings.sprite}\", for yaml \"{path}\", does not exist.")
                for k, v in vars(settings).items():
                    if v is not None:
                        getattr(erargs, k)[player] = v
            except Exception as e:
                raise ValueError(f"File {path} is destroyed. Please fix your yaml.") from e
        else:
            raise RuntimeError(f'No weights specified for player {player}')
        if not erargs.name[player]:
            erargs.name[player] = os.path.split(path)[-1].split(".")[0]
    if args.weights:
        erargs.names = ""
    else:
        erargs.names = ",".join(erargs.name[i] for i in range(1, args.multi + 1))
    del (erargs.name)
    if args.yaml_output:
        import yaml
        important = {}
        for option, player_settings in vars(erargs).items():
            if type(player_settings) == dict:
                if len(set(player_settings.values())) > 1:
                    important[option] = {player: value for player, value in player_settings.items() if
                                         player <= args.yaml_output}
                elif len(set(player_settings.values())) > 0:
                    important[option] = player_settings[1]
                else:
                    logging.debug(f"No player settings defined for option '{option}'")
            else:
                if player_settings != "":  # is not empty name
                    important[option] = player_settings
                else:
                    logging.debug(f"No player settings defined for option '{option}'")
        if args.outputpath:
            os.makedirs(args.outputpath, exist_ok=True)
        with open(os.path.join(args.outputpath if args.outputpath else ".", f"mystery_result_{seed}.yaml"), "wt") as f:
            yaml.dump(important, f)

    erargs.skip_progression_balancing = {player: not balanced for player, balanced in
                                         erargs.progression_balancing.items()}
    del (erargs.progression_balancing)
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


def get_choice(option, root) -> typing.Any:
    if option not in root:
        return None
    if type(root[option]) is not dict:
        return interpret_on_off(root[option])
    if not root[option]:
        return None
    return interpret_on_off(
        random.choices(list(root[option].keys()), weights=list(map(int, root[option].values())))[0])


def handle_name(name: str):
    return name.strip().replace(' ', '_')


def roll_settings(weights):
    ret = argparse.Namespace()
    if "linked_options" in weights:
        weights = weights.copy()  # make sure we don't write back to other weights sets in same_settings
        for option_set in weights["linked_options"]:
            if random.random() < (option_set["percentage"] / 100):
                weights.update(option_set["options"])

    ret.name = get_choice('name', weights)
    if ret.name:
        ret.name = handle_name(ret.name)

    glitches_required = get_choice('glitches_required', weights)
    if glitches_required not in ['none', 'no_logic', 'overworld_glitches']:
        logging.warning("Only NMG, OWG and No Logic supported")
        glitches_required = 'none'
    ret.logic = {None: 'noglitches', 'none': 'noglitches', 'no_logic': 'nologic', 'overworld_glitches': 'owglitches'}[
        glitches_required]
    ret.progression_balancing = get_choice('progression_balancing',
                                           weights) if 'progression_balancing' in weights else True
    # item_placement = get_choice('item_placement')
    # not supported in ER

    dungeon_items = get_choice('dungeon_items', weights)
    if dungeon_items == 'full' or dungeon_items == True:
        dungeon_items = 'mcsb'
    elif dungeon_items == 'standard':
        dungeon_items = ""
    elif not dungeon_items:
        dungeon_items = ""

    ret.mapshuffle = get_choice('map_shuffle', weights) if 'map_shuffle' in weights else 'm' in dungeon_items
    ret.compassshuffle = get_choice('compass_shuffle', weights) if 'compass_shuffle' in weights else 'c' in dungeon_items
    ret.keyshuffle = get_choice('smallkey_shuffle', weights) if 'smallkey_shuffle' in weights else 's' in dungeon_items
    ret.bigkeyshuffle = get_choice('bigkey_shuffle', weights) if 'bigkey_shuffle' in weights else 'b' in dungeon_items

    ret.accessibility = get_choice('accessibility', weights)

    entrance_shuffle = get_choice('entrance_shuffle', weights)
    ret.shuffle = entrance_shuffle if entrance_shuffle != 'none' else 'vanilla'

    goal = get_choice('goals', weights)
    ret.goal = {'ganon': 'ganon',
                'fast_ganon': 'crystals',
                'dungeons': 'dungeons',
                'pedestal': 'pedestal',
                'triforce_hunt': 'triforcehunt',
                'triforce-hunt': 'triforcehunt',  # deprecated, moving all goals to `_`
                'local_triforce_hunt': 'localtriforcehunt'
                }[goal]
    ret.openpyramid = goal == 'fast_ganon'

    ret.crystals_gt = get_choice('tower_open', weights)

    ret.crystals_ganon = get_choice('ganon_open', weights)

    ret.triforce_pieces_required = get_choice('triforce_pieces_required',
                                              weights) if "triforce_pieces_required" in weights else 20
    ret.triforce_pieces_required = min(max(1, int(ret.triforce_pieces_required)), 30)

    ret.mode = get_choice('world_state', weights)
    if ret.mode == 'retro':
        ret.mode = 'open'
        ret.retro = True

    ret.hints = get_choice('hints', weights)

    ret.swords = {'randomized': 'random',
                  'assured': 'assured',
                  'vanilla': 'vanilla',
                  'swordless': 'swordless'
                  }[get_choice('weapons', weights)]

    ret.difficulty = get_choice('item_pool', weights)

    ret.item_functionality = get_choice('item_functionality', weights)

    ret.shufflebosses = {'none': 'none',
                         'simple': 'basic',
                         'full': 'normal',
                         'random': 'chaos'
                         }[get_choice('boss_shuffle', weights)]

    ret.shuffleenemies = {'none': 'none',
                          'shuffled': 'shuffled',
                          'random': 'chaos'
                          }[get_choice('enemy_shuffle', weights)]

    ret.enemy_damage = {'default': 'default',
                        'shuffled': 'shuffled',
                        'random': 'chaos'
                        }[get_choice('enemy_damage', weights)]

    ret.enemy_health = get_choice('enemy_health', weights)

    ret.shufflepots = get_choice('pot_shuffle', weights)

    ret.beemizer = int(get_choice('beemizer', weights)) if 'beemizer' in weights else 0

    ret.timer = {'none': False,
                 None: False,
                 False: False,
                 'timed': 'timed',
                 'timed_ohko': 'timed-ohko',
                 'ohko': 'ohko',
                 'timed_countdown': 'timed-countdown',
                 'display': 'display'}[get_choice('timer', weights)] if 'timer' in weights.keys() else False

    ret.dungeon_counters = get_choice('dungeon_counters', weights) if 'dungeon_counters' in weights else 'default'

    ret.progressive = convert_to_on_off(get_choice('progressive', weights)) if "progressive" in weights else 'on'
    inventoryweights = weights.get('startinventory', {})
    startitems = []
    for item in inventoryweights.keys():
        itemvalue = get_choice(item, inventoryweights)
        if item.startswith(('Progressive ', 'Small Key ', 'Rupee', 'Piece of Heart', 'Boss Heart Container',
                            'Sanctuary Heart Container', 'Arrow', 'Bombs ', 'Bomb ', 'Bottle')) and isinstance(
            itemvalue, int):
            for i in range(int(itemvalue)):
                startitems.append(item)
        elif itemvalue:
            startitems.append(item)
    ret.startinventory = ','.join(startitems)

    ret.glitch_boots = get_choice('glitch_boots', weights) if 'glitch_boots' in weights else True

    ret.remote_items = get_choice('remote_items', weights) if 'remote_items' in weights else False

    ret.local_items = set()
    for item_name in weights.get('local_items', []):
        items = item_name_groups.get(item_name, {item_name})
        for item in items:
            if item in item_table:
                ret.local_items.add(item)
            else:
                logging.warning(f"Could not force item {item} to be world-local, as it was not recognized.")
    ret.local_items = ",".join(ret.local_items)

    if 'rom' in weights:
        romweights = weights['rom']
        ret.sprite = get_choice('sprite', romweights)
        ret.disablemusic = get_choice('disablemusic', romweights)
        ret.quickswap = get_choice('quickswap', romweights)
        ret.fastmenu = get_choice('menuspeed', romweights)
        ret.heartcolor = get_choice('heartcolor', romweights)
        ret.heartbeep = convert_to_on_off(get_choice('heartbeep', romweights))
        ret.ow_palettes = get_choice('ow_palettes', romweights)
        ret.uw_palettes = get_choice('uw_palettes', romweights)

    return ret

if __name__ == '__main__':
    main()
