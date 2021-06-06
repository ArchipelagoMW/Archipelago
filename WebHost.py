import os
import multiprocessing
import logging

import ModuleUpdate
ModuleUpdate.requirements_files.append(os.path.join("WebHostLib", "requirements.txt"))
ModuleUpdate.update()

from WebHostLib import app as raw_app
from waitress import serve

from WebHostLib.models import db
from WebHostLib.autolauncher import autohost

configpath = os.path.abspath("config.yaml")


def get_app():
    app = raw_app
    if os.path.exists(configpath):
        import yaml
        app.config.from_file(configpath, yaml.safe_load)
        logging.info(f"Updated config from {configpath}")
    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    return app


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)
    app = get_app()
    if app.config["SELFLAUNCH"]:
        autohost(app.config)
    if app.config["SELFHOST"]:  # using WSGI, you just want to run get_app()
        if app.config["DEBUG"]:
            autohost(app.config)
            app.run(debug=True, port=app.config["PORT"])
        else:
            serve(app, port=app.config["PORT"], threads=app.config["WAITRESS_THREADS"])
