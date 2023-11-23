from __future__ import annotations

import argparse
import logging
import os
import random
import string
import urllib.parse
import urllib.request
from collections import Counter
from typing import Any, Dict, Tuple, Union

import ModuleUpdate

ModuleUpdate.update()

import copy
import Utils
import Options
from BaseClasses import seeddigits, get_seed, PlandoOptions
from Main import main as ERmain
from settings import get_settings
from Utils import parse_yamls, version_tuple, __version__, tuplize_version
from worlds.alttp import Options as LttPOptions
from worlds.alttp.EntranceRandomizer import parse_arguments
from worlds.alttp.Text import TextTable
from worlds.AutoWorld import AutoWorldRegister
from worlds.generic import PlandoConnection


def mystery_argparse():
    options = get_settings()
    defaults = options.generator

    parser = argparse.ArgumentParser(description="CMD Generation Interface, defaults come from host.yaml.")
    parser.add_argument('--weights_file_path', default=defaults.weights_file_path,
                        help='Path to the weights file to use for rolling game settings, urls are also valid')
    parser.add_argument('--samesettings', help='Rolls settings per weights file rather than per player',
                        action='store_true')
    parser.add_argument('--player_files_path', default=defaults.player_files_path,
                        help="Input directory for player files.")
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--multi', default=defaults.players, type=lambda value: max(int(value), 1))
    parser.add_argument('--spoiler', type=int, default=defaults.spoiler)
    parser.add_argument('--outputpath', default=options.general_options.output_path,
                        help="Path to output folder. Absolute or relative to cwd.")  # absolute or relative to cwd
    parser.add_argument('--race', action='store_true', default=defaults.race)
    parser.add_argument('--meta_file_path', default=defaults.meta_file_path)
    parser.add_argument('--log_level', default='info', help='Sets log level')
    parser.add_argument('--yaml_output', default=0, type=lambda value: max(int(value), 0),
                        help='Output rolled mystery results to yaml up to specified number (made for async multiworld)')
    parser.add_argument('--plando', default=defaults.plando_options,
                        help='List of options that can be set manually. Can be combined, for example "bosses, items"')
    parser.add_argument("--skip_prog_balancing", action="store_true",
                        help="Skip progression balancing step during generation.")
    parser.add_argument("--skip_output", action="store_true",
                        help="Skips generation assertion and output stages and skips multidata and spoiler output. "
                             "Intended for debugging and testing purposes.")
    args = parser.parse_args()
    if not os.path.isabs(args.weights_file_path):
        args.weights_file_path = os.path.join(args.player_files_path, args.weights_file_path)
    if not os.path.isabs(args.meta_file_path):
        args.meta_file_path = os.path.join(args.player_files_path, args.meta_file_path)
    args.plando: PlandoOptions = PlandoOptions.from_option_string(args.plando)
    return args, options


def get_seed_name(random_source) -> str:
    return f"{random_source.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits)


def main(args=None, callback=ERmain):
    if not args:
        args, options = mystery_argparse()
    else:
        options = get_settings()

    seed = get_seed(args.seed)
    Utils.init_logging(f"Generate_{seed}", loglevel=args.log_level)
    random.seed(seed)
    seed_name = get_seed_name(random)

    if args.race:
        logging.info("Race mode enabled. Using non-deterministic random source.")
        random.seed()  # reset to time-based random source

    weights_cache: Dict[str, Tuple[Any, ...]] = {}
    if args.weights_file_path and os.path.exists(args.weights_file_path):
        try:
            weights_cache[args.weights_file_path] = read_weights_yamls(args.weights_file_path)
        except Exception as e:
            raise ValueError(f"File {args.weights_file_path} is invalid. Please fix your yaml.") from e
        logging.info(f"Weights: {args.weights_file_path} >> "
                     f"{get_choice('description', weights_cache[args.weights_file_path][-1], 'No description specified')}")

    if args.meta_file_path and os.path.exists(args.meta_file_path):
        try:
            meta_weights = read_weights_yamls(args.meta_file_path)[-1]
        except Exception as e:
            raise ValueError(f"File {args.meta_file_path} is invalid. Please fix your yaml.") from e
        logging.info(f"Meta: {args.meta_file_path} >> {get_choice('meta_description', meta_weights)}")
        try:  # meta description allows us to verify that the file named meta.yaml is intentionally a meta file
            del(meta_weights["meta_description"])
        except Exception as e:
            raise ValueError("No meta description found for meta.yaml. Unable to verify.") from e
        if args.samesettings:
            raise Exception("Cannot mix --samesettings with --meta")
    else:
        meta_weights = None
    player_id = 1
    player_files = {}
    for file in os.scandir(args.player_files_path):
        fname = file.name
        if file.is_file() and not fname.startswith(".") and \
                os.path.join(args.player_files_path, fname) not in {args.meta_file_path, args.weights_file_path}:
            path = os.path.join(args.player_files_path, fname)
            try:
                weights_cache[fname] = read_weights_yamls(path)
            except Exception as e:
                raise ValueError(f"File {fname} is invalid. Please fix your yaml.") from e

    # sort dict for consistent results across platforms:
    weights_cache = {key: value for key, value in sorted(weights_cache.items())}
    for filename, yaml_data in weights_cache.items():
        if filename not in {args.meta_file_path, args.weights_file_path}:
            for yaml in yaml_data:
                logging.info(f"P{player_id} Weights: {filename} >> "
                             f"{get_choice('description', yaml, 'No description specified')}")
                player_files[player_id] = filename
                player_id += 1

    args.multi = max(player_id - 1, args.multi)

    if args.multi == 0:
        raise ValueError(
            "No individual player files found and number of players is 0. "
            "Provide individual player files or specify the number of players via host.yaml or --multi."
        )

    logging.info(f"Generating for {args.multi} player{'s' if args.multi > 1 else ''}, "
                 f"{seed_name} Seed {seed} with plando: {args.plando}")

    if not weights_cache:
        raise Exception(f"No weights found. "
                        f"Provide a general weights file ({args.weights_file_path}) or individual player files. "
                        f"A mix is also permitted.")
    erargs = parse_arguments(['--multi', str(args.multi)])
    erargs.seed = seed
    erargs.plando_options = args.plando
    erargs.glitch_triforce = options.generator.glitch_triforce_room
    erargs.spoiler = args.spoiler
    erargs.race = args.race
    erargs.outputname = seed_name
    erargs.outputpath = args.outputpath
    erargs.skip_prog_balancing = args.skip_prog_balancing
    erargs.skip_output = args.skip_output

    settings_cache: Dict[str, Tuple[argparse.Namespace, ...]] = \
        {fname: (tuple(roll_settings(yaml, args.plando) for yaml in yamls) if args.samesettings else None)
         for fname, yamls in weights_cache.items()}

    if meta_weights:
        for category_name, category_dict in meta_weights.items():
            for key in category_dict:
                option = roll_meta_option(key, category_name, category_dict)
                if option is not None:
                    for path in weights_cache:
                        for yaml in weights_cache[path]:
                            if category_name is None:
                                for category in yaml:
                                    if category in AutoWorldRegister.world_types and \
                                            key in Options.CommonOptions.type_hints:
                                        yaml[category][key] = option
                            elif category_name not in yaml:
                                logging.warning(f"Meta: Category {category_name} is not present in {path}.")
                            else:
                                yaml[category_name][key] = option

    player_path_cache = {}
    for player in range(1, args.multi + 1):
        player_path_cache[player] = player_files.get(player, args.weights_file_path)
    name_counter = Counter()
    erargs.player_options = {}

    player = 1
    while player <= args.multi:
        path = player_path_cache[player]
        if path:
            try:
                settings: Tuple[argparse.Namespace, ...] = settings_cache[path] if settings_cache[path] else \
                    tuple(roll_settings(yaml, args.plando) for yaml in weights_cache[path])
                for settingsObject in settings:
                    for k, v in vars(settingsObject).items():
                        if v is not None:
                            try:
                                getattr(erargs, k)[player] = v
                            except AttributeError:
                                setattr(erargs, k, {player: v})
                            except Exception as e:
                                raise Exception(f"Error setting {k} to {v} for player {player}") from e

                    if path == args.weights_file_path:  # if name came from the weights file, just use base player name
                        erargs.name[player] = f"Player{player}"
                    elif not erargs.name[player]:  # if name was not specified, generate it from filename
                        erargs.name[player] = os.path.splitext(os.path.split(path)[-1])[0]
                    erargs.name[player] = handle_name(erargs.name[player], player, name_counter)

                    player += 1
            except Exception as e:
                raise ValueError(f"File {path} is invalid. Please fix your yaml.") from e
        else:
            raise RuntimeError(f'No weights specified for player {player}')

    if len(set(name.lower() for name in erargs.name.values())) != len(erargs.name):
        raise Exception(f"Names have to be unique. Names: {Counter(name.lower() for name in erargs.name.values())}")

    if args.yaml_output:
        import yaml
        important = {}
        for option, player_settings in vars(erargs).items():
            if type(player_settings) == dict:
                if all(type(value) != list for value in player_settings.values()):
                    if len(player_settings.values()) > 1:
                        important[option] = {player: value for player, value in player_settings.items() if
                                             player <= args.yaml_output}
                    else:
                        logging.debug(f"No player settings defined for option '{option}'")

            else:
                if player_settings != "":  # is not empty name
                    important[option] = player_settings
                else:
                    logging.debug(f"No player settings defined for option '{option}'")
        if args.outputpath:
            os.makedirs(args.outputpath, exist_ok=True)
        with open(os.path.join(args.outputpath if args.outputpath else ".", f"generate_{seed_name}.yaml"), "wt") as f:
            yaml.dump(important, f)

    return callback(erargs, seed)


def read_weights_yamls(path) -> Tuple[Any, ...]:
    try:
        if urllib.parse.urlparse(path).scheme in ('https', 'file'):
            yaml = str(urllib.request.urlopen(path).read(), "utf-8-sig")
        else:
            with open(path, 'rb') as f:
                yaml = str(f.read(), "utf-8-sig")
    except Exception as e:
        raise Exception(f"Failed to read weights ({path})") from e

    return tuple(parse_yamls(yaml))


def interpret_on_off(value) -> bool:
    return {"on": True, "off": False}.get(value, value)


def convert_to_on_off(value) -> str:
    return {True: "on", False: "off"}.get(value, value)


def get_choice_legacy(option, root, value=None) -> Any:
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


def get_choice(option, root, value=None) -> Any:
    if option not in root:
        return value
    if type(root[option]) is list:
        return random.choices(root[option])[0]
    if type(root[option]) is not dict:
        return root[option]
    if not root[option]:
        return value
    if any(root[option].values()):
        return random.choices(list(root[option].keys()), weights=list(map(int, root[option].values())))[0]
    raise RuntimeError(f"All options specified in \"{option}\" are weighted as zero.")


class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def handle_name(name: str, player: int, name_counter: Counter):
    name_counter[name.lower()] += 1
    number = name_counter[name.lower()]
    new_name = "%".join([x.replace("%number%", "{number}").replace("%player%", "{player}") for x in name.split("%%")])
    new_name = string.Formatter().vformat(new_name, (), SafeDict(number=number,
                                                                 NUMBER=(number if number > 1 else ''),
                                                                 player=player,
                                                                 PLAYER=(player if player > 1 else '')))
    new_name = new_name.strip()[:16]
    if new_name == "Archipelago":
        raise Exception(f"You cannot name yourself \"{new_name}\"")
    return new_name


def prefer_int(input_data: str) -> Union[str, int]:
    try:
        return int(input_data)
    except:
        return input_data


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


def roll_percentage(percentage: Union[int, float]) -> bool:
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


def roll_meta_option(option_key, game: str, category_dict: Dict) -> Any:
    if not game:
        return get_choice(option_key, category_dict)
    if game in AutoWorldRegister.world_types:
        game_world = AutoWorldRegister.world_types[game]
        options = game_world.options_dataclass.type_hints
        if option_key in options:
            if options[option_key].supports_weighting:
                return get_choice(option_key, category_dict)
            return category_dict[option_key]
    if game == "A Link to the Past":  # TODO wow i hate this
        if option_key in {"glitches_required", "dark_room_logic", "entrance_shuffle", "goals", "triforce_pieces_mode",
                          "triforce_pieces_percentage", "triforce_pieces_available", "triforce_pieces_extra",
                          "triforce_pieces_required", "shop_shuffle", "mode", "item_pool", "item_functionality",
                          "boss_shuffle", "enemy_damage", "enemy_health", "timer", "countdown_start_time",
                          "red_clock_time", "blue_clock_time", "green_clock_time", "dungeon_counters", "shuffle_prizes",
                          "misery_mire_medallion", "turtle_rock_medallion", "sprite_pool", "sprite",
                          "random_sprite_on_event"}:
            return get_choice(option_key, category_dict)
    raise Exception(f"Error generating meta option {option_key} for {game}.")


def roll_linked_options(weights: dict) -> dict:
    weights = copy.deepcopy(weights)  # make sure we don't write back to other weights sets in same_settings
    for option_set in weights["linked_options"]:
        if "name" not in option_set:
            raise ValueError("One of your linked options does not have a name.")
        try:
            if roll_percentage(option_set["percentage"]):
                logging.debug(f"Linked option {option_set['name']} triggered.")
                new_options = option_set["options"]
                for category_name, category_options in new_options.items():
                    currently_targeted_weights = weights
                    if category_name:
                        currently_targeted_weights = currently_targeted_weights[category_name]
                    update_weights(currently_targeted_weights, category_options, "Linked", option_set["name"])
            else:
                logging.debug(f"linked option {option_set['name']} skipped.")
        except Exception as e:
            raise ValueError(f"Linked option {option_set['name']} is invalid. "
                             f"Please fix your linked option.") from e
    return weights


def roll_triggers(weights: dict, triggers: list) -> dict:
    weights = copy.deepcopy(weights)  # make sure we don't write back to other weights sets in same_settings
    weights["_Generator_Version"] = Utils.__version__
    for i, option_set in enumerate(triggers):
        try:
            currently_targeted_weights = weights
            category = option_set.get("option_category", None)
            if category:
                currently_targeted_weights = currently_targeted_weights[category]
            key = get_choice("option_name", option_set)
            if key not in currently_targeted_weights:
                logging.warning(f'Specified option name {option_set["option_name"]} did not '
                                f'match with a root option. '
                                f'This is probably in error.')
            trigger_result = get_choice("option_result", option_set)
            result = get_choice(key, currently_targeted_weights)
            currently_targeted_weights[key] = result
            if result == trigger_result and roll_percentage(get_choice("percentage", option_set, 100)):
                for category_name, category_options in option_set["options"].items():
                    currently_targeted_weights = weights
                    if category_name:
                        currently_targeted_weights = currently_targeted_weights[category_name]
                    update_weights(currently_targeted_weights, category_options, "Triggered", option_set["option_name"])

        except Exception as e:
            raise ValueError(f"Your trigger number {i + 1} is invalid. "
                             f"Please fix your triggers.") from e
    return weights


def handle_option(ret: argparse.Namespace, game_weights: dict, option_key: str, option: type(Options.Option), plando_options: PlandoOptions):
    if option_key in game_weights:
        try:
            if not option.supports_weighting:
                player_option = option.from_any(game_weights[option_key])
            else:
                player_option = option.from_any(get_choice(option_key, game_weights))
            setattr(ret, option_key, player_option)
        except Exception as e:
            raise Exception(f"Error generating option {option_key} in {ret.game}") from e
        else:
            player_option.verify(AutoWorldRegister.world_types[ret.game], ret.name, plando_options)
    else:
        setattr(ret, option_key, option.from_any(option.default))  # call the from_any here to support default "random"


def roll_settings(weights: dict, plando_options: PlandoOptions = PlandoOptions.bosses):
    if "linked_options" in weights:
        weights = roll_linked_options(weights)

    if "triggers" in weights:
        weights = roll_triggers(weights, weights["triggers"])

    requirements = weights.get("requires", {})
    if requirements:
        version = requirements.get("version", __version__)
        if tuplize_version(version) > version_tuple:
            raise Exception(f"Settings reports required version of generator is at least {version}, "
                            f"however generator is of version {__version__}")
        required_plando_options = PlandoOptions.from_option_string(requirements.get("plando", ""))
        if required_plando_options not in plando_options:
            if required_plando_options:
                raise Exception(f"Settings reports required plando module {str(required_plando_options)}, "
                                f"which is not enabled.")

    ret = argparse.Namespace()
    for option_key in Options.PerGameCommonOptions.type_hints:
        if option_key in weights and option_key not in Options.CommonOptions.type_hints:
            raise Exception(f"Option {option_key} has to be in a game's section, not on its own.")

    ret.game = get_choice("game", weights)
    if ret.game not in AutoWorldRegister.world_types:
        picks = Utils.get_fuzzy_results(ret.game, AutoWorldRegister.world_types, limit=1)[0]
        raise Exception(f"No world found to handle game {ret.game}. Did you mean '{picks[0]}' ({picks[1]}% sure)? "
                        f"Check your spelling or installation of that world.")

    if ret.game not in weights:
        raise Exception(f"No game options for selected game \"{ret.game}\" found.")

    world_type = AutoWorldRegister.world_types[ret.game]
    game_weights = weights[ret.game]

    if "triggers" in game_weights:
        weights = roll_triggers(weights, game_weights["triggers"])
        game_weights = weights[ret.game]

    ret.name = get_choice('name', weights)
    for option_key, option in Options.CommonOptions.type_hints.items():
        setattr(ret, option_key, option.from_any(get_choice(option_key, weights, option.default)))

    for option_key, option in world_type.options_dataclass.type_hints.items():
        handle_option(ret, game_weights, option_key, option, plando_options)
    if PlandoOptions.items in plando_options:
        ret.plando_items = game_weights.get("plando_items", [])
    if ret.game == "Minecraft" or ret.game == "Ocarina of Time":
        # bad hardcoded behavior to make this work for now
        ret.plando_connections = []
        if PlandoOptions.connections in plando_options:
            options = game_weights.get("plando_connections", [])
            for placement in options:
                if roll_percentage(get_choice("percentage", placement, 100)):
                    ret.plando_connections.append(PlandoConnection(
                        get_choice("entrance", placement),
                        get_choice("exit", placement),
                        get_choice("direction", placement)
                    ))
    elif ret.game == "A Link to the Past":
        roll_alttp_settings(ret, game_weights, plando_options)

    return ret


def roll_alttp_settings(ret: argparse.Namespace, weights, plando_options):
    if "dungeon_items" in weights and get_choice_legacy('dungeon_items', weights, "none") != "none":
        raise Exception(f"dungeon_items key in A Link to the Past was removed, but is present in these weights as {get_choice_legacy('dungeon_items', weights, False)}.")
    glitches_required = get_choice_legacy('glitches_required', weights)
    if glitches_required not in [None, 'none', 'no_logic', 'overworld_glitches', 'hybrid_major_glitches', 'minor_glitches']:
        logging.warning("Only NMG, OWG, HMG and No Logic supported")
        glitches_required = 'none'
    ret.logic = {None: 'noglitches', 'none': 'noglitches', 'no_logic': 'nologic', 'overworld_glitches': 'owglitches',
                 'minor_glitches': 'minorglitches', 'hybrid_major_glitches': 'hybridglitches'}[
        glitches_required]

    ret.dark_room_logic = get_choice_legacy("dark_room_logic", weights, "lamp")
    if not ret.dark_room_logic:  # None/False
        ret.dark_room_logic = "none"
    if ret.dark_room_logic == "sconces":
        ret.dark_room_logic = "torches"
    if ret.dark_room_logic not in {"lamp", "torches", "none"}:
        raise ValueError(f"Unknown Dark Room Logic: \"{ret.dark_room_logic}\"")

    entrance_shuffle = get_choice_legacy('entrance_shuffle', weights, 'vanilla')
    if entrance_shuffle.startswith('none-'):
        ret.shuffle = 'vanilla'
    else:
        ret.shuffle = entrance_shuffle if entrance_shuffle != 'none' else 'vanilla'

    goal = get_choice_legacy('goals', weights, 'ganon')

    ret.goal = goals[goal]


    extra_pieces = get_choice_legacy('triforce_pieces_mode', weights, 'available')

    ret.triforce_pieces_required = LttPOptions.TriforcePieces.from_any(get_choice_legacy('triforce_pieces_required', weights, 20))

    # sum a percentage to required
    if extra_pieces == 'percentage':
        percentage = max(100, float(get_choice_legacy('triforce_pieces_percentage', weights, 150))) / 100
        ret.triforce_pieces_available = int(round(ret.triforce_pieces_required * percentage, 0))
    # vanilla mode (specify how many pieces are)
    elif extra_pieces == 'available':
        ret.triforce_pieces_available = LttPOptions.TriforcePieces.from_any(
            get_choice_legacy('triforce_pieces_available', weights, 30))
    # required pieces + fixed extra
    elif extra_pieces == 'extra':
        extra_pieces = max(0, int(get_choice_legacy('triforce_pieces_extra', weights, 10)))
        ret.triforce_pieces_available = ret.triforce_pieces_required + extra_pieces

    # change minimum to required pieces to avoid problems
    ret.triforce_pieces_available = min(max(ret.triforce_pieces_required, int(ret.triforce_pieces_available)), 90)

    ret.shop_shuffle = get_choice_legacy('shop_shuffle', weights, '')
    if not ret.shop_shuffle:
        ret.shop_shuffle = ''

    ret.mode = get_choice_legacy("mode", weights)

    ret.difficulty = get_choice_legacy('item_pool', weights)

    ret.item_functionality = get_choice_legacy('item_functionality', weights)


    ret.enemy_damage = {None: 'default',
                        'default': 'default',
                        'shuffled': 'shuffled',
                        'random': 'chaos', # to be removed
                        'chaos': 'chaos',
                        }[get_choice_legacy('enemy_damage', weights)]

    ret.enemy_health = get_choice_legacy('enemy_health', weights)

    ret.timer = {'none': False,
                 None: False,
                 False: False,
                 'timed': 'timed',
                 'timed_ohko': 'timed-ohko',
                 'ohko': 'ohko',
                 'timed_countdown': 'timed-countdown',
                 'display': 'display'}[get_choice_legacy('timer', weights, False)]

    ret.countdown_start_time = int(get_choice_legacy('countdown_start_time', weights, 10))
    ret.red_clock_time = int(get_choice_legacy('red_clock_time', weights, -2))
    ret.blue_clock_time = int(get_choice_legacy('blue_clock_time', weights, 2))
    ret.green_clock_time = int(get_choice_legacy('green_clock_time', weights, 4))

    ret.dungeon_counters = get_choice_legacy('dungeon_counters', weights, 'default')

    ret.shuffle_prizes = get_choice_legacy('shuffle_prizes', weights, "g")

    ret.required_medallions = [get_choice_legacy("misery_mire_medallion", weights, "random"),
                               get_choice_legacy("turtle_rock_medallion", weights, "random")]

    for index, medallion in enumerate(ret.required_medallions):
        ret.required_medallions[index] = {"ether": "Ether", "quake": "Quake", "bombos": "Bombos", "random": "random"} \
            .get(medallion.lower(), None)
        if not ret.required_medallions[index]:
            raise Exception(f"unknown Medallion {medallion} for {'misery mire' if index == 0 else 'turtle rock'}")

    ret.plando_texts = {}
    if PlandoOptions.texts in plando_options:
        tt = TextTable()
        tt.removeUnwantedText()
        options = weights.get("plando_texts", [])
        for placement in options:
            if roll_percentage(get_choice_legacy("percentage", placement, 100)):
                at = str(get_choice_legacy("at", placement))
                if at not in tt:
                    raise Exception(f"No text target \"{at}\" found.")
                ret.plando_texts[at] = str(get_choice_legacy("text", placement))

    ret.plando_connections = []
    if PlandoOptions.connections in plando_options:
        options = weights.get("plando_connections", [])
        for placement in options:
            if roll_percentage(get_choice_legacy("percentage", placement, 100)):
                ret.plando_connections.append(PlandoConnection(
                    get_choice_legacy("entrance", placement),
                    get_choice_legacy("exit", placement),
                    get_choice_legacy("direction", placement, "both")
                ))

    ret.sprite_pool = weights.get('sprite_pool', [])
    ret.sprite = get_choice_legacy('sprite', weights, "Link")
    if 'random_sprite_on_event' in weights:
        randomoneventweights = weights['random_sprite_on_event']
        if get_choice_legacy('enabled', randomoneventweights, False):
            ret.sprite = 'randomon'
            ret.sprite += '-hit' if get_choice_legacy('on_hit', randomoneventweights, True) else ''
            ret.sprite += '-enter' if get_choice_legacy('on_enter', randomoneventweights, False) else ''
            ret.sprite += '-exit' if get_choice_legacy('on_exit', randomoneventweights, False) else ''
            ret.sprite += '-slash' if get_choice_legacy('on_slash', randomoneventweights, False) else ''
            ret.sprite += '-item' if get_choice_legacy('on_item', randomoneventweights, False) else ''
            ret.sprite += '-bonk' if get_choice_legacy('on_bonk', randomoneventweights, False) else ''
            ret.sprite = 'randomonall' if get_choice_legacy('on_everything', randomoneventweights, False) else ret.sprite
            ret.sprite = 'randomonnone' if ret.sprite == 'randomon' else ret.sprite

            if (not ret.sprite_pool or get_choice_legacy('use_weighted_sprite_pool', randomoneventweights, False)) \
                    and 'sprite' in weights:  # Use sprite as a weighted sprite pool, if a sprite pool is not already defined.
                for key, value in weights['sprite'].items():
                    if key.startswith('random'):
                        ret.sprite_pool += ['random'] * int(value)
                    else:
                        ret.sprite_pool += [key] * int(value)


if __name__ == '__main__':
    import atexit
    confirmation = atexit.register(input, "Press enter to close.")
    multiworld = main()
    if __debug__:
        import gc
        import sys
        import weakref
        weak = weakref.ref(multiworld)
        del multiworld
        gc.collect()  # need to collect to deref all hard references
        assert not weak(), f"MultiWorld object was not de-allocated, it's referenced {sys.getrefcount(weak())} times." \
                           " This would be a memory leak."
    # in case of error-free exit should not need confirmation
    atexit.unregister(confirmation)
