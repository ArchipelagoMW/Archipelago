# module has yet to be made capable of running in multiple processes

import os
import logging
import sys
import threading
import typing
import multiprocessing
import functools
from pony.flask import Pony
from pony.orm import Database, Required, Optional, commit, select, db_session

import websockets
from flask import Flask, flash, request, redirect, url_for, render_template, Response, g
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


def run_server_process(multidata: str):
    async def main():
        logging.basicConfig(format='[%(asctime)s] %(message)s',
                            level=logging.INFO,
                            filename=os.path.join(LOGS_FOLDER, multidata + ".txt"))
        ctx = Context("", 0, "", 1, 1000,
                      True, "enabled", "goal")
        ctx.load(os.path.join(multidata_folder, multidata), True)
        ctx.auto_shutdown = 24 * 60 * 60  # 24 hours
        ctx.init_save()

        ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, 0, ping_timeout=None,
                                      ping_interval=None)

        await ctx.server
        for wssocket in ctx.server.ws_server.sockets:
            socketname = wssocket.getsockname()
            if wssocket.family == socket.AF_INET6:
                logging.info(f'Hosting game at [{get_public_ipv6()}]:{socketname[1]}')
            elif wssocket.family == socket.AF_INET:
                logging.info(f'Hosting game at {get_public_ipv4()}:{socketname[1]}')
        while ctx.running:
            await asyncio.sleep(1)
        logging.info("Shutting down")

    import asyncio
    if ".." not in sys.path:
        sys.path.append("..")
    from MultiServer import Context, server
    from Utils import get_public_ipv4, get_public_ipv6
    import socket
    asyncio.run(main())


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    app.run(debug=True)
