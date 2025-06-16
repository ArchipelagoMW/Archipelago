import base64
import json
import pickle
import typing
import uuid
import zipfile
import zlib

from io import BytesIO
from flask import request, flash, redirect, url_for, session, render_template, abort
from markupsafe import Markup
from pony.orm import commit, flush, select, rollback
from pony.orm.core import TransactionIntegrityError
import schema

import MultiServer
from NetUtils import SlotType
from Utils import VersionException, __version__
from worlds import GamesPackage
from worlds.Files import AutoPatchRegister
from worlds.AutoWorld import data_package_checksum
from . import app
from .models import Seed, Room, Slot, GameDataPackage

banned_extensions = (".sfc", ".z64", ".n64", ".nes", ".smc", ".sms", ".gb", ".gbc", ".gba")
allowed_options_extensions = (".yaml", ".json", ".yml", ".txt", ".zip")
allowed_generation_extensions = (".archipelago", ".zip")

games_package_schema = schema.Schema({
    "item_name_groups": {str: [str]},
    "item_name_to_id": {str: int},
    "location_name_groups": {str: [str]},
    "location_name_to_id": {str: int},
    schema.Optional("checksum"): str,
    schema.Optional("version"): int,
})


def allowed_options(filename: str) -> bool:
    return filename.endswith(allowed_options_extensions)


def allowed_generation(filename: str) -> bool:
    return filename.endswith(allowed_generation_extensions)


def banned_file(filename: str) -> bool:
    return filename.endswith(banned_extensions)


def process_multidata(compressed_multidata, files={}):
    game_data: GamesPackage

    decompressed_multidata = MultiServer.Context.decompress(compressed_multidata)

    slots: typing.Set[Slot] = set()
    if "datapackage" in decompressed_multidata:
        # strip datapackage from multidata, leaving only the checksums
        game_data_packages: typing.List[GameDataPackage] = []
        for game, game_data in decompressed_multidata["datapackage"].items():
            if game_data.get("checksum"):
                original_checksum = game_data.pop("checksum")
                game_data = games_package_schema.validate(game_data)
                game_data = {key: value for key, value in sorted(game_data.items())}
                game_data["checksum"] = data_package_checksum(game_data)
                if original_checksum != game_data["checksum"]:
                    raise Exception(f"Original checksum {original_checksum} != "
                                    f"calculated checksum {game_data['checksum']} "
                                    f"for game {game}.")

                game_data_package = GameDataPackage(checksum=game_data["checksum"],
                                                    data=pickle.dumps(game_data))
                decompressed_multidata["datapackage"][game] = {
                    "version": game_data.get("version", 0),
                    "checksum": game_data["checksum"],
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
    if all(allowed_options(file.filename) or file.is_dir() for file in infolist):
        flash(Markup("Error: Your .zip file only contains options files. "
                     'Did you mean to <a href="/generate">generate a game</a>?'))
        return

    spoiler = ""
    files = {}
    multidata = None

    # Load files.
    for file in infolist:
        handler = AutoPatchRegister.get_handler(file.filename)
        if banned_file(file.filename):
            return "Uploaded data contained a rom file, which is likely to contain copyrighted material. " \
                   "Your file was deleted."

        # AP Container
        elif handler:
            data = zfile.open(file, "r").read()
            with zipfile.ZipFile(BytesIO(data)) as container:
                player = json.loads(container.open("archipelago.json").read())["player"]
            files[player] = data

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


@app.route("/uploads", methods=["GET", "POST"])
def uploads():
    if request.method == "POST":
        # check if the POST request has a file part.
        if "file" not in request.files:
            flash("No file part in POST request.")
        else:
            uploaded_file = request.files["file"]
            # If the user does not select file, the browser will still submit an empty string without a file name.
            if uploaded_file.filename == "":
                flash("No selected file.")
            elif uploaded_file and allowed_generation(uploaded_file.filename):
                if zipfile.is_zipfile(uploaded_file):
                    with zipfile.ZipFile(uploaded_file, "r") as zfile:
                        try:
                            res = upload_zip_to_db(zfile)
                        except VersionException:
                            flash(f"Could not load multidata. Wrong Version detected.")
                        except Exception as e:
                            flash(f"Could not load multidata. File may be corrupted or incompatible. ({e})")
                        else:
                            if res is str:
                                return res
                            elif res:
                                return redirect(url_for("view_seed", seed=res.id))
                else:
                    uploaded_file.seek(0)  # offset from is_zipfile check
                    # noinspection PyBroadException
                    try:
                        multidata = uploaded_file.read()
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


@app.route("/disown_seed/<suuid:seed>", methods=["GET"])
def disown_seed(seed):
    seed = Seed.get(id=seed)
    if not seed:
        return abort(404)
    if seed.owner !=  session["_id"]:
        return abort(403)
    
    seed.owner = 0

    return redirect(url_for("user_content"))


@app.route("/disown_room/<suuid:room>", methods=["GET"])
def disown_room(room):
    room = Room.get(id=room)
    if not room:
        return abort(404)
    if room.owner != session["_id"]:
        return abort(403)

    room.owner = 0

    return redirect(url_for("user_content"))
