"""All code related to changing the color of kongs."""

import js
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import CharacterColors, KongModels
from randomizer.Settings import Settings
from randomizer.Patching.Library.Generic import PaletteFillType
from randomizer.Patching.Library.DataTypes import int_to_list
from randomizer.Patching.Library.Image import getKongItemColor, getBonusSkinOffset, ExtraTextures
from randomizer.Patching.Library.Assets import TableNames, getRawFile, writeRawFile
from randomizer.Patching.generate_kong_color_images import convertColors
from randomizer.Patching.Cosmetics.Krusha import kong_index_mapping
from randomizer.Patching.Cosmetics.ModelSwaps import model_texture_sections
from randomizer.Patching.Patcher import LocalROM, ROM

DEFAULT_COLOR = "#000000"


class KongPalette:
    """Class to store information regarding a kong palette."""

    def __init__(self, name: str, image: int, fill_type: PaletteFillType, alt_name: str = None):
        """Initialize with given parameters."""
        self.name = name
        self.image = image
        self.fill_type = fill_type
        self.alt_name = alt_name
        if alt_name is None:
            self.alt_name = name


class KongPaletteSetting:
    """Class to store information regarding the kong palette setting."""

    def __init__(self, kong: str, kong_index: int, palettes: list[KongPalette]):
        """Initialize with given parameters."""
        self.kong = kong
        self.kong_index = kong_index
        self.palettes = palettes.copy()
        self.setting_kong = kong


krusha_texture_replacement = {
    # Textures Krusha can use when he replaces various kongs (Main color, belt color)
    Kongs.donkey: (3724, 0x177D),
    Kongs.diddy: (4971, 4966),
    Kongs.lanky: (3689, 0xE9A),
    Kongs.tiny: (6014, 0xE68),
    Kongs.chunky: (3687, 3778),
}

KONG_ZONES = {
    "DK": ["Fur", "Tie"],
    "Diddy": ["Clothes"],
    "Lanky": ["Clothes", "Fur"],
    "Tiny": ["Clothes", "Hair"],
    "Chunky": ["Main", "Other"],
    "Rambi": ["Skin"],
    "Enguarde": ["Skin"],
}


def writeKongColors(settings: Settings, ROM_COPY: ROM):
    """Write kong colors based on the settings."""
    color_palettes = []
    color_obj = {}
    colors_dict = {}
    kong_settings = [
        KongPaletteSetting(
            "dk",
            0,
            [
                KongPalette("fur", 3724, PaletteFillType.block),
                KongPalette("tie", 0x177D, PaletteFillType.block),
                KongPalette("tie", 0xE8D, PaletteFillType.patch),
            ],
        ),
        KongPaletteSetting(
            "diddy",
            1,
            [
                KongPalette("clothes", 3686, PaletteFillType.block),
                KongPalette("clothes", 0xE6C, PaletteFillType.patch),
            ],
        ),
        KongPaletteSetting(
            "lanky",
            2,
            [
                KongPalette("clothes", 3689, PaletteFillType.block),
                KongPalette("clothes", 3734, PaletteFillType.patch),
                KongPalette("fur", 0xE9A, PaletteFillType.block),
                KongPalette("fur", 0xE94, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "tiny",
            3,
            [
                KongPalette("clothes", 6014, PaletteFillType.block),
                KongPalette("hair", 0xE68, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "chunky",
            4,
            [
                KongPalette("main", 3769, PaletteFillType.checkered, "other"),
                KongPalette("main", 3687, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "rambi",
            5,
            [
                KongPalette("skin", 3826, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "enguarde",
            6,
            [
                KongPalette("skin", 3847, PaletteFillType.block),
            ],
        ),
    ]

    if js.document.getElementById("override_cosmetics").checked or True:
        if js.document.getElementById("random_kong_colors").checked:
            for kong in KONG_ZONES:
                for zone in KONG_ZONES[kong]:
                    settings.__setattr__(f"{kong.lower()}_{zone.lower()}_colors", CharacterColors.randomized)
        else:
            for kong in KONG_ZONES:
                for zone in KONG_ZONES[kong]:
                    settings.__setattr__(
                        f"{kong.lower()}_{zone.lower()}_colors",
                        CharacterColors[js.document.getElementById(f"{kong.lower()}_{zone.lower()}_colors").value],
                    )
                    settings.__setattr__(
                        f"{kong.lower()}_{zone.lower()}_custom_color",
                        js.document.getElementById(f"{kong.lower()}_{zone.lower()}_custom_color").value,
                    )
    else:
        if len(settings.random_colors_selected) > 0:
            for kong in KONG_ZONES:
                for zone in KONG_ZONES[kong]:
                    settings.__setattr__(f"{kong.lower()}_{zone.lower()}_colors", CharacterColors.randomized)

    colors_dict = {}
    for kong in KONG_ZONES:
        for zone in KONG_ZONES[kong]:
            colors_dict[f"{kong.lower()}_{zone.lower()}_colors"] = settings.__getattribute__(f"{kong.lower()}_{zone.lower()}_colors")
            colors_dict[f"{kong.lower()}_{zone.lower()}_custom_color"] = settings.__getattribute__(f"{kong.lower()}_{zone.lower()}_custom_color")
    for kong in kong_settings:
        if kong.kong_index == 4:
            if settings.kong_model_chunky == KongModels.disco_chunky:
                kong.palettes = [
                    KongPalette("main", 3777, PaletteFillType.sparkle),
                    KongPalette("other", 3778, PaletteFillType.sparkle),
                ]
        elif kong.kong_index == 0:
            if settings.kong_model_dk == KongModels.disco_donkey:
                kong.palettes = [
                    KongPalette("fur", getBonusSkinOffset(ExtraTextures.DiscoDonkShirt), PaletteFillType.sparkle),
                    KongPalette("tie", getBonusSkinOffset(ExtraTextures.DiscoDonkGlove), PaletteFillType.sparkle),
                    KongPalette("tie", 0x177D, PaletteFillType.block),
                    KongPalette("tie", 0xE8D, PaletteFillType.patch),
                ]
        settings_values = [
            settings.kong_model_dk,
            settings.kong_model_diddy,
            settings.kong_model_lanky,
            settings.kong_model_tiny,
            settings.kong_model_chunky,
        ]
        if kong.kong_index >= 0 and kong.kong_index < len(settings_values):
            if settings_values[kong.kong_index] in model_texture_sections:
                base_setting = kong.palettes[0].name
                kong.palettes = [
                    KongPalette(base_setting, krusha_texture_replacement[kong.kong_index][0], PaletteFillType.block),  # krusha_skin
                    KongPalette(base_setting, krusha_texture_replacement[kong.kong_index][1], PaletteFillType.kong),  # krusha_indicator
                ]
        base_obj = {"kong": kong.kong, "zones": []}
        zone_to_colors = {}
        for palette in kong.palettes:
            arr = [DEFAULT_COLOR]
            if palette.fill_type == PaletteFillType.checkered:
                arr = ["#FFFF00", "#00FF00"]
            elif palette.fill_type == PaletteFillType.kong:
                arr = [getKongItemColor(settings.colorblind_mode, kong.kong_index)]
            zone_data = {
                "zone": palette.name,
                "image": palette.image,
                "fill_type": palette.fill_type,
                "colors": arr,
            }
            for index in range(len(arr)):
                base_setting = f"{kong.kong}_{palette.name}_colors"
                custom_setting = f"{kong.kong}_{palette.name}_custom_color"
                if index == 1:  # IS THE CHECKERED PATTERN
                    base_setting = f"{kong.kong}_{palette.alt_name}_colors"
                    custom_setting = f"{kong.kong}_{palette.alt_name}_custom_color"
                if (settings.override_cosmetics and colors_dict[base_setting] != CharacterColors.vanilla) or (palette.fill_type == PaletteFillType.kong):
                    color = None
                    # if this palette color is randomized, and isn't krusha's kong indicator:
                    if colors_dict[base_setting] == CharacterColors.randomized and palette.fill_type != PaletteFillType.kong:
                        if base_setting in zone_to_colors:
                            color = zone_to_colors[base_setting]
                        else:
                            color = f"#{format(settings.random.randint(0, 0xFFFFFF), '06x')}"
                            zone_to_colors[base_setting] = color
                    # if this palette color is not randomized (but might be a custom color) and isn't krusha's kong indicator:
                    elif palette.fill_type != PaletteFillType.kong:
                        color = colors_dict[custom_setting]
                        if not color:
                            color = DEFAULT_COLOR
                    # if this is krusha's kong indicator:
                    else:
                        color = getKongItemColor(settings.colorblind_mode, kong.kong_index)
                    if color is not None:
                        zone_data["colors"][index] = color
                        base_obj["zones"].append(zone_data)
                        color_palettes.append(base_obj)
                        color_obj[f"{kong.kong} {palette.name}"] = color
    settings.colors = color_obj
    if len(color_palettes) > 0:
        # this is just to prune the duplicates that appear. someone should probably fix the root of the dupe issue tbh
        new_color_palettes = []
        for pal in color_palettes:
            if pal not in new_color_palettes:
                new_color_palettes.append(pal)
        convertColors(new_color_palettes, ROM_COPY)


def changeModelTextures(settings: Settings, ROM_COPY: LocalROM, kong_index: int):
    """Change the textures associated with a model."""
    settings_values = [
        settings.kong_model_dk,
        settings.kong_model_diddy,
        settings.kong_model_lanky,
        settings.kong_model_tiny,
        settings.kong_model_chunky,
    ]
    if kong_index < 0 or kong_index >= len(settings_values):
        return
    model = settings_values[kong_index]
    if model not in model_texture_sections:
        return
    for x in range(2):
        file = kong_index_mapping[kong_index][x]
        if file is None:
            continue
        data = getRawFile(ROM_COPY, TableNames.ActorGeometry, file, True)
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Retexture for colors
        for tex_idx in model_texture_sections[model]["skin"]:
            for di, d in enumerate(int_to_list(krusha_texture_replacement[kong_index][0], 2)):  # Main
                num_data[tex_idx + di] = d
        for tex_idx in model_texture_sections[model]["kong"]:
            for di, d in enumerate(int_to_list(krusha_texture_replacement[kong_index][1], 2)):  # Belt
                num_data[tex_idx + di] = d
        data = bytearray(num_data)  # convert num_data back to binary string
        writeRawFile(TableNames.ActorGeometry, file, True, data, ROM_COPY)
