from enum import StrEnum, IntEnum

class PacketDirection(StrEnum):
    Incoming = 'Incoming'
    Outgoing = 'Outgoing'

class IncAPCommands(StrEnum):
    RoomInfo = 'RoomInfo'
    ConnectionRefused = 'ConnectionRefused'
    Connected = 'Connected'
    PrintJSON = 'PrintJSON'
    Retrieved = 'Retrieved'
    RecievedItems = 'RecievedItems'
    LocationInfo = 'LocationInfo'
    Bounced = 'Bounced'
    RoomUpdate = 'RoomUpdate'

class APPacket:
    def __init__(self, cmd: str, packet_direction: str):
        self.cmd: str = cmd
        self.packet_direction: str = packet_direction
        self.response: dict[str, any] = {}

class IncRoomInfo(APPacket):
    def __init__(self, data: dict, packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.password: bool = data['password']
        self.games: list[str] = data['games']
        self.tags: list[str] = data['tags']
        self.version: dict[str, int | str] = data['version']
        self.generator_version: dict[str, int | str] = data['generator_version']
        self.permissions: dict[str, int] = data['permissions']
        self.hint_cost: int = data['hint_cost']
        self.location_check_points: int = data['location_check_points']
        self.datapackage_checksums: dict[str, str] = data['datapackage_checksums']
        self.seed_name: str = data['seed_name']
        self.time: str = data['time']

    def create_response(self, slot_name: str, password: str, uuid: int, version: dict[str, int | str], client_name_tag: str = "APNothing") -> None:
        self.response: dict[str, any] = {
            'cmd': 'Connect',
            'game': '',
            'items_handling': 0,
            'name': slot_name,
            'password': password,
            'slot_data': True,
            'tags': [
                'HintGame',
                client_name_tag
            ],
            'uuid': uuid,
            'version': version
        }

class IncConnectionRefused(APPacket):
    def __init__(self, data: dict, packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.errors: list[str] = data['errors']
        self.error_messages: list[str] = []

        self.__process_error_messages()

    def __process_error_messages(self) -> None:
        for error in self.errors:
            match error:
                case 'InvalidPassword':
                    self.error_messages.append(f'Error: Invalid Password')
                case _:
                    self.error_messages.append(f'Unknown Error: \'{error}\'')

class APNetworkPlayer:
    def __init__(self, team: int, slot: int, alias: str, name: str):
        self.team: int = team
        self.slot: int = slot
        self.alias: str = alias
        self.name: str = name

class APNetworkItemType(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    USEFUL = 2
    PROGRESSION_SKIP_BALANCING = 3
    TRAP = 4

class APNetworkItem:
    def __init__(self, item_id: int, location_id: int, player_id: int, flags: int, player_is_receiving: bool = False):
        self.item_id: int = item_id
        self.location_id: int = location_id
        self.player_id: int = player_id
        self.player_is_receiving: bool = player_is_receiving # Usually False, except for in LocationInfo. Denotes if the player id is the player who has the item in their world (False) or the player the item is for (True). (This is stupid AP why the inconsistency???)
        self.type: int = APNetworkItemType(flags)


class IncConnected(APPacket):
    def __init__(self, data: dict, packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.team: int = data['team']
        self.slot: int = data['slot']
        self.missing_locations: list[int] = data['missing_locations']
        self.checked_locations: list[int] = data['checked_locations']
        self.slot_info: dict[str, dict[str, str | int | list]] = data['slot_info']
        self.hint_points: int = data['hint_points']
        self.slot_data: dict[str, any] = data['slot_data']
        
        self.players: list[APNetworkPlayer] = []
        
        for player in data['players']:
            if player['class'] == 'NetworkPlayer':
                self.players.append(APNetworkPlayer(player['team'], player['slot'], player['alias'], player['name']))

class PrintJSONMessageTypes(StrEnum):
    Join = 'Join'
    Tutorial = 'Tutorial'
    Hint = 'Hint'

class IncPrintJSON(APPacket):
    def __init__(self, data: dict, network_players: list[APNetworkPlayer] = [], network_items: list[APNetworkItem] = [], packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.data: list[dict[str, any]] = data['data']
        self.type: str = data['type']
        
        self.output_messages: list[str] = []

        match self.type:
            case PrintJSONMessageTypes.Join:
                self.team: int = data['team']
                self.slot: int = data['slot']
                self.tags: list[str] = data['tags']
            case PrintJSONMessageTypes.Tutorial:
                pass
            case PrintJSONMessageTypes.Hint:
                combined_string: str = ''
                for line in self.data:
                    if 'player_id' in line.values():
                        player_id = int(line['text'])
                        for player in network_players:
                            if player.slot == player_id:
                                player_name = player.name
                        line['text'] = player_name
                    '''elif 'location_id' in line.values():
                        location_id = int(line['text'])
                        for item in network_items:
                            if item.location_id == location_id:
                                location_id = item.name                 # item.name doesn't exist. Where do we get the item's name?
                    combined_string += line['text']
                    '''
                    combined_string += line['text']
                self.data = [{'text': combined_string}]
            case _:
                print(f'Unknown PrintJSON type: {self.type}')

        self.__process_output_messages()

    def __process_output_messages(self) -> None:
        for msg in self.data:
            msg: str = msg['text']
            self.output_messages.append(msg)

class OutLocationChecks(APPacket):
    def __init__(self, locations: list[int], packet_direction: str = PacketDirection.Outgoing):
        super().__init__('LocationChecks', packet_direction)
        self.locations: list[int] = locations

        self.__create_response()

    def __create_response(self) -> None:
        self.response: dict[str, any] = {
            'cmd': self.cmd,
            'locations': self.locations
        }

class OutSetNotify(APPacket):
    def __init__(self, keys: list[str], packet_direction: str = PacketDirection.Outgoing):
        super().__init__('SetNotify', packet_direction)
        self.keys: list[str] = keys

        self.__create_response()

    def __create_response(self) -> None:
        self.response: dict[str, any] = {
            'cmd': self.cmd,
            'keys': self.keys
        }

class OutGet(APPacket):
    def __init__(self, keys: list[str], packet_direction: str = PacketDirection.Outgoing):
        super().__init__('Get', packet_direction)
        self.keys: list[str] = keys

        self.__create_response()

    def __create_response(self) -> None:
        self.response: dict[str, any] = {
            'cmd': self.cmd,
            'keys': self.keys
        }

class OutLocationScouts(APPacket):
    def __init__(self, locations: list[int], create_as_hint: int = 0, packet_direction: str = PacketDirection.Outgoing):
        super().__init__('LocationScouts', packet_direction)
        self.locations: list[int] = locations
        self.create_as_hint: int = create_as_hint

        self.__create_response()

    def __create_response(self) -> None:
        self.response: dict[str, any] = {
            'cmd': self.cmd,
            'locations': self.locations,
            'create_as_hint': self.create_as_hint
        }

class IncRetrieved(APPacket):
    def __init__(self, data: dict, packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.keys: dict[str, dict[str, any]] = data['keys']

class IncLocationInfo(APPacket):
    def __init__(self, data: dict, packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.network_locations: list[APNetworkItem] = []
        for loc in data['locations']:
            if loc['class'] == 'NetworkItem':
                new_loc: APNetworkItem = APNetworkItem(loc['item'], loc['location'], loc['player'], loc['flags'], True)
                self.network_locations.append(new_loc)

class IncRecievedItems(APPacket):
    def __init__(self, index: int, data: dict, packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.network_items: list[APNetworkItem] = []
        self.last = index
        for loc in data['locations']:
            if loc['class'] == 'NetworkItem':
                new_loc: APNetworkItem = APNetworkItem(loc['item'], loc['location'], loc['player'], loc['flags'], True)
                self.network_items.append(new_loc)

class IncBounced(APPacket):
    def __init__(self, data: dict, packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.slots: list[int] = data['slots']

class IncRoomUpdate(APPacket):
    def __init__(self, data: dict, packet_direction: str = PacketDirection.Incoming):
        super().__init__(data['cmd'], packet_direction)
        self.checked_locations: list[int] | None = None
        for key in data.keys():
            match key:
                case 'hint_points':
                    self.hint_points: int = data['hint_points']
                case 'checked_locations':
                    self.checked_locations = data['checked_locations']
                case _:
                    pass

'''
{
    "cmd": "RoomUpdate",
    "hint_points": 17
}
'''