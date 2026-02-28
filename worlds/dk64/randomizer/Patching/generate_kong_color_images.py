"""Convert RGB colors into a kong color palette."""

import gzip
import math

from randomizer.Patching.Patcher import ROM
from randomizer.Patching.Library.Generic import PaletteFillType
from randomizer.Patching.Library.Image import TextureFormat, convertRGBAToBytearray, clampRGBA, getImageFile
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames


def patchColorTranspose(x: int, y: int, patch_img, target_color: list, image_index: int):
    """Transposes RGBA value from patch file to new palette."""
    currentPix = patch_img.getpixel((x, y))
    if image_index in (3725, 0xE6C):
        redRef = (255, 0, 0, 1)
        yellowRef = (255, 255, 0, 1)
        if (abs(currentPix[0] - redRef[0]) < 20) and (abs(currentPix[1] - redRef[1]) < 20) and (abs(currentPix[2] - redRef[2]) < 20):
            # if currentPix is exactly our reference colour or close enough to not be noticable
            return target_color
        elif currentPix[0] > currentPix[1] and (abs(currentPix[1] - currentPix[0]) > 200):
            # if currentPix is red-ish (should be changed to target_color-ish)
            dr, dg, db = redRef[0] - currentPix[0], redRef[1] - currentPix[1], redRef[2] - currentPix[2]
            return (
                clampRGBA(clampRGBA(target_color[0] << 3) - dr) >> 3,
                clampRGBA(clampRGBA(target_color[1] << 3) - dg) >> 3,
                clampRGBA(clampRGBA(target_color[2] << 3) - db) >> 3,
                1,
            )
        elif not (currentPix[0] > currentPix[1] and (abs(currentPix[1] - currentPix[0]) > 200)) and (currentPix[3] == 255):
            # if currentPix is yellow (should be changed to the invert of target_color)
            if (abs(target_color[0] - redRef[0]) < 20) and (abs(target_color[1] - redRef[1]) < 20) and (abs(target_color[2] - redRef[2]) < 20):
                # if target is close enough to original red, just return the vanilla yellow values
                return (currentPix[0] >> 3, currentPix[1] >> 3, currentPix[2] >> 3, currentPix[3] & 1)
            else:
                # get the intensity of the green channel (since red and blue channels are almost always 255 and 0 respectively) to effectively get a metric for how "not yellow" the pixel is
                unyellowness = ((yellowRef[1] - currentPix[1]) / 255) - 0.1
                # grey edge case; set the letter colour to white
                if (100 < (target_color[0] << 3) < 150) and (100 < (target_color[1] << 3) < 150) and (100 < (target_color[2] << 3) < 150):
                    ir, ig, ib = 255, 255, 255
                else:
                    ir, ig, ib = (
                        (255 - (target_color[0] << 3)),
                        (255 - (target_color[1] << 3)),
                        (255 - (target_color[2] << 3)),
                    )

                return (
                    clampRGBA(unyellowness * (target_color[0] << 3) + (1 - unyellowness) * ir) >> 3,
                    clampRGBA(unyellowness * (target_color[1] << 3) + (1 - unyellowness) * ig) >> 3,
                    clampRGBA(unyellowness * (target_color[2] << 3) + (1 - unyellowness) * ib) >> 3,
                    1,
                )
        else:
            # quickly convert the read pixel from RGBA32 to RGBA5551 so it doesnt write garbage data later
            return (currentPix[0] >> 3, currentPix[1] >> 3, currentPix[2] >> 3, currentPix[3] & 1)
    elif image_index == 3734:
        blueRef = (0, 90, 255, 1)
        if (abs(currentPix[0] - blueRef[0]) < 20) and (abs(currentPix[1] - blueRef[1]) < 20) and (abs(currentPix[2] - blueRef[2]) < 20):
            # if currentPix is exactly our reference colour or close enough to not be noticable
            return target_color
        elif currentPix[2] > currentPix[1] and currentPix[2] > currentPix[0]:
            # if currentPic is blue-ish (should be changed to target_color-ish)
            dr, dg, db = blueRef[0] - currentPix[0], blueRef[1] - currentPix[1], blueRef[2] - currentPix[2]
            return (
                clampRGBA(clampRGBA(clampRGBA(clampRGBA(target_color[0]) << 3) - dr) >> 3),
                clampRGBA(clampRGBA(clampRGBA(clampRGBA(target_color[1]) << 3) - dg) >> 3),
                clampRGBA(clampRGBA(clampRGBA(clampRGBA(target_color[2]) << 3) - db) >> 3),
                1,
            )
        else:
            # quickly convert the read pixel from RGBA32 to RGBA5551 so it doesnt write garbage data later
            return (currentPix[0] >> 3, currentPix[1] >> 3, currentPix[2] >> 3, currentPix[3] & 1)


def convertColors(color_palettes, ROM_COPY: ROM):
    """Convert color into RGBA5551 format."""
    for palette in color_palettes:
        for zone in palette["zones"]:
            rgba_list = []
            if zone["fill_type"] in (PaletteFillType.checkered, PaletteFillType.radial):
                lim = 2
            else:
                lim = 1
            for x in range(lim):
                rgba = [0, 0, 0, 1]
                for i in range(3):
                    if zone["fill_type"] == PaletteFillType.radial:
                        val = int(int(f"0x{zone['colors'][0][(2 * i) + 1:(2 * i) + 3]}", 16) * (1 / 8))
                        if x == 1:
                            val = int(val * 2)
                    else:
                        val = int(int(f"0x{zone['colors'][x][(2 * i) + 1:(2 * i) + 3]}", 16) * (1 / 8))
                    if val < 0:
                        val = 0
                    elif val > 31:
                        val = 31
                    rgba[i] = val
                rgba_list.append(rgba)
            bytes_array = []
            if zone["fill_type"] in (PaletteFillType.block, PaletteFillType.kong):
                ext = convertRGBAToBytearray(rgba_list[0])
                for x in range(32 * 32):
                    bytes_array.extend(ext)
            elif zone["fill_type"] == PaletteFillType.radial:
                cen_x = 15.5
                cen_y = 15.5
                max_dist = (cen_x * cen_x) + (cen_y * cen_y)
                channel_diffs = [0, 0, 0]
                for i in range(3):
                    channel_diffs[i] = rgba_list[1][i] - rgba_list[0][i]
                for y in range(32):
                    for x in range(32):
                        dx = cen_x - x
                        dy = cen_y - y
                        dst = (dx * dx) + (dy * dy)
                        proportion = 1 - (dst / max_dist)
                        prop = [0, 0, 0, 1]
                        for i in range(3):
                            val = int((channel_diffs[i] * proportion) + rgba_list[0][i])
                            if val < 0:
                                val = 0
                            elif val > 31:
                                val = 31
                            prop[i] = val
                        ext = convertRGBAToBytearray(prop)
                        bytes_array.extend(ext)
            elif zone["fill_type"] == PaletteFillType.checkered:
                for size_mult in range(3):
                    dim_s = int(32 / math.pow(2, size_mult))
                    pol_s = int(dim_s / 8)
                    for y in range(dim_s):
                        for x in range(dim_s):
                            y_offset = 0
                            if size_mult == 1:
                                y_offset = 1
                            color_polarity_x = int(x / pol_s) % 2
                            color_polarity_y = int((y + y_offset) / pol_s) % 2
                            color_polarity = (color_polarity_x + color_polarity_y) % 2
                            ext = convertRGBAToBytearray(rgba_list[color_polarity])
                            bytes_array.extend(ext)
                for i in range(18):
                    ext = convertRGBAToBytearray(rgba_list[1])
                    bytes_array.extend(ext)
                for i in range(4):
                    ext = convertRGBAToBytearray([0, 0, 0, 0])
                    bytes_array.extend(ext)
                for i in range(3):
                    ext = convertRGBAToBytearray(rgba_list[1])
                    bytes_array.extend(ext)
                for i in range(3):
                    ext = convertRGBAToBytearray([0, 0, 0, 0])
                    bytes_array.extend(ext)
            elif zone["fill_type"] == PaletteFillType.patch:
                if zone["image"] in (3725, 3734, 0xE6C):
                    # DK's tie, lanky's butt patch and diddy's back star, respectively
                    patch_img = getImageFile(ROM_COPY, 25, zone["image"], True, 32, 64, TextureFormat.RGBA5551)

                    safe = True
                    for y in range(64):
                        for x in range(32):
                            ext = convertRGBAToBytearray(patchColorTranspose(x, y, patch_img, rgba_list[0], zone["image"]))
                            # Potentially fix the TA crash issues
                            if y == 42:
                                if (x >= 18 and x < 22) or (x >= 25):
                                    ext = [0, 0]
                            bytes_array.extend(ext)
                            if len(bytes_array) == 2744:
                                # its done copying all the bytes we care about (not the full 32x64); bail
                                safe = False
                                break
                        if not safe:
                            break
                else:
                    for size_mult in range(3):
                        patch_start_x = int(6 / math.pow(2, size_mult))
                        patch_start_y = int(8 / math.pow(2, size_mult))
                        # print(f"{patch_start_x} | {patch_start_y}")
                        patch_size = 3 - size_mult
                        if patch_size == 3:
                            patch_size = 5
                        dim_s = int(32 / math.pow(2, size_mult))
                        for y in range(dim_s):
                            for x in range(dim_s):
                                is_block = True  # Set to false to generate patch
                                if x < patch_start_x:
                                    is_block = True
                                elif x >= patch_start_x + (4 * patch_size):
                                    is_block = True
                                elif y < patch_start_y:
                                    is_block = True
                                elif y >= patch_start_y + (3 * patch_size):
                                    is_block = True
                                if is_block:
                                    ext = convertRGBAToBytearray(rgba_list[0])
                                else:
                                    delta_x = x - patch_start_x
                                    delta_y = y - patch_start_y
                                    color_polarity_x = int(delta_x / patch_size) % 2
                                    color_polarity_y = int(delta_y / patch_size) % 2
                                    color_polarity = (color_polarity_x + color_polarity_y) % 2
                                    patch_rgba = [31, 31, 31, 1]
                                    if color_polarity == 1:
                                        patch_rgba = [31, 0, 0, 1]
                                    ext = convertRGBAToBytearray(patch_rgba)
                                bytes_array.extend(ext)
                    for i in range(18):
                        ext = convertRGBAToBytearray(rgba_list[0])
                        bytes_array.extend(ext)
                    for i in range(4):
                        ext = convertRGBAToBytearray([0, 0, 0, 0])
                        bytes_array.extend(ext)
                    for i in range(3):
                        ext = convertRGBAToBytearray(rgba_list[0])
                        bytes_array.extend(ext)
                    for i in range(3):
                        ext = convertRGBAToBytearray([0, 0, 0, 0])
                        bytes_array.extend(ext)
            elif zone["fill_type"] == PaletteFillType.sparkle:
                dim_rgba = []
                for channel_index, channel in enumerate(rgba_list[0]):
                    if channel_index == 3:
                        dim_rgba.append(1)
                    else:
                        dim_channel = 0.8 * channel
                        dim_rgba.append(int(dim_channel))
                for y in range(32):
                    for x in range(32):
                        pix_rgba = []
                        if x == 31:
                            pix_rgba = rgba_list[0].copy()
                        else:
                            for channel_index in range(4):
                                if channel_index == 3:
                                    pix_channel = 1
                                else:
                                    diff = rgba_list[0][channel_index] - dim_rgba[channel_index]
                                    applied_diff = int(diff * (x / 31))
                                    pix_channel = dim_rgba[channel_index] + applied_diff
                                    if pix_channel < 0:
                                        pix_channel = 0
                                    if pix_channel > 31:
                                        pix_channel = 31
                                pix_rgba.append(pix_channel)
                        sparkle_px = [
                            [28, 5],
                            [27, 10],
                            [21, 11],
                            [25, 14],
                            [23, 15],
                            [23, 16],
                            [26, 18],
                            [20, 19],
                            [25, 25],
                        ]
                        for px in sparkle_px:
                            if px[0] == x and px[1] == y:
                                pix_rgba = [0xFF, 0xFF, 0xFF, 1]
                        bytes_array.extend(convertRGBAToBytearray(pix_rgba))

            write_point = getPointerLocation(TableNames.TexturesGeometry, zone["image"])
            ROM_COPY.seek(write_point)
            ROM_COPY.writeBytes(gzip.compress(bytearray(bytes_array), compresslevel=9))
