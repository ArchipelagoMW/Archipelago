from enum import IntEnum
import asyncio
import socket

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
        pass;

    async def start_server(self):
        print("Starting server... waiting for game.")
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        #self.client_socket, addr = self.server_socket.accept()
        self.loop = asyncio.get_event_loop()
        self.client_socket, addr = await self.loop.sock_accept(self.server_socket)
        self.loop.create_task(self.listen())
        self.isConnected = True

    async def listen(self):
        while True:
            message = await self.loop.sock_recv(self.client_socket, 1024)
            msgStr = message.decode("utf-8")
            while "\n" in msgStr:
                line, msgStr = msgStr.split("\n", 1)
                values = line.split(";")
                print("Received message:", line)
                self.handle_message(values)

    def send(self, msgId: int, values: list):
        msg = str(msgId)
        for val in values:
            msg += ";" + str(val)
        msg += "\r\n"
        self.client_socket.send(msg.encode("utf-8"))
        print("Sent message: "+msg)

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

        elif (msgType == MessageType.Victory):
            self.client.kh2_finished_game = True
        #TODO actually handle messages

    def send_singleItem(self, id: int, itemCnt):
        msgCont = [str(id), str(itemCnt)]
        self.send(5, msgCont)


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
            values[currMsg].append(item.item)
            currItemCount += 1
            sendCnt += 1
            if currItemCount > msgLimit:
                currItemCount = 0
                currMsg = currMsg + 1


        sendMsg = 0
        for msg in values:
            msg.append(itemCnt-(sendCnt-(msgLimit*sendMsg)))
            sendCnt -= 1
            sendMsg += 1
            self.send(3, msg)

    def send_slot_data(self, data):
        self.send(MessageType.SlotData, [data])

    def shutdown_server(self):
        self.client_socket.close()
        self.server_socket.close()