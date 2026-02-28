"""Code associated with custom textures that can be applied through the cosmetic pack."""

import js
import math
from io import BytesIO

from randomizer.Settings import Settings
from randomizer.Patching.Library.ASM import getROMAddress, populateOverlayOffsets, Overlay
from randomizer.Patching.Library.Image import writeColorImageToROM, TextureFormat, getImageFile, writeColorImageToAddress, ExtraTextures, getBonusSkinOffset
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
    im_f = Image.open(BytesIO(bytes(selected_transition[0]))).convert("RGBA")
    # Check if image has any low-alpha pixels. If it does, assume shrink mode
    low_alpha_found = False
    px = im_f.load()
    w, h = im_f.size
    low_alpha_conversion = Image.new(mode="RGBA", size=(w, h))
    px_new = low_alpha_conversion.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 128:
                low_alpha_found = True
            intensity = 255 - a
            px_new[x, y] = (intensity, intensity, intensity, 255)
    if low_alpha_found:
        im_f = low_alpha_conversion.transpose(Image.FLIP_LEFT_RIGHT).resize((64, 64))
        px = im_f.load()
        for x in range(64):
            px[0, x] = (255, 255, 255, 255)
            px[63, x] = (255, 255, 255, 255)
            px[x, 0] = (255, 255, 255, 255)
            px[x, 63] = (255, 255, 255, 255)
    else:
        if w != 64 or h != 64:
            return
    settings.custom_transition = selected_transition[1].split("/")[-1]  # File Name
    writeColorImageToROM(im_f, 14, 95, 64, 64, False, TextureFormat.IA4, ROM_COPY)


def getImageShrink(im_f, width: int, height: int):
    """Shrink image so the entirety of it fits within the selected width and height."""
    im_w, im_h = im_f.size
    scale_w = width / im_w
    scale_h = height / im_h
    scale = min(scale_w, scale_h)
    new_w = int(im_w * scale)
    new_h = int(im_h * scale)
    im_f = im_f.resize((new_w, new_h))
    im_new = Image.new(mode="RGBA", size=(width, height))
    dw = int((width - new_w) / 2)
    dh = int((height - new_h) / 2)
    im_new.paste(im_f, (dw, dh), im_f)
    return im_new


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
    if js.cosmetics.paintings is None:
        return
    if js.cosmetic_names.paintings is None:
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


class ArcadeSprite:
    """Class to store information regarding an arcade sprite."""

    def __init__(self, sprite_name: str, address: int, width: int = 0, height: int = 0, ignore: bool = False):
        """Initialize with given parameters."""
        self.sprite_name = sprite_name
        self.address = address
        self.width = width
        self.height = height
        self.ignore = ignore


class SpriteSet:
    """Class to store information regarding a sprite set."""

    def __init__(self, group: str, sprites: list[ArcadeSprite], specific: bool = True, common_width: int = 0, common_height: int = 0):
        """Initialize with given parameters."""
        self.group = group
        self.sprites = sprites
        self.specific = specific
        self.common_width = common_width
        self.common_height = common_height


ARCADE_SPRITE_INFO = {
    SpriteSet(
        "jumpman",
        [
            ArcadeSprite("run_0", 0x8003B610, 16, 18),
            ArcadeSprite("run_1", 0x8003B180, 16, 18),
            ArcadeSprite("run_2", 0x8003B3C8, 16, 18),
            ArcadeSprite("climb_0", 0x8003B858, 16, 18),
            ArcadeSprite("climb_1", 0x8003BAA0, 16, 18),
            ArcadeSprite("climb_2", 0x8003BCE8, 16, 18),
            ArcadeSprite("climb_3", 0x8003BF30, 16, 18),
            ArcadeSprite("hammer_0", 0x8003C178, 16, 18),
            ArcadeSprite("hammer_1", 0x8003C3C0, 16, 18),
            ArcadeSprite("hammer_2", 0x8003C608, 16, 18),
            ArcadeSprite("hammer_3", 0x8003C850, 16, 18),
            ArcadeSprite("hammer_4", 0x8003CA98, 16, 18),
            ArcadeSprite("hammer_5", 0x8003CCE0, 16, 18),
            ArcadeSprite("death_0", 0x8003D3B8, 16, 18),
            ArcadeSprite("death_1", 0x8003D600, 16, 18),
            ArcadeSprite("death_2", 0x8003D848, 16, 18),
            ArcadeSprite("jump_0", 0x8003CF28, 16, 18),
            ArcadeSprite("jump_1", 0x8003D170, 16, 18),
            ArcadeSprite("lives_counter", 0x8003DA90, 8, 8),
        ],
    ),
    SpriteSet(
        "dk",
        [
            ArcadeSprite("barrel_left", 0x8003E9F0, 48, 42),
            ArcadeSprite("rage", 0x800424D0, 48, 42),
            ArcadeSprite("climb", 0x800463F0, 48, 42),
            ArcadeSprite("dead_0", 0x800473B8, 48, 42),
            ArcadeSprite("dead_1", 0x80048380, 48, 42),
            ArcadeSprite("dead_2", 0x80049348, 48, 42),
            ArcadeSprite("idle", 0x80040540, 48, 42),
            ArcadeSprite("idle_teeth", 0x80041508, 48, 42),
            ArcadeSprite("hench", 0x80043498, 48, 48),
            ArcadeSprite("climb_with_pauline_0", 0x80044460, 48, 48),
            ArcadeSprite("climb_with_pauline_1", 0x80045428, 48, 48),
            ArcadeSprite("how_high", 0x8003F9B8, 46, 32),
        ],
    ),
    SpriteSet(
        "pauline",
        [
            ArcadeSprite("bottom", 0x8003DB18, 16, 18),
            ArcadeSprite("top", 0x8003E438, 16, 18),
            ArcadeSprite("bottom_actions", 0x8003DD60, 16, 55),  # ?
        ],
    ),
    SpriteSet(
        "items",
        [
            ArcadeSprite("dress", 0x80038DE0),
            ArcadeSprite("purse", 0x80038FE8),
            ArcadeSprite("umbrella", 0x800391F0),
        ],
        False,
        16,
        16,
    ),
    SpriteSet(
        "pie",
        [
            ArcadeSprite("pie", 0x8003AA48, 16, 16),
        ],
    ),
    SpriteSet(
        "orange_barrel",
        [
            ArcadeSprite("roll_0", 0x80034610, 16, 16),
            ArcadeSprite("roll_1", 0x80034818, 16, 16),
            ArcadeSprite("roll_2", 0x80034A20, 16, 16),
            ArcadeSprite("roll_3", 0x80034C28, 16, 16),
            ArcadeSprite("fall_0", 0x80035650, 16, 16),
            ArcadeSprite("fall_1", 0x80035898, 16, 16),
            ArcadeSprite("stack", 0x80037130, 16, 16),
        ],
    ),
    SpriteSet(
        "blue_barrel",
        [
            ArcadeSprite("roll_0", 0x80034E30, 16, 16),
            ArcadeSprite("roll_1", 0x80035038, 16, 16),
            ArcadeSprite("roll_2", 0x80035240, 16, 16),
            ArcadeSprite("roll_3", 0x80035448, 16, 16),
            ArcadeSprite("fall_0", 0x80035AE0, 16, 16),
            ArcadeSprite("fall_1", 0x80035CE8, 16, 16),
        ],
    ),
    SpriteSet(
        "orange_flame",
        [
            ArcadeSprite("roam_0", 0x80035EF0, 16, 18),
            ArcadeSprite("roam_1", 0x80036138, 16, 18),
        ],
    ),
    SpriteSet(
        "blue_flame",
        [
            ArcadeSprite("roam_0", 0x80036CA0, 16, 18),
            ArcadeSprite("roam_1", 0x80036EE8, 16, 18),
        ],
    ),
    SpriteSet(
        "orange_duck",
        [
            ArcadeSprite("roam_0", 0x80036380, 16, 18),
            ArcadeSprite("roam_1", 0x800365C8, 16, 18),
        ],
    ),
    SpriteSet(
        "blue_duck",
        [
            ArcadeSprite("roam_0", 0x80036810, 16, 18),
            ArcadeSprite("roam_1", 0x80036A58, 16, 18),
        ],
    ),
    SpriteSet(
        "spring",
        [
            ArcadeSprite("bounce_0", 0x80037788, 16, 16),
            ArcadeSprite("bounce_1", 0x80037990, 16, 16),
        ],
    ),
    SpriteSet(
        "ladder",
        [
            ArcadeSprite("white", 0x8003A638, 16, 16, True),
            ArcadeSprite("rung_blue", 0x80032B48, 8, 4, True),
            ArcadeSprite("rung_orange", 0x80032B90, 8, 4, True),
            ArcadeSprite("rung_white", 0x80032BD8, 8, 4, True),
        ],
    ),
    # Misc
    SpriteSet(
        "ui",
        [
            ArcadeSprite("highscore_character_selector", 0x8003A840, 16, 16, True),
            ArcadeSprite("black", 0x80034360, 16, 16, True),
            ArcadeSprite("bonus_osd_25m", 0x80032F68, 43, 43),  # Also 75m
            ArcadeSprite("bonus_osd_50m", 0x80033C48, 43, 20),
            ArcadeSprite("bonus_osd_100m", 0x800335D8, 43, 20),
        ],
    ),
    SpriteSet(
        "particles",
        [
            ArcadeSprite("sparks", 0x8003AC50, 16, 16, True),
            ArcadeSprite("point_spark_0", 0x8003A1A8, 16, 18),
            ArcadeSprite("point_spark_1", 0x8003A3F0, 16, 18),
            ArcadeSprite("heart", 0x800389D0, 16, 16),
            ArcadeSprite("heart_broken", 0x80038BD8, 16, 16),
            ArcadeSprite("help_aqua", 0x8003E680, 24, 10),
            ArcadeSprite("help_midnight_blue", 0x8003E868, 24, 10),
            ArcadeSprite("hammer_particle_0", 0x80039D18, 16, 18),
            ArcadeSprite("hammer_particle_1", 0x80039F60, 16, 18),
            ArcadeSprite("points_100", 0x800381B0, 16, 16),
            ArcadeSprite("points_300", 0x800383B8, 16, 16),
            ArcadeSprite("points_500", 0x800385C0, 16, 16),
            ArcadeSprite("points_800", 0x800387C8, 16, 16),
            ArcadeSprite("orange_spark", 0x800342B8, 8, 10),  # ?
        ],
    ),
    SpriteSet(
        "misc",
        [
            ArcadeSprite("nintendo_coin", 0x8003AE58, 20, 20, True),  # Never change this under any circumstances
        ],
    ),
    SpriteSet(
        "stage",
        [
            ArcadeSprite("pulley_horizontal_0", 0x80037B98, 16, 16),
            ArcadeSprite("pulley_horizontal_1", 0x80037DA0, 16, 16),
            ArcadeSprite("pulley_horizontal_2", 0x80037FA8, 16, 16),
            ArcadeSprite("pulley_vertical", 0x80037580, 16, 16),
            ArcadeSprite("oil_fire_0", 0x80032228, 16, 18),
            ArcadeSprite("oil_fire_1", 0x80032470, 16, 18),
            ArcadeSprite("oil_fire_2", 0x800326B8, 16, 18),
            ArcadeSprite("oil_fire_3", 0x80032900, 16, 18),
            ArcadeSprite("oil_drum", 0x80037338, 16, 18),
            ArcadeSprite("elevator_cord", 0x80032F40, 8, 2),
            ArcadeSprite("girder_red", 0x80034568, 16, 5),
            ArcadeSprite("girder_8px_orange", 0x80032D50, 8, 10),  # ????
            ArcadeSprite("girder_8px_red", 0x80032DF8, 8, 8),  # ????
            ArcadeSprite("rivet", 0x80032E80, 8, 9),  # 100m
            ArcadeSprite("100m_segment", 0x80032C20, 8, 8),  # ????
            ArcadeSprite("conveyor_segment", 0x80032CA8, 16, 5),  # ?
            ArcadeSprite("blue", 0x80032F18, 8, 2),  # ?
        ],
    ),
    SpriteSet(
        "hammer",
        [
            ArcadeSprite("burgundy_0", 0x800393F8, 16, 18),
            ArcadeSprite("burgundy_1", 0x80039640, 16, 18),
            ArcadeSprite("gold_0", 0x80039888, 16, 18),
            ArcadeSprite("gold_1", 0x80039AD0, 16, 18),
        ],
    ),
}


def hasCustomArcadeSprite(address: int) -> bool:
    """Return whether a custom arcade sprite has been provided for that RAM address."""
    for filename in ARCADE_SPRITE_INFO:
        if ARCADE_SPRITE_INFO[filename]["address"] != address:
            # Not a matching address
            continue
        if ARCADE_SPRITE_INFO[filename]["ignore"]:
            # Ignored, can never have a sprite.
            # By this point, we've determined that we're on the right address, so can start returning stuff
            return False
    return False


def writeCustomArcadeSprites(settings: Settings, ROM_COPY: ROM) -> None:
    """Write a custom series of arcade sprites to ROM."""
    if js.cosmetics is None:
        return
    if js.cosmetics.arcade_sprites is None:
        return
    if js.cosmetic_names.arcade_sprites is None:
        return
    file_data = list(zip(js.cosmetics.arcade_sprites, js.cosmetic_names.arcade_sprites))
    if len(file_data) == 0:
        return
    offset_dict = populateOverlayOffsets(ROM_COPY)
    SPLITTER = "textures/arcade_sprites/"
    set_pools = {}
    for file in file_data:
        # Compose the set pools
        local_path_segments = SPLITTER.join(file[1].split(SPLITTER)[1:]).split("/")
        target_sprite_set = local_path_segments[0]
        name = local_path_segments[-1].split(".")[0]
        sprite_set = None
        for sset in ARCADE_SPRITE_INFO:
            if sset.group == target_sprite_set:
                sprite_set = sset
                break
        if sprite_set is None:
            # Invalid sprite set, don't process
            continue
        if target_sprite_set not in set_pools:
            set_pools[target_sprite_set] = []
        set_pools[target_sprite_set].append(local_path_segments[1])
    determined_set = {}
    valid_sets = []
    if len(list(set_pools.keys())) == 0:
        # No sets to pick from
        return
    for set_name in set_pools:
        chosen_set = settings.random.choice(set_pools[set_name])
        set_path = f"{SPLITTER}{set_name}/{chosen_set}/"
        determined_set[set_name] = set_path
        valid_sets.append(set_path)
    valid_nonspecific_sprites = {}
    sprite_to_set = {}
    for file in file_data:
        # Now that we have selected sets, get to placing those files in
        valid_file = False
        for vset in valid_sets:
            if vset in file[1]:
                valid_file = True
        if not valid_file:
            # Not part of a selected set, discard
            continue
        local_path_segments = SPLITTER.join(file[1].split(SPLITTER)[1:]).split("/")
        target_sprite_set = local_path_segments[0]
        name = local_path_segments[-1].split(".")[0]
        sprite_set = None
        for sset in ARCADE_SPRITE_INFO:
            if sset.group == target_sprite_set:
                sprite_set = sset
                break
        if sprite_set is None:
            # Invalid sprite set, don't process
            continue
        if sprite_set.specific:
            # Needs to have a specific filename
            sprite = None
            for tested_sprite in sset.sprites:
                if tested_sprite.sprite_name == name:
                    sprite = tested_sprite
            if sprite is None:
                # Invalid sprite name, discard
                continue
            if sprite.ignore:
                # Ignored sprite, discard
                continue
            image = Image.open(BytesIO(bytes(file[0])))
            width, height = image.size
            if width != sprite.width or height != sprite.height:
                # Invalid size, don't process
                continue
            addr = getROMAddress(sprite.address, Overlay.Arcade, offset_dict)
            image = image.convert("RGBA")
            writeColorImageToAddress(image, addr, sprite.width, sprite.height, False, TextureFormat.RGBA5551, ROM_COPY, False, 2 * sprite.width * sprite.height)
        else:
            # Can be any filename
            image = Image.open(BytesIO(bytes(file[0])))
            width, height = image.size
            if width != sprite_set.common_width or height != sprite_set.common_height:
                # Invalid size, don't process
                continue
            if target_sprite_set not in valid_nonspecific_sprites:
                valid_nonspecific_sprites[target_sprite_set] = []
            valid_nonspecific_sprites[target_sprite_set].append(file[1])
            sprite_to_set[file[1]] = sprite_set
    for sset in valid_nonspecific_sprites:
        settings.random.shuffle(valid_nonspecific_sprites[sset])
    for file in file_data:
        if file[1] not in sprite_to_set:
            # Isn't a considered file
            continue
        sprite_set: SpriteSet = sprite_to_set[file[1]]
        set_name = sprite_set.group
        limit = len([x for x in sprite_set.sprites if not x.ignore])
        if file[1] not in valid_nonspecific_sprites[set_name]:
            # Isn't in the selection for some reason. Skip
            continue
        idx = valid_nonspecific_sprites[set_name].index(file[1])
        if idx >= limit:
            # Isn't part of first {limit} items in the shuffled list, discord
            continue
        addr = getROMAddress(sprite_set.sprites[idx].address, Overlay.Arcade, offset_dict)
        image = Image.open(BytesIO(bytes(file[0])))
        image = image.convert("RGBA")
        writeColorImageToAddress(image, addr, sprite_set.common_width, sprite_set.common_height, False, TextureFormat.RGBA5551, ROM_COPY, False, 2 * sprite_set.common_width * sprite_set.common_height)


def writeCustomReels(settings: Settings, ROM_COPY: ROM) -> None:
    """Write custom reel files to ROM."""
    if js.cosmetics is None:
        return
    if js.cosmetics.reel_sprites is None:
        return
    if js.cosmetic_names.reel_sprites is None:
        return
    REEL_INFO = [
        PaintingData(32, 32, 1, 1, False, [getBonusSkinOffset(ExtraTextures.BanditImage0)]),  # Grape
        PaintingData(40, 51, 1, 1, False, [getBonusSkinOffset(ExtraTextures.BanditImage1)]),  # Coconut
        PaintingData(48, 42, 1, 1, False, [getBonusSkinOffset(ExtraTextures.BanditImage2)]),  # Melon
        PaintingData(32, 48, 1, 1, False, [getBonusSkinOffset(ExtraTextures.BanditImage3)]),  # Pineapple
    ]
    file_data = list(zip(js.cosmetics.reel_sprites, js.cosmetic_names.reel_sprites))
    if len(file_data) == 0:
        return
    list_pool = file_data.copy()
    settings.random.shuffle(list_pool)
    for reel in REEL_INFO:
        reel.name = None
        if len(list_pool) < 1:
            continue
        selected_reel = list_pool.pop(0)
        reel.name = selected_reel[1].split("/")[-1]  # File Name
        im_f = Image.open(BytesIO(bytes(selected_reel[0]))).convert("RGBA")
        im_f = getImageShrink(im_f, reel.width, reel.height)
        im_f = im_f.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
        chunks = []
        chunk_w = int(reel.width / reel.x_split)
        chunk_h = int(reel.height / reel.y_split)
        for y in range(reel.y_split):
            for x in range(reel.x_split):
                left = x * chunk_w
                top = y * chunk_h
                chunk_im = im_f.crop((int(left), int(top), int(left + chunk_w), int(top + chunk_h)))
                chunks.append(chunk_im)
        for chunk_index, chunk in enumerate(chunks):
            img_index = reel.texture_order[chunk_index]
            writeColorImageToROM(chunk, 25, img_index, chunk_w, chunk_h, True, TextureFormat.RGBA5551, ROM_COPY)


kong_colors = [
    (0xFF, 0xD7, 0x00),
    (0xFF, 0x00, 0x00),
    (0x16, 0x99, 0xFF),
    (0xB0, 0x45, 0xFF),
    (0x41, 0xFF, 0x25),
    (0xFF, 0xFF, 0xFF),
]


def writeCustomItemSprites(settings: Settings, ROM_COPY: ROM) -> None:
    """Write custom coin gif files to ROM."""
    if js.cosmetics is None:
        return
    if js.cosmetics.item_sprites is None:
        return
    if js.cosmetic_names.item_sprites is None:
        return
    file_data = list(zip(js.cosmetics.item_sprites, js.cosmetic_names.item_sprites))
    if len(file_data) == 0:
        return
    list_pool = file_data.copy()
    groups = {}
    group_files = {}
    for item in list_pool:
        name = item[1].split("/")[-1].split(".")[0]
        numbers = [str(x) for x in range(10)]
        item_name = name
        item_number = ""
        error = False
        while True:
            if len(item_name) == 0:
                # Reached the start of the item name without detecting a non-number
                error = True
                break
            if item_name[-1] in numbers:
                item_number = item_name[-1] + item_number
                item_name = item_name[:-1]
            else:
                break
        if item_number == "" or error:
            # Has no number at the end, or is all numbers
            continue
        if item_name not in groups:
            groups[item_name] = []
            group_files[item_name] = {}
        groups[item_name].append(int(item_number))
        group_files[item_name][int(item_number)] = item[0]
    valid_item_names = []
    for name, numbers in groups.items():
        for x in range(len(numbers)):
            if x not in numbers:
                groups[name] = list(range(x))
                break
        if len(groups[name]) > 0:
            valid_item_names.append(name)
    if len(valid_item_names) == 0:
        return
    chosen_item = settings.random.choice(valid_item_names)
    frames_per_frame = len(groups[chosen_item]) / 8  # I promise this variable name makes sense
    coin_data = [
        # DK
        {"table": 7, "image": 0x00E0, "frame": 0, "color": 0},
        {"table": 7, "image": 0x00E1, "frame": 1, "color": 0},
        {"table": 7, "image": 0x00E2, "frame": 2, "color": 0},
        {"table": 7, "image": 0x00E3, "frame": 3, "color": 0},
        {"table": 7, "image": 0x00E4, "frame": 4, "color": 0},
        {"table": 7, "image": 0x00E5, "frame": 5, "color": 0},
        {"table": 7, "image": 0x00E6, "frame": 6, "color": 0},
        {"table": 7, "image": 0x00E7, "frame": 7, "color": 0},
        {"table": 25, "image": 0x0C39, "frame": 4, "color": 0},
        # Diddy
        {"table": 7, "image": 0x0100, "frame": 0, "color": 1},
        {"table": 7, "image": 0x0101, "frame": 1, "color": 1},
        {"table": 7, "image": 0x0102, "frame": 2, "color": 1},
        {"table": 7, "image": 0x0103, "frame": 3, "color": 1},
        {"table": 7, "image": 0x0104, "frame": 4, "color": 1},
        {"table": 7, "image": 0x0105, "frame": 5, "color": 1},
        {"table": 7, "image": 0x0106, "frame": 6, "color": 1},
        {"table": 7, "image": 0x0107, "frame": 7, "color": 1},
        # Lanky
        {"table": 7, "image": 0x00F8, "frame": 0, "color": 2},
        {"table": 7, "image": 0x00F9, "frame": 1, "color": 2},
        {"table": 7, "image": 0x00FA, "frame": 2, "color": 2},
        {"table": 7, "image": 0x00FB, "frame": 3, "color": 2},
        {"table": 7, "image": 0x00FC, "frame": 4, "color": 2},
        {"table": 7, "image": 0x00FD, "frame": 5, "color": 2},
        {"table": 7, "image": 0x00FE, "frame": 6, "color": 2},
        {"table": 7, "image": 0x00FF, "frame": 7, "color": 2},
        # Tiny
        {"table": 7, "image": 0x00D8, "frame": 0, "color": 3},
        {"table": 7, "image": 0x00D9, "frame": 1, "color": 3},
        {"table": 7, "image": 0x00DA, "frame": 2, "color": 3},
        {"table": 7, "image": 0x00DB, "frame": 3, "color": 3},
        {"table": 7, "image": 0x00DC, "frame": 4, "color": 3},
        {"table": 7, "image": 0x00DD, "frame": 5, "color": 3},
        {"table": 7, "image": 0x00DE, "frame": 6, "color": 3},
        {"table": 7, "image": 0x00DF, "frame": 7, "color": 3},
        # Chunky
        {"table": 7, "image": 0x0108, "frame": 0, "color": 4},
        {"table": 7, "image": 0x0109, "frame": 1, "color": 4},
        {"table": 7, "image": 0x010A, "frame": 2, "color": 4},
        {"table": 7, "image": 0x010B, "frame": 3, "color": 4},
        {"table": 7, "image": 0x010C, "frame": 4, "color": 4},
        {"table": 7, "image": 0x010D, "frame": 5, "color": 4},
        {"table": 7, "image": 0x010E, "frame": 6, "color": 4},
        {"table": 7, "image": 0x010F, "frame": 7, "color": 4},
    ]

    for x in range(8):
        selected_frame = int(frames_per_frame * x)
        selected_frame_data = group_files[chosen_item][selected_frame]
        im_f = Image.open(BytesIO(bytes(selected_frame_data))).convert("RGBA")
        im_f = getImageShrink(im_f, 48, 42)
        im_f = im_f.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
        for img_data in coin_data:
            if img_data["frame"] != x:
                continue
            r, g, b, a = im_f.split()
            gray = Image.merge("RGB", (r, g, b)).convert("L")
            target_color = kong_colors[img_data["color"]]
            tinted_r = Image.eval(gray, lambda v: v * target_color[0] // 255)
            tinted_g = Image.eval(gray, lambda v: v * target_color[1] // 255)
            tinted_b = Image.eval(gray, lambda v: v * target_color[2] // 255)
            tinted = Image.merge("RGBA", (tinted_r, tinted_g, tinted_b, a))
            writeColorImageToROM(tinted, img_data["table"], img_data["image"], 48, 42, False, TextureFormat.RGBA5551, ROM_COPY)
