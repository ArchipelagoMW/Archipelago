import logging
import typing
import asyncio
import colorama

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled

from .GameID import jak1_name
from .client.ReplClient import JakAndDaxterReplClient
from .client.MemoryReader import JakAndDaxterMemoryReader

import ModuleUpdate
ModuleUpdate.update()


all_tasks = set()


def create_task_log_exception(awaitable: typing.Awaitable) -> asyncio.Task:
    async def _log_exception(a):
        try:
            return await a
        except Exception as e:
            logger.exception(e)
        finally:
            all_tasks.remove(task)
    task = asyncio.create_task(_log_exception(awaitable))
    all_tasks.add(task)
    return task


class JakAndDaxterClientCommandProcessor(ClientCommandProcessor):
    ctx: "JakAndDaxterContext"

    # TODO - Clean up commands related to the REPL, make them more user friendly.
    #  The REPL has a specific order of operations it needs to do in order to process our input:
    #  1. Connect (we need to open a socket connection on ip/port to the REPL).
    #  2. Listen (have the REPL compiler connect and listen on the game's REPL server's socket).
    #  3. Compile (have the REPL compiler compile the game into object code it can run).
    #  All 3 need to be done, and in this order, for this to work.
    def _cmd_repl(self, *arguments: str):
        """Sends a command to the OpenGOAL REPL. Arguments:
        - connect <ip> <port> : connect a new client to the REPL.
        - listen : listen to the game's internal socket.
        - compile : compile the game into executable object code.
        - verify : verify successful compilation."""
        if arguments:
            if arguments[0] == "connect":
                if arguments[1] and arguments[2]:
                    self.ctx.repl.ip = str(arguments[1])
                    self.ctx.repl.port = int(arguments[2])
                    self.ctx.repl.connect()
                else:
                    logging.error("You must provide the ip address and port (default 127.0.0.1 port 8181).")
            if arguments[0] == "listen":
                self.ctx.repl.listen()
            if arguments[0] == "compile":
                self.ctx.repl.compile()
            if arguments[0] == "verify":
                self.ctx.repl.verify()


class JakAndDaxterContext(CommonContext):
    tags = {"AP"}
    game = jak1_name
    items_handling = 0b111  # Full item handling
    command_processor = JakAndDaxterClientCommandProcessor

    # We'll need two agents working in tandem to handle two-way communication with the game.
    # The REPL Client will handle the server->game direction by issuing commands directly to the running game.
    # But the REPL cannot send information back to us, it only ingests information we send it.
    # Luckily OpenGOAL sets up memory addresses to write to, that AutoSplit can read from, for speedrunning.
    # We'll piggyback off this system with a Memory Reader, and that will handle the game->server direction.
    repl: JakAndDaxterReplClient
    memr: JakAndDaxterMemoryReader

    # And two associated tasks, so we have handles on them.
    repl_task: asyncio.Task
    memr_task: asyncio.Task

    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str]) -> None:
        self.repl = JakAndDaxterReplClient()
        self.memr = JakAndDaxterMemoryReader()
        super().__init__(server_address, password)

    def run_gui(self):
        from kvui import GameManager

        class JakAndDaxterManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Jak and Daxter ArchipelaGOAL Client"

        self.ui = JakAndDaxterManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        if cmd == "ReceivedItems":
            for index, item in enumerate(args["items"], start=args["index"]):
                self.repl.item_inbox[index] = item

    async def ap_inform_location_checks(self, location_ids: typing.List[int]):
        message = [{"cmd": "LocationChecks", "locations": location_ids}]
        await self.send_msgs(message)

    def on_locations(self, location_ids: typing.List[int]):
        create_task_log_exception(self.ap_inform_location_checks(location_ids))

    async def run_repl_loop(self):
        await self.repl.main_tick()
        await asyncio.sleep(0.1)

    async def run_memr_loop(self):
        await self.memr.main_tick(self.on_locations)
        await asyncio.sleep(0.1)


async def main():
    Utils.init_logging("JakAndDaxterClient", exception_logger="Client")

    ctx = JakAndDaxterContext(None, None)

    await ctx.repl.init()

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.repl_task = create_task_log_exception(ctx.run_repl_loop())
    ctx.memr_task = create_task_log_exception(ctx.run_memr_loop())

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    colorama.init()
    asyncio.run(main())
    colorama.deinit()