from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator1Top
from ..regions.Sector1 import *
from ..regions.Sector2 import Sector2TubeLeft
from ..regions.Sector3 import Sector3TubeRight
from ..regions.Sector6 import Sector6RestrictedZoneElevatorToTourian

Sector1Hub.connections = [
    VariableConnection(SectorHubElevator1Top, []),
    Connection(Sector1Antechamber, [
        Level2KeycardRequirement([], [CanScrewAttackAndSpaceJump])
    ]),
    Connection(Sector1TubeLeft, [
        Level1KeycardRequirement(["Morph Ball", "Screw Attack"], [])
    ]),
    Connection(Sector1FirstStabilizerZone, [
        CanDefeatSmallGeron,
        Level1And2KeycardRequirement([], [CanLavaDive]),
        CanDoAdvancedShinespark
    ]),
]

Sector1Antechamber.connections = [
    Connection(Sector1Hub, [
        Level2KeycardRequirement([], [HasScrewAttack])
    ], one_way=True),
    Connection(Sector1TubeRight, [HasMorph], one_way=True)
]

Sector1TubeRight.connections = [
    Connection(Sector1Antechamber, [CanBallJump]),
    VariableConnection(Sector2TubeLeft, [])
]

Sector1TubeLeft.connections = [
    VariableConnection(Sector3TubeRight, [])
]

Sector1FirstStabilizerZone.connections = [
    Connection(Sector1SecondStabilizerZone, [CanDefeatStabilizerOrToughEnemy]),
    Connection(Sector1AfterChargeCoreZone, [HasWaveBeam], one_way=True),
]

Sector1SecondStabilizerZone.connections = [
    Connection(Sector1ThirdStabilizerZone, [CanDefeatStabilizerOrToughEnemy]),
    Connection(Sector1TourianExit, [
        Requirement(["Screw Attack"], [])
    ], one_way=True)
]

Sector1ThirdStabilizerZone.connections = [
    Connection(Sector1ChargeCoreZone, [
        PONRRequirement(["Morph Ball"], [CanDefeatThirdStabilizer]),
        Requirement(["Morph Ball", "Missile Data"], [CanDefeatThirdStabilizer])
    ], one_way=True),
]

Sector1ChargeCoreZone.connections = [
    Connection(Sector1AfterChargeCoreZone, [CanFightBeginnerBoss])
]

Sector1AfterChargeCoreZone.connections = [
    Connection(Sector1FirstStabilizerZone, [], one_way=True)
]

Sector1TourianExit.connections = [
    Connection(Sector1SecondStabilizerZone, [CanScrewAttackAndSpaceJump]),
    Connection(Sector1TourianHub, [
        Requirement(
            ["Missile Data", "Morph Ball", "Screw Attack"],
            [HasSpaceJump, CanDoSimpleWallJump],
            level_4_e_tanks)
    ], one_way=True)
]

Sector1TourianHub.connections = [
    Connection(Sector1TourianExit, [
        Requirement(
            ["Screw Attack", "Morph Ball", "Wave Beam"],
            [HasMissile],
            level_4_e_tanks)
    ])
]

Sector1TourianHubElevatorTop.connections = [
    VariableConnection(Sector6RestrictedZoneElevatorToTourian, []),
    Connection(Sector1TourianHub, [Requirement([], [], level_4_e_tanks)])
]

Sector1Antechamber.locations = [
    FusionLocation("Sector 1 (SRX) -- Antechamber", False, [])
]

Sector1FirstStabilizerZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Atmospheric Stabilizer Northeast", False, []),
    FusionLocation("Sector 1 (SRX) -- Hornoad Hole", False, [HasMorph]),
    FusionLocation("Sector 1 (SRX) -- Wall Jump Tutorial", False, [
        CanAccessWallJumpTutorialWithSpaceJump,
        CanAccessWallJumpTutorialWithWallJump
    ])
]

Sector1SecondStabilizerZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Lower Item", False, [
        Requirement(["Morph Ball"], [CanLavaDive])
    ]),
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Upper Left Item", False, [
        HasSpaceJump,
        CanDoBeginnerShinespark
    ]),
    FusionLocation("Sector 1 (SRX) -- Lava Lake -- Upper Right Item", False, []),
]

Sector1ThirdStabilizerZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Stabilizer Storage", False, [CanDefeatThirdStabilizer])
]

Sector1ChargeCoreZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Charge Core Arena -- Core X", True, [
        CanFightBeginnerBoss
    ]),
    FusionLocation("Sector 1 (SRX) -- Charge Core Arena -- Upper Item", False, [
        Requirement(["Speed Booster"], [CanFightBeginnerBoss])
    ]),
    FusionLocation("Sector 1 (SRX) -- Watering Hole", False, [CanAccessWateringHole])
]

Sector1AfterChargeCoreZone.locations = [
    FusionLocation("Sector 1 (SRX) -- Crab Rave", False, [
        Requirement(["Morph Ball", "Missile Data"], [])
    ])
]

Sector1TourianHub.locations = [
    FusionLocation("Sector 1 (SRX) -- Animorphs Cache", False, [
        PONRRequirement([], [CanReachAnimorphs]),
        Requirement(["Space Jump"], [CanReachAnimorphs]),
    ]),
    FusionLocation("Sector 1 (SRX) -- Ridley Arena", True, [
        Requirement(["Charge Beam", "Wave Beam"], [CanFightLateGameBoss]),
        Requirement(["Power Bomb Data"], [CanFightLateGameBoss]),
        Requirement(["Charge Beam", "Wave Beam"], [CanFightLategameBossOnAdvanced]),
        Requirement(["Power Bomb Data"], [CanFightLategameBossOnAdvanced]),
        Requirement(["Charge Beam", "Wave Beam"], [CanFightBossOnExpert]),
        Requirement(["Power Bomb Data"], [CanFightBossOnExpert])
    ]),
    FusionLocation("Sector 1 (SRX) -- Ripper Maze", False, [CanDiffusionMissile])
]
