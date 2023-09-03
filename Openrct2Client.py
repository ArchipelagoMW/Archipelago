
import asyncio
import logging
import sys
import traceback
import typing
import urllib
import time
from CommonClient import CommonContext, get_base_parser, server_loop
import Utils
import socket
import json

print("\n\n\n\n\n\n==================================\n")

if __name__ == "__main__":
    Utils.init_logging("TextClient", exception_logger="Client")
# without terminal, we have to use gui mode
gui_enabled = not sys.stdout or "--nogui" not in sys.argv

logger = logging.getLogger("Client")

class OpenRCT2Socket:
    listener:socket = None
    game:socket = None
    gameport:int = 38280

    def __init__(self, ctx):
        self.ctx = ctx
        self.maintask = asyncio.create_task(self.main(), name="GameListen")
    
    async def main(self):
        while True:
            try:
                await self.proc()
            except KeyboardInterrupt as e:
                break
            except Exception as e:
                print(e)
                print(traceback.format_exc())
        if self.listener:
            try:
                self.listener.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.listener.close()

    async def proc(self):
        socket.setdefaulttimeout(10)
        self.connectgame()

        while True:
            await self.tick()
            await asyncio.sleep(0.01)


    async def connectgame(self):
        if self.game:
            self.game.shutdown(socket.SHUT_RDWR)
            self.game.close()
        self.game = None
        while True:
            await asyncio.sleep(1)
            if not self.listener:
                print('listening on port', self.gameport)
                reuse_port = None
                if sys.platform in ["linux", "linux2"]:
                    reuse_port = True
                print("Reuse Port:",reuse_port,sys.platform)
                self.listener = socket.create_server(("127.0.0.1",self.gameport), reuse_port=reuse_port)
            try:
                print("connectgame got listener:", self.listener)
                #self.listener.settimeout(5)
                (self.game, addr) = self.listener.accept()
                print("Connected to game at", self.game, addr)
                break
            except socket.timeout as e:
                print('error connecting to game', e)
            except BlockingIOError as e:
                print('error connecting to game', e)
            except Exception as e:
                self.listener.close()
                print(traceback.format_exc())
                print('error connecting to game', e)
                raise

        # self.game.setblocking(0)

    
    def recv(self):
        # print('Attempting to Receive', self.game, self)
        try:
            sock = self.game
            data = sock.recv(16384)
            if data:
                print('received', len(data), 'bytes from', sock.getpeername(), '->', sock.getsockname(),':\n', data)
            return data
        except socket.timeout as e:
            pass
        except BlockingIOError as e:
            pass
        except Exception as e:
            print("Error in recv", e)
            raise
        return None

    
    def _send(self, data):
        try:
            if data:
                sock = self.game
                sock.sendall(data)
                print('sent', len(data), 'bytes to', sock.getsockname(), '->', sock.getpeername(),':\n', data)
        except socket.timeout as e:
            print(e)
        except BlockingIOError as e:
            print(e)

    async def sendobj(self, obj):
        data = json.dumps(obj)
        data = data.encode()
        try:
            self._send(data)
        except Exception as e:
            print('error sending to game', e)
            self.connectgame()
            self._send(data)

    async def tick(self):
        data = None
        if not self.game:
            await self.connectgame()
        
        try:
            data = self.recv()
        except Exception as e:
            print('error receiving from game', e)
            self.connectgame()
        
        if True:
            await self.ctx.send_death('Some death message')



class OpenRCT2Context(CommonContext):
    # Text Mode to use !hint and such with games that have no text entry
    tags = {"AP", "TextOnly"}
    game = ""  # empty matches any game since 0.3.2
    items_handling = 0b111  # receive all items for /received
    want_slot_data = False  # Can't use game specific slot_data

    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str]) -> None:
        super().__init__(server_address, password)
        self.gamesock = OpenRCT2Socket(self)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(OpenRCT2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.game = ""
        await super().disconnect(allow_autoreconnect)
    
    async def shutdown(self):
        await super().shutdown()


    # DeathLink hooks
    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        super().on_deathlink(data)
        self.gamesock.sendobj({'cmd': 'DeathLink'})


async def main(args):
    ctx = OpenRCT2Context(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()
    
def run_as_textclient():
    import colorama

    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args()

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    run_as_textclient()
