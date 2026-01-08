from ..Connection import Connection
from ..Requirement import PONRRequirement
from ..VariableConnection import VariableConnection
from ..Requirements import *
from ..FusionLocation import FusionLocation

from ..regions.MainDeck import SectorHubElevator4Top
from ..regions.Sector2 import Sector2TubeRight
from ..regions.Sector4 import *
from ..regions.Sector5 import Sector5NightmareHub
from ..regions.Sector6 import Sector6TubeLeft

Sector4Hub.connections = [
    VariableConnection(SectorHubElevator4Top, []),
    Connection(Sector4UpperZone, [CanBombOrPowerBomb], one_way=True),
    Connection(Sector4DataZone, [
        CanDrainAQARequirement(["Missile Data", "Diffusion Missile"], [HasMorph]),
        CanDrainAQARequirement(["Ice Beam", "Wave Beam"], [HasMorph])
    ]),
    Connection(Sector4RightWaterZone, [
        CanDrainAQARequirement(
            ["Missile Data", "Diffusion Missile", "Gravity Suit"],
            [CanBombOrPowerBomb]
        ),
        CanDrainAQARequirement(
            ["Ice Beam", "Wave Beam", "Gravity Suit"],
            [CanBombOrPowerBomb]
        )
    ])
]

Sector4TubeRight.connections = [
    VariableConnection(Sector6TubeLeft, [HasScrewAttack]),
    Connection(Sector4RightDataZone, [
        Requirement(["Morph Ball"], [HasMissile])
    ]),
]

Sector4TubeLeft.connections = [
    VariableConnection(Sector2TubeRight, []),
    Connection(Sector4RightWaterZone, [
        Requirement(["Gravity Suit", "Screw Attack"], [HasSpaceJump, CanDoSimpleWallJump])
    ])
]

Sector4UpperZone.connections = [
    Connection(Sector4Hub, [CanDrainAQARequirement([], [])], one_way=True),
    Connection(Sector4BeforePumpControlZone, [CanBombOrPowerBomb])
]

Sector4BeforePumpControlZone.connections = [
    Connection(Sector4PumpControl, [
        Level1KeycardRequirement([], [HasSpeedBooster])
    ], one_way=True),
    Connection(Sector4UpperWaterZone, [
        CanDrainAQARequirement(["Gravity Suit"], [HasKeycard4])
    ], one_way=True),
    Connection(Sector4SerrisZone, [
        PONRRequirement(["Hi-Jump"], [CanBombOrPowerBomb]),
        PONRRequirement(["Morph Ball", "Bomb Data", "Gravity Suit"], []),
        Requirement(["Hi-Jump", "Speed Booster"], [CanBombOrPowerBomb]),
        Requirement(["Morph Ball", "Bomb Data", "Gravity Suit", "Speed Booster"], [])
    ], one_way=True),
    Connection(Sector4UpperZone, [
        CanDrainAQARequirement([], [HasMorph])
    ], one_way=True)
]

Sector4SerrisZone.connections = [
    Connection(Sector4BeforePumpControlZone, [
        Requirement(
            ["Gravity Suit", "Morph Ball", "Bomb Data"],
            [CanDoSimpleWallJump, HasSpaceJump]
        ),
        Requirement(
            ["Gravity Suit", "Morph Ball", "Power Bomb Data"],
            [CanDoSimpleWallJump, HasSpaceJump]
        )
    ]),
    Connection(Sector4UpperZone, [HasSpeedBooster], one_way=True)
]

Sector4PumpControl.connections = [
    Connection(Sector4BeforePumpControlZone, [CanBallJump], one_way=True)
]

Sector4UpperWaterZone.connections = [
    Connection(Sector4BeforePumpControlZone, [
        Level4KeycardRequirement([], [CanJumpHighUnderwater]),
        Level4KeycardRequirement(["Gravity Suit"], [CanDoBeginnerShinespark])
    ]),
    Connection(Sector5NightmareHub, [
        Requirement(["Gravity Suit", "Speed Booster"], [CanJumpHigh])
    ], one_way=True),
    Connection(Sector4SecurityZone, [
        CanSpeedBoosterUnderwater,
        Requirement(["Screw Attack", "Gravity Suit"], [CanBallJump])
    ]),
]

Sector4SecurityZone.connections = [
    Connection(Sector4RightWaterZone, [CanCrossSector4LowerSecurityToRightWaterZone]),
    Connection(Sector4LowerSecurityZone, [
        PONRRequirement([], [HasKeycard4]),
        PONRRequirement([], [CanAscendCheddarBay]),
        Requirement(["Space Jump"], [HasKeycard4]),
        Requirement(["Space Jump"], [CanAscendCheddarBay])
    ]),
    Connection(Sector4SecurityRoom, [
        PONRRequirement([], [CanAscendCheddarBay]),
        Requirement(["Level 4 Keycard", "Space Jump"], [CanAscendCheddarBay]),
    ], one_way=True),
]

Sector4LowerSecurityZone.connections = [
    Connection(Sector4SecurityRoom, [HasKeycard4])
]

Sector4RightWaterZone.connections = [
    Connection(Sector4RightDataZone, [
        Requirement(["Gravity Suit"], [CanCrossSector4RightWaterCorner])
    ]),
    Connection(Sector4TubeLeft, [
        Requirement(["Gravity Suit"] ,[HasScrewAttack])
    ], one_way=True)
]

Sector4DataZone.connections = [
    Connection(Sector4RightDataZone, [
        Level4KeycardRequirement([], [CanBombOrPowerBomb])
    ])
]

Sector4RightDataZone.connections = [
    Connection(Sector4RightWaterZone, [
        Requirement(["Morph Ball", "Gravity Suit"], [CanDiffusionMissile])
    ], one_way=True)
]

Sector4Hub.locations = [
    FusionLocation("Sector 4 (AQA) -- Drain Pipe", False, [
        CanDrainAQARequirement(["Morph Ball"], [CanDefeatLargeGeron]),
        CanDrainAQARequirement(["Morph Ball"], [HasWaveBeam]),

    ]),
    FusionLocation("Sector 4 (AQA) -- Reservoir East", False, [
        CanDrainAQARequirement([], [CanPowerBomb])
    ])
]

Sector4PumpControl.locations = [
    FusionLocation("Sector 4 (AQA) -- Pump Control Unit", False, [HasMorph])
]

Sector4UpperZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Broken Bridge", False, []),
    FusionLocation("Sector 4 (AQA) -- C-Cache", False, []),
    FusionLocation("Sector 4 (AQA) -- Reservoir Vault -- Lower Item", False, [
        Requirement(["Missile Data"], [CanAccessReservoirVault])
    ]),
    FusionLocation("Sector 4 (AQA) -- Reservoir Vault -- Upper Item", False, [
        CanAccessReservoirVault
    ]),
    FusionLocation("Sector 4 (AQA) -- Waterway", False, [
        CanDrainAQARequirement([], [HasMorph])
    ]),
]

Sector4SerrisZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Serris Arena", True, [
        Requirement(["Hi-Jump"], [CanFightBoss]),
        Requirement(["Space Jump"], [CanFightBoss])
    ])
]

Sector4UpperWaterZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Cargo Hold to Sector 5 (ARC)", False, [
        CanScrewAttackUnderwater,
        Requirement(["Morph Ball"], [CanSpeedBoosterUnderwater])
    ]),
    FusionLocation("Sector 4 (AQA) -- Aquarium Pirate Tank", False, [CanPowerBomb]),
]

Sector4SecurityZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Cheddar Bay", False, [CanAscendCheddarBay]),
    FusionLocation("Sector 4 (AQA) -- Yard Firing Range", False, [])
]

Sector4LowerSecurityZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Sanctuary Cache", False, [
        Requirement(["Morph Ball", "Bomb Data"], [CanAccessSanctuaryCache]),
        Requirement(["Morph Ball", "Hi-Jump"], [CanAccessSanctuaryCache])
    ])
]

Sector4SecurityRoom.locations = [
    FusionLocation("Sector 4 (AQA) -- Level 4 Security Room", True, [
        Requirement(["Space Jump"], [HasKeycard4, CanAscendCheddarBay])
    ]),
]

Sector4RightWaterZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Aquarium Kago Storage -- Left Item", False, [
        HasSpeedBooster,
        HasScrewAttack
    ]),
    FusionLocation("Sector 4 (AQA) -- Aquarium Kago Storage -- Right Item", False, [
        HasSpeedBooster
    ])
]

Sector4DataZone.locations = [
    FusionLocation("Sector 4 (AQA) -- Data Room", True, [
        CanDrainAQARequirement([], [HasKeycard4])
    ])
]
