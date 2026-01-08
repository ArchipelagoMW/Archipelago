from __future__ import annotations

import hashlib
import logging
import pkgutil
import struct
from typing import Literal, NotRequired, TypedDict

import bsdiff4

from . import lz10
from .backgrounds import fix_crateria_door_locks, patch_chozodia_spotlight, write_item_clipdata_and_gfx
from .constants import RC_COUNT, PIXEL_SIZE, Area, Event, ItemType
from .items import item_data_table
from .layout_patches import apply_layout_patches
from .local_rom import LocalRom, get_rom_address
from .sprites import builtin_sprite_pointers, sprite_imports, write_decompressed_item_sprites
from .symbols import get_symbol
from .text import NEWLINE, TERMINATOR_CHAR, Message, make_item_message


MD5_US = "ebbce58109988b6da61ebb06c7a432d5"
MD5_US_VC = "e23c14997c2ea4f11e5996908e577125"


class PatchJson(TypedDict):
    player_name: NotRequired[str]
    seed_name: NotRequired[str]
    config: SeedConfig
    locations: list[Location]
    start_inventory: NotRequired[dict[str, int | bool]]
    text: NotRequired[dict[str, dict[str, str]]]
    layout_patches: NotRequired[list[str] | Literal["all"]]


class SeedConfig(TypedDict):
    goal: NotRequired[Literal["vanilla", "bosses", "metroid_dna"]]
    difficulty: NotRequired[Literal["normal", "hard", "either"]]
    remove_gravity_heat_resistance: NotRequired[bool]
    power_bombs_without_bomb: NotRequired[bool]
    buff_power_bomb_drops: NotRequired[bool]
    separate_hijump_springball: NotRequired[bool]
    skip_chozodia_stealth: NotRequired[bool]
    chozodia_requires_mother_brain: NotRequired[bool]
    start_with_maps: NotRequired[bool]
    reveal_maps: NotRequired[bool]
    reveal_hidden_blocks: NotRequired[bool]
    skip_tourian_opening_cutscenes: NotRequired[bool]
    elevator_speed: NotRequired[int]
    metroid_dna_required: NotRequired[int]


class Location(TypedDict):
    id: int
    item_name: str
    sprite_name: NotRequired[str | None]
    message: NotRequired[str | None]


GOAL_MAPPING = {
    "vanilla": 0,
    "bosses": 1,
}


DIFFICULTY_MAPPING = {
    "normal": 0b01,
    "hard": 0b10,
    "either": 0b11,
}


RUINS_TEST_LOCATION_ID = 100


# TODO: Support overriding more text
TEXT_INDICES = {
    "Story": {
        "Intro": 0,
        "Escape 1": 1,
        "Escape 2": 2,
    }
}


def patch_rom(data: bytes, patch: PatchJson) -> bytes:
    rom = LocalRom(apply_basepatch(data))

    write_seed_config(rom, patch)

    write_decompressed_item_sprites(rom)
    place_items(rom, patch["locations"])
    write_start_inventory(rom, patch.get("start_inventory", {}))

    write_item_clipdata_and_gfx(rom)
    patch_chozodia_spotlight(rom)
    fix_crateria_door_locks(rom)
    apply_layout_patches(rom, patch.get("layout_patches", []))

    write_warp_to_start_cosmetics(rom)

    write_text(rom, patch.get("text", {}))

    return rom.to_bytes()


def apply_basepatch(rom: bytes) -> bytes:
    basepatch = pkgutil.get_data(__name__, "data/basepatch.bsdiff")

    hasher = hashlib.md5()
    hasher.update(rom)
    if hasher.hexdigest() == MD5_US:
        return bsdiff4.patch(rom, basepatch)

    logging.warning("You appear to be using a Virtual Console ROM. "
                    "This is not officially supported and may cause bugs.")
    entry_point = (0xEA00002E).to_bytes(4, 'little')  # b 0x80000C0
    return bsdiff4.patch(entry_point + rom[4:], basepatch)


def write_seed_config(rom: LocalRom, patch: PatchJson):
    config = patch["config"]
    goal = config.get("goal", "vanilla")
    seed_info = (
        patch.get("player_name", "").encode("utf-8")[:64],
        patch.get("seed_name", "").encode("utf-8")[:64],

        DIFFICULTY_MAPPING[config.get("difficulty", "either")],
        config.get("remove_gravity_heat_resistance", False),
        config.get("power_bombs_without_bomb", False),
        config.get("buff_power_bomb_drops", False),
        config.get("separate_hijump_springball", False),
        config.get("skip_chozodia_stealth", False),
        config.get("start_with_maps", False),
        config.get("reveal_maps", False),
        config.get("reveal_hidden_blocks", False),
        config.get("skip_tourian_opening_cutscenes", False),
        2 * PIXEL_SIZE * config.get("elevator_speed", 1),

        config.get("metroid_dna_required", 5) if goal == "metroid_dna" else 0,
    )
    rom.write(get_rom_address("sRandoSeed"), struct.pack("<64s64s12B", *seed_info))

    if goal != "vanilla":
        if goal == "bosses":
            event = Event.MOTHER_BRAIN_KILLED
        elif goal == "metroid_dna":
            event = Event.METROID_DNA_ACQUIRED
            write_metroid_dna_status_screen_patch(rom)
        else:
            raise ValueError(f"Invalid goal: {goal}")

        rom.write(
            get_rom_address("sHatchLockEventsChozodia", 8 * 15 + 1),  # sHatchLockEventsChozodia[15].event
            struct.pack("<B", event)
        )
        rom.write(get_rom_address("sNumberOfHatchLockEventsPerArea", 2 * Area.CHOZODIA), struct.pack("<H", 16))

    if config.get("chozodia_requires_mother_brain", False):
        rom.write(get_rom_address("sNumberOfHatchLockEventsPerArea", 2 * Area.CRATERIA), struct.pack("<H", 4))

    if config.get("reveal_maps"):
        rom.write(get_rom_address("sMinimapTilesPal"), pkgutil.get_data(__name__, "data/pause_screen/revealed_map_tile.pal"))


def _make_tile_bytes(tile_id: int, palette: int, hflip=False, vflip=False):
    return (tile_id | hflip << 10 | vflip << 11 | palette << 12).to_bytes(2, "little")


def write_metroid_dna_status_screen_patch(rom: LocalRom):
    def get_frame_address(animation_index, frame_number) -> int:
        frame_data_ptr, = rom.read(get_rom_address("sPauseScreenMiscOam", 8 * animation_index), "<I")
        return get_rom_address(frame_data_ptr, 8 * frame_number)

    def shift_sprite(array_address, index, x_amount):
        sprite_address = array_address + 2 * (1 + 3 * index)
        attr1, = rom.read(sprite_address + 2, "<H")
        x = ((attr1 & 0x1FF) + x_amount) & 0x1FF
        attr1 = (attr1 & 0xFE00) | x
        rom.write(sprite_address + 2, struct.pack("<H", attr1))

    # Add DNA header
    frame_data = struct.pack("<I", get_symbol("sRandoOam_EnergyDNAHeader"))
    rom.write(get_frame_address(23, 0), frame_data)

    # Shift bomb category pointer graphic
    for i, frame_count in enumerate([1, 2, 2, 3, 2, 3, 4, 5, 2]):
        oam_ptr, = rom.read(get_frame_address(33, i), "<I")
        oam_addr = get_rom_address(oam_ptr)
        for j in range(frame_count):
            shift_sprite(oam_addr, j, 1)
    oam_ptr, = rom.read(get_frame_address(33, 8), "<I")
    shift_sprite(get_rom_address(oam_ptr), 3, 1)

    # Add sprite tiles
    sprites_gfx = rom.decompress_lzss(get_rom_address("sTankIconsGfx"))
    edited_gfx = bytearray(sprites_gfx)
    edited_gfx[0x29C0:0x2A80] = bytes(64) + pkgutil.get_data(__name__, "data/pause_screen/dna_bar_sprite.gfx")
    edited_gfx = lz10.compress(edited_gfx)
    assert len(edited_gfx) <= 4 * (1786 + 11)
    rom.write(get_rom_address("sTankIconsGfx"), edited_gfx)

    # Add background tiles
    wireframe_bg_gfx = rom.decompress_lzss(get_rom_address("sMotifBehindWireframeSamusGfx"))
    edited_gfx = bytearray(wireframe_bg_gfx)
    edited_gfx[0x40:0xA0] = pkgutil.get_data(__name__, "data/pause_screen/dna_icon_bottom.gfx")
    edited_gfx[0x100:0x140] = pkgutil.get_data(__name__, "data/pause_screen/dna_bar_extension.gfx")
    edited_gfx = lz10.compress(edited_gfx)
    assert len(edited_gfx) <= 4 * (278 + 7)
    rom.write(get_rom_address("sMotifBehindWireframeSamusGfx"), edited_gfx)

    pause_screen_gfx = rom.decompress_lzss(get_rom_address("sPauseScreenHudGfx"))
    edited_gfx = bytearray(pause_screen_gfx)
    edited_gfx[0x4E60:0x4EC0] = pkgutil.get_data(__name__, "data/pause_screen/dna_icon_top.gfx")
    edited_gfx = lz10.compress(edited_gfx)
    assert len(edited_gfx) <= 4 * 1404
    rom.write(get_rom_address("sPauseScreenHudGfx"), edited_gfx)

    # Copy color to unused spot in background palette
    rom.write(get_rom_address("sPauseScreen_3fcef0", 2 * (6 * 16 + 15)), (0x797F).to_bytes(2, "little"))

    # Patch tile map
    grid_tile = _make_tile_bytes(736, 11)
    slash_tile = _make_tile_bytes(748, 11)

    def patch_tilemap(symbol: str, length: int):
        tilemap = rom.decompress_lzss(get_rom_address(symbol))
        edited_tilemap = bytearray(tilemap)
        edited_tilemap[0x58:0x5A] = _make_tile_bytes(757, 11)
        edited_tilemap[0x84:0xA4] = (
            4 * grid_tile + slash_tile + 4 * grid_tile +
            _make_tile_bytes(755, 11) + _make_tile_bytes(756, 11) +
            2 * grid_tile + slash_tile + 2 * grid_tile
        )
        edited_tilemap[0xC4:0xD0] = 6 * _make_tile_bytes(758, 11)
        for i, tile in enumerate(range(0xD4, 0xDA, 2)):
            edited_tilemap[tile:tile + 2] = _make_tile_bytes(2 + i, 11)
        for i, tile in enumerate(range(0xE0, 0xE4, 2)):
            edited_tilemap[tile:tile + 2] = _make_tile_bytes(8 + i, 11)
        edited_tilemap = lz10.compress(edited_tilemap)
        assert len(edited_tilemap) <= length
        rom.write(get_rom_address(symbol), edited_tilemap)

    patch_tilemap("sStatusScreenTilemap", 4 * 264)
    patch_tilemap("sStatusScreenBackgroundTilemap", 4 * 169)

    # Shift energy text position
    rom.write(get_rom_address("sStatusScreenGroupsData", 5 * 5 + 2), bytes([2, 5]))
    rom.write(get_rom_address("sStatusScreenGroupsData", 5 * 6 + 2), bytes([7, 10]))


def place_items(rom: LocalRom, locations: list[Location]):
    message_pointers: dict[tuple[str, str], int] = {}
    def get_or_insert_message(first_line: str, second_line: str = "") -> int:
        if (first_line, second_line) in message_pointers:
            return message_pointers[(first_line, second_line)]
        message_bytes = make_item_message(first_line, second_line).to_bytes()
        message_ptr = rom.append(message_bytes)
        message_pointers[(first_line, second_line)] = message_ptr
        return message_ptr

    file_pointers: dict[str, int] = {}
    def get_or_insert_file(name: str) -> int:
        if name in file_pointers:
            return file_pointers[name]
        file_bytes = pkgutil.get_data(__name__, f"data/item_sprites/{name}")
        file_ptr = rom.append(file_bytes)
        file_pointers[name] = file_ptr
        return file_ptr

    sprite_pointers: dict[str, int] = {**builtin_sprite_pointers}
    def get_or_insert_sprite(name: str) -> int:
        if name in sprite_pointers:
            return sprite_pointers[name]
        gfx, pal = sprite_imports[name]
        gfx_pointer = gfx if type(gfx) is int else get_or_insert_file(gfx)
        pal_pointer = pal if type(pal) is int else get_or_insert_file(pal)
        sprite = struct.pack("<II", gfx_pointer, pal_pointer)
        sprite_ptr = rom.append(sprite)
        sprite_pointers[name] = sprite_ptr
        return sprite_ptr

    placed_items: set[int] = set()
    for location in locations:
        location_id = location["id"]
        if location_id >= RC_COUNT or location_id < 0:
            raise ValueError(f"Invalid location ID: {location_id}")
        item_name = location["item"]
        sprite_name = location.get("sprite")
        message = location.get("message")

        item_data = item_data_table[item_name]
        sprite_pointer = get_or_insert_sprite(item_data.sprite if sprite_name is None else sprite_name)
        if message is None:
            if item_data.message is None:
                message_pointer = 0
                one_line = True
            else:
                message = item_data.message
        if message is not None:
            message_lines = message.splitlines()
            one_line = len(message_lines) <= 1
            message_pointer = get_or_insert_message(*message_lines)
        sound = 0x4A if location_id == RUINS_TEST_LOCATION_ID else item_data.sound
        rom.write(
            get_rom_address("sPlacedItems", 16 * location_id),
            struct.pack(
                "<BBHIIHBB",
                item_data.type, False, item_data.bits,
                sprite_pointer,
                message_pointer, sound, item_data.acquisition, one_line
            )
        )
        placed_items.add(location_id)

    for i in range(RC_COUNT):
        if i not in placed_items:
            item_data = item_data_table["Nothing"]
            rom.write(
                get_rom_address("sPlacedItems", 16 * i),
                struct.pack(
                    "<BBHIIHBB",
                    item_data.type, False, item_data.bits,
                    get_or_insert_sprite(item_data.sprite),
                    get_or_insert_message(item_data.message), item_data.sound, item_data.acquisition, True
                )
            )


def write_start_inventory(rom: LocalRom, start_inventory: dict[str, int | bool]):
    pickups = [0, 0, 0, 0]
    beams = misc = custom = 0
    for item_name, value in start_inventory.items():
        item_data = item_data_table[item_name]
        if value <= 0:
            continue
        if item_data.type == ItemType.BEAM:
            beams |= item_data.bits
        elif item_data.type == ItemType.MAJOR:
            misc |= item_data.bits
        elif item_data.type == ItemType.CUSTOM:
            custom |= item_data.bits
        elif item_data.type <= ItemType.POWER_BOMB_TANK:
            pickups[item_data.type - 1] = value
    rom.write(
        get_rom_address("sRandoStartingInventory"),
        struct.pack("<BxHBBBBB", *pickups, beams, misc, custom)
    )


def write_warp_to_start_cosmetics(rom: LocalRom):
    menu_names = rom.decompress_lzss(get_rom_address("sMenuNamesEnglishGfx"))
    edited_menu_names = lz10.compress(menu_names[:0x20] +
                                      pkgutil.get_data(__name__, f"data/pause_screen/warp.gfx") +
                                      menu_names[0x80:])
    assert len(edited_menu_names) <= len(menu_names)
    rom.write(get_rom_address("sMenuNamesEnglishGfx"), edited_menu_names)

    warp_to_start_text = [Message(line).center_align() for line in [
        "Warp to start?",
        "You will be returned to your starting",
        "location, and your progress will be",
        "reset to your last save."
    ]]
    line_1 = warp_to_start_text[0].append(NEWLINE) + warp_to_start_text[1].append(TERMINATOR_CHAR)
    line_2 = warp_to_start_text[2].append(NEWLINE) + warp_to_start_text[3].append(TERMINATOR_CHAR)
    line_1_ptr = rom.append(line_1.to_bytes())
    line_2_ptr = rom.append(line_2.to_bytes())
    rom.write(
        get_rom_address(f"sEnglishTextPointers_Message", 4 * 36),
        struct.pack("<II", line_1_ptr, line_2_ptr)
    )


def write_text(rom: LocalRom, text: dict[str, dict[str, str]]):
    for group, messages in text.items():
        for name, message in messages.items():
            array_index = TEXT_INDICES[group][name]
            encoded_message = Message(message).append(TERMINATOR_CHAR)
            text_address = rom.append(encoded_message.to_bytes())
            rom.write(
                get_rom_address(f"sEnglishTextPointers_{group}", 4 * array_index),
                struct.pack("<I", text_address)
            )
