from collections import defaultdict
from typing import TYPE_CHECKING
from colorsys import hsv_to_rgb, rgb_to_hsv, hls_to_rgb, rgb_to_hls
from Options import OptionError

if TYPE_CHECKING:
    from . import KSSWorld

palette_addresses = {
    "Kirby": [0x467D8, 0x467F8, 0x468F8],
    "Cutter": [0x469D8],
    "Beam": [0x469F8, 0x46818],
    "Yo-Yo": [0x46A18],
    "Ninja": [0x46A38, 0x46838],
    "Wing": [0x46A58],
    "Fighter": [0x46A78],
    "Jet": [0x46A98],
    "Sword": [0x46AB8],
    "Fire": [0x46AD8, 0x46AF8, 0x46B18, 0x46B38, 0x64B58, 0x46858],
    "Stone": [0x46C18, 0x46878],  # There's one for each transformation, but since they use different setup we won't touch
    "Bomb": [0x46CD8],
    "Plasma": [0x46CF8, 0x46D18, 0x46D38, 0x46D58, 0x46D78, 0x46D98, 0x46DB8, 0x46DD8, 0x46898],
    "Wheel": [0x46DF8, 0x46E18, 0x46E38],
    "Ice": [0x46E58, 0x46E78, 0x46E98, 0x468B8],
    "Mirror": [0x46EB8, 0x46ED8, 0x46EF8, 0x468D8],
    "Copy": [0x470F8, 0x47118, 0x47138, 0x47158, 0x47178, 0x47198],
    "Suplex": [0x471B8, 0x46918],
    "Hammer": [0x471D8, 0x46938],
    "Parasol": [0x471F8],
    "Mike": [0x47218, 0x47238, 0x47258, 0x47278, 0x47298, 0x472B8,
             0x472D8, 0x472F8, 0x47318, 0x47338, 0x47358, 0x47378],
    "Sleep": [0x47398, 0x473B8, 0x473D8, 0x473F8],
    "Paint": [0x47418, 0x47438, 0x47458, 0x47478],
    "Cook": [0x47498, 0x474B8, 0x474D8, 0x474F8],
    "Crash": [0x47518, 0x47538, 0x47558, 0x47578],
}

palette_factors: dict[int, tuple[float, float, float]] = defaultdict(lambda: (0.0, 1.0, 1.0), {
    # LS are multipliers
    # Hue is additive (given the way hue works, multiplier doesn't make sense)
    0x46E38: (0.0, 1.5, 1.0),
    0x470F8: (0.0, 0.3, 1.0),
    0x47138: (0.2, 1.0, 1.0),
    0x47218: (0.0, 0.3, 1.0),
    0x47258: (0.2, 1.0, 1.0),
    0x47298: (0.0, 0.3, 1.0),
    0x472D8: (0.2, 1.0, 1.0),
    0x47318: (0.0, 0.3, 1.0),
    0x47358: (0.2, 1.0, 1.0),
    0x47398: (0.0, 0.3, 1.0),
    0x473D8: (0.2, 1.0, 1.0),
    0x47418: (0.0, 0.3, 1.0),
    0x47458: (0.2, 1.0, 1.0),
    0x47498: (0.0, 0.3, 1.0),
    0x474D8: (0.2, 1.0, 1.0),
    0x47518: (0.0, 0.3, 1.0),
    0x47558: (0.2, 1.0, 1.0),
})

flavor_presets = {
    1: {
        "2": "FF91C6",
        "5": "B0123B",
        "7": "D60052",
        "4": "DE4873",
        "6": "000000",
        "3": "F770A5",
        "8": "E01784",
        "1": "FFA1DE"
    },
    2: {
        "2": "FF3554",
        "5": "AA0040",
        "7": "E02068",
        "4": "C2183F",
        "6": "872939",
        "3": "E82B47",
        "8": "E80067",
        "1": "F85068"
    },
    3: {
        "2": "e6e6fa",
        "5": "bcbcf2",
        "7": "2929ec",
        "4": "b5b5f0",
        "6": "3232d6",
        "3": "d6d6ef",
        "8": "4a52ef",
        "1": "f6f6fd"
    },
    4: {
        "2": "F0E08D",
        "5": "C8A060",
        "7": "E03700",
        "4": "EFC063",
        "6": "A8501C",
        "3": "E8D070",
        "8": "E2501E",
        "1": "F8F8A5"
    },
    5: {
        "2": "88F27B",
        "5": "57A044",
        "7": "C75418",
        "4": "57BA23",
        "6": "2D6823",
        "3": "3FD744",
        "8": "E06C16",
        "1": "98F89A"
    },
    6: {
        "2": "CA8AE8",
        "5": "8250A5",
        "7": "A52068",
        "4": "8D64B8",
        "6": "672D9A",
        "3": "BA82D5",
        "8": "B55098",
        "1": "DA98F8"
    },
    7: {
        "2": "C2735C",
        "5": "5C351C",
        "7": "9F2F0C",
        "4": "874C3B",
        "6": "4C1E00",
        "3": "B06458",
        "8": "921C16",
        "1": "CF785B"
    },
    8: {
        "2": "e6e6e6",
        "5": "bcbcbc",
        "7": "909090",
        "4": "b5b5b5",
        "6": "646464",
        "3": "d6d6d6",
        "8": "525252",
        "1": "f6f6f6"
    },
    9: {
        "2": "6B6B6B",
        "5": "2B2B2B",
        "7": "640000",
        "4": "3D3D3D",
        "6": "020202",
        "3": "606060",
        "8": "980000",
        "1": "808080"
    },
    10: {
        "2": "EF8A9D",
        "5": "C84F6B",
        "7": "126018",
        "4": "D85F6F",
        "6": "A24858",
        "3": "E77B8D",
        "8": "168025",
        "1": "F897AD"
    },
    11: {
        "2": "FF9A00",
        "5": "B05C1C",
        "7": "D23B0C",
        "4": "E08200",
        "6": "8A2B16",
        "3": "EF970A",
        "8": "E24800",
        "1": "FFAF27"},
    12: {
        "2": "4FF29D",
        "5": "2BA04C",
        "7": "C7C218",
        "4": "33BA5F",
        "6": "2D6823",
        "3": "1CD773",
        "8": "E0CF16",
        "1": "43F8B2"
    },
    13: {
        "2": "CACAE7",
        "5": "7B7BA8",
        "7": "B57EDC",
        "4": "8585C5",
        "6": "474796",
        "3": "B2B2D8",
        "8": "B790EF",
        "1": "E6E6FA"
    },
    14: {
        "2": "98d5d3",
        "5": "1aa5ab",
        "7": "4f5559",
        "4": "1dbac2",
        "6": "093a3c",
        "3": "86cecb",
        "8": "a0afbc",
        "1": "bce4e2"
    }
}

def color_string_to_rgb(color: str) -> tuple[float, float, float]:
    if color.startswith("#"):
        color = color.replace("#", "")
    colint = int(color, 16)
    col: tuple[int, int, int] = ((colint & 0xFF0000) >> 16, (colint & 0xFF00) >> 8, colint & 0xFF)
    return (col[0] / 256, col[1] / 256, col[2] / 256)

def rgb_to_hex_color(red: float, green: float, blue: float) -> str:
    col = (int(red * 255) << 16) + (int(green * 255) << 8) + int(blue * 255)
    return f"{hex(col)[2:]:6}"

def generate_palette(primary: str, secondary: str, pair: str) -> dict[str, str]:
    # first generate the hsv for primary
    primary_rgb = color_string_to_rgb(primary)
    primary_hsv = rgb_to_hsv(*primary_rgb)
    if not pair:
        pair = "complement"
    if not secondary:
        if pair == "complement":
            secondary_hsv = (primary_hsv[0] + 0.5 if primary_hsv[0] < 0.5 else primary_hsv[0] - 0.5,
                             primary_hsv[1], primary_hsv[2])
        elif pair == "analogous":
            secondary_hsv = (primary_hsv[0] + 0.1, primary_hsv[1], primary_hsv[2])
        elif pair == "intensify":
            # increase saturation on primary
            secondary_hsv = (primary_hsv[0], min(primary_hsv[1] * 2, 1.0), primary_hsv[2])
        else:
            raise OptionError(f"Unknown palette pairing type: {pair}")
    else:
        secondary_hsv = rgb_to_hsv(*color_string_to_rgb(secondary))
    secondary_rgb = hsv_to_rgb(*secondary_hsv)

    # now we have to generate the rest of the palette
    primary_hls = rgb_to_hls(*primary_rgb)
    secondary_hls = rgb_to_hls(*secondary_rgb)
    colors = {"1": "FFFFFF", "2": rgb_to_hex_color(*primary_rgb), "8": rgb_to_hex_color(*secondary_rgb)}
    # start primary as index 2, this is kirby's primary color
    for i, f in enumerate((0.8, 0.6, 0.4, 0.2)):
        colors[f"{i + 3}"] = rgb_to_hex_color(*hls_to_rgb(primary_hls[0], primary_hls[1] * f, primary_hls[2]))
    colors["7"] = rgb_to_hex_color(*hls_to_rgb(secondary_hls[0], secondary_hls[1] * 0.75, secondary_hls[2]))
    return colors


def split_auto_string(palette: str) -> tuple[str, str, str]:
    # format can be one of 3
    # 1. #RRGGBB
    # 2. #RRGGBB|complementary/analogous/intensify
    # 3. #RRGGBB|#RRGGBB
    split_val = palette.split("|")
    if all(x in "abcdef0123456789#" for x in split_val[0].lower()):
        if len(split_val) == 1:
            # we only provided the one string, return
            return (split_val[0], "", "")
        # at least two, check the next value
        if split_val[1] in ("complement", "analogous", "intensify"):
            return (split_val[0], "", split_val[1])
        elif all(x in "abcdef0123456789#" for x in split_val[0].lower()):
            return (split_val[0], split_val[1], "")
    raise OptionError(f"Invalid palette string: {palette}")


def get_palette(world: "KSSWorld", palette: int | str) -> dict[str, str] | None:
    if isinstance(palette, str):
        if palette in world.options.kirby_flavors:
            return world.options.kirby_flavors.get(palette, None)
        else:
            return generate_palette(*split_auto_string(palette))

    return flavor_presets.get(palette, None)


def rgb888_to_bgr555(red: int, green: int, blue: int) -> bytes:
    red = red >> 3
    green = green >> 3
    blue = blue >> 3
    outcol = (blue << 10) + (green << 5) + red
    return outcol.to_bytes(2, "little")


def get_palette_bytes(palette: dict[str, str], factor: tuple[float, float, float]) -> bytes:
    output_data = bytearray()
    for color in [f"{i}" for i in range(1, 9)]:
        col = rgb_to_hls(*color_string_to_rgb(palette[color]))
        col = (col[0] + factor[0], col[1] * factor[1], col[2] * factor[2])
        col = tuple(int(x * 255) for x in hls_to_rgb(*col))
        byte_data = rgb888_to_bgr555(*col)
        output_data.extend(bytearray(byte_data))
    return bytes(output_data)
