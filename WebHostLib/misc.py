import datetime
import os
from typing import List, Dict, Union

import jinja2.exceptions
from flask import request, redirect, url_for, render_template, Response, session, abort, send_from_directory
from pony.orm import count, commit, db_session

from worlds.AutoWorld import AutoWorldRegister
from . import app, cache
from .models import Seed, Room, Command, UUID, uuid4


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
@cache.cached()
def start_playing():
    return render_template(f"startPlaying.html")


# TODO for back compat. remove around 0.4.5
@app.route("/weighted-settings")
def weighted_settings():
    return redirect("weighted-options", 301)


@app.route("/weighted-options")
@cache.cached()
def weighted_options():
    return render_template("weighted-options.html")


# TODO for back compat. remove around 0.4.5
@app.route("/games/<string:game>/player-settings")
def player_settings(game: str):
    return redirect(url_for("player_options", game=game), 301)


# Player options pages
@app.route("/games/<string:game>/player-options")
@cache.cached()
def player_options(game: str):
    return render_template("player-options.html", game=game, theme=get_world_theme(game))


# Game Info Pages
@app.route('/games/<string:game>/info/<string:lang>')
@cache.cached()
def game_info(game, lang):
    return render_template('gameInfo.html', game=game, lang=lang, theme=get_world_theme(game))


# List of supported games
@app.route('/games')
@cache.cached()
def games():
    worlds = {}
    for game, world in AutoWorldRegister.world_types.items():
        if not world.hidden:
            worlds[game] = world
    return render_template("supportedGames.html", worlds=worlds)


@app.route('/tutorial/<string:game>/<string:file>/<string:lang>')
@cache.cached()
def tutorial(game, file, lang):
    return render_template("tutorial.html", game=game, file=file, lang=lang, theme=get_world_theme(game))


@app.route('/tutorial/')
@cache.cached()
def tutorial_landing():
    return render_template("tutorialLanding.html")


@app.route('/faq/<string:lang>/')
@cache.cached()
def faq(lang):
    return render_template("faq.html", lang=lang)


@app.route('/glossary/<string:lang>/')
@cache.cached()
def terms(lang):
    return render_template("glossary.html", lang=lang)


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
        file_path = os.path.join("logs", str(room.id) + ".txt")
        if os.path.exists(file_path):
            return Response(_read_log(file_path), mimetype="text/plain;charset=UTF-8")
        return "Log File does not exist."

    return "Access Denied", 403


@app.route('/room/<suuid:room>', methods=['GET', 'POST'])
def host_room(room: UUID):
    room: Room = Room.get(id=room)
    if room is None:
        return abort(404)
    if request.method == "POST":
        if room.owner == session["_id"]:
            cmd = request.form["cmd"]
            if cmd:
                Command(room=room, commandtext=cmd)
                commit()

    now = datetime.datetime.utcnow()
    # indicate that the page should reload to get the assigned port
    should_refresh = not room.last_port and now - room.creation_time < datetime.timedelta(seconds=3)
    with db_session:
        room.last_activity = now  # will trigger a spinup, if it's not already running

    return render_template("hostRoom.html", room=room, should_refresh=should_refresh)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static", "static"),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/discord')
def discord():
    return redirect("https://discord.gg/8Z65BR2")


@app.route('/datapackage')
@cache.cached()
def get_datapackage():
    """A pretty print version of /api/datapackage"""
    from worlds import network_data_package
    import json
    return Response(json.dumps(network_data_package, indent=4), mimetype="text/plain")


@app.route('/index')
@app.route('/sitemap')
@cache.cached()
def get_sitemap():
    available_games: List[Dict[str, Union[str, bool]]] = []
    for game, world in AutoWorldRegister.world_types.items():
        if not world.hidden:
            has_settings: bool = isinstance(world.web.options_page, bool) and world.web.options_page
            available_games.append({ 'title': game, 'has_settings': has_settings })
    return render_template("siteMap.html", games=available_games)
