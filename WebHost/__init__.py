import os
import logging
import sys
import threading
import multiprocessing
import functools

import websockets
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

sys.path.append("..")
from MultiServer import Context, server

UPLOAD_FOLDER = 'uploads'

multidata_folder = os.path.join(UPLOAD_FOLDER, "multidata")
os.makedirs(multidata_folder, exist_ok=True)
os.makedirs("logs", exist_ok=True)


def allowed_file(filename):
    return filename.endswith('multidata')


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 megabyte limit
app.config["SECRET_KEY"] = os.urandom(32)
name = "localhost"

portrange = (30000, 40000)
current_port = portrange[0]


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


def get_next_port():
    global current_port
    with portlock:
        current_port += 1
        return current_port


@app.route('/log/<filename>')
def display_log(filename):
    with open(os.path.join("logs", filename + ".txt")) as log:
        return log.read().replace("\n", "<br>")


@app.route('/hosted/<filename>')
def host_multidata(filename=None):
    if not filename:
        return redirect(url_for('upload_multidata'))
    else:
        multidata = os.path.join(multidata_folder, filename)
        port = get_next_port()
        queue = multiprocessing.SimpleQueue()
        process = multiprocessing.Process(group=None, target=run_server_process,
                                          args=(port, multidata, filename, queue),
                                          name="MultiHost" + str(port))
        process.start()
        return "Hosting " + filename + " at " + name + ":" + str(port)


def run_server_process(port, multidata, filename, queue):
    async def main():
        logging.basicConfig(format='[%(asctime)s] %(message)s',
                            level=logging.INFO,
                            filename=os.path.join("logs", filename + ".txt"))
        ctx = Context(None, port, "", 1, 1000,
                      True, "enabled", "goal")

        data_filename = multidata

        try:
            ctx.load(data_filename, True)
        except Exception as e:
            logging.exception('Failed to read multiworld data (%s)' % e)
            raise

        ctx.init_save()

        ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, ctx.port, ping_timeout=None,
                                      ping_interval=None)

        logging.info('Hosting game at %s:%d (%s)' % (name, ctx.port,
                                                     'No password' if not ctx.password else 'Password: %s' % ctx.password))
        await ctx.server
        while ctx.running:
            await asyncio.sleep(1)
        logging.info("shutting down")

    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app.run()
