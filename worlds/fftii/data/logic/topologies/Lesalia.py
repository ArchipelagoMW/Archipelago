from ..Connection import Connection
from ..Requirements import *
from ..FFTLocation import FFTLocation, LocationNames, RareBattleLocation, SidequestLocation

from ..regions.Lesalia import *
from ..regions.Gallione import Dorter
from ..regions.Fovoham import Grog, Riovanes
from ..regions.Limberry import Bethla
from ..regions.Lionel import Zaland

Araguay.connections = [
    Connection(Dorter, [HasGallionePass]),
    Connection(Zirekile)
]

Araguay.locations = [
    FFTLocation(LocationNames.ARAGUAY_STORY, battle_level=4),
    FFTLocation(LocationNames.BOCO_RECRUIT, battle_level=4),
    RareBattleLocation(LocationNames.ARAGUAY_RARE, battle_level=8)
]

Zeklaus.connections = [
    Connection(Dorter, [HasGallionePass]),
    Connection(Goland),
    Connection(BerveniaVolcano)
]

Zeklaus.locations = [
    FFTLocation(LocationNames.ZEKLAUS_STORY, battle_level=1),
    FFTLocation(LocationNames.ZEKLAUS_SHOP, battle_level=1),
    RareBattleLocation(LocationNames.ZEKLAUS_RARE, battle_level=8)
]

BerveniaVolcano.connections = [
    Connection(Zeklaus),
    Connection(Riovanes, [HasFovohamPass])
]

BerveniaVolcano.locations = [
    RareBattleLocation(LocationNames.BERVENIA_VOLCANO_RARE, battle_level=8)
]

Zirekile.connections = [
    Connection(Araguay),
    Connection(Zaland, [HasLionelPass]),
    Connection(Bethla, [HasLimberryPass])
]

Zirekile.locations = [
    FFTLocation(LocationNames.ZIREKILE_STORY, battle_level=4),
    FFTLocation(LocationNames.ZIREKILE_SHOP, battle_level=4),
    RareBattleLocation(LocationNames.ZIREKILE_RARE, battle_level=8)
]

Goland.connections = [
    Connection(Zeklaus),
    Connection(Lesalia)
]

Goland.locations = [
    FFTLocation(LocationNames.GOLAND_STORY, battle_level=8),
    SidequestLocation(LocationNames.GOLAND_1_SIDEQUEST, battle_level=8),
    SidequestLocation(LocationNames.GOLAND_2_SIDEQUEST, battle_level=8),
    SidequestLocation(LocationNames.GOLAND_3_SIDEQUEST, battle_level=8),
    SidequestLocation(LocationNames.GOLAND_4_SIDEQUEST, battle_level=8),
    SidequestLocation(LocationNames.BEOWULF_RECRUIT, battle_level=8),
    SidequestLocation(LocationNames.REIS_DRAGON_RECRUIT, battle_level=8),
    SidequestLocation(LocationNames.WORKER_8_RECRUIT, battle_level=8)
]

Lesalia.connections = [
    Connection(Goland),
    Connection(Grog, [HasFovohamPass])
]

Lesalia.locations = [
    FFTLocation(LocationNames.LESALIA_STORY, battle_level=8),
    FFTLocation(LocationNames.LESALIA_SHOP, battle_level=8)
]
