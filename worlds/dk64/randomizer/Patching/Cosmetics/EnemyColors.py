"""All code changes associated with enemy color rando."""

import js
import gzip
import random
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Models import Model
from randomizer.Enums.Settings import RandomModels, ColorblindMode, ColorOptions
from randomizer.Patching.Library.Image import (
    getBonusSkinOffset,
    ExtraTextures,
    getRandomHueShift,
    getImageFile,
    TextureFormat,
    hueShift,
    hueShiftImageContainer,
    maskImageWithColor,
    writeColorImageToROM,
    getLuma,
    hueShiftColor,
)
from randomizer.Patching.Library.Generic import getValueFromByteArray, IsColorOptionSelected
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames, getRawFile
from randomizer.Patching.Patcher import ROM
from PIL import Image


def getEnemySwapColor(channel_min: int = 0, channel_max: int = 255, min_channel_variance: int = 0) -> int:
    """Get an RGB color compatible with enemy swaps."""
    channels = []
    for _ in range(2):
        channels.append(random.randint(channel_min, channel_max))
    min_channel = min(channels[0], channels[1])
    max_channel = max(channels[0], channels[1])
    bounds = []
    if (min_channel - channel_min) >= min_channel_variance:
        bounds.append([channel_min, min_channel])
    if (channel_max - max_channel) >= min_channel_variance:
        bounds.append([max_channel, channel_max])
    if (len(bounds) == 0) or ((max_channel - min_channel) >= min_channel_variance):
        # Default to random number pick
        channels.append(random.randint(channel_min, channel_max))
    else:
        selected_bound = random.choice(bounds)
        channels.append(random.randint(selected_bound[0], selected_bound[1]))
    random.shuffle(channels)
    value = 0
    for x in range(3):
        value <<= 8
        value += channels[x]
    return value


class EnemyColorSwap:
    """Class to store information regarding an enemy color swap."""

    def __init__(self, search_for: list, forced_color: int = None):
        """Initialize with given parameters."""
        self.search_for = search_for.copy()
        total_channels = [0] * 3
        for color in self.search_for:
            for channel in range(3):
                shift = 8 * (2 - channel)
                value = (color >> shift) & 0xFF
                total_channels[channel] += value
        average_channels = [int(x / len(self.search_for)) for x in total_channels]
        self.average_color = 0
        for x in average_channels:
            self.average_color <<= 8
            self.average_color += x
        self.replace_with = forced_color
        if forced_color is None:
            self.replace_with = getEnemySwapColor(80, min_channel_variance=80)

    def getOutputColor(self, color: int):
        """Get output color based on randomization."""
        if color not in self.search_for:
            return color
        if color == self.search_for[0]:
            return self.replace_with
        new_color = 0
        total_boost = 0
        for x in range(3):
            shift = 8 * (2 - x)
            provided_channel = (color >> shift) & 0xFF
            primary_channel = (self.search_for[0] >> shift) & 0xFF
            boost = 1  # Failsafe for div by 0
            if primary_channel != 0:
                boost = provided_channel / primary_channel
            total_boost += boost  # Used to get an average
        for x in range(3):
            shift = 8 * (2 - x)
            replacement_channel = (self.replace_with >> shift) & 0xFF
            replacement_channel = int(replacement_channel * (total_boost / 3))
            if replacement_channel > 255:
                replacement_channel = 255
            elif replacement_channel < 0:
                replacement_channel = 0
            new_color <<= 8
            new_color += replacement_channel
        return new_color


# Enemy texture data
FIRE_TEXTURES = (
    [0x1539, 0x1553, 32],  # Fireball. RGBA32 32x32
    [0x14B6, 0x14F5, 32],  # Fireball. RGBA32 32x32
    [0x1554, 0x155B, 16],  # Small Fireball. RGBA32 16x16
    [0x1654, 0x1683, 32],  # Fire Wall. RGBA32 32x32
    [0x1495, 0x14A0, 32],  # Small Explosion, RGBA32 32x32
    [0x13B9, 0x13C3, 32],  # Small Explosion, RGBA32 32x32
)
KLUMP_JACKET_TEXTURES = [
    {"image": 0x104D, "px": 1372},
    {"image": 0x1058, "px": 1372},
    {"image": 0x1059, "px": 176},
]
KLUMP_HAT_AMMO_TEXTURES = [
    {"image": 0x104E, "px": 1372},
    {"image": 0x104F, "px": 1372},
    {"image": 0x1050, "px": 1372},
    {"image": 0x1051, "px": 700},
    {"image": 0x1052, "px": 348},
    {"image": 0x1053, "px": 348},
]
KREMLING_TEXTURE_DIMENSIONS = [
    [32, 64],  # FCE
    [64, 24],  # FCF
    [1, 1372],  # fd0
    [32, 32],  # fd1
    [24, 8],  # fd2
    [24, 8],  # fd3
    [24, 8],  # fd4
    [24, 24],  # fd5
    [32, 32],  # fd6
    [32, 64],  # fd7
    [32, 64],  # fd8
    [36, 16],  # fd9
    [20, 28],  # fda
    [32, 32],  # fdb
    [32, 32],  # fdc
    [12, 28],  # fdd
    [64, 24],  # fde
    [32, 32],  # fdf
]
RABBIT_TEXTURE_DIMENSIONS = [
    [1, 1372],  # 111A
    [1, 1372],  # 111B
    [1, 700],  # 111C
    [1, 700],  # 111D
    [1, 1372],  # 111E
    [1, 1372],  # 111F
    [1, 1372],  # 1120
    [1, 1404],  # 1121
    [1, 348],  # 1122
    [32, 64],  # 1123
    [1, 688],  # 1124
    [64, 32],  # 1125
]
BEANSTALK_TEXTURE_FILE_SIZES = [
    0x480,
    0x480,
    0x480,
    0x2B8,
    0xAC0,
    0xAB8,
    0xAB8,
    0xAB8,
    0xAB8,
    0xAB8,
    0xAB8,
    0xAB8,
    0xAB8,
    0xAF8,
    0xAB8,
    0xAB8,
    0xAB8,
    0xAF8,
    0x578,
    0xAB8,
    0x578,
    0x5F8,
    0xAB8,
    0xAB8,
    0xAB8,
    0xAB8,
    0x578,
    0xAB8,
    0xAF8,
    0xAB8,
    0xAB8,
    0x560,
    0xAB8,
    0x2B8,
]
SCOFF_TEXTURE_DATA = {
    0xFB8: 0x55C,
    0xFB9: 0x800,
    0xFBA: 0x40,
    0xFBB: 0x800,
    0xFBC: 0x240,
    0xFBD: 0x480,
    0xFBE: 0x80,
    0xFBF: 0x800,
    0xFC0: 0x200,
    0xFC1: 0x240,
    0xFC2: 0x100,
    0xFB2: 0x240,
    0xFB3: 0x800,
    0xFB4: 0x800,
    0xFB5: 0x200,
    0xFB6: 0x200,
    0xFB7: 0x200,
}
TROFF_TEXTURE_DATA = {
    0xF78: 0x800,
    0xF79: 0x800,
    0xF7A: 0x800,
    0xF7B: 0x800,
    0xF7C: 0x800,
    0xF7D: 0x400,
    0xF7E: 0x600,
    0xF7F: 0x400,
    0xF80: 0x800,
    0xF81: 0x600,
    0xF82: 0x400,
    0xF83: 0x400,
    0xF84: 0x800,
    0xF85: 0x800,
    0xF86: 0x280,
    0xF87: 0x180,
    0xF88: 0x800,
    0xF89: 0x800,
    0xF8A: 0x400,
    0xF8B: 0x300,
    0xF8C: 0x800,
    0xF8D: 0x400,
    0xF8E: 0x500,
    0xF8F: 0x180,
}
SPIDER_TEXTURE_DIMENSIONS = {
    0x110A: (32, 64),
    0x110B: (32, 64),
    0x110C: (32, 64),
    0x110D: (64, 16),
    0x110E: (32, 64),
    0x110F: (32, 64),
    0x1110: (32, 64),
    0x1111: (32, 64),
    0x1112: (32, 64),
    0x1113: (16, 32),
    0x1114: (32, 32),
    0x1115: (32, 32),
    0x1116: (32, 32),
    0x1117: (64, 16),
    0x1118: (64, 32),
    0x1119: (64, 32),
}


def convertColorIntToTuple(color: int) -> tuple:
    """Convert color stored as 3-byte int to tuple."""
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)


def adjustFungiMushVertexColor(shift: int, ROM_COPY):
    """Adjust the special vertex coloring on Fungi Giant Mushroom."""
    fungi_geo = bytearray(getRawFile(ROM_COPY, TableNames.MapGeometry, Maps.FungiForest, True))
    DEFAULT_MUSHROOM_COLOR = (255, 90, 82)
    for x in range(0x27DA, 0x2839):
        start = 0x25140 + (x * 0x10) + 0xC
        channels = []
        is_zero = True
        for y in range(3):
            val = fungi_geo[start + y]
            if val != 0:
                is_zero = False
            channels.append(val)
        if is_zero:
            continue
        visual_color = [int((x / 255) * DEFAULT_MUSHROOM_COLOR[xi]) for xi, x in enumerate(channels)]
        luma = int(getLuma(visual_color))
        # Diversify shading
        luma -= 128
        luma = int(luma * 1.2)
        luma += 128
        # Brighten
        luma += 60
        # Clamp
        if luma < 0:
            luma = 0
        elif luma > 255:
            luma = 255
        # Apply shading
        for y in range(3):
            fungi_geo[start + y] = luma
        fungi_geo[start + 3] = 0xFF
    file_data = gzip.compress(fungi_geo, compresslevel=9)
    ROM_COPY.seek(getPointerLocation(TableNames.MapGeometry, Maps.FungiForest))
    ROM_COPY.writeBytes(file_data)


def writeMiscCosmeticChanges(settings, ROM_COPY: ROM):
    """Write miscellaneous changes to the cosmetic colors."""
    enemy_changes = {}
    mush_man_shift = getRandomHueShift()
    if IsColorOptionSelected(settings, ColorOptions.enemies):
        # Barrel Enemy Skins - Random
        klobber_shift = getRandomHueShift(0, 300)
        kaboom_shift = getRandomHueShift()
        for img_index in range(3):
            px_count = 1404 if img_index < 2 else 1372
            hueShiftImageContainer(25, 0xF12 + img_index, 1, px_count, TextureFormat.RGBA5551, klobber_shift, ROM_COPY)
            hueShiftImageContainer(25, 0xF22 + img_index, 1, px_count, TextureFormat.RGBA5551, kaboom_shift, ROM_COPY)
            if img_index < 2:
                hueShiftImageContainer(25, 0xF2B + img_index, 1, px_count, TextureFormat.RGBA5551, kaboom_shift, ROM_COPY)
        # Klump
        klump_jacket_shift = getRandomHueShift()
        for img_data in KLUMP_JACKET_TEXTURES:
            hueShiftImageContainer(25, img_data["image"], 1, img_data["px"], TextureFormat.RGBA5551, klump_jacket_shift, ROM_COPY)
        klump_hatammo_shift = getRandomHueShift()
        for img_data in KLUMP_HAT_AMMO_TEXTURES:
            hueShiftImageContainer(25, img_data["image"], 1, img_data["px"], TextureFormat.RGBA5551, klump_hatammo_shift, ROM_COPY)
        # Pufftup
        pufftup_shift = getRandomHueShift()
        for img_index in range(0x11E5, 0x11EB + 1):
            px_count = 348
            if img_index == 0x11E7:
                px_count = 696
            elif img_index in (0x11E5, 0x11E6):
                px_count = 1372
            hueShiftImageContainer(25, img_index, 1, px_count, TextureFormat.RGBA5551, pufftup_shift, ROM_COPY)
        # Kosha
        kosha_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x1232, 1, 348, TextureFormat.RGBA5551, kosha_shift, ROM_COPY)
        hueShiftImageContainer(25, 0x1235, 1, 348, TextureFormat.RGBA5551, kosha_shift, ROM_COPY)
        kosha_helmet_int = getEnemySwapColor(80, min_channel_variance=80)
        kosha_helmet_list = [
            (kosha_helmet_int >> 16) & 0xFF,
            (kosha_helmet_int >> 8) & 0xFF,
            kosha_helmet_int & 0xFF,
        ]
        kosha_club_int = getEnemySwapColor(80, min_channel_variance=80)
        kosha_club_list = [(kosha_club_int >> 16) & 0xFF, (kosha_club_int >> 8) & 0xFF, kosha_club_int & 0xFF]
        for img in range(0x122E, 0x1230):
            kosha_im = getImageFile(ROM_COPY, 25, img, True, 1, 1372, TextureFormat.RGBA5551)
            kosha_im = maskImageWithColor(kosha_im, tuple(kosha_helmet_list))
            writeColorImageToROM(kosha_im, 25, img, 1, 1372, False, TextureFormat.RGBA5551, ROM_COPY)
        for img in range(0x1229, 0x122C):
            kosha_im = getImageFile(ROM_COPY, 25, img, True, 1, 1372, TextureFormat.RGBA5551)
            kosha_im = maskImageWithColor(kosha_im, tuple(kosha_club_list))
            writeColorImageToROM(kosha_im, 25, img, 1, 1372, False, TextureFormat.RGBA5551, ROM_COPY)
        if settings.colorblind_mode == ColorblindMode.off:
            # Kremling
            while True:
                kremling_shift = getRandomHueShift()
                # Block red coloring
                if kremling_shift > 290:
                    break
                if kremling_shift > -70 and kremling_shift < 228:
                    break
                if kremling_shift < -132:
                    break
            for dim_index, dims in enumerate(KREMLING_TEXTURE_DIMENSIONS):
                if dims is not None:
                    hueShiftImageContainer(25, 0xFCE + dim_index, dims[0], dims[1], TextureFormat.RGBA5551, kremling_shift, ROM_COPY)
        # Krobot
        spinner_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xFA9, 1, 1372, TextureFormat.RGBA5551, spinner_shift, ROM_COPY)
        krobot_textures = [[[1, 1372], [0xFAF, 0xFAA, 0xFA8, 0xFAB, 0xFAD]], [[32, 32], [0xFAC, 0xFB1, 0xFAE, 0xFB0]]]
        krobot_color_int = getEnemySwapColor(80, min_channel_variance=80)
        krobot_color_list = [(krobot_color_int >> 16) & 0xFF, (krobot_color_int >> 8) & 0xFF, krobot_color_int & 0xFF]
        for tex_set in krobot_textures:
            for tex in tex_set[1]:
                krobot_im = getImageFile(ROM_COPY, 25, tex, True, tex_set[0][0], tex_set[0][1], TextureFormat.RGBA5551)
                krobot_im = maskImageWithColor(krobot_im, tuple(krobot_color_list))
                writeColorImageToROM(krobot_im, 25, tex, tex_set[0][0], tex_set[0][1], False, TextureFormat.RGBA5551, ROM_COPY)
        # Ghost
        ghost_shift = getRandomHueShift()
        for img in range(0x119D, 0x11AF):
            px_count = 1372
            if img == 0x119E:
                px_count = 176
            elif img == 0x11AC:
                px_count = 688
            hueShiftImageContainer(25, img, 1, px_count, TextureFormat.RGBA5551, ghost_shift, ROM_COPY)
        # Zinger
        zinger_shift = getRandomHueShift()
        zinger_color = hueShiftColor((0xFF, 0xFF, 0x0A), zinger_shift)
        zinger_color_int = (zinger_color[0] << 16) | (zinger_color[1] << 8) | (zinger_color[2])
        hueShiftImageContainer(25, 0xF0A, 1, 1372, TextureFormat.RGBA5551, zinger_shift, ROM_COPY)
        # Mechazinger, use zinger color
        for img_index in (0x10A0, 0x10A2, 0x10A4, 0x10A5):
            hueShiftImageContainer(25, img_index, 1, 1372, TextureFormat.RGBA5551, zinger_shift, ROM_COPY)
        hueShiftImageContainer(25, 0x10A3, 32, 32, TextureFormat.RGBA32, zinger_shift, ROM_COPY)
        # Spider
        spider_shift = getRandomHueShift()
        for img_index in SPIDER_TEXTURE_DIMENSIONS:
            hueShiftImageContainer(
                25,
                img_index,
                SPIDER_TEXTURE_DIMENSIONS[img_index][0],
                SPIDER_TEXTURE_DIMENSIONS[img_index][1],
                TextureFormat.RGBA5551,
                spider_shift,
                ROM_COPY,
            )
        # Mushroom Men
        for img_index in (0x11FC, 0x11FD, 0x11FE, 0x11FF, 0x1200, 0x1209, 0x120A, 0x120B):
            hueShiftImageContainer(25, img_index, 1, 1372, TextureFormat.RGBA5551, mush_man_shift, ROM_COPY)
        for img_index in (0x11F8, 0x1205):
            hueShiftImageContainer(25, img_index, 1, 692, TextureFormat.RGBA5551, mush_man_shift, ROM_COPY)
        blue_beaver_color = getEnemySwapColor(80, min_channel_variance=80)
        enemy_changes[Model.BeaverBlue_LowPoly] = EnemyColorSwap([0xB2E5FF, 0x65CCFF, 0x00ABE8, 0x004E82, 0x008BD1, 0x001333, 0x1691CE], blue_beaver_color)  # Primary
        enemy_changes[Model.BeaverBlue] = EnemyColorSwap([0xB2E5FF, 0x65CCFF, 0x00ABE8, 0x004E82, 0x008BD1, 0x001333, 0x1691CE], blue_beaver_color)  # Primary
        enemy_changes[Model.BeaverGold] = EnemyColorSwap([0xFFE5B2, 0xFFCC65, 0xE8AB00, 0x824E00, 0xD18B00, 0x331300, 0xCE9116])  # Primary
        enemy_changes[Model.Zinger] = EnemyColorSwap([0xFFFF0A, 0xFF7F00], zinger_color_int)  # Legs
        enemy_changes[Model.RoboZinger] = EnemyColorSwap([0xFFFF00, 0xFF5500], zinger_color_int)  # Legs
        enemy_changes[Model.Kasplat] = EnemyColorSwap([0x8FD8FF, 0x182A4F, 0x0B162C, 0x7A98D3, 0x3F6CC4, 0x8FD8FF, 0x284581])
        enemy_changes[Model.Klump] = EnemyColorSwap([0xE66B78, 0x621738, 0x300F20, 0xD1426F, 0xA32859])
    if IsColorOptionSelected(settings, ColorOptions.bosses):
        # Pufftoss
        pufftoss_shift = getRandomHueShift()
        for img_index in range(0x105C, 0x1069 + 1):
            if img_index in (0x1066, 0x1067, 0x1068):
                continue
            px_count = 1372
            if img_index in (0x1060, 0x1065):
                px_count = 348
            elif img_index in (0x1061, 0x1062):
                px_count = 700
            hueShiftImageContainer(25, img_index, 1, px_count, TextureFormat.RGBA5551, pufftoss_shift, ROM_COPY)
        # K Rool
        red_cs_im = Image.new(mode="RGBA", size=(32, 32), color=convertColorIntToTuple(getEnemySwapColor()))
        shorts_im = Image.new(mode="RGBA", size=(32, 32), color=convertColorIntToTuple(getEnemySwapColor()))
        glove_im = Image.new(mode="RGBA", size=(32, 32), color=convertColorIntToTuple(getEnemySwapColor()))
        skin_im = Image.new(mode="RGBA", size=(32, 32), color=convertColorIntToTuple(getEnemySwapColor(80, min_channel_variance=80)))
        krool_data = {
            0x1149: red_cs_im,
            0x1261: shorts_im,
            0xDA8: glove_im,
            0x114A: skin_im,
            0x114D: skin_im,
        }
        for index in krool_data:
            writeColorImageToROM(krool_data[index], 25, index, 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)
        toe_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x126E, 1, 1372, TextureFormat.RGBA5551, toe_shift, ROM_COPY)
        hueShiftImageContainer(25, 0x126F, 1, 1372, TextureFormat.RGBA5551, toe_shift, ROM_COPY)
        gold_shift = getRandomHueShift()  # belt
        hueShiftImageContainer(25, 0x1265, 32, 32, TextureFormat.RGBA5551, gold_shift, ROM_COPY)
        hueShiftImageContainer(25, 0x1148, 32, 32, TextureFormat.RGBA5551, gold_shift, ROM_COPY)
        # Army Dillo
        dillo_px_count = {
            0x102D: 64 * 32,
            0x103A: 16 * 16,
            0x102A: 24 * 24,
            0x102B: 24 * 24,
            0x102C: 1372,
            0x103D: 688,
            0x103E: 688,
        }
        dillo_shift = getRandomHueShift()
        for img, px_count in dillo_px_count.items():
            hueShiftImageContainer(25, img, 1, px_count, TextureFormat.RGBA5551, dillo_shift, ROM_COPY)
        # Dogadon
        dogadon_color = getEnemySwapColor(80, 160, min_channel_variance=80)
        enemy_changes[Model.Dogadon] = EnemyColorSwap(
            [
                0xFF0000,
                0xFF7F00,
                0x450A1F,
                0xB05800,
                0xFF3200,
                0xFFD400,
                0x4F260D,
                0x600F00,
                0x6A1400,
                0xAA0000,
                0xDF3F1F,
                0xFF251F,
                0x8F4418,
                0x522900,
                0xDF9F1F,
                0x3B0606,
                0x91121E,
                0x700C0D,
                0xFF5900,
                0xFF7217,
                0xFF7425,
                0xFF470B,
                0xA82100,
                0x4A0D18,
                0x580E00,
                0x461309,
                0x4C1503,
                0x780D0E,
                0xFFA74A,
                0x7E120F,
                0x700000,
                0xB64D19,
                0x883A13,
                0xBD351A,
                0xD42900,
                0xFF2A00,
                0x921511,
                0x9C662D,
                0xDF5F1F,
                0x9B1112,
                0x461F0A,
                0x4B0808,
                0x500809,
                0xA42000,
                0x5F0B13,
                0xBF6A3F,
                0x602E10,
                0x971414,
                0x422C15,
                0xFC5800,
                0x5C0D0B,
            ],
            dogadon_color,
        )
        enemy_changes[Model.Laser] = EnemyColorSwap([0xF30000])
    if IsColorOptionSelected(settings, ColorOptions.fire):
        # Fire-based sprites
        fire_shift = getRandomHueShift()
        for sprite_data in FIRE_TEXTURES:
            for img_index in range(sprite_data[0], sprite_data[1] + 1):
                dim = sprite_data[2]
                hueShiftImageContainer(25, img_index, dim, dim, TextureFormat.RGBA32, fire_shift, ROM_COPY)
        for img_index in range(0x29, 0x32 + 1):
            hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA32, fire_shift, ROM_COPY)
        for img_index in range(0x250, 0x26F + 1):
            hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA32, fire_shift, ROM_COPY)
        for img_index in range(0xA0, 0xA7 + 1):
            hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA5551, fire_shift, ROM_COPY)
        # Blue Fire
        for img_index in range(129, 138 + 1):
            hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA32, fire_shift, ROM_COPY)
    if IsColorOptionSelected(settings, ColorOptions.friendly_npcs):
        # Rabbit
        rabbit_shift = getRandomHueShift()
        for dim_index, dims in enumerate(RABBIT_TEXTURE_DIMENSIONS):
            if dims is not None:
                hueShiftImageContainer(25, 0x111A + dim_index, dims[0], dims[1], TextureFormat.RGBA5551, rabbit_shift, ROM_COPY)
        # Snake
        snake_shift = getRandomHueShift()
        for x in range(2):
            hueShiftImageContainer(25, 0xEF7 + x, 32, 32, TextureFormat.RGBA5551, snake_shift, ROM_COPY)
        # Beanstalk
        beanstalk_shift = getRandomHueShift()
        for index, size in enumerate(BEANSTALK_TEXTURE_FILE_SIZES):
            hueShiftImageContainer(25, 0x1126 + index, 1, int(size >> 1), TextureFormat.RGBA5551, beanstalk_shift, ROM_COPY)
        # Funky
        funky_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xECF, 1, 1372, TextureFormat.RGBA5551, funky_shift, ROM_COPY)
        hueShiftImageContainer(25, 0xED6, 1, 1372, TextureFormat.RGBA5551, funky_shift, ROM_COPY)
        hueShiftImageContainer(25, 0xEDF, 1, 1372, TextureFormat.RGBA5551, funky_shift, ROM_COPY)
        enemy_changes[Model.Candy] = EnemyColorSwap(
            [
                0xFF96EB,
                0x572C58,
                0xB86CAA,
                0xEB4C91,
                0x8B2154,
                0xD13B80,
                0xFF77C1,
                0xFF599E,
                0x7F1E4C,
                0x61173A,
                0x902858,
                0xA42E64,
                0x791C49,
                0x67183E,
                0x9E255C,
                0xC12E74,
                0x572C58,
                0xFF96EB,
                0xB86CAA,
            ]
        )
        scoff_shift = getRandomHueShift()
        troff_shift = getRandomHueShift()

        for img in SCOFF_TEXTURE_DATA:
            hueShiftImageContainer(25, img, 1, SCOFF_TEXTURE_DATA[img], TextureFormat.RGBA5551, scoff_shift, ROM_COPY)

        # Scoff had too many bananas, and passed potassium poisoning onto Troff
        # https://i.imgur.com/WFDLSzA.png
        # for img in TROFF_TEXTURE_DATA:
        #     hueShiftImageContainer(25, img, 1, TROFF_TEXTURE_DATA[img], TextureFormat.RGBA5551, troff_shift, ROM_COPY)

        # enemy_changes[Model.BananaFairy] = EnemyColorSwap([0xFFD400, 0xFFAA00, 0xFCD200, 0xD68F00, 0xD77D0A, 0xe49800, 0xdf7f1f, 0xa26c00, 0xd6b200, 0xdf9f1f])
    if IsColorOptionSelected(settings, ColorOptions.environment):
        # Mushrooms
        for img_index in (0x67F, 0x680):
            hueShiftImageContainer(25, img_index, 32, 64, TextureFormat.RGBA5551, mush_man_shift, ROM_COPY)
        hueShiftImageContainer(25, 0x6F3, 4, 4, TextureFormat.RGBA5551, mush_man_shift, ROM_COPY)
        adjustFungiMushVertexColor(mush_man_shift, ROM_COPY)
        # Pendulum Bob
        pendulum_shift = getRandomHueShift()
        for index in range(0x2B6, 0x2E1 + 1):
            hueShiftImageContainer(TableNames.TexturesUncompressed, index, 32, 32, TextureFormat.RGBA5551, pendulum_shift, ROM_COPY)
        # Gong
        gong_shift = getRandomHueShift()
        for index in range(0x1D4, 0x1EF + 1):
            hueShiftImageContainer(TableNames.TexturesUncompressed, index, 32, 32, TextureFormat.RGBA5551, gong_shift, ROM_COPY)
        # Number Game Numbers
        if settings.colorblind_mode == ColorblindMode.off:
            colors = [getRandomHueShift() for _ in range(2)]
            vanilla_blue = [1, 3, 6, 8, 11, 14, 15, 16]
            for x in range(16):
                number_hue_shift = colors[0]
                if (x + 1) in vanilla_blue:
                    number_hue_shift = colors[1]
                for sub_img in range(2):
                    img_index = 0x1FE + (2 * x) + sub_img
                    hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA5551, number_hue_shift, ROM_COPY)
            hueShiftImageContainer(25, 0xC2D, 32, 32, TextureFormat.RGBA5551, colors[1], ROM_COPY)
            hueShiftImageContainer(25, 0xC2E, 32, 32, TextureFormat.RGBA5551, colors[0], ROM_COPY)
        hueShiftImageContainer(TableNames.TexturesGeometry, 0x2EA, 4, 4, TextureFormat.RGBA5551, getRandomHueShift(), ROM_COPY)
        rail_color = getEnemySwapColor(min_channel_variance=200)
        rail_color_list = [(rail_color >> 16) & 0xFF, (rail_color >> 8) & 0xFF, rail_color & 0xFF]
        for palette in (0x86B, 0x86D):
            pal_im = getImageFile(ROM_COPY, TableNames.TexturesGeometry, palette, True, 4, 4, TextureFormat.RGBA5551)
            pal_im = maskImageWithColor(pal_im, tuple(rail_color_list))
            writeColorImageToROM(pal_im, TableNames.TexturesGeometry, palette, 4, 4, False, TextureFormat.RGBA5551, ROM_COPY)

    if IsColorOptionSelected(settings, ColorOptions.playable_characters):
        # Jetman
        for xi, x in enumerate(settings.jetman_color):
            ROM_COPY.seek(settings.rom_data + 0x1E8 + xi)
            ROM_COPY.writeMultipleBytes(x, 1)
    if IsColorOptionSelected(settings, ColorOptions.particles):
        # Shockwave Particles
        shockwave_shift = getRandomHueShift()
        for img_index in range(0x174F, 0x1757):
            hueShiftImageContainer(25, img_index, 16, 16, TextureFormat.RGBA32, shockwave_shift, ROM_COPY)
        # Fairy Particles Sprites
        fairy_particles_shift = getRandomHueShift()
        for x in range(0xB):
            hueShiftImageContainer(25, 0x138D + x, 32, 32, TextureFormat.RGBA32, fairy_particles_shift, ROM_COPY)
        # Sparkle Particles
        for index in range(3):
            sparkle_shift = getRandomHueShift()
            start_index = 0x13D6 + (8 * index)
            end_index = start_index + 8
            for img_index in range(start_index, end_index):
                hueShiftImageContainer(TableNames.TexturesGeometry, img_index, 16, 16, TextureFormat.RGBA32, sparkle_shift, ROM_COPY)
        sparkle_shift = getRandomHueShift()
        for index in range(0x3CA, 0x3D1 + 1):
            hueShiftImageContainer(TableNames.TexturesUncompressed, index, 32, 32, TextureFormat.RGBA32, sparkle_shift, ROM_COPY)
        hueShiftImageContainer(TableNames.TexturesGeometry, 0x1484, 32, 32, TextureFormat.RGBA32, getRandomHueShift(), ROM_COPY)
    if IsColorOptionSelected(settings, ColorOptions.items):
        # Headphones Sprite
        headphones_shift = getRandomHueShift()
        for x in range(8):
            hueShiftImageContainer(7, 0x3D3 + x, 40, 40, TextureFormat.RGBA5551, headphones_shift, ROM_COPY)
        race_coin_shift = getRandomHueShift()
        for x in range(8):
            hueShiftImageContainer(7, 0x1F0 + x, 48, 42, TextureFormat.RGBA5551, race_coin_shift, ROM_COPY)
        # Melon HUD
        data = {
            TableNames.TexturesUncompressed: [[0x13C, 0x147]],
            TableNames.TexturesHUD: [[0x5A, 0x5D]],
            TableNames.TexturesGeometry: [
                [getBonusSkinOffset(ExtraTextures.MelonSurface), getBonusSkinOffset(ExtraTextures.MelonSurface)],
                [0x144B, 0x1452],
            ],
        }
        shift = getRandomHueShift()
        for table in data:
            table_data = data[table]
            for set in table_data:
                for img in range(set[0], set[1] + 1):
                    if table == TableNames.TexturesGeometry:
                        dims = (32, 32)
                    else:
                        dims = (48, 42)
                    melon_im = getImageFile(ROM_COPY, table, img, table != 7, dims[0], dims[1], TextureFormat.RGBA5551)
                    melon_im = hueShift(melon_im, shift)
                    melon_px = melon_im.load()
                    bytes_array = []
                    for y in range(dims[1]):
                        for x in range(dims[0]):
                            pix_data = list(melon_px[x, y])
                            red = int((pix_data[0] >> 3) << 11)
                            green = int((pix_data[1] >> 3) << 6)
                            blue = int((pix_data[2] >> 3) << 1)
                            alpha = int(pix_data[3] != 0)
                            value = red | green | blue | alpha
                            bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
                    px_data = bytearray(bytes_array)
                    if table != TableNames.TexturesUncompressed:
                        px_data = gzip.compress(px_data, compresslevel=9)
                    ROM_COPY.seek(getPointerLocation(table, img))
                    ROM_COPY.writeBytes(px_data)
        # Crowns & Keys
        new_key_crown_color = []
        for _ in range(3):
            new_key_crown_color.append(settings.random.randint(0, 0xFF))
        for img_index in (0xC6F, 0xBAB, 0x132D, getBonusSkinOffset(ExtraTextures.MedalRim), 0xBAA):
            dim = 32
            if img_index in (0xC6F, 0xBAA):
                dim = 4
            shine_img = getImageFile(ROM_COPY, 25, img_index, True, dim, dim, TextureFormat.RGBA5551)
            shine_img = maskImageWithColor(shine_img, tuple(new_key_crown_color))
            writeColorImageToROM(shine_img, 25, img_index, dim, dim, False, TextureFormat.RGBA5551, ROM_COPY)
        min_rgb = min(new_key_crown_color[0], new_key_crown_color[1], new_key_crown_color[2])
        max_rgb = max(new_key_crown_color[0], new_key_crown_color[1], new_key_crown_color[2])
        is_greyscale = (max_rgb - min_rgb) < 50
        fake_item_color = list(hueShiftColor(tuple(new_key_crown_color), 60, 1750))
        delta_mag = 80
        if is_greyscale:
            delta = -delta_mag
            if max_rgb < 128:
                delta = delta_mag
            for x in range(3):
                fake_item_color[x] = new_key_crown_color[x] + delta
        for img_index in (ExtraTextures.FakeKey, ExtraTextures.FakeKeyPalette):
            dim = 32
            if img_index == ExtraTextures.FakeKeyPalette:
                dim = 4
            shine_img = getImageFile(ROM_COPY, 25, getBonusSkinOffset(img_index), True, dim, dim, TextureFormat.RGBA5551)
            shine_img = maskImageWithColor(shine_img, tuple(fake_item_color))
            writeColorImageToROM(shine_img, 25, getBonusSkinOffset(img_index), dim, dim, False, TextureFormat.RGBA5551, ROM_COPY)
    if IsColorOptionSelected(settings, ColorOptions.barrels_and_boulders):
        boulder_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x12F4, 1, 1372, TextureFormat.RGBA5551, boulder_shift, ROM_COPY)
        for img_index in range(2):
            hueShiftImageContainer(25, 0xDE1 + img_index, 32, 64, TextureFormat.RGBA5551, boulder_shift, ROM_COPY)
        # Blast Barrels
        blast_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x127E, 1, 1372, TextureFormat.RGBA5551, blast_shift, ROM_COPY)
        for x in range(4):
            hueShiftImageContainer(25, 0x127F + x, 16, 64, TextureFormat.RGBA5551, blast_shift, ROM_COPY)
        hueShiftImageContainer(25, getBonusSkinOffset(ExtraTextures.BlastTop), 1, 1372, TextureFormat.RGBA5551, blast_shift, ROM_COPY)
    if IsColorOptionSelected(settings, ColorOptions.misc_objects):
        # Instruments
        trombone_sax_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xEA2, 32, 32, TextureFormat.RGBA5551, trombone_sax_shift, ROM_COPY)  # Shine
        hueShiftImageContainer(25, 0x15AF, 40, 40, TextureFormat.RGBA5551, trombone_sax_shift, ROM_COPY)  # Trombone Icon
        hueShiftImageContainer(25, 0x15AD, 40, 40, TextureFormat.RGBA5551, trombone_sax_shift, ROM_COPY)  # Sax Icon
        hueShiftImageContainer(25, 0xBCC, 32, 64, TextureFormat.RGBA5551, trombone_sax_shift, ROM_COPY)  # Sax (Pad)
        hueShiftImageContainer(25, 0xBCD, 32, 64, TextureFormat.RGBA5551, trombone_sax_shift, ROM_COPY)  # Sax (Pad)
        hueShiftImageContainer(25, 0xBD0, 32, 64, TextureFormat.RGBA5551, trombone_sax_shift, ROM_COPY)  # Trombone (Pad)
        hueShiftImageContainer(25, 0xBD1, 32, 64, TextureFormat.RGBA5551, trombone_sax_shift, ROM_COPY)  # Trombone (Pad)
        triangle_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xEBF, 32, 32, TextureFormat.RGBA5551, triangle_shift, ROM_COPY)  # Shine
        hueShiftImageContainer(25, 0x15AE, 40, 40, TextureFormat.RGBA5551, triangle_shift, ROM_COPY)  # Triangle Icon
        hueShiftImageContainer(25, 0xBCE, 32, 64, TextureFormat.RGBA5551, triangle_shift, ROM_COPY)  # Triangle (Pad)
        hueShiftImageContainer(25, 0xBCF, 32, 64, TextureFormat.RGBA5551, triangle_shift, ROM_COPY)  # Triangle (Pad)
        bongo_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x1317, 1, 1372, TextureFormat.RGBA5551, bongo_shift, ROM_COPY)  # Skin
        hueShiftImageContainer(25, 0x1318, 1, 1404, TextureFormat.RGBA5551, bongo_shift, ROM_COPY)  # Side
        hueShiftImageContainer(25, 0x1319, 1, 1404, TextureFormat.RGBA5551, bongo_shift, ROM_COPY)  # Side 2
        hueShiftImageContainer(25, 0x15AC, 40, 40, TextureFormat.RGBA5551, bongo_shift, ROM_COPY)  # Bongo Icon
        hueShiftImageContainer(25, 0xBC8, 32, 64, TextureFormat.RGBA5551, bongo_shift, ROM_COPY)  # Bongo (Pad)
        hueShiftImageContainer(25, 0xBC9, 32, 64, TextureFormat.RGBA5551, bongo_shift, ROM_COPY)  # Bongo (Pad)
        # Rings/DK Star
        ring_shift = getRandomHueShift()
        for x in range(2):
            hueShiftImageContainer(25, 0xE1C + x, 1, 344, TextureFormat.RGBA5551, ring_shift, ROM_COPY)
            hueShiftImageContainer(25, 0xD38 + x, 64, 32, TextureFormat.RGBA5551, ring_shift, ROM_COPY)
        hueShiftImageContainer(7, 0x2EB, 32, 32, TextureFormat.RGBA5551, ring_shift, ROM_COPY)
        # Buoys
        for x in range(2):
            hueShiftImageContainer(25, 0x133A + x, 1, 1372, TextureFormat.RGBA5551, getRandomHueShift(), ROM_COPY)
        # Trap Bubble
        hueShiftImageContainer(25, 0x134C, 32, 32, TextureFormat.RGBA5551, getRandomHueShift(), ROM_COPY)
        # Slam Switch Borders
        green_switch_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xBAD, 64, 16, TextureFormat.RGBA5551, green_switch_shift, ROM_COPY)
        hueShiftImageContainer(25, 0xBAE, 64, 16, TextureFormat.RGBA5551, green_switch_shift, ROM_COPY)
        blue_switch_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xD01, 64, 16, TextureFormat.RGBA5551, blue_switch_shift, ROM_COPY)
        hueShiftImageContainer(25, 0xD02, 64, 16, TextureFormat.RGBA5551, blue_switch_shift, ROM_COPY)

    for enemy in enemy_changes:
        file_data = bytearray(getRawFile(ROM_COPY, 5, enemy, True))
        vert_start = 0x28
        file_head = getValueFromByteArray(file_data, 0, 4)
        disp_list_end = (getValueFromByteArray(file_data, 4, 4) - file_head) + 0x28
        vert_end = (getValueFromByteArray(file_data, disp_list_end, 4) - file_head) + 0x28
        vert_count = int((vert_end - vert_start) / 0x10)
        for vert in range(vert_count):
            local_start = 0x28 + (0x10 * vert)
            test_rgb = getValueFromByteArray(file_data, local_start + 0xC, 3)
            new_rgb = enemy_changes[enemy].getOutputColor(test_rgb)
            for x in range(3):
                shift = 8 * (2 - x)
                channel = (new_rgb >> shift) & 0xFF
                file_data[local_start + 0xC + x] = channel
        file_data = gzip.compress(file_data, compresslevel=9)
        ROM_COPY.seek(getPointerLocation(TableNames.ActorGeometry, enemy))
        ROM_COPY.writeBytes(file_data)


def writeRainbowAmmo(settings, ROM_COPY: ROM):
    """Desaturate all ammo textures so that they look good with rainbow ammo."""
    if not settings.rainbow_ammo:
        return
    entries = [
        {
            # Coconut
            "first": 0x2A3,
            "last": 0x2B2,
            "table": TableNames.TexturesUncompressed,
            "width": 0x28,
            "height": 0x33,
        },
        {
            # Peanut
            "first": 0x1474,
            "last": 0x1483,
            "table": TableNames.TexturesGeometry,
            "width": 0x20,
            "height": 0x20,
        },
        {
            # Grape
            "first": 0x1506,
            "last": 0x1514,
            "table": TableNames.TexturesGeometry,
            "width": 0x20,
            "height": 0x20,
        },
        {
            # Grape
            "first": 0x12E1,
            "last": 0x12E1,
            "table": TableNames.TexturesGeometry,
            "width": 0x20,
            "height": 0x20,
        },
        {
            # Feather
            "first": 0x15A3,
            "last": 0x15AA,
            "table": TableNames.TexturesGeometry,
            "width": 0x20,
            "height": 0x20,
        },
        {
            # Feather Custom Sprite
            "first": getBonusSkinOffset(ExtraTextures.Feather0),
            "last": getBonusSkinOffset(ExtraTextures.Feather7),
            "table": TableNames.TexturesGeometry,
            "width": 0x20,
            "height": 0x20,
        },
        {
            # Pineapple
            "first": 0x12E5,
            "last": 0x12E5,
            "table": TableNames.TexturesGeometry,
            "width": 0x20,
            "height": 0x30,
        },
        {
            # Pineapple
            "first": 0x14A7,
            "last": 0x14B5,
            "table": TableNames.TexturesGeometry,
            "width": 0x20,
            "height": 0x30,
        },
    ]
    for entry in entries:
        delta = entry["last"] - entry["first"]
        table = entry["table"]
        for x in range(delta + 1):
            file = entry["first"] + x
            im_f = getImageFile(ROM_COPY, table, file, table != TableNames.TexturesUncompressed, entry["width"], entry["height"], TextureFormat.RGBA5551)
            if im_f.mode != "RGBA":
                im_f = im_f.convert("RGBA")
            r, g, b, a = im_f.split()
            rgb = Image.merge("RGB", (r, g, b))
            gray = rgb.convert("L")
            # Recombine with alpha
            desat_im_f = Image.merge("RGBA", (gray, gray, gray, a))
            writeColorImageToROM(desat_im_f, table, file, entry["width"], entry["height"], False, TextureFormat.RGBA5551, ROM_COPY)
