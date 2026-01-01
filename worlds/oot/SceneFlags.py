from math import ceil

from .LocationList import location_table

# Create a dict of dicts of the format:
# {
#   scene_number_n : {
#       room_setup_number: max_flags
#   }
# }
# where room_setup_number defines the room + scene setup as ((setup << 6) + room) for scene n
# and max_flags is the highest used enemy flag for that setup/room
def get_collectible_flag_table(world):
    scene_flags = {}
    alt_list = []
    for i in range(0, 101):
        max_room_num = 0
        max_enemy_flag = 0
        scene_flags[i] = {}
        for location in world.get_locations():
            if(location.scene == i and location.type in ["Freestanding", "Pot", "FlyingPot", "Crate", "SmallCrate", "Beehive", "RupeeTower"]):
                default = location.default
                if(isinstance(default, list)): #List of alternative room/setup/flag to use
                    primary_tuple = default[0]
                    for c in range(1,len(default)):
                        alt_list.append((location, default[c], primary_tuple))
                    default = location.default[0] #Use the first tuple as the primary tuple
                if(isinstance(default, tuple)):
                    room, setup, flag = default
                    room_setup = room + (setup << 6)
                    if(room_setup in scene_flags[i].keys()):
                        curr_room_max_flag = scene_flags[i][room_setup]
                        if flag > curr_room_max_flag:
                            scene_flags[i][room_setup] = flag
                    else:
                        scene_flags[i][room_setup] = flag
        if len(scene_flags[i].keys()) == 0:
            del scene_flags[i]
        #scene_flags.append((i, max_enemy_flag))
    return (scene_flags, alt_list)

# Create a byte array from the scene flag table created by get_collectible_flag_table
def get_collectible_flag_table_bytes(scene_flag_table):
    num_flag_bytes = 0
    bytes = bytearray()
    bytes.append(len(scene_flag_table.keys()))
    for scene_id in scene_flag_table.keys():
        rooms = scene_flag_table[scene_id]
        room_count = len(rooms.keys())
        bytes.append(scene_id)
        bytes.append(room_count)
        for room in rooms:
            bytes.append(room)
            bytes.append((num_flag_bytes & 0xFF00) >> 8)
            bytes.append(num_flag_bytes & 0x00FF )
            num_flag_bytes += ceil((rooms[room] + 1) / 8)
            
    return bytes, num_flag_bytes

def get_alt_list_bytes(alt_list):
    bytes = bytearray()
    for entry in alt_list:
        location, alt, primary = entry
        room, scene_setup, flag = alt
        alt_override = (room << 8) + (scene_setup << 14) + flag
        room, scene_setup, flag = primary
        primary_override = (room << 8) + (scene_setup << 14) + flag
        bytes.append(location.scene)
        bytes.append(0x06)
        bytes.append((alt_override & 0xFF00) >> 8)
        bytes.append(alt_override & 0xFF)
        bytes.append(location.scene)
        bytes.append(0x06)
        bytes.append((primary_override & 0xFF00) >> 8)
        bytes.append(primary_override & 0xFF)
    return bytes

# AP method to retrieve address + bit for each item
# Based on get_collectible_flag_offset in the C code
def get_collectible_flag_addresses(world, collectible_scene_flags_table):

    # Ported directly from get_items.c
    def get_collectible_flag_offset(scene: int, room: int, setup_id: int) -> int:
        num_scenes = collectible_scene_flags_table[0]
        index = 1
        scene_id = 0
        room_id = 0
        room_setup_count = 0
        room_byte_offset = 0
        # Loop through collectible_scene_flags_table until we find the right scene
        while num_scenes > 0:
            scene_id = collectible_scene_flags_table[index]
            room_setup_count = collectible_scene_flags_table[index+1]
            index += 2
            if scene_id == scene:  # found the scene
                # Loop through each room/setup combination until we find the right one.
                for i in range(room_setup_count):
                    room_id = collectible_scene_flags_table[index] & 0x3F
                    setup_id_temp = (collectible_scene_flags_table[index] & 0xC0) >> 6
                    room_byte_offset = (collectible_scene_flags_table[index+1] << 8) + collectible_scene_flags_table[index+2]
                    index += 3
                    if room_id == room and setup_id_temp == setup_id:
                        return room_byte_offset
            else:  # Not the right scene, skip to the next one
                index += 3 * room_setup_count
            num_scenes -= 1
        return -1

    collectible_flag_addresses = {}
    for location in world.get_locations():
        if location.type in ["Freestanding", "Pot", "FlyingPot", "Crate", "SmallCrate", "Beehive", "RupeeTower"]:
            default = location.default
            if isinstance(default, list):
                default = default[0]
            room, setup, flag = default
            offset = get_collectible_flag_offset(location.scene, room, setup)
            item_id = location.address
            collectible_flag_addresses[item_id] = [offset, flag]
    return collectible_flag_addresses

