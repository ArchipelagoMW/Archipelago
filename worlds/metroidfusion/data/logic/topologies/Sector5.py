from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator5Top
from ..regions.Sector3 import Sector3TubeLeft
from ..regions.Sector4 import Sector4UpperWaterZone
from ..regions.Sector5 import *
from ..regions.Sector6 import Sector6TubeRight

Sector5Hub.connections = [
    VariableConnection(SectorHubElevator5Top, []),
    Connection(Sector5MagicBox, [
        Level3KeycardRequirement([], [])
    ]),
    Connection(Sector5TopLeftBigRoom, [
        Level3KeycardRequirement([], [CanJumpHigh, CanDoAdvancedWallJump]),
        Requirement(["Morph Ball"], [HasMissile])
    ]),
    Connection(Sector5FrozenHub, [
        Requirement(["Varia Suit"], [HasKeycard3])
    ])
]

Sector5TubeLeft.connections = [
    VariableConnection(Sector6TubeRight, []),
    Connection(Sector5MagicBox, [HasScrewAttack])
]

Sector5TubeRight.connections = [
    VariableConnection(Sector3TubeLeft, []),
    Connection(Sector5BeforeNightmareHub, [], one_way=True)
]

Sector5TopLeftBigRoom.connections = [
    Connection(Sector5FrozenHub, [HasVaria], one_way=True)
]

Sector5FrozenHub.connections = [
    Connection(Sector5DataRoom, [HasKeycard3], one_way=True),
    Connection(Sector5BeforeNightmareHub, [
        Level3KeycardRequirement([], [HasVaria])
    ]),
    Connection(Sector5SecurityZone, [
        Requirement(["Speed Booster"], [CanBombOrPowerBomb]),
        Level3KeycardRequirement([], [HasWaveBeam])
    ], one_way=True),
    Connection(Sector5TopLeftBigRoom, [
        Requirement(["Varia Suit"], [CanJumpHigh]),
        Requirement(["Varia Suit"], [CanDoAdvancedWallJump])
    ])
]

Sector5SecurityZone.connections = [
    Connection(Sector5DataRoom, [Requirement(["Space Jump"], [HasKeycard3])]),
    Connection(Sector5FrozenHub, [
        HasKeycard3,
        Requirement(["Space Jump"], [CanBombOrPowerBomb]),
        Requirement(["Space Jump", "Speed Booster", "Morph Ball"], [CanFreezeEnemies])
    ], one_way=True)
]

Sector5DataRoom.connections = [
    Connection(Sector5FrozenHub, [
        Level3KeycardRequirement([], [HasWaveBeam])
    ]),
    Connection(Sector5SecurityZone, [], one_way=True)
]

Sector5BeforeNightmareHub.connections = [
    Connection(Sector5TubeRight, [CanJumpHigh, CanDoSimpleWallJump]),
    Connection(Sector5NightmareHub, [
        PONRRequirement(["Hi-Jump"], [CanBeatToughEnemy]),
        PONRRequirement(["Space Jump"], [CanBeatToughEnemy]),
        Requirement(["Gravity Suit", "Space Jump", "Screw Attack"],[CanBeatToughEnemy])
    ], one_way=True)
]

Sector5NightmareHub.connections = [
    Connection(Sector5BeforeNightmareHub, [
        Requirement(["Gravity Suit"], [CanScrewAttackAndSpaceJump])
    ]),
    Connection(Sector5NightmareZoneArena, [CanSpeedBoosterUnderwater], one_way=True),
    Connection(Sector4UpperWaterZone, [CanSpeedBoosterUnderwater]),
    Connection(Sector5NightmareZoneUpper, [
        Requirement(["Charge Beam"], [HasSpaceJump, CanDoSimpleWallJump]),
        Requirement(["Missile Data"], [HasSpaceJump, CanDoSimpleWallJump])
    ])
]

Sector5NightmareZoneUpper.connections = [
    Connection(Sector5NightmareZoneArena, [
        PONRRequirement(["Nothing"], []),
        CanEscapeNightmareRoom
    ])
]

Sector5NightmareZoneArena.connections = [
    Connection(Sector5NightmareHub, [CanEscapeNightmareRoom])
]

Sector5Hub.locations = [
    FusionLocation("Sector 5 (ARC) -- Gerubus Gully", False, [
        PONRRequirement(["Morph Ball", "Level 3 Keycard"], [HasScrewAttack]),
        Requirement(["Level 3 Keycard"], [CanPowerBomb]),
        Requirement(["Morph Ball", "Bomb Data", "Level 3 Keycard"], [HasScrewAttack])
    ]),
]

Sector5MagicBox.locations = [
    FusionLocation("Sector 5 (ARC) -- Magic Box", False, [])
]

Sector5TopLeftBigRoom.locations = [
    FusionLocation("Sector 5 (ARC) -- Training Aerie -- Left Item", False, [
        Requirement(["Speed Booster"], [HasSpaceJump, CanFreezeEnemies])
    ]),
    FusionLocation("Sector 5 (ARC) -- Training Aerie -- Right Item", False, [
        HasSpaceJump,
        CanFreezeEnemies
    ])
]

Sector5FrozenHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Ripper Road", False, [CanAccessRipperRoad])
]

Sector5BeforeNightmareHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Crow's Nest", False, [
        Requirement(
            ["Morph Ball", "Power Bomb Data"],
            [HasSpaceJump, CanDoSimpleWallJumpWithHiJump, CanDoAdvancedWallJump]
        ),
        Requirement(
            ["Morph Ball"],
            [
                CanScrewAttackAndSpaceJump,
                CanDoSimpleWallJumpWithHiJumpAndScrewAttack,
                CanDoAdvancedWallJumpWithScrewAttack
            ]
        ),
    ])
]

Sector5DataRoom.locations = [
    FusionLocation("Sector 5 (ARC) -- Data Room", True, [])
]

Sector5SecurityZone.locations = [
    FusionLocation("Sector 5 (ARC) -- E-Tank Mimic Den", False, [
        PONRRequirement(
            ["Morph Ball", "Power Bomb Data", "Level 3 Keycard"],
            [CanFreezeEnemies, HasSpaceJump]
        ),
        PONRRequirement(
            ["Morph Ball", "Screw Attack", "Level 3 Keycard"],
            [CanFreezeEnemies, HasSpaceJump]
        ),
        Requirement(
            ["Morph Ball", "Bomb Data", "Level 3 Keycard"],
            [CanFreezeEnemies, HasSpaceJump]
        ),
        Requirement(
            ["Morph Ball", "Power Bomb Data", "Hi-Jump", "Level 3 Keycard"],
            [CanFreezeEnemies, HasSpaceJump]
        ),
    ]),
    FusionLocation("Sector 5 (ARC) -- Level 3 Security Room", True, []),
    FusionLocation("Sector 5 (ARC) -- Ripper's Treasure", False, [CanAccessRipperTreasure]),
    FusionLocation("Sector 5 (ARC) -- Security Shaft East", False, [CanPowerBomb]),
    FusionLocation("Sector 5 (ARC) -- Transmutation Trial", False, [
        Level3KeycardRequirement(["Morph Ball", "Hi-Jump"], [HasSpaceJump, CanFreezeEnemies]),
        Level3KeycardRequirement(["Morph Ball", "Bomb Data"], [HasSpaceJump, CanFreezeEnemies])
    ])
]

Sector5NightmareHub.locations = [
    FusionLocation("Sector 5 (ARC) -- Flooded Airlock to Sector 4 (AQA)", False, [
        CanSpeedBoosterUnderwater
    ]),
    FusionLocation("Sector 5 (ARC) -- Mini-Fridge", False, [
        Requirement(
            ["Morph Ball", "Missile Data", "Varia Suit", "Gravity Suit"],
            [CanFreezeEnemies, HasSpaceJump])
    ]),
    FusionLocation("Sector 5 (ARC) -- Nightmare Hub", False, [
        Requirement(["Power Bomb Data"], [CanBallJump])
    ]),
    FusionLocation("Sector 5 (ARC) -- Ruined Break Room", False, [CanPowerBomb])
]

Sector5NightmareZoneUpper.locations = [
    FusionLocation("Sector 5 (ARC) -- Nightmare Nook", False, [
        PONRRequirement([], [CanBallJumpAndBomb]),
        Requirement(
            ["Morph Ball", "Bomb Data", "Gravity Suit", "Speed Booster"],
            [CanFightLateGameBoss, CanFightLategameBossOnAdvanced, CanFightBossOnExpert]
        ),
        Requirement(
            ["Morph Ball", "Hi-Jump", "Power Bomb Data", "Gravity Suit", "Speed Booster"],
            [CanFightLateGameBoss, CanFightLategameBossOnAdvanced, CanFightBossOnExpert]
        ),
    ])
]

Sector5NightmareZoneArena.locations = [
    FusionLocation("Sector 5 (ARC) -- Nightmare Arena", True, [
        CanFightLateGameBoss,
        CanFightLategameBossOnAdvanced,
        CanFightBossOnExpert
    ])
]