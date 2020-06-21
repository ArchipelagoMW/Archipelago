import functools
import logging
import os
import websockets
import asyncio
import socket
import threading
import time
import random

from WebHost import LOGS_FOLDER
from .models import *

from MultiServer import Context, server, auto_shutdown, ServerCommandProcessor
from Utils import get_public_ipv4, get_public_ipv6


class DBCommandProcessor(ServerCommandProcessor):
    def output(self, text: str):
        logging.info(text)


class WebHostContext(Context):
    def __init__(self):
        super(WebHostContext, self).__init__("", 0, "", 1, 40, True, "enabled", "enabled", 0)
        self.main_loop = asyncio.get_running_loop()

    def listen_to_db_commands(self):
        cmdprocessor = DBCommandProcessor(self)

        while self.running:
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
        return self._load(room.seed.multidata, True)

    @db_session
    def init_save(self, enabled: bool = True):
        self.saving = enabled
        if self.saving:
            existings_savegame = Room.get(id=self.room_id).multisave
            if existings_savegame:
                self.set_save(existings_savegame)
            self._start_async_saving()
        threading.Thread(target=self.listen_to_db_commands, daemon=True).start()

    @db_session
    def _save(self) -> bool:
        Room.get(id=self.room_id).multisave = self.get_save()
        return True


def get_random_port():
    return random.randint(49152, 65535)

def run_server_process(room_id, ponyconfig: dict):
    # establish DB connection for multidata and multisave
    db.bind(**ponyconfig)
    db.generate_mapping(check_tables=False)

    async def main():

        logging.basicConfig(format='[%(asctime)s] %(message)s',
                            level=logging.INFO,
                            filename=os.path.join(LOGS_FOLDER, f"{room_id}.txt"))
        ctx = WebHostContext()
        ctx.load(room_id)
        ctx.auto_shutdown = 24 * 60 * 60  # 24 hours
        ctx.init_save()

        try:
            ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, ctx.port, ping_timeout=None,
                                          ping_interval=None)

            await ctx.server
        except Exception:  # likely port in use - in windows this is OSError, but I didn't check the others
            ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, 0, ping_timeout=None,
                                          ping_interval=None)

            await ctx.server
        for wssocket in ctx.server.ws_server.sockets:
            socketname = wssocket.getsockname()
            if wssocket.family == socket.AF_INET6:
                logging.info(f'Hosting game at [{get_public_ipv6()}]:{socketname[1]}')
                with db_session:
                    room = Room.get(id=ctx.room_id)
                    room.last_port = socketname[1]
            elif wssocket.family == socket.AF_INET:
                logging.info(f'Hosting game at {get_public_ipv4()}:{socketname[1]}')
        ctx.auto_shutdown = 6 * 60
        ctx.shutdown_task = asyncio.create_task(auto_shutdown(ctx, []))
        await ctx.shutdown_task
        logging.info("Shutting down")

    asyncio.run(main())
