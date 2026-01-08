from ..data.map_property import MapProperty

from ..data import npcs as npcs
from ..data.npc import NPC

from ..data.chests import Chests

from ..data import map_events as events
from ..data.map_event import MapEvent, LongMapEvent

from ..data import map_exits as exits
from ..data.map_exit import ShortMapExit, LongMapExit

from ..data import world_map_event_modifications as world_map_event_modifications
from ..data.world_map import WorldMap

from ..instruction import asm as asm
from ..memory.space import Reserve

class Maps():
    MAP_COUNT = 416

    EVENT_PTR_START = 0x40000
    LONG_EVENT_PTR_START = events.LongMapEvents.POINTER_START_ADDR_LONG
    ENTRANCE_EVENTS_START_ADDR = 0x11fa00

    SHORT_EXIT_PTR_START = 0x1fbb00
    LONG_EXIT_PTR_START = 0x2df480

    NPCS_PTR_START = 0x41a10

    def __init__(self, rom, args, items):
        self.rom = rom
        self.args = args

        self.npcs = npcs.NPCs(rom)
        self.chests = Chests(self.rom, self.args, items)
        self.events = events.MapEvents(rom)
        self.long_events = events.LongMapEvents(rom)
        self.exits = exits.MapExits(rom)
        self.world_map_event_modifications = world_map_event_modifications.WorldMapEventModifications(rom)
        self.world_map = WorldMap(rom, args)
        self.read()

    def read(self):
        self.maps = []
        self.properties = []

        for map_index in range(self.MAP_COUNT):
            self.maps.append({"id" : map_index})

            map_property = MapProperty(self.rom, map_index)
            self.properties.append(map_property)
            self.maps[map_index]["name_index"] = map_property.name_index

            entrance_event_start = self.ENTRANCE_EVENTS_START_ADDR + map_index * self.rom.LONG_PTR_SIZE
            entrance_event = self.rom.get_bytes(entrance_event_start, self.rom.LONG_PTR_SIZE)
            self.maps[map_index]["entrance_event_address"] = entrance_event[0] | (entrance_event[1] << 8) | (entrance_event[2] << 16)

            events_ptr_address = self.EVENT_PTR_START + map_index * self.rom.SHORT_PTR_SIZE
            events_ptr = self.rom.get_bytes(events_ptr_address, self.rom.SHORT_PTR_SIZE)
            self.maps[map_index]["events_ptr"] = events_ptr[0] | (events_ptr[1] << 8)

            # LONG EVENTS INITIALIZATION: Vanilla code has no long events.
            # Set initial offset to the vanilla value for each map.
            self.maps[map_index]["long_events_ptr"] = self.maps[0]["events_ptr"]

            short_exit_ptr_address = self.SHORT_EXIT_PTR_START + map_index * self.rom.SHORT_PTR_SIZE
            short_exit_ptr = self.rom.get_bytes(short_exit_ptr_address, self.rom.SHORT_PTR_SIZE)
            self.maps[map_index]["short_exits_ptr"] = short_exit_ptr[0] | (short_exit_ptr[1] << 8)

            long_exit_ptr_address = self.LONG_EXIT_PTR_START + map_index * self.rom.SHORT_PTR_SIZE
            long_exit_ptr = self.rom.get_bytes(long_exit_ptr_address, self.rom.SHORT_PTR_SIZE)
            self.maps[map_index]["long_exits_ptr"] = long_exit_ptr[0] | (long_exit_ptr[1] << 8)

            npcs_ptr_address = self.NPCS_PTR_START + map_index * self.rom.SHORT_PTR_SIZE
            npcs_ptr = self.rom.get_bytes(npcs_ptr_address, self.rom.SHORT_PTR_SIZE)
            self.maps[map_index]["npcs_ptr"] = npcs_ptr[0] | (npcs_ptr[1] << 8)

    def set_entrance_event(self, map_id, event_address):
        self.maps[map_id]["entrance_event_address"] = event_address

    def get_entrance_event(self, map_id):
        return self.maps[map_id]["entrance_event_address"]

    def get_npc_index(self, map_id, npc_id):
        first_npc_index = (self.maps[map_id]["npcs_ptr"] - self.maps[0]["npcs_ptr"]) // NPC.DATA_SIZE
        return first_npc_index + (npc_id - 0x10)

    def get_npc(self, map_id, npc_id):
        return self.npcs.get_npc(self.get_npc_index(map_id, npc_id))

    def append_npc(self, map_id, new_npc):
        prev_npc_count = self.get_npc_count(map_id)
        new_npc_id = 0x10 + prev_npc_count

        for map_index in range(map_id + 1, self.MAP_COUNT):
            self.maps[map_index]["npcs_ptr"] += NPC.DATA_SIZE

        npc_index = (self.maps[map_id]["npcs_ptr"] - self.maps[0]["npcs_ptr"]) // NPC.DATA_SIZE
        npc_index += prev_npc_count # add new npc to the end of current map's npcs
        self.npcs.add_npc(npc_index, new_npc)

        return new_npc_id # return id of the new npc

    def remove_npc(self, map_id, npc_id):
        for map_index in range(map_id + 1, self.MAP_COUNT):
            self.maps[map_index]["npcs_ptr"] -= NPC.DATA_SIZE

        self.npcs.remove_npc(self.get_npc_index(map_id, npc_id))

    def get_npc_count(self, map_id):
        return (self.maps[map_id + 1]["npcs_ptr"] - self.maps[map_id]["npcs_ptr"]) // NPC.DATA_SIZE

    def get_chest_count(self, map_id):
        return self.chests.chest_count(map_id)

    def set_chest_item(self, map_id, x, y, item_id):
        self.chests.set_item(map_id, x, y, item_id)

    def get_event_count(self, map_id):
        return (self.maps[map_id + 1]["events_ptr"] - self.maps[map_id]["events_ptr"]) // MapEvent.DATA_SIZE

    def print_events(self, map_id):
        first_event_id = (self.maps[map_id]["events_ptr"] - self.maps[0]["events_ptr"]) // MapEvent.DATA_SIZE

        self.events.print_range(first_event_id, self.get_event_count(map_id))

    def get_event(self, map_id, x, y):
        first_event_id = (self.maps[map_id]["events_ptr"] - self.maps[0]["events_ptr"]) // MapEvent.DATA_SIZE
        last_event_id = first_event_id + self.get_event_count(map_id)
        return self.events.get_event(first_event_id, last_event_id, x, y)

    def add_event(self, map_id, new_event):
        for map_index in range(map_id + 1, self.MAP_COUNT):
            self.maps[map_index]["events_ptr"] += MapEvent.DATA_SIZE

        event_id = (self.maps[map_id]["events_ptr"] - self.maps[0]["events_ptr"]) // MapEvent.DATA_SIZE
        self.events.add_event(event_id, new_event)

    def delete_event(self, map_id, x, y):
        for map_index in range(map_id + 1, self.MAP_COUNT):
            self.maps[map_index]["events_ptr"] -= MapEvent.DATA_SIZE

        first_event_id = (self.maps[map_id]["events_ptr"] - self.maps[0]["events_ptr"]) // MapEvent.DATA_SIZE
        last_event_id = first_event_id + self.get_event_count(map_id)
        self.events.delete_event(first_event_id, last_event_id, x, y)

    ### LONG EVENTS ###
    def get_long_event_count(self, map_id):
        return (self.maps[map_id + 1]["long_events_ptr"] - self.maps[map_id][
            "long_events_ptr"]) // LongMapEvent.DATA_SIZE

    def print_long_events(self, map_id):
        first_event_id = (self.maps[map_id]["long_events_ptr"] - self.maps[0][
            "long_events_ptr"]) // LongMapEvent.DATA_SIZE

        self.long_events.print_range(first_event_id, self.get_event_count(map_id))

    def get_long_event(self, map_id, x, y):
        first_event_id = (self.maps[map_id]["long_events_ptr"] - self.maps[0][
            "long_events_ptr"]) // LongMapEvent.DATA_SIZE
        last_event_id = first_event_id + self.get_event_count(map_id)
        return self.long_events.get_event(first_event_id, last_event_id, x, y)

    def add_long_event(self, map_id, new_event):
        for map_index in range(map_id + 1, self.MAP_COUNT):
            self.maps[map_index]["long_events_ptr"] += LongMapEvent.DATA_SIZE

        event_id = (self.maps[map_id]["long_events_ptr"] - self.maps[0][
            "long_events_ptr"]) // LongMapEvent.DATA_SIZE
        self.long_events.add_event(event_id, new_event)

    def delete_long_event(self, map_id, x, y):
        for map_index in range(map_id + 1, self.MAP_COUNT):
            self.maps[map_index]["long_events_ptr"] -= LongMapEvent.DATA_SIZE

        first_event_id = (self.maps[map_id]["long_events_ptr"] - self.maps[0][
            "long_events_ptr"]) // LongMapEvent.DATA_SIZE
        last_event_id = first_event_id + self.get_event_count(map_id)
        self.long_events.delete_event(first_event_id, last_event_id, x, y)
    ### LONG EVENTS ###

    def get_short_exit_count(self, map_id):
        return (self.maps[map_id + 1]["short_exits_ptr"] - self.maps[map_id]["short_exits_ptr"]) // ShortMapExit.DATA_SIZE

    def print_short_exits(self, map_id):
        first_exit_id = (self.maps[map_id]["short_exits_ptr"] - self.maps[0]["short_exits_ptr"]) // ShortMapExit.DATA_SIZE
        self.exits.print_short_exit_range(first_exit_id, self.get_short_exit_count(map_id))

    def delete_short_exit(self, map_id, x, y):
        for map_index in range(map_id + 1, self.MAP_COUNT):
            self.maps[map_index]["short_exits_ptr"] -= ShortMapExit.DATA_SIZE

        map_first_short_exit = (self.maps[map_id]["short_exits_ptr"] - self.maps[0]["short_exits_ptr"]) // ShortMapExit.DATA_SIZE
        self.exits.delete_short_exit(map_first_short_exit, x, y)

    def get_long_exit_count(self, map_id):
        return (self.maps[map_id + 1]["long_exits_ptr"] - self.maps[map_id]["long_exits_ptr"]) // LongMapExit.DATA_SIZE

    def print_long_exits(self, map_id):
        first_exit_id = (self.maps[map_id]["long_exits_ptr"] - self.maps[0]["long_exits_ptr"]) // LongMapExit.DATA_SIZE
        self.exits.print_long_exit_range(first_exit_id, self.get_long_exit_count(map_id))

    def _fix_imperial_camp_boxes(self):
        # near the northern tent normally accessed by jumping over a wall
        # there is a box which can be walked into but not out of which causes the game to lock
        # fix the three boxes to no longer be walkable

        from ..ff6wcutils.compression import compress, decompress
        layer1_tilemap = 0x1c
        tilemap_ptrs_start = 0x19cd90
        tilemap_ptr_addr = tilemap_ptrs_start + layer1_tilemap * self.rom.LONG_PTR_SIZE
        tilemap_addr_bytes = self.rom.get_bytes(tilemap_ptr_addr, self.rom.LONG_PTR_SIZE)
        tilemap_addr = int.from_bytes(tilemap_addr_bytes, byteorder = "little")

        next_tilemap_ptr_addr = tilemap_ptr_addr + self.rom.LONG_PTR_SIZE
        next_tilemap_addr_bytes = self.rom.get_bytes(next_tilemap_ptr_addr, self.rom.LONG_PTR_SIZE)
        next_tilemap_addr = int.from_bytes(next_tilemap_addr_bytes, byteorder = "little")

        tilemaps_start = 0x19d1b0
        tilemap_len = next_tilemap_addr - tilemap_addr
        tilemap = self.rom.get_bytes(tilemaps_start + tilemap_addr, tilemap_len)
        decompressed = decompress(tilemap)

        map_width = 64
        impassable_box_tile = 62 # box tile that cannot be entered
        coordinates = [(19, 13), (15, 14), (18, 14)] # coordinates of boxes to change
        for coordinate in coordinates:
            decompressed[coordinate[0] + coordinate[1] * map_width] = impassable_box_tile

        compressed = compress(decompressed)
        self.rom.set_bytes(tilemaps_start + tilemap_addr, compressed)

    def _fix_Cid_timer_glitch(self):
        from ..memory.space import Bank, Write
        from ..instruction import field as field
        from ..event.event import EVENT_CODE_START
        # If you start Cid's timer and then leave, the timer can affect event tile, NPC and objective triggering
        # Write some LongMapEvents to turn off the Cid timer when exiting to the world map.
        HORIZ = 0
        VERT = 128

        # LONG EVENT #1: play the lore sound effect on some horizontal tiles on the Blackjack
        src = [
            field.BranchIfEventBitSet(0x1b5, "SetBit"),
            field.ResetTimer(0),
            field.SetEventBit(0x1b5),
            "SetBit",
            field.Return(),
        ]
        space = Write(Bank.CC, src, 'Reset Cid event timer')

        map_id = 0x18c  # Cid's Island, Outside

        new_event_data = [(16, 1, 14, VERT), (15, 1, 14, VERT),  # (x, y, length, direction)
                          (0, 1, 14, VERT), (1, 1, 14, VERT),    # Include 2 layers to make sure it doesn't get skipped
                          (0, 1, 3, HORIZ), (0, 2, 3, HORIZ),
                          (7, 0, 2, HORIZ), (7, 1, 2, HORIZ),
                          (12, 1, 3, HORIZ), (12, 2, 3, HORIZ)]
        for i in range(len(new_event_data)):
            new_le = LongMapEvent()
            new_le.x = new_event_data[i][0]
            new_le.y = new_event_data[i][1]
            new_le.size = new_event_data[i][2]
            new_le.direction = new_event_data[i][3]
            new_le.event_address = space.start_address - EVENT_CODE_START
            self.add_long_event(map_id, new_le)

    def _disable_saves(self):
        # Ironmog mode -- disable saves
        space = Reserve(0x32ead, 0x32eae, asm.NOP())
        space.add_label("DISABLE SAVE", 0x32ebf)
        space.write(
            asm.BRA("DISABLE SAVE") # replace the vanilla BPL $2EBF to always branch)
        )

    def mod(self, characters):
        self.npcs.mod(characters)
        self.chests.mod()
        self.world_map.mod()

        self._fix_imperial_camp_boxes()
        self._fix_Cid_timer_glitch()
        if self.args.no_saves:
            self._disable_saves()

    def write(self):
        self.npcs.write()
        self.chests.write()
        self.events.write()
        self.long_events.write()
        self.exits.write()
        self.world_map_event_modifications.write()

        for map_index, cur_map in enumerate(self.maps):
            self.properties[map_index].write()

            entrance_event_start = self.ENTRANCE_EVENTS_START_ADDR + cur_map["id"] * self.rom.LONG_PTR_SIZE
            entrance_event_bytes = [0x00] * self.rom.LONG_PTR_SIZE
            entrance_event_bytes[0] = cur_map["entrance_event_address"] & 0xff
            entrance_event_bytes[1] = (cur_map["entrance_event_address"] & 0xff00) >> 8
            entrance_event_bytes[2] = (cur_map["entrance_event_address"] & 0xff0000) >> 16
            self.rom.set_bytes(entrance_event_start, entrance_event_bytes)

            events_ptr_start = self.EVENT_PTR_START + cur_map["id"] * self.rom.SHORT_PTR_SIZE
            events_ptr_bytes = [0x00] * self.rom.SHORT_PTR_SIZE
            events_ptr_bytes[0] = cur_map["events_ptr"] & 0xff
            events_ptr_bytes[1] = (cur_map["events_ptr"] & 0xff00) >> 8
            self.rom.set_bytes(events_ptr_start, events_ptr_bytes)

            # LONG EVENTS
            long_events_ptr_start = self.LONG_EVENT_PTR_START + cur_map["id"] * self.rom.SHORT_PTR_SIZE
            long_events_ptr_bytes = [0x00] * self.rom.SHORT_PTR_SIZE
            long_events_ptr_bytes[0] = cur_map["long_events_ptr"] & 0xff
            long_events_ptr_bytes[1] = (cur_map["long_events_ptr"] & 0xff00) >> 8
            self.rom.set_bytes(long_events_ptr_start, long_events_ptr_bytes)

            short_exits_ptr_start = self.SHORT_EXIT_PTR_START + cur_map["id"] * self.rom.SHORT_PTR_SIZE
            short_exits_bytes = [0x00] * self.rom.SHORT_PTR_SIZE
            short_exits_bytes[0] = cur_map["short_exits_ptr"] & 0xff
            short_exits_bytes[1] = (cur_map["short_exits_ptr"] & 0xff00) >> 8
            self.rom.set_bytes(short_exits_ptr_start, short_exits_bytes)

            long_exits_ptr_start = self.LONG_EXIT_PTR_START + cur_map["id"] * self.rom.SHORT_PTR_SIZE
            long_exits_bytes = [0x00] * self.rom.SHORT_PTR_SIZE
            long_exits_bytes[0] = cur_map["long_exits_ptr"] & 0xff
            long_exits_bytes[1] = (cur_map["long_exits_ptr"] & 0xff00) >> 8
            self.rom.set_bytes(long_exits_ptr_start, long_exits_bytes)

            npcs_ptr_address = self.NPCS_PTR_START + cur_map["id"] * self.rom.SHORT_PTR_SIZE
            npcs_ptr = [0x00] * self.rom.SHORT_PTR_SIZE
            npcs_ptr[0] = cur_map["npcs_ptr"] & 0xff
            npcs_ptr[1] = (cur_map["npcs_ptr"] & 0xff00) >> 8
            self.rom.set_bytes(npcs_ptr_address, npcs_ptr)
