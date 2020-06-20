import os
import logging
import typing
import multiprocessing
import threading
import json
import zlib

from pony.orm import db_session, commit
from pony.flask import Pony
from flask import Flask, flash, request, redirect, url_for, render_template, Response, session

from .models import *

UPLOAD_FOLDER = os.path.relpath('uploads')
LOGS_FOLDER = os.path.relpath('logs')
os.makedirs(LOGS_FOLDER, exist_ok=True)


def allowed_file(filename):
    return filename.endswith('multidata')


app = Flask(__name__)
Pony(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 megabyte limit
# if you want persistent sessions on your server, make sure you make this a constant in your config.yaml
app.config["SECRET_KEY"] = os.urandom(32)
app.config['SESSION_PERMANENT'] = True
app.config["PONY"] = {
    'provider': 'sqlite',
    'filename': os.path.abspath('db.db3'),
    'create_db': True
}

multiworlds = {}


@app.before_first_request
def register_session():
    session.permanent = True  # technically 31 days after the last visit
    if not session.get("_id", None):
        session["_id"] = uuid4()  # uniquely identify each session without needing a login


class MultiworldInstance():
    def __init__(self, room: Room):
        self.room_id = room.id
        self.process: typing.Optional[multiprocessing.Process] = None
        multiworlds[self.room_id] = self

    def start(self):
        if self.process and self.process.is_alive():
            return False

        logging.info(f"Spinning up {self.room_id}")
        with db_session:
            self.process = multiprocessing.Process(group=None, target=run_server_process,
                                                   args=(self.room_id, app.config["PONY"]),
                                                   name="MultiHost")
        self.process.start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

@app.route('/', methods=['GET', 'POST'])
def upload_multidata():
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
                try:
                    multidata = json.loads(zlib.decompress(file.read()).decode("utf-8-sig"))
                except:
                    flash("Could not load multidata. File may be corrupted or incompatible.")
                else:
                    seed = Seed(multidata=multidata)
                    commit()  # place into DB and generate ids
                    return redirect(url_for("view_seed", seed=seed.id))
            else:
                flash("Not recognized file format. Awaiting a .multidata file.")
    return render_template("upload_multidata.html")


@app.route('/seed/<int:seed>')
def view_seed(seed: int):
    seed = Seed.get(id=seed)
    return render_template("view_seed.html", seed=seed)


@app.route('/new_room/<int:seed>')
def new_room(seed: int):
    seed = Seed.get(id=seed)
    room = Room(seed=seed, owner=session["_id"])
    commit()
    return redirect(url_for("host_room", room=room.id))


def _read_log(path: str):
    if os.path.exists(path):
        with open(path) as log:
            yield from log
    else:
        yield f"Logfile {path} does not exist. " \
              f"Likely a crash during spinup of multiworld instance or it is still spinning up."


@app.route('/log/<int:room>')
def display_log(room: int):
    # noinspection PyTypeChecker
    return Response(_read_log(os.path.join("logs", str(room) + ".txt")), mimetype="text/plain;charset=UTF-8")


processstartlock = threading.Lock()


@app.route('/hosted/<int:room>', methods=['GET', 'POST'])
def host_room(room: int):
    room = Room.get(id=room)
    if request.method == "POST":
        if room.owner == session["_id"]:
            cmd = request.form["cmd"]
            Command(room=room, commandtext=cmd)
            commit()
    with db_session:
        multiworld = multiworlds.get(room.id, None)
        if not multiworld:
            multiworld = MultiworldInstance(room)

    with processstartlock:
        multiworld.start()

    return render_template("host_room.html", room=room)


from WebHost.customserver import run_server_process
