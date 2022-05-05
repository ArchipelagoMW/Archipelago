import os
import sys
import multiprocessing
import logging
import typing

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

from worlds.AutoWorld import AutoWorldRegister, WebWorld

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


def create_ordered_tutorials_file() -> typing.List[typing.Dict[str, typing.Any]]:
    import json
    import shutil
    worlds = {}
    target_path = Utils.local_path("WebHostLib", "static", "generated", "tutorials")
    data = []
    for game, world in AutoWorldRegister.world_types.items():
        if hasattr(world.web, 'tutorials'):
            worlds[game] = world
    for game, world in worlds.items():
        game_data = {}
        game_data['gameTitle'] = game
        game_data['tutorials'] = [{}]
        for tutorial in world.web.tutorials:
            # build dict for the json file
            current_tutorial = {
                'name': tutorial.tutorial_name,
                'description': tutorial.description,
                'files': [{
                    'language': tutorial.language,
                    'filename': game + '/' + tutorial.file_name,
                    'link': f'{game}/{tutorial.link}',
                    'authors': tutorial.author
                }]
            }
            added: bool = False
            if 'name' in game_data['tutorials'][0]:
                for guide in game_data['tutorials']:
                    if tutorial.tutorial_name in guide['name']:
                        guide['files'].append(current_tutorial['files'][0])
                        added = True
                if not added:
                    game_data['tutorials'].append(current_tutorial)
            else:
                game_data['tutorials'][0] = current_tutorial
            # copy the tutorial files to the generated folder
            source_file = Utils.local_path(os.path.dirname(sys.modules[world.__module__].__file__), 'docs', tutorial.file_name)
            target_file = Utils.local_path(target_path, game, tutorial.file_name)
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            shutil.copyfile(source_file, target_file)
        data.append(game_data)
    with open(Utils.local_path("WebHostLib", "static", "generated", "tutorials.json"), 'w') as json_target:
        generic_data = {}
        for games in data:
            if 'Archipelago' in games.values():
                generic_data = data.pop(data.index(games))
        sorted_data = [generic_data] + sorted(data, key=lambda entry: entry["gameTitle"].lower())
        json.dump(sorted_data, json_target, indent=2)
    return sorted_data


def copy_game_info_files():
    worlds = {}
    for game, world in AutoWorldRegister.world_types.items():
        if not world.hidden:
            worlds[game] = world
    target_path = os.path.join("WebHostLib", "static", "generated", "gameInfo")
    for game in worlds:
        source_path = os.path.join(os.path.dirname(sys.modules[worlds[game].__module__].__file__), 'docs')
        languages = [lang for lang in worlds[game].web.game_info_languages]
        for lang in languages:
            filename = f'{lang}_{game}_gameinfo.md'
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
    # TODO create a proper hook for world documents so they don't need to be copied
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
