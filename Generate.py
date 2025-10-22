from __future__ import annotations

import argparse
import copy
import logging
import os
import random
import string
import sys
import urllib.parse
import urllib.request
from collections import Counter
from itertools import chain
from typing import Any

import ModuleUpdate

ModuleUpdate.update()

import Utils
import Options
from BaseClasses import seeddigits, get_seed, PlandoOptions
from Utils import parse_yamls, version_tuple, __version__, tuplize_version


def mystery_argparse(argv: list[str] | None = None):
    from settings import get_settings
    settings = get_settings()
    defaults = settings.generator

    parser = argparse.ArgumentParser(description="CMD Generation Interface, defaults come from host.yaml.")
    parser.add_argument('--weights_file_path', default=defaults.weights_file_path,
                        help='Path to the weights file to use for rolling game options, urls are also valid')
    parser.add_argument('--sameoptions', help='Rolls options per weights file rather than per player',
                        action='store_true')
    parser.add_argument('--player_files_path', default=defaults.player_files_path,
                        help="Input directory for player files.")
    parser.add_argument('--seed', help='Define seed number to generate.', type=int)
    parser.add_argument('--multi', default=defaults.players, type=lambda value: max(int(value), 1))
    parser.add_argument('--spoiler', type=int, default=defaults.spoiler)
    parser.add_argument('--outputpath', default=settings.general_options.output_path,
                        help="Path to output folder. Absolute or relative to cwd.")  # absolute or relative to cwd
    parser.add_argument('--race', action='store_true', default=defaults.race)
    parser.add_argument('--meta_file_path', default=defaults.meta_file_path)
    parser.add_argument('--log_level', default=defaults.loglevel, help='Sets log level')
    parser.add_argument('--log_time', help="Add timestamps to STDOUT",
                        default=defaults.logtime, action='store_true')
    parser.add_argument("--csv_output", action="store_true",
                        help="Output rolled player options to csv (made for async multiworld).")
    parser.add_argument("--plando", default=defaults.plando_options,
                        help="List of options that can be set manually. Can be combined, for example \"bosses, items\"")
    parser.add_argument("--skip_prog_balancing", action="store_true",
                        help="Skip progression balancing step during generation.")
    parser.add_argument("--skip_output", action="store_true",
                        help="Skips generation assertion and output stages and skips multidata and spoiler output. "
                             "Intended for debugging and testing purposes.")
    parser.add_argument("--spoiler_only", action="store_true",
                        help="Skips generation assertion and multidata, outputting only a spoiler log. "
                             "Intended for debugging and testing purposes.")
    args = parser.parse_args(argv)

    if args.skip_output and args.spoiler_only:
        parser.error("Cannot mix --skip_output and --spoiler_only")
    elif args.spoiler == 0 and args.spoiler_only:
        parser.error("Cannot use --spoiler_only when --spoiler=0. Use --skip_output or set --spoiler to a different value")

    if not os.path.isabs(args.weights_file_path):
        args.weights_file_path = os.path.join(args.player_files_path, args.weights_file_path)
    if not os.path.isabs(args.meta_file_path):
        args.meta_file_path = os.path.join(args.player_files_path, args.meta_file_path)
    args.plando: PlandoOptions = PlandoOptions.from_option_string(args.plando)

    return args


def get_seed_name(random_source) -> str:
    return f"{random_source.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits)


def main(args=None) -> tuple[argparse.Namespace, int]:
    # __name__ == "__main__" check so unittests that already imported worlds don't trip this.
    if __name__ == "__main__" and "worlds" in sys.modules:
        raise Exception("Worlds system should not be loaded before logging init.")

    if not args:
        args = mystery_argparse()

    seed = get_seed(args.seed)

    Utils.init_logging(f"Generate_{seed}", loglevel=args.log_level, add_timestamp=args.log_time)
    random.seed(seed)
    seed_name = get_seed_name(random)

    if args.race:
        logging.info("Race mode enabled. Using non-deterministic random source.")
        random.seed()  # reset to time-based random source

    weights_cache: dict[str, tuple[Any, ...]] = {}
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
        if args.sameoptions:
            raise Exception("Cannot mix --sameoptions with --meta")
    else:
        meta_weights = None


    player_id = 1
    player_files = {}
    for file in os.scandir(args.player_files_path):
        fname = file.name
        if file.is_file() and not fname.startswith(".") and not fname.lower().endswith(".ini") and \
                os.path.join(args.player_files_path, fname) not in {args.meta_file_path, args.weights_file_path}:
            path = os.path.join(args.player_files_path, fname)
            try:
                weights_for_file = []
                for doc_idx, yaml in enumerate(read_weights_yamls(path)):
                    if yaml is None:
                        logging.warning(f"Ignoring empty yaml document #{doc_idx + 1} in {fname}")
                    else:
                        weights_for_file.append(yaml)
                weights_cache[fname] = tuple(weights_for_file)
                        
            except Exception as e:
                raise ValueError(f"File {fname} is invalid. Please fix your yaml.") from e

    # sort dict for consistent results across platforms:
    weights_cache = {key: value for key, value in sorted(weights_cache.items(), key=lambda k: k[0].casefold())}
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

    from worlds.AutoWorld import AutoWorldRegister
    args.outputname = seed_name
    args.sprite = dict.fromkeys(range(1, args.multi+1), None)
    args.sprite_pool = dict.fromkeys(range(1, args.multi+1), None)
    args.name = {}

    settings_cache: dict[str, tuple[argparse.Namespace, ...]] = \
        {fname: (tuple(roll_settings(yaml, args.plando) for yaml in yamls) if args.sameoptions else None)
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
    args.player_options = {}

    player = 1
    while player <= args.multi:
        path = player_path_cache[player]
        if path:
            try:
                settings: tuple[argparse.Namespace, ...] = settings_cache[path] if settings_cache[path] else \
                    tuple(roll_settings(yaml, args.plando) for yaml in weights_cache[path])
                for settingsObject in settings:
                    for k, v in vars(settingsObject).items():
                        if v is not None:
                            try:
                                getattr(args, k)[player] = v
                            except AttributeError:
                                setattr(args, k, {player: v})
                            except Exception as e:
                                raise Exception(f"Error setting {k} to {v} for player {player}") from e

                    # name was not specified
                    if player not in args.name:
                        if path == args.weights_file_path:
                            # weights file, so we need to make the name unique
                            args.name[player] = f"Player{player}"
                        else:
                            # use the filename
                            args.name[player] = os.path.splitext(os.path.split(path)[-1])[0]
                    args.name[player] = handle_name(args.name[player], player, name_counter)

                    player += 1
            except Exception as e:
                raise ValueError(f"File {path} is invalid. Please fix your yaml.") from e
        else:
            raise RuntimeError(f'No weights specified for player {player}')

    if len(set(name.lower() for name in args.name.values())) != len(args.name):
        raise Exception(f"Names have to be unique. Names: {Counter(name.lower() for name in args.name.values())}")

    return args, seed


def read_weights_yamls(path) -> tuple[Any, ...]:
    try:
        if urllib.parse.urlparse(path).scheme in ('https', 'file'):
            yaml = str(urllib.request.urlopen(path).read(), "utf-8-sig")
        else:
            with open(path, 'rb') as f:
                yaml = str(f.read(), "utf-8-sig")
    except Exception as e:
        raise Exception(f"Failed to read weights ({path})") from e

    from yaml.error import MarkedYAMLError
    try:
        return tuple(parse_yamls(yaml))
    except MarkedYAMLError as ex:
        if ex.problem_mark:
            lines = yaml.splitlines()
            if ex.context_mark:
                relevant_lines = "\n".join(lines[ex.context_mark.line:ex.problem_mark.line+1])
            else:
                relevant_lines = lines[ex.problem_mark.line]
            error_line = " " * ex.problem_mark.column + "^"
            raise Exception(f"{ex.context} {ex.problem} on line {ex.problem_mark.line}:"
                            f"\n{relevant_lines}\n{error_line}")
        raise ex


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


class SafeFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        if isinstance(key, int):
            if key < len(args):
                return args[key]
            else:
                return "{" + str(key) + "}"
        else:
            return kwargs.get(key, "{" + key + "}")


def handle_name(name: str, player: int, name_counter: Counter):
    name_counter[name.lower()] += 1
    number = name_counter[name.lower()]
    new_name = "%".join([x.replace("%number%", "{number}").replace("%player%", "{player}") for x in name.split("%%")])

    new_name = SafeFormatter().vformat(new_name, (), {"number": number,
                                                      "NUMBER": (number if number > 1 else ''),
                                                      "player": player,
                                                      "PLAYER": (player if player > 1 else '')})
    # Run .strip twice for edge case where after the initial .slice new_name has a leading whitespace.
    # Could cause issues for some clients that cannot handle the additional whitespace.
    new_name = new_name.strip()[:16].strip()

    if new_name == "Archipelago":
        raise Exception(f"You cannot name yourself \"{new_name}\"")
    return new_name


def update_weights(weights: dict, new_weights: dict, update_type: str, name: str) -> dict:
    logging.debug(f'Applying {new_weights}')
    cleaned_weights = {}
    for option in new_weights:
        option_name = option.lstrip("+-")
        if option.startswith("+") and option_name in weights:
            cleaned_value = weights[option_name]
            new_value = new_weights[option]
            if isinstance(new_value, set):
                cleaned_value.update(new_value)
            elif isinstance(new_value, list):
                cleaned_value.extend(new_value)
            elif isinstance(new_value, dict):
                cleaned_value = dict(Counter(cleaned_value) + Counter(new_value))
            else:
                raise Exception(f"Cannot apply merge to non-dict, set, or list type {option_name},"
                                f" received {type(new_value).__name__}.")
            cleaned_weights[option_name] = cleaned_value
        elif option.startswith("-") and option_name in weights:
            cleaned_value = weights[option_name]
            new_value = new_weights[option]
            if isinstance(new_value, set):
                cleaned_value.difference_update(new_value)
            elif isinstance(new_value, list):
                for element in new_value:
                    cleaned_value.remove(element)
            elif isinstance(new_value, dict):
                cleaned_value = dict(Counter(cleaned_value) - Counter(new_value))
            else:
                raise Exception(f"Cannot apply remove to non-dict, set, or list type {option_name},"
                                f" received {type(new_value).__name__}.")
            cleaned_weights[option_name] = cleaned_value
        else:
            cleaned_weights[option_name] = new_weights[option]
    new_options = set(cleaned_weights) - set(weights)
    weights.update(cleaned_weights)
    if new_options:
        for new_option in new_options:
            logging.warning(f'{update_type} Suboption "{new_option}" of "{name}" did not '
                            f'overwrite a root option. '
                            f'This is probably in error.')
    return weights


def roll_meta_option(option_key, game: str, category_dict: dict) -> Any:
    from worlds import AutoWorldRegister

    if not game:
        return get_choice(option_key, category_dict)
    if game in AutoWorldRegister.world_types:
        game_world = AutoWorldRegister.world_types[game]
        options = game_world.options_dataclass.type_hints
        if option_key in options:
            if options[option_key].supports_weighting:
                return get_choice(option_key, category_dict)
            return category_dict[option_key]
    raise Options.OptionError(f"Error generating meta option {option_key} for {game}.")


def roll_linked_options(weights: dict) -> dict:
    weights = copy.deepcopy(weights)  # make sure we don't write back to other weights sets in same_settings
    for option_set in weights["linked_options"]:
        if "name" not in option_set:
            raise ValueError("One of your linked options does not have a name.")
        try:
            if Options.roll_percentage(option_set["percentage"]):
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


def roll_triggers(weights: dict, triggers: list, valid_keys: set) -> dict:
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
            if result == trigger_result and Options.roll_percentage(get_choice("percentage", option_set, 100)):
                for category_name, category_options in option_set["options"].items():
                    currently_targeted_weights = weights
                    if category_name:
                        currently_targeted_weights = currently_targeted_weights[category_name]
                    update_weights(currently_targeted_weights, category_options, "Triggered", option_set["option_name"])
            valid_keys.add(key)
        except Exception as e:
            raise ValueError(f"Your trigger number {i + 1} is invalid. "
                             f"Please fix your triggers.") from e
    return weights


def handle_option(ret: argparse.Namespace, game_weights: dict, option_key: str, option: type(Options.Option), plando_options: PlandoOptions):
    try:
        if option_key in game_weights:
            if not option.supports_weighting:
                player_option = option.from_any(game_weights[option_key])
            else:
                player_option = option.from_any(get_choice(option_key, game_weights))
        else:
            player_option = option.from_any(option.default)  # call the from_any here to support default "random"
        setattr(ret, option_key, player_option)
    except Exception as e:
        raise Options.OptionError(f"Error generating option {option_key} in {ret.game}") from e
    else:
        from worlds import AutoWorldRegister
        player_option.verify(AutoWorldRegister.world_types[ret.game], ret.name, plando_options)


def roll_settings(weights: dict, plando_options: PlandoOptions = PlandoOptions.bosses):
    """
    Roll options from specified weights, usually originating from a .yaml options file.

    Important note:
    The same weights dict is shared between all slots using the same yaml (e.g. generic weights file for filler slots).
    This means it should never be modified without making a deepcopy first.
    """

    from worlds import AutoWorldRegister

    if "linked_options" in weights:
        weights = roll_linked_options(weights)

    valid_keys = {"triggers"}
    if "triggers" in weights:
        weights = roll_triggers(weights, weights["triggers"], valid_keys)

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
        games = requirements.get("game", {})
        for game, version in games.items():
            if game not in AutoWorldRegister.world_types:
                continue
            if not version:
                raise Exception(f"Invalid version for game {game}: {version}.")
            if isinstance(version, str):
                version = {"min": version}
            if "min" in version and tuplize_version(version["min"]) > AutoWorldRegister.world_types[game].world_version:
                raise Exception(f"Settings reports required version of world \"{game}\" is at least {version['min']}, "
                                f"however world is of version "
                                f"{AutoWorldRegister.world_types[game].world_version.as_simple_string()}.")
            if "max" in version and tuplize_version(version["max"]) < AutoWorldRegister.world_types[game].world_version:
                raise Exception(f"Settings reports required version of world \"{game}\" is no later than {version['max']}, "
                                f"however world is of version "
                                f"{AutoWorldRegister.world_types[game].world_version.as_simple_string()}.")
    ret = argparse.Namespace()
    for option_key in Options.PerGameCommonOptions.type_hints:
        if option_key in weights and option_key not in Options.CommonOptions.type_hints:
            raise Exception(f"Option {option_key} has to be in a game's section, not on its own.")

    ret.game = get_choice("game", weights)
    if not isinstance(ret.game, str):
        if ret.game is None:
            raise Exception('"game" not specified')
        raise Exception(f"Invalid game: {ret.game}")
    if ret.game not in AutoWorldRegister.world_types:
        from worlds import failed_world_loads
        picks = Utils.get_fuzzy_results(ret.game, list(AutoWorldRegister.world_types) + failed_world_loads, limit=1)[0]
        if picks[0] in failed_world_loads:
            raise Exception(f"No functional world found to handle game {ret.game}. "
                            f"Did you mean '{picks[0]}' ({picks[1]}% sure)? "
                            f"If so, it appears the world failed to initialize correctly.")
        raise Exception(f"No world found to handle game {ret.game}. Did you mean '{picks[0]}' ({picks[1]}% sure)? "
                        f"Check your spelling or installation of that world.")

    if ret.game not in weights:
        raise Exception(f"No game options for selected game \"{ret.game}\" found.")

    world_type = AutoWorldRegister.world_types[ret.game]
    game_weights = weights[ret.game]

    for weight in chain(game_weights, weights):
        if weight.startswith("+"):
            raise Exception(f"Merge tag cannot be used outside of trigger contexts. Found {weight}")
        if weight.startswith("-"):
            raise Exception(f"Remove tag cannot be used outside of trigger contexts. Found {weight}")

    if "triggers" in game_weights:
        weights = roll_triggers(weights, game_weights["triggers"], valid_keys)
        game_weights = weights[ret.game]

    ret.name = get_choice('name', weights)
    for option_key, option in Options.CommonOptions.type_hints.items():
        setattr(ret, option_key, option.from_any(get_choice(option_key, weights, option.default)))

    for option_key, option in world_type.options_dataclass.type_hints.items():
        handle_option(ret, game_weights, option_key, option, plando_options)
        valid_keys.add(option_key)

    if ret.game == "A Link to the Past":
        # TODO there are still more LTTP options not on the options system
        valid_keys |= {"sprite_pool", "sprite", "random_sprite_on_event"}
        roll_alttp_settings(ret, game_weights)

    # log a warning for options within a game section that aren't determined as valid
    for option_key in game_weights:
        if option_key in valid_keys:
            continue
        logging.warning(f"{option_key} is not a valid option name for {ret.game} and is not present in triggers "
                        f"for player {ret.name}.")

    return ret


def roll_alttp_settings(ret: argparse.Namespace, weights):
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
    erargs, seed = main()
    from Main import main as ERmain
    multiworld = ERmain(erargs, seed)
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
