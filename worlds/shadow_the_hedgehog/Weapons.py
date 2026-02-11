from dataclasses import dataclass

from BaseClasses import ItemClassification
from . import Levels, Options, Objects, Names
from .Levels import LevelRegion
from .Names import REGION_INDICES, WEAPONS
from .ObjectTypes import ObjectType


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
        self.attributes = attributes

        self.available_stages = []

        # Temporary code before rewriting weapon accessibility overhaul
        # TODO Change full weapon accessibility
        for stage in stages:
            if type(stage) is tuple:
                self.available_stages.append(stage)
            elif stage in Levels.BOSS_STAGES:
                self.available_stages.append(stage)
            elif not Levels.HasCheckpointZero(stage):
                self.available_stages.append((stage, 1))
            else:
                self.available_stages.append(stage)

        
    
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


def GetRuleByWeaponRequirement(player, req, regionInfo: LevelRegion):

    if req is None or req == Names.REGION_RESTRICTION_TYPES.NoRestriction:
        return lambda state: True

    if regionInfo is None:
        region_to_use = None
    else:
        region_to_use = regionInfo.regionIndex

    if region_to_use is None:
        region_to_use = 0

    if regionInfo is not None:
        matches_items = [ item for item in WEAPON_INFO if (regionInfo.stageId, region_to_use) in item.available_stages
                          and (req in item.attributes or req is None) ]
    else:
        matches_items = [ item for item in WEAPON_INFO if item.name == req ]

    accessibility_rule = None

    if len(matches_items) == 0:
        matches_items = [item for item in WEAPON_INFO if regionInfo.stageId in
                         [ stage[0] for stage in item.available_stages if req in item.attributes ]]

        if len(matches_items) != 0:
            built_rule = lambda state: True
            for item in matches_items:
                possibilities = [ c[1] for c in item.available_stages if c[0] == regionInfo.stageId]
                for p in possibilities:
                    built_rule = lambda state, br=built_rule: (br(state) or
                                                               state.can_reach_region(Levels.stage_id_to_region(p[0], p[1])))

            accessibility_rule = built_rule

    matches_groups = [ group[0] for group in WeaponGroups.items() if len([ x for x in group[1] if x in
                                                                           [m.game_id for m in matches_items]]) > 0]
    matches = []
    matches.extend([ x.name for x in matches_items])
    matches.extend(matches_groups)

    #print(stage, regions_use, matches)

    if len(matches) == 0:
        print("Unable to find weapon match", regionInfo.stageId, req, regionInfo.regionIndex)
        #raise Exception("Invalid accessibility")
        return None
        return lambda state: False

    weapon_rule = lambda state, reqs=matches: state.has_any([m for m in reqs],player)
    if accessibility_rule is not None:
        weapon_rule = lambda state, a_rule=accessibility_rule, w_rule=weapon_rule: a_rule(state) and w_rule(state)

    return weapon_rule

BASE_WEAPON_INFO = [
    WeaponInfo(WEAPONS.PISTOL, "Pistol", 2, 10,
               [Levels.STAGE_WESTOPOLIS,Levels.STAGE_LETHAL_HIGHWAY, Levels.STAGE_PRISON_ISLAND,
                Levels.STAGE_CENTRAL_CITY, Levels.STAGE_THE_DOOM,
                (Levels.STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_PULLEY),
                Levels.STAGE_LOST_IMPACT, Levels.BOSS_BLACK_BULL_DR, Levels.BOSS_DIABLON_GF],
               [WeaponAttributes.SHOT]),
    WeaponInfo(WEAPONS.SUB_MACHINE_GUN, "Sub Machine Gun", 2, 20,
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
    WeaponInfo(WEAPONS.SEMI_AUTOMATIC_RIFLE, "Semi Automatic Rifle", 4, 20,
               [Levels.STAGE_LETHAL_HIGHWAY,
                    Levels.STAGE_PRISON_ISLAND, (Levels.STAGE_CIRCUS_PARK,REGION_INDICES.CIRCUS_PARK_CHECKPOINT_THREE),
                Levels.STAGE_CENTRAL_CITY,
                    Levels.STAGE_THE_DOOM,
                (Levels.STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_PULLEY),
                    Levels.STAGE_THE_ARK, Levels.STAGE_AIR_FLEET,
                (Levels.STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_GOLD_BEETLE),
                Levels.STAGE_SPACE_GADGET, Levels.STAGE_LOST_IMPACT,
                Levels.STAGE_GUN_FORTRESS, (Levels.STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_ZIPWIRE),
                Levels.BOSS_BLACK_DOOM_CF],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(WEAPONS.HEAVY_MACHINE_GUN, "Heavy Machine Gun", 6, 30,
               [(Levels.STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_GUN_TURRET),
                (Levels.STAGE_CENTRAL_CITY,REGION_INDICES.CENTRAL_CITY_GUN_TURRET),
                Levels.STAGE_THE_DOOM,
                (Levels.STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_GUN_TURRET),
                (Levels.STAGE_THE_ARK,REGION_INDICES.THE_ARK_BLACK_VOLT),
                (Levels.STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_PULLEY),
                Levels.STAGE_SPACE_GADGET,
                (Levels.STAGE_GUN_FORTRESS,REGION_INDICES.GUN_FORTRESS_GUN_TURRET),
                (Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_WARP_HOLE),
                (Levels.STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_PULLEY_NORMAL),
                Levels.BOSS_EGG_BREAKER_IJ],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(WEAPONS.GATLING_GUN, "Gatling Gun", 6, 40,
               [(Levels.STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_KEY_DOOR),
                   (Levels.STAGE_THE_ARK,REGION_INDICES.THE_ARK_BLACK_VOLT),
                (Levels.STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_ROCKET), Levels.STAGE_GUN_FORTRESS,
                (Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_AIR_SAUCER)],
               [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(WEAPONS.EGG_GUN, "Egg Gun", 2, 20,
               [(Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_BALLOON), Levels.STAGE_CIRCUS_PARK, Levels.STAGE_SKY_TROOPS,
                Levels.STAGE_MAD_MATRIX, Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER,
                Levels.BOSS_EGG_BREAKER_CC, Levels.BOSS_EGG_BREAKER_MM,
                Levels.BOSS_EGG_BREAKER_IJ, Levels.BOSS_EGG_DEALER_BC,
                Levels.BOSS_EGG_DEALER_LS, Levels.BOSS_EGG_DEALER_CF],
        [WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(WEAPONS.LIGHT_SHOT, "Light Shot", 2, 20,
                [Levels.STAGE_WESTOPOLIS,
                Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_LETHAL_HIGHWAY,
                 (Levels.STAGE_CRYPTIC_CASTLE,REGION_INDICES.CRYPTIC_CASTLE_HAWK), Levels.STAGE_PRISON_ISLAND,
                Levels.STAGE_CENTRAL_CITY, Levels.STAGE_DEATH_RUINS,
                 (Levels.STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_ZIPWIRE),
                 Levels.BOSS_BLACK_BULL_LH, Levels.BOSS_BLACK_BULL_DR, Levels.BOSS_DIABLON_BC],
            [WeaponAttributes.SHOT]),
    WeaponInfo(WEAPONS.FLASH_SHOT, "Flash Shot", 2, 20,
               [Levels.STAGE_WESTOPOLIS, Levels.STAGE_GLYPHIC_CANYON,
                Levels.STAGE_LETHAL_HIGHWAY, (Levels.STAGE_CRYPTIC_CASTLE,REGION_INDICES.CRYPTIC_CASTLE_HAWK),
                Levels.STAGE_PRISON_ISLAND, Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_DEATH_RUINS, Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_BLACK_COMET, Levels.BOSS_DIABLON_BC, Levels.BOSS_BLACK_BULL_LH,
               Levels.BOSS_DIABLON_FH, Levels.BOSS_BLACK_DOOM_FH],
               [WeaponAttributes.SHOT]),
    WeaponInfo(WEAPONS.RING_SHOT, "Ring Shot", 4, 20,
           [Levels.STAGE_SKY_TROOPS, Levels.STAGE_SPACE_GADGET,
                Levels.STAGE_FINAL_HAUNT, Levels.BOSS_DIABLON_BC,
            Levels.BOSS_DIABLON_FH, Levels.BOSS_BLACK_DOOM_FH,
            Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.SHOT]),
    WeaponInfo(WEAPONS.HEAVY_SHOT, "Heavy Shot", 5, 20,
               [(Levels.STAGE_FINAL_HAUNT,REGION_INDICES.FINAL_HAUNT_ROCKET_NORMAL),
                (Levels.STAGE_THE_LAST_WAY,REGION_INDICES.THE_LAST_WAY_BLACK_VOLT)],
               [WeaponAttributes.SHOT]),
    WeaponInfo(WEAPONS.GRENADE_LAUNCHER, "Grenade Launcher", 4, 10,
               [Levels.STAGE_GLYPHIC_CANYON, (Levels.STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_BOMBS),
                (Levels.STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_SIX_WALLS),
                (Levels.STAGE_SPACE_GADGET,REGION_INDICES.SPACE_GADGET_AIR_SAUCER_HERO),
                Levels.STAGE_LOST_IMPACT, Levels.BOSS_BLACK_DOOM_GF],
    [WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(WEAPONS.BAZOOKA, "Bazooka", 8, 5,
               [Levels.STAGE_CENTRAL_CITY, (Levels.STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_PULLEY),
                (Levels.STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_AIR_SAUCER), #
                (Levels.STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_PULLEY_NORMAL),
                Levels.BOSS_BLACK_DOOM_CF],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(WEAPONS.TANK_CANNON, "Tank Cannon", 16, 5,
               [(Levels.STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_KEY_DOOR),
                (Levels.STAGE_IRON_JUNGLE,REGION_INDICES.IRON_JUNGLE_KEY_DOOR),
                (Levels.STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_BEHIND_KEY_DOOR)],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(WEAPONS.BLACK_BARREL, "Black Barrel", 4, 5,
               [(Levels.STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_ROCKET_NORMAL),
                (Levels.STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_AIR_SAUCER_HERO),
    (Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_BLACK_TURRET),
                Levels.STAGE_FINAL_HAUNT,Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(WEAPONS.BIG_BARREL, "Big Barrel", 8, 5,
               [(Levels.STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_PULLEY_NORMAL),
                Levels.STAGE_FINAL_HAUNT,
                Levels.BOSS_BLACK_DOOM_FH,Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(WEAPONS.EGG_BAZOOKA, "Egg Bazooka", 8, 5,
               [(Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_TORCH),
                (Levels.STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_THREE),
                Levels.STAGE_SKY_TROOPS,
                (Levels.STAGE_MAD_MATRIX,REGION_INDICES.MAD_MATRIX_GUN),
                Levels.STAGE_IRON_JUNGLE, Levels.STAGE_LAVA_SHELTER,
                Levels.BOSS_EGG_BREAKER_MM, Levels.BOSS_EGG_BREAKER_IJ,
                Levels.BOSS_EGG_DEALER_BC, Levels.BOSS_EGG_DEALER_LS, Levels.BOSS_EGG_DEALER_CF],
[WeaponAttributes.NOT_AIMABLE, WeaponAttributes.EXPLOSION]),
    WeaponInfo(WEAPONS.RPG, "RPG", 6, 10,
               [(Levels.STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_BOMBS),
                Levels.STAGE_THE_ARK,
                Levels.STAGE_GUN_FORTRESS],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(WEAPONS.FOUR_SHOT_RPG, "4-Shot RPG", 8, 10,
               [(Levels.STAGE_THE_ARK,REGION_INDICES.THE_ARK_BLACK_VOLT),
                Levels.STAGE_IRON_JUNGLE, Levels.STAGE_SPACE_GADGET,
                Levels.BOSS_HEAVY_DOG, Levels.BOSS_BLUE_FALCON,
                Levels.BOSS_BLACK_DOOM_GF, Levels.BOSS_BLACK_DOOM_CF],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(WEAPONS.EIGHT_SHOT_RPG, "8-Shot RPG", 8, 10,
               [Levels.STAGE_GUN_FORTRESS, (Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_AIR_SAUCER)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(WEAPONS.WORM_SHOOTER, "Worm Shooter", 6, 5,
               [Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,
                (Levels.STAGE_PRISON_ISLAND,REGION_INDICES.PRISON_ISLAND_AIR_SAUCER),
                (Levels.STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_GUN),
                (Levels.STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_SIX_WALLS),
                (Levels.STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_AIR_SAUCER_HERO)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(WEAPONS.WIDE_WORM_SHOOTER, "Wide Worm Shooter", 8, 5,
               [(Levels.STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_YELLOW_ENTRY),
                (Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_TWO_WORMS),
                Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(WEAPONS.BIG_WORM_SHOOTER, "Big Worm Shooter", 16, 5,
               [(Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_THREE_FLOATERS),
                (Levels.STAGE_THE_LAST_WAY,REGION_INDICES.THE_LAST_WAY_VOLT_OR_WARP)],
[WeaponAttributes.NOT_AIMABLE]),
    WeaponInfo(WEAPONS.VACUUM_POD, "Vacuum Pod", None, 20,
               [Levels.STAGE_CENTRAL_CITY,
                (Levels.STAGE_SPACE_GADGET,REGION_INDICES.SPACE_GADGET_AIR_SAUCER_HERO),
                Levels.STAGE_FINAL_HAUNT],
[WeaponAttributes.VACUUM]),
    WeaponInfo(WEAPONS.LASER_RIFLE, "Laser Rifle", 3, 20,
               [(Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_AIR_SAUCER)],
[WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(WEAPONS.SPLITTER, "Splitter", 4, 20,
               [(Levels.STAGE_DEATH_RUINS,REGION_INDICES.DEATH_RUINS_PULLEY), Levels.STAGE_AIR_FLEET,
                (Levels.STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_AIR_SAUCER_HERO), Levels.STAGE_GUN_FORTRESS],
[WeaponAttributes.SHOT]),
    WeaponInfo(WEAPONS.REFRACTOR, "Refractor", 5, 20,
               [(Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_AIR_SAUCER),
                #(Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_END_WORMS),
                #(Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_LATER_WORMS),
                #(Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_SIX_WORMS),
                #(Levels.STAGE_BLACK_COMET,REGION_INDICES.BLACK_COMET_SEVEN_WORMS),

                Levels.STAGE_FINAL_HAUNT,
                Levels.BOSS_BLACK_DOOM_FH, Levels.STAGE_THE_LAST_WAY],
[WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(WEAPONS.SURVIVAL_KNIFE, "Survival Knife", 2, 5,
               [Levels.STAGE_THE_DOOM],
[]),
    WeaponInfo(0x1F, "Black Sword", 4, 5,
               [Levels.STAGE_DIGITAL_CIRCUIT,Levels.STAGE_GLYPHIC_CANYON,
                (Levels.STAGE_CRYPTIC_CASTLE,REGION_INDICES.CRYPTIC_CASTLE_TORCH),
                (Levels.STAGE_PRISON_ISLAND,REGION_INDICES.PRISON_ISLAND_AIR_SAUCER), Levels.STAGE_CENTRAL_CITY,
                Levels.STAGE_SKY_TROOPS, Levels.STAGE_AIR_FLEET,
                Levels.STAGE_FINAL_HAUNT, Levels.STAGE_THE_LAST_WAY],
[]),
    WeaponInfo(0x20, "Dark Hammer", 6, 5,
               [Levels.STAGE_FINAL_HAUNT,
                (Levels.STAGE_THE_LAST_WAY,REGION_INDICES.THE_LAST_WAY_LIGHT_DASH_EASY)],
[]),
    WeaponInfo(0x21, "Egg Spear", 2, 4,
               [Levels.STAGE_CRYPTIC_CASTLE, Levels.STAGE_CIRCUS_PARK,
                (Levels.STAGE_SKY_TROOPS,REGION_INDICES.SKY_TROOPS_ROCKET_NORMAL),
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
               [(Levels.STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_ROCKET)],
[]),

    WeaponInfo(0x26, "Cryptic Torch",2, 4,
               [(Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_BALLOON),
                    (Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_TWO_BALLOON),
                    (Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_FIVE_BALLOON),
                    (Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_BOMB_EASY_2),
                    (Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_SIX),
                    (Levels.STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_SEVEN)

                ],
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
               [(Levels.STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_GUN)], []),

    WeaponInfo(0x2D, "Ruins Branch",2, 4,
               [Levels.STAGE_DEATH_RUINS],
[]),
    WeaponInfo(0x2F, "Fleet Pole",2, 4,
               [(Levels.STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_PULLEY)],
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
               [(Levels.STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_ZIPWIRE)],
[]),
    WeaponInfo(0x37, "Haunt Pole",2, 4,
               [Levels.STAGE_FINAL_HAUNT],
[]),
    WeaponInfo(0x38, "Last Pole",2, 4,
               [Levels.STAGE_THE_LAST_WAY],
[]),

    WeaponInfo(0x3A, "Samurai Blade", 8, 6,
               [],[WeaponAttributes.SPECIAL]),
    WeaponInfo(0x3C, "Satellite Gun", 18, 6,
               [],
[WeaponAttributes.SPECIAL, WeaponAttributes.NOT_AIMABLE,WeaponAttributes.LOCKON]),
    WeaponInfo(0x3E, "Egg Vacuum", None, 20,
               [],
[WeaponAttributes.SPECIAL, WeaponAttributes.VACUUM]),
    WeaponInfo(0x40, "Omochao Gun", 10, 10,
               [],
[WeaponAttributes.SPECIAL, WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE]),
    WeaponInfo(0x42, "Heal Cannon", None, 10,
               [],
[WeaponAttributes.SPECIAL, WeaponAttributes.HEAL]),
    WeaponInfo(0x43, "Shadow Rifle", 32, 20,
               [],
[WeaponAttributes.SPECIAL, WeaponAttributes.SHOT, WeaponAttributes.LONG_RANGE, WeaponAttributes.SHADOW_RIFLE])
]


NON_OBJECT_WEAPONS = [
    (Names.BOSS_HEAVY_DOG, WEAPONS.FOUR_SHOT_RPG, 0),
    (Names.BOSS_BLUE_FALCON, WEAPONS.FOUR_SHOT_RPG, 0),

    (Names.STAGE_WESTOPOLIS, WEAPONS.SPEED_LIMIT_SIGN, REGION_INDICES.WESTOPOLIS_CHECKPOINT_ONE),
    (Names.STAGE_WESTOPOLIS, WEAPONS.SPEED_LIMIT_SIGN, REGION_INDICES.WESTOPOLIS_CHECKPOINT_THREE),
    (Names.STAGE_WESTOPOLIS, WEAPONS.SPEED_LIMIT_SIGN, REGION_INDICES.WESTOPOLIS_BEHIND_THREE),
    (Names.STAGE_WESTOPOLIS, WEAPONS.SPEED_LIMIT_SIGN, REGION_INDICES.WESTOPOLIS_CHECKPOINT_FOUR),

    (Names.STAGE_DIGITAL_CIRCUIT, WEAPONS.DIGITAL_POLE, REGION_INDICES.DIGITAL_CIRCUIT_BEHIND_ONE),
    (Names.STAGE_DIGITAL_CIRCUIT, WEAPONS.DIGITAL_POLE, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_ONE),
    (Names.STAGE_DIGITAL_CIRCUIT, WEAPONS.DIGITAL_POLE, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_FOUR),

    (Names.STAGE_GLYPHIC_CANYON, WEAPONS.CANYON_POLE, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_ONE),
    (Names.STAGE_GLYPHIC_CANYON, WEAPONS.CANYON_POLE, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_TWO),
    (Names.STAGE_GLYPHIC_CANYON, WEAPONS.CANYON_POLE, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_THREE),
    (Names.STAGE_GLYPHIC_CANYON, WEAPONS.CANYON_POLE, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_FIVE),
    (Names.STAGE_GLYPHIC_CANYON, WEAPONS.CANYON_POLE, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_SIX),
    (Names.STAGE_GLYPHIC_CANYON, WEAPONS.CANYON_POLE, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_EIGHT),

    (Names.STAGE_LETHAL_HIGHWAY, WEAPONS.LETHAL_POLE, REGION_INDICES.LETHAL_HIGHWAY_THREE_FALL),
    (Names.STAGE_LETHAL_HIGHWAY, WEAPONS.LETHAL_POLE, REGION_INDICES.LETHAL_HIGHWAY_FIVE_ROCKET),

    (Names.STAGE_PRISON_ISLAND, WEAPONS.PRISON_BRANCH, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_ONE),
    (Names.STAGE_PRISON_ISLAND, WEAPONS.PRISON_BRANCH, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_TWO),
    (Names.STAGE_PRISON_ISLAND, WEAPONS.PRISON_BRANCH, REGION_INDICES.PRISON_ISLAND_AIR_SAUCER),
    (Names.STAGE_PRISON_ISLAND, WEAPONS.PRISON_BRANCH, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_THREE),
    (Names.STAGE_PRISON_ISLAND, WEAPONS.PRISON_BRANCH, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_FOUR),
    (Names.STAGE_PRISON_ISLAND, WEAPONS.PRISON_BRANCH, REGION_INDICES.PRISON_ISLAND_FOUR_AIR_SAUCER),
    (Names.STAGE_PRISON_ISLAND, WEAPONS.PRISON_BRANCH, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_SIX),
    (Names.STAGE_PRISON_ISLAND, WEAPONS.PRISON_BRANCH, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_SEVEN),

    (Names.STAGE_CIRCUS_PARK, WEAPONS.CIRCUS_POLE, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ZERO),
    (Names.STAGE_CIRCUS_PARK, WEAPONS.CIRCUS_POLE, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ONE),
    (Names.STAGE_CIRCUS_PARK, WEAPONS.CIRCUS_POLE, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO),
    (Names.STAGE_CIRCUS_PARK, WEAPONS.CIRCUS_POLE, REGION_INDICES.CIRCUS_PARK_THREE_LOWER),
    (Names.STAGE_CIRCUS_PARK, WEAPONS.CIRCUS_POLE, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FOUR),
    (Names.STAGE_CIRCUS_PARK, WEAPONS.CIRCUS_POLE, REGION_INDICES.CIRCUS_PARK_FOUR_LOWER),
    (Names.STAGE_CIRCUS_PARK, WEAPONS.CIRCUS_POLE, REGION_INDICES.CIRCUS_PARK_ROCKET),
    (Names.STAGE_CIRCUS_PARK, WEAPONS.CIRCUS_POLE, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_SIX),

    (Names.STAGE_CENTRAL_CITY, WEAPONS.STOP_SIGN, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_ZERO),
    (Names.STAGE_CENTRAL_CITY, WEAPONS.STOP_SIGN, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_THREE),
    (Names.STAGE_CENTRAL_CITY, WEAPONS.STOP_SIGN, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FIVE),
    (Names.STAGE_CENTRAL_CITY, WEAPONS.STOP_SIGN, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_SIX),

    (Names.STAGE_THE_DOOM, WEAPONS.DOOM_POLE, REGION_INDICES.THE_DOOM_CHECKPOINT_ONE),
    (Names.STAGE_THE_DOOM, WEAPONS.DOOM_POLE, REGION_INDICES.THE_DOOM_BOMBS),
    (Names.STAGE_THE_DOOM, WEAPONS.DOOM_POLE, REGION_INDICES.THE_DOOM_CHECKPOINT_TWO),
    (Names.STAGE_THE_DOOM, WEAPONS.DOOM_POLE, REGION_INDICES.THE_DOOM_CHECKPOINT_THREE),
    (Names.STAGE_THE_DOOM, WEAPONS.DOOM_POLE, REGION_INDICES.THE_DOOM_CHECKPOINT_FOUR),
    (Names.STAGE_THE_DOOM, WEAPONS.DOOM_POLE, REGION_INDICES.THE_DOOM_CHECKPOINT_FIVE),
    (Names.STAGE_THE_DOOM, WEAPONS.DOOM_POLE, REGION_INDICES.THE_DOOM_CHECKPOINT_SIX),

    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_CHECKPOINT_ONE),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_CHECKPOINT_TWO),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_GUN_JUMPER),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_ROCKET_NORMAL),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_CHECKPOINT_THREE),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_CHECKPOINT_FOUR),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_CHECKPOINT_FIVE),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_CHECKPOINT_SIX),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_HAWK_OR_VOLT),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_CHECKPOINT_SEVEN),
    (Names.STAGE_SKY_TROOPS, WEAPONS.SKY_POLE, REGION_INDICES.SKY_TROOPS_CHECKPOINT_EIGHT),

    (Names.STAGE_MAD_MATRIX, WEAPONS.MATRIX_POLE, REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM),

    (Names.STAGE_DEATH_RUINS, WEAPONS.RUINS_BRANCH, REGION_INDICES.DEATH_RUINS_CHECKPOINT_ONE),
    (Names.STAGE_DEATH_RUINS, WEAPONS.RUINS_BRANCH, REGION_INDICES.DEATH_RUINS_PULLEY),
    (Names.STAGE_DEATH_RUINS, WEAPONS.RUINS_BRANCH, REGION_INDICES.DEATH_RUINS_CHECKPOINT_TWO),
    (Names.STAGE_DEATH_RUINS, WEAPONS.RUINS_BRANCH, REGION_INDICES.DEATH_RUINS_CHECKPOINT_THREE),
    (Names.STAGE_DEATH_RUINS, WEAPONS.RUINS_BRANCH, REGION_INDICES.DEATH_RUINS_RAIL_SECTION),
    (Names.STAGE_DEATH_RUINS, WEAPONS.RUINS_BRANCH, REGION_INDICES.DEATH_RUINS_CHECKPOINT_FIVE),
    (Names.STAGE_DEATH_RUINS, WEAPONS.RUINS_BRANCH, REGION_INDICES.DEATH_RUINS_CHECKPOINT_SIX),

    (Names.STAGE_AIR_FLEET, WEAPONS.FLEET_POLE, REGION_INDICES.AIR_FLEET_CHECKPOINT_ONE),
    (Names.STAGE_AIR_FLEET, WEAPONS.FLEET_POLE, REGION_INDICES.AIR_FLEET_CHECKPOINT_FOUR),

    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_ZERO),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_ZERO_BACKTRACK),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_ONE),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_TWO),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_ANDROID_HOLE_ONE),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_ROCKET_LANDING),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_THREE),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FOUR),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_LIGHT_DASH_DARK),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_SEVEN),
    (Names.STAGE_IRON_JUNGLE, WEAPONS.IRON_POLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_EIGHT),

    (Names.STAGE_SPACE_GADGET, WEAPONS.GADGET_POLE, REGION_INDICES.SPACE_GADGET_CHECKPOINT_ONE),
    (Names.STAGE_SPACE_GADGET, WEAPONS.GADGET_POLE, REGION_INDICES.SPACE_GADGET_TWO_LOWER),
    (Names.STAGE_SPACE_GADGET, WEAPONS.GADGET_POLE, REGION_INDICES.SPACE_GADGET_CHECKPOINT_FIVE),

    (Names.STAGE_LOST_IMPACT, WEAPONS.IMPACT_POLE, REGION_INDICES.LOST_IMPACT_CHECKPOINT_ONE),
    (Names.STAGE_LOST_IMPACT, WEAPONS.IMPACT_POLE, REGION_INDICES.LOST_IMPACT_CHECKPOINT_TWO),
    (Names.STAGE_LOST_IMPACT, WEAPONS.IMPACT_POLE, REGION_INDICES.LOST_IMPACT_CHECKPOINT_THREE),
    (Names.STAGE_LOST_IMPACT, WEAPONS.IMPACT_POLE, REGION_INDICES.LOST_IMPACT_CHECKPOINT_FOUR),
    (Names.STAGE_LOST_IMPACT, WEAPONS.IMPACT_POLE, REGION_INDICES.LOST_IMPACT_CHECKPOINT_FIVE),
    (Names.STAGE_LOST_IMPACT, WEAPONS.IMPACT_POLE, REGION_INDICES.LOST_IMPACT_CHECKPOINT_SIX),
    (Names.STAGE_LOST_IMPACT, WEAPONS.IMPACT_POLE, REGION_INDICES.LOST_IMPACT_CHECKPOINT_EIGHT),

    (Names.STAGE_GUN_FORTRESS, WEAPONS.FORTRESS_POLE, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_ONE),
    (Names.STAGE_GUN_FORTRESS, WEAPONS.FORTRESS_POLE, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_TWO),
    (Names.STAGE_GUN_FORTRESS, WEAPONS.FORTRESS_POLE, REGION_INDICES.GUN_FORTRESS_ZIPWIRE),

    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_ZERO),
    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_LOWER_ZERO),
    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_ONE),
    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_TWO),
    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_PULLEY),
    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_PULLEY_OR_LAVA),
    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_THREE),
    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FOUR),
    (Names.STAGE_LAVA_SHELTER, WEAPONS.LAVA_SHOVEL, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_SEVEN),

    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_CHECKPOINT_ONE),
    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_PULLEY_NORMAL),
    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_CHECKPOINT_THREE),
    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_CHECKPOINT_FOUR),
    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_CHECKPOINT_SIX),
    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_LIGHT_DASH),
    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_GUN_JUMPER),
    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_GUN_JUMPER_PULLEY_HARD),
    (Names.STAGE_COSMIC_FALL, WEAPONS.COSMIC_POLE, REGION_INDICES.COSMIC_FALL_LD_OR_JUMPER),

    (Names.STAGE_FINAL_HAUNT, WEAPONS.HAUNT_POLE, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_ONE),
    (Names.STAGE_FINAL_HAUNT, WEAPONS.HAUNT_POLE, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_TWO),
    (Names.STAGE_FINAL_HAUNT, WEAPONS.HAUNT_POLE, REGION_INDICES.FINAL_HAUNT_VACUUM),
    (Names.STAGE_FINAL_HAUNT, WEAPONS.HAUNT_POLE, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_FOUR),

    (Names.STAGE_THE_LAST_WAY, WEAPONS.LAST_POLE, REGION_INDICES.THE_LAST_WAY_KEY_DOOR_ROOM),
    (Names.STAGE_THE_LAST_WAY, WEAPONS.LAST_POLE, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_ONE),
    (Names.STAGE_THE_LAST_WAY, WEAPONS.LAST_POLE, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_TWO),
    (Names.STAGE_THE_LAST_WAY, WEAPONS.LAST_POLE, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_THREE),
    (Names.STAGE_THE_LAST_WAY, WEAPONS.LAST_POLE, REGION_INDICES.THE_LAST_WAY_POST_CHAOS_CONTROL_1),
    (Names.STAGE_THE_LAST_WAY, WEAPONS.LAST_POLE, REGION_INDICES.THE_LAST_WAY_ABOVE_4),
    (Names.STAGE_THE_LAST_WAY, WEAPONS.LAST_POLE, REGION_INDICES.THE_LAST_WAY_CHAOS_CONTROL_3)

]

def GenerateWeaponInfo():
    weapon_info = []

    shadow_box_info = [w for w in Objects.DESIRABLE_OBJECTS if w.object_type == ObjectType.SHADOW_BOX]
    stage_info = [ w for w in Objects.DESIRABLE_OBJECTS if w.weapon is not None and w.object_type !=  ObjectType.SHADOW_BOX
                   and w.object_type in Objects.GetPlayableObjectTypes()]

    for weapon_id in Names.WEAPONS:
        found_weapon = [ i for i in BASE_WEAPON_INFO if i.game_id == weapon_id ][0]

        if WeaponAttributes.SPECIAL in found_weapon.attributes:
            found_weapon.available_stages = []
            weapon_usage = [x for x in shadow_box_info ]
            unique_regions = []
            for i in weapon_usage:
                if (i.stage, i.region) not in unique_regions:
                    unique_regions.append((i.stage, i.region))

            for use in unique_regions:
                if use[1] is None:
                    found_weapon.available_stages.append((use[0], 0))
                else:
                    found_weapon.available_stages.append(use)

        else:
            found_weapon.available_stages = []
            weapon_usage = [ x for x in stage_info if x.weapon == found_weapon.game_id ]
            unique_regions = []
            for i in weapon_usage:
                if (i.stage, i.region) not in unique_regions:
                    unique_regions.append((i.stage, i.region))

            for use in unique_regions:
                if use[1] is None:
                    found_weapon.available_stages.append(use[0])
                else:
                    found_weapon.available_stages.append(use)

        special_cases = [ s for s in NON_OBJECT_WEAPONS if s[1] == weapon_id ]
        for case in special_cases:
            if (case[0], case[2]) not in found_weapon.available_stages:
                found_weapon.available_stages.append((case[0], case[2]))

        weapon_info.append(found_weapon)

    return weapon_info

WEAPON_INFO = GenerateWeaponInfo()

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


