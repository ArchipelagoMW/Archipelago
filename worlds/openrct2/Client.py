
import logging
import sys
import asyncio
import typing
from CommonClient import CommonContext, get_base_parser, server_loop
import Utils
import re
from .OpenRCT2Socket import OpenRCT2Socket

if __name__ == "__main__":
    print("\n\n\n\n\n\n==================================\n")
    Utils.init_logging("TextClient", exception_logger="Client")
# without terminal, we have to use gui mode
gui_enabled = not sys.stdout or "--nogui" not in sys.argv

logger = logging.getLogger("Client")

class OpenRCT2Context(CommonContext):
    tags = {"DeathLink"}
    game = "OpenRCT2"
    items_handling = 0b111  # receive all items for /received
    want_slot_data = True 

    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str]) -> None:
        super().__init__(server_address, password)
        self.gamesock = OpenRCT2Socket(self)
        self.game_connection_established = False
        #kivy.set_title("OpenRCT2 Client")

    async def server_auth(self, password_requested: bool = False):
        if not self.game_connection_established:
            logger.info('Awaiting connection to OpenRCT2')
            await self.gamesock.connected_to_game.wait()
            
        
        if password_requested and not self.password:
            await super(OpenRCT2Context, self).server_auth(password_requested)


        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        # if cmd == "Connected":
        #     self.game = self.game#slot_info[self.slot].game
        if cmd == "PrintJSON":
            for index, item in enumerate(args['data']):
                match = re.search(r'\[color=[^\]]+\](.*?)\[/color\]', args['data'][index]['text'])
                if match:
                    args['data'][index]['text'] = match.group(1) 
        print(args)
        self.gamesock.sendobj(args)



    # DeathLink hooks
    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        super().on_deathlink(data)
        self.gamesock.sendobj({'cmd': 'DeathLink'})

    def run_gui(self): #Sets the title of the client
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class TextManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "OpenRCT2 Client"

        self.ui = TextManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def main():
    Utils.init_logging("OpenRCT2Client", exception_logger="Client")

    async def _main():
        ctx = OpenRCT2Context(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()

        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())

    colorama.deinit()
