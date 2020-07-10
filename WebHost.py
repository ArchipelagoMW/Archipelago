import os
import multiprocessing
import logging

from WebHost import app
from waitress import serve

from WebHost.models import db, Room, db_session, select

DEBUG = False
port = 80


def autohost(config: dict):
    return
    # not implemented yet. https://github.com/ponyorm/pony/issues/527
    import time
    from datetime import timedelta, datetime

    def keep_running():
        # db.bind(**config["PONY"])
        # db.generate_mapping(check_tables=False)
        while 1:
            time.sleep(3)
            with db_session:
                rooms = select(
                    room for room in Room if
                    room.last_activity >= datetime.utcnow() - timedelta(hours=room.timeout))
                logging.info(rooms)

    import threading
    threading.Thread(target=keep_running).start()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

    configpath = "config.yaml"

    if os.path.exists(configpath):
        import yaml
        with open(configpath) as c:
            app.config.update(yaml.safe_load(c))

        logging.info(f"Updated config from {configpath}")
    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    if DEBUG:
        autohost(app.config)
        app.run(debug=True, port=port)
    else:
        serve(app, port=port, threads=app.config["WAITRESS_THREADS"])
