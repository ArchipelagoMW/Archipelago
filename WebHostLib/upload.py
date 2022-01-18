import zipfile
import lzma
import json
import base64
import MultiServer
import uuid

from flask import request, flash, redirect, url_for, session, render_template
from pony.orm import flush, select

from WebHostLib import app, Seed, Room, Slot
from Utils import parse_yaml, VersionException
from Patch import preferred_endings

banned_zip_contents = (".sfc",)


def upload_zip_to_db(zfile: zipfile.ZipFile, owner=None, meta={"race": False}, sid=None):
    if not owner:
        owner = session["_id"]
    infolist = zfile.infolist()
    slots = set()
    spoiler = ""
    multidata = None
    for file in infolist:
        if file.filename.endswith(banned_zip_contents):
            return "Uploaded data contained a rom file, which is likely to contain copyrighted material. " \
                   "Your file was deleted."
        elif file.filename.endswith(tuple(preferred_endings.values())):
            data = zfile.open(file, "r").read()
            yaml_data = parse_yaml(lzma.decompress(data).decode("utf-8-sig"))
            if yaml_data["version"] < 2:
                return "Old format cannot be uploaded (outdated .apbp)"
            metadata = yaml_data["meta"]

            slots.add(Slot(data=data,
                           player_name=metadata["player_name"],
                           player_id=metadata["player_id"],
                           game=yaml_data["game"]))

        elif file.filename.endswith(".apmc"):
            data = zfile.open(file, "r").read()
            metadata = json.loads(base64.b64decode(data).decode("utf-8"))
            slots.add(Slot(data=data, player_name=metadata["player_name"],
                           player_id=metadata["player_id"],
                           game="Minecraft"))

        elif file.filename.endswith(".zip"):
            # Factorio mods need a specific name or they do not function
            _, seed_name, slot_id, slot_name = file.filename.rsplit("_", 1)[0].split("-", 3)
            slots.add(Slot(data=zfile.open(file, "r").read(), player_name=slot_name,
                           player_id=int(slot_id[1:]), game="Factorio"))

        elif file.filename.endswith(".apz5"):
            # .apz5 must be named specifically since they don't contain any metadata
            _, seed_name, slot_id, slot_name = file.filename.split('.')[0].split('_', 3)
            slots.add(Slot(data=zfile.open(file, "r").read(), player_name=slot_name,
                           player_id=int(slot_id[1:]), game="Ocarina of Time"))

        elif file.filename.endswith(".txt"):
            spoiler = zfile.open(file, "r").read().decode("utf-8-sig")
        elif file.filename.endswith(".archipelago"):
            try:
                multidata = zfile.open(file).read()
            except:
                flash("Could not load multidata. File may be corrupted or incompatible.")
                multidata = None

    if multidata:
        decompressed_multidata = MultiServer.Context.decompress(multidata)
        player_names = {slot.player_name for slot in slots}
        leftover_names = [(name, index) for index, name in
                          enumerate((name for name in decompressed_multidata["names"][0]), start=1)]
        newslots = [(Slot(data=None, player_name=name, player_id=slot, game=decompressed_multidata["games"][slot]))
                    for name, slot in leftover_names if name not in player_names]
        for slot in newslots:
            slots.add(slot)

        flush()  # commit slots
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
                        MultiServer.Context.decompress(multidata)
                    except Exception as e:
                        flash(f"Could not load multidata. File may be corrupted or incompatible. ({e})")
                    else:
                        seed = Seed(multidata=multidata, owner=session["_id"])
                        flush()  # place into DB and generate ids
                        return redirect(url_for("view_seed", seed=seed.id))
            else:
                flash("Not recognized file format. Awaiting a .archipelago file or .zip containing one.")
    return render_template("hostGame.html")


@app.route('/user-content', methods=['GET'])
def user_content():
    rooms = select(room for room in Room if room.owner == session["_id"])
    seeds = select(seed for seed in Seed if seed.owner == session["_id"])
    return render_template("userContent.html", rooms=rooms, seeds=seeds)


def allowed_file(filename):
    return filename.endswith(('.archipelago', ".zip"))
