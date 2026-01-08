from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import KSSWorld

palette_addresses = {
    "Kirby": [0x467D8],
    "Cutter": [0x469D8],
    "Beam": [0x469F8],
    "Yo-Yo": [0x46A18],
    "Ninja": [0x46A38],
    "Wing": [0x46A58],
    "Fighter": [0x46A78],
    "Jet": [0x46A98],
    "Sword": [0x46AB8],
    "Fire": [0x46AD8, 0x46AF8, 0x46B18, 0x46B38, 0x64B58],
    "Stone": [0x46C18],  # There's one for each transformation, but since they use different setup we won't touch
    "Bomb": [0x46CD8],
    "Plasma": [0x46CF8, 0x46D18, 0x46D38, 0x46D58, 0x46D78, 0x46D98, 0x46DB8, 0x46DD8],
    "Wheel": [0x46DF8, 0x46E18, 0x46E38],
    "Ice": [0x46E58, 0x46E78, 0x46E98],
    "Mirror": [0x46EB8, 0x46ED8, 0x46EF8],
    # "Copy": [],  # too complex for the moment
    "Suplex": [0x471B8],
    "Hammer": [0x471D8],
    "Parasol": [0x471F8],
    # as are the rest of the screen nukes + Sleep
}

palette_factors: dict[int, float] = defaultdict(lambda: 1.0, {
    0x46E36: 1.5
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


def get_palette(world: "KSSWorld", palette: int) -> dict[str, str] | None:
    from .options import KirbyFlavorPreset
    if palette == KirbyFlavorPreset.option_custom:
        return world.options.kirby_flavor.value
    return flavor_presets.get(palette, None)


def rgb888_to_bgr555(red: int, green: int, blue: int) -> bytes:
    red = red >> 3
    green = green >> 3
    blue = blue >> 3
    outcol = (blue << 10) + (green << 5) + red
    return outcol.to_bytes(2, "little")


def get_palette_bytes(palette: dict[str, str], factor: float) -> bytes:
    output_data = bytearray()
    for color in [f"{i}" for i in range(1, 9)]:
        hexcol = palette[color]
        if hexcol.startswith("#"):
            hexcol = hexcol.replace("#", "")
        colint = int(hexcol, 16)
        col: tuple[int, ...] = ((colint & 0xFF0000) >> 16, (colint & 0xFF00) >> 8, colint & 0xFF)
        col = tuple(int(factor*x) for x in col)
        byte_data = rgb888_to_bgr555(col[0], col[1], col[2])
        output_data.extend(bytearray(byte_data))
    return bytes(output_data)
