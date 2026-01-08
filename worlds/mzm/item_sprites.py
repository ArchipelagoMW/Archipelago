from typing import Mapping

from BaseClasses import Item

from .patcher.sprites import Sprite


unknown_item_alt_sprites: Mapping[str, str] = {
    "Plasma Beam": Sprite.UnknownPlasmaBeam,
    "Space Jump": Sprite.UnknownSpaceJump,
    "Gravity Suit": Sprite.UnknownGravitySuit,
}


compatible_games: Mapping[str, Mapping[str, str]] = {
    "Super Metroid": {
        "Energy Tank": Sprite.EnergyTank,
        "Missile": Sprite.MissileTank,
        "Super Missile": Sprite.SuperMissileTank,
        "Power Bomb": Sprite.PowerBombTank,
        "Bomb": Sprite.Bomb,
        "Charge Beam": Sprite.ChargeBeam,
        "Ice Beam": Sprite.IceBeam,
        "Hi-Jump Boots": Sprite.HiJump,
        "Speed Booster": Sprite.SpeedBooster,
        "Wave Beam": Sprite.WaveBeam,
        "Spazer": Sprite.SpazerBeam,
        "Spring Ball": Sprite.SpringBall,
        "Varia Suit": Sprite.VariaSuit,
        "Plasma Beam": Sprite.PlasmaBeam,
        "Grappling Beam": Sprite.GrappleBeam,
        "Morph Ball": Sprite.MorphBall,
        "Reserve Tank": Sprite.ReserveTank,
        "Gravity Suit": Sprite.GravitySuit,
        "X-Ray Scope": Sprite.XRayScope,
        "Space Jump": Sprite.SpaceJump,
        "Screw Attack": Sprite.ScrewAttack,
    },
    "SMZ3": {
        "Missile": Sprite.MissileTank,
        "Super": Sprite.SuperMissileTank,
        "PowerBomb": Sprite.PowerBombTank,
        "Grapple": Sprite.GrappleBeam,
        "XRay": Sprite.XRayScope,
        "ETank": Sprite.EnergyTank,
        "ReserveTank": Sprite.ReserveTank,
        "Charge": Sprite.ChargeBeam,
        "Ice": Sprite.IceBeam,
        "Wave": Sprite.WaveBeam,
        "Spazer": Sprite.SpazerBeam,
        "Plasma": Sprite.PlasmaBeam,
        "Varia": Sprite.VariaSuit,
        "Gravity": Sprite.GravitySuit,
        "Morph": Sprite.MorphBall,
        "Bombs": Sprite.Bomb,
        "SpringBall": Sprite.SpringBall,
        "ScrewAttack": Sprite.ScrewAttack,
        "HiJump": Sprite.HiJump,
        "SpaceJump": Sprite.SpaceJump,
        "SpeedBooster": Sprite.SpeedBooster,
        # "CardCrateriaL1":
        # "CardCrateriaL2":
        # "CardCrateriaBoss":
        # "CardBrinstarL1":
        # "CardBrinstarL2":
        # "CardBrinstarBoss":
        # "CardNorfairL1":
        # "CardNorfairL2":
        # "CardNorfairBoss":
        # "CardMaridiaL1":
        # "CardMaridiaL2":
        # "CardMaridiaBoss":
        # "CardWreckedShipL1":
        # "CardWreckedShipBoss":
        # "CardLowerNorfairL1":
        # "CardLowerNorfairBoss":
    },
    "Metroid Fusion": {
        "Nothing": Sprite.Nothing,
        # "Level 0 Keycard":
        # "Missile Data":
        "Morph Ball": Sprite.MorphBall,
        "Charge Beam": Sprite.ChargeBeam,
        # "Level 1 Keycard":
        "Bomb Data": Sprite.Bomb,
        "Hi-Jump": Sprite.HiJump,
        "Speed Booster": Sprite.SpeedBooster,
        # "Level 2 Keycard":
        # "Super Missile":
        "Varia Suit": Sprite.VariaSuit,
        # "Level 3 Keycard":
        # "Ice Missile":
        "Wide Beam": Sprite.SpazerBeam,
        # "Power Bomb Data":
        "Space Jump": Sprite.SpaceJump,
        "Plasma Beam": Sprite.PlasmaBeam,
        "Gravity Suit": Sprite.GravitySuit,
        # "Level 4 Keycard":
        # "Diffusion Missile":
        "Wave Beam": Sprite.WaveBeam,
        "Screw Attack": Sprite.ScrewAttack,
        "Ice Beam": Sprite.IceBeam,
        "Missile Tank": Sprite.MissileTank,
        "Energy Tank": Sprite.EnergyTank,
        "Power Bomb Tank": Sprite.PowerBombTank,
        # "Ice Trap":
        # "Infant Metroid":
    },
    "Metroid Prime": {
        "Power Beam": Sprite.PowerBeam,
        "Ice Beam": Sprite.IceBeam,
        "Wave Beam": Sprite.WaveBeam,
        "Plasma Beam": Sprite.PlasmaBeam,
        "Missile Expansion": Sprite.MissileTank,
        # "Scan Visor":
        "Morph Ball Bomb": Sprite.Bomb,
        "Power Bomb Expansion": Sprite.PowerBombTank,
        # "Flamethrower":
        # "Thermal Visor":
        "Charge Beam": Sprite.ChargeBeam,
        # "Super Missile":
        "Grapple Beam": Sprite.GrappleBeam,
        # "X-Ray Visor":
        # "Ice Spreader":
        "Space Jump Boots": Sprite.SpaceJump,
        "Morph Ball": Sprite.MorphBall,
        # "Boost Ball":
        "Spider Ball": Sprite.SpiderBall,
        "Gravity Suit": Sprite.GravitySuit,
        "Varia Suit": Sprite.VariaSuit,
        # "Phazon Suit":
        "Energy Tank": Sprite.EnergyTank,
        # "Wavebuster":
        # "Missile Launcher":
        # "Power Bomb (Main)":
        "Progressive Power Beam": Sprite.PowerBeam,
        "Progressive Ice Beam": Sprite.IceBeam,
        "Progressive Wave Beam": Sprite.WaveBeam,
        "Progressive Plasma Beam": Sprite.PlasmaBeam,
    },
    "Super Metroid Map Rando": {
        "ETank": Sprite.EnergyTank,
        "Missile": Sprite.MissileTank,
        "Super": Sprite.SuperMissileTank,
        "PowerBomb": Sprite.PowerBombTank,
        "Bombs": Sprite.Bomb,
        "Charge": Sprite.ChargeBeam,
        "Ice": Sprite.IceBeam,
        "HiJump": Sprite.HiJump,
        "SpeedBooster": Sprite.SpeedBooster,
        "Wave": Sprite.WaveBeam,
        "Spazer": Sprite.SpazerBeam,
        "SpringBall": Sprite.SpringBall,
        "Varia": Sprite.VariaSuit,
        "Gravity": Sprite.GravitySuit,
        "XRayScope": Sprite.XRayScope,
        "Plasma": Sprite.PlasmaBeam,
        "Grapple": Sprite.GrappleBeam,
        "SpaceJump": Sprite.SpaceJump,
        "ScrewAttack": Sprite.ScrewAttack,
        "Morph": Sprite.MorphBall,
        "ReserveTank": Sprite.ReserveTank,
        "WallJump": Sprite.WallJump,
    },
}


def get_zero_mission_sprite(item: Item) -> str | None:
    if item.game not in compatible_games:
        return None

    return compatible_games[item.game].get(item.name)
