"""Code associated with custom textures that can be applied through the cosmetic pack."""

import js
import math
from io import BytesIO

from randomizer.Settings import Settings
from randomizer.Patching.Library.Image import writeColorImageToROM, TextureFormat, getImageFile
from randomizer.Patching.Patcher import ROM
from PIL import Image


def writeTransition(settings: Settings, ROM_COPY: ROM) -> None:
    """Write transition cosmetic to ROM."""
    if js.cosmetics is None:
        return
    if js.cosmetics.transitions is None:
        return
    if js.cosmetic_names.transitions is None:
        return
    file_data = list(zip(js.cosmetics.transitions, js.cosmetic_names.transitions))
    settings.custom_transition = None
    if len(file_data) == 0:
        return
    selected_transition = settings.random.choice(file_data)
    im_f = Image.open(BytesIO(bytes(selected_transition[0])))
    w, h = im_f.size
    if w != 64 or h != 64:
        return
    settings.custom_transition = selected_transition[1].split("/")[-1]  # File Name
    writeColorImageToROM(im_f, 14, 95, 64, 64, False, TextureFormat.IA4, ROM_COPY)


def getImageChunk(im_f, width: int, height: int):
    """Get an image chunk based on a width and height."""
    width_height_ratio = width / height
    im_w, im_h = im_f.size
    im_wh_ratio = im_w / im_h
    if im_wh_ratio != width_height_ratio:
        # Ratio doesn't match, we have to do some rejigging
        scale = 1
        if width_height_ratio > im_wh_ratio:
            # Scale based on width
            scale = width / im_w
        else:
            # Height needs growing
            scale = height / im_h
        im_f = im_f.resize((int(im_w * scale), int(im_h * scale)))
        im_w, im_h = im_f.size
        middle_w = im_w / 2
        middle_h = im_h / 2
        middle_targ_w = width / 2
        middle_targ_h = height / 2
        return im_f.crop(
            (
                int(middle_w - middle_targ_w),
                int(middle_h - middle_targ_h),
                int(middle_w + middle_targ_w),
                int(middle_h + middle_targ_h),
            )
        )
    # Ratio matches, just scale up
    return im_f.resize((width, height))


def writeCustomPortal(settings: Settings, ROM_COPY: ROM) -> None:
    """Write custom portal file to ROM."""
    if js.cosmetics is None:
        return
    if js.cosmetics.tns_portals is None:
        return
    if js.cosmetic_names.tns_portals is None:
        return
    file_data = list(zip(js.cosmetics.tns_portals, js.cosmetic_names.tns_portals))
    settings.custom_troff_portal = None
    if len(file_data) == 0:
        return
    selected_portal = settings.random.choice(file_data)
    settings.custom_troff_portal = selected_portal[1].split("/")[-1]  # File Name
    im_f = Image.open(BytesIO(bytes(selected_portal[0])))
    im_f = getImageChunk(im_f, 63, 63)
    im_f = im_f.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    portal_data = {
        "NW": {
            "x_min": 0,
            "y_min": 0,
            "writes": [0x39E, 0x39F],
        },
        "SW": {
            "x_min": 0,
            "y_min": 31,
            "writes": [0x3A0, 0x39D],
        },
        "SE": {
            "x_min": 31,
            "y_min": 31,
            "writes": [0x3A2, 0x39B],
        },
        "NE": {
            "x_min": 31,
            "y_min": 0,
            "writes": [0x39C, 0x3A1],
        },
    }
    for sub in portal_data.keys():
        x_min = portal_data[sub]["x_min"]
        y_min = portal_data[sub]["y_min"]
        local_img = im_f.crop((x_min, y_min, x_min + 32, y_min + 32))
        for idx in portal_data[sub]["writes"]:
            writeColorImageToROM(local_img, 7, idx, 32, 32, False, TextureFormat.RGBA5551, ROM_COPY)


class PaintingData:
    """Class to store information regarding a painting."""

    def __init__(self, width: int, height: int, x_split: int, y_split: int, is_bordered: bool, texture_order: list, is_ci: bool = False):
        """Initialize with given parameters."""
        self.width = width
        self.height = height
        self.x_split = x_split
        self.y_split = y_split
        self.is_bordered = is_bordered
        self.texture_order = texture_order.copy()
        self.name = None


def writeCustomPaintings(settings: Settings, ROM_COPY: ROM) -> None:
    """Write custom painting files to ROM."""
    if js.cosmetics is None:
        return
    if js.cosmetics.tns_portals is None:
        return
    if js.cosmetic_names.tns_portals is None:
        return
    PAINTING_INFO = [
        PaintingData(64, 64, 2, 1, False, [0x1EA, 0x1E9]),  # DK Isles
        PaintingData(128, 128, 2, 4, True, [0x90A, 0x909, 0x903, 0x908, 0x904, 0x907, 0x905, 0x906]),  # K Rool
        PaintingData(128, 128, 2, 4, True, [0x9B4, 0x9AD, 0x9B3, 0x9AE, 0x9B2, 0x9AF, 0x9B1, 0x9B0]),  # Knight
        PaintingData(128, 128, 2, 4, True, [0x9A5, 0x9AC, 0x9A6, 0x9AB, 0x9A7, 0x9AA, 0x9A8, 0x9A9]),  # Sword
        PaintingData(64, 32, 1, 1, False, [0xA53]),  # Dolphin
        PaintingData(32, 64, 1, 1, False, [0xA46]),  # Candy
        # PaintingData(64, 64, 1, 1, False, [0x614, 0x615], True),  # K Rool Run
        # PaintingData(64, 64, 1, 1, False, [0x625, 0x626], True),  # K Rool Blunderbuss
        # PaintingData(64, 64, 1, 1, False, [0x627, 0x628], True),  # K Rool Head
    ]
    file_data = list(zip(js.cosmetics.paintings, js.cosmetic_names.paintings))
    settings.painting_isles = None
    settings.painting_museum_krool = None
    settings.painting_museum_knight = None
    settings.painting_museum_swords = None
    settings.painting_treehouse_dolphin = None
    settings.painting_treehouse_candy = None
    if len(file_data) == 0:
        return
    list_pool = file_data.copy()
    PAINTING_COUNT = len(PAINTING_INFO)
    if len(list_pool) < PAINTING_COUNT:
        mult = math.ceil(PAINTING_COUNT / len(list_pool)) - 1
        for _ in range(mult):
            list_pool.extend(file_data.copy())
    settings.random.shuffle(list_pool)
    for painting in PAINTING_INFO:
        painting.name = None
        selected_painting = list_pool.pop(0)
        painting.name = selected_painting[1].split("/")[-1]  # File Name
        im_f = Image.open(BytesIO(bytes(selected_painting[0])))
        im_f = getImageChunk(im_f, painting.width, painting.height)
        im_f = im_f.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
        chunks = []
        chunk_w = int(painting.width / painting.x_split)
        chunk_h = int(painting.height / painting.y_split)
        for y in range(painting.y_split):
            for x in range(painting.x_split):
                left = x * chunk_w
                top = y * chunk_h
                chunk_im = im_f.crop((int(left), int(top), int(left + chunk_w), int(top + chunk_h)))
                chunks.append(chunk_im)
        border_imgs = []
        for x in range(8):
            border_tex = PAINTING_INFO[1].texture_order[x]
            border_img = getImageFile(ROM_COPY, 25, border_tex, True, 64, 32, TextureFormat.RGBA5551)
            border_imgs.append(border_img)
        for chunk_index, chunk in enumerate(chunks):
            if painting.is_bordered:
                border_img = border_imgs[chunk_index]
                if chunk_index in (0, 1):
                    # Top
                    border_seg_img = border_img.crop((0, 0, 64, 14))
                    chunk.paste(border_seg_img, (0, 0), border_seg_img)
                if chunk_index in (0, 2, 4, 6):
                    # Left
                    border_seg_img = border_img.crop((0, 0, 14, 32))
                    chunk.paste(border_seg_img, (0, 0), border_seg_img)
                if chunk_index in (1, 3, 5, 7):
                    # Right
                    border_seg_img = border_img.crop((50, 0, 64, 32))
                    chunk.paste(border_seg_img, (50, 0), border_seg_img)
                if chunk_index in (6, 7):
                    # Bottom
                    border_seg_img = border_img.crop((0, 20, 64, 32))
                    chunk.paste(border_seg_img, (0, 20), border_seg_img)
            img_index = painting.texture_order[chunk_index]
            writeColorImageToROM(chunk, 25, img_index, chunk_w, chunk_h, False, TextureFormat.RGBA5551, ROM_COPY)
    settings.painting_isles = PAINTING_INFO[0].name
    settings.painting_museum_krool = PAINTING_INFO[1].name
    settings.painting_museum_knight = PAINTING_INFO[2].name
    settings.painting_museum_swords = PAINTING_INFO[3].name
    settings.painting_treehouse_dolphin = PAINTING_INFO[4].name
    settings.painting_treehouse_candy = PAINTING_INFO[5].name
