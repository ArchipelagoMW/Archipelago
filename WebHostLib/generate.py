import os
import tempfile
import random
import json
import zipfile
from collections import Counter
from typing import Dict, Optional as TypeOptional
from Utils import __version__

from flask import request, flash, redirect, url_for, session, render_template

from worlds.alttp.EntranceRandomizer import parse_arguments
from Main import main as ERmain
from BaseClasses import seeddigits, get_seed
from Generate import handle_name
import pickle

from .models import *
from WebHostLib import app
from .check import get_yaml_data, roll_options
from .upload import upload_zip_to_db


def get_meta(options_source: dict) -> dict:
    meta = {
        "hint_cost": int(options_source.get("hint_cost", 10)),
        "forfeit_mode": options_source.get("forfeit_mode", "goal"),
        "remaining_mode": options_source.get("remaining_mode", "disabled"),
        "collect_mode": options_source.get("collect_mode", "disabled"),
    }
    return meta


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
            if type(options) == str:
                flash(options)
            else:
                results, gen_options = roll_options(options)
                # get form data -> server settings
                meta = get_meta(request.form)
                meta["race"] = race

                if race:
                    meta["item_cheat"] = False
                    meta["remaining_mode"] = False

                if any(type(result) == str for result in results.values()):
                    return render_template("checkResult.html", results=results)
                elif len(gen_options) > app.config["MAX_ROLL"]:
                    flash(f"Sorry, generating of multiworlds is limited to {app.config['MAX_ROLL']} players for now. "
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


def gen_game(gen_options, meta: TypeOptional[Dict[str, object]] = None, owner=None, sid=None):
    if not meta:
        meta: Dict[str, object] = {}

    meta.setdefault("hint_cost", 10)
    race = meta.get("race", False)
    del (meta["race"])
    try:
        target = tempfile.TemporaryDirectory()
        playercount = len(gen_options)
        seed = get_seed()
        random.seed(seed)

        if race:
            random.seed()  # reset to time-based random source

        seedname = "W" + (f"{random.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits))

        erargs = parse_arguments(['--multi', str(playercount)])
        erargs.seed = seed
        erargs.name = {x: "" for x in range(1, playercount + 1)}  # only so it can be overwrittin in mystery
        erargs.spoiler = 0 if race else 2
        erargs.race = race
        erargs.outputname = seedname
        erargs.outputpath = target.name
        erargs.teams = 1

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
        ERmain(erargs, seed, baked_server_options=meta)

        return upload_to_db(target.name, sid, owner, race)
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
