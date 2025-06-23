import base64
import os
import socket
import uuid

from flask import Flask
from flask_caching import Cache
from flask_compress import Compress
from pony.flask import Pony
from werkzeug.routing import BaseConverter

from Utils import title_sorted, get_file_safe_name

UPLOAD_FOLDER = os.path.relpath('uploads')
LOGS_FOLDER = os.path.relpath('logs')
os.makedirs(LOGS_FOLDER, exist_ok=True)

app = Flask(__name__)
Pony(app)

app.jinja_env.filters['any'] = any
app.jinja_env.filters['all'] = all
app.jinja_env.filters['get_file_safe_name'] = get_file_safe_name

app.config["SELFHOST"] = True  # application process is in charge of running the websites
app.config["GENERATORS"] = 8  # maximum concurrent world gens
app.config["HOSTERS"] = 8  # maximum concurrent room hosters
app.config["SELFLAUNCH"] = True  # application process is in charge of launching Rooms.
app.config["SELFLAUNCHCERT"] = None  # can point to a SSL Certificate to encrypt Room websocket connections
app.config["SELFLAUNCHKEY"] = None  # can point to a SSL Certificate Key to encrypt Room websocket connections
app.config["SELFGEN"] = True  # application process is in charge of scheduling Generations.
app.config["DEBUG"] = False
app.config["PORT"] = 80
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64 megabyte limit
# if you want to deploy, make sure you have a non-guessable secret key
app.config["SECRET_KEY"] = bytes(socket.gethostname(), encoding="utf-8")
# at what amount of worlds should scheduling be used, instead of rolling in the web-thread
app.config["JOB_THRESHOLD"] = 1
# after what time in seconds should generation be aborted, freeing the queue slot. Can be set to None to disable.
app.config["JOB_TIME"] = 600
# memory limit for generator processes in bytes
app.config["GENERATOR_MEMORY_LIMIT"] = 4294967296
app.config['SESSION_PERMANENT'] = True

# waitress uses one thread for I/O, these are for processing of views that then get sent
# archipelago.gg uses gunicorn + nginx; ignoring this option
app.config["WAITRESS_THREADS"] = 10
# a default that just works. archipelago.gg runs on mariadb
app.config["PONY"] = {
    'provider': 'sqlite',
    'filename': os.path.abspath('ap.db3'),
    'create_db': True
}
app.config["MAX_ROLL"] = 20
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["HOST_ADDRESS"] = ""
app.config["ASSET_RIGHTS"] = False

cache = Cache()
Compress(app)


class B64UUIDConverter(BaseConverter):

    def to_python(self, value):
        return uuid.UUID(bytes=base64.urlsafe_b64decode(value + '=='))

    def to_url(self, value):
        return base64.urlsafe_b64encode(value.bytes).rstrip(b'=').decode('ascii')


# short UUID
app.url_map.converters["suuid"] = B64UUIDConverter
app.jinja_env.filters['suuid'] = lambda value: base64.urlsafe_b64encode(value.bytes).rstrip(b'=').decode('ascii')
app.jinja_env.filters["title_sorted"] = title_sorted


def register():
    """Import submodules, triggering their registering on flask routing.
    Note: initializes worlds subsystem."""
    # has automatic patch integration
    import worlds.Files
    app.jinja_env.filters['is_applayercontainer'] = worlds.Files.is_ap_player_container

    from WebHostLib.customserver import run_server_process
    # to trigger app routing picking up on it
    from . import tracker, upload, landing, check, generate, downloads, api, stats, misc, robots, options, session

    app.register_blueprint(api.api_endpoints)
