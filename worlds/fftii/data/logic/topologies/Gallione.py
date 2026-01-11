from ..Connection import Connection
from ..Requirements import *
from ..FFTLocation import FFTLocation, RareBattleLocation, LocationNames

from ..regions.Gallione import *
from ..regions.Fovoham import Fovoham
from ..regions.Lesalia import Zeklaus, Araguay
from ..regions.Murond import Murond, Orbonne

Gariland.connections = [
    Connection(Mandalia),
    Connection(Sweegy),
    Connection(Lenalia),
    Connection(Murond, [HasMurondPass])
]

Gariland.locations = [
    FFTLocation(LocationNames.GARILAND_STORY, battle_level=0)
]

Mandalia.connections = [
    Connection(Gariland),
    Connection(ThievesFort),
    Connection(Igros)
]

Mandalia.locations = [
    FFTLocation(LocationNames.MANDALIA_STORY, battle_level=0),
    FFTLocation(LocationNames.MANDALIA_SHOP, battle_level=0),
    RareBattleLocation(LocationNames.MANDALIA_RARE, battle_level=8)
]

Igros.connections = [
    Connection(Mandalia),
    Connection(Zeakden)
]

Igros.locations = [
    FFTLocation(LocationNames.IGROS_STORY, battle_level=14)
]

Sweegy.connections = [
    Connection(Gariland),
    Connection(Dorter)
]

Sweegy.locations = [
    FFTLocation(LocationNames.SWEEGY_STORY, battle_level=1),
    RareBattleLocation(LocationNames.SWEEGY_RARE, battle_level=8)
]

Dorter.connections = [
    Connection(Sweegy),
    Connection(Zeklaus, [HasLesaliaPass]),
    Connection(Araguay, [HasLesaliaPass]),
    Connection(Orbonne, [HasMurondPass])
]

Dorter.locations = [
    FFTLocation(LocationNames.DORTER_1_STORY, battle_level=1),
    FFTLocation(LocationNames.DORTER_2_STORY, battle_level=4)
]

ThievesFort.connections = [
    Connection(Mandalia)
]

ThievesFort.locations = [
    FFTLocation(LocationNames.THIEVES_FORT_STORY, battle_level=2)
]

Lenalia.connections = [
    Connection(Gariland),
    Connection(Fovoham, [HasFovohamPass])
]

Lenalia.locations = [
    FFTLocation(LocationNames.LENALIA_STORY, battle_level=2),
    FFTLocation(LocationNames.LENALIA_SHOP, battle_level=2),
    RareBattleLocation(LocationNames.LENALIA_RARE, battle_level=8)

]

Zeakden.connections = [
    Connection(Igros),
    Connection(Fovoham, [HasFovohamPass])
]

Zeakden.locations = [
    FFTLocation(LocationNames.ZEAKDEN_STORY, battle_level=3),
    FFTLocation(LocationNames.ZEAKDEN_SHOP, battle_level=3),
    FFTLocation(LocationNames.RAMZA_CHAPTER_2_UNLOCK, battle_level=3),
    FFTLocation(LocationNames.RAD_RECRUIT, battle_level=3),
    FFTLocation(LocationNames.ALICIA_RECRUIT, battle_level=3),
    FFTLocation(LocationNames.LAVIAN_RECRUIT, battle_level=3)
]