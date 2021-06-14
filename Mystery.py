import argparse
import logging
import random
import urllib.request
import urllib.parse
import typing
import os
from collections import Counter
import string

import ModuleUpdate
from worlds.generic import PlandoItem, PlandoConnection

ModuleUpdate.update()

from Utils import parse_yaml
from worlds.alttp.EntranceRandomizer import parse_arguments
from Main import main as ERmain
from Main import get_seed, seeddigits
import Options
from worlds import lookup_any_item_name_to_id
from worlds.alttp.Items import item_name_groups, item_table
from worlds.alttp import Bosses
from worlds.alttp.Text import TextTable
from worlds.alttp.Regions import location_table, key_drop_data


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
    parser.add_argument('--pre_roll', action='store_true')
    parser.add_argument('--rom')
    parser.add_argument('--enemizercli')
    parser.add_argument('--outputpath')
    parser.add_argument('--glitch_triforce', action='store_true')
    parser.add_argument('--race', action='store_true')
    parser.add_argument('--meta', default=None)
    parser.add_argument('--log_output_path', help='Path to store output log')
    parser.add_argument('--loglevel', default='info', help='Sets log level')
    parser.add_argument('--create_diff', action="store_true")
    parser.add_argument('--yaml_output', default=0, type=lambda value: min(max(int(value), 0), 255),
                        help='Output rolled mystery results to yaml up to specified number (made for async multiworld)')
    parser.add_argument('--plando', default="bosses",
                        help='List of options that can be set manually. Can be combined, for example "bosses, items"')
    parser.add_argument('--seed_name')
    for player in range(1, multiargs.multi + 1):
        parser.add_argument(f'--p{player}', help=argparse.SUPPRESS)
    args = parser.parse_args()
    args.plando: typing.Set[str] = {arg.strip().lower() for arg in args.plando.split(",")}
    return args

def get_seed_name(random):
    return f"{random.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits)

def main(args=None, callback=ERmain):
    if not args:
        args = mystery_argparse()

    seed = get_seed(args.seed)
    random.seed(seed)
    seed_name = args.seed_name if args.seed_name else get_seed_name(random)
    print(f"Generating for {args.multi} player{'s' if args.multi > 1 else ''}, {seed_name} Seed {seed}")

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
    erargs.glitch_triforce = args.glitch_triforce
    erargs.race = args.race
    erargs.skip_playthrough = args.skip_playthrough
    erargs.outputname = seed_name
    erargs.outputpath = args.outputpath
    erargs.teams = args.teams

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

    name_counter = Counter()
    erargs.player_settings = {}
    for player in range(1, args.multi + 1):
        path = player_path_cache[player]
        if path:
            try:
                settings = settings_cache[path] if settings_cache[path] else \
                    roll_settings(weights_cache[path], args.plando)
                if args.pre_roll:
                    import yaml
                    if path == args.weights:
                        settings.name = f"Player{player}"
                    elif not settings.name:
                        settings.name = os.path.splitext(os.path.split(path)[-1])[0]

                    if "-" not in settings.shuffle and settings.shuffle != "vanilla":
                        settings.shuffle += f"-{random.randint(0, 2 ** 64)}"

                    pre_rolled = dict()
                    pre_rolled["original_seed_number"] = seed
                    pre_rolled["original_seed_name"] = seed_name
                    pre_rolled["pre_rolled"] = vars(settings).copy()
                    if "plando_items" in pre_rolled["pre_rolled"]:
                        pre_rolled["pre_rolled"]["plando_items"] = [item.to_dict() for item in
                                                                    pre_rolled["pre_rolled"]["plando_items"]]
                    if "plando_connections" in pre_rolled["pre_rolled"]:
                        pre_rolled["pre_rolled"]["plando_connections"] = [connection.to_dict() for connection in
                                                                          pre_rolled["pre_rolled"][
                                                                              "plando_connections"]]

                    with open(os.path.join(args.outputpath if args.outputpath else ".",
                                           f"{os.path.split(path)[-1].split('.')[0]}_pre_rolled.yaml"), "wt") as f:
                        yaml.dump(pre_rolled, f)
                for k, v in vars(settings).items():
                    if v is not None:
                        try:
                            getattr(erargs, k)[player] = v
                        except AttributeError:
                            setattr(erargs, k, {player: v})
            except Exception as e:
                raise ValueError(f"File {path} is destroyed. Please fix your yaml.") from e
        else:
            raise RuntimeError(f'No weights specified for player {player}')
        if path == args.weights:  # if name came from the weights file, just use base player name
            erargs.name[player] = f"Player{player}"
        elif not erargs.name[player]:  # if name was not specified, generate it from filename
            erargs.name[player] = os.path.splitext(os.path.split(path)[-1])[0]
        erargs.name[player] = handle_name(erargs.name[player], player, name_counter)

    erargs.names = ",".join(erargs.name[i] for i in range(1, args.multi + 1))
    del (erargs.name)
    if args.yaml_output:
        import yaml
        important = {}
        for option, player_settings in vars(erargs).items():
            if type(player_settings) == dict:
                if all(type(value) != list for value in player_settings.values()):
                    if len(player_settings.values()) > 1:
                        important[option] = {player: value for player, value in player_settings.items() if
                                             player <= args.yaml_output}
                    elif len(player_settings.values()) > 0:
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


class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def handle_name(name: str, player: int, name_counter: Counter):
    name_counter[name] += 1
    new_name = "%".join([x.replace("%number%", "{number}").replace("%player%", "{player}") for x in name.split("%%")])
    new_name = string.Formatter().vformat(new_name, (), SafeDict(number=name_counter[name],
                                                                 NUMBER=(name_counter[name] if name_counter[
                                                                                                   name] > 1 else ''),
                                                                 player=player,
                                                                 PLAYER=(player if player > 1 else '')))
    new_name = new_name.strip().replace(' ', '_')[:16]
    if new_name == "Archipelago":
        raise Exception(f"You cannot name yourself \"{new_name}\"")
    return new_name


def prefer_int(input_data: str) -> typing.Union[str, int]:
    try:
        return int(input_data)
    except:
        return input_data


available_boss_names: typing.Set[str] = {boss.lower() for boss in Bosses.boss_table if boss not in
                                         {'Agahnim', 'Agahnim2', 'Ganon'}}
available_boss_locations: typing.Set[str] = {f"{loc.lower()}{f' {level}' if level else ''}" for loc, level in
                                             Bosses.boss_location_table}

boss_shuffle_options = {None: 'none',
                        'none': 'none',
                        'basic': 'basic',
                        'full': 'full',
                        'chaos': 'chaos',
                        'singularity': 'singularity'
                        }

goals = {
    'ganon': 'ganon',
    'crystals': 'crystals',
    'bosses': 'bosses',
    'pedestal': 'pedestal',
    'ganon_pedestal': 'ganonpedestal',
    'triforce_hunt': 'triforcehunt',
    'local_triforce_hunt': 'localtriforcehunt',
    'ganon_triforce_hunt': 'ganontriforcehunt',
    'local_ganon_triforce_hunt': 'localganontriforcehunt',
    'ice_rod_hunt': 'icerodhunt',
}

# remove sometime before 1.0.0, warn before
legacy_boss_shuffle_options = {
    # legacy, will go away:
    'simple': 'basic',
    'random': 'full',
    'normal': 'full'
}

legacy_goals = {
    'dungeons': 'bosses',
    'fast_ganon': 'crystals',
}


def roll_percentage(percentage: typing.Union[int, float]) -> bool:
    """Roll a percentage chance.
    percentage is expected to be in range [0, 100]"""
    return random.random() < (float(percentage) / 100)


def update_weights(weights: dict, new_weights: dict, type: str, name: str) -> dict:
    logging.debug(f'Applying {new_weights}')
    new_options = set(new_weights) - set(weights)
    weights.update(new_weights)
    if new_options:
        for new_option in new_options:
            logging.warning(f'{type} Suboption "{new_option}" of "{name}" did not '
                            f'overwrite a root option. '
                            f'This is probably in error.')
    return weights


def roll_linked_options(weights: dict) -> dict:
    weights = weights.copy()  # make sure we don't write back to other weights sets in same_settings
    for option_set in weights["linked_options"]:
        if "name" not in option_set:
            raise ValueError("One of your linked options does not have a name.")
        try:
            if roll_percentage(option_set["percentage"]):
                logging.debug(f"Linked option {option_set['name']} triggered.")
                if "options" in option_set:
                    weights = update_weights(weights, option_set["options"], "Linked", option_set["name"])
                if "rom_options" in option_set:
                    rom_weights = weights.get("rom", dict())
                    rom_weights = update_weights(rom_weights, option_set["rom_options"], "Linked Rom",
                                                 option_set["name"])
                    weights["rom"] = rom_weights
            else:
                logging.debug(f"linked option {option_set['name']} skipped.")
        except Exception as e:
            raise ValueError(f"Linked option {option_set['name']} is destroyed. "
                             f"Please fix your linked option.") from e
    return weights


def roll_triggers(weights: dict) -> dict:
    weights = weights.copy()  # make sure we don't write back to other weights sets in same_settings
    weights["_Generator_Version"] = "Archipelago"  # Some means for triggers to know if the seed is on main or doors.
    for i, option_set in enumerate(weights["triggers"]):
        try:
            key = get_choice("option_name", option_set)
            if key not in weights:
                logging.warning(f'Specified option name {option_set["option_name"]} did not '
                                f'match with a root option. '
                                f'This is probably in error.')
            trigger_result = get_choice("option_result", option_set)
            result = get_choice(key, weights)
            weights[key] = result
            if result == trigger_result and roll_percentage(get_choice("percentage", option_set, 100)):
                if "options" in option_set:
                    weights = update_weights(weights, option_set["options"], "Triggered", option_set["option_name"])

                if "rom_options" in option_set:
                    rom_weights = weights.get("rom", dict())
                    rom_weights = update_weights(rom_weights, option_set["rom_options"], "Triggered Rom",
                                                 option_set["option_name"])
                    weights["rom"] = rom_weights

        except Exception as e:
            raise ValueError(f"Your trigger number {i+1} is destroyed. "
                             f"Please fix your triggers.") from e
    return weights


def get_plando_bosses(boss_shuffle: str, plando_options: typing.Set[str]) -> str:
    if boss_shuffle in legacy_boss_shuffle_options:
        new_boss_shuffle = legacy_boss_shuffle_options[boss_shuffle]
        logging.warning(f"Boss shuffle {boss_shuffle} is deprecated, "
                        f"please use {new_boss_shuffle} instead")
        return new_boss_shuffle
    if boss_shuffle in boss_shuffle_options:
        return boss_shuffle_options[boss_shuffle]
    elif "bosses" in plando_options:
        options = boss_shuffle.lower().split(";")
        remainder_shuffle = "none"  # vanilla
        bosses = []
        for boss in options:
            if boss in legacy_boss_shuffle_options:
                remainder_shuffle = legacy_boss_shuffle_options[boss_shuffle]
                logging.warning(f"Boss shuffle {boss} is deprecated, "
                                f"please use {remainder_shuffle} instead")
            if boss in boss_shuffle_options:
                remainder_shuffle = boss_shuffle_options[boss]
            elif "-" in boss:
                loc, boss_name = boss.split("-")
                if boss_name not in available_boss_names:
                    raise ValueError(f"Unknown Boss name {boss_name}")
                if loc not in available_boss_locations:
                    raise ValueError(f"Unknown Boss Location {loc}")
                level = ''
                if loc.split(" ")[-1] in {"top", "middle", "bottom"}:
                    # split off level
                    loc = loc.split(" ")
                    level = f" {loc[-1]}"
                    loc = " ".join(loc[:-1])
                loc = loc.title().replace("Of", "of")
                if not Bosses.can_place_boss(boss_name.title(), loc, level):
                    raise ValueError(f"Cannot place {boss_name} at {loc}{level}")
                bosses.append(boss)
            elif boss not in available_boss_names:
                raise ValueError(f"Unknown Boss name or Boss shuffle option {boss}.")
            else:
                bosses.append(boss)
        return ";".join(bosses + [remainder_shuffle])
    else:
        raise Exception(f"Boss Shuffle {boss_shuffle} is unknown and boss plando is turned off.")


def roll_settings(weights: dict, plando_options: typing.Set[str] = frozenset(("bosses",))):
    if "pre_rolled" in weights:
        pre_rolled = weights["pre_rolled"]

        if "plando_items" in pre_rolled:
            pre_rolled["plando_items"] = [PlandoItem(item["item"],
                                                     item["location"],
                                                     item["world"],
                                                     item["from_pool"],
                                                     item["force"]) for item in pre_rolled["plando_items"]]
            if "items" not in plando_options and pre_rolled["plando_items"]:
                raise Exception("Item Plando is turned off. Reusing this pre-rolled setting not permitted.")

        if "plando_connections" in pre_rolled:
            pre_rolled["plando_connections"] = [PlandoConnection(connection["entrance"],
                                                                 connection["exit"],
                                                                 connection["direction"]) for connection in
                                                pre_rolled["plando_connections"]]
            if "connections" not in plando_options and pre_rolled["plando_connections"]:
                raise Exception("Connection Plando is turned off. Reusing this pre-rolled setting not permitted.")

        if "bosses" not in plando_options:
            try:
                pre_rolled["shufflebosses"] = get_plando_bosses(pre_rolled["shufflebosses"], plando_options)
            except Exception as ex:
                raise Exception("Boss Plando is turned off. Reusing this pre-rolled setting not permitted.") from ex

        if pre_rolled.get("plando_texts") and "texts" not in plando_options:
            raise Exception("Text Plando is turned off. Reusing this pre-rolled setting not permitted.")

        return argparse.Namespace(**pre_rolled)

    if "linked_options" in weights:
        weights = roll_linked_options(weights)

    if "triggers" in weights:
        weights = roll_triggers(weights)

    ret = argparse.Namespace()
    ret.name = get_choice('name', weights)
    ret.accessibility = get_choice('accessibility', weights)
    ret.progression_balancing = get_choice('progression_balancing', weights, True)
    ret.game = get_choice("game", weights, "A Link to the Past")

    ret.local_items = set()
    for item_name in weights.get('local_items', []):
        items = item_name_groups.get(item_name, {item_name})
        for item in items:
            if item in lookup_any_item_name_to_id:
                ret.local_items.add(item)
            else:
                raise Exception(f"Could not force item {item} to be world-local, as it was not recognized.")

    ret.non_local_items = set()
    for item_name in weights.get('non_local_items', []):
        items = item_name_groups.get(item_name, {item_name})
        for item in items:
            if item in lookup_any_item_name_to_id:
                ret.non_local_items.add(item)
            else:
                raise Exception(f"Could not force item {item} to be world-non-local, as it was not recognized.")

    inventoryweights = weights.get('startinventory', {})
    startitems = []
    for item in inventoryweights.keys():
        itemvalue = get_choice(item, inventoryweights)
        if isinstance(itemvalue, int):
            for i in range(int(itemvalue)):
                startitems.append(item)
        elif itemvalue:
            startitems.append(item)
    ret.startinventory = startitems
    ret.start_hints = set(weights.get('start_hints', []))


    if ret.game == "A Link to the Past":
        roll_alttp_settings(ret, weights, plando_options)
    elif ret.game == "Hollow Knight":
        for option_name, option in Options.hollow_knight_options.items():
            setattr(ret, option_name, option.from_any(get_choice(option_name, weights, True)))
    elif ret.game == "Factorio":
        for option_name, option in Options.factorio_options.items():
            if option_name in weights:
                if issubclass(option, Options.OptionDict):  # get_choice should probably land in the Option class
                    setattr(ret, option_name, option.from_any(weights[option_name]))
                else:
                    setattr(ret, option_name, option.from_any(get_choice(option_name, weights)))
            else:
                setattr(ret, option_name, option(option.default))
    elif ret.game == "Minecraft":
        for option_name, option in Options.minecraft_options.items():
            if option_name in weights:
                setattr(ret, option_name, option.from_any(get_choice(option_name, weights)))
            else:
                setattr(ret, option_name, option(option.default))
        # bad hardcoded behavior to make this work for now    
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
    else:
        raise Exception(f"Unsupported game {ret.game}")
    return ret


def roll_alttp_settings(ret: argparse.Namespace, weights, plando_options):
    for option_name, option in Options.alttp_options.items():
        if option_name in weights:
            setattr(ret, option_name, option.from_any(get_choice(option_name, weights)))
        else:
            setattr(ret, option_name, option(option.default))

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

    entrance_shuffle = get_choice('entrance_shuffle', weights, 'vanilla')
    if entrance_shuffle.startswith('none-'):
        ret.shuffle = 'vanilla'
    else:
        ret.shuffle = entrance_shuffle if entrance_shuffle != 'none' else 'vanilla'

    goal = get_choice('goals', weights, 'ganon')

    if goal in legacy_goals:
        logging.warning(f"Goal {goal} is depcrecated, please use {legacy_goals[goal]} instead.")
        goal = legacy_goals[goal]
    ret.goal = goals[goal]

    # TODO consider moving open_pyramid to an automatic variable in the core roller, set to True when
    # fast ganon + ganon at hole
    ret.open_pyramid = get_choice('open_pyramid', weights, 'goal')

    extra_pieces = get_choice('triforce_pieces_mode', weights, 'available')

    ret.triforce_pieces_required = Options.TriforcePieces.from_any(get_choice('triforce_pieces_required', weights))

    # sum a percentage to required
    if extra_pieces == 'percentage':
        percentage = max(100, float(get_choice('triforce_pieces_percentage', weights, 150))) / 100
        ret.triforce_pieces_available = int(round(ret.triforce_pieces_required * percentage, 0))
    # vanilla mode (specify how many pieces are)
    elif extra_pieces == 'available':
        ret.triforce_pieces_available = Options.TriforcePieces.from_any(get_choice('triforce_pieces_available', weights))
    # required pieces + fixed extra
    elif extra_pieces == 'extra':
        extra_pieces = max(0, int(get_choice('triforce_pieces_extra', weights, 10)))
        ret.triforce_pieces_available = ret.triforce_pieces_required + extra_pieces

    # change minimum to required pieces to avoid problems
    ret.triforce_pieces_available = min(max(ret.triforce_pieces_required, int(ret.triforce_pieces_available)), 90)

    ret.shop_shuffle = get_choice('shop_shuffle', weights, '')
    if not ret.shop_shuffle:
        ret.shop_shuffle = ''

    ret.mode = get_choice("mode", weights)
    ret.retro = get_choice("retro", weights)

    ret.hints = get_choice('hints', weights)

    ret.swordless = get_choice('swordless', weights, False)

    ret.difficulty = get_choice('item_pool', weights)

    ret.item_functionality = get_choice('item_functionality', weights)

    boss_shuffle = get_choice('boss_shuffle', weights)
    ret.shufflebosses = get_plando_bosses(boss_shuffle, plando_options)

    ret.enemy_shuffle = bool(get_choice('enemy_shuffle', weights, False))


    ret.killable_thieves = get_choice('killable_thieves', weights, False)
    ret.tile_shuffle = get_choice('tile_shuffle', weights, False)
    ret.bush_shuffle = get_choice('bush_shuffle', weights, False)

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

    ret.required_medallions = [get_choice("misery_mire_medallion", weights, "random"),
                               get_choice("turtle_rock_medallion", weights, "random")]

    for index, medallion in enumerate(ret.required_medallions):
        ret.required_medallions[index] = {"ether": "Ether", "quake": "Quake", "bombos": "Bombos", "random": "random"} \
            .get(medallion.lower(), None)
        if not ret.required_medallions[index]:
            raise Exception(f"unknown Medallion {medallion} for {'misery mire' if index == 0 else 'turtle rock'}")

    ret.glitch_boots = get_choice('glitch_boots', weights, True)

    if get_choice("local_keys", weights, "l" in dungeon_items):
        # () important for ordering of commands, without them the Big Keys section is part of the Small Key else
        ret.local_items |= item_name_groups["Small Keys"] if ret.keyshuffle else set()
        ret.local_items |= item_name_groups["Big Keys"] if ret.bigkeyshuffle else set()

    ret.plando_items = []
    if "items" in plando_options:

        def add_plando_item(item: str, location: str):
            if item not in item_table:
                raise Exception(f"Could not plando item {item} as the item was not recognized")
            if location not in location_table and location not in key_drop_data:
                raise Exception(
                    f"Could not plando item {item} at location {location} as the location was not recognized")
            ret.plando_items.append(PlandoItem(item, location, location_world, from_pool, force))

        options = weights.get("plando_items", [])
        for placement in options:
            if roll_percentage(get_choice("percentage", placement, 100)):
                from_pool = get_choice("from_pool", placement, PlandoItem._field_defaults["from_pool"])
                location_world = get_choice("world", placement, PlandoItem._field_defaults["world"])
                force = str(get_choice("force", placement, PlandoItem._field_defaults["force"])).lower()
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
        ret.triforcehud = get_choice('triforcehud', romweights, 'hide_goal')
        ret.quickswap = get_choice('quickswap', romweights, True)
        ret.fastmenu = get_choice('menuspeed', romweights, "normal")
        ret.reduceflashing = get_choice('reduceflashing', romweights, False)
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


if __name__ == '__main__':
    main()
