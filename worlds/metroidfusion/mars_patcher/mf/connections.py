import os
import pkgutil
from collections.abc import Sequence

from ..constants import game_data as gd
from .auto_generated_types import (
    MarsschemamfElevatorconnections,
    MarsschemamfSectorshortcuts,
    Validelevatorbottoms,
    Validelevatortops,
)
from .constants.main_hub_numbers import (
    MAIN_HUB_CENTER_ROOM,
    MAIN_HUB_CENTER_SMALL_NUM_COORDS_1,
    MAIN_HUB_CENTER_SMALL_NUM_COORDS_2,
    MAIN_HUB_ELE_DOORS,
    MAIN_HUB_ELE_ROOM_LARGE_NUM_COORD,
    MAIN_HUB_ELE_ROOM_SMALL_NUM_COORDS,
    MAIN_HUB_ELE_ROOMS,
    MAIN_HUB_GFX_ADDR,
    MAIN_HUB_LARGE_NUM_BLOCKS,
    MAIN_HUB_SMALL_NUM_BLOCK,
    MAIN_HUB_TILEMAP_ADDR,
)
from .data import get_data_path
from ..minimap import Minimap
from ..rom import Game, Rom
from ..room_entry import BlockLayer, RoomEntry

# Area ID, Room ID, Is area connection
ELEVATOR_TOPS = {
    "OperationsDeckTop": (0, 0x1A, False),
    "MainHubToSector1": (0, 0x43, True),
    "MainHubToSector2": (0, 0x44, True),
    "MainHubToSector3": (0, 0x45, True),
    "MainHubToSector4": (0, 0x46, True),
    "MainHubToSector5": (0, 0x47, True),
    "MainHubToSector6": (0, 0x48, True),
    "MainHubTop": (0, 0x5E, False),
    "HabitationDeckTop": (0, 0xB2, False),
    "Sector1ToRestrictedLab": (1, 0x41, True),
}

ELEVATOR_BOTTOMS = {
    "OperationsDeckBottom": (0, 0x19, False),
    "MainHubBottom": (0, 0x32, False),
    "RestrictedLabToSector1": (0, 0x9A, True),
    "HabitationDeckBottom": (0, 0xB1, False),
    "Sector1ToMainHub": (1, 0x00, True),
    "Sector2ToMainHub": (2, 0x00, True),
    "Sector3ToMainHub": (3, 0x00, True),
    "Sector4ToMainHub": (4, 0x00, True),
    "Sector5ToMainHub": (5, 0x00, True),
    "Sector6ToMainHub": (6, 0x00, True),
}

# (Area ID, Dest area): Door ID
SHORTCUT_LEFT_DOORS = [0x6B, 0x7F, 0x59, 0x6C, 0x02, 0x51]
SHORTCUT_RIGHT_DOORS = [0x68, 0x82, 0x56, 0x6A, 0x53, 0x54]

SHORTCUT_LEFT_NUM_COORD = (6, 3)
SHORTCUT_RIGHT_NUM_COORD = (9, 3)
SHORTCUT_NUM_X_OFFSET = 3
SHORTCUT_NUM_BLOCKS = [0x101, 0x104, 0xE5, 0xE6, 0xE7, 0xE8]

DOOR_TYPE_AREA_CONN = 1
DOOR_TYPE_NO_HATCH = 2


class Connections:
    """Class for handling elevator shuffle and sector shortcut shuffle."""

    def __init__(self, rom: Rom):
        self.rom = rom
        self.area_doors_ptrs = gd.area_doors_ptrs(rom)
        self.area_conns_addr = gd.area_connections(rom)
        self.area_conns_count = gd.area_connections_count(rom)

    def set_elevator_connections(self, data: MarsschemamfElevatorconnections) -> None:
        # Repoint area connections data
        size = self.area_conns_count * 3
        # Reserve space for 8 more area connections
        new_size = size + 8 * 3
        ac_addr = self.rom.reserve_free_space(new_size)
        self.rom.copy_bytes(self.area_conns_addr, ac_addr, size)
        # TODO: Move constant
        self.rom.write_ptr(0x6945C, ac_addr)
        self.area_conns_addr = ac_addr

        # Connect tops to bottoms
        pairs_top = data["ElevatorTops"]
        self.connect_elevators(ELEVATOR_TOPS, ELEVATOR_BOTTOMS, pairs_top)
        # Connect bottoms to tops
        pairs_bottom = data["ElevatorBottoms"]
        self.connect_elevators(ELEVATOR_BOTTOMS, ELEVATOR_TOPS, pairs_bottom)
        if self.rom.game == Game.MF:
            # Update area number tiles in main hub rooms
            self.fix_main_hub_tiles()
            # Remove area numbers from Main Deck minimap
            self.remove_main_deck_minimap_area_nums()

    def set_shortcut_connections(self, data: MarsschemamfSectorshortcuts) -> None:
        for i, dst_area in enumerate(data["LeftAreas"]):
            self.connect_shortcuts(i + 1, dst_area, True)
        for i, dst_area in enumerate(data["RightAreas"]):
            self.connect_shortcuts(i + 1, dst_area, False)

    def connect_shortcuts(self, area: int, dst_area: int, left: bool) -> None:
        # Connect doors and update area connection
        if left:
            src_list = SHORTCUT_LEFT_DOORS
            dst_list = SHORTCUT_RIGHT_DOORS
            x, y = SHORTCUT_LEFT_NUM_COORD
            left_area, right_area = dst_area, area
        else:
            src_list = SHORTCUT_RIGHT_DOORS
            dst_list = SHORTCUT_LEFT_DOORS
            x, y = SHORTCUT_RIGHT_NUM_COORD
            left_area, right_area = area, dst_area
        door = src_list[area - 1]
        dst_door = dst_list[dst_area - 1]
        self.connect_doors(area, door, dst_area, dst_door)
        self.connect_areas(area, door, dst_area, True)

        # Update area numbers on BG1
        addr = self.rom.read_ptr(self.area_doors_ptrs + area * 4) + door * 0xC
        room = self.rom.read_8(addr + 1)
        room_entry = RoomEntry(self.rom, area, room)
        with room_entry.load_bg1() as bg1:
            block = SHORTCUT_NUM_BLOCKS[left_area - 1]
            bg1.set_block_value(x, y, block)
            bg1.set_block_value(x, y + 1, block + 0x10)
            block = SHORTCUT_NUM_BLOCKS[right_area - 1]
            x += SHORTCUT_NUM_X_OFFSET
            bg1.set_block_value(x, y, block)
            bg1.set_block_value(x, y + 1, block + 0x10)

    def connect_elevators(
        self,
        src_dict: dict,
        dst_dict: dict,
        pairs: dict[Validelevatortops, Validelevatorbottoms]
        | dict[Validelevatorbottoms, Validelevatortops],
    ) -> None:
        for src_name, dst_name in pairs.items():
            src_area, src_door, in_list = src_dict[src_name]
            dst_area, dst_door, _ = dst_dict[dst_name]
            # Modify door entry
            self.connect_doors(src_area, src_door, dst_area, dst_door)
            # Modify area connection
            self.connect_areas(src_area, src_door, dst_area, in_list)

    def connect_doors(self, src_area: int, src_door: int, dst_area: int, dst_door: int) -> None:
        addr = self.rom.read_ptr(self.area_doors_ptrs + src_area * 4) + src_door * 0xC
        # Fix door type
        props = self.rom.read_8(addr)
        door_type = DOOR_TYPE_AREA_CONN if src_area != dst_area else DOOR_TYPE_NO_HATCH
        self.rom.write_8(addr, props & 0xF0 | door_type)
        # Set destination door
        self.rom.write_8(addr + 6, dst_door)

    def connect_areas(self, src_area: int, src_door: int, dst_area: int, in_list: bool) -> None:
        rom = self.rom
        same_area = src_area == dst_area
        if in_list:
            # Find existing area connection
            for i in range(self.area_conns_count):
                addr = self.area_conns_addr + i * 3
                if rom.read_8(addr) == src_area and rom.read_8(addr + 1) == src_door:
                    if same_area:
                        # Make entry blank
                        rom.write_8(addr, 0)
                        rom.write_8(addr + 1, 0)
                        rom.write_8(addr + 2, 0)
                    else:
                        rom.write_8(addr + 2, dst_area)
                    return
            raise ValueError(f"Area connection not found for Area {src_area} Door {src_door:02X}")
        elif not same_area:
            addr = self.area_conns_addr + self.area_conns_count * 3
            rom.write_8(addr, src_area)
            rom.write_8(addr + 1, src_door)
            rom.write_8(addr + 2, dst_area)
            self.area_conns_count += 1

    def fix_main_hub_tiles(self) -> None:
        # Get areas that the 6 elevators go to
        ele_areas = [0 for _ in MAIN_HUB_ELE_DOORS]
        for i in range(self.area_conns_count):
            addr = self.area_conns_addr + i * 3
            # Skip if not main deck
            if self.rom.read_8(addr) != 0:
                continue
            door = self.rom.read_8(addr + 1)
            for j, ele_door in enumerate(MAIN_HUB_ELE_DOORS):
                if door == ele_door:
                    ele_areas[j] = self.rom.read_8(addr + 2)
                    break

        # Write new graphics and tilemap
        path = os.path.join("data", "main_hub.gfx.lz")
        gfx = pkgutil.get_data(__name__, path)
        self.rom.write_bytes(MAIN_HUB_GFX_ADDR, gfx)
        path = os.path.join("data", "main_hub_tilemap.bin")
        tilemap = pkgutil.get_data(__name__, path)
        self.rom.write_bytes(MAIN_HUB_TILEMAP_ADDR + 2, tilemap)

        # Overwrite numbers on BG2
        # Central room
        room_entry = RoomEntry(self.rom, 0, MAIN_HUB_CENTER_ROOM)
        with room_entry.load_bg2() as bg2:
            self._write_main_hub_small_nums(bg2, MAIN_HUB_CENTER_SMALL_NUM_COORDS_1, ele_areas)
            self._write_main_hub_small_nums(bg2, MAIN_HUB_CENTER_SMALL_NUM_COORDS_2, ele_areas)
        # Elevator rooms
        large_x, large_y = MAIN_HUB_ELE_ROOM_LARGE_NUM_COORD
        for i, room in enumerate(MAIN_HUB_ELE_ROOMS):
            coords = MAIN_HUB_ELE_ROOM_SMALL_NUM_COORDS[i]
            room_entry = RoomEntry(self.rom, 0, room)
            with room_entry.load_bg2() as bg2:
                self._write_main_hub_small_nums(bg2, coords, ele_areas)
                block = MAIN_HUB_LARGE_NUM_BLOCKS[ele_areas[i]]
                bg2.set_block_value(large_x, large_y, block)
                bg2.set_block_value(large_x, large_y + 1, block + 0x10)

    def _write_main_hub_small_nums(
        self, bg2: BlockLayer, coords: Sequence[tuple[int, int] | None], ele_areas: list[int]
    ) -> None:
        for area, coord in enumerate(coords):
            if coord is None:
                continue
            block = MAIN_HUB_SMALL_NUM_BLOCK + ele_areas[area] * 0x10
            if area % 2 == 0:
                block += 2
            x, y = coord
            bg2.set_block_value(x, y, block)
            bg2.set_block_value(x + 1, y, block + 1)

    def remove_main_deck_minimap_area_nums(self) -> None:
        with Minimap(self.rom, 0) as minimap:
            minimap.set_tile_value(0x2, 0x11, 0xA0, 0)  # 5
            minimap.set_tile_value(0x3, 0x10, 0xA0, 0)  # 3
            minimap.set_tile_value(0x4, 0x0F, 0xA0, 0)  # 1
            minimap.set_tile_value(0x8, 0x0F, 0xA0, 0)  # 2
            minimap.set_tile_value(0x9, 0x10, 0xA0, 0)  # 4
            minimap.set_tile_value(0xA, 0x11, 0xA0, 0)  # 6
