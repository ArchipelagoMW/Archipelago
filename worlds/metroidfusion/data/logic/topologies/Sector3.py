from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator3Top
from ..regions.Sector1 import Sector1TubeLeft
from ..regions.Sector3 import *
from ..regions.Sector5 import Sector5TubeRight

Sector3Hub.connections = [
    VariableConnection(SectorHubElevator3Top, []),
    Connection(Sector3FieryStorageRight, [CanAccessFieryStorage]),
    Connection(Sector3SecurityZone, [HasSpeedBooster]),
    Connection(Sector3MainShaft, [
        Requirement(["Morph Ball", "Speed Booster"], [])
    ]),
    Connection(Sector3BobZone, [
        Level2KeycardRequirement([], [CanDefeatMediumGeron])
    ]),
    Connection(Sector3LowerAttic, [
        Requirement(["Screw Attack", "Space Jump", "Morph Ball"], [])
    ])
]

Sector3TubeLeft.connections = [
    VariableConnection(Sector5TubeRight, []),
    Connection(Sector3FieryStorageLeft, [
        Requirement(["Screw Attack"], [CanJumpHigh, CanDoSimpleWallJump])
    ])
]

Sector3TubeRight.connections = [
    VariableConnection(Sector1TubeLeft, []),
]

Sector3FieryStorageRight.connections = [
    Connection(Sector3FieryStorageLeft, [CanDestroyBombBlocks])
]

Sector3FieryStorageLeft.connections = [
    Connection(Sector3TubeLeft, [
        PONRRequirement([], [HasScrewAttack])
    ], one_way=True)
]

Sector3MainShaft.connections = [
    Connection(Sector3BoilerZone, [Level2KeycardRequirement([], [HasVaria])]),
    Connection(Sector3BobZone, [Requirement([], [CanBallJumpAndBomb])]),
    Connection(Sector3SovaProcessing, [
        Level2KeycardRequirement(
            ["Varia Suit", "Morph Ball", "Bomb Data"],
            [
                HasSpaceJump,
                HasWaveBeam,
                Requirement(["Missile Data"], [CanDoBeginnerShinespark])
            ]
        ),
        Level2KeycardRequirement(
            ["Varia Suit", "Morph Ball", "Power Bomb Data"],
            [
                HasSpaceJump,
                HasWaveBeam,
                Requirement(["Missile Data"], [CanDoBeginnerShinespark])
            ]),
        Level2KeycardRequirement(
            ["Varia Suit", "Screw Attack"],
            [
                HasSpaceJump,
                HasWaveBeam,
                Requirement(["Missile Data"], [CanDoBeginnerShinespark])
            ]),
    ])
]

Sector3BobZone.connections = [
    Connection(Sector3BOXZone, [Requirement(["Morph Ball"], [HasKeycard2])]),
    Connection(Sector3MainShaft, [HasMorph], one_way=True),
    Connection(Sector3Hub, [], one_way=True)
]

Sector3BOXZone.connections = [
    Connection(Sector3UpperAttic, [CanAscendBOXRoom])
]

Sector3LowerAttic.connections = [
    Connection(Sector3Hub, [CanDestroyBombBlocks], one_way=True),
    Connection(Sector3UpperAttic, [
        Requirement(["Space Jump"], [CanBombOrPowerBomb]),
        Requirement(["Morph Ball", "Bomb Data"], [CanDoAdvancedWallJumpWithHiJump]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanDoAdvancedWallJumpWithHiJump]),
        Requirement(["Morph Ball", "Bomb Data", "Hi-Jump"], [CanFreezeEnemies]),
        Requirement(["Morph Ball", "Power Bomb Data", "Hi-Jump"], [CanFreezeEnemies]),
        Requirement(["Morph Ball", "Bomb Data"], [CanDoSimpleWallJumpAndFreezeEnemies]),
        Requirement(
            ["Morph Ball", "Power Bomb Data"],
        [CanDoSimpleWallJumpAndFreezeEnemies]
        )
    ])
]

Sector3UpperAttic.connections = [
    Connection(Sector3BOXZone, [CanFightBoss], one_way=True),
    Connection(Sector3TubeRight, [
        Requirement(["Screw Attack"], [CanJumpHigh])
    ]),
    Connection(Sector3LowerAttic, [HasScrewAttack, CanBallJumpAndBomb], one_way=True)
]

Sector3SovaProcessing.connections = [
    Connection(Sector3UpperAttic, [CanAccessGarbageChute], one_way=True)
]

Sector3FieryStorageRight.locations = [
    FusionLocation("Sector 3 (PYR) -- Fiery Storage -- Lower Item", False, []),
]

Sector3FieryStorageLeft.locations = [
    FusionLocation("Sector 3 (PYR) -- Fiery Storage -- Upper Item", False, [
        CanAccessFieryStorageUpper
    ])
]

Sector3TubeLeft.locations = [
    FusionLocation("Sector 3 (PYR) -- Glass Tube to Sector 5 (ARC)", False, [
        CanAccessGlassTubeItem
    ])
]

Sector3SecurityZone.locations = [
    FusionLocation("Sector 3 (PYR) -- Level 2 Security Room", True, [
        HasKeycard2,
        CanAccessLevel2SecurityRoom
    ]),
    FusionLocation("Sector 3 (PYR) -- Security Access", False, [CanBeatToughEnemyAndJumpHigh])
]

Sector3MainShaft.locations = [
    FusionLocation("Sector 3 (PYR) -- Namihe's Lair", False, [CanPowerBombAndJumpHigh]),
    FusionLocation("Sector 3 (PYR) -- Processing Access", False, [
        Level2KeycardRequirement([], [])
    ]),
]

Sector3BoilerZone.locations = [
    FusionLocation("Sector 3 (PYR) -- Lava Maze", False, [
        Requirement([], [CanNavigateLavaMaze])
    ]),
    FusionLocation("Sector 3 (PYR) -- Main Boiler Control Room -- Boiler", True, [
        Requirement(["Missile Data"], [HasSpaceJump, CanFreezeEnemies])
    ]),
    FusionLocation("Sector 3 (PYR) -- Main Boiler Control Room -- Core X", True, [
        Requirement(["Missile Data"], [HasSpaceJump, CanFreezeEnemies])
    ]),
]

Sector3BobZone.locations = [
    FusionLocation("Sector 3 (PYR) -- Bob's Abode", False, [CanBallJump]),
]

Sector3BOXZone.locations = [
    FusionLocation("Sector 3 (PYR) -- Data Room", True, [
        Level2KeycardRequirement([], [CanFightBoss])
    ]),
    FusionLocation("Sector 3 (PYR) -- Geron's Treasure", False, [CanDefeatMediumGeron])
]

Sector3LowerAttic.locations = [
    FusionLocation("Sector 3 (PYR) -- Alcove -- Lower Item", False, [
        CanAccessSector3LowerAlcove
    ]),
    FusionLocation("Sector 3 (PYR) -- Alcove -- Upper Item", False, [
        Requirement(["Speed Booster"], [CanPowerBomb])
    ]),
]

Sector3UpperAttic.locations = [
    FusionLocation("Sector 3 (PYR) -- Deserted Runway", False, [HasSpeedBooster]),
]

Sector3SovaProcessing.locations = [
    FusionLocation("Sector 3 (PYR) -- Sova Processing -- Left Item", False, [
        Requirement(["Morph Ball"], [
            Requirement(["Bomb Data"], [HasSpaceJump]),
            Requirement(["Hi-Jump"], [HasSpaceJump]),
            Requirement(["Bomb Data"], [CanFreezeEnemies]),
            Requirement(["Hi-Jump"], [CanFreezeEnemies])
        ])
    ]),
    FusionLocation("Sector 3 (PYR) -- Sova Processing -- Right Item", False, [
        Requirement(["Morph Ball"], [HasSpaceJump, CanFreezeEnemies])
    ]),
    FusionLocation("Sector 3 (PYR) -- Garbage Chute -- Lower Item", False, [
        CanAccessGarbageChute
    ]),
    FusionLocation("Sector 3 (PYR) -- Garbage Chute -- Upper Item", False, [
        CanAccessGarbageChute
    ])
]
