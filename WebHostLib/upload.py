import json
import zlib
import zipfile
import logging
import MultiServer

from flask import request, flash, redirect, url_for, session, render_template
from pony.orm import commit, select

from WebHostLib import app, Seed, Room, Patch

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
                    patches = set()
                    spoiler = ""
                    multidata = None
                    with zipfile.ZipFile(file, 'r') as zfile:
                        infolist = zfile.infolist()

                        for file in infolist:
                            if file.filename.endswith(banned_zip_contents):
                                return "Uploaded data contained a rom file, which is likely to contain copyrighted material. Your file was deleted."
                            elif file.filename.endswith(".apbp"):
                                splitted = file.filename.split("/")[-1][3:].split("P", 1)
                                player = int(splitted[1].split(".")[0].split("_")[0])
                                patches.add(Patch(data=zfile.open(file, "r").read(), player=player))
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
                            commit()  # commit patches
                            seed = Seed(multidata=multidata, spoiler=spoiler, patches=patches, owner=session["_id"])
                            commit()  # create seed
                            for patch in patches:
                                patch.seed = seed

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
                        logging.info(multidata)
                        seed = Seed(multidata=multidata, owner=session["_id"])
                        commit()  # place into DB and generate ids
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
