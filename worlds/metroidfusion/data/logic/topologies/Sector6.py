from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator6Top
from ..regions.Sector1 import Sector1TourianHubElevatorTop
from ..regions.Sector4 import Sector4TubeRight
from ..regions.Sector5 import Sector5TubeLeft
from ..regions.Sector6 import *


Sector6Hub.connections = [
    VariableConnection(SectorHubElevator6Top, []),
    Connection(Sector6Crossroads, [CanDefeatMediumGeron, CanDoBeginnerShinespark]),
    Connection(Sector6TubeLeft, [HasScrewAttack])
]

Sector6TubeLeft.connections = [
    VariableConnection(Sector4TubeRight, [])
]

Sector6TubeRight.connections = [
    VariableConnection(Sector5TubeLeft, []),
    Connection(Sector6Crossroads, [HasScrewAttack])
]

Sector6Crossroads.connections = [
    Connection(Sector6BeforeXBOXZone, [
        Level4KeycardRequirement(["Varia Suit"], [CanPowerBomb])
    ]),
    Connection(Sector6BeforeVariaCoreXZone, [
        PONRRequirement(["Speed Booster"], [CanBombOrPowerBomb]),
        CanDoAdvancedShinespark(["Morph Ball", "Power Bomb Data"], [
            HasSpaceJump, CanDoAdvancedWallJump
        ]),
        Level2KeycardRequirement(["Speed Booster", "Charge Beam", "Missile Data", "Varia Suit"], [
            CanBombOrPowerBomb
        ])
    ]),
    Connection(Sector6AfterVariaCoreXZone, [
        Requirement(["Morph Ball", "Varia Suit"], [HasScrewAttack])
    ])
]

Sector6BeforeXBOXZone.connections = [
    Connection(Sector6XBOXZone, [
        PONRRequirement(["Nothing"], []),
        Requirement([], [CanScrewAttackAndSpaceJump]),
        Requirement(["Speed Booster", "Wave Beam"], [])
    ], one_way=True)
]

Sector6XBOXZone.connections = [
    Connection(Sector6AfterXBOXZone, [
        CanFightLateGameBoss,
        CanFightLategameBossOnAdvanced,
        CanFightBossOnExpert
    ])
]

Sector6AfterXBOXZone.connections = [
    Connection(Sector6BeforeXBOXZone, [
        Requirement([], [CanScrewAttackAndSpaceJump]),
        Requirement(["Screw Attack", "Hi-Jump"], [CanFreezeEnemies, CanDoSimpleWallJump])
    ], one_way=True),
    Connection(Sector6RestrictedZone, [HasWaveBeam])
]

Sector6RestrictedZone.connections = [
    Connection(Sector6RestrictedZoneElevatorToTourian, [HasSpeedBooster], one_way=True)
]

Sector6RestrictedZoneElevatorToTourian.connections = [
    VariableConnection(Sector1TourianHubElevatorTop, [HasKeycard4])
]

Sector6BeforeVariaCoreXZone.connections = [
    Connection(Sector6VariaCoreXZone, [
        Level2KeycardRequirement([], [CanFightBoss])
    ])
]

Sector6VariaCoreXZone.connections = [
    Connection(Sector6AfterVariaCoreXZone, [
        Requirement(["Varia Suit"], [CanFightBoss])
    ])
]

Sector6AfterVariaCoreXZone.connections = [
    Connection(Sector6Crossroads, [HasMorph], one_way=True)
]

Sector6Hub.locations = [
    FusionLocation("Sector 6 (NOC) -- Entrance Lobby", False, [
        Requirement(["Screw Attack"], [CanBallJump]),
        Requirement([], [CanBallJumpAndBomb]),
        CanDoBeginnerShinespark([], [CanBallJump])
    ])
]

Sector6Crossroads.locations = [
    FusionLocation("Sector 6 (NOC) -- Catacombs", False, [
        PONRRequirement([], [HasSpeedBooster]),
        CanDoAdvancedShinespark,
        Level2KeycardRequirement(["Speed Booster", "Charge Beam", "Missile Data", "Varia Suit"], [
            CanBombOrPowerBomb
        ])
    ]),
    FusionLocation("Sector 6 (NOC) -- Missile Mimic Lodge", False, [
        Requirement(["Varia Suit"], [CanBombOrPowerBomb])
    ]),
    FusionLocation("Sector 6 (NOC) -- Pillar Highway", False, [
        Requirement(
            ["Screw Attack", "Speed Booster", "Varia Suit"],
            [CanBomb, HasWaveBeam]
        )
    ]),
    FusionLocation("Sector 6 (NOC) -- Vault", False, [CanBallJumpAndBomb])
]

Sector6BeforeXBOXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- Spaceboost Alley -- Lower Item", False, [
        Requirement(["Hi-Jump", "Space Jump", "Screw Attack"], [HasSpeedBooster])
    ]),
    FusionLocation("Sector 6 (NOC) -- Spaceboost Alley -- Upper Item", False, [
        Requirement(["Screw Attack"], [HasSpeedBooster])
    ])
]

Sector6XBOXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- X-B.O.X. Arena", True, [
        CanFightLateGameBoss,
        CanFightLategameBossOnAdvanced,
        CanFightBossOnExpert
    ])
]

Sector6AfterXBOXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- X-B.O.X. Garage -- Lower Item", False, [HasWaveBeam]),
    FusionLocation("Sector 6 (NOC) -- X-B.O.X. Garage -- Upper Item", False, [
        Requirement(["Morph Ball", "Bomb Data"], [CanScrewAttackAndSpaceJump]),
    ])
]

Sector6RestrictedZone.locations = [
    FusionLocation("Main Deck -- Restricted Airlock", False, [HasSpeedBooster])
]

Sector6BeforeVariaCoreXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- Zozoro Wine Cellar", False, [
        Requirement(["Morph Ball", "Bomb Data"], [CanJumpHigh]),
        Requirement(["Morph Ball", "Power Bomb Data"], [CanJumpHigh]),
    ])
]

Sector6VariaCoreXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- Varia Core-X Arena", True, [CanFightBoss])
]

Sector6AfterVariaCoreXZone.locations = [
    FusionLocation("Sector 6 (NOC) -- Twin Caverns West -- Lower Item", False, [
        Requirement(["Morph Ball"], [CanJumpHigh])
    ]),
    FusionLocation("Sector 6 (NOC) -- Twin Caverns West -- Upper Item", False, [])
]
