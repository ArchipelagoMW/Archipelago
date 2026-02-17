import copy


class PointerInfo:
    shift: int = 0
    size: int = 0

    def __init__(self, _shift, _size):
        self.shift = _shift
        self.size = _size


class ObjectInfo:
    length: int = 0
    pointers: dict[str, PointerInfo] = {}

    def __init__(self, _length, _pointers):
        self.length = _length
        self.pointers = _pointers


POKEMON_NAME_TO_ID = {
    "Bulbasaur": 1,
    "Ivysaur": 2,
    "Venusaur": 3,
    "Charmander": 4,
    "Charmeleon": 5,
    "Charizard": 6,
    "Squirtle": 7,
    "Wartortle": 8,
    "Blastoise": 9,
    "Caterpie": 10,
    "Metapod": 11,
    "Butterfree": 12,
    "Weedle": 13,
    "Kakuna": 14,
    "Beedrill": 15,
    "Pidgey": 16,
    "Pidgeotto": 17,
    "Pidgeot": 18,
    "Rattata": 19,
    "Raticate": 20,
    "Spearow": 21,
    "Fearow": 22,
    "Ekans": 23,
    "Arbok": 24,
    "Pikachu": 25,
    "Raichu": 26,
    "Sandshrew": 27,
    "Sandslash": 28,
    "Nidoran Female": 29,
    "Nidorina": 30,
    "Nidoqueen": 31,
    "Nidoran Male": 32,
    "Nidorino": 33,
    "Nidoking": 34,
    "Clefairy": 35,
    "Clefable": 36,
    "Vulpix": 37,
    "Ninetales": 38,
    "Jigglypuff": 39,
    "Wigglytuff": 40,
    "Zubat": 41,
    "Golbat": 42,
    "Oddish": 43,
    "Gloom": 44,
    "Vileplume": 45,
    "Paras": 46,
    "Parasect": 47,
    "Venonat": 48,
    "Venomoth": 49,
    "Diglett": 50,
    "Dugtrio": 51,
    "Meowth": 52,
    "Persian": 53,
    "Psyduck": 54,
    "Golduck": 55,
    "Mankey": 56,
    "Primeape": 57,
    "Growlithe": 58,
    "Arcanine": 59,
    "Poliwag": 60,
    "Poliwhirl": 61,
    "Poliwrath": 62,
    "Abra": 63,
    "Kadabra": 64,
    "Alakazam": 65,
    "Machop": 66,
    "Machoke": 67,
    "Machamp": 68,
    "Bellsprout": 69,
    "Weepinbell": 70,
    "Victreebel": 71,
    "Tentacool": 72,
    "Tentacruel": 73,
    "Geodude": 74,
    "Graveler": 75,
    "Golem": 76,
    "Ponyta": 77,
    "Rapidash": 78,
    "Slowpoke": 79,
    "Slowbro": 80,
    "Magnemite": 81,
    "Magneton": 82,
    "Farfetch'd": 83,
    "Doduo": 84,
    "Dodrio": 85,
    "Seel": 86,
    "Dewgong": 87,
    "Grimer": 88,
    "Muk": 89,
    "Shellder": 90,
    "Cloyster": 91,
    "Gastly": 92,
    "Haunter": 93,
    "Gengar": 94,
    "Onix": 95,
    "Drowzee": 96,
    "Hypno": 97,
    "Krabby": 98,
    "Kingler": 99,
    "Voltorb": 100,
    "Electrode": 101,
    "Exeggcute": 102,
    "Exeggutor": 103,
    "Cubone": 104,
    "Marowak": 105,
    "Hitmonlee": 106,
    "Hitmonchan": 107,
    "Lickitung": 108,
    "Koffing": 109,
    "Weezing": 110,
    "Rhyhorn": 111,
    "Rhydon": 112,
    "Chansey": 113,
    "Tangela": 114,
    "Kangaskhan": 115,
    "Horsea": 116,
    "Seadra": 117,
    "Goldeen": 118,
    "Seaking": 119,
    "Staryu": 120,
    "Starmie": 121,
    "Mr. Mime": 122,
    "Scyther": 123,
    "Jynx": 124,
    "Electabuzz": 125,
    "Magmar": 126,
    "Pinsir": 127,
    "Tauros": 128,
    "Magikarp": 129,
    "Gyarados": 130,
    "Lapras": 131,
    "Ditto": 132,
    "Eevee": 133,
    "Vaporeon": 134,
    "Jolteon": 135,
    "Flareon": 136,
    "Porygon": 137,
    "Omanyte": 138,
    "Omastar": 139,
    "Kabuto": 140,
    "Kabutops": 141,
    "Aerodactyl": 142,
    "Snorlax": 143,
    "Articuno": 144,
    "Zapdos": 145,
    "Moltres": 146,
    "Dratini": 147,
    "Dragonair": 148,
    "Dragonite": 149,
    "Mewtwo": 150,
    "Mew": 151,
    "Chikorita": 152,
    "Bayleef": 153,
    "Meganium": 154,
    "Cyndaquil": 155,
    "Quilava": 156,
    "Typhlosion": 157,
    "Totodile": 158,
    "Croconaw": 159,
    "Feraligatr": 160,
    "Sentret": 161,
    "Furret": 162,
    "Hoothoot": 163,
    "Noctowl": 164,
    "Ledyba": 165,
    "Ledian": 166,
    "Spinarak": 167,
    "Ariados": 168,
    "Crobat": 169,
    "Chinchou": 170,
    "Lanturn": 171,
    "Pichu": 172,
    "Cleffa": 173,
    "Igglybuff": 174,
    "Togepi": 175,
    "Togetic": 176,
    "Natu": 177,
    "Xatu": 178,
    "Mareep": 179,
    "Flaaffy": 180,
    "Ampharos": 181,
    "Bellossom": 182,
    "Marill": 183,
    "Azumarill": 184,
    "Sudowoodo": 185,
    "Politoed": 186,
    "Hoppip": 187,
    "Skiploom": 188,
    "Jumpluff": 189,
    "Aipom": 190,
    "Sunkern": 191,
    "Sunflora": 192,
    "Yanma": 193,
    "Wooper": 194,
    "Quagsire": 195,
    "Espeon": 196,
    "Umbreon": 197,
    "Murkrow": 198,
    "Slowking": 199,
    "Misdreavus": 200,
    "Unown A": 201,
    "Wobbuffet": 202,
    "Girafarig": 203,
    "Pineco": 204,
    "Forretress": 205,
    "Dunsparce": 206,
    "Gligar": 207,
    "Steelix": 208,
    "Snubbull": 209,
    "Granbull": 210,
    "Qwilfish": 211,
    "Scizor": 212,
    "Shuckle": 213,
    "Heracross": 214,
    "Sneasel": 215,
    "Teddiursa": 216,
    "Ursaring": 217,
    "Slugma": 218,
    "Magcargo": 219,
    "Swinub": 220,
    "Piloswine": 221,
    "Corsola": 222,
    "Remoraid": 223,
    "Octillery": 224,
    "Delibird": 225,
    "Mantine": 226,
    "Skarmory": 227,
    "Houndour": 228,
    "Houndoom": 229,
    "Kingdra": 230,
    "Phanpy": 231,
    "Donphan": 232,
    "Porygon2": 233,
    "Stantler": 234,
    "Smeargle": 235,
    "Tyrogue": 236,
    "Hitmontop": 237,
    "Smoochum": 238,
    "Elekid": 239,
    "Magby": 240,
    "Miltank": 241,
    "Blissey": 242,
    "Raikou": 243,
    "Entei": 244,
    "Suicune": 245,
    "Larvitar": 246,
    "Pupitar": 247,
    "Tyranitar": 248,
    "Lugia": 249,
    "Ho-oh": 250,
    "Celebi": 251,
    "Treecko": 252,
    "Grovyle": 253,
    "Sceptile": 254,
    "Torchic": 255,
    "Combusken": 256,
    "Blaziken": 257,
    "Mudkip": 258,
    "Marshtomp": 259,
    "Swampert": 260,
    "Poochyena": 261,
    "Mightyena": 262,
    "Zigzagoon": 263,
    "Linoone": 264,
    "Wurmple": 265,
    "Silcoon": 266,
    "Beautifly": 267,
    "Cascoon": 268,
    "Dustox": 269,
    "Lotad": 270,
    "Lombre": 271,
    "Ludicolo": 272,
    "Seedot": 273,
    "Nuzleaf": 274,
    "Shiftry": 275,
    "Taillow": 276,
    "Swellow": 277,
    "Wingull": 278,
    "Pelipper": 279,
    "Ralts": 280,
    "Kirlia": 281,
    "Gardevoir": 282,
    "Surskit": 283,
    "Masquerain": 284,
    "Shroomish": 285,
    "Breloom": 286,
    "Slakoth": 287,
    "Vigoroth": 288,
    "Slaking": 289,
    "Nincada": 290,
    "Ninjask": 291,
    "Shedinja": 292,
    "Whismur": 293,
    "Loudred": 294,
    "Exploud": 295,
    "Makuhita": 296,
    "Hariyama": 297,
    "Azurill": 298,
    "Nosepass": 299,
    "Skitty": 300,
    "Delcatty": 301,
    "Sableye": 302,
    "Mawile": 303,
    "Aron": 304,
    "Lairon": 305,
    "Aggron": 306,
    "Meditite": 307,
    "Medicham": 308,
    "Electrike": 309,
    "Manectric": 310,
    "Plusle": 311,
    "Minun": 312,
    "Volbeat": 313,
    "Illumise": 314,
    "Roselia": 315,
    "Gulpin": 316,
    "Swalot": 317,
    "Carvanha": 318,
    "Sharpedo": 319,
    "Wailmer": 320,
    "Wailord": 321,
    "Numel": 322,
    "Camerupt": 323,
    "Torkoal": 324,
    "Spoink": 325,
    "Grumpig": 326,
    "Spinda": 327,
    "Trapinch": 328,
    "Vibrava": 329,
    "Flygon": 330,
    "Cacnea": 331,
    "Cacturne": 332,
    "Swablu": 333,
    "Altaria": 334,
    "Zangoose": 335,
    "Seviper": 336,
    "Lunatone": 337,
    "Solrock": 338,
    "Barboach": 339,
    "Whiscash": 340,
    "Corphish": 341,
    "Crawdaunt": 342,
    "Baltoy": 343,
    "Claydol": 344,
    "Lileep": 345,
    "Cradily": 346,
    "Anorith": 347,
    "Armaldo": 348,
    "Feebas": 349,
    "Milotic": 350,
    "Castform": 351,
    "Kecleon": 352,
    "Shuppet": 353,
    "Banette": 354,
    "Duskull": 355,
    "Dusclops": 356,
    "Tropius": 357,
    "Chimecho": 358,
    "Absol": 359,
    "Wynaut": 360,
    "Snorunt": 361,
    "Glalie": 362,
    "Spheal": 363,
    "Sealeo": 364,
    "Walrein": 365,
    "Clamperl": 366,
    "Huntail": 367,
    "Gorebyss": 368,
    "Relicanth": 369,
    "Luvdisc": 370,
    "Bagon": 371,
    "Shelgon": 372,
    "Salamence": 373,
    "Beldum": 374,
    "Metang": 375,
    "Metagross": 376,
    "Regirock": 377,
    "Regice": 378,
    "Registeel": 379,
    "Latias": 380,
    "Latios": 381,
    "Kyogre": 382,
    "Groudon": 383,
    "Rayquaza": 384,
    "Jirachi": 385,
    "Deoxys": 386,
    "Unown B": 387,
    "Unown C": 388,
    "Unown D": 389,
    "Unown E": 390,
    "Unown F": 391,
    "Unown G": 392,
    "Unown H": 393,
    "Unown I": 394,
    "Unown J": 395,
    "Unown K": 396,
    "Unown L": 397,
    "Unown M": 398,
    "Unown N": 399,
    "Unown O": 400,
    "Unown P": 401,
    "Unown Q": 402,
    "Unown R": 403,
    "Unown S": 404,
    "Unown T": 405,
    "Unown U": 406,
    "Unown V": 407,
    "Unown W": 408,
    "Unown X": 409,
    "Unown Y": 410,
    "Unown Z": 411,
    "Unown Exclamation Mark": 412,
    "Unown Question Mark": 413,
    "Egg": 414
}
POKEMON_ID_TO_INTERNAL_ID = {
    252: 277,
    253: 278,
    254: 279,
    255: 280,
    256: 281,
    257: 282,
    258: 283,
    259: 284,
    260: 285,
    261: 286,
    262: 287,
    263: 288,
    264: 289,
    265: 290,
    266: 291,
    267: 292,
    268: 293,
    269: 294,
    270: 295,
    271: 296,
    272: 297,
    273: 298,
    274: 299,
    275: 300,
    276: 304,
    277: 305,
    278: 309,
    279: 310,
    280: 392,
    281: 393,
    282: 394,
    283: 311,
    284: 312,
    285: 306,
    286: 307,
    287: 364,
    288: 365,
    289: 366,
    290: 301,
    291: 302,
    292: 303,
    293: 370,
    294: 371,
    295: 372,
    296: 335,
    297: 336,
    298: 350,
    299: 320,
    300: 315,
    301: 316,
    302: 322,
    303: 355,
    304: 382,
    305: 383,
    306: 384,
    307: 356,
    308: 357,
    309: 337,
    310: 338,
    311: 353,
    312: 354,
    313: 386,
    314: 387,
    315: 363,
    316: 367,
    317: 368,
    318: 330,
    319: 331,
    320: 313,
    321: 314,
    322: 339,
    323: 340,
    324: 321,
    325: 351,
    326: 352,
    327: 308,
    328: 332,
    329: 333,
    330: 334,
    331: 344,
    332: 345,
    333: 358,
    334: 359,
    335: 380,
    336: 379,
    337: 348,
    338: 349,
    339: 323,
    340: 324,
    341: 326,
    342: 327,
    343: 318,
    344: 319,
    345: 388,
    346: 389,
    347: 390,
    348: 391,
    349: 328,
    350: 329,
    351: 385,
    352: 317,
    353: 377,
    354: 378,
    355: 361,
    356: 362,
    357: 369,
    358: 411,
    359: 376,
    360: 360,
    361: 346,
    362: 347,
    363: 341,
    364: 342,
    365: 343,
    366: 373,
    367: 374,
    368: 375,
    369: 381,
    370: 325,
    371: 395,
    372: 396,
    373: 397,
    374: 398,
    375: 399,
    376: 400,
    377: 401,
    378: 402,
    379: 403,
    380: 407,
    381: 408,
    382: 404,
    383: 405,
    384: 406,
    385: 409,
    386: 410,
    387: 413,
    388: 414,
    389: 415,
    390: 416,
    391: 417,
    392: 418,
    393: 419,
    394: 420,
    395: 421,
    396: 422,
    397: 423,
    398: 424,
    399: 425,
    400: 426,
    401: 427,
    402: 428,
    403: 429,
    404: 430,
    405: 431,
    406: 432,
    407: 433,
    408: 434,
    409: 435,
    410: 436,
    411: 437,
    412: 438,
    413: 439,
    414: 412,
}
POKEMON_TYPES = [
    "Normal",
    "Fighting",
    "Flying",
    "Poison",
    "Ground",
    "Rock",
    "Bug",
    "Ghost",
    "Steel",
    "???",
    "Fire",
    "Water",
    "Grass",
    "Electric",
    "Psychic",
    "Ice",
    "Dragon",
    "Dark"
]
POKEMON_MOVES = [
    "POUND",
    "KARATE CHOP",
    "DOUBLESLAP",
    "COMET PUNCH",
    "MEGA PUNCH",
    "PAY DAY",
    "FIRE PUNCH",
    "ICE PUNCH",
    "THUNDERPUNCH",
    "SCRATCH",
    "VICEGRIP",
    "GUILLOTINE",
    "RAZOR WIND",
    "SWORDS DANCE",
    "CUT",
    "GUST",
    "WING ATTACK",
    "WHIRLWIND",
    "FLY",
    "BIND",
    "SLAM",
    "VINE WHIP",
    "STOMP",
    "DOUBLE KICK",
    "MEGA KICK",
    "JUMP KICK",
    "ROLLING KICK",
    "SAND-ATTACK",
    "HEADBUTT",
    "HORN ATTACK",
    "FURY ATTACK",
    "HORN DRILL",
    "TACKLE",
    "BODY SLAM",
    "WRAP",
    "TAKE DOWN",
    "THRASH",
    "DOUBLE-EDGE",
    "TAIL WHIP",
    "POISON STING",
    "TWINEEDLE",
    "PIN MISSILE",
    "LEER",
    "BITE",
    "GROWL",
    "ROAR",
    "SING",
    "SUPERSONIC",
    "SONICBOOM",
    "DISABLE",
    "ACID",
    "EMBER",
    "FLAMETHROWER",
    "MIST",
    "WATER GUN",
    "HYDRO PUMP",
    "SURF",
    "ICE BEAM",
    "BLIZZARD",
    "PSYBEAM",
    "BUBBLEBEAM",
    "AURORA BEAM",
    "HYPER BEAM",
    "PECK",
    "DRILL PECK",
    "SUBMISSION",
    "LOW KICK",
    "COUNTER",
    "SEISMIC TOSS",
    "STRENGTH",
    "ABSORB",
    "MEGA DRAIN",
    "LEECH SEED",
    "GROWTH",
    "RAZOR LEAF",
    "SOLARBEAM",
    "POISONPOWDER",
    "STUN SPORE",
    "SLEEP POWDER",
    "PETAL DANCE",
    "STRING SHOT",
    "DRAGON RAGE",
    "FIRE SPIN",
    "THUNDERSHOCK",
    "THUNDERBOLT",
    "THUNDER WAVE",
    "THUNDER",
    "ROCK THROW",
    "EARTHQUAKE",
    "FISSURE",
    "DIG",
    "TOXIC",
    "CONFUSION",
    "PSYCHIC",
    "HYPNOSIS",
    "MEDITATE",
    "AGILITY",
    "QUICK ATTACK",
    "RAGE",
    "TELEPORT",
    "NIGHT SHADE",
    "MIMIC",
    "SCREECH",
    "DOUBLE TEAM",
    "RECOVER",
    "HARDEN",
    "MINIMIZE",
    "SMOKESCREEN",
    "CONFUSE RAY",
    "WITHDRAW",
    "DEFENSE CURL",
    "BARRIER",
    "LIGHT SCREEN",
    "HAZE",
    "REFLECT",
    "FOCUS ENERGY",
    "BIDE",
    "METRONOME",
    "MIRROR MOVE",
    "SELFDESTRUCT",
    "EGG BOMB",
    "LICK",
    "SMOG",
    "SLUDGE",
    "BONE CLUB",
    "FIRE BLAST",
    "WATERFALL",
    "CLAMP",
    "SWIFT",
    "SKULL BASH",
    "SPIKE CANNON",
    "CONSTRICT",
    "AMNESIA",
    "KINESIS",
    "SOFTBOILED",
    "HI JUMP KICK",
    "GLARE",
    "DREAM EATER",
    "POISON GAS",
    "BARRAGE",
    "LEECH LIFE",
    "LOVELY KISS",
    "SKY ATTACK",
    "TRANSFORM",
    "BUBBLE",
    "DIZZY PUNCH",
    "SPORE",
    "FLASH",
    "PSYWAVE",
    "SPLASH",
    "ACID ARMOR",
    "CRABHAMMER",
    "EXPLOSION",
    "FURY SWIPES",
    "BONEMERANG",
    "REST",
    "ROCK SLIDE",
    "HYPER FANG",
    "SHARPEN",
    "CONVERSION",
    "TRI ATTACK",
    "SUPER FANG",
    "SLASH",
    "SUBSTITUTE",
    "STRUGGLE",
    "SKETCH",
    "TRIPLE KICK",
    "THIEF",
    "SPIDER WEB",
    "MIND READER",
    "NIGHTMARE",
    "FLAME WHEEL",
    "SNORE",
    "CURSE",
    "FLAIL",
    "CONVERSION 2",
    "AEROBLAST",
    "COTTON SPORE",
    "REVERSAL",
    "SPITE",
    "POWDER SNOW",
    "PROTECT",
    "MACH PUNCH",
    "SCARY FACE",
    "FAINT ATTACK",
    "SWEET KISS",
    "BELLY DRUM",
    "SLUDGE BOMB",
    "MUD-SLAP",
    "OCTAZOOKA",
    "SPIKES",
    "ZAP CANNON",
    "FORESIGHT",
    "DESTINY BOND",
    "PERISH SONG",
    "ICY WIND",
    "DETECT",
    "BONE RUSH",
    "LOCK-ON",
    "OUTRAGE",
    "SANDSTORM",
    "GIGA DRAIN",
    "ENDURE",
    "CHARM",
    "ROLLOUT",
    "FALSE SWIPE",
    "SWAGGER",
    "MILK DRINK",
    "SPARK",
    "FURY CUTTER",
    "STEEL WING",
    "MEAN LOOK",
    "ATTRACT",
    "SLEEP TALK",
    "HEAL BELL",
    "RETURN",
    "PRESENT",
    "FRUSTRATION",
    "SAFEGUARD",
    "PAIN SPLIT",
    "SACRED FIRE",
    "MAGNITUDE",
    "DYNAMICPUNCH",
    "MEGAHORN",
    "DRAGONBREATH",
    "BATON PASS",
    "ENCORE",
    "PURSUIT",
    "RAPID SPIN",
    "SWEET SCENT",
    "IRON TAIL",
    "METAL CLAW",
    "VITAL THROW",
    "MORNING SUN",
    "SYNTHESIS",
    "MOONLIGHT",
    "HIDDEN POWER",
    "CROSS CHOP",
    "TWISTER",
    "RAIN DANCE",
    "SUNNY DAY",
    "CRUNCH",
    "MIRROR COAT",
    "PSYCH UP",
    "EXTREMESPEED",
    "ANCIENTPOWER",
    "SHADOW BALL",
    "FUTURE SIGHT",
    "ROCK SMASH",
    "WHIRLPOOL",
    "BEAT UP",
    "FAKE OUT",
    "UPROAR",
    "STOCKPILE",
    "SPIT UP",
    "SWALLOW",
    "HEAT WAVE",
    "HAIL",
    "TORMENT",
    "FLATTER",
    "WILL-O-WISP",
    "MEMENTO",
    "FACADE",
    "FOCUS PUNCH",
    "SMELLINGSALT",
    "FOLLOW ME",
    "NATURE POWER",
    "CHARGE",
    "TAUNT",
    "HELPING HAND",
    "TRICK",
    "ROLE PLAY",
    "WISH",
    "ASSIST",
    "INGRAIN",
    "SUPERPOWER",
    "MAGIC COAT",
    "RECYCLE",
    "REVENGE",
    "BRICK BREAK",
    "YAWN",
    "KNOCK OFF",
    "ENDEAVOR",
    "ERUPTION",
    "SKILL SWAP",
    "IMPRISON",
    "REFRESH",
    "GRUDGE",
    "SNATCH",
    "SECRET POWER",
    "DIVE",
    "ARM THRUST",
    "CAMOUFLAGE",
    "TAIL GLOW",
    "LUSTER PURGE",
    "MIST BALL",
    "FEATHERDANCE",
    "TEETER DANCE",
    "BLAZE KICK",
    "MUD SPORT",
    "ICE BALL",
    "NEEDLE ARM",
    "SLACK OFF",
    "HYPER VOICE",
    "POISON FANG",
    "CRUSH CLAW",
    "BLAST BURN",
    "HYDRO CANNON",
    "METEOR MASH",
    "ASTONISH",
    "WEATHER BALL",
    "AROMATHERAPY",
    "FAKE TEARS",
    "AIR CUTTER",
    "OVERHEAT",
    "ODOR SLEUTH",
    "ROCK TOMB",
    "SILVER WIND",
    "METAL SOUND",
    "GRASSWHISTLE",
    "TICKLE",
    "COSMIC POWER",
    "WATER SPOUT",
    "SIGNAL BEAM",
    "SHADOW PUNCH",
    "EXTRASENSORY",
    "SKY UPPERCUT",
    "SAND TOMB",
    "SHEER COLD",
    "MUDDY WATER",
    "BULLET SEED",
    "AERIAL ACE",
    "ICICLE SPEAR",
    "IRON DEFENSE",
    "BLOCK",
    "HOWL",
    "DRAGON CLAW",
    "FRENZY PLANT",
    "BULK UP",
    "BOUNCE",
    "MUD SHOT",
    "POISON TAIL",
    "COVET",
    "VOLT TACKLE",
    "MAGICAL LEAF",
    "WATER SPORT",
    "CALM MIND",
    "LEAF BLADE",
    "DRAGON DANCE",
    "ROCK BLAST",
    "SHOCK WAVE",
    "WATER PULSE",
    "DOOM DESIRE",
    "PSYCHO BOOST",
]
POKEMON_ABILITIES = [
    "-------",
    "STENCH",
    "DRIZZLE",
    "SPEED BOOST",
    "BATTLE ARMOR",
    "STURDY",
    "DAMP",
    "LIMBER",
    "SAND VEIL",
    "STATIC",
    "VOLT ABSORB",
    "WATER ABSORB",
    "OBLIVIOUS",
    "CLOUD NINE",
    "COMPOUNDEYES",
    "INSOMNIA",
    "COLOR CHANGE",
    "IMMUNITY",
    "FLASH FIRE",
    "SHIELD DUST",
    "OWN TEMPO",
    "SUCTION CUPS",
    "INTIMIDATE",
    "SHADOW TAG",
    "ROUGH SKIN",
    "WONDER GUARD",
    "LEVITATE",
    "EFFECT SPORE",
    "SYNCHRONIZE",
    "CLEAR BODY",
    "NATURAL CURE",
    "LIGHTNINGROD",
    "SERENE GRACE",
    "SWIFT SWIM",
    "CHLOROPHYLL",
    "ILLUMINATE",
    "TRACE",
    "HUGE POWER",
    "POISON POINT",
    "INNER FOCUS",
    "MAGMA ARMOR",
    "WATER VEIL",
    "MAGNET PULL",
    "SOUNDPROOF",
    "RAIN DISH",
    "SAND STREAM",
    "PRESSURE",
    "THICK FAT",
    "EARLY BIRD",
    "FLAME BODY",
    "RUN AWAY",
    "KEEN EYE",
    "HYPER CUTTER",
    "PICKUP",
    "TRUANT",
    "HUSTLE",
    "CUTE CHARM",
    "PLUS",
    "MINUS",
    "FORECAST",
    "STICKY HOLD",
    "SHED SKIN",
    "GUTS",
    "MARVEL SCALE",
    "LIQUID OOZE",
    "OVERGROW",
    "BLAZE",
    "TORRENT",
    "SWARM",
    "ROCK HEAD",
    "DROUGHT",
    "ARENA TRAP",
    "VITAL SPIRIT",
    "WHITE SMOKE",
    "PURE POWER",
    "SHELL ARMOR",
    "CACOPHONY",
    "AIR LOCK"
]
POKEMON_M_OR_F_RATIOS = {
    0:   "100% M",
    31:  "87% M",
    63:  "75% M",
    89:  "65% M",
    127: "50% M",
    165: "65% F",
    191: "75% F",
    223: "87% F",
    254: "100% F",
    255: "None",
}
REVERSE_POKEMON_M_OR_F_RATIOS = {v: k for k, v in POKEMON_M_OR_F_RATIOS.items()}

POKEMON_FOLDERS = list(POKEMON_NAME_TO_ID.keys())
POKEMON_HATCH_PALETTE_EXTRACTION_PRIORITY = ["hatch_anim"]

TRAINER_REFLECTION_PALETTE_EXTRACTION_PRIORITY = ["reflection"]
TRAINER_UNDERWATER_PALETTE_EXTRACTION_PRIORITY = ["underwater"]
TRAINER_BATTLE_BACK_PALETTE_EXTRACTION_PRIORITY = ["battle_back"]
TRAINER_BATTLE_FRONT_PALETTE_EXTRACTION_PRIORITY = ["battle_front"]

SIMPLE_TRAINER_SPRITES = ["walking", "battle_front"]
SIMPLE_TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY = ["walking"]
SIMPLE_TRAINER_BATTLE_FRONT_PALETTE_EXTRACTION_PRIORITY = ["battle_front"]
SIMPLE_TRAINER_PALETTES = {
    "palette": SIMPLE_TRAINER_MAIN_PALETTE_EXTRACTION_PRIORITY,
    "palette_battle_front": SIMPLE_TRAINER_BATTLE_FRONT_PALETTE_EXTRACTION_PRIORITY
}

SPRITE_PIXEL_REFERENCE = {
    "sfront_anim": "front_anim",
    "sfront":      "front",
    "sback":       "back",
    "reflection":  "walking_running"
}

OBJECT_NEEDS_COMPRESSION = {
    "pokemon_front_anim":             True,
    "pokemon_front":                  True,
    "pokemon_back":                   True,
    "players_battle_front":           True,
    "trainer_battle_front":           True,
    "trainer_battle_front_1":         True,
    "trainer_battle_front_2":         True,
    "trainer_battle_front_3":         True,
    "pokemon_palette":                True,
    "pokemon_palette_shiny":          True,
    "players_palette_battle_back":    True,
    "players_palette_battle_front":   True,
    "trainer_palette_battle_front":   True,
    "trainer_palette_battle_front_1": True,
    "trainer_palette_battle_front_2": True,
    "trainer_palette_battle_front_3": True,
}

COMPLEX_SPRITES_LIST = [
    "players_walking_running",
    "players_bike",
    "players_mach_bike",
    "players_acro_bike",
    "players_surfing",
    "players_field_move",
    "players_underwater",
    "players_fishing",
    "players_watering",
    "players_decorating",
    "players_bike_vs_seeker",
    "players_battle_back_throw",
    "trainer_walking"
]

OVERWORLD_PALETTE_INFO: ObjectInfo = ObjectInfo(8, {
    "palette_ptr": PointerInfo(0, 4),
    "id":          PointerInfo(4, 2),
    "padding":     PointerInfo(6, 2)
})

OVERWORLD_SPRITE_OBJECT_INFO: ObjectInfo = ObjectInfo(36, {
    "starter_bytes":  PointerInfo(0, 2),
    "palette_id":     PointerInfo(2, 2),
    "second_pal_id":  PointerInfo(4, 2),
    "sprite_length":  PointerInfo(6, 2),
    "sprite_width":   PointerInfo(8, 2),
    "sprite_height":  PointerInfo(10, 2),
    "sprite_info":    PointerInfo(12, 1),
    "footprint_type": PointerInfo(13, 1),
    "distrib_ptr":    PointerInfo(16, 3),
    "size_draw_ptr":  PointerInfo(20, 3),
    "animation_ptr":  PointerInfo(24, 3),
    "sprites_ptr":    PointerInfo(28, 3),
    "ram_store_ptr":  PointerInfo(32, 3)
})

POKEMON_DATA_INFO: ObjectInfo = ObjectInfo(26, {
    "hp":             PointerInfo(0, 1),
    "atk":            PointerInfo(1, 1),
    "dfs":            PointerInfo(2, 1),
    "spatk":          PointerInfo(3, 1),
    "spdef":          PointerInfo(4, 1),
    "spd":            PointerInfo(5, 1),
    "type1":          PointerInfo(6, 1),
    "type2":          PointerInfo(7, 1),
    "catch_rate":     PointerInfo(8, 1),
    "base_exp":       PointerInfo(9, 1),
    "evs":            PointerInfo(10, 2),
    "item1":          PointerInfo(12, 2),
    "item2":          PointerInfo(14, 2),
    "gender_ratio":   PointerInfo(16, 1),
    "steps_to_hatch": PointerInfo(17, 1),
    "base_happiness": PointerInfo(18, 1),
    "growth_rate":    PointerInfo(19, 1),
    "egg_group1":     PointerInfo(20, 1),
    "egg_group2":     PointerInfo(21, 1),
    "ability1":       PointerInfo(22, 1),
    "ability2":       PointerInfo(23, 1),
    "run_rate":       PointerInfo(24, 1),
    "dex":            PointerInfo(25, 1),
})

VALID_ICON_PALETTES = {
    0: [
        98, 156, 131,
        131, 131, 115,
        189, 189, 189,
        255, 255, 255,
        189, 164, 65,
        246, 246, 41,
        213, 98, 65,
        246, 148, 41,
        139, 123, 255,
        98, 74, 205,
        238, 115, 156,
        255, 180, 164,
        164, 197, 255,
        106, 172, 156,
        98, 98, 90,
        65, 65, 65
    ],
    1: [
        98, 156, 131,
        115, 115, 115,
        189, 189, 189,
        255, 255, 255,
        123, 156, 74,
        156, 205, 74,
        148, 246, 74,
        238, 115, 156,
        246, 148, 246,
        189, 164, 90,
        246, 230, 41,
        246, 246, 172,
        213, 213, 106,
        230, 74, 41,
        98, 98, 90,
        65, 65, 65
    ],
    2: [
        98, 156, 131,
        123, 123, 123,
        189, 189, 180,
        255, 255, 255,
        115, 115, 205,
        164, 172, 246,
        180, 131, 90,
        238, 197, 139,
        197, 172, 41,
        246, 246, 41,
        246, 98, 82,
        148, 123, 205,
        197, 164, 205,
        189, 41, 156,
        98, 98, 90,
        65, 65, 65
    ]
}

VALID_FOOTPRINT_PALETTE = [
    0, 0, 0,
    255, 255, 255
]

VALID_OVERWORLD_UNDERWATER_PALETTE = [
    115, 197, 164,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    98, 123, 156,
    74, 90, 131,
    49, 65, 106,
    24, 41, 82,
    131, 164, 197
]

VALID_OVERWORLD_PALETTE = [
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    255, 255, 255,
    0, 0, 0
]

VALID_REFLECTION_PALETTE = [
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    255, 255, 255
]

VALID_WEAK_OVERWORLD_PALETTE = [
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    -1, -1, -1,
    0, 0, 0
]

VALID_UNOWN_PALETTE = [
    205, 205, 172,
    -1,  -1,  -1,
    -1,  -1,  -1,
    -1,  -1,  -1,
    222, 222, 222,
    255, 255, 255,
    16,  16,  16,
    164, 164, 164,
    115, 115, 115,
    82,  82,  82
]

VALID_UNOWN_SHINY_PALETTE = [
    205, 205, 172,
    -1,  -1,  -1,
    -1,  -1,  -1,
    -1,  -1,  -1,
    98,  205, 255,
    255, 255, 255,
    16,  16,  16,
    41,  115, 255,
    32,  65,  156,
    49,  57,  106
]


class DataAddressInfo():
    crc32: int = 0
    original_addresses: dict[str, int] = {}
    ap_addresses: dict[str, int] = {}
    data_address_beginning: int = 0
    data_address_end: int = 0

    def __init__(self, _crc32, _original_addresses, _ap_addresses, _data_address_beginning, _data_address_end):
        self.crc32 = _crc32
        self.original_addresses = _original_addresses
        self.ap_addresses = _ap_addresses
        self.data_address_beginning = _data_address_beginning
        self.data_address_end = _data_address_end


class FolderObjectInfo():
    name: str = ""
    key: str = ""
    folders: list[str] = []
    sprites: list[str] = []
    palettes: dict[str, list[str]] = {}

    def __init__(self, _key, _folders, _sprites, _palettes, _name = ""):
        self.key = _key
        self.folders = _folders
        self.sprites = _sprites
        self.palettes = _palettes
        self.name = _name


class OverworldSpriteSize():
    width: int = 0
    height: int = 0
    data: str = ""
    distrib: str = ""

    def __init__(self, _width, _height, _data, _distrib = ""):
        self.width = _width
        self.height = _height
        self.data = _data
        self.distrib = _distrib


class SpriteRequirement():
    frames: list[int] = []
    width: int = 0
    height: int = 0
    palette: list[int] = []
    palettes: dict[int, list[int]] = {}
    palette_number: int = 1
    palette_size: int = 0
    internal_frames: int = 0
    palette_per_frame: bool = False
    fields = ["frames", "width", "height", "palette", "palettes", "palette_number", "palette_size", "internal_frames",
              "palette_per_frame"]

    def __init__(self, _frames = [], _width = 0, _height = 0, _palette = [], _palettes = {}, _palette_number = 1,
                 _palette_size = 0,_internal_frames = 0, _palette_per_frame = False):
        self.frames = _frames
        self.width = _width
        self.height = _height
        self.palette = _palette
        self.palettes = _palettes
        self.palette_number = _palette_number
        self.palette_size = _palette_size
        self.internal_frames = _internal_frames
        self.palette_per_frame = _palette_per_frame

    def set(self, _field: str, _value):
        if _field == "frames":            self.frames = _value
        if _field == "width":             self.width = _value
        if _field == "height":            self.height = _value
        if _field == "palette":           self.palette = _value
        if _field == "palettes":          self.palettes = _value
        if _field == "palette_number":    self.palette_number = _value
        if _field == "palette_size":      self.palette_size = _value
        if _field == "internal_frames":   self.internal_frames = _value
        if _field == "palette_per_frame": self.palette_per_frame = _value

    def get(self, _field: str):
        if _field == "frames":            return self.frames
        if _field == "width":             return self.width
        if _field == "height":            return self.height
        if _field == "palette":           return self.palette
        if _field == "palettes":          return self.palettes
        if _field == "palette_number":    return self.palette_number
        if _field == "palette_size":      return self.palette_size
        if _field == "internal_frames":   return self.internal_frames
        if _field == "palette_per_frame": return self.palette_per_frame
        return 0

    def is_field_empty(self, _field: str):
        if _field == "frames":            return len(self.frames) == 0
        if _field == "width":             return self.width == 0
        if _field == "height":            return self.height == 0
        if _field == "palette":           return len(self.palette) == 0
        if _field == "palettes":          return len(self.palettes) == 0
        if _field == "palette_number":    return self.palette_number == 1
        if _field == "palette_size":      return self.palette_size == 0
        if _field == "internal_frames":   return self.internal_frames == 0
        if _field == "palette_per_frame": return self.palette_per_frame == False
        return True

    def __add__(self, _other):
        output = copy.deepcopy(self)
        for field in self.fields:
            if not _other.is_field_empty(field):
                output.set(field, _other.get(field))
        return output


class PokemonMoveInfo():
    move: str = ""
    level: int = 0

    def __init__(self, _move, _level):
        self.move = _move
        self.level = _level


class PokemonData():
    hp: int = -1
    atk: int = -1
    dfs: int = -1
    spatk: int = -1
    spdef: int = -1
    spd: int = -1
    type1: int = -1
    type2: int = -1
    catch_rate: int = -1
    base_exp: int = -1
    evs: int = -1
    item1: int = -1
    item2: int = -1
    gender_ratio: int = -1
    steps_to_hatch: int = -1
    base_happiness: int = -1
    growth_rate: int = -1
    egg_group1: int = -1
    egg_group2: int = -1
    ability1: int = -1
    ability2: int = -1
    run_rate: int = -1
    dex: int = -1
    move_pool: list[PokemonMoveInfo] = []
    fields: list[str] = ["hp", "atk", "dfs", "spatk", "spdef", "spd", "type1", "type2", "catch_rate", "base_exp",
                         "evs", "item1", "item2", "gender_ratio", "steps_to_hatch", "base_happiness", "growth_rate",
                         "egg_group1", "egg_group2", "ability1", "ability2", "run_rate", "dex", "move_pool"]

    def get_stat(self, _field: str) -> int:
        if _field == "hp": return self.hp
        if _field == "atk": return self.atk
        if _field == "dfs": return self.dfs
        if _field == "spatk": return self.spatk
        if _field == "spdef": return self.spdef
        if _field == "spd": return self.spd
        if _field == "type1": return self.type1
        if _field == "type2": return self.type2
        if _field == "catch_rate": return self.catch_rate
        if _field == "base_exp": return self.base_exp
        if _field == "evs": return self.evs
        if _field == "item1": return self.item1
        if _field == "item2": return self.item2
        if _field == "gender_ratio": return self.gender_ratio
        if _field == "steps_to_hatch": return self.steps_to_hatch
        if _field == "base_happiness": return self.base_happiness
        if _field == "growth_rate": return self.growth_rate
        if _field == "egg_group1": return self.egg_group1
        if _field == "egg_group2": return self.egg_group2
        if _field == "ability1": return self.ability1
        if _field == "ability2": return self.ability2
        if _field == "run_rate": return self.run_rate
        if _field == "dex": return self.dex
        return 0

    def get_move_pool(self, _field: str) -> list[PokemonMoveInfo]:
        if _field == "move_pool": return self.move_pool
        return []

    def is_field_empty(self, _field: str):
        if _field == "move_pool": return len(self.get_move_pool(_field)) == 0
        return self.get_stat(_field) == -1

    def set(self, _field: str, _value: int = 0, _value_move_pool: list[PokemonMoveInfo] = []):
        if _field == "hp": self.hp = _value
        if _field == "atk": self.atk = _value
        if _field == "dfs": self.dfs = _value
        if _field == "spatk": self.spatk = _value
        if _field == "spdef": self.spdef = _value
        if _field == "spd": self.spd = _value
        if _field == "type1": self.type1 = _value
        if _field == "type2": self.type2 = _value
        if _field == "catch_rate": self.catch_rate = _value
        if _field == "base_exp": self.base_exp = _value
        if _field == "evs": self.evs = _value
        if _field == "item1": self.item1 = _value
        if _field == "item2": self.item2 = _value
        if _field == "gender_ratio": self.gender_ratio = _value
        if _field == "steps_to_hatch": self.steps_to_hatch = _value
        if _field == "base_happiness": self.base_happiness = _value
        if _field == "growth_rate": self.growth_rate = _value
        if _field == "egg_group1": self.egg_group1 = _value
        if _field == "egg_group2": self.egg_group2 = _value
        if _field == "ability1": self.ability1 = _value
        if _field == "ability2": self.ability2 = _value
        if _field == "run_rate": self.run_rate = _value
        if _field == "dex": self.dex = _value
        if _field == "move_pool": self.move_pool = _value_move_pool


class SafePokemonData():
    hp: str = ""
    atk: str = ""
    dfs: str = ""
    spatk: str = ""
    spdef: str = ""
    spd: str = ""
    type1: str = ""
    type2: str = ""
    catch_rate: str = ""
    base_exp: str = ""
    evs: str = ""
    item1: str = ""
    item2: str = ""
    gender_ratio: str = ""
    steps_to_hatch: str = ""
    base_happiness: str = ""
    growth_rate: str = ""
    egg_group1: str = ""
    egg_group2: str = ""
    ability1: str = ""
    ability2: str = ""
    run_rate: str = ""
    dex: str = ""
    move_pool: str = ""
    fields: list[str] = ["hp", "atk", "dfs", "spatk", "spdef", "spd", "type1", "type2", "catch_rate", "base_exp",
                         "evs", "item1", "item2", "gender_ratio", "steps_to_hatch", "base_happiness", "growth_rate",
                         "egg_group1", "egg_group2", "ability1", "ability2", "run_rate", "dex", "move_pool"]

    def get(self, _field: str) -> str:
        if _field == "hp": return self.hp
        if _field == "atk": return self.atk
        if _field == "dfs": return self.dfs
        if _field == "spatk": return self.spatk
        if _field == "spdef": return self.spdef
        if _field == "spd": return self.spd
        if _field == "type1": return self.type1
        if _field == "type2": return self.type2
        if _field == "catch_rate": return self.catch_rate
        if _field == "base_exp": return self.base_exp
        if _field == "evs": return self.evs
        if _field == "item1": return self.item1
        if _field == "item2": return self.item2
        if _field == "gender_ratio": return self.gender_ratio
        if _field == "steps_to_hatch": return self.steps_to_hatch
        if _field == "base_happiness": return self.base_happiness
        if _field == "growth_rate": return self.growth_rate
        if _field == "egg_group1": return self.egg_group1
        if _field == "egg_group2": return self.egg_group2
        if _field == "ability1": return self.ability1
        if _field == "ability2": return self.ability2
        if _field == "run_rate": return self.run_rate
        if _field == "dex": return self.dex
        if _field == "move_pool": return self.move_pool
        return ""

    def set(self, _field: str, _value: str = ""):
        if _field == "hp": self.hp = _value
        if _field == "atk": self.atk = _value
        if _field == "dfs": self.dfs = _value
        if _field == "spatk": self.spatk = _value
        if _field == "spdef": self.spdef = _value
        if _field == "spd": self.spd = _value
        if _field == "type1": self.type1 = _value
        if _field == "type2": self.type2 = _value
        if _field == "catch_rate": self.catch_rate = _value
        if _field == "base_exp": self.base_exp = _value
        if _field == "evs": self.evs = _value
        if _field == "item1": self.item1 = _value
        if _field == "item2": self.item2 = _value
        if _field == "gender_ratio": self.gender_ratio = _value
        if _field == "steps_to_hatch": self.steps_to_hatch = _value
        if _field == "base_happiness": self.base_happiness = _value
        if _field == "growth_rate": self.growth_rate = _value
        if _field == "egg_group1": self.egg_group1 = _value
        if _field == "egg_group2": self.egg_group2 = _value
        if _field == "ability1": self.ability1 = _value
        if _field == "ability2": self.ability2 = _value
        if _field == "run_rate": self.run_rate = _value
        if _field == "dex": self.dex = _value
        if _field == "move_pool": self.move_pool = _value