import zipfile
import lzma
import json
import base64
import MultiServer

from flask import request, flash, redirect, url_for, session, render_template
from pony.orm import flush, select

from WebHostLib import app, Seed, Room, Slot
from Utils import parse_yaml

accepted_zip_contents = {"patches": ".apbp",
                         "spoiler": ".txt",
                         "multidata": ".archipelago"}

banned_zip_contents = (".sfc",)


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
                if file.filename.endswith(".zip"):
                    slots = set()
                    spoiler = ""
                    multidata = None
                    with zipfile.ZipFile(file, 'r') as zfile:
                        infolist = zfile.infolist()

                        for file in infolist:
                            if file.filename.endswith(banned_zip_contents):
                                return "Uploaded data contained a rom file, which is likely to contain copyrighted material. Your file was deleted."
                            elif file.filename.endswith(".apbp"):
                                data = zfile.open(file, "r").read()
                                yaml_data = parse_yaml(lzma.decompress(data).decode("utf-8-sig"))
                                if yaml_data["version"] < 2:
                                    return "Old format cannot be uploaded (outdated .apbp)", 500
                                metadata = yaml_data["meta"]
                                slots.add(Slot(data=data, player_name=metadata["player_name"],
                                               player_id=metadata["player_id"],
                                               game="A Link to the Past"))

                            elif file.filename.endswith(".apmc"):
                                data = zfile.open(file, "r").read()
                                metadata = json.loads(base64.b64decode(data).decode("utf-8"))
                                slots.add(Slot(data=data, player_name=metadata["player_name"],
                                               player_id=metadata["player_id"],
                                               game="Minecraft"))

                            elif file.filename.endswith(".zip"):
                                # Factorio mods needs a specific name or they do no function
                                _, seed_name, slot_id, slot_name = file.filename.rsplit("_", 1)[0].split("-")
                                slots.add(Slot(data=zfile.open(file, "r").read(), player_name=slot_name,
                                              player_id=int(slot_id[1:]), game="Factorio"))

                            elif file.filename.endswith(".txt"):
                                spoiler = zfile.open(file, "r").read().decode("utf-8-sig")
                            elif file.filename.endswith(".archipelago"):
                                try:
                                    multidata = zfile.open(file).read()
                                    MultiServer.Context._decompress(multidata)
                                except:
                                    flash("Could not load multidata. File may be corrupted or incompatible.")
                                else:
                                    multidata = zfile.open(file).read()
                        if multidata:
                            flush()  # commit slots
                            seed = Seed(multidata=multidata, spoiler=spoiler, slots=slots, owner=session["_id"])
                            flush()  # create seed
                            for slot in slots:
                                slot.seed = seed

                            return redirect(url_for("viewSeed", seed=seed.id))
                        else:
                            flash("No multidata was found in the zip file, which is required.")
                else:
                    try:
                        multidata = file.read()
                        MultiServer.Context._decompress(multidata)
                    except:
                        flash("Could not load multidata. File may be corrupted or incompatible.")
                        raise
                    else:
                        seed = Seed(multidata=multidata, owner=session["_id"])
                        flush()  # place into DB and generate ids
                        return redirect(url_for("viewSeed", seed=seed.id))
            else:
                flash("Not recognized file format. Awaiting a .multidata file.")
    return render_template("hostGame.html")


@app.route('/user-content', methods=['GET'])
def user_content():
    rooms = select(room for room in Room if room.owner == session["_id"])
    seeds = select(seed for seed in Seed if seed.owner == session["_id"])
    return render_template("userContent.html", rooms=rooms, seeds=seeds)


def allowed_file(filename):
    return filename.endswith(('.archipelago', ".zip"))
