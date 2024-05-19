from __future__ import annotations

import json
import logging
import multiprocessing
import typing
from datetime import timedelta, datetime
from threading import Event, Thread
from uuid import UUID

from pony.orm import db_session, select, commit

from Utils import restricted_loads
from .locker import Locker, AlreadyRunningException

_stop_event = Event()


def stop():
    """Stops previously launched threads"""
    global _stop_event
    stop_event = _stop_event
    _stop_event = Event()  # new event for new threads
    stop_event.set()


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


def cleanup():
    """delete unowned user-content"""
    with db_session:
        # >>> bool(uuid.UUID(int=0))
        # True
        rooms = Room.select(lambda room: room.owner == UUID(int=0)).delete(bulk=True)
        seeds = Seed.select(lambda seed: seed.owner == UUID(int=0) and not seed.rooms).delete(bulk=True)
        slots = Slot.select(lambda slot: not slot.seed).delete(bulk=True)
        # Command gets deleted by ponyorm Cascade Delete, as Room is Required
    if rooms or seeds or slots:
        logging.info(f"{rooms} Rooms, {seeds} Seeds and {slots} Slots have been deleted.")


def autohost(config: dict):
    def keep_running():
        stop_event = _stop_event
        try:
            with Locker("autohost"):
                cleanup()
                hosters = []
                for x in range(config["HOSTERS"]):
                    hoster = MultiworldInstance(config, x)
                    hosters.append(hoster)
                    hoster.start()

                while not stop_event.wait(0.1):
                    with db_session:
                        rooms = select(
                            room for room in Room if
                            room.last_activity >= datetime.utcnow() - timedelta(days=3))
                        for room in rooms:
                            # we have to filter twice, as the per-room timeout can't currently be PonyORM transpiled.
                            if room.last_activity >= datetime.utcnow() - timedelta(seconds=room.timeout + 5):
                                hosters[room.id.int % len(hosters)].start_room(room.id)

        except AlreadyRunningException:
            logging.info("Autohost reports as already running, not starting another.")

    Thread(target=keep_running, name="AP_Autohost").start()


def autogen(config: dict):
    def keep_running():
        stop_event = _stop_event
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

                    while not stop_event.wait(0.1):
                        with db_session:
                            # for update locks the database row(s) during transaction, preventing writes from elsewhere
                            to_start = select(
                                generation for generation in Generation
                                if generation.state == STATE_QUEUED).for_update()
                            for generation in to_start:
                                launch_generator(generator_pool, generation)
        except AlreadyRunningException:
            logging.info("Autogen reports as already running, not starting another.")

    Thread(target=keep_running, name="AP_Autogen").start()


multiworlds: typing.Dict[type(Room.id), MultiworldInstance] = {}


class MultiworldInstance():
    def __init__(self, config: dict, id: int):
        self.room_ids = set()
        self.process: typing.Optional[multiprocessing.Process] = None
        self.ponyconfig = config["PONY"]
        self.cert = config["SELFLAUNCHCERT"]
        self.key = config["SELFLAUNCHKEY"]
        self.host = config["HOST_ADDRESS"]
        self.rooms_to_start = multiprocessing.Queue()
        self.rooms_shutting_down = multiprocessing.Queue()
        self.name = f"MultiHoster{id}"

    def start(self):
        if self.process and self.process.is_alive():
            return False

        process = multiprocessing.Process(group=None, target=run_server_process,
                                          args=(self.name, self.ponyconfig, get_static_server_data(),
                                                self.cert, self.key, self.host,
                                                self.rooms_to_start, self.rooms_shutting_down),
                                          name=self.name)
        process.start()
        self.process = process

    def start_room(self, room_id):
        while not self.rooms_shutting_down.empty():
            self.room_ids.remove(self.rooms_shutting_down.get(block=True, timeout=None))
        if room_id in self.room_ids:
            pass  # should already be hosted currently.
        else:
            self.room_ids.add(room_id)
            self.rooms_to_start.put(room_id)

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def done(self):
        return self.process and not self.process.is_alive()

    def collect(self):
        self.process.join()  # wait for process to finish
        self.process = None


from .models import Room, Generation, STATE_QUEUED, STATE_STARTED, STATE_ERROR, db, Seed, Slot
from .customserver import run_server_process, get_static_server_data
from .generate import gen_game
