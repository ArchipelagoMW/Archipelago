"""All code associated with updating textures for puzzles."""

import io
import js
from randomizer.Enums.Maps import Maps
from randomizer.Settings import Settings
from randomizer.Patching.Library.Image import writeColorImageToROM, TextureFormat, getImageFile, getNumberImage, ExtraTextures, getBonusSkinOffset, TableNames
from randomizer.Patching.Patcher import LocalROM
from PIL import Image, ImageEnhance


def updateMillLeverTexture(settings: Settings, ROM_COPY: LocalROM) -> None:
    """Update the 21132 texture."""
    if settings.mill_levers[0] > 0:
        # Get Number bounds
        base_num_texture = getImageFile(ROM_COPY, 25, 0x7CA, True, 64, 32, TextureFormat.RGBA5551)
        number_textures = [None, None, None]
        number_x_bounds = (
            (18, 25),
            (5, 16),
            (36, 47),
        )
        modified_tex = getImageFile(ROM_COPY, 25, 0x7CA, True, 64, 32, TextureFormat.RGBA5551)
        for tex in range(3):
            number_textures[tex] = base_num_texture.crop((number_x_bounds[tex][0], 7, number_x_bounds[tex][1], 25))
        total_width = 0
        for x in range(5):
            if settings.mill_levers[x] > 0:
                idx = settings.mill_levers[x] - 1
                total_width += number_x_bounds[idx][1] - number_x_bounds[idx][0]
        # Overwrite old panel
        overwrite_panel = Image.new(mode="RGBA", size=(58, 26), color=(131, 65, 24))
        modified_tex.paste(overwrite_panel, (3, 3), overwrite_panel)
        # Generate new number texture
        new_num_texture = Image.new(mode="RGBA", size=(total_width, 18))
        x_pos = 0
        for num in range(5):
            if settings.mill_levers[num] > 0:
                num_val = settings.mill_levers[num] - 1
                new_num_texture.paste(number_textures[num_val], (x_pos, 0), number_textures[num_val])
                x_pos += number_x_bounds[num_val][1] - number_x_bounds[num_val][0]
        scale_x = 58 / total_width
        scale_y = 26 / 18
        scale = min(scale_x, scale_y)
        x_size = int(total_width * scale)
        y_size = int(18 * scale)
        new_num_texture = new_num_texture.resize((x_size, y_size))
        x_offset = int((58 - x_size) / 2)
        modified_tex.paste(new_num_texture, (3 + x_offset, 3), new_num_texture)
        writeColorImageToROM(modified_tex, 25, 0x7CA, 64, 32, False, TextureFormat.RGBA5551, ROM_COPY)


def updateDiddyDoors(settings: Settings, ROM_COPY: LocalROM):
    """Update the textures for the doors."""
    enable_code = False
    for code in settings.diddy_rnd_doors:
        if sum(code) > 0:  # Has a non-zero element
            enable_code = True
    SEG_WIDTH = 48
    SEG_HEIGHT = 42
    NUMBERS_START = (27, 33)
    if enable_code:
        # Order: 4231, 3124, 1342
        starts = (0xCE8, 0xCE4, 0xCE0)
        for index, code in enumerate(settings.diddy_rnd_doors):
            start = starts[index]
            total = Image.new(mode="RGBA", size=(SEG_WIDTH * 2, SEG_HEIGHT * 2))
            for img_index in range(4):
                img = getImageFile(ROM_COPY, 25, start + img_index, True, SEG_WIDTH, SEG_HEIGHT, TextureFormat.RGBA5551)
                x_offset = SEG_WIDTH * (img_index & 1)
                y_offset = SEG_HEIGHT * ((img_index & 2) >> 1)
                total.paste(img, (x_offset, y_offset), img)
            total = total.transpose(Image.FLIP_TOP_BOTTOM)
            # Overlay color
            cover = Image.new(mode="RGBA", size=(42, 20), color=(115, 98, 65))
            total.paste(cover, NUMBERS_START, cover)
            # Paste numbers
            number_images = []
            number_offsets = []
            total_length = 0
            for num in code:
                num_img = getNumberImage(num + 1, ROM_COPY)
                w, h = num_img.size
                number_offsets.append(total_length)
                total_length += w
                number_images.append(num_img)
            total_numbers = Image.new(mode="RGBA", size=(total_length, 24))
            for img_index, img in enumerate(number_images):
                total_numbers.paste(img, (number_offsets[img_index], 0), img)
            total.paste(total_numbers, (SEG_WIDTH - int(total_length / 2), SEG_HEIGHT - 12), total_numbers)
            total = total.transpose(Image.FLIP_TOP_BOTTOM)
            for img_index in range(4):
                x_offset = SEG_WIDTH * (img_index & 1)
                y_offset = SEG_HEIGHT * ((img_index & 2) >> 1)
                sub_img = total.crop((x_offset, y_offset, x_offset + SEG_WIDTH, y_offset + SEG_HEIGHT))
                writeColorImageToROM(sub_img, 25, start + img_index, SEG_WIDTH, SEG_HEIGHT, False, TextureFormat.RGBA5551, ROM_COPY)


def updateCryptLeverTexture(settings: Settings, ROM_COPY: LocalROM) -> None:
    """Update the two textures for Donkey Minecart entry."""
    if settings.crypt_levers[0] > 0:
        # Get a blank texture
        texture_0 = getImageFile(ROM_COPY, 25, 0x999, True, 32, 64, TextureFormat.RGBA5551)
        blank = texture_0.crop((8, 5, 23, 22))
        texture_0.paste(blank, (8, 42), blank)
        texture_1 = texture_0.copy()
        for xi, x in enumerate(settings.crypt_levers):
            corrected = x - 1
            y_slot = corrected % 3
            num = getNumberImage(xi + 1, ROM_COPY)
            num = num.transpose(Image.FLIP_TOP_BOTTOM)
            w, h = num.size
            scale = 2 / 3
            y_offset = int((h * scale) / 2)
            x_offset = int((w * scale) / 2)
            num = num.resize((int(w * scale), int(h * scale)))
            y_pos = (51, 33, 14)
            tl_y = y_pos[y_slot] - y_offset
            tl_x = 16 - x_offset
            if corrected < 3:
                texture_0.paste(num, (tl_x, tl_y), num)
            else:
                texture_1.paste(num, (tl_x, tl_y), num)
        writeColorImageToROM(texture_0, 25, 0x99A, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
        writeColorImageToROM(texture_1, 25, 0x999, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)


def updateHelmFaces(settings: Settings, ROM_COPY: LocalROM) -> None:
    """Write the textures for Helm Order."""
    helm_order_images = [
        ExtraTextures.FinalBoss1Left,
        ExtraTextures.FinalBoss1Right,
        ExtraTextures.FinalBoss2Left,
        ExtraTextures.FinalBoss2Right,
        ExtraTextures.FinalBoss3Left,
        ExtraTextures.FinalBoss3Right,
        ExtraTextures.FinalBoss4Left,
        ExtraTextures.FinalBoss4Right,
        ExtraTextures.FinalBoss5Left,
        ExtraTextures.FinalBoss5Right,
    ]
    map_data = {
        Maps.KroolDonkeyPhase: {
            "local_image": False,
            "images": [0x27C, 0x27B],
        },
        Maps.KroolDiddyPhase: {
            "local_image": False,
            "images": [0x279, 0x27A],
        },
        Maps.KroolLankyPhase: {
            "local_image": False,
            "images": [0x277, 0x278],
        },
        Maps.KroolTinyPhase: {
            "local_image": False,
            "images": [0x276, 0x275],
        },
        Maps.KroolChunkyPhase: {
            "local_image": False,
            "images": [0x273, 0x274],
        },
        Maps.JapesBoss: {
            "local_image": True,
            "image": "base-hack/assets/displays/head_dillo1.png",
        },
        Maps.AztecBoss: {
            "local_image": True,
            "image": "base-hack/assets/displays/head_dog1.png",
        },
        Maps.FactoryBoss: {
            "local_image": True,
            "image": "base-hack/assets/displays/head_mj.png",
        },
        Maps.GalleonBoss: {
            "local_image": True,
            "image": "base-hack/assets/displays/head_pufftoss.png",
        },
        Maps.FungiBoss: {
            "local_image": True,
            "image": "base-hack/assets/displays/head_dog2.png",
        },
        Maps.CavesBoss: {
            "local_image": True,
            "image": "base-hack/assets/displays/head_dillo2.png",
        },
        Maps.CastleBoss: {
            "local_image": True,
            "image": "base-hack/assets/displays/head_kko.png",
        },
    }
    for index, image in enumerate(helm_order_images):
        order_index = int(index / 2)
        img_index = getBonusSkinOffset(image)
        if order_index >= len(settings.krool_order):
            # Overwrite with a blank image
            img_written = Image.new(mode="RGBA", size=(32, 64))
        else:
            map_index = settings.krool_order[order_index]
            data = map_data[map_index]
            big_image = None
            if data["local_image"]:
                # Pull image from the repo
                big_image = Image.open(io.BytesIO(js.getFile(data["image"])))
                big_image = big_image.resize((64, 64)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                if index % 2 == 0:
                    # Left side
                    img_written = big_image.crop((0, 0, 32, 64))
                else:
                    # Right side
                    img_written = big_image.crop((32, 0, 64, 64))
            else:
                # Pull image from ROM
                img_written = getImageFile(ROM_COPY, TableNames.TexturesGeometry, data["images"][index % 2], True, 32, 64, TextureFormat.RGBA5551)
        writeColorImageToROM(img_written, TableNames.TexturesGeometry, img_index, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)


def updateSnidePanel(settings: Settings, ROM_COPY: LocalROM) -> None:
    """Modify the panel on Snide's to make it easier to spot the indicator."""
    if not settings.snide_reward_rando:
        return
    im_f = getImageFile(ROM_COPY, TableNames.TexturesGeometry, 0xA6F, True, 32, 64, TextureFormat.RGBA5551)
    enhancer = ImageEnhance.Brightness(im_f)
    im_f = enhancer.enhance(0.5)
    writeColorImageToROM(im_f, TableNames.TexturesGeometry, 0xB85, 32, 64, False, TextureFormat.RGBA5551, ROM_COPY)
