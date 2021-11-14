import asyncio
import json
import time
from asyncio import StreamReader, StreamWriter
from typing import List

import Utils
from CommonClient import init_logging, CommonContext, server_loop, gui_enabled, console_loop, ClientCommandProcessor, \
    logger


class FF1CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_send(self, location_id: int):
        """Test sending a location"""
        if not self.ctx.game:
            self.output("No game set, cannot send location.")
            return
        asyncio.create_task(self.ctx.send_msgs([
            {"cmd": "LocationChecks",
             "locations": [int(location_id)]}
        ]))


class FF1Context(CommonContext):
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.nes_streams: (StreamReader, StreamWriter) = None
        self.nes_sync_task = None
        self.messages = {}
        self.locations_array = None
        self.auth = "Player 01"

    command_processor = FF1CommandProcessor

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(FF1Context, self).server_auth(password_requested)
        if not self.auth:
            logger.info('Enter slot name:')
            self.auth = await self.console_input()

        await self.send_msgs([{"cmd": 'Connect',
                               'password': self.password, 'name': self.auth, 'version': Utils.version_tuple,
                               'tags': {},
                               'uuid': Utils.get_unique_identifier(), 'game': 'Final Fantasy'
                               }])

    def _set_message(self, msg: str, msg_id: int):
        self.messages[(time.time(), msg_id)] = msg

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.game = self.games.get(self.slot, None)
        elif cmd == 'Print':
            self._set_message(args['text'], 0)
        elif cmd == "ReceivedItems":
            msg = f"Recieved {', '.join([self.item_name_getter(item.item) for item in args['items']])}"
            self._set_message(msg, 0)
        elif cmd == 'PrintJSON':
            print_type = args['type']
            item = args['item']
            player_name = self.player_names[args['receiving']]
            if print_type == 'Hint':
                msg = f"Hint: Item {self.item_name_getter(item.item)} is at" \
                      f" {self.player_names[item.player]}'s {self.location_name_getter(item.location)}"
                self._set_message(msg, item.item)
            elif print_type == 'ItemSend':
                msg = f"Sent {self.item_name_getter(item.item)} to {player_name}"
                self._set_message(msg, item.item)


def get_payload(ctx: FF1Context):
    current_time = time.time()
    return json.dumps(
        {
            "items": [item.item for item in ctx.items_received],
            "messages": {f'{key[0]}:{key[1]}': value for key, value in ctx.messages.items() if key[0] > current_time - 10}
        }
    )


async def parse_locations(locations_array: List[int], ctx: FF1Context):
    if locations_array == ctx.locations_array:
        return
    else:
        # print("New values")
        ctx.locations_array = locations_array
        locations_checked = []
        for location in ctx.missing_locations:
            # index will be - 0x100 or 0x200
            index = location
            if location < 0x200:
                index -= 0x100
                flag = 0x04
            else:
                index -= 0x200
                flag = 0x02

            # print(f"Location: {ctx.location_name_getter(location)}")
            # print(f"Index: {str(hex(index))}")
            # print(f"value: {locations_array[index] & flag != 0}")
            if locations_array[index] & flag != 0:
                locations_checked.append(location)
        if locations_checked:
            # print([ctx.location_name_getter(location) for location in locations_checked])
            await ctx.send_msgs([
                {"cmd": "LocationChecks",
                 "locations": locations_checked}
            ])


async def nes_sync_task(ctx: FF1Context):
    while not ctx.exit_event.is_set():
        if ctx.nes_streams:
            (reader, writer) = ctx.nes_streams
            msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.0)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=5.0)
                    if data == b'TERMINATED_CHAOS\n' and ctx.game is not None:
                        if not ctx.finished_game:
                            await ctx.send_msgs([
                                {"cmd": "StatusUpdate",
                                "status": 30}
                            ])
                            ctx.finished_game = True
                    elif data != b'\n' and ctx.game is not None:
                        asyncio.create_task(parse_locations(json.loads(data.decode()), ctx))
                except asyncio.TimeoutError:
                    logger.warn("Read Timed Out, Reconnecting")
                    writer.close()
                    ctx.nes_streams = None
                except ConnectionResetError as e:
                    logger.error("Connection Lost, Reconnecting")
                    writer.close()
                    ctx.nes_streams = None
            except asyncio.TimeoutError:
                logger.warn("Connection Timed Out, Reconnecting")
                writer.close()
                ctx.nes_streams = None
            except ConnectionResetError:
                logger.error("Connection Lost, Reconnecting")
                writer.close()
                ctx.nes_streams = None
            await asyncio.sleep(0.5)
        else:
            try:
                logger.info("Attempting to connect to NES")
                ctx.nes_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 43885), timeout=5.0)
            except TimeoutError:
                logger.info("Connection Timed Out, Trying Again")
                continue
            except ConnectionRefusedError:
                logger.info("Connection Refused, Trying Again")
                continue
            logger.info("Connecting to NES Succeeded: Connection Opened")


if __name__ == '__main__':
    # Text Mode to use !hint and such with games that have no text entry
    init_logging("TextClient")

    async def main(args):
        ctx = FF1Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            input_task = None
            from kvui import TextManager
            ctx.ui = TextManager(ctx)
            ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
        else:
            input_task = asyncio.create_task(console_loop(ctx), name="Input")
            ui_task = None

        ctx.nes_sync_task = asyncio.create_task(nes_sync_task(ctx), name="NES Sync")
        await ctx.exit_event.wait()

        ctx.server_address = None
        if ctx.server and not ctx.server.socket.closed:
            await ctx.server.socket.close()
        if ctx.server_task:
            await ctx.server_task
        if ctx.nes_sync_task:
            await ctx.nes_sync_task

        while ctx.input_requests > 0:
            ctx.input_queue.put_nowait(None)
            ctx.input_requests -= 1

        if ui_task:
            await ui_task

        if input_task:
            input_task.cancel()


    import argparse
    import colorama

    parser = argparse.ArgumentParser(description="FF1 Archipelago Client")
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    if not Utils.is_frozen():  # Frozen state has no cmd window in the first place
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")

    args, rest = parser.parse_known_args()
    colorama.init()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
    loop.close()
    colorama.deinit()
