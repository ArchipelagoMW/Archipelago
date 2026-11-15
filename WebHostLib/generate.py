import concurrent.futures
import json
import os
import random
import tempfile
import zipfile
from collections import Counter
from pickle import PicklingError
from typing import Any

from flask import flash, redirect, render_template, request, session, url_for
from pony.orm import commit, db_session

from BaseClasses import get_seed, seeddigits
from Generate import PlandoOptions, handle_name, mystery_argparse
from Main import main as ERmain
from Utils import __version__, restricted_dumps, DaemonThreadPoolExecutor
from WebHostLib import app
from settings import ServerOptions, GeneratorOptions
from .check import get_yaml_data, roll_options
from .models import Generation, STATE_ERROR, STATE_QUEUED, Seed, UUID
from .upload import upload_zip_to_db


def get_meta(options_source: dict, race: bool = False) -> dict[str, list[str] | dict[str, Any]]:
    plando_options: set[str] = set()
    for substr in ("bosses", "items", "connections", "texts"):
        if options_source.get(f"plando_{substr}", substr in GeneratorOptions.plando_options):
            plando_options.add(substr)

    server_options = {
        "hint_cost": int(options_source.get("hint_cost", ServerOptions.hint_cost)),
        "release_mode": str(options_source.get("release_mode", ServerOptions.release_mode)),
        "remaining_mode": str(options_source.get("remaining_mode", ServerOptions.remaining_mode)),
        "collect_mode": str(options_source.get("collect_mode", ServerOptions.collect_mode)),
        "countdown_mode": str(options_source.get("countdown_mode", ServerOptions.countdown_mode)),
        "item_cheat": bool(int(options_source.get("item_cheat", not ServerOptions.disable_item_cheat))),
        "server_password": str(options_source.get("server_password", None)),
    }
    generator_options = {
        "spoiler": int(options_source.get("spoiler", GeneratorOptions.spoiler)),
        "race": race,
    }

    if race:
        server_options["item_cheat"] = False
        server_options["remaining_mode"] = "disabled"
        generator_options["spoiler"] = 0

    return {
        "server_options": server_options,
        "plando_options": list(plando_options),
        "generator_options": generator_options,
    }


@app.route('/generate', methods=['GET', 'POST'])
@app.route('/generate/<race>', methods=['GET', 'POST'])
def generate(race=False):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        else:
            files = request.files.getlist('file')
            options = get_yaml_data(files)
            if isinstance(options, str):
                flash(options)
            else:
                meta = get_meta(request.form, race)
                return start_generation(options, meta)

    return render_template("generate.html", race=race, version=__version__)


def format_exception(e: BaseException) -> str:
    return f"{e.__class__.__name__}: {e}"


def start_generation(options: dict[str, dict | str], meta: dict[str, Any]):
    results, gen_options = roll_options(options, set(meta["plando_options"]))

    if any(type(result) == str for result in results.values()):
        return render_template("checkResult.html", results=results)
    elif len(gen_options) > app.config["MAX_ROLL"]:
        flash(f"Sorry, generating of multiworlds is limited to {app.config['MAX_ROLL']} players. "
              f"If you have a larger group, please generate it yourself and upload it.")
        return redirect(url_for(request.endpoint, **(request.view_args or {})))
    elif len(gen_options) >= app.config["JOB_THRESHOLD"]:
        try:
            gen = Generation(
                options=restricted_dumps({name: vars(options) for name, options in gen_options.items()}),
                # convert to json compatible
                meta=json.dumps(meta),
                state=STATE_QUEUED,
                owner=session["_id"])
        except PicklingError as e:
            from .autolauncher import handle_generation_failure
            handle_generation_failure(e)
            meta["error"] = format_exception(e)
            details = json.dumps(meta, indent=4).strip()
            return render_template("seedError.html", seed_error=meta["error"], details=details)

        commit()

        return redirect(url_for("wait_seed", seed=gen.id))
    else:
        try:
            seed_id = gen_game({name: vars(options) for name, options in gen_options.items()},
                               meta=meta, owner=session["_id"].int, timeout=app.config["JOB_TIME"])
        except BaseException as e:
            from .autolauncher import handle_generation_failure
            handle_generation_failure(e)
            meta["error"] = format_exception(e)
            details = json.dumps(meta, indent=4).strip()
            return render_template("seedError.html", seed_error=meta["error"], details=details)

        return redirect(url_for("view_seed", seed=seed_id))


def gen_game(gen_options: dict, meta: dict[str, Any] | None = None, owner=None, sid=None, timeout: int|None = None):
    if meta is None:
        meta = {}

    meta.setdefault("server_options", {}).setdefault("hint_cost", 10)
    race = meta.setdefault("generator_options", {}).setdefault("race", False)

    def task():
        target = tempfile.TemporaryDirectory()
        playercount = len(gen_options)
        seed = get_seed()

        if race:
            random.seed()  # use time-based random source
        else:
            random.seed(seed)

        seedname = "W" + (f"{random.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits))

        args = mystery_argparse([])  # Just to set up the Namespace with defaults
        args.multi = playercount
        args.seed = seed
        args.name = {x: "" for x in range(1, playercount + 1)}  # only so it can be overwritten in mystery
        args.spoiler = meta["generator_options"].get("spoiler", 0)
        args.race = race
        args.outputname = seedname
        args.outputpath = target.name
        args.teams = 1
        args.plando_options = PlandoOptions.from_set(meta.setdefault("plando_options",
                                                                     {"bosses", "items", "connections", "texts"}))
        args.skip_prog_balancing = False
        args.skip_output = False
        args.spoiler_only = False
        args.csv_output = False
        args.sprite = dict.fromkeys(range(1, args.multi+1), None)
        args.sprite_pool = dict.fromkeys(range(1, args.multi+1), None)

        name_counter = Counter()
        for player, (playerfile, settings) in enumerate(gen_options.items(), 1):
            for k, v in settings.items():
                if v is not None:
                    if hasattr(args, k):
                        getattr(args, k)[player] = v
                    else:
                        setattr(args, k, {player: v})

            if not args.name[player]:
                args.name[player] = os.path.splitext(os.path.split(playerfile)[-1])[0]
            args.name[player] = handle_name(args.name[player], player, name_counter)
        if len(set(args.name.values())) != len(args.name):
            raise Exception(f"Names have to be unique. Names: {Counter(args.name.values())}")
        ERmain(args, seed, baked_server_options=meta["server_options"])

        return upload_to_db(target.name, sid, owner, race)

    thread_pool = DaemonThreadPoolExecutor(max_workers=1)
    thread = thread_pool.submit(task)

    try:
        return thread.result(timeout)
    except concurrent.futures.TimeoutError as e:
        if sid:
            with db_session:
                gen = Generation.get(id=sid)
                if gen is not None:
                    gen.state = STATE_ERROR
                    meta = json.loads(gen.meta)
                    meta["error"] = ("Allowed time for Generation exceeded, " +
                                     "please consider generating locally instead. " +
                                     format_exception(e))
                    gen.meta = json.dumps(meta)
                    commit()
    except (KeyboardInterrupt, SystemExit):
        # don't update db, retry next time
        raise
    except BaseException as e:
        if sid:
            with db_session:
                gen = Generation.get(id=sid)
                if gen is not None:
                    gen.state = STATE_ERROR
                    meta = json.loads(gen.meta)
                    meta["error"] = format_exception(e)
                    gen.meta = json.dumps(meta)
                    commit()
        raise
    finally:
        # free resources claimed by thread pool, if possible
        # NOTE: Timeout depends on the process being killed at some point
        #       since we can't actually cancel a running gen at the moment.
        thread_pool.shutdown(wait=False, cancel_futures=True)


@app.route('/wait/<suuid:seed>')
def wait_seed(seed: UUID):
    seed_id = seed
    seed = Seed.get(id=seed_id)
    if seed:
        return redirect(url_for("view_seed", seed=seed_id))
    generation = Generation.get(id=seed_id)

    if not generation:
        return "Generation not found."
    elif generation.state == STATE_ERROR:
        meta = json.loads(generation.meta)
        details = json.dumps(meta, indent=4).strip()
        return render_template("seedError.html", seed_error=meta["error"], details=details)
    return render_template("waitSeed.html", seed_id=seed_id)


def upload_to_db(folder, sid, owner, race):
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        if file.endswith(".zip"):
            with db_session:
                with zipfile.ZipFile(file) as zfile:
                    res = upload_zip_to_db(zfile, owner, {"race": race}, sid)
                if type(res) == "str":
                    raise Exception(res)
                elif res:
                    seed = res
                    gen = Generation.get(id=seed.id)
                    if gen is not None:
                        gen.delete()
                    return seed.id
    raise Exception("Generation zipfile not found.")
