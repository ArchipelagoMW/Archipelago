import os
import multiprocessing
import logging

from WebHost import app as raw_app
from waitress import serve

from WebHost.models import db
from WebHost.autolauncher import autohost

configpath = "config.yaml"


def get_app():
    app = raw_app
    if os.path.exists(configpath):
        import yaml
        with open(configpath) as c:
            app.config.update(yaml.safe_load(c))

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
