import os
import logging
import sys
import threading
import typing
import multiprocessing
import functools

import websockets
from flask import Flask, flash, request, redirect, url_for, render_template, Response
from werkzeug.utils import secure_filename

if ".." not in sys.path:
    sys.path.append("..")

UPLOAD_FOLDER = 'uploads'
LOGS_FOLDER = 'logs'

multidata_folder = os.path.join(UPLOAD_FOLDER, "multidata")
os.makedirs(multidata_folder, exist_ok=True)
os.makedirs(LOGS_FOLDER, exist_ok=True)


def allowed_file(filename):
    return filename.endswith('multidata')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 megabyte limit
app.config["SECRET_KEY"] = os.urandom(32)
name = "localhost"

portrange = (49152, 65535)
current_port = portrange[0]
current_ports = {}
current_multiworlds = {}


class Multiworld():
    def __init__(self, file: str):
        self.port = get_next_port()
        self.multidata = file

        current_ports[self.port] = self
        current_multiworlds[self.multidata] = self

        self.process: typing.Optional[multiprocessing.Process] = None

    def start(self):
        if self.process and self.process.is_alive():
            return
        logging.info(f"Spinning up {self.multidata}")
        self.process = multiprocessing.Process(group=None, target=run_server_process,
                                               args=(self.port, self.multidata),
                                               name="MultiHost" + str(self.port))
        self.process.start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

        del (current_ports[self.port])
        del (current_multiworlds[self.multidata])

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
    return '''
    <!doctype html>
    <title>Upload Multidata</title>
    <h1>Upload Multidata</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


portlock = threading.Lock()


def get_next_port() -> int:
    global current_port
    with portlock:
        while current_port in current_ports:
            if current_port >= portrange[1]:
                current_port = portrange[0]
            else:
                current_port += 1

        return current_port


def _read_log(path: str):
    with open(path) as log:
        yield from log


@app.route('/log/<filename>')
def display_log(filename: str):
    # noinspection PyTypeChecker
    return Response(_read_log(os.path.join("logs", filename + ".txt")), mimetype="text/plain;charset=UTF-8")


processstartlock = threading.Lock()


@app.route('/hosted/<filename>')
def host_multidata(filename: str = None):
    if not filename:
        return redirect(url_for('upload_multidata'))
    else:
        multidata = os.path.join(multidata_folder, filename)
        if multidata in current_multiworlds:
            multiworld = current_multiworlds[multidata]
        else:
            with processstartlock:
                multiworld = Multiworld(multidata)
                multiworld.start()

        return render_template("host_multidata.html", filename=filename, port=multiworld.port, name=name)


def run_server_process(port: int, multidata: str):
    async def main():
        logging.basicConfig(format='[%(asctime)s] %(message)s',
                            level=logging.INFO,
                            filename=os.path.join(LOGS_FOLDER, os.path.split(multidata)[-1] + ".txt"))

        ctx = Context("", port, "", 1, 1000,
                      True, "enabled", "goal")
        ctx.load(multidata, True)
        ctx.init_save()

        ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, ctx.port, ping_timeout=None,
                                      ping_interval=None)

        logging.info('Hosting game at %s:%d (%s)' % (name, ctx.port,
                                                     'No password' if not ctx.password else 'Password: %s' % ctx.password))
        await ctx.server
        while ctx.running:
            await asyncio.sleep(1)
        logging.info("Shutting down")

    import asyncio
    from MultiServer import Context, server
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app.run()
