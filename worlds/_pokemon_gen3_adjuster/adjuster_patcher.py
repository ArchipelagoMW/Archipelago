import math
import os
from typing import Callable
import zlib

from Utils import open_image_secure

# Try to import the Pokemon Emerald and Pokemon Firered/Leafgreen data
from .adjuster_constants import POKEMON_NAME_TO_ID, POKEMON_ID_TO_INTERNAL_ID, POKEMON_TYPES, POKEMON_MOVES, \
    POKEMON_ABILITIES, POKEMON_GENDER_RATIOS, REVERSE_POKEMON_GENDER_RATIOS, SPRITE_PIXEL_REFERENCE, \
    OBJECT_NEEDS_COMPRESSION, COMPLEX_SPRITES_LIST, OVERWORLD_PALETTE_INFO, OVERWORLD_SPRITE_OBJECT_INFO, \
    POKEMON_DATA_INFO, VALID_ICON_PALETTES, VALID_FOOTPRINT_PALETTE
try:
    from worlds.pokemon_emerald.adjuster_constants import EMERALD_FOLDER_OBJECT_INFOS, \
        EMERALD_INTERNAL_ID_TO_OBJECT_ADDRESS, EMERALD_OVERWORLD_SPRITE_ADDRESSES, EMERALD_POINTER_REFERENCES, \
        EMERALD_OVERWORLD_PALETTE_IDS, EMERALD_DATA_ADDRESS_INFOS, EMERALD_VALID_OVERWORLD_SPRITE_SIZES, \
        EMERALD_SPRITES_REQUIREMENTS, EMERALD_SPRITES_REQUIREMENTS_EXCEPTIONS
    emerald_support = True
except ModuleNotFoundError:
    from .adjuster_constants_emerald_fallback import EMERALD_FOLDER_OBJECT_INFOS, \
        EMERALD_INTERNAL_ID_TO_OBJECT_ADDRESS, EMERALD_OVERWORLD_SPRITE_ADDRESSES, EMERALD_POINTER_REFERENCES, \
        EMERALD_OVERWORLD_PALETTE_IDS, EMERALD_DATA_ADDRESS_INFOS, EMERALD_VALID_OVERWORLD_SPRITE_SIZES, \
        EMERALD_SPRITES_REQUIREMENTS, EMERALD_SPRITES_REQUIREMENTS_EXCEPTIONS
    emerald_support = False
try:
    from worlds.pokemon_frlg.adjuster_constants import FR_LG_FOLDER_OBJECT_INFOS, \
        FR_LG_INTERNAL_ID_TO_OBJECT_ADDRESS, FR_LG_OVERWORLD_SPRITE_ADDRESSES, FR_LG_POINTER_REFERENCES, \
        FR_LG_OVERWORLD_PALETTE_IDS, FR_LG_DATA_ADDRESS_INFOS, FR_LG_VALID_OVERWORLD_SPRITE_SIZES, \
        FR_LG_SPRITES_REQUIREMENTS, FR_LG_SPRITES_REQUIREMENTS_EXCEPTIONS
    frlg_support = True
except ModuleNotFoundError:
    from .adjuster_constants_frlg_fallback import FR_LG_FOLDER_OBJECT_INFOS, \
        FR_LG_INTERNAL_ID_TO_OBJECT_ADDRESS, FR_LG_OVERWORLD_SPRITE_ADDRESSES, FR_LG_POINTER_REFERENCES, \
        FR_LG_OVERWORLD_PALETTE_IDS, FR_LG_DATA_ADDRESS_INFOS, FR_LG_VALID_OVERWORLD_SPRITE_SIZES, \
        FR_LG_SPRITES_REQUIREMENTS, FR_LG_SPRITES_REQUIREMENTS_EXCEPTIONS
    frlg_support = False

sprite_pack_data: dict[str, int | list[dict[str, int | bytes]]] = {}
resource_address_to_insert_to = 0x00
current_rom: bytearray = None
rom_version = "Emerald"
rom_is_ap = False
data_addresses: dict[str, int] = None

##################
# Main Functions #
##################

pokemon_data_added: list[str] = []


def get_patch_from_sprite_pack(_sprite_pack_path: str, _rom_version: str):
    # Builds a patch from a given sprite pack to apply to the ROM
    global rom_version
    rom_version = _rom_version

    extended_data_dict.clear()
    extract_all_data()

    global sprite_pack_data, resource_address_to_insert_to
    # Build patch data, fetch end of file
    sprite_pack_data = {"length": 16777216, "data": []}
    if _rom_version == "Emerald":
        DATA_ADDRESSES_INFO["data_address_beginning"] = ((data_addresses["sEmpty6"] >> 12) + 1) << 12
    resource_address_to_insert_to = int(DATA_ADDRESSES_INFO["data_address_beginning"])

    # Handle existing Trainer & Pokemon folders
    pokemon_data_added.clear()
    for folder_object_info in [x for x in FOLDER_OBJECT_INFOS if "name" not in x]:
        add_sprite_pack_object_collection(_sprite_pack_path, folder_object_info)

    add_ability_fix(find_folder_object_info("pokemon"))
    add_all_extended_data()

    return sprite_pack_data


#######################
# Patch Data Building #
#######################


def add_sprite_pack_object_collection(
        _sprite_pack_path: str,
        _folder_object_info: dict[str, str | list[str] | dict[str, list[str]]]):
    # Adds data from all pokemon or all trainers to the patch if a folder including their name can be found
    folders: list[str] = _folder_object_info["folders"]
    for object_name in folders:
        _folder_object_info = find_folder_object_info(_folder_object_info["key"], object_name)
        is_pokemon = _folder_object_info["key"] == "pokemon" and "name" not in list(_folder_object_info.keys())
        is_unown_form = object_name.startswith("Unown ") and object_name != "Unown A"
        object_folder_path = os.path.join(_sprite_pack_path, object_name)
        if not os.path.exists(object_folder_path):
            continue
        found_sprites: dict[str, str] = {}
        for resource_name in os.listdir(object_folder_path):
            if resource_name == "data.txt" and is_pokemon and not is_unown_form:
                pokemon_data_added.append(object_name)
                add_pokemon_data(object_name, os.path.join(object_folder_path, resource_name))
            if not resource_name.endswith(".png"):
                continue
            # Only handle sprites which are awaited for the current object
            matching_sprite_name = next(filter(lambda f: resource_name.split(".")[0].split("-")[0] == f,
                                               _folder_object_info["sprites"]), None)
            if not matching_sprite_name:
                continue
            if is_unown_form and matching_sprite_name == 'footprint':
                # Unown shapes have no footprint data
                continue
            extra_sprite_data = resource_name[:-4].split("-")[1:] or ""
            sprite_path = os.path.join(object_folder_path, resource_name)
            if found_sprites.get(matching_sprite_name):
                continue
            found_sprites[matching_sprite_name] = resource_name
            add_sprite(_folder_object_info["key"], object_name, matching_sprite_name, extra_sprite_data, sprite_path)
        for palette, palette_extraction_priority_queue in _folder_object_info["palettes"].items():
            # Generate palettes if sprites exist
            found_sprite = False
            for resource_name in palette_extraction_priority_queue:
                if resource_name in found_sprites:
                    sprite_path = os.path.join(object_folder_path, str(found_sprites.get(resource_name)))
                    found_sprite = True
                    add_palette(_folder_object_info["key"], object_name, palette, resource_name, sprite_path)
                    break
            if not found_sprite:
                # Try to find raw sprites if they have not been recorded yet
                for resource_name in palette_extraction_priority_queue:
                    sprite_path = os.path.join(object_folder_path, resource_name + ".png")
                    if os.path.exists(sprite_path):
                        add_palette(_folder_object_info["key"], object_name, palette, resource_name, sprite_path)
                        break


def add_sprite(_key: str, _object_name: str, _sprite_name: str, _extra_data: list[str], _path: str):
    # Adds a sprite to the patch
    sprite_key = f"{_key}_{_sprite_name}"
    data_address, is_raw, data_object = get_address_from_address_collection(_object_name, sprite_key, _sprite_name)[0]

    if _key == "pokemon" and _sprite_name == "icon" and _extra_data:
        # Pokemon palette indexed icon: Switch the palette to use if it"s forced within the file"s name
        palette_index = int(_extra_data[0])
        icon_index_address, _, _ = get_address_from_address_collection(_object_name, sprite_key + "_index",
                                                                       _sprite_name)[0]
        add_data_to_patch({"address": icon_index_address, "length": 1, "data": palette_index.to_bytes(1, "little")})

    data_length = 0
    if is_complex_sprite(sprite_key):
        is_raw = True
        data_length = replace_complex_sprite(data_address, sprite_key, _object_name, _extra_data, _path)
        data_address = resource_address_to_insert_to

    if sprite_key != "players_battle_back":
        if is_raw:
            add_raw_resource(False, sprite_key, data_address, _path)
        else:
            add_resource(False, sprite_key, data_address, _path, data_object)
    else:
        # In case of Trainer battle back sprite, rerun this function to fill in the ball throwing animation table
        address_bytes = resource_address_to_insert_to.to_bytes(3, "little")
        add_data_to_patch({"address": data_address, "length": 3, "data": address_bytes})
        add_sprite(_key, _object_name, _sprite_name + "_throw", _extra_data, _path)
    if data_length:
        add_data_at_end(_data_length=data_length, _replace_address=False)


def add_palette(_key: str, _object_name: str, _palette_name: str, _sprite_name: str, _path: str):
    # Adds a palette to the patch
    palette_key = f"{_key}_{_palette_name}"
    if _object_name.startswith("Unown "):
        _object_name = "Unown A"
    data_extended = False
    if is_overworld_sprite(palette_key) and _sprite_name != "reflection":
        # If trainer overworld sprite, the palette needs to be added to the palette list
        # and it must be assigned to the trainer's overworld sprite
        # If player overworld sprite, the palette needs to be fixed as it may be incorrect
        new_id: int = 0x00
        if _palette_name == "palette_underwater":
            new_id = OVERWORLD_PALETTE_IDS["Underwater"]
        elif _key == "players":
            new_id = OVERWORLD_PALETTE_IDS[_object_name]
        if new_id == 0x00:
            data_extended = True
            new_id = extend_data("overworld_palette_table", resource_address_to_insert_to,
                                 extend_overworld_palette_table)
        sprite_key = f"{_key}_{_sprite_name}"
        reference_sprite_name: str = SPRITE_PIXEL_REFERENCE.get(_sprite_name, _sprite_name)
        sprite_data_address, _, _ = get_address_from_address_collection(_object_name, sprite_key,
                                                                        reference_sprite_name)[0]
        replace_complex_sprite_palette(sprite_data_address, palette_key, new_id, data_extended)

    data_address_infos = get_address_from_address_collection(_object_name, palette_key, _palette_name)
    data_addresses = [data_address for data_address, _, _ in data_address_infos]
    _, is_raw, _ = data_address_infos[0]
    data_objects = [data_object for _, _, data_object in data_address_infos]

    if is_raw:
        add_raw_resource(True, palette_key, data_addresses[len(data_addresses) - 1], _path)
    else:
        add_resource(True, palette_key, data_addresses, _path, data_objects, not data_extended)


def add_resource(_is_palette: str, _key: str, _data_addresses: int | list[int], _path: str,
                 _data_objects: bytearray | list[bytearray] = bytearray(), _replace_address=True):
    # Adds a resource (sprite or palette) to the patch and replaces its given pointers
    if _replace_address:
        if type(_data_addresses) is int:
            _data_addresses = [_data_addresses]
        if type(_data_objects) is bytearray:
            _data_objects = [_data_objects]
        for i in range(len(_data_addresses)):
            data_address = _data_addresses[i]
            data_object = _data_objects[i]
            address_bytes = resource_address_to_insert_to.to_bytes(3, "little")
            if data_object:
                data_object[data_address:data_address+3] = address_bytes
            else:
                add_data_to_patch({"address": data_address, "length": 3, "data": address_bytes})
    add_raw_resource(_is_palette, _key, resource_address_to_insert_to, _path)


def add_data_at_end(_address=0x00, _data=b"", _data_length=0, _replace_address=True):
    # Updates the end of the current available data address
    # Also appends data at its value if any is given
    global resource_address_to_insert_to
    if _replace_address:
        address_bytes = resource_address_to_insert_to.to_bytes(3, "little")
        add_data_to_patch({"address": _address, "length": 3, "data": address_bytes})
    if _data:
        add_data_to_patch({"address": resource_address_to_insert_to, "length": len(_data), "data": _data})
    resource_address_to_insert_to = resource_address_to_insert_to + (_data_length or len(_data))
    if resource_address_to_insert_to > DATA_ADDRESSES_INFO["data_address_end"]:
        # Out of bounds: Too much data to add
        raise Exception("Too much data to add to the ROM! Please remove some resources.")


def add_raw_resource(_is_palette: bool, _key: str, _data_address: int, _path: str):
    # Adds a raw resource to the patch at the given address
    needs_compression: bool = OBJECT_NEEDS_COMPRESSION.get(_key, False)
    if _is_palette:
        resource_data = handle_sprite_to_palette(_path, needs_compression)
    else:
        resource_data = handle_sprite_to_gba_sprite(_path, needs_compression)
    if _data_address == resource_address_to_insert_to:
        add_data_at_end(_data=resource_data, _replace_address=False)
    else:
        add_data_to_patch({"address": _data_address, "length": len(resource_data), "data": resource_data})


def add_pokemon_data(_pokemon_name: str, _data_path="",
                     _forced_data: dict[str, int | list[dict[str, str | int]]] = None):
    # Adds a given pokemon data and move pool to the patch
    if _forced_data is not None:
        new_pokemon_data = _forced_data
    else:
        with open(_data_path) as data_file:
            new_pokemon_data = destringify_pokemon_data(_pokemon_name, data_file.read())
    old_pokemon_data = get_pokemon_data(_pokemon_name)

    # Replace the pokemon data as a whole
    pokemon_data = merge_pokemon_data(old_pokemon_data, new_pokemon_data, True)
    pokemon_data_bytes = encode_pokemon_data(pokemon_data)
    data_address_stats, _, _ = get_address_from_address_collection(_pokemon_name, "pokemon_stats", "stats")[0]
    add_data_to_patch({"address": data_address_stats, "length": 28, "data": pokemon_data_bytes})

    if "move_pool" in new_pokemon_data:
        # Add a new move pool table and replace the pointer to it
        pokemon_move_pool_bytes = encode_move_pool(pokemon_data["move_pool"])
        global resource_address_to_insert_to
        # Move pool data MUST be isolated in its own 16 byte blocks, or reading it WILL cause garbage code execution
        resource_address_to_insert_to = (((resource_address_to_insert_to - 1) >> 4) + 1) << 4
        data_pointer_move_pool, _, _ = get_address_from_address_collection(_pokemon_name, "pokemon_move_pool",
                                                                           "move_pool")[0]
        add_data_at_end(data_pointer_move_pool, pokemon_move_pool_bytes,
                        (((len(pokemon_move_pool_bytes) - 1) >> 4) + 1) << 4)


def add_data_to_patch(_data: dict[str, int | bytes]):
    # Adds the given data to the patch
    if _data["address"] == 0x00:
        raise Exception("Bad address 0x00!")
    if _data["length"] == 0x00:
        raise Exception("Bad length 0!")
    if not type(_data["data"]) is bytes:
        raise Exception(f"Tried to add data of type {type(_data['data'])} to the patch.")
    # Order entries by ascending starting address
    index = 0
    data_begin = _data["address"]
    data_end = _data["address"] + _data["length"]
    for existing_data in sprite_pack_data["data"]:
        if data_begin >= existing_data["address"] + existing_data["length"]:
            index = index + 1
        elif data_end <= existing_data["address"]:
            break
        else:
            # Do not duplicate values
            return
    sprite_pack_data["data"].insert(index, _data)


def add_ability_fix(_folder_object_info: dict[str, str | list[str] | dict[str, list[str]]]):
    # Adds data from all pokemon or all trainers to the patch if a folder including their name can be found
    for object_name in filter(lambda o: o not in pokemon_data_added, _folder_object_info["folders"]):
        if (object_name.startswith("Unown ") and object_name != "Unown A")\
                or find_folder_object_info(_folder_object_info["key"], object_name) != _folder_object_info:
            continue
        add_pokemon_data(object_name, _forced_data={})


##################
# Data Extension #
##################

extended_data_dict: dict[str, dict[str, int | str | bytearray]] = {}
extended_data_dict_by_named_address: dict[str, dict[str, int | str | bytearray]] = {}


def extract_all_data():
    # Extracts all the data we want to prepare for extension
    extract_data("overworld_palette_table", OVERWORLD_PALETTE_INFO, "sObjectEventSpritePalettes")


def extract_data(_key: str, _info_object: dict[str, int | dict[str, int]], _named_address: str):
    # Extracts all the data in a given data table to prepare it for extension
    data_address: int = data_addresses[_named_address]
    data_id_info: int = _info_object.get("id", None)
    data_contents, data_last_id = extract_complex_sprite_data(data_address, _info_object["length"], data_id_info)
    extended_data: dict[str, int | str | bytearray] = {"data": data_contents, "length": _info_object["length"],
                                                       "named_address": _named_address}
    if data_id_info:
        extended_data["next_id"] = data_last_id + 1
    extended_data_dict[_key] = extended_data
    extended_data_dict_by_named_address[_named_address] = extended_data


def extend_data(_key: str, _contents: any, _line_fill_func: Callable[[any, int], bytes]):
    # Extends a data table that may be constrained by other data by extracting it
    # and replacing all pointers to it
    extended_data = extended_data_dict.get(_key, None)
    if not extended_data:
        raise Exception("Unknown data table to extend")

    data_last_id: int = extended_data.get("next_id", 0)
    new_line = _line_fill_func(_contents, data_last_id)
    if data_last_id:
        extended_data["next_id"] += 1
    extended_data["data"].extend(new_line)
    return data_last_id


def extend_overworld_palette_table(_contents: int, _new_id: int):
    # Builds a new line for the overworld palette table
    new_line = bytearray()
    new_line.extend(_contents.to_bytes(3, "little"))
    new_line.extend(b"\x08")
    new_line.extend(_new_id.to_bytes(2, "little"))
    new_line.extend(b"\x00\x00")
    return bytes(new_line)


def add_all_extended_data():
    # Adds all extended data tables to the patch
    for key, extended_data in extended_data_dict.items():
        # Replace all references to this data with its new address
        address_bytes = resource_address_to_insert_to.to_bytes(3, "little")
        for address in [data_addresses[ptr] + shift for ptr, shift in POINTER_REFERENCES[key]]:
            add_data_to_patch({"address": address, "length": 3, "data": address_bytes})

        # Add one line of padding to signify this is the end of the table
        data: bytearray = extended_data["data"]
        for i in range(extended_data["length"]):
            data.extend(b"\x00")
        add_data_at_end(_data=bytes(data), _replace_address=False)


###########################
# Complex Sprite Handling #
###########################


def replace_complex_sprite(_data_address: int, _sprite_key: str, _object_name: str, _extra_data: list[str], _path: str):
    # Replaces a complex sprite's sprite data and update its other fields if needed
    sprite_size_data: dict[str, int | str] = {}
    if _sprite_key == "players_battle_back_throw":
        # Trainer back sprites need further pointer seeking
        info_object_address = _data_address
        _data_address += 12
    elif is_overworld_sprite(_sprite_key):
        # Trainer overworld sprites need two objects to delve into
        info_object_address = int.from_bytes(bytes(current_rom[_data_address:_data_address + 3]), "little")
        _data_address = get_overworld_sprite_data(info_object_address, "sprites_ptr", True)
        if _extra_data:
            # If size given, extract it and check if it is supported
            sprite_size_data = handle_overworld_custom_size(_extra_data)

    sprite_requirements = get_sprite_requirements(_sprite_key, _object_name)
    if not sprite_requirements:
        raise Exception(f"Could not find sprite data for the sprite with key {_sprite_key} of object {_object_name}.")

    sprite_width: int = sprite_size_data.get("width") if sprite_size_data else sprite_requirements.get("width", 0)
    sprite_height: int = sprite_size_data.get("height") if sprite_size_data else sprite_requirements.get("height", 0)
    sprite_palette_size: int = sprite_requirements.get("palette_size", 16)
    bits_per_pixel = get_bits_per_pixel_from_palette_size(sprite_palette_size)
    if is_overworld_sprite(_sprite_key) and not sprite_size_data:
        sprite_width = get_overworld_sprite_data(info_object_address, "sprite_width")
        sprite_height = get_overworld_sprite_data(info_object_address, "sprite_height")
    sprite_size = round(sprite_width * sprite_height * bits_per_pixel / 8)

    # Build a new complex sprite table and insert it
    sprite_image = open_image_secure(_path)
    if sprite_height == 0:
        raise Exception(f"The complex sprite {_sprite_key} doesn't have a required height!")
    sprite_frames: int = round(sprite_image.height / sprite_height)
    temp_address = resource_address_to_insert_to
    output_data = bytearray(0)
    for _ in range(0, sprite_frames):
        output_data.extend(temp_address.to_bytes(3, "little"))
        output_data.extend(b"\x08")
        output_data.extend(sprite_size.to_bytes(2, "little"))
        output_data.extend(b"\x00\x00")
        temp_address += sprite_size
    if not is_overworld_sprite(_sprite_key):
        add_data_to_patch({"address": _data_address, "length": 3, "data": temp_address.to_bytes(3, "little")})
    add_data_to_patch({"address": temp_address, "length": len(output_data), "data": bytes(output_data)})

    if _sprite_key.endswith("battle_back_throw"):
        # Set the right animation for the battle back throwing animation
        anim_data_address, _, _ = get_address_from_address_collection(_object_name, _sprite_key, "battle_throw_anim")[0]
        if sprite_frames == 4:
            new_anim_data_address, _, _ = get_address_from_address_collection(_object_name, _sprite_key,
                                                                              "emerald_battle_throw_anim", True)[0]
        else:
            new_anim_data_address, _, _ = get_address_from_address_collection(_object_name, _sprite_key,
                                                                              "frlg_battle_throw_anim", True)[0]
        add_data_to_patch({"address": anim_data_address, "length": 3,
                           "data": bytes(current_rom[new_anim_data_address:new_anim_data_address+3])})
    if is_overworld_sprite(_sprite_key):
        for pointer in get_overworld_sprite_addresses(_object_name, _sprite_key[8:]):
            current_overworld_info_object = int.from_bytes(bytes(current_rom[pointer:pointer + 3]), "little")
            set_overworld_sprite_data(current_overworld_info_object, "sprites_ptr", temp_address)
            if sprite_size_data:
                # If custom size given, update overworld sprite data
                set_overworld_sprite_data(current_overworld_info_object, "sprite_length", sprite_size)
                set_overworld_sprite_data(current_overworld_info_object, "sprite_width", sprite_width)
                set_overworld_sprite_data(current_overworld_info_object, "sprite_height", sprite_height)
                set_overworld_sprite_data(current_overworld_info_object, "size_draw_ptr",
                                          data_addresses[sprite_size_data.get("data")])
                set_overworld_sprite_data(current_overworld_info_object, "distrib_ptr",
                                          data_addresses[sprite_size_data.get("distrib")])

    return len(output_data)


def replace_complex_sprite_palette(_data_address: int, _palette_key: str, _new_id: int, _palette_extended=False):
    # Replaces a complex sprite's palette ID, only for overworld sprites
    if is_overworld_sprite(_palette_key):
        info_object_address = int.from_bytes(bytes(current_rom[_data_address:_data_address + 3]), "little")
        set_overworld_sprite_data(info_object_address, "palette_id", _new_id)
        if _palette_extended:
            # If a palette has been added, change its palette slot so it doesn't overlap with other object palettes
            sprite_info = get_overworld_sprite_data(info_object_address, "sprite_info")
            sprite_info = (sprite_info >> 4 << 4) | 10  # Setting sprite to palette slot 10, expand if needed later
            set_overworld_sprite_data(info_object_address, "sprite_info", sprite_info)


def extract_complex_sprite(_overworld_struct_address: int, _sprite_key: str, _object_name: str,
                           _palette_sprite_name: str):
    # Extracts a complex sprite from the ROM as a Pillow sprite ready to be saved
    start_sprite_pointer = get_overworld_sprite_data(_overworld_struct_address, "sprites_ptr")
    sprite_width = get_overworld_sprite_data(_overworld_struct_address, "sprite_width")
    sprite_height = get_overworld_sprite_data(_overworld_struct_address, "sprite_height")
    sprites_pixel_data = []
    sprite_palette = None
    extra_sprite_name = ""

    sprite_requirements = get_sprite_requirements(_sprite_key, _object_name)
    for i in range(sprite_requirements["internal_frames"]):
        # Considers each frame as a sprite, then adds all of the frames" pixel data together
        start_sprite_address = int.from_bytes(bytes(current_rom[start_sprite_pointer:start_sprite_pointer + 3]),
                                              "little")
        sprite, current_extra_sprite_name = extract_sprite(start_sprite_address, _sprite_key, _object_name,
                                                           _palette_sprite_name, (sprite_width, sprite_height))
        sprites_pixel_data += sprite.getdata()
        if i == 0:
            sprite_palette = sprite.getpalette()
            extra_sprite_name = current_extra_sprite_name
        start_sprite_pointer += 8

    from PIL import Image
    final_image = Image.new("P", (sprite_width, sprite_height * sprite_requirements["internal_frames"]))
    final_image.putdata(sprites_pixel_data)
    final_image.putpalette(sprite_palette)
    return final_image, extra_sprite_name


def extract_complex_sprite_data(_data_address: int, _length: int, _data_id_info: dict[str, int] = None):
    result = bytearray()
    data_last_id = 0
    while True:
        # Extract all useful data lines from the object (last line is padding)
        data_line = current_rom[_data_address:_data_address+_length]
        if int.from_bytes(data_line, "little") in [0, int(math.pow(16, _length))-1]:
            break
        result.extend(data_line)
        _data_address += _length
        # Extract the resource ID on each line and keep the highest one if there's any
        if _data_id_info:
            line_id = int.from_bytes(data_line[_data_id_info["shift"]:_data_id_info["shift"]+_data_id_info["size"]],
                                     "little")
            if data_last_id < line_id:
                data_last_id = line_id
    return result, data_last_id


###################
# Data Extraction #
###################


def extract_palette_from_file(_path: str):
    # Extracts a palette from an existing sprite file
    sprite_image = open_image_secure(_path)
    sprite_palette = sprite_image.getpalette() or []
    sprite_palette_colors: list[str] = []
    for i in range(round(len(sprite_palette) / 3)):
        index = i * 3
        color = (int(sprite_palette[index]) << 16) + (int(sprite_palette[index+1]) << 8) + int(sprite_palette[index+2])
        sprite_palette_colors.append(hex(color)[2:].zfill(6))
    return sprite_palette_colors


def extract_sprites(_object_name: str, _output_path: str):
    # Extracts all sprites from a given object from the ROM into the given output folder
    def handle_sprite_extraction(_sprite_name: str):
        reference_sprite_name: str = SPRITE_PIXEL_REFERENCE.get(_sprite_name, _sprite_name)
        sprite_key = f"{folder_object_info['key']}_{reference_sprite_name}"
        data_address, is_raw, _ = get_address_from_address_collection(_object_name, sprite_key,
                                                                      reference_sprite_name)[0]
        if not is_raw:
            data_address = int.from_bytes(bytes(current_rom[data_address:data_address + 3]), "little")

        if is_complex_sprite(sprite_key):
            sprite_object, extra_sprite_name = extract_complex_sprite(data_address, sprite_key, _object_name,
                                                                      _sprite_name)
        else:
            sprite_object, extra_sprite_name = extract_sprite(data_address, sprite_key, _object_name, _sprite_name)
        full_path = os.path.join(_output_path, _sprite_name + extra_sprite_name + ".png")
        sprite_object.save(full_path)

    folder_object_info = find_folder_object_info(_name=_object_name)
    extracted_sprites: list[str] = []

    # Extract all sprites awaited for the given object
    sprite_list: list[str] = folder_object_info["sprites"]
    is_unown_form = _object_name.startswith("Unown ") and _object_name != "Unown A"
    if is_unown_form:
        # Unown shapes have no footprint data
        sprite_list = [s for s in sprite_list if s != 'footprint']
    for sprite_name in sprite_list:
        handle_sprite_extraction(sprite_name)
        extracted_sprites.append(sprite_name)

    # If any extra sprite is awaited for depicting palettes, extract them as well
    palette_lists: dict[str, list[str]] = folder_object_info["palettes"]
    palette_sprites = [palette_lists[palette_list] for palette_list in palette_lists]
    palette_sprites: filter[str] = filter(lambda s: s, [sprite if sprite not in extracted_sprites else None
                                                        for sprite in flatten_2d(palette_sprites)])
    for sprite_name in palette_sprites:
        handle_sprite_extraction(sprite_name)


def extract_sprite(_data_address: int, _sprite_key: str, _object_name: str, _palette_sprite_name: str,
                   _preset_size: tuple[int, int] = ()):
    # Extracts a given sprite from the ROM as a Pillow sprite ready to be saved
    extra_sprite_name = ""

    needs_compression: bool = OBJECT_NEEDS_COMPRESSION.get(_sprite_key, False)
    sprite_requirements = get_sprite_requirements(_sprite_key, _object_name)
    sprite_palette_size: int = sprite_requirements.get("palette_size", 16)
    bits_per_pixel = get_bits_per_pixel_from_palette_size(sprite_palette_size)
    # Retrieve the sprite's size
    if _preset_size:
        sprite_width = _preset_size[0]
        sprite_height = _preset_size[1]
    else:
        sprite_width: int = sprite_requirements["width"]
        sprite_height: int = sprite_requirements["height"] * sprite_requirements["internal_frames"]

    # Extract the sprite's pixel data
    sprite_size = round(sprite_width * sprite_height * bits_per_pixel / 8)
    end_address = _data_address + sprite_size + ((4 + math.ceil(sprite_size / 8) + 4) if needs_compression else 0)
    sprite_pixel_data = bytes(current_rom[_data_address:end_address])
    if needs_compression:
        sprite_pixel_data = truncate_lz_compressed_data(sprite_pixel_data, sprite_size)
        sprite_pixel_data = decompress_lz_data(sprite_pixel_data)
    sprite_pixel_data = decompress_sprite(sprite_pixel_data, bits_per_pixel)
    sprite_pixel_data = dechunk_sprite(sprite_pixel_data, sprite_width, sprite_height)
    if sprite_requirements.get("palette_per_frame", False):
        sprite_pixel_data = spread_palettes_to_sprite_frames(sprite_pixel_data, sprite_width, sprite_height,
                                                             sprite_requirements.get("palettes", 1))

    # Extract the sprite's palette(s)
    if _palette_sprite_name == "icon":
        # Retrieve the icon's palette index and add it at the end of the file's name
        icon_index_address, _, _ = get_address_from_address_collection(_object_name, _sprite_key + "_index",
                                                                       _object_name)[0]
        icon_index = int(current_rom[icon_index_address])
        sprite_palette: list[int] = VALID_ICON_PALETTES[icon_index]
        extra_sprite_name = f"-{int(icon_index)}"
    elif _palette_sprite_name == "footprint":
        sprite_palette: list[int] = VALID_FOOTPRINT_PALETTE
    else:
        sprite_palette = extract_palette(_object_name, _palette_sprite_name, _sprite_key[:7])

    # Assemble the sprite
    from PIL import Image
    extracted_image = Image.new("P", (sprite_width, sprite_height))
    extracted_image.putdata(sprite_pixel_data)
    extracted_image.putpalette(sprite_palette)
    return extracted_image, extra_sprite_name


def extract_palette(_object_name: str, _sprite_name: str, _key: str):
    # Extracts a palette as a list of RGB colors with values between 0 and 255
    folder_object_info = find_folder_object_info(_key, _object_name)
    palette_lists: dict[str, list[str]] = folder_object_info["palettes"]
    palette_name = next(filter(lambda palette: palette if _sprite_name in palette_lists[palette] else None,
                               palette_lists), None)
    palette_key = f"{_key}_{palette_name}"
    sprite_key = f"{_key}_{_sprite_name}"

    sprite_requirements = get_sprite_requirements(sprite_key, _object_name)
    palette_size: int = sprite_requirements.get("palette_size", 16) * sprite_requirements.get("palettes", 1) * 2
    data_address, is_raw, _ = get_address_from_address_collection(_object_name, palette_key, palette_name)[0]
    if not is_raw:
        data_address = int.from_bytes(bytes(current_rom[data_address:data_address + 3]), "little")

    needs_compression: bool = OBJECT_NEEDS_COMPRESSION.get(palette_key, False)
    end_address = data_address + palette_size + ((4 + math.ceil(palette_size / 8) + 4) if needs_compression else 0)
    palette_data = bytes(current_rom[data_address:end_address])
    if needs_compression:
        # If the data is compressed, decompress it first
        palette_data = truncate_lz_compressed_data(palette_data, palette_size)
        palette_data = decompress_lz_data(palette_data)

    palette: list[int] = []
    for i in range(round(palette_size / 2)):
        palette_five_bits_color = int.from_bytes(palette_data[i*2:i*2+2], "little")
        for _ in range(3):
            palette.append(five_to_eight_bits_palette(palette_five_bits_color % 32))
            palette_five_bits_color >>= 5
    return palette


###################
# Data Conversion #
###################


def handle_sprite_to_gba_sprite(_sprite_path: str, _needs_compression: bool):
    # Transforms indexed/grayscale PNG sprites into GBA sprites
    sprite_image = open_image_secure(_sprite_path)
    sprite_palette_size = round(len(sprite_image.getpalette()) / 3)
    bits_per_pixel = get_bits_per_pixel_from_palette_size(sprite_palette_size)

    # Chunk the data then compress it
    sprite_data = compress_sprite(chunk_sprite(bytes(sprite_image.getdata()), sprite_image.width, sprite_image.height),
                                  bits_per_pixel)
    if _needs_compression:
        # Compresses sprite if needed
        sprite_data = compress_lz_data(sprite_data)
    return bytes(sprite_data)


def handle_sprite_to_palette(_sprite_path: str, _needs_compression: bool):
    # Transforms indexed/grayscale PNG sprites into GBA palettes
    sprite_image = open_image_secure(_sprite_path)
    palette_data: list[int] = sprite_image.getpalette()
    palette_size = round(len(palette_data) / 3)

    # Transforms normal palette data into a GBA palette (8 bit colors to 5 bit colors)
    palette = [0 for _ in range(palette_size * 2)]
    for i in range(palette_size):
        palette_color_eight_bits = palette_data[i*3:(i+1)*3]
        palette_color_five_bits = 0
        for j in range(2, -1, -1):
            color_five_bits = eight_to_five_bits_palette(palette_color_eight_bits[j])
            palette_color_five_bits |= color_five_bits
            if j > 0:
                palette_color_five_bits <<= 5
        palette[i*2] = palette_color_five_bits & 0xFF
        palette[i*2+1] = palette_color_five_bits >> 8

    if _needs_compression:
        # Compresses palette if needed
        palette = compress_lz_data(bytes(palette))
    return bytes(palette)


#################
# Data Checking #
#################

sprite_pack_folder_list: list[str] = []


def validate_sprite_pack(_sprite_pack_path: str) -> tuple[str, bool]:
    # Validates an entire sprite pack to see if it can be applied to the given ROM
    errors = ""
    has_error = False

    def add_error(_error: str, _is_error=False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += "{}{}".format('\n' if errors else '', _error)

    sprite_pack_folder_list.clear()
    for folder_object_info in [x for x in FOLDER_OBJECT_INFOS if "name" not in list(x.keys())]:
        add_error(*validate_object_collection(_sprite_pack_path, folder_object_info))

    if not sprite_pack_folder_list:
        add_error("Error: The current sprite pack contains no resource to apply.", True)

    return errors, has_error


def validate_object_collection(_sprite_pack_path: str,
                               _folder_object_info: dict[str, str | list[str] | dict[str, list[str]]])\
                               -> tuple[str, bool]:
    # Validates all pokemon or all trainers if a folder including their name can be found
    errors = ""
    has_error = False

    def add_error(_error: str, _is_error=False, _processed=False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += "{}{}{}".format("\n" if errors else "",
                                      "" if _processed else "Error: " if _is_error else "Warning: ", _error)

    def add_to_folder_list(_folder):
        if _folder not in sprite_pack_folder_list:
            sprite_pack_folder_list.append(_folder)

    folders: list[str] = _folder_object_info["folders"]
    for object_name in folders:
        _folder_object_info = find_folder_object_info(_folder_object_info["key"], object_name)
        is_pokemon = _folder_object_info["key"] == "pokemon" and "name" not in list(_folder_object_info.keys())
        is_unown_form = object_name.startswith("Unown ") and object_name != "Unown A"
        object_folder_path = os.path.join(_sprite_pack_path, object_name)
        if not os.path.exists(object_folder_path):
            continue
        found_sprites: dict[str, str] = {}
        for resource_name in os.listdir(object_folder_path):
            if resource_name == "data.txt" and is_pokemon and not is_unown_form:
                # Text file that holds the Pokemon's modified data
                with open(os.path.join(object_folder_path, resource_name)) as pokemon_data_file:
                    add_error(*validate_pokemon_data_string(object_name, pokemon_data_file.read()), True)
                    add_to_folder_list(object_name)
                    continue
            if not resource_name.endswith(".png"):
                add_error(f"File {resource_name} in folder {object_name}: Not a recognized file and should be removed.")
                continue
            # Only handle sprites which are awaited for the current object
            matching_sprite_name = next(filter(lambda f: resource_name.split(".")[0].split("-")[0] == f,
                                               _folder_object_info["sprites"]), None)
            if not matching_sprite_name:
                # Allow sprites depicting an awaited palette
                if not next(filter(lambda palette: resource_name[:-4] in _folder_object_info["palettes"][palette],
                                   _folder_object_info["palettes"]), None):
                    add_error(f"File {resource_name} in folder {object_name}: "
                              + "Cannot be linked to a valid internal sprite or palette.")
                    continue
                matching_sprite_name = resource_name[:-4]
            if is_unown_form and matching_sprite_name == 'footprint':
                # Unown shapes have no footprint data
                add_error(f"File {resource_name} in folder {object_name}: "
                          + "Cannot be linked to a valid internal sprite or palette.")
                continue
            extra_sprite_data = resource_name[:-4].split("-")[1:] or ""
            sprite_path = os.path.join(object_folder_path, resource_name)
            if found_sprites.get(matching_sprite_name):
                add_error(f"File {resource_name} in folder {object_name}: "
                          + f"Duplicate internal sprite entry with sprite {object_name}.", True)
                continue
            found_sprites[matching_sprite_name] = resource_name
            add_to_folder_list(object_name)
            add_error(*validate_sprite(object_name, matching_sprite_name, extra_sprite_data, sprite_path), True)
    return errors, has_error


def validate_sprite(_object_name: str, _sprite_name: str, _extra_data: list[str], _path: str) -> tuple[str, bool]:
    # Validates a given sprite using metrics registered in the sprite requirements table
    errors = ""
    has_error = False

    def add_error(_error: str, _is_error=False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += "{}{}: {}".format("\n" if errors else "", "Error" if _is_error else "Warning", _error)

    folder_object_info = find_folder_object_info(_name=_object_name)
    sprite_key = f"{folder_object_info['key']}_{_sprite_name}"
    sprite_requirements = get_sprite_requirements(sprite_key, _object_name)

    try:
        sprite_image = open_image_secure(_path)
    except Exception:
        add_error(f"File {_sprite_name} in folder {_object_name}: The sprite is not a valid PNG file.", True)
        return errors, has_error

    # Palette checks
    if not sprite_image.palette:
        add_error(f"File {_sprite_name} in folder {_object_name}: The sprite is not an indexed PNG file.", True)
    elif sprite_image.mode != "P":
        add_error(f"File {_sprite_name} in folder {_object_name}: The sprite is not a valid indexed PNG file. "
                  + "Colors should be RGB, with no transparency.", True)
    else:
        sprite_palette_colors: list[int] = sprite_image.getpalette()
        palette_model: list[int] = sprite_requirements.get("palette", [])
        palette_set_size: int = sprite_requirements.get("palette_size", 0) * sprite_requirements.get("palettes", 1)
        palette_max_size: int = palette_set_size or 16 * sprite_requirements.get("palettes", 1)
        palette_colors = round(len(sprite_palette_colors) / 3)
        if palette_colors > palette_max_size or (palette_set_size > 0 and palette_colors != palette_set_size):
            add_error(f"File {_sprite_name} in folder {_object_name}: The sprite's palette has {palette_colors} colors "
                      + f"but should have {palette_max_size}{'' if palette_set_size > 0 else ' or less'}.", True)
        elif palette_model:
            matching_palette_model = True
            if _sprite_name == "icon":
                # Icons can have several palettes, one must be chosen
                if _extra_data:
                    # Icon palette ID is given in the icon's file name
                    palette_index = int(_extra_data[0])
                    if palette_index < 0 or palette_index > 2:
                        matching_palette_model = False
                        add_error(f"File {_sprite_name} in folder {_object_name}: Icons only have 3 palettes, "
                                  + f"but you tried using palette #{palette_index + 1}.", True)
                else:
                    # Icon palette ID must be retrieved from the ROM
                    icon_index_address, _, _ = get_address_from_address_collection(_object_name, sprite_key + "_index",
                                                                                   _object_name)[0]
                    palette_index = int.from_bytes(bytes(current_rom[icon_index_address]), "little")
                if matching_palette_model:
                    palette_model = palette_model[palette_index]
            if matching_palette_model and not is_palette_valid(sprite_palette_colors, palette_model):
                add_error(f"File {_sprite_name} in folder {_object_name}: The sprite's palette does not contain the "
                          + "required colors.", True)

    # Size checks
    sprite_valid_dimensions: list[dict[str, int]] = []
    if is_overworld_sprite(sprite_key) and _extra_data:
        # If a custom frame size is given for overworld sprites, check that it is valid
        allowed_sizes = [f"{size['width']}x{size['height']}" for size in VALID_OVERWORLD_SPRITE_SIZES]
        if not _extra_data[0] in allowed_sizes:
            add_error(f"File {_sprite_name} in folder {_object_name}: Invalid custom size {_extra_data[0]}. "
                      + f"The expected sizes are: {allowed_sizes}.", True)
            sprite_valid_dimensions.append({"width": 0, "height": 0})
        else:
            sizes = _extra_data[0].split("x")
            sprite_valid_dimensions.append({"width": int(sizes[0]),
                                            "height": int(sizes[1]) * sprite_requirements.get("frames", [1])[0]})
    else:
        valid_frames: list[int] = sprite_requirements.get("frames", [0])
        for valid_frame in valid_frames:
            sprite_valid_dimensions.append({"width": sprite_requirements.get("width", 0),
                                            "height": sprite_requirements.get("height", 0) * valid_frame})
    if sprite_valid_dimensions[0]["width"] > 0 and sprite_valid_dimensions[0]["height"] > 0:
        # Check that the sprite has the awaited size
        if not next(filter(lambda size: size["width"] == sprite_image.width and
                           size["height"] == sprite_image.height, sprite_valid_dimensions), None):
            allowed_sizes = [f"{size['width']}x{size['height']}" for size in sprite_valid_dimensions]
            current_size = f"{sprite_image.width}x{sprite_image.height}"
            add_error(f"File {_sprite_name} in folder {_object_name}: Invalid size {current_size}. "
                      + f"The expected size{' is' if len(allowed_sizes) == 1 else 's are'}: "
                      + f"{allowed_sizes[0] if len(allowed_sizes) == 1 else allowed_sizes}.", True)

    return errors, has_error


def is_palette_valid(_palette: list[int], _palette_model: list[int]):
    # Compares a given palette to its model and checks if it is valid or not
    for i in range(min(len(_palette), len(_palette_model))):
        if _palette_model[i] != -1 and _palette[i] != _palette_model[i]:
            return False
    return True


def validate_pokemon_data_string(_pokemon_name: str, _data: str | dict[str, int | str | list[tuple[str, int]]])\
                                 -> tuple[str, bool]:
    # Validates given Pokemon data, making sure that all fields are valid
    errors = ""
    has_error = False

    def add_error(_error: str, _is_error=False, _processed=False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += "{}{}{}".format("\n" if errors else "",
                                      "" if _processed else "Error: " if _is_error else "Warning: ", _error)

    if _pokemon_name.startswith("Unown "):
        _pokemon_name = "Unown A"

    # If the given data is a string, extracts its data first
    data_dict: dict[str, int | str | list[tuple[str, int]]]
    if type(_data) is str:
        try:
            data_dict = destringify_pokemon_data(_pokemon_name, _data, True)
        except Exception as e:
            if hasattr(e, "message"):
                return e.message, True
            else:
                return str(e), True
    else:
        data_dict = _data

    for field_name in data_dict:
        field_value = data_dict[field_name]
        if field_name in ["hp", "atk", "def", "spatk", "spdef", "spd"]:
            # Data must be a number between 1 and 255
            try:
                field_number_value = int(field_value)
                if field_number_value < 1 or field_number_value > 255:
                    add_error(f"{_pokemon_name}'s {field_name} value is invalid: '{field_value}'.", True)
            except Exception:
                add_error(f"{_pokemon_name}'s {field_name} value is invalid: '{field_value}'.", True)
        elif field_name in ["type1", "type2"]:
            # Data must be a number corresponding to a valid type
            try:
                if field_value.capitalize() not in POKEMON_TYPES:
                    field_number_value = int(field_value)
                    if field_number_value < 0 or field_number_value >= len(POKEMON_TYPES):
                        add_error(f"{_pokemon_name}'s {field_name} value is invalid: '{field_value}'.", True)
            except Exception:
                add_error(f"{_pokemon_name}'s {field_name} value is invalid: '{field_value}'.", True)
        elif field_name in ["ability1", "ability2"]:
            # Data must be a number corresponding to a valid ability
            try:
                if field_value.upper() not in POKEMON_ABILITIES:
                    field_number_value = int(field_value)
                    if field_number_value < 1 or field_number_value >= len(POKEMON_ABILITIES):
                        add_error(f"{_pokemon_name}'s {field_name} value is invalid: '{field_value}'.", True)
            except Exception:
                add_error(f"{_pokemon_name}'s {field_name} value is invalid: '{field_value}'.", True)
        elif field_name == "gender_ratio":
            # Data must be a number corresponding to a valid gender ratio
            try:
                if field_value not in list(POKEMON_GENDER_RATIOS.values()):
                    field_number_value = int(field_value)
                    if field_number_value not in list(POKEMON_GENDER_RATIOS.keys()):
                        add_error(f"{_pokemon_name}'s {field_name} value is invalid: '{field_value}'.", True)
            except Exception:
                add_error(f"{_pokemon_name}'s {field_name} value is invalid: '{field_value}'.", True)
        elif field_name == "dex":
            # Data must either be a 0 (allowed) or a 1 (forbidden)
            if field_value not in [0, 1, "0", "1", "True", "False"]:
                add_error(f"{_pokemon_name}'s forbid_flip value is invalid: '{field_value}'.", True)
        elif field_name == "move_pool":
            # Data must be a valid move pool table string
            if len(field_value) < 4:
                add_error(f"{_pokemon_name}'s move pool is empty.", True)
            else:
                add_error(*validate_move_pool_string(_pokemon_name, field_value.replace(", ", "\n")), True)
    return errors, has_error


def validate_move_pool_string(_pokemon_name: str, _move_pool_string: str) -> tuple[str, bool]:
    # Validates a move pool given as a string
    errors = ""
    has_error = False

    def add_error(_error, _is_error=False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += "{}{}: {}".format("\n" if errors else "", "Error" if _is_error else "Warning", _error)

    if not _move_pool_string:
        add_error(f"{_pokemon_name}'s move pool is empty.", True)

    move_lines = _move_pool_string.split("\n")
    for i in range(len(move_lines)):
        move_line = move_lines[i]
        if not move_line:
            continue
        move_info = move_line.split(":", 1)
        if len(move_info) != 2:
            add_error(f"{_pokemon_name}'s move #{i + 1} is malformed: '{move_info}'", True)
            continue
        move_name = move_info[0].strip()
        if not move_name.upper() in POKEMON_MOVES:
            add_error(f"{_pokemon_name}'s move #{i + 1} '{move_name}' is unknown.", True)
        move_level = move_info[1].strip()
        try:
            move_level_value = int(move_level)
            move_level_valid = 1 <= move_level_value <= 100
        except Exception:
            move_level_valid = False
        if not move_level_valid:
            add_error(f"{_pokemon_name}'s move #{i + 1}'s ({move_name}) level '{move_level}' is invalid.", True)
    return errors, has_error


##################
# LZ Compression #
##################


def truncate_lz_compressed_data(_data: bytes, _data_size: int):
    # Given data, truncates it so that the output contains only LZ-compressed data and nothing more
    data_length = len(_data)
    shift = 4
    while True:
        control_byte = int(_data[shift])
        shift += 1
        for i in range(8):
            if shift >= data_length:
                return _data
            is_compressed = control_byte & 0x80
            control_byte <<= 1
            if not is_compressed:
                _data_size -= 1
                shift += 1
            else:
                diff = 3 + (int(_data[shift]) >> 4)
                shift += 2
                _data_size -= diff
            if _data_size <= 0:
                return _data[:shift]


def compress_lz_data(_src: bytes, _min_distance=2):
    # Performs an LZ compression of the given data
    src_size = len(_src)

    worst_case_dest_size = 4 + src_size + math.ceil((src_size + 7) / 8)
    worst_case_dest_size = ((worst_case_dest_size >> 2) + 1) << 2

    dest = [0 for _ in range(worst_case_dest_size)]
    dest[0] = 0x10
    dest[1] = src_size & 0xFF
    dest[2] = (src_size >> 8) & 0xFF
    dest[3] = (src_size >> 16) & 0xFF

    src_pos = 0
    dest_pos = 4

    while True:
        flags_index = dest_pos
        dest_pos += 1

        for i in range(8):
            best_block_distance = 0
            best_block_size = 0
            block_distance = _min_distance

            # Smaller lookback for better speed and less compression
            while block_distance <= src_pos and block_distance <= 0x40:
                block_start = src_pos - block_distance
                block_size = 0

                while block_size < 18 and src_pos + block_size < src_size\
                        and _src[block_start + block_size] == _src[src_pos + block_size]:
                    block_size += 1

                if block_size > best_block_size:
                    best_block_distance = block_distance
                    best_block_size = block_size
                    if block_size == 18:
                        break

                block_distance += 1

            if best_block_size >= 3:
                dest[flags_index] |= 0x80 >> i
                src_pos += best_block_size
                best_block_size -= 3
                best_block_distance -= 1
                dest[dest_pos:dest_pos+2] = [(best_block_size << 4) | ((best_block_distance >> 8) & 0xF),
                                             best_block_distance & 0xFF]
                dest_pos += 2
            else:
                dest[dest_pos] = _src[src_pos]
                src_pos += 1
                dest_pos += 1

            if src_pos >= src_size:
                # Pad to multiple of 4 bytes
                dest_pos = ((dest_pos >> 2) + 1) << 2
                return bytes(dest[:dest_pos])


def decompress_lz_data(_src: bytes):
    # Performs an LZ decompression of the given data
    src_size = len(_src)
    if src_size < 4:
        raise Exception(f"Fatal error while decompressing LZ file: size of file is {src_size}")

    dest_size = int.from_bytes(bytes(_src[1:4]), "little")
    dest = [0 for _ in range(dest_size)]

    src_pos = 4
    dest_pos = 0
    compressed_byte_count = 0

    while True:
        if src_pos >= src_size:
            raise Exception(f"Fatal error while decompressing LZ file: {src_pos}/{src_size}")

        # A control byte exists to give info about the 8 following data points
        # Each bit tells whether the next data point is compressed (1) or raw (0) data
        control_byte = int(_src[src_pos])
        src_pos += 1

        for i in range(8):
            if control_byte & 0x80:
                # Compressed data: references data previously added to the output file and the number of repetitions
                if src_pos + 1 >= src_size:
                    raise Exception(f"Fatal error while decompressing LZ file: {src_pos}/{src_size}")

                compressed_byte_count += 1
                block = int.from_bytes(bytes(_src[src_pos:src_pos+2]), "big")
                block_size = (block >> 12) + 3
                block_distance = (block & 0xFFF) + 1

                src_pos += 2

                block_pos = dest_pos - block_distance
                if dest_pos + block_size > dest_size:
                    block_size = dest_size - dest_pos
                    print("LZ decompression: Destination buffer overflow.")

                if block_pos < 0:
                    raise Exception("Fatal error while decompressing LZ file: "
                                    + f"Distance is {block_pos} ({dest_pos} - {dest_pos}).")

                for j in range(block_size):
                    dest[dest_pos] = dest[block_pos + j]
                    dest_pos += 1
            else:
                # Raw data: copies the byte as-is to the output
                if src_pos >= src_size or dest_pos >= dest_size:
                    raise Exception("Fatal error while decompressing LZ file: "
                                    + f"{src_pos}/{src_size} and {dest_pos}/{dest_size}.")
                dest[dest_pos] = _src[src_pos]
                dest_pos += 1
                src_pos += 1

            if dest_pos == dest_size:
                return bytes(dest)

            control_byte <<= 1


#########################
# Sprite Transformation #
#########################


def compress_sprite(_src: bytes, _bits_per_pixel: int):
    # Returns sprite data with each pixel taking as little space as possible
    # Useful for turning Pillow sprite data into GBA sprite data
    if _bits_per_pixel == 8:
        return _src

    pixels_per_bytes = round(8 / _bits_per_pixel)
    dest: list[int] = []
    for src_bytes in [_src[i:i+pixels_per_bytes] for i in range(0, len(_src), pixels_per_bytes)]:
        dest_byte = 0
        bits = 0
        for src_byte in src_bytes:
            dest_byte |= src_byte << bits
            bits += _bits_per_pixel
        dest.append(dest_byte)
    return bytes(dest)


def decompress_sprite(_src: bytes, _bits_per_pixel: int):
    # Returns sprite data with each pixel taking one full byte of space
    # Useful for turning GBA sprite data into Pillow sprite data
    if _bits_per_pixel == 8:
        return _src

    pixels_per_bytes = round(8 / _bits_per_pixel)
    data_per_pixel = int(math.pow(2, _bits_per_pixel)) - 1

    dest: list[int] = []
    for byte in _src:
        for _ in range(pixels_per_bytes):
            pixel = byte & data_per_pixel
            byte >>= _bits_per_pixel
            dest.append(pixel)
    return bytes(dest)


def chunk_sprite(_src: bytes, _width: int, _height: int):
    # Sprites stored in ROMs are bundled in 8x8 pixel chunks
    # This function applies this behavior, turning simple sprites into chunked pixel data
    # Only allows for sprites having both dimensions as a multiple of 8 for speed's sake
    if _width % 8 or _height % 8:
        raise Exception("Sprites must have both of their dimensions as multiples of 8 to be chunkable!")

    src_size = _width * _height
    dest = [0 for _ in range(src_size)]

    blocks_per_line = math.ceil(_width / 8)
    block_x_shift = 64
    block_y_shift = block_x_shift * blocks_per_line
    src_shift = 0
    while src_shift < src_size:
        block_x = math.floor((src_shift % _width) / 8)
        temp_src_shift = math.floor(src_shift / _width)
        y = temp_src_shift % 8
        block_y = math.floor(temp_src_shift / 8)
        dest_pos = (block_y * block_y_shift) + (block_x * block_x_shift) + (y * 8)
        dest[dest_pos:dest_pos+8] = [int(byte) for byte in _src[src_shift:src_shift+8]]
        src_shift += 8
    return bytes(dest)


def dechunk_sprite(_src: bytes, _width: int, _height: int):
    # Sprites stored in ROMs are bundled in 8x8 pixel chunks
    # This function reverts this behavior, returning raw, non-chunked pixel data
    # Only allows for sprites having both dimensions as a multiple of 8 for speed's sake
    if _width % 8 or _height % 8:
        raise Exception("Sprites must have both of their dimensions as multiples of 8 to be chunkable!")

    src_size = _width * _height
    dest = [0 for _ in range(src_size)]

    src_shift = 0
    block_x = 0
    block_y = 0
    while src_shift < src_size:
        for y in range(min(_height - (block_y * 8), 8)):
            dest_pos = (block_y * 8 + y) * _width + block_x * 8
            dest[dest_pos:dest_pos+8] = [int(byte) for byte in _src[src_shift:src_shift+8]]
            src_shift += 8
        block_x += 1
        if block_x * 8 >= _width:
            block_x = 0
            block_y += 1
    return bytes(dest)


def spread_palettes_to_sprite_frames(_src: bytes, _width: int, _height: int, _frames: int):
    # Adds values to the pixels in the sheet to match values in an extended palette
    # Assumes all palettes have exactly 16 colors
    _src = bytearray(_src)
    src_size = _width * _height
    data_size_per_frame = round(src_size / _frames)
    for frame in range(1, _frames):
        shift = frame * data_size_per_frame
        for pixel in range(data_size_per_frame):
            _src[shift + pixel] |= frame << 4
    return bytes(_src)


#############################
# Pokemon Data Manipulation #
#############################


def get_pokemon_data(_pokemon_name: str, _field=""):
    # Gets a given field or all data from a given pokemon
    if _pokemon_name.startswith("Unown "):
        _pokemon_name = "Unown A"
    data_container_name = "move_pool" if _field == "move_pool" else "stats"
    data_key = f"pokemon_{data_container_name}"
    data_address, _, _ = get_address_from_address_collection(_pokemon_name, data_key, data_container_name)[0]
    if _field == "move_pool":
        # Move pools are given as pointers, so seek their value
        data_address = int.from_bytes(bytes(current_rom[data_address:data_address+3]), "little")
    end_address = data_address + (100 if _field == "move_pool" else 28)
    data = current_rom[data_address:end_address]
    if _field == "move_pool":
        return decode_move_pool(data)
    if not _field:
        return get_all_pokemon_data(_pokemon_name)
    field_info = POKEMON_DATA_INFO.get(_field, {})
    if not field_info:
        raise Exception(f"The field {_field} doesn't exist in a Pokemon's data.")
    data_address = field_info["shift"]
    end_address = data_address + field_info["size"]
    return int.from_bytes(bytes(data[data_address:end_address]), "little")


def get_all_pokemon_data(_pokemon_name: str):
    # Gets all the data from a given pokemon
    if _pokemon_name.startswith("Unown "):
        _pokemon_name = "Unown A"
    result: dict[str, int | list[dict[str, str | int]]] = {}
    for field in [*POKEMON_DATA_INFO, "move_pool"]:
        result[field] = get_pokemon_data(_pokemon_name, field)
    return result


def encode_pokemon_data(_data: dict[str, int | list[dict[str, str | int]]]) -> bytes:
    # Encodes pokemon data into data to add to the ROM
    output = bytearray(28)
    for field_name in _data:
        if field_name == "move_pool":
            continue
        shift = POKEMON_DATA_INFO[field_name]["shift"]
        size = POKEMON_DATA_INFO[field_name]["size"]
        output[shift:shift+size] = _data[field_name].to_bytes(size, "little")
    return bytes(output)


def stringify_pokemon_data(_data: dict[str, int | list[dict[str, str | int]]]):
    # Transforms a pokemon's data into a string
    result = ""
    for field_name in _data:
        field_value: int | list[dict[str, str | int]] = _data[field_name]
        new_field_value: str
        if field_name in ["type1", "type2"]:
            new_field_value = POKEMON_TYPES[field_value]
        elif field_name in ["ability1", "ability2"]:
            new_field_value = POKEMON_ABILITIES[field_value].title()
        elif field_name == "gender_ratio":
            new_field_value = POKEMON_GENDER_RATIOS[field_value]
        elif field_name == "dex":
            # The dex value is stored as a boolean named "forbid_flip" for clarity
            new_field_value = "True" if field_value & 0x80 else "False"
            field_name = "forbid_flip"
        elif field_name == "move_pool":
            new_field_value = stringify_move_pool(field_value).replace("\n", ", ")
        else:
            new_field_value = str(field_value)
        result += "{}: {}\n".format(field_name, new_field_value)
    return result[:-1]


def destringify_pokemon_data(_pokemon_name: str, _data_string: str, _safe_mode=False):
    # Transforms a pokemon's data given as a string into a dictionary holding said pokemon's data
    if _pokemon_name.startswith("Unown "):
        _pokemon_name = "Unown A"
    result: dict[str, int | list[dict[str, str | int]]] = {}
    for field_line in _data_string.split("\n"):
        field_info = field_line.split(":", 1)
        field_name = field_info[0].strip()
        field_value = field_info[1].strip()
        new_field_value: str | int | list[dict[str, str | int]]
        if field_name in ["hp", "atk", "def", "spatk", "spdef", "spd"]:
            new_field_value = field_value if _safe_mode else int(field_value)
        elif field_name in ["type1", "type2"]:
            new_field_value = field_value if _safe_mode else POKEMON_TYPES.index(field_value)
        elif field_name in ["ability1", "ability2"]:
            new_field_value = field_value if _safe_mode else POKEMON_ABILITIES.index(field_value.upper())
        elif field_name == "gender_ratio":
            new_field_value = field_value if _safe_mode else REVERSE_POKEMON_GENDER_RATIOS[field_value]
        elif field_name in ["dex", "forbid_flip"]:
            # The dex value is stored as a boolean named "forbid_flip" for clarity
            new_field_value = field_value if _safe_mode else (1 if field_value in [1, "1", "True"] else 0)
            field_name = "dex"
        elif field_name == "move_pool":
            # Used to transform an old data format into the current format
            if field_value.startswith("[ "):
                field_value = field_value[2:-2]
            if not _safe_mode:
                move_pool_errors, has_move_pool_error = validate_move_pool_string(_pokemon_name,
                                                                                  field_value.replace(", ", "\n"))
                if has_move_pool_error:
                    raise Exception(f"Bad move pool: {move_pool_errors}")
                new_field_value = destringify_move_pool(field_value.replace(", ", "\n"))
            else:
                new_field_value = field_value
        result[field_name] = new_field_value
    return result


def merge_pokemon_data(_old_data: dict[str, int | list[dict[str, str | int]]],
                       _new_data: dict[str, int | list[dict[str, str | int]]],
                       _is_dex_simple=False):
    # Merges two pokemon data objects
    merged_data = _old_data
    for field_name in _new_data:
        if _is_dex_simple and field_name == "dex":
            merged_data[field_name] = (_new_data[field_name] << 7) + (_old_data[field_name] & 0x7F)
        else:
            merged_data[field_name] = _new_data[field_name]
    if "ability1" in merged_data and "ability2" in merged_data and not merged_data["ability2"]:
        merged_data["ability2"] = merged_data["ability1"]
    return merged_data


def keep_different_pokemon_data(_old_data: dict[str, int | list[dict[str, str | int]]],
                                _new_data: dict[str, int | list[dict[str, str | int]]]):
    # Returns only different fields between the two pokemon data objects given
    different_data = {k: v for k, v in _new_data.items()
                      if k not in list(_old_data.keys()) or (v != _old_data[k] and k != "move_pool")}

    if "ability2" in different_data and "ability2" in _new_data and "ability2" in _old_data and "ability1" in _old_data:
        # In case of no ability2, validate the check if the value is the same as ability1"s
        if not _old_data["ability2"] and _new_data["ability2"] == _old_data["ability1"]:
            different_data.pop("ability2")

    if "move_pool" in list(_new_data.keys()) and "move_pool" in list(_old_data.keys())\
            and not are_move_pools_equal(_new_data["move_pool"], _old_data["move_pool"]):
        different_data["move_pool"] = _new_data["move_pool"]
    return different_data


def stringify_move_pool(_move_pool: list[dict[str, str | int]]):
    # Transforms a pokemon"s move pool a string
    result = ""
    for move_info in _move_pool:
        result += "{}: {}\n".format(move_info['move'], move_info['level'])
    return result[:-1]


def destringify_move_pool(_move_pool_string: str):
    # Transforms a pokemon's move pool given as a string into a list of dictionaries holding said move pool data
    result: list[dict[str, str | int]] = []
    for move_line in _move_pool_string.split("\n"):
        if not move_line:
            continue
        move_info = move_line.split(":", 1)
        move_name = move_info[0].strip()
        move_level = int(move_info[1].strip())
        result.append({"move": move_name, "level": move_level})
    return result


def decode_move_pool(_data: bytes):
    # Decodes move pool data from a list of bytes into a list of moves
    result: list[dict[str, str | int]] = []
    data_size = round(len(_data) / 2)
    for i in range(data_size):
        move_data = int.from_bytes(bytes(_data[i*2:(i+1)*2]), "little")
        if move_data == 0xFFFF:
            break
        move_id = move_data & 0x1FF
        move_level = move_data >> 9
        result.append({"move": POKEMON_MOVES[move_id - 1].title(), "level": move_level})
    return result


def encode_move_pool(_move_pool: list[dict[str, str | int]]):
    # Encodes move pool data from a list of moves into a list of bytes
    result = bytearray()
    for move_data in _move_pool:
        move_id = POKEMON_MOVES.index(move_data["move"].upper()) + 1
        move_level = move_data["level"]
        move_data = (move_level << 9) + move_id
        result.extend(move_data.to_bytes(2, "little"))
    # Surround the table by FFFF as the move pool functions looks for the beginning and end of the table
    return bytes(result + b"\xff\xff")


def are_move_pools_equal(_move_pool_1: list[dict[str, str | int]], _move_pool_2: list[dict[str, str | int]]):
    # Compares two move pool objects
    if len(_move_pool_1) != len(_move_pool_2):
        return False
    for i in range(len(_move_pool_1)):
        move_data_1 = _move_pool_1[i]
        move_data_2 = _move_pool_2[i]
        if move_data_1["move"] != move_data_2["move"] or move_data_1["level"] != move_data_2["level"]:
            return False
    return True


###################
# FR/LG Extension #
###################

FOLDER_OBJECT_INFOS: list[dict[str, str | list[str] | dict[str, list[str]]]] = None
INTERNAL_ID_TO_OBJECT_ADDRESS: dict[str, tuple[str, int, bool]] = None
OVERWORLD_SPRITE_ADDRESSES: dict[str, list[int]] = None
POINTER_REFERENCES: dict[str, list[tuple[str, int]]] = None
VALID_OVERWORLD_SPRITE_SIZES: list[dict[str, int | str]] = None
SPRITES_REQUIREMENTS: dict[str, dict[str, bool | int | list[int]]] = None
SPRITES_REQUIREMENTS_EXCEPTIONS: dict[str, dict[str, dict[str, bool | int | list[int]]]] = None
OVERWORLD_PALETTE_IDS: dict[str, int] = None
DATA_ADDRESSES_INFO: dict[str, int | dict[str, int]] = None


def load_constants(_rom_version=rom_version):
    # Loads all constants depending on the version of the Pokemon ROM
    global FOLDER_OBJECT_INFOS, INTERNAL_ID_TO_OBJECT_ADDRESS, OVERWORLD_SPRITE_ADDRESSES, POINTER_REFERENCES, \
        VALID_OVERWORLD_SPRITE_SIZES, SPRITES_REQUIREMENTS, SPRITES_REQUIREMENTS_EXCEPTIONS, OVERWORLD_PALETTE_IDS, \
        DATA_ADDRESSES_INFO
    if not frlg_support or _rom_version == "Emerald":
        FOLDER_OBJECT_INFOS = EMERALD_FOLDER_OBJECT_INFOS
        INTERNAL_ID_TO_OBJECT_ADDRESS = EMERALD_INTERNAL_ID_TO_OBJECT_ADDRESS
        OVERWORLD_SPRITE_ADDRESSES = EMERALD_OVERWORLD_SPRITE_ADDRESSES
        POINTER_REFERENCES = EMERALD_POINTER_REFERENCES
        VALID_OVERWORLD_SPRITE_SIZES = EMERALD_VALID_OVERWORLD_SPRITE_SIZES
        SPRITES_REQUIREMENTS = EMERALD_SPRITES_REQUIREMENTS
        SPRITES_REQUIREMENTS_EXCEPTIONS = EMERALD_SPRITES_REQUIREMENTS_EXCEPTIONS
        OVERWORLD_PALETTE_IDS = EMERALD_OVERWORLD_PALETTE_IDS
    else:
        FOLDER_OBJECT_INFOS = FR_LG_FOLDER_OBJECT_INFOS
        INTERNAL_ID_TO_OBJECT_ADDRESS = FR_LG_INTERNAL_ID_TO_OBJECT_ADDRESS
        OVERWORLD_SPRITE_ADDRESSES = FR_LG_OVERWORLD_SPRITE_ADDRESSES
        POINTER_REFERENCES = FR_LG_POINTER_REFERENCES
        VALID_OVERWORLD_SPRITE_SIZES = FR_LG_VALID_OVERWORLD_SPRITE_SIZES
        SPRITES_REQUIREMENTS = FR_LG_SPRITES_REQUIREMENTS
        SPRITES_REQUIREMENTS_EXCEPTIONS = FR_LG_SPRITES_REQUIREMENTS_EXCEPTIONS
        OVERWORLD_PALETTE_IDS = FR_LG_OVERWORLD_PALETTE_IDS
    data_addresses_infos = EMERALD_DATA_ADDRESS_INFOS | FR_LG_DATA_ADDRESS_INFOS
    DATA_ADDRESSES_INFO = data_addresses_infos.get(_rom_version, {})
    if not DATA_ADDRESSES_INFO:
        raise Exception(f"Unknown ROM version {_rom_version}.")


def find_folder_object_info(_key="", _name=""):
    # Returns a folder object info dictionary given a key, name, or both given
    for folder_info in FOLDER_OBJECT_INFOS:
        if _key and not _key.startswith(folder_info["key"]):
            # Key found but is not a match
            continue
        if "name" in list(folder_info.keys()) and _name != folder_info["name"]:
            # Name restriction is not a match
            continue
        if _name and _name not in folder_info["folders"]:
            # Name given is not a match
            continue
        return folder_info
    raise Exception(f"Unknown folder object with key {_key}{f' and name {_name}' if _name else ''}")


#####################
# Utility Functions #
#####################


def get_bits_per_pixel_from_palette_size(_palette_size: int) -> int:
    # Returns how many bits are needed to store a pixel for a palette of a given size
    if _palette_size <= 2:
        return 1
    if _palette_size <= 16:
        return 4
    if _palette_size <= 256:
        return 8
    raise Exception("A sprite with a palette with more than 256 colors cannot be handled by the ROM.")


def get_address_from_address_collection(_object_name: str, _resource_key: str, _resource_name: str,
                                        _raw_key=False) -> list[tuple[int, bool, bytearray]]:
    # Returns known addresses from the ROM's address collection

    if _resource_key.startswith("pokemon_"):
        # Fetches internal Pokemon ID then resource address
        pokemon_id: int = POKEMON_NAME_TO_ID[_object_name]
        pokemon_internal_id: int = POKEMON_ID_TO_INTERNAL_ID.get(pokemon_id, pokemon_id)
        address_name, id_shift, is_raw = INTERNAL_ID_TO_OBJECT_ADDRESS[_resource_key]
        shift = id_shift * pokemon_internal_id
    elif not _raw_key:
        # Fetches named Trainer resource address
        named_key = f"{_object_name.lower()}_{_resource_name}"
        address_name, shift, is_raw = INTERNAL_ID_TO_OBJECT_ADDRESS[named_key]
    else:
        address_name, shift, is_raw = INTERNAL_ID_TO_OBJECT_ADDRESS[_resource_name]

    output: list[tuple[int, bool, bytearray]] = []
    if address_name in extended_data_dict_by_named_address:
        output.append((shift, is_raw, extended_data_dict_by_named_address[address_name]["data"]))
    output.append((data_addresses[address_name] + shift, is_raw, bytearray()))
    return output


def get_overworld_sprite_addresses(_object_name: str, _resource_name: str):
    named_key = f"{_object_name.lower()}_{_resource_name}"
    return [data_addresses["gObjectEventGraphicsInfoPointers"] + shift
            for shift in OVERWORLD_SPRITE_ADDRESSES[named_key]]


def handle_overworld_custom_size(_extra_data: list[str]):
    # Checks if the custom size passed for a given overworld sprite sheet is valid
    sizes = _extra_data[0].split("x")
    if len(sizes) != 2:
        raise Exception("An overworld sprite's custom size must be in the format <width>x<height>, "
                        + "with <width> and <height> as numbers.")
    sprite_width = int(sizes[0])
    sprite_height = int(sizes[1])
    valid_sprite_size = next(filter(lambda f: f["width"] == sprite_width and f["height"] == sprite_height,
                                    VALID_OVERWORLD_SPRITE_SIZES), None)
    if not valid_sprite_size:
        raise Exception(f"Overworld sprites cannot have a custom size of {sizes[0]}x{sizes[1]}")
    return valid_sprite_size


def get_overworld_sprite_data(_data_address: int, _key: str, _get_address=False):
    # Returns the value of given data from an overworld sprite data object
    value_data: dict[str, int] = OVERWORLD_SPRITE_OBJECT_INFO.get(_key, {})
    if not value_data:
        raise Exception(f"Could not get the value {_key} from an overworld sprite's data.")
    start_address: int = _data_address + value_data.get("shift")
    if _get_address:
        return start_address
    end_address: int = start_address + value_data.get("size")
    return int.from_bytes(bytes(current_rom[start_address:end_address]), "little")


def set_overworld_sprite_data(_data_address: int, _key: str, _value: int):
    # Sets the value of given data from an overworld sprite data object
    value_data: dict[str, int] = OVERWORLD_SPRITE_OBJECT_INFO.get(_key, {})
    if not value_data:
        raise Exception(f"Could not set the value {_key} from an overworld sprite's data.")
    _data_address += value_data.get("shift")
    size: int = value_data.get("size")
    add_data_to_patch({"address": _data_address, "length": size, "data": _value.to_bytes(size, "little")})


def get_sprite_requirements(_sprite_key: str, _object_name: str):
    # Returns the requirements of a given sprite for a given pokemon or trainer
    if _object_name.startswith("Unown "):
        _object_name = "Unown A"

    sprite_name = _sprite_key[8:]
    reference_sprite_name: str = SPRITE_PIXEL_REFERENCE.get(sprite_name, sprite_name)
    reference_sprite_key = _sprite_key[:8] + reference_sprite_name
    _sprite_key = _sprite_key[:8] + sprite_name

    reqs = SPRITES_REQUIREMENTS.get(_sprite_key, {})
    reference_reqs = SPRITES_REQUIREMENTS.get(reference_sprite_key, {})
    reqs_exceptions_list = SPRITES_REQUIREMENTS_EXCEPTIONS.get(_object_name, {})
    reqs_exceptions = reqs_exceptions_list.get(_sprite_key, {})
    reference_reqs_exceptions = reqs_exceptions_list.get(reference_sprite_key, {})
    result = reference_reqs | reference_reqs_exceptions | reqs | reqs_exceptions
    if "frames" in result:
        if type(result["frames"]) is int:
            result["frames"] = [result["frames"]]
        if "internal_frames" not in result:
            result["internal_frames"] = result["frames"][0]

    return result


def is_complex_sprite(_sprite_key: str):
    # Checks if a sprite is a complex sprite
    return _sprite_key in COMPLEX_SPRITES_LIST


def is_overworld_sprite(_sprite_key: str):
    # Checks if a sprite is an overworld sprite
    return not _sprite_key.startswith("pokemon_") and "battle" not in _sprite_key


def handle_address_collection(_rom: bytearray, _rom_version: str, _forced_is_ap: bool = None):
    # Picks and stores the right address collection for the given ROM
    global rom_version
    rom_version = _rom_version

    data_address_infos: list[dict[str, int | dict[str, int]]] = EMERALD_DATA_ADDRESS_INFOS | FR_LG_DATA_ADDRESS_INFOS
    data_address_info: dict[str, int | dict[str, int]] = data_address_infos.get(_rom_version, {})
    if not data_address_info:
        raise Exception(f"Unknown ROM version {_rom_version}")

    global rom_is_ap
    rom_is_ap = _forced_is_ap if _forced_is_ap is not None else zlib.crc32(_rom) != data_address_info["crc32"]

    global data_addresses
    data_addresses = data_address_info["ap_addresses"] if rom_is_ap else data_address_info["original_addresses"]

    global current_rom
    current_rom = _rom
    return rom_is_ap


def five_to_eight_bits_palette(value: int):
    # Transforms a 5-bit long palette color into an 8-bit long palette color
    return (value << 3) + math.floor(value / 31 * 7)


def eight_to_five_bits_palette(value: int):
    # Transforms a 8-bit long palette color into an 5-bit long palette color
    return value >> 3


def flatten_2d(input_list: list):
    # Flattens a list containing lists into a single unidimensional list
    result = []
    for sublist in input_list:
        for item in sublist:
            result.append(item)
    return result
