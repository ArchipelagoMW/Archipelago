# mzxrules 2018
# In order to patch MQ to the existing data...
#
# Scenes:
#
# Ice Cavern (Scene 9) needs to have it's header altered to support MQ's path list. This
# expansion will delete the otherwise unused alternate headers command
#
# Transition actors will be patched over the old data, as the number of records is the same
# Path data will be appended to the end of the scene file.
#
# The size of a single path on file is NUM_POINTS * 6, rounded up to the nearest 4 byte boundary
# The total size consumed by the path data is NUM_PATHS * 8, plus the sum of all path file sizes
# padded to the nearest 0x10 bytes
#
# Collision:
# OoT's collision data consists of these elements: vertices, surface types, water boxes,
# camera behavior data, and polys. MQ's vertice and polygon geometry data is identical.
# However, the surface types and the collision exclusion flags bound to the polys have changed
# for some polygons, as well as the number of surface type records and camera type records.
#
# To patch collision, a flag denotes whether collision data cannot be written in place without
# expanding the size of the scene file. If true, the camera data is relocated to the end
# of the scene file, and the surface types are shifted down into where the camera types
# were situated. If false, the camera data isn't moved, but rather the surface type list
# will be shifted to the end of the camera data
#
# Rooms:
#
# Object file initialization data will be appended to the end of the room file.
# The total size consumed by the object file data is NUM_OBJECTS * 0x02, aligned to
# the nearest 0x04 bytes
#
# Actor spawn data will be appended to the end of the room file, after the objects.
# The total size consumed by the actor spawn data is NUM_ACTORS * 0x10
#
# Finally:
#
# Scene and room files will be padded to the nearest 0x10 bytes
#
# Maps:
# Jabu Jabu's B1 map contains no chests in the vanilla layout. Because of this,
# the floor map data is missing a vertex pointer that would point within kaleido_scope.
# As such, if the file moves, the patch will break.

from .Utils import data_path
from .Rom import Rom
import json
from struct import pack, unpack

SCENE_TABLE = 0xB71440


class File(object):
    def __init__(self, file):
        self.name = file['Name']
        self.start = int(file['Start'], 16) if 'Start' in file else 0
        self.end = int(file['End'], 16) if 'End' in file else self.start
        self.remap = file['RemapStart'] if 'RemapStart' in file else None
        self.from_file = self.start

        # used to update the file's associated dmadata record
        self.dma_key = self.start

        if self.remap is not None:
            self.remap = int(self.remap, 16)

    def __repr__(self):
        remap = "None"
        if self.remap is not None:
            remap = "{0:x}".format(self.remap)
        return "{0}: {1:x} {2:x}, remap {3}".format(self.name, self.start, self.end, remap)

    def relocate(self, rom:Rom):
        if self.remap is None:
            self.remap = rom.free_space()

        new_start = self.remap

        offset = new_start - self.start
        new_end = self.end + offset

        rom.buffer[new_start:new_end] = rom.buffer[self.start:self.end]
        self.start = new_start
        self.end = new_end
        update_dmadata(rom, self)

    # The file will now refer to the new copy of the file
    def copy(self, rom:Rom):
        self.dma_key = None
        self.relocate(rom)


class CollisionMesh(object):
    def __init__(self, rom:Rom, start, offset):
        self.offset = offset
        self.poly_addr = rom.read_int32(start + offset + 0x18)
        self.polytypes_addr = rom.read_int32(start + offset + 0x1C)
        self.camera_data_addr = rom.read_int32(start + offset + 0x20)
        self.polytypes = (self.poly_addr - self.polytypes_addr) // 8

    def write_to_scene(self, rom:Rom, start):
        addr = start + self.offset + 0x18
        rom.write_int32s(addr, [self.poly_addr, self.polytypes_addr, self.camera_data_addr])


class ColDelta(object):
    def __init__(self, delta):
        self.is_larger = delta['IsLarger']
        self.polys = delta['Polys']
        self.polytypes = delta['PolyTypes']
        self.cams = delta['Cams']


class Icon(object):
    def __init__(self, data):
        self.icon = data["Icon"];
        self.count = data["Count"];
        self.points = [IconPoint(x) for x in data["IconPoints"]]

    def write_to_minimap(self, rom:Rom, addr):
        rom.write_sbyte(addr, self.icon)
        rom.write_byte(addr + 1,  self.count)
        cur = 2
        for p in self.points:
            p.write_to_minimap(rom, addr + cur)
            cur += 0x03

    def write_to_floormap(self, rom:Rom, addr):
        rom.write_int16(addr, self.icon)
        rom.write_int32(addr + 0x10, self.count)

        cur = 0x14
        for p in self.points:
            p.write_to_floormap(rom, addr + cur)
            cur += 0x0C


class IconPoint(object):
    def __init__(self, point):
        self.flag = point["Flag"]
        self.x = point["x"]
        self.y = point["y"]

    def write_to_minimap(self, rom:Rom, addr):
        rom.write_sbyte(addr, self.flag)
        rom.write_byte(addr+1, self.x)
        rom.write_byte(addr+2, self.y)

    def write_to_floormap(self, rom:Rom, addr):
        rom.write_int16(addr, self.flag)
        rom.write_f32(addr + 4, float(self.x))
        rom.write_f32(addr + 8, float(self.y))


class Scene(object):
    def __init__(self, scene):
        self.file = File(scene['File'])
        self.id = scene['Id']
        self.transition_actors = [convert_actor_data(x) for x in scene['TActors']]
        self.rooms = [Room(x) for x in scene['Rooms']]
        self.paths = []
        self.coldelta = ColDelta(scene["ColDelta"])
        self.minimaps = [[Icon(icon) for icon in minimap['Icons']] for minimap in scene['Minimaps']]
        self.floormaps = [[Icon(icon) for icon in floormap['Icons']] for floormap in scene['Floormaps']]
        temp_paths = scene['Paths']
        for item in temp_paths:
            self.paths.append(item['Points'])


    def write_data(self, rom:Rom):
        # write floormap and minimap data
        self.write_map_data(rom)

        # move file to remap address
        if self.file.remap is not None:
            self.file.relocate(rom)

        start = self.file.start
        headcur = self.file.start

        room_list_offset = 0

        code = rom.read_byte(headcur)
        loop = 0x20
        while loop > 0 and code != 0x14: #terminator
            loop -= 1

            if code == 0x03: #collision
                col_mesh_offset = rom.read_int24(headcur + 5)
                col_mesh = CollisionMesh(rom, start, col_mesh_offset)
                self.patch_mesh(rom, col_mesh);

            elif code == 0x04: #rooms
                room_list_offset = rom.read_int24(headcur + 5)

            elif code == 0x0D: #paths
                path_offset = self.append_path_data(rom)
                rom.write_int32(headcur + 4, path_offset)

            elif code == 0x0E: #transition actors
                t_offset = rom.read_int24(headcur + 5)
                addr = self.file.start + t_offset
                write_actor_data(rom, addr, self.transition_actors)

            headcur += 8
            code = rom.read_byte(headcur)

        # update file references
        self.file.end = align16(self.file.end)
        update_dmadata(rom, self.file)
        update_scene_table(rom, self.id, self.file.start, self.file.end)

        # write room file data
        for room in self.rooms:
            room.write_data(rom)
            if self.id == 6 and room.id == 6:
                patch_spirit_temple_mq_room_6(rom, room.file.start)

        cur = self.file.start + room_list_offset
        for room in self.rooms:
            rom.write_int32s(cur, [room.file.start, room.file.end])
            cur += 0x08


    def write_map_data(self, rom:Rom):
        if self.id >= 10:
            return

        # write floormap
        floormap_indices = 0xB6C934
        floormap_vrom = 0xBC7E00
        floormap_index = rom.read_int16(floormap_indices + (self.id * 2))
        floormap_index //= 2 # game uses texture index, where two textures are used per floor

        cur = floormap_vrom + (floormap_index * 0x1EC)
        for floormap in self.floormaps:
            for icon in floormap:
                Icon.write_to_floormap(icon, rom, cur)
                cur += 0xA4


        # fixes jabu jabu floor B1 having no chest data
        if self.id == 2:
            cur = floormap_vrom + (0x08 * 0x1EC + 4)
            kaleido_scope_chest_verts = 0x803A3DA0 # hax, should be vram 0x8082EA00
            rom.write_int32s(cur, [0x17, kaleido_scope_chest_verts, 0x04])

        # write minimaps
        map_mark_vrom = 0xBF40D0
        map_mark_vram = 0x808567F0
        map_mark_array_vram = 0x8085D2DC # ptr array in map_mark_data to minimap "marks"

        array_vrom = map_mark_array_vram - map_mark_vram + map_mark_vrom
        map_mark_scene_vram = rom.read_int32(self.id * 4 + array_vrom)
        mark_vrom = map_mark_scene_vram - map_mark_vram + map_mark_vrom

        cur = mark_vrom
        for minimap in self.minimaps:
            for icon in minimap:
                Icon.write_to_minimap(icon, rom, cur)
                cur += 0x26


    def patch_mesh(self, rom:Rom, mesh:CollisionMesh):
        start = self.file.start

        final_cams = []

        # build final camera data
        for cam in self.coldelta.cams:
            data = cam['Data']
            pos = cam['PositionIndex']
            if pos < 0:
                final_cams.append((data, 0))
            else:
                addr = start + (mesh.camera_data_addr & 0xFFFFFF)
                seg_off = rom.read_int32(addr + (pos * 8) + 4)
                final_cams.append((data, seg_off))

        types_move_addr = 0

        # if data can't fit within the old mesh space, append camera data
        if self.coldelta.is_larger:
            types_move_addr = mesh.camera_data_addr

            # append to end of file
            self.write_cam_data(rom, self.file.end, final_cams)
            mesh.camera_data_addr = get_segment_address(2, self.file.end - self.file.start)
            self.file.end += len(final_cams) * 8

        else:
            types_move_addr = mesh.camera_data_addr + (len(final_cams) * 8)

            # append in place
            addr = self.file.start + (mesh.camera_data_addr & 0xFFFFFF)
            self.write_cam_data(rom, addr, final_cams)

        # if polytypes needs to be moved, do so
        if (types_move_addr != mesh.polytypes_addr):
            a_start = self.file.start + (mesh.polytypes_addr & 0xFFFFFF)
            b_start = self.file.start + (types_move_addr & 0xFFFFFF)
            size = mesh.polytypes * 8

            rom.buffer[b_start:b_start + size] = rom.buffer[a_start:a_start + size]
            mesh.polytypes_addr = types_move_addr

        # patch polytypes
        for item in self.coldelta.polytypes:
            id = item['Id']
            high = item['High']
            low = item['Low']
            addr = self.file.start + (mesh.polytypes_addr & 0xFFFFFF) + (id * 8)
            rom.write_int32s(addr, [high, low])

        # patch poly data
        for item in self.coldelta.polys:
            id = item['Id']
            t = item['Type']
            flags = item['Flags']

            addr = self.file.start + (mesh.poly_addr & 0xFFFFFF) + (id * 0x10)
            vert_bit =  rom.read_byte(addr + 0x02) & 0x1F # VertexA id data
            rom.write_int16(addr, t)
            rom.write_byte(addr + 0x02, (flags << 5) + vert_bit)

        # Write Mesh to Scene
        mesh.write_to_scene(rom, self.file.start)


    def write_cam_data(self, rom:Rom, addr, cam_data):

        for item in cam_data:
            data, pos = item
            rom.write_int32s(addr, [data, pos])
            addr += 8


    # appends path data to the end of the rom
    # returns segment address to path data
    def append_path_data(self, rom:Rom):
        start = self.file.start
        cur = self.file.end
        records = []

        for path in self.paths:
            nodes = len(path)
            offset = get_segment_address(2, cur - start)
            records.append((nodes, offset))

            #flatten
            points = [x for points in path for x in points]
            rom.write_int16s(cur, points)
            path_size = align4(len(path) * 6)
            cur += path_size

        records_offset = get_segment_address(2, cur - start)
        for node, offset in records:
            rom.write_byte(cur, node)
            rom.write_int32(cur + 4, offset)
            cur += 8

        self.file.end = cur
        return records_offset


class Room(object):
    def __init__(self, room):
        self.file = File(room['File'])
        self.id = room['Id']
        self.objects = [int(x, 16) for x in room['Objects']]
        self.actors = [convert_actor_data(x) for x in room['Actors']]

    def write_data(self, rom:Rom):
        # move file to remap address
        if self.file.remap is not None:
            self.file.relocate(rom)

        headcur = self.file.start

        code = rom.read_byte(headcur)
        loop = 0x20
        while loop != 0 and code != 0x14: #terminator
            loop -= 1

            if code == 0x01: # actors
                offset = self.file.end - self.file.start
                write_actor_data(rom, self.file.end, self.actors)
                self.file.end += len(self.actors) * 0x10

                rom.write_byte(headcur + 1, len(self.actors))
                rom.write_int32(headcur + 4, get_segment_address(3, offset))

            elif code == 0x0B: # objects
                offset = self.append_object_data(rom, self.objects)

                rom.write_byte(headcur + 1, len(self.objects))
                rom.write_int32(headcur + 4, get_segment_address(3, offset))

            headcur += 8
            code = rom.read_byte(headcur)

        # update file reference
        self.file.end = align16(self.file.end)
        update_dmadata(rom, self.file)


    def append_object_data(self, rom:Rom, objects):
        offset = self.file.end - self.file.start
        cur = self.file.end
        rom.write_int16s(cur, objects)

        objects_size = align4(len(objects) * 2)
        self.file.end += objects_size
        return offset


def patch_files(rom:Rom, mq_scenes:list):

    data = get_json()
    scenes = [Scene(x) for x in data]
    for scene in scenes:
        if scene.id in mq_scenes:
            if scene.id == 9:
                patch_ice_cavern_scene_header(rom)
            scene.write_data(rom)



def get_json():
    with open(data_path('mqu.json'), 'r') as stream:
        data = json.load(stream)
    return data


def convert_actor_data(str):
    spawn_args = str.split(" ")
    return [ int(x,16) for x in spawn_args ]


def get_segment_address(base, offset):
    offset &= 0xFFFFFF
    base *= 0x01000000
    return base + offset


def patch_ice_cavern_scene_header(rom):
    rom.buffer[0x2BEB000:0x2BEB038] = rom.buffer[0x2BEB008:0x2BEB040]
    rom.write_int32s(0x2BEB038, [0x0D000000, 0x02000000])


def patch_spirit_temple_mq_room_6(rom:Rom, room_addr):
    cur = room_addr

    actor_list_addr = 0
    cmd_actors_offset = 0

    # scan for actor list and header end
    code = rom.read_byte(cur)
    while code != 0x14: #terminator
        if code == 0x01: # actors
            actor_list_addr = rom.read_int32(cur + 4)
            cmd_actors_offset = cur - room_addr

        cur += 8
        code = rom.read_byte(cur)

    cur += 8

    # original header size
    header_size = cur - room_addr

    # set alternate header data location
    alt_data_off = header_size + 8

    # set new alternate header offset
    alt_header_off = align16(alt_data_off + (4 * 3)) # alt header record size * num records

    # write alternate header data
    # the first 3 words are mandatory. the last 3 are just to make the binary
    # cleaner to read
    rom.write_int32s(room_addr + alt_data_off,
                    [0, get_segment_address(3, alt_header_off), 0, 0, 0, 0])

    # clone header
    a_start = room_addr
    a_end = a_start + header_size
    b_start = room_addr + alt_header_off
    b_end = b_start + header_size

    rom.buffer[b_start:b_end] = rom.buffer[a_start:a_end]

    # make the child header skip the first actor,
    # which avoids the spawning of the block while in the hole
    cmd_addr = room_addr + cmd_actors_offset
    actor_list_addr += 0x10
    actors = rom.read_byte(cmd_addr + 1)
    rom.write_byte(cmd_addr+1, actors - 1)
    rom.write_int32(cmd_addr + 4, actor_list_addr)

    # move header
    rom.buffer[a_start + 8:a_end + 8] = rom.buffer[a_start:a_end]

    # write alternate header command
    seg = get_segment_address(3, alt_data_off)
    rom.write_int32s(room_addr, [0x18000000, seg])


def verify_remap(scenes):
    def test_remap(file:File):
        if file.remap is not None:
            if file.start < file.remap:
                return False
        return True
    print("test code: verify remap won't corrupt data")

    for scene in scenes:
        file = scene.file
        result = test_remap(file)
        print("{0} - {1}".format(result, file))

        for room in scene.rooms:
            file = room.file
            result = test_remap(file)
            print("{0} - {1}".format(result, file))


def update_dmadata(rom:Rom, file:File):
    key, start, end, from_file = file.dma_key, file.start, file.end, file.from_file
    rom.update_dmadata_record(key, start, end, from_file)
    file.dma_key = file.start

def update_scene_table(rom:Rom, sceneId, start, end):
    cur = sceneId * 0x14 + SCENE_TABLE
    rom.write_int32s(cur, [start, end])


def write_actor_data(rom:Rom, cur, actors):
    for actor in actors:
        rom.write_int16s(cur, actor)
        cur += 0x10

def align4(value):
    return ((value + 3) // 4) * 4

def align16(value):
    return ((value + 0xF) // 0x10) * 0x10

# This function inserts space in a ovl section at the section's offset
# The section size is expanded
# Every relocation entry in the section after the offet is moved accordingly
# Every relocation value that is after the inserted space is increased accordingly
def insert_space(rom, file, vram_start, insert_section, insert_offset, insert_size):
    sections = []
    val_hi = {}
    adr_hi = {}

    # get the ovl header
    cur = file.end - rom.read_int32(file.end - 4)
    section_total = 0
    for i in range(0, 4):
        # build the section offsets
        section_size = rom.read_int32(cur)
        sections.append(section_total)
        section_total += section_size

        # increase the section to be expanded
        if insert_section == i:
            rom.write_int32(cur, section_size + insert_size)

        cur += 4

    # calculate the insert address in vram
    insert_vram = sections[insert_section] + insert_offset + vram_start
    insert_rom = sections[insert_section] + insert_offset + file.start

    # iterate over the relocation table
    relocate_count = rom.read_int32(cur)
    cur += 4
    for i in range(0, relocate_count):
        entry = rom.read_int32(cur)

        # parse relocation entry
        section = ((entry & 0xC0000000) >> 30) - 1
        type = (entry & 0x3F000000) >> 24
        offset = entry & 0x00FFFFFF

        # calculate relocation address in rom
        address = file.start + sections[section] + offset

        # move relocation if section is increased and it's after the insert
        if insert_section == section and offset >= insert_offset:
            # rebuild new relocation entry
            rom.write_int32(cur,
                ((section + 1) << 30) |
                (type << 24) |
                (offset + insert_size))

        # value contains the vram address
        value = rom.read_int32(address)
        raw_value = value
        if type == 2:
            # Data entry: value is the raw vram address
            pass
        elif type == 4:
            # Jump OP: Get the address from a Jump instruction
            value = 0x80000000 | (value & 0x03FFFFFF) << 2
        elif type == 5:
            # Load High: Upper half of an address load
            reg = (value >> 16) & 0x1F
            val_hi[reg] = (value & 0x0000FFFF) << 16
            adr_hi[reg] = address
            # Do not process, wait until the lower half is read
            value = None
        elif type == 6:
            # Load Low: Lower half of the address load
            reg = (value >> 21) & 0x1F
            val_low = value & 0x0000FFFF
            val_low = unpack('h', pack('H', val_low))[0]
            # combine with previous load high
            value = val_hi[reg] + val_low
        else:
            # unknown. OoT does not use any other types
            value = None

        # update the vram values if it's been moved
        if value != None and value >= insert_vram:
            # value = new vram address
            new_value = value + insert_size

            if type == 2:
                # Data entry: value is the raw vram address
                rom.write_int32(address, new_value)
            elif type == 4:
                # Jump OP: Set the address in the Jump instruction
                op = rom.read_int32(address) & 0xFC000000
                new_value = (new_value & 0x0FFFFFFC) >> 2
                new_value = op | new_value
                rom.write_int32(address, new_value)
            elif type == 6:
                # Load Low: Lower half of the address load
                op = rom.read_int32(address) & 0xFFFF0000
                new_val_low = new_value & 0x0000FFFF
                rom.write_int32(address, op | new_val_low)

                # Load High: Upper half of an address load
                op = rom.read_int32(adr_hi[reg]) & 0xFFFF0000
                new_val_hi = (new_value & 0xFFFF0000) >> 16
                if new_val_low >= 0x8000:
                    # add 1 if the lower part is negative for borrow
                    new_val_hi += 1
                rom.write_int32(adr_hi[reg], op | new_val_hi)

        cur += 4

    # Move rom bytes
    rom.buffer[(insert_rom + insert_size):(file.end + insert_size)] = rom.buffer[insert_rom:file.end]
    rom.buffer[insert_rom:(insert_rom + insert_size)] = [0] * insert_size
    file.end += insert_size


def add_relocations(rom, file, addresses):
    relocations = []
    sections = []
    header_size = rom.read_int32(file.end - 4)
    header = file.end - header_size
    cur = header

    # read section sizes and build offsets
    section_total = 0
    for i in range(0, 4):
        section_size = rom.read_int32(cur)
        sections.append(section_total)
        section_total += section_size
        cur += 4

    # get all entries in relocation table
    relocate_count = rom.read_int32(cur)
    cur += 4
    for i in range(0, relocate_count):
        relocations.append(rom.read_int32(cur))
        cur += 4

    # create new enties
    for address in addresses:
        if isinstance(address, tuple):
            # if type provided use it
            type, address = address
        else:
            # Otherwise, try to infer type from value
            value = rom.read_int32(address)
            op = value >> 26
            type = 2 # default: data
            if op == 0x02 or op == 0x03: # j or jal
                type = 4
            elif op == 0x0F: # lui
                type = 5
            elif op == 0x08: # addi
                type = 6

        # Calculate section and offset
        address = address - file.start
        section = 0
        for section_start in sections:
            if address >= section_start:
                section += 1
            else:
                break
        offset = address - sections[section - 1]

        # generate relocation entry
        relocations.append((section << 30)
                        | (type << 24)
                        | (offset & 0x00FFFFFF))

    # Rebuild Relocation Table
    cur = header + 0x10
    relocations.sort(key = lambda val: val & 0xC0FFFFFF)
    rom.write_int32(cur, len(relocations))
    cur += 4
    for relocation in relocations:
        rom.write_int32(cur, relocation)
        cur += 4

    # Add padded 0?
    rom.write_int32(cur, 0)
    cur += 4

    # Update Header and File size
    new_header_size = (cur + 4) - header
    rom.write_int32(cur, new_header_size)
    file.end += (new_header_size - header_size)
