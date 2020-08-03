import os
import tempfile
import random
import zlib
import json

from flask import request, flash, redirect, url_for, session, render_template, send_file, Response

from EntranceRandomizer import parse_arguments
from Main import main as ERmain
from Main import get_seed, seeddigits
from Patch import update_patch_data

from .models import *
from WebHostLib import app
from .check import get_yaml_data, roll_yamls


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
                results, gen_options = roll_yamls(options)
                if any(result == str for result in results.values()):
                    return render_template("checkresult.html", results=results)
                elif len(gen_options) > app.config["MAX_ROLL"]:
                    flash(f"Sorry, generating of multiworld is limited to {app.config['MAX_ROLL']} players for now. "
                          f"If you have a larger group, please generate it yourself and upload it.")
                else:
                    seed_id = gen(gen_options, race=race)
                    return redirect(url_for("view_seed", seed=seed_id))
    return render_template("generate.html", race=race)


@app.route("/dl_patch/<int:patch_id>/<suuid:room_id>")
def download_patch(patch_id, room_id):
    patch = Patch.get(id=patch_id)
    if not patch:
        return "Patch not found"
    else:
        import io

        room = Room.get(id=room_id)
        last_port = room.last_port
        pname = room.seed.multidata["names"][0][patch.player - 1]

        patch_data = update_patch_data(patch.data, server="berserkermulti.world:" + str(last_port))
        patch_data = io.BytesIO(patch_data)

        fname = f"P{patch.player}_{pname}_{app.jinja_env.filters['suuid'](room_id)}.bmbp"
        return send_file(patch_data, as_attachment=True, attachment_filename=fname)


@app.route("/dl_spoiler/<suuid:seed_id>")
def download_spoiler(seed_id):
    return Response(Seed.get(id=seed_id).spoiler, mimetype="text/plain")


@app.route("/dl_raw_patch/<suuid:seed_id>/<int:player_id>")
def download_raw_patch(seed_id, player_id):
    patch = select(patch for patch in Patch if patch.player == player_id and patch.seed.id == seed_id).first()

    if not patch:
        return "Patch not found"
    else:
        import io

        pname = patch.seed.multidata["names"][0][patch.player - 1]

        patch_data = update_patch_data(patch.data, server="")
        patch_data = io.BytesIO(patch_data)

        fname = f"P{patch.player}_{pname}_{app.jinja_env.filters['suuid'](seed_id)}.bmbp"
        return send_file(patch_data, as_attachment=True, attachment_filename=fname)


def gen(gen_options, race=False):
    target = tempfile.TemporaryDirectory()
    with target:
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

        for player, (playerfile, settings) in enumerate(gen_options.items(), 1):
            for k, v in vars(settings).items():
                if v is not None:
                    getattr(erargs, k)[player] = v

            if not erargs.name[player]:
                erargs.name[player] = os.path.split(playerfile)[-1].split(".")[0]

        erargs.names = ",".join(erargs.name[i] for i in range(1, playercount + 1))
        del (erargs.name)

        erargs.skip_progression_balancing = {player: not balanced for player, balanced in
                                             erargs.progression_balancing.items()}
        del (erargs.progression_balancing)
        ERmain(erargs, seed)
        return upload_to_db(target.name)


def upload_to_db(folder):
    patches = set()
    spoiler = ""
    multidata = None
    for file in os.listdir(folder):
        file = os.path.join(folder, file)
        if file.endswith(".bmbp"):
            player = int(file.split("P")[-1].split(".")[0].split("_")[0])
            patches.add(Patch(data=open(file, "rb").read(), player=player))
        elif file.endswith(".txt"):
            spoiler = open(file, "rt").read()
        elif file.endswith("multidata"):
            try:
                multidata = json.loads(zlib.decompress(open(file, "rb").read()))
            except Exception as e:
                flash(e)
    if multidata:
        commit()  # commit patches
        seed = Seed(multidata=multidata, spoiler=spoiler, patches=patches, owner=session["_id"])
        commit()  # create seed
        for patch in patches:
            patch.seed = seed
        return seed.id
