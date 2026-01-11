from ..Connection import Connection
from ..Requirements import *
from ..FFTLocation import FFTLocation, LocationNames, RareBattleLocation

from ..regions.Lionel import *
from ..regions.Lesalia import Zirekile
from ..regions.Murond import Goug, DeepDungeon

Zaland.connections = [
    Connection(Zirekile, [HasLesaliaPass]),
    Connection(BariausHill)
]

Zaland.locations = [
    FFTLocation(LocationNames.ZALAND_STORY, battle_level=5)
]

BariausHill.connections = [
    Connection(Zaland),
    Connection(Lionel)
]

BariausHill.locations = [
    FFTLocation(LocationNames.BARIAUS_HILL_STORY, battle_level=5),
    FFTLocation(LocationNames.BARIAUS_HILL_SHOP, battle_level=5),
    RareBattleLocation(LocationNames.BARIAUS_HILL_RARE, battle_level=8)
]

Lionel.connections = [
    Connection(BariausHill),
    Connection(Zigolis),
    Connection(BariausValley)
]

Lionel.locations = [
    FFTLocation(LocationNames.LIONEL_1_STORY, battle_level=7),
    FFTLocation(LocationNames.LIONEL_2_STORY, battle_level=7),
    FFTLocation(LocationNames.LIONEL_SHOP, battle_level=7)
]

BariausValley.connections = [
    Connection(Lionel),
    Connection(Golgorand),
    Connection(Warjilis)
]

BariausValley.locations = [
    FFTLocation(LocationNames.BARIAUS_VALLEY_STORY, battle_level=6),
    FFTLocation(LocationNames.BARIAUS_VALLEY_SHOP, battle_level=6),
    FFTLocation(LocationNames.AGRIAS_RECRUIT, battle_level=6),
    RareBattleLocation(LocationNames.BARIAUS_VALLEY_RARE, battle_level=8)
]

Golgorand.connections = [
    Connection(BariausValley)
]

Golgorand.locations = [
    FFTLocation(LocationNames.GOLGORAND_STORY, battle_level=7)
]

Warjilis.connections = [
    Connection(BariausValley),
    Connection(DeepDungeon, [HasMurondPass])
]

Zigolis.connections = [
    Connection(Lionel),
    Connection(Goug, [HasMurondPass])
]

Zigolis.locations = [
    FFTLocation(LocationNames.ZIGOLIS_STORY, battle_level=6),
    RareBattleLocation(LocationNames.ZIGOLIS_RARE, battle_level=8)
]
