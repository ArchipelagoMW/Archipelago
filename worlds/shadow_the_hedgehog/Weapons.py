import copy
from dataclasses import dataclass

from BaseClasses import ItemClassification
from . import Levels, Options
from .Names import REGION_INDICIES

@dataclass
class WeaponInfo:
    game_id: int
    name: str
    available_stages: []
    power = 0
    base_ammo = 0
    
    def __init__(self, id, name, power, base_ammo,
                 stages, attributes):
        self.game_id = id
        self.power = power
        self.base_ammo = base_ammo
        self.name = "Weapon:"+name
        self.available_stages = stages
        self.attributes = attributes
        
    
class WeaponAttributes:
    SHOT = 1
    LONG_RANGE = 2
    VACUUM = 4
    TORCH = 8
    NOT_AIMABLE = 16
    HEAL = 32
    SPECIAL = 64
    SHADOW_RIFLE = 128
    EXPLOSION = 256
    LOCKON = 512


def GetAnyShadowBoxRegions():

    return [
        Levels.STAGE_WESTOPOLIS, Levels.STAGE_DIGITAL_CIRCUIT, Levels.STAGE_GLYPHIC_CANYON,
        Levels.STAGE_LETHAL_HIGHWAY,
        (Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_TORCH),
        (Levels.STAGE_PRISON_ISLAND, REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER),
        (Levels.STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_ZIP_WIRE), Levels.STAGE_CENTRAL_CITY, Levels.STAGE_THE_DOOM,
        Levels.STAGE_SKY_TROOPS, (Levels.STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_GUN), Levels.STAGE_DEATH_RUINS,
        (Levels.STAGE_THE_ARK,REGION_INDICIES.THE_ARK_BLACK_VOLT),
        (Levels.STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_PULLEY), Levels.STAGE_IRON_JUNGLE,
        Levels.STAGE_SPACE_GADGET, Levels.STAGE_LOST_IMPACT, Levels.STAGE_GUN_FORTRESS,
        (Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_AIR_SAUCER), Levels.STAGE_LAVA_SHELTER,
        (Levels.STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_ZIPWIRE),
        Levels.STAGE_FINAL_HAUNT, Levels.STAGE_THE_LAST_WAY
    ]

def GetRuleByWeaponRequirement(player, req, stage, regions):
    regions_use = []

    # Technicality not handled for weapons not carriable between regions
    # e.g. Melee weapons through some vehicles
    # Currently this never comes up

    if regions is not None:
        regions_use = copy.copy(regions)
        for region in regions_use:
            if region == 0:
                if 0 not in regions_use:
                    regions_use.append(0)
                continue
            p_regions = [l.fromRegions for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == stage
                         and l.regionIndex == region]

            if len(p_regions) != 1:
                #print("Unknown find", stage, region)
                continue

            if len(p_regions[0]) == 1:
                regions_use.extend([ p for p in p_regions[0] if p not in regions_use])

    elif stage is not None:
        p_regions = [ l.regionIndex for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == stage]
        if len(p_regions) == 0:
            regions_use = []
        else:
            regions_use = p_regions

    matches_items = [ w for w in WEAPON_INFO if (
            (req is None and len(w.attributes) > 0)
            or req in w.attributes or req == w.name) and
                len([ a for a in w.available_stages
                  if (stage is not None and type(a) is tuple and a[0] == stage and a[1] in regions_use)
                  or
                      (stage is None)
                  or
                      (stage is not None and type(a) is not tuple and a == stage)
                ]) > 0
                ]

    matches_groups = [ group[0] for group in WeaponGroups.items() if len([ x for x in group[1] if x in
                                                                           [m.game_id for m in matches_items]]) > 0]
    matches = []
    matches.extend([ x.name for x in matches_items])
    matches.extend(matches_groups)

    #print(stage, regions_use, matches)

    if len(matches) == 0:
        return None

    return lambda state, reqs=matches: state.has_any([m for m in reqs],player)


class WEAPONS:
    PISTOL = 0x1
    SUB_MACHINE_GUN = 0x2
    SEMI_AUTOMATIC_RIFLE = 0x3
    HEAVY_MACHINE_GUN = 0x4
    GATLING_GUN = 0x5
    EGG_GUN = 0x7
    LIGHT_SHOT = 0x8
    FLASH_SHOT = 0x9
    RING_SHOT = 0xA
    HEAVY_SHOT = 0xB
    GRENADE_LAUNCHER = 0xC
    BAZOOKA = 0xD
    TANK_CANNON = 0xE
    BLACK_BARREL = 0xF
    BIG_BARREL = 0x10
    EGG_BAZOOKA = 0x11
    RPG = 0x12
    FOUR_SHOT_RPG = 0x13
    EIGHT_SHOT_RPG = 0x14
    WORM_SHOOTER = 0x15
    WIDE_WORM_SHOOTER = 0x16
    BIG_WORM_SHOOTER = 0x17
    VACUUM_POD = 0x18
    LASER_RIFLE = 0x19
    SPLITTER = 0x1A
    REFRACTOR = 0x1B
    SURVIVAL_KNIFE = 0x1E
    BLACK_SWORD = 0x1F
    DARK_HAMMER = 0x20
    EGG_SPEAR = 0x21
    SPEED_LIMIT_SIGN = 0x22
    DIGITAL_POLE = 0x23
    CANYON_POLE = 0x24
    LETHAL_POLE = 0x25
    CRYPTIC_TORCH = 0x26
    PRISON_BRANCH = 0x27
    CIRCUS_POLE = 0x28
    STOP_SIGN = 0x29
    DOOM_POLE = 0x2A
    SKY_POLE = 0x2B
    MATRIX_POLE = 0x2C
    RUINS_BRANCH = 0x2D
    FLEET_POLE = 0x2F
    IRON_POLE = 0x30
    GADGET_POLE = 0x31
    IMPACT_POLE = 0x32
    FORTRESS_POLE = 0x33
    LAVA_SHOVEL = 0x35
    COSMIC_POLE = 0x36
    HAUNT_POLE = 0x37
    LAST_POLE = 0x38
    SAMURAI_BLADE = 0x3A
    SATELLITE_GUN = 0x3C
    EGG_VACUUM = 0x3E
    OMOCHAO_GUN = 0x40
    HEAL_CANNON = 0x42
    SHADOW_RIFLE = 0x43


WEAPON_INFO = [
    WeaponInfo(0x1, "Pistol", 2, 10,
               [Levels.STAGE_WESTOPOLIS,Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND,
                Levels.STAGE_CENTRAL_CITY, Levels.STAGE_THE_DOOM,
                (Levels.STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_PULLEY),
                Levels.STAGE_LOST_IMPACT, Levels.BOSS_BLACK_BULL_DR, Levels.BOSS_DIABLON_GF],
               [WeaponAttributes.SHOT]),
    WeaponInfo(0x2, "Sub Machine Gun", 2, 20,
               [Levels.STAGE_WESTOPOLIS,
                Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,Levels.STAGE_LETHAL_HIGHWAY,
                Levels.STAGE_PRISON_ISLAND,
                Levels.STAGE_CIRCUS_PARK, Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_THE_DOOM,
                Levels.STAGE_DEATH_RUINS,
                Levels.STAGE_LOST_IMPACT,
                Levels.BOSS_BLUE_FALCON,
                Levels.BOSS_BLACK_DOOM_GF, Levels.BOSS_BLACK_DOOM_CF],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x3, "Semi Automatic Rifle", 4, 20,
               [Levels.STAGE_LETHAL_HIGHWAY,
                    Levels.STAGE_PRISON_ISLAND, (Levels.STAGE_CIRCUS_PARK,REGION_INDICIES.CIRCUS_PARK_ROCKET_EASY),
                Levels.STAGE_CENTRAL_CITY,
                    Levels.STAGE_THE_DOOM,
                (Levels.STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_PULLEY),
                    Levels.STAGE_THE_ARK, Levels.STAGE_AIR_FLEET,
                (Levels.STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_GOLD_BEETLE),
                Levels.STAGE_SPACE_GADGET, Levels.STAGE_LOST_IMPACT,
                Levels.STAGE_GUN_FORTRESS, (Levels.STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_ZIPWIRE),
                Levels.BOSS_BLACK_DOOM_CF],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x4, "Heavy Machine Gun", 6, 30,
               [(Levels.STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_GUN_TURRET),
                (Levels.STAGE_CENTRAL_CITY,REGION_INDICIES.CENTRAL_CITY_GUN_TURRET),
                Levels.STAGE_THE_DOOM,
                (Levels.STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_GUN_TURRET),
                (Levels.STAGE_THE_ARK,REGION_INDICIES.THE_ARK_BLACK_VOLT),
                (Levels.STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_PULLEY),
                Levels.STAGE_SPACE_GADGET,
                (Levels.STAGE_GUN_FORTRESS,REGION_INDICIES.GUN_FORTRESS_GUN_TURRET),
                (Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_WARP_HOLE),
                (Levels.STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL),
                Levels.BOSS_EGG_BREAKER_IJ],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x5, "Gatling Gun", 6, 40,
               [(Levels.STAGE_LETHAL_HIGHWAY, REGION_INDICIES.LETHAL_HIGHWAY_KEY_DOOR),
                   (Levels.STAGE_THE_ARK,REGION_INDICIES.THE_ARK_BLACK_VOLT),
                (Levels.STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_ROCKET), Levels.STAGE_GUN_FORTRESS,
                (Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_AIR_SAUCER)],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x7, "Egg Gun", 2, 20,
               [(Levels.STAGE_CRYPTIC_CASTLE,1), Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
                Levels.STAGE_MAD_MATRIX, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER,
                Levels.BOSS_EGG_BREAKER_CC, Levels.BOSS_EGG_BREAKER_MM,
                Levels.BOSS_EGG_BREAKER_IJ, Levels.BOSS_EGG_DEALER_BC,
                Levels.BOSS_EGG_DEALER_LS, Levels.BOSS_EGG_DEALER_CF],
        [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x8, "Light Shot", 2, 20,
                [Levels.STAGE_WESTOPOLIS,
                Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_LETHAL_HIGHWAY,
                 (Levels.STAGE_CRYPTIC_CASTLE,REGION_INDICIES.CRYPTIC_CASTLE_HAWK), Levels.STAGE_PRISON_ISLAND,
                Levels.STAGE_CENTRAL_CITY, Levels.STAGE_DEATH_RUINS,
                 (Levels.STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_ZIPWIRE),
                 Levels.BOSS_BLACK_BULL_LH, Levels.BOSS_BLACK_BULL_DR, Levels.BOSS_DIABLON_BC],
            [WeaponAttributes.SHOT]),
    WeaponInfo(0x9, "Flash Shot", 2, 20,
               [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON,
                Levels.STAGE_LETHAL_HIGHWAY, (Levels.STAGE_CRYPTIC_CASTLE,REGION_INDICIES.CRYPTIC_CASTLE_HAWK),
                Levels.STAGE_PRISON_ISLAND, Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_DEATH_RUINS, Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_BLACK_COMET, Levels.BOSS_DIABLON_BC, Levels.BOSS_BLACK_BULL_LH,
               Levels.BOSS_DIABLON_FH, Levels.BOSS_BLACK_DOOM_FH],
               [WeaponAttributes.SHOT]),
    WeaponInfo(0xA, "Ring Shot", 4, 20,
           [Levels.STAGE_SKY_TROOPS, Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_FINAL_HAUNT, Levels.BOSS_DIABLON_BC,
            Levels.BOSS_DIABLON_FH, Levels.BOSS_BLACK_DOOM_FH,
            Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.SHOT]),
    WeaponInfo(0xB, "Heavy Shot", 5, 20,
               [(Levels.STAGE_FINAL_HAUNT,REGION_INDICIES.FINAL_HAUNT_ROCKET_NORMAL),
                (Levels.STAGE_THE_LAST_WAY,REGION_INDICIES.THE_LAST_WAY_BLACK_VOLT)],
               [WeaponAttributes.SHOT]),
    WeaponInfo(0xC, "Grenade Launcher", 4, 10,
               [Levels.STAGE_GLYPHIC_CANYON, (Levels.STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_BOMBS),
                (Levels.STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_WALLS),
                (Levels.STAGE_SPACE_GADGET,REGION_INDICIES.SPACE_GADGET_AIR_SAUCER),
                Levels.STAGE_LOST_IMPACT, Levels.BOSS_BLACK_DOOM_GF],
    [WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(0xD, "Bazooka", 8, 5,
               [Levels.STAGE_CENTRAL_CITY, (Levels.STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_PULLEY),
                (Levels.STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_AIR_SAUCER), #
                (Levels.STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL),
                Levels.BOSS_BLACK_DOOM_CF],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(0xE, "Tank Cannon", 16, 5,
               [(Levels.STAGE_PRISON_ISLAND, REGION_INDICIES.PRISON_ISLAND_KEY_DOOR),
                (Levels.STAGE_IRON_JUNGLE,REGION_INDICIES.IRON_JUNGLE_KEY_DOOR),
                (Levels.STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_BEHIND_KEY_DOOR)],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(0xF, "Black Barrel", 4, 5,
               [(Levels.STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_ROCKET_NORMAL),
                (Levels.STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_AIR_SAUCER),
    (Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_BLACK_TURRET),
                Levels.STAGE_FINAL_HAUNT,Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(0x10, "Big Barrel", 8, 5,
               [(Levels.STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL),
                Levels.STAGE_FINAL_HAUNT,
                Levels.BOSS_BLACK_DOOM_FH,Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(0x11, "Egg Bazooka", 8, 5,
               [(Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_TORCH),
                (Levels.STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_ROCKET_EASY),
                Levels.STAGE_SKY_TROOPS,
                (Levels.STAGE_MAD_MATRIX,REGION_INDICIES.MAD_MATRIX_GUN),
                Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER,
                Levels.BOSS_EGG_BREAKER_MM, Levels.BOSS_EGG_BREAKER_IJ,
                Levels.BOSS_EGG_DEALER_BC, Levels.BOSS_EGG_DEALER_LS, Levels.BOSS_EGG_DEALER_CF],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(0x12, "RPG", 6, 10,
               [(Levels.STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_BOMBS),
                Levels.STAGE_THE_ARK,
                Levels.STAGE_GUN_FORTRESS],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x13, "4-Shot RPG", 8, 10,
               [(Levels.STAGE_THE_ARK,REGION_INDICIES.THE_ARK_BLACK_VOLT),
                Levels.STAGE_IRON_JUNGLE, Levels.STAGE_SPACE_GADGET,
                Levels.BOSS_HEAVY_DOG, Levels.BOSS_BLUE_FALCON,
                Levels.BOSS_BLACK_DOOM_GF, Levels.BOSS_BLACK_DOOM_CF],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x14, "8-Shot RPG", 8, 10,
               [Levels.STAGE_GUN_FORTRESS, (Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_AIR_SAUCER)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x15, "Worm Shooter", 6, 5,
               [Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,
                (Levels.STAGE_PRISON_ISLAND,REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER),
                (Levels.STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_GUN),
                (Levels.STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_WALLS),
                (Levels.STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_AIR_SAUCER)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x16, "Wide Worm Shooter", 8, 5,
               [(Levels.STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_YELLOW_ENTRY),
                (Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_FLOATERS),
                Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x17, "Big Worm Shooter", 16, 5,
               [(Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_FLOATERS),
                (Levels.STAGE_THE_LAST_WAY,REGION_INDICIES.THE_LAST_WAY_VOLT_OR_WARP)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(0x18, "Vacuum Pod", None, 20,
               [Levels.STAGE_CENTRAL_CITY,
                (Levels.STAGE_SPACE_GADGET,REGION_INDICIES.SPACE_GADGET_AIR_SAUCER),
                Levels.STAGE_FINAL_HAUNT],
[WeaponAttributes.VACUUM]),
    WeaponInfo(0x19, "Laser Rifle", 3, 20,
               [(Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_AIR_SAUCER)],
[WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x1A, "Splitter", 4, 20,
               [(Levels.STAGE_DEATH_RUINS,REGION_INDICIES.DEATH_RUINS_PULLEY), Levels.STAGE_AIR_FLEET,
                (Levels.STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_AIR_SAUCER), Levels.STAGE_GUN_FORTRESS],
[WeaponAttributes.SHOT]),
    WeaponInfo(0x1B, "Refractor", 5, 20,
               [(Levels.STAGE_BLACK_COMET,REGION_INDICIES.BLACK_COMET_AIR_SAUCER),Levels.STAGE_FINAL_HAUNT,
                Levels.BOSS_BLACK_DOOM_FH, Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x1E, "Survival Knife", 2, 5,
               [Levels.STAGE_THE_DOOM],
[]),
    WeaponInfo(0x1F, "Black Sword", 4, 5,
               [Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,
                (Levels.STAGE_CRYPTIC_CASTLE,REGION_INDICIES.CRYPTIC_CASTLE_TORCH),
                (Levels.STAGE_PRISON_ISLAND,REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER), Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_SKY_TROOPS, Levels.STAGE_AIR_FLEET,
                Levels.STAGE_FINAL_HAUNT, Levels.STAGE_THE_LAST_WAY],
[]),
    WeaponInfo(0x20, "Dark Hammer", 6, 5,
               [Levels.STAGE_FINAL_HAUNT,
                (Levels.STAGE_THE_LAST_WAY,REGION_INDICIES.THE_LAST_WAY_LIGHT_DASH_EASY)],
[]),
    WeaponInfo(0x21, "Egg Spear", 2, 4,
               [Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CIRCUS_PARK,
                (Levels.STAGE_SKY_TROOPS,REGION_INDICIES.SKY_TROOPS_ROCKET_NORMAL),
                Levels.STAGE_MAD_MATRIX, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER,
                Levels.BOSS_EGG_DEALER_BC, Levels.BOSS_EGG_DEALER_LS,
                Levels.BOSS_EGG_DEALER_CF],
[]),

    WeaponInfo(0x22, "Speed Limit Sign",2, 4,
                   [Levels.STAGE_WESTOPOLIS],
    []),

    WeaponInfo(0x23, "Digital Pole",2, 4,
               [Levels.STAGE_DIGITAL_CIRCUIT],
[]),
    WeaponInfo(0x24, "Canyon Pole",2, 4,
               [Levels.STAGE_GLYPHIC_CANYON],
[]),

    WeaponInfo(0x25, "Lethal Pole",2, 4,
               [(Levels.STAGE_LETHAL_HIGHWAY, REGION_INDICIES.LETHAL_HIGHWAY_ROCKET)],
[]),

    WeaponInfo(0x26, "Cryptic Torch",2, 4,
               [(Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_BALLOON)],
            [WeaponAttributes.TORCH]),
    WeaponInfo(0x27, "Prison Branch",2, 4,
               [Levels.STAGE_PRISON_ISLAND],
[]),
    WeaponInfo(0x28, "Circus Pole",2, 4,
               [Levels.STAGE_CIRCUS_PARK],
[]),

 WeaponInfo(0x29, "Stop Sign",2, 4,
               [Levels.STAGE_CENTRAL_CITY],
[]),

    WeaponInfo(0x2A, "Doom Pole",2, 4,
               [Levels.STAGE_THE_DOOM],
[]),

    WeaponInfo(0x2B, "Sky Pole",2, 4,
               [Levels.STAGE_SKY_TROOPS],
[]),

    WeaponInfo(0x2C, "Matrix Pole",2, 4,
               [(Levels.STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_GUN)], []),

    WeaponInfo(0x2D, "Ruins Branch",2, 4,
               [Levels.STAGE_DEATH_RUINS],
[]),
    WeaponInfo(0x2F, "Fleet Pole",2, 4,
               [(Levels.STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_PULLEY)],
[]),
    WeaponInfo(0x30, "Iron Pole",2, 4,
               [Levels.STAGE_IRON_JUNGLE],
[]),
    WeaponInfo(0x31, "Gadget Pole",2, 4,
               [Levels.STAGE_SPACE_GADGET],
[]),
    WeaponInfo(0x32, "Impact Pole",2, 4,
               [Levels.STAGE_LOST_IMPACT],
[]),
    WeaponInfo(0x33, "Fortress Pole",2, 4,
               [Levels.STAGE_GUN_FORTRESS],
[]),

    WeaponInfo(0x35, "Lava Shovel",2, 4,
               [Levels.STAGE_LAVA_SHELTER],
[]),
    WeaponInfo(0x36, "Cosmic Pole",2, 4,
               [(Levels.STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_ZIPWIRE)],
[]),
    WeaponInfo(0x37, "Haunt Pole",2, 4,
               [Levels.STAGE_FINAL_HAUNT],
[]),
    WeaponInfo(0x38, "Last Pole",2, 4,
               [Levels.STAGE_THE_LAST_WAY],
[]),

    WeaponInfo(0x3A, "Samurai Blade", 8, 6,
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL]),
    WeaponInfo(0x3C, "Satellite Gun", 18, 6,
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.NOT_AIMABLE,WeaponAttributes.LOCKON]),
    WeaponInfo(0x3E, "Egg Vacuum", None, 20,
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.VACUUM]),
    WeaponInfo(0x40, "Omochao Gun", 10, 10,
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x42, "Heal Cannon", None, 10,
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.HEAL]),
    WeaponInfo(0x43, "Shadow Rifle", 32, 20,
               GetAnyShadowBoxRegions(),
[WeaponAttributes.SPECIAL, WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE, WeaponAttributes.SHADOW_RIFLE])
]

def GetWeaponDict():
    weapon_dict = {}
    for weapon in WEAPON_INFO:
        weapon_dict[weapon.name] = weapon

    return weapon_dict

def GetWeaponDictById():
    weapon_dict = {}
    for weapon in WEAPON_INFO:
        weapon_dict[weapon.game_id] = weapon

    return weapon_dict

def GetWeaponGroupsDict():
    weapons = GetWeaponDictById()
    weapon_groups_dict = {}
    for group in WeaponGroups.items():
        weapon_groups_dict[group[0]] = []
        for item in group[1]:
            weapon_item = weapons[item]
            weapon_groups_dict[group[0]].append(weapon_item)

    return weapon_groups_dict


def GetWeaponByStageDict():
    stages_dict = {}
    for Weapon in WEAPON_INFO:
        for stage in Weapon.available_stages:
            stage_n = stage if type(stage) is int else stage[0]
            if stage_n not in stages_dict:
                stages_dict[stage_n] = []
            if WeaponAttributes.SPECIAL in Weapon.attributes:
                continue
            stages_dict[stage_n].append(Weapon.game_id)

    return stages_dict

def WeaponInfoByWeapon():
    stages_dict = {}
    for Weapon in WEAPON_INFO:
        print("###", Weapon.name.replace("Weapon:", ""), ":", Weapon.game_id, "\n * ",
              "\n * ".join([ Levels.LEVEL_ID_TO_LEVEL[x] if type(x) is int else Levels.LEVEL_ID_TO_LEVEL[x[0]]+"-"+str(x[1])
                for x in Weapon.available_stages]), "\n\n")
        for stage in Weapon.available_stages:
            stage_n = Levels.LEVEL_ID_TO_LEVEL[stage] if type(stage) is int else Levels.LEVEL_ID_TO_LEVEL[stage[0]]+"-"+str(stage[1])
            if stage_n not in stages_dict:
                stages_dict[stage_n] = []
            if WeaponAttributes.SPECIAL in Weapon.attributes:
                continue
            stages_dict[stage_n].append(Weapon)

    to_order = []
    for stage,weapons in stages_dict.items():
        to_order.append((stage, weapons))

    inv_map = {v: k for k, v in Levels.LEVEL_ID_TO_LEVEL.items()}
    to_order.sort(key= lambda x: inv_map[x[0].split("-")[0]])

    for stage,weapons in to_order:
        print("### ", stage, "\n *", "\n * ".join([w.name.replace("Weapon:", "") for w in weapons]), "\n\n")


    pass

#WeaponInfoByWeapon()

def GetWeaponByName(name):
    weapon = [ w for w in WEAPON_INFO if w.name == name]
    if len(weapon)  == 0:
        return None

    return weapon[0]

WeaponGroups = {

    "Stage Melee Weapons": [WEAPONS.SPEED_LIMIT_SIGN, WEAPONS.DIGITAL_POLE, WEAPONS.CANYON_POLE, WEAPONS.LETHAL_POLE,
                    WEAPONS.PRISON_BRANCH, WEAPONS.CIRCUS_POLE, WEAPONS.STOP_SIGN, WEAPONS.DOOM_POLE,
                    WEAPONS.SKY_POLE, WEAPONS.MATRIX_POLE, WEAPONS.RUINS_BRANCH, WEAPONS.FLEET_POLE,
                    WEAPONS.IRON_POLE, WEAPONS.GADGET_POLE, WEAPONS.IMPACT_POLE, WEAPONS.FORTRESS_POLE,
                    WEAPONS.LAVA_SHOVEL, WEAPONS.COSMIC_POLE, WEAPONS.HAUNT_POLE, WEAPONS.LAST_POLE],

    "Environment Weapons": [WEAPONS.SPEED_LIMIT_SIGN, WEAPONS.DIGITAL_POLE, WEAPONS.CANYON_POLE, WEAPONS.LETHAL_POLE,
                    WEAPONS.PRISON_BRANCH, WEAPONS.CIRCUS_POLE, WEAPONS.STOP_SIGN, WEAPONS.DOOM_POLE,
                    WEAPONS.SKY_POLE, WEAPONS.MATRIX_POLE, WEAPONS.RUINS_BRANCH, WEAPONS.FLEET_POLE,
                    WEAPONS.IRON_POLE, WEAPONS.GADGET_POLE, WEAPONS.IMPACT_POLE, WEAPONS.FORTRESS_POLE,
                    WEAPONS.LAVA_SHOVEL, WEAPONS.COSMIC_POLE, WEAPONS.HAUNT_POLE, WEAPONS.LAST_POLE, WEAPONS.CRYPTIC_TORCH],

    "Egg Pawn Weapons": [WEAPONS.EGG_GUN, WEAPONS.EGG_SPEAR, WEAPONS.EGG_BAZOOKA],

    "GUN Launcher Weapons": [WEAPONS.RPG, WEAPONS.FOUR_SHOT_RPG, WEAPONS.EIGHT_SHOT_RPG, WEAPONS.BAZOOKA,
                             WEAPONS.TANK_CANNON],

    "Black Warrior Weapons": [WEAPONS.FLASH_SHOT, WEAPONS.LIGHT_SHOT, WEAPONS.HEAVY_SHOT, WEAPONS.RING_SHOT,
                              WEAPONS.BLACK_SWORD],

    "Black Oak Weapons": [WEAPONS.BLACK_SWORD, WEAPONS.BLACK_BARREL, WEAPONS.BIG_BARREL,
                          WEAPONS.DARK_HAMMER],

    "Worm Weapons": [WEAPONS.WORM_SHOOTER, WEAPONS.WIDE_WORM_SHOOTER, WEAPONS.BIG_WORM_SHOOTER],

    "Gun Soldier Weapons": [WEAPONS.PISTOL, WEAPONS.GRENADE_LAUNCHER, WEAPONS.SURVIVAL_KNIFE,
                            WEAPONS.SUB_MACHINE_GUN],

    "Gun Mech Weapons": [WEAPONS.SEMI_AUTOMATIC_RIFLE, WEAPONS.LASER_RIFLE, WEAPONS.HEAVY_MACHINE_GUN,
                         WEAPONS.SUB_MACHINE_GUN, WEAPONS.GATLING_GUN],

    "Laser Weapons": [WEAPONS.REFRACTOR, WEAPONS.LASER_RIFLE, WEAPONS.SPLITTER, WEAPONS.RING_SHOT],

    "Standard Melee Weapons": [WEAPONS.SURVIVAL_KNIFE, WEAPONS.BLACK_SWORD, WEAPONS.DARK_HAMMER],

    "All Melee Weapons": [WEAPONS.SPEED_LIMIT_SIGN, WEAPONS.DIGITAL_POLE, WEAPONS.CANYON_POLE, WEAPONS.LETHAL_POLE,
                    WEAPONS.PRISON_BRANCH, WEAPONS.CIRCUS_POLE, WEAPONS.STOP_SIGN, WEAPONS.DOOM_POLE,
                    WEAPONS.SKY_POLE, WEAPONS.MATRIX_POLE, WEAPONS.RUINS_BRANCH, WEAPONS.FLEET_POLE,
                    WEAPONS.IRON_POLE, WEAPONS.GADGET_POLE, WEAPONS.IMPACT_POLE, WEAPONS.FORTRESS_POLE,
                    WEAPONS.LAVA_SHOVEL, WEAPONS.COSMIC_POLE, WEAPONS.HAUNT_POLE, WEAPONS.LAST_POLE, WEAPONS.CRYPTIC_TORCH,
                          WEAPONS.SURVIVAL_KNIFE, WEAPONS.BLACK_SWORD, WEAPONS.DARK_HAMMER]

}


def GetWeaponClassification(world, weapon : WeaponInfo):
    if world.options.weapon_sanity_hold == Options.WeaponsanityHold.option_unlocked:
        return ItemClassification.progression

    if WeaponAttributes.SPECIAL in weapon.attributes and world.options.weapon_sanity_hold:
        return ItemClassification.progression

    # technically need to check if item is required for any regions
    # skip over this issue for now
    # but an issue with easy logic Gold Beetle (Vacuum)
    # and hard logic Doom (Satelitte)
    # and Shadow Rifle for easy craft logic

    if WeaponAttributes.SPECIAL in weapon.attributes:
        return ItemClassification.progression

    if len(weapon.attributes) == 0:
        return ItemClassification.filler

    # Could be more in-depth
    if world.options.weapon_sanity_unlock:
        return ItemClassification.progression

    return ItemClassification.useful


