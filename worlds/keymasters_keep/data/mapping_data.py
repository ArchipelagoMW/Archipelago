from typing import Any, Dict, Tuple

from ..enums import (
    KeymastersKeepGoals,
    KeymastersKeepItems,
    KeymastersKeepLocations,
    KeymastersKeepGamePlatforms,
    KeymastersKeepRegions,
    KeymastersKeepShops,
    KeymastersKeepShopkeepers,
)


color_to_hex_codes: Dict[str, str] = {
    "aliceblue": "F0F8FF",
    "antiquewhite": "FAEBD7",
    "aqua": "00FFFF",
    "aquamarine": "7FFFD4",
    "azure": "F0FFFF",
    "beige": "F5F5DC",
    "bisque": "FFE4C4",
    "black": "000000",
    "blanchedalmond": "FFEBCD",
    "blue": "0000FF",
    "blueviolet": "8A2BE2",
    "brown": "A52A2A",
    "burlywood": "DEB887",
    "cadetblue": "5F9EA0",
    "chartreuse": "7FFF00",
    "chocolate": "D2691E",
    "coral": "FF7F50",
    "cornflowerblue": "6495ED",
    "cornsilk": "FFF8DC",
    "crimson": "DC143C",
    "cyan": "00FFFF",
    "darkblue": "00008B",
    "darkcyan": "008B8B",
    "darkgoldenrod": "B8860B",
    "darkgray": "A9A9A9",
    "darkgreen": "006400",
    "darkgrey": "A9A9A9",
    "darkkhaki": "BDB76B",
    "darkmagenta": "8B008B",
    "darkolivegreen": "556B2F",
    "darkorange": "FF8C00",
    "darkorchid": "9932CC",
    "darkred": "8B0000",
    "darksalmon": "E9967A",
    "darkseagreen": "8FBC8F",
    "darkslateblue": "483D8B",
    "darkslategray": "2F4F4F",
    "darkslategrey": "2F4F4F",
    "darkturquoise": "00CED1",
    "darkviolet": "9400D3",
    "deeppink": "FF1493",
    "deepskyblue": "00BFFF",
    "dimgray": "696969",
    "dimgrey": "696969",
    "dodgerblue": "1E90FF",
    "firebrick": "B22222",
    "floralwhite": "FFFAF0",
    "forestgreen": "228B22",
    "fuchsia": "FF00FF",
    "gainsboro": "DCDCDC",
    "ghostwhite": "F8F8FF",
    "gold": "FFD700",
    "goldenrod": "DAA520",
    "gray": "808080",
    "green": "008000",
    "greenyellow": "ADFF2F",
    "grey": "808080",
    "honeydew": "F0FFF0",
    "hotpink": "FF69B4",
    "indianred": "CD5C5C",
    "indigo": "4B0082",
    "ivory": "FFFFF0",
    "khaki": "F0E68C",
    "lavender": "E6E6FA",
    "lavenderblush": "FFF0F5",
    "lawngreen": "7CFC00",
    "lemonchiffon": "FFFACD",
    "lightblue": "ADD8E6",
    "lightcoral": "F08080",
    "lightcyan": "E0FFFF",
    "lightgoldenrodyellow": "FAFAD2",
    "lightgray": "D3D3D3",
    "lightgreen": "90EE90",
    "lightgrey": "D3D3D3",
    "lightpink": "FFB6C1",
    "lightsalmon": "FFA07A",
    "lightseagreen": "20B2AA",
    "lightskyblue": "87CEFA",
    "lightslategray": "778899",
    "lightslategrey": "778899",
    "lightsteelblue": "B0C4DE",
    "lightyellow": "FFFFE0",
    "lime": "00FF00",
    "limegreen": "32CD32",
    "linen": "FAF0E6",
    "magenta": "FF00FF",
    "maroon": "800000",
    "mediumaquamarine": "66CDAA",
    "mediumblue": "0000CD",
    "mediumorchid": "BA55D3",
    "mediumpurple": "9370DB",
    "mediumseagreen": "3CB371",
    "mediumslateblue": "7B68EE",
    "mediumspringgreen": "00FA9A",
    "mediumturquoise": "48D1CC",
    "mediumvioletred": "C71585",
    "midnightblue": "191970",
    "mintcream": "F5FFFA",
    "mistyrose": "FFE4E1",
    "moccasin": "FFE4B5",
    "navajowhite": "FFDEAD",
    "navy": "000080",
    "oldlace": "FDF5E6",
    "olive": "808000",
    "olivedrab": "6B8E23",
    "orange": "FFA500",
    "orangered": "FF4500",
    "orchid": "DA70D6",
    "palegoldenrod": "EEE8AA",
    "palegreen": "98FB98",
    "paleturquoise": "AFEEEE",
    "palevioletred": "DB7093",
    "papayawhip": "FFEFD5",
    "peachpuff": "FFDAB9",
    "peru": "CD853F",
    "pink": "FFC0CB",
    "plum": "DDA0DD",
    "powderblue": "B0E0E6",
    "purple": "800080",
    "red": "FF0000",
    "rosybrown": "BC8F8F",
    "royalblue": "4169E1",
    "saddlebrown": "8B4513",
    "salmon": "FA8072",
    "sandybrown": "F4A460",
    "seagreen": "2E8B57",
    "seashell": "FFF5EE",
    "sienna": "A0522D",
    "silver": "C0C0C0",
    "skyblue": "87CEEB",
    "slateblue": "6A5ACD",
    "slategray": "708090",
    "slategrey": "708090",
    "snow": "FFFAFA",
    "springgreen": "00FF7F",
    "steelblue": "4682B4",
    "tan": "D2B48C",
    "teal": "008080",
    "thistle": "D8BFD8",
    "tomato": "FF6347",
    "turquoise": "40E0D0",
    "violet": "EE82EE",
    "wheat": "F5DEB3",
    "white": "FFFFFF",
    "whitesmoke": "F5F5F5",
    "yellow": "FFFF00",
    "yellowgreen": "9ACD32",
}

item_classification_to_colors: Dict[int, str] = {
    0: "00EEEE",
    1: "AF99EF",
    2: "6D8BE8",
    3: "AF99EF",
    4: "FA8072",
    5: "AF99EF",
    6: "6D8BE8",
    7: "AF99EF",
    8: "00EEEE",
    9: "AF99EF",
    10: "6D8BE8",
    11: "AF99EF",
    12: "FA8072",
    13: "AF99EF",
    14: "6D8BE8",
    15: "AF99EF",
}

item_classification_to_rarities: Dict[int, str] = {
    0: "Common",
    1: "Rare",
    2: "Magic",
    3: "Rare",
    4: "Cursed",
    5: "Cursed Rare",
    6: "Cursed Magic",
    7: "Cursed Rare",
    8: "Common",
    9: "Rare",
    10: "Magic",
    11: "Rare",
    12: "Cursed",
    13: "Cursed Rare",
    14: "Cursed Magic",
    15: "Cursed Rare",
}

key_item_to_colors: Dict[KeymastersKeepItems, Tuple[str, str]] = {
    KeymastersKeepItems.KEY_AMBER_INFERNO: ("orange", "darkorange"),
    KeymastersKeepItems.KEY_AMBER_STONE: ("gold", "darkgoldenrod"),
    KeymastersKeepItems.KEY_ASHEN_SPARK: ("gray", "orangered"),
    KeymastersKeepItems.KEY_AURIC_FLASH: ("gold", "goldenrod"),
    KeymastersKeepItems.KEY_AURORA_BEAM: ("powderblue", "darkturquoise"),
    KeymastersKeepItems.KEY_AZURE_TIDE: ("blue", "deepskyblue"),
    KeymastersKeepItems.KEY_BRONZE_ROOT: ("sienna", "peru"),
    KeymastersKeepItems.KEY_CELESTIAL_STAR: ("silver", "dimgray"),
    KeymastersKeepItems.KEY_CERULEAN_RIPPLE: ("royalblue", "cornflowerblue"),
    KeymastersKeepItems.KEY_COBALT_SKY: ("steelblue", "lightskyblue"),
    KeymastersKeepItems.KEY_COPPER_BLOOM: ("chocolate", "saddlebrown"),
    KeymastersKeepItems.KEY_CRIMSON_BLAZE: ("red", "firebrick"),
    KeymastersKeepItems.KEY_CRYSTAL_GLACIER: ("lightcyan", "lightblue"),
    KeymastersKeepItems.KEY_DUSKLIGHT_VEIL: ("darkgray", "tomato"),
    KeymastersKeepItems.KEY_EBONY_OAK: ("black", "darkslategray"),
    KeymastersKeepItems.KEY_ELECTRIC_STORM: ("blue", "aqua"),
    KeymastersKeepItems.KEY_EMERALD_GROVE: ("seagreen", "mediumaquamarine"),
    KeymastersKeepItems.KEY_FROSTBITE: ("azure", "paleturquoise"),
    KeymastersKeepItems.KEY_FROZEN_TWILIGHT: ("thistle", "blueviolet"),
    KeymastersKeepItems.KEY_GLACIAL_SHARD: ("darkturquoise", "mediumturquoise"),
    KeymastersKeepItems.KEY_GOLDEN_BIRCH: ("gold", "khaki"),
    KeymastersKeepItems.KEY_GOLDEN_FLAME: ("gold", "darkorange"),
    KeymastersKeepItems.KEY_GOLDEN_ZEPHYR: ("yellow", "gold"),
    KeymastersKeepItems.KEY_HALO_FLAME: ("darkorange", "tomato"),
    KeymastersKeepItems.KEY_ICY_CASCADE: ("lightskyblue", "powderblue"),
    KeymastersKeepItems.KEY_IRONCLAD: ("darkgray", "slategray"),
    KeymastersKeepItems.KEY_IVORY_DRIFT: ("ivory", "aliceblue"),
    KeymastersKeepItems.KEY_IVORY_SPROUT: ("beige", "mintcream"),
    KeymastersKeepItems.KEY_MAHOGANY_BARK: ("maroon", "saddlebrown"),
    KeymastersKeepItems.KEY_MIDNIGHT_ABYSS: ("midnightblue", "navy"),
    KeymastersKeepItems.KEY_MIDNIGHT_SHADE: ("indigo", "darkslateblue"),
    KeymastersKeepItems.KEY_OBSIDIAN_CORE: ("black", "darkgray"),
    KeymastersKeepItems.KEY_OBSIDIAN_WRAITH: ("darkslategray", "maroon"),
    KeymastersKeepItems.KEY_ONYX_ECLIPSE: ("black", "slategray"),
    KeymastersKeepItems.KEY_PALE_GALE: ("gainsboro", "whitesmoke"),
    KeymastersKeepItems.KEY_PEARLESCENT_GLOW: ("ghostwhite", "honeydew"),
    KeymastersKeepItems.KEY_PLASMA_SURGE: ("blueviolet", "magenta"),
    KeymastersKeepItems.KEY_PLATINUM_FORGE: ("gainsboro", "silver"),
    KeymastersKeepItems.KEY_RADIANT_DAWN: ("orangered", "tomato"),
    KeymastersKeepItems.KEY_RUSTSTONE: ("brown", "darkgoldenrod"),
    KeymastersKeepItems.KEY_SAPPHIRE_SURGE: ("mediumblue", "dodgerblue"),
    KeymastersKeepItems.KEY_SCARLET_EMBER: ("crimson", "darkred"),
    KeymastersKeepItems.KEY_SILVER_BREEZE: ("silver", "lightsteelblue"),
    KeymastersKeepItems.KEY_SILVER_SHIELD: ("gray", "slategray"),
    KeymastersKeepItems.KEY_SNOWDRIFT: ("snow", "aliceblue"),
    KeymastersKeepItems.KEY_STORMCALL: ("slategray", "steelblue"),
    KeymastersKeepItems.KEY_STORMCLOUD: ("darkgray", "indigo"),
    KeymastersKeepItems.KEY_VERDANT_MOSS: ("darkolivegreen", "olivedrab"),
    KeymastersKeepItems.KEY_VERDANT_TIMBER: ("forestgreen", "seagreen"),
    KeymastersKeepItems.KEY_VOID_EMBER: ("black", "orangered"),
}

label_mapping: Dict[Any, str] = {
    False: "Off",
    True: "On",
    KeymastersKeepGoals.KEYMASTERS_CHALLENGE: "Keymaster's Challenge",
    KeymastersKeepGoals.MAGIC_KEY_HEIST: "Magic Key Heist",
    KeymastersKeepGamePlatforms._32X: "Sega 32X",
    KeymastersKeepGamePlatforms._3DO: "3DO Multiplayer",
    KeymastersKeepGamePlatforms._3DS: "Nintendo 3DS",
    KeymastersKeepGamePlatforms.A2: "Apple II",
    KeymastersKeepGamePlatforms.A26: "Atari 2600",
    KeymastersKeepGamePlatforms.A2GS: "Apple IIGS",
    KeymastersKeepGamePlatforms.A52: "Atari 5200",
    KeymastersKeepGamePlatforms.A78: "Atari 7800",
    KeymastersKeepGamePlatforms.A8: "Atari 8-bit: 400, 800, XL, XE",
    KeymastersKeepGamePlatforms.ADV: "Entex AdventureVision",
    KeymastersKeepGamePlatforms.AMI: "Commodore Amiga",
    KeymastersKeepGamePlatforms.AND: "Android",
    KeymastersKeepGamePlatforms.ARC: "Arcade",
    KeymastersKeepGamePlatforms.ARCH: "Acorn Archimedes",
    KeymastersKeepGamePlatforms.AST: "Atari ST",
    KeymastersKeepGamePlatforms.BA: "Bally Astrocade",
    KeymastersKeepGamePlatforms.BB: "BlackBerry",
    KeymastersKeepGamePlatforms.BBCM: "BBC Micro",
    KeymastersKeepGamePlatforms.BOARD: "Board Game (Physical)",
    KeymastersKeepGamePlatforms.BREW: "Qualcomm BREW",
    KeymastersKeepGamePlatforms.C64: "Commodore 64",
    KeymastersKeepGamePlatforms.C128: "Commodore 128",
    KeymastersKeepGamePlatforms.CARD: "Card Game (Physical)",
    KeymastersKeepGamePlatforms.CD32: "Amiga CD32",
    KeymastersKeepGamePlatforms.CDI: "Philips CD-i",
    KeymastersKeepGamePlatforms.CDTV: "Commodore CDTV",
    KeymastersKeepGamePlatforms.CHF: "Fairchild Channel F",
    KeymastersKeepGamePlatforms.CP4: "Commodore 116, 16, Plus/4",
    KeymastersKeepGamePlatforms.CPC: "Amstrad CPC 464, CPC664, CPC6128",
    KeymastersKeepGamePlatforms.CV: "ColecoVision",
    KeymastersKeepGamePlatforms.DC: "Sega Dreamcast",
    KeymastersKeepGamePlatforms.DOS: "MS-DOS",
    KeymastersKeepGamePlatforms.ELEC: "Acorn Electron",
    KeymastersKeepGamePlatforms.EXEN: "In-Fusion ExEn",
    KeymastersKeepGamePlatforms.FAL: "Atari Falcon030",
    KeymastersKeepGamePlatforms.FC: "Nintendo Famicom",
    KeymastersKeepGamePlatforms.FDS: "Nintendo Famicom Disk System",
    KeymastersKeepGamePlatforms.FIRE: "Amazon Fire OS",
    KeymastersKeepGamePlatforms.FM7: "Fujitsu FM-7",
    KeymastersKeepGamePlatforms.FMT: "Fujitsu FM Towns",
    KeymastersKeepGamePlatforms.GB: "Nintendo Game Boy",
    KeymastersKeepGamePlatforms.GBA: "Nintendo Game Boy Advance",
    KeymastersKeepGamePlatforms.GBC: "Nintendo Game Boy Color",
    KeymastersKeepGamePlatforms.GC: "Nintendo GameCube",
    KeymastersKeepGamePlatforms.GCOM: "Tiger Game.com",
    KeymastersKeepGamePlatforms.GEN: "Sega Genesis",
    KeymastersKeepGamePlatforms.GG: "Sega Game Gear",
    KeymastersKeepGamePlatforms.GIZ: "Tiger Gizmondo",
    KeymastersKeepGamePlatforms.GW: "Nintendo Game & Watch",
    KeymastersKeepGamePlatforms.GX4: "Amstrad GX4000",
    KeymastersKeepGamePlatforms.IMOD: "NTT DoCoMo i-mode",
    KeymastersKeepGamePlatforms.INTV: "Intellivision, Intellivision II",
    KeymastersKeepGamePlatforms.IOS: "Apple iOS",
    KeymastersKeepGamePlatforms.J2ME: "Sun Java 2 Micro Edition",
    KeymastersKeepGamePlatforms.JAG: "Atari Jaguar",
    KeymastersKeepGamePlatforms.JCD: "Atari Jaguar CD",
    KeymastersKeepGamePlatforms.LASR: "Pioneer LaserActive",
    KeymastersKeepGamePlatforms.LYNX: "Atari Lynx",
    KeymastersKeepGamePlatforms.MART: "Fujitsu FM Towns Marty",
    KeymastersKeepGamePlatforms.MCD: "Sega Mega CD",
    KeymastersKeepGamePlatforms.META: "Metagame",
    KeymastersKeepGamePlatforms.MOD: "Modded Game",
    KeymastersKeepGamePlatforms.MSX: "MSX",
    KeymastersKeepGamePlatforms.MSX2: "MSX2, MSX2+, MSX TurboR",
    KeymastersKeepGamePlatforms.N64: "Nintendo 64",
    KeymastersKeepGamePlatforms.NDS: "Nintendo DS",
    KeymastersKeepGamePlatforms.NES: "Nintendo Entertainment System",
    KeymastersKeepGamePlatforms.NG: "SNK Neo Geo",
    KeymastersKeepGamePlatforms.NGAGE: "Nokia N-GAGE",
    KeymastersKeepGamePlatforms.NGCD: "SNK Neo Geo CD",
    KeymastersKeepGamePlatforms.NGP: "SNK Neo Geo Pocket",
    KeymastersKeepGamePlatforms.NGPC: "SNK Neo Geo Pocket Color",
    KeymastersKeepGamePlatforms.ODY2: "Magnavox Odyssey 2",
    KeymastersKeepGamePlatforms.OUYA: "Ouya",
    KeymastersKeepGamePlatforms.PALM: "Palm OS",
    KeymastersKeepGamePlatforms.PBL: "Pinball",
    KeymastersKeepGamePlatforms.PC: "PC",
    KeymastersKeepGamePlatforms.PC10: "Nintendo PlayChoice-10",
    KeymastersKeepGamePlatforms.PC88: "NEC PC-8801",
    KeymastersKeepGamePlatforms.PC98: "NEC PC-9801",
    KeymastersKeepGamePlatforms.PCB: "PC Boot Loader",
    KeymastersKeepGamePlatforms.PCCD: "NEC PC Engine CD-ROM",
    KeymastersKeepGamePlatforms.PCE: "NEC PC Engine",
    KeymastersKeepGamePlatforms.PCED: "NEC PC Engine Duo",
    KeymastersKeepGamePlatforms.PICO: "Sega Pico / Kids Computer Pico",
    KeymastersKeepGamePlatforms.PICO8: "PICO-8 Fantasy Console",
    KeymastersKeepGamePlatforms.PPC: "Microsoft Pocket PC",
    KeymastersKeepGamePlatforms.PS1: "Sony PlayStation",
    KeymastersKeepGamePlatforms.PS2: "Sony PlayStation 2",
    KeymastersKeepGamePlatforms.PS3: "Sony PlayStation 3",
    KeymastersKeepGamePlatforms.PS4: "Sony PlayStation 4",
    KeymastersKeepGamePlatforms.PS5: "Sony PlayStation 5",
    KeymastersKeepGamePlatforms.PSP: "Sony PlayStation Portable",
    KeymastersKeepGamePlatforms.QL: "Sinclair Quantum Leap",
    KeymastersKeepGamePlatforms.SAM: "Sam Coupe",
    KeymastersKeepGamePlatforms.SAT: "Sega Saturn",
    KeymastersKeepGamePlatforms.SCD: "Sega CD",
    KeymastersKeepGamePlatforms.SFC: "Nintendo Super Famicom",
    KeymastersKeepGamePlatforms.SLOT: "Slot Machine",
    KeymastersKeepGamePlatforms.SM3: "Sega Mark III",
    KeymastersKeepGamePlatforms.SMD: "Sega Mega Drive",
    KeymastersKeepGamePlatforms.SMS: "Sega Master System",
    KeymastersKeepGamePlatforms.SNES: "Super Nintendo Entertainment System",
    KeymastersKeepGamePlatforms.SW: "Nintendo Switch",
    KeymastersKeepGamePlatforms.SYM: "Symbian",
    KeymastersKeepGamePlatforms.TD: "NEC TurboDuo",
    KeymastersKeepGamePlatforms.TG16: "NEC TurboGrafx-16",
    KeymastersKeepGamePlatforms.TGCD: "NEC TurboGrafx CD-ROM",
    KeymastersKeepGamePlatforms.TMO: "Thomson MO",
    KeymastersKeepGamePlatforms.TRSC: "Radio Shack TRS-80 Color Computer",
    KeymastersKeepGamePlatforms.TRS: "Radio Shack TRS-80",
    KeymastersKeepGamePlatforms.TTO: "Thomson TO",
    KeymastersKeepGamePlatforms.VB: "Nintendo Virtual Boy",
    KeymastersKeepGamePlatforms.VECT: "General Consumer Electric Vectrex",
    KeymastersKeepGamePlatforms.VIC: "Commodore VIC 20",
    KeymastersKeepGamePlatforms.VITA: "Sony PlayStation Vita",
    KeymastersKeepGamePlatforms.VR: "Virtual Reality",
    KeymastersKeepGamePlatforms.VS: "Nintendo VS. System",
    KeymastersKeepGamePlatforms.VVS: "V-Tech V-Smile",
    KeymastersKeepGamePlatforms.VSP: "V-Tech V-Smile Pocket",
    KeymastersKeepGamePlatforms.W16: "16-bit Microsoft Windows: 1, 2, 3, 3.1, 3.11",
    KeymastersKeepGamePlatforms.WCE: "Microsoft Windows CE",
    KeymastersKeepGamePlatforms.WEB: "Web Browser",
    KeymastersKeepGamePlatforms.WII: "Nintendo Wii",
    KeymastersKeepGamePlatforms.WIIU: "Nintendo Wii U",
    KeymastersKeepGamePlatforms.WMOB: "Windows Mobile: 2003, 2003 SE, 5, 6, 6.1, 6.5",
    KeymastersKeepGamePlatforms.WPH: "Windows Phone",
    KeymastersKeepGamePlatforms.WS: "Bandai WonderSwan",
    KeymastersKeepGamePlatforms.WSC: "Bandai WonderSwan Color",
    KeymastersKeepGamePlatforms.X1: "Sharp X1",
    KeymastersKeepGamePlatforms.X360: "Microsoft Xbox 360",
    KeymastersKeepGamePlatforms.X68: "Sharp X68000",
    KeymastersKeepGamePlatforms.XBOX: "Microsoft Xbox",
    KeymastersKeepGamePlatforms.XEGS: "Atari XEGS",
    KeymastersKeepGamePlatforms.XONE: "Microsoft Xbox One",
    KeymastersKeepGamePlatforms.XSX: "Microsoft Xbox Series X/S",
    KeymastersKeepGamePlatforms.ZEBO: "Zeebo Zeebo",
    KeymastersKeepGamePlatforms.ZOD: "Tapwave Zodiac",
    KeymastersKeepGamePlatforms.ZXS: "Sinclair ZX Spectrum",
}

region_to_trial_locations: Dict[KeymastersKeepRegions, KeymastersKeepLocations] = {
    KeymastersKeepRegions.THE_ARCANE_DOOR: KeymastersKeepLocations.THE_ARCANE_DOOR_TRIAL,
    KeymastersKeepRegions.THE_ARCANE_PASSAGE: KeymastersKeepLocations.THE_ARCANE_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_ARCANE_THRESHOLD: KeymastersKeepLocations.THE_ARCANE_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_CLANDESTINE_PASSAGE: KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_CLOAKED_ENTRANCE: KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_TRIAL,
    KeymastersKeepRegions.THE_CLOAKED_THRESHOLD: KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_CLOAKED_VAULT: KeymastersKeepLocations.THE_CLOAKED_VAULT_TRIAL,
    KeymastersKeepRegions.THE_CONCEALED_THRESHOLD: KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_CONCEALED_VAULT: KeymastersKeepLocations.THE_CONCEALED_VAULT_TRIAL,
    KeymastersKeepRegions.THE_CRYPTIC_CHAMBER: KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_TRIAL,
    KeymastersKeepRegions.THE_CRYPTIC_GATEWAY: KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_CRYPTIC_VAULT: KeymastersKeepLocations.THE_CRYPTIC_VAULT_TRIAL,
    KeymastersKeepRegions.THE_DISGUISED_GATEWAY: KeymastersKeepLocations.THE_DISGUISED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_ECHOING_PASSAGE: KeymastersKeepLocations.THE_ECHOING_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_ELUSIVE_DOOR: KeymastersKeepLocations.THE_ELUSIVE_DOOR_TRIAL,
    KeymastersKeepRegions.THE_ENCHANTED_GATEWAY: KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_ENCHANTED_PASSAGE: KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_ENIGMATIC_PORTAL: KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_ENIGMATIC_THRESHOLD: KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_FADED_GATEWAY: KeymastersKeepLocations.THE_FADED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_FAINT_DOORWAY: KeymastersKeepLocations.THE_FAINT_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_FAINT_PATH: KeymastersKeepLocations.THE_FAINT_PATH_TRIAL,
    KeymastersKeepRegions.THE_FAINT_THRESHOLD: KeymastersKeepLocations.THE_FAINT_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_FORBIDDEN_ENTRANCE: KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_TRIAL,
    KeymastersKeepRegions.THE_FORGOTTEN_DOOR: KeymastersKeepLocations.THE_FORGOTTEN_DOOR_TRIAL,
    KeymastersKeepRegions.THE_FORGOTTEN_GATEWAY: KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_FORGOTTEN_PORTAL: KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_FORGOTTEN_THRESHOLD: KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_GHOSTED_PASSAGEWAY: KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_TRIAL,
    KeymastersKeepRegions.THE_GHOSTLY_PASSAGE: KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_ARCHWAY: KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_CHAMBER: KeymastersKeepLocations.THE_HIDDEN_CHAMBER_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_DOORWAY: KeymastersKeepLocations.THE_HIDDEN_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_ENTRANCE: KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_KEYHOLE: KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_PASSAGEWAY: KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_PATH: KeymastersKeepLocations.THE_HIDDEN_PATH_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_REACH: KeymastersKeepLocations.THE_HIDDEN_REACH_TRIAL,
    KeymastersKeepRegions.THE_HIDDEN_VAULT: KeymastersKeepLocations.THE_HIDDEN_VAULT_TRIAL,
    KeymastersKeepRegions.THE_INCONSPICUOUS_DOOR: KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_TRIAL,
    KeymastersKeepRegions.THE_INVISIBLE_DOORWAY: KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_LOCKED_DOORWAY: KeymastersKeepLocations.THE_LOCKED_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_LOCKED_GATEWAY: KeymastersKeepLocations.THE_LOCKED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_LOST_ARCHWAY: KeymastersKeepLocations.THE_LOST_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_LOST_PORTAL: KeymastersKeepLocations.THE_LOST_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_LOST_THRESHOLD: KeymastersKeepLocations.THE_LOST_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_MYSTERIOUS_ARCH: KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_TRIAL,
    KeymastersKeepRegions.THE_MYSTERIOUS_DOORWAY: KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_MYSTERIOUS_PASSAGE: KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_MYSTERIOUS_VAULT: KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_TRIAL,
    KeymastersKeepRegions.THE_MYSTICAL_PASSAGE: KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_OBSCURED_ARCH: KeymastersKeepLocations.THE_OBSCURED_ARCH_TRIAL,
    KeymastersKeepRegions.THE_OBSCURED_DOORWAY: KeymastersKeepLocations.THE_OBSCURED_DOORWAY_TRIAL,
    KeymastersKeepRegions.THE_OBSCURED_PORTAL: KeymastersKeepLocations.THE_OBSCURED_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_OBSCURED_VAULT: KeymastersKeepLocations.THE_OBSCURED_VAULT_TRIAL,
    KeymastersKeepRegions.THE_OBSCURE_PASSAGE: KeymastersKeepLocations.THE_OBSCURE_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_PHANTOM_PASSAGE: KeymastersKeepLocations.THE_PHANTOM_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_PHANTOM_VAULT: KeymastersKeepLocations.THE_PHANTOM_VAULT_TRIAL,
    KeymastersKeepRegions.THE_QUIET_ARCHWAY: KeymastersKeepLocations.THE_QUIET_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_QUIET_THRESHOLD: KeymastersKeepLocations.THE_QUIET_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SEALED_CHAMBER: KeymastersKeepLocations.THE_SEALED_CHAMBER_TRIAL,
    KeymastersKeepRegions.THE_SEALED_GATEWAY: KeymastersKeepLocations.THE_SEALED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_SEALED_THRESHOLD: KeymastersKeepLocations.THE_SEALED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SECRETED_DOOR: KeymastersKeepLocations.THE_SECRETED_DOOR_TRIAL,
    KeymastersKeepRegions.THE_SECRETIVE_DOOR: KeymastersKeepLocations.THE_SECRETIVE_DOOR_TRIAL,
    KeymastersKeepRegions.THE_SECRET_ARCHWAY: KeymastersKeepLocations.THE_SECRET_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_SECRET_PASSAGEWAY: KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_TRIAL,
    KeymastersKeepRegions.THE_SECRET_THRESHOLD: KeymastersKeepLocations.THE_SECRET_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SECRET_VAULT: KeymastersKeepLocations.THE_SECRET_VAULT_TRIAL,
    KeymastersKeepRegions.THE_SHADOWED_PORTAL: KeymastersKeepLocations.THE_SHADOWED_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_SHADOWED_THRESHOLD: KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SHADOWY_PASSAGE: KeymastersKeepLocations.THE_SHADOWY_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_SHIMMERING_PASSAGE: KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_SHROUDED_GATEWAY: KeymastersKeepLocations.THE_SHROUDED_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_SHROUDED_PORTAL: KeymastersKeepLocations.THE_SHROUDED_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_SILENT_ARCHWAY: KeymastersKeepLocations.THE_SILENT_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_SILENT_PASSAGE: KeymastersKeepLocations.THE_SILENT_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_SILENT_THRESHOLD: KeymastersKeepLocations.THE_SILENT_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_SILENT_VAULT: KeymastersKeepLocations.THE_SILENT_VAULT_TRIAL,
    KeymastersKeepRegions.THE_UNFATHOMABLE_DOOR: KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_TRIAL,
    KeymastersKeepRegions.THE_UNKNOWN_ARCH: KeymastersKeepLocations.THE_UNKNOWN_ARCH_TRIAL,
    KeymastersKeepRegions.THE_UNKNOWN_GATEWAY: KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_UNMARKED_PASSAGE: KeymastersKeepLocations.THE_UNMARKED_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_UNMARKED_VAULT: KeymastersKeepLocations.THE_UNMARKED_VAULT_TRIAL,
    KeymastersKeepRegions.THE_UNRAVELED_DOOR: KeymastersKeepLocations.THE_UNRAVELED_DOOR_TRIAL,
    KeymastersKeepRegions.THE_UNSEEN_ARCHWAY: KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_UNSEEN_DOOR: KeymastersKeepLocations.THE_UNSEEN_DOOR_TRIAL,
    KeymastersKeepRegions.THE_UNSEEN_PASSAGE: KeymastersKeepLocations.THE_UNSEEN_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_UNSEEN_PORTAL: KeymastersKeepLocations.THE_UNSEEN_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_UNSPOKEN_GATE: KeymastersKeepLocations.THE_UNSPOKEN_GATE_TRIAL,
    KeymastersKeepRegions.THE_UNTOLD_GATEWAY: KeymastersKeepLocations.THE_UNTOLD_GATEWAY_TRIAL,
    KeymastersKeepRegions.THE_UNTRACEABLE_PATH: KeymastersKeepLocations.THE_UNTRACEABLE_PATH_TRIAL,
    KeymastersKeepRegions.THE_VANISHING_ARCHWAY: KeymastersKeepLocations.THE_VANISHING_ARCHWAY_TRIAL,
    KeymastersKeepRegions.THE_VANISHING_DOOR: KeymastersKeepLocations.THE_VANISHING_DOOR_TRIAL,
    KeymastersKeepRegions.THE_VAULT_OF_WHISPERS: KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_TRIAL,
    KeymastersKeepRegions.THE_VEILED_PASSAGE: KeymastersKeepLocations.THE_VEILED_PASSAGE_TRIAL,
    KeymastersKeepRegions.THE_VEILED_PATH: KeymastersKeepLocations.THE_VEILED_PATH_TRIAL,
    KeymastersKeepRegions.THE_WHISPERED_PORTAL: KeymastersKeepLocations.THE_WHISPERED_PORTAL_TRIAL,
    KeymastersKeepRegions.THE_WHISPERED_THRESHOLD: KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_TRIAL,
    KeymastersKeepRegions.THE_WHISPERING_DOOR: KeymastersKeepLocations.THE_WHISPERING_DOOR_TRIAL,
}

region_to_unlock_location_and_item: Dict[KeymastersKeepRegions, Tuple[KeymastersKeepLocations, KeymastersKeepItems]] = {
    KeymastersKeepRegions.THE_ARCANE_DOOR: (
        KeymastersKeepLocations.THE_ARCANE_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ARCANE_DOOR
    ),
    KeymastersKeepRegions.THE_ARCANE_PASSAGE: (
        KeymastersKeepLocations.THE_ARCANE_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ARCANE_PASSAGE
    ),
    KeymastersKeepRegions.THE_ARCANE_THRESHOLD: (
        KeymastersKeepLocations.THE_ARCANE_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ARCANE_THRESHOLD
    ),
    KeymastersKeepRegions.THE_CLANDESTINE_PASSAGE: (
        KeymastersKeepLocations.THE_CLANDESTINE_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CLANDESTINE_PASSAGE
    ),
    KeymastersKeepRegions.THE_CLOAKED_ENTRANCE: (
        KeymastersKeepLocations.THE_CLOAKED_ENTRANCE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CLOAKED_ENTRANCE
    ),
    KeymastersKeepRegions.THE_CLOAKED_THRESHOLD: (
        KeymastersKeepLocations.THE_CLOAKED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CLOAKED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_CLOAKED_VAULT: (
        KeymastersKeepLocations.THE_CLOAKED_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CLOAKED_VAULT
    ),
    KeymastersKeepRegions.THE_CONCEALED_THRESHOLD: (
        KeymastersKeepLocations.THE_CONCEALED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CONCEALED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_CONCEALED_VAULT: (
        KeymastersKeepLocations.THE_CONCEALED_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CONCEALED_VAULT
    ),
    KeymastersKeepRegions.THE_CRYPTIC_CHAMBER: (
        KeymastersKeepLocations.THE_CRYPTIC_CHAMBER_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CRYPTIC_CHAMBER
    ),
    KeymastersKeepRegions.THE_CRYPTIC_GATEWAY: (
        KeymastersKeepLocations.THE_CRYPTIC_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CRYPTIC_GATEWAY
    ),
    KeymastersKeepRegions.THE_CRYPTIC_VAULT: (
        KeymastersKeepLocations.THE_CRYPTIC_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_CRYPTIC_VAULT
    ),
    KeymastersKeepRegions.THE_DISGUISED_GATEWAY: (
        KeymastersKeepLocations.THE_DISGUISED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_DISGUISED_GATEWAY
    ),
    KeymastersKeepRegions.THE_ECHOING_PASSAGE: (
        KeymastersKeepLocations.THE_ECHOING_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ECHOING_PASSAGE
    ),
    KeymastersKeepRegions.THE_ELUSIVE_DOOR: (
        KeymastersKeepLocations.THE_ELUSIVE_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ELUSIVE_DOOR
    ),
    KeymastersKeepRegions.THE_ENCHANTED_GATEWAY: (
        KeymastersKeepLocations.THE_ENCHANTED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ENCHANTED_GATEWAY
    ),
    KeymastersKeepRegions.THE_ENCHANTED_PASSAGE: (
        KeymastersKeepLocations.THE_ENCHANTED_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ENCHANTED_PASSAGE
    ),
    KeymastersKeepRegions.THE_ENIGMATIC_PORTAL: (
        KeymastersKeepLocations.THE_ENIGMATIC_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ENIGMATIC_PORTAL
    ),
    KeymastersKeepRegions.THE_ENIGMATIC_THRESHOLD: (
        KeymastersKeepLocations.THE_ENIGMATIC_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_ENIGMATIC_THRESHOLD
    ),
    KeymastersKeepRegions.THE_FADED_GATEWAY: (
        KeymastersKeepLocations.THE_FADED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FADED_GATEWAY
    ),
    KeymastersKeepRegions.THE_FAINT_DOORWAY: (
        KeymastersKeepLocations.THE_FAINT_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FAINT_DOORWAY
    ),
    KeymastersKeepRegions.THE_FAINT_PATH: (
        KeymastersKeepLocations.THE_FAINT_PATH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FAINT_PATH
    ),
    KeymastersKeepRegions.THE_FAINT_THRESHOLD: (
        KeymastersKeepLocations.THE_FAINT_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FAINT_THRESHOLD
    ),
    KeymastersKeepRegions.THE_FORBIDDEN_ENTRANCE: (
        KeymastersKeepLocations.THE_FORBIDDEN_ENTRANCE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORBIDDEN_ENTRANCE
    ),
    KeymastersKeepRegions.THE_FORGOTTEN_DOOR: (
        KeymastersKeepLocations.THE_FORGOTTEN_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_DOOR
    ),
    KeymastersKeepRegions.THE_FORGOTTEN_GATEWAY: (
        KeymastersKeepLocations.THE_FORGOTTEN_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_GATEWAY
    ),
    KeymastersKeepRegions.THE_FORGOTTEN_PORTAL: (
        KeymastersKeepLocations.THE_FORGOTTEN_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_PORTAL
    ),
    KeymastersKeepRegions.THE_FORGOTTEN_THRESHOLD: (
        KeymastersKeepLocations.THE_FORGOTTEN_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_FORGOTTEN_THRESHOLD
    ),
    KeymastersKeepRegions.THE_GHOSTED_PASSAGEWAY: (
        KeymastersKeepLocations.THE_GHOSTED_PASSAGEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_GHOSTED_PASSAGEWAY
    ),
    KeymastersKeepRegions.THE_GHOSTLY_PASSAGE: (
        KeymastersKeepLocations.THE_GHOSTLY_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_GHOSTLY_PASSAGE
    ),
    KeymastersKeepRegions.THE_HIDDEN_ARCHWAY: (
        KeymastersKeepLocations.THE_HIDDEN_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_ARCHWAY
    ),
    KeymastersKeepRegions.THE_HIDDEN_CHAMBER: (
        KeymastersKeepLocations.THE_HIDDEN_CHAMBER_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_CHAMBER
    ),
    KeymastersKeepRegions.THE_HIDDEN_DOORWAY: (
        KeymastersKeepLocations.THE_HIDDEN_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_DOORWAY
    ),
    KeymastersKeepRegions.THE_HIDDEN_ENTRANCE: (
        KeymastersKeepLocations.THE_HIDDEN_ENTRANCE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_ENTRANCE
    ),
    KeymastersKeepRegions.THE_HIDDEN_KEYHOLE: (
        KeymastersKeepLocations.THE_HIDDEN_KEYHOLE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_KEYHOLE
    ),
    KeymastersKeepRegions.THE_HIDDEN_PASSAGEWAY: (
        KeymastersKeepLocations.THE_HIDDEN_PASSAGEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_PASSAGEWAY
    ),
    KeymastersKeepRegions.THE_HIDDEN_PATH: (
        KeymastersKeepLocations.THE_HIDDEN_PATH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_PATH
    ),
    KeymastersKeepRegions.THE_HIDDEN_REACH: (
        KeymastersKeepLocations.THE_HIDDEN_REACH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_REACH
    ),
    KeymastersKeepRegions.THE_HIDDEN_VAULT: (
        KeymastersKeepLocations.THE_HIDDEN_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_HIDDEN_VAULT
    ),
    KeymastersKeepRegions.THE_INCONSPICUOUS_DOOR: (
        KeymastersKeepLocations.THE_INCONSPICUOUS_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_INCONSPICUOUS_DOOR
    ),
    KeymastersKeepRegions.THE_INVISIBLE_DOORWAY: (
        KeymastersKeepLocations.THE_INVISIBLE_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_INVISIBLE_DOORWAY
    ),
    KeymastersKeepRegions.THE_LOCKED_DOORWAY: (
        KeymastersKeepLocations.THE_LOCKED_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOCKED_DOORWAY
    ),
    KeymastersKeepRegions.THE_LOCKED_GATEWAY: (
        KeymastersKeepLocations.THE_LOCKED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOCKED_GATEWAY
    ),
    KeymastersKeepRegions.THE_LOST_ARCHWAY: (
        KeymastersKeepLocations.THE_LOST_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOST_ARCHWAY
    ),
    KeymastersKeepRegions.THE_LOST_PORTAL: (
        KeymastersKeepLocations.THE_LOST_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOST_PORTAL
    ),
    KeymastersKeepRegions.THE_LOST_THRESHOLD: (
        KeymastersKeepLocations.THE_LOST_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_LOST_THRESHOLD
    ),
    KeymastersKeepRegions.THE_MYSTERIOUS_ARCH: (
        KeymastersKeepLocations.THE_MYSTERIOUS_ARCH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_ARCH
    ),
    KeymastersKeepRegions.THE_MYSTERIOUS_DOORWAY: (
        KeymastersKeepLocations.THE_MYSTERIOUS_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_DOORWAY
    ),
    KeymastersKeepRegions.THE_MYSTERIOUS_PASSAGE: (
        KeymastersKeepLocations.THE_MYSTERIOUS_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_PASSAGE
    ),
    KeymastersKeepRegions.THE_MYSTERIOUS_VAULT: (
        KeymastersKeepLocations.THE_MYSTERIOUS_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTERIOUS_VAULT
    ),
    KeymastersKeepRegions.THE_MYSTICAL_PASSAGE: (
        KeymastersKeepLocations.THE_MYSTICAL_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_MYSTICAL_PASSAGE
    ),
    KeymastersKeepRegions.THE_OBSCURED_ARCH: (
        KeymastersKeepLocations.THE_OBSCURED_ARCH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURED_ARCH
    ),
    KeymastersKeepRegions.THE_OBSCURED_DOORWAY: (
        KeymastersKeepLocations.THE_OBSCURED_DOORWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURED_DOORWAY
    ),
    KeymastersKeepRegions.THE_OBSCURED_PORTAL: (
        KeymastersKeepLocations.THE_OBSCURED_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURED_PORTAL
    ),
    KeymastersKeepRegions.THE_OBSCURED_VAULT: (
        KeymastersKeepLocations.THE_OBSCURED_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURED_VAULT
    ),
    KeymastersKeepRegions.THE_OBSCURE_PASSAGE: (
        KeymastersKeepLocations.THE_OBSCURE_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_OBSCURE_PASSAGE
    ),
    KeymastersKeepRegions.THE_PHANTOM_PASSAGE: (
        KeymastersKeepLocations.THE_PHANTOM_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_PHANTOM_PASSAGE
    ),
    KeymastersKeepRegions.THE_PHANTOM_VAULT: (
        KeymastersKeepLocations.THE_PHANTOM_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_PHANTOM_VAULT
    ),
    KeymastersKeepRegions.THE_QUIET_ARCHWAY: (
        KeymastersKeepLocations.THE_QUIET_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_QUIET_ARCHWAY
    ),
    KeymastersKeepRegions.THE_QUIET_THRESHOLD: (
        KeymastersKeepLocations.THE_QUIET_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_QUIET_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SEALED_CHAMBER: (
        KeymastersKeepLocations.THE_SEALED_CHAMBER_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SEALED_CHAMBER
    ),
    KeymastersKeepRegions.THE_SEALED_GATEWAY: (
        KeymastersKeepLocations.THE_SEALED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SEALED_GATEWAY
    ),
    KeymastersKeepRegions.THE_SEALED_THRESHOLD: (
        KeymastersKeepLocations.THE_SEALED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SEALED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SECRETED_DOOR: (
        KeymastersKeepLocations.THE_SECRETED_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRETED_DOOR
    ),
    KeymastersKeepRegions.THE_SECRETIVE_DOOR: (
        KeymastersKeepLocations.THE_SECRETIVE_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRETIVE_DOOR
    ),
    KeymastersKeepRegions.THE_SECRET_ARCHWAY: (
        KeymastersKeepLocations.THE_SECRET_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRET_ARCHWAY
    ),
    KeymastersKeepRegions.THE_SECRET_PASSAGEWAY: (
        KeymastersKeepLocations.THE_SECRET_PASSAGEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRET_PASSAGEWAY
    ),
    KeymastersKeepRegions.THE_SECRET_THRESHOLD: (
        KeymastersKeepLocations.THE_SECRET_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRET_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SECRET_VAULT: (
        KeymastersKeepLocations.THE_SECRET_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SECRET_VAULT
    ),
    KeymastersKeepRegions.THE_SHADOWED_PORTAL: (
        KeymastersKeepLocations.THE_SHADOWED_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHADOWED_PORTAL
    ),
    KeymastersKeepRegions.THE_SHADOWED_THRESHOLD: (
        KeymastersKeepLocations.THE_SHADOWED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHADOWED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SHADOWY_PASSAGE: (
        KeymastersKeepLocations.THE_SHADOWY_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHADOWY_PASSAGE
    ),
    KeymastersKeepRegions.THE_SHIMMERING_PASSAGE: (
        KeymastersKeepLocations.THE_SHIMMERING_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHIMMERING_PASSAGE
    ),
    KeymastersKeepRegions.THE_SHROUDED_GATEWAY: (
        KeymastersKeepLocations.THE_SHROUDED_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHROUDED_GATEWAY
    ),
    KeymastersKeepRegions.THE_SHROUDED_PORTAL: (
        KeymastersKeepLocations.THE_SHROUDED_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SHROUDED_PORTAL
    ),
    KeymastersKeepRegions.THE_SILENT_ARCHWAY: (
        KeymastersKeepLocations.THE_SILENT_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SILENT_ARCHWAY
    ),
    KeymastersKeepRegions.THE_SILENT_PASSAGE: (
        KeymastersKeepLocations.THE_SILENT_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SILENT_PASSAGE
    ),
    KeymastersKeepRegions.THE_SILENT_THRESHOLD: (
        KeymastersKeepLocations.THE_SILENT_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SILENT_THRESHOLD
    ),
    KeymastersKeepRegions.THE_SILENT_VAULT: (
        KeymastersKeepLocations.THE_SILENT_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_SILENT_VAULT
    ),
    KeymastersKeepRegions.THE_UNFATHOMABLE_DOOR: (
        KeymastersKeepLocations.THE_UNFATHOMABLE_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNFATHOMABLE_DOOR
    ),
    KeymastersKeepRegions.THE_UNKNOWN_ARCH: (
        KeymastersKeepLocations.THE_UNKNOWN_ARCH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNKNOWN_ARCH
    ),
    KeymastersKeepRegions.THE_UNKNOWN_GATEWAY: (
        KeymastersKeepLocations.THE_UNKNOWN_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNKNOWN_GATEWAY
    ),
    KeymastersKeepRegions.THE_UNMARKED_PASSAGE: (
        KeymastersKeepLocations.THE_UNMARKED_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNMARKED_PASSAGE
    ),
    KeymastersKeepRegions.THE_UNMARKED_VAULT: (
        KeymastersKeepLocations.THE_UNMARKED_VAULT_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNMARKED_VAULT
    ),
    KeymastersKeepRegions.THE_UNRAVELED_DOOR: (
        KeymastersKeepLocations.THE_UNRAVELED_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNRAVELED_DOOR
    ),
    KeymastersKeepRegions.THE_UNSEEN_ARCHWAY: (
        KeymastersKeepLocations.THE_UNSEEN_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSEEN_ARCHWAY
    ),
    KeymastersKeepRegions.THE_UNSEEN_DOOR: (
        KeymastersKeepLocations.THE_UNSEEN_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSEEN_DOOR
    ),
    KeymastersKeepRegions.THE_UNSEEN_PASSAGE: (
        KeymastersKeepLocations.THE_UNSEEN_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSEEN_PASSAGE
    ),
    KeymastersKeepRegions.THE_UNSEEN_PORTAL: (
        KeymastersKeepLocations.THE_UNSEEN_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSEEN_PORTAL
    ),
    KeymastersKeepRegions.THE_UNSPOKEN_GATE: (
        KeymastersKeepLocations.THE_UNSPOKEN_GATE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNSPOKEN_GATE
    ),
    KeymastersKeepRegions.THE_UNTOLD_GATEWAY: (
        KeymastersKeepLocations.THE_UNTOLD_GATEWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNTOLD_GATEWAY
    ),
    KeymastersKeepRegions.THE_UNTRACEABLE_PATH: (
        KeymastersKeepLocations.THE_UNTRACEABLE_PATH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_UNTRACEABLE_PATH
    ),
    KeymastersKeepRegions.THE_VANISHING_ARCHWAY: (
        KeymastersKeepLocations.THE_VANISHING_ARCHWAY_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VANISHING_ARCHWAY
    ),
    KeymastersKeepRegions.THE_VANISHING_DOOR: (
        KeymastersKeepLocations.THE_VANISHING_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VANISHING_DOOR
    ),
    KeymastersKeepRegions.THE_VAULT_OF_WHISPERS: (
        KeymastersKeepLocations.THE_VAULT_OF_WHISPERS_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VAULT_OF_WHISPERS
    ),
    KeymastersKeepRegions.THE_VEILED_PASSAGE: (
        KeymastersKeepLocations.THE_VEILED_PASSAGE_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VEILED_PASSAGE
    ),
    KeymastersKeepRegions.THE_VEILED_PATH: (
        KeymastersKeepLocations.THE_VEILED_PATH_UNLOCK, KeymastersKeepItems.UNLOCK_THE_VEILED_PATH
    ),
    KeymastersKeepRegions.THE_WHISPERED_PORTAL: (
        KeymastersKeepLocations.THE_WHISPERED_PORTAL_UNLOCK, KeymastersKeepItems.UNLOCK_THE_WHISPERED_PORTAL
    ),
    KeymastersKeepRegions.THE_WHISPERED_THRESHOLD: (
        KeymastersKeepLocations.THE_WHISPERED_THRESHOLD_UNLOCK, KeymastersKeepItems.UNLOCK_THE_WHISPERED_THRESHOLD
    ),
    KeymastersKeepRegions.THE_WHISPERING_DOOR: (
        KeymastersKeepLocations.THE_WHISPERING_DOOR_UNLOCK, KeymastersKeepItems.UNLOCK_THE_WHISPERING_DOOR
    ),
}

shop_to_shop_item_locations: Dict[KeymastersKeepShops, KeymastersKeepLocations] = {
    KeymastersKeepShops.ABYSSFORGE_CURIOS: KeymastersKeepLocations.SHOP_ABYSSFORGE_CURIOS_ITEM,
    KeymastersKeepShops.ARCANE_LANTERN_WORKSHOP: KeymastersKeepLocations.SHOP_ARCANE_LANTERN_WORKSHOP_ITEM,
    KeymastersKeepShops.ASTRAL_ECHO_ATELIER: KeymastersKeepLocations.SHOP_ASTRAL_ECHO_ATELIER_ITEM,
    KeymastersKeepShops.ASTRALGLOW_COLLECTION: KeymastersKeepLocations.SHOP_ASTRALGLOW_COLLECTION_ITEM,
    KeymastersKeepShops.ASTRALHELM_ARMORY: KeymastersKeepLocations.SHOP_ASTRALHELM_ARMORY_ITEM,
    KeymastersKeepShops.BLOODROSE_ATELIER: KeymastersKeepLocations.SHOP_BLOODROSE_ATELIER_ITEM,
    KeymastersKeepShops.CELESTIAL_CODEX_CURIOS: KeymastersKeepLocations.SHOP_CELESTIAL_CODEX_CURIOS_ITEM,
    KeymastersKeepShops.DAWNSHARD_DEPOT: KeymastersKeepLocations.SHOP_DAWNSHARD_DEPOT_ITEM,
    KeymastersKeepShops.DRAGONBONE_BAZAAR: KeymastersKeepLocations.SHOP_DRAGONBONE_BAZAAR_ITEM,
    KeymastersKeepShops.DREAMSHARD_COLLECTION: KeymastersKeepLocations.SHOP_DREAMSHARD_COLLECTION_ITEM,
    KeymastersKeepShops.DREAMLIGHT_DEPOT: KeymastersKeepLocations.SHOP_DREAMLIGHT_DEPOT_ITEM,
    KeymastersKeepShops.ECHOCHIME_PARLOR: KeymastersKeepLocations.SHOP_ECHOCHIME_PARLOR_ITEM,
    KeymastersKeepShops.ECLIPSEGEAR_EMPORIUM: KeymastersKeepLocations.SHOP_ECLIPSEGEAR_EMPORIUM_ITEM,
    KeymastersKeepShops.EMBERHEART_FORGE_AND_FINDS: KeymastersKeepLocations.SHOP_EMBERHEART_FORGE_AND_FINDS_ITEM,
    KeymastersKeepShops.EMBERWING_EMPORIUM: KeymastersKeepLocations.SHOP_EMBERWING_EMPORIUM_ITEM,
    KeymastersKeepShops.ETHERHOLLOW_COLLECTION: KeymastersKeepLocations.SHOP_ETHERHOLLOW_COLLECTION_ITEM,
    KeymastersKeepShops.FIRESONG_FORGE: KeymastersKeepLocations.SHOP_FIRESONG_FORGE_ITEM,
    KeymastersKeepShops.FROSTLIGHT_CABINET: KeymastersKeepLocations.SHOP_FROSTLIGHT_CABINET_ITEM,
    KeymastersKeepShops.FROSTWIND_FRONTIER: KeymastersKeepLocations.SHOP_FROSTWIND_FRONTIER_ITEM,
    KeymastersKeepShops.IRONBLOOM_BAZAAR: KeymastersKeepLocations.SHOP_IRONBLOOM_BAZAAR_ITEM,
    KeymastersKeepShops.IRONSHARD_ARMORY: KeymastersKeepLocations.SHOP_IRONSHARD_ARMORY_ITEM,
    KeymastersKeepShops.LUMINSPIRE_WORKSHOP: KeymastersKeepLocations.SHOP_LUMINSPIRE_WORKSHOP_ITEM,
    KeymastersKeepShops.MOONLIT_RELIQUARY: KeymastersKeepLocations.SHOP_MOONLIT_RELIQUARY_ITEM,
    KeymastersKeepShops.MOONREIGN_PARLOR: KeymastersKeepLocations.SHOP_MOONREIGN_PARLOR_ITEM,
    KeymastersKeepShops.MOONSTONE_MARKET: KeymastersKeepLocations.SHOP_MOONSTONE_MARKET_ITEM,
    KeymastersKeepShops.MYTHRIL_MIRROR_MARKET: KeymastersKeepLocations.SHOP_MYTHRIL_MIRROR_MARKET_ITEM,
    KeymastersKeepShops.NETHERGLOW_WORKSHOP: KeymastersKeepLocations.SHOP_NETHERGLOW_WORKSHOP_ITEM,
    KeymastersKeepShops.NIGHTSPIRE_NOOK: KeymastersKeepLocations.SHOP_NIGHTSPIRE_NOOK_ITEM,
    KeymastersKeepShops.OBSIDIANFLARE_OUTPOST: KeymastersKeepLocations.SHOP_OBSIDIANFLARE_OUTPOST_ITEM,
    KeymastersKeepShops.OPALINE_RELIQUARY: KeymastersKeepLocations.SHOP_OPALINE_RELIQUARY_ITEM,
    KeymastersKeepShops.RADIANTCORE_GALLERY: KeymastersKeepLocations.SHOP_RADIANTCORE_GALLERY_ITEM,
    KeymastersKeepShops.RUNEBOUND_REPOSITORY: KeymastersKeepLocations.SHOP_RUNEBOUND_REPOSITORY_ITEM,
    KeymastersKeepShops.RUNEBROOK_EXCHANGE: KeymastersKeepLocations.SHOP_RUNEBROOK_EXCHANGE_ITEM,
    KeymastersKeepShops.RUNECROWN_BOUTIQUE: KeymastersKeepLocations.SHOP_RUNECROWN_BOUTIQUE_ITEM,
    KeymastersKeepShops.SHADEWOOD_TROVE: KeymastersKeepLocations.SHOP_SHADEWOOD_TROVE_ITEM,
    KeymastersKeepShops.SHADOWMANTLE_MARKET: KeymastersKeepLocations.SHOP_SHADOWMANTLE_MARKET_ITEM,
    KeymastersKeepShops.SHATTERSTONE_TROVE: KeymastersKeepLocations.SHOP_SHATTERSTONE_TROVE_ITEM,
    KeymastersKeepShops.SILVERDAWN_SUNDRIES: KeymastersKeepLocations.SHOP_SILVERDAWN_SUNDRIES_ITEM,
    KeymastersKeepShops.SILVERQUARTZ_EXCHANGE: KeymastersKeepLocations.SHOP_SILVERQUARTZ_EXCHANGE_ITEM,
    KeymastersKeepShops.SPIRITCHIME_BOUTIQUE: KeymastersKeepLocations.SHOP_SPIRITCHIME_BOUTIQUE_ITEM,
    KeymastersKeepShops.STARBOUND_STUDIO: KeymastersKeepLocations.SHOP_STARBOUND_STUDIO_ITEM,
    KeymastersKeepShops.STARROOT_REPOSITORY: KeymastersKeepLocations.SHOP_STARROOT_REPOSITORY_ITEM,
    KeymastersKeepShops.STARWEAVE_ARMORY: KeymastersKeepLocations.SHOP_STARWEAVE_ARMORY_ITEM,
    KeymastersKeepShops.STORMHOLLOW_GEARWORKS: KeymastersKeepLocations.SHOP_STORMHOLLOW_GEARWORKS_ITEM,
    KeymastersKeepShops.SUNFORGE_SUNDRIES: KeymastersKeepLocations.SHOP_SUNFORGE_SUNDRIES_ITEM,
    KeymastersKeepShops.THORNBLOOM_CRAFTWORKS: KeymastersKeepLocations.SHOP_THORNBLOOM_CRAFTWORKS_ITEM,
    KeymastersKeepShops.THORNVALE_WORKSHOP: KeymastersKeepLocations.SHOP_THORNVALE_WORKSHOP_ITEM,
    KeymastersKeepShops.THUNDERSHARD_TROVE: KeymastersKeepLocations.SHOP_THUNDERSHARD_TROVE_ITEM,
    KeymastersKeepShops.VINEWHISPER_VAULT: KeymastersKeepLocations.SHOP_VINEWHISPER_VAULT_ITEM,
    KeymastersKeepShops.VOIDSPIRE_VAULT: KeymastersKeepLocations.SHOP_VOIDSPIRE_VAULT_ITEM,
}

shopkeeper_greetings: Dict[KeymastersKeepShopkeepers, str] = {
    KeymastersKeepShopkeepers.AURELIA_IRONQUILL: "Step inside and sign your fate in ink forged from celestial steel",
    KeymastersKeepShopkeepers.AURETH_THE_LUMINARCH: "Behold my shining wares... may they light the darkest corners of your journey",
    KeymastersKeepShopkeepers.BARIS_THE_SHADOWFORGED: "Welcome to where dusk and steel entwine... find your edge here",
    KeymastersKeepShopkeepers.BAROTH_DARKHOLLOW: "Tread softly, friend... each relic in this hollow has a story worth your coin",
    KeymastersKeepShopkeepers.CAELIA_THE_DREAMSPUN: "Enter, dream‑seeker... my curios will spin your reality anew",
    KeymastersKeepShopkeepers.CALYSTA_EMBERWISP: "Feel the flicker of possibility... kindle it with one of my ember‑touched trinkets",
    KeymastersKeepShopkeepers.CASSIA_THE_LUNEHARROW: "By moonlight and magic... peruse my wares and discover your hidden power",
    KeymastersKeepShopkeepers.DAMIEL_THE_VEILBREAKER: "Shatter the unseen barriers... my artifacts will pierce the veil for you",
    KeymastersKeepShopkeepers.DURNIK_THE_COLDSTEEL: "Steel never wavers, and neither will my prices... choose your blade",
    KeymastersKeepShopkeepers.EDRIN_THE_RIFTWALKER: "Rifts are my realm... step through and claim what reality left behind",
    KeymastersKeepShopkeepers.ELOWEN_FROSTWHISPER: "Let the chill of these treasures awaken your resolve",
    KeymastersKeepShopkeepers.ERYNDOR_THE_ECHOWEAVER: "Listen close.. my wares hum with echoes of forgotten song",
    KeymastersKeepShopkeepers.FENRIC_UMBRALSTAFF: "Darkness bends to will... let me show you how",
    KeymastersKeepShopkeepers.FIANNA_THE_RUNESONG: "Hear the runes sing... choose one and make it yours",
    KeymastersKeepShopkeepers.GARRICK_THE_GAVELBEARER: "I'll preside over your bargains...make your offer!",
    KeymastersKeepShopkeepers.GARRON_THE_BONECARVER: "Bone and bone alike... everything here shares the same skeleton of truth",
    KeymastersKeepShopkeepers.HALDOR_THE_SHROUDMAKER: "Wrap yourself in secrets... each cloak here hides a story",
    KeymastersKeepShopkeepers.HORIAN_THE_ASHGROVE: "“From ash springs new life... discover rebirth among my curios",
    KeymastersKeepShopkeepers.ILLYRA_THE_WHISPERING: "Lean in close... these whispers have secrets you can't resist",
    KeymastersKeepShopkeepers.ISOLDE_THE_MOONREIGN: "Under my reign, the moon crowns your path... select your guiding star",
    KeymastersKeepShopkeepers.KARZAK_SKULLGRIP: "Grip your courage tightly... only the brave seek my wares",
    KeymastersKeepShopkeepers.KORRIN_THE_RELICMASTER: "Masterfully curated relics await... choose yours with care",
    KeymastersKeepShopkeepers.LUNARA_THE_GHOSTBLOOM: "My blooms fade at dawn... choose before they vanish",
    KeymastersKeepShopkeepers.LYSARA_THE_GLOOMCHANT: "Let my verse guide you... each chant here is yours to claim",
    KeymastersKeepShopkeepers.MARISOL_THE_EMBERSTITCH: "I stitch ember into cloth... take warmth that lasts beyond the flame",
    KeymastersKeepShopkeepers.MARREK_THE_SOULBINDER: "Souls long for anchors... let me tether yours to a relic of true power",
    KeymastersKeepShopkeepers.MELISANDE_THE_VESPERWIND: "Ride the evening breeze... my wares carry the scent of dusk",
    KeymastersKeepShopkeepers.MILARA_SHADOWGROVE: "Enter the grove of shadows... there's a piece of night here for you",
    KeymastersKeepShopkeepers.NERYSSA_MOONSHARD: "Shattered moonlight forges strength... select your shard",
    KeymastersKeepShopkeepers.NORGIM_THE_BONEFORGED: "Forged in bone and iron... my tools outlast flesh and time",
    KeymastersKeepShopkeepers.ORIAX_THE_VEILBRINGER: "I bring the unseen into view... take a glimpse",
    KeymastersKeepShopkeepers.ORIELLE_THE_STARFLAME: "Starlight captured in flame... ignite your potential",
    KeymastersKeepShopkeepers.ORLOK_THE_CHAINBREAKER: "Shatter every shackle... my collection is your path to unbridled power",
    KeymastersKeepShopkeepers.RHOGAR_THE_STORMCALL: "Heed the thunder... each of my wares crackles with power",
    KeymastersKeepShopkeepers.RIVEN_ASHENVAULT: "From smoldering ruins arise forgotten treasures... dare you claim one?",
    KeymastersKeepShopkeepers.RODERICK_THE_DAWNSEEKER: "Welcome dawn's first light... these relics shine on new beginnings",
    KeymastersKeepShopkeepers.SELENE_SILVERVEIL: "Silvery whispers drift through these aisles... listen, and choose the one that calls",
    KeymastersKeepShopkeepers.SELWYN_THE_MISTFORGED: "Forged in drifting mist... these artifacts blur the line between worlds",
    KeymastersKeepShopkeepers.SEREN_THE_DREAMSHAPER: "Shape your destiny... one dreamwoven relic at a time",
    KeymastersKeepShopkeepers.SYLRIUS_NIGHTBLOOM: "Night's petals only open here... take one before the sun rises",
    KeymastersKeepShopkeepers.TALGOR_FROSTGRAVE: "Cold never forgets... feel the bite of these relics and carry their legacy",
    KeymastersKeepShopkeepers.THALIA_THE_TIDEWEAVER: "Ride the moon's tide... my curios ebb and flow with magic",
    KeymastersKeepShopkeepers.TORRIK_EMBERFALL: "When embers fall, new power rises... gather yours here",
    KeymastersKeepShopkeepers.VALEENA_THE_FROSTCHIME: "Chimes of ice ring true... listen, then select",
    KeymastersKeepShopkeepers.VARKUL_DEEPGAZE: "Within these relics slumbers the power of sunken worlds... dare you look?",
    KeymastersKeepShopkeepers.VENTOR_THE_SHARDBINDER: "I bind shattered magic into whole... take what you need",
    KeymastersKeepShopkeepers.VOREN_GALESONG: "Hear the wind's melody... each trinket sings a different tune",
    KeymastersKeepShopkeepers.YSOLDE_THE_VEILBOUND: "Bound by veils of secrecy... lift one, and discover what lies concealed",
    KeymastersKeepShopkeepers.ZAREK_THE_IRONREND: "Rend iron and fate alike... my blades await your grip",
    KeymastersKeepShopkeepers.ZEPHYRION_DUSKWEAVER: "Weave yourself into dusk's tapestry... find the relic to thread",
}
