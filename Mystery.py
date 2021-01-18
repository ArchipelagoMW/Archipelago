import argparse
import logging
import random
import urllib.request
import urllib.parse
import typing
import os

import ModuleUpdate
from BaseClasses import PlandoItem, PlandoConnection

ModuleUpdate.update()

import Bosses
from Utils import parse_yaml
from Rom import Sprite
from EntranceRandomizer import parse_arguments
from Main import main as ERmain
from Main import get_seed, seeddigits
from Items import item_name_groups, item_table
from Regions import location_table, key_drop_data
from Text import TextTable


def mystery_argparse():
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
    parser.add_argument('--create_diff', action="store_true")
    parser.add_argument('--yaml_output', default=0, type=lambda value: min(max(int(value), 0), 255),
                        help='Output rolled mystery results to yaml up to specified number (made for async multiworld)')
    parser.add_argument('--plando', default="bosses",
                        help='List of options that can be set manually. Can be combined, for example "bosses, items"')

    for player in range(1, multiargs.multi + 1):
        parser.add_argument(f'--p{player}', help=argparse.SUPPRESS)
    args = parser.parse_args()
    args.plando: typing.Set[str] = {arg.strip().lower() for arg in args.plando.split(",")}
    return args


def main(args=None, callback=ERmain):
    if not args:
        args = mystery_argparse()

    seed = get_seed(args.seed)
    random.seed(seed)

    seedname = "M" + (f"{random.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits))
    print(f"Generating mystery for {args.multi} player{'s' if args.multi > 1 else ''}, {seedname} Seed {seed}")

    if args.race:
        random.seed()  # reset to time-based random source

    weights_cache = {}
    if args.weights:
        try:
            weights_cache[args.weights] = get_weights(args.weights)
        except Exception as e:
            raise ValueError(f"File {args.weights} is destroyed. Please fix your yaml.") from e
        print(f"Weights: {args.weights} >> "
              f"{get_choice('description', weights_cache[args.weights], 'No description specified')}")
    if args.meta:
        try:
            weights_cache[args.meta] = get_weights(args.meta)
        except Exception as e:
            raise ValueError(f"File {args.meta} is destroyed. Please fix your yaml.") from e
        meta_weights = weights_cache[args.meta]
        print(f"Meta: {args.meta} >> {get_choice('meta_description', meta_weights, 'No description specified')}")
        if args.samesettings:
            raise Exception("Cannot mix --samesettings with --meta")

    for player in range(1, args.multi + 1):
        path = getattr(args, f'p{player}')
        if path:
            try:
                if path not in weights_cache:
                    weights_cache[path] = get_weights(path)
                print(f"P{player} Weights: {path} >> "
                      f"{get_choice('description', weights_cache[path], 'No description specified')}")

            except Exception as e:
                raise ValueError(f"File {path} is destroyed. Please fix your yaml.") from e
    erargs = parse_arguments(['--multi', str(args.multi)])
    erargs.seed = seed
    erargs.name = {x: "" for x in range(1, args.multi + 1)}  # only so it can be overwrittin in mystery
    erargs.create_spoiler = args.create_spoiler
    erargs.create_diff = args.create_diff
    erargs.race = args.race
    erargs.skip_playthrough = args.skip_playthrough
    erargs.outputname = seedname
    erargs.outputpath = args.outputpath
    erargs.teams = args.teams
    erargs.progression_balancing = {}

    # set up logger
    if args.loglevel:
        erargs.loglevel = args.loglevel
    loglevel = {'error': logging.ERROR, 'info': logging.INFO, 'warning': logging.WARNING, 'debug': logging.DEBUG}[
        erargs.loglevel]

    if args.log_output_path:
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

        log = logging.getLogger("stderr")
        log.addHandler(logging.StreamHandler())
        sys.stderr = LoggerWriter(log.error)
        os.makedirs(args.log_output_path, exist_ok=True)
        logging.basicConfig(format='%(message)s', level=loglevel,
                            filename=os.path.join(args.log_output_path, f"{seed}.log"))
    else:
        logging.basicConfig(format='%(message)s', level=loglevel)
    if args.rom:
        erargs.rom = args.rom

    if args.enemizercli:
        erargs.enemizercli = args.enemizercli

    settings_cache = {k: (roll_settings(v, args.plando) if args.samesettings else None)
                      for k, v in weights_cache.items()}
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
                settings = settings_cache[path] if settings_cache[path] else \
                    roll_settings(weights_cache[path], args.plando)
                if settings.sprite and not os.path.isfile(settings.sprite) and not Sprite.get_sprite_from_name(
                        settings.sprite):
                    logging.warning(
                        f"Warning: The chosen sprite, \"{settings.sprite}\", for yaml \"{path}\", does not exist.")
                for k, v in vars(settings).items():
                    if v is not None:
                        getattr(erargs, k)[player] = v
            except Exception as e:
                raise ValueError(f"File {path} is destroyed. Please fix your yaml.") from e
        else:
            raise RuntimeError(f'No weights specified for player {player}')
        if path == args.weights:  # if name came from the weights file, just use base player name
            erargs.name[player] = f"Player{player}"
        elif not erargs.name[player]:  # if name was not specified, generate it from filename
            erargs.name[player] = os.path.split(path)[-1].split(".")[0]
    erargs.names = ",".join(erargs.name[i] for i in range(1, args.multi + 1))
    del (erargs.name)
    if args.yaml_output:
        import yaml
        important = {}
        for option, player_settings in vars(erargs).items():
            if type(player_settings) == dict:
                if all(type(value) != list for value in player_settings.values()):
                    if len(frozenset(player_settings.values())) > 1:
                        important[option] = {player: value for player, value in player_settings.items() if
                                             player <= args.yaml_output}
                    elif len(frozenset(player_settings.values())) > 0:
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
    callback(erargs, seed)


def get_weights(path):
    try:
        if urllib.parse.urlparse(path).scheme:
            yaml = str(urllib.request.urlopen(path).read(), "utf-8")
        else:
            with open(path, 'rb') as f:
                yaml = str(f.read(), "utf-8")
    except Exception as e:
        raise Exception(f"Failed to read weights ({path})") from e

    return parse_yaml(yaml)


def interpret_on_off(value):
    return {"on": True, "off": False}.get(value, value)


def convert_to_on_off(value):
    return {True: "on", False: "off"}.get(value, value)


def get_choice(option, root, value=None) -> typing.Any:
    if option not in root:
        return value
    if type(root[option]) is list:
        return interpret_on_off(random.choices(root[option])[0])
    if type(root[option]) is not dict:
        return interpret_on_off(root[option])
    if not root[option]:
        return value
    if any(root[option].values()):
        return interpret_on_off(
            random.choices(list(root[option].keys()), weights=list(map(int, root[option].values())))[0])
    raise RuntimeError(f"All options specified in \"{option}\" are weighted as zero.")


def handle_name(name: str):
    return name.strip().replace(' ', '_')[:16]


def prefer_int(input_data: str) -> typing.Union[str, int]:
    try:
        return int(input_data)
    except:
        return input_data


available_boss_names: typing.Set[str] = {boss.lower() for boss in Bosses.boss_table if boss not in
                                         {'Agahnim', 'Agahnim2', 'Ganon'}}

boss_shuffle_options = {None: 'none',
                        'none': 'none',
                        'simple': 'basic',
                        'basic': 'basic',
                        'full': 'normal',
                        'normal': 'normal',
                        'random': 'chaos',
                        'chaos': 'chaos',
                        'singularity': 'singularity',
                        'duality': 'singularity'
                        }


def roll_percentage(percentage: typing.Union[int, float]) -> bool:
    """Roll a percentage chance.
    percentage is expected to be in range [0, 100]"""
    return random.random() < (float(percentage) / 100)


def roll_settings(weights, plando_options: typing.Set[str] = frozenset(("bosses"))):
    ret = argparse.Namespace()
    if "linked_options" in weights:
        weights = weights.copy()  # make sure we don't write back to other weights sets in same_settings
        for option_set in weights["linked_options"]:
            if "name" not in option_set:
                raise ValueError("One of your linked options does not have a name.")
            try:
                if roll_percentage(option_set["percentage"]):
                    logging.debug(f"Linked option {option_set['name']} triggered.")
                    logging.debug(f'Applying {option_set["options"]}')
                    new_options = set(option_set["options"]) - set(weights)
                    weights.update(option_set["options"])
                    if new_options:
                        for new_option in new_options:
                            logging.warning(f'Linked Suboption "{new_option}" of "{option_set["name"]}" did not '
                                            f'overwrite a root option. '
                                            f"This is probably in error.")
                else:
                    logging.debug(f"linked option {option_set['name']} skipped.")
            except Exception as e:
                raise ValueError(f"Linked option {option_set['name']} is destroyed. "
                                 f"Please fix your linked option.") from e

    ret.name = get_choice('name', weights)
    if ret.name:
        ret.name = handle_name(ret.name)

    glitches_required = get_choice('glitches_required', weights)
    if glitches_required not in [None, 'none', 'no_logic', 'overworld_glitches', 'minor_glitches']:
        logging.warning("Only NMG, OWG and No Logic supported")
        glitches_required = 'none'
    ret.logic = {None: 'noglitches', 'none': 'noglitches', 'no_logic': 'nologic', 'overworld_glitches': 'owglitches',
                 'minor_glitches': 'minorglitches'}[
        glitches_required]

    ret.dark_room_logic = get_choice("dark_room_logic", weights, "lamp")
    if not ret.dark_room_logic:  # None/False
        ret.dark_room_logic = "none"
    if ret.dark_room_logic == "sconces":
        ret.dark_room_logic = "torches"
    if ret.dark_room_logic not in {"lamp", "torches", "none"}:
        raise ValueError(f"Unknown Dark Room Logic: \"{ret.dark_room_logic}\"")

    ret.restrict_dungeon_item_on_boss = get_choice('restrict_dungeon_item_on_boss', weights, False)

    ret.progression_balancing = get_choice('progression_balancing', weights, True)
    # item_placement = get_choice('item_placement')
    # not supported in ER

    dungeon_items = get_choice('dungeon_items', weights)
    if dungeon_items == 'full' or dungeon_items == True:
        dungeon_items = 'mcsb'
    elif dungeon_items == 'standard':
        dungeon_items = ""
    elif not dungeon_items:
        dungeon_items = ""
    if "u" in dungeon_items:
        dungeon_items.replace("s", "")

    ret.mapshuffle = get_choice('map_shuffle', weights, 'm' in dungeon_items)
    ret.compassshuffle = get_choice('compass_shuffle', weights, 'c' in dungeon_items)
    ret.keyshuffle = get_choice('smallkey_shuffle', weights,
                                'universal' if 'u' in dungeon_items else 's' in dungeon_items)
    ret.bigkeyshuffle = get_choice('bigkey_shuffle', weights, 'b' in dungeon_items)

    ret.accessibility = get_choice('accessibility', weights)

    entrance_shuffle = get_choice('entrance_shuffle', weights)
    ret.shuffle = entrance_shuffle if entrance_shuffle != 'none' else 'vanilla'

    goal = get_choice('goals', weights, 'ganon')
    ret.goal = {'ganon': 'ganon',
                'fast_ganon': 'crystals',
                'dungeons': 'dungeons',
                'pedestal': 'pedestal',
                'ganon_pedestal': 'ganonpedestal',
                'triforce_hunt': 'triforcehunt',
                'triforce-hunt': 'triforcehunt',  # deprecated, moving all goals to `_`
                'local_triforce_hunt': 'localtriforcehunt',
                'ganon_triforce_hunt': 'ganontriforcehunt',
                'local_ganon_triforce_hunt': 'localganontriforcehunt',
                'ice_rod_hunt': 'icerodhunt'
                }[goal]

    # TODO consider moving open_pyramid to an automatic variable in the core roller, set to True when
    # fast ganon + ganon at hole
    ret.open_pyramid = ret.goal in {'crystals', 'ganontriforcehunt', 'localganontriforcehunt', 'ganonpedestal'}

    ret.crystals_gt = prefer_int(get_choice('tower_open', weights))

    ret.crystals_ganon = prefer_int(get_choice('ganon_open', weights))

    extra_pieces = get_choice('triforce_pieces_mode', weights, 'available')

    ret.triforce_pieces_required = int(get_choice('triforce_pieces_required', weights, 20))
    ret.triforce_pieces_required = min(max(1, int(ret.triforce_pieces_required)), 90)

    # sum a percentage to required
    if extra_pieces == 'percentage':
        percentage = max(100, float(get_choice('triforce_pieces_percentage', weights, 150))) / 100
        ret.triforce_pieces_available = int(round(ret.triforce_pieces_required * percentage, 0))
    # vanilla mode (specify how many pieces are)
    elif extra_pieces == 'available':
        ret.triforce_pieces_available = int(get_choice('triforce_pieces_available', weights, 30))
    # required pieces + fixed extra
    elif extra_pieces == 'extra':
        extra_pieces = max(0, int(get_choice('triforce_pieces_extra', weights, 10)))
        ret.triforce_pieces_available = ret.triforce_pieces_required + extra_pieces

    # change minimum to required pieces to avoid problems
    ret.triforce_pieces_available = min(max(ret.triforce_pieces_required, int(ret.triforce_pieces_available)), 90)

    ret.shop_shuffle_slots = int(get_choice('shop_shuffle_slots', weights, '0'))

    ret.shop_shuffle = get_choice('shop_shuffle', weights, '')
    if not ret.shop_shuffle:
        ret.shop_shuffle = ''

    ret.mode = get_choice('world_state', weights, None)  # legacy support
    if ret.mode == 'retro':
        ret.mode = 'open'
        ret.retro = True
    elif ret.mode is None:
        ret.mode = get_choice("mode", weights)
        ret.retro = get_choice("retro", weights)

    ret.hints = get_choice('hints', weights)

    ret.swords = {'randomized': 'random',
                  'assured': 'assured',
                  'vanilla': 'vanilla',
                  'swordless': 'swordless'
                  }[get_choice('weapons', weights, 'assured')]

    ret.difficulty = get_choice('item_pool', weights)

    ret.item_functionality = get_choice('item_functionality', weights)

    boss_shuffle = get_choice('boss_shuffle', weights)

    if boss_shuffle in boss_shuffle_options:
        ret.shufflebosses = boss_shuffle_options[boss_shuffle]
    elif "bosses" in plando_options:
        options = boss_shuffle.lower().split(";")
        remainder_shuffle = "none"  # vanilla
        bosses = []
        for boss in options:
            if boss in boss_shuffle_options:
                remainder_shuffle = boss_shuffle_options[boss]
            elif boss not in available_boss_names and not "-" in boss:
                raise ValueError(f"Unknown Boss name or Boss shuffle option {boss}.")
            else:
                bosses.append(boss)
        ret.shufflebosses = ";".join(bosses + [remainder_shuffle])
    else:
        raise Exception(f"Boss Shuffle {boss_shuffle} is unknown and boss plando is turned off.")

    ret.enemy_shuffle = {'none': False,
                         'shuffled': 'shuffled',
                         'random': 'chaos',
                         'chaosthieves': 'chaosthieves',
                         'chaos': 'chaos',
                         True: True,
                         False: False,
                         None: False
                         }[get_choice('enemy_shuffle', weights, False)]

    ret.killable_thieves = get_choice('killable_thieves', weights, False)
    ret.tile_shuffle = get_choice('tile_shuffle', weights, False)
    ret.bush_shuffle = get_choice('bush_shuffle', weights, False)

    # legacy support for enemy shuffle
    if type(ret.enemy_shuffle) == str:
        if ret.enemy_shuffle == 'shuffled':
            ret.killable_thieves = True
        elif ret.enemy_shuffle == 'chaos':
            ret.killable_thieves = True
            ret.bush_shuffle = True
            ret.tile_shuffle = True
        elif ret.enemy_shuffle == "chaosthieves":
            ret.killable_thieves = bool(random.randint(0, 1))
            ret.bush_shuffle = True
            ret.tile_shuffle = True
        ret.enemy_shuffle = True

    # end of legacy block

    ret.enemy_damage = {None: 'default',
                        'default': 'default',
                        'shuffled': 'shuffled',
                        'random': 'chaos'
                        }[get_choice('enemy_damage', weights)]

    ret.enemy_health = get_choice('enemy_health', weights)

    ret.shufflepots = get_choice('pot_shuffle', weights)

    ret.beemizer = int(get_choice('beemizer', weights, 0))

    ret.timer = {'none': False,
                 None: False,
                 False: False,
                 'timed': 'timed',
                 'timed_ohko': 'timed-ohko',
                 'ohko': 'ohko',
                 'timed_countdown': 'timed-countdown',
                 'display': 'display'}[get_choice('timer', weights, False)]

    ret.countdown_start_time = int(get_choice('countdown_start_time', weights, 10))
    ret.red_clock_time = int(get_choice('red_clock_time', weights, -2))
    ret.blue_clock_time = int(get_choice('blue_clock_time', weights, 2))
    ret.green_clock_time = int(get_choice('green_clock_time', weights, 4))

    ret.dungeon_counters = get_choice('dungeon_counters', weights, 'default')

    ret.progressive = convert_to_on_off(get_choice('progressive', weights, 'on'))

    ret.shuffle_prizes = get_choice('shuffle_prizes', weights, "g")

    ret.required_medallions = (get_choice("misery_mire_medallion", weights, "random"),
                               get_choice("turtle_rock_medallion", weights, "random"))
    for medallion in ret.required_medallions:
        if medallion not in {"random", "Ether", "Bombos", "Quake"}:
            raise Exception(f"unknown Medallion {medallion}")
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

    ret.glitch_boots = get_choice('glitch_boots', weights, True)

    ret.remote_items = get_choice('remote_items', weights, False)

    if get_choice("local_keys", weights, "l" in dungeon_items):
        # () important for ordering of commands, without them the Big Keys section is part of the Small Key else
        ret.local_items = (item_name_groups["Small Keys"] if ret.keyshuffle else set()) \
                          | item_name_groups["Big Keys"] if ret.bigkeyshuffle else set()
    else:
        ret.local_items = set()
    for item_name in weights.get('local_items', []):
        items = item_name_groups.get(item_name, {item_name})
        for item in items:
            if item in item_table:
                ret.local_items.add(item)
            else:
                raise Exception(f"Could not force item {item} to be world-local, as it was not recognized.")

    ret.local_items = ",".join(ret.local_items)

    ret.non_local_items = set()
    for item_name in weights.get('non_local_items', []):
        items = item_name_groups.get(item_name, {item_name})
        for item in items:
            if item in item_table:
                ret.non_local_items.add(item)
            else:
                raise Exception(f"Could not force item {item} to be world-non-local, as it was not recognized.")

    ret.non_local_items = ",".join(ret.non_local_items)

    ret.plando_items = []
    if "items" in plando_options:

        def add_plando_item(item: str, location: str):
            if item not in item_table:
                raise Exception(f"Could not plando item {item} as the item was not recognized")
            if location not in location_table and location not in key_drop_data:
                raise Exception(f"Could not plando item {item} at location {location} as the location was not recognized")
            ret.plando_items.append(PlandoItem(item, location, location_world, from_pool, force))

        options = weights.get("plando_items", [])
        for placement in options:
            if roll_percentage(get_choice("percentage", placement, 100)):
                from_pool = get_choice("from_pool", placement, PlandoItem.from_pool)
                location_world = get_choice("world", placement, PlandoItem.world)
                force = str(get_choice("force", placement, PlandoItem.force)).lower()
                if "items" in placement and "locations" in placement:
                    items = placement["items"]
                    locations = placement["locations"]
                    if isinstance(items, dict):
                        item_list = []
                        for key, value in items.items():
                            item_list += [key] * value
                        items = item_list
                    if not items or not locations:
                        raise Exception("You must specify at least one item and one location to place items.")
                    random.shuffle(items)
                    random.shuffle(locations)
                    for item, location in zip(items, locations):
                        add_plando_item(item, location)
                else:
                    item = get_choice("item", placement, get_choice("items", placement))
                    location = get_choice("location", placement)
                    add_plando_item(item, location)

    ret.plando_texts = {}
    if "texts" in plando_options:
        tt = TextTable()
        tt.removeUnwantedText()
        options = weights.get("plando_texts", [])
        for placement in options:
            if roll_percentage(get_choice("percentage", placement, 100)):
                at = str(get_choice("at", placement))
                if at not in tt:
                    raise Exception(f"No text target \"{at}\" found.")
                ret.plando_texts[at] = str(get_choice("text", placement))

    ret.plando_connections = []
    if "connections" in plando_options:
        options = weights.get("plando_connections", [])
        for placement in options:
            if roll_percentage(get_choice("percentage", placement, 100)):
                ret.plando_connections.append(PlandoConnection(
                    get_choice("entrance", placement),
                    get_choice("exit", placement),
                    get_choice("direction", placement, "both")
                ))

    if 'rom' in weights:
        romweights = weights['rom']

        ret.sprite_pool = romweights['sprite_pool'] if 'sprite_pool' in romweights else []
        ret.sprite = get_choice('sprite', romweights, "Link")
        if 'random_sprite_on_event' in romweights:
            randomoneventweights = romweights['random_sprite_on_event']
            if get_choice('enabled', randomoneventweights, False):
                ret.sprite = 'randomon'
                ret.sprite += '-hit' if get_choice('on_hit', randomoneventweights, True) else ''
                ret.sprite += '-enter' if get_choice('on_enter', randomoneventweights, False) else ''
                ret.sprite += '-exit' if get_choice('on_exit', randomoneventweights, False) else ''
                ret.sprite += '-slash' if get_choice('on_slash', randomoneventweights, False) else ''
                ret.sprite += '-item' if get_choice('on_item', randomoneventweights, False) else ''
                ret.sprite += '-bonk' if get_choice('on_bonk', randomoneventweights, False) else ''
                ret.sprite = 'randomonall' if get_choice('on_everything', randomoneventweights, False) else ret.sprite
                ret.sprite = 'randomonnone' if ret.sprite == 'randomon' else ret.sprite

                if (not ret.sprite_pool or get_choice('use_weighted_sprite_pool', randomoneventweights, False)) \
                        and 'sprite' in romweights:  # Use sprite as a weighted sprite pool, if a sprite pool is not already defined.
                    for key, value in romweights['sprite'].items():
                        if key.startswith('random'):
                            ret.sprite_pool += ['random'] * int(value)
                        else:
                            ret.sprite_pool += [key] * int(value)

        ret.disablemusic = get_choice('disablemusic', romweights, False)
        ret.quickswap = get_choice('quickswap', romweights, True)
        ret.fastmenu = get_choice('menuspeed', romweights, "normal")
        ret.heartcolor = get_choice('heartcolor', romweights, "red")
        ret.heartbeep = convert_to_on_off(get_choice('heartbeep', romweights, "normal"))
        ret.ow_palettes = get_choice('ow_palettes', romweights, "default")
        ret.uw_palettes = get_choice('uw_palettes', romweights, "default")
        ret.hud_palettes = get_choice('hud_palettes', romweights, "default")
        ret.sword_palettes = get_choice('sword_palettes', romweights, "default")
        ret.shield_palettes = get_choice('shield_palettes', romweights, "default")
        ret.link_palettes = get_choice('link_palettes', romweights, "default")

    else:
        ret.quickswap = True
        ret.sprite = "Link"
    return ret


if __name__ == '__main__':
    main()
