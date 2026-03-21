from websockets.sync.client import connect
from enum import Enum, auto
from ap_packets import *
#from nothing import *
import random
import json
import sys

class APStatus(Enum):
    DISCONNECTED = auto()      # Not connected to any Archipelago server
    SOCKET_CONNECTING = auto() # Socket attempting to connect
    CONNECTING = auto()        # Socket connected, trying to connect with server
    CONNECTED = auto()         # Connected with server, authenticating for selected slot
    PLAYING = auto()           # Authenticated and actively playing
    DISCONNECTING = auto()     # Attempting to disconnect from the server

class Archipelago:
    def __init__(self, ip: str , port: str, slot_name: str, password: str = '', wss: bool = True) -> None:
        self.ip = ip
        self.port = port
        self.slot_name = slot_name
        self.password = password
        self.status: APStatus = APStatus.DISCONNECTED
        self.wss = wss
        self.needsync = 0
        self.uuid: int = random.randint(1000000000, 9999999999)

        self.ap_version: dict[str, int | str] = {
            'major': 0,
            'minor': 2,
            'build': 1,
            'class': 'Version'
        }

        self.client_name_tag: str = "Nothing_Archipelago"

        self.queued_requests: list = []
        
        self.remote_keys: dict[str, any] = {}
        self.network_items: list[APNetworkItem] = []
        self.network_locations: list[APNetworkItem] = []

        self.players: list[APNetworkPlayer] = []

        self.team_id: int = -1
        self.slot_id: int = -1

        self.checked_locations: list[int] = []
        self.missing_locations: list[int] = []

        

    def get_url(self) -> str:
        return f'{"wss" if self.wss else "ws"}://{self.ip}:{self.port}'
    
    def connect(self) -> None:
        self.status = APStatus.CONNECTING

        url: str = self.get_url()
        self.client = connect(url)
        
        data: list = self.__receive_data(1)
        self.process_data(data)

    def __send_data(self, data: dict | list[dict]) -> None:
        if not isinstance(data, list):
            data = [data]
        message: str = json.dumps(data)
        self.client.send(message)   

    def __receive_data(self, timeout: int = 0) -> list:
        try:
            message: str = self.client.recv(timeout=timeout)
            data: list = json.loads(message)
        except TimeoutError as e:
            data = []
        return data
    
    def process_data(self, data: list) -> None:
        for frame in data:
            # print(f'- {frame['cmd']}') - For debugging
            match frame['cmd']:
                case IncAPCommands.RoomInfo:
                    cmd = IncRoomInfo(frame, PacketDirection.Incoming)
                    cmd.create_response(self.slot_name, self.password, self.uuid, self.ap_version, self.client_name_tag)
                    self.queued_requests.append(cmd.response)
                case IncAPCommands.ConnectionRefused:
                    cmd = IncConnectionRefused(frame, PacketDirection.Incoming)
                    for error_msg in cmd.error_messages:
                        print(error_msg)
                        sys.exit(1)
                case IncAPCommands.Connected:
                    cmd = IncConnected(frame, PacketDirection.Incoming)
                    self.status = APStatus.CONNECTED

                    self.team_id = cmd.team
                    self.slot_id = cmd.slot

                    self.checked_locations = cmd.checked_locations
                    self.missing_locations = cmd.missing_locations

                    self.needsync = 1
                    self.players = cmd.players
                    
                    # Send some packets at start of connection
                    packets_to_send: list[APPacket] = []
                    
                    packet = OutLocationChecks(locations=cmd.checked_locations)
                    packets_to_send.append(packet)

                    packet = OutSetNotify(keys=[f'Nothing_Archipelago_Settings'])
                    packets_to_send.append(packet)

                    packet = OutGet(keys=[f'Nothing_Archipelago_Settings'])
                    packets_to_send.append(packet)

                    for packet in packets_to_send:
                        self.queued_requests.append(packet.response)
                case IncAPCommands.PrintJSON:
                    cmd = IncPrintJSON(frame, self.players, self.network_items, PacketDirection.Incoming)
                    messages: list[str] = cmd.output_messages
                    for message in messages:
                        print(message)
                case IncAPCommands.Retrieved:
                    cmd = IncRetrieved(frame, PacketDirection.Incoming)
                    for key, value in cmd.keys.items():
                        self.remote_keys[key] = value
                case IncAPCommands.LocationInfo:
                    cmd = IncLocationInfo(frame, PacketDirection.Incoming)
                    for network_location in cmd.network_locations:
                        self.network_locations.append(network_location)
                case IncAPCommands.RecievedItems:
                    cmd = IncRecievedItems(frame, PacketDirection.Incoming)
                    self.last_item = cmd.last
                    for network_item in cmd.network_items:
                        self.network_items.append(network_item)
                case IncAPCommands.Bounced:
                    cmd = IncBounced(frame, PacketDirection.Incoming)
                    # What do we want to do when bounced?
                case IncAPCommands.RoomUpdate:
                    cmd = IncRoomUpdate(frame, PacketDirection.Incoming)
                    self.needsync = 1
                    if cmd.checked_locations:
                        self.checked_locations = cmd.checked_locations
                case _ as cmd_name:
                    print(f'- Unknown Command Received: {cmd_name}')


    def run(self,data) -> None:
        if self.status == APStatus.CONNECTING or self.status == APStatus.CONNECTED or self.status == APStatus.PLAYING:
            if self.needsync:
                self.sync_locations(data)

            if len(self.queued_requests) > 0:
                queued_cmds: list[str] = []
                for req in self.queued_requests:
                    queued_cmds.append(req['cmd'])
                #print(f'Queued Requests: {queued_cmds}') - For debugging
                req = self.queued_requests.pop(0)
                self.__send_data(req)
            
            recieved_data = self.__receive_data()
            if len(recieved_data) > 0:
                self.process_data(recieved_data)
            
            self.updateloctions(data)
            self.updateitems(data)

    def sync_locations(self,data):
        self.needsync = 0
        data.checked_locations_player = self.checked_locations
        for location in data.check_locations_player:
            if location <= 86400:
                data.milestones[location-1,1] = 1
                data.milestones[location-1,0] = 0
            else:
                data.spentcoins += data.shop[((location-86401)//10)%10][(location-86401)%10][3]
                data.shop[((location-86401)//10)%10][(location-86401)%10][1] = 1
            

    def updateloctions(self,data) -> None:
        packets_to_send: list[APPacket] = []
        if data.checked_locations == data.checked_locations_player:
            return
        else:
            data.checked_locations = data.check_locations_player
            self.checked_locations = data.checked_locations
            self.missing_locations = data.missing_locations
            packet = OutLocationChecks(locations=self.checked_locations)
            packets_to_send.append(packet)


        for packet in packets_to_send:
            self.queued_requests.append(packet.response)


    def updateitems(self,data) -> None:
        digitcount = 0
        data.timecaps = 1
        data.giftcoins = 0
        for network_item in self.network_items:
            if network_item.item_id == 1:
                data.shop[0][0][2] = 1
            elif network_item.item_id == 2:
                data.shop[0][1][2] = 1
            elif network_item.item_id == 3:
                data.shop[0][2+digitcount][2] = 1
                digitcount +=1
            elif network_item.item_id == 4:
                data.timecaps += 1
                data.timecap = data.timecaps * data.timecapint
            elif network_item.item_id == 5:
                giftcoins += 1
            elif network_item.item_id == 11:
                data.shop[2][0][2] = 1
            elif network_item.item_id == 12:
                data.shop[2][1][2] = 1
            elif network_item.item_id == 13:
                data.shop[2][2][2] = 1
            elif network_item.item_id == 14:
                data.shop[2][3][2] = 1
            elif network_item.item_id == 15:
                data.shop[2][4][2] = 1
            elif network_item.item_id == 16:
                data.shop[2][5][2] = 1
            elif network_item.item_id == 17:
                data.shop[2][6][2] = 1
            elif network_item.item_id == 18:
                data.shop[2][7][2] = 1
            elif network_item.item_id == 19:
                data.shop[2][8][2] = 1
            elif network_item.item_id == 20:
                data.shop[2][9][2] = 1
            elif network_item.item_id == 21:
                data.shop[1][0][2] = 1
            elif network_item.item_id == 22:
                data.shop[1][1][2] = 1
            elif network_item.item_id == 23:
                data.shop[1][2][2] = 1
            elif network_item.item_id == 24:
                data.shop[1][3][2] = 1
            elif network_item.item_id == 25:
                data.shop[1][4][2] = 1
            elif network_item.item_id == 26:
                data.shop[1][5][2] = 1
            elif network_item.item_id == 27:
                data.shop[1][6][2] = 1
            elif network_item.item_id == 28:
                data.shop[1][7][2] = 1
            elif network_item.item_id == 29:
                data.shop[1][8][2] = 1
            elif network_item.item_id == 30:
                data.shop[1][9][2] = 1
            elif network_item.item_id == 32:
                data.shop[3][1][2] = 1
            elif network_item.item_id == 33:
                data.shop[3][2][2] = 1
            elif network_item.item_id == 34:
                data.shop[3][3][2] = 1
            elif network_item.item_id == 35:
                data.shop[3][4][2] = 1
            elif network_item.item_id == 36:
                data.shop[3][5][2] = 1
            elif network_item.item_id == 37:
                data.shop[3][6][2] = 1
            elif network_item.item_id == 38:
                data.shop[3][7][2] = 1
            elif network_item.item_id == 39:
                data.shop[3][8][2] = 1
            elif network_item.item_id == 40:
                data.shop[3][9][2] = 1
        
        if data.giftcoins > data.spentcoins:
            data.points += data.giftcoins - data.spentcoins

