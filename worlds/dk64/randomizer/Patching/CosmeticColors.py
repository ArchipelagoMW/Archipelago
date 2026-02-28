"""Apply cosmetic skins to kongs."""

from __future__ import annotations

import gzip
from typing import TYPE_CHECKING, List, Tuple
from io import BytesIO

from PIL import Image, ImageDraw, ImageEnhance

import js
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import CharacterColors, ColorblindMode, KongModels, WinConditionComplex
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Types import BarrierItems
from randomizer.Patching.Cosmetics.CustomTextures import writeTransition, writeCustomPaintings, writeCustomPortal, writeCustomArcadeSprites, writeCustomReels, writeCustomItemSprites
from randomizer.Patching.Cosmetics.Krusha import placeKrushaHead, fixBaboonBlasts, kong_index_mapping, fixModelSmallKongCollision
from randomizer.Patching.Cosmetics.Colorblind import (
    recolorKlaptraps,
    writeWhiteKasplatHairColorToROM,
    recolorBells,
    recolorWrinklyDoors,
    recolorSlamSwitches,
    recolorBlueprintModelTwo,
    recolorPotions,
    recolorMushrooms,
    recolorHintItem,
    writeKasplatHairColorToROM,
    maskBlueprintImage,
    maskLaserImage,
    recolorKRoolShipSwitch,
    recolorRotatingRoomTiles,
)
from randomizer.Patching.Library.Generic import compatible_background_textures, IsColorOptionSelected
from randomizer.Patching.Library.Image import (
    getImageFile,
    TextureFormat,
    ExtraTextures,
    getBonusSkinOffset,
    writeColorImageToROM,
    numberToImage,
    maskImage,
    maskImageWithColor,
    getKongItemColor,
    hueShiftColor,
)
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Settings import Settings, ColorOptions
from randomizer.Patching.Cosmetics.ModelSwaps import (
    model_mapping,
    applyCosmeticModelSwaps,
)
from randomizer.Patching.Cosmetics.KongColor import writeKongColors, changeModelTextures


class HelmDoorSetting:
    """Class to store information regarding helm doors."""

    def __init__(self, item_setting: BarrierItems, count: int, item_image: int, number_image: int) -> None:
        """Initialize with given parameters."""
        self.item_setting = item_setting
        self.count = count
        self.item_image = item_image
        self.number_image = number_image


class HelmDoorImages:
    """Class to store information regarding helm door item images."""

    def __init__(
        self,
        setting: BarrierItems,
        image_indexes: List[int],
        flip: bool = False,
        table: int = 25,
        dimensions: Tuple[int, int] = (44, 44),
        format: TextureFormat = TextureFormat.RGBA5551,
    ) -> None:
        """Initialize with given parameters."""
        self.setting = setting
        self.image_indexes = image_indexes
        self.flip = flip
        self.table = table
        self.dimensions = dimensions
        self.format = format


def changePatchFace(settings: Settings, ROM_COPY: ROM):
    """Change the top of the dirt patch image."""
    if not settings.better_dirt_patch_cosmetic:
        return
    dirt_im = getImageFile(ROM_COPY, 25, 0x1379, True, 32, 32, TextureFormat.RGBA5551)
    letd_im = getImageFile(ROM_COPY, 14, 0x75, True, 40, 51, TextureFormat.RGBA5551).resize((18, 32)).rotate(-5)
    letk_im = getImageFile(ROM_COPY, 14, 0x76, True, 40, 51, TextureFormat.RGBA5551).resize((18, 32))
    letter_ims = (letd_im, letk_im)
    for letter in letter_ims:
        imw, imh = letter.size
        px = letter.load()
        for x in range(imw):
            for y in range(imh):
                r, g, b, a = letter.getpixel((x, y))
                px[x, y] = (r, g, b, 150 if a > 128 else 0)
    dirt_im.paste(letd_im, (0, 0), letd_im)
    dirt_im.paste(letk_im, (16, 0), letk_im)
    writeColorImageToROM(dirt_im, 25, 0x1379, 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)


def apply_cosmetic_colors(settings: Settings, ROM_COPY: ROM):
    """Apply cosmetic skins to kongs."""
    applyCosmeticModelSwaps(settings, ROM_COPY)
    changePatchFace(settings, ROM_COPY)
    writeKongColors(settings, ROM_COPY)

    settings.jetman_color = [0xFF, 0xFF, 0xFF]
    if settings.override_cosmetics:
        if settings.misc_cosmetics:
            # Menu Background
            textures = list(compatible_background_textures.keys())
            weights = [compatible_background_textures[x].weight for x in textures]
            selected_texture = settings.random.choices(textures, weights=weights, k=1)[0]
            settings.menu_texture_index = selected_texture
            settings.menu_texture_name = compatible_background_textures[selected_texture].name
        if IsColorOptionSelected(settings, ColorOptions.playable_characters):
            # Jetman
            jetman_color = [0xFF] * 3
            sufficiently_bright = False
            brightness_threshold = 80
            for channel in range(3):
                jetman_color[channel] = settings.random.randint(0, 0xFF)
                if jetman_color[channel] >= brightness_threshold:
                    sufficiently_bright = True
            if not sufficiently_bright:
                channel = settings.random.randint(0, 2)
                value = settings.random.randint(brightness_threshold, 0xFF)
                jetman_color[channel] = value
            settings.jetman_color = jetman_color.copy()

    if js.document.getElementById("override_cosmetics").checked or True:
        writeTransition(settings, ROM_COPY)
        writeCustomPortal(settings, ROM_COPY)
        writeCustomPaintings(settings, ROM_COPY)
        writeCustomReels(settings, ROM_COPY)
        writeCustomArcadeSprites(settings, ROM_COPY)
        writeCustomItemSprites(settings, ROM_COPY)
        settings.gb_colors = CharacterColors[js.document.getElementById("gb_colors").value]
        settings.gb_custom_color = js.document.getElementById("gb_custom_color").value
    else:
        settings.gb_colors = CharacterColors.randomized

    # GB Shine
    if settings.override_cosmetics and settings.gb_colors != CharacterColors.vanilla:
        channels = []
        if settings.gb_colors == CharacterColors.randomized:
            for x in range(3):
                channels.append(settings.random.randint(0, 255))
        elif settings.gb_colors == CharacterColors.custom:
            for x in range(3):
                start = (2 * x) + 1
                finish = (2 * x) + 3
                channel = int(settings.gb_custom_color[start:finish], 16)
                channels.append(channel)
        base_textures = [0xB7B, 0x323]
        # base_textures = [0xB7B, 0x323, 0xBAA, rim_texture, 0xE4D, 0xE4E]  # Banana hoard looks **very** strange like this
        textures = base_textures + list(range(0x155C, 0x1568))
        for tex in textures:
            dim_pattern = {
                0xB7B: (32, 32),
                0x323: (32, 32),
                0xBAA: (4, 4),
                0xE4D: (64, 32),
                0xE4E: (64, 32),
            }
            dim_pattern_local = dim_pattern.get(tex, (44, 44))
            width = dim_pattern_local[0]
            height = dim_pattern_local[1]
            shine_img = getImageFile(ROM_COPY, 25, tex, True, width, height, TextureFormat.RGBA5551)
            gb_shine_img = maskImageGBSpin(shine_img, tuple(channels), tex)
            if tex == 0xB7B:
                # Create fake GB shine img
                min_rgb = min(channels[0], channels[1], channels[2])
                max_rgb = max(channels[0], channels[1], channels[2])
                is_greyscale = (max_rgb - min_rgb) < 50
                fakegb_shine_img = None
                delta_mag = 80
                if is_greyscale:
                    delta = -delta_mag
                    if max_rgb < 128:
                        delta = delta_mag
                    fakegb_shine_img = maskImageWithColor(shine_img, tuple([x + delta for x in channels]))
                else:
                    new_color = hueShiftColor(tuple(channels), 60, 1750)
                    fakegb_shine_img = maskImageWithColor(shine_img, new_color)
                writeColorImageToROM(
                    fakegb_shine_img,
                    25,
                    getBonusSkinOffset(ExtraTextures.FakeGBShine),
                    width,
                    height,
                    False,
                    TextureFormat.RGBA5551,
                    ROM_COPY,
                )
            writeColorImageToROM(gb_shine_img, 25, tex, width, height, False, TextureFormat.RGBA5551, ROM_COPY)


balloon_single_frames = [(4, 38), (5, 38), (5, 38), (5, 38), (5, 38), (5, 38), (4, 38), (4, 38)]


def getSpinPixels() -> dict:
    """Get pixels that shouldn't be affected by the mask."""
    spin_lengths = {
        0x155C: {
            17: (12, 2),
            18: (11, 4),
            19: (10, 6),
            20: (10, 7),
            21: (10, 7),
            22: (10, 6),
            23: (11, 3),
        },
        0x155D: {
            14: (15, 1),
            15: (14, 5),
            16: (13, 7),
            17: (12, 9),
            18: (12, 10),
            19: (12, 11),
            20: (12, 11),
            21: (13, 10),
            22: (14, 8),
            23: (15, 4),
        },
        0x155E: {
            14: (19, 5),
            15: (19, 7),
            16: (18, 9),
            17: (18, 10),
            18: (18, 10),
            19: (19, 10),
            20: (20, 9),
            21: (21, 8),
            22: (22, 7),
        },
        0x155F: {
            14: (27, 2),
            15: (26, 5),
            16: (26, 6),
            17: (26, 6),
            18: (27, 6),
            19: (27, 6),
            20: (28, 5),
            21: (29, 4),
            22: (29, 4),
            23: (30, 3),
        },
        0x1560: {
            16: (32, 1),
            17: (32, 2),
            18: (33, 1),
            19: (33, 2),
            20: (33, 1),
            21: (33, 1),
            22: (33, 1),
        },
    }
    spin_pixels = {}
    for tex in spin_lengths:
        local_lst = []
        for y in spin_lengths[tex]:
            for x_o in range(spin_lengths[tex][y][1]):
                local_lst.append((spin_lengths[tex][y][0] + x_o, y))
        spin_pixels[tex] = local_lst
    return spin_pixels


def maskImageGBSpin(im_f, color: tuple, image_index: int):
    """Mask the GB Spin Sprite."""
    if image_index in (getBonusSkinOffset(ExtraTextures.MedalRim), 0xBAA):
        color = tuple([int(x * 0.75) for x in list(color)])
    masked_im = maskImageWithColor(im_f, color)
    spin_pixels = getSpinPixels()
    if image_index not in spin_pixels:
        return masked_im
    px = im_f.load()
    px_0 = masked_im.load()
    for point in spin_pixels[image_index]:
        px_0[point[0], point[1]] = px[point[0], point[1]]
    return masked_im


def maskImageWithOutline(im_f, base_index, min_y, colorblind_mode, type=""):
    """Apply RGB mask to image with an Outline in a different color."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, min_y, w, h))
    if type != "bunch" or base_index == 4:
        brightener = ImageEnhance.Brightness(im_dupe)
        im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, min_y), im_dupe)
    pix = im_f.load()
    mask = getKongItemColor(colorblind_mode, base_index, True)
    if base_index == 2 or (base_index == 0 and colorblind_mode == ColorblindMode.trit):  # lanky or (DK in tritanopia mode)
        mask2 = getKongItemColor(colorblind_mode, Kongs.chunky, True)
    else:
        mask2 = getKongItemColor(colorblind_mode, Kongs.diddy, True)
    contrast = False
    if base_index == 0:
        contrast = True
    for channel in range(3):
        mask[channel] = max(39, mask[channel])  # Too black is bad for these items
        if base_index == 0 and type == "single":  # Donkey's single
            mask[channel] += 20
    w, h = im_f.size
    for x in range(w):
        for y in range(min_y, h):
            base = list(pix[x, y])
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                    if contrast is True:
                        if base[channel] > 30:
                            base[channel] = int(base[channel] / 2)
                        else:
                            base[channel] = int(base[channel] / 4)
                pix[x, y] = (base[0], base[1], base[2], base[3])
    for t in range(3):
        for x in range(w):
            for y in range(min_y, h):
                base = list(pix[x, y])
                if base[3] > 0:
                    if (
                        (x + t < w and list(pix[x + t, y])[3] == 0)
                        or (y + t < h and list(pix[x, y + t])[3] == 0)
                        or (x - t > -1 and list(pix[x - t, y])[3] == 0)
                        or (y - t > min_y - 1 and list(pix[x, y - t])[3] == 0)
                    ):
                        pix[x, y] = (mask2[0], mask2[1], mask2[2], base[3])
    return im_f


SINGLE_START = [168, 152, 232, 208, 240]
BALLOON_START = [5835, 5827, 5843, 5851, 5819]
LASER_START = [784, 748, 363, 760, 772]
SHOCKWAVE_START = [4897, 4903, 4712, 4950, 4925]
BLUEPRINT_START = [5624, 5608, 5519, 5632, 5616]
COIN_START = [224, 256, 248, 216, 264]
BUNCH_START = [274, 854, 818, 842, 830]


def overwrite_object_colors(settings, ROM_COPY: ROM):
    """Overwrite object colors."""
    mode = settings.colorblind_mode
    sav = settings.rom_data
    galleon_switch_value = None
    ROM_COPY.seek(sav + 0x103)
    switch_rando_on = int.from_bytes(ROM_COPY.readBytes(1), "big") != 0
    if switch_rando_on:
        ROM_COPY.seek(sav + 0x104 + 3)
        galleon_switch_value = int.from_bytes(ROM_COPY.readBytes(1), "big")
    if mode != ColorblindMode.off:
        if mode in (ColorblindMode.prot, ColorblindMode.deut):
            recolorBells(ROM_COPY)
        # Preload DK single cb image to paste onto balloons
        dk_single = getImageFile(ROM_COPY, 7, 175, False, 44, 44, TextureFormat.RGBA5551)
        dk_single = dk_single.resize((21, 21))
        blueprint_lanky = []
        # Preload blueprint images. Lanky's blueprint image is so much easier to mask, because it is blue, and the frame is brown
        for file in range(8):
            blueprint_lanky.append(getImageFile(ROM_COPY, 25, 5519 + file, True, 48, 42, TextureFormat.RGBA5551))
        writeWhiteKasplatHairColorToROM("#FFFFFF", "#000000", 25, 4125, TextureFormat.RGBA5551, ROM_COPY)
        recolorWrinklyDoors(mode, ROM_COPY)
        recolorSlamSwitches(galleon_switch_value, ROM_COPY, mode)
        recolorRotatingRoomTiles(mode, ROM_COPY)
        recolorBlueprintModelTwo(mode, ROM_COPY)
        recolorKlaptraps(mode, ROM_COPY)
        recolorPotions(settings, mode, ROM_COPY)
        recolorMushrooms(mode, ROM_COPY)
        recolorHintItem(mode, ROM_COPY)
        for kong_index in range(5):
            # file = 4120
            # # Kasplat Hair
            # hair_im = getFile(25, file, True, 32, 44, TextureFormat.RGBA5551)
            # hair_im = maskImage(hair_im, kong_index, 0)
            # writeColorImageToROM(hair_im, 25, [4124, 4122, 4123, 4120, 4121][kong_index], 32, 44, False, ROM_COPY)
            writeKasplatHairColorToROM(getKongItemColor(mode, kong_index), 25, [4124, 4122, 4123, 4120, 4121][kong_index], TextureFormat.RGBA5551, ROM_COPY)
            for offset in range(8):
                # Blueprint sprite
                blueprint_im = blueprint_lanky[offset]
                blueprint_im = maskBlueprintImage(blueprint_im, kong_index, mode)
                writeColorImageToROM(blueprint_im, 25, BLUEPRINT_START[kong_index] + offset, 48, 42, False, TextureFormat.RGBA5551, ROM_COPY)
            for offset in range(6):
                # Shockwave
                shockwave_im = getImageFile(ROM_COPY, 25, SHOCKWAVE_START[kong_index] + offset, True, 32, 32, TextureFormat.RGBA32)
                shockwave_im = maskImage(shockwave_im, kong_index, 0, False, mode)
                writeColorImageToROM(shockwave_im, 25, SHOCKWAVE_START[kong_index] + offset, 32, 32, False, TextureFormat.RGBA32, ROM_COPY)
            for offset in range(12):
                # Helm Laser (will probably also affect the Pufftoss laser and the Game Over laser)
                laser_im = getImageFile(ROM_COPY, 7, LASER_START[kong_index] + offset, False, 32, 32, TextureFormat.RGBA32)
                laser_im = maskLaserImage(laser_im, kong_index, mode)
                writeColorImageToROM(laser_im, 7, LASER_START[kong_index] + offset, 32, 32, False, TextureFormat.RGBA32, ROM_COPY)
            if kong_index in (Kongs.donkey, Kongs.tiny) or (kong_index == Kongs.lanky and mode != ColorblindMode.trit):  # Lanky (prot, deut only) or DK or Tiny
                for offset in range(8):
                    # Single
                    single_im = getImageFile(ROM_COPY, 7, SINGLE_START[kong_index] + offset, False, 44, 44, TextureFormat.RGBA5551)
                    single_im = maskImageWithOutline(single_im, kong_index, 0, mode, "single")
                    writeColorImageToROM(single_im, 7, SINGLE_START[kong_index] + offset, 44, 44, False, TextureFormat.RGBA5551, ROM_COPY)
                for offset in range(8):
                    # Coin
                    coin_im = getImageFile(ROM_COPY, 7, COIN_START[kong_index] + offset, False, 48, 42, TextureFormat.RGBA5551)
                    coin_im = maskImageWithOutline(coin_im, kong_index, 0, mode)
                    writeColorImageToROM(coin_im, 7, COIN_START[kong_index] + offset, 48, 42, False, TextureFormat.RGBA5551, ROM_COPY)
                for offset in range(12):
                    # Bunch
                    bunch_im = getImageFile(ROM_COPY, 7, BUNCH_START[kong_index] + offset, False, 44, 44, TextureFormat.RGBA5551)
                    bunch_im = maskImageWithOutline(bunch_im, kong_index, 0, mode, "bunch")
                    writeColorImageToROM(bunch_im, 7, BUNCH_START[kong_index] + offset, 44, 44, False, TextureFormat.RGBA5551, ROM_COPY)
                for offset in range(8):
                    # Balloon
                    balloon_im = getImageFile(ROM_COPY, 25, BALLOON_START[kong_index] + offset, True, 32, 64, TextureFormat.RGBA5551)
                    balloon_im = maskImageWithOutline(balloon_im, kong_index, 33, mode)
                    balloon_im.paste(dk_single, balloon_single_frames[offset], dk_single)
                    writeColorImageToROM(balloon_im, 25, BALLOON_START[kong_index] + offset, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
            else:
                for offset in range(8):
                    # Single
                    single_im = getImageFile(ROM_COPY, 7, SINGLE_START[kong_index] + offset, False, 44, 44, TextureFormat.RGBA5551)
                    single_im = maskImage(single_im, kong_index, 0, False, mode)
                    writeColorImageToROM(single_im, 7, SINGLE_START[kong_index] + offset, 44, 44, False, TextureFormat.RGBA5551, ROM_COPY)
                for offset in range(8):
                    # Coin
                    coin_im = getImageFile(ROM_COPY, 7, COIN_START[kong_index] + offset, False, 48, 42, TextureFormat.RGBA5551)
                    coin_im = maskImage(coin_im, kong_index, 0, False, mode)
                    writeColorImageToROM(coin_im, 7, COIN_START[kong_index] + offset, 48, 42, False, TextureFormat.RGBA5551, ROM_COPY)
                for offset in range(12):
                    # Bunch
                    bunch_im = getImageFile(ROM_COPY, 7, BUNCH_START[kong_index] + offset, False, 44, 44, TextureFormat.RGBA5551)
                    bunch_im = maskImage(bunch_im, kong_index, 0, True, mode)
                    writeColorImageToROM(bunch_im, 7, BUNCH_START[kong_index] + offset, 44, 44, False, TextureFormat.RGBA5551, ROM_COPY)
                for offset in range(8):
                    # Balloon
                    balloon_im = getImageFile(ROM_COPY, 25, BALLOON_START[kong_index] + offset, True, 32, 64, TextureFormat.RGBA5551)
                    balloon_im = maskImage(balloon_im, kong_index, 33, False, mode)
                    balloon_im.paste(dk_single, balloon_single_frames[offset], dk_single)
                    writeColorImageToROM(balloon_im, 25, BALLOON_START[kong_index] + offset, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
    else:
        # Recolor slam switch if colorblind mode is off
        if galleon_switch_value is not None:
            if galleon_switch_value != 1:
                new_color = [0xFF, 0x00, 0x00]
                if galleon_switch_value == 2:
                    new_color = [0x26, 0xA3, 0xE9]
                recolorKRoolShipSwitch(new_color, ROM_COPY)
    if settings.head_balloons:
        for kong in range(5):
            for offset in range(8):
                balloon_im = getImageFile(ROM_COPY, 25, BALLOON_START[kong] + offset, True, 32, 64, TextureFormat.RGBA5551)
                kong_im = getImageFile(ROM_COPY, 14, 190 + kong, True, 32, 32, TextureFormat.RGBA5551)
                kong_im = kong_im.transpose(Image.FLIP_TOP_BOTTOM).resize((20, 20))
                balloon_im.paste(kong_im, (5, 39), kong_im)
                writeColorImageToROM(balloon_im, 25, BALLOON_START[kong] + offset, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)


ORANGE_SCALING = 0.7
model_index_mapping = {
    # Regular model, instrument model
    KongModels.krusha: (0xDA, 0xDA),
    KongModels.disco_chunky: (0xD, 0xEC),
    KongModels.krool_fight: (0x113, 0x113),
    KongModels.krool_cutscene: (0x114, 0x114),
    KongModels.cranky: (0x115, 0x115),
    KongModels.candy: (0x116, 0x116),
    KongModels.funky: (0x117, 0x117),
    KongModels.disco_donkey: (0x129, 0x129),
}

LIME_COLORS = {
    Kongs.donkey: (255, 224, 8),
    Kongs.diddy: (255, 48, 32),
    Kongs.lanky: (40, 168, 255),
    Kongs.tiny: (216, 100, 248),
    Kongs.chunky: (0, 255, 0),
    Kongs.any: (100, 255, 60),
}


def applyKongModelSwaps(settings: Settings, ROM_COPY: LocalROM) -> None:
    """Apply Krusha Kong setting."""
    settings_values = [
        settings.kong_model_dk,
        settings.kong_model_diddy,
        settings.kong_model_lanky,
        settings.kong_model_tiny,
        settings.kong_model_chunky,
    ]
    for index, value in enumerate(settings_values):
        ROM_COPY.seek(settings.rom_data + 0x1B8 + index)
        if value not in model_mapping:
            ROM_COPY.write(0)
        else:
            ROM_COPY.write(model_mapping[value])
            if value == KongModels.default:
                continue
            dest_data = kong_index_mapping[index]
            source_data = model_index_mapping[value]
            for model_subindex in range(2):
                if dest_data[model_subindex] is not None:
                    dest_start = getPointerLocation(TableNames.ActorGeometry, dest_data[model_subindex])
                    source_start = getPointerLocation(TableNames.ActorGeometry, source_data[model_subindex])
                    source_end = getPointerLocation(TableNames.ActorGeometry, source_data[model_subindex] + 1)
                    source_size = source_end - source_start
                    ROM_COPY.seek(source_start)
                    file_bytes = ROM_COPY.readBytes(source_size)
                    ROM_COPY.seek(dest_start)
                    ROM_COPY.writeBytes(file_bytes)
                    # Write uncompressed size
                    unc_table = getPointerLocation(TableNames.UncompressedFileSizes, TableNames.ActorGeometry)
                    ROM_COPY.seek(unc_table + (source_data[model_subindex] * 4))
                    unc_size = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(unc_table + (dest_data[model_subindex] * 4))
                    ROM_COPY.writeMultipleBytes(unc_size, 4)
            changeModelTextures(settings, ROM_COPY, index)
            if value in (KongModels.krusha, KongModels.krool_cutscene, KongModels.krool_fight):
                fixModelSmallKongCollision(index, ROM_COPY)
            if value == KongModels.krusha:
                placeKrushaHead(ROM_COPY, settings, index)
                if index == Kongs.donkey:
                    fixBaboonBlasts(ROM_COPY)
                # Orange Switches
                switch_faces = [0xB25, 0xB1E, 0xC81, 0xC80, 0xB24]
                base_im = getImageFile(ROM_COPY, 25, 0xC20, True, 32, 32, TextureFormat.RGBA5551)
                orange_im = getImageFile(ROM_COPY, 7, 0x136, False, 32, 32, TextureFormat.RGBA5551)
                if settings.colorblind_mode == ColorblindMode.off:
                    orange_im = maskImageWithColor(orange_im, LIME_COLORS[index])
                else:
                    orange_im = maskImageWithColor(orange_im, (0, 255, 0))  # Brighter green makes this more distinguishable for colorblindness
                dim_length = int(32 * ORANGE_SCALING)
                dim_offset = int((32 - dim_length) / 2)
                orange_im = orange_im.resize((dim_length, dim_length))
                base_im.paste(orange_im, (dim_offset, dim_offset), orange_im)
                writeColorImageToROM(base_im, 25, switch_faces[index], 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)


def darkenDPad(ROM_COPY: ROM):
    """Change the DPad cross texture for the DPad HUD."""
    img = getImageFile(ROM_COPY, 14, 187, True, 32, 32, TextureFormat.RGBA5551)
    px = img.load()
    bytes_array = []
    for y in range(32):
        for x in range(32):
            pix_data = list(px[x, y])
            for c in range(3):
                pix_data[c] = 255 - pix_data[c]
            value = 1 if pix_data[3] > 128 else 0
            for v in range(3):
                value |= (pix_data[v] >> 3) << 1 + (5 * (2 - v))
            bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    px_data = bytearray(bytes_array)
    px_data = gzip.compress(px_data, compresslevel=9)
    ROM_COPY.seek(getPointerLocation(TableNames.TexturesHUD, 187))
    ROM_COPY.writeBytes(px_data)


def applyHelmDoorCosmetics(settings: Settings, ROM_COPY: LocalROM) -> None:
    """Apply Helm Door Cosmetic Changes."""
    crown_door_required_item = settings.crown_door_item
    coin_door_required_item = settings.coin_door_item
    Doors = [
        HelmDoorSetting(crown_door_required_item, settings.crown_door_item_count, 6022, 6023),
        HelmDoorSetting(coin_door_required_item, settings.coin_door_item_count, 6024, 6025),
    ]
    Images = [
        HelmDoorImages(BarrierItems.GoldenBanana, [0x155C]),
        HelmDoorImages(BarrierItems.Blueprint, [x + 4 for x in (0x15F8, 0x15E8, 0x158F, 0x1600, 0x15F0)], False, 25, (48, 42)),
        HelmDoorImages(BarrierItems.Bean, [6020], False, 25, (64, 32)),
        HelmDoorImages(BarrierItems.Pearl, [0xD5F], False, 25, (32, 32)),
        HelmDoorImages(BarrierItems.Fairy, [0x16ED], False, 25, (32, 32), TextureFormat.RGBA32),
        HelmDoorImages(BarrierItems.Key, [5877]),
        HelmDoorImages(BarrierItems.Medal, [0x156C]),
        HelmDoorImages(BarrierItems.RainbowCoin, [5963], False, 25, (48, 42)),
        HelmDoorImages(BarrierItems.Crown, [5893]),
        HelmDoorImages(BarrierItems.CompanyCoin, [5905, 5912]),
    ]
    for door in Doors:
        for image_data in Images:
            if image_data.setting == door.item_setting:
                base = Image.new(mode="RGBA", size=(44, 44))
                base_overlay = Image.new(mode="RGBA", size=image_data.dimensions)
                for image_slot, image in enumerate(image_data.image_indexes):
                    item_im = getImageFile(
                        ROM_COPY,
                        image_data.table,
                        image,
                        image_data.table in (14, 25),
                        image_data.dimensions[0],
                        image_data.dimensions[1],
                        image_data.format,
                    )
                    start_x = 0
                    finish_x = image_data.dimensions[0]
                    if len(image_data.image_indexes) > 1:
                        start_x = int(image_slot * (image_data.dimensions[0] / len(image_data.image_indexes)))
                        finish_x = int((image_slot + 1) * (image_data.dimensions[0] / len(image_data.image_indexes)))
                        item_im = item_im.crop((start_x, 0, finish_x, image_data.dimensions[1]))
                    base_overlay.paste(item_im, (start_x, 0), item_im)
                if image_data.flip:
                    base_overlay = base_overlay.transpose(Image.FLIP_TOP_BOTTOM)
                if image_data.dimensions[0] > image_data.dimensions[1]:
                    # Width shrinked to 44
                    new_height = image_data.dimensions[1] * (44 / image_data.dimensions[0])
                    base_overlay = base_overlay.resize((44, int(new_height)))
                    base.paste(base_overlay, (0, int(22 - (new_height / 2))), base_overlay)
                else:
                    # Height shrinked to 44
                    new_width = image_data.dimensions[0] * (44 / image_data.dimensions[1])
                    base_overlay = base_overlay.resize((int(new_width), 44))
                    base.paste(base_overlay, (int(22 - (new_width / 2)), 0), base_overlay)
                if door.item_setting == BarrierItems.Pearl:
                    pearl_mask_im = Image.new("RGBA", (44, 44), (0, 0, 0, 255))
                    draw = ImageDraw.Draw(pearl_mask_im)
                    draw.ellipse((0, 0, 43, 43), fill=(0, 0, 0, 0), outline=(0, 0, 0, 0))
                    pix_pearl = base.load()
                    for y in range(44):
                        for x in range(44):
                            r, g, b, a = pearl_mask_im.getpixel((x, y))
                            if a > 128:
                                pix_pearl[x, y] = (0, 0, 0, 0)
                writeColorImageToROM(base, 25, door.item_image, 44, 44, True, TextureFormat.RGBA5551, ROM_COPY)
                writeColorImageToROM(
                    numberToImage(door.count, (44, 44), ROM_COPY).transpose(Image.FLIP_TOP_BOTTOM),
                    25,
                    door.number_image,
                    44,
                    44,
                    True,
                    TextureFormat.RGBA5551,
                    ROM_COPY,
                )


def darkenPauseBubble(settings: Settings, ROM_COPY: ROM):
    """Change the brightness of the text bubble used for the pause menu for dark mode."""
    if not settings.dark_mode_textboxes:
        return
    img = getImageFile(ROM_COPY, 14, 107, True, 48, 32, TextureFormat.RGBA5551)
    px = img.load()
    canary_px = list(px[24, 16])
    if canary_px[0] < 128 and canary_px[1] < 128 and canary_px[2] < 128:
        # Already darkened, cancel
        return
    bytes_array = []
    for y in range(32):
        for x in range(48):
            pix_data = list(px[x, y])
            value = 1 if pix_data[3] > 128 else 0
            for v in range(3):
                pix_data[v] = 0xFF - pix_data[v]
                value |= (pix_data[v] >> 3) << 1 + (5 * (2 - v))
            bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    px_data = bytearray(bytes_array)
    px_data = gzip.compress(px_data, compresslevel=9)
    ROM_COPY.seek(getPointerLocation(TableNames.TexturesHUD, 107))
    ROM_COPY.writeBytes(px_data)


class WinConData:
    """Class to store information about win condition."""

    def __init__(self, table: int, image: int, tex_format: TextureFormat, width: int, height: int, flip: bool, default_count: int):
        """Initialize with given parameters."""
        self.table = table
        self.image = image
        self.tex_format = tex_format
        self.width = width
        self.height = height
        self.flip = flip
        self.default_count = default_count


def writeWinConImage(settings: Settings, image: Image, ROM_COPY: LocalROM):
    """Wrap function for writing a win con image, detecting K Rool win con."""
    # if settings.win_condition_spawns_ship:
    #     base_im = Image.new(mode="RGBA", size=(64, 64))
    #     left_im = getImageFile(ROM_COPY, TableNames.TexturesGeometry, 0x383, True, 32, 64, TextureFormat.RGBA5551)
    #     right_im = getImageFile(ROM_COPY, TableNames.TexturesGeometry, 0x384, True, 32, 64, TextureFormat.RGBA5551)
    #     base_im.paste(left_im, (0, 0), left_im)
    #     base_im.paste(right_im, (32, 0), right_im)
    #     base_im = base_im.transpose(Image.FLIP_TOP_BOTTOM)
    #     base_im = base_im.resize((32, 32))
    #     base_im.paste(image, (0, 0), image)
    # else:
    #     base_im = image
    base_im = image
    writeColorImageToROM(base_im, 14, 195, 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)


def showWinCondition(settings: Settings, ROM_COPY: LocalROM):
    """Alter the image that's shown on the main menu to display the win condition."""
    win_con = settings.win_condition_item
    helmhurry = settings.helm_hurry and settings.archipelago

    if win_con == WinConditionComplex.krools_challenge:
        images = [
            (0x903, 0, 1),
            (0x904, 0, 2),
            (0x905, 0, 3),
            (0x906, 1, 3),
            (0x907, 1, 2),
            (0x908, 1, 1),
            (0x909, 1, 0),
            (0x90A, 0, 0),
        ]
        output_image = Image.new(mode="RGBA", size=(128, 128))
        for img in images:
            local_img = getImageFile(ROM_COPY, 25, img[0], True, 64, 32, TextureFormat.RGBA5551)
            local_img = local_img.convert("RGBA")
            pos_x = 64 * img[1]
            pos_y = 32 * img[2]
            output_image.paste(local_img, (pos_x, pos_y), local_img)
        output_image = output_image.resize((32, 32)).transpose(Image.FLIP_TOP_BOTTOM)
        writeWinConImage(settings, output_image, ROM_COPY)
    if helmhurry:
        output_image = Image.open(BytesIO(js.getFile("base-hack/assets/displays/treasurechest.png")))
        output_image = output_image.resize((32, 32))
        writeWinConImage(settings, output_image, ROM_COPY)
        return
    if win_con == WinConditionComplex.get_key8:
        output_image = Image.open(BytesIO(js.getFile("base-hack/assets/displays/key8.png")))
        output_image = output_image.resize((32, 32))
        writeWinConImage(settings, output_image, ROM_COPY)
        return
    if win_con == WinConditionComplex.req_bean:
        output_image = Image.open(BytesIO(js.getFile("base-hack/assets/arcade_jetpac/arcade/bean.png")))
        output_image = output_image.resize((32, 32))
        writeWinConImage(settings, output_image, ROM_COPY)
        return
    if win_con == WinConditionComplex.krem_kapture:
        item_im = getImageFile(ROM_COPY, 14, 0x90, True, 32, 32, TextureFormat.RGBA5551)
        writeWinConImage(settings, item_im, ROM_COPY)
        return
    if win_con == WinConditionComplex.dk_rap_items:
        item_im = getImageFile(ROM_COPY, 7, 0x3D3, False, 40, 40, TextureFormat.RGBA5551)
        item_im = item_im.resize((32, 32)).transpose(Image.FLIP_TOP_BOTTOM)
        writeWinConImage(settings, item_im, ROM_COPY)
        return
    if win_con == WinConditionComplex.kill_the_rabbit:
        output_image = Image.open(BytesIO(js.getFile("base-hack/assets/displays/kill_the_rabbit.png")))
        output_image = output_image.resize((32, 32))
        writeColorImageToROM(output_image, 14, 195, 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)
        return
    win_con_data = {
        WinConditionComplex.req_bp: WinConData(25, 0x1593, TextureFormat.RGBA5551, 48, 42, True, 40),
        WinConditionComplex.req_medal: WinConData(25, 0x156C, TextureFormat.RGBA5551, 44, 44, True, 40),
        WinConditionComplex.req_fairy: WinConData(25, 0x16ED, TextureFormat.RGBA32, 32, 32, True, 20),
        WinConditionComplex.req_key: WinConData(25, 0x16F6, TextureFormat.RGBA5551, 44, 44, True, 8),
        WinConditionComplex.req_companycoins: WinConData(25, 0x1718, TextureFormat.RGBA5551, 44, 44, True, 2),
        WinConditionComplex.req_crown: WinConData(25, 0x1707, TextureFormat.RGBA5551, 44, 44, True, 10),
        WinConditionComplex.req_gb: WinConData(25, 0x155C, TextureFormat.RGBA5551, 44, 44, True, 201),
        WinConditionComplex.req_pearl: WinConData(25, 0, TextureFormat.RGBA5551, 44, 44, True, 5),
        WinConditionComplex.req_rainbowcoin: WinConData(25, 0x174B, TextureFormat.RGBA5551, 48, 42, True, 16),
        WinConditionComplex.req_bosses: WinConData(25, 0xC9D, TextureFormat.RGBA5551, 48, 42, True, 7),
        WinConditionComplex.req_bonuses: WinConData(14, 0x2B, TextureFormat.RGBA32, 32, 32, False, 43),
    }
    if win_con not in win_con_data:
        return
    item_data = win_con_data[win_con]
    if win_con == WinConditionComplex.req_pearl:
        base_im = Image.open(BytesIO(js.getFile("base-hack/assets/arcade_jetpac/arcade/pearl.png")))
    else:
        item_im = getImageFile(
            ROM_COPY,
            item_data.table,
            item_data.image,
            item_data.table != 7,
            item_data.width,
            item_data.height,
            item_data.tex_format,
        )
        if item_data.flip:
            item_im = item_im.transpose(Image.FLIP_TOP_BOTTOM)
        dim = max(item_data.width, item_data.height)
        base_im = Image.new(mode="RGBA", size=(dim, dim))
        base_im.paste(item_im, (int((dim - item_data.width) >> 1), int((dim - item_data.height) >> 1)), item_im)
    base_im = base_im.resize((32, 32))
    num_im = numberToImage(settings.win_condition_count, (20, 20), ROM_COPY)
    base_im.paste(num_im, (6, 6), num_im)
    writeWinConImage(settings, base_im, ROM_COPY)
