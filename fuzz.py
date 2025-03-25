import sys
import os

ap_path = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.insert(0, ap_path)

from worlds import AutoWorldRegister
from Options import (
    get_option_groups,
    Choice,
    Toggle,
    Range,
    ItemSet,
    ItemDict,
    LocationSet,
    OptionSet,
    FreeText,
    PlandoConnections,
    OptionList,
    PlandoTexts,
    OptionDict,
    OptionError,
)
from Utils import __version__, local_path
import Utils

from Generate import main as GenMain
from Main import main as ERmain
from argparse import Namespace, ArgumentParser
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import ctypes
import threading
from contextlib import redirect_stderr, redirect_stdout
from enum import Enum
from functools import wraps
from io import StringIO
from multiprocessing import Pool

import functools
import logging
import multiprocessing
import random
import shutil
import string
import tempfile
import time
import traceback
import yaml


OUT_DIR = f"fuzz_output"
ORIG_USER_PATH = Utils.user_path


def exception_in_causes(e, ty):
    if isinstance(e, ty):
        return True
    if e.__cause__ is not None:
        return exception_in_causes(e.__cause__, ty)
    return False


executor = ThreadPoolExecutor(max_workers=1)
def run_with_timeout(func, seconds, *args, **kwargs):
    global executor
    future = executor.submit(func, *args, **kwargs)
    try:
        return future.result(timeout=seconds)
    except TimeoutError:
        for thread in threading.enumerate():
            if thread.name != "MainThread":
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(TimeoutError))

        executor.shutdown(wait=True, cancel_futures=True)
        executor = ThreadPoolExecutor(max_workers=1)
        raise TimeoutError(
            f"Function '{func.__name__}' timed out after {seconds} seconds"
        )


def world_from_apworld_name(apworld_name):
    for name, world in AutoWorldRegister.world_types.items():
        if world.__module__.startswith(f"worlds.{apworld_name}"):
            return name, world

    raise Exception(f"Couldn't find loaded workd with world: {apworld_name}")


# See https://github.com/yaml/pyyaml/issues/103
yaml.SafeDumper.ignore_aliases = lambda *args: True

# Adapted from archipelago'd generate_yaml_templates
# https://github.com/ArchipelagoMW/Archipelago/blob/f75a1ae1174fb467e5c5bd5568d7de3c806d5b1c/Options.py#L1504
def generate_random_yaml(world_name, meta):
    def dictify_range(option):
        data = {option.default: 50}
        for sub_option in ["random", "random-low", "random-high"]:
            if sub_option != option.default:
                data[sub_option] = 0

        notes = {}
        for name, number in getattr(option, "special_range_names", {}).items():
            notes[name] = f"equivalent to {number}"
            if number in data:
                data[name] = data[number]
                del data[number]
            else:
                data[name] = 0

        return data, notes

    def sanitize(value):
        if isinstance(value, frozenset):
            return list(value)
        return value

    game_name, world = world_from_apworld_name(world_name)
    if world is None:
        raise Exception(f"Failed to resolve apworld from apworld name: {apworld_name}")

    game_options = {}
    option_groups = get_option_groups(world)
    for group, options in option_groups.items():
        for option_name, option_value in options.items():
            override = meta.get(None, {}).get(option_name)
            if not override:
                override = meta.get(game_name, {}).get(option_name)

            if override is not None:
                game_options[option_name] = override
                continue

            game_options[option_name] = sanitize(
                get_random_value(option_name, option_value)
            )

    yaml_content = {
        "description": "%s Template, generated with https://github.com/Eijebong/Archipelago-fuzzer"
        % game_name,
        "game": game_name,
        "requires": {
            "version": __version__,
        },
        game_name: game_options,
    }

    res = yaml.safe_dump(yaml_content, sort_keys=False)

    return res


def get_random_value(name, option):
    if name == "item_links":
        # Let's not fuck with item links right now, I'm scared
        return option.default

    if name == "megamix_mod_data":
        # Megamix is a special child and requires this to be valid JSON. Since we can't provide that, just ignore it
        return option.default

    if issubclass(option, (PlandoConnections, PlandoTexts)):
        # See, I was already afraid with item_links but now it's plain terror. Let's not ever touch this ever.
        return option.default

    if name == "gfxmod":
        # XXX: LADX has this and it should be a choice but is freetext for some reason...
        # Putting invalid values here means the gen fails even though it doesn't affect any logic
        # Just return Link for now.
        return "Link"

    if issubclass(option, OptionDict):
        # This is for example factorio's start_items and worldgen settings. I don't think it's worth randomizing those as I'm not expecting the generation outcome to change from them.
        # Plus I have no idea how to randomize them in the first place :)
        return option.default

    if issubclass(option, (Choice, Toggle)):
        return random.choice(list(option.options.keys()))

    if issubclass(option, Range):
        return random.randint(option.range_start, option.range_end)

    if issubclass(option, (ItemSet, ItemDict, LocationSet)):
        # I don't know what to do here so just return the default value instead of a random one.
        # This affects options like start inventory, local items, non local
        # items so it's not the end of the world if they don't get randomized
        # but we might want to look into that later on
        return option.default

    if issubclass(option, OptionSet):
        return random.sample(
            list(option.valid_keys), k=random.randint(0, len(option.valid_keys))
        )

    if issubclass(option, OptionList):
        return random.sample(
            list(option.valid_keys), k=random.randint(0, len(option.valid_keys))
        )

    if issubclass(option, FreeText):
        return "".join(
            random.choice(string.ascii_letters) for i in range(random.randint(0, 255))
        )

    return option.default


def call_generate(yaml_path, output_path):
    from settings import get_settings

    settings = get_settings()

    args = Namespace(
        **{
            "weights_file_path": settings.generator.weights_file_path,
            "sameoptions": False,
            "player_files_path": yaml_path,
            "seed": random.randint(0, 1000000000),
            "multi": 1,
            "spoiler": 1,
            "outputpath": output_path,
            "race": False,
            "meta_file_path": "meta-doesnt-exist.yaml",
            "log_level": "info",
            "yaml_output": 1,
            "plando": [],
            "skip_prog_balancing": False,
            "skip_output": False,
            "csv_output": False,
            "log_time": False,
        }
    )
    erargs, seed = GenMain(args)
    ERmain(erargs, seed)


def gen_wrapper(yaml_contents, apworld_name, timeout_s, i, dump_option_errors):
    out_buf = StringIO()

    try:
        # We don't care about the actual gen output, just trash it immediately after gen
        output_path = tempfile.mkdtemp(prefix="apfuzz")

        # Override Utils.user path so we can customize the logs folder
        # This is very important because every gen starts a thread that cleans all logs older than 7 days.
        # This is not customizable in any way shape or form. By throwing logs files away, we prevent that thread
        # from becoming more and more busy as gens go.
        def my_user_path(name):
            if name == "logs":
                return output_path
            return ORIG_USER_PATH(name)

        Utils.user_path = my_user_path

        yaml_path_dir = tempfile.mkdtemp(prefix="apfuzz")
        for nb, yaml_content in enumerate(yaml_contents):
            yaml_path = os.path.join(yaml_path_dir, f"{i}-{nb}.yaml")
            open(yaml_path, "wb").write(yaml_content.encode("utf-8"))

        with redirect_stdout(out_buf), redirect_stderr(out_buf):
            run_with_timeout(call_generate, timeout_s, yaml_path_dir, output_path)
        return GenOutcome.Success
    except Exception as e:
        is_timeout = isinstance(e, TimeoutError)
        is_option_error = exception_in_causes(e, OptionError)

        if is_option_error and not dump_option_errors:
            return GenOutcome.OptionError

        if is_option_error:
            error_ty = "ignored"
        elif is_timeout:
            error_ty = "timeout"
        else:
            error_ty = "error"

        error_output_dir = os.path.join(OUT_DIR, error_ty, apworld_name, str(i))
        os.makedirs(error_output_dir)

        for nb, yaml_content in enumerate(yaml_contents):
            error_yaml_path = os.path.join(error_output_dir, f"{i}-{nb}.yaml")
            open(error_yaml_path, "wb").write(yaml_content.encode("utf-8"))

        error_log_path = os.path.join(error_output_dir, f"{i}.log")
        with open(error_log_path, "w") as fd:
            fd.write(out_buf.getvalue())

            if is_timeout:
                fd.write(f"[...] Generation killed here after {timeout_s}s")
                return GenOutcome.Timeout
            else:
                fd.write("".join(traceback.format_exception(e)))

        return GenOutcome.OptionError if is_option_error else GenOutcome.Failure
    finally:
        root_logger = logging.getLogger()
        handlers = root_logger.handlers[:]
        for handler in handlers:
            root_logger.removeHandler(handler)
            handler.close()

        shutil.rmtree(output_path)
        shutil.rmtree(yaml_path_dir)


class GenOutcome(Enum):
    Success = 0
    Failure = 1
    Timeout = 2
    OptionError = 3


SUCCESS = 0
FAILURE = 0
TIMEOUTS = 0
OPTION_ERRORS = 0
SUBMITTED = 0


def success(result):
    global SUCCESS, FAILURE, SUBMITTED, OPTION_ERRORS, TIMEOUTS
    if result == GenOutcome.Success:
        SUCCESS += 1
        print(".", end="")
    elif result == GenOutcome.Failure:
        print("F", end="")
        FAILURE += 1
    elif result == GenOutcome.Timeout:
        print("T", end="")
        TIMEOUTS += 1
    elif result == GenOutcome.OptionError:
        print("I", end="")
        OPTION_ERRORS += 1

    sys.stdout.flush()

    SUBMITTED -= 1


def error(e):
    import traceback

    traceback.print_exception(e)


def print_status():
    print()
    print("Success:", SUCCESS)
    print("Failures:", FAILURE)
    print("Timeouts:", TIMEOUTS)
    print("Ignored:", OPTION_ERRORS)
    print()
    print("Time taken:{:.2f}s".format(time.time() - START))


if __name__ == "__main__":

    def main(p, args):
        global SUBMITTED

        apworld_name = args.game
        if args.meta:
            with open(args.meta, "r") as fd:
                meta = yaml.safe_load(fd.read())
        else:
            meta = {}

        if apworld_name is not None:
            world = world_from_apworld_name(apworld_name)
            if world is None:
                raise Exception(
                    f"Failed to resolve apworld from apworld name: {apworld_name}"
                )

        if os.path.exists(OUT_DIR):
            shutil.rmtree(OUT_DIR)
        os.makedirs(OUT_DIR)

        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.flush()

        i = 0
        valid_worlds = [
            world.__module__.split(".")[1]
            for world in AutoWorldRegister.world_types.values()
        ]
        if "apsudoku" in valid_worlds:
            valid_worlds.remove("apsudoku")

        yamls_per_run_bounds = [int(arg) for arg in args.yamls_per_run.split("-")]

        if len(yamls_per_run_bounds) not in {1, 2}:
            raise Exception(
                "Invalid value passed for `yamls_per_run`. Either pass an int or a range like `1-10`"
            )

        if len(yamls_per_run_bounds) == 2:
            if yamls_per_run_bounds[0] >= yamls_per_run_bounds[1]:
                raise Exception("Invalid range value passed for `yamls_per_run`.")

        while i < args.runs:
            if apworld_name is None:
                actual_apworld = random.choice(valid_worlds)
            else:
                actual_apworld = apworld_name

            if len(yamls_per_run_bounds) == 1:
                yamls_this_run = yamls_per_run_bounds[0]
            else:
                # +1 here to make the range inclusive
                yamls_this_run = random.randrange(
                    yamls_per_run_bounds[0], yamls_per_run_bounds[1] + 1
                )

            random_yamls = [
                generate_random_yaml(actual_apworld, meta) for _ in range(yamls_this_run)
            ]

            SUBMITTED += 1
            last_job = p.apply_async(
                gen_wrapper,
                args=(random_yamls, actual_apworld, args.timeout, i, args.dump_ignored),
                callback=success,
                error_callback=error,
            )

            while SUBMITTED >= args.jobs * 10:
                # Poll the last job to keep the queue running
                last_job.ready()
                time.sleep(0.001)

            i += 1

        while SUBMITTED > 0:
            last_job.ready()
            time.sleep(0.05)

    parser = ArgumentParser(prog="apfuzz")
    parser.add_argument("-g", "--game", default=None)
    parser.add_argument("-j", "--jobs", default=10, type=int)
    parser.add_argument("-r", "--runs", type=int)
    parser.add_argument("-n", "--yamls_per_run", default="1", type=str)
    parser.add_argument("-t", "--timeout", default=15, type=int)
    parser.add_argument("-m", "--meta", default=None, type=None)
    parser.add_argument("--dump-ignored", default=False, action="store_true")

    args = parser.parse_args()

    try:
        can_fork = hasattr(os, "fork")
        # fork here is way faster because it doesn't have to reload all worlds, but it's only available on some platforms
        # forking for every job also has the advantage of being sure that the process is "clean". Although I don't know if that actually matters
        start_method = "fork" if can_fork else "spawn"
        multiprocessing.set_start_method(start_method)
        with Pool(processes=args.jobs, maxtasksperchild=None) as p:
            START = time.time()
            main(p, args)
    except KeyboardInterrupt:
        pass
    finally:
        print_status()
        executor.shutdown()
