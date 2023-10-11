import base64
import json
import pickle
import typing
import uuid
import zipfile
import zlib

from io import BytesIO
from flask import request, flash, redirect, url_for, session, render_template
from markupsafe import Markup
from pony.orm import commit, flush, select, rollback
from pony.orm.core import TransactionIntegrityError

import MultiServer
from NetUtils import SlotType
from Utils import VersionException, __version__
from worlds.Files import AutoPatchRegister
from . import app
from .models import Seed, Room, Slot, GameDataPackage

banned_zip_contents = (".sfc", ".z64", ".n64", ".sms", ".gb")

def process_multidata(compressed_multidata, files={}):
    decompressed_multidata = MultiServer.Context.decompress(compressed_multidata)

    slots: typing.Set[Slot] = set()
    if "datapackage" in decompressed_multidata:
        # strip datapackage from multidata, leaving only the checksums
        game_data_packages: typing.List[GameDataPackage] = []
        for game, game_data in decompressed_multidata["datapackage"].items():
            if game_data.get("checksum"):
                game_data_package = GameDataPackage(checksum=game_data["checksum"],
                                                    data=pickle.dumps(game_data))
                decompressed_multidata["datapackage"][game] = {
                    "version": game_data.get("version", 0),
                    "checksum": game_data["checksum"]
                }
                try:
                    commit()  # commit game data package
                    game_data_packages.append(game_data_package)
                except TransactionIntegrityError:
                    del game_data_package
                    rollback()

    if "slot_info" in decompressed_multidata:
        for slot, slot_info in decompressed_multidata["slot_info"].items():
            # Ignore Player Groups (e.g. item links)
            if slot_info.type == SlotType.group:
                continue
            slots.add(Slot(data=files.get(slot, None),
                            player_name=slot_info.name,
                            player_id=slot,
                            game=slot_info.game))
        flush()  # commit slots

    compressed_multidata = compressed_multidata[0:1] + zlib.compress(pickle.dumps(decompressed_multidata), 9)
    return slots, compressed_multidata

def upload_zip_to_db(zfile: zipfile.ZipFile, owner=None, meta={"race": False}, sid=None):
    if not owner:
        owner = session["_id"]
    infolist = zfile.infolist()
    if all(file.filename.endswith((".yaml", ".yml")) or file.is_dir() for file in infolist):
        flash(Markup("Error: Your .zip file only contains .yaml files. "
                     'Did you mean to <a href="/generate">generate a game</a>?'))
        return

    spoiler = ""
    files = {}
    multidata = None

    # Load files.
    for file in infolist:
        handler = AutoPatchRegister.get_handler(file.filename)
        if file.filename.endswith(banned_zip_contents):
            return "Uploaded data contained a rom file, which is likely to contain copyrighted material. " \
                   "Your file was deleted."

        # AP Container
        elif handler:
            data = zfile.open(file, "r").read()
            patch = handler(BytesIO(data))
            patch.read()
            files[patch.player] = data

        # Spoiler
        elif file.filename.endswith(".txt"):
            spoiler = zfile.open(file, "r").read().decode("utf-8-sig")

        # Multi-data
        elif file.filename.endswith(".archipelago"):
            try:
                multidata = zfile.open(file).read()
            except:
                flash("Could not load multidata. File may be corrupted or incompatible.")
                multidata = None

        # Minecraft
        elif file.filename.endswith(".apmc"):
            data = zfile.open(file, "r").read()
            metadata = json.loads(base64.b64decode(data).decode("utf-8"))
            files[metadata["player_id"]] = data

        # Factorio
        elif file.filename.endswith(".zip"):
            try:
                _, _, slot_id, *_ = file.filename.split('_')[0].split('-', 3)
            except ValueError:
                flash("Error: Unexpected file found in .zip: " + file.filename)
                return
            data = zfile.open(file, "r").read()
            files[int(slot_id[1:])] = data

        # All other files using the standard MultiWorld.get_out_file_name_base method
        else:
            try:
                _, _, slot_id, *_ = file.filename.split('.')[0].split('_', 3)
            except ValueError:
                flash("Error: Unexpected file found in .zip: " + file.filename)
                return
            data = zfile.open(file, "r").read()
            files[int(slot_id[1:])] = data

    # Load multi data.
    if multidata:
        slots, multidata = process_multidata(multidata, files)

        seed = Seed(multidata=multidata, spoiler=spoiler, slots=slots, owner=owner, meta=json.dumps(meta),
                    id=sid if sid else uuid.uuid4())
        flush()  # create seed
        for slot in slots:
            slot.seed = seed
        return seed
    else:
        flash("No multidata was found in the zip file, which is required.")


@app.route('/uploads', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        else:
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
            elif file and allowed_file(file.filename):
                if zipfile.is_zipfile(file):
                    with zipfile.ZipFile(file, 'r') as zfile:
                        try:
                            res = upload_zip_to_db(zfile)
                        except VersionException:
                            flash(f"Could not load multidata. Wrong Version detected.")
                        else:
                            if type(res) == str:
                                return res
                            elif res:
                                return redirect(url_for("view_seed", seed=res.id))
                else:
                    file.seek(0)  # offset from is_zipfile check
                    # noinspection PyBroadException
                    try:
                        multidata = file.read()
                        slots, multidata = process_multidata(multidata)
                    except Exception as e:
                        flash(f"Could not load multidata. File may be corrupted or incompatible. ({e})")
                    else:
                        seed = Seed(multidata=multidata, slots=slots, owner=session["_id"])
                        flush()  # place into DB and generate ids
                        return redirect(url_for("view_seed", seed=seed.id))
            else:
                flash("Not recognized file format. Awaiting a .archipelago file or .zip containing one.")
    return render_template("hostGame.html", version=__version__)


@app.route('/user-content', methods=['GET'])
def user_content():
    rooms = select(room for room in Room if room.owner == session["_id"])
    seeds = select(seed for seed in Seed if seed.owner == session["_id"])
    return render_template("userContent.html", rooms=rooms, seeds=seeds)


def allowed_file(filename):
    return filename.endswith(('.archipelago', ".zip"))
