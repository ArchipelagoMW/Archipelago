import json
import os
import pickle
import random
import tempfile
import zipfile
import concurrent.futures
from collections import Counter
from typing import Dict, Optional, Any

from flask import request, flash, redirect, url_for, session, render_template
from pony.orm import commit, db_session

from BaseClasses import seeddigits, get_seed
from Generate import handle_name, PlandoOptions
from Main import main as ERmain
from Utils import __version__
from WebHostLib import app
from worlds.alttp.EntranceRandomizer import parse_arguments
from .check import get_yaml_data, roll_options
from .models import Generation, STATE_ERROR, STATE_QUEUED, Seed, UUID
from .upload import upload_zip_to_db


def get_meta(options_source: dict) -> dict:
    plando_options = {
        options_source.get("plando_bosses", ""),
        options_source.get("plando_items", ""),
        options_source.get("plando_connections", ""),
        options_source.get("plando_texts", "")
    }
    plando_options -= {""}

    server_options = {
        "hint_cost": int(options_source.get("hint_cost", 10)),
        "release_mode": options_source.get("release_mode", "goal"),
        "remaining_mode": options_source.get("remaining_mode", "disabled"),
        "collect_mode": options_source.get("collect_mode", "disabled"),
        "item_cheat": bool(int(options_source.get("item_cheat", 1))),
        "server_password": options_source.get("server_password", None),
    }
    return {"server_options": server_options, "plando_options": list(plando_options)}


@app.route('/generate', methods=['GET', 'POST'])
@app.route('/generate/<race>', methods=['GET', 'POST'])
def generate(race=False):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        else:
            file = request.files['file']
            options = get_yaml_data(file)
            if isinstance(options, str):
                flash(options)
            else:
                meta = get_meta(request.form)
                meta["race"] = race
                results, gen_options = roll_options(options, meta["plando_options"])

                if race:
                    meta["server_options"]["item_cheat"] = False
                    meta["server_options"]["remaining_mode"] = "disabled"

                if any(type(result) == str for result in results.values()):
                    return render_template("checkResult.html", results=results)
                elif len(gen_options) > app.config["MAX_ROLL"]:
                    flash(f"Sorry, generating of multiworlds is limited to {app.config['MAX_ROLL']} players. "
                          f"If you have a larger group, please generate it yourself and upload it.")
                elif len(gen_options) >= app.config["JOB_THRESHOLD"]:
                    gen = Generation(
                        options=pickle.dumps({name: vars(options) for name, options in gen_options.items()}),
                        # convert to json compatible
                        meta=json.dumps(meta),
                        state=STATE_QUEUED,
                        owner=session["_id"])
                    commit()

                    return redirect(url_for("wait_seed", seed=gen.id))
                else:
                    try:
                        seed_id = gen_game({name: vars(options) for name, options in gen_options.items()},
                                           meta=meta, owner=session["_id"].int)
                    except BaseException as e:
                        from .autolauncher import handle_generation_failure
                        handle_generation_failure(e)
                        return render_template("seedError.html", seed_error=(e.__class__.__name__ + ": " + str(e)))

                    return redirect(url_for("view_seed", seed=seed_id))

    return render_template("generate.html", race=race, version=__version__)


def gen_game(gen_options: dict, meta: Optional[Dict[str, Any]] = None, owner=None, sid=None):
    if not meta:
        meta: Dict[str, Any] = {}

    meta.setdefault("server_options", {}).setdefault("hint_cost", 10)
    race = meta.setdefault("race", False)

    def task():
        target = tempfile.TemporaryDirectory()
        playercount = len(gen_options)
        seed = get_seed()

        if race:
            random.seed()  # use time-based random source
        else:
            random.seed(seed)

        seedname = "W" + (f"{random.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits))

        erargs = parse_arguments(['--multi', str(playercount)])
        erargs.seed = seed
        erargs.name = {x: "" for x in range(1, playercount + 1)}  # only so it can be overwritten in mystery
        erargs.spoiler = 0 if race else 3
        erargs.race = race
        erargs.outputname = seedname
        erargs.outputpath = target.name
        erargs.teams = 1
        erargs.plando_options = PlandoOptions.from_set(meta.setdefault("plando_options",
                                                                        {"bosses", "items", "connections", "texts"}))

        name_counter = Counter()
        for player, (playerfile, settings) in enumerate(gen_options.items(), 1):
            for k, v in settings.items():
                if v is not None:
                    if hasattr(erargs, k):
                        getattr(erargs, k)[player] = v
                    else:
                        setattr(erargs, k, {player: v})

            if not erargs.name[player]:
                erargs.name[player] = os.path.splitext(os.path.split(playerfile)[-1])[0]
            erargs.name[player] = handle_name(erargs.name[player], player, name_counter)
        if len(set(erargs.name.values())) != len(erargs.name):
            raise Exception(f"Names have to be unique. Names: {Counter(erargs.name.values())}")
        ERmain(erargs, seed, baked_server_options=meta["server_options"])

        return upload_to_db(target.name, sid, owner, race)
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    thread = thread_pool.submit(task)

    try:
        return thread.result(app.config["JOB_TIME"])
    except concurrent.futures.TimeoutError as e:
        if sid:
            with db_session:
                gen = Generation.get(id=sid)
                if gen is not None:
                    gen.state = STATE_ERROR
                    meta = json.loads(gen.meta)
                    meta["error"] = (
                            "Allowed time for Generation exceeded, please consider generating locally instead. " +
                            e.__class__.__name__ + ": " + str(e))
                    gen.meta = json.dumps(meta)
                    commit()
    except BaseException as e:
        if sid:
            with db_session:
                gen = Generation.get(id=sid)
                if gen is not None:
                    gen.state = STATE_ERROR
                    meta = json.loads(gen.meta)
                    meta["error"] = (e.__class__.__name__ + ": " + str(e))
                    gen.meta = json.dumps(meta)
                    commit()
        raise


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
        return render_template("seedError.html", seed_error=generation.meta)
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
