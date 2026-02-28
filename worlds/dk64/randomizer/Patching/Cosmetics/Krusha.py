"""All code associated with Krusha."""

import js
import zlib
import gzip
from typing import TYPE_CHECKING
from randomizer.Settings import Settings
from randomizer.Enums.Settings import ColorblindMode
from randomizer.Patching.Library.Generic import getObjectAddress
from randomizer.Patching.Library.DataTypes import float_to_hex, intf_to_float, int_to_list
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Image import (
    writeColorImageToROM,
    getImageFile,
    getBonusSkinOffset,
    ExtraTextures,
    TextureFormat,
)
from randomizer.Patching.Library.Assets import TableNames, getRawFile, writeRawFile
from randomizer.Enums.Kongs import Kongs
from PIL import Image

DK_SCALE = 0.75
GENERIC_SCALE = 0.49
krusha_scaling = [
    # [x, y, z, xz, y]
    # DK
    [
        lambda x: x * DK_SCALE,
        lambda x: x * DK_SCALE,
        lambda x: x * GENERIC_SCALE,
        lambda x: x * DK_SCALE,
        lambda x: x * DK_SCALE,
    ],
    # Diddy
    [
        lambda x: (x * 1.043) - 41.146,
        lambda x: (x * 9.893) - 8.0,
        lambda x: x * GENERIC_SCALE,
        lambda x: (x * 1.103) - 14.759,
        lambda x: (x * 0.823) + 35.220,
    ],
    # Lanky
    [
        lambda x: (x * 0.841) - 17.231,
        lambda x: (x * 6.925) - 2.0,
        lambda x: x * GENERIC_SCALE,
        lambda x: (x * 0.680) - 18.412,
        lambda x: (x * 0.789) + 42.138,
    ],
    # Tiny
    [
        lambda x: (x * 0.632) + 7.590,
        lambda x: (x * 6.925) + 0.0,
        lambda x: x * GENERIC_SCALE,
        lambda x: (x * 1.567) - 21.676,
        lambda x: (x * 0.792) + 41.509,
    ],
    # Chunky
    [lambda x: x, lambda x: x, lambda x: x, lambda x: x, lambda x: x],
]


def readListAsInt(arr: list, start: int, size: int) -> int:
    """Read list and convert to int."""
    val = 0
    for i in range(size):
        val = (val * 256) + arr[start + i]
    return val


kong_index_mapping = {
    # Regular model, instrument model
    Kongs.donkey: (3, None),
    Kongs.diddy: (0, 1),
    Kongs.lanky: (5, 6),
    Kongs.tiny: (8, 9),
    Kongs.chunky: (11, 12),
}


def fixModelSmallKongCollision(kong_index: int, ROM_COPY: LocalROM):
    """Modify Krusha Model to be smaller to enable him to fit through smaller gaps."""
    for x in range(2):
        file = kong_index_mapping[kong_index][x]
        if file is None:
            continue
        data = getRawFile(ROM_COPY, TableNames.ActorGeometry, file, True)
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        head = readListAsInt(num_data, 0, 4)
        ptr = readListAsInt(num_data, 0xC, 4)
        base = (ptr - head) + 0x28 + 8
        count_0 = readListAsInt(num_data, base, 4)
        changes = krusha_scaling[kong_index][:3]
        changes_0 = [
            krusha_scaling[kong_index][3],
            krusha_scaling[kong_index][4],
            krusha_scaling[kong_index][3],
        ]
        for i in range(count_0):
            i_start = base + 4 + (i * 0x14)
            for coord_index, change in enumerate(changes):
                val_i = readListAsInt(num_data, i_start + (4 * coord_index) + 4, 4)
                val_f = change(intf_to_float(val_i))
                val_i = int(float_to_hex(val_f), 16)
                for di, d in enumerate(int_to_list(val_i, 4)):
                    num_data[i_start + (4 * coord_index) + 4 + di] = d
        section_2_start = base + 4 + (count_0 * 0x14)
        count_1 = readListAsInt(num_data, section_2_start, 4)
        for i in range(count_1):
            i_start = section_2_start + 4 + (i * 0x10)
            for coord_index, change in enumerate(changes_0):
                val_i = readListAsInt(num_data, i_start + (4 * coord_index), 4)
                val_f = change(intf_to_float(val_i))
                val_i = int(float_to_hex(val_f), 16)
                for di, d in enumerate(int_to_list(val_i, 4)):
                    num_data[i_start + (4 * coord_index) + di] = d
        data = bytearray(num_data)  # convert num_data back to binary string
        writeRawFile(TableNames.ActorGeometry, file, True, data, ROM_COPY)


def fixBaboonBlasts(ROM_COPY: LocalROM):
    """Fix various baboon blasts to work for Krusha."""
    # Fungi Baboon Blast
    for id in (2, 5):
        item_start = getObjectAddress(ROM_COPY, 0xBC, id, "actor")
        if item_start is not None:
            ROM_COPY.seek(item_start + 0x14)
            ROM_COPY.writeMultipleBytes(0xFFFFFFEC, 4)
            ROM_COPY.seek(item_start + 0x1B)
            ROM_COPY.writeMultipleBytes(0, 1)
    # Caves Baboon Blast
    item_start = getObjectAddress(ROM_COPY, 0xBA, 4, "actor")
    if item_start is not None:
        ROM_COPY.seek(item_start + 0x4)
        ROM_COPY.writeFloat(510)
    item_start = getObjectAddress(ROM_COPY, 0xBA, 12, "actor")
    if item_start is not None:
        ROM_COPY.seek(item_start + 0x4)
        ROM_COPY.writeFloat(333)
    # Castle Baboon Blast
    item_start = getObjectAddress(ROM_COPY, 0xBB, 4, "actor")
    if item_start is not None:
        ROM_COPY.seek(item_start + 0x0)
        ROM_COPY.writeFloat(2472)
        ROM_COPY.seek(item_start + 0x8)
        ROM_COPY.writeFloat(1980)


def placeKrushaHead(ROM_COPY: LocalROM, settings: Settings, slot):
    """Replace a kong's face with the Krusha face."""
    if settings.colorblind_mode != ColorblindMode.off:
        return

    kong_face_textures = [[0x27C, 0x27B], [0x279, 0x27A], [0x277, 0x278], [0x276, 0x275], [0x273, 0x274]]
    unc_face_textures = [[579, 586], [580, 587], [581, 588], [582, 589], [577, 578]]
    krushaFace64 = getImageFile(ROM_COPY, TableNames.TexturesGeometry, getBonusSkinOffset(ExtraTextures.KrushaFace1 + slot), True, 64, 64, TextureFormat.RGBA5551)
    krushaFace64Left = krushaFace64.crop([0, 0, 32, 64])
    krushaFace64Right = krushaFace64.crop([32, 0, 64, 64])
    # Used in File Select, Pause Menu, Tag Barrels, Switches, Transformation Barrels
    writeColorImageToROM(krushaFace64Left, 25, kong_face_textures[slot][0], 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
    writeColorImageToROM(krushaFace64Right, 25, kong_face_textures[slot][1], 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
    # Used in Troff and Scoff
    writeColorImageToROM(krushaFace64Left, 7, unc_face_textures[slot][0], 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
    writeColorImageToROM(krushaFace64Right, 7, unc_face_textures[slot][1], 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)

    krushaFace32 = krushaFace64.resize((32, 32))
    krushaFace32 = krushaFace32.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    krushaFace32RBGA32 = getImageFile(ROM_COPY, TableNames.TexturesGeometry, getBonusSkinOffset(ExtraTextures.KrushaFace321 + slot), True, 32, 32, TextureFormat.RGBA32)
    # Used in the DPad Selection Menu
    writeColorImageToROM(krushaFace32, 14, 190 + slot, 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)
    # Used in Shops Previews
    writeColorImageToROM(krushaFace32RBGA32, 14, 197 + slot, 32, 32, False, TextureFormat.RGBA32, ROM_COPY)
