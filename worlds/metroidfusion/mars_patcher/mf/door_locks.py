import logging
from collections import defaultdict
from enum import Enum
from typing import Annotated, TypedDict

from ..common_types import AreaId, AreaRoomPair, RoomId
from ..constants.game_data import area_doors_ptrs
from .auto_generated_types import MarsschemamfDoorlocksItem
from .constants.game_data import hatch_lock_event_count, hatch_lock_events
from .constants.minimap_tiles import (
    ALL_DOOR_TILE_IDS,
    ALL_DOOR_TILES,
    ColoredDoor,
    Edge,
)
from ..minimap import Minimap
from ..rom import Rom
from ..room_entry import BlockLayer, RoomEntry


class HatchLock(Enum):
    OPEN = 0
    LEVEL_0 = 1
    LEVEL_1 = 2
    LEVEL_2 = 3
    LEVEL_3 = 4
    LEVEL_4 = 5
    LOCKED = 6


HATCH_LOCK_ENUMS = {
    "Open": HatchLock.OPEN,
    "Level0": HatchLock.LEVEL_0,
    "Level1": HatchLock.LEVEL_1,
    "Level2": HatchLock.LEVEL_2,
    "Level3": HatchLock.LEVEL_3,
    "Level4": HatchLock.LEVEL_4,
    "Locked": HatchLock.LOCKED,
}

BG1_VALUES = {
    HatchLock.OPEN: 0x4,
    HatchLock.LEVEL_0: 0x6,
    HatchLock.LEVEL_1: 0x8,
    HatchLock.LEVEL_2: 0xA,
    HatchLock.LEVEL_3: 0xC,
    HatchLock.LEVEL_4: 0xE,
    HatchLock.LOCKED: 0x819A,
}

CLIP_VALUES = {
    HatchLock.OPEN: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    HatchLock.LEVEL_0: [0x30, 0x31, 0x32, 0x33, 0x34, 0x35],
    HatchLock.LEVEL_1: [0x36, 0x37, 0x38, 0x39, 0x3A, 0x3B],
    HatchLock.LEVEL_2: [0x40, 0x41, 0x42, 0x43, 0x44, 0x45],
    HatchLock.LEVEL_3: [0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B],
    HatchLock.LEVEL_4: [0x3C, 0x3D, 0x3E, 0x4C, 0x4D, 0x4E],
    HatchLock.LOCKED: [0x10, 0x10, 0x10, 0x10, 0x10, 0x10],
}

CLIP_TO_HATCH_LOCK: dict[int, HatchLock] = {}
for lock, vals in CLIP_VALUES.items():
    for val in vals:
        CLIP_TO_HATCH_LOCK[val] = lock


EXCLUDED_DOORS = {
    (0, 0xB4),  # Restricted lab escape
}

HatchSlot = Annotated[int, "0 <= value <= 5"]

MinimapLocation = tuple[int, int, RoomId]
"""`(X, Y, RoomId)`"""


class MinimapLockChanges(TypedDict, total=False):
    left: HatchLock
    right: HatchLock


# TODO:
# - Optimize by only loading rooms that contain doors to modify
# - Split into more than one function for readability
def set_door_locks(rom: Rom, data: list[MarsschemamfDoorlocksItem]) -> None:
    door_locks = parse_door_lock_data(data)

    # Go through all doors in game in order
    doors_ptrs = area_doors_ptrs(rom)
    loaded_rooms: dict[AreaRoomPair, RoomEntry] = {}

    # (AreaID, RoomID): (BG1, Clipdata)
    loaded_bg1_and_clip: dict[AreaRoomPair, tuple[BlockLayer, BlockLayer]] = {}

    # (AreaID, RoomID): (CappedSlot, CaplessSlot)
    orig_room_hatch_slots: dict[AreaRoomPair, tuple[HatchSlot, HatchSlot]] = {}
    new_room_hatch_slots: dict[AreaRoomPair, tuple[HatchSlot, HatchSlot]] = {}

    hatch_slot_changes: dict[AreaRoomPair, dict[HatchSlot, HatchSlot]] = {}

    def factory() -> dict:
        return defaultdict(dict)

    # AreaID: {(MinimapX, MinimapY, RoomID): {"left" | "right": HatchLock}}
    minimap_changes: dict[AreaId, dict[MinimapLocation, MinimapLockChanges]] = defaultdict(factory)

    for area in range(7):
        area_addr = rom.read_ptr(doors_ptrs + area * 4)
        for door in range(256):
            door_addr = area_addr + door * 0xC
            door_type = rom.read_8(door_addr)

            # Check if at end of list
            if door_type == 0:
                break

            # Skip doors that mage marks as deleted
            room = rom.read_8(door_addr + 1)
            if room == 0xFF:
                continue

            # Skip excluded doors and doors that aren't lockable hatches
            lock = door_locks.get((area, door))
            if (area, door) in EXCLUDED_DOORS or door_type & 0xF != 4:
                # Don't log the error if door is open and JSON says to change to open.
                if lock is not None and not (lock is HatchLock.OPEN and door_type & 0xF == 3):
                    logging.error(f"Area {area} door {door} cannot have its lock changed")
                continue

            # Load room's BG1 and clipdata if not already loaded
            area_room = (area, room)
            room_entry = loaded_rooms.get(area_room)
            if room_entry is None:
                room_entry = RoomEntry(rom, area, room)
                bg1 = room_entry.load_bg1()
                clip = room_entry.load_clip()
                loaded_rooms[area_room] = room_entry
                loaded_bg1_and_clip[area_room] = (bg1, clip)
                orig_room_hatch_slots[area_room] = (0, 5)
                new_room_hatch_slots[area_room] = (0, 5)
                hatch_slot_changes[area_room] = {}
            else:
                _tuple = loaded_bg1_and_clip.get(area_room)
                if _tuple is not None:
                    bg1, clip = _tuple

            # Check x exit distance to get facing direction
            x_exit = rom.read_8(door_addr + 7)
            facing_right = x_exit < 0x80
            dx = 1 if facing_right else -1

            # Get hatch position
            hatch_x = rom.read_8(door_addr + 2) + dx
            hatch_y = rom.read_8(door_addr + 4)

            # Get original hatch slot number
            capped_slot, capless_slot = orig_room_hatch_slots[area_room]
            clip_val = clip.get_block_value(hatch_x, hatch_y)
            orig_has_cap = clip_val != 0
            if orig_has_cap:
                # Has cap
                orig_hatch_slot = capped_slot
                capped_slot += 1
            else:
                # Capless
                orig_hatch_slot = capless_slot
                capless_slot -= 1
            orig_room_hatch_slots[area_room] = (capped_slot, capless_slot)

            # Get new hatch slot number
            capped_slot, capless_slot = new_room_hatch_slots[area_room]
            if lock == HatchLock.LOCKED:
                new_hatch_slot = orig_hatch_slot
                # Mark door as deleted
                rom.write_8(door_addr + 1, 0xFF)
            elif (lock is None and orig_has_cap) or (lock is not None and lock != HatchLock.OPEN):
                # Has cap
                new_hatch_slot = capped_slot
                capped_slot += 1
            else:
                # Capless
                new_hatch_slot = capless_slot
                capless_slot -= 1
            new_room_hatch_slots[area_room] = (capped_slot, capless_slot)

            if new_hatch_slot != orig_hatch_slot:
                hatch_slot_changes[area_room][orig_hatch_slot] = new_hatch_slot

            # Map tiles
            if lock is not None:
                screen_offset_x = (hatch_x - 2) // 15
                screen_offset_y = (hatch_y - 2) // 10

                minimap_x = room_entry.map_x + screen_offset_x
                minimap_y = room_entry.map_y + screen_offset_y

                minimap_areas = [area]
                if area == 0:
                    minimap_areas = [0, 9]  # Main deck seemingly has two maps?
                for minimap_area in minimap_areas:
                    map_tile = minimap_changes[minimap_area][minimap_x, minimap_y, room]
                    if facing_right:
                        map_tile["left"] = lock
                    else:
                        map_tile["right"] = lock

            # Overwrite BG1 and clipdata
            if lock is None:
                # Even if a hatch's lock hasn't changed, its slot may have changed
                lock = CLIP_TO_HATCH_LOCK.get(clip_val)
                if lock is None:
                    continue

            bg1_val = BG1_VALUES[lock]
            if facing_right:
                bg1_val += 1

            clip_val = CLIP_VALUES[lock][new_hatch_slot]

            for y in range(4):
                bg1.set_block_value(hatch_x, hatch_y + y, bg1_val)
                clip.set_block_value(hatch_x, hatch_y + y, clip_val)
                bg1_val += 0x10

    # Write BG1 and clipdata for each room
    for bg1, clip in loaded_bg1_and_clip.values():
        bg1.write()
        clip.write()

    fix_hatch_lock_events(rom, hatch_slot_changes)

    change_minimap_tiles(rom, minimap_changes)


def parse_door_lock_data(data: list[MarsschemamfDoorlocksItem]) -> dict[AreaRoomPair, HatchLock]:
    """Returns a dictionary of `(AreaID, RoomID): HatchLock` from the input data."""
    door_locks: dict[AreaRoomPair, HatchLock] = {}
    for entry in data:
        area_door = (entry["Area"], entry["Door"])
        lock = HATCH_LOCK_ENUMS[entry["LockType"]]
        door_locks[area_door] = lock
    return door_locks


def fix_hatch_lock_events(
    rom: Rom, hatch_slot_changes: dict[AreaRoomPair, dict[HatchSlot, HatchSlot]]
) -> None:
    hatch_locks_addr = hatch_lock_events(rom)
    count = hatch_lock_event_count(rom)
    for i in range(count):
        addr = hatch_locks_addr + i * 5
        area = rom.read_8(addr + 1)
        room = rom.read_8(addr + 2) - 1
        changes = hatch_slot_changes.get((area, room))
        # Some rooms no longer have doors in rando
        if changes is None:
            continue
        hatch_flags = rom.read_8(addr + 3)
        new_flags = 0
        remain = (1 << 6) - 1
        for prev_slot, new_slot in changes.items():
            if (1 << prev_slot) & hatch_flags != 0:
                new_flags |= 1 << new_slot
            remain &= ~(1 << new_slot)
        new_flags |= hatch_flags & remain
        rom.write_8(addr + 3, new_flags)


def change_minimap_tiles(
    rom: Rom, minimap_changes: dict[AreaId, dict[MinimapLocation, MinimapLockChanges]]
) -> None:
    MAP_EDGES: dict[HatchLock, Edge | ColoredDoor] = {
        HatchLock.OPEN: Edge.DOOR,
        HatchLock.LEVEL_0: Edge.DOOR,
        HatchLock.LEVEL_1: ColoredDoor.BLUE,
        HatchLock.LEVEL_2: ColoredDoor.GREEN,
        HatchLock.LEVEL_3: ColoredDoor.YELLOW,
        HatchLock.LEVEL_4: ColoredDoor.RED,
        HatchLock.LOCKED: Edge.DOOR,
        # HatchLock.LOCKED: Edge.WALL,
    }

    for area, area_map in minimap_changes.items():
        with Minimap(rom, area) as minimap:
            for (x, y, room), tile_changes in area_map.items():
                tile_id, palette, h_flip, v_flip = minimap.get_tile_value(x, y)

                tile_data = ALL_DOOR_TILES[tile_id]

                # Account for h_flip before changing edges
                left = tile_changes.get("left")
                right = tile_changes.get("right")
                if h_flip:
                    left, right = right, left

                # Replace edges
                edges = tile_data.edges
                if left is not None:
                    edges = edges._replace(left=MAP_EDGES[left])
                if right is not None:
                    edges = edges._replace(right=MAP_EDGES[right])
                og_new_tile_data = tile_data._replace(edges=edges)
                new_tile_data = og_new_tile_data

                def tile_exists() -> bool:
                    return new_tile_data in ALL_DOOR_TILE_IDS

                if new_tile_data.content.can_h_flip and not tile_exists():
                    # Try flipping horizontally
                    new_tile_data = og_new_tile_data.h_flip()
                    if tile_exists():
                        h_flip = not h_flip

                if new_tile_data.content.can_v_flip and not tile_exists():
                    # Try flipping vertically
                    new_tile_data = og_new_tile_data.v_flip()
                    if tile_exists():
                        v_flip = not v_flip

                if (
                    new_tile_data.content.can_h_flip
                    and new_tile_data.content.can_v_flip
                    and not tile_exists()
                ):
                    # Try flipping it both ways
                    new_tile_data = og_new_tile_data.v_flip()
                    new_tile_data = new_tile_data.h_flip()
                    if tile_exists():
                        v_flip = not v_flip
                        h_flip = not h_flip

                if not tile_exists():
                    logging.debug(
                        "Could not edit map tile door icons for "
                        f"area {area} room {room:X}. ({x:X}, {y:X})."
                    )
                    logging.debug(f"  Desired tile: {og_new_tile_data.as_str}")
                    logging.debug("  Falling back to unlocked doors.")

                    # Try replacing with open doors
                    if (left is not None) and tile_data.edges.left.is_door:
                        edges = edges._replace(left=Edge.DOOR)
                    if (right is not None) and tile_data.edges.right.is_door:
                        edges = edges._replace(right=Edge.DOOR)
                    new_tile_data = og_new_tile_data._replace(edges=edges)

                    if tile_exists():
                        logging.debug("  Still no luck. Using vanilla tile.")

                    logging.debug("")

                if tile_exists():
                    minimap.set_tile_value(
                        x,
                        y,
                        ALL_DOOR_TILE_IDS[new_tile_data],
                        palette,
                        h_flip,
                        v_flip,
                    )
