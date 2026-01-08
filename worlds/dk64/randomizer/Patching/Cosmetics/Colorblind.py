"""All code associated with colorblind mode."""

import gzip
from randomizer.Settings import ColorblindMode
from randomizer.Patching.Library.Image import (
    getRGBFromHash,
    TextureFormat,
    maskImage,
    getImageFile,
    getImageFromAddress,
    getKongItemColor,
    writeColorImageToROM,
    ExtraTextures,
    getBonusSkinOffset,
    rgba32to5551,
)
from randomizer.Patching.Library.Generic import Overlay
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames, getRawFile, writeRawFile
from randomizer.Patching.Library.ASM import getROMAddress, populateOverlayOffsets
from randomizer.Patching.Patcher import ROM
from randomizer.Enums.Kongs import Kongs
from PIL import ImageEnhance, Image


def changeVertexColor(num_data: list[int], offset: int, new_color: list[int]) -> list[int]:
    """Change the vertex color based on the luminance of the original."""
    total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
    channel_light = int(total_light / 3)
    for i in range(3):
        num_data[offset + i] = int(channel_light * (new_color[i] / 255))
    return num_data


def writeKasplatHairColorToROM(color: str, table_index: TableNames, file_index: int, format: str, ROM_COPY: ROM):
    """Write color to ROM for kasplats."""
    file_start = getPointerLocation(table_index, file_index)
    mask = getRGBFromHash(color)
    if format == TextureFormat.RGBA32:
        color_lst = mask.copy()
        color_lst.append(255)  # Alpha
        null_color = [0] * 4
    else:
        color_lst = rgba32to5551(mask)
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            bytes_array.extend(color_lst)
    for i in range(18):
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == TableNames.TexturesGeometry:
        data = gzip.compress(data, compresslevel=9)
    ROM_COPY.seek(file_start)
    ROM_COPY.writeBytes(data)


def writeWhiteKasplatHairColorToROM(color1: str, color2: str, table_index: TableNames, file_index: int, format: str, ROM_COPY: ROM):
    """Write color to ROM for white kasplats, giving them a black-white block pattern."""
    file_start = getPointerLocation(table_index, file_index)
    mask = getRGBFromHash(color1)
    mask2 = getRGBFromHash(color2)
    if format == TextureFormat.RGBA32:
        color_lst_0 = mask.copy()
        color_lst_0.append(255)
        color_lst_1 = mask2.copy()
        color_lst_1.append(255)
        null_color = [0] * 4
    else:
        color_lst_0 = rgba32to5551(mask)
        color_lst_1 = rgba32to5551(mask2)
        null_color = [0] * 2
    bytes_array = []
    for y in range(42):
        for x in range(32):
            if (int(y / 7) + int(x / 8)) % 2 == 0:
                bytes_array.extend(color_lst_0)
            else:
                bytes_array.extend(color_lst_1)
    for i in range(18):
        bytes_array.extend(color_lst_0)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        bytes_array.extend(color_lst_0)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM_COPY.seek(file_start)
    ROM_COPY.writeBytes(data)


def writeKlaptrapSkinColorToROM(color_index, table_index, file_index, format: str, mode: ColorblindMode, ROM_COPY: ROM):
    """Write color to ROM for klaptraps."""
    im_f = getImageFile(ROM_COPY, table_index, file_index, True, 32, 43, format)
    im_f = maskImage(im_f, color_index, 0, (color_index != 3), mode)
    pix = im_f.load()
    file_start = getPointerLocation(table_index, file_index)
    if format == TextureFormat.RGBA32:
        null_color = [0] * 4
    else:
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            color_lst = calculateKlaptrapPixel(list(pix[x, y]), format)
            bytes_array.extend(color_lst)
    for i in range(18):
        color_lst = calculateKlaptrapPixel(list(pix[i, 42]), format)
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        color_lst = calculateKlaptrapPixel(list(pix[(22 + i), 42]), format)
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM_COPY.seek(file_start)
    ROM_COPY.writeBytes(data)


def writeSpecialKlaptrapTextureToROM(color_index, table_index, file_index, format: str, pixels_to_ignore: list, mode: ColorblindMode, ROM_COPY: ROM):
    """Write color to ROM for klaptraps special texture(s)."""
    im_f = getImageFile(ROM_COPY, table_index, file_index, True, 32, 43, format)
    pix_original = im_f.load()
    pixels_original = []
    for x in range(32):
        pixels_original.append([])
        for y in range(43):
            pixels_original[x].append(list(pix_original[x, y]).copy())
    im_f_masked = maskImage(im_f, color_index, 0, (color_index != 3), mode)
    pix = im_f_masked.load()
    file_start = getPointerLocation(table_index, file_index)
    if format == TextureFormat.RGBA32:
        null_color = [0] * 4
    else:
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            if [x, y] not in pixels_to_ignore:
                color_lst = calculateKlaptrapPixel(list(pix[x, y]), format)
            else:
                color_lst = calculateKlaptrapPixel(list(pixels_original[x][y]), format)
            bytes_array.extend(color_lst)
    for i in range(18):
        if [i, 42] not in pixels_to_ignore:
            color_lst = calculateKlaptrapPixel(list(pix[i, 42]), format)
        else:
            color_lst = calculateKlaptrapPixel(list(pixels_original[i][42]), format)
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        if [(22 + i), 42] not in pixels_to_ignore:
            color_lst = calculateKlaptrapPixel(list(pix[(22 + i), 42]), format)
        else:
            color_lst = calculateKlaptrapPixel(list(pixels_original[(22 + i)][42]), format)
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM_COPY.seek(file_start)
    ROM_COPY.writeBytes(data)


def calculateKlaptrapPixel(mask: list, format: str):
    """Calculate the new color for the given pixel."""
    if format == TextureFormat.RGBA32:
        return mask + [255]
    return rgba32to5551(mask)


def maskBlueprintImage(im_f, base_index, mode: ColorblindMode):
    """Apply RGB mask to blueprint image."""
    w, h = im_f.size
    im_f_original = im_f
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, 0, w, h))
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    pix2 = im_f_original.load()
    mask = getKongItemColor(mode, base_index, True)
    if max(mask[0], max(mask[1], mask[2])) < 39:
        for channel in range(3):
            mask[channel] = max(39, mask[channel])  # Too black is bad for these items
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base2 = list(pix2[x, y])
            if base[3] > 0:
                # Filter out the wooden frame
                # brown is orange, is red and (red+green), is very little blue
                # but, if the color is light, we can't rely on the blue value alone.
                if base2[2] > 20 and (base2[2] > base2[1] or base2[1] - base2[2] < 20):
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                    pix[x, y] = (base[0], base[1], base[2], base[3])
                else:
                    pix[x, y] = (base2[0], base2[1], base2[2], base2[3])
    return im_f


def maskLaserImage(im_f, base_index, mode: ColorblindMode):
    """Apply RGB mask to laser texture."""
    w, h = im_f.size
    im_f_original = im_f
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, 0, w, h))
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    pix2 = im_f_original.load()
    mask = getKongItemColor(mode, base_index, True)
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base2 = list(pix2[x, y])
            if base[3] > 0:
                # Filter out the white center of the laser
                if min(base2[0], min(base2[1], base2[2])) <= 210:
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                    pix[x, y] = (base[0], base[1], base[2], base[3])
                else:
                    pix[x, y] = (base2[0], base2[1], base2[2], base2[3])
    return im_f


def maskPotionImage(im_f, primary_color, secondary_color=None):
    """Apply RGB mask to DK arcade potion reward preview texture."""
    w, h = im_f.size
    pix = im_f.load()
    mask = getRGBFromHash(primary_color)
    if secondary_color is not None:
        mask2 = secondary_color
    for channel in range(3):
        mask[channel] = max(1, mask[channel])
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            # Filter out transparent pixels and the cork
            if base[3] > 0 and y > 2 and [x, y] not in [[9, 4], [10, 4]]:
                # Filter out the bottle's contents
                if base[0] == base[1] and base[1] == base[2]:
                    if secondary_color is not None:
                        # Color the bottle itself
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
                else:
                    # Color the bottle's contents
                    average_light = int((base[0] + base[1] + base[2]) / 3)
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (average_light / 255))
            pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


WRINKLY_DOOR_COLOR_1_OFFSETS = [
    1548,
    1580,
    1612,
    1644,
    1676,
    1708,
    1756,
    1788,
    1804,
    1820,
    1836,
    1852,
    1868,
    1884,
    1900,
    1916,
    1932,
    1948,
    1964,
    1980,
    1996,
    2012,
    2028,
    2044,
    2076,
    2108,
    2124,
    2156,
    2188,
    2220,
    2252,
    2284,
    2316,
    2348,
    2380,
    2396,
    2412,
    2428,
    2444,
    2476,
    2508,
    2540,
    2572,
    2604,
    2636,
    2652,
    2668,
    2684,
    2700,
    2716,
    2732,
    2748,
    2764,
    2780,
    2796,
    2812,
    2828,
    2860,
    2892,
    2924,
    2956,
    2988,
    3020,
    3052,
]
WRINKLY_DOOR_COLOR_2_OFFSETS = [1564, 1596, 1628, 1660, 1692, 1724, 1740, 1772, 2332, 2364, 2460, 2492, 2524, 2556, 2588, 2620]


def recolorWrinklyDoors(mode: ColorblindMode, ROM_COPY: ROM):
    """Recolor the Wrinkly hint door doorframes for colorblind mode."""
    file = [0xF0, 0xF2, 0xEF, 0x67, 0xF1]
    for kong in range(5):
        file_index = file[kong]
        data = getRawFile(ROM_COPY, TableNames.ModelTwoGeometry, file_index, True)
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them (list extensions to mitigate the linter's "artistic freedom" putting 1 value per line)
        color_str = getKongItemColor(mode, kong)
        new_color1 = getRGBFromHash(color_str)
        new_color2 = getRGBFromHash(color_str)
        if kong == 0:
            for channel in range(3):
                new_color2[channel] = max(80, new_color1[channel])  # Too black is bad, because anything times 0 is 0

        # Recolor the doorframe
        for offset in WRINKLY_DOOR_COLOR_1_OFFSETS:
            for i in range(3):
                num_data[offset + i] = new_color1[i]
        for offset in WRINKLY_DOOR_COLOR_2_OFFSETS:
            for i in range(3):
                num_data[offset + i] = new_color2[i]

        data = bytearray(num_data)  # convert num_data back to binary string
        writeRawFile(TableNames.ModelTwoGeometry, file_index, True, data, ROM_COPY)


def recolorKRoolShipSwitch(color: tuple, ROM_COPY: ROM):
    """Recolors the simian slam switch that is part of K. Rool's ship in galleon."""
    addresses = (
        0x4C34,
        0x4C44,
        0x4C54,
        0x4C64,
        0x4C74,
        0x4C84,
    )
    data = bytearray(getRawFile(ROM_COPY, TableNames.ModelTwoGeometry, 305, True))
    for addr in addresses:
        for x in range(3):
            data[addr + x] = color[x]
    new_tex = [
        0xE7000000,
        0x00000000,
        0xE200001C,
        0x0C192038,
        0xE3000A01,
        0x00100000,
        0xE3000F00,
        0x00000000,
        0xE7000000,
        0x00000000,
        0xFC127E03,
        0xFFFFF9F8,
        0xFD900000,
        0x00000BAF,
        0xF5900000,
        0x07080200,
        0xE6000000,
        0x00000000,
        0xF3000000,
        0x077FF100,
        0xE7000000,
        0x00000000,
        0xF5881000,
        0x00080200,
        0xF2000000,
        0x000FC0FC,
    ]
    for x in range(8):
        data[0x1AD8 + x] = 0
    for xi, x in enumerate(new_tex):
        for y in range(4):
            offset = (xi * 4) + y
            shift = 24 - (8 * y)
            data[0x1AE8 + offset] = (x >> shift) & 0xFF
    for x in range(40):
        data[0x1B58 + x] = 0
    writeRawFile(TableNames.ModelTwoGeometry, 305, True, data, ROM_COPY)


def recolorSlamSwitches(galleon_switch_value, ROM_COPY: ROM, mode: ColorblindMode):
    """Recolor the Simian Slam switches for colorblind mode."""
    file = [0x94, 0x93, 0x95, 0x96, 0xB8, 0x16C, 0x16B, 0x16D, 0x16E, 0x16A, 0x167, 0x166, 0x168, 0x169, 0x165]
    written_galleon_ship = False
    for switch_index, file_index in enumerate(file):
        data = getRawFile(ROM_COPY, TableNames.ModelTwoGeometry, file_index, True)
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color_offsets = [1828, 1844, 1860, 1876, 1892, 1908]
        new_color1 = getKongItemColor(mode, Kongs.chunky, True)
        new_color2 = getKongItemColor(mode, Kongs.lanky, True)
        new_color3 = getKongItemColor(mode, Kongs.diddy, True)

        for offset in color_offsets:
            # Green switches
            if switch_index < 5:
                for i in range(3):
                    num_data[offset + i] = new_color1[i]
            # Blue switches
            elif switch_index < 10:
                for i in range(3):
                    num_data[offset + i] = new_color2[i]
            # Red switches
            else:
                for i in range(3):
                    num_data[offset + i] = new_color3[i]

        data = bytearray(num_data)  # convert num_data back to binary string
        writeRawFile(TableNames.ModelTwoGeometry, file_index, True, data, ROM_COPY)
        if not written_galleon_ship:
            galleon_switch_color = new_color1.copy()
            if galleon_switch_value is not None:
                if galleon_switch_value != 1:
                    galleon_switch_color = new_color3.copy()
                    if galleon_switch_value == 2:
                        galleon_switch_color = new_color2.copy()
            recolorKRoolShipSwitch(galleon_switch_color, ROM_COPY)
            written_galleon_ship = True


def recolorBlueprintModelTwo(mode: ColorblindMode, ROM_COPY: ROM):
    """Recolor the Blueprint Model2 items for colorblind mode."""
    file = [0xDE, 0xE0, 0xE1, 0xDD, 0xDF]
    for kong, file_index in enumerate(file):
        data = getRawFile(ROM_COPY, TableNames.ModelTwoGeometry, file_index, True)
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color1_offsets = [0x52C, 0x54C, 0x57C, 0x58C, 0x5AC, 0x5CC, 0x5FC, 0x61C]
        color2_offsets = [0x53C, 0x55C, 0x5EC, 0x60C]
        color3_offsets = [0x56C, 0x59C, 0x5BC, 0x5DC]
        color_offsets = color1_offsets + color2_offsets + color3_offsets
        new_color = getKongItemColor(mode, kong, True)
        if kong == 0:
            for channel in range(3):
                new_color[channel] = max(39, new_color[channel])  # Too black is bad, because anything times 0 is 0

        # Recolor the model2 item
        for offset in color_offsets:
            num_data = changeVertexColor(num_data, offset, new_color)

        data = bytearray(num_data)  # convert num_data back to binary string
        writeRawFile(TableNames.ModelTwoGeometry, file_index, True, data, ROM_COPY)


def maskImageRotatingRoomTile(im_f, im_mask, paste_coords, image_color_index, tile_side, mode: ColorblindMode):
    """Apply RGB mask to image of a Rotating Room Memory Tile."""
    w, h = im_f.size
    im_original = im_f
    pix_original = im_original.load()
    pixels_original = []
    for x in range(w):
        pixels_original.append([])
        for y in range(h):
            pixels_original[x].append(list(pix_original[x, y]).copy())
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    brightener = ImageEnhance.Brightness(im_f)
    im_f = brightener.enhance(2)
    pix = im_f.load()
    pix_mask = im_mask.load()
    w2, h2 = im_mask.size
    mask_coords = []
    for x in range(w2):
        for y in range(h2):
            coord = list(pix_mask[x, y])
            if coord[3] > 0:
                mask_coords.append([(x + paste_coords[0]), (y + paste_coords[1])])
    if image_color_index < 5:
        mask = getKongItemColor(mode, image_color_index, True)
        for channel in range(3):
            mask[channel] = max(39, mask[channel])  # Too dark looks bad
    else:
        mask = getKongItemColor(mode, Kongs.lanky, True)
    mask2 = [0x00, 0x00, 0x00]
    if image_color_index == 0:
        mask2 = [0xFF, 0xFF, 0xFF]
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base_original = list(pixels_original[x][y])
            if [x, y] not in mask_coords:
                if image_color_index in [1, 2, 4]:  # Diddy, Lanky and Chunky don't get any special features
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                elif image_color_index in [0, 3]:  # Donkey and Tiny get a diamond-shape frame
                    side = w
                    if tile_side == 1:
                        side = 0
                    if abs(abs(side - x) - y) < 2 or abs(abs(side - x) - abs(h - y)) < 2:
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
                    else:
                        for channel in range(3):
                            base[channel] = int(mask[channel] * (base[channel] / 255))
                else:  # Golden Banana gets a block-pattern
                    if (int(x / 8) + int(y / 8)) % 2 == 0:
                        for channel in range(3):
                            base[channel] = int(mask[channel] * (base[channel] / 255))
                    else:
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
            else:
                for channel in range(3):
                    base[channel] = base_original[channel]
            pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def recolorRotatingRoomTiles(mode: ColorblindMode, ROM_COPY: ROM):
    """Determine how to recolor the tiles rom the memory game in Donkey's Rotating Room in Caves."""
    question_mark_tiles = [900, 901, 892, 893, 896, 897, 890, 891, 898, 899, 894, 895]
    face_tiles = [
        874,
        878,
        875,
        879,
        876,
        886,
        877,
        885,
        880,
        887,
        881,
        888,
        870,
        872,
        871,
        873,
        866,
        882,
        867,
        883,
        868,
        889,
        869,
        884,
    ]
    question_mark_tile_masks = [508, 509]
    face_tile_masks = [636, 635, 633, 634, 631, 632, 630, 629, 627, 628, 5478, 5478]
    question_mark_resize = [17, 37]
    face_resize = [[32, 64], [32, 64], [32, 64], [32, 64], [32, 64], [71, 66]]
    question_mark_offsets = [[16, 14], [0, 14]]
    face_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [-5, -1], [-38, -1]]

    for tile in range(len(question_mark_tiles)):
        tile_image = getImageFile(ROM_COPY, 7, question_mark_tiles[tile], False, 32, 64, TextureFormat.RGBA5551)
        mask = getImageFile(ROM_COPY, 7, question_mark_tile_masks[(tile % 2)], False, 32, 64, TextureFormat.RGBA5551)
        resize = question_mark_resize
        mask = mask.resize((resize[0], resize[1]))
        masked_tile = maskImageRotatingRoomTile(tile_image, mask, question_mark_offsets[(tile % 2)], int(tile / 2), (tile % 2), mode)
        writeColorImageToROM(masked_tile, 7, question_mark_tiles[tile], 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
    for tile_index, tile in enumerate(face_tiles):
        face_index = int(tile_index / 4)
        if face_index < 5:
            width = 32
            height = 64
        else:
            width = 44
            height = 44
        mask = getImageFile(ROM_COPY, 25, face_tile_masks[int(tile_index / 2)], True, width, height, TextureFormat.RGBA5551)
        resize = face_resize[face_index]
        mask = mask.resize((resize[0], resize[1]))
        tile_image = getImageFile(ROM_COPY, 7, tile, False, 32, 64, TextureFormat.RGBA5551)
        masked_tile = maskImageRotatingRoomTile(tile_image, mask, face_offsets[int(tile_index / 2)], face_index, (int(tile_index / 2) % 2), mode)
        writeColorImageToROM(masked_tile, 7, tile, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)


def recolorBells(ROM_COPY: ROM):
    """Recolor the Chunky Minecart bells for colorblind mode (prot/deut)."""
    data = getRawFile(ROM_COPY, TableNames.ModelTwoGeometry, 693, True)
    num_data = []  # data, but represented as nums rather than b strings
    for d in data:
        num_data.append(d)
    # Figure out which colors to use and where to put them
    color1_offsets = [0x214, 0x244, 0x264, 0x274, 0x284]
    color2_offsets = [0x224, 0x234, 0x254]
    new_color1 = [0x00, 0x66, 0xFF]
    new_color2 = [0x00, 0x00, 0xFF]

    # Recolor the bell
    for offset in color1_offsets:
        for i in range(3):
            num_data[offset + i] = new_color1[i]
    for offset in color2_offsets:
        for i in range(3):
            num_data[offset + i] = new_color2[i]

    data = bytearray(num_data)  # convert num_data back to binary string
    writeRawFile(TableNames.ModelTwoGeometry, 693, True, data, ROM_COPY)


def recolorKlaptraps(mode, ROM_COPY: ROM):
    """Recolor the klaptrap models for colorblind mode."""
    green_files = [0xF31, 0xF32, 0xF33, 0xF35, 0xF37, 0xF39]  # 0xF2F collar? 0xF30 feet?
    red_files = [0xF44, 0xF45, 0xF46, 0xF47, 0xF48, 0xF49]  # , 0xF42 collar? 0xF43 feet?
    purple_files = [0xF3C, 0xF3D, 0xF3E, 0xF3F, 0xF40, 0xF41]  # 0xF3B feet?, 0xF3A collar?

    # Regular textures
    for file in range(6):
        writeKlaptrapSkinColorToROM(4, 25, green_files[file], TextureFormat.RGBA5551, mode, ROM_COPY)
        writeKlaptrapSkinColorToROM(1, 25, red_files[file], TextureFormat.RGBA5551, mode, ROM_COPY)
        writeKlaptrapSkinColorToROM(3, 25, purple_files[file], TextureFormat.RGBA5551, mode, ROM_COPY)

    belly_pixels_to_ignore = []
    for x in range(32):
        for y in range(43):
            if y < 29 or (y > 31 and y < 39) or y == 40 or y == 42:
                belly_pixels_to_ignore.append([x, y])
            elif (y == 39 and x < 16) or (y == 41 and x < 24):
                belly_pixels_to_ignore.append([x, y])

    # Special texture that requires only partial recoloring, in this case file 0xF38 which is the belly, and only the few green pixels
    writeSpecialKlaptrapTextureToROM(4, 25, 0xF38, TextureFormat.RGBA5551, belly_pixels_to_ignore, mode, ROM_COPY)


def getPotionColor(colorblind_mode: ColorblindMode, kong: Kongs) -> list[int]:
    """Get the potion color associated with a kong."""
    diddy_color = getKongItemColor(colorblind_mode, Kongs.diddy, True)
    chunky_color = getKongItemColor(colorblind_mode, Kongs.chunky, True)
    secondary_color = [diddy_color, None, chunky_color, diddy_color, None, None]
    if colorblind_mode == ColorblindMode.trit:
        secondary_color[Kongs.donkey] = chunky_color
        secondary_color[Kongs.lanky] = None
    if kong < 5:
        new_color = getKongItemColor(colorblind_mode, kong, True)
    else:
        new_color = [0xFF, 0xFF, 0xFF]
    if secondary_color[kong] is not None:
        if kong == Kongs.tiny:
            return secondary_color[kong].copy()
        elif kong == Kongs.donkey:
            return [int(x / 8) for x in secondary_color[kong]]
        else:
            return [int(x / 4) for x in secondary_color[kong]]
    return new_color.copy()


def recolorPotions(settings, colorblind_mode: ColorblindMode, ROM_COPY: ROM):
    """Overwrite potion colors."""
    # Actor:
    file = [[0xED, 0xEE, 0xEF, 0xF0, 0xF1, 0xF2], [0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA]]
    for type in range(2):
        for potion_color in range(6):
            file_index = file[type][potion_color]
            data = getRawFile(ROM_COPY, TableNames.ActorGeometry, file_index, True)
            num_data = []  # data, but represented as nums rather than b strings
            for d in data:
                num_data.append(d)
            # Figure out which colors to use and where to put them
            color1_offsets = [0x34]
            color2_offsets = [0x44, 0x54, 0xA4]
            color3_offsets = [0x64, 0x74, 0x84, 0xE4]
            color4_offsets = [0x94]
            color5_offsets = [0xB4, 0xC4, 0xD4]
            color_not_base_offsets = color2_offsets + color3_offsets + color4_offsets + color5_offsets
            # color6_offsets = [0xF4, 0x104, 0x114, 0x124, 0x134, 0x144, 0x154, 0x164]
            if potion_color < 5:
                new_color = getKongItemColor(colorblind_mode, potion_color, True)
            else:
                new_color = [0xFF, 0xFF, 0xFF]

            # Recolor the actor item
            color_applied = getPotionColor(colorblind_mode, potion_color)
            for offset in color1_offsets:
                num_data = changeVertexColor(num_data, offset, color_applied)
            for offset in color_not_base_offsets:
                num_data = changeVertexColor(num_data, offset, new_color)

            data = bytearray(num_data)  # convert num_data back to binary string
            writeRawFile(TableNames.ActorGeometry, file_index, True, data, ROM_COPY)

    # Model2:
    file = [91, 498, 89, 499, 501, 502]
    for potion_color in range(6):
        file_index = file[potion_color]
        data = getRawFile(ROM_COPY, TableNames.ModelTwoGeometry, file_index, True)
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color1_offsets = [0x144]
        color2_offsets = [0x154, 0x164, 0x1B4]
        color3_offsets = [0x174, 0x184, 0x194, 0x1F4]
        color4_offsets = [0x1A4]
        color5_offsets = [0x1C4, 0x1D4, 0x1E4]
        color_not_base_offsets = color2_offsets + color3_offsets + color4_offsets + color5_offsets
        # color6_offsets = [0x204, 0x214, 0x224, 0x234, 0x244, 0x254, 0x264, 0x274]
        if potion_color < 5:
            new_color = getKongItemColor(colorblind_mode, potion_color, True)
        else:
            new_color = [0xFF, 0xFF, 0xFF]

        # Recolor the model2 item
        color_applied = getPotionColor(colorblind_mode, potion_color)
        for offset in color1_offsets:
            num_data = changeVertexColor(num_data, offset, color_applied)
        for offset in color_not_base_offsets:
            num_data = changeVertexColor(num_data, offset, new_color)

        data = bytearray(num_data)  # convert num_data back to binary string
        writeRawFile(TableNames.ModelTwoGeometry, file_index, True, data, ROM_COPY)

    ROM_COPY.seek(settings.rom_data + 0x15A)
    arcade_sprite = int.from_bytes(ROM_COPY.readBytes(1), "big")
    if arcade_sprite == 0:
        return
    kong = arcade_sprite - 1
    if kong == Kongs.any:
        color = "#FFFFFF"
    elif kong < 5:
        color = getKongItemColor(colorblind_mode, kong)
    offset_dict = populateOverlayOffsets(ROM_COPY)
    addr = getROMAddress(0x8003AE58, Overlay.Arcade, offset_dict)
    potion_image = getImageFromAddress(ROM_COPY, addr, 20, 20, False, 800, TextureFormat.RGBA5551)
    potion_image = maskPotionImage(potion_image, color, getPotionColor(colorblind_mode, kong))
    px = potion_image.load()
    ROM_COPY.seek(addr)
    for y in range(20):
        for x in range(20):
            px_data = px[x, y]
            val = 1 if px_data[3] > 128 else 0
            for c in range(3):
                local_channel = (px_data[c] >> 3) & 0x1F
                shift = 1 + (5 * (2 - c))
                val |= local_channel << shift
            ROM_COPY.writeMultipleBytes(val, 2)


def maskMushroomImage(im_f, reference_image, color, side_2=False):
    """Apply RGB mask to mushroom image."""
    w, h = im_f.size
    pixels_to_mask = []
    pix_ref = reference_image.load()
    for x in range(w):
        for y in range(h):
            base_ref = list(pix_ref[x, y])
            # Filter out the white dots that won't get filtered out correctly with the below conditions
            if not (max(abs(base_ref[0] - base_ref[2]), abs(base_ref[1] - base_ref[2])) < 41 and abs(base_ref[0] - base_ref[1]) < 11):
                # Filter out that one lone pixel that is technically blue AND gets through the above filter, but should REALLY not be blue
                if not (side_2 is True and x == 51 and y == 21):
                    # Select the exact pixels to mask, which is all the "blue" pixels, filtering out the white spots
                    if base_ref[2] > base_ref[0] and base_ref[2] > base_ref[1] and int(base_ref[0] + base_ref[1]) < 200:
                        pixels_to_mask.append([x, y])
                    # Select the darker blue pixels as well
                    elif base_ref[2] > int(base_ref[0] + base_ref[1]):
                        pixels_to_mask.append([x, y])
    pix = im_f.load()
    mask = getRGBFromHash(color)
    for channel in range(3):
        mask[channel] = max(1, mask[channel])  # Absolute black is bad
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            if base[3] > 0 and [x, y] in pixels_to_mask:
                average_light = int((base[0] + base[1] + base[2]) / 3)
                for channel in range(3):
                    base[channel] = int(mask[channel] * (average_light / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def recolorMushrooms(mode: ColorblindMode, ROM_COPY: ROM):
    """Recolor the various colored mushrooms in the game for colorblind mode."""
    reference_mushroom_image = getImageFile(ROM_COPY, 7, 297, False, 32, 32, TextureFormat.RGBA5551)
    reference_mushroom_image_side1 = getImageFile(ROM_COPY, 25, 0xD64, True, 64, 32, TextureFormat.RGBA5551)
    reference_mushroom_image_side2 = getImageFile(ROM_COPY, 25, 0xD65, True, 64, 32, TextureFormat.RGBA5551)
    files_table_7 = [296, 295, 297, 299, 298]
    files_table_25_side_1 = [0xD60, getBonusSkinOffset(ExtraTextures.MushTop0), 0xD64, 0xD62, 0xD66]
    files_table_25_side_2 = [0xD61, getBonusSkinOffset(ExtraTextures.MushTop1), 0xD65, 0xD63, 0xD67]
    for file in range(5):
        # Mushroom on the ceiling inside Fungi Forest Lobby
        file_color = getKongItemColor(mode, file)
        mushroom_image = getImageFile(ROM_COPY, 7, files_table_7[file], False, 32, 32, TextureFormat.RGBA5551)
        mushroom_image = maskMushroomImage(mushroom_image, reference_mushroom_image, file_color)
        writeColorImageToROM(mushroom_image, 7, files_table_7[file], 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)
        # Mushrooms in Lanky's colored mushroom puzzle (and possibly also the bouncy mushrooms)
        mushroom_image_side_1 = getImageFile(ROM_COPY, 25, files_table_25_side_1[file], True, 64, 32, TextureFormat.RGBA5551)
        mushroom_image_side_1 = maskMushroomImage(mushroom_image_side_1, reference_mushroom_image_side1, file_color)
        writeColorImageToROM(mushroom_image_side_1, 25, files_table_25_side_1[file], 64, 32, False, TextureFormat.RGBA5551, ROM_COPY)
        mushroom_image_side_2 = getImageFile(ROM_COPY, 25, files_table_25_side_2[file], True, 64, 32, TextureFormat.RGBA5551)
        mushroom_image_side_2 = maskMushroomImage(mushroom_image_side_2, reference_mushroom_image_side2, file_color, True)
        writeColorImageToROM(mushroom_image_side_2, 25, files_table_25_side_2[file], 64, 32, False, TextureFormat.RGBA5551, ROM_COPY)


def recolorHintItem(mode: ColorblindMode, ROM_COPY: ROM):
    """Recolor the hint item for colorblind mode."""
    textures = {
        Kongs.donkey: 0x1360,
        Kongs.diddy: 0x135D,
        Kongs.lanky: 0x135E,
        Kongs.tiny: 0x135F,
        Kongs.chunky: 0x135C,
    }
    for kong, texture in textures.items():
        color = getKongItemColor(mode, kong)
        im = Image.new("RGBA", (32, 32), color)
        writeColorImageToROM(im, 25, texture, 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)
