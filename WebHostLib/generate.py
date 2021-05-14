import os
import tempfile
import random
import json
from collections import Counter

from flask import request, flash, redirect, url_for, session, render_template

from worlds.alttp.EntranceRandomizer import parse_arguments
from Main import main as ERmain
from Main import get_seed, seeddigits
from Mystery import handle_name
import pickle

from .models import *
from WebHostLib import app
from .check import get_yaml_data, roll_options


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
                if any(type(result) == str for result in results.values()):
                    return render_template("checkResult.html", results=results)
                elif len(gen_options) > app.config["MAX_ROLL"]:
                    flash(f"Sorry, generating of multiworlds is limited to {app.config['MAX_ROLL']} players for now. "
                          f"If you have a larger group, please generate it yourself and upload it.")
                elif len(gen_options) >= app.config["JOB_THRESHOLD"]:
                    gen = Generation(
                        options=pickle.dumps({name: vars(options) for name, options in gen_options.items()}),
                        # convert to json compatible
                        meta=pickle.dumps({"race": race}), state=STATE_QUEUED,
                        owner=session["_id"])
                    commit()

                    return redirect(url_for("wait_seed", seed=gen.id))
                else:
                    try:
                        seed_id = gen_game({name: vars(options) for name, options in gen_options.items()},
                                           race=race, owner=session["_id"].int)
                    except BaseException as e:
                        from .autolauncher import handle_generation_failure
                        handle_generation_failure(e)
                        return render_template("seedError.html", seed_error=(e.__class__.__name__ + ": "+ str(e)))

                    return redirect(url_for("viewSeed", seed=seed_id))

    return render_template("generate.html", race=race)


def gen_game(gen_options, race=False, owner=None, sid=None):
    try:
        target = tempfile.TemporaryDirectory()
        playercount = len(gen_options)
        seed = get_seed()
        random.seed(seed)

        if race:
            random.seed()  # reset to time-based random source

        seedname = "M" + (f"{random.randint(0, pow(10, seeddigits) - 1)}".zfill(seeddigits))

        erargs = parse_arguments(['--multi', str(playercount)])
        erargs.seed = seed
        erargs.name = {x: "" for x in range(1, playercount + 1)}  # only so it can be overwrittin in mystery
        erargs.create_spoiler = not race
        erargs.race = race
        erargs.skip_playthrough = race
        erargs.outputname = seedname
        erargs.outputpath = target.name
        erargs.teams = 1
        erargs.progression_balancing = {}
        erargs.create_diff = True

        name_counter = Counter()
        for player, (playerfile, settings) in enumerate(gen_options.items(), 1):
            for k, v in settings.items():
                if v is not None:
                    getattr(erargs, k)[player] = v

            if not erargs.name[player]:
                erargs.name[player] = os.path.splitext(os.path.split(playerfile)[-1])[0]
            erargs.name[player] = handle_name(erargs.name[player], player, name_counter)

        erargs.names = ",".join(erargs.name[i] for i in range(1, playercount + 1))
        del (erargs.name)
        ERmain(erargs, seed)

        return upload_to_db(target.name, owner, sid, race)
    except BaseException as e:
        if sid:
            with db_session:
                gen = Generation.get(id=sid)
                if gen is not None:
                    gen.state = STATE_ERROR
                    meta = json.loads(gen.meta)
                    meta["error"] = (e.__class__.__name__ + ": "+ str(e))
                    gen.meta = json.dumps(meta)

                    commit()
        raise


@app.route('/wait/<suuid:seed>')
def wait_seed(seed: UUID):
    seed_id = seed
    seed = Seed.get(id=seed_id)
    if seed:
        return redirect(url_for("viewSeed", seed=seed_id))
    generation = Generation.get(id=seed_id)

    if not generation:
        return "Generation not found."
    elif generation.state == STATE_ERROR:
        return render_template("seedError.html", seed_error=generation.meta)
    return render_template("waitSeed.html", seed_id=seed_id)


def upload_to_db(folder, owner, sid, race:bool):
    patches = set()
    spoiler = ""

    multidata = None
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        if file.endswith(".apbp"):
            player_text = file.split("_P", 1)[1]
            player_name = player_text.split("_", 1)[1].split(".", 1)[0]
            player_id = int(player_text.split(".", 1)[0].split("_", 1)[0])
            patches.add(Patch(data=open(file, "rb").read(),
                              player_id=player_id, player_name = player_name))
        elif file.endswith(".txt"):
            spoiler = open(file, "rt", encoding="utf-8-sig").read()
        elif file.endswith(".archipelago"):
            multidata = open(file, "rb").read()
    if multidata:
        with db_session:
            if sid:
                seed = Seed(multidata=multidata, spoiler=spoiler, patches=patches, owner=owner,
                            id=sid, meta=json.dumps({"tags": ["generated"]}))
            else:
                seed = Seed(multidata=multidata, spoiler=spoiler, patches=patches, owner=owner,
                            meta=json.dumps({"tags": ["generated"]}))
            for patch in patches:
                patch.seed = seed
            if sid:
                gen = Generation.get(id=sid)
                if gen is not None:
                    gen.delete()
        return seed.id
    else:
        raise Exception("Multidata required (.archipelago), but not found.")
