from ..Connection import Connection
from ..Requirements import *
from ..FFTLocation import FFTLocation, LocationNames, RareBattleLocation, SidequestLocation

from ..regions.Zeltennia import *
from ..regions.Fovoham import Grog
from ..regions.Limberry import Bed, Poeskas

BerveniaCity.connections = [
    Connection(Doguola, [HasLesaliaPass]),
    Connection(Bed, [HasLimberryPass]),
    Connection(Finath)
]

BerveniaCity.locations = [
    FFTLocation(LocationNames.BERVENIA_CITY_STORY, battle_level=12)
]

Finath.connections = [
    Connection(BerveniaCity),
    Connection(Zeltennia)
]

Finath.locations = [
    FFTLocation(LocationNames.FINATH_STORY, battle_level=12),
    RareBattleLocation(LocationNames.FINATH_RARE, battle_level=8)
]

Zeltennia.connections = [
    Connection(Finath),
    Connection(Zarghidas),
    Connection(Nelveska)
]

Zeltennia.locations = [
    FFTLocation(LocationNames.ZELTENNIA_STORY, battle_level=12)
]

Zarghidas.connections = [
    Connection(Zeltennia),
    Connection(Germinas)
]

Zarghidas.locations = [
    SidequestLocation(LocationNames.ZARGHIDAS_SIDEQUEST, battle_level=14),
    SidequestLocation(LocationNames.CLOUD_RECRUIT, battle_level=14)
]

Germinas.connections = [
    Connection(Zarghidas),
    Connection(Poeskas, [HasLimberryPass])
]

Germinas.locations = [
    FFTLocation(LocationNames.GERMINAS_STORY, battle_level=13),
    RareBattleLocation(LocationNames.GERMINAS_RARE, battle_level=8)
]

Nelveska.connections = [
    Connection(Zeltennia)
]

Nelveska.locations = [
    SidequestLocation(LocationNames.NELVESKA_SIDEQUEST, battle_level=12),
    SidequestLocation(LocationNames.REIS_HUMAN_RECRUIT, battle_level=12)
]

Doguola.connections = [
    Connection(Grog),
    Connection(BerveniaCity)
]

Doguola.locations = [
    FFTLocation(LocationNames.DOGUOLA_STORY, battle_level=12),
    RareBattleLocation(LocationNames.DOGUOLA_RARE, battle_level=8)
]