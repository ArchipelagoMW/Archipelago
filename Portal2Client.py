import asyncio
import logging
import typing

from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger
from worlds.portal2.Items import item_table
from worlds.portal2.ItemHandling import handle_item
from worlds.portal2.Locations import location_names_to_map_codes, map_codes_to_location_names, all_locations_table
import Utils

if __name__ == "__main__":
    Utils.init_logging("Portal2Client", exception_logger="Portal2Client")
    
logger = logging.getLogger("Portal2Client")

class Portal2CommandProcessor(ClientCommandProcessor):

    def _cmd_checkcon(self):
        if self.ctx.check_game_connection():
            self.output("Connection to Portal 2 is up and running")
        else:
            self.output("Disconnected from Portal 2. Make sure the mod is open and the -netconport launch option is set")

    def _cmd_command(self, *command):
        self.ctx.command_queue.append(' '.join(command) + "\n")

    # Debug commands
    def _cmd_mapid(self, map_code):
        self.output(self.ctx.map_code_to_location_id(map_code))

class Portal2Context(CommonContext):
    command_processor = Portal2CommandProcessor
    game_command_sender_task: typing.Optional["asyncio.Task[None]"] = None
    game_message_listener_task: typing.Optional["asyncio.Task[None]"] = None
    game = "Portal 2"
    items_handling = 0b111  # receive all items for /received

    HOST = "localhost"
    PORT = 3000

    item_list = []
    item_remove_commands = []
    command_queue = []
    game_message_queue = []

    sender_active : bool = False
    listener_active : bool = False

    item_name_to_id: dict[str, int] = None
    location_name_to_id: dict[str, int] = None

    def create_level_begin_command(self):
        '''Generates a command that deletes all entities not collected yet and connects end level trigger with map completion event'''
        return f'{';'.join(self.item_remove_commands)};script CreateCompleteLevelAlertHook()\n'

    def send_player_to_main_menu_command(self):
        '''Sends the player back to the main menu (called on map completion)'''
        return 'disconnect;startupmenu force\n'

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
            logger.info(f"Map Joined {message.split(':', 1)[1]}")
            # append the whole command string
            command_string = self.create_level_begin_command()
            print(command_string)
            self.command_queue.append(command_string)

        elif message.startswith("map_complete:"):
            done_map = message.split(':', 1)[1]
            logger.info("Check made: " + done_map)
            await self.check_locations([self.map_code_to_location_id(done_map)])
            self.command_queue.append(self.send_player_to_main_menu_command())

    def check_game_connection(self):
        logger.info("Sender active: "  + str(self.sender_active) + " Listener active: " + str(self.listener_active))
        return self.sender_active and self.listener_active
    
    def update_game(self, game_package, game):
        super().update_game(game_package, game)
        self.item_name_to_id = game_package["item_name_to_id"]
        self.location_name_to_id = game_package["location_name_to_id"]
    
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
        if not map_code in map_codes_to_location_names:
            return None
        
        location_name = map_codes_to_location_names[map_code]
        if not self.location_name_to_id:
            raise Exception("location_name_to_id dict has not been created yet")
        return self.location_name_to_id[location_name]

    def on_package(self, cmd, args):
        # Add item names to list
        if cmd == "Retrieved":
            if f"_read_item_name_groups_{self.game}" in args["keys"]:
                self.item_list = args["keys"][f"_read_item_name_groups_{self.game}"]["Everything"]
                self.update_item_remove_commands()

        if cmd == "ReceivedItems":
            # Update item list to only include items not collected
            items_received_temp = [self.item_names.lookup_in_game(i.item) for i in self.items_received if i.player == self.slot]
            self.item_list = list(set(self.item_list) - set(items_received_temp))
            self.update_item_remove_commands()

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

if __name__ == '__main__':
    async def main():
        ctx = Portal2Context()
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        ctx.game_command_sender_task = asyncio.create_task(ctx.p2_command_sender(), name="sender loop")
        ctx.game_message_listener_task = asyncio.create_task(ctx.p2_message_listener(), name="listener loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    # use colorama to display colored text highlighting on windows
    colorama.just_fix_windows_console()

    logger.setLevel(logging.INFO)

    asyncio.run(main())
    colorama.deinit()
