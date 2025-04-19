import os
from pygbagfx import _gbagfx # from package
from .data import data

POKEMON_NAME_TO_ID = { "Bulbasaur": 1, "Ivysaur": 2, "Venusaur": 3, "Charmander": 4, "Charmeleon": 5, "Charizard": 6, "Squirtle": 7, "Wartortle": 8, "Blastoise": 9, "Caterpie": 10, "Metapod": 11, "Butterfree": 12, "Weedle": 13, "Kakuna": 14, "Beedrill": 15, "Pidgey": 16, "Pidgeotto": 17, "Pidgeot": 18, "Rattata": 19, "Raticate": 20, "Spearow": 21, "Fearow": 22, "Ekans": 23, "Arbok": 24, "Pikachu": 25, "Raichu": 26, "Sandshrew": 27, "Sandslash": 28, "Nidoran♀": 29, "Nidorina": 30, "Nidoqueen": 31, "Nidoran♂": 32, "Nidorino": 33, "Nidoking": 34, "Clefairy": 35, "Clefable": 36, "Vulpix": 37, "Ninetales": 38, "Jigglypuff": 39, "Wigglytuff": 40, "Zubat": 41, "Golbat": 42, "Oddish": 43, "Gloom": 44, "Vileplume": 45, "Paras": 46, "Parasect": 47, "Venonat": 48, "Venomoth": 49, "Diglett": 50, "Dugtrio": 51, "Meowth": 52, "Persian": 53, "Psyduck": 54, "Golduck": 55, "Mankey": 56, "Primeape": 57, "Growlithe": 58, "Arcanine": 59, "Poliwag": 60, "Poliwhirl": 61, "Poliwrath": 62, "Abra": 63, "Kadabra": 64, "Alakazam": 65, "Machop": 66, "Machoke": 67, "Machamp": 68, "Bellsprout": 69, "Weepinbell": 70, "Victreebel": 71, "Tentacool": 72, "Tentacruel": 73, "Geodude": 74, "Graveler": 75, "Golem": 76, "Ponyta": 77, "Rapidash": 78, "Slowpoke": 79, "Slowbro": 80, "Magnemite": 81, "Magneton": 82, "Farfetch'd": 83, "Doduo": 84, "Dodrio": 85, "Seel": 86, "Dewgong": 87, "Grimer": 88, "Muk": 89, "Shellder": 90, "Cloyster": 91, "Gastly": 92, "Haunter": 93, "Gengar": 94, "Onix": 95, "Drowzee": 96, "Hypno": 97, "Krabby": 98, "Kingler": 99, "Voltorb": 100, "Electrode": 101, "Exeggcute": 102, "Exeggutor": 103, "Cubone": 104, "Marowak": 105, "Hitmonlee": 106, "Hitmonchan": 107, "Lickitung": 108, "Koffing": 109, "Weezing": 110, "Rhyhorn": 111, "Rhydon": 112, "Chansey": 113, "Tangela": 114, "Kangaskhan": 115, "Horsea": 116, "Seadra": 117, "Goldeen": 118, "Seaking": 119, "Staryu": 120, "Starmie": 121, "Mr. Mime": 122, "Scyther": 123, "Jynx": 124, "Electabuzz": 125, "Magmar": 126, "Pinsir": 127, "Tauros": 128, "Magikarp": 129, "Gyarados": 130, "Lapras": 131, "Ditto": 132, "Eevee": 133, "Vaporeon": 134, "Jolteon": 135, "Flareon": 136, "Porygon": 137, "Omanyte": 138, "Omastar": 139, "Kabuto": 140, "Kabutops": 141, "Aerodactyl": 142, "Snorlax": 143, "Articuno": 144, "Zapdos": 145, "Moltres": 146, "Dratini": 147, "Dragonair": 148, "Dragonite": 149, "Mewtwo": 150, "Mew": 151, "Chikorita": 152, "Bayleef": 153, "Meganium": 154, "Cyndaquil": 155, "Quilava": 156, "Typhlosion": 157, "Totodile": 158, "Croconaw": 159, "Feraligatr": 160, "Sentret": 161, "Furret": 162, "Hoothoot": 163, "Noctowl": 164, "Ledyba": 165, "Ledian": 166, "Spinarak": 167, "Ariados": 168, "Crobat": 169, "Chinchou": 170, "Lanturn": 171, "Pichu": 172, "Cleffa": 173, "Igglybuff": 174, "Togepi": 175, "Togetic": 176, "Natu": 177, "Xatu": 178, "Mareep": 179, "Flaaffy": 180, "Ampharos": 181, "Bellossom": 182, "Marill": 183, "Azumarill": 184, "Sudowoodo": 185, "Politoed": 186, "Hoppip": 187, "Skiploom": 188, "Jumpluff": 189, "Aipom": 190, "Sunkern": 191, "Sunflora": 192, "Yanma": 193, "Wooper": 194, "Quagsire": 195, "Espeon": 196, "Umbreon": 197, "Murkrow": 198, "Slowking": 199, "Misdreavus": 200, "Unown": 201, "Wobbuffet": 202, "Girafarig": 203, "Pineco": 204, "Forretress": 205, "Dunsparce": 206, "Gligar": 207, "Steelix": 208, "Snubbull": 209, "Granbull": 210, "Qwilfish": 211, "Scizor": 212, "Shuckle": 213, "Heracross": 214, "Sneasel": 215, "Teddiursa": 216, "Ursaring": 217, "Slugma": 218, "Magcargo": 219, "Swinub": 220, "Piloswine": 221, "Corsola": 222, "Remoraid": 223, "Octillery": 224, "Delibird": 225, "Mantine": 226, "Skarmory": 227, "Houndour": 228, "Houndoom": 229, "Kingdra": 230, "Phanpy": 231, "Donphan": 232, "Porygon2": 233, "Stantler": 234, "Smeargle": 235, "Tyrogue": 236, "Hitmontop": 237, "Smoochum": 238, "Elekid": 239, "Magby": 240, "Miltank": 241, "Blissey": 242, "Raikou": 243, "Entei": 244, "Suicune": 245, "Larvitar": 246, "Pupitar": 247, "Tyranitar": 248, "Lugia": 249, "Ho-oh": 250, "Celebi": 251, "Treecko": 252, "Grovyle": 253, "Sceptile": 254, "Torchic": 255, "Combusken": 256, "Blaziken": 257, "Mudkip": 258, "Marshtomp": 259, "Swampert": 260, "Poochyena": 261, "Mightyena": 262, "Zigzagoon": 263, "Linoone": 264, "Wurmple": 265, "Silcoon": 266, "Beautifly": 267, "Cascoon": 268, "Dustox": 269, "Lotad": 270, "Lombre": 271, "Ludicolo": 272, "Seedot": 273, "Nuzleaf": 274, "Shiftry": 275, "Taillow": 276, "Swellow": 277, "Wingull": 278, "Pelipper": 279, "Ralts": 280, "Kirlia": 281, "Gardevoir": 282, "Surskit": 283, "Masquerain": 284, "Shroomish": 285, "Breloom": 286, "Slakoth": 287, "Vigoroth": 288, "Slaking": 289, "Nincada": 290, "Ninjask": 291, "Shedinja": 292, "Whismur": 293, "Loudred": 294, "Exploud": 295, "Makuhita": 296, "Hariyama": 297, "Azurill": 298, "Nosepass": 299, "Skitty": 300, "Delcatty": 301, "Sableye": 302, "Mawile": 303, "Aron": 304, "Lairon": 305, "Aggron": 306, "Meditite": 307, "Medicham": 308, "Electrike": 309, "Manectric": 310, "Plusle": 311, "Minun": 312, "Volbeat": 313, "Illumise": 314, "Roselia": 315, "Gulpin": 316, "Swalot": 317, "Carvanha": 318, "Sharpedo": 319, "Wailmer": 320, "Wailord": 321, "Numel": 322, "Camerupt": 323, "Torkoal": 324, "Spoink": 325, "Grumpig": 326, "Spinda": 327, "Trapinch": 328, "Vibrava": 329, "Flygon": 330, "Cacnea": 331, "Cacturne": 332, "Swablu": 333, "Altaria": 334, "Zangoose": 335, "Seviper": 336, "Lunatone": 337, "Solrock": 338, "Barboach": 339, "Whiscash": 340, "Corphish": 341, "Crawdaunt": 342, "Baltoy": 343, "Claydol": 344, "Lileep": 345, "Cradily": 346, "Anorith": 347, "Armaldo": 348, "Feebas": 349, "Milotic": 350, "Castform": 351, "Kecleon": 352, "Shuppet": 353, "Banette": 354, "Duskull": 355, "Dusclops": 356, "Tropius": 357, "Chimecho": 358, "Absol": 359, "Wynaut": 360, "Snorunt": 361, "Glalie": 362, "Spheal": 363, "Sealeo": 364, "Walrein": 365, "Clamperl": 366, "Huntail": 367, "Gorebyss": 368, "Relicanth": 369, "Luvdisc": 370, "Bagon": 371, "Shelgon": 372, "Salamence": 373, "Beldum": 374, "Metang": 375, "Metagross": 376, "Regirock": 377, "Regice": 378, "Registeel": 379, "Latias": 380, "Latios": 381, "Kyogre": 382, "Groudon": 383, "Rayquaza": 384, "Jirachi": 385, "Deoxys": 386 }
POKEMON_ID_TO_INTERNAL_ID = { 252: 277, 253: 278, 254: 279, 255: 280, 256: 281, 257: 282, 258: 283, 259: 284, 260: 285, 261: 286, 262: 287, 263: 288, 264: 289, 265: 290, 266: 291, 267: 292, 268: 293, 269: 294, 270: 295, 271: 296, 272: 297, 273: 298, 274: 299, 275: 300, 276: 304, 277: 305, 278: 309, 279: 310, 280: 392, 281: 393, 282: 394, 283: 311, 284: 312, 285: 306, 286: 307, 287: 364, 288: 365, 289: 366, 290: 301, 291: 302, 292: 303, 293: 370, 294: 371, 295: 372, 296: 335, 297: 336, 298: 350, 299: 320, 300: 315, 301: 316, 302: 322, 303: 355, 304: 382, 305: 383, 306: 384, 307: 356, 308: 357, 309: 337, 310: 338, 311: 353, 312: 354, 313: 386, 314: 387, 315: 363, 316: 367, 317: 368, 318: 330, 319: 331, 320: 313, 321: 314, 322: 339, 323: 340, 324: 321, 325: 351, 326: 352, 327: 308, 328: 332, 329: 333, 330: 334, 331: 344, 332: 345, 333: 358, 334: 359, 335: 380, 336: 379, 337: 348, 338: 349, 339: 323, 340: 324, 341: 326, 342: 327, 343: 318, 344: 319, 345: 388, 346: 389, 347: 390, 348: 391, 349: 328, 350: 329, 351: 385, 352: 317, 353: 377, 354: 378, 355: 361, 356: 362, 357: 369, 358: 411, 359: 376, 360: 360, 361: 346, 362: 347, 363: 341, 364: 342, 365: 343, 366: 373, 367: 375, 368: 376, 369: 381, 370: 325, 371: 395, 372: 396, 373: 397, 374: 398, 375: 399, 376: 400, 377: 401, 378: 402, 379: 403, 380: 407, 381: 408, 382: 404, 383: 405, 384: 406, 385: 409, 386: 410 }

POKEMON_FOLDERS = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys"]
POKEMON_SPRITES = ["front_anim", "back", "icon", "icon_0", "icon_1", "icon_2", "footprint"]
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
TRAINER_BATTLE_PALETTE_EXTRACTION_PRIORITY = ["battle_front", "battle_back"]
TRAINER_PALETTES = {
    "palette": TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY,
    "palette_reflection": TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY,
    "palette_underwater": TRAINER_UNDERWATER_PALETTE_EXTRACTION_PRIORITY,
    "palette_battle": TRAINER_BATTLE_PALETTE_EXTRACTION_PRIORITY
}

OBJECT_NEEDS_COMPRESSION = {
    "pokemon_front_anim":     True,
    "pokemon_back":           True,
    "trainer_battle_front":   True,
    "pokemon_palette":        True,
    "pokemon_palette_shiny":  True,
    "trainer_palette_battle": True,
}

# TODO: Replace DATA_ADDRESSES_MOCK with data.rom_addresses
INTERNAL_ID_TO_SPRITE_ADDRESS = {
    "pokemon_front_anim":    lambda a : DATA_ADDRESSES_MOCK["gMonFrontPicTable"]      + 8 * a,
    "pokemon_back":          lambda a : DATA_ADDRESSES_MOCK["gMonBackPicTable"]       + 8 * a,
    "pokemon_icon":          lambda a : DATA_ADDRESSES_MOCK["gMonIconTable"]          + 4 * a,
    "pokemon_icon_index":    lambda a : DATA_ADDRESSES_MOCK["gMonIconPaletteIndices"] + a,
    "pokemon_footprint":     lambda a : DATA_ADDRESSES_MOCK["gMonFootprintTable"]     + 4 * a,
    "pokemon_palette":       lambda a : DATA_ADDRESSES_MOCK["gMonPaletteTable"]       + 8 * a,
    "pokemon_palette_shiny": lambda a : DATA_ADDRESSES_MOCK["gMonShinyPaletteTable"]  + 8 * a,
    "brendan_walking_running": lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanNormal"],
    "brendan_mach_bike":       lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanMachBike"],
    "brendan_acro_bike":       lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanAcroBike"],
    "brendan_surfing":         lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanSurfing"],
    "brendan_field_move":      lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanFieldMove"],
    "brendan_underwater":      lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanUnderwater"],
    "brendan_fishing":         lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanFishing"],
    "brendan_watering":        lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanWatering"],
    "brendan_decorating":      lambda : DATA_ADDRESSES_MOCK["sPicTable_BrendanDecorating"],
    "brendan_battle_front":    lambda : DATA_ADDRESSES_MOCK["gTrainerFrontPicTable"] + 568,
    "brendan_battle_back":     lambda : DATA_ADDRESSES_MOCK["gTrainerBackPicTable"],
    "brendan_battle_back_2":   lambda : DATA_ADDRESSES_MOCK["sTrainerBackSpriteTemplates"],
    "brendan_palette_battle":  lambda : DATA_ADDRESSES_MOCK["gTrainerBackPicPaletteTable"],
    "may_walking_running": lambda : DATA_ADDRESSES_MOCK["sPicTable_MayNormal"],
    "may_mach_bike":       lambda : DATA_ADDRESSES_MOCK["sPicTable_MayMachBike"],
    "may_acro_bike":       lambda : DATA_ADDRESSES_MOCK["sPicTable_MayAcroBike"],
    "may_surfing":         lambda : DATA_ADDRESSES_MOCK["sPicTable_MaySurfing"],
    "may_field_move":      lambda : DATA_ADDRESSES_MOCK["sPicTable_MayFieldMove"],
    "may_underwater":      lambda : DATA_ADDRESSES_MOCK["sPicTable_MayUnderwater"],
    "may_fishing":         lambda : DATA_ADDRESSES_MOCK["sPicTable_MayFishing"],
    "may_watering":        lambda : DATA_ADDRESSES_MOCK["sPicTable_MayWatering"],
    "may_decorating":      lambda : DATA_ADDRESSES_MOCK["sPicTable_MayDecorating"],
    "may_battle_front":    lambda : DATA_ADDRESSES_MOCK["gTrainerFrontPicTable"] + 576,
    "may_battle_back":     lambda : DATA_ADDRESSES_MOCK["gTrainerBackPicTable"] + 8,
    "may_battle_back_2":   lambda : DATA_ADDRESSES_MOCK["sTrainerBackSpriteTemplates"] + 24,
    "may_palette_battle":  lambda : DATA_ADDRESSES_MOCK["gTrainerBackPicPaletteTable"] + 8,
}

PALETTE_TO_ADDRESS_LABEL_DICT = {
    "trainer_palette": "gObjectEventPal_OBJECT",
    "trainer_palette_reflection": "gObjectEventPal_OBJECTReflection",
    "trainer_palette_underwater": "gObjectEventPal_PlayerUnderwater"
}

TRAINER_SPRITES_FRAMES_AND_SIZES = {
    "trainer_walking_running": { "frames": 18, "size": 256  },
    "trainer_mach_bike":       { "frames": 9,  "size": 512  },
    "trainer_acro_bike":       { "frames": 27, "size": 512  },
    "trainer_surfing":         { "frames": 12, "size": 512  },
    "trainer_field_move":      { "frames": 5,  "size": 512  },
    "trainer_underwater":      { "frames": 9,  "size": 512  },
    "trainer_fishing":         { "frames": 12, "size": 512  },
    "trainer_watering":        { "frames": 9,  "size": 512  },
    "trainer_decorating":      { "frames": 1,  "size": 256  },
    "trainer_battle_back_2":   { "frames": 4,  "size": 2048 }
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
    "gTrainerFrontPicTable": 0x309f9c,
    "gTrainerBackPicTable": 0x30a694,
    "gTrainerBackPicPaletteTable": 0x30a6d4,
    "sTrainerBackSpriteTemplates": 0x00,
    "sPicTable_BrendanNormal": 0x00,
    "sPicTable_BrendanMachBike": 0x00,
    "sPicTable_BrendanAcroBike": 0x00,
    "sPicTable_BrendanSurfing": 0x00,
    "sPicTable_BrendanUnderwater": 0x00,
    "sPicTable_BrendanFieldMove": 0x00,
    "sPicTable_BrendanFishing": 0x00,
    "sPicTable_BrendanWatering": 0x00,
    "sPicTable_BrendanDecorating": 0x00,
    "sPicTable_MayNormal": 0x00,
    "sPicTable_MayMachBike": 0x00,
    "sPicTable_MayAcroBike": 0x00,
    "sPicTable_MaySurfing": 0x00,
    "sPicTable_MayUnderwater": 0x00,
    "sPicTable_MayFieldMove": 0x00,
    "sPicTable_MayFishing": 0x00,
    "sPicTable_MayWatering": 0x00,
    "sPicTable_MayDecorating": 0x00,
    "gObjectEventPal_Brendan": 0x49fd28,
    "gObjectEventPal_May": 0x4ab7a8,
    "gObjectEventPal_BrendanReflection": 0x4a1148,
    "gObjectEventPal_MayReflection": 0x4ab7c8,
    "gObjectEventPal_PlayerUnderwater": 0x4aa588,
    "sEmpty6": 0xe3cf51
}
DATA_ADDRESSES_MOCK_BASE = {
    "gMonFrontPicTable": 0x30a18c,
    "gMonBackPicTable": 0x3028b8,
    "gMonIconTable": 0x57bca8,
    "gMonFootprintTable": 0x56e694,
    "gMonPaletteTable": 0x303678,
    "gMonShinyPaletteTable": 0x304438,
    "gMonIconPaletteIndices": 0x57c388,
    "gObjectEventGraphicsInfoPointers": 0x505620,
    "gTrainerFrontPicTable": 0x305654,
    "gTrainerBackPicTable": 0x305d4c,
    "gTrainerBackPicPaletteTable": 0x305d8c,
    "sTrainerBackSpriteTemplates": 0x329df8,
    "sPicTable_BrendanNormal": 0x505a8c,
    "sPicTable_BrendanMachBike": 0x505b1c,
    "sPicTable_BrendanAcroBike": 0x505b64,
    "sPicTable_BrendanSurfing": 0x505c3c,
    "sPicTable_BrendanUnderwater": 0x505c9c,
    "sPicTable_BrendanFieldMove": 0x505ce4,
    "sPicTable_BrendanFishing": 0x507a4c,
    "sPicTable_BrendanWatering": 0x507e24,
    "sPicTable_BrendanDecorating": 0x507eb4,
    "sPicTable_MayNormal": 0x507144,
    "sPicTable_MayMachBike": 0x5071d4,
    "sPicTable_MayAcroBike": 0x50721c,
    "sPicTable_MaySurfing": 0x5072f4,
    "sPicTable_MayUnderwater": 0x507354,
    "sPicTable_MayFieldMove": 0x50739c,
    "sPicTable_MayFishing": 0x507aac,
    "sPicTable_MayWatering": 0x507e6c,
    "sPicTable_MayDecorating": 0x507ebc,
    "gObjectEventPal_Brendan": 0x4987f8,
    "gObjectEventPal_May": 0x4a4278,
    "gObjectEventPal_BrendanReflection": 0x499c18,
    "gObjectEventPal_MayReflection": 0x4a4298,
    "gObjectEventPal_PlayerUnderwater": 0x4a3058,
    "sEmpty6": 0xe3cf31
}
DATA_ADDRESSES_MOCK = DATA_ADDRESSES_MOCK_BASE # Use DATA_ADDRESSES_MOCK_BASE for original ROMS, DATA_ADDRESSES_MOCK_AP for AP-patched ROMS

address_label_to_resource_path_list = { }
files_to_clean_up = []
sprite_pack_data = { }
sprite_address_to_insert_to = 0x00


def handle_sprite_pack(_sprite_pack_path, _rom):
    global sprite_pack_data, sprite_address_to_insert_to
    # Build patch data, fetch end of file
    sprite_pack_data = { "length": 16777216, "data": [] }
    sprite_address_to_insert_to = ((DATA_ADDRESSES_MOCK["sEmpty6"] >> 12) + 1) << 12 # Should be E3D000

    # Handle existing Pokemon & Trainer folders
    for pokemon_name in POKEMON_FOLDERS:
        pokemon_folder_path = os.path.join(_sprite_pack_path, pokemon_name)
        if os.path.exists(pokemon_folder_path):
            handle_pokemon_folder(pokemon_folder_path, pokemon_name, _rom)
    for trainer_name in TRAINER_FOLDERS:
        trainer_folder_path = os.path.join(_sprite_pack_path, trainer_name)
        if os.path.exists(trainer_folder_path):
            handle_trainer_folder(trainer_folder_path, trainer_name, _rom)

    print(sprite_pack_data)
    # Remove temporary files
    clean_up()
    return sprite_pack_data


def handle_pokemon_folder(_pokemon_folder_path, _pokemon_name, _rom):
    for sprite_name in POKEMON_SPRITES:
        # Handle existing Pokemon sprites
        sprite_path = os.path.join(_pokemon_folder_path, sprite_name) + ".png"
        if os.path.exists(sprite_path):
            add_sprite(True, _pokemon_name, sprite_name, sprite_path, _rom)
    for palette, palette_extraction_priority_queue in POKEMON_PALETTES.items():
        # Generate Pokemon palettes if sprites exist
        for sprite_name in palette_extraction_priority_queue:
            sprite_path = os.path.join(_pokemon_folder_path, sprite_name) + ".png"
            if os.path.exists(sprite_path):
                add_palette(True, _pokemon_name, palette, sprite_path, _rom)
                break

def handle_trainer_folder(_trainer_folder_path, _trainer_name, _rom):
    for sprite_name in TRAINER_SPRITES:
        # Handle existing Trainer sprites
        sprite_path = os.path.join(_trainer_folder_path, sprite_name) + ".png"
        if os.path.exists(sprite_path):
            add_sprite(False, _trainer_name, sprite_name, sprite_path, _rom)
    for palette, palette_extraction_priority_queue in TRAINER_PALETTES.items():
        # Generate Trainer palettes if sprites exist
        for sprite_name in palette_extraction_priority_queue:
            sprite_path = os.path.join(_trainer_folder_path, sprite_name) + ".png"
            if os.path.exists(sprite_path):
                add_palette(False, _trainer_name, palette, sprite_path, _rom)
                break


def handle_sprite_to_gba_sprite(_sprite_path, _needs_compression) -> str:
    # Transform Indexed/Grayscale PNG sprites into GBA sprites
    sprite_path_with_no_extension = str(os.path.splitext(_sprite_path)[0])
    file_format = ".1bpp" if sprite_path_with_no_extension.endswith("footprint") else ".4bpp"
    gba_sprite_path = sprite_path_with_no_extension + file_format
    call_gbagfx(_sprite_path, gba_sprite_path, False)
    if not _needs_compression:
        files_to_clean_up.append(gba_sprite_path)
        return gba_sprite_path
    else:
        # Compress sprite if needed
        compressed_gba_sprite_path = gba_sprite_path + ".lz"
        call_gbagfx(gba_sprite_path, compressed_gba_sprite_path, True)
        files_to_clean_up.append(compressed_gba_sprite_path)
        return compressed_gba_sprite_path

def add_sprite(_is_pokemon, _object_name, _sprite_name, _path, _rom):
    is_palette_indexed_icon = False
    palette_index = 0
    if _sprite_name.startswith("icon_"):
        # Palette indexed icon: Store palette index from file name
        is_palette_indexed_icon = True
        palette_index = int(_sprite_name[-1:])
        _sprite_name = "icon"
    sprite_key = ("pokemon_" if _is_pokemon else "trainer_") + _sprite_name

    global sprite_address_to_insert_to
    if _is_pokemon:
        # Fetch internal Pokemon ID & sprite address
        pokemon_id = POKEMON_NAME_TO_ID[_object_name]
        pokemon_internal_id = POKEMON_ID_TO_INTERNAL_ID.get(pokemon_id, pokemon_id)
        data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[sprite_key](pokemon_internal_id)
        if is_palette_indexed_icon:
            # Special case: Palette indexed icons, since icons have 3 palettes
            icon_index_address = INTERNAL_ID_TO_SPRITE_ADDRESS[sprite_key + "_index"](pokemon_internal_id)
            add_data_to_sprite_pack({ "address": icon_index_address, "length": 1, "data": palette_index.to_bytes(1, 'little')})
    else:
        # Fetch named Trainer sprite address
        named_key = _object_name.lower() + "_" + _sprite_name
        data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[named_key]()

    if not _is_pokemon and sprite_key in TRAINER_SPRITES_FRAMES_AND_SIZES:
        # Special case: Some Trainer sprites point to info struct, not sprite itself
        if sprite_key == "trainer_battle_back_2":
            # Special case: Trainer Back sprites need further pointer seeking
            data_address = int.from_bytes(bytes(_rom[data_address + 12:data_address + 15]), 'little')
        build_complex_sprite(data_address, sprite_key)
    else:
        # Replace pointer to old sprite with pointer to new sprite
        address_bytes = sprite_address_to_insert_to.to_bytes(3, 'little')
        add_data_to_sprite_pack({ "address": data_address, "length": 3, "data": address_bytes })


    if sprite_key != "trainer_battle_back":
        # Register sprite at end of file, push back end of file
        needs_compression = OBJECT_NEEDS_COMPRESSION.get(sprite_key, False)
        _path = handle_sprite_to_gba_sprite(_path, needs_compression)
        sprite_file = open(_path, "rb")
        sprite_file_data = sprite_file.read()
        add_data_to_sprite_pack({ "address": sprite_address_to_insert_to, "length": len(sprite_file_data), "data": sprite_file_data })
        sprite_address_to_insert_to = (((sprite_address_to_insert_to + len(sprite_file_data)) >> 8) + 1) << 8
    else:
        # Special case: In case of Trainer Battle back sprite, rerun this function for the ball throwing animation
        add_sprite(_is_pokemon, _object_name, _sprite_name + "_2", _path, _rom)

def build_complex_sprite(data_address, named_key):
    frames_and_size = TRAINER_SPRITES_FRAMES_AND_SIZES.get(named_key)
    temp_address = sprite_address_to_insert_to
    if not frames_and_size:
        return
    output_data = bytearray(0)
    for i in range(0, frames_and_size["frames"]):
        output_data.extend(temp_address.to_bytes(3, 'little'))
        output_data.extend(b'\x08')
        output_data.extend(frames_and_size["size"].to_bytes(2, 'little'))
        output_data.extend(b'\x00\x00')
        temp_address += frames_and_size["size"]
    add_data_to_sprite_pack({"address": data_address, "length": len(output_data), "data": bytes(output_data)})


def handle_sprite_to_palette(_sprite_path, _palette_name, _needs_compression) -> str:
    # Transform Indexed/Grayscale PNG sprites into GBA palettes
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

def add_palette(_is_pokemon, _object_name, _palette_name, _path, _rom):
    palette_key = ("pokemon" if _is_pokemon else "trainer") + "_" + _palette_name
    data_address = 0x00
    if _is_pokemon:
        # Pokemon: All labels broken, grab palette pointer address from corresponding palette table
        pokemon_id = POKEMON_NAME_TO_ID[_object_name]
        pokemon_internal_id = POKEMON_ID_TO_INTERNAL_ID.get(pokemon_id, pokemon_id)
        palette_key = "pokemon_" + _palette_name
        data_address = INTERNAL_ID_TO_SPRITE_ADDRESS[palette_key](pokemon_internal_id)
    else:
        # Trainer: Battle palette labels broken, fetch from trainer battle palette table
        named_key = _object_name.lower() + "_" + _palette_name
        data_address_func = INTERNAL_ID_TO_SPRITE_ADDRESS.get(named_key)
        if data_address_func:
            data_address = data_address_func()
    if data_address:
        # Fetch address in ROM if no direct palette address available/valid
        data_address = int.from_bytes(bytes(_rom[data_address:data_address + 3]), 'little')

    # Replace tag with Pokemon/Trainer name for direct palette addresses
    address_label = PALETTE_TO_ADDRESS_LABEL_DICT.get(palette_key)
    if address_label:
        address_label = address_label.replace("OBJECT", _object_name)

    needs_compression = OBJECT_NEEDS_COMPRESSION.get(palette_key, False)
    _path = handle_sprite_to_palette(_path, _palette_name, needs_compression)
    palette_file = open(_path, "rb")
    palette_file_data = palette_file.read()
    add_data_to_sprite_pack({ "address": data_address or DATA_ADDRESSES_MOCK[address_label], "length": len(palette_file_data), "data": palette_file_data })


def add_data_to_sprite_pack(_data):
    index = 0
    # Order entries by ascending starting address
    for existing_data in sprite_pack_data["data"]:
        if existing_data["address"] < _data["address"]:
            index = index + 1
        else:
            break
    sprite_pack_data["data"].insert(index, _data)


def clean_up():
    # Remove all temporary files after processing
    for file in files_to_clean_up:
        if os.path.isfile(file):
            os.remove(file)
    files_to_clean_up.clear()


def call_gbagfx(_input, _output, _delete_input = False):
    # Calls sprite processing C app
    _gbagfx.main(_input, _output)
    if _delete_input:
        os.remove(_input)