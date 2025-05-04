import math
import os
import zlib

from pygbagfx import _gbagfx # from package
from PIL import Image
from .data import data
from .adjuster_constants import *

address_label_to_resource_path_list = { }
files_to_clean_up = []
sprite_pack_data = { }
resource_address_to_insert_to = 0x00
current_rom = None

data_addresses = DATA_ADDRESSES_MOCK_AP

####################
## Main Functions ##
####################

def get_patch_from_sprite_pack(_sprite_pack_path, _rom):
    # Builds a patch from a given sprite pack to apply to the ROM
    handle_address_collection(_rom, True)

    global sprite_pack_data, resource_address_to_insert_to
    # Build patch data, fetch end of file
    sprite_pack_data = { "length": 16777216, "data": [] }
    resource_address_to_insert_to = ((data_addresses["sEmpty6"] >> 12) + 1) << 12 # Should be E3D000

    # Handle existing Trainer & Pokemon folders
    add_sprite_pack_object_collection(_sprite_pack_path, TRAINER_FOLDERS, TRAINER_SPRITES, TRAINER_PALETTES, False)
    add_sprite_pack_object_collection(_sprite_pack_path, POKEMON_FOLDERS, POKEMON_SPRITES, POKEMON_PALETTES, True)

    # Remove temporary files
    clean_up()
    return sprite_pack_data

def clean_up():
    # Remove all temporary files after processing
    for file in files_to_clean_up:
        if os.path.isfile(file):
            os.remove(file)
    files_to_clean_up.clear()

#########################
## Patch Data Building ##
#########################

def add_sprite_pack_object_collection(_sprite_pack_path, _folders_list, _sprites_list, _palette_lists, _is_pokemon):
    # Adds data from all pokemon or all trainers to the patch if a folder including their name can be found
    for object_name in _folders_list:
        object_folder_path = os.path.join(_sprite_pack_path, object_name)
        if not os.path.exists(object_folder_path):
            continue
        found_sprites = { }
        for sprite_name in os.listdir(object_folder_path):
            if not sprite_name.endswith('.png'):
                continue
            # Only handle sprites which are awaited for the current object
            matching_sprite_name = next(filter(lambda f: sprite_name.startswith(f), _sprites_list), None)
            if not matching_sprite_name:
                continue
            sprite_file_name_data = sprite_name[:-4].split('-')[1:]
            extra_sprite_data = sprite_file_name_data or None
            sprite_path = os.path.join(object_folder_path, sprite_name)
            if os.path.exists(sprite_path):
                if found_sprites.get(matching_sprite_name):
                    continue
                found_sprites[matching_sprite_name] = sprite_name
                add_sprite(_is_pokemon, object_name, matching_sprite_name, extra_sprite_data, sprite_path)
        for palette, palette_extraction_priority_queue in _palette_lists.items():
            # Generate palettes if sprites exist
            found_sprite = False
            for sprite_name in palette_extraction_priority_queue:
                if sprite_name in found_sprites:
                    sprite_path = os.path.join(object_folder_path, found_sprites.get(sprite_name))
                    found_sprite = True
                    add_palette(_is_pokemon, object_name, palette, sprite_path)
                    break
            if not found_sprite:
                # Try to find raw sprites if they have not been recorded yet
                for sprite_name in palette_extraction_priority_queue:
                    sprite_path = os.path.join(object_folder_path, sprite_name + '.png')
                    if os.path.exists(sprite_path):
                        add_palette(_is_pokemon, object_name, palette, sprite_path)
                        break

def add_sprite(_is_pokemon, _object_name, _sprite_name, _extra_data, _path):
    # Adds a sprite to the patch
    sprite_key = ("pokemon_" if _is_pokemon else "trainer_") + _sprite_name
    data_address = get_address_from_address_collection(_object_name, sprite_key, _sprite_name)

    if _is_pokemon and _sprite_name == 'icon' and _extra_data:
        # Pokemon palette indexed icon: Switch the palette to use if it's forced within the file's name
        palette_index = int(_extra_data[0])
        icon_index_address = get_address_from_address_collection(_object_name, sprite_key + '_index', _sprite_name)
        add_data_to_patch({ "address": icon_index_address, "length": 1, "data": palette_index.to_bytes(1, 'little')})

    if is_complex_sprite(sprite_key):
        data_address = replace_complex_sprite(data_address, sprite_key, _object_name, _extra_data)

    if sprite_key != "trainer_battle_back":
        add_resource(False, sprite_key, _sprite_name, data_address, _path)
    else:
        # In case of Trainer battle back sprite, rerun this function to fill in the ball throwing animation table
        address_bytes = resource_address_to_insert_to.to_bytes(3, 'little')
        add_data_to_patch({ "address": data_address, "length": 3, "data": address_bytes })
        add_sprite(_is_pokemon, _object_name, _sprite_name + "_throw", _extra_data, _path)

def add_palette(_is_pokemon, _object_name, _palette_name, _path):
    # Adds a palette to the patch
    palette_key = ("pokemon" if _is_pokemon else "trainer") + "_" + _palette_name
    data_address = get_address_from_address_collection(_object_name, palette_key, _palette_name)
    add_resource(True, palette_key, _palette_name, data_address, _path)

def add_resource(_is_palette, _key, _name, _data_address, _path):
    # Adds a resource (sprite or palette) to the patch
    global resource_address_to_insert_to
    address_bytes = resource_address_to_insert_to.to_bytes(3, 'little')
    add_data_to_patch({ "address": _data_address, "length": 3, "data": address_bytes })
    
    needs_compression = OBJECT_NEEDS_COMPRESSION.get(_key, False)
    if _is_palette:
        _path = handle_sprite_to_palette(_path, _name, needs_compression)
    else:
        _path = handle_sprite_to_gba_sprite(_path, needs_compression)
    
    file = open(_path, "rb")
    file_data = file.read()

    add_data_to_patch({ "address": resource_address_to_insert_to, "length": len(file_data), "data": file_data })
    # TODO: Fill in a free space list from the replaced data to fit more resources in the ROM
    resource_address_to_insert_to = resource_address_to_insert_to + len(file_data)
    if resource_address_to_insert_to > 0xFFFFFF:
        # Out of bounds: Too much data to add
        raise Exception('Too much data to add to the ROM! Please remove some resources.')

def add_data_to_patch(_data):
    # Adds the given data to the patch
    index = 0
    # Order entries by ascending starting address
    for existing_data in sprite_pack_data["data"]:
        if existing_data["address"] < _data["address"]:
            index = index + 1
        elif existing_data["address"] == _data["address"]:
            # Do not duplicate values
            return
        else:
            break
    sprite_pack_data["data"].insert(index, _data)

def call_gbagfx(_input, _output, _delete_input = False):
    # Calls the sprite processing C app
    _gbagfx.main(_input, _output)
    if _delete_input:
        os.remove(_input)

#############################
## Complex Sprite Handling ##
#############################

def replace_complex_sprite(_data_address, _sprite_key, _object_name, _extra_data):
    # Replaces a complex sprite's sprite data and update its other fields if needed
    sprite_size_data = None
    if _sprite_key == "trainer_battle_back_throw":
        # Trainer back sprites need further pointer seeking
        info_object_address = _data_address
        _data_address = int.from_bytes(bytes(current_rom[_data_address + 12:_data_address + 15]), 'little')
    elif is_overworld_sprite(_sprite_key):
        # Trainer overworld sprites need two objects to delve into
        info_object_address = int.from_bytes(bytes(current_rom[_data_address:_data_address + 3]), 'little')
        _data_address = get_overworld_sprite_data(info_object_address, 'sprites_ptr')
        if _extra_data:
            # If size given, extract it and check if it is supported
            sprite_size_data = handle_overworld_custom_size(_extra_data)

    sprite_data = get_sprite_requirements(_sprite_key, _object_name)
    temp_address = resource_address_to_insert_to
    if not sprite_data:
        raise Exception('Could not find sprite data for the sprite with key {} of object {}.'.format(_sprite_key, _object_name))

    sprite_width = sprite_size_data.get('width') if sprite_size_data else sprite_data.get('width', 0)
    sprite_height = sprite_size_data.get('height') if sprite_size_data else sprite_data.get('height', 0)
    sprite_palette_size = sprite_data.get('palette_size', 16)
    sprite_bytes_per_pixel, _ = get_pixel_size_and_extension_from_palette_size(sprite_palette_size)
    if is_overworld_sprite(_sprite_key) and not sprite_size_data:
        sprite_width = get_overworld_sprite_data(info_object_address, 'sprite_width')
        sprite_height = get_overworld_sprite_data(info_object_address, 'sprite_height')
    sprite_size = round(sprite_bytes_per_pixel * sprite_width * sprite_height)
    
    # Build a new complex sprite table and insert it
    output_data = bytearray(0)
    for i in range(0, sprite_data.get('frames')):
        output_data.extend(temp_address.to_bytes(3, 'little'))
        output_data.extend(b'\x08')
        output_data.extend(sprite_size.to_bytes(2, 'little'))
        output_data.extend(b'\x00\x00')
        temp_address += sprite_size
    add_data_to_patch({"address": _data_address, "length": len(output_data), "data": bytes(output_data)})
    
    if is_overworld_sprite(_sprite_key) and sprite_size_data:
        # If custom size given, update overworld sprite data
        for current_overworld_info_object_pointer in get_overworld_sprite_addresses(_object_name, _sprite_key[8:]):
            current_overworld_info_object = int.from_bytes(bytes(current_rom[current_overworld_info_object_pointer:current_overworld_info_object_pointer + 3]), 'little')
            set_overworld_sprite_data(current_overworld_info_object, 'sprite_length', sprite_size)
            set_overworld_sprite_data(current_overworld_info_object, 'sprite_width', sprite_width)
            set_overworld_sprite_data(current_overworld_info_object, 'sprite_height', sprite_height)
            set_overworld_sprite_data(current_overworld_info_object, 'size_draw_ptr', data_addresses[sprite_size_data.get('data')])
    
    return _data_address

def extract_complex_sprite(_overworld_struct_address, _sprite_key, _object_name, _palette_sprite_name):
    # Extracts a complex sprite from the ROM as a Pillow sprite ready to be saved 
    start_sprite_pointer = get_overworld_sprite_data(_overworld_struct_address, 'sprites_ptr')
    sprite_width = get_overworld_sprite_data(_overworld_struct_address, 'sprite_width')
    sprite_height = get_overworld_sprite_data(_overworld_struct_address, 'sprite_height')
    sprite_data = get_sprite_requirements(_sprite_key, _object_name)
    if not sprite_data:
        return
    sprites_pixel_data = []
    sprite_palette = None
    extra_sprite_name = ''
    for i in range(sprite_data['frames']):
        # Considers each frame as a sprite, then adds all of the frames' pixel data together
        start_sprite_address = int.from_bytes(bytes(current_rom[start_sprite_pointer:start_sprite_pointer + 3]), 'little')
        sprite, current_extra_sprite_name = extract_sprite(start_sprite_address, _sprite_key, _object_name, _palette_sprite_name, (sprite_width, sprite_height))
        sprites_pixel_data += sprite.getdata()
        if i == 0:
            sprite_palette = sprite.getpalette()
            extra_sprite_name = current_extra_sprite_name
        start_sprite_pointer += 8
    
    final_image = Image.new('P', (sprite_width, sprite_height * sprite_data['frames']))
    final_image.putdata(sprites_pixel_data)
    final_image.putpalette(sprite_palette)
    return final_image, extra_sprite_name


#####################
## Data Extraction ##
#####################

def extract_palette_from_file(_path):
    # Extracts a palette from an existing sprite file
    sprite_image = Image.open(_path)
    sprite_palette = sprite_image.getpalette() or []
    sprite_palette_colors = []
    for i in range(round(len(sprite_palette) / 3)):
        index = i * 3
        color = (int(sprite_palette[index]) << 16) + (int(sprite_palette[index+1]) << 8) + int(sprite_palette[index+2])
        sprite_palette_colors.append(hex(color)[2:].zfill(6))
    return sprite_palette_colors

def extract_sprites(_object_name, _output_path, _rom):
    # Extracts all sprites from a given object from the ROM into the given output folder
    handle_address_collection(_rom)

    def handle_sprite_extraction(_sprite_name):
        reference_sprite_name = SPRITE_PIXEL_REFERENCE.get(_sprite_name, _sprite_name)
        sprite_key = ('pokemon' if is_pokemon else 'trainer') + '_' + reference_sprite_name
        data_address = get_address_from_address_collection(_object_name, sprite_key, reference_sprite_name)
        data_address = int.from_bytes(bytes(current_rom[data_address:data_address + 3]), 'little')

        if is_complex_sprite(sprite_key):
            sprite_object, extra_sprite_name = extract_complex_sprite(data_address, sprite_key, _object_name, reference_sprite_name)
        else:
            sprite_object, extra_sprite_name = extract_sprite(data_address, sprite_key, _object_name, _sprite_name)
        full_path = os.path.join(_output_path, _sprite_name + extra_sprite_name + '.png')
        sprite_object.save(full_path)

    is_pokemon = not _object_name in TRAINER_FOLDERS
    extracted_sprites = []

    # Extract all sprites awaited for the given object
    sprite_list = POKEMON_SPRITES if is_pokemon else TRAINER_SPRITES
    for sprite_name in sprite_list:
        handle_sprite_extraction(sprite_name)
        extracted_sprites.append(sprite_name)

    # If any extra sprite is awaited for depicting palettes, extract them as well
    palette_lists = POKEMON_PALETTES if is_pokemon else TRAINER_PALETTES
    palette_sprites = [palette_lists[palette_list] for palette_list in palette_lists]
    palette_sprites = filter(lambda s: s, [sprite if not sprite in extracted_sprites else None for sprite in flatten_2d(palette_sprites)])
    for sprite_name in palette_sprites:
        handle_sprite_extraction(sprite_name)

def extract_sprite(_data_address, _sprite_key, _object_name, _palette_sprite_name, _preset_size = 0):
    # Extracts a given sprite from the ROM as a Pillow sprite ready to be saved
    extra_sprite_name = ''

    needs_compression = OBJECT_NEEDS_COMPRESSION.get(_sprite_key, False)
    sprite_requirements = get_sprite_requirements(_sprite_key, _object_name)
    sprite_palette_size = sprite_requirements.get('palette_size', 16)
    pixel_byte_size, _ = get_pixel_size_and_extension_from_palette_size(sprite_palette_size)
    # Retrieve the sprite's size
    if _preset_size:
        sprite_width = _preset_size[0]
        sprite_height = _preset_size[1]
    else:
        sprite_width = sprite_requirements['width']
        sprite_height = sprite_requirements['height'] * sprite_requirements['frames']
    
    # Extract the sprite's pixel data
    sprite_size = round(sprite_width * sprite_height * pixel_byte_size)
    end_address = _data_address + sprite_size + ((4 + math.ceil(sprite_size / 8)) if needs_compression else 0)
    sprite_pixel_data = current_rom[_data_address:end_address]
    if needs_compression:
        sprite_pixel_data = truncate_lz_compressed_data(sprite_pixel_data, sprite_size)
        sprite_pixel_data = decompress_lz_data(sprite_pixel_data)
    sprite_pixel_data = decompress_sprite(sprite_pixel_data, round(8 * pixel_byte_size))
    sprite_pixel_data = dechunk_sprite(sprite_pixel_data, sprite_width, sprite_height)
    if sprite_requirements.get('palette_per_frame', False):
        sprite_pixel_data = spread_palettes_to_sprite_frames(sprite_pixel_data, sprite_width, sprite_height, sprite_requirements.get('palettes', 1))
    
    # Extract the sprite's palette(s)
    if _palette_sprite_name == 'icon':
        # Retrieve the icon's palette index and add it at the end of the file's name
        icon_index_address = get_address_from_address_collection(_object_name, _sprite_key + '_index', _object_name)
        icon_index = int(current_rom[icon_index_address])
        sprite_palette = bytes(VALID_ICON_PALETTES[icon_index])
        extra_sprite_name = '-{}'.format(int(icon_index))
    elif _palette_sprite_name == 'footprint':
        sprite_palette = bytes(VALID_FOOTPRINT_PALETTE)
    else:
        sprite_palette = extract_palette(_object_name, _palette_sprite_name, _sprite_key.startswith('pokemon_'))

    # Assemble the sprite
    extracted_image = Image.new('P', (sprite_width, sprite_height))
    extracted_image.putdata(sprite_pixel_data)
    extracted_image.putpalette(sprite_palette)
    return extracted_image, extra_sprite_name

def extract_palette(_object_name, _sprite_name, _is_pokemon):
    # Extracts a palette as a list of RGB colors with values between 0 and 255
    palette_lists = POKEMON_PALETTES if _is_pokemon else TRAINER_PALETTES
    palette_name = next(filter(lambda palette_list: palette_list if _sprite_name in palette_lists[palette_list] else None, palette_lists), None)
    palette_key = ('pokemon_' if _is_pokemon else 'trainer_') + palette_name
    sprite_key = ('pokemon_' if _is_pokemon else 'trainer_') + _sprite_name

    sprite_requirements = get_sprite_requirements(sprite_key, _object_name)
    palette_size = sprite_requirements.get('palette_size', 16) * sprite_requirements.get('palettes', 1) * 2
    data_address = get_address_from_address_collection(_object_name, palette_key, palette_name)
    data_address = int.from_bytes(bytes(current_rom[data_address:data_address + 3]), 'little')

    needs_compression = OBJECT_NEEDS_COMPRESSION.get(palette_key, False)
    end_address = data_address + palette_size + ((4 + math.ceil(palette_size / 8)) if needs_compression else 0)
    palette_data = current_rom[data_address:end_address]
    if needs_compression:
        # If the data is compressed, decompress it first
        palette_data = truncate_lz_compressed_data(palette_data, palette_size)
        palette_data = decompress_lz_data(palette_data)

    palette = []
    for i in range(round(palette_size / 2)):
        palette_five_bits_color = int.from_bytes(palette_data[i*2:i*2+2], 'little')
        for _ in range(3):
            palette.append(five_to_eight_bits_palette(palette_five_bits_color % 32))
            palette_five_bits_color >>= 5
    return palette

#####################
## Data Conversion ##
#####################

def handle_sprite_to_gba_sprite(_sprite_path, _needs_compression) -> str:
    # Transforms indexed/grayscale PNG sprites into GBA sprites
    sprite_path_with_no_extension = str(os.path.splitext(_sprite_path)[0])
    file_format = ".1bpp" if sprite_path_with_no_extension.endswith("footprint") else ".4bpp"
    gba_sprite_path = sprite_path_with_no_extension + file_format
    call_gbagfx(_sprite_path, gba_sprite_path, False)
    if not _needs_compression:
        files_to_clean_up.append(gba_sprite_path)
        return gba_sprite_path
    else:
        # Compresses sprite if needed
        compressed_gba_sprite_path = gba_sprite_path + ".lz"
        call_gbagfx(gba_sprite_path, compressed_gba_sprite_path, True)
        files_to_clean_up.append(compressed_gba_sprite_path)
        return compressed_gba_sprite_path

def handle_gba_sprite_to_sprite(_gba_sprite_path, _needs_compression) -> str:
    # Transforms GBA sprite into indexed/grayscale PNG sprites
    _gba_sprite_path_with_no_extension = str(os.path.splitext(_gba_sprite_path)[0])
    file_format = ".1bpp" if _gba_sprite_path_with_no_extension.endswith("footprint") else ".4bpp"
    decompressed_gba_sprite_path = _gba_sprite_path_with_no_extension + file_format
    sprite_path = _gba_sprite_path_with_no_extension + ".png"
    if _needs_compression:
        # Decompresses sprite if needed
        call_gbagfx(_gba_sprite_path, decompressed_gba_sprite_path, True)
    call_gbagfx(decompressed_gba_sprite_path, sprite_path, True)
    return sprite_path

def handle_sprite_to_palette(_sprite_path, _palette_name, _needs_compression) -> str:
    # Transforms indexed/grayscale PNG sprites into GBA palettes
    sprite_path_with_no_extension = str(os.path.splitext(_sprite_path)[0])
    palette_path_with_no_extension = os.path.join(os.path.dirname(sprite_path_with_no_extension), _palette_name)
    palette_path = sprite_path_with_no_extension + ".pal"
    gba_palette_path = palette_path_with_no_extension + ".gbapal"
    call_gbagfx(_sprite_path, palette_path, False)
    call_gbagfx(palette_path, gba_palette_path, True)
    if not _needs_compression:
        files_to_clean_up.append(gba_palette_path)
        return gba_palette_path
    else:
        # Compress palette if needed
        compressed_gba_palette_path = gba_palette_path + ".lz"
        call_gbagfx(gba_palette_path, compressed_gba_palette_path, True)
        files_to_clean_up.append(compressed_gba_palette_path)
        return str(compressed_gba_palette_path)

###################
## Data Checking ##
###################

def validate_sprite_pack(_sprite_pack_path, _rom):
    # Validates an entire sprite pack to see if it can be applied to the given ROM
    handle_address_collection(_rom)

    errors = ""
    has_error = False
    def add_error(_error, _is_error = False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += ('\n' if errors else '') + _error
    
    add_error(*validate_object_collection(_sprite_pack_path, TRAINER_FOLDERS, TRAINER_SPRITES, TRAINER_PALETTES))
    add_error(*validate_object_collection(_sprite_pack_path, POKEMON_FOLDERS, POKEMON_SPRITES, POKEMON_PALETTES))
    return errors, has_error

def validate_object_collection(_sprite_pack_path, _folders_list, _sprites_list, _palette_lists):
    # Validates all pokemon or all trainers if a folder including their name can be found
    errors = ""
    has_error = False
    def add_error(_error, _is_error = False, _processed = False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += ('\n' if errors else '') + ('' if _processed else 'Error: ' if _is_error else 'Warning: ') + _error

    for object_name in _folders_list:
        object_folder_path = os.path.join(_sprite_pack_path, object_name)
        if not os.path.exists(object_folder_path):
            continue
        found_sprites = { }
        for sprite_name in os.listdir(object_folder_path):
            if not sprite_name.endswith('.png'):
                add_error('File {} in folder {}: Not a sprite and should be removed.'.format(sprite_name, object_name))
                continue
            # Only handle sprites which are awaited for the current object
            matching_sprite_name = next(filter(lambda f: sprite_name.startswith(f), _sprites_list), None)
            if not matching_sprite_name:
                # Allow sprites depicting an awaited palette
                if not next(filter(lambda palette_list: sprite_name[:-4] in _palette_lists[palette_list], _palette_lists), None):
                    add_error('File {} in folder {}: Cannot be linked to a valid internal sprite or palette.'.format(sprite_name, object_name))
                    continue
                matching_sprite_name = sprite_name[:-4]
            sprite_file_name_data = sprite_name[:-4].split('-')[1:]
            extra_sprite_data = sprite_file_name_data or None
            sprite_path = os.path.join(object_folder_path, sprite_name)
            if os.path.exists(sprite_path):
                if found_sprites.get(matching_sprite_name):
                    add_error('File {} in folder {}: Duplicate internal sprite entry with sprite {}.'.format(sprite_name, object_name, found_sprites.get(matching_sprite_name)), True)
                    continue
                found_sprites[matching_sprite_name] = sprite_name
                add_error(*validate_sprite(object_name, matching_sprite_name, extra_sprite_data, sprite_path), True)
    return errors, has_error

def validate_sprite(_object_name, _sprite_name, _extra_data, _path):
    # Validates a given sprite using metrics registered in the sprite requirements table
    errors = ""
    has_error = False
    def add_error(_error, _is_error = False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += ('\n' if errors else '') + ('Error: ' if _is_error else 'Warning: ') + _error

    is_pokemon = _object_name in POKEMON_FOLDERS
    sprite_key = ("pokemon_" if is_pokemon else "trainer_") + _sprite_name
    sprite_requirements = get_sprite_requirements(sprite_key, _object_name)

    sprite_image = Image.open(_path)

    # Palette checks
    if not sprite_image.palette:
        add_error('File {} in folder {}: The sprite is not an indexed PNG file.'.format(_sprite_name, _object_name), True)
    else:
        sprite_palette_colors = sprite_image.getpalette()
        sprite_palette_model = sprite_requirements.get('palette', None)
        # TODO: Support sprites with more/less palette colors if there is no requirement
        sprite_palette_required_size = sprite_requirements.get('palette_size', 16) * sprite_requirements.get('palettes', 1)
        if round(len(sprite_palette_colors) / 3) != sprite_palette_required_size:
            add_error('File {} in folder {}: The sprite\'s palette has {} colors but should have {}.'.format(_sprite_name, _object_name, round(len(sprite_palette_colors) / 3), sprite_palette_required_size), True)
        elif sprite_palette_model:
            matching_palette_model = True
            if is_pokemon and _sprite_name == 'icon':
                # Icons can have several palettes, one must be chosen
                if _extra_data:
                    # Icon palette ID is given in the icon's file name
                    palette_index = int(_extra_data[0])
                    if palette_index < 0 or palette_index > 2:
                        matching_palette_model = False
                        add_error('File {} in folder {}: Icons only have 3 palettes, but you tried using palette #{}.'.format(_sprite_name, _object_name, palette_index + 1), True)
                else:
                    # Icon palette ID must be retrieved from the ROM
                    icon_index_address = get_address_from_address_collection(_object_name, sprite_key + '_index', _object_name)
                    palette_index = int.from_bytes(bytes(current_rom[icon_index_address]), 'little')
                if matching_palette_model:
                    sprite_palette_model = sprite_palette_model[palette_index]
            if matching_palette_model and not is_palette_valid(sprite_palette_colors, sprite_palette_model):
                add_error('File {} in folder {}: The sprite\'s palette does not contain the required colors.'.format(_sprite_name, _object_name), True)

    # Size checks
    sprite_valid_dimensions = []
    if is_overworld_sprite(sprite_key) and _extra_data:
        # If a custom frame size is given for overworld sprites, check that it is valid
        allowed_sizes = ['{}x{}'.format(size['width'], size['height']) for size in VALID_OVERWORLD_SPRITE_SIZES]
        if not _extra_data[0] in allowed_sizes:
            add_error('File {} in folder {}: Invalid custom size {}. The expected sizes are: {}.'.format(_sprite_name, _object_name, _extra_data[0], allowed_sizes), True)
            sprite_valid_dimensions.append({ 'width': 0, 'height': 0 })
        else:
            sizes = _extra_data[0].split('x')
            sprite_valid_dimensions.append({ 'width': int(sizes[0]), 'height': int(sizes[1]) * sprite_requirements.get('frames', 1) })
    else:
        sprite_valid_dimensions.append({ 'width': sprite_requirements.get('width', 0), 'height': sprite_requirements.get('height', 0) * sprite_requirements.get('frames', 0) })
    if sprite_valid_dimensions[0]['width'] > 0 and sprite_valid_dimensions[0]['height'] > 0:
        # Check that the sprite has the awaited size
        if not next(filter(lambda size: size['width'] == sprite_image.width and size['height'] == sprite_image.height, sprite_valid_dimensions), None):
            allowed_sizes = ['{}x{}'.format(size['width'], size['height']) for size in sprite_valid_dimensions]
            current_size = '{}x{}'.format(sprite_image.width, sprite_image.height)
            add_error('File {} in folder {}: Invalid size {}. The expected size{}: {}.'.format(_sprite_name, _object_name, current_size, ' is' if len(allowed_sizes) == 1 else 's are', allowed_sizes[0] if len(allowed_sizes) == 1 else allowed_sizes), True)
    
    return errors, has_error

def is_palette_valid(_palette, _palette_model):
    # Compares a given palette to its model and checks if it is valid or not
    for i in range(min(len(_palette), len(_palette_model))):
        if _palette_model[i] != -1 and _palette[i] != _palette_model[i]:
            return False
    return True

####################
## LZ Compression ##
####################

def truncate_lz_compressed_data(_data, _data_size):
    # Given data, truncates it so that the output contains only LZ-compressed data and nothing more
    data_length = len(_data)
    shift = 4
    while True:
        control_byte = int(_data[shift])
        shift += 1
        for i in range(8):
            if shift >= data_length:
                return _data
            is_compressed = control_byte >= 128
            control_byte = (control_byte << 1) % 256
            if not is_compressed:
                _data_size -= 1
                shift += 1
            else:
                diff = 3 + (int(_data[shift]) >> 4)
                shift += 2
                _data_size -= diff
            if _data_size <= 0:
                return _data[:shift]

def decompress_lz_data(_src:bytes):
    # Performs an LZ decompression of the given data
    src_size = len(_src)
    if src_size < 4:
        raise Exception('Fatal error while decompressing LZ file: size of file is {}'.format(src_size))
    
    dest_size = int.from_bytes(bytes(_src[1:4]), 'little')
    dest = [0 for _ in range(dest_size)]

    src_pos = 4
    dest_pos = 0
    compressed_byte_count = 0

    while True:
        if src_pos >= src_size:
            raise Exception('Fatal error while decompressing LZ file: {}/{}'.format(src_pos, src_size))
        
        # A control byte exists to give info about the 8 following data points
        # Each bit tells whether the next data point is compressed (1) or raw (0) data
        control_byte = int(_src[src_pos])
        src_pos += 1

        for i in range(8):
            if control_byte >= 128:
                # Compressed data: references data previously added to the output file and the number of repetitions
                if src_pos + 1 >= src_size:
                    raise Exception('Fatal error while decompressing LZ file: {}/{}'.format(src_pos, src_size))
                
                compressed_byte_count += 1
                block = int.from_bytes(bytes(_src[src_pos:src_pos+2]), 'big')
                block_size = (block >> 12) + 3
                block_distance = (block & 0xFFF) + 1

                src_pos += 2

                block_pos = dest_pos - block_distance
                if dest_pos + block_size > dest_size:
                    block_size = dest_size - dest_pos
                    print('LZ decompression: Destination buffer overflow.')

                if block_pos < 0:
                    raise Exception('Fatal error while decompressing LZ file: Distance is {} ({} - {}).'.format(block_pos, dest_pos, block_distance))

                for j in range(block_size):
                    dest[dest_pos] = dest[block_pos + j]
                    dest_pos += 1
            else:
                # Raw data: copies the byte as-is to the output
                if src_pos >= src_size or dest_pos >= dest_size:
                    raise Exception('Fatal error while decompressing LZ file: {}/{} and {}/{}.'.format(src_pos, src_size, dest_pos, dest_size))
                dest[dest_pos] = _src[src_pos]
                dest_pos += 1
                src_pos += 1
            
            if dest_pos == dest_size:
                return bytes(dest)
            
            control_byte = (control_byte << 1) % 256

###########################
## Sprite Transformation ##
###########################

def decompress_sprite(_data, _bits_per_pixel):
    # Returns sprite data with each pixel taking one full byte of space
    # Useful for making sprites on-the-fly using Pillow
    pixels_per_bytes = round(8 / _bits_per_pixel)
    data_per_pixel = int(math.pow(2, _bits_per_pixel))

    data_size = len(_data)
    dest_size = data_size * pixels_per_bytes
    dest = [0 for _ in range(dest_size)]

    data_shift = 0
    for byte_index in range(data_size):
        bits = 8
        byte = int(_data[byte_index])
        while bits > 0:
            pixel = byte & (data_per_pixel - 1)
            byte >>= _bits_per_pixel
            bits -= _bits_per_pixel
            dest[data_shift] = pixel
            data_shift += 1
    return bytes(dest)

def dechunk_sprite(_data, _width, _height):
    # Sprites stored in ROMs are bundled in 8x8 pixel chunks
    # This function reverts this behavior, returning raw, non-chunked pixel data
    data_size = _width * _height
    dest = [0 for _ in range(data_size)]

    shift = 0
    block_x = 0
    block_y = 0
    while shift < data_size:
        for y in range(min(_height - (block_y * 8), 8)):
            for x in range(min(_width - (block_x * 8), 8)):
                new_pos = (block_y * 8 + y) * _width + block_x * 8 + x
                dest[new_pos] = int(_data[shift])
                shift += 1
        block_x += 1
        if block_x * 8 >= _width:
            block_x = 0
            block_y += 1
    return bytes(dest)

def spread_palettes_to_sprite_frames(_data, _width, _height, _frames):
    # Adds values to the pixels in the sheet to match values in an extended palette
    # Assumes all palettes have exactly 16 colors
    _data = bytearray(_data)
    data_size = _width * _height
    data_size_per_frame = round(data_size / _frames)
    for frame in range(1, _frames):
        shift = frame * data_size_per_frame
        for pixel in range(data_size_per_frame):
            _data[shift + pixel] |= frame << 4
    return bytes(_data)

#######################
## Utility Functions ##
#######################

def get_pixel_size_and_extension_from_palette_size(_palette_size):
    # Returns the matching byte size of a pixel and file extension for a palette of a given size
    if _palette_size <= 2:   return 1/8, '.1bpp'
    if _palette_size <= 4:   return 1/4, '.2bpp'
    if _palette_size <= 16:  return 1/2, '.4bpp'
    if _palette_size <= 256: return 1,   '.8bpp'
    raise Exception('A sprite with a palette with more than 256 colors cannot be handled by the ROM.')

def get_address_from_address_collection(_object_name, _resource_key, _resource_name):
    # Returns a known address from the ROM's address collection
    if _resource_key.startswith('pokemon_'):
        # Fetches internal Pokemon ID then resource address
        pokemon_id = POKEMON_NAME_TO_ID[_object_name]
        pokemon_internal_id = POKEMON_ID_TO_INTERNAL_ID.get(pokemon_id, pokemon_id)
        data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[_resource_key](data_addresses, pokemon_internal_id)
    else:
        # Fetches named Trainer resource address
        named_key = _object_name.lower() + "_" + _resource_name
        data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[named_key](data_addresses)
    return data_address

def get_overworld_sprite_addresses(_object_name, _resource_name):
    named_key = _object_name.lower() + "_" + _resource_name
    return OVERWORLD_SPRITE_ADDRESSES[named_key](data_addresses)

def handle_overworld_custom_size(_extra_data):
    # Checks if the custom size passed for a given overworld sprite sheet is valid
    sizes = _extra_data[0].split('x')
    if len(sizes) != 2:
        raise Exception('An overworld sprite\'s custom size must be in the format <width>x<height>, with <width> and <height> as numbers.')
    sprite_width = int(sizes[0])
    sprite_height = int(sizes[1])
    valid_sprite_size = next(filter(lambda f: f['width'] == sprite_width and f['height'] == sprite_height, VALID_OVERWORLD_SPRITE_SIZES), None)
    if not valid_sprite_size:
        raise Exception('Overworld sprites cannot have a custom size of {}x{}'.format(sizes[0], sizes[1]))
    return valid_sprite_size

def get_overworld_sprite_data(_data_address, _key):
    # Returns the value of given data from an overworld sprite data object
    value_data = OVERWORLD_SPRITE_OBJECT_INFO.get(_key, None)
    if not value_data:
        raise Exception('Could not get the value {} from an overworld sprite\'s data.'.format(_key))
    starting_address = _data_address + value_data.get('shift')
    end_address = starting_address + value_data.get('size')
    return int.from_bytes(bytes(current_rom[starting_address:end_address]), 'little')

def set_overworld_sprite_data(_data_address, _key, _value:int):
    # Sets the value of given data from an overworld sprite data object
    value_data = OVERWORLD_SPRITE_OBJECT_INFO.get(_key, None)
    if not value_data:
        raise Exception('Could not set the value {} from an overworld sprite\'s data.'.format(_key))
    starting_address = _data_address + value_data.get('shift')
    size = value_data.get('size')
    add_data_to_patch({ "address": starting_address, "length": size, "data": _value.to_bytes(size, 'little')})

def get_sprite_requirements(_sprite_key, _object_name):
    # Returns the requirements of a given sprite for a given pokemon or trainer
    sprite_name = _sprite_key[8:]
    reference_sprite_name = SPRITE_PIXEL_REFERENCE.get(sprite_name, sprite_name)
    _sprite_key = _sprite_key[:8] + reference_sprite_name

    reqs = SPRITES_REQUIREMENTS.get(_sprite_key, {})
    reqs_exceptions_list = SPRITES_REQUIREMENTS_EXCEPTIONS.get(_object_name, {})
    reqs_exceptions = reqs_exceptions_list.get(_sprite_key, {})
    return reqs | reqs_exceptions

def is_complex_sprite(_sprite_key):
    # Checks if a sprite is a complex sprite
    return _sprite_key in COMPLEX_SPRITES_LIST

def is_overworld_sprite(_sprite_key:str):
    # Checks if a sprite is an overworld sprite
    return _sprite_key.startswith('trainer_') and not 'battle' in _sprite_key

def handle_address_collection(_rom, _display_message = False):
    # Picks and stores the right address collection for the given ROM
    global data_addresses
    if zlib.crc32(_rom) == ORIGINAL_ROM_CRC32:
        if _display_message:
            print("Original Emerald ROM detected! Loading its address dictionary...")
        data_addresses = DATA_ADDRESSES_ORIGINAL
    else:
        data_addresses = DATA_ADDRESSES_MOCK_AP
    
    global current_rom
    current_rom = _rom

def five_to_eight_bits_palette(value):
    # Transforms a 5-bit long palette color into an 8-bit long palette color
    return value * 8 + math.floor(value / 4.4)

def flatten_2d(input_list):
   # Flattens a list containing lists into a single unidimensional list
   result = []
   for sublist in input_list:
      for item in sublist:
        result.append(item)
   return result