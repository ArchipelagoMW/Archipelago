import json

from .LADXR.entranceInfo import ENTRANCE_INFO

class Consts:
    room = 0xFFF6
    map_id = 0xFFF7
    indoor_flag = 0xDBA5
    spawn_map = 0xDB60
    spawn_room = 0xDB61
    spawn_x = 0xDB62
    spawn_y = 0xDB63
    entrance_room_offset = 0xD800
    transition_state = 0xC124
    transition_target_x = 0xC12C
    transition_target_y = 0xC12D
    transition_scroll_x = 0xFF96
    transition_scroll_y = 0xFF97
    link_motion_state = 0xC11C
    transition_sequence = 0xC16B 
    screen_coord = 0xFFFA

class EntranceCoord:
    def __init__(self, name, room, x, y):
        self.name = name
        self.room = room
        self.x = x
        self.y = y
    
    def __repr__(self):
        return EntranceCoord.coordString(self.room, self.x, self.y)
    
    def coordString(room, x, y):
        return f"{room:#05x}, {x}, {y}"

class Entrance:
    def __init__(self, outdoor, indoor, name, indoor_address=None):
        self.outdoor_room = outdoor
        self.indoor_map = indoor
        self.indoor_address = indoor_address
        self.name = name
        self.changed = False
        self.mapped_indoor = None

    def map(self, indoor):
        if indoor != self.mapped_indoor:
            self.changed = True
        
        self.mapped_indoor = indoor

        print(f'mapped {self.name} to {indoor}')

class GpsTracker:
    room = None
    last_room = None
    last_different_room = None
    room_same_for = 0
    room_changed = False
    location_changed = False
    screen_x = 0
    screen_y = 0
    spawn_x = 0
    spawn_y = 0
    indoors = None
    indoors_changed = False
    spawn_map = None
    spawn_room = None
    spawn_changed = False
    spawn_same_for = 0
    entrance_mapping = None

    def __init__(self, gameboy) -> None:
        self.gameboy = gameboy

        self.gameboy.set_location_range(
            Consts.link_motion_state,
            Consts.transition_sequence - Consts.link_motion_state + 1,
            [Consts.transition_state]
        )
    
    def load_slot_data(self, slot_data):
        if 'entrance_mapping' not in slot_data:
            return
        
        self.entrance_mapping = {}

        # Convert to upstream's newer format
        for outside, inside in slot_data['entrance_mapping'].items():
            new_inside = inside + ':inside'
            self.entrance_mapping[outside] = new_inside
            self.entrance_mapping[new_inside] = outside

        self.reverse_entrance_mapping = {value: key for key, value in self.entrance_mapping.items()}

        self.entrances_by_target = {} 
        self.entrances_by_name = {} 

        for name, info in ENTRANCE_INFO.items():
            alternate_address = entrance_address_overrides[info.target] if info.target in entrance_address_overrides else None
            entrance = Entrance(info.room, info.target, name, alternate_address)
            self.entrances_by_target[info.room] = entrance
            self.entrances_by_name[name] = entrance

            inside_entrance = Entrance(info.target, info.room, f"{name}:inside", alternate_address)
            self.entrances_by_target[info.target] = inside_entrance
            self.entrances_by_name[f"{name}:inside"] = inside_entrance

    async def read_byte(self, b):
        return (await self.gameboy.read_memory_cache([b]))[b]

    async def read_location(self):
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
        
        spawn_map = await self.read_byte(Consts.spawn_map)
        map_digit = map_map[spawn_map] << 8 if self.spawn_map else 0
        spawn_room = await self.read_byte(Consts.spawn_room) + map_digit
        spawn_x = await self.read_byte(Consts.spawn_x)
        spawn_y = await self.read_byte(Consts.spawn_y)

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

        map_id = await self.read_byte(Consts.map_id)
        if map_id not in map_map:
            print(f'Unknown map ID {hex(map_id)}')
            return

        map_digit = map_map[map_id] << 8 if indoors else 0
        self.last_room = self.room
        self.room = await self.read_byte(Consts.room) + map_digit

        if self.last_room != self.room:
            self.room_same_for = 0
            self.room_changed = True
            self.last_different_room = self.last_room
        else:
            self.room_same_for += 1

        if motion_state in [0, 1]:
            old_x = self.screen_x
            old_y = self.screen_y

            coords = await self.read_byte(Consts.screen_coord)
            self.screen_x = coords & 0x0F
            self.screen_y = (coords & 0xF0) >> 4

            if (self.room != self.last_room
                or old_x != self.screen_x
                or old_y != self.screen_y):
                self.location_changed = True
    
    async def read_entrances(self):
        if not self.last_different_room or not self.entrance_mapping:
            return

        if self.spawn_changed and self.spawn_same_for > 0 and self.room_same_for > 0:
            spawn_coord = EntranceCoord(None, self.spawn_room, self.spawn_x, self.spawn_y)
            if str(spawn_coord) in entrance_lookup:
                valid_sources = {x.name for x in entrance_coords if x.room == self.last_different_room}
                dest_entrance = entrance_lookup[str(spawn_coord)].name
                source_entrance = [x for x in self.entrance_mapping if self.entrance_mapping[x] == dest_entrance and x in valid_sources]

                if source_entrance:
                    self.entrances_by_name[source_entrance[0]].map(dest_entrance)
            
            self.spawn_changed = False
        elif self.room_changed and self.room_same_for > 0:
            # Check for the stupid sidescroller rooms that don't set your spawn point
            if self.last_different_room in sidescroller_rooms:
                source_entrance = sidescroller_rooms[self.last_different_room]
                if source_entrance in self.entrance_mapping:
                    dest_entrance = self.entrance_mapping[source_entrance]

                    expected_room = self.entrances_by_name[dest_entrance].outdoor_room
                    if dest_entrance.endswith(":indoor"):
                        expected_room = self.entrances_by_name[dest_entrance].indoor_map
                    
                    if expected_room == self.room:
                        self.entrances_by_name[source_entrance].map(dest_entrance)

            if self.room in sidescroller_rooms:
                valid_sources = {x.name for x in entrance_coords if x.room == self.last_different_room}
                dest_entrance = sidescroller_rooms[self.room]
                source_entrance = [x for x in self.entrance_mapping if self.entrance_mapping[x] == dest_entrance and x in valid_sources]

                if source_entrance:
                    self.entrances_by_name[source_entrance[0]].map(dest_entrance)
            
            self.room_changed = False

    last_message = {}
    async def send_location(self, socket, diff=False):
        if self.room is None: 
            return

        message = {
            "type":"location",
            "refresh": True,
            "room": f'0x{self.room:02X}',
            "x": self.screen_x,
            "y": self.screen_y,
            "drawFine": True,
        }

        if message != self.last_message:
            self.last_message = message
            await socket.send(json.dumps(message))

entrance_address_overrides = {
    0x312: 0xDDF2,
}

map_map = {
    0x00: 0x01,
    0x01: 0x01,
    0x02: 0x01,
    0x03: 0x01,
    0x04: 0x01,
    0x05: 0x01,
    0x06: 0x02,
    0x07: 0x02,
    0x08: 0x02,
    0x09: 0x02,
    0x0A: 0x02,
    0x0B: 0x02,
    0x0C: 0x02,
    0x0D: 0x02,
    0x0E: 0x02,
    0x0F: 0x02,
    0x10: 0x02,
    0x11: 0x02,
    0x12: 0x02,
    0x13: 0x02,
    0x14: 0x02,
    0x15: 0x02,
    0x16: 0x02,
    0x17: 0x02,
    0x18: 0x02,
    0x19: 0x02,
    0x1D: 0x01,
    0x1E: 0x01,
    0x1F: 0x01,
    0xFF: 0x03,
}

sidescroller_rooms = {
    0x2e9: "seashell_mansion:inside",
    0x08a: "seashell_mansion",
    0x2fd: "mambo:inside",
    0x02a: "mambo",
    0x1eb: "castle_secret_exit:inside",
    0x049: "castle_secret_exit",
    0x1ec: "castle_secret_entrance:inside",
    0x04a: "castle_secret_entrance",
    0x117: "d1:inside", # not a sidescroller, but acts weird 
}

entrance_coords = [
    EntranceCoord("writes_house:inside", 0x2a8, 80, 124),
    EntranceCoord("rooster_grave", 0x92, 88, 82),
    EntranceCoord("start_house:inside", 0x2a3, 80, 124),
    EntranceCoord("dream_hut", 0x83, 40, 66),
    EntranceCoord("papahl_house_right:inside", 0x2a6, 80, 124),
    EntranceCoord("papahl_house_right", 0x82, 120, 82),
    EntranceCoord("papahl_house_left:inside", 0x2a5, 80, 124),
    EntranceCoord("papahl_house_left", 0x82, 88, 82),
    EntranceCoord("d2:inside", 0x136, 80, 124),
    EntranceCoord("shop", 0x93, 72, 98),
    EntranceCoord("armos_maze_cave:inside", 0x2fc, 104, 96),
    EntranceCoord("start_house", 0xa2, 88, 82),
    EntranceCoord("animal_house3:inside", 0x2d9, 80, 124),
    EntranceCoord("trendy_shop", 0xb3, 88, 82),
    EntranceCoord("mabe_phone:inside", 0x2cb, 80, 124),
    EntranceCoord("mabe_phone", 0xb2, 88, 82),
    EntranceCoord("ulrira:inside", 0x2a9, 80, 124),
    EntranceCoord("ulrira", 0xb1, 72, 98),
    EntranceCoord("moblin_cave:inside", 0x2f0, 80, 124),
    EntranceCoord("kennel", 0xa1, 88, 66),
    EntranceCoord("madambowwow:inside", 0x2a7, 80, 124),
    EntranceCoord("madambowwow", 0xa1, 56, 66),
    EntranceCoord("library:inside", 0x1fa, 80, 124),
    EntranceCoord("library", 0xb0, 56, 50),
    EntranceCoord("d5:inside", 0x1a1, 80, 124),
    EntranceCoord("d1", 0xd3, 104, 34),
    EntranceCoord("d1:inside", 0x117, 80, 124),
    EntranceCoord("d3:inside", 0x152, 80, 124),
    EntranceCoord("d3", 0xb5, 104, 32),
    EntranceCoord("banana_seller", 0xe3, 72, 48),
    EntranceCoord("armos_temple:inside", 0x28f, 80, 124),
    EntranceCoord("boomerang_cave", 0xf4, 24, 32),
    EntranceCoord("forest_madbatter:inside", 0x1e1, 136, 80),
    EntranceCoord("ghost_house", 0xf6, 88, 66),
    EntranceCoord("prairie_low_phone:inside", 0x29d, 80, 124),
    EntranceCoord("prairie_low_phone", 0xe8, 56, 98),
    EntranceCoord("prairie_madbatter_connector_entrance:inside", 0x1f6, 136, 112),
    EntranceCoord("prairie_madbatter_connector_entrance", 0xf9, 120, 80),
    EntranceCoord("prairie_madbatter_connector_exit", 0xe7, 104, 32),
    EntranceCoord("prairie_madbatter_connector_exit:inside", 0x1e5, 40, 48),
    EntranceCoord("ghost_house:inside", 0x1e3, 80, 124),
    EntranceCoord("prairie_madbatter", 0xe6, 72, 64),
    EntranceCoord("d4:inside", 0x17a, 80, 124),
    EntranceCoord("d5", 0xd9, 88, 64),
    EntranceCoord("prairie_right_cave_bottom:inside", 0x293, 48, 124),
    EntranceCoord("prairie_right_cave_bottom", 0xc8, 40, 80),
    EntranceCoord("prairie_right_cave_high", 0xb8, 88, 48),
    EntranceCoord("prairie_right_cave_high:inside", 0x295, 112, 124),
    EntranceCoord("prairie_right_cave_top", 0xb8, 120, 96),
    EntranceCoord("prairie_right_cave_top:inside", 0x292, 48, 124),
    EntranceCoord("prairie_to_animal_connector:inside", 0x2d0, 40, 64),
    EntranceCoord("prairie_to_animal_connector", 0xaa, 136, 64),
    EntranceCoord("animal_to_prairie_connector", 0xab, 120, 80),
    EntranceCoord("animal_to_prairie_connector:inside", 0x2d1, 120, 64),
    EntranceCoord("animal_phone:inside", 0x2e3, 80, 124),
    EntranceCoord("animal_phone", 0xdb, 120, 82),
    EntranceCoord("animal_house1:inside", 0x2db, 80, 124),
    EntranceCoord("animal_house1", 0xcc, 40, 80),
    EntranceCoord("animal_house2:inside", 0x2dd, 80, 124),
    EntranceCoord("animal_house2", 0xcc, 120, 80),
    EntranceCoord("hookshot_cave:inside", 0x2b3, 80, 124),
    EntranceCoord("animal_house3", 0xcd, 40, 80),
    EntranceCoord("animal_house4:inside", 0x2da, 80, 124),
    EntranceCoord("animal_house4", 0xcd, 88, 80),
    EntranceCoord("banana_seller:inside", 0x2fe, 80, 124),
    EntranceCoord("animal_house5", 0xdd, 88, 66),
    EntranceCoord("animal_cave:inside", 0x2f7, 96, 124),
    EntranceCoord("animal_cave", 0xcd, 136, 32),
    EntranceCoord("d6", 0x8c, 56, 64),
    EntranceCoord("madbatter_taltal:inside", 0x1e2, 136, 80),
    EntranceCoord("desert_cave", 0xcf, 88, 16),
    EntranceCoord("dream_hut:inside", 0x2aa, 80, 124),
    EntranceCoord("armos_maze_cave", 0xae, 72, 112),
    EntranceCoord("shop:inside", 0x2a1, 80, 124),
    EntranceCoord("armos_temple", 0xac, 88, 64),
    EntranceCoord("d6_connector_exit:inside", 0x1f0, 56, 16),
    EntranceCoord("d6_connector_exit", 0x9c, 88, 16),
    EntranceCoord("desert_cave:inside", 0x1f9, 120, 96),
    EntranceCoord("d6_connector_entrance:inside", 0x1f1, 136, 96),
    EntranceCoord("d6_connector_entrance", 0x9d, 56, 48),
    EntranceCoord("armos_fairy:inside", 0x1ac, 80, 124),
    EntranceCoord("armos_fairy", 0x8d, 56, 32),
    EntranceCoord("raft_return_enter:inside", 0x1f7, 136, 96),
    EntranceCoord("raft_return_enter", 0x8f, 8, 32),
    EntranceCoord("raft_return_exit", 0x2f, 24, 112),
    EntranceCoord("raft_return_exit:inside", 0x1e7, 72, 16),
    EntranceCoord("raft_house:inside", 0x2b0, 80, 124),
    EntranceCoord("raft_house", 0x3f, 40, 34),
    EntranceCoord("heartpiece_swim_cave:inside", 0x1f2, 72, 124),
    EntranceCoord("heartpiece_swim_cave", 0x2e, 88, 32),
    EntranceCoord("rooster_grave:inside", 0x1f4, 88, 112),
    EntranceCoord("d4", 0x2b, 72, 34),
    EntranceCoord("castle_phone:inside", 0x2cc, 80, 124),
    EntranceCoord("castle_phone", 0x4b, 72, 34),
    EntranceCoord("castle_main_entrance:inside", 0x2d3, 80, 124),
    EntranceCoord("castle_main_entrance", 0x69, 88, 64),
    EntranceCoord("castle_upper_left", 0x59, 24, 48),
    EntranceCoord("castle_upper_left:inside", 0x2d5, 80, 124),
    EntranceCoord("witch:inside", 0x2a2, 80, 124),
    EntranceCoord("castle_upper_right", 0x59, 88, 64),
    EntranceCoord("prairie_left_cave2:inside", 0x2f4, 64, 124),
    EntranceCoord("castle_jump_cave", 0x78, 40, 112),
    EntranceCoord("prairie_left_cave1:inside", 0x2cd, 80, 124),
    EntranceCoord("seashell_mansion", 0x8a, 88, 64),
    EntranceCoord("prairie_right_phone:inside", 0x29c, 80, 124),
    EntranceCoord("prairie_right_phone", 0x88, 88, 82),
    EntranceCoord("prairie_left_fairy:inside", 0x1f3, 80, 124),
    EntranceCoord("prairie_left_fairy", 0x87, 40, 16),
    EntranceCoord("bird_cave:inside", 0x27e, 96, 124),
    EntranceCoord("prairie_left_cave2", 0x86, 24, 64),
    EntranceCoord("prairie_left_cave1", 0x84, 152, 98),
    EntranceCoord("prairie_left_phone:inside", 0x2b4, 80, 124),
    EntranceCoord("prairie_left_phone", 0xa4, 56, 66),
    EntranceCoord("mamu:inside", 0x2fb, 136, 112),
    EntranceCoord("mamu", 0xd4, 136, 48),
    EntranceCoord("richard_house:inside", 0x2c7, 80, 124),
    EntranceCoord("richard_house", 0xd6, 72, 80),
    EntranceCoord("richard_maze:inside", 0x2c9, 128, 124),
    EntranceCoord("richard_maze", 0xc6, 56, 80),
    EntranceCoord("graveyard_cave_left:inside", 0x2de, 56, 64),
    EntranceCoord("graveyard_cave_left", 0x75, 56, 64),
    EntranceCoord("graveyard_cave_right:inside", 0x2df, 56, 48),
    EntranceCoord("graveyard_cave_right", 0x76, 104, 80),
    EntranceCoord("trendy_shop:inside", 0x2a0, 80, 124),
    EntranceCoord("d0", 0x77, 120, 46),
    EntranceCoord("boomerang_cave:inside", 0x1f5, 72, 124),
    EntranceCoord("witch", 0x65, 72, 50),
    EntranceCoord("toadstool_entrance:inside", 0x2bd, 80, 124),
    EntranceCoord("toadstool_entrance", 0x62, 120, 66),
    EntranceCoord("toadstool_exit", 0x50, 136, 50),
    EntranceCoord("toadstool_exit:inside", 0x2ab, 80, 124),
    EntranceCoord("prairie_madbatter:inside", 0x1e0, 136, 112),
    EntranceCoord("hookshot_cave", 0x42, 56, 66),
    EntranceCoord("castle_upper_right:inside", 0x2d6, 80, 124),
    EntranceCoord("forest_madbatter", 0x52, 104, 48),
    EntranceCoord("writes_phone:inside", 0x29b, 80, 124),
    EntranceCoord("writes_phone", 0x31, 104, 82),
    EntranceCoord("d0:inside", 0x312, 80, 92),
    EntranceCoord("writes_house", 0x30, 120, 50),
    EntranceCoord("writes_cave_left:inside", 0x2ae, 80, 124),
    EntranceCoord("writes_cave_left", 0x20, 136, 50),
    EntranceCoord("writes_cave_right:inside", 0x2af, 80, 124),
    EntranceCoord("writes_cave_right", 0x21, 24, 50),
    EntranceCoord("d6:inside", 0x1d4, 80, 124),
    EntranceCoord("d2", 0x24, 56, 34),
    EntranceCoord("animal_house5:inside", 0x2d7, 80, 124),
    EntranceCoord("moblin_cave", 0x35, 104, 80),
    EntranceCoord("crazy_tracy:inside", 0x2ad, 80, 124),
    EntranceCoord("crazy_tracy", 0x45, 136, 66),
    EntranceCoord("photo_house:inside", 0x2b5, 80, 124),
    EntranceCoord("photo_house", 0x37, 72, 66),
    EntranceCoord("obstacle_cave_entrance:inside", 0x2b6, 80, 124),
    EntranceCoord("obstacle_cave_entrance", 0x17, 56, 50),
    EntranceCoord("left_to_right_taltalentrance:inside", 0x2ee, 120, 48),
    EntranceCoord("left_to_right_taltalentrance", 0x7, 56, 80),
    EntranceCoord("obstacle_cave_outside_chest:inside", 0x2bb, 80, 124),
    EntranceCoord("obstacle_cave_outside_chest", 0x18, 104, 18),
    EntranceCoord("obstacle_cave_exit:inside", 0x2bc, 48, 124),
    EntranceCoord("obstacle_cave_exit", 0x18, 136, 18),
    EntranceCoord("papahl_entrance:inside", 0x289, 64, 124),
    EntranceCoord("papahl_entrance", 0x19, 136, 64),
    EntranceCoord("papahl_exit:inside", 0x28b, 80, 124),
    EntranceCoord("papahl_exit", 0xa, 24, 112),
    EntranceCoord("rooster_house:inside", 0x29f, 80, 124),
    EntranceCoord("rooster_house", 0xa, 72, 34),
    EntranceCoord("d7:inside", 0x20e, 80, 124),
    EntranceCoord("bird_cave", 0xa, 120, 112),
    EntranceCoord("multichest_top:inside", 0x2f2, 80, 124),
    EntranceCoord("multichest_top", 0xd, 24, 112),
    EntranceCoord("multichest_left:inside", 0x2f9, 32, 124),
    EntranceCoord("multichest_left", 0x1d, 24, 48),
    EntranceCoord("multichest_right:inside", 0x2fa, 112, 124),
    EntranceCoord("multichest_right", 0x1d, 120, 80),
    EntranceCoord("right_taltal_connector1:inside", 0x280, 32, 124),
    EntranceCoord("right_taltal_connector1", 0x1e, 56, 16),
    EntranceCoord("right_taltal_connector3:inside", 0x283, 128, 124),
    EntranceCoord("right_taltal_connector3", 0x1e, 120, 16),
    EntranceCoord("right_taltal_connector2:inside", 0x282, 112, 124),
    EntranceCoord("right_taltal_connector2", 0x1f, 40, 16),
    EntranceCoord("right_fairy:inside", 0x1fb, 80, 124),
    EntranceCoord("right_fairy", 0x1f, 56, 80),
    EntranceCoord("right_taltal_connector4:inside", 0x287, 96, 124),
    EntranceCoord("right_taltal_connector4", 0x1f, 88, 64),
    EntranceCoord("right_taltal_connector5:inside", 0x28c, 96, 124),
    EntranceCoord("right_taltal_connector5", 0x1f, 120, 16),
    EntranceCoord("right_taltal_connector6:inside", 0x28e, 112, 124),
    EntranceCoord("right_taltal_connector6", 0xf, 72, 80),
    EntranceCoord("d7", 0x0e, 88, 48),
    EntranceCoord("left_taltal_entrance:inside", 0x2ea, 80, 124),
    EntranceCoord("left_taltal_entrance", 0x15, 136, 64),
    EntranceCoord("castle_jump_cave:inside", 0x1fd, 88, 80),
    EntranceCoord("madbatter_taltal", 0x4, 120, 112),
    EntranceCoord("fire_cave_exit:inside", 0x1ee, 24, 64),
    EntranceCoord("fire_cave_exit", 0x3, 72, 80),
    EntranceCoord("fire_cave_entrance:inside", 0x1fe, 112, 124),
    EntranceCoord("fire_cave_entrance", 0x13, 88, 16),
    EntranceCoord("phone_d8:inside", 0x299, 80, 124),
    EntranceCoord("phone_d8", 0x11, 104, 50),
    EntranceCoord("kennel:inside", 0x2b2, 80, 124),
    EntranceCoord("d8", 0x10, 88, 16),
    EntranceCoord("d8:inside", 0x25d, 80, 124),
]

entrance_lookup = {str(coord): coord for coord in entrance_coords}
