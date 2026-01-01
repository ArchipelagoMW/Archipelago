from .Rom import Rom
from .Utils import *

# Read a ci4 texture from rom and convert to rgba16
# rom - Rom
# address - address of the ci4 texture in Rom
# length - size of the texture in PIXELS
# palette - 4-bit color palette to use (max of 16 colors)
def ci4_to_rgba16(rom: Rom, address, length, palette):
    newPixels = []
    texture = rom.read_bytes(address, length // 2)
    for byte in texture:
        newPixels.append(palette[(byte & 0xF0) >> 4])
        newPixels.append(palette[byte & 0x0F])
    return newPixels

# Convert an rgba16 texture to ci8
# rgba16_texture - texture to convert
# returns - tuple (ci8_texture, palette)
def rgba16_to_ci8(rgba16_texture):
    ci8_texture = []
    palette = get_colors_from_rgba16(rgba16_texture) # Get all of the colors in the texture
    if len(palette) > 0x100: # Make sure there are <= 256 colors. Could probably do some fancy stuff to convert, but nah.
        raise(Exception("RGB Texture exceeds maximum of 256 colors"))
    if len(palette) < 0x100: #Pad the palette with 0x0001 #Pad the palette with 0001s to take up the full 256 colors
        for i in range(0, 0x100 - len(palette)):
            palette.append(0x0001)

    # Create the new ci8 texture (list of bytes) by locating the index of each color from the rgba16 texture in the color palette.
    for pixel in rgba16_texture:
        if pixel in palette:
            ci8_texture.append(palette.index(pixel))
    return (ci8_texture, palette)

# Load a palette (essentially just an rgba16 texture) from rom
def load_palette(rom: Rom, address, length):
    palette = []
    for i in range(0, length):
        palette.append(rom.read_int16(address + 2 * i))
    return palette

# Get a list of unique colors (palette) from an rgba16 texture
def get_colors_from_rgba16(rgba16_texture):
    colors = []
    for pixel in rgba16_texture:
        if pixel not in colors:
            colors.append(pixel)
    return colors

# Apply a patch to a rgba16 texture. The patch texture is exclusive or'd with the original to produce the result
# rgba16_texture - Original texture
# rgba16_patch - Patch texture. If this parameter is not supplied, this function will simply return the original texture.
# returns - new texture = texture xor patch
def apply_rgba16_patch(rgba16_texture, rgba16_patch):
    if rgba16_patch is not None and (len(rgba16_texture) != len(rgba16_patch)):
        raise(Exception("OG Texture and Patch not the same length!"))

    new_texture = []
    if not rgba16_patch:
        for i in range(0, len(rgba16_texture)):
            new_texture.append(rgba16_texture[i])
        return new_texture
    for i in range(0, len(rgba16_texture)):
        new_texture.append(rgba16_texture[i] ^ rgba16_patch[i])
    return new_texture

# Save a rgba16 texture to a file
def save_rgba16_texture(rgba16_texture, fileStr):
    file = open(fileStr, 'wb')
    bytes = bytearray()
    for pixel in rgba16_texture:
        bytes.extend(pixel.to_bytes(2, 'big'))
    file.write(bytes)
    file.close()

# Save a ci8 texture to a file
def save_ci8_texture(ci8_texture, fileStr):
    file = open(fileStr, 'wb')
    bytes = bytearray()
    for pixel in ci8_texture:
        bytes.extend(pixel.to_bytes(1, 'big'))
    file.write(bytes)
    file.close()

# Read an rgba16 texture from ROM
# rom - Rom object to load the texture from
# base_texture_address - Address of the rbga16 texture in ROM
# size - Size of the texture in PIXELS
# returns - list of ints representing each 16-bit pixel
def load_rgba16_texture_from_rom(rom: Rom, base_texture_address, size):
    texture = []
    for i in range(0, size):
        texture.append(int.from_bytes(rom.read_bytes(base_texture_address + 2 * i, 2), 'big'))
    return texture

# Load an rgba16 texture from a binary file.
# fileStr - path to the file
# size - number of 16-bit pixels in the texture.
def load_rgba16_texture(fileStr, size):
    texture = []
    file = open(fileStr, 'rb')
    for i in range(0, size):
        texture.append(int.from_bytes(file.read(2), 'big'))

    file.close()
    return(texture)

# Create an new rgba16 texture byte array from a rgba16 binary file. Use this if you want to create complete new textures using no copyrighted content (or for testing).
# rom - Unused set to None
# base_texture_address - Unusued set to None
# base_palette_address - Unusued set to None
# size - Size of the texture in PIXELS
# patchfile - File containing the texture to load
# returns - bytearray containing the new texture
def rgba16_from_file(rom: Rom, base_texture_address, base_palette_address, size, patchfile):
    new_texture = load_rgba16_texture(patchfile, size)
    bytes = bytearray()
    for pixel in new_texture:
        bytes.extend(int.to_bytes(pixel, 2, 'big'))
    return bytes

# Create a new rgba16 texture from a original rgba16 texture and a rgba16 patch file
# rom - Rom object to load the original texture from
# base_texture_address - Address of the original rbga16 texture in ROM
# base_palette_address - Unused. Set to None (this is only used for CI4 style textures)
# size - Size of the texture in PIXELS
# patchfile - file path of a rgba16 binary texture to patch
# returns - bytearray of the new texture
def rgba16_patch(rom: Rom, base_texture_address, base_palette_address, size, patchfile):
    base_texture_rgba16 = load_rgba16_texture_from_rom(rom, base_texture_address, size)
    patch_rgba16 = None
    if patchfile:
        patch_rgba16 = load_rgba16_texture(patchfile, size)
    new_texture_rgba16 = apply_rgba16_patch(base_texture_rgba16, patch_rgba16)
    bytes = bytearray()
    for pixel in new_texture_rgba16:
        bytes.extend(int.to_bytes(pixel, 2, 'big'))
    return bytes

# Create a new ci8 texture from a ci4 texture/palette and a rgba16 patch file
# rom - Rom object to load the original textures from
# base_texture_address - Address of the original ci4 texture in ROM
# base_palette_address - Address of the ci4 palette in ROM
# size - Size of the texture in PIXELS
# patchfile - file path of a rgba16 binary texture to patch
# returns - bytearray of the new texture
def ci4_rgba16patch_to_ci8(rom, base_texture_address, base_palette_address, size, patchfile):
    palette = load_palette(rom, base_palette_address, 16) # load the original palette from rom
    base_texture_rgba16 = ci4_to_rgba16(rom, base_texture_address, size, palette) # load the original texture from rom and convert to ci8
    patch_rgba16 = None
    if patchfile:
        patch_rgba16 = load_rgba16_texture(patchfile, size)
    new_texture_rgba16 = apply_rgba16_patch(base_texture_rgba16, patch_rgba16)
    ci8_texture, ci8_palette = rgba16_to_ci8(new_texture_rgba16)
    # merge the palette and the texture
    bytes = bytearray()
    for pixel in ci8_palette:
        bytes.extend(int.to_bytes(pixel, 2, 'big'))
    for pixel in ci8_texture:
        bytes.extend(int.to_bytes(pixel, 1, 'big'))
    return bytes

# Function to create rgba16 texture patches for crates
def build_crate_ci8_patches():
    # load crate textures from rom
    object_kibako2_addr = 0x018B6000
    SIZE_CI4_32X128 = 4096
    rom = Rom("ZOOTDEC.z64")
    crate_palette = load_palette(rom, object_kibako2_addr + 0x00, 16)
    crate_texture_rgba16 = ci4_to_rgba16(rom, object_kibako2_addr + 0x20, SIZE_CI4_32X128, crate_palette)

    # load new textures
    crate_texture_gold_rgba16 = load_rgba16_texture('crate_gold_rgba16.bin', 0x1000)
    crate_texture_skull_rgba16 = load_rgba16_texture('crate_skull_rgba16.bin', 0x1000)
    crate_texture_key_rgba16 = load_rgba16_texture('crate_key_rgba16.bin', 0x1000)
    crate_texture_bosskey_rgba16 = load_rgba16_texture('crate_bosskey_rgba16.bin', 0x1000)

    # create patches
    gold_patch = apply_rgba16_patch(crate_texture_rgba16, crate_texture_gold_rgba16)
    key_patch = apply_rgba16_patch(crate_texture_rgba16, crate_texture_key_rgba16)
    skull_patch = apply_rgba16_patch(crate_texture_rgba16, crate_texture_skull_rgba16)
    bosskey_patch = apply_rgba16_patch(crate_texture_rgba16, crate_texture_bosskey_rgba16)

    # save patches
    save_rgba16_texture(gold_patch, 'crate_gold_rgba16_patch.bin')
    save_rgba16_texture(key_patch, 'crate_key_rgba16_patch.bin')
    save_rgba16_texture(skull_patch, 'crate_skull_rgba16_patch.bin')
    save_rgba16_texture(bosskey_patch, 'crate_bosskey_rgba16_patch.bin')

    # create ci8s
    default_ci8, default_palette = rgba16_to_ci8(crate_texture_rgba16)
    gold_ci8, gold_palette = rgba16_to_ci8(crate_texture_gold_rgba16)
    key_ci8, key_palette = rgba16_to_ci8(crate_texture_key_rgba16)
    skull_ci8, skull_palette = rgba16_to_ci8(crate_texture_skull_rgba16)
    bosskey_ci8, bosskey_palette = rgba16_to_ci8(crate_texture_bosskey_rgba16)

    # save ci8 textures
    save_ci8_texture(default_ci8, 'crate_default_ci8.bin')
    save_ci8_texture(gold_ci8, 'crate_gold_ci8.bin')
    save_ci8_texture(key_ci8, 'crate_key_ci8.bin')
    save_ci8_texture(skull_ci8, 'crate_skull_ci8.bin')
    save_ci8_texture(bosskey_ci8, 'crate_bosskey_ci8.bin')

    # save palettes
    save_rgba16_texture(default_palette, 'crate_default_palette.bin')
    save_rgba16_texture(gold_palette, 'crate_gold_palette.bin')
    save_rgba16_texture(key_palette, 'crate_key_palette.bin')
    save_rgba16_texture(skull_palette, 'crate_skull_palette.bin')
    save_rgba16_texture(bosskey_palette, 'crate_bosskey_palette.bin')

    crate_textures = [
        (5, 'texture_crate_default', 0x18B6000 + 0x20, 0x018B6000, 4096, ci4_rgba16patch_to_ci8, None),
        (6, 'texture_crate_gold'   , 0x18B6000 + 0x20, 0x018B6000, 4096, ci4_rgba16patch_to_ci8, 'crate_gold_rgba16_patch.bin'),
        (7, 'texture_crate_key', 0x18B6000 + 0x20, 0x018B6000, 4096, ci4_rgba16patch_to_ci8, 'crate_key_rgba16_patch.bin'),
        (8, 'texture_crate_skull',  0x18B6000 + 0x20, 0x018B6000, 4096, ci4_rgba16patch_to_ci8, 'crate_skull_rgba16_patch.bin'),
        (9, 'texture_crate_bosskey', 0x18B6000 + 0x20, 0x018B6000, 4096, ci4_rgba16patch_to_ci8, 'crate_bosskey_rgba16_patch.bin'),
    ]

    for texture_id, texture_name, rom_address_base, rom_address_palette, size,func, patchfile in crate_textures:
        texture = func(rom, rom_address_base, rom_address_palette, size, patchfile)
        file = open(texture_name, 'wb')
        file.write(texture)
        file.close()
        print(texture)

# Function to create rgba16 texture patches for pots.
def build_pot_patches():
    # load pot textures from rom
    object_tsubo_side_addr = 0x01738000
    SIZE_32X64 = 2048
    rom = Rom("ZOOTDEC.z64")

    pot_default_rgba16 = load_rgba16_texture_from_rom(rom, object_tsubo_side_addr, SIZE_32X64)
    pot_gold_rgba16 = load_rgba16_texture('pot_gold_rgba16.bin', SIZE_32X64)
    pot_key_rgba16 = load_rgba16_texture('pot_key_rgba16.bin', SIZE_32X64)
    pot_skull_rgba16 = load_rgba16_texture('pot_skull_rgba16.bin', SIZE_32X64)
    pot_bosskey_rgba16 = load_rgba16_texture('pot_bosskey_rgba16.bin', SIZE_32X64)

    # create patches
    gold_patch = apply_rgba16_patch(pot_default_rgba16, pot_gold_rgba16)
    key_patch = apply_rgba16_patch(pot_default_rgba16, pot_key_rgba16)
    skull_patch = apply_rgba16_patch(pot_default_rgba16, pot_skull_rgba16)
    bosskey_patch = apply_rgba16_patch(pot_default_rgba16, pot_bosskey_rgba16)

    # save patches
    save_rgba16_texture(gold_patch, 'pot_gold_rgba16_patch.bin')
    save_rgba16_texture(key_patch, 'pot_key_rgba16_patch.bin')
    save_rgba16_texture(skull_patch, 'pot_skull_rgba16_patch.bin')
    save_rgba16_texture(bosskey_patch, 'pot_bosskey_rgba16_patch.bin')

def build_smallcrate_patches():
    # load small crate texture from rom
    object_kibako_texture_addr = 0xF7ECA0

    SIZE_32X64 = 2048
    rom = Rom("ZOOTDEC.z64")

    # Load textures
    smallcrate_default_rgba16 = load_rgba16_texture_from_rom(rom, object_kibako_texture_addr, SIZE_32X64)
    smallcrate_gold_rgba16 = load_rgba16_texture('smallcrate_gold_rgba16.bin', SIZE_32X64)
    smallcrate_key_rgba16 = load_rgba16_texture('smallcrate_key_rgba16.bin', SIZE_32X64)
    smallcrate_skull_rgba16 = load_rgba16_texture('smallcrate_skull_rgba16.bin', SIZE_32X64)
    smallcrate_bosskey_rgba16 = load_rgba16_texture('smallcrate_bosskey_rgba16.bin', SIZE_32X64)

    save_rgba16_texture(smallcrate_default_rgba16, 'smallcrate_default_rgba16.bin')
    # Create patches
    gold_patch = apply_rgba16_patch(smallcrate_default_rgba16, smallcrate_gold_rgba16)
    key_patch = apply_rgba16_patch(smallcrate_default_rgba16, smallcrate_key_rgba16)
    skull_patch = apply_rgba16_patch(smallcrate_default_rgba16, smallcrate_skull_rgba16)
    bosskey_patch = apply_rgba16_patch(smallcrate_default_rgba16, smallcrate_bosskey_rgba16)

    # save patches
    save_rgba16_texture(gold_patch, 'smallcrate_gold_rgba16_patch.bin')
    save_rgba16_texture(key_patch, 'smallcrate_key_rgba16_patch.bin')
    save_rgba16_texture(skull_patch, 'smallcrate_skull_rgba16_patch.bin')
    save_rgba16_texture(bosskey_patch, 'smallcrate_bosskey_rgba16_patch.bin')


#build_crate_ci8_patches()
#build_pot_patches()
#build_smallcrate_patches()
