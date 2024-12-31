import argparse
import os
import multiprocessing
import logging
import typing

import ModuleUpdate

ModuleUpdate.requirements_files.add(os.path.join("WebHostLib", "requirements.txt"))
ModuleUpdate.update()

# in case app gets imported by something like gunicorn
import Utils
import settings
from Utils import get_file_safe_name

if typing.TYPE_CHECKING:
    from flask import Flask

Utils.local_path.cached_path = os.path.dirname(__file__)
settings.no_gui = True
configpath = os.path.abspath("config.yaml")
if not os.path.exists(configpath):  # fall back to config.yaml in home
    configpath = os.path.abspath(Utils.user_path('config.yaml'))


def get_app() -> "Flask":
    from WebHostLib import register, cache, app as raw_app
    from WebHostLib.models import db

    app = raw_app
    if os.path.exists(configpath) and not app.config["TESTING"]:
        import yaml
        app.config.from_file(configpath, yaml.safe_load)
        logging.info(f"Updated config from {configpath}")
    # inside get_app() so it's usable in systems like gunicorn, which do not run WebHost.py, but import it.
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--config_override', default=None,
                        help="Path to yaml config file that overrules config.yaml.")
    args = parser.parse_known_args()[0]
    if args.config_override:
        import yaml
        app.config.from_file(os.path.abspath(args.config_override), yaml.safe_load)
        logging.info(f"Updated config from {args.config_override}")
    if not app.config["HOST_ADDRESS"]:
        logging.info("Getting public IP, as HOST_ADDRESS is empty.")
        app.config["HOST_ADDRESS"] = Utils.get_public_ipv4()
        logging.info(f"HOST_ADDRESS was set to {app.config['HOST_ADDRESS']}")

    register()
    cache.init_app(app)
    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    return app


def create_ordered_tutorials_file() -> typing.List[typing.Dict[str, typing.Any]]:
    import json
    import shutil
    import zipfile

    zfile: zipfile.ZipInfo

    from worlds.AutoWorld import AutoWorldRegister
    worlds = {}
    data = []
    for game, world in AutoWorldRegister.world_types.items():
        if hasattr(world.web, 'tutorials') and (not world.hidden or game == 'Archipelago'):
            worlds[game] = world

    base_target_path = Utils.local_path("WebHostLib", "static", "generated", "docs")
    shutil.rmtree(base_target_path, ignore_errors=True)
    for game, world in worlds.items():
        # copy files from world's docs folder to the generated folder
        target_path = os.path.join(base_target_path, get_file_safe_name(game))
        os.makedirs(target_path, exist_ok=True)

        if world.zip_path:
            zipfile_path = world.zip_path

            assert os.path.isfile(zipfile_path), f"{zipfile_path} is not a valid file(path)."
            assert zipfile.is_zipfile(zipfile_path), f"{zipfile_path} is not a valid zipfile."

            with zipfile.ZipFile(zipfile_path) as zf:
                for zfile in zf.infolist():
                    if not zfile.is_dir() and "/docs/" in zfile.filename:
                        zfile.filename = os.path.basename(zfile.filename)
                        zf.extract(zfile, target_path)
        else:
            source_path = Utils.local_path(os.path.dirname(world.__file__), "docs")
            files = os.listdir(source_path)
            for file in files:
                shutil.copyfile(Utils.local_path(source_path, file), Utils.local_path(target_path, file))

        # build a json tutorial dict per game
        game_data = {'gameTitle': game, 'tutorials': []}
        for tutorial in world.web.tutorials:
            # build dict for the json file
            current_tutorial = {
                'name': tutorial.tutorial_name,
                'description': tutorial.description,
                'files': [{
                    'language': tutorial.language,
                    'filename': game + '/' + tutorial.file_name,
                    'link': f'{game}/{tutorial.link}',
                    'authors': tutorial.authors
                }]
            }

            # check if the name of the current guide exists already
            for guide in game_data['tutorials']:
                if guide and tutorial.tutorial_name == guide['name']:
                    guide['files'].append(current_tutorial['files'][0])
                    break
            else:
                game_data['tutorials'].append(current_tutorial)

        data.append(game_data)
    with open(Utils.local_path("WebHostLib", "static", "generated", "tutorials.json"), 'w', encoding='utf-8-sig') as json_target:
        generic_data = {}
        for games in data:
            if 'Archipelago' in games['gameTitle']:
                generic_data = data.pop(data.index(games))
        sorted_data = [generic_data] + Utils.title_sorted(data, key=lambda entry: entry["gameTitle"])
        json.dump(sorted_data, json_target, indent=2, ensure_ascii=False)
    return sorted_data


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

    from WebHostLib.lttpsprites import update_sprites_lttp
    from WebHostLib.autolauncher import autohost, autogen, stop
    from WebHostLib.options import create as create_options_files

    try:
        update_sprites_lttp()
    except Exception as e:
        logging.exception(e)
        logging.warning("Could not update LttP sprites.")
    app = get_app()
    create_options_files()
    create_ordered_tutorials_file()
    if app.config["SELFLAUNCH"]:
        autohost(app.config)
    if app.config["SELFGEN"]:
        autogen(app.config)
    if app.config["SELFHOST"]:  # using WSGI, you just want to run get_app()
        if app.config["DEBUG"]:
            app.run(debug=True, port=app.config["PORT"])
        else:
            from waitress import serve
            serve(app, port=app.config["PORT"], threads=app.config["WAITRESS_THREADS"])
    else:
        from time import sleep
        try:
            while True:
                sleep(1)  # wait for process to be killed
        except (SystemExit, KeyboardInterrupt):
            pass
    stop()  # stop worker threads
