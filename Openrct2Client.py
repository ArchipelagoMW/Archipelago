
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
        self.connected_to_game = asyncio.Event()
        self.initial_connection = True
        self.package_queue = []

    
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


    def disconnectgame(self):
        if self.game:
            self.game.shutdown(socket.SHUT_RDWR)
            self.game.close()
        self.game = None
    
    async def connectgame(self):
        #self.disconnectgame()
        #while True:
        if not self.game:
            await asyncio.sleep(0.5)
            if not self.listener:
                print('listening on port', self.gameport)
                reuse_port = None
                if sys.platform in ["linux", "linux2"]:
                    reuse_port = True
                #print("Reuse Port:",reuse_port,sys.platform)
                self.listener = socket.create_server(("127.0.0.1",self.gameport), reuse_port=reuse_port)
                print("connectgame got listener:", self.listener)
            try:
                #self.listener.settimeout(0.01)
                self.listener.setblocking(0)
                (newgame, addr) = self.listener.accept()
                if newgame:
                    # maybe we should do a recv before disconnecting?
                    self.disconnectgame()
                    self.game = newgame
                    print("Connected to game at", self.game, addr)
                    if self.initial_connection:
                        logger.info("Connection to OpenRCT2 Established!")
                        self.initial_connection = False
                    self.connected_to_game.set()
                    self.game.setblocking(0)
                    while self.package_queue:
                        self._send(self.package_queue[0])
                        self.package_queue.pop()
                    #break
            except socket.timeout as e:
                #print('error connecting to game', e)
                pass
            except BlockingIOError as e:
                #print('error connecting to game', e)
                pass
            except Exception as e:
                self.listener.close()
                print(traceback.format_exc())
                print('error connecting to game', e)
                raise

    
    def recv(self):
        # print('Attempting to Receive', self.game, self)
        try:
            sock = self.game
            data = sock.recv(16384)
            if data:
                print('received', len(data), 'bytes from', sock.getpeername(), '->', sock.getsockname(),':\n', data)
                data = data.rstrip(b'\x00')#Strip the terminator from string
                data = data.decode('UTF-8')
                # data = json.dumps(data)
                data = [json.loads(data)]
                print(data)
                self.disconnectgame()
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
        time.sleep(0.2)
        try:
            if data:
                print("DATA")
                sock = self.game
                print(sock)
                if sock:
                    print("SOCK")
                    sock.sendall(data)
                    print('sent', len(data), 'bytes to', sock.getsockname(), '->', sock.getpeername(),':\n', data)
                else:
                    self.package_queue.append(data)
                    print(self.package_queue)
                    # raise Exception("Socket not connected")
                    # asynchio.run(self.connectgame())
                    # self._send(data)
        except socket.timeout as e:
            print(e)
        except BlockingIOError as e:
            print(e)

    def sendobj(self, obj):
        # asyncio.run(self.connectgame())
        data = json.dumps(obj)
        data = data.encode()
        try:
            self._send(data)
        except Exception as e:
            print('error sending to game', e)
            self.disconnectgame()
            self.connectgame()
            # asyncio.get_event_loop().run_until_complete(connectgame())
            self._send(data)

    async def tick(self):
        await self.connectgame()
        try:
            data = self.recv()
            if data:
                await self.ctx.send_msgs(data)
                #await self.ctx.send_death('Some death message')
        except Exception as e:
            print('error receiving from game', e)
            #self.connectgame()
        



class OpenRCT2Context(CommonContext):
    tags = {"AP", "DeathLink"}
    game = "OpenRCT2"
    items_handling = 0b111  # receive all items for /received
    want_slot_data = True 

    def __init__(self, server_address: typing.Optional[str], password: typing.Optional[str]) -> None:
        super().__init__(server_address, password)
        self.gamesock = OpenRCT2Socket(self)
        self.game_connection_established = False

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
        print("PACKAGE!!!")
        print(args)
        self.gamesock.sendobj(args)

    async def disconnect(self, allow_autoreconnect: bool = False):
        # self.game = ""
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

    parser = get_base_parser(description="Client to connect OpenRCT2 to Archipelago")
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
