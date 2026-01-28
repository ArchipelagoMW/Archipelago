from argparse import Namespace
import asyncio
import logging
import sys
import time
import typing

from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger
from NetUtils import ClientStatus, JSONMessagePart, NetworkItem
from Utils import async_start, init_logging

from ..mod_helpers.ItemHandling import handle_item, handle_map_start, handle_trap
from ..mod_helpers.MapMenu import Menu
from ..Locations import location_names_to_map_codes, map_codes_to_location_names, all_locations_table
from .. import Portal2World

if __name__ == "__main__":
    init_logging("Portal2Client", exception_logger="Portal2Client")
    
logger = logging.getLogger("Portal2Client")

class Portal2CommandProcessor(ClientCommandProcessor):

    def _cmd_check_connection(self):
        """Responds with the status of the client's connection to the Portal 2 mod"""
        self.ctx.alert_game_connection()

    def _cmd_command(self, *command):
        """Sends a command to the game. Should not be used unless you get softlocked"""
        self.ctx.command_queue.append(' '.join(command) + "\n")

    def _cmd_deathlink(self):
        """Toggles death link for this client"""
        self.ctx.death_link_active = not self.ctx.death_link_active
        async_start(self.ctx.update_death_link(self.ctx.death_link_active), "set_deathlink")
        self.output(f"Death link has been {"enabled" if self.ctx.death_link_active else "disabled"}")

    def _cmd_refresh_menu(self):
        """Refreshed the in game menu in case of maps being inaccessible when they should be"""
        self.ctx.refresh_menu()

    def _cmd_message_in_game(self, message: str, *color_string):
        """Send a message to be displayed in game (only works while in a map). 
        message can be any text 
        color_string is an optional RGB string e.g. 255 100 0"""
        if len(color_string) == 3:
            self.ctx.add_to_in_game_message_queue(message, ' '.join(color_string))
        else:
            self.ctx.add_to_in_game_message_queue(message)

    def _cmd_needed(self, *location_name):
        """Get the requirements for the map separated by all requirements and ones not yet acquired"""
        # Check if map name is in the list of map names
        message = "Location not found, use /locations to get a list of locations"
        location_name = ' '.join(location_name)
        for location in location_names_to_map_codes.keys():
            if location_name in location:
                requirements = all_locations_table[location].required_items
                requirements_not_collected = list(set(self.ctx.item_list) & set(requirements))
                requirements.sort()
                requirements_not_collected.sort()

                message = ("Required Items: \n"
                           f"{", ".join(requirements)}\n"
                           f"{"All items acquired" if not requirements_not_collected else "Still needed: \n" + ", ".join(requirements_not_collected)}")
                break
        self.output(message)

class Portal2Context(CommonContext):
    command_processor = Portal2CommandProcessor
    game_command_sender_task: typing.Optional["asyncio.Task[None]"] = None
    game_message_listener_task: typing.Optional["asyncio.Task[None]"] = None
    game = "Portal 2"
    items_handling = 0b111  # receive all items for /received

    HOST = "localhost"
    PORT = int(Portal2World.settings.default_portal2_port)

    death_link_active = False
    goal_map_code = ""

    item_list: list[str] = []
    item_remove_commands: list[str] = []
    command_queue: list[str] = []
    game_message_queue: list[str] = []

    sender_active : bool = False
    listener_active : bool = False

    location_name_to_id: dict[str, int] = None

    menu: Menu = None

    def alert_game_connection(self):
        if self.check_game_connection():
            self.command_processor.output(self.command_processor, "Connection to Portal 2 is up and running")
        else:
            self.command_processor.output(self.command_processor, "Disconnected from Portal 2. Make sure the mod is open and the `-netconport 3000` launch option is set")

    def create_level_begin_command(self):
        '''Generates a command that deletes all entities not collected yet'''
        return f"{';'.join(self.item_remove_commands)}\n"
    
    def update_menu(self, finished_map: str = None):
        menu_file = Portal2World.settings.menu_file
        if finished_map:
            self.menu.complete_map(finished_map)
        # Write the menu to that file
        with open(menu_file, "w", encoding='utf-8') as f:
            f.write(str(self.menu))

    def refresh_menu(self):
        for location_id in self.checked_locations:
            self.menu.complete_map(location_id)
        self.update_menu()

    def add_to_in_game_message_queue(self, message: str, color_string: str = None) -> None:
        self.command_queue.append(f'script AddToTextQueue("{message}"{f',"{color_string}"' if color_string else ""})\n')

    async def p2_message_listener(self):
        '''Listener for the messages sent from portal 2 to the client'''
        try:
            while True:
                try:
                    reader, writer = await asyncio.open_connection(self.HOST, self.PORT)
                except ConnectionRefusedError:
                    self.listener_active = False
                    await asyncio.sleep(self.current_reconnect_delay)
                    continue
                
                self.listener_active = True
                try:
                    while True:
                        data = await reader.read(4096)
                        if not data:
                            # connection closed by server; break to reconnect
                            break
                        
                        # Add messages to the queue for consumption
                        data_list = data.decode(errors="ignore").replace("\'", "").split('\r\n')
                        self.game_message_queue += data_list

                except asyncio.CancelledError:
                    logger.info("Game listener closed from cancellation")
                    raise
                except Exception as e:
                    logger.error(f"An error occurred in listener loop: {e}")
                finally:
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except Exception:
                        pass
                    self.listener_active = False
                    await asyncio.sleep(self.current_reconnect_delay)
        except asyncio.CancelledError:
            logger.info("Game listener closed from cancellation")
            raise

    async def p2_command_sender(self):
        '''Command sender for the console commands sent to portal 2 from the client'''
        try:
            while True:
                try:
                    reader, writer = await asyncio.open_connection(self.HOST, self.PORT)
                except ConnectionRefusedError:
                    self.sender_active = False
                    await asyncio.sleep(self.current_reconnect_delay)
                    continue

                self.sender_active = True
                try:
                    # Keep the connection open and send queued commands without blocking the loop
                    while True:
                        # handle commands
                        if self.command_queue:
                            c = self.command_queue.pop(0)
                            if c:
                                writer.write(c.encode())
                                await writer.drain()

                        # Handle messages
                        elif self.game_message_queue:
                            message = self.game_message_queue.pop(0)
                            await self.handle_message(message)

                        else:
                            # yield control briefly so other tasks (listener, etc.) run smoothly
                            await asyncio.sleep(0.1)
                except asyncio.CancelledError:
                    logger.info("Game sender closed from cancellation")
                    raise
                except Exception as e:
                    logger.error(f"An error occurred in sender loop: {e}")
                finally:
                    try:
                        writer.close()
                        await writer.wait_closed()
                    except Exception:
                        pass
                    self.sender_active = False
                    await asyncio.sleep(self.current_reconnect_delay)
        except asyncio.CancelledError:
            logger.info("Game sender closed from cancellation")
            raise

    async def handle_message(self, message: str):
        if message.startswith("map_name:"):
            map_name = message.split(':', 1)[1]
            # append the whole command string
            command_string = self.create_level_begin_command()
            self.command_queue.append(command_string)
            self.command_queue += handle_map_start(map_name, self.item_list)

        # For map complete checks
        elif message.startswith("map_complete:"):
            done_map = message.split(':', 1)[1]
            if done_map == self.goal_map_code:
                await self.handle_goal_completion()
            
            map_id = self.map_code_to_location_id(done_map)
            if map_id:
                await self.check_locations([map_id])
                self.update_menu(map_id)
        
        # For all other checks
        elif message.startswith("item_collected:"):
            item_collected = message.split(":", 1)[1]
            check_id = all_locations_table[item_collected].id
            await self.check_locations([check_id])
        
        elif message.startswith("send_deathlink"):
            if self.death_link_active and time.time() - self.last_death_link > 10:
                await self.send_death()

    async def handle_goal_completion(self):
        if self.finished_game:
            return
        
        self.finished_game = True
        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    def on_deathlink(self, data):
        self.command_queue.append("restart\n")
        return super().on_deathlink(data)

    def check_game_connection(self):
        logger.info("Sender active: "  + str(self.sender_active) + " Listener active: " + str(self.listener_active))
        return self.sender_active and self.listener_active
    
    # Used for nothing?
    def location_id_to_map_code(self, location_id: str) -> str:
        '''Converts a location ID to a map code (if that id relates to a map location)'''
        # Convert id to name
        location_name = self.location_names.lookup_in_game(location_id)
        # Get info for location name
        if location_name in location_names_to_map_codes:
            return location_names_to_map_codes[location_name]
        
        return None
    
    def map_code_to_location_id(self, map_code: str):
        '''Convert in game map name to location id for location checks'''
        if map_code not in map_codes_to_location_names:
            return None
        
        location_name = map_codes_to_location_names[map_code]
        if not self.location_name_to_id:
            raise Exception("location_name_to_id dict has not been created yet")
        if location_name not in self.location_name_to_id:
            return None
        return self.location_name_to_id[location_name]
    
    def handle_slot_data(self, slot_data: dict):
        if "death_link" in slot_data:
            self.death_link_active = slot_data["death_link"]
            async_start(self.update_death_link(self.death_link_active), "set_deathlink")

        if "goal_map_code" in slot_data:
            self.goal_map_code = slot_data["goal_map_code"]

        if "location_name_to_id" in slot_data:
            self.location_name_to_id = slot_data["location_name_to_id"]

        if "chapter_dict" in slot_data:
            self.menu = Menu(slot_data["chapter_dict"], self)
            self.refresh_menu()
        else:
            raise Exception("chapter_dict not found in slot data")
        
        if "open_world" in slot_data:
            self.menu.is_open_world = slot_data["open_world"]

    def on_package(self, cmd, args):
        def update_item_list():
            # Update item list to only include items not collected
            items_received_names = [self.item_names.lookup_in_game(i.item, self.game) for i in self.items_received]
            self.item_list = list(set(self.item_list) - set(items_received_names))
            self.refresh_menu()

        # Add item names to list
        if cmd == "Retrieved":
            if f"_read_item_name_groups_{self.game}" in args["keys"]:
                self.item_list = args["keys"][f"_read_item_name_groups_{self.game}"]["Everything"]
                update_item_list()
                self.update_item_remove_commands()

        if cmd == "ReceivedItems":
            items = args["items"]
            traps = [i for i in items if i.flags == 0b100]
            for trap in traps:
                self.command_queue.append(handle_trap(self.item_names.lookup_in_game(trap.item, self.game)))
            update_item_list()
            self.update_item_remove_commands()

        if cmd == "Connected":
            self.handle_slot_data(args["slot_data"])
            self.alert_game_connection()

        if cmd == "PrintJSON":
            if "type" in args:
                if args["type"] == "ItemSend" and args["receiving"] == self.slot:
                    item: NetworkItem = args["item"]
                    text = self.parse_message(args["data"], sending = item.player)
                elif args["type"] == "Goal":
                    text = self.parse_message(args["data"])
                else:
                    if args["type"] == "Collect":
                        self.update_menu()
                    return # Don't send text to game
                self.add_to_in_game_message_queue(text)

    def parse_message(self, data: list[dict], sending: int | None = None) -> str: # data pats not cast to JSONMessagePart as expected, dict instead
        message = ""
        for part in data:
            text = part["text"]
            if "type" in part:
                if part["type"] == "item_id":
                    text = self.item_names.lookup_in_slot(int(text), self.slot)
                elif part["type"] == "location_id":
                    text = self.location_names.lookup_in_slot(int(text), sending)
                elif part["type"] == "player_id":
                    text = self.player_names[int(text)]
            message += text

        return message


    def update_item_remove_commands(self):
        temp_commands = []
        for item_name in self.item_list:
            item_commands = handle_item(item_name)
            if item_commands:
                temp_commands += item_commands

        self.item_remove_commands = temp_commands

    def make_gui(self):
        from kvui import GameManager

        class Portal2TextManager(GameManager):
            base_title = "Portal 2 Text Client"
            def __init__(self, ctx):
                super().__init__(ctx)
                self.icon = r"worlds/portal2/data/Portalpelago.png"

        return Portal2TextManager
    
    async def shutdown(self):
        self.server_address = ""
        self.username = None
        self.password = None
        self.cancel_autoreconnect()
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task:
            await self.server_task
        if self.game_command_sender_task:
            self.game_command_sender_task.cancel()
        if self.game_message_listener_task:
            self.game_message_listener_task.cancel()

        while self.input_requests > 0:
            self.input_queue.put_nowait(None)
            self.input_requests -= 1
        self.keep_alive_task.cancel()
        if self.ui_task:
            await self.ui_task
        if self.input_task:
            self.input_task.cancel()

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)

async def main(args: Namespace):
    ctx = Portal2Context(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.game_command_sender_task = asyncio.create_task(ctx.p2_command_sender(), name="sender loop")
    ctx.game_message_listener_task = asyncio.create_task(ctx.p2_message_listener(), name="listener loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    
    await ctx.exit_event.wait()
    await ctx.shutdown()

def launch(*args: str) -> None:
    from .Launch import launch_portal_2_client

    launch_portal_2_client(*args)


if __name__ == "__main__":
    launch(*sys.argv[1:])
