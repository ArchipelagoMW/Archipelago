import asyncio
import json
import os
import requests
import time
import re
from NetUtils import ClientStatus
import Utils
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop
from .Items import bl2_base_id

# import ModuleUpdate
# ModuleUpdate.update()

# Testing:
# import colorama
# from asyncio import Task
#

from worlds.borderlands2.Locations import location_name_to_id


class Borderlands2Context(CommonContext):
    game = "Borderlands 2"
    items_handling = 0b111  # Indicates you get items sent from other worlds. possibly should be 0b011
    client_version = "0.4"
    deathlink_pending = False

    def __init__(self, server_address, password):
        super(Borderlands2Context, self).__init__(server_address, password)
        self.slot_data = dict()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Borderlands2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.server_state_synchronized = False
        await super(Borderlands2Context, self).connection_closed()

    async def shutdown(self):
        await super(Borderlands2Context, self).shutdown()

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class BL2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago BL2 Client"

        self.ui = BL2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def is_connected(self) -> bool:
        if self.server and self.server.socket.open and self.seed_name and self.slot_data:
            return True
        return False

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.slot_data = args.get("slot_data", {})
        elif cmd == "RoomInfo":
            self.seed_name = args['seed_name']

    def on_deathlink(self, data: dict):
        self.deathlink_pending = True
        super().on_deathlink(data)
        self.command_processor.output(self.command_processor, str("Death link received"))

async def main(launch_args):
    ctx = Borderlands2Context(launch_args.connect, launch_args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    def consolelog(msg):
        ctx.command_processor.output(ctx.command_processor, str(msg))

    async def handle_sock_client(reader, writer):
        """
        Handles communication with a single client asynchronously.
        """
        addr = writer.get_extra_info('peername')
        print(f"sock connection from {addr}")
        ctx.command_processor.output(ctx.command_processor, f"sock connection from {addr}")

        while True:
            if ctx.slot_data.get("death_link", False) and "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
            try:
                data = await reader.read(100)  # Read data asynchronously
                if not data:
                    break
                message = data.decode()
                print(f"Received from {addr}: {message}")
                if message.startswith('blghello'):
                    print("initialization request received")
                    mod_vers = message.split(":")[-1]
                    if mod_vers != ctx.client_version:
                        ctx.command_processor.output(
                            ctx.command_processor,
                            f"Version Mismatch! Unexpected results ahead. mine:{ctx.client_version} mod:{mod_vers}"
                        )
                    response = "blgwelcome:" + ctx.client_version
                    writer.write(response.encode())
                    await writer.drain()
                elif message == 'is_archi_connected':
                    print("is_archi_connected")
                    response = str(ctx.is_connected())
                    print("sending: " + response)
                    writer.write(response.encode())
                    await writer.drain()
                elif message == 'options':
                    print("options")
                    opt = dict(ctx.slot_data)
                    opt["seed"] = ctx.seed_name
                    response = json.dumps(opt)
                    print(response)
                    writer.write(response.encode())
                    await writer.drain()
                elif message.startswith('items_all'):
                    print("list items request received")
                    offset = message.split(":")[-1]
                    if offset == "items_all":
                        offset = 0
                    offset = int(offset)

                    # subtract bl2_base_id; mod is unaware of the base id, and the msg is shorter
                    chunk_end = offset + 500
                    # grab next 500 starting from offset
                    item_ids = [str(x.item - bl2_base_id) for x in ctx.items_received[offset:chunk_end]]

                    if chunk_end >= len(ctx.items_received): # mark end of list with 0
                        item_ids.append("0")

                    response = ",".join(item_ids)
                    writer.write(response.encode())
                    await writer.drain()
                elif message.startswith('locations_all'):
                    print("list locations request received")
                    offset = message.split(":")[-1]
                    if offset == "locations_all":
                        offset = 0
                    offset = int(offset)

                    # subtract bl2_base_id; mod is unaware of the base id, and the msg is shorter
                    loc_ids = [str(x - bl2_base_id) for x in ctx.checked_locations]
                    # grab next 500 starting from offset
                    chunk_end = offset + 500
                    loc_ids = loc_ids[offset:chunk_end]
                    if chunk_end >= len(ctx.checked_locations): # mark end of list with 0
                        loc_ids.append("0")

                    response = ",".join(loc_ids)
                    writer.write(response.encode())
                    await writer.drain()
                elif message == 'died':
                    if ctx.slot_data.get("death_link", False):
                        await ctx.send_death("BL2 Death")
                        response = "ok"
                    else:
                        response = "disabled"
                    writer.write(response.encode())
                    await writer.drain()
                elif message == 'deathlink':
                    if ctx.deathlink_pending:
                        response = "yes"
                        ctx.deathlink_pending = False
                    else:
                        response = "no"
                    writer.write(response.encode())
                    await writer.drain()
                else:
                    print("msg_check: " + str(message))
                    if message is None:
                        continue
                    item_id = int(message)
                    if (item_id + bl2_base_id) in ctx.locations_checked:
                        response = "skipped"
                    else:
                        response = "ack:" + str(item_id)
                    writer.write(response.encode())
                    await writer.drain()

                    if item_id == ctx.slot_data["goal"]:  # victory condition
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                        continue

                    await ctx.check_locations([item_id + bl2_base_id])

            except asyncio.CancelledError:
                print(f"Client {addr} disconnected (cancelled).")
                ctx.command_processor.output(ctx.command_processor,f"sock client {addr} disconnected.")
            except Exception as e:
                print(f"Error with client {addr}: {e}")
                ctx.command_processor.output(ctx.command_processor,f"Error with sock client {addr}: {e}")
                break
        # done with client
        print(f"Client disconnected from: {addr}")
        writer.close()
        await writer.wait_closed()

    server = await asyncio.start_server(
        handle_sock_client, 'localhost', 9997
    )
    ctx.command_processor.output(ctx.command_processor,"sock server started on localhost:9997")

    await ctx.exit_event.wait()
    ctx.server_address = None
    # await progression_watcher
    await ctx.shutdown()
def launch():
    import colorama
    parser = get_base_parser(description="Borderlands 2 Client, for text interfacing.")
    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
