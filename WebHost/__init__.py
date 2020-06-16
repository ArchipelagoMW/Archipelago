# module has yet to be made capable of running in multiple processes

import os
import logging
import threading
import typing
import multiprocessing
from pony.orm import Database, db_session

from flask import Flask, flash, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = os.path.relpath('uploads')
LOGS_FOLDER = os.path.relpath('logs')
multidata_folder = os.path.join(UPLOAD_FOLDER, "multidata")
os.makedirs(multidata_folder, exist_ok=True)
os.makedirs(LOGS_FOLDER, exist_ok=True)


def allowed_file(filename):
    return filename.endswith('multidata')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 megabyte limit
app.config["SECRET_KEY"] = os.urandom(32)
app.config["PONY"] = {
    'provider': 'sqlite',
    'filename': 'db.db3',
    'create_db': True
}

db = Database()

name = "localhost"

multiworlds = {}


class Multiworld():
    def __init__(self, multidata: str):
        self.multidata = multidata
        self.process: typing.Optional[multiprocessing.Process] = None
        multiworlds[multidata] = self

    def start(self):
        if self.process and self.process.is_alive():
            return False

        logging.info(f"Spinning up {self.multidata}")
        self.process = multiprocessing.Process(group=None, target=run_server_process,
                                               args=(self.multidata,),
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
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(multidata_folder, filename))
            return redirect(url_for('host_multidata',
                                    filename=filename))
    return render_template("upload_multidata.html")


def _read_log(path: str):
    if os.path.exists(path):
        with open(path) as log:
            yield from log
    else:
        yield f"Logfile {path} does not exist. " \
              f"Likely a crash during spinup of multiworld instance or it is still spinning up."


@app.route('/log/<filename>')
def display_log(filename: str):
    filename = secure_filename(filename)
    # noinspection PyTypeChecker
    return Response(_read_log(os.path.join("logs", filename + ".txt")), mimetype="text/plain;charset=UTF-8")


processstartlock = threading.Lock()


@app.route('/hosted/<filename>')
def host_multidata(filename: str):
    with db_session:
        multiworld = multiworlds.get(filename, None)
        if not multiworld:
            multiworld = Multiworld(filename)

        with processstartlock:
            multiworld.start()

    return render_template("host_multidata.html", filename=filename)


from WebHost.customserver import run_server_process

if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    app.run(debug=True)
