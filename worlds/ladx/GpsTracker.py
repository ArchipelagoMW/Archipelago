import json
import typing
from websockets import WebSocketServerProtocol

from . import TrackerConsts as Consts
from .TrackerConsts import EntranceCoord
from .LADXR.entranceInfo import ENTRANCE_INFO

class Entrance:
    outdoor_room: int
    indoor_map: int
    indoor_address: int
    name: str
    other_side_name: str = None
    changed: bool = False
    known_to_server: bool = False

    def __init__(self, outdoor: int, indoor: int, name: str, indoor_address: int=None):
        self.outdoor_room = outdoor
        self.indoor_map = indoor
        self.indoor_address = indoor_address
        self.name = name

    def map(self, other_side: str, known_to_server: bool = False):
        if other_side != self.other_side_name:
            self.changed = True
            self.known_to_server = known_to_server
        
        self.other_side_name = other_side

class GpsTracker:
    room: int = None
    last_room: int = None
    last_different_room: int = None
    room_same_for: int = 0
    room_changed: bool = False
    screen_x: int = 0
    screen_y: int = 0
    spawn_x: int = 0
    spawn_y: int = 0
    indoors: int = None
    indoors_changed: bool = False
    spawn_map: int = None
    spawn_room: int = None
    spawn_changed: bool = False
    spawn_same_for: int = 0
    entrance_mapping: typing.Dict[str, str] = None
    entrances_by_name: typing.Dict[str, Entrance] = {}
    needs_found_entrances: bool = False
    needs_slot_data: bool = True

    def __init__(self, gameboy) -> None:
        self.gameboy = gameboy

        self.gameboy.set_location_range(
            Consts.link_motion_state,
            Consts.transition_sequence - Consts.link_motion_state + 1,
            [Consts.transition_state]
        )

    async def read_byte(self, b: int):
        return (await self.gameboy.read_memory_cache([b]))[b]

    def load_slot_data(self, slot_data: typing.Dict[str, typing.Any]):
        if 'entrance_mapping' not in slot_data:
            return

        # We need to know how entrances were mapped at generation before we can autotrack them
        self.entrance_mapping = {}

        # Convert to upstream's newer format
        for outside, inside in slot_data['entrance_mapping'].items():
            new_inside = f"{inside}:inside"
            self.entrance_mapping[outside] = new_inside
            self.entrance_mapping[new_inside] = outside

        self.entrances_by_name = {} 

        for name, info in ENTRANCE_INFO.items():
            alternate_address = (
                Consts.entrance_address_overrides[info.target]
                if info.target in Consts.entrance_address_overrides
                else None
            )

            entrance = Entrance(info.room, info.target, name, alternate_address)
            self.entrances_by_name[name] = entrance

            inside_entrance = Entrance(info.target, info.room, f"{name}:inside", alternate_address)
            self.entrances_by_name[f"{name}:inside"] = inside_entrance
        
        self.needs_slot_data = False
        self.needs_found_entrances = True

    async def read_location(self):
        # We need to wait for screen transitions to finish
        transition_state = await self.read_byte(Consts.transition_state)
        transition_target_x = await self.read_byte(Consts.transition_target_x)
        transition_target_y = await self.read_byte(Consts.transition_target_y)
        transition_scroll_x = await self.read_byte(Consts.transition_scroll_x)
        transition_scroll_y = await self.read_byte(Consts.transition_scroll_y)
        transition_sequence = await self.read_byte(Consts.transition_sequence)
        motion_state = await self.read_byte(Consts.link_motion_state)
        if (transition_state != 0
            or transition_target_x != transition_scroll_x
            or transition_target_y != transition_scroll_y
            or transition_sequence != 0x04):
            return

        indoors = await self.read_byte(Consts.indoor_flag)

        if indoors != self.indoors and self.indoors != None:
            self.indoors_changed = True

        self.indoors = indoors

        # We use the spawn point to know which entrance was most recently entered
        spawn_map = await self.read_byte(Consts.spawn_map)
        map_digit = Consts.map_map[spawn_map] << 8 if self.spawn_map else 0
        spawn_room = await self.read_byte(Consts.spawn_room) + map_digit
        spawn_x = await self.read_byte(Consts.spawn_x)
        spawn_y = await self.read_byte(Consts.spawn_y)

        # The spawn point needs to be settled before we can trust location data
        if ((spawn_room != self.spawn_room and self.spawn_room != None)
            or (spawn_map != self.spawn_map and self.spawn_map != None)
            or (spawn_x != self.spawn_x and self.spawn_x != None)
            or (spawn_y != self.spawn_y and self.spawn_y != None)):
            self.spawn_changed = True
            self.spawn_same_for = 0
        else:
            self.spawn_same_for += 1

        self.spawn_map = spawn_map
        self.spawn_room = spawn_room
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

        # Spawn point is preferred, but doesn't work for the sidescroller entrances
        # Those can be addressed by keeping track of which room we're in
        # Also used to validate that we came from the right room for what the spawn point is mapped to
        map_id = await self.read_byte(Consts.map_id)
        if map_id not in Consts.map_map:
            print(f'Unknown map ID {hex(map_id)}')
            return

        map_digit = Consts.map_map[map_id] << 8 if indoors else 0
        self.last_room = self.room
        self.room = await self.read_byte(Consts.room) + map_digit

        # Again, the room needs to settle before we can trust location data
        if self.last_room != self.room:
            self.room_same_for = 0
            self.room_changed = True
            self.last_different_room = self.last_room
        else:
            self.room_same_for += 1

        # Only update Link's location when he's not in the air to avoid weirdness
        if motion_state in [0, 1]:
            coords = await self.read_byte(Consts.screen_coord)
            self.screen_x = coords & 0x0F
            self.screen_y = (coords & 0xF0) >> 4

    async def read_entrances(self):
        if not self.last_different_room or not self.entrance_mapping:
            return

        if self.spawn_changed and self.spawn_same_for > 0 and self.room_same_for > 0:
            # Use the spawn location, last room, and entrance mapping at generation to map the right entrance
            # A bit overkill for simple ER, but necessary for upstream's advanced ER
            spawn_coord = EntranceCoord(None, self.spawn_room, self.spawn_x, self.spawn_y)
            if str(spawn_coord) in Consts.entrance_lookup:
                valid_sources = {x.name for x in Consts.entrance_coords if x.room == self.last_different_room}
                dest_entrance = Consts.entrance_lookup[str(spawn_coord)].name
                source_entrance = [
                    x for x in self.entrance_mapping
                    if self.entrance_mapping[x] == dest_entrance and x in valid_sources
                ]

                if source_entrance:
                    self.entrances_by_name[source_entrance[0]].map(dest_entrance)

            self.spawn_changed = False
        elif self.room_changed and self.room_same_for > 0:
            # Check for the stupid sidescroller rooms that don't set your spawn point
            if self.last_different_room in Consts.sidescroller_rooms:
                source_entrance = Consts.sidescroller_rooms[self.last_different_room]
                if source_entrance in self.entrance_mapping:
                    dest_entrance = self.entrance_mapping[source_entrance]

                    expected_room = self.entrances_by_name[dest_entrance].outdoor_room
                    if dest_entrance.endswith(":indoor"):
                        expected_room = self.entrances_by_name[dest_entrance].indoor_map

                    if expected_room == self.room:
                        self.entrances_by_name[source_entrance].map(dest_entrance)

            if self.room in Consts.sidescroller_rooms:
                valid_sources = {x.name for x in Consts.entrance_coords if x.room == self.last_different_room}
                dest_entrance = Consts.sidescroller_rooms[self.room]
                source_entrance = [
                    x for x in self.entrance_mapping
                    if self.entrance_mapping[x] == dest_entrance and x in valid_sources
                ]

                if source_entrance:
                    self.entrances_by_name[source_entrance[0]].map(dest_entrance)

            self.room_changed = False

    last_location_message = {}
    async def send_location(self, socket: WebSocketServerProtocol) -> None:
        if self.room is None or self.room_same_for < 1: 
            return

        message = {
            "type":"location",
            "refresh": True,
            "room": f'0x{self.room:02X}',
            "x": self.screen_x,
            "y": self.screen_y,
            "drawFine": True,
        }

        if message != self.last_location_message:
            self.last_location_message = message
            await socket.send(json.dumps(message))

    async def send_entrances(self, socket: WebSocketServerProtocol, diff: bool=True) -> typing.Dict[str, str]:
        if not self.entrance_mapping:
            return

        new_entrances = [x for x in self.entrances_by_name.values() if x.changed or (not diff and x.other_side_name)]

        if not new_entrances:
            return

        message = {
            "type":"entrance",
            "refresh": True,
            "diff": True,
            "entranceMap": {},
        }

        for entrance in new_entrances:
            message['entranceMap'][entrance.name] = entrance.other_side_name
            entrance.changed = False

        await socket.send(json.dumps(message))

        new_to_server = { 
            entrance.name: entrance.other_side_name 
            for entrance in new_entrances 
            if not entrance.known_to_server 
        } 
 
        return new_to_server

    def receive_found_entrances(self, found_entrances: typing.Dict[str, str]):
        if not found_entrances:
            return

        for entrance, destination in found_entrances.items():
            if entrance in self.entrances_by_name:
                self.entrances_by_name[entrance].map(destination, known_to_server=True)
