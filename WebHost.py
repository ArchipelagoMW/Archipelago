import os
import multiprocessing
import logging

import ModuleUpdate

ModuleUpdate.requirements_files.add(os.path.join("WebHostLib", "requirements.txt"))
ModuleUpdate.update()

# in case app gets imported by something like gunicorn
import Utils

Utils.local_path.cached_path = os.path.dirname(__file__)

from WebHostLib import app as raw_app
from waitress import serve

from WebHostLib.models import db
from WebHostLib.autolauncher import autohost, autogen
from WebHostLib.lttpsprites import update_sprites_lttp
from WebHostLib.options import create as create_options_files

from worlds.AutoWorld import AutoWorldRegister

configpath = os.path.abspath("config.yaml")
if not os.path.exists(configpath):  # fall back to config.yaml in home
    configpath = os.path.abspath(Utils.user_path('config.yaml'))


def get_app():
    app = raw_app
    if os.path.exists(configpath):
        import yaml
        app.config.from_file(configpath, yaml.safe_load)
        logging.info(f"Updated config from {configpath}")
    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    return app


def create_ordered_tutorials_file():
    import json
    with open(os.path.join("WebHostLib", "static", "assets", "tutorial", "tutorials.json")) as source:
        data = json.load(source)
    data = sorted(data, key=lambda entry: entry["gameTitle"].lower())
    with open(os.path.join("WebHostLib", "static", "generated", "tutorials.json"), "w") as target:
        json.dump(data, target)


def copy_game_info_files():
    import sys
    files = {}
    worlds = {}
    for game, world in AutoWorldRegister.world_types.items():
        if not world.hidden:
            worlds[game] = world
    for game in worlds:
        source_path = os.path.dirname(sys.modules[worlds[game].__module__].__file__)
        target_path = os.path.join("WebHostLib", "static", "generated", "gameInfo")
        filename = f'en_{game}.md'
        if not os.path.exists(os.path.join(target_path, filename)):
            if os.path.exists(os.path.join(source_path, filename)):
                with open(os.path.join(source_path, filename), 'r') as source:
                    data = source.read()
                with open(os.path.join(target_path, filename), 'w') as target:
                    target.write(data)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)
    try:
        update_sprites_lttp()
    except Exception as e:
        logging.exception(e)
        logging.warning("Could not update LttP sprites.")
    app = get_app()
    create_options_files()
    create_ordered_tutorials_file()
    copy_game_info_files()
    if app.config["SELFLAUNCH"]:
        autohost(app.config)
    if app.config["SELFGEN"]:
        autogen(app.config)
    if app.config["SELFHOST"]:  # using WSGI, you just want to run get_app()
        if app.config["DEBUG"]:
            autohost(app.config)
            app.run(debug=True, port=app.config["PORT"])
        else:
            serve(app, port=app.config["PORT"], threads=app.config["WAITRESS_THREADS"])
