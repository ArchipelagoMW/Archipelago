# rom.py
#
# Copyright (C) 2025 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

import bsdiff4
from collections import Counter
import os
import pkgutil
from typing import Any, Dict, TYPE_CHECKING
from settings import get_settings
from worlds.Files import APAutoPatchInterface
import zipfile

from worlds.pokemon_platinum.options import GameOptions

from .data.charmap import charmap
from .data.locations import locations, LocationTable
from .data.items import items

if TYPE_CHECKING:
    from . import PokemonPlatinumWorld

PLATINUM_1_0_US_HASH = "d66ad7a2a0068b5d46e0781ca4953ae9"
PLATINUM_1_1_US_HASH = "ab828b0d13f09469a71460a34d0de51b"

class PokemonPlatinumPatch(APAutoPatchInterface):
    game = "Pokemon Platinum"
    patch_file_ending = ".applatinum"
    hashes: list[str | bytes] = []
    source_data: bytes
    files: Dict[str, bytes]
    result_file_ending = ".nds"

    @staticmethod
    def get_source_data() -> bytes:
        with open(get_settings().pokemon_platinum_settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
        return base_rom_bytes

    @staticmethod
    def get_source_data_with_cache() -> bytes:
        if not hasattr(PokemonPlatinumPatch, "source_data"):
            PokemonPlatinumPatch.source_data = PokemonPlatinumPatch.get_source_data()
        return PokemonPlatinumPatch.source_data

    def patch(self, target: str) -> None:
        self.read()
        data = PokemonPlatinumPatch.get_source_data_with_cache()
        rom_version = data[0x01E]
        if rom_version == 0:
            patch_name = "base_patch_us_rev0.bsdiff4"
        else:
            patch_name = "base_patch_us_rev1.bsdiff4"
        data = bytearray(bsdiff4.patch(data, self.get_file(patch_name)))

        ap_bin_start = data.find(b'AP BIN FILLER ' * 5)
        ap_bin_end = data.find(b'\0', ap_bin_start)
        ap_bin_len = ap_bin_end - ap_bin_start + 1
        print(f"s: {ap_bin_start}, e: {ap_bin_end}, l: {ap_bin_len}")

        ap_bin = self.get_file("ap.bin")
        if len(ap_bin) > ap_bin_len:
            raise IndexError(f"ap.bin length is too long to fit in ROM. ap.bin: {len(ap_bin)}, capacity: {ap_bin_len}")
        data[ap_bin_start:ap_bin_start + len(ap_bin)] = ap_bin

        with open(target, 'wb') as f:
            f.write(data)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.files = {}

    def get_manifest(self) -> Dict[str, Any]:
        manifest = super().get_manifest()
        manifest["result_file_ending"] = self.result_file_ending
        manifest["allowed_hashes"] = self.hashes
        return manifest

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        for file in opened_zipfile.namelist():
            if file not in ["archipelago.json"]:
                self.files[file] = opened_zipfile.read(file)
        return manifest

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        for file in self.files:
            opened_zipfile.writestr(file, self.files[file],
                                    compress_type=zipfile.ZIP_STORED if file.endswith(".bsdiff4") else None)

    def get_file(self, file: str) -> bytes:
        if file not in self.files:
            self.read()
        print(self.files.keys())
        return self.files[file]

    def write_file(self, file_name: str, file: bytes) -> None:
        self.files[file_name] = file

def encode_name(name: str) -> bytes | None:
    ret = bytes()
    state = "normal"
    buf = ""
    for c in name:
        match state:
            case "normal":
                if c == '\\':
                    state = "escape"
                elif c == '{':
                    state = "bracket"
                    buf = ""
                elif c in charmap:
                    ret += charmap[c].to_bytes(length=2, byteorder='little')
                else:
                    return None
            case "escape":
                if "\\" + c in charmap:
                    ret += charmap["\\" + c].to_bytes(length=2, byteorder='little')
                    state = "normal"
                else:
                    return None
            case "bracket":
                if c == '}':
                    if buf in charmap:
                        ret += charmap[buf].to_bytes(length=2, byteorder='little')
                    else:
                        return None
                    state = "normal"
                else:
                    buf += c
        if len(ret) >= 15:
            return None
    return ret + b'\xFF' * (16 - len(ret))

def process_name(name: str, world: "PokemonPlatinumWorld") -> bytes:
    if name == "vanilla":
        return b'\xFF' * 16
    if name == "random":
        other_players = [world.multiworld.get_file_safe_player_name(id) for id in world.multiworld.player_name if id != world.player] # type: ignore
        world.random.shuffle(other_players)
        # if no player name matches, then return vanilla
        for name in other_players:
            ret = encode_name(name)
            if ret:
                return ret
        return b'\xFF' * 16
    if name == "player_name":
        ret = encode_name(world.multiworld.get_file_safe_player_name(world.player))
    else:
        ret = encode_name(name)
    if ret is not None:
        return ret
    else:
        return b'\xFF' * 16

def generate_output(world: "PokemonPlatinumWorld", output_directory: str, patch: PokemonPlatinumPatch) -> None:
    game_opts = world.options.game_options
    ap_bin = bytes()
    ap_bin += process_name(game_opts.default_player_name, world)
    ap_bin += process_name(game_opts.default_rival_name, world)
    match game_opts.default_gender:
        case "male":
            ap_bin += b'\x00'
        case "female":
            ap_bin += b'\x01'
        case "random":
            ap_bin += world.random.choice([b'\x00', b'\x01'])
        case "vanilla":
            ap_bin += b'\x02'
        case _:
            raise ValueError(f"invalid default gender: \"{game_opts.default_gender}\"")
    match game_opts.text_speed:
        case "fast":
            ap_bin += b'\x02'
        case "slow":
            ap_bin += b'\x00'
        case "mid":
            ap_bin += b'\x01'
        case _:
            raise ValueError(f"invalid text speed: \"{game_opts.text_speed}\"")
    match game_opts.sound:
        case "mono":
            ap_bin += b'\x01'
        case "stereo":
            ap_bin += b'\x00'
        case _:
            raise ValueError(f"invalid sound: \"{game_opts.sound}\"")
    match game_opts.battle_scene:
        case "off":
            ap_bin += b'\x01'
        case "on":
            ap_bin += b'\x00'
        case _:
            raise ValueError(f"invalid battle scene: \"{game_opts.battle_scene}\"")
    match game_opts.battle_style:
        case "set":
            ap_bin += b'\x01'
        case "shift":
            ap_bin += b'\x00'
        case _:
            raise ValueError(f"invalid battle style: \"{game_opts.battle_style}\"")
    match game_opts.button_mode:
        case "start=x":
            ap_bin += b'\x01'
        case "l=a":
            ap_bin += b'\x02'
        case "normal":
            ap_bin += b'\x00'
        case _:
            raise ValueError(f"invalid button mode: \"{game_opts.button_mode}\"")
    text_frame = game_opts.text_frame
    if isinstance(text_frame, int) and 1 <= text_frame and text_frame <= 20:
        ap_bin += (text_frame - 1).to_bytes(length=1, byteorder='little')
    elif text_frame == "random":
        ap_bin += world.random.randint(0, 19).to_bytes(length=1, byteorder='little')
    else:
        raise ValueError(f"invalid text frame: \"{text_frame}\"")

    if world.options.hm_badge_requirement.value == 1:
        hm_accum = 0
        hm_order = ["CUT", "FLY", "SURF", "STRENGTH", "DEFOG", "ROCK_SMASH", "WATERFALL", "ROCK_CLIMB"]
        for i, v in enumerate(hm_order):
            if v in world.options.remove_badge_requirements:
                hm_accum |= 1 << i
    else:
        hm_accum = 0xFF
    ap_bin += hm_accum.to_bytes(length=1, byteorder='little')

    def add_opt_byte(name: str):
        nonlocal ap_bin
        ap_bin += getattr(world.options, name).value.to_bytes(length=1, byteorder='little')

    add_opt_byte("exp_multiplier")
    add_opt_byte("parcel_coupons_route_203")
    add_opt_byte("regional_dex_goal")
    add_opt_byte("marsh_pass")
    add_opt_byte("remote_items")
    add_opt_byte("early_sunyshore")
    add_opt_byte("unown_option")
    add_opt_byte("pastoria_barriers")

    match game_opts.received_items_notification:
        case "nothing":
            ap_bin += b'\x00'
        case "message":
            ap_bin += b'\x03'
        case "jingle":
            ap_bin += b'\x04'
        case _:
            raise ValueError(f"invalid received items notification: \"{game_opts.received_items_notification}\"")
    add_opt_byte("blind_trainers")
    add_opt_byte("fps60")
    add_opt_byte("hm_cut_ins")
    add_opt_byte("buck_pos")
    ap_bin += (world.options.hb_speed.value - 1).to_bytes(length=1, byteorder='little')

    if len(ap_bin) % 2 == 1:
        ap_bin += b'\x00'

    tables: dict[LocationTable, bytearray] = {}

    def put_in_table(table: LocationTable, id: int, item_id: int):
        if table not in tables:
            tables[table] = bytearray()
        l = len(tables[table])
        if id >= l // 2:
            tables[table] = tables[table] + b'\x00\xF0' * (id - l // 2 + 1)
        tables[table][2*id:2*(id+1)] = item_id.to_bytes(length=2, byteorder='little')

    filled_locations = set()

    for location in world.multiworld.get_locations(world.player):
        if location.address is None or location.item is None or location.item.code is None:
            continue
        table = LocationTable(location.address >> 16)
        id = location.address & 0xFFFF
        filled_locations.add(location.name)
        if location.item.player == world.player:
            item_id = location.item.code
        else:
            item_id = 0xE000
        put_in_table(table, id, item_id)

    for location in locations.values():
        if location.label not in filled_locations:
            if isinstance(location.original_item, str):
                original_item = location.original_item
            else:
                original_item = world.random.choice(location.original_item)
            put_in_table(location.table, location.id, items[original_item].get_raw_id())

    ap_bin += len(tables).to_bytes(length=4, byteorder='little')
    for table in sorted(tables.keys()):
        data = tables[table]
        ap_bin += (len(data) // 2).to_bytes(length=4, byteorder='little')
        ap_bin += data

    precollected = world.multiworld.precollected_items[world.player]
    start_inventory: Counter[int] = Counter(map(lambda item : item.code, precollected)) # type: ignore
    entries = [code.to_bytes(length=2, byteorder='little') + count.to_bytes(length=2, byteorder='little') for code, count in start_inventory.items()]
    ap_bin += len(entries).to_bytes(length=4, byteorder='little')
    ap_bin += b''.join(entries)

    patch.write_file("ap.bin", ap_bin)

    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))
