from __future__ import annotations
import logging
import multiprocessing
from datetime import timedelta, datetime
import sys
import typing
import time

from pony.orm import db_session, select, commit

from Utils import restricted_loads

class CommonLocker():
    """Uses a file lock to signal that something is already running"""

    def __init__(self, lockname: str):
        self.lockname = lockname
        self.lockfile = f"./{self.lockname}.lck"


class AlreadyRunningException(Exception):
    pass


if sys.platform == 'win32':
    import os

    class Locker(CommonLocker):
        def __enter__(self):
            try:
                if os.path.exists(self.lockfile):
                    os.unlink(self.lockfile)
                self.fp = os.open(
                    self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except OSError as e:
                raise AlreadyRunningException() from e

        def __exit__(self, _type, value, tb):
            fp = getattr(self, "fp", None)
            if fp:
                os.close(self.fp)
                os.unlink(self.lockfile)
else:  # unix
    import fcntl

    class Locker(CommonLocker):
        def __enter__(self):
            try:
                self.fp = open(self.lockfile, "wb")
                fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX)
            except OSError as e:
                raise AlreadyRunningException() from e

        def __exit__(self, _type, value, tb):
            fcntl.flock(self.fp.fileno(), fcntl.LOCK_UN)
            self.fp.close()


def launch_room(room: Room, config: dict):
    # requires db_session!
    if room.last_activity >= datetime.utcnow() - timedelta(seconds=room.timeout):
        multiworld = multiworlds.get(room.id, None)
        if not multiworld:
            multiworld = MultiworldInstance(room, config)

        multiworld.start()


def handle_generation_success(seed_id):
    logging.info(f"Generation finished for seed {seed_id}")


def handle_generation_failure(result: BaseException):
    try:  # hacky way to get the full RemoteTraceback
        raise result
    except Exception as e:
        logging.exception(e)


def launch_generator(pool: multiprocessing.pool.Pool, generation: Generation):
    options = restricted_loads(generation.options)
    logging.info(f"Generating {generation.id} for {len(options)} players")

    meta = restricted_loads(generation.meta)
    pool.apply_async(gen_game, (options,),
                     {"race": meta["race"], "sid": generation.id, "owner": generation.owner},
                     handle_generation_success, handle_generation_failure)
    generation.state = STATE_STARTED


def init_db(pony_config: dict):
    db.bind(**pony_config)
    db.generate_mapping()


def autohost(config: dict):
    def keep_running():
        try:
            with Locker("autohost"):

                with multiprocessing.Pool(config["GENERATORS"], initializer=init_db,
                                          initargs=(config["PONY"],)) as generator_pool:
                    with db_session:
                        to_start = select(generation for generation in Generation if generation.state == STATE_STARTED)

                        if to_start:
                            logging.info("Resuming generation")
                            for generation in to_start:
                                sid = Seed.get(id=generation.id)
                                if sid:
                                    generation.delete()
                                else:
                                    launch_generator(generator_pool, generation)

                            commit()
                        select(generation for generation in Generation if generation.state == STATE_ERROR).delete()

                    while 1:
                        time.sleep(0.50)
                        with db_session:
                            rooms = select(
                                room for room in Room if
                                room.last_activity >= datetime.utcnow() - timedelta(days=3))
                            for room in rooms:
                                launch_room(room, config)
                            to_start = select(
                                generation for generation in Generation if generation.state == STATE_QUEUED)
                            for generation in to_start:
                                launch_generator(generator_pool, generation)
        except AlreadyRunningException:
            pass

    import threading
    threading.Thread(target=keep_running).start()


multiworlds = {}


class MultiworldInstance():
    def __init__(self, room: Room, config: dict):
        self.room_id = room.id
        self.process: typing.Optional[multiprocessing.Process] = None
        multiworlds[self.room_id] = self
        self.ponyconfig = config["PONY"]

    def start(self):
        if self.process and self.process.is_alive():
            return False

        logging.info(f"Spinning up {self.room_id}")
        self.process = multiprocessing.Process(group=None, target=run_server_process,
                                               args=(self.room_id, self.ponyconfig),
                                               name="MultiHost")
        self.process.start()

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None


from .models import Room, Generation, STATE_QUEUED, STATE_STARTED, STATE_ERROR, db, Seed
from .customserver import run_server_process
from .generate import gen_game
