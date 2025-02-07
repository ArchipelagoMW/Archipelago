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
from jinja2 import Template

from argparse import Namespace, ArgumentParser
import yaml
import random
import shutil
import string
import multiprocessing
import tempfile
from multiprocessing import Pool
from io import StringIO
import time
from Main import main as ERmain
from Generate import main as GenMain
from enum import Enum
import traceback
import threading
import signal
import functools
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, TimeoutError


OUT_DIR = f"fuzz_output"


def exception_in_causes(e, ty):
    if isinstance(e, ty):
        return True
    if e.__cause__ is not None:
        return exception_in_causes(e.__cause__, ty)
    return False

executor = ThreadPoolExecutor(max_workers=1)
def run_with_timeout(func, seconds, *args, **kwargs):
    future = executor.submit(func, *args, **kwargs)
    try:
        return future.result(timeout=seconds)
    except TimeoutError:
        raise TimeoutError(f"Function '{func.__name__}' timed out after {seconds} seconds")


def world_from_apworld_name(apworld_name):
    for name, world in AutoWorldRegister.world_types.items():
        if world.__module__.startswith(f"worlds.{apworld_name}"):
            return name, world

    raise Exception(f"Couldn't find loaded workd with world: {apworld_name}")


# In Options.py
def generate_random_yaml(world_name):
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

    def yaml_dump_scalar(scalar) -> str:
        # yaml dump may add end of document marker and newlines.
        return yaml.dump(scalar).replace("...\n", "").strip()

    game_name, world = world_from_apworld_name(world_name)
    if world is None:
        raise Exception(f"Failed to resolve apworld from apworld name: {apworld_name}")

    option_groups = get_option_groups(world)
    for group, options in option_groups.items():
        for option_name, option_value in options.items():
            option_value.default = get_random_value(option_name, option_value)
    with open(local_path("data", "options.yaml")) as f:
        file_data = f.read()

    res = Template(file_data).render(
        option_groups=option_groups,
        __version__=__version__,
        game=game_name,
        yaml_dump=yaml_dump_scalar,
        dictify_range=dictify_range,
    )

    return res


def get_random_value(name, option):
    if name == "item_links":
        # Let's not fuck with item links right now, I'm scared
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
        return random.choice(list(option.options.values()))

    if issubclass(option, Range):
        return random.randint(option.range_start, option.range_end)

    if issubclass(option, (ItemSet, ItemDict, LocationSet)):
        # I don't know what to do here so just return the default value instead of a random one.
        # This affects options like start inventory, local items, non local
        # items so it's not the end of the world if they don't get randomized
        # but we might want to look into that later on
        return option.default

    if issubclass(option, OptionSet):
        return random.choices(option.options, k=random.randint(0, len(option.options)))

    if issubclass(option, OptionList):
        return random.choices(
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


def gen_wrapper(yaml_contents, apworld_name, timeout_s, i):
    out_buf = StringIO()
    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    try:
        # We don't care about the actual gen output, just trash it immediately after gen
        output_path = tempfile.mkdtemp(prefix="apfuzz")
        yaml_path_dir = tempfile.mkdtemp(prefix="apfuzz")
        for nb, yaml_content in enumerate(yaml_contents):
            yaml_path = os.path.join(yaml_path_dir, f"{i}-{nb}.yaml")
            open(yaml_path, "w").write(yaml_content)

        sys.stdout = out_buf
        sys.stderr = out_buf
        run_with_timeout(call_generate, timeout_s, yaml_path_dir, output_path)
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr
        return GenOutcome.Success
    except Exception as e:
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

        is_timeout = isinstance(e, TimeoutError)
        is_option_error = exception_in_causes(e, OptionError)

        if is_option_error:
            return GenOutcome.OptionError

        error_ty = "timeout" if is_timeout else "error"
        error_output_dir = os.path.join(OUT_DIR, error_ty, apworld_name, str(i))
        os.makedirs(error_output_dir)

        for nb, yaml_content in enumerate(yaml_contents):
            error_yaml_path = os.path.join(error_output_dir, f"{i}-{nb}.yaml")
            open(error_yaml_path, "w").write(yaml_content)

        error_log_path = os.path.join(error_output_dir, f"{i}.log")
        with open(error_log_path, "w") as fd:
            fd.write(out_buf.getvalue())

            if is_timeout:
                fd.write("[...] Generation killed here after 15s")
                return GenOutcome.Timeout
            else:
                fd.write("".join(traceback.format_exception(e)))

        return GenOutcome.Failure
    finally:
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

        while i < args.runs:
            if apworld_name is None:
                actual_apworld = random.choice(valid_worlds)
            else:
                actual_apworld = apworld_name
            random_yamls = [
                generate_random_yaml(actual_apworld) for _ in range(args.yamls_per_run)
            ]

            SUBMITTED += 1
            last_job = p.apply_async(
                gen_wrapper,
                args=(random_yamls, actual_apworld, args.timeout, i),
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
    parser.add_argument("-n", "--yamls_per_run", default=1, type=int)
    parser.add_argument("-t", "--timeout", default=15, type=int)

    args = parser.parse_args()

    try:
        can_fork = hasattr(os, "fork")
        # fork here is way faster because it doesn't have to reload all worlds, but it's only available on some platforms
        # forking for every job also has the advantage of being sure that the process is "clean". Although I don't know if that actually matters
        start_method = "fork" if can_fork else "spawn"
        multiprocessing.set_start_method(start_method)
        p = Pool(processes=args.jobs, maxtasksperchild=None)
        START = time.time()
        main(p, args)
    except KeyboardInterrupt:
        p.close()
        p.join()
    except Exception as e:
        p.close()
        p.join()
        raise e
    finally:
        print_status()
        executor.shutdown()
