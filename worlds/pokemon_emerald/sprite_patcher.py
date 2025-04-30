import os
import zlib

from pygbagfx import _gbagfx # from package
from PIL import Image
from .data import data

POKEMON_NAME_TO_ID = { "Bulbasaur": 1, "Ivysaur": 2, "Venusaur": 3, "Charmander": 4, "Charmeleon": 5, "Charizard": 6, "Squirtle": 7, "Wartortle": 8, "Blastoise": 9, "Caterpie": 10, "Metapod": 11, "Butterfree": 12, "Weedle": 13, "Kakuna": 14, "Beedrill": 15, "Pidgey": 16, "Pidgeotto": 17, "Pidgeot": 18, "Rattata": 19, "Raticate": 20, "Spearow": 21, "Fearow": 22, "Ekans": 23, "Arbok": 24, "Pikachu": 25, "Raichu": 26, "Sandshrew": 27, "Sandslash": 28, "Nidoran Female": 29, "Nidorina": 30, "Nidoqueen": 31, "Nidoran Male": 32, "Nidorino": 33, "Nidoking": 34, "Clefairy": 35, "Clefable": 36, "Vulpix": 37, "Ninetales": 38, "Jigglypuff": 39, "Wigglytuff": 40, "Zubat": 41, "Golbat": 42, "Oddish": 43, "Gloom": 44, "Vileplume": 45, "Paras": 46, "Parasect": 47, "Venonat": 48, "Venomoth": 49, "Diglett": 50, "Dugtrio": 51, "Meowth": 52, "Persian": 53, "Psyduck": 54, "Golduck": 55, "Mankey": 56, "Primeape": 57, "Growlithe": 58, "Arcanine": 59, "Poliwag": 60, "Poliwhirl": 61, "Poliwrath": 62, "Abra": 63, "Kadabra": 64, "Alakazam": 65, "Machop": 66, "Machoke": 67, "Machamp": 68, "Bellsprout": 69, "Weepinbell": 70, "Victreebel": 71, "Tentacool": 72, "Tentacruel": 73, "Geodude": 74, "Graveler": 75, "Golem": 76, "Ponyta": 77, "Rapidash": 78, "Slowpoke": 79, "Slowbro": 80, "Magnemite": 81, "Magneton": 82, "Farfetch'd": 83, "Doduo": 84, "Dodrio": 85, "Seel": 86, "Dewgong": 87, "Grimer": 88, "Muk": 89, "Shellder": 90, "Cloyster": 91, "Gastly": 92, "Haunter": 93, "Gengar": 94, "Onix": 95, "Drowzee": 96, "Hypno": 97, "Krabby": 98, "Kingler": 99, "Voltorb": 100, "Electrode": 101, "Exeggcute": 102, "Exeggutor": 103, "Cubone": 104, "Marowak": 105, "Hitmonlee": 106, "Hitmonchan": 107, "Lickitung": 108, "Koffing": 109, "Weezing": 110, "Rhyhorn": 111, "Rhydon": 112, "Chansey": 113, "Tangela": 114, "Kangaskhan": 115, "Horsea": 116, "Seadra": 117, "Goldeen": 118, "Seaking": 119, "Staryu": 120, "Starmie": 121, "Mr. Mime": 122, "Scyther": 123, "Jynx": 124, "Electabuzz": 125, "Magmar": 126, "Pinsir": 127, "Tauros": 128, "Magikarp": 129, "Gyarados": 130, "Lapras": 131, "Ditto": 132, "Eevee": 133, "Vaporeon": 134, "Jolteon": 135, "Flareon": 136, "Porygon": 137, "Omanyte": 138, "Omastar": 139, "Kabuto": 140, "Kabutops": 141, "Aerodactyl": 142, "Snorlax": 143, "Articuno": 144, "Zapdos": 145, "Moltres": 146, "Dratini": 147, "Dragonair": 148, "Dragonite": 149, "Mewtwo": 150, "Mew": 151, "Chikorita": 152, "Bayleef": 153, "Meganium": 154, "Cyndaquil": 155, "Quilava": 156, "Typhlosion": 157, "Totodile": 158, "Croconaw": 159, "Feraligatr": 160, "Sentret": 161, "Furret": 162, "Hoothoot": 163, "Noctowl": 164, "Ledyba": 165, "Ledian": 166, "Spinarak": 167, "Ariados": 168, "Crobat": 169, "Chinchou": 170, "Lanturn": 171, "Pichu": 172, "Cleffa": 173, "Igglybuff": 174, "Togepi": 175, "Togetic": 176, "Natu": 177, "Xatu": 178, "Mareep": 179, "Flaaffy": 180, "Ampharos": 181, "Bellossom": 182, "Marill": 183, "Azumarill": 184, "Sudowoodo": 185, "Politoed": 186, "Hoppip": 187, "Skiploom": 188, "Jumpluff": 189, "Aipom": 190, "Sunkern": 191, "Sunflora": 192, "Yanma": 193, "Wooper": 194, "Quagsire": 195, "Espeon": 196, "Umbreon": 197, "Murkrow": 198, "Slowking": 199, "Misdreavus": 200, "Unown": 201, "Wobbuffet": 202, "Girafarig": 203, "Pineco": 204, "Forretress": 205, "Dunsparce": 206, "Gligar": 207, "Steelix": 208, "Snubbull": 209, "Granbull": 210, "Qwilfish": 211, "Scizor": 212, "Shuckle": 213, "Heracross": 214, "Sneasel": 215, "Teddiursa": 216, "Ursaring": 217, "Slugma": 218, "Magcargo": 219, "Swinub": 220, "Piloswine": 221, "Corsola": 222, "Remoraid": 223, "Octillery": 224, "Delibird": 225, "Mantine": 226, "Skarmory": 227, "Houndour": 228, "Houndoom": 229, "Kingdra": 230, "Phanpy": 231, "Donphan": 232, "Porygon2": 233, "Stantler": 234, "Smeargle": 235, "Tyrogue": 236, "Hitmontop": 237, "Smoochum": 238, "Elekid": 239, "Magby": 240, "Miltank": 241, "Blissey": 242, "Raikou": 243, "Entei": 244, "Suicune": 245, "Larvitar": 246, "Pupitar": 247, "Tyranitar": 248, "Lugia": 249, "Ho-oh": 250, "Celebi": 251, "Treecko": 252, "Grovyle": 253, "Sceptile": 254, "Torchic": 255, "Combusken": 256, "Blaziken": 257, "Mudkip": 258, "Marshtomp": 259, "Swampert": 260, "Poochyena": 261, "Mightyena": 262, "Zigzagoon": 263, "Linoone": 264, "Wurmple": 265, "Silcoon": 266, "Beautifly": 267, "Cascoon": 268, "Dustox": 269, "Lotad": 270, "Lombre": 271, "Ludicolo": 272, "Seedot": 273, "Nuzleaf": 274, "Shiftry": 275, "Taillow": 276, "Swellow": 277, "Wingull": 278, "Pelipper": 279, "Ralts": 280, "Kirlia": 281, "Gardevoir": 282, "Surskit": 283, "Masquerain": 284, "Shroomish": 285, "Breloom": 286, "Slakoth": 287, "Vigoroth": 288, "Slaking": 289, "Nincada": 290, "Ninjask": 291, "Shedinja": 292, "Whismur": 293, "Loudred": 294, "Exploud": 295, "Makuhita": 296, "Hariyama": 297, "Azurill": 298, "Nosepass": 299, "Skitty": 300, "Delcatty": 301, "Sableye": 302, "Mawile": 303, "Aron": 304, "Lairon": 305, "Aggron": 306, "Meditite": 307, "Medicham": 308, "Electrike": 309, "Manectric": 310, "Plusle": 311, "Minun": 312, "Volbeat": 313, "Illumise": 314, "Roselia": 315, "Gulpin": 316, "Swalot": 317, "Carvanha": 318, "Sharpedo": 319, "Wailmer": 320, "Wailord": 321, "Numel": 322, "Camerupt": 323, "Torkoal": 324, "Spoink": 325, "Grumpig": 326, "Spinda": 327, "Trapinch": 328, "Vibrava": 329, "Flygon": 330, "Cacnea": 331, "Cacturne": 332, "Swablu": 333, "Altaria": 334, "Zangoose": 335, "Seviper": 336, "Lunatone": 337, "Solrock": 338, "Barboach": 339, "Whiscash": 340, "Corphish": 341, "Crawdaunt": 342, "Baltoy": 343, "Claydol": 344, "Lileep": 345, "Cradily": 346, "Anorith": 347, "Armaldo": 348, "Feebas": 349, "Milotic": 350, "Castform": 351, "Kecleon": 352, "Shuppet": 353, "Banette": 354, "Duskull": 355, "Dusclops": 356, "Tropius": 357, "Chimecho": 358, "Absol": 359, "Wynaut": 360, "Snorunt": 361, "Glalie": 362, "Spheal": 363, "Sealeo": 364, "Walrein": 365, "Clamperl": 366, "Huntail": 367, "Gorebyss": 368, "Relicanth": 369, "Luvdisc": 370, "Bagon": 371, "Shelgon": 372, "Salamence": 373, "Beldum": 374, "Metang": 375, "Metagross": 376, "Regirock": 377, "Regice": 378, "Registeel": 379, "Latias": 380, "Latios": 381, "Kyogre": 382, "Groudon": 383, "Rayquaza": 384, "Jirachi": 385, "Deoxys": 386 }
POKEMON_ID_TO_INTERNAL_ID = { 252: 277, 253: 278, 254: 279, 255: 280, 256: 281, 257: 282, 258: 283, 259: 284, 260: 285, 261: 286, 262: 287, 263: 288, 264: 289, 265: 290, 266: 291, 267: 292, 268: 293, 269: 294, 270: 295, 271: 296, 272: 297, 273: 298, 274: 299, 275: 300, 276: 304, 277: 305, 278: 309, 279: 310, 280: 392, 281: 393, 282: 394, 283: 311, 284: 312, 285: 306, 286: 307, 287: 364, 288: 365, 289: 366, 290: 301, 291: 302, 292: 303, 293: 370, 294: 371, 295: 372, 296: 335, 297: 336, 298: 350, 299: 320, 300: 315, 301: 316, 302: 322, 303: 355, 304: 382, 305: 383, 306: 384, 307: 356, 308: 357, 309: 337, 310: 338, 311: 353, 312: 354, 313: 386, 314: 387, 315: 363, 316: 367, 317: 368, 318: 330, 319: 331, 320: 313, 321: 314, 322: 339, 323: 340, 324: 321, 325: 351, 326: 352, 327: 308, 328: 332, 329: 333, 330: 334, 331: 344, 332: 345, 333: 358, 334: 359, 335: 380, 336: 379, 337: 348, 338: 349, 339: 323, 340: 324, 341: 326, 342: 327, 343: 318, 344: 319, 345: 388, 346: 389, 347: 390, 348: 391, 349: 328, 350: 329, 351: 385, 352: 317, 353: 377, 354: 378, 355: 361, 356: 362, 357: 369, 358: 411, 359: 376, 360: 360, 361: 346, 362: 347, 363: 341, 364: 342, 365: 343, 366: 373, 367: 375, 368: 376, 369: 381, 370: 325, 371: 395, 372: 396, 373: 397, 374: 398, 375: 399, 376: 400, 377: 401, 378: 402, 379: 403, 380: 407, 381: 408, 382: 404, 383: 405, 384: 406, 385: 409, 386: 410 }

POKEMON_FOLDERS = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran Female", "Nidorina", "Nidoqueen", "Nidoran Male", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys"]
POKEMON_SPRITES = ["front_anim", "back", "icon", "footprint"]
POKEMON_MAIN_PALETTE_EXTRACTION_PRIORITY = ["front_anim", "back"]
POKEMON_SHINY_PALETTE_EXTRACTION_PRIORITY = ["sfront_anim", "sback"]
POKEMON_PALETTES = {
    "palette": POKEMON_MAIN_PALETTE_EXTRACTION_PRIORITY,
    "palette_shiny": POKEMON_SHINY_PALETTE_EXTRACTION_PRIORITY
}

TRAINER_FOLDERS = ["Brendan", "May"]
TRAINER_SPRITES = ["walking_running", "acro_bike", "mach_bike", "surfing", "field_move", "underwater", "fishing", "watering", "decorating", "battle_front", "battle_back"]
TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY = ["walking_running", "acro_bike", "mach_bike", "surfing", "fishing", "watering", "decorating"]
TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY = ["reflection"]
TRAINER_UNDERWATER_PALETTE_EXTRACTION_PRIORITY = ["underwater"]
TRAINER_BATTLE_BACK_PALETTE_EXTRACTION_PRIORITY = ["battle_back"]
TRAINER_BATTLE_FRONT_PALETTE_EXTRACTION_PRIORITY = ["battle_front"]
TRAINER_PALETTES = {
    "palette": TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY,
    "palette_reflection": TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY,
    "palette_underwater": TRAINER_UNDERWATER_PALETTE_EXTRACTION_PRIORITY,
    "palette_battle_back": TRAINER_BATTLE_BACK_PALETTE_EXTRACTION_PRIORITY,
    "palette_battle_front": TRAINER_BATTLE_FRONT_PALETTE_EXTRACTION_PRIORITY
}

OBJECT_NEEDS_COMPRESSION = {
    "pokemon_front_anim":           True,
    "pokemon_back":                 True,
    "trainer_battle_front":         True,
    "pokemon_palette":              True,
    "pokemon_palette_shiny":        True,
    "trainer_palette_battle_back":  True,
    "trainer_palette_battle_front": True,
}

INTERNAL_ID_TO_SPRITE_ADDRESS = {
    "pokemon_front_anim":    lambda a : data_addresses["gMonFrontPicTable"]      + 8 * a,
    "pokemon_back":          lambda a : data_addresses["gMonBackPicTable"]       + 8 * a,
    "pokemon_icon":          lambda a : data_addresses["gMonIconTable"]          + 4 * a,
    "pokemon_icon_index":    lambda a : data_addresses["gMonIconPaletteIndices"] + a,
    "pokemon_footprint":     lambda a : data_addresses["gMonFootprintTable"]     + 4 * a,
    "pokemon_palette":       lambda a : data_addresses["gMonPaletteTable"]       + 8 * a,
    "pokemon_palette_shiny": lambda a : data_addresses["gMonShinyPaletteTable"]  + 8 * a,

    "brendan_walking_running":      lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 400,
    "brendan_mach_bike":            lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 404,
    "brendan_acro_bike":            lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 408,
    "brendan_surfing":              lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 412,
    "brendan_field_move":           lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 416,
    "brendan_underwater":           lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 444,
    "brendan_fishing":              lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 548,
    "brendan_watering":             lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 764,
    "brendan_decorating":           lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 772,
    "brendan_battle_front":         lambda : data_addresses["gTrainerFrontPicTable"] + 568,
    "brendan_battle_back":          lambda : data_addresses["gTrainerBackPicTable"],
    "brendan_battle_back_2":        lambda : data_addresses["sTrainerBackSpriteTemplates"],
    "brendan_palette":              lambda : data_addresses["sObjectEventSpritePalettes"] + 64,
    "brendan_palette_reflection":   lambda : data_addresses["sObjectEventSpritePalettes"] + 72,
    "brendan_palette_underwater":   lambda : data_addresses["sObjectEventSpritePalettes"] + 88,
    "brendan_palette_battle_back":  lambda : data_addresses["gTrainerBackPicPaletteTable"],
    "brendan_palette_battle_front": lambda : data_addresses["gTrainerFrontPicPaletteTable"] + 568,

    "may_walking_running":      lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 420,
    "may_mach_bike":            lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 424,
    "may_acro_bike":            lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 428,
    "may_surfing":              lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 432,
    "may_field_move":           lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 436,
    "may_underwater":           lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 448,
    "may_fishing":              lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 552,
    "may_watering":             lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 768,
    "may_decorating":           lambda : data_addresses["gObjectEventGraphicsInfoPointers"] + 776,
    "may_battle_front":         lambda : data_addresses["gTrainerFrontPicTable"] + 576,
    "may_battle_back":          lambda : data_addresses["gTrainerBackPicTable"] + 8,
    "may_battle_back_2":        lambda : data_addresses["sTrainerBackSpriteTemplates"] + 24,
    "may_palette":              lambda : data_addresses["sObjectEventSpritePalettes"] + 136,
    "may_palette_reflection":   lambda : data_addresses["sObjectEventSpritePalettes"] + 144,
    "may_palette_underwater":   lambda : data_addresses["sObjectEventSpritePalettes"] + 88,
    "may_palette_battle_back":  lambda : data_addresses["gTrainerBackPicPaletteTable"] + 8,
    "may_palette_battle_front": lambda : data_addresses["gTrainerFrontPicPaletteTable"] + 576,
}

COMPLEX_SPRITES_LIST = [ "trainer_walking_running", "trainer_mach_bike", "trainer_acro_bike", "trainer_surfing", "trainer_field_move", "trainer_underwater", "trainer_fishing", "trainer_watering", "trainer_decorating", "trainer_battle_back_2" ]

OVERWORLD_SPRITE_OBJECT_INFO = {
    "starter_bytes":  { "shift": 0,  "size": 2 },
    "palette_id":     { "shift": 2,  "size": 2 },
    "second_pal_id":  { "shift": 4,  "size": 2 },
    "sprite_length":  { "shift": 6,  "size": 2 },
    "sprite_width":   { "shift": 8,  "size": 2 },
    "sprite_height":  { "shift": 10, "size": 2 },
    "extra_info":     { "shift": 12, "size": 1 },
    "footprint_type": { "shift": 13, "size": 1 },
    "distrib_ptr":    { "shift": 16, "size": 3 },
    "size_draw_ptr":  { "shift": 20, "size": 3 },
    "animation_ptr":  { "shift": 24, "size": 3 },
    "sprites_ptr":    { "shift": 28, "size": 3 },
    "ram_store_ptr":  { "shift": 32, "size": 3 },
}

DATA_ADDRESSES_MOCK_AP = {
    "gMonFrontPicTable": 0x30ead4,
    "gMonBackPicTable": 0x307200,
    "gMonIconTable": 0x583bec,
    "gMonFootprintTable": 0x5762d4,
    "gMonPaletteTable": 0x307fc0,
    "gMonShinyPaletteTable": 0x308d80,
    "gMonIconPaletteIndices": 0x5842cc,
    "gObjectEventGraphicsInfoPointers": 0x50cb50,
    "sObjectEventSpritePalettes": 0x5130f8,
    "gTrainerFrontPicTable": 0x309f9c,
    "gTrainerFrontPicPaletteTable": 0x30a284,
    "gTrainerBackPicTable": 0x30a694,
    "gTrainerBackPicPaletteTable": 0x30a6d4,
    "sTrainerBackSpriteTemplates": 0x32ed60,
    "sOamTables_16x16": 0x510a7c,
    "sOamTables_16x32": 0x510ad0,
    "sOamTables_32x32": 0x510b24,
    "sEmpty6": 0xe3cf51
}
DATA_ADDRESSES_ORIGINAL = {
    "gMonFrontPicTable": 0x30a18c,
    "gMonBackPicTable": 0x3028b8,
    "gMonIconTable": 0x57bca8,
    "gMonFootprintTable": 0x56e694,
    "gMonPaletteTable": 0x303678,
    "gMonShinyPaletteTable": 0x304438,
    "gMonIconPaletteIndices": 0x57c388,
    "gObjectEventGraphicsInfoPointers": 0x505620,
    "sObjectEventSpritePalettes": 0x50bbc8,
    "gTrainerFrontPicTable": 0x305654,
    "gTrainerFrontPicPaletteTable": 0x30593c,
    "gTrainerBackPicTable": 0x305d4c,
    "gTrainerBackPicPaletteTable": 0x305d8c,
    "sTrainerBackSpriteTemplates": 0x329df8,
    "sOamTables_16x16": 0x50954c,
    "sOamTables_16x32": 0x5095a0,
    "sOamTables_32x32": 0x5095f4,
    "sEmpty6": 0xe3cf31
}

# TODO: Replace DATA_ADDRESSES_MOCK_AP with data.rom_addresses
data_addresses = DATA_ADDRESSES_MOCK_AP

ORIGINAL_ROM_CRC32 = 0x1F1C08FB

address_label_to_resource_path_list = { }
files_to_clean_up = []
sprite_pack_data = { }
resource_address_to_insert_to = 0x00
current_rom = None


####################
## Main Functions ##
####################

def handle_sprite_pack(_sprite_pack_path, _rom):
    global data_addresses
    if zlib.crc32(_rom) == ORIGINAL_ROM_CRC32:
        print("Original Emerald ROM detected! Loading its address dictionary...")
        data_addresses = DATA_ADDRESSES_ORIGINAL

    global sprite_pack_data, resource_address_to_insert_to
    # Build patch data, fetch end of file
    sprite_pack_data = { "length": 16777216, "data": [] }
    resource_address_to_insert_to = ((data_addresses["sEmpty6"] >> 12) + 1) << 12 # Should be E3D000

    global current_rom
    current_rom = _rom
    # Handle existing Trainer & Pokemon folders
    handle_folder(_sprite_pack_path, TRAINER_FOLDERS, TRAINER_SPRITES, TRAINER_PALETTES, False)
    handle_folder(_sprite_pack_path, POKEMON_FOLDERS, POKEMON_SPRITES, POKEMON_PALETTES, True)

    # Remove temporary files
    clean_up()
    return sprite_pack_data

def clean_up():
    # Remove all temporary files after processing
    for file in files_to_clean_up:
        if os.path.isfile(file):
            os.remove(file)
    files_to_clean_up.clear()


#########################
## Patch Data Building ##
#########################

def handle_folder(_sprite_pack_path, _folders_list, _sprites_list, _palettes_list, _is_pokemon):
    for object_name in _folders_list:
        object_folder_path = os.path.join(_sprite_pack_path, object_name)
        if not os.path.exists(object_folder_path):
            continue
        found_sprites = { }
        for sprite_name in os.listdir(object_folder_path):
            if not sprite_name.endswith('.png'):
                continue
            # Only handle sprites with a matching name
            matching_sprite_name = next(filter(lambda f: sprite_name.startswith(f), _sprites_list), None)
            if not matching_sprite_name:
                continue
            sprite_data_chunks = sprite_name[:-4].split('-')
            extra_sprite_data = sprite_data_chunks[1:] if len(sprite_data_chunks) > 1 else None
            sprite_path = os.path.join(object_folder_path, sprite_name)
            if os.path.exists(sprite_path):
                if found_sprites.get(matching_sprite_name):
                    continue
                found_sprites[matching_sprite_name] = sprite_name
                add_sprite(_is_pokemon, object_name, matching_sprite_name, extra_sprite_data, sprite_path)
        for palette, palette_extraction_priority_queue in _palettes_list.items():
            # Generate palettes if sprites exist
            found_sprite = False
            for sprite_name in palette_extraction_priority_queue:
                if sprite_name in found_sprites:
                    sprite_path = os.path.join(object_folder_path, found_sprites.get(sprite_name))
                    found_sprite = True
                    add_palette(_is_pokemon, object_name, palette, sprite_path)
                    break
            if not found_sprite:
                # Try to find raw sprites if they have not been recorded yet
                for sprite_name in palette_extraction_priority_queue:
                    sprite_path = os.path.join(object_folder_path, sprite_name + '.png')
                    if os.path.exists(sprite_path):
                        add_palette(_is_pokemon, object_name, palette, sprite_path)
                        break

def add_sprite(_is_pokemon, _object_name, _sprite_name, _extra_data, _path):
    is_palette_indexed_icon = False
    palette_index = 0
    if _sprite_name == 'icon' and _extra_data:
        # Palette indexed icon: Store palette index from file name
        is_palette_indexed_icon = True
        palette_index = int(_extra_data[0])
        _sprite_name = "icon"
    sprite_key = ("pokemon_" if _is_pokemon else "trainer_") + _sprite_name

    global resource_address_to_insert_to
    if _is_pokemon:
        # Fetch internal Pokemon ID & sprite address
        pokemon_id = POKEMON_NAME_TO_ID[_object_name]
        pokemon_internal_id = POKEMON_ID_TO_INTERNAL_ID.get(pokemon_id, pokemon_id)
        data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[sprite_key](pokemon_internal_id)
        if is_palette_indexed_icon:
            # Special case: Palette indexed icons, since icons have 3 palettes
            icon_index_address = INTERNAL_ID_TO_SPRITE_ADDRESS[sprite_key + "_index"](pokemon_internal_id)
            add_data_to_patch({ "address": icon_index_address, "length": 1, "data": palette_index.to_bytes(1, 'little')})
    else:
        # Fetch named Trainer sprite address
        named_key = _object_name.lower() + "_" + _sprite_name
        data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[named_key]()

    if is_complex_sprite(sprite_key):
        # Special case: Some Trainer sprites point to info struct, not sprite itself
        sprite_size_data = None
        if sprite_key == "trainer_battle_back_2":
            # Special case: Trainer Back sprites need further pointer seeking
            info_object_address = data_address
            data_address = int.from_bytes(bytes(current_rom[data_address + 12:data_address + 15]), 'little')
        elif is_overworld_sprite(sprite_key):
            # Special case: Trainer Overworld sprites need two objects to delve into
            info_object_address = int.from_bytes(bytes(current_rom[data_address:data_address + 3]), 'little')
            data_address = get_overworld_sprite_data(info_object_address, 'sprites_ptr')
            if _extra_data:
                # If size given, extract it and check if it is supported
                sprite_size_data = handle_overworld_custom_size(_extra_data)
        replace_complex_sprite(data_address, sprite_key, info_object_address, sprite_size_data)

    if sprite_key != "trainer_battle_back":
        add_resource(False, sprite_key, _sprite_name, data_address, _path)
    else:
        # Special case: In case of Trainer Battle back sprite, rerun this function for the ball throwing animation
        address_bytes = resource_address_to_insert_to.to_bytes(3, 'little')
        add_data_to_patch({ "address": data_address, "length": 3, "data": address_bytes })
        add_sprite(_is_pokemon, _object_name, _sprite_name + "_2", _extra_data, _path)

def add_palette(_is_pokemon, _object_name, _palette_name, _path):
    palette_key = ("pokemon" if _is_pokemon else "trainer") + "_" + _palette_name
    data_address = 0x00
    if _is_pokemon:
        # Pokemon: Grab palette pointer address from corresponding palette table
        pokemon_id = POKEMON_NAME_TO_ID[_object_name]
        pokemon_internal_id = POKEMON_ID_TO_INTERNAL_ID.get(pokemon_id, pokemon_id)
        palette_key = "pokemon_" + _palette_name
        data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[palette_key](pokemon_internal_id)
    else:
        # Trainer: Fetch from trainer battle palette table
        named_key = _object_name.lower() + "_" + _palette_name
        data_address_func = INTERNAL_ID_TO_SPRITE_ADDRESS.get(named_key)
        if not data_address_func:
            raise Exception('Could not find trainer sprite with key {}.'.format(named_key))
        data_address = data_address_func()

    add_resource(True, palette_key, _palette_name, data_address, _path)

def add_resource(_is_palette, _key, _name, _data_address, _path):
    global resource_address_to_insert_to
    address_bytes = resource_address_to_insert_to.to_bytes(3, 'little')
    add_data_to_patch({ "address": _data_address, "length": 3, "data": address_bytes })
    
    needs_compression = OBJECT_NEEDS_COMPRESSION.get(_key, False)
    if _is_palette:
        _path = handle_sprite_to_palette(_path, _name, needs_compression)
    else:
        _path = handle_sprite_to_gba_sprite(_path, needs_compression)
    
    file = open(_path, "rb")
    file_data = file.read()

    add_data_to_patch({ "address": resource_address_to_insert_to, "length": len(file_data), "data": file_data })
    resource_address_to_insert_to = (((resource_address_to_insert_to + len(file_data)) >> 4) + 1) << 4

def add_data_to_patch(_data):
    index = 0
    # Order entries by ascending starting address
    for existing_data in sprite_pack_data["data"]:
        if existing_data["address"] < _data["address"]:
            index = index + 1
        elif existing_data["address"] == _data["address"]:
            # Do not duplicate values
            return
        else:
            break
    sprite_pack_data["data"].insert(index, _data)

def call_gbagfx(_input, _output, _delete_input = False):
    # Calls sprite processing C app
    _gbagfx.main(_input, _output)
    if _delete_input:
        os.remove(_input)

#############################
## Complex Sprite Handling ##
#############################

def replace_complex_sprite(_sprite_list_address, _sprite_key, _info_object_address, _size_data = None):
    # TODO: Handle having to replace SEVERAL complex sprites for duplicate overworld objects (ex: duplicate player sprites)
    # Replaces complex sprite's sprite data and update sprite fields if needed
    sprite_data = SPRITES_REQUIREMENTS.get(_sprite_key)
    temp_address = resource_address_to_insert_to
    if not sprite_data:
        raise Exception('Could not find sprite data for the sprite with key {}.'.format(_sprite_key))

    sprite_width = _size_data.get('width') if _size_data else sprite_data.get('width', 0)
    sprite_height = _size_data.get('height') if _size_data else sprite_data.get('height', 0)
    sprite_palette_size = sprite_data.get('palette_size', 16)
    sprite_bytes_per_pixel, _ = get_pixel_size_and_extension_from_palette_size(sprite_palette_size)
    if is_overworld_sprite(_sprite_key) and not _size_data:
        sprite_width = get_overworld_sprite_data(_info_object_address, 'sprite_width')
        sprite_height = get_overworld_sprite_data(_info_object_address, 'sprite_height')
    sprite_size = round(sprite_bytes_per_pixel * sprite_width * sprite_height)
    if not sprite_width or not sprite_height:
        raise Exception('Sprite dimensions not ({}, {}) for key {}.'.format(sprite_width, sprite_height, _sprite_key))
    
    output_data = bytearray(0)
    for i in range(0, sprite_data.get('frames')):
        output_data.extend(temp_address.to_bytes(3, 'little'))
        output_data.extend(b'\x08')
        output_data.extend(sprite_size.to_bytes(2, 'little'))
        output_data.extend(b'\x00\x00')
        temp_address += sprite_size
    add_data_to_patch({"address": _sprite_list_address, "length": len(output_data), "data": bytes(output_data)})
    
    if is_overworld_sprite(_sprite_key) and _size_data:
        # If custom size given, update overworld sprite data 
        set_overworld_sprite_data(_info_object_address, 'sprite_length', sprite_size)
        set_overworld_sprite_data(_info_object_address, 'sprite_width', sprite_width)
        set_overworld_sprite_data(_info_object_address, 'sprite_height', sprite_height)
        set_overworld_sprite_data(_info_object_address, 'size_draw_ptr', data_addresses[_size_data.get('data')])

def extract_complex_sprite(_data_address, _sprite_key):
    # Extracts complex sprite graphics
    overworld_struct_address = int.from_bytes(bytes(current_rom[_data_address:_data_address + 3]), 'little')
    start_sprite_address = get_overworld_sprite_data(overworld_struct_address, 'sprites_ptr')
    sprite_data = SPRITES_REQUIREMENTS.get(_sprite_key)
    sprite_size = 0
    if not sprite_data:
        return
    for i in range(sprite_data["frames"]):
        size_address = _data_address + i * 8 + 4
        sprite_size = sprite_size + int.from_bytes(bytes(current_rom[size_address:size_address+1]), 'little')
    extract_sprite(start_sprite_address, _sprite_key, sprite_size)


#####################
## Data Extraction ##
#####################

def extract_palette(_path):
    # Extracts a palette from an existing sprite
    sprite_image = Image.open(_path)
    sprite_palette = sprite_image.getpalette() or []
    sprite_palette_colors = []
    for i in range(round(len(sprite_palette) / 3)):
        index = i * 3
        color = (int(sprite_palette[index]) << 16) + (int(sprite_palette[index+1]) << 8) + int(sprite_palette[index+2])
        sprite_palette_colors.append(hex(color)[2:].zfill(6))
    return sprite_palette_colors

def extract_sprites(_object_name, _output_path):
    # Extracts all sprites from given object from ROM into output folder
    is_pokemon = not _object_name in TRAINER_FOLDERS
    sprite_list = POKEMON_SPRITES if is_pokemon else TRAINER_SPRITES

    for sprite_name in sprite_list:
        sprite_key = ('pokemon' if is_pokemon else 'trainer') + '_' + _object_name + ('_2' if _object_name == 'battle_back' else '')
        
        if is_pokemon:
            # Fetch internal Pokemon ID & sprite address
            pokemon_id = POKEMON_NAME_TO_ID[_object_name]
            pokemon_internal_id = POKEMON_ID_TO_INTERNAL_ID.get(pokemon_id, pokemon_id)
            data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[sprite_key](pokemon_internal_id)
        else:
            # Fetch named Trainer sprite address
            named_key = _object_name.lower() + "_" + sprite_name
            data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[named_key]()

        if is_complex_sprite(sprite_key):
            sprite_data = extract_complex_sprite(data_address, sprite_key)
        else:
            sprite_data = extract_sprite(data_address, sprite_key)
        
        # Save data as gba sprite, compressed or not, then transform into actual sprite
        needs_compression = OBJECT_NEEDS_COMPRESSION.get(sprite_key, False)
        file_format = (".1bpp" if sprite_key.endswith("footprint") else ".4bpp") + ('.lz' if needs_compression else '')
        full_path_with_no_extension = os.path.join(_output_path, _object_name)
        full_path = full_path_with_no_extension + file_format
        with open(full_path, "wb") as sprite_file:
            sprite_file.write(sprite_data)
        
        handle_gba_sprite_to_sprite(full_path, needs_compression)

def extract_sprite(_data_address, _sprite_key, _preset_size = 0):
    # TODO: Find out how much data to extract & handle compression case
    # TODO: List awaited sprite size & frame amount
    # TODO: Extract awaited sprite size * frames
    # TODO: If compression, go through LZ and record the requied blocks, truncate the rest
    if _preset_size:
        sprite_size = _preset_size
    else:
        pass
    needs_compression = OBJECT_NEEDS_COMPRESSION.get(_sprite_key, False)
    print('TODO: Extract sprite with key {} at address {} from ROM.'.format(_sprite_key, _data_address))
    pass

#####################
## Data Conversion ##
#####################

def handle_sprite_to_gba_sprite(_sprite_path, _needs_compression) -> str:
    # Transforms Indexed/Grayscale PNG sprites into GBA sprites
    sprite_path_with_no_extension = str(os.path.splitext(_sprite_path)[0])
    file_format = ".1bpp" if sprite_path_with_no_extension.endswith("footprint") else ".4bpp"
    gba_sprite_path = sprite_path_with_no_extension + file_format
    call_gbagfx(_sprite_path, gba_sprite_path, False)
    if not _needs_compression:
        files_to_clean_up.append(gba_sprite_path)
        return gba_sprite_path
    else:
        # Compresses sprite if needed
        compressed_gba_sprite_path = gba_sprite_path + ".lz"
        call_gbagfx(gba_sprite_path, compressed_gba_sprite_path, True)
        files_to_clean_up.append(compressed_gba_sprite_path)
        return compressed_gba_sprite_path

def handle_gba_sprite_to_sprite(_gba_sprite_path, _needs_compression) -> str:
    # Transforms GBA sprite into indexed/grayscale PNG sprites
    _gba_sprite_path_with_no_extension = str(os.path.splitext(_gba_sprite_path)[0])
    file_format = ".1bpp" if _gba_sprite_path_with_no_extension.endswith("footprint") else ".4bpp"
    uncompressed_gba_sprite_path = _gba_sprite_path_with_no_extension + file_format
    sprite_path = _gba_sprite_path_with_no_extension + ".png"
    if _needs_compression:
        call_gbagfx(_gba_sprite_path, uncompressed_gba_sprite_path, True)
    call_gbagfx(uncompressed_gba_sprite_path, sprite_path, True)
    return sprite_path

def handle_sprite_to_palette(_sprite_path, _palette_name, _needs_compression) -> str:
    # Transforms Indexed/Grayscale PNG sprites into GBA palettes
    sprite_path_with_no_extension = str(os.path.splitext(_sprite_path)[0])
    palette_path_with_no_extension = os.path.join(os.path.dirname(sprite_path_with_no_extension), _palette_name)
    palette_path = sprite_path_with_no_extension + ".pal"
    gba_palette_path = palette_path_with_no_extension + ".gbapal"
    call_gbagfx(_sprite_path, palette_path, False)
    call_gbagfx(palette_path, gba_palette_path, True)
    if not _needs_compression:
        files_to_clean_up.append(gba_palette_path)
        return gba_palette_path
    else:
        # Compress palette if needed
        compressed_gba_palette_path = gba_palette_path + ".lz"
        call_gbagfx(gba_palette_path, compressed_gba_palette_path, True)
        files_to_clean_up.append(compressed_gba_palette_path)
        return str(compressed_gba_palette_path)

###################
## Data Checking ##
###################

VALID_OVERWORLD_SPRITE_SIZES = [
    { "width": 16, "height": 16, "data": 'sOamTables_16x16' },
    { "width": 16, "height": 32, "data": 'sOamTables_16x32' },
    { "width": 32, "height": 32, "data": 'sOamTables_32x32' },
]

VALID_ICON_PALETTES = {
    0: [ 98, 156, 131, 131, 131, 115, 189, 189, 189, 255, 255, 255, 189, 164, 65,  246, 246, 41,  213, 98,  65,  246, 148, 41,  139, 123, 255, 98,  74,  205, 238, 115, 156, 255, 180, 164, 164, 197, 255, 106, 172, 156, 98, 98, 90, 65, 65, 65 ],
    1: [ 98, 156, 131, 115, 115, 115, 189, 189, 189, 255, 255, 255, 123, 156, 74,  156, 205, 74,  148, 246, 74,  238, 115, 156, 246, 148, 246, 189, 164, 90,  246, 230, 41,  246, 246, 172, 213, 213, 106, 230, 74,  41,  98, 98, 90, 65, 65, 65 ],
    2: [ 98, 156, 131, 123, 123, 123, 189, 189, 180, 255, 255, 255, 115, 115, 205, 164, 172, 246, 180, 131, 90,  238, 197, 139, 197, 172, 41,  246, 246, 41,  246, 98,  82,  148, 123, 205, 197, 164, 205, 189, 41,  156, 98, 98, 90, 65, 65, 65 ]
}

VALID_FOOTPRINT_PALETTE = [ 0, 0, 0, 255, 255, 255 ]

VALID_OVERWORLD_UNDERWATER_PALETTE = [ 115, 197, 164, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 98, 123, 156, 74, 90, 131, 49, 65, 106, 24, 41, 82, 131, 164, 197 ]
VALID_OVERWORLD_PALETTE = [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 255, 255, 255, 0, 0, 0 ]

SPRITES_REQUIREMENTS = {
    "pokemon_front_anim":      { "frames": 2,  "width": 64, "height": 64 },
    "pokemon_back":            { "frames": 1,  "width": 64, "height": 64 },
    "pokemon_icon":            { "frames": 2,  "width": 32, "height": 32, "palette": VALID_ICON_PALETTES },
    "pokemon_footprint":       { "frames": 1,  "width": 16, "height": 16, "palette_size": 2, "palette": VALID_FOOTPRINT_PALETTE },
    "trainer_walking_running": { "frames": 18, "width": 16, "height": 32, "palette": VALID_OVERWORLD_PALETTE },
    "trainer_mach_bike":       { "frames": 9,  "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE },
    "trainer_acro_bike":       { "frames": 27, "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE },
    "trainer_surfing":         { "frames": 12, "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE },
    "trainer_field_move":      { "frames": 5,  "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE },
    "trainer_underwater":      { "frames": 9,  "width": 32, "height": 32, "palette": VALID_OVERWORLD_UNDERWATER_PALETTE },
    "trainer_fishing":         { "frames": 12, "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE },
    "trainer_watering":        { "frames": 9,  "width": 32, "height": 32, "palette": VALID_OVERWORLD_PALETTE },
    "trainer_decorating":      { "frames": 1,  "width": 16, "height": 32, "palette": VALID_OVERWORLD_PALETTE },
    "trainer_battle_back_2":   { "frames": 4,  "width": 64, "height": 64 },
    "trainer_battle_front":    { "frames": 1,  "width": 64, "height": 64 },
    "trainer_battle_back":     { "frames": 4,  "width": 64, "height": 64 }
}

def validate_sprite_pack(_sprite_pack_path, _rom):
    global current_rom
    current_rom = _rom

    errors = ""
    has_error = False
    def add_error(_error, _is_error = False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += ('\n' if errors else '') + _error
    
    add_error(*validate_folder(_sprite_pack_path, TRAINER_FOLDERS, TRAINER_SPRITES, TRAINER_PALETTES, False))
    add_error(*validate_folder(_sprite_pack_path, POKEMON_FOLDERS, POKEMON_SPRITES, POKEMON_PALETTES, True))
    return errors, has_error

def validate_folder(_sprite_pack_path, _folders_list, _sprites_list, _palettes_list, _is_pokemon):
    errors = ""
    has_error = False
    def add_error(_error, _is_error = False, _processed = False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += ('\n' if errors else '') + ('' if _processed else 'Error: ' if _is_error else 'Warning: ') + _error

    for object_name in _folders_list:
        object_folder_path = os.path.join(_sprite_pack_path, object_name)
        if not os.path.exists(object_folder_path):
            continue
        found_sprites = { }
        for sprite_name in os.listdir(object_folder_path):
            if not sprite_name.endswith('.png'):
                add_error('File {} in folder {}: Not a sprite and should be removed.'.format(sprite_name, object_name))
                continue
            # Only handle sprites with a matching name
            matching_sprite_name = next(filter(lambda f: sprite_name.startswith(f), _sprites_list), None)
            if not matching_sprite_name:
                # Allow sprites with a matching palette
                if not next(filter(lambda palette_list: sprite_name[:-4] in _palettes_list[palette_list], _palettes_list), None):
                    add_error('File {} in folder {}: Cannot be linked to a valid internal sprite or palette.'.format(sprite_name, object_name))
                    continue
                matching_sprite_name = sprite_name[:-4]
            sprite_data_chunks = sprite_name[:-4].split('-')
            extra_sprite_data = sprite_data_chunks[1:] if len(sprite_data_chunks) > 1 else None
            sprite_path = os.path.join(object_folder_path, sprite_name)
            if os.path.exists(sprite_path):
                if found_sprites.get(matching_sprite_name):
                    add_error('File {} in folder {}: Duplicate internal sprite entry with sprite {}.'.format(sprite_name, object_name, found_sprites.get(matching_sprite_name)), True)
                    continue
                found_sprites[matching_sprite_name] = sprite_name
                add_error(*validate_sprite(_is_pokemon, object_name, matching_sprite_name, extra_sprite_data, sprite_path), True)
    return errors, has_error

def validate_sprite(_is_pokemon, _object_name, _sprite_name, _extra_data, _path):
    errors = ""
    has_error = False
    def add_error(_error, _is_error = False):
        nonlocal errors, has_error
        if _error:
            has_error = has_error or _is_error
            errors += ('\n' if errors else '') + ('Error: ' if _is_error else 'Warning: ') + _error

    sprite_key = ("pokemon_" if _is_pokemon else "trainer_") + _sprite_name
    sprite_requirements = SPRITES_REQUIREMENTS.get(sprite_key, {})

    sprite_image = Image.open(_path)

    # Palette checks
    if not sprite_image.palette:
        add_error('File {} in folder {}: The sprite is not an indexed PNG file.'.format(_sprite_name, _object_name), True)
    else:
        sprite_palette_colors = sprite_image.getpalette()
        sprite_palette_model = sprite_requirements.get('palette', None)
        # TODO: Support sprites with more/less palette colors if there is no requirement
        sprite_palette_required_size = sprite_requirements.get('palette_size', 16)
        if round(len(sprite_palette_colors) / 3) != sprite_palette_required_size:
            add_error('File {} in folder {}: The sprite\'s palette has {} colors but should have {}.'.format(_sprite_name, _object_name, round(len(sprite_palette_colors) / 3), sprite_palette_required_size), True)
        elif sprite_palette_model:
            valid_palette_model = True
            if _is_pokemon and _sprite_name == 'icon':
                # Special case: icons can have several palettes
                if _extra_data:
                    # Icon palette ID is given in the icon's file name
                    palette_index = int(_extra_data[0])
                    if palette_index < 0 or palette_index > 2:
                        valid_palette_model = False
                        add_error('File {} in folder {}: Icons only have 3 palettes, but you tried using palette #{}.'.format(_sprite_name, _object_name, palette_index + 1), True)
                else:
                    # Icon palette ID must be fetched from the 
                    pokemon_id = POKEMON_NAME_TO_ID[_object_name]
                    pokemon_internal_id = POKEMON_ID_TO_INTERNAL_ID.get(pokemon_id, pokemon_id)
                    icon_index_address = INTERNAL_ID_TO_SPRITE_ADDRESS[sprite_key + "_index"](pokemon_internal_id)
                    palette_index = int.from_bytes(bytes(current_rom[icon_index_address]), 'little')
                if valid_palette_model:
                    sprite_palette_model = sprite_palette_model[palette_index]
            if valid_palette_model and not is_palette_valid(sprite_palette_colors, sprite_palette_model):
                add_error('File {} in folder {}: The sprite\'s palette does not contain the required colors.'.format(_sprite_name, _object_name), True)

    # Size checks
    sprite_valid_dimensions = []
    if not is_overworld_sprite(sprite_key) or not _extra_data:
        sprite_valid_dimensions.append({ 'width': sprite_requirements.get('width', 0), 'height': sprite_requirements.get('height', 0) * sprite_requirements.get('frames', 0) })
    else:
        allowed_sizes = ['{}x{}'.format(size['width'], size['height']) for size in VALID_OVERWORLD_SPRITE_SIZES]
        if not _extra_data[0] in allowed_sizes:
            add_error('File {} in folder {}: Invalid custom size {}. The expected sizes are: {}.'.format(_sprite_name, _object_name, _extra_data[0], allowed_sizes), True)
            sprite_valid_dimensions.append({ 'width': 0, 'height': 0 })
        else:
            sizes = _extra_data[0].split('x')
            sprite_valid_dimensions.append({ 'width': int(sizes[0]), 'height': int(sizes[1]) * sprite_requirements.get('frames', 1) })
    if sprite_valid_dimensions[0]['width'] > 0 and sprite_valid_dimensions[0]['height'] > 0:
        if not next(filter(lambda size: size['width'] == sprite_image.width and size['height'] == sprite_image.height, sprite_valid_dimensions), None):
            allowed_sizes = ['{}x{}'.format(size['width'], size['height']) for size in sprite_valid_dimensions]
            current_size = '{}x{}'.format(sprite_image.width, sprite_image.height)
            add_error('File {} in folder {}: Invalid size {}. The expected size{}: {}.'.format(_sprite_name, _object_name, current_size, ' is' if len(allowed_sizes) == 1 else 's are', allowed_sizes[0] if len(allowed_sizes) == 1 else allowed_sizes), True)
    
    return errors, has_error

def is_palette_valid(_palette, _palette_model):
    # Compares a given palette to its model and checks if it is valid or not
    for i in range(min(len(_palette), len(_palette_model))):
        if _palette_model[i] != -1 and _palette[i] != _palette_model[i]:
            return False
    return True

#######################
## Utility Functions ##
#######################

def get_pixel_size_and_extension_from_palette_size(_palette_size):
    # Returns the matching byte size of a pixel and file extension for a palette of a given size
    if _palette_size <= 2:   return 1/8, '.1bpp'
    if _palette_size <= 4:   return 1/4, '.2bpp'
    if _palette_size <= 16:  return 1/2, '.4bpp'
    if _palette_size <= 256: return 1,   '.8bpp'
    raise Exception('A sprite with a palette with more than 256 colors cannot be handled by the ROM.')

def handle_overworld_custom_size(_extra_data):
    # Checks if the custom size passed for a given overworld sprite sheet is valid
    sizes = _extra_data[0].split('x')
    if len(sizes) != 2:
        raise Exception('An overworld sprite\'s custom size must be in the format <width>x<height>, with <width> and <height> as numbers.')
    sprite_width = int(sizes[0])
    sprite_height = int(sizes[1])
    valid_sprite_size = next(filter(lambda f: f['width'] == sprite_width and f['height'] == sprite_height, VALID_OVERWORLD_SPRITE_SIZES), None)
    if not valid_sprite_size:
        raise Exception('Overworld sprites cannot have a custom size of {}x{}'.format(sizes[0], sizes[1]))
    return valid_sprite_size

def get_overworld_sprite_data(_data_address, _key):
    # Returns the value of given data from an overworld sprite data object
    value_data = OVERWORLD_SPRITE_OBJECT_INFO.get(_key, None)
    if not value_data:
        raise Exception('Could not get the value {} from an overworld sprite\'s data.'.format(_key))
    starting_address = _data_address + value_data.get('shift')
    end_address = starting_address + value_data.get('size')
    return int.from_bytes(bytes(current_rom[starting_address:end_address]), 'little')

def set_overworld_sprite_data(_data_address, _key, _value:int):
    # Sets the value of given data from an overworld sprite data object
    value_data = OVERWORLD_SPRITE_OBJECT_INFO.get(_key, None)
    if not value_data:
        raise Exception('Could not set the value {} from an overworld sprite\'s data.'.format(_key))
    starting_address = _data_address + value_data.get('shift')
    size = value_data.get('size')
    add_data_to_patch({ "address": starting_address, "length": size, "data": _value.to_bytes(size, 'little')})

def is_complex_sprite(_sprite_key):
    return _sprite_key in COMPLEX_SPRITES_LIST

def is_overworld_sprite(_sprite_key:str):
    return _sprite_key.startswith('trainer_') and not 'battle' in _sprite_key