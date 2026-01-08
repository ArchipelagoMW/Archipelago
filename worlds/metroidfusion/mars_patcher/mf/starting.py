from ..constants.game_data import area_doors_ptrs, spriteset_ptrs
from .auto_generated_types import (
    MarsschemamfStartingitems,
    MarsschemamfStartinglocation,
)
from .constants.game_data import starting_equipment
from .constants.items import BEAM_FLAGS, MISSILE_BOMB_FLAGS, SUIT_MISC_FLAGS
from .constants.reserved_space import ReservedConstantsMF
from ..rom import Rom
from ..room_entry import RoomEntry

# Keep in sync with base patch
STARTING_LOC_ADDR = ReservedConstantsMF.STARTING_LOCATION_ADDR


def set_starting_location(rom: Rom, data: MarsschemamfStartinglocation) -> None:
    area = data["Area"]
    room = data["Room"]
    # Don't do anything for area 0 room 0
    if area == 0 and room == 0:
        return
    # Find any door in the provided room
    door = find_door_in_room(rom, area, room)
    # Check if save pad in room
    pos = find_save_pad_position(rom, area, room)
    if pos is not None:
        x_pos, y_pos = pos
    else:
        # Convert block coordinates to actual position
        x_pos = data["BlockX"] * 64 + 31
        y_pos = data["BlockY"] * 64 + 63
    # Write to rom
    starting_location = rom.read_ptr(STARTING_LOC_ADDR)
    rom.write_8(starting_location, area)
    rom.write_8(starting_location + 1, room)
    rom.write_8(starting_location + 2, door)
    rom.write_16(starting_location + 4, x_pos)
    rom.write_16(starting_location + 6, y_pos)


def find_door_in_room(rom: Rom, area: int, room: int) -> int:
    door_addr = rom.read_ptr(area_doors_ptrs(rom) + area * 4)
    door = None
    for d in range(256):
        if rom.read_8(door_addr) == 0:
            break
        if rom.read_8(door_addr + 1) == room:
            door = d
            break
        door_addr += 0xC
    if door is None:
        raise ValueError(f"No door found for area {area} room {room:X}")
    return door


def find_save_pad_position(rom: Rom, area: int, room: int) -> tuple[int, int] | None:
    # Check if room's spriteset has save pad
    room_entry = RoomEntry(rom, area, room)
    spriteset = room_entry.default_spriteset()
    ss_addr = rom.read_ptr(spriteset_ptrs(rom) + spriteset * 4)
    ss_idx = None
    for i in range(15):
        sprite_id = rom.read_8(ss_addr)
        if sprite_id == 0:
            break
        if sprite_id == 0x1F:
            ss_idx = i
            break
        ss_addr += 2
    if ss_idx is None:
        return None
    # Find save pad in sprite layout list
    layout_addr = room_entry.default_sprite_layout_addr()
    for i in range(24):
        sp_y = rom.read_8(layout_addr)
        sp_x = rom.read_8(layout_addr + 1)
        prop = rom.read_8(layout_addr + 2)
        if sp_x == 0xFF and sp_y == 0xFF and prop == 0xFF:
            break
        if (prop & 0xF) - 1 == ss_idx:
            x_pos = sp_x * 64 + 32
            y_pos = sp_y * 64 + 9
            return x_pos, y_pos
        layout_addr += 3
    # No save pad found
    return None


def set_starting_items(rom: Rom, data: MarsschemamfStartingitems) -> None:
    def get_ability_flags(ability_flags: dict[str, int]) -> int:
        status = 0
        for ability, flag in ability_flags.items():
            if ability in abilities:
                status |= flag
        return status

    # Get health/ammo amounts
    energy = data.get("Energy", 99)
    missiles = data.get("Missiles", 10)
    power_bombs = data.get("PowerBombs", 10)
    # Get ability status flags
    abilities = data.get("Abilities", [])
    beam_status = get_ability_flags(BEAM_FLAGS)
    missile_bomb_status = get_ability_flags(MISSILE_BOMB_FLAGS)
    suit_misc_status = get_ability_flags(SUIT_MISC_FLAGS)
    # Get security level flags
    levels = data.get("SecurityLevels", [0])
    level_status = 0
    for level in levels:
        level_status |= 1 << level
    # Get downloaded map flags
    maps = data.get("DownloadedMaps", range(7))
    map_status = 0
    for map in maps:
        map_status |= 1 << map
    # Write to rom
    addr = starting_equipment(rom)
    rom.write_16(addr, energy)
    rom.write_16(addr + 2, energy)
    rom.write_16(addr + 4, missiles)
    rom.write_16(addr + 6, missiles)
    rom.write_8(addr + 8, power_bombs)
    rom.write_8(addr + 9, power_bombs)
    rom.write_8(addr + 0xA, beam_status)
    rom.write_8(addr + 0xB, missile_bomb_status)
    rom.write_8(addr + 0xC, suit_misc_status)
    rom.write_8(addr + 0xD, level_status)
    rom.write_8(addr + 0xE, map_status)
