from __future__ import annotations

import json
import logging
import multiprocessing
import threading
import time
import typing
from datetime import timedelta, datetime

from pony.orm import db_session, select, commit

from Utils import restricted_loads
from .locker import Locker, AlreadyRunningException


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
    try:
        meta = json.loads(generation.meta)
        options = restricted_loads(generation.options)
        logging.info(f"Generating {generation.id} for {len(options)} players")
        pool.apply_async(gen_game, (options,),
                         {"meta": meta,
                          "sid": generation.id,
                          "owner": generation.owner},
                         handle_generation_success, handle_generation_failure)
    except Exception as e:
        generation.state = STATE_ERROR
        commit()
        logging.exception(e)
    else:
        generation.state = STATE_STARTED


def init_db(pony_config: dict):
    db.bind(**pony_config)
    db.generate_mapping()


def autohost(config: dict):
    def keep_running():
        try:
            with Locker("autohost"):
                run_guardian()
                while 1:
                    time.sleep(0.1)
                    with db_session:
                        rooms = select(
                            room for room in Room if
                            room.last_activity >= datetime.utcnow() - timedelta(days=3))
                        for room in rooms:
                            launch_room(room, config)

        except AlreadyRunningException:
            logging.info("Autohost reports as already running, not starting another.")

    import threading
    threading.Thread(target=keep_running, name="AP_Autohost").start()


def autogen(config: dict):
    def keep_running():
        try:
            with Locker("autogen"):

                with multiprocessing.Pool(config["GENERATORS"], initializer=init_db,
                                          initargs=(config["PONY"],), maxtasksperchild=10) as generator_pool:
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
                        time.sleep(0.1)
                        with db_session:
                            # for update locks the database row(s) during transaction, preventing writes from elsewhere
                            to_start = select(
                                generation for generation in Generation
                                if generation.state == STATE_QUEUED).for_update()
                            for generation in to_start:
                                launch_generator(generator_pool, generation)
        except AlreadyRunningException:
            logging.info("Autogen reports as already running, not starting another.")

    import threading
    threading.Thread(target=keep_running, name="AP_Autogen").start()


multiworlds: typing.Dict[type(Room.id), MultiworldInstance] = {}


class MultiworldInstance():
    def __init__(self, room: Room, config: dict):
        self.room_id = room.id
        self.process: typing.Optional[multiprocessing.Process] = None
        with guardian_lock:
            multiworlds[self.room_id] = self
        self.ponyconfig = config["PONY"]
        self.cert = config["SELFLAUNCHCERT"]
        self.key = config["SELFLAUNCHKEY"]
        self.host = config["HOST_ADDRESS"]

    def start(self):
        if self.process and self.process.is_alive():
            return False

        logging.info(f"Spinning up {self.room_id}")
        process = multiprocessing.Process(group=None, target=run_server_process,
                                          args=(self.room_id, self.ponyconfig, get_static_server_data(),
                                                self.cert, self.key, self.host),
                                          name="MultiHost")
        process.start()
        # bind after start to prevent thread sync issues with guardian.
        self.process = process

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def done(self):
        return self.process and not self.process.is_alive()

    def collect(self):
        self.process.join()  # wait for process to finish
        self.process = None


guardian = None
guardian_lock = threading.Lock()


def run_guardian():
    global guardian
    global multiworlds
    with guardian_lock:
        if not guardian:
            try:
                import resource
            except ModuleNotFoundError:
                pass  # unix only module
            else:
                # Each Server is another file handle, so request as many as we can from the system
                file_limit = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
                # set soft limit to hard limit
                resource.setrlimit(resource.RLIMIT_NOFILE, (file_limit, file_limit))

            def guard():
                while 1:
                    time.sleep(1)
                    done = []
                    with guardian_lock:
                        for key, instance in multiworlds.items():
                            if instance.done():
                                instance.collect()
                                done.append(key)
                        for key in done:
                            del (multiworlds[key])

            guardian = threading.Thread(name="Guardian", target=guard)


from .models import Room, Generation, STATE_QUEUED, STATE_STARTED, STATE_ERROR, db, Seed
from .customserver import run_server_process, get_static_server_data
from .generate import gen_game
