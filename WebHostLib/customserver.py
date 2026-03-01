from __future__ import annotations

import asyncio
import collections
import datetime
import functools
import logging
import multiprocessing
import pickle
import random
import socket
import threading
import time
import typing
import sys
from asyncio import AbstractEventLoop

import websockets
from pony.orm import commit, db_session, select

import Utils

from MultiServer import (
    Context, server, auto_shutdown, ServerCommandProcessor, ClientMessageProcessor, load_server_cert,
    server_per_message_deflate_factory,
)
from Utils import restricted_loads, cache_argsless
from NetUtils import GamesPackage
from apmw.webhost.customserver.gamespackage.cache import DBGamesPackageCache
from .locker import Locker
from .models import Command, Room, db


class CustomClientMessageProcessor(ClientMessageProcessor):
    ctx: WebHostContext

    def _cmd_video(self, platform: str, user: str):
        """Set a link for your name in the WebHostLib tracker pointing to a video stream.
        Currently, only YouTube and Twitch platforms are supported.
        """
        if platform.lower().startswith("t"):  # twitch
            self.ctx.video[self.client.team, self.client.slot] = "Twitch", user
            self.ctx.save()
            self.output(f"Registered Twitch Stream https://www.twitch.tv/{user}")
            return True
        elif platform.lower().startswith("y"):  # youtube
            self.ctx.video[self.client.team, self.client.slot] = "Youtube", user
            self.ctx.save()
            self.output(f"Registered Youtube Stream for {user}")
            return True
        return False


# inject
import MultiServer

MultiServer.client_message_processor = CustomClientMessageProcessor
del MultiServer


class DBCommandProcessor(ServerCommandProcessor):
    def output(self, text: str):
        self.ctx.logger.info(text)


class WebHostContext(Context):
    room_id: int
    video: dict[tuple[int, int], tuple[str, str]]
    main_loop: AbstractEventLoop
    static_server_data: StaticServerData

    def __init__(
            self,
            static_server_data: StaticServerData,
            games_package_cache: DBGamesPackageCache,
            logger: logging.Logger,
    ) -> None:
        # static server data is used during _load_game_data to load required data,
        # without needing to import worlds system, which takes quite a bit of memory
        super(WebHostContext, self).__init__(
            "",
            0,
            "",
            "",
            1,
            40,
            True,
            "enabled",
            "enabled",
            "enabled",
            0,
            2,
            games_package_cache=games_package_cache,
            logger=logger,
        )
        self.tags = ["AP", "WebHost"]
        self.video = {}
        self.main_loop = asyncio.get_running_loop()
        self.static_server_data = static_server_data
        self.games_package_cache = games_package_cache

    def __del__(self):
        try:
            import psutil
            from Utils import format_SI_prefix
            self.logger.debug(f"Context destroyed, Mem: {format_SI_prefix(psutil.Process().memory_info().rss, 1024)}iB")
        except ImportError:
            self.logger.debug("Context destroyed")

    async def listen_to_db_commands(self):
        cmdprocessor = DBCommandProcessor(self)

        while not self.exit_event.is_set():
            await self.main_loop.run_in_executor(None, self._process_db_commands, cmdprocessor)
            try:
                await asyncio.wait_for(self.exit_event.wait(), 5)
            except asyncio.TimeoutError:
                pass

    def _process_db_commands(self, cmdprocessor):
        with db_session:
            commands = select(command for command in Command if command.room.id == self.room_id)
            if commands:
                for command in commands:
                    self.main_loop.call_soon_threadsafe(cmdprocessor, command.commandtext)
                    command.delete()
                commit()

    @db_session
    def load(self, room_id: int):
        self.room_id = room_id
        room = Room.get(id=room_id)
        if room.last_port:
            self.port = room.last_port
        else:
            self.port = get_random_port()

        multidata = self.decompress(room.seed.multidata)
        return self._load(multidata, True)

    def _load_world_data(self):
        # Use static_server_data, but skip static data package since that is in cache anyway.
        # Also NOT importing worlds here!
        # FIXME: does this copy the non_hintable_names (also for games not part of the room)?
        self.non_hintable_names = collections.defaultdict(frozenset, self.static_server_data["non_hintable_names"])
        del self.static_server_data  # Not used past this point. Free memory.

    def init_save(self, enabled: bool = True):
        self.saving = enabled
        if self.saving:
            with db_session:
                savegame_data = Room.get(id=self.room_id).multisave
                if savegame_data:
                    self.set_save(restricted_loads(savegame_data))
            self._start_async_saving(atexit_save=False)
        asyncio.create_task(self.listen_to_db_commands())

    @db_session
    def _save(self, exit_save: bool = False) -> bool:
        room = Room.get(id=self.room_id)
        # Does not use Utils.restricted_dumps because we'd rather make a save than not make one
        room.multisave = pickle.dumps(self.get_save())
        # saving only occurs on activity, so we can "abuse" this information to mark this as last_activity
        if not exit_save:  # we don't want to count a shutdown as activity, which would restart the server again
            room.last_activity = datetime.datetime.utcnow()
        return True

    def get_save(self) -> dict:
        d = super(WebHostContext, self).get_save()
        d["video"] = [(tuple(playerslot), videodata) for playerslot, videodata in self.video.items()]
        return d


def get_random_port():
    return random.randint(49152, 65535)


class StaticServerData(typing.TypedDict, total=True):
    non_hintable_names: dict[str, typing.AbstractSet[str]]
    games_package: dict[str, GamesPackage]


@cache_argsless
def get_static_server_data() -> StaticServerData:
    import worlds

    return {
        "non_hintable_names": {
            world_name: world.hint_blacklist
            for world_name, world in worlds.AutoWorldRegister.world_types.items()
        },
        "games_package": worlds.network_data_package["games"]
    }


def set_up_logging(room_id) -> logging.Logger:
    import os
    # logger setup
    logger = logging.getLogger(f"RoomLogger {room_id}")

    # this *should* be empty, but just in case.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    file_handler = logging.FileHandler(
        os.path.join(Utils.user_path("logs"), f"{room_id}.txt"),
        "a",
        encoding="utf-8-sig")
    file_handler.setFormatter(logging.Formatter("[%(asctime)s]: %(message)s"))
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger


def tear_down_logging(room_id):
    """Close logging handling for a room."""
    logger_name = f"RoomLogger {room_id}"
    if logger_name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()
        del logging.Logger.manager.loggerDict[logger_name]


def run_server_process(
        name: str,
        ponyconfig: dict[str, typing.Any],
        static_server_data: StaticServerData,
        cert_file: typing.Optional[str],
        cert_key_file: typing.Optional[str],
        host: str,
        rooms_to_run: multiprocessing.Queue,
        rooms_shutting_down: multiprocessing.Queue,
) -> None:
    import gc

    from setproctitle import setproctitle

    setproctitle(name)
    Utils.init_logging(name)
    try:
        import resource
    except ModuleNotFoundError:
        pass  # unix only module
    else:
        # Each Server is another file handle, so request as many as we can from the system
        file_limit = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        # set soft limit to hard limit
        resource.setrlimit(resource.RLIMIT_NOFILE, (file_limit, file_limit))
        del resource, file_limit

    # prime the data package cache with static data
    games_package_cache = DBGamesPackageCache(static_server_data["games_package"])

    # establish DB connection for multidata and multisave
    db.bind(**ponyconfig)
    db.generate_mapping(check_tables=False)

    if "worlds" in sys.modules:
        raise Exception("Worlds system should not be loaded in the custom server.")

    if not cert_file:
        def get_ssl_context():
            return None
    else:
        load_date = None
        ssl_context = load_server_cert(cert_file, cert_key_file)

        def get_ssl_context():
            nonlocal load_date, ssl_context
            today = datetime.date.today()
            if load_date != today:
                ssl_context = load_server_cert(cert_file, cert_key_file)
                load_date = today
            return ssl_context

    del ponyconfig
    gc.collect()  # free intermediate objects used during setup

    loop = asyncio.get_event_loop()

    async def start_room(room_id):
        with Locker(f"RoomLocker {room_id}"):
            try:
                logger = set_up_logging(room_id)
                ctx = WebHostContext(static_server_data, games_package_cache, logger)
                ctx.load(room_id)
                ctx.init_save()
                assert ctx.server is None
                try:
                    ctx.server = websockets.serve(
                        functools.partial(server, ctx=ctx),
                        ctx.host,
                        ctx.port,
                        ssl=get_ssl_context(),
                        extensions=[server_per_message_deflate_factory],
                    )
                    await ctx.server
                except OSError:  # likely port in use
                    ctx.server = websockets.serve(
                        functools.partial(server, ctx=ctx), ctx.host, 0, ssl=get_ssl_context())

                    await ctx.server
                port = 0
                for wssocket in ctx.server.ws_server.sockets:
                    socketname = wssocket.getsockname()
                    if wssocket.family == socket.AF_INET6:
                        # Prefer IPv4, as most users seem to not have working ipv6 support
                        if not port:
                            port = socketname[1]
                    elif wssocket.family == socket.AF_INET:
                        port = socketname[1]
                if port:
                    ctx.logger.info(f'Hosting game at {host}:{port}')
                    with db_session:
                        room = Room.get(id=ctx.room_id)
                        room.last_port = port
                    del room
                else:
                    ctx.logger.exception("Could not determine port. Likely hosting failure.")
                with db_session:
                    ctx.auto_shutdown = Room.get(id=room_id).timeout
                if ctx.saving:
                    setattr(asyncio.current_task(), "save", lambda: ctx._save(True))
                assert ctx.shutdown_task is None
                ctx.shutdown_task = asyncio.create_task(auto_shutdown(ctx, []))
                await ctx.shutdown_task

            except (KeyboardInterrupt, SystemExit):
                if ctx.saving:
                    ctx._save(True)
                    setattr(asyncio.current_task(), "save", None)
            except Exception as e:
                with db_session:
                    room = Room.get(id=room_id)
                    room.last_port = -1
                del room
                logger.exception(e)
                raise
            else:
                if ctx.saving:
                    ctx._save(True)
                    setattr(asyncio.current_task(), "save", None)
            finally:
                try:
                    ctx.save_dirty = False  # make sure the saving thread does not write to DB after final wakeup
                    ctx.exit_event.set()  # make sure the saving thread stops at some point
                    # NOTE: async saving should probably be an async task and could be merged with shutdown_task

                    if ctx.server and hasattr(ctx.server, "ws_server"):
                        ctx.server.ws_server.close()
                        await ctx.server.ws_server.wait_closed()

                    with db_session:
                        # ensure the Room does not spin up again on its own, minute of safety buffer
                        room = Room.get(id=room_id)
                        room.last_activity = datetime.datetime.utcnow() - \
                                             datetime.timedelta(minutes=1, seconds=room.timeout)
                    del room
                    tear_down_logging(room_id)
                    logging.info(f"Shutting down room {room_id} on {name}.")
                finally:
                    await asyncio.sleep(5)
                    rooms_shutting_down.put(room_id)

    class Starter(threading.Thread):
        _tasks: typing.List[asyncio.Future]

        def __init__(self):
            super().__init__()
            self._tasks = []

        def _done(self, task: asyncio.Future):
            self._tasks.remove(task)
            task.result()

        def run(self):
            while 1:
                next_room = rooms_to_run.get(block=True,  timeout=None)
                gc.collect()
                task = asyncio.run_coroutine_threadsafe(start_room(next_room), loop)
                self._tasks.append(task)
                task.add_done_callback(self._done)
                logging.info(f"Starting room {next_room} on {name}.")
                del task  # delete reference to task object

    starter = Starter()
    starter.daemon = True
    starter.start()
    try:
        loop.run_forever()
    finally:
        # save all tasks that want to be saved during shutdown
        for task in asyncio.all_tasks(loop):
            save: typing.Optional[typing.Callable[[], typing.Any]] = getattr(task, "save", None)
            if save:
                save()
