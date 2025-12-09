from enum import IntEnum
import asyncio
import socket
from CommonClient import logger

class MessageType (IntEnum):
    Invalid = -1,
    Test = 0,
    WorldLocationChecked = 1,
    LevelChecked = 2,
    KeybladeChecked = 3,
    ClientCommand = 4,
    Deathlink = 5,
    SlotData = 6,
    BountyList = 7,
    ReceiveAllItems = 8,
    RequestAllItems = 9,
    ReceiveSingleItem = 10,
    Victory = 11,
    Closed = 20
    pass

class KH2Socket():
    def __init__(self, client, host: str = "127.0.0.1", port:int = 13713):
        self.client: KH2Context = client
        self.host: str = host
        self.port: int = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None
        self.isConnected = False
        self.closing = False
        pass;

    async def start_server(self):
        self.loop = asyncio.get_event_loop()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        await self._accept_client()

    async def _accept_client(self):
        """Wait for a client to connect and start a listener task."""
        while not self.closing:
            logger.info("Waiting for KH2 game connection...")
            try:
                self.client_socket, addr = await self.loop.sock_accept(self.server_socket)
                self.isConnected = True
                self.client.kh2connected = True
                print(f"Client connected from {addr}")
                logger.info("Connected")
                self.loop.create_task(self.listen())
                return
            except OSError as e:
                print(f"Socket accept failed ({e}); retrying in 5s")
                self.isConnected = False
                self.client.kh2connected = False
                await asyncio.sleep(5)

    def _safe_close_client(self):
        """Close the current client socket without killing the server socket."""
        try:
            if self.client_socket:
                self.client_socket.close()
        finally:
            self.client_socket = None
            self.isConnected = False
            self.client.kh2connected = False

    async def listen(self):
        while not self.closing:
            try:
                message = await self.loop.sock_recv(self.client_socket, 1024)
                if not message:
                    raise ConnectionResetError("Client disconnected")
                msgStr = message.decode("utf-8").replace("\n", "")
                values = msgStr.split(";")
                print("Received message: "+msgStr)
                self.handle_message(values)
            except (ConnectionResetError, OSError) as e:
                if not self.closing:
                    logger.info("Connection to game lost, reconnecting...")
                    self._safe_close_client()
                    await self._accept_client()
                    return

    def send(self, msgId: int, values: list):
        if not self.isConnected or self.client_socket is None:
               return
        try:
            msg = str(msgId)
            for val in values:
                msg += ";" + str(val)
            msg += "\r\n"
            self.client_socket.send(msg.encode("utf-8"))
            print("Sent message: "+msg)
        except (OSError, ConnectionResetError, BrokenPipeError) as e:
            print(f"Error sending message {msgId}: {e}; connection may be lost")
            self.isConnected = False
        except Exception as e:
            print(f"Error sending message {msgId}: {e}")

    def handle_message(self, message: list[str]):
        if message[0] == '':
            return

        print("Handling message: "+str(message))
        msgType = MessageType(int(message[0]))

        if msgType == MessageType.WorldLocationChecked:
            self.client.world_locations_checked.append(message[1])

        elif (msgType == MessageType.LevelChecked):
            self.client.sora_form_levels[message[2]] = int(message[1])

        elif (msgType == MessageType.KeybladeChecked):
            self.client.keyblade_ability_checked.append(message[1])

        elif (msgType == MessageType.SlotData):
            self.client.current_world_int = int(message[1])

        elif (msgType == MessageType.Deathlink):
            self.client.Room = int(message[1])
            self.client.Event = int(message[2])
            self.client.World = int(message[3])
            self.client.SoraDied = True

        elif (msgType == MessageType.Victory):
            self.client.kh2_finished_game = True

        elif msgType == MessageType.RequestAllItems:
            self.client.get_items()

    def send_singleItem(self, id: int, itemCnt):
        msgCont = [str(id.kh2id), str(itemCnt)]
        self.send(MessageType.ReceiveSingleItem, msgCont)


    def send_multipleItems(self, items, itemCnt):
        print(f"Sending multiple items {len(items)}")
        values = []

        msgLimit = 3 #Need to cap how long each message can be to prevent data from being lost

        currItemCount = 0
        currMsg = 0

        sendCnt = 0
        for item in items:
            if currItemCount == 0:
                values.append([])
            values[currMsg].append(item.kh2id)
            currItemCount += 1
            sendCnt += 1
            if currItemCount > msgLimit:
                currItemCount = 0
                currMsg = currMsg + 1


        sendMsg = 0
        for msg in values:
            sendCnt -= 1
            sendMsg += 1
            self.send(MessageType.ReceiveAllItems, msg)

    def send_slot_data(self, data):
        self.send(MessageType.SlotData, [data])

    def shutdown_server(self):
        self.closing = True
        self.client_socket.shutdown(socket.SHUT_WR)
        self.client_socket.close()
        self.server_socket.close()