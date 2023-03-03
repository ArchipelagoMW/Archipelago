from __future__ import annotations
import os
import logging
import json
import string
import copy
import re
import subprocess
import sys
import time
import random
import typing

import ModuleUpdate
ModuleUpdate.update()

import factorio_rcon
import colorama
import asyncio
from queue import Queue
import Utils

def check_stdin() -> None:
    if Utils.is_windows and sys.stdin:
        print("WARNING: Console input is not routed reliably on Windows, use the GUI instead.")

if __name__ == "__main__":
    Utils.init_logging("FactorioClient", exception_logger="Client")
    check_stdin()

from CommonClient import CommonContext, server_loop, ClientCommandProcessor, logger, gui_enabled, get_base_parser
from MultiServer import mark_raw
from NetUtils import NetworkItem, ClientStatus, JSONtoTextParser, JSONMessagePart
from Utils import async_start

from worlds.factorio import Factorio


class FactorioCommandProcessor(ClientCommandProcessor):
    ctx: FactorioContext

    def _cmd_energy_link(self):
        """Print the status of the energy link."""
        self.output(f"Energy Link: {self.ctx.energy_link_status}")

    @mark_raw
    def _cmd_factorio(self, text: str) -> bool:
        """Send the following command to the bound Factorio Server."""
        if self.ctx.rcon_client:
            # TODO: Print the command non-silently only for race seeds, or otherwise block anything but /factorio /save in race seeds.
            self.ctx.print_to_game(f"/factorio {text}")
            result = self.ctx.rcon_client.send_command(text)
            if result:
                self.output(result)
            return True
        return False

    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.ctx.awaiting_bridge = True

    def _cmd_toggle_send_filter(self):
        """Toggle filtering of item sends that get displayed in-game to only those that involve you."""
        self.ctx.toggle_filter_item_sends()

    def _cmd_toggle_chat(self):
        """Toggle sending of chat messages from players on the Factorio server to Archipelago."""
        self.ctx.toggle_bridge_chat_out()

class FactorioContext(CommonContext):
    command_processor = FactorioCommandProcessor
    game = "Factorio"
    items_handling = 0b111  # full remote

    # updated by spinup server
    mod_version: Utils.Version = Utils.Version(0, 0, 0)

    def __init__(self, server_address, password):
        super(FactorioContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.rcon_client = None
        self.awaiting_bridge = False
        self.write_data_path = None
        self.death_link_tick: int = 0  # last send death link on Factorio layer
        self.factorio_json_text_parser = FactorioJSONtoTextParser(self)
        self.energy_link_increment = 0
        self.last_deplete = 0
        self.filter_item_sends: bool = False
        self.multiplayer: bool = False  # whether multiple different players have connected
        self.bridge_chat_out: bool = True

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(FactorioContext, self).server_auth(password_requested)

        if self.rcon_client:
            await get_info(self, self.rcon_client)  # retrieve current auth code
        else:
            raise Exception("Cannot connect to a server with unknown own identity, "
                            "bridge to Factorio first.")

        await self.send_connect()

    def on_print(self, args: dict):
        super(FactorioContext, self).on_print(args)
        if self.rcon_client:
            if not args['text'].startswith(self.player_names[self.slot] + ":"):
                self.print_to_game(args['text'])

    def on_print_json(self, args: dict):
        if self.rcon_client:
            if (not self.filter_item_sends or not self.is_uninteresting_item_send(args)) \
                    and not self.is_echoed_chat(args):
                text = self.factorio_json_text_parser(copy.deepcopy(args["data"]))
                if not text.startswith(self.player_names[self.slot] + ":"): # TODO: Remove string heuristic in the future.
                    self.print_to_game(text)
        super(FactorioContext, self).on_print_json(args)

    @property
    def savegame_name(self) -> str:
        return f"AP_{self.seed_name}_{self.auth}_Save.zip"

    def print_to_game(self, text):
        self.rcon_client.send_command(f"/ap-print [font=default-large-bold]Archipelago:[/font] "
                                      f"{text}")

    @property
    def energy_link_status(self) -> str:
        if not self.energy_link_increment:
            return "Disabled"
        elif self.current_energy_link_value is None:
            return "Standby"
        else:
            return f"{Utils.format_SI_prefix(self.current_energy_link_value)}J"

    def on_deathlink(self, data: dict):
        if self.rcon_client:
            self.rcon_client.send_command(f"/ap-deathlink {data['source']}")
        super(FactorioContext, self).on_deathlink(data)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected", "RoomUpdate"}:
            # catch up sync anything that is already cleared.
            if "checked_locations" in args and args["checked_locations"]:
                self.rcon_client.send_commands({item_name: f'/ap-get-technology ap-{item_name}-\t-1' for
                                                item_name in args["checked_locations"]})
            if cmd == "Connected" and self.energy_link_increment:
                async_start(self.send_msgs([{
                    "cmd": "SetNotify", "keys": ["EnergyLink"]
                }]))
        elif cmd == "SetReply":
            if args["key"] == "EnergyLink":
                if self.energy_link_increment and args.get("last_deplete", -1) == self.last_deplete:
                    # it's our deplete request
                    gained = int(args["original_value"] - args["value"])
                    gained_text = Utils.format_SI_prefix(gained) + "J"
                    if gained:
                        logger.debug(f"EnergyLink: Received {gained_text}. "
                                     f"{Utils.format_SI_prefix(args['value'])}J remaining.")
                        self.rcon_client.send_command(f"/ap-energylink {gained}")

    def on_user_say(self, text: str) -> typing.Optional[str]:
        # Mirror chat sent from the UI to the Factorio server.
        self.print_to_game(f"{self.player_names[self.slot]}: {text}")
        return text

    async def chat_from_factorio(self, user: str, message: str) -> None:
        if not self.bridge_chat_out:
            return

        # Pass through commands
        if message.startswith("!"):
            await self.send_msgs([{"cmd": "Say", "text": message}])
            return

        # Omit messages that contain local coordinates
        if "[gps=" in message:
            return

        prefix = f"({user}) " if self.multiplayer else ""
        await self.send_msgs([{"cmd": "Say", "text": f"{prefix}{message}"}])

    def toggle_filter_item_sends(self) -> None:
        self.filter_item_sends = not self.filter_item_sends
        if self.filter_item_sends:
            announcement = "Item sends are now filtered."
        else:
            announcement = "Item sends are no longer filtered."
        logger.info(announcement)
        self.print_to_game(announcement)

    def toggle_bridge_chat_out(self) -> None:
        self.bridge_chat_out = not self.bridge_chat_out
        if self.bridge_chat_out:
            announcement = "Chat is now bridged to Archipelago."
        else:
            announcement = "Chat is no longer bridged to Archipelago."
        logger.info(announcement)
        self.print_to_game(announcement)

    def run_gui(self):
        from kvui import GameManager

        class FactorioManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("FactorioServer", "Factorio Server Log"),
                ("FactorioWatcher", "Bridge Data Log"),
            ]
            base_title = "Archipelago Factorio Client"

        self.ui = FactorioManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def game_watcher(ctx: FactorioContext):
    bridge_logger = logging.getLogger("FactorioWatcher")
    next_bridge = time.perf_counter() + 1
    try:
        while not ctx.exit_event.is_set():
            # TODO: restore on-demand refresh
            if ctx.rcon_client and time.perf_counter() > next_bridge:
                next_bridge = time.perf_counter() + 1
                ctx.awaiting_bridge = False
                data = json.loads(ctx.rcon_client.send_command("/ap-sync"))
                if not ctx.auth:
                    pass  # auth failed, wait for new attempt
                elif data["slot_name"] != ctx.auth:
                    bridge_logger.warning(f"Connected World is not the expected one {data['slot_name']} != {ctx.auth}")
                elif data["seed_name"] != ctx.seed_name:
                    bridge_logger.warning(
                        f"Connected Multiworld is not the expected one {data['seed_name']} != {ctx.seed_name}")
                else:
                    data = data["info"]
                    research_data = data["research_done"]
                    research_data = {int(tech_name.split("-")[1]) for tech_name in research_data}
                    victory = data["victory"]
                    await ctx.update_death_link(data["death_link"])
                    ctx.multiplayer = data.get("multiplayer", False)

                    if not ctx.finished_game and victory:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True

                    if ctx.locations_checked != research_data:
                        bridge_logger.debug(
                            f"New researches done: "
                            f"{[ctx.location_names[rid] for rid in research_data - ctx.locations_checked]}")
                        ctx.locations_checked = research_data
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": tuple(research_data)}])
                    death_link_tick = data.get("death_link_tick", 0)
                    if death_link_tick != ctx.death_link_tick:
                        ctx.death_link_tick = death_link_tick
                        if "DeathLink" in ctx.tags:
                            async_start(ctx.send_death())
                    if ctx.energy_link_increment:
                        in_world_bridges = data["energy_bridges"]
                        if in_world_bridges:
                            in_world_energy = data["energy"]
                            if in_world_energy < (ctx.energy_link_increment * in_world_bridges):
                                # attempt to refill
                                ctx.last_deplete = time.time()
                                async_start(ctx.send_msgs([{
                                    "cmd": "Set", "key": "EnergyLink", "operations":
                                        [{"operation": "add", "value": -ctx.energy_link_increment * in_world_bridges},
                                         {"operation": "max", "value": 0}],
                                    "last_deplete": ctx.last_deplete
                                }]))
                            # Above Capacity - (len(Bridges) * ENERGY_INCREMENT)
                            elif in_world_energy > (in_world_bridges * ctx.energy_link_increment * 5) - \
                                ctx.energy_link_increment*in_world_bridges:
                                value = ctx.energy_link_increment * in_world_bridges
                                async_start(ctx.send_msgs([{
                                    "cmd": "Set", "key": "EnergyLink", "operations":
                                        [{"operation": "add", "value": value}]
                                }]))
                                ctx.rcon_client.send_command(
                                    f"/ap-energylink -{value}")
                                logger.debug(f"EnergyLink: Sent {Utils.format_SI_prefix(value)}J")

            await asyncio.sleep(0.1)

    except Exception as e:
        logging.exception(e)
        logging.error("Aborted Factorio Server Bridge")


def stream_factorio_output(pipe, queue, process):
    pipe.reconfigure(errors="replace")

    def queuer():
        while process.poll() is None:
            text = pipe.readline().strip()
            if text:
                queue.put_nowait(text)

    from threading import Thread

    thread = Thread(target=queuer, name="Factorio Output Queue", daemon=True)
    thread.start()
    return thread


async def factorio_server_watcher(ctx: FactorioContext):
    savegame_name = os.path.abspath(ctx.savegame_name)
    if not os.path.exists(savegame_name):
        logger.info(f"Creating savegame {savegame_name}")
        subprocess.run((
            executable, "--create", savegame_name, "--preset", "archipelago"
        ))
    factorio_process = subprocess.Popen((executable, "--start-server", ctx.savegame_name,
                                         *(str(elem) for elem in server_args)),
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.DEVNULL,
                                        encoding="utf-8")
    factorio_server_logger.info("Started Factorio Server")
    factorio_queue = Queue()
    stream_factorio_output(factorio_process.stdout, factorio_queue, factorio_process)
    stream_factorio_output(factorio_process.stderr, factorio_queue, factorio_process)
    try:
        while not ctx.exit_event.is_set():
            if factorio_process.poll() is not None:
                factorio_server_logger.info("Factorio server has exited.")
                ctx.exit_event.set()

            while not factorio_queue.empty():
                msg = factorio_queue.get()
                factorio_queue.task_done()

                if not ctx.rcon_client and "Starting RCON interface at IP ADDR:" in msg:
                    ctx.rcon_client = factorio_rcon.RCONClient("localhost", rcon_port, rcon_password)
                    if not ctx.server:
                        logger.info("Established bridge to Factorio Server. "
                                    "Ready to connect to Archipelago via /connect")
                        check_stdin()

                if not ctx.awaiting_bridge and "Archipelago Bridge Data available for game tick " in msg:
                    ctx.awaiting_bridge = True
                    factorio_server_logger.debug(msg)
                elif re.match(r"^[0-9.]+ Script @[^ ]+\.lua:\d+: Player command energy-link$", msg):
                    factorio_server_logger.debug(msg)
                    ctx.print_to_game(f"Energy Link: {ctx.energy_link_status}")
                elif re.match(r"^[0-9.]+ Script @[^ ]+\.lua:\d+: Player command toggle-ap-send-filter$", msg):
                    factorio_server_logger.debug(msg)
                    ctx.toggle_filter_item_sends()
                elif re.match(r"^[0-9.]+ Script @[^ ]+\.lua:\d+: Player command toggle-ap-chat$", msg):
                    factorio_server_logger.debug(msg)
                    ctx.toggle_bridge_chat_out()
                else:
                    factorio_server_logger.info(msg)
                    match = re.match(r"^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d \[CHAT\] ([^:]+): (.*)$", msg)
                    if match:
                        await ctx.chat_from_factorio(match.group(1), match.group(2))
            if ctx.rcon_client:
                commands = {}
                while ctx.send_index < len(ctx.items_received):
                    transfer_item: NetworkItem = ctx.items_received[ctx.send_index]
                    item_id = transfer_item.item
                    player_name = ctx.player_names[transfer_item.player]
                    if item_id not in Factorio.item_id_to_name:
                        factorio_server_logger.error(f"Cannot send unknown item ID: {item_id}")
                    else:
                        item_name = Factorio.item_id_to_name[item_id]
                        factorio_server_logger.info(f"Sending {item_name} to Nauvis from {player_name}.")
                        commands[ctx.send_index] = f'/ap-get-technology {item_name}\t{ctx.send_index}\t{player_name}'
                    ctx.send_index += 1
                if commands:
                    ctx.rcon_client.send_commands(commands)
            await asyncio.sleep(0.1)

    except Exception as e:
        logging.exception(e)
        logging.error("Aborted Factorio Server Bridge")
        ctx.exit_event.set()

    finally:
        if factorio_process.poll() is not None:
            if ctx.rcon_client:
                ctx.rcon_client.close()
                ctx.rcon_client = None
            return

        sent_quit = False
        if ctx.rcon_client:
            # Attempt clean quit through RCON.
            try:
                ctx.rcon_client.send_command("/quit")
            except factorio_rcon.RCONNetworkError:
                pass
            else:
                sent_quit = True
            ctx.rcon_client.close()
            ctx.rcon_client = None
        if not sent_quit:
            # Attempt clean quit using SIGTERM. (Note that on Windows this kills the process instead.)
            factorio_process.terminate()

        try:
            factorio_process.wait(10)
        except subprocess.TimeoutExpired:
            factorio_process.kill()


async def get_info(ctx: FactorioContext, rcon_client: factorio_rcon.RCONClient):
    info = json.loads(rcon_client.send_command("/ap-rcon-info"))
    ctx.auth = info["slot_name"]
    ctx.seed_name = info["seed_name"]
    # 0.2.0 addition, not present earlier
    death_link = bool(info.get("death_link", False))
    ctx.energy_link_increment = info.get("energy_link", 0)
    logger.debug(f"Energy Link Increment: {ctx.energy_link_increment}")
    if ctx.energy_link_increment and ctx.ui:
        ctx.ui.enable_energy_link()
    await ctx.update_death_link(death_link)


async def factorio_spinup_server(ctx: FactorioContext) -> bool:
    savegame_name = os.path.abspath("Archipelago.zip")
    if not os.path.exists(savegame_name):
        logger.info(f"Creating savegame {savegame_name}")
        subprocess.run((
            executable, "--create", savegame_name
        ))
    factorio_process = subprocess.Popen(
        (executable, "--start-server", savegame_name, *(str(elem) for elem in server_args)),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        encoding="utf-8")
    factorio_server_logger.info("Started Information Exchange Factorio Server")
    factorio_queue = Queue()
    stream_factorio_output(factorio_process.stdout, factorio_queue, factorio_process)
    stream_factorio_output(factorio_process.stderr, factorio_queue, factorio_process)
    rcon_client = None
    try:
        while not ctx.auth:
            while not factorio_queue.empty():
                msg = factorio_queue.get()
                factorio_server_logger.info(msg)
                if "Loading mod AP-" in msg and msg.endswith("(data.lua)"):
                    parts = msg.split()
                    ctx.mod_version = Utils.Version(*(int(number) for number in parts[-2].split(".")))
                elif "Write data path: " in msg:
                    ctx.write_data_path = Utils.get_text_between(msg, "Write data path: ", " [")
                    if "AppData" in ctx.write_data_path:
                        logger.warning("It appears your mods are loaded from Appdata, "
                                       "this can lead to problems with multiple Factorio instances. "
                                       "If this is the case, you will get a file locked error running Factorio.")
                if not rcon_client and "Starting RCON interface at IP ADDR:" in msg:
                    rcon_client = factorio_rcon.RCONClient("localhost", rcon_port, rcon_password)
                    if ctx.mod_version == ctx.__class__.mod_version:
                        raise Exception("No Archipelago mod was loaded. Aborting.")
                    await get_info(ctx, rcon_client)
            await asyncio.sleep(0.01)

    except Exception as e:
        logger.exception(e, extra={"compact_gui": True})
        msg = "Aborted Factorio Server Bridge"
        logger.error(msg)
        ctx.gui_error(msg, e)
        ctx.exit_event.set()

    else:
        logger.info(
            f"Got World Information from AP Mod {tuple(ctx.mod_version)} for seed {ctx.seed_name} in slot {ctx.auth}")
        return True
    finally:
        factorio_process.terminate()
        factorio_process.wait(5)
    return False


async def main(args):
    ctx = FactorioContext(args.connect, args.password)
    ctx.filter_item_sends = initial_filter_item_sends
    ctx.bridge_chat_out = initial_bridge_chat_out
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    factorio_server_task = asyncio.create_task(factorio_spinup_server(ctx), name="FactorioSpinupServer")
    successful_launch = await factorio_server_task
    if successful_launch:
        factorio_server_task = asyncio.create_task(factorio_server_watcher(ctx), name="FactorioServer")
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="FactorioProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher
        await factorio_server_task

    await ctx.shutdown()


class FactorioJSONtoTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        colors = node["color"].split(";")
        for color in colors:
            if color in self.color_codes:
                node["text"] = f"[color=#{self.color_codes[color]}]{node['text']}[/color]"
            return self._handle_text(node)
        return self._handle_text(node)


if __name__ == '__main__':
    parser = get_base_parser(description="Optional arguments to FactorioClient follow. "
                                         "Remaining arguments get passed into bound Factorio instance."
                                         "Refer to Factorio --help for those.")
    parser.add_argument('--rcon-port', default='24242', type=int, help='Port to use to communicate with Factorio')
    parser.add_argument('--rcon-password', help='Password to authenticate with RCON.')
    parser.add_argument('--server-settings', help='Factorio server settings configuration file.')

    args, rest = parser.parse_known_args()
    colorama.init()
    rcon_port = args.rcon_port
    rcon_password = args.rcon_password if args.rcon_password else ''.join(
        random.choice(string.ascii_letters) for x in range(32))

    factorio_server_logger = logging.getLogger("FactorioServer")
    options = Utils.get_options()
    executable = options["factorio_options"]["executable"]
    server_settings = args.server_settings if args.server_settings else options["factorio_options"].get("server_settings", None)
    if server_settings:
        server_settings = os.path.abspath(server_settings)
    if not isinstance(options["factorio_options"]["filter_item_sends"], bool):
        logging.warning(f"Warning: Option filter_item_sends should be a bool.")
    initial_filter_item_sends = bool(options["factorio_options"]["filter_item_sends"])
    if not isinstance(options["factorio_options"]["bridge_chat_out"], bool):
        logging.warning(f"Warning: Option bridge_chat_out should be a bool.")
    initial_bridge_chat_out = bool(options["factorio_options"]["bridge_chat_out"])

    if not os.path.exists(os.path.dirname(executable)):
        raise FileNotFoundError(f"Path {os.path.dirname(executable)} does not exist or could not be accessed.")
    if os.path.isdir(executable):  # user entered a path to a directory, let's find the executable therein
        executable = os.path.join(executable, "factorio")
    if not os.path.isfile(executable):
        if os.path.isfile(executable + ".exe"):
            executable = executable + ".exe"
        else:
            raise FileNotFoundError(f"Path {executable} is not an executable file.")

    if server_settings and os.path.isfile(server_settings):
        server_args = ("--rcon-port", rcon_port, "--rcon-password", rcon_password, "--server-settings", server_settings, *rest)
    else:
        server_args = ("--rcon-port", rcon_port, "--rcon-password", rcon_password, *rest)

    asyncio.run(main(args))
    colorama.deinit()
