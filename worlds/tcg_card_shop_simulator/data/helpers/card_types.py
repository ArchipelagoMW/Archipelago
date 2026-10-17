from dataclasses import dataclass
from enum import Enum, IntEnum, StrEnum


class Rarity(IntEnum):
    COMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 4


class Expansion(IntEnum):
    TETRAMON = 0
    DESTINY = 1


class Border(IntEnum):
    BASE = 0
    FIRST_EDITION = 1
    SILVER = 2
    GOLD = 3
    EX = 4
    FULL_ART = 5


class Foil(IntEnum):
    NON_FOIL = 0
    FOIL = 1



class CardAction(StrEnum):
    OPEN = "Open"
    SELL = "Sell"
    GRADE = "Grade"


class Difficulty(IntEnum):
    DISABLED = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3
    IMPOSSIBLE = 4


class CardSpecies(IntEnum):
    PIGNI = 1
    BURPIG = 2
    INFERHOG = 3
    BLAZOAR = 4
    KIDSUNE = 5
    BONFIOX = 6
    HONOBI = 7
    KYUENBI = 8
    NANOMITE = 9
    DECIMITE = 10
    MEGANITE = 11
    GIGANITE = 12
    SAPOLING = 13
    FORUSH = 14
    TIMBRO = 15
    MAMMOTREE = 16
    MINSTAR = 17
    TRICKSTAR = 18
    PRINCESTAR = 19
    KINGSTAR = 20
    SHELLOW = 21
    CLAMIGO = 22
    AQUARIFF = 23
    FISTRONK = 24
    WURMGLE = 25
    PUPAZZ = 26
    MOTHINI = 27
    ROYALAMA = 28
    NOCTI = 29
    LUNIGHT = 30
    VAMPICANT = 31
    DRACUNIX = 32
    MINOTOS = 33
    DRILCEROS = 34
    GRIZZAW = 35
    JELICLEEN = 36
    WISPO = 37
    MUMMOG = 38
    HELIO = 39
    PIXY = 40
    FLORY = 41
    MAGNORIA = 42
    WERBOO = 43
    FLAMI = 44
    ANGEZ = 45
    MOSKIT = 46
    KYRONE = 47
    TWOFROST = 48
    THREEZE = 49
    HYDROID = 50
    DRAKON = 51
    BOGON = 52
    HYDRON = 53
    RAIZON = 54
    TORTUGOR = 55
    LUPUP = 56
    LUPHIRE = 57
    LUCINDER = 58
    LUCADENCE = 59
    GUPI = 60
    SHARFIN = 61
    GILGABASS = 62
    JIGAJAWR = 63
    BATRANG = 64
    DUSKO = 65
    WOLGIN = 66
    JACKTERN = 67
    TETRON = 68
    RAXX = 69
    GANNON = 70
    GIGATRON_X = 71
    CLAWOP = 72
    CLAWDOS = 73
    CLAWAKEN = 74
    CLAWCIFEAR = 75
    SUNFLORK = 76
    SCARLIOS = 77
    SCARKGORUS = 78
    CROBIB = 79
    CROSILISK = 80
    CRORATHIAN = 81
    NIMBLIS = 82
    NIMBOCULO = 83
    NIMBUSTRIKE = 84
    ESMERI = 85
    ESMEROCK = 86
    ESMERDIOS = 87
    LITSPIRE = 88
    VOLTREX = 89
    CRABLOX = 90
    CLAWVENGER = 91
    FLAMBROLLY = 92
    LUMIE = 93
    SEEDANT = 94
    BUDWING = 95
    BUZZEED = 96
    BEAKAI = 97
    TALONTSU = 98
    TALONIKA = 99
    TALONRYU = 100
    KATARYU = 101
    KATENGU = 102
    MUFFLIN = 103
    MUFFLEUR = 104
    MUFFLIMAX = 105
    ANGUIFISH = 106
    AMNESHARK = 107
    AMNESILLA = 108
    FRIZARD = 109
    GEKOFLARE = 110
    TERRADRAKON = 111
    FLAMCHIK = 112
    PYROPECK = 113
    POSEIA = 114
    POSTEED = 115
    POSEIGON = 116
    POSEIDRAKE = 117
    SLUDGLOP = 118
    SLUDGETOX = 119
    TOXIGOOP = 120
    TOXIMUCK = 121


SPECIES_NAMES: dict[CardSpecies, str] = {
    CardSpecies.PIGNI: 'Pigni',
    CardSpecies.BURPIG: 'Burpig',
    CardSpecies.INFERHOG: 'Inferhog',
    CardSpecies.BLAZOAR: 'Blazoar',
    CardSpecies.KIDSUNE: 'Kidsune',
    CardSpecies.BONFIOX: 'Bonfiox',
    CardSpecies.HONOBI: 'Honobi',
    CardSpecies.KYUENBI: 'Kyuenbi',
    CardSpecies.NANOMITE: 'Nanomite',
    CardSpecies.DECIMITE: 'Decimite',
    CardSpecies.MEGANITE: 'Meganite',
    CardSpecies.GIGANITE: 'Giganite',
    CardSpecies.SAPOLING: 'Sapoling',
    CardSpecies.FORUSH: 'Forush',
    CardSpecies.TIMBRO: 'Timbro',
    CardSpecies.MAMMOTREE: 'Mammotree',
    CardSpecies.MINSTAR: 'Minstar',
    CardSpecies.TRICKSTAR: 'Trickstar',
    CardSpecies.PRINCESTAR: 'Princestar',
    CardSpecies.KINGSTAR: 'Kingstar',
    CardSpecies.SHELLOW: 'Shellow',
    CardSpecies.CLAMIGO: 'Clamigo',
    CardSpecies.AQUARIFF: 'Aquariff',
    CardSpecies.FISTRONK: 'Fistronk',
    CardSpecies.WURMGLE: 'Wurmgle',
    CardSpecies.PUPAZZ: 'Pupazz',
    CardSpecies.MOTHINI: 'Mothini',
    CardSpecies.ROYALAMA: 'Royalama',
    CardSpecies.NOCTI: 'Nocti',
    CardSpecies.LUNIGHT: 'Lunight',
    CardSpecies.VAMPICANT: 'Vampicant',
    CardSpecies.DRACUNIX: 'Dracunix',
    CardSpecies.MINOTOS: 'Minotos',
    CardSpecies.DRILCEROS: 'Drilceros',
    CardSpecies.GRIZZAW: 'Grizzaw',
    CardSpecies.JELICLEEN: 'Jelicleen',
    CardSpecies.WISPO: 'Wispo',
    CardSpecies.MUMMOG: 'Mummog',
    CardSpecies.HELIO: 'Helio',
    CardSpecies.PIXY: 'Pixy',
    CardSpecies.FLORY: 'Flory',
    CardSpecies.MAGNORIA: 'Magnoria',
    CardSpecies.WERBOO: 'Werboo',
    CardSpecies.FLAMI: 'Flami',
    CardSpecies.ANGEZ: 'Angez',
    CardSpecies.MOSKIT: 'Moskit',
    CardSpecies.KYRONE: 'Kyrone',
    CardSpecies.TWOFROST: 'Twofrost',
    CardSpecies.THREEZE: 'Threeze',
    CardSpecies.HYDROID: 'Hydroid',
    CardSpecies.DRAKON: 'Drakon',
    CardSpecies.BOGON: 'Bogon',
    CardSpecies.HYDRON: 'Hydron',
    CardSpecies.RAIZON: 'Raizon',
    CardSpecies.TORTUGOR: 'Tortugor',
    CardSpecies.LUPUP: 'Lupup',
    CardSpecies.LUPHIRE: 'Luphire',
    CardSpecies.LUCINDER: 'Lucinder',
    CardSpecies.LUCADENCE: 'Lucadence',
    CardSpecies.GUPI: 'Gupi',
    CardSpecies.SHARFIN: 'Sharfin',
    CardSpecies.GILGABASS: 'Gilgabass',
    CardSpecies.JIGAJAWR: 'Jigajawr',
    CardSpecies.BATRANG: 'Batrang',
    CardSpecies.DUSKO: 'Dusko',
    CardSpecies.WOLGIN: 'Wolgin',
    CardSpecies.JACKTERN: 'Jacktern',
    CardSpecies.TETRON: 'Tetron',
    CardSpecies.RAXX: 'Raxx',
    CardSpecies.GANNON: 'Gannon',
    CardSpecies.GIGATRON_X: 'GigatronX',
    CardSpecies.CLAWOP: 'Clawop',
    CardSpecies.CLAWDOS: 'Clawdos',
    CardSpecies.CLAWAKEN: 'Clawaken',
    CardSpecies.CLAWCIFEAR: 'Clawcifear',
    CardSpecies.SUNFLORK: 'Sunflork',
    CardSpecies.SCARLIOS: 'Scarlios',
    CardSpecies.SCARKGORUS: 'Scarkgorus',
    CardSpecies.CROBIB: 'Crobib',
    CardSpecies.CROSILISK: 'Crosilisk',
    CardSpecies.CRORATHIAN: 'Crorathian',
    CardSpecies.NIMBLIS: 'Nimblis',
    CardSpecies.NIMBOCULO: 'Nimboculo',
    CardSpecies.NIMBUSTRIKE: 'Nimbustrike',
    CardSpecies.ESMERI: 'Esmeri',
    CardSpecies.ESMEROCK: 'Esmerock',
    CardSpecies.ESMERDIOS: 'Esmerdios',
    CardSpecies.LITSPIRE: 'Litspire',
    CardSpecies.VOLTREX: 'Voltrex',
    CardSpecies.CRABLOX: 'Crablox',
    CardSpecies.CLAWVENGER: 'Clawvenger',
    CardSpecies.FLAMBROLLY: 'Flambrolly',
    CardSpecies.LUMIE: 'Lumie',
    CardSpecies.SEEDANT: 'Seedant',
    CardSpecies.BUDWING: 'Budwing',
    CardSpecies.BUZZEED: 'Buzzeed',
    CardSpecies.BEAKAI: 'Beakai',
    CardSpecies.TALONTSU: 'Talontsu',
    CardSpecies.TALONIKA: 'Talonika',
    CardSpecies.TALONRYU: 'Talonryu',
    CardSpecies.KATARYU: 'Kataryu',
    CardSpecies.KATENGU: 'Katengu',
    CardSpecies.MUFFLIN: 'Mufflin',
    CardSpecies.MUFFLEUR: 'Muffleur',
    CardSpecies.MUFFLIMAX: 'Mufflimax',
    CardSpecies.ANGUIFISH: 'Anguifish',
    CardSpecies.AMNESHARK: 'Amneshark',
    CardSpecies.AMNESILLA: 'Amnesilla',
    CardSpecies.FRIZARD: 'Frizard',
    CardSpecies.GEKOFLARE: 'Gekoflare',
    CardSpecies.TERRADRAKON: 'Terradrakon',
    CardSpecies.FLAMCHIK: 'Flamchik',
    CardSpecies.PYROPECK: 'Pyropeck',
    CardSpecies.POSEIA: 'Poseia',
    CardSpecies.POSTEED: 'Posteed',
    CardSpecies.POSEIGON: 'Poseigon',
    CardSpecies.POSEIDRAKE: 'Poseidrake',
    CardSpecies.SLUDGLOP: 'Sludglop',
    CardSpecies.SLUDGETOX: 'Sludgetox',
    CardSpecies.TOXIGOOP: 'Toxigoop',
    CardSpecies.TOXIMUCK: 'Toximuck',
}

SPECIES_RARITIES: dict[CardSpecies, Rarity] = {
    CardSpecies.PIGNI: Rarity.COMMON,
    CardSpecies.BURPIG: Rarity.RARE,
    CardSpecies.INFERHOG: Rarity.EPIC,
    CardSpecies.BLAZOAR: Rarity.LEGENDARY,
    CardSpecies.KIDSUNE: Rarity.COMMON,
    CardSpecies.BONFIOX: Rarity.RARE,
    CardSpecies.HONOBI: Rarity.EPIC,
    CardSpecies.KYUENBI: Rarity.LEGENDARY,
    CardSpecies.NANOMITE: Rarity.COMMON,
    CardSpecies.DECIMITE: Rarity.RARE,
    CardSpecies.MEGANITE: Rarity.EPIC,
    CardSpecies.GIGANITE: Rarity.LEGENDARY,
    CardSpecies.SAPOLING: Rarity.COMMON,
    CardSpecies.FORUSH: Rarity.RARE,
    CardSpecies.TIMBRO: Rarity.EPIC,
    CardSpecies.MAMMOTREE: Rarity.LEGENDARY,
    CardSpecies.MINSTAR: Rarity.COMMON,
    CardSpecies.TRICKSTAR: Rarity.RARE,
    CardSpecies.PRINCESTAR: Rarity.EPIC,
    CardSpecies.KINGSTAR: Rarity.LEGENDARY,
    CardSpecies.SHELLOW: Rarity.COMMON,
    CardSpecies.CLAMIGO: Rarity.RARE,
    CardSpecies.AQUARIFF: Rarity.EPIC,
    CardSpecies.FISTRONK: Rarity.LEGENDARY,
    CardSpecies.WURMGLE: Rarity.COMMON,
    CardSpecies.PUPAZZ: Rarity.RARE,
    CardSpecies.MOTHINI: Rarity.EPIC,
    CardSpecies.ROYALAMA: Rarity.LEGENDARY,
    CardSpecies.NOCTI: Rarity.COMMON,
    CardSpecies.LUNIGHT: Rarity.RARE,
    CardSpecies.VAMPICANT: Rarity.EPIC,
    CardSpecies.DRACUNIX: Rarity.LEGENDARY,
    CardSpecies.MINOTOS: Rarity.RARE,
    CardSpecies.DRILCEROS: Rarity.EPIC,
    CardSpecies.GRIZZAW: Rarity.EPIC,
    CardSpecies.JELICLEEN: Rarity.RARE,
    CardSpecies.WISPO: Rarity.RARE,
    CardSpecies.MUMMOG: Rarity.RARE,
    CardSpecies.HELIO: Rarity.COMMON,
    CardSpecies.PIXY: Rarity.RARE,
    CardSpecies.FLORY: Rarity.EPIC,
    CardSpecies.MAGNORIA: Rarity.LEGENDARY,
    CardSpecies.WERBOO: Rarity.COMMON,
    CardSpecies.FLAMI: Rarity.COMMON,
    CardSpecies.ANGEZ: Rarity.RARE,
    CardSpecies.MOSKIT: Rarity.EPIC,
    CardSpecies.KYRONE: Rarity.COMMON,
    CardSpecies.TWOFROST: Rarity.RARE,
    CardSpecies.THREEZE: Rarity.EPIC,
    CardSpecies.HYDROID: Rarity.LEGENDARY,
    CardSpecies.DRAKON: Rarity.LEGENDARY,
    CardSpecies.BOGON: Rarity.LEGENDARY,
    CardSpecies.HYDRON: Rarity.LEGENDARY,
    CardSpecies.RAIZON: Rarity.LEGENDARY,
    CardSpecies.TORTUGOR: Rarity.EPIC,
    CardSpecies.LUPUP: Rarity.COMMON,
    CardSpecies.LUPHIRE: Rarity.RARE,
    CardSpecies.LUCINDER: Rarity.EPIC,
    CardSpecies.LUCADENCE: Rarity.LEGENDARY,
    CardSpecies.GUPI: Rarity.COMMON,
    CardSpecies.SHARFIN: Rarity.RARE,
    CardSpecies.GILGABASS: Rarity.EPIC,
    CardSpecies.JIGAJAWR: Rarity.LEGENDARY,
    CardSpecies.BATRANG: Rarity.COMMON,
    CardSpecies.DUSKO: Rarity.RARE,
    CardSpecies.WOLGIN: Rarity.EPIC,
    CardSpecies.JACKTERN: Rarity.LEGENDARY,
    CardSpecies.TETRON: Rarity.COMMON,
    CardSpecies.RAXX: Rarity.RARE,
    CardSpecies.GANNON: Rarity.EPIC,
    CardSpecies.GIGATRON_X: Rarity.LEGENDARY,
    CardSpecies.CLAWOP: Rarity.COMMON,
    CardSpecies.CLAWDOS: Rarity.RARE,
    CardSpecies.CLAWAKEN: Rarity.EPIC,
    CardSpecies.CLAWCIFEAR: Rarity.LEGENDARY,
    CardSpecies.SUNFLORK: Rarity.COMMON,
    CardSpecies.SCARLIOS: Rarity.RARE,
    CardSpecies.SCARKGORUS: Rarity.EPIC,
    CardSpecies.CROBIB: Rarity.COMMON,
    CardSpecies.CROSILISK: Rarity.RARE,
    CardSpecies.CRORATHIAN: Rarity.EPIC,
    CardSpecies.NIMBLIS: Rarity.COMMON,
    CardSpecies.NIMBOCULO: Rarity.RARE,
    CardSpecies.NIMBUSTRIKE: Rarity.EPIC,
    CardSpecies.ESMERI: Rarity.COMMON,
    CardSpecies.ESMEROCK: Rarity.RARE,
    CardSpecies.ESMERDIOS: Rarity.EPIC,
    CardSpecies.LITSPIRE: Rarity.EPIC,
    CardSpecies.VOLTREX: Rarity.LEGENDARY,
    CardSpecies.CRABLOX: Rarity.RARE,
    CardSpecies.CLAWVENGER: Rarity.EPIC,
    CardSpecies.FLAMBROLLY: Rarity.LEGENDARY,
    CardSpecies.LUMIE: Rarity.RARE,
    CardSpecies.SEEDANT: Rarity.COMMON,
    CardSpecies.BUDWING: Rarity.RARE,
    CardSpecies.BUZZEED: Rarity.EPIC,
    CardSpecies.BEAKAI: Rarity.RARE,
    CardSpecies.TALONTSU: Rarity.EPIC,
    CardSpecies.TALONIKA: Rarity.EPIC,
    CardSpecies.TALONRYU: Rarity.LEGENDARY,
    CardSpecies.KATARYU: Rarity.EPIC,
    CardSpecies.KATENGU: Rarity.LEGENDARY,
    CardSpecies.MUFFLIN: Rarity.COMMON,
    CardSpecies.MUFFLEUR: Rarity.RARE,
    CardSpecies.MUFFLIMAX: Rarity.EPIC,
    CardSpecies.ANGUIFISH: Rarity.COMMON,
    CardSpecies.AMNESHARK: Rarity.RARE,
    CardSpecies.AMNESILLA: Rarity.EPIC,
    CardSpecies.FRIZARD: Rarity.RARE,
    CardSpecies.GEKOFLARE: Rarity.EPIC,
    CardSpecies.TERRADRAKON: Rarity.LEGENDARY,
    CardSpecies.FLAMCHIK: Rarity.COMMON,
    CardSpecies.PYROPECK: Rarity.RARE,
    CardSpecies.POSEIA: Rarity.COMMON,
    CardSpecies.POSTEED: Rarity.RARE,
    CardSpecies.POSEIGON: Rarity.EPIC,
    CardSpecies.POSEIDRAKE: Rarity.LEGENDARY,
    CardSpecies.SLUDGLOP: Rarity.COMMON,
    CardSpecies.SLUDGETOX: Rarity.RARE,
    CardSpecies.TOXIGOOP: Rarity.EPIC,
    CardSpecies.TOXIMUCK: Rarity.LEGENDARY,
}