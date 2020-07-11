from __future__ import annotations
import logging
import multiprocessing
from datetime import timedelta, datetime
import sys
import typing

from pony.orm import db_session, select


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


def autohost(config: dict):
    import time

    def keep_running():
        try:
            with Locker("autohost"):
                logging.info("Starting autohost service")
                # db.bind(**config["PONY"])
                # db.generate_mapping(check_tables=False)
                while 1:
                    time.sleep(3)
                    with db_session:
                        rooms = select(
                            room for room in Room if
                            room.last_activity >= datetime.utcnow() - timedelta(days=3))
                        for room in rooms:
                            launch_room(room, config)

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


from .models import Room
from .customserver import run_server_process
