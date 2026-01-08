from .Items import *

_DEFAULT_NANO_XP_TABLE: list[int] = [
    0x00B4, 0x00D2, 0x00F0, 0x010E, 0x012C, 0x014A, 0x0168, 0x0186,
    0x01A4, 0x01C2, 0x01E0, 0x01F4, 0x0208, 0x0208, 0x0208, 0x0208,
    0x0208, 0x0208, 0x0208, 0x0208, 0x0208, 0x0212, 0x0212, 0x0230,
    0x0244, 0x0258, 0x026C, 0x0280, 0x0294, 0x02A8, 0x02BC, 0x02D0,
    0x02E4, 0x02F8, 0x030C, 0x0320, 0x0348, 0x032A, 0x03B1, 0x0438,
    0x04BF, 0x0546, 0x05CD, 0x0654, 0x06DB, 0x0762, 0x07E9, 0x0870,
    0x08CA, 0x0924, 0x0924, 0x0924, 0x0924, 0x0924, 0x0924, 0x0924,
    0x0924, 0x0924, 0x0951, 0x09AB, 0x09D8, 0x0A32, 0x0A8C, 0x0AE6,
    0x0B40, 0x0BB8
]


def get_nanotech_xp_table(xp_factor: float):
    return [int(xp * xp_factor) for xp in _DEFAULT_NANO_XP_TABLE]


_WEAPON_UPGRADES = {
    CLANK_ZAPPER.offset: (0x09C4, CLANK_SHOCKER.offset),
    SHEEPINATOR.offset: (0x0384, BLACK_SHEEPINATOR.offset),
    CHOPPER.offset: (0x0190, MULTISTAR.offset),
    PULSE_RIFLE.offset: (0x0096, VAPORIZER.offset),
    SEEKER_GUN.offset: (0x041A, HK_22.offset),
    HOVERBOMB_GUN.offset: (0x0DAC, TETRABOMB_GUN.offset),
    BLITZ_GUN.offset: (0x02EE, BLITZ_CANNON.offset),
    MINIROCKET_TUBE.offset: (0x0FA0, MEGAROCKET_CANNON.offset),
    PLASMA_COIL.offset: (0x0834, PLASMA_STORM.offset),
    LAVA_GUN.offset: (0x0578, METEOR_GUN.offset),
    LANCER.offset: (0x0118, HEAVY_LANCER.offset),
    SYNTHENOID.offset: (0x04B0, KILONOID.offset),
    SPIDERBOT_GLOVE.offset: (0x03E8, TANKBOT_GLOVE.offset),
    BOUNCER.offset: (0x06A4, HEAVY_BOUNCER.offset),
    MINITURRET_GLOVE.offset: (0x02EE, MEGATURRET_GLOVE.offset),
    GRAVITY_BOMB.offset: (0x00C8, MINI_NUKE.offset),
    SHIELD_CHARGER.offset: (0x01C2, TESLA_BARRIER.offset),

    MEGA_HEAVY_LANCER.offset: (0x1F40, ULTRA_HEAVY_LANCER.offset),
    MEGA_MINI_NUKE.offset: (0x2EE0, ULTRA_MINI_NUKE.offset),
    MEGA_MULTISTAR.offset: (0x1388, ULTRA_MULTISTAR.offset),
    MEGA_HK_22.offset: (0x2968, ULTRA_HK_22.offset),
    MEGA_VAPORIZER.offset: (0x1130, ULTRA_VAPORIZER.offset),
    MEGA_MEGATURRET_GLOVE.offset: (0x1770, ULTRA_MEGATURRET_GLOVE.offset),
    MEGA_BLITZ_CANNON.offset: (0x1B58, ULTRA_BLITZ_CANNON.offset),
    MEGA_KILONOID.offset: (0x0FA0, ULTRA_KILONOID.offset),
    MEGA_METEOR_GUN.offset: (0x0FA0, ULTRA_METEOR_GUN.offset),
    MEGA_HEAVY_BOUNCER.offset: (0x1388, ULTRA_HEAVY_BOUNCER.offset),
    MEGA_MEGAROCKET_CANNON.offset: (0x1F40, ULTRA_MEGAROCKET_CANNON.offset),
    MEGA_PLASMA_STORM.offset: (0x1F40, ULTRA_PLASMA_STORM.offset),
    MEGA_TETRABOMB_GUN.offset: (0x2710, ULTRA_TETRABOMB_GUN.offset),
    MEGA_TANKBOT_GLOVE.offset: (0x1F40, ULTRA_TANKBOT_GLOVE.offset),
    MEGA_TESLA_BARRIER.offset: (0x1770, ULTRA_TESLA_BARRIER.offset),
}

_EXTENDED_UPGRADES = {
    HEAVY_LANCER.offset: (LANCER, MEGA_HEAVY_LANCER),
    MINI_NUKE.offset: (GRAVITY_BOMB, MEGA_MINI_NUKE),
    MULTISTAR.offset: (CHOPPER, MEGA_MULTISTAR),
    HK_22.offset: (SEEKER_GUN, MEGA_HK_22),
    VAPORIZER.offset: (PULSE_RIFLE, MEGA_VAPORIZER),
    MEGATURRET_GLOVE.offset: (MINITURRET_GLOVE, MEGA_MEGATURRET_GLOVE),
    BLITZ_CANNON.offset: (BLITZ_GUN, MEGA_BLITZ_CANNON),
    KILONOID.offset: (SYNTHENOID, MEGA_KILONOID),
    METEOR_GUN.offset: (LAVA_GUN, MEGA_METEOR_GUN),
    HEAVY_BOUNCER.offset: (BOUNCER, MEGA_HEAVY_BOUNCER),
    MEGAROCKET_CANNON.offset: (MINIROCKET_TUBE, MEGA_MEGAROCKET_CANNON),
    PLASMA_STORM.offset: (PLASMA_COIL, MEGA_PLASMA_STORM),
    TETRABOMB_GUN.offset: (HOVERBOMB_GUN, MEGA_TETRABOMB_GUN),
    TANKBOT_GLOVE.offset: (SPIDERBOT_GLOVE, MEGA_TANKBOT_GLOVE),
    TESLA_BARRIER.offset: (SHIELD_CHARGER, MEGA_TESLA_BARRIER),

    TESLA_CLAW.offset: (TESLA_CLAW, MEGA_TESLA_CLAW),
    BOMB_GLOVE.offset: (BOMB_GLOVE, MEGA_BOMB_GLOVE),
    WALLOPER.offset: (WALLOPER, MEGA_WALLOPER),
    VISIBOMB_GUN.offset: (VISIBOMB_GUN, MEGA_VISIBOMB_GUN),
    DECOY_GLOVE.offset: (DECOY_GLOVE, MEGA_DECOY_GLOVE),
}


def get_weapon_upgrades_table(xp_factor: float, extend_weapon_progression: bool):
    weapon_upgrades = {
        weapon_id: (int(xp * xp_factor), upgraded_id)
        for weapon_id, (xp, upgraded_id) in _WEAPON_UPGRADES.items()
    }
    if extend_weapon_progression:
        for lv2_weapon_id, (lv1_weapon, lv3_weapon) in _EXTENDED_UPGRADES.items():
            lv2_required_xp, _ = weapon_upgrades.get(lv1_weapon.offset, (None, None))
            lv4_required_xp, lv4_weapon = weapon_upgrades.get(lv3_weapon.offset, (None, None))
            if lv2_required_xp is not None and lv4_required_xp is not None:
                # Lv3 required XP is the median between Lv2 and Lv4
                lv3_required_xp = lv2_required_xp + int(lv4_required_xp * 0.5)
                # In vanilla game, weapon XP gets reset when buying the Lv3 variant from shop.
                # To compensate for this, we add Lv3 required XP to the value required to get Lv4
                lv4_required_xp += lv3_required_xp
                weapon_upgrades[lv3_weapon.offset] = (lv4_required_xp, lv4_weapon)
            else:
                # RaC1 weapons case: no XP-based upgrade exist in vanilla for those, invent an XP value that feels right
                lv3_required_xp = int(0x600 * xp_factor)
            weapon_upgrades[lv2_weapon_id] = (lv3_required_xp, lv3_weapon.offset)
    return weapon_upgrades
