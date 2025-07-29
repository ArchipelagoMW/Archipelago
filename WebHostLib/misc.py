import datetime
import os
from typing import Any, IO, Dict, Iterator, List, Tuple, Union

import jinja2.exceptions
from flask import request, redirect, url_for, render_template, Response, session, abort, send_from_directory
from pony.orm import count, commit, db_session
from werkzeug.utils import secure_filename

from worlds.AutoWorld import AutoWorldRegister
from . import app, cache
from .models import Seed, Room, Command, UUID, uuid4


def get_world_theme(game_name: str):
    if game_name in AutoWorldRegister.world_types:
        return AutoWorldRegister.world_types[game_name].web.theme
    return 'grass'


@app.errorhandler(404)
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def page_not_found(err):
    return render_template('404.html'), 404


# Start Playing Page
@app.route('/start-playing')
@cache.cached()
def start_playing():
    return render_template(f"startPlaying.html")


# Game Info Pages
@app.route('/games/<string:game>/info/<string:lang>')
@cache.cached()
def game_info(game, lang):
    try:
        world = AutoWorldRegister.world_types[game]
        if lang not in world.web.game_info_languages:
            raise KeyError("Sorry, this game's info page is not available in that language yet.")
    except KeyError:
        return abort(404)
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
    try:
        world = AutoWorldRegister.world_types[game]
        if lang not in [tut.link.split("/")[1] for tut in world.web.tutorials]:
            raise KeyError("Sorry, the tutorial is not available in that language yet.")
    except KeyError:
        return abort(404)
    return render_template("tutorial.html", game=game, file=file, lang=lang, theme=get_world_theme(game))


@app.route('/tutorial/')
@cache.cached()
def tutorial_landing():
    return render_template("tutorialLanding.html")


@app.route('/faq/<string:lang>/')
@cache.cached()
def faq(lang: str):
    import markdown
    with open(os.path.join(app.static_folder, "assets", "faq", secure_filename(lang)+".md")) as f:
        document = f.read()
    return render_template(
        "markdown_document.html",
        title="Frequently Asked Questions",
        html_from_markdown=markdown.markdown(
            document,
            extensions=["toc", "mdx_breakless_lists"],
            extension_configs={
                "toc": {"anchorlink": True}
            }
        ),
    )


@app.route('/glossary/<string:lang>/')
@cache.cached()
def glossary(lang: str):
    import markdown
    with open(os.path.join(app.static_folder, "assets", "glossary", secure_filename(lang)+".md")) as f:
        document = f.read()
    return render_template(
        "markdown_document.html",
        title="Glossary",
        html_from_markdown=markdown.markdown(
            document,
            extensions=["toc", "mdx_breakless_lists"],
            extension_configs={
                "toc": {"anchorlink": True}
            }
        ),
    )


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


def _read_log(log: IO[Any], offset: int = 0) -> Iterator[bytes]:
    marker = log.read(3)  # skip optional BOM
    if marker != b'\xEF\xBB\xBF':
        log.seek(0, os.SEEK_SET)
    log.seek(offset, os.SEEK_CUR)
    yield from log
    log.close()  # free file handle as soon as possible


@app.route('/log/<suuid:room>')
def display_log(room: UUID) -> Union[str, Response, Tuple[str, int]]:
    room = Room.get(id=room)
    if room is None:
        return abort(404)
    if room.owner == session["_id"]:
        file_path = os.path.join("logs", str(room.id) + ".txt")
        try:
            log = open(file_path, "rb")
            range_header = request.headers.get("Range")
            if range_header:
                range_type, range_values = range_header.split('=')
                start, end = map(str.strip, range_values.split('-', 1))
                if range_type != "bytes" or end != "":
                    return "Unsupported range", 500
                # NOTE: we skip Content-Range in the response here, which isn't great but works for our JS
                return Response(_read_log(log, int(start)), mimetype="text/plain", status=206)
            return Response(_read_log(log), mimetype="text/plain")
        except FileNotFoundError:
            return Response(f"Logfile {file_path} does not exist. "
                            f"Likely a crash during spinup of multiworld instance or it is still spinning up.",
                            mimetype="text/plain")

    return "Access Denied", 403


@app.post("/room/<suuid:room>")
def host_room_command(room: UUID):
    room: Room = Room.get(id=room)
    if room is None:
        return abort(404)

    if room.owner == session["_id"]:
        cmd = request.form["cmd"]
        if cmd:
            Command(room=room, commandtext=cmd)
            commit()
    return redirect(url_for("host_room", room=room.id))


@app.get("/room/<suuid:room>")
def host_room(room: UUID):
    room: Room = Room.get(id=room)
    if room is None:
        return abort(404)

    now = datetime.datetime.utcnow()
    # indicate that the page should reload to get the assigned port
    should_refresh = ((not room.last_port and now - room.creation_time < datetime.timedelta(seconds=3))
                      or room.last_activity < now - datetime.timedelta(seconds=room.timeout))
    with db_session:
        room.last_activity = now  # will trigger a spinup, if it's not already running

    browser_tokens = "Mozilla", "Chrome", "Safari"
    automated = ("update" in request.args
                 or "Discordbot" in request.user_agent.string
                 or not any(browser_token in request.user_agent.string for browser_token in browser_tokens))

    def get_log(max_size: int = 0 if automated else 1024000) -> str:
        if max_size == 0:
            return "…"
        try:
            with open(os.path.join("logs", str(room.id) + ".txt"), "rb") as log:
                raw_size = 0
                fragments: List[str] = []
                for block in _read_log(log):
                    if raw_size + len(block) > max_size:
                        fragments.append("…")
                        break
                    raw_size += len(block)
                    fragments.append(block.decode("utf-8"))
                return "".join(fragments)
        except FileNotFoundError:
            return ""

    return render_template("hostRoom.html", room=room, should_refresh=should_refresh, get_log=get_log)


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
