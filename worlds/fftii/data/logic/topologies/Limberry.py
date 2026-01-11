from ..Connection import Connection
from ..Requirements import *
from ..FFTLocation import FFTLocation, LocationNames, RareBattleLocation

from ..regions.Limberry import *
from ..regions.Zeltennia import BerveniaCity, Germinas
from ..regions.Lesalia import Zirekile

Bed.connections = [
    Connection(BerveniaCity, [HasZeltenniaPass]),
    Connection(Bethla)
]

Bed.locations = [
    FFTLocation(LocationNames.BED_STORY, battle_level=12),
    RareBattleLocation(LocationNames.BED_RARE, battle_level=8)
]

Bethla.connections = [
    Connection(Bed),
    Connection(Dolbodar),
    Connection(Zirekile, [HasLesaliaPass])
]

Bethla.locations = [
    FFTLocation(LocationNames.BETHLA_NORTH_STORY, battle_level=12),
    FFTLocation(LocationNames.BETHLA_SOUTH_STORY, battle_level=12),
    FFTLocation(LocationNames.BETHLA_SLUICE_STORY, battle_level=12),
    FFTLocation(LocationNames.BETHLA_SHOP, battle_level=12),
    FFTLocation(LocationNames.ORLANDU_RECRUIT, battle_level=12)
]

Dolbodar.connections = [
    Connection(Bethla),
    Connection(Limberry)
]

Dolbodar.locations = [
    RareBattleLocation(LocationNames.DOLBODAR_RARE, battle_level=8)
]

Limberry.connections = [
    Connection(Dolbodar),
    Connection(Poeskas)
]

Limberry.locations = [
    FFTLocation(LocationNames.LIMBERRY_1_STORY, battle_level=13),
    FFTLocation(LocationNames.LIMBERRY_2_STORY, battle_level=13),
    FFTLocation(LocationNames.LIMBERRY_3_STORY, battle_level=13),
    FFTLocation(LocationNames.LIMBERRY_SHOP, battle_level=13),
    FFTLocation(LocationNames.MELIADOUL_RECRUIT, battle_level=13)
]

Poeskas.connections = [
    Connection(Germinas, [HasZeltenniaPass]),
    Connection(Limberry)
]

Poeskas.locations = [
    FFTLocation(LocationNames.POESKAS_STORY, battle_level=13),
    RareBattleLocation(LocationNames.POESKAS_RARE, battle_level=8)
]