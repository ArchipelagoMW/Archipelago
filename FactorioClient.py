import os
import logging
import json
import string
import copy
from concurrent.futures import ThreadPoolExecutor

import colorama
import asyncio
from queue import Queue, Empty
from CommonClient import CommonContext, server_loop, console_loop, ClientCommandProcessor, logger
from MultiServer import mark_raw

import Utils
import random
from NetUtils import RawJSONtoTextParser, NetworkItem

from worlds.factorio.Technologies import lookup_id_to_name

rcon_port = 24242
rcon_password = ''.join(random.choice(string.ascii_letters) for x in range(32))
save_name = "Archipelago"

server_args = (save_name, "--rcon-port", rcon_port, "--rcon-password", rcon_password)

logging.basicConfig(format='[%(name)s]: %(message)s', level=logging.INFO)
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

script_folder = options["factorio_options"]["script-output"]

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

    def _cmd_connect(self, address: str = "", name="") -> bool:
        """Connect to a MultiWorld Server"""
        self.ctx.auth = name
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
        if self.auth is None:
            logging.info('Enter the name of your slot to join this game:')
            self.auth = await self.console_input()

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
        copy_data = copy.deepcopy(args["data"]) # jsontotextparser is destructive currently
        logger.info(self.jsontotextparser(args["data"]))
        if self.rcon_client:
            cleaned_text = self.raw_json_text_parser(copy_data).replace('"', '')
            self.rcon_client.send_command(f"/sc game.print(\"Archipelago: {cleaned_text}\")")

async def game_watcher(ctx: FactorioContext):
    bridge_logger = logging.getLogger("FactorioWatcher")
    bridge_file = os.path.join(script_folder, "ap_bridge.json")
    if os.path.exists(bridge_file):
        os.remove(bridge_file)
    from worlds.factorio.Technologies import lookup_id_to_name
    bridge_counter = 0
    try:
        while 1:
            if os.path.exists(bridge_file):
                bridge_logger.info("Found Factorio Bridge file.")
                while 1:
                    with open(bridge_file) as f:
                        data = json.load(f)
                        research_data = data["research_done"]
                        research_data = {int(tech_name.split("-")[1]) for tech_name in research_data}
                    if ctx.locations_checked != research_data:
                        bridge_logger.info(f"New researches done: "
                                             f"{[lookup_id_to_name[rid] for rid in research_data - ctx.locations_checked]}")
                        ctx.locations_checked = research_data
                        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": tuple(research_data)}])
                    await asyncio.sleep(1)
            else:
                bridge_counter += 1
                if bridge_counter >= 60:
                    bridge_logger.info("Did not find Factorio Bridge file, waiting for mod to run, which requires the server to run, which requires a player to be connected.")
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
    try:
        while 1:
            while not factorio_queue.empty():
                msg = factorio_queue.get()
                factorio_server_logger.info(msg)
                if not ctx.rcon_client and "Hosting game at IP ADDR:" in msg:
                    ctx.rcon_client = factorio_rcon.RCONClient("localhost", rcon_port, rcon_password)
                    # trigger lua interface confirmation
                    ctx.rcon_client.send_command("/sc game.print('Starting Archipelago Bridge')")
                    ctx.rcon_client.send_command("/sc game.print('Starting Archipelago Bridge')")
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


async def main():
    ctx = FactorioContext(None, None, True)
    # testing shortcuts
    # ctx.server_address = "localhost"
    # ctx.auth = "Nauvis"
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
    await asyncio.sleep(3)
    watcher_task = asyncio.create_task(game_watcher(ctx), name="FactorioProgressionWatcher")
    input_task = asyncio.create_task(console_loop(ctx), name="Input")
    factorio_server_task = asyncio.create_task(factorio_server_watcher(ctx), name="FactorioServer")
    await ctx.exit_event.wait()
    ctx.server_address = None
    ctx.snes_reconnect_address = None

    await asyncio.gather(watcher_task, input_task, factorio_server_task)

    if ctx.server is not None and not ctx.server.socket.closed:
        await ctx.server.socket.close()
    if ctx.server_task is not None:
        await ctx.server_task
    await factorio_server_task

    while ctx.input_requests > 0:
        ctx.input_queue.put_nowait(None)
        ctx.input_requests -= 1

    await input_task


if __name__ == '__main__':
    colorama.init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    colorama.deinit()
