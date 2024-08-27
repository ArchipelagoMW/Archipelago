import os
import subprocess
import colorama

import asyncio
from asyncio import Task

from typing import Set, Awaitable, Optional, List

import pymem
from pymem.exception import ProcessNotFound

import Utils
from NetUtils import ClientStatus
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled
from .JakAndDaxterOptions import EnableOrbsanity

from .GameID import jak1_name
from .client.ReplClient import JakAndDaxterReplClient
from .client.MemoryReader import JakAndDaxterMemoryReader

import ModuleUpdate
ModuleUpdate.update()


all_tasks: Set[Task] = set()


def create_task_log_exception(awaitable: Awaitable) -> asyncio.Task:
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

    # The command processor is not async so long-running operations like the /repl connect command
    # (which takes 10-15 seconds to compile the game) have to be requested with user-initiated flags.
    # The flags are checked by the agents every main_tick.
    def _cmd_repl(self, *arguments: str):
        """Sends a command to the OpenGOAL REPL. Arguments:
        - connect : connect the client to the REPL (goalc).
        - status : check internal status of the REPL."""
        if arguments:
            if arguments[0] == "connect":
                logger.info("This may take a bit... Wait for the success audio cue before continuing!")
                self.ctx.repl.initiated_connect = True
            if arguments[0] == "status":
                create_task_log_exception(self.ctx.repl.print_status())

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

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        self.repl = JakAndDaxterReplClient()
        self.memr = JakAndDaxterMemoryReader()
        # self.repl.load_data()
        # self.memr.load_data()
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

        if cmd == "Connected":
            slot_data = args["slot_data"]
            orbsanity_option = slot_data["enable_orbsanity"]
            if orbsanity_option == EnableOrbsanity.option_per_level:
                orbsanity_bundle = slot_data["level_orbsanity_bundle_size"]
            elif orbsanity_option == EnableOrbsanity.option_global:
                orbsanity_bundle = slot_data["global_orbsanity_bundle_size"]
            else:
                orbsanity_bundle = 1

            # Keep compatibility with 0.0.8 at least for now - TODO: Remove this.
            if "completion_condition" in slot_data:
                goal_id = slot_data["completion_condition"]
            else:
                goal_id = slot_data["jak_completion_condition"]

            create_task_log_exception(
                self.repl.setup_options(orbsanity_option,
                                        orbsanity_bundle,
                                        slot_data["fire_canyon_cell_count"],
                                        slot_data["mountain_pass_cell_count"],
                                        slot_data["lava_tube_cell_count"],
                                        slot_data["citizen_orb_trade_amount"],
                                        slot_data["oracle_orb_trade_amount"],
                                        goal_id))

            # Because Orbsanity and the orb traders in the game are intrinsically linked, we need the server
            # to track our trades at all times to support async play. "Retrieved" will tell us the orbs we lost,
            # while "ReceivedItems" will tell us the orbs we gained. This will give us the correct balance.
            if orbsanity_option in [EnableOrbsanity.option_per_level, EnableOrbsanity.option_global]:
                async def get_orb_balance():
                    await self.send_msgs([{"cmd": "Get", "keys": [f"jakanddaxter_{self.auth}_orbs_paid"]}])

                create_task_log_exception(get_orb_balance())

        if cmd == "Retrieved":
            if f"jakanddaxter_{self.auth}_orbs_paid" in args["keys"]:
                orbs_traded = args["keys"][f"jakanddaxter_{self.auth}_orbs_paid"]
                orbs_traded = orbs_traded if orbs_traded is not None else 0
                create_task_log_exception(self.repl.subtract_traded_orbs(orbs_traded))

        if cmd == "ReceivedItems":
            for index, item in enumerate(args["items"], start=args["index"]):
                logger.debug(f"index: {str(index)}, item: {str(item)}")
                self.repl.item_inbox[index] = item

    async def json_to_game_text(self, args: dict):
        if "type" in args and args["type"] in {"ItemSend"}:
            item = args["item"]
            recipient = args["receiving"]

            # Receiving an item from the server.
            if self.slot_concerns_self(recipient):
                self.repl.my_item_name = self.item_names.lookup_in_game(item.item)

                # Did we find it, or did someone else?
                if self.slot_concerns_self(item.player):
                    self.repl.my_item_finder = "MYSELF"
                else:
                    self.repl.my_item_finder = self.player_names[item.player]

            # Sending an item to the server.
            if self.slot_concerns_self(item.player):
                self.repl.their_item_name = self.item_names.lookup_in_slot(item.item, recipient)

                # Does it belong to us, or to someone else?
                if self.slot_concerns_self(recipient):
                    self.repl.their_item_owner = "MYSELF"
                else:
                    self.repl.their_item_owner = self.player_names[recipient]

            # Write to game display.
            await self.repl.write_game_text()

    def on_print_json(self, args: dict) -> None:

        # Even though N items come in as 1 ReceivedItems packet, there are still N PrintJson packets to process,
        # and they all arrive before the ReceivedItems packet does. Defer processing of these packets as
        # async tasks to speed up large releases of items.
        create_task_log_exception(self.json_to_game_text(args))
        super(JakAndDaxterContext, self).on_print_json(args)

    def on_deathlink(self, data: dict):
        if self.memr.deathlink_enabled:
            self.repl.received_deathlink = True
            super().on_deathlink(data)

    async def ap_inform_location_check(self, location_ids: List[int]):
        message = [{"cmd": "LocationChecks", "locations": location_ids}]
        await self.send_msgs(message)

    def on_location_check(self, location_ids: List[int]):
        create_task_log_exception(self.ap_inform_location_check(location_ids))

    async def ap_inform_finished_game(self):
        if not self.finished_game and self.memr.finished_game:
            message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
            await self.send_msgs(message)
            self.finished_game = True

    def on_finish_check(self):
        create_task_log_exception(self.ap_inform_finished_game())

    async def ap_inform_deathlink(self):
        if self.memr.deathlink_enabled:
            player = self.player_names[self.slot] if self.slot is not None else "Jak"
            death_text = self.memr.cause_of_death.replace("Jak", player)
            await self.send_death(death_text)
            logger.info(death_text)

        # Reset all flags.
        self.memr.send_deathlink = False
        self.memr.cause_of_death = ""
        await self.repl.reset_deathlink()

    def on_deathlink_check(self):
        create_task_log_exception(self.ap_inform_deathlink())

    async def ap_inform_deathlink_toggle(self):
        await self.update_death_link(self.memr.deathlink_enabled)

    def on_deathlink_toggle(self):
        create_task_log_exception(self.ap_inform_deathlink_toggle())

    async def ap_inform_orb_trade(self, orbs_changed: int):
        if self.memr.orbsanity_enabled:
            await self.send_msgs([{"cmd": "Set",
                                   "key": f"jakanddaxter_{self.auth}_orbs_paid",
                                   "default": 0,
                                   "want_reply": False,
                                   "operations": [{"operation": "add", "value": orbs_changed}]
                                   }])

    def on_orb_trade(self, orbs_changed: int):
        create_task_log_exception(self.ap_inform_orb_trade(orbs_changed))

    async def run_repl_loop(self):
        while True:
            await self.repl.main_tick()
            await asyncio.sleep(0.1)

    async def run_memr_loop(self):
        while True:
            await self.memr.main_tick(self.on_location_check,
                                      self.on_finish_check,
                                      self.on_deathlink_check,
                                      self.on_deathlink_toggle,
                                      self.on_orb_trade)
            await asyncio.sleep(0.1)


async def run_game(ctx: JakAndDaxterContext):

    # These may already be running. If they are not running, try to start them.
    gk_running = False
    try:
        pymem.Pymem("gk.exe")  # The GOAL Kernel
        gk_running = True
    except ProcessNotFound:
        logger.info("Game not running, attempting to start.")

    goalc_running = False
    try:
        pymem.Pymem("goalc.exe")  # The GOAL Compiler and REPL
        goalc_running = True
    except ProcessNotFound:
        logger.info("Compiler not running, attempting to start.")

    # Don't mind all the arguments, they are exactly what you get when you run "task boot-game" or "task repl".
    # TODO - Support other OS's. cmd for some reason does not work with goalc. Pymem is Windows-only.
    if not gk_running:
        try:
            gk_path = Utils.get_settings()["jakanddaxter_options"]["root_directory"]
            gk_path = os.path.normpath(gk_path)
            gk_path = os.path.join(gk_path, "gk.exe")
        except AttributeError as e:
            logger.error(f"Hosts.yaml does not contain {e.args[0]}, unable to locate game executables.")
            return

        if gk_path:
            gk_process = subprocess.Popen(
                ["powershell.exe", gk_path, "--game jak1", "--", "-v", "-boot", "-fakeiso", "-debug"],
                creationflags=subprocess.CREATE_NEW_CONSOLE)  # These need to be new consoles for stability.

    if not goalc_running:
        try:
            goalc_path = Utils.get_settings()["jakanddaxter_options"]["root_directory"]
            goalc_path = os.path.normpath(goalc_path)
            goalc_path = os.path.join(goalc_path, "goalc.exe")
        except AttributeError as e:
            logger.error(f"Hosts.yaml does not contain {e.args[0]}, unable to locate game executables.")
            return

        if goalc_path:
            goalc_process = subprocess.Popen(
                ["powershell.exe", goalc_path, "--game jak1"],
                creationflags=subprocess.CREATE_NEW_CONSOLE)  # These need to be new consoles for stability.

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
    await run_game(ctx)
    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
