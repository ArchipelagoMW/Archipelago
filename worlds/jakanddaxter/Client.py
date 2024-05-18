import logging
import os
import subprocess
import typing
import asyncio
import colorama

import Utils
from NetUtils import ClientStatus
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled

from worlds.jakanddaxter.GameID import jak1_name
from worlds.jakanddaxter.client.ReplClient import JakAndDaxterReplClient
from worlds.jakanddaxter.client.MemoryReader import JakAndDaxterMemoryReader

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

    # The command processor is not async and cannot use async tasks, so long-running operations
    # like the /repl connect command (which takes 10-15 seconds to compile the game) have to be requested
    # with user-initiated flags. The text client will hang while the operation runs, but at least we can
    # inform the user to wait. The flags are checked by the agents every main_tick.
    def _cmd_repl(self, *arguments: str):
        """Sends a command to the OpenGOAL REPL. Arguments:
        - connect : connect the client to the REPL (goalc).
        - status : check internal status of the REPL."""
        if arguments:
            if arguments[0] == "connect":
                logger.info("This may take a bit... Wait for the success audio cue before continuing!")
                self.ctx.repl.initiated_connect = True
            if arguments[0] == "status":
                self.ctx.repl.print_status()

    def _cmd_memr(self, *arguments: str):
        """Sends a command to the Memory Reader. Arguments:
        - connect : connect the memory reader to the game process (gk).
        - status : check the internal status of the Memory Reader."""
        if arguments:
            if arguments[0] == "connect":
                self.ctx.memr.initiated_connect = True
            if arguments[0] == "status":
                self.ctx.memr.print_status()


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

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(JakAndDaxterContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "ReceivedItems":
            for index, item in enumerate(args["items"], start=args["index"]):
                logger.info(args)
                self.repl.item_inbox[index] = item

    async def ap_inform_location_check(self, location_ids: typing.List[int]):
        message = [{"cmd": "LocationChecks", "locations": location_ids}]
        await self.send_msgs(message)

    def on_location_check(self, location_ids: typing.List[int]):
        create_task_log_exception(self.ap_inform_location_check(location_ids))

    async def ap_inform_finished_game(self):
        if not self.finished_game and self.memr.finished_game:
            message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
            await self.send_msgs(message)
            self.finished_game = True

    def on_finish(self):
        create_task_log_exception(self.ap_inform_finished_game())

    async def run_repl_loop(self):
        while True:
            await self.repl.main_tick()
            await asyncio.sleep(0.1)

    async def run_memr_loop(self):
        while True:
            await self.memr.main_tick(self.on_location_check, self.on_finish)
            await asyncio.sleep(0.1)


async def run_game(ctx: JakAndDaxterContext):
    exec_directory = ""
    try:
        exec_directory = Utils.get_settings()["jakanddaxter_options"]["root_directory"]
        files_in_path = os.listdir(exec_directory)
        if ".git" in files_in_path:
            # Indicates the user is running from source, append expected subdirectory appropriately.
            exec_directory = os.path.join(exec_directory, "out", "build", "Release", "bin")
        else:
            # Indicates the user is running from the official launcher, a mod launcher, or otherwise.
            # We'll need to handle version numbers in the path somehow...
            exec_directory = os.path.join(exec_directory, "versions", "official")
            latest_version = list(reversed(os.listdir(exec_directory)))[0]
            exec_directory = os.path.join(exec_directory, str(latest_version))
    except FileNotFoundError:
        logger.error(f"Unable to locate directory {exec_directory}, "
                     f"unable to locate game executable.")
        return
    except KeyError as e:
        logger.error(f"Hosts.yaml does not contain {e.args[0]}, "
                     f"unable to locate game executable.")
        return

    gk = os.path.join(exec_directory, "gk.exe")
    goalc = os.path.join(exec_directory, "goalc.exe")

    # Don't mind all the arguments, they are exactly what you get when you run "task boot-game" or "task repl".
    await asyncio.create_subprocess_exec(
        gk,
        "-v", "--game jak1", "--", "-boot", "-fakeiso", "-debug",
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stdin=subprocess.DEVNULL)

    # You MUST launch goalc as a console application, so powershell/cmd/bash/etc is the program
    # and goalc is just an argument. It HAS to be this way.
    #  TODO - Support other OS's.
    await asyncio.create_subprocess_exec(
        "powershell.exe",
        goalc, "--user-auto", "--game jak1")

    # Auto connect the repl and memr agents. Sleep 5 because goalc takes just a little bit of time to load,
    # and it's not something we can await.
    logger.info("This may take a bit... Wait for the success audio cue before continuing!")
    await asyncio.sleep(5)
    ctx.repl.initiated_connect = True
    ctx.memr.initiated_connect = True


async def main():
    Utils.init_logging("JakAndDaxterClient", exception_logger="Client")

    ctx = JakAndDaxterContext(None, None)

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.repl_task = create_task_log_exception(ctx.run_repl_loop())
    ctx.memr_task = create_task_log_exception(ctx.run_memr_loop())

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    # Find and run the game (gk) and compiler/repl (goalc).
    # await run_game(ctx)
    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
