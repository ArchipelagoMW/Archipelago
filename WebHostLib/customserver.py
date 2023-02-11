from __future__ import annotations

import asyncio
import collections
import datetime
import functools
import logging
import pickle
import random
import socket
import threading
import time
import typing

import websockets
from pony.orm import commit, db_session, select

import Utils

from MultiServer import Context, server, auto_shutdown, ServerCommandProcessor, ClientMessageProcessor, load_server_cert
from Utils import get_public_ipv4, get_public_ipv6, restricted_loads, cache_argsless
from .models import Room, Command, db


class CustomClientMessageProcessor(ClientMessageProcessor):
    ctx: WebHostContext

    def _cmd_video(self, platform, user):
        """Set a link for your name in the WebHostLib tracker pointing to a video stream"""
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
        logging.info(text)


class WebHostContext(Context):
    room_id: int

    def __init__(self, static_server_data: dict):
        # static server data is used during _load_game_data to load required data,
        # without needing to import worlds system, which takes quite a bit of memory
        self.static_server_data = static_server_data
        super(WebHostContext, self).__init__("", 0, "", "", 1, 40, True, "enabled", "enabled", "enabled", 0, 2)
        del self.static_server_data
        self.main_loop = asyncio.get_running_loop()
        self.video = {}
        self.tags = ["AP", "WebHost"]

    def _load_game_data(self):
        for key, value in self.static_server_data.items():
            setattr(self, key, value)
        self.non_hintable_names = collections.defaultdict(frozenset, self.non_hintable_names)

    def listen_to_db_commands(self):
        cmdprocessor = DBCommandProcessor(self)

        while not self.exit_event.is_set():
            with db_session:
                commands = select(command for command in Command if command.room.id == self.room_id)
                if commands:
                    for command in commands:
                        self.main_loop.call_soon_threadsafe(cmdprocessor, command.commandtext)
                        command.delete()
                    commit()
            time.sleep(5)

    @db_session
    def load(self, room_id: int):
        self.room_id = room_id
        room = Room.get(id=room_id)
        if room.last_port:
            self.port = room.last_port
        else:
            self.port = get_random_port()

        return self._load(self.decompress(room.seed.multidata), True)

    @db_session
    def init_save(self, enabled: bool = True):
        self.saving = enabled
        if self.saving:
            savegame_data = Room.get(id=self.room_id).multisave
            if savegame_data:
                self.set_save(restricted_loads(Room.get(id=self.room_id).multisave))
            self._start_async_saving()
        threading.Thread(target=self.listen_to_db_commands, daemon=True).start()

    @db_session
    def _save(self, exit_save: bool = False) -> bool:
        room = Room.get(id=self.room_id)
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


@cache_argsless
def get_static_server_data() -> dict:
    import worlds
    data = {
        "non_hintable_names": {},
        "gamespackage": worlds.network_data_package["games"],
        "item_name_groups": {world_name: world.item_name_groups for world_name, world in
                             worlds.AutoWorldRegister.world_types.items()},
    }

    for world_name, world in worlds.AutoWorldRegister.world_types.items():
        data["non_hintable_names"][world_name] = world.hint_blacklist

    return data


def run_server_process(room_id, ponyconfig: dict, static_server_data: dict,
                       cert_file: typing.Optional[str], cert_key_file: typing.Optional[str]):
    # establish DB connection for multidata and multisave
    db.bind(**ponyconfig)
    db.generate_mapping(check_tables=False)

    async def main():
        Utils.init_logging(str(room_id), write_mode="a")
        ctx = WebHostContext(static_server_data)
        ctx.load(room_id)
        ctx.init_save()
        ssl_context = load_server_cert(cert_file, cert_key_file) if cert_file else None
        try:
            ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, ctx.port, ping_timeout=None,
                                          ping_interval=None, ssl=ssl_context)

            await ctx.server
        except Exception:  # likely port in use - in windows this is OSError, but I didn't check the others
            ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, 0, ping_timeout=None,
                                          ping_interval=None, ssl=ssl_context)

            await ctx.server
        port = 0
        for wssocket in ctx.server.ws_server.sockets:
            socketname = wssocket.getsockname()
            if wssocket.family == socket.AF_INET6:
                logging.info(f'Hosting game at [{get_public_ipv6()}]:{socketname[1]}')
                # Prefer IPv4, as most users seem to not have working ipv6 support
                if not port:
                    port = socketname[1]
            elif wssocket.family == socket.AF_INET:
                logging.info(f'Hosting game at {get_public_ipv4()}:{socketname[1]}')
                port = socketname[1]
        if port:
            with db_session:
                room = Room.get(id=ctx.room_id)
                room.last_port = port
        with db_session:
            ctx.auto_shutdown = Room.get(id=room_id).timeout
        ctx.shutdown_task = asyncio.create_task(auto_shutdown(ctx, []))
        await ctx.shutdown_task
        logging.info("Shutting down")

    from .autolauncher import Locker
    with Locker(room_id):
        try:
            asyncio.run(main())
        except:
            with db_session:
                room = Room.get(id=room_id)
                room.last_port = -1
                # ensure the Room does not spin up again on its own, minute of safety buffer
                room.last_activity = datetime.datetime.utcnow() - datetime.timedelta(minutes=1, seconds=room.timeout)
            raise
