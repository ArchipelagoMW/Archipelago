from __future__ import annotations
import os
import logging
import json
import string
import copy
import sys
import subprocess
import factorio_rcon

import colorama
import asyncio
from queue import Queue
from CommonClient import CommonContext, server_loop, console_loop, ClientCommandProcessor, logger
from MultiServer import mark_raw

import Utils
import random
from NetUtils import RawJSONtoTextParser, NetworkItem, ClientStatus, JSONtoTextParser, JSONMessagePart

from worlds.factorio.Technologies import lookup_id_to_name

os.makedirs("logs", exist_ok=True)

# Log to file in gui case
if getattr(sys, "frozen", False) and not "--nogui" in sys.argv:
    logging.basicConfig(format='[%(name)s]: %(message)s', level=logging.INFO,
                        filename=os.path.join("logs", "FactorioClient.txt"), filemode="w")
else:
    logging.basicConfig(format='[%(name)s]: %(message)s', level=logging.INFO)
    logging.getLogger().addHandler(logging.FileHandler(os.path.join("logs", "FactorioClient.txt"), "w"))

gui_enabled = Utils.is_frozen() or "--nogui" not in sys.argv

def get_kivy_app():
    os.environ["KIVY_NO_CONSOLELOG"] = "1"
    os.environ["KIVY_NO_FILELOG"] = "1"
    os.environ["KIVY_NO_ARGS"] = "1"
    from kivy.app import App
    from kivy.base import ExceptionHandler, ExceptionManager, Config
    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.recycleview import RecycleView
    from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
    from kivy.lang import Builder


    class FactorioManager(App):
        def __init__(self, ctx):
            super(FactorioManager, self).__init__()
            self.ctx = ctx
            self.commandprocessor = ctx.command_processor(ctx)
            self.icon = r"data/icon.png"

        def build(self):
            self.grid = GridLayout()
            self.grid.cols = 1

            self.tabs = TabbedPanel()
            self.tabs.default_tab_text = "All"
            self.title = "Archipelago Factorio Client"
            pairs = [
                ("Client", "Archipelago"),
                ("FactorioServer", "Factorio Server Log"),
                ("FactorioWatcher", "Bridge Data Log"),
            ]
            self.tabs.default_tab_content = UILog(*(logging.getLogger(logger_name) for logger_name, name in pairs))
            for logger_name, display_name in pairs:
                bridge_logger = logging.getLogger(logger_name)
                panel = TabbedPanelItem(text=display_name)
                panel.content = UILog(bridge_logger)
                self.tabs.add_widget(panel)

            self.grid.add_widget(self.tabs)
            textinput = TextInput(size_hint_y=None, height=30, multiline=False)
            textinput.bind(on_text_validate=self.on_message)
            self.grid.add_widget(textinput)
            self.commandprocessor("/help")
            return self.grid

        def on_stop(self):
            self.ctx.exit_event.set()

        def on_message(self, textinput: TextInput):
            try:
                input_text = textinput.text.strip()
                textinput.text = ""

                if self.ctx.input_requests > 0:
                    self.ctx.input_requests -= 1
                    self.ctx.input_queue.put_nowait(input_text)
                elif input_text:
                    self.commandprocessor(input_text)
            except Exception as e:
                logger.exception(e)

        def on_address(self, text: str):
            print(text)


    class LogtoUI(logging.Handler):
        def __init__(self, on_log):
            super(LogtoUI, self).__init__(logging.DEBUG)
            self.on_log = on_log

        def handle(self, record: logging.LogRecord) -> None:
            self.on_log(record)


    class UILog(RecycleView):
        cols = 1

        def __init__(self, *loggers_to_handle, **kwargs):
            super(UILog, self).__init__(**kwargs)
            self.data = []
            for logger in loggers_to_handle:
                logger.addHandler(LogtoUI(self.on_log))

        def on_log(self, record: logging.LogRecord) -> None:
            self.data.append({"text": record.getMessage()})


    class E(ExceptionHandler):
        def handle_exception(self, inst):
            logger.exception(inst)
            return ExceptionManager.RAISE


    ExceptionManager.add_handler(E())

    Config.set("input", "mouse", "mouse,disable_multitouch")
    Builder.load_file(Utils.local_path("data", "client.kv"))
    return FactorioManager

class FactorioCommandProcessor(ClientCommandProcessor):
    ctx: FactorioContext

    @mark_raw
    def _cmd_factorio(self, text: str) -> bool:
        """Send the following command to the bound Factorio Server."""
        if self.ctx.rcon_client:
            result = self.ctx.rcon_client.send_command(text)
            if result:
                self.output(result)
            return True
        return False

    def _cmd_connect(self, address: str = "") -> bool:
        """Connect to a MultiWorld Server"""
        if not self.ctx.auth:
            if self.ctx.rcon_client:
                get_info(self.ctx, self.ctx.rcon_client)  # retrieve current auth code
            else:
                self.output("Cannot connect to a server with unknown own identity, bridge to Factorio first.")
        return super(FactorioCommandProcessor, self)._cmd_connect(address)


class FactorioContext(CommonContext):
    command_processor = FactorioCommandProcessor
    game = "Factorio"

    def __init__(self, server_address, password):
        super(FactorioContext, self).__init__(server_address, password)
        self.send_index = 0
        self.rcon_client = None
        self.awaiting_bridge = False
        self.raw_json_text_parser = RawJSONtoTextParser(self)
        self.factorio_json_text_parser = FactorioJSONtoTextParser(self)

    async def server_auth(self, password_requested):
        if password_requested and not self.password:
            await super(FactorioContext, self).server_auth(password_requested)

        await self.send_msgs([{"cmd": 'Connect',
                               'password': self.password, 'name': self.auth, 'version': Utils.version_tuple,
                               'tags': ['AP'],
                               'uuid': Utils.get_unique_identifier(), 'game': "Factorio"
                               }])

    def on_print(self, args: dict):
        logger.info(args["text"])
        if self.rcon_client:
            cleaned_text = args['text'].replace('"', '')
            self.rcon_client.send_command(f"/sc game.print(\"[font=default-large-bold]Archipelago:[/font] "
                                          f"{cleaned_text}\")")

    def on_print_json(self, args: dict):
        text = self.raw_json_text_parser(copy.deepcopy(args["data"]))
        logger.info(text)
        if self.rcon_client:
            text = self.factorio_json_text_parser(args["data"])
            cleaned_text = text.replace('"', '')
            self.rcon_client.send_command(f"/sc game.print(\"[font=default-large-bold]Archipelago:[/font] "
                                          f"{cleaned_text}\")")

    @property
    def savegame_name(self) -> str:
        return f"AP_{self.seed_name}_{self.auth}.zip"


async def game_watcher(ctx: FactorioContext):
    bridge_logger = logging.getLogger("FactorioWatcher")
    from worlds.factorio.Technologies import lookup_id_to_name
    try:
        while not ctx.exit_event.is_set():
            if ctx.awaiting_bridge and ctx.rcon_client:
                ctx.awaiting_bridge = False
                data = json.loads(ctx.rcon_client.send_command("/ap-sync"))
                if data["slot_name"] != ctx.auth:
                    logger.warning(f"Connected World is not the expected one {data['slot_name']} != {ctx.auth}")
                elif data["seed_name"] != ctx.seed_name:
                    logger.warning(
                        f"Connected Multiworld is not the expected one {data['seed_name']} != {ctx.seed_name}")
                else:
                    data = data["info"]
                    research_data = data["research_done"]
                    research_data = {int(tech_name.split("-")[1]) for tech_name in research_data}
                    victory = data["victory"]

                    if not ctx.finished_game and victory:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True

                    if ctx.locations_checked != research_data:
                        bridge_logger.info(
                            f"New researches done: "
                            f"{[lookup_id_to_name[rid] for rid in research_data - ctx.locations_checked]}")
                        ctx.locations_checked = research_data
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": tuple(research_data)}])
            await asyncio.sleep(1)

    except Exception as e:
        logging.exception(e)
        logging.error("Aborted Factorio Server Bridge")


def stream_factorio_output(pipe, queue, process):
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
            if factorio_process.poll():
                factorio_server_logger.info("Factorio server has exited.")
                ctx.exit_event.set()

            while not factorio_queue.empty():
                msg = factorio_queue.get()
                factorio_server_logger.info(msg)
                if not ctx.rcon_client and "Starting RCON interface at IP ADDR:" in msg:
                    ctx.rcon_client = factorio_rcon.RCONClient("localhost", rcon_port, rcon_password)
                    # trigger lua interface confirmation
                    ctx.rcon_client.send_command("/sc game.print('Starting Archipelago Bridge')")
                    ctx.rcon_client.send_command("/sc game.print('Starting Archipelago Bridge')")
                if not ctx.awaiting_bridge and "Archipelago Bridge Data available for game tick " in msg:
                    ctx.awaiting_bridge = True
            if ctx.rcon_client:
                while ctx.send_index < len(ctx.items_received):
                    transfer_item: NetworkItem = ctx.items_received[ctx.send_index]
                    item_id = transfer_item.item
                    player_name = ctx.player_names[transfer_item.player]
                    if item_id not in lookup_id_to_name:
                        logging.error(f"Cannot send unknown item ID: {item_id}")
                    else:
                        item_name = lookup_id_to_name[item_id]
                        factorio_server_logger.info(f"Sending {item_name} to Nauvis from {player_name}.")
                        ctx.rcon_client.send_command(f'/ap-get-technology {item_name}\t{ctx.send_index}\t{player_name}')
                    ctx.send_index += 1
            await asyncio.sleep(0.1)

    except Exception as e:
        logging.exception(e)
        logging.error("Aborted Factorio Server Bridge")
        ctx.rcon_client = None
        ctx.exit_event.set()

    finally:
        factorio_process.terminate()


def get_info(ctx, rcon_client):
    info = json.loads(rcon_client.send_command("/ap-rcon-info"))
    ctx.auth = info["slot_name"]
    ctx.seed_name = info["seed_name"]


async def factorio_spinup_server(ctx: FactorioContext):
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
                if not rcon_client and "Starting RCON interface at IP ADDR:" in msg:
                    rcon_client = factorio_rcon.RCONClient("localhost", rcon_port, rcon_password)
                    get_info(ctx, rcon_client)

            await asyncio.sleep(0.01)

    except Exception as e:
        logging.exception(e)
        logging.error("Aborted Factorio Server Bridge")
        ctx.exit_event.set()

    else:
        logger.info(f"Got World Information from AP Mod for seed {ctx.seed_name} in slot {ctx.auth}")

    finally:
        factorio_process.terminate()


async def main(args):
    ctx = FactorioContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    if gui_enabled:
        input_task = None
        ui_app = get_kivy_app()(ctx)
        ui_task = asyncio.create_task(ui_app.async_run(), name="UI")
    else:
        input_task = asyncio.create_task(console_loop(ctx), name="Input")
        ui_task = None
    factorio_server_task = asyncio.create_task(factorio_spinup_server(ctx), name="FactorioSpinupServer")
    await factorio_server_task
    factorio_server_task = asyncio.create_task(factorio_server_watcher(ctx), name="FactorioServer")
    progression_watcher = asyncio.create_task(
        game_watcher(ctx), name="FactorioProgressionWatcher")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await progression_watcher
    await factorio_server_task

    if ctx.server and not ctx.server.socket.closed:
        await ctx.server.socket.close()
    if ctx.server_task is not None:
        await ctx.server_task

    while ctx.input_requests > 0:
        ctx.input_queue.put_nowait(None)
        ctx.input_requests -= 1

    if ui_task:
        await ui_task

    if input_task:
        input_task.cancel()


class FactorioJSONtoTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        colors = node["color"].split(";")
        for color in colors:
            if color in {"red", "green", "blue", "orange", "yellow", "pink", "purple", "white", "black", "gray",
                         "brown", "cyan", "acid"}:
                node["text"] = f"[color={color}]{node['text']}[/color]"
                return self._handle_text(node)
            elif color == "magenta":
                node["text"] = f"[color=pink]{node['text']}[/color]"
            return self._handle_text(node)
        return self._handle_text(node)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Optional arguments to FactorioClient follow. "
                                                 "Remaining arguments get passed into bound Factorio instance."
                                                 "Refer to factorio --help for those.")
    parser.add_argument('--rcon-port', default='24242', type=int, help='Port to use to communicate with Factorio')
    parser.add_argument('--rcon-password', help='Password to authenticate with RCON.')
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    if not Utils.is_frozen():  # Frozen state has no cmd window in the first place
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")

    args, rest = parser.parse_known_args()
    colorama.init()
    rcon_port = args.rcon_port
    rcon_password = args.rcon_password if args.rcon_password else ''.join(random.choice(string.ascii_letters) for x in range(32))

    factorio_server_logger = logging.getLogger("FactorioServer")
    options = Utils.get_options()
    executable = options["factorio_options"]["executable"]
    bin_dir = os.path.dirname(executable)
    if not os.path.exists(bin_dir):
        raise FileNotFoundError(f"Path {bin_dir} does not exist or could not be accessed.")
    if not os.path.isdir(bin_dir):
        raise FileNotFoundError(f"Path {bin_dir} is not a directory.")
    if not os.path.exists(executable):
        if os.path.exists(executable + ".exe"):
            executable = executable + ".exe"
        else:
            raise FileNotFoundError(f"Path {executable} is not an executable file.")

    server_args = ("--rcon-port", rcon_port, "--rcon-password", rcon_password, *rest)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
    loop.close()
    colorama.deinit()
