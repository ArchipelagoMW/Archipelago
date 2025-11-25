import asyncio
import logging
import socket
import typing

from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger
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

class Portal2Context(CommonContext):
    command_processor = Portal2CommandProcessor
    game_command_sender_task: typing.Optional["asyncio.Task[None]"] = None
    game_message_listener_task: typing.Optional["asyncio.Task[None]"] = None

    HOST = "localhost"
    PORT = 3000

    entity_list = []

    command_queue = []

    sender_active : bool = False
    listener_active : bool = False

    def create_level_begin_command(self, entities_list):
        '''Generates a command that deletes all entities not collected yet and connects end level trigger with map completion event'''
        return f"script ::e <- {str(entities_list).replace('\'', '\"')};script DeleteEntities(e);script CreateCompleteLevelAlertHook()\n"

    def send_player_to_main_menu_command(self):
        '''Sends the player back to the main menu (called on map completion)'''
        return 'disconnect;startupmenu force\n'

    async def p2_message_listener(self):
        '''Listener for the messages sent from portal 2 to the client'''
        try:
            self.listener_active = True
            reader, writer = await asyncio.open_connection(self.HOST, self.PORT)
            try:
                while True:
                    data = await reader.read(4096)
                    if not data:
                        # connection closed by server; break to reconnect
                        break
                    data_string = data.decode(errors="ignore").split('\r')[0].strip('\'"')
                    if data_string.startswith("map_name:"):
                        logger.info(f"Map Joined {data_string.split(':', 1)[1]}")
                        logger.info("Deleting Entities: " + str(self.entity_list))
                        # append the whole command string, not extend into characters
                        self.command_queue.append(self.create_level_begin_command(self.entity_list))

                    elif data_string.startswith("map_complete:"):
                        done_map = data_string.split(':', 1)[1]
                        logger.info("Check made: " + done_map)
                        self.command_queue.append(self.send_player_to_main_menu_command())
            finally:
                try:
                    writer.close()
                    await writer.wait_closed()
                except Exception:
                    pass

        except asyncio.CancelledError:
            logger.info("Game listener closed from cancellation")
            raise
        except ConnectionRefusedError:
            logger.error("Connection failed. Make sure the mod is open and the -netconport launch option is set")
            self.listener_active = False
            await asyncio.sleep(self.current_reconnect_delay)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            self.listener_active = False
            await asyncio.sleep(self.current_reconnect_delay)
            

    async def p2_command_sender(self):
        '''Command sender for the consol commands sent to portal 2 from the client'''
        try:
            if self.command_queue:
                c = self.command_queue.pop(0)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.HOST, self.PORT))
                    s.sendall(c.encode())
            
            self.sender_active = True
        except asyncio.CancelledError:
            logger.info("Game sender closed from cancellation")
            raise
        except ConnectionRefusedError:
            logger.error("Connection failed. Make sure the mod is open and the -netconport launch option is set")
            self.sender_active = False
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            self.sender_active = False
        finally:
            await asyncio.sleep(self.current_reconnect_delay)
            # Restart the loop
            self.game_command_sender_task = asyncio.create_task(self.p2_command_sender(), name="sender loop")

    def check_game_connection(self):
        logger.info("Sender active: "  + str(self.sender_active) + " Listener active: " + str(self.listener_active))
        return self.sender_active and self.listener_active
    
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
