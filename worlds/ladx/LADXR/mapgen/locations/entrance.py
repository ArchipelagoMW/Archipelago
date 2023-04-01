from ...locations.items import BOMB
from .base import LocationBase
from ...roomEditor import RoomEditor, Object, ObjectWarp
from ...entranceInfo import ENTRANCE_INFO
from ...assembler import ASM
from .entrance_info import INFO


class Entrance(LocationBase):
    def __init__(self, room, x, y, entrance_name):
        super().__init__(room, x, y)
        self.entrance_name = entrance_name
        self.entrance_info = ENTRANCE_INFO[entrance_name]
        self.source_warp = None
        self.target_warp_idx = None

        self.inside_logic = None

    def prepare(self, rom):
        info = self.entrance_info
        re = RoomEditor(rom, info.alt_room if info.alt_room is not None else info.room)
        self.source_warp = re.getWarps()[info.index if info.index not in (None, "all") else 0]
        re = RoomEditor(rom, self.source_warp.room)
        for idx, warp in enumerate(re.getWarps()):
            if warp.room == info.room or warp.room == info.alt_room:
                self.target_warp_idx = idx

    def update_room(self, rom, re: RoomEditor):
        re.objects.append(self.source_warp)

        target = RoomEditor(rom, self.source_warp.room)
        warp = target.getWarps()[self.target_warp_idx]
        warp.room = self.room.x | (self.room.y << 4)
        warp.target_x = self.x * 16 + 8
        warp.target_y = self.y * 16 + 18
        target.store(rom)

    def prepare_logic(self, configuration_options, world_setup, requirements_settings):
        if self.entrance_name in INFO and INFO[self.entrance_name].logic is not None:
            self.inside_logic = INFO[self.entrance_name].logic(configuration_options, world_setup, requirements_settings)

    def connect_logic(self, logic_location):
        if self.entrance_name not in INFO:
            raise RuntimeError(f"WARNING: Logic connection to entrance unmapped! {self.entrance_name}")
        if self.inside_logic:
            req = None
            if self.room.tiles[self.x + self.y * 10] == 0xBA:
                req = BOMB
            logic_location.connect(self.inside_logic, req)
        if INFO[self.entrance_name].exits:
            return [(name, logic(logic_location)) for name, logic in INFO[self.entrance_name].exits]
        return None

    def get_item_pool(self):
        if self.entrance_name not in INFO:
            return {}
        return INFO[self.entrance_name].items or {}


class DummyEntrance(LocationBase):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)

    def update_room(self, rom, re: RoomEditor):
        re.objects.append(ObjectWarp(0x01, 0x10, 0x2A3, 0x50, 0x7C))

    def connect_logic(self, logic_location):
        return

    def get_item_pool(self):
        return {}


class EggEntrance(LocationBase):
    def __init__(self, room, x, y):
        super().__init__(room, x, y)

    def update_room(self, rom, re: RoomEditor):
        # Setup the warps
        re.objects.insert(0, Object(5, 3, 0xE1))  # Hide an entrance tile under the tile where the egg will open.
        re.objects.append(ObjectWarp(0x01, 0x08, 0x270, 0x50, 0x7C))
        re.entities.append((0, 0, 0xDE))  # egg song event

        egg_inside = RoomEditor(rom, 0x270)
        egg_inside.getWarps()[0].room = self.room.x
        egg_inside.store(rom)

        # Fix the alt room layout
        alt = RoomEditor(rom, "Alt06")
        tiles = re.getTileArray()
        tiles[25] = 0xC1
        tiles[35] = 0xCB
        alt.buildObjectList(tiles, reduce_size=True)
        alt.store(rom)

        # Patch which room shows as Alt06
        rom.patch(0x00, 0x31F1, ASM("cp $06"), ASM(f"cp ${self.room.x:02x}"))
        rom.patch(0x00, 0x31F5, ASM("ld a, [$D806]"), ASM(f"ld a, [${0xD800 + self.room.x:04x}]"))
        rom.patch(0x20, 0x2DE6, ASM("cp $06"), ASM(f"cp ${self.room.x:02x}"))
        rom.patch(0x20, 0x2DEA, ASM("ld a, [$D806]"), ASM(f"ld a, [${0xD800 + self.room.x:04x}]"))
        rom.patch(0x19, 0x0D1A, ASM("ld hl, $D806"), ASM(f"ld hl, ${0xD800 + self.room.x:04x}"))

    def connect_logic(self, logic_location):
        return

    def get_item_pool(self):
        return {}
