"""Locate Hash images for displaying on the website."""

import base64
import io
import zlib
import js

from PIL import Image

from randomizer.Patching.Patcher import ROM, LocalROM


class ImageInfo:
    """Class to store parameters for an image in ROM."""

    def __init__(self, name: str, format: str, table: int, index: int, width: int, height: int, mode: str):
        """Initialize with given parameters."""
        self.name = name
        self.format = format
        self.table = table
        self.index = index
        self.width = width
        self.height = height
        self.mode = mode


def genGIFFrame(im: Image, cap=128):
    """Generate information necessary for a gif frame."""
    alpha = im.getchannel("A")
    im = im.convert("RGB").convert("P", palette=Image.Palette.ADAPTIVE, colors=255)
    mask = Image.eval(alpha, lambda a: 255 if a <= cap else 0)
    im.paste(255, mask)
    im.info["transparency"] = 255
    return im


def get_hash_images(type="local", mode="hash"):
    """Get and return a list of hash images for the website UI."""
    images = [
        ImageInfo("bongos", "rgba16", 25, 5548, 40, 40, "hash"),
        ImageInfo("crown", "rgba16", 25, 5893, 44, 44, "hash"),
        ImageInfo("dk_coin", "rgba16", 7, 500, 48, 44, "hash"),
        ImageInfo("fairy", "rgba32", 25, 5869, 32, 32, "hash"),
        ImageInfo("guitar", "rgba16", 25, 5547, 40, 40, "hash"),
        ImageInfo("nin_coin", "rgba16", 25, 5912, 44, 44, "hash"),
        ImageInfo("orange", "rgba16", 7, 309, 32, 32, "hash"),
        ImageInfo("rainbow_coin", "rgba16", 25, 5963, 48, 44, "hash"),
        ImageInfo("rw_coin", "rgba16", 25, 5905, 44, 44, "hash"),
        ImageInfo("saxophone", "rgba16", 25, 5549, 40, 40, "hash"),
    ]

    for x in range(0x8):
        # Fairy
        images.append(ImageInfo(f"Fairy Image {x}", "rgba32", 25, 0x16ED + x, 32, 32, "loading-fairy"))
    for x in range(0x1B):
        # Explosion
        images.append(ImageInfo(f"Explosion Image {x}", "rgba32", 25, 0x1539 + x, 32, 32, "loading-dead"))

    ptr_offset = 0x101C50
    loaded_images = []
    gif_frames = []
    rom_type = None
    if type == "browser":
        if mode in ("loading-fairy", "loading-dead"):
            rom_type = ROM(js.romFile)
        else:
            rom_type = ROM()
    else:
        rom_type = LocalROM()
    filtered_list = [x for x in images if x.mode == mode]
    for x in filtered_list:
        rom_type.seek(ptr_offset + (x.table * 4))
        ptr_table = ptr_offset + int.from_bytes(rom_type.readBytes(4), "big")
        rom_type.seek(ptr_table + (x.index * 4))
        img_start = ptr_offset + int.from_bytes(rom_type.readBytes(4), "big")
        rom_type.seek(ptr_table + ((x.index + 1) * 4))
        img_end = ptr_offset + int.from_bytes(rom_type.readBytes(4), "big")
        img_size = img_end - img_start
        rom_type.seek(img_start)
        if x.table == 25:
            dec = zlib.decompress(rom_type.readBytes(img_size), 15 + 32)
        else:
            dec = rom_type.readBytes(img_size)
        im = Image.new(mode="RGBA", size=(x.width, x.height))
        pix = im.load()
        pix_count = x.width * x.height
        for pixel in range(pix_count):
            if x.format == "rgba16":
                start = pixel * 2
                end = start + 2
                pixel_data = int.from_bytes(dec[start:end], "big")
                red = (pixel_data >> 11) & 0x1F
                green = (pixel_data >> 6) & 0x1F
                blue = (pixel_data >> 1) & 0x1F
                alpha = pixel_data & 1
                red = int((red / 0x1F) * 0xFF)
                green = int((green / 0x1F) * 0xFF)
                blue = int((blue / 0x1F) * 0xFF)
                alpha = alpha * 255
            elif x.format == "rgba32":
                start = pixel * 4
                end = start + 4
                pixel_data = int.from_bytes(dec[start:end], "big")
                red = (pixel_data >> 24) & 0xFF
                green = (pixel_data >> 16) & 0xFF
                blue = (pixel_data >> 8) & 0xFF
                alpha = pixel_data & 0xFF
                if alpha == 0:
                    red = 0
                    green = 0
                    blue = 0
            pix_x = pixel % x.width
            pix_y = int(pixel / x.width)
            pix[pix_x, pix_y] = (red, green, blue, alpha)

        in_mem_file = io.BytesIO()
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im.save(in_mem_file, format="PNG")
        if mode == "hash":
            in_mem_file.seek(0)
            img_bytes = in_mem_file.read()

            base64_encoded_result_bytes = base64.b64encode(img_bytes)
            base64_encoded_result_str = base64_encoded_result_bytes.decode("ascii")
            loaded_images.append(base64_encoded_result_str)
        else:
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
            gif_frames.append(genGIFFrame(im, 10 if mode == "loading-dead" else 128))
    if mode in ("loading-fairy", "loading-dead"):
        in_mem_file = io.BytesIO()
        if mode == "loading-dead":
            null_frame = Image.new(mode="RGBA", size=(32, 32))
            gif_frames.append(genGIFFrame(im, 10))
            gif_frames[0].save(
                in_mem_file,
                save_all=True,
                append_images=gif_frames[1:],
                duration=2 * len(gif_frames),
                disposal=2,
                format="GIF",
            )
        else:
            gif_frames[0].save(
                in_mem_file,
                save_all=True,
                append_images=gif_frames[1:],
                loop=0,
                duration=12 * len(gif_frames),
                disposal=2,
                format="GIF",
            )

        in_mem_file.seek(0)
        img_bytes = in_mem_file.read()

        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        base64_encoded_result_str = base64_encoded_result_bytes.decode("ascii")
        loaded_images.append(base64_encoded_result_str)
    return loaded_images
