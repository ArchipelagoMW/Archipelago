
import asyncio
import logging
import sys
import traceback
import typing
import urllib
import time
from select import select
# import CommonClient
from CommonClient import CommonContext, get_base_parser, server_loop
import Utils
import socket
import json
import re
import traceback

print("\n\n\n\n\n\n==================================\n")

if __name__ == "__main__":
    Utils.init_logging("TextClient", exception_logger="Client")
# without terminal, we have to use gui mode
gui_enabled = not sys.stdout or "--nogui" not in sys.argv

logger = logging.getLogger("Client")

class OpenRCT2Socket:
    listener:socket.socket = None
    gamecons:list[socket.socket] = []
    gameport:int = 38280

    def __init__(self, ctx):
        self.ctx = ctx
        self.maintask = asyncio.create_task(self.main(), name="GameListen")
        self.connected_to_game = asyncio.Event()
        self.initial_connection = True
        self.outbound_packet_queue = []

    
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
        await self.connectgame()

        while True:
            await self.tick()
            await asyncio.sleep(0.01)


    def disconnectgame(self, sock:socket.socket):
        if sock:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            if sock in self.gamecons:
                self.gamecons.remove(sock)
    
    async def connectgame(self):
        await asyncio.sleep(0.5)
        self.gamecons = self.gamecons[-10:]
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
                #self.disconnectgame()
                self.gamecons.append(newgame)
                print("Connected to game at", newgame, addr)
                if self.initial_connection:
                    logger.info("Connection to OpenRCT2 Established!")
                    self.initial_connection = False
                self.connected_to_game.set()
                newgame.setblocking(0)
                try:
                    while self.outbound_packet_queue:
                        self._send(self.outbound_packet_queue.pop(0))
                        await asyncio.sleep(0.1)
                except Exception as e:
                    print("Error in connect game: " + e)
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
        packets = []
        # print('Attempting to Receive', self.game, self)
        for sock in select(self.gamecons, [], [])[0]:
            # print(repr(sock))
            try:
                data = sock.recv(1000000)
                if data:
                    print('received', len(data), 'bytes:\n', data)
                    new_packets = self._parseReceivedData(data)
                    if new_packets:
                        packets.extend(new_packets)
                        self.disconnectgame(sock)
            except socket.timeout as e:
                pass
            except BlockingIOError as e:
                pass
            except ConnectionAbortedError as e:
                print('closing')
                self.gamecons.remove(sock)
            except Exception as e:
                print(traceback.format_exc(100))
                print("Error in recv", e)
                #self.disconnectgame(sock)
                # raise
                # self.connectgame()
        return packets

    def _parseReceivedData(self, data:bytes):
        if not data:
            return []
        print('received', len(data), 'bytes:\n', data)
        packets = []
        for packet in data.split(b'\0'):
            packet = packet.decode('UTF-8')
            if packet:
                try:
                    packets.append(json.loads(packet))
                except Exception as e:
                    print("partial packet received?", e)
        print(packets)
        return packets

    def _send(self, data):
        # time.sleep(0.3)
        try:
            if data:
                print("DATA")
                sock = self.gamecons[-1]
                print(sock)
                if sock:
                    print("SOCK")
                    sock.sendall(data)
                    print('sent', len(data), 'bytes to', sock.getsockname(), '->', sock.getpeername(),':\n', data)
                    data = None
        except socket.timeout as e:
            print(e)
        except BlockingIOError as e:
            print(e)
        finally:
            if data:
                self.outbound_packet_queue.append(data)
                print("Unable to send. Appending packet to outbound queue")
                print(self.outbound_packet_queue)


    def sendobj(self, obj):
        # asyncio.run(self.connectgame())
        data = json.dumps(obj) + "\0"
        data = data.encode()
        try:
            self._send(data)
        except Exception as e:
            print('error sending to game', e)
            #self.disconnectgame(self.gamecons[-1])
            # self.connectgame()
            # asyncio.get_event_loop().run_until_complete(connectgame())
            #Tself._send(data)

    async def tick(self):
        await self.connectgame()
        loop = asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, self.recv)
            if data:
                await self.ctx.send_msgs(data)
                #await self.ctx.send_death('Some death message')
        except Exception as e:
            print('error receiving from game', e)
            #self.connectgame()
        



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
        print("PACKAGE!!!")
        if cmd == "PrintJSON":
            for index, item in enumerate(args['data']):
                match = re.search(r'\[color=[^\]]+\](.*?)\[/color\]', args['data'][index]['text'])
                if match:
                    args['data'][index]['text'] = match.group(1) 
        print(args)
        self.gamesock.sendobj(args)
        time.sleep(0.00000272727*len(args)) #Future Colby, this probably won't help to extend... but maybe?

    # async def disconnect(self, allow_autoreconnect: bool = False):
    #     # self.game = ""
    #     await super().disconnect(allow_autoreconnect)
    
    # async def shutdown(self):
    #     await super().shutdown()


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

# Replacing this with code from Serpent.ai to make a .apworld
# async def main(args): 
#     ctx = OpenRCT2Context(args.connect, args.password)
#     ctx.auth = args.name
#     ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

#     if gui_enabled:
#         ctx.run_gui()
#     ctx.run_cli()

#     await ctx.exit_event.wait()
#     await ctx.shutdown()

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
