from enum import Enum


class SpriteNames(Enum):
    Empty = "Empty"
    Missiles = "Missiles"
    Level0 = "Level0"
    MorphBall = "MorphBall"
    ChargeBeam = "ChargeBeam"
    Level1 = "Level1"
    Bombs = "Bombs"
    HiJump = "HiJump"
    SpeedBooster = "SpeedBooster"
    Level2 = "Level2"
    SuperMissiles = "SuperMissiles"
    VariaSuit = "VariaSuit"
    Level3 = "Level3"
    IceMissiles = "IceMissiles"
    WideBeam = "WideBeam"
    PowerBombs = "PowerBombs"
    SpaceJump = "SpaceJump"
    PlasmaBeam = "PlasmaBeam"
    GravitySuit = "GravitySuit"
    Level4 = "Level4"
    DiffusionMissiles = "DiffusionMissiles"
    WaveBeam = "WaveBeam"
    ScrewAttack = "ScrewAttack"
    IceBeam = "IceBeam"
    MissileTank = "MissileTank"
    EnergyTank = "EnergyTank"
    PowerBombTank = "PowerBombTank"
    Anonymous = "Anonymous"
    ShinyMissileTank = "ShinyMissileTank"
    ShinyPowerBombTank = "ShinyPowerBombTank"
    InfantMetroid = "InfantMetroid"

offworld_sprites: dict[str, dict[str, SpriteNames]] = {
    "Super Metroid": {
        "Energy Tank": SpriteNames.EnergyTank,
        "Missile": SpriteNames.MissileTank,
        "Super Missile": SpriteNames.SuperMissiles,
        "Power Bomb": SpriteNames.PowerBombTank,
        "Bomb": SpriteNames.Bombs,
        "Charge Beam": SpriteNames.ChargeBeam,
        "Ice Beam": SpriteNames.IceBeam,
        "Hi-Jump Boots": SpriteNames.HiJump,
        "Speed Booster": SpriteNames.SpeedBooster,
        "Wave Beam": SpriteNames.WaveBeam,
        "Spazer": SpriteNames.WideBeam,
        "Plasma Beam": SpriteNames.PlasmaBeam,
        "Spring Ball": SpriteNames.HiJump,
        "Varia Suit": SpriteNames.VariaSuit,
        "Morph Ball": SpriteNames.MorphBall,
        "Reserve Tank": SpriteNames.EnergyTank,
        "Gravity Suit": SpriteNames.GravitySuit,
        "Space Jump": SpriteNames.SpaceJump,
        "Screw Attack": SpriteNames.ScrewAttack
    },
    "Metroid Fusion": {
        "Nothing": SpriteNames.Empty,
        "Level 0 Keycard": SpriteNames.Level0,
        "Missile Data": SpriteNames.Missiles,
        "Morph Ball": SpriteNames.MorphBall,
        "Charge Beam": SpriteNames.ChargeBeam,
        "Level 1 Keycard": SpriteNames.Level1,
        "Bomb Data": SpriteNames.Bombs,
        "Hi-Jump": SpriteNames.HiJump,
        "Speed Booster": SpriteNames.SpeedBooster,
        "Level 2 Keycard": SpriteNames.Level2,
        "Super Missile": SpriteNames.SuperMissiles,
        "Varia Suit": SpriteNames.VariaSuit,
        "Level 3 Keycard": SpriteNames.Level3,
        "Ice Missile": SpriteNames.IceMissiles,
        "Wide Beam": SpriteNames.WideBeam,
        "Power Bomb Data": SpriteNames.PowerBombs,
        "Space Jump": SpriteNames.SpaceJump,
        "Plasma Beam": SpriteNames.PlasmaBeam,
        "Gravity Suit": SpriteNames.GravitySuit,
        "Level 4 Keycard": SpriteNames.Level4,
        "Diffusion Missile": SpriteNames.DiffusionMissiles,
        "Wave Beam": SpriteNames.WaveBeam,
        "Screw Attack": SpriteNames.ScrewAttack,
        "Ice Beam": SpriteNames.IceBeam,
        "Missile Tank": SpriteNames.MissileTank,
        "Energy Tank": SpriteNames.EnergyTank,
        "Power Bomb Tank": SpriteNames.PowerBombTank,
        "Ice Trap": SpriteNames.Anonymous,
        "Infant Metroid": SpriteNames.InfantMetroid
    },
    "SMZ3": {
        "ETank": SpriteNames.EnergyTank,
        "Missile": SpriteNames.MissileTank,
        "Super": SpriteNames.SuperMissiles,
        "PowerBomb": SpriteNames.PowerBombTank,
        "Bombs": SpriteNames.Bombs,
        "Charge": SpriteNames.ChargeBeam,
        "Ice": SpriteNames.IceBeam,
        "HiJump": SpriteNames.HiJump,
        "SpeedBooster": SpriteNames.SpeedBooster,
        "Wave": SpriteNames.WaveBeam,
        "Spazer": SpriteNames.WideBeam,
        "Plasma": SpriteNames.PlasmaBeam,
        "SpringBall": SpriteNames.HiJump,
        "Varia": SpriteNames.VariaSuit,
        "Morph": SpriteNames.MorphBall,
        "ReserveTank": SpriteNames.EnergyTank,
        "Gravity": SpriteNames.GravitySuit,
        "SpaceJump": SpriteNames.SpaceJump,
        "ScrewAttack": SpriteNames.ScrewAttack
    },
    "Metroid Zero Mission": {
        "Energy Tank": SpriteNames.EnergyTank,
        "Missile Tank": SpriteNames.MissileTank,
        "Super Missile Tank": SpriteNames.SuperMissiles,
        "Power Bomb Tank": SpriteNames.PowerBombTank,
        "Charge Beam": SpriteNames.ChargeBeam,
        "Ice Beam": SpriteNames.IceBeam,
        "Wave Beam": SpriteNames.WaveBeam,
        "Plasma Beam": SpriteNames.PlasmaBeam,
        "Bomb": SpriteNames.Bombs,
        "Varia Suit": SpriteNames.VariaSuit,
        "Gravity Suit": SpriteNames.GravitySuit,
        "Morph Ball": SpriteNames.MorphBall,
        "Speed Booster": SpriteNames.SpeedBooster,
        "Hi-Jump Boots": SpriteNames.HiJump,
        "Screw Attack": SpriteNames.ScrewAttack,
        "Space Jump": SpriteNames.SpaceJump
    },
    "Metroid Prime": {
        "Power Beam": SpriteNames.ChargeBeam,
        "Ice Beam": SpriteNames.IceBeam,
        "Wave Beam": SpriteNames.WaveBeam,
        "Plasma Beam": SpriteNames.PlasmaBeam,
        "Missile Expansion": SpriteNames.MissileTank,
        "Morph Ball Bomb": SpriteNames.Bombs,
        "Power Bomb Expansion": SpriteNames.PowerBombTank,
        "Charge Beam": SpriteNames.ChargeBeam,
        "Super Missile": SpriteNames.SuperMissiles,
        "Wavebuster": SpriteNames.WaveBeam,
        "Flamethrower": SpriteNames.PlasmaBeam,
        "Ice Spreader": SpriteNames.IceBeam,
        "Space Jump Boots": SpriteNames.SpaceJump,
        "Morph Ball": SpriteNames.MorphBall,
        "Varia Suit": SpriteNames.VariaSuit,
        "Gravity Suit": SpriteNames.GravitySuit,
        "Energy Tank": SpriteNames.EnergyTank,
        "Missile Launcher": SpriteNames.Missiles,
        "Power Bomb (Main)": SpriteNames.PowerBombs,
        "Charge Beam (Power)": SpriteNames.ChargeBeam,
        "Charge Beam (Wave)": SpriteNames.WaveBeam,
        "Charge Beam (Ice)": SpriteNames.IceBeam,
        "Charge Beam (Plasma)": SpriteNames.PlasmaBeam,
        "Progressive Power Beam": SpriteNames.ChargeBeam,
        "Progressive Ice Beam": SpriteNames.IceBeam,
        "Progressive Wave Beam": SpriteNames.WaveBeam,
        "Progressive Plasma Beam": SpriteNames.PlasmaBeam
    },
    "Super Metroid Map Rando": {
        "ETank": SpriteNames.EnergyTank,
        "Missile": SpriteNames.MissileTank,
        "Super": SpriteNames.SuperMissiles,
        "PowerBomb": SpriteNames.PowerBombTank,
        "Bombs": SpriteNames.Bombs,
        "Charge": SpriteNames.ChargeBeam,
        "Ice": SpriteNames.IceBeam,
        "HiJump": SpriteNames.HiJump,
        "SpeedBooster": SpriteNames.SpeedBooster,
        "Wave": SpriteNames.WaveBeam,
        "Spazer": SpriteNames.WideBeam,
        "Plasma": SpriteNames.PlasmaBeam,
        "SpringBall": SpriteNames.HiJump,
        "Varia": SpriteNames.VariaSuit,
        "Morph": SpriteNames.MorphBall,
        "ReserveTank": SpriteNames.EnergyTank,
        "Gravity": SpriteNames.GravitySuit,
        "SpaceJump": SpriteNames.SpaceJump,
        "ScrewAttack": SpriteNames.ScrewAttack
    },
    "Super Junkoid": {
        "Magic Bolt": SpriteNames.Missiles,  # (Consumable Charge Beam)
        "Baseball": SpriteNames.MissileTank, # (Missiles that become Super Missiles after obtaining Big League Glove)
        "Sparksuit": SpriteNames.PowerBombTank, # (Takes the Power Bomb slot but allows you to shinespark anywhere)
        "Rat Cloak": SpriteNames.MorphBall,
        "Wave Bangle": SpriteNames.ScrewAttack,
        "Rat Burst": SpriteNames.Bombs,
        "Feather": SpriteNames.HiJump,
        "Purple Locket": SpriteNames.VariaSuit,
        "Sanguine Fin": SpriteNames.GravitySuit,
        "Gem Of Ice": SpriteNames.IceBeam,
        "Gem Of Blood": SpriteNames.WaveBeam,
        "Gem Of Storms": SpriteNames.PlasmaBeam,
        "Gem Of Death": SpriteNames.ChargeBeam,
        "Rat Dasher": SpriteNames.SpeedBooster,
        "Dreamer's Crown": SpriteNames.SpeedBooster, # (Upgrade for Sparksuits that make you take no damage during the spark)
        "Wallkicks": SpriteNames.Empty, # Space Jump/Hi-Jump Boots?
        "Magic Broom": SpriteNames.SpaceJump,
        "Heart": SpriteNames.EnergyTank,
        "Lucky Frog": SpriteNames.EnergyTank,
        "Magic Soap": SpriteNames.MissileTank, # (Refills your Magic Bolts at Save Stations)
        "Big League Glove": SpriteNames.SuperMissiles, # (Turns Baseballs into Super Baseballs)
    }
}
