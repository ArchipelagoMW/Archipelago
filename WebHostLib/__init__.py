import os
import uuid
import base64
import socket

import jinja2.exceptions
from pony.flask import Pony
from flask import Flask, request, redirect, url_for, render_template, Response, session, abort, send_from_directory
from flask import Blueprint
from flask_caching import Cache
from flask_compress import Compress

from .models import *

UPLOAD_FOLDER = os.path.relpath('uploads')
LOGS_FOLDER = os.path.relpath('logs')
os.makedirs(LOGS_FOLDER, exist_ok=True)

app = Flask(__name__)
Pony(app)

app.jinja_env.filters['any'] = any
app.jinja_env.filters['all'] = all

app.config["SELFHOST"] = True
app.config["GENERATORS"] = 8  # maximum concurrent world gens
app.config["SELFLAUNCH"] = True
app.config["DEBUG"] = False
app.config["PORT"] = 80
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4 megabyte limit
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
app.config["CACHE_TYPE"] = "simple"
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


@app.before_request
def register_session():
    session.permanent = True  # technically 31 days after the last visit
    if not session.get("_id", None):
        session["_id"] = uuid4()  # uniquely identify each session without needing a login


@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def page_not_found(err):
    return render_template('404.html'), 404


games_list = {
    "zelda3": ("The Legend of Zelda: A Link to the Past",
               """
               The Legend of Zelda: A Link to the Past is an action/adventure game. Take on the role of Link,
               a boy who is destined to save the land of Hyrule. Delve through three palaces and nine dungeons on
               your quest to rescue the descendents of the seven wise men and defeat the evil Ganon!"""),
    "factorio": ("Factorio",
                 """
                 Factorio is a game about automation. You play as an engineer who has crash landed on the planet
                 Nauvis, an inhospitable world filled with dangerous creatures called biters. Build a factory,
                 research new technologies, and become more efficient in your quest to build a rocket and return home.
                 """),
    "minecraft": ("Minecraft",
                  """
                  Minecraft is a game about creativity. In a world made entirely of cubes, you explore, discover, mine,
                  craft, and try not to explode. Delve deep into the earth and discover abandoned mines, ancient
                  structures, and materials to create a portal to another world. Defeat the Ender Dragon, and claim
                  victory!""")
}


# Player settings pages
@app.route('/games/<game>/player-settings')
def player_settings(game):
    return render_template(f"/games/{game}/playerSettings.html")


# Zelda3 pages
@app.route('/games/zelda3/<string:page>')
def zelda3_pages(page):
    return render_template(f"/games/zelda3/{page}.html")


# Factorio pages
@app.route('/games/factorio/<string:page>')
def factorio_pages(page):
    return render_template(f"/games/factorio/{page}.html")


# Minecraft pages
@app.route('/games/minecraft/<string:page>')
def minecraft_pages(page):
    return render_template(f"/games/factorio/{page}.html")


# Game landing pages
@app.route('/games/<game>')
def game_page(game):
    return render_template(f"/games/{game}/{game}.html")


# List of supported games
@app.route('/games')
def games():
    return render_template("games/games.html", games_list=games_list)


@app.route('/tutorial/<string:game>/<string:file>/<string:lang>')
def tutorial(game, file, lang):
    return render_template("tutorial.html", game=game, file=file, lang=lang)


@app.route('/tutorial')
def tutorial_landing():
    return render_template("tutorialLanding.html")


@app.route('/weighted-settings')
def weighted_settings():
    return render_template("weightedSettings.html")


@app.route('/seed/<suuid:seed>')
def viewSeed(seed: UUID):
    seed = Seed.get(id=seed)
    if not seed:
        abort(404)
    return render_template("viewSeed.html", seed=seed,
                           rooms=[room for room in seed.rooms if room.owner == session["_id"]])


@app.route('/new_room/<suuid:seed>')
def new_room(seed: UUID):
    seed = Seed.get(id=seed)
    if not seed:
        abort(404)
    room = Room(seed=seed, owner=session["_id"], tracker=uuid4())
    commit()
    return redirect(url_for("hostRoom", room=room.id))


def _read_log(path: str):
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as log:
            yield from log
    else:
        yield f"Logfile {path} does not exist. " \
              f"Likely a crash during spinup of multiworld instance or it is still spinning up."


@app.route('/log/<suuid:room>')
def display_log(room: UUID):
    # noinspection PyTypeChecker
    return Response(_read_log(os.path.join("logs", str(room) + ".txt")), mimetype="text/plain;charset=UTF-8")


@app.route('/hosted/<suuid:room>', methods=['GET', 'POST'])
def hostRoom(room: UUID):
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    if request.method == "POST":
        if room.owner == session["_id"]:
            cmd = request.form["cmd"]
            Command(room=room, commandtext=cmd)
            commit()

    with db_session:
        room.last_activity = datetime.utcnow()  # will trigger a spinup, if it's not already running

    return render_template("hostRoom.html", room=room)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


from WebHostLib.customserver import run_server_process
from . import tracker, upload, landing, check, generate, downloads, api  # to trigger app routing picking up on it
app.register_blueprint(api.api_endpoints)
