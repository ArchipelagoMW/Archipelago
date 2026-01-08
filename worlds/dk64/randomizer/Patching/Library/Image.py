"""Image modification library functions."""

import zlib
import random
import gzip
import math
from enum import IntEnum, auto
from PIL import Image, ImageEnhance
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Settings import ColorblindMode
from randomizer.Enums.Kongs import Kongs
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from typing import Tuple, Union


class TextureFormat(IntEnum):
    """Texture Format Enum."""

    Null = auto()
    RGBA5551 = auto()
    RGBA32 = auto()
    I8 = auto()
    I4 = auto()
    IA8 = auto()
    IA4 = auto()


class ExtraTextures(IntEnum):
    """Extra Textures in Table 25 after the bonus skins."""

    FakeGBShine = 0
    RainbowCoin0 = auto()
    RainbowCoin1 = auto()
    RainbowCoin2 = auto()
    MelonSurface = auto()
    BonusShell = auto()
    OSprintLogoLeft = auto()
    OSprintLogoRight = auto()
    BLockerItemMove = auto()
    BLockerItemBlueprint = auto()
    BLockerItemFairy = auto()
    BLockerItemBean = auto()
    BLockerItemPearl = auto()
    BLockerItemRainbowCoin = auto()
    BLockerItemIceTrap = auto()
    BLockerItemPercentage = auto()
    BLockerItemBalloon = auto()
    BLockerItemCompanyCoin = auto()
    BLockerItemKong = auto()
    BeetleTex0 = auto()
    BeetleTex1 = auto()
    BeetleTex2 = auto()
    BeetleTex3 = auto()
    BeetleTex4 = auto()
    BeetleTex5 = auto()
    BeetleTex6 = auto()
    Feather0 = auto()
    Feather1 = auto()
    Feather2 = auto()
    Feather3 = auto()
    Feather4 = auto()
    Feather5 = auto()
    Feather6 = auto()
    Feather7 = auto()
    FoolOverlay = auto()
    MedalRim = auto()
    MushTop0 = auto()
    MushTop1 = auto()
    ShellWood = auto()
    ShellMetal = auto()
    ShellQMark = auto()
    RocketTop = auto()
    BlastTop = auto()
    Anniv25Sticker = auto()
    Anniv25Barrel = auto()
    BeanSpin01 = auto()
    BeanSpin02 = auto()
    BeanSpin03 = auto()
    BeanSpin04 = auto()
    BeanSpin05 = auto()
    BeanSpin06 = auto()
    BeanSpin07 = auto()
    BeanSpin08 = auto()
    BeanSpin09 = auto()
    BeanSpin10 = auto()
    BeanSpin11 = auto()
    BeanSpin12 = auto()
    KrushaFace1 = auto()
    KrushaFace2 = auto()
    KrushaFace3 = auto()
    KrushaFace4 = auto()
    KrushaFace5 = auto()
    KrushaFace321 = auto()
    KrushaFace322 = auto()
    KrushaFace323 = auto()
    KrushaFace324 = auto()
    KrushaFace325 = auto()
    APPearl0 = auto()
    APPearl1 = auto()
    APPearl2 = auto()
    APPearl3 = auto()
    APPearl4 = auto()
    APPearl5 = auto()


barrel_skins = (
    "gb",
    "dk",
    "diddy",
    "lanky",
    "tiny",
    "chunky",
    "bp",
    "nin_coin",
    "rw_coin",
    "key",
    "crown",
    "medal",
    "potion",
    "bean",
    "pearl",
    "fairy",
    "rainbow",
    "fakegb",
    "melon",
    "cranky",
    "funky",
    "candy",
    "snide",
    "hint",
    "ap",
)


def getBonusSkinOffset(offset: int):
    """Get texture index after the barrel skins."""
    return 6026 + (3 * len(barrel_skins)) + offset


def getImageFromAddress(ROM_COPY: Union[LocalROM, ROM], rom_address: int, width: int, height: int, compressed: bool, file_size: int, format: TextureFormat):
    """Get image from a ROM address."""
    ROM_COPY.seek(rom_address)
    data = ROM_COPY.readBytes(file_size)
    if compressed:
        data = zlib.decompress(data, (15 + 32))
    im_f = Image.new(mode="RGBA", size=(width, height))
    pix = im_f.load()
    for y in range(height):
        for x in range(width):
            if format == TextureFormat.RGBA32:
                offset = ((y * width) + x) * 4
                pix_data = int.from_bytes(data[offset : offset + 4], "big")
                red = (pix_data >> 24) & 0xFF
                green = (pix_data >> 16) & 0xFF
                blue = (pix_data >> 8) & 0xFF
                alpha = pix_data & 0xFF
            elif format == TextureFormat.RGBA5551:
                offset = ((y * width) + x) * 2
                pix_data = int.from_bytes(data[offset : offset + 2], "big")
                red = ((pix_data >> 11) & 31) << 3
                green = ((pix_data >> 6) & 31) << 3
                blue = ((pix_data >> 1) & 31) << 3
                alpha = (pix_data & 1) * 255
            elif format == TextureFormat.IA8:
                offset = (y * width) + x
                pix_data = int.from_bytes(data[offset : offset + 1], "big")
                intensity = int(((pix_data >> 4) / 0xF) * 255)
                alpha = int(((pix_data & 0xF) / 0xF) * 255)
                red = intensity
                green = intensity
                blue = intensity
            else:
                raise Exception(f"Unhandled Codec: {format}")
            pix[x, y] = (red, green, blue, alpha)
    return im_f


def getImageFile(ROM_COPY: Union[LocalROM, ROM], table_index: TableNames, file_index: int, compressed: bool, width: int, height: int, format: TextureFormat):
    """Grab image from file."""
    file_start = getPointerLocation(table_index, file_index)
    file_end = getPointerLocation(table_index, file_index + 1)
    file_size = file_end - file_start
    return getImageFromAddress(ROM_COPY, file_start, width, height, compressed, file_size, format)


def getRandomHueShift(min: int = -359, max: int = 359) -> int:
    """Get random hue shift."""
    return random.randint(min, max)


def hueShift(im, amount: int):
    """Apply a hue shift on an image."""
    hsv_im = im.convert("HSV")
    im_px = im.load()
    w, h = hsv_im.size
    hsv_px = hsv_im.load()
    amount = int(amount * (256 / 360))  # Truncate to within 256
    for y in range(h):
        for x in range(w):
            old = list(hsv_px[x, y]).copy()
            old[0] = (old[0] + amount) % 256
            hsv_px[x, y] = (old[0], old[1], old[2])
    rgb_im = hsv_im.convert("RGB")
    rgb_px = rgb_im.load()
    for y in range(h):
        for x in range(w):
            new = list(rgb_px[x, y])
            new.append(list(im_px[x, y])[3])
            im_px[x, y] = (new[0], new[1], new[2], new[3])
    return im


def hueShiftImageFromAddress(ROM_COPY: Union[ROM, LocalROM], address: int, width: int, height: int, format: TextureFormat, shift: int):
    """Hue shift image located at a certain ROM address."""
    size_per_px = {
        TextureFormat.RGBA5551: 2,
        TextureFormat.RGBA32: 4,
    }
    data_size_per_px = size_per_px.get(format, None)
    if data_size_per_px is None:
        raise Exception(f"Texture Format unsupported by this function. Let the devs know if you see this. Attempted format: {format.name}")
    loaded_im = getImageFromAddress(ROM_COPY, address, width, height, False, data_size_per_px * width * height, format)
    loaded_im = hueShift(loaded_im, shift)
    loaded_px = loaded_im.load()
    bytes_array = []
    for y in range(height):
        for x in range(width):
            pix_data = list(loaded_px[x, y])
            if format == TextureFormat.RGBA32:
                bytes_array.extend(pix_data)
            elif format == TextureFormat.RGBA5551:
                red = int((pix_data[0] >> 3) << 11)
                green = int((pix_data[1] >> 3) << 6)
                blue = int((pix_data[2] >> 3) << 1)
                alpha = int(pix_data[3] != 0)
                value = red | green | blue | alpha
                bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    px_data = bytearray(bytes_array)
    ROM_COPY.seek(address)
    ROM_COPY.writeBytes(px_data)


def clampRGBA(n):
    """Restricts input to integer value between 0 and 255."""
    return math.floor(max(0, min(n, 255)))


def convertRGBAToBytearray(rgba_lst):
    """Convert RGBA list with 4 items (r,g,b,a) to a two-byte array in RGBA5551 format."""
    twobyte = (rgba_lst[0] << 11) | (rgba_lst[1] << 6) | (rgba_lst[2] << 1) | (rgba_lst[3] & 1)
    lower = twobyte % 256
    upper = int(twobyte / 256) % 256
    return [upper, lower]


def imageToCI(ROM_COPY: ROM, im_f, ci_index: int, tex_index: int, pal_index: int):
    """Change image to a CI texture."""
    if ci_index not in (4, 8):
        return
    color_count = 1 << ci_index
    if color_count < 32:
        im_f = im_f.quantize(colors=color_count, method=Image.MAXCOVERAGE)
    else:
        im_f = im_f.convert("P", palette=Image.ADAPTIVE, colors=color_count)
    palette_indexes = list(im_f.getdata())
    palette = im_f.getpalette()
    palette_colors = [tuple(palette[i : i + 3]) for i in range(0, len(palette), 3)]
    rgba5551_values = []
    for color in palette_colors:
        colv = 0
        for channel_value in color:
            val = channel_value & 0x1F
            colv <<= 5
            colv |= val
        colv |= 1
        rgba5551_values.append(colv)
    tex_bin = []
    if ci_index == 8:
        tex_bin = palette_indexes.copy()
    else:
        output_value = 0
        for index, value in enumerate(palette_indexes):
            if (index & 1) == 0:
                output_value = (value & 0xF) << 4
            else:
                output_value |= value & 0xF
                tex_bin.append(output_value)
    pal_bin = []
    for half in rgba5551_values:
        upper = (half >> 8) & 0xFF
        lower = half & 0xFF
        pal_bin.extend([upper, lower])
    tex_bin_file = gzip.compress(bytearray(tex_bin), compresslevel=9)
    pal_bin_file = gzip.compress(bytearray(pal_bin), compresslevel=9)
    tex_start = getPointerLocation(TableNames.TexturesGeometry, tex_index)
    tex_end = getPointerLocation(TableNames.TexturesGeometry, tex_index + 1)
    pal_start = getPointerLocation(TableNames.TexturesGeometry, pal_index)
    pal_end = getPointerLocation(TableNames.TexturesGeometry, pal_index + 1)
    if (tex_end - tex_start) < len(tex_bin_file):
        return
    if (pal_end - pal_start) < len(pal_bin_file):
        return
    ROM_COPY.seek(tex_start)
    ROM_COPY.write(tex_bin_file)
    ROM_COPY.seek(pal_start)
    ROM_COPY.write(pal_bin_file)


def writeColorImageToROM(im_f, table_index: TableNames, file_index: int, width: int, height: int, transparent_border: bool, format: TextureFormat, ROM_COPY: Union[LocalROM, ROM]) -> None:
    """Write texture to ROM."""
    file_start = getPointerLocation(table_index, file_index)
    file_end = getPointerLocation(table_index, file_index + 1)
    file_size = file_end - file_start
    ROM_COPY.seek(file_start)
    pix = im_f.load()
    width, height = im_f.size
    bytes_array = []
    border = 1
    right_border = 3
    for y in range(height):
        for x in range(width):
            if transparent_border:
                if ((x < border) or (y < border) or (x >= (width - border)) or (y >= (height - border))) or (x == (width - right_border)):
                    pix_data = [0, 0, 0, 0]
                else:
                    pix_data = list(pix[x, y])
            else:
                pix_data = list(pix[x, y])
            if format == TextureFormat.RGBA32:
                bytes_array.extend(pix_data)
            elif format == TextureFormat.RGBA5551:
                red = int((pix_data[0] >> 3) << 11)
                green = int((pix_data[1] >> 3) << 6)
                blue = int((pix_data[2] >> 3) << 1)
                alpha = int(pix_data[3] != 0)
                value = red | green | blue | alpha
                bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
            elif format == TextureFormat.IA4:
                intensity = pix_data[0] >> 5
                alpha = 0 if pix_data[3] == 0 else 1
                data = ((intensity << 1) | alpha) & 0xF
                bytes_array.append(data)
    bytes_per_px = 2
    if format == TextureFormat.IA4:
        temp_ba = bytes_array.copy()
        bytes_array = []
        value_storage = 0
        bytes_per_px = 0.5
        for idx, val in enumerate(temp_ba):
            polarity = idx % 2
            if polarity == 0:
                value_storage = val << 4
            else:
                value_storage |= val
                bytes_array.append(value_storage)
    data = bytearray(bytes_array)
    if format == TextureFormat.RGBA32:
        bytes_per_px = 4
    if len(data) > (bytes_per_px * width * height):
        print(f"Image too big error: {table_index} > {file_index}")
    if table_index in (14, 25):
        data = gzip.compress(data, compresslevel=9)
    if len(data) > file_size:
        print(f"File too big error: {table_index} > {file_index}")
    ROM_COPY.writeBytes(data)


def getNumberImage(number: int, ROM_COPY: Union[LocalROM, ROM]):
    """Get Number Image from number."""
    if number < 5:
        num_0_bounds = [0, 20, 30, 45, 58, 76]
        x = number
        return getImageFile(ROM_COPY, 14, 15, True, 76, 24, TextureFormat.RGBA5551).crop((num_0_bounds[x], 0, num_0_bounds[x + 1], 24))
    num_1_bounds = [0, 15, 28, 43, 58, 76]
    x = number - 5
    return getImageFile(ROM_COPY, 14, 16, True, 76, 24, TextureFormat.RGBA5551).crop((num_1_bounds[x], 0, num_1_bounds[x + 1], 24))


def numberToImage(number: int, dim: Tuple[int, int], ROM_COPY: Union[LocalROM, ROM]):
    """Convert multi-digit number to image."""
    digits = 1
    if number < 10:
        digits = 1
    elif number < 100:
        digits = 2
    else:
        digits = 3
    current = number
    nums = []
    total_width = 0
    max_height = 0
    sep_dist = 1
    for _ in range(digits):
        base = getNumberImage(current % 10, ROM_COPY)
        bbox = base.getbbox()
        base = base.crop(bbox)
        nums.append(base)
        base_w, base_h = base.size
        max_height = max(max_height, base_h)
        total_width += base_w
        current = int(current / 10)
    nums.reverse()
    total_width += (digits - 1) * sep_dist
    base = Image.new(mode="RGBA", size=(total_width, max_height))
    pos = 0
    for num in nums:
        base.paste(num, (pos, 0), num)
        num_w, num_h = num.size
        pos += num_w + sep_dist
    output = Image.new(mode="RGBA", size=dim)
    xScale = dim[0] / total_width
    yScale = dim[1] / max_height
    scale = xScale
    if yScale < xScale:
        scale = yScale
    new_w = int(total_width * scale)
    new_h = int(max_height * scale)
    x_offset = int((dim[0] - new_w) / 2)
    y_offset = int((dim[1] - new_h) / 2)
    new_dim = (new_w, new_h)
    base = base.resize(new_dim)
    output.paste(base, (x_offset, y_offset), base)
    return output


def getRGBFromHash(hash: str):
    """Convert hash RGB code to rgb array."""
    red = int(hash[1:3], 16)
    green = int(hash[3:5], 16)
    blue = int(hash[5:7], 16)
    return [red, green, blue]


def maskImageWithColor(im_f: Image, mask: tuple):
    """Apply rgb mask to image using a rgb color tuple."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.copy()
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def getColorBase(mode: ColorblindMode) -> list[str]:
    """Get the color base array."""
    if mode == ColorblindMode.prot:
        return ["#000000", "#0072FF", "#766D5A", "#FFFFFF", "#FDE400"]
    elif mode == ColorblindMode.deut:
        return ["#000000", "#318DFF", "#7F6D59", "#FFFFFF", "#E3A900"]
    elif mode == ColorblindMode.trit:
        return ["#000000", "#C72020", "#13C4D8", "#FFFFFF", "#FFA4A4"]
    return ["#FFD700", "#FF0000", "#1699FF", "#B045FF", "#41FF25"]


def getKongItemColor(mode: ColorblindMode, kong: Kongs, output_as_list: bool = False) -> str:
    """Get the color assigned to a kong."""
    hash_str = getColorBase(mode)[kong]
    if output_as_list:
        return getRGBFromHash(hash_str)
    return hash_str


def maskImage(im_f, base_index, min_y, keep_dark=False, mode=ColorblindMode.off):
    """Apply RGB mask to image."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, min_y, w, h))
    if keep_dark is False:
        brightener = ImageEnhance.Brightness(im_dupe)
        im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, min_y), im_dupe)
    pix = im_f.load()
    mask = getKongItemColor(mode, base_index, True)
    w, h = im_f.size
    for x in range(w):
        for y in range(min_y, h):
            base = list(pix[x, y])
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def hueShiftImageContainer(table: int, image: int, width: int, height: int, format: TextureFormat, shift: int, ROM_COPY: ROM):
    """Load an image, shift the hue and rewrite it back to ROM."""
    loaded_im = getImageFile(ROM_COPY, table, image, table != 7, width, height, format)
    loaded_im = hueShift(loaded_im, shift)
    loaded_px = loaded_im.load()
    bytes_array = []
    for y in range(height):
        for x in range(width):
            pix_data = list(loaded_px[x, y])
            if format == TextureFormat.RGBA32:
                bytes_array.extend(pix_data)
            elif format == TextureFormat.RGBA5551:
                red = int((pix_data[0] >> 3) << 11)
                green = int((pix_data[1] >> 3) << 6)
                blue = int((pix_data[2] >> 3) << 1)
                alpha = int(pix_data[3] != 0)
                value = red | green | blue | alpha
                bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    px_data = bytearray(bytes_array)
    if table != 7:
        px_data = gzip.compress(px_data, compresslevel=9)
    ROM_COPY.seek(getPointerLocation(table, image))
    ROM_COPY.writeBytes(px_data)


def getLuma(color: tuple) -> float:
    """Get the luma value of a color."""
    return (0.299 * color[0]) + (0.587 * color[1]) + (0.114 * color[2])


def hueShiftColor(color: tuple, amount: int, head_ratio: int = None) -> tuple:
    """Apply a hue shift to a color."""
    # RGB -> HSV Conversion
    red_ratio = color[0] / 255
    green_ratio = color[1] / 255
    blue_ratio = color[2] / 255
    color_max = max(red_ratio, green_ratio, blue_ratio)
    color_min = min(red_ratio, green_ratio, blue_ratio)
    color_delta = color_max - color_min
    hue = 0
    if color_delta != 0:
        if color_max == red_ratio:
            hue = 60 * (((green_ratio - blue_ratio) / color_delta) % 6)
        elif color_max == green_ratio:
            hue = 60 * (((blue_ratio - red_ratio) / color_delta) + 2)
        else:
            hue = 60 * (((red_ratio - green_ratio) / color_delta) + 4)
    sat = 0 if color_max == 0 else color_delta / color_max
    val = color_max
    # Adjust Hue
    if head_ratio is not None and sat != 0:
        amount = head_ratio / (sat * 100)
    hue = (hue + amount) % 360
    # HSV -> RGB Conversion
    c = val * sat
    x = c * (1 - abs(((hue / 60) % 2) - 1))
    m = val - c
    if hue < 60:
        red_ratio = c
        green_ratio = x
        blue_ratio = 0
    elif hue < 120:
        red_ratio = x
        green_ratio = c
        blue_ratio = 0
    elif hue < 180:
        red_ratio = 0
        green_ratio = c
        blue_ratio = x
    elif hue < 240:
        red_ratio = 0
        green_ratio = x
        blue_ratio = c
    elif hue < 300:
        red_ratio = x
        green_ratio = 0
        blue_ratio = c
    else:
        red_ratio = c
        green_ratio = 0
        blue_ratio = x
    return (int((red_ratio + m) * 255), int((green_ratio + m) * 255), int((blue_ratio + m) * 255))


def rgba32to5551(rgba_32: list[int]) -> list[int]:
    """Convert list as RGBA32 bytes with no alpha to list of RGBA5551 bytes."""
    val_r = int((rgba_32[0] >> 3) << 11)
    val_g = int((rgba_32[1] >> 3) << 6)
    val_b = int((rgba_32[2] >> 3) << 1)
    rgba_val = val_r | val_g | val_b | 1
    return [(rgba_val >> 8) & 0xFF, rgba_val & 0xFF]
