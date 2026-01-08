from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import *
from ..regions.Sector1 import Sector1Hub
from ..regions.Sector2 import Sector2NettoriZone, Sector2Hub
from ..regions.Sector3 import Sector3Hub
from ..regions.Sector4 import Sector4Hub
from ..regions.Sector5 import Sector5Hub
from ..regions.Sector6 import Sector6Hub

MainDeckHub.connections = [
    Connection(OperationsDeckElevatorBottom, []),
    Connection(VentilationZone, [CanDefeatSmallGeron]),
    Connection(LowerArachnusArena, [HasMorph]),
    Connection(UpperArachnusArena, [
        Requirement(["Morph Ball", "Screw Attack"], [CanJumpHigh, CanDoSimpleWallJump])
    ]),
    Connection(HabitationDeckElevatorBottom, [HasKeycard2]),
    Connection(SectorHubElevatorTop, [HasMorph, CanDoAdvancedShinespark]),
    Connection(ReactorZone, [
        Requirement(["Morph Ball"], [HasKeycard4, CanPowerBomb], 5)
    ]),
    Connection(NexusStorage, [
        Level2KeycardRequirement([], [CanDefeatLargeGeron])
    ])
]

VentilationZone.connections = [
    Connection(UpperArachnusArena, [
        Requirement(["Morph Ball"], [HasMissile]),
        Requirement(["Morph Ball", "Charge Beam"], [CanDefeatSmallGeron]),
        PONRRequirement([], [CanBeatToughEnemy])
    ], one_way=True)
]

OperationsDeckElevatorBottom.connections = [
    VariableConnection(OperationsDeckElevatorTop, [])
]

OperationsDeckElevatorTop.connections = [
    VariableConnection(OperationsDeckElevatorBottom, []),
    Connection(OperationsDeck, [])
]

OperationsDeck.connections = [
    Connection(LowerArachnusArena, [HasMissile], one_way=True)
]

HabitationDeckElevatorBottom.connections = [
    VariableConnection(HabitationDeckElevatorTop, [])
]

HabitationDeckElevatorTop.connections = [
    VariableConnection(HabitationDeckElevatorBottom, []),
    Connection(HabitationDeck, [HasKeycard2])
]

ReactorZone.connections = [
    Connection(YakuzaZone, [
        PONRRequirement([], [CanAccessYakuza]),
        Requirement(["Space Jump"], [CanAccessYakuza]),
    ], one_way=True),
    Connection(AuxiliaryReactor, [HasWaveBeam]),
    Connection(Sector2NettoriZone, [CanCrossFromReactorToSector2], one_way=True)
]

AuxiliaryReactor.connections = [
    Connection(ReactorZone, [], one_way=True),
    Connection(YakuzaZone, [PONRRequirement(["Nothing"], [])], one_way=True)
]

YakuzaZone.connections = [
    Connection(AuxiliaryReactor, [HasSpaceJump])
]

SectorHubElevatorTop.connections = [
    Connection(MainDeckHub, [
        HasMorph,
        PONRRequirement([], [HasSpeedBooster])
    ], one_way=True),
    VariableConnection(SectorHubElevatorBottom, [])
]

SectorHubElevatorBottom.connections = [
    VariableConnection(SectorHubElevatorTop, []),
    Connection(SectorHubElevator1Top, []),
    Connection(SectorHubElevator2Top, []),
    Connection(SectorHubElevator3Top, [SectorHubLevel1KeycardRequirement]),
    Connection(SectorHubElevator4Top, [SectorHubLevel1KeycardRequirement]),
    Connection(SectorHubElevator5Top, [SectorHubLevel1And2KeycardRequirement]),
    Connection(SectorHubElevator6Top, [SectorHubLevel1And2KeycardRequirement])
]

SectorHubElevator1Top.connections = [
    VariableConnection(Sector1Hub, [])
]

SectorHubElevator2Top.connections = [
    VariableConnection(Sector2Hub, [])
]

SectorHubElevator3Top.connections = [
    VariableConnection(Sector3Hub, [])
]

SectorHubElevator4Top.connections = [
    VariableConnection(Sector4Hub, [])
]

SectorHubElevator5Top.connections = [
    VariableConnection(Sector5Hub, [])
]

SectorHubElevator6Top.connections = [
    VariableConnection(Sector6Hub, [])
]

MainDeckHub.locations = [
    FusionLocation("Main Deck -- Cubby Hole", False, [HasMorph]),
    FusionLocation("Main Deck -- Genesis Speedway", False, [CanReachGenesisSpeedway]),
    FusionLocation("Main Deck -- Quarantine Bay", False, []),
    FusionLocation("Main Deck -- Station Entrance", False, [CanPowerBomb]),
    FusionLocation("Main Deck -- Sub-Zero Containment", False, [
        Level3KeycardRequirement([], [HasVaria])
    ])
]

OperationsDeck.locations = [
    FusionLocation("Main Deck -- Operations Deck Data Room", True, [])
]

VentilationZone.locations = [
    FusionLocation("Main Deck -- Operations Ventilation", False, []),
    FusionLocation("Main Deck -- Operations Ventilation Storage", False, [])
]

UpperArachnusArena.locations = [
    FusionLocation("Main Deck -- Arachnus Arena -- Upper Item", False, []),
    FusionLocation("Main Deck -- Attic", False, [HasMissile]),
]

LowerArachnusArena.locations = [
    FusionLocation("Main Deck -- Arachnus Arena -- Core X", True, [HasMissile])
]

HabitationDeck.locations = [
    FusionLocation("Main Deck -- Habitation Deck -- Animals", True, [
        Level2KeycardRequirement([], [CanReachAnimals]),
        CanFreezeEnemies(["Level 2 Keycard", "Speed Booster"], [CanDoSimpleWallJump]),
        CanFreezeEnemies(["Level 2 Keycard", "Wave Beam"], [CanDoSimpleWallJump, HasHiJump])
    ]),
    FusionLocation("Main Deck -- Habitation Deck -- Lower Item", False, [
        Level2KeycardRequirement([], [HasSpaceJump, HasWaveBeam]),
        CanFreezeEnemies(["Level 2 Keycard"], [HasHiJump, CanDoAdvancedWallJump])
    ])
]

ReactorZone.locations = [
    FusionLocation("Main Deck -- Silo Catwalk", False, [CanDefeatStabilizerOrToughEnemy]),
    FusionLocation("Main Deck -- Silo Scaffolding", False, [
        PONRRequirement(["Morph Ball"], [CanDefeatStabilizerOrToughEnemy]),
        CanDefeatStabilizerOrToughEnemy(["Morph Ball"], [CanJumpHigh, CanDoAdvancedWallJump])
    ])
]

YakuzaZone.locations = [
    FusionLocation("Main Deck -- Yakuza Arena", True, [
        CanFightMidgameBoss,
        CanFightBossOnAdvanced
    ])
]

AuxiliaryReactor.locations = [
    FusionLocation("Main Deck -- Auxiliary Power Station", True, [])
]

SectorHubElevatorTop.locations = [
    FusionLocation("Main Deck -- Main Elevator Cache", False, [HasSpeedBooster])
]

NexusStorage.locations = [
    FusionLocation("Main Deck -- Nexus Storage", False, [CanBallJumpAndBomb])
]
