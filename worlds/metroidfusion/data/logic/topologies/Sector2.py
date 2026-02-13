from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..Requirements import CanBombOrPowerBomb
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator2Top
from ..regions.Sector1 import Sector1TubeRight
from ..regions.Sector2 import *
from ..regions.Sector4 import Sector4TubeLeft

Sector2Hub.connections = [
    VariableConnection(SectorHubElevator2Top, []),
    Connection(Sector2TubeLeft, [HasScrewAttack]),
    Connection(Sector2TubeRight, [HasScrewAttack]),
    Connection(Sector2LeftSide, [
        PONRRequirement(["Morph Ball"], [CanDestroyBombBlocks]),
        Requirement(["Morph Ball", "Hi-Jump"], [CanDestroyBombBlocks]),
        Requirement(["Morph Ball", "Bomb Data"], [CanDestroyBombBlocks]),
    ]),
    Connection(Sector2ZazabiZoneUpper, [CanBombOrPowerBomb]),
    Connection(Sector2NettoriZone, [
        CanPowerBombAndJumpHigh,
        Requirement(["Morph Ball", "Power Bomb Data"], [CanDoSimpleWallJump])
    ])
]

Sector2TubeLeft.connections = [
    VariableConnection(Sector1TubeRight, [])
]

Sector2TubeRight.connections = [
    VariableConnection(Sector4TubeLeft, [])
]

Sector2LeftSide.connections = [
    Connection(Sector2ZazabiZone, [CanBombOrPowerBomb], one_way=True)
]

Sector2ZazabiZone.connections = [
    Connection(Sector2LeftSide, [
        Requirement(["Space Jump"], [CanBombOrPowerBomb])
    ]),
    Connection(Sector2NettoriZone, [HasSpaceJump]),
    Connection(Sector2ZazabiZoneUpper, [
        Requirement([], [HasSpaceJump]),
        Requirement(["Hi-Jump"], [CanFightBoss]),
    ])
]

Sector2ZazabiZoneUpper.connections = [
    Connection(Sector2ZazabiZone, [
        PONRRequirement(["Nothing"], []),
        Requirement(["Hi-Jump"], [CanFightBoss]),
        Requirement(["Space Jump"], []),
    ], one_way=True)
]

Sector2Hub.locations = [
    FusionLocation("Sector 2 (TRO) -- Crumble City -- Lower Item", False, [
        CanScrewAttackAndSpaceJump
    ]),
    FusionLocation("Sector 2 (TRO) -- Crumble City -- Upper Item", False, [
        CanScrewAttackAndSpaceJump
    ]),
    FusionLocation("Sector 2 (TRO) -- Data Courtyard", False, [CanBombOrPowerBomb]),
    FusionLocation("Sector 2 (TRO) -- Data Room", True, [
        Requirement(["Level 1 Keycard"], [])
    ]),
    FusionLocation("Sector 2 (TRO) -- Kago Room", False, [
        CanJumpHigh, HasScrewAttack, CanFreezeEnemies, CanDoBeginnerShinespark
    ]),
    FusionLocation("Sector 2 (TRO) -- Level 1 Security Room", True, [
        PONRRequirement(["Nothing"], []),
        Requirement([], [HasSpaceJump]),
        Requirement(["Level 1 Keycard"], []),
    ]),
    FusionLocation("Sector 2 (TRO) -- Lobby Cache", False, [
        Level1KeycardRequirement([], [CanBombOrPowerBomb])
    ]),
]

Sector2LeftSide.locations = [
    FusionLocation("Sector 2 (TRO) -- Zoro Zig-Zag", False, [
        Requirement(["Morph Ball"], [CanActivatePillar, CanJumpHigh])
    ])
]

Sector2ZazabiZone.locations = [
    FusionLocation("Sector 2 (TRO) -- Cultivation Station", False, [
        CanBacktrackToCultivationStation
    ]),
    FusionLocation("Sector 2 (TRO) -- Oasis", False, [CanJumpHigh]),
    FusionLocation("Sector 2 (TRO) -- Oasis Storage", False, [CanReachOasisStorage]),
    FusionLocation("Sector 2 (TRO) -- Ripper Tower -- Lower Item", False, [
        Requirement(["Morph Ball"], [CanFreezeEnemies])
    ]),
    FusionLocation("Sector 2 (TRO) -- Ripper Tower -- Upper Item", False, [
        Requirement(["Morph Ball"], [CanFreezeEnemies])
    ]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Arena", True, [
        PONRRequirement([], [CanFightBoss]),
        Requirement(["Hi-Jump"], [CanFightBoss]),
        Requirement(["Space Jump"], [CanFightBoss]),
    ]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Arena Access", False, []),
    FusionLocation("Sector 2 (TRO) -- Zazabi Speedway -- Lower Item", False, [
        CanAccessZazabiSpeedway
    ]),
    FusionLocation("Sector 2 (TRO) -- Zazabi Speedway -- Upper Item", False, [
        CanAccessZazabiSpeedway
    ])
]

Sector2ZazabiZoneUpper.locations = [
    FusionLocation("Sector 2 (TRO) -- Dessgeega Dorm", False, [
        PONRRequirement(["Morph Ball"], [CanDestroyBombBlocks]),
        CanBombOrPowerBomb
    ])
]

Sector2NettoriZone.locations = [
    FusionLocation("Sector 2 (TRO) -- Nettori Arena", True, [
        CanFightMidgameBoss,
        CanFightBossOnAdvanced
    ]),
    FusionLocation("Sector 2 (TRO) -- Overgrown Cache", False, [HasMorph]),
    FusionLocation("Sector 2 (TRO) -- Puyo Palace", False, [])
]
