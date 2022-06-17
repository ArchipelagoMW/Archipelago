import os
import uuid
import base64
import socket

import jinja2.exceptions
from pony.flask import Pony
from flask import Flask, request, redirect, url_for, render_template, Response, session, abort, send_from_directory
from flask_caching import Cache
from flask_compress import Compress
from worlds.AutoWorld import AutoWorldRegister

from .models import *

UPLOAD_FOLDER = os.path.relpath('uploads')
LOGS_FOLDER = os.path.relpath('logs')
os.makedirs(LOGS_FOLDER, exist_ok=True)

app = Flask(__name__)
Pony(app)

app.jinja_env.filters['any'] = any
app.jinja_env.filters['all'] = all

app.config["SELFHOST"] = True  # application process is in charge of running the websites
app.config["GENERATORS"] = 8  # maximum concurrent world gens
app.config["SELFLAUNCH"] = True  # application process is in charge of launching Rooms.
app.config["SELFGEN"] = True  # application process is in charge of scheduling Generations.
app.config["DEBUG"] = False
app.config["PORT"] = 80
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64 megabyte limit
# if you want to deploy, make sure you have a non-guessable secret key
app.config["SECRET_KEY"] = bytes(socket.gethostname(), encoding="utf-8")
# at what amount of worlds should scheduling be used, instead of rolling in the webthread
app.config["JOB_THRESHOLD"] = 2
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
app.config["CACHE_TYPE"] = "flask_caching.backends.SimpleCache"
app.config["JSON_AS_ASCII"] = False
app.config["PATCH_TARGET"] = "archipelago.gg"

cache = Cache(app)
Compress(app)

from werkzeug.routing import BaseConverter


class B64UUIDConverter(BaseConverter):

    def to_python(self, value):
        return uuid.UUID(bytes=base64.urlsafe_b64decode(value + '=='))

    def to_url(self, value):
        return base64.urlsafe_b64encode(value.bytes).rstrip(b'=').decode('ascii')


# short UUID
app.url_map.converters["suuid"] = B64UUIDConverter
app.jinja_env.filters['suuid'] = lambda value: base64.urlsafe_b64encode(value.bytes).rstrip(b'=').decode('ascii')


def get_world_theme(game_name: str):
    if game_name in AutoWorldRegister.world_types:
        return AutoWorldRegister.world_types[game_name].web.theme
    return 'grass'


@app.before_request
def register_session():
    session.permanent = True  # technically 31 days after the last visit
    if not session.get("_id", None):
        session["_id"] = uuid4()  # uniquely identify each session without needing a login


@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def page_not_found(err):
    return render_template('404.html'), 404


# Start Playing Page
@app.route('/start-playing')
def start_playing():
    return render_template(f"startPlaying.html")


@app.route('/weighted-settings')
def weighted_settings():
    return render_template(f"weighted-settings.html")


# Player settings pages
@app.route('/games/<string:game>/player-settings')
def player_settings(game):
    return render_template(f"player-settings.html", game=game, theme=get_world_theme(game))


# Game Info Pages
@app.route('/games/<string:game>/info/<string:lang>')
def game_info(game, lang):
    return render_template('gameInfo.html', game=game, lang=lang, theme=get_world_theme(game))


# List of supported games
@app.route('/games')
def games():
    worlds = {}
    for game, world in AutoWorldRegister.world_types.items():
        if not world.hidden:
            worlds[game] = world
    return render_template("supportedGames.html", worlds=worlds)


@app.route('/tutorial/<string:game>/<string:file>/<string:lang>')
def tutorial(game, file, lang):
    return render_template("tutorial.html", game=game, file=file, lang=lang, theme=get_world_theme(game))


@app.route('/tutorial/')
def tutorial_landing():
    worlds = {}
    for game, world in AutoWorldRegister.world_types.items():
        if not world.hidden:
            worlds[game] = world
    return render_template("tutorialLanding.html")


@app.route('/faq/<string:lang>/')
def faq(lang):
    return render_template("faq.html", lang=lang)


@app.route('/seed/<suuid:seed>')
def view_seed(seed: UUID):
    seed = Seed.get(id=seed)
    if not seed:
        abort(404)
    return render_template("viewSeed.html", seed=seed, slot_count=count(seed.slots))


@app.route('/new_room/<suuid:seed>')
def new_room(seed: UUID):
    seed = Seed.get(id=seed)
    if not seed:
        abort(404)
    room = Room(seed=seed, owner=session["_id"], tracker=uuid4())
    commit()
    return redirect(url_for("host_room", room=room.id))


def _read_log(path: str):
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as log:
            yield from log
    else:
        yield f"Logfile {path} does not exist. " \
              f"Likely a crash during spinup of multiworld instance or it is still spinning up."


@app.route('/log/<suuid:room>')
def display_log(room: UUID):
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    if room.owner == session["_id"]:
        return Response(_read_log(os.path.join("logs", str(room.id) + ".txt")), mimetype="text/plain;charset=UTF-8")
    return "Access Denied", 403


@app.route('/room/<suuid:room>', methods=['GET', 'POST'])
def host_room(room: UUID):
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    if request.method == "POST":
        if room.owner == session["_id"]:
            cmd = request.form["cmd"]
            if cmd:
                Command(room=room, commandtext=cmd)
                commit()

    with db_session:
        room.last_activity = datetime.utcnow()  # will trigger a spinup, if it's not already running

    return render_template("hostRoom.html", room=room)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/discord')
def discord():
    return redirect("https://discord.gg/archipelago")


@app.route('/datapackage')
@cache.cached()
def get_datapackge():
    """A pretty print version of /api/datapackage"""
    from worlds import network_data_package
    import json
    return Response(json.dumps(network_data_package, indent=4), mimetype="text/plain")


@app.route('/index')
@app.route('/sitemap')
def get_sitemap():
    available_games = []
    for game, world in AutoWorldRegister.world_types.items():
        if not world.hidden:
            available_games.append(game)
    return render_template("siteMap.html", games=available_games)


from WebHostLib.customserver import run_server_process
from . import tracker, upload, landing, check, generate, downloads, api, stats  # to trigger app routing picking up on it

app.register_blueprint(api.api_endpoints)
