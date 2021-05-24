import os
import logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(format='[%(name)s]: %(message)s', level=logging.INFO)
logging.getLogger().addHandler(logging.FileHandler(os.path.join("logs", "FactorioClient.txt"), "w"))
import json
import string
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ["KIVY_NO_ARGS"] = "1"
from concurrent.futures import ThreadPoolExecutor


import asyncio
from queue import Queue
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, logger
from MultiServer import mark_raw

import Utils
import random
from NetUtils import RawJSONtoTextParser, NetworkItem, ClientStatus

from worlds.factorio.Technologies import lookup_id_to_name

rcon_port = 24242
rcon_password = ''.join(random.choice(string.ascii_letters) for x in range(32))
save_name = "Archipelago"



options = Utils.get_options()
executable = options["factorio_options"]["executable"]
bin_dir = os.path.dirname(executable)
if not os.path.isdir(bin_dir):
    raise FileNotFoundError(bin_dir)
if not os.path.exists(executable):
    if os.path.exists(executable + ".exe"):
        executable = executable + ".exe"
    else:
        raise FileNotFoundError(executable)

import sys
server_args = (save_name, "--rcon-port", rcon_port, "--rcon-password", rcon_password, *sys.argv[1:])

threadpool = ThreadPoolExecutor(10)


class FactorioCommandProcessor(ClientCommandProcessor):
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
            self.output("Cannot connect to a server with unknown own identity, bridge to Factorio first.")
        return super(FactorioCommandProcessor, self)._cmd_connect(address)


class FactorioContext(CommonContext):
    command_processor = FactorioCommandProcessor

    def __init__(self, *args, **kwargs):
        super(FactorioContext, self).__init__(*args, **kwargs)
        self.send_index = 0
        self.rcon_client = None
        self.raw_json_text_parser = RawJSONtoTextParser(self)

    async def server_auth(self, password_requested):
        if password_requested and not self.password:
            await super(FactorioContext, self).server_auth(password_requested)

        await self.send_msgs([{"cmd": 'Connect',
                               'password': self.password, 'name': self.auth, 'version': Utils._version_tuple,
                               'tags': ['AP'],
                               'uuid': Utils.get_unique_identifier(), 'game': "Factorio"
                               }])

    def on_print(self, args: dict):
        logger.info(args["text"])
        if self.rcon_client:
            cleaned_text = args['text'].replace('"', '')
            self.rcon_client.send_command(f"/sc game.print(\"Archipelago: {cleaned_text}\")")

    def on_print_json(self, args: dict):
        if not self.found_items and args.get("type", None) == "ItemSend" and args["receiving"] == args["sending"]:
            pass  # don't want info on other player's local pickups.
        text = self.raw_json_text_parser(args["data"])
        logger.info(text)
        if self.rcon_client:
            cleaned_text = text.replace('"', '')
            self.rcon_client.send_command(f"/sc game.print(\"Archipelago: {cleaned_text}\")")

async def game_watcher(ctx: FactorioContext, bridge_file: str):
    bridge_logger = logging.getLogger("FactorioWatcher")
    from worlds.factorio.Technologies import lookup_id_to_name
    bridge_counter = 0
    try:
        while not ctx.exit_event.is_set():
            if os.path.exists(bridge_file):
                bridge_logger.info("Found Factorio Bridge file.")
                while not ctx.exit_event.is_set():
                    with open(bridge_file) as f:
                        data = json.load(f)
                        research_data = data["research_done"]
                        research_data = {int(tech_name.split("-")[1]) for tech_name in research_data}
                        victory = data["victory"]
                        ctx.auth = data["slot_name"]
                        ctx.seed_name = data["seed_name"]

                    if not ctx.finished_game and victory:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True

                    if ctx.locations_checked != research_data:
                        bridge_logger.info(f"New researches done: "
                                           f"{[lookup_id_to_name[rid] for rid in research_data - ctx.locations_checked]}")
                        ctx.locations_checked = research_data
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": tuple(research_data)}])
                    await asyncio.sleep(1)
            else:
                bridge_counter += 1
                if bridge_counter >= 60:
                    bridge_logger.info(
                        "Did not find Factorio Bridge file, "
                        "waiting for mod to run, which requires the server to run, "
                        "which requires a player to be connected.")
                    bridge_counter = 0
                await asyncio.sleep(1)
    except Exception as e:
        logging.exception(e)
        logging.error("Aborted Factorio Server Bridge")


def stream_factorio_output(pipe, queue):
    def queuer():
        while 1:
            text = pipe.readline().strip()
            if text:
                queue.put_nowait(text)

    from threading import Thread

    thread = Thread(target=queuer, name="Factorio Output Queue", daemon=True)
    thread.start()


async def factorio_server_watcher(ctx: FactorioContext):
    import subprocess
    import factorio_rcon
    factorio_server_logger = logging.getLogger("FactorioServer")
    factorio_process = subprocess.Popen((executable, "--start-server", *(str(elem) for elem in server_args)),
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.DEVNULL,
                                        encoding="utf-8")
    factorio_server_logger.info("Started Factorio Server")
    factorio_queue = Queue()
    stream_factorio_output(factorio_process.stdout, factorio_queue)
    stream_factorio_output(factorio_process.stderr, factorio_queue)
    script_folder = None
    progression_watcher = None
    try:
        while not ctx.exit_event.is_set():
            while not factorio_queue.empty():
                msg = factorio_queue.get()
                factorio_server_logger.info(msg)
                if not ctx.rcon_client and "Starting RCON interface at IP ADDR:" in msg:
                    ctx.rcon_client = factorio_rcon.RCONClient("localhost", rcon_port, rcon_password)
                    # trigger lua interface confirmation
                    ctx.rcon_client.send_command("/sc game.print('Starting Archipelago Bridge')")
                    ctx.rcon_client.send_command("/sc game.print('Starting Archipelago Bridge')")
                    ctx.rcon_client.send_command("/ap-sync")
                if not script_folder and "Write data path:" in msg:
                    script_folder = msg.split("Write data path: ", 1)[1].split("[", 1)[0].strip()
                    bridge_file = os.path.join(script_folder, "script-output", "ap_bridge.json")
                    if os.path.exists(bridge_file):
                        os.remove(bridge_file)
                    logging.info(f"Bridge File Path: {bridge_file}")
                    progression_watcher= asyncio.create_task(
                        game_watcher(ctx, bridge_file), name="FactorioProgressionWatcher")
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
                        ctx.rcon_client.send_command(f'/ap-get-technology {item_name} {player_name}')
                    ctx.send_index += 1
            await asyncio.sleep(1)


    except Exception as e:
        logging.exception(e)
        logging.error("Aborted Factorio Server Bridge")

    finally:
        factorio_process.terminate()
        if progression_watcher:
            await progression_watcher

async def main():
    ctx = FactorioContext(None, None, True)

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    factorio_server_task = asyncio.create_task(factorio_server_watcher(ctx), name="FactorioServer")
    ui_app = FactorioManager(ctx)
    ui_task = asyncio.create_task(ui_app.async_run(), name="UI")

    await ctx.exit_event.wait() # wait for signal to exit application
    ui_app.stop()
    ctx.server_address = None
    ctx.snes_reconnect_address = None
    # allow tasks to quit
    await ui_task
    await factorio_server_task
    await ctx.server_task

    if ctx.server is not None and not ctx.server.socket.closed:
        await ctx.server.socket.close()
    if ctx.server_task is not None:
        await ctx.server_task

    while ctx.input_requests > 0: # clear queue for shutdown
        ctx.input_queue.put_nowait(None)
        ctx.input_requests -= 1


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.lang import Builder


class FactorioManager(App):
    def __init__(self, ctx):
        super(FactorioManager, self).__init__()
        self.ctx = ctx
        self.commandprocessor = ctx.command_processor(ctx)
        self.icon = "data/icon.png"

    def build(self):
        self.grid = GridLayout()
        self.grid.cols = 1
        self.tabs = TabbedPanel()
        self.tabs.default_tab_text = "All"
        self.title = "Archipelago Factorio Client"
        pairs = [
            ("Client", "Archipelago"),
            ("FactorioServer", "Factorio Server Log"),
            ("FactorioWatcher", "Bridge File Log"),
        ]
        self.tabs.default_tab_content = UILog(*(logging.getLogger(logger_name) for logger_name, name in pairs))
        for logger_name, display_name in pairs:
            bridge_logger = logging.getLogger(logger_name)
            panel = TabbedPanelHeader(text=display_name)
            self.tabs.add_widget(panel)
            panel.content = UILog(bridge_logger)
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

class LogtoUI(logging.Handler):
    def __init__(self, on_log):
        super(LogtoUI, self).__init__(logging.DEBUG)
        self.on_log = on_log

    def handle(self, record: logging.LogRecord) -> None:
        self.on_log(record)

Builder.load_string('''
<TabbedPanel>
    tab_width: 200
<Row@Label>:
    canvas.before:
        Color:
            rgba: 0.2, 0.2, 0.2, 1
        Rectangle:
            size: self.size
            pos: self.pos
    text_size: self.width, None
    size_hint_y: None
    height: self.texture_size[1]
    font_size: dp(20)
<UILog>:
    viewclass: 'Row'
    scroll_y: 0
    effect_cls: "ScrollEffect"
    RecycleBoxLayout:
        default_size: None, dp(20)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: dp(3)
''')

class UILog(RecycleView):
    cols = 1
    def __init__(self, *loggers_to_handle, **kwargs):
        super(UILog, self).__init__(**kwargs)
        self.data = []
        for logger in loggers_to_handle:
            logger.addHandler(LogtoUI(self.on_log))

    def on_log(self, record: logging.LogRecord) -> None:
        self.data.append({"text": record.getMessage()})

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width * 0.9, None)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
