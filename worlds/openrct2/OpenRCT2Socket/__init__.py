import asyncio
import socket
import json
import sys
import traceback
import logging
from select import select

logger = logging.getLogger("Client")

def logex(*args):
    print(traceback.format_exc())
    print(*sys.exc_info())
    if args:
        print(*args)

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
        self.inbound_buffer = ''


    async def main(self):
        while True:
            try:
                await self.proc()
            except KeyboardInterrupt as e:
                break
            except Exception as e:
                logex(e)
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
            self.listener.setblocking(False)
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
                newgame.setblocking(False)
                try:
                    while self.outbound_packet_queue:
                        self._send(self.outbound_packet_queue.pop(0))
                        await asyncio.sleep(0.1)
                except Exception as e:
                    logex("Error in connect game: ", e)
        except socket.timeout as e:
            #print('error connecting to game', e)
            pass
        except BlockingIOError as e:
            #print('error connecting to game', e)
            pass
        except Exception as e:
            self.listener.close()
            logex('error connecting to game', e)
            raise

    
    def recv(self):
        packets = []
        # print('Attempting to Receive', self.game, self)
        if not self.gamecons:
            return
        sock:socket
        for sock in select(self.gamecons, [], [], 1)[0]:
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
                logex("Error in recv", e)
                #self.disconnectgame(sock)
                # raise
                # self.connectgame()
        return packets

    def _parseReceivedData(self, data:bytes):
        if not data:
            return []
        #print('received', len(data), 'bytes:\n', data)
        packets = []
        for packet in data.split(b'\0'):
            packet = packet.decode('UTF-8')
            if packet:
                try:
                    packets.append(json.loads(packet))
                    self.inbound_buffer = ''
                except Exception as e:
                    self.inbound_buffer += packet
                    try:
                        packets.append(json.loads(self.inbound_buffer))
                        self.inbound_buffer = ''
                    except Exception as e:
                        print("partial packet received?")
        print(packets)
        return packets

    def _send(self, data):
        # time.sleep(0.3)
        try:
            if data:
                #print("DATA")
                sock:socket = None
                if self.gamecons:
                    sock = self.gamecons[-1]
                if sock:
                    #print("SOCK")
                    sock.sendall(data)
                    print('sent', len(data), 'bytes to', sock.getsockname(), '->', sock.getpeername(),':\n', data)
                    data = None
        except socket.timeout as e:
            logex(e)
        except BlockingIOError as e:
            logex(e)
        finally:
            if data:
                self.outbound_packet_queue.append(data)
                print("Unable to send. Appending packet to outbound queue")
                print(self.outbound_packet_queue)


    def sendobj(self, obj):
        # asyncio.run(self.connectgame())
        data = json.dumps(obj)
        data = b"\0" + data.encode() + b"\0"
        try:
            self._send(data)
        except Exception as e:
            logex('error sending to game:', e)
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
            logex('error receiving from game', e)
            #self.connectgame()
        
