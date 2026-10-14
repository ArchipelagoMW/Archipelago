import os
import io
import re
import struct
import pkgutil
from typing import Dict, Optional
import Utils
import zipfile
import json
from copy import deepcopy

from .Locations import location_table
from .Items import item_table
from .Data import CHAR_TO_KH, ITEMHELP, MP_COST_LABELS, SPELL_LEVELS_BY_SPELL, SYSMSG, WORD
from worlds.Files import APPlayerContainer

class KH1Container(APPlayerContainer):
    game: str = 'Kingdom Hearts'
    patch_file_ending = ".zip"

    def __init__(self, patch_data: Dict[str, str | bytes] | io.BytesIO, base_path: str = "", output_directory: str = "",
        player: Optional[int] = None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + self.patch_file_ending)
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, text in self.patch_data.items():
            opened_zipfile.writestr(filename, text)
        super().write_contents(opened_zipfile)


def generate_json(world, output_directory):
    mod_name = f"AP-{world.multiworld.seed_name}-P{world.player}-{world.multiworld.get_file_safe_player_name(world.player)}"
    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__)
    
    item_location_map = get_item_location_map(world)
    location_spheres = get_location_spheres(world)
    progression_locations = get_progression_locations(world)
    settings = get_settings(world)
    keyblade_stats = world.get_keyblade_stats()

    files = {
        "item_location_map.json":     json.dumps(item_location_map),
        "location_spheres.json":      json.dumps(location_spheres),
        "progression_locations.json": json.dumps(progression_locations),
        "keyblade_stats.json":        json.dumps(keyblade_stats),
        "settings.json":              json.dumps(settings),
        "ap_costs.json":              json.dumps(world.get_ap_costs()),
        "mp_costs.json":              json.dumps(world.get_mp_costs()),
        "spell_effectiveness.json":   json.dumps(world.get_spell_effectiveness()),
        "items.json":                 json.dumps(get_items()),
        "locations.json":             json.dumps(get_locations()),
        "mod.yml":                    get_mod_yml(settings),
        "UK_Word.bin":                generate_word(settings),
        "UK_ItemHelp.bin":            generate_itemhelp(keyblade_stats, item_location_map),
        "UK_sysmsg.binl":             generate_sysmsg(world.get_mp_costs()),
        "icon.png":                   pkgutil.get_data(__name__, "icons/mod_icon.png"),
    }

    mod = KH1Container(files, mod_dir, output_directory, world.player,
            world.multiworld.get_file_safe_player_name(world.player))
    mod.write()

def get_item_location_map(world):
    location_item_map = {}
    for location in world.multiworld.get_filled_locations(world.player):
        if location.name != "Final Ansem":
            if world.player != location.item.player or (world.player == location.item.player and world.options.remote_items.current_key == "full" and {"Accessory", "Augment"}.isdisjoint(location_table[location.name].groups)):
                item_id = 2641230
            else:
                item_id = location.item.code
            location_data = location_table[location.name]
            location_id = location_data.code
            location_item_map[location_id] = item_id
    return location_item_map

def get_items():
    return {data.code: {"name": name} for name, data in item_table.items()}

def get_locations():
    return {data.code: {"name": name, "category": data.region, "type": ";".join(data.groups)} for name, data in location_table.items()}

def get_location_spheres(world):
    location_spheres = {}
    reachable = True
    for sphere_index, sphere in enumerate(world.multiworld.get_spheres()):
        if not sphere:
            reachable = False
            continue
        for location in sphere:
            if location.player != world.player or location.name == "Final Ansem":
                continue
            location_data = location_table[location.name]
            location_spheres[location_data.code] = sphere_index if reachable else -1
    return location_spheres

def get_progression_locations(world):
    progression_locations = []
    for location in world.multiworld.get_filled_locations(world.player):
        if location.address is None or location.name == "Final Ansem":
            continue
        if location.item.advancement:
            progression_locations.append(location_table[location.name].code)
    return sorted(progression_locations)

def get_mod_yml(settings):
    seed_str = settings["seed"].lstrip("W")
    hex_seed = f"{int(seed_str):X}" if seed_str.isdigit() else settings["seed"]
    return f"""
title: KH1 Randomizer Seed {hex_seed}
originalAuthor: Gicu
description: KH1 Randomizer Seed Information.  For use with gaithern/KH1-RANDOMIZER
assets:
- name: scripts/io_packages/json/item_location_map.json
  method: copy
  source:
    - name: item_location_map.json
- name: scripts/io_packages/json/location_spheres.json
  method: copy
  source:
    - name: location_spheres.json
- name: scripts/io_packages/json/progression_locations.json
  method: copy
  source:
    - name: progression_locations.json
- name: scripts/io_packages/json/keyblade_stats.json
  method: copy
  source:
    - name: keyblade_stats.json
- name: scripts/io_packages/json/settings.json
  method: copy
  source:
    - name: settings.json
- name: scripts/io_packages/json/ap_costs.json
  method: copy
  source:
    - name: ap_costs.json
- name: scripts/io_packages/json/mp_costs.json
  method: copy
  source:
    - name: mp_costs.json
- name: scripts/io_packages/json/spell_effectiveness.json
  method: copy
  source:
    - name: spell_effectiveness.json
- name: scripts/io_packages/json/items.json
  method: copy
  source:
    - name: items.json
- name: scripts/io_packages/json/locations.json
  method: copy
  source:
    - name: locations.json
- name: remastered/btltbl.bin/UK_Word.bin
  method: copy
  source:
    - name: UK_Word.bin
- name: remastered/btltbl.bin/UK_ItemHelp.bin
  method: copy
  source:
    - name: UK_ItemHelp.bin
- name: remastered/menu/uk/sysmsg.bin/UK_sysmsg.binl
  method: copy
  source:
    - name: UK_sysmsg.binl"""

def get_settings(world):
    settings = world.fill_slot_data()
    return settings

def generate_word(settings):
    seed_words = deepcopy(WORD)
    seed_words[seed_words.index("Puppy")] = f"{settings["puppy_value"]} Puppies"
    if settings.get("slides_bundle", True):
        seed_words[seed_words.index("Slide 1")] = "Slides"
    encoded_words = []
    for word in seed_words:
        encoded_word = bytearray()
        for token in re.findall(r"\{[^}]*\}|.", word):
            encoded_word.append(CHAR_TO_KH[token])
        encoded_words.append(bytes(encoded_word))
    return b"\x00".join(encoded_words)

def generate_itemhelp(keyblade_stats, item_location_map):
    seed_itemhelp = deepcopy(ITEMHELP)

    # Handle keyblade stats
    for i, stats in enumerate(keyblade_stats):
        seed_itemhelp[80 + i] = "".join(f"{key} {value} " for key, value in stats.items())
    
    # Handle augments
    item_code_to_name = {data.code: name for name, data in item_table.items()}
    for _, loc_data in location_table.items():
        if "Augment" in loc_data.groups:
            item_id = item_location_map.get(loc_data.code)
            if item_id is not None:
                item_name = item_code_to_name.get(item_id, "Unknown")
                itemhelp_idx = loc_data.code - 2659100 + 16
                seed_itemhelp[itemhelp_idx] = f"Augment: {item_name}"

    encoded_itemhelp = []
    for entry in seed_itemhelp:
        encoded_entry = bytearray()
        for token in re.findall(r"\{[^}]*\}|.", entry):
            encoded_entry.append(CHAR_TO_KH[token])
        encoded_itemhelp.append(bytes(encoded_entry))
    return b"\x00".join(encoded_itemhelp)

def generate_sysmsg(mp_costs):
    messages = list(SYSMSG)
    for levels in SPELL_LEVELS_BY_SPELL.values():
        desc = "{lf}".join(f"{level.name} - {MP_COST_LABELS[mp_costs[level.index]]}" for level in levels)
        for level in levels:
            messages[level.sysmsg_index] = desc

    encoded_messages = []
    for message in messages:
        encoded_message = bytearray()
        for token in re.findall(r"\{[^}]*\}|.", message):
            encoded_message.append(CHAR_TO_KH[token])
        encoded_messages.append(bytes(encoded_message))

    count = len(encoded_messages)
    tbl_start = 0x20
    tbl_size = (count + 1) * 2
    str_base = tbl_start + tbl_size

    offsets = []
    blob = bytearray()
    for encoded_message in encoded_messages:
        offsets.append(len(blob))
        blob += encoded_message + b"\x00"
    offsets.append(len(blob))  # sentinel entry marking the end of the blob
    if len(blob) % 2:
        blob += b"\x00"  # pad the blob to an even length, as the original files do

    header = bytearray(str_base)
    header[0x00:0x0C] = b"Message v361"
    struct.pack_into("<I", header, 0x0C, count)
    struct.pack_into("<I", header, 0x10, tbl_start)
    struct.pack_into("<I", header, 0x14, str_base)
    struct.pack_into("<I", header, 0x18, tbl_size)
    struct.pack_into("<I", header, 0x1C, len(blob))
    for i, offset in enumerate(offsets):
        struct.pack_into("<H", header, tbl_start + i * 2, offset)

    result = bytes(header) + blob
    remainder = len(result) % 16
    if remainder:
        result += b"\xCD" * (16 - remainder)
    return result
