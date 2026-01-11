from dataclasses import dataclass

from . import Options
from .Names import *

MISSION_ALIGNMENT_DARK = 0
MISSION_ALIGNMENT_NEUTRAL = 1
MISSION_ALIGNMENT_HERO = 2

LOCATION_ID_PLUS = 100066
LOCATION_ID_SHADOW_RIFLE_COMPLETE = 100067


STAGE_TO_STORY_BLOCK = \
{
    STAGE_WESTOPOLIS: 5,
    STAGE_DIGITAL_CIRCUIT: 6,
    STAGE_GLYPHIC_CANYON: 7,
    STAGE_LETHAL_HIGHWAY: 8,
    STAGE_CRYPTIC_CASTLE: 9,
    STAGE_PRISON_ISLAND: 10,
    STAGE_CIRCUS_PARK: 11,
    STAGE_CENTRAL_CITY: 12,
    STAGE_THE_DOOM: 13,
    STAGE_SKY_TROOPS: 14,
    STAGE_MAD_MATRIX: 15,
    STAGE_DEATH_RUINS: 16,
    STAGE_THE_ARK: 17,
    STAGE_AIR_FLEET: 18,
    STAGE_IRON_JUNGLE: 19,
    STAGE_SPACE_GADGET: 20,
    STAGE_LOST_IMPACT: 21,
    STAGE_GUN_FORTRESS: 22,
    STAGE_BLACK_COMET: 23,
    STAGE_LAVA_SHELTER: 24,
    STAGE_COSMIC_FALL: 25,
    STAGE_FINAL_HAUNT: 26,

    STAGE_THE_LAST_WAY: 27,

    BOSS_BLACK_BULL_LH: 28,
    BOSS_EGG_BREAKER_CC: 29,
    BOSS_HEAVY_DOG: 30,
    BOSS_EGG_BREAKER_MM: 31,
    BOSS_BLACK_BULL_DR: 32,
    BOSS_BLUE_FALCON: 33,
    BOSS_EGG_BREAKER_IJ: 34,
    BOSS_BLACK_DOOM_GF:  35,
    BOSS_DIABLON_GF: 36,
    BOSS_EGG_DEALER_BC: 37,
    BOSS_DIABLON_BC: 38,
    BOSS_EGG_DEALER_LS: 39,
    BOSS_EGG_DEALER_CF: 40,
    BOSS_BLACK_DOOM_CF: 41,
    BOSS_BLACK_DOOM_FH: 42,
    BOSS_DIABLON_FH: 43,
    BOSS_DEVIL_DOOM: 44

}

BOSS_GROUPING = {
    "Black Doom": [BOSS_BLACK_DOOM_GF, BOSS_BLACK_DOOM_CF, BOSS_BLACK_DOOM_FH],
    "Egg Dealer": [BOSS_EGG_DEALER_BC, BOSS_EGG_DEALER_LS, BOSS_EGG_DEALER_CF],
    "Diablon": [BOSS_DIABLON_GF, BOSS_DIABLON_BC, BOSS_DIABLON_FH],
    "Egg Breaker": [BOSS_EGG_BREAKER_CC, BOSS_EGG_BREAKER_MM, BOSS_EGG_BREAKER_IJ],
    "Black Bull": [BOSS_BLACK_BULL_LH, BOSS_BLACK_BULL_DR]

}


def IsObjectRestriction(restriction_types):
    object_restrictions = [REGION_RESTRICTION_TYPES.Pulley, REGION_RESTRICTION_TYPES.LightDash,
               REGION_RESTRICTION_TYPES.WarpHole, REGION_RESTRICTION_TYPES.Rocket,
               REGION_RESTRICTION_TYPES.Zipwire]

    return len(set(restriction_types).intersection(object_restrictions)) > 0


class REGION_RESTRICTION_REFERENCE_TYPES:
    BaseLogic = 1
    BossLogic = 2
    CraftLogic = 3

def IsWeaponsanityRestriction(restriction_types):
    weapons = [REGION_RESTRICTION_TYPES.Torch, REGION_RESTRICTION_TYPES.LongRangeGun,
               REGION_RESTRICTION_TYPES.Vacuum, REGION_RESTRICTION_TYPES.Gun,
               REGION_RESTRICTION_TYPES.Heal, REGION_RESTRICTION_TYPES.AnyStageWeapon,
               REGION_RESTRICTION_TYPES.VacuumOrShot,
               REGION_RESTRICTION_TYPES.SatelliteGun]

    for w in weapons:
        if w in restriction_types:
            return True

    return False

def IsVeichleSanityRestriction(restriction_types):
    vehicles = [REGION_RESTRICTION_TYPES.BlackHawk, REGION_RESTRICTION_TYPES.BlackVolt,
                REGION_RESTRICTION_TYPES.AirSaucer, REGION_RESTRICTION_TYPES.Car,
                REGION_RESTRICTION_TYPES.GunJumper, REGION_RESTRICTION_TYPES.GunLift,
                REGION_RESTRICTION_TYPES.BlackArmsTurret, REGION_RESTRICTION_TYPES.GunTurret]

    for v in vehicles:
        if v in restriction_types:
            return True

    return False

@dataclass
class LevelRegion:
    stageId: int
    regionIndex: int
    restrictionTypes: list[REGION_RESTRICTION_TYPES]
    logicType: int
    chaosControlLogicType: int
    fromRegions: list
    hardLogicOnly: bool = False

    def __init__(self, stageId, regionIndex,
                 restrictionTypes: list[REGION_RESTRICTION_TYPES] | REGION_RESTRICTION_TYPES):
        self.stageId = stageId
        self.regionIndex = regionIndex

        ##if type(restrictionTypes) == int:
        #    print("INT TYPE", stageId, regionIndex, restrictionTypes)

        if type(restrictionTypes) != list:
            self.restrictionTypes = [restrictionTypes]
        else:
            self.restrictionTypes = restrictionTypes
        self.fromRegions = None if regionIndex is None else [regionIndex - 1]
        self.logicType = Options.LogicLevel.option_normal
        self.chaosControlLogicType = Options.ChaosControlLogicLevel.option_off
        self.chaosControlLogicRequiresHeal = False

    def setHardLogicOnly(self):
        self.hardLogicOnly = True
        return self

    def setLogicType(self, logicLevel,
                     chaosControlLogicLevel=Options.ChaosControlLogicLevel.option_off,
                     chaosControlRequiresHeal=False):


        self.logicType = logicLevel
        self.chaosControlLogicType = chaosControlLogicLevel
        self.chaosControlLogicRequiresHeal = chaosControlRequiresHeal
        return self

    def setFromRegion(self, fromRegion):
        if type(fromRegion) is int:
            self.fromRegions = [fromRegion]
        elif type(fromRegion) is list:
            self.fromRegions = fromRegion

        return self


def IsRegionRestrictionApplication(region_restriction, options, starting_items):
    if region_restriction == REGION_RESTRICTION_TYPES.ShootOrTurret and \
            not (options.weapon_sanity_unlock and options.vehicle_logic):
        return False

    if region_restriction == REGION_RESTRICTION_TYPES.ShootOrTurret and "Vehicle:Gun Turret" in starting_items:
        return False

    if region_restriction == REGION_RESTRICTION_TYPES.Explosion and not \
            (options.weapon_sanity_unlock or options.object_units):
        return False

    if region_restriction == REGION_RESTRICTION_TYPES.Explosion and "Bombs" in starting_items:
        return False

    if IsWeaponsanityRestriction([region_restriction]) and not options.weapon_sanity_unlock:
        return False

    if IsVeichleSanityRestriction([region_restriction]) and not options.vehicle_logic:
        return False

    if IsObjectRestriction([region_restriction]):
        if not options.object_unlocks:
            return False
        if (region_restriction == REGION_RESTRICTION_TYPES.Zipwire and
                (not options.object_ziplines or "Zipwire" in starting_items)):
            return False
        if (region_restriction == REGION_RESTRICTION_TYPES.LightDash and
                (not options.object_light_dashes or "Air Shoes" in starting_items)):
            return False
        if (region_restriction == REGION_RESTRICTION_TYPES.WarpHole and
                (not options.object_warp_holes or "Warp Hole" in starting_items)):
            return False
        if (region_restriction == REGION_RESTRICTION_TYPES.Rocket and
                (not options.object_rockets or "Rocket" in starting_items)):
            return False
        if (region_restriction == REGION_RESTRICTION_TYPES.Pulley and
                (not options.object_pulleys or "Pulley" in starting_items)):
            return False

    return True

def IsLogicLevelApplicable(region, options, path_type, starting_items):

    logic_level = options.logic_level

    if path_type == REGION_RESTRICTION_REFERENCE_TYPES.BossLogic:

        if options.boss_logic_level == Options.BossLogicLevel.option_hard:
            if region.logicType == Options.LogicLevel.option_easy:
                return False

        logic_level = options.boss_logic_level


    if path_type == REGION_RESTRICTION_REFERENCE_TYPES.CraftLogic:
        if options.craft_logic_level == Options.CraftLogicLevel.option_hard:
            if region.logicType == Options.LogicLevel.option_easy:
                return False

        logic_level = options.craft_logic_level

    region_restrictions = region.restrictionTypes

    if len(region_restrictions) == 1 and REGION_RESTRICTION_TYPES.NoRestriction in region_restrictions and \
        len(region.fromRegions) == 1:
        #print("Weirdly defined region:", region)
        return False

    if region.hardLogicOnly:
        if logic_level != Options.LogicLevel.option_hard:
            return False

    if region.logicType == Options.LogicLevel.option_easy and \
            logic_level != Options.LogicLevel.option_easy:
        return False

    if region.logicType == Options.LogicLevel.option_hard and \
            logic_level  == Options.LogicLevel.option_hard:
        return False

    if region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_easy and \
            options.chaos_control_logic_level != Options.ChaosControlLogicLevel.option_off:
        return False

    if region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_intermediate and \
            options.chaos_control_logic_level not in \
        [Options.ChaosControlLogicLevel.option_off, Options.ChaosControlLogicLevel.option_easy]:

        #if region.chaosControlLogicRequiresHeal:
        #    return True

        return False

    if region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_hard and \
            options.chaos_control_logic_level == Options.ChaosControlLogicLevel.option_hard:

        #if region.chaosControlLogicRequiresHeal:
        #    return True

        return False

    required = False
    for region_restriction in region_restrictions:
        r = IsRegionRestrictionApplication(region_restriction, options, starting_items)
        required = required or r

    return required

def GetBaseAccessibleRegions(stages, options, starting_items):
    accessible = {}
    for level in stages:
        accessible[level] = [0]
    for i in INDIVIDUAL_LEVEL_REGIONS:
        if i.stageId not in accessible:
            continue
        if not IsLogicLevelApplicable(i, options, None, starting_items):
            for f in i.fromRegions:
                if f in accessible[i.stageId]:
                    accessible[i.stageId].append(i.regionIndex)
                    break

    result = []
    for stage,regions in accessible.items():
        for r in regions:
            result.append((stage, r))

    return result



INDIVIDUAL_LEVEL_REGIONS = \
[
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICIES.WESTOPOLIS_PULLEY,
                [REGION_RESTRICTION_TYPES.Pulley])
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_WESTOPOLIS, REGION_INDICIES.WESTOPOLIS_WEAPON,
                REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(0),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICIES.WESTOPOLIS_KEY_DOOR,
            REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(0),
LevelRegion(STAGE_WESTOPOLIS, REGION_INDICIES.WESTOPOLIS_GOLD_BEETLE,
            REGION_RESTRICTION_TYPES.GoldBeetle)
    .setFromRegion(0),


    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICIES.DIGITAL_CIRCUIT_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICIES.DIGITAL_CIRCUIT_KEY_WARP_HOLE,
                REGION_RESTRICTION_TYPES.WarpHole),
LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICIES.DIGITAL_CIRCUIT_GOLD_BEETLE,
            REGION_RESTRICTION_TYPES.GoldBeetle)
    .setFromRegion(0),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICIES.DIGITAL_CIRCUIT_DARK_WARP_HOLE,
                REGION_RESTRICTION_TYPES.WarpHole).setFromRegion(0),

    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICIES.GLYPHIC_CANYON_PULLEY,
                REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICIES.GLYPHIC_CANYON_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICIES.GLYPHIC_CANYON_BLACK_VOLT,
                REGION_RESTRICTION_TYPES.BlackVolt),

    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICIES.LETHAL_HIGHWAY_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICIES.LETHAL_HIGHWAY_ROCKET,
                REGION_RESTRICTION_TYPES.Rocket)
        .setFromRegion(0)
        .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICIES.LETHAL_HIGHWAY_PULLEY,
                REGION_RESTRICTION_TYPES.Pulley)
        .setLogicType(Options.LogicLevel.option_easy),

    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_BALLOON,
                REGION_RESTRICTION_TYPES.Zipwire),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_TORCH,
                REGION_RESTRICTION_TYPES.Torch),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_BOMB_EASY_1,
                REGION_RESTRICTION_TYPES.Explosion)
        .setLogicType(Options.LogicLevel.option_easy),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_HAWK,
                REGION_RESTRICTION_TYPES.BlackHawk)
        .setFromRegion(REGION_INDICIES.CRYPTIC_CASTLE_TORCH),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_HAWK_RIDE,
                REGION_RESTRICTION_TYPES.BlackHawk)
    .setFromRegion(REGION_INDICIES.CRYPTIC_CASTLE_HAWK),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_ENEMY_HAWKS,
                REGION_RESTRICTION_TYPES.VacuumOrShot),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor)
        .setFromRegion(REGION_INDICIES.CRYPTIC_CASTLE_HAWK),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_BOMB_EASY_2,
                REGION_RESTRICTION_TYPES.Explosion)
        .setFromRegion(REGION_INDICIES.CRYPTIC_CASTLE_HAWK)
        .setLogicType(Options.LogicLevel.option_easy),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_DARK_LIGHT_DASH,
                REGION_RESTRICTION_TYPES.LightDash)
        .setLogicType(Options.LogicLevel.option_hard),

    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_HAWK_2,
                REGION_RESTRICTION_TYPES.BlackHawk),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_HAWK_RIDE_2,
                REGION_RESTRICTION_TYPES.BlackHawk),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICIES.CRYPTIC_CASTLE_ENEMY_HAWKS_2,
                REGION_RESTRICTION_TYPES.VacuumOrShot),

    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER,
                REGION_RESTRICTION_TYPES.AirSaucer)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICIES.PRISON_ISLAND_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICIES.PRISON_ISLAND_PULLEY_EASY,
                REGION_RESTRICTION_TYPES.Pulley)
        .setLogicType(Options.LogicLevel.option_easy)
        .setFromRegion(REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICIES.PRISON_ISLAND_GOLD_BEETLE,
                REGION_RESTRICTION_TYPES.GoldBeetle)
    .setFromRegion(REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER),

    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_ZIP_WIRE,
                REGION_RESTRICTION_TYPES.Zipwire),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_ROCKET_ITEM,
                REGION_RESTRICTION_TYPES.Rocket),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_ROCKET_EASY,
                    REGION_RESTRICTION_TYPES.Rocket)
        .setLogicType(Options.LogicLevel.option_easy)
        .setFromRegion(REGION_INDICIES.CIRCUS_PARK_ZIP_WIRE),
        LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_SECOND_CHECKPOINT_HERO_GOAL,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setHardLogicOnly(),

    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_GUN_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret)
        .setFromRegion(REGION_INDICIES.CIRCUS_PARK_ROCKET_EASY),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
        .setFromRegion(REGION_INDICIES.CIRCUS_PARK_ROCKET_EASY),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket)
        .setFromRegion(REGION_INDICIES.CIRCUS_PARK_ROCKET_EASY)
        .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),

    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_HERO_GOAL_STANDARD,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICIES.CIRCUS_PARK_HERO_GOAL,
                REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.CIRCUS_PARK_SECOND_CHECKPOINT_HERO_GOAL,
                    REGION_INDICIES.CIRCUS_PARK_HERO_GOAL_STANDARD]),

    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_ROCKET_1,
                    REGION_RESTRICTION_TYPES.Rocket)
        .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_TRAVERSE_HARD,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setHardLogicOnly()
    .setFromRegion(0),
LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_ROCKET_1_OR_TRAVERSE_HARD,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.CENTRAL_CITY_TRAVERSE_HARD,
                    REGION_INDICIES.CENTRAL_CITY_ROCKET_1]),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA,
                    REGION_RESTRICTION_TYPES.Explosion)
        .setFromRegion(0)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_TRAVERSE_EASY,
                    REGION_RESTRICTION_TYPES.Car)
        .setFromRegion(0)
        .setLogicType(Options.LogicLevel.option_easy),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),

    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA_2,
                REGION_RESTRICTION_TYPES.Explosion)
        .setFromRegion(REGION_INDICIES.CENTRAL_CITY_TRAVERSE_EASY)
        .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard),

    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_GUN_TURRET,
                REGION_RESTRICTION_TYPES.GunTurret),

    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_ROCKET_2,
                    REGION_RESTRICTION_TYPES.Rocket)
        .setLogicType(Options.LogicLevel.option_hard)
        .setFromRegion(REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA_2),

    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA_3,
                REGION_RESTRICTION_TYPES.Explosion)
        .setLogicType(Options.LogicLevel.option_hard),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_PULLEY,
                REGION_RESTRICTION_TYPES.Pulley),
    LevelRegion(STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),
    LevelRegion(STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_BOMBS,
                    REGION_RESTRICTION_TYPES.Explosion)
        .setFromRegion(0)
        .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_THROUGH_DOOR,
                REGION_RESTRICTION_TYPES.SatelliteGun)
    .setHardLogicOnly()
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
    .setFromRegion(0),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_DOOR_1_SWITCH,
                REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.THE_DOOM_BOMBS, REGION_INDICIES.THE_DOOM_THROUGH_DOOR]),

LevelRegion(STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_FAN_ROOM,
                REGION_RESTRICTION_TYPES.VacuumOrShot)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate)
    .setFromRegion(REGION_INDICIES.THE_DOOM_DOOR_1_SWITCH),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_PULLEY_2,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICIES.THE_DOOM_BOMBS),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICIES.THE_DOOM_GOLD_BEETLE,
                REGION_RESTRICTION_TYPES.GoldBeetle)
    .setFromRegion(REGION_INDICIES.THE_DOOM_BOMBS),


LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.LightDash),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_GUN_JUMPER_EASY,
                    REGION_RESTRICTION_TYPES.GunJumper)
    .setLogicType(Options.LogicLevel.option_easy),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_ROCKET_NORMAL,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_BLACK_HAWK,
                    REGION_RESTRICTION_TYPES.BlackHawk)
    .setFromRegion(REGION_INDICIES.SKY_TROOPS_ROCKET),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_HAWK_RIDE,
                    REGION_RESTRICTION_TYPES.BlackHawk),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_HAWK_ENEMIES,
                    REGION_RESTRICTION_TYPES.VacuumOrShot)
    .setFromRegion(REGION_INDICIES.SKY_TROOPS_BLACK_HAWK),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_BLACK_HAWK_CC_EASY_1,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setFromRegion(REGION_INDICIES.SKY_TROOPS_ROCKET),

LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_BLACK_HAWK_CC_EASY_2,
                    REGION_RESTRICTION_TYPES.BlackHawk)
    .setFromRegion(REGION_INDICIES.SKY_TROOPS_BLACK_HAWK_CC_EASY_1)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),

LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_BLACK_HAWK_CC_HARD,
                    REGION_RESTRICTION_TYPES.BlackHawk)
    .setFromRegion(REGION_INDICIES.SKY_TROOPS_ROCKET)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard),

LevelRegion(STAGE_SKY_TROOPS, REGION_INDICIES.SKY_TROOPS_HAWK_OR_VOLT,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.SKY_TROOPS_BLACK_VOLT,
                    REGION_INDICIES.SKY_TROOPS_BLACK_HAWK,
                    REGION_INDICIES.SKY_TROOPS_BLACK_HAWK_CC_HARD,
                    REGION_INDICIES.SKY_TROOPS_BLACK_HAWK_CC_EASY_2
                    ]),


LevelRegion(STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_GUN,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setLogicType(Options.LogicLevel.option_easy),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_YELLOW_ENTRY,
                    REGION_RESTRICTION_TYPES.WarpHole),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_GREEN_ENTRY,
                    REGION_RESTRICTION_TYPES.WarpHole)
    .setFromRegion(REGION_INDICIES.MAD_MATRIX_GUN),

LevelRegion(STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_GREEN_PROGRESSION,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate,
                  chaosControlRequiresHeal=True),

LevelRegion(STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_RED_ENTRY,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setFromRegion(REGION_INDICIES.MAD_MATRIX_GUN),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICIES.MAD_MATRIX_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICIES.MAD_MATRIX_GUN),

LevelRegion(STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_GOLD_BEETLE,
            REGION_RESTRICTION_TYPES.GoldBeetle),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(0),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_KEY_WARP,
                    REGION_RESTRICTION_TYPES.WarpHole),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICIES.DEATH_RUINS_WALLS,
                    REGION_RESTRICTION_TYPES.Explosion)
    .setFromRegion(REGION_INDICIES.DEATH_RUINS_PULLEY)
    .setLogicType(Options.LogicLevel.option_easy),

LevelRegion(STAGE_THE_ARK, REGION_INDICIES.THE_ARK_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt),
LevelRegion(STAGE_THE_ARK, REGION_INDICIES.THE_ARK_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),

# need to work out the hard logic for this
LevelRegion(STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_RAIL_HARD,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setHardLogicOnly()
    .setFromRegion(REGION_INDICIES.AIR_FLEET_PULLEY),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_RAILS,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.AIR_FLEET_RAIL_HARD,
                    REGION_INDICIES.AIR_FLEET_AIR_SAUCER]),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICIES.AIR_FLEET_GOLD_BEETLE,
                    REGION_RESTRICTION_TYPES.GoldBeetle)
    .setFromRegion(REGION_INDICIES.AIR_FLEET_PULLEY),

LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_EARLY_JUMPER,
                    REGION_RESTRICTION_TYPES.GunJumper),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(0),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_PULLEY_NORMAL,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(0),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_GOLD_BEETLE,
                    REGION_RESTRICTION_TYPES.GoldBeetle),

LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH_LOWER,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setLogicType(Options.LogicLevel.option_easy)
    .setFromRegion(REGION_INDICIES.IRON_JUNGLE_ROCKET),

LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_GUN_JUMPER,
                    REGION_RESTRICTION_TYPES.GunJumper)
    .setFromRegion(REGION_INDICIES.IRON_JUNGLE_ROCKET),

LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_JUMPER_OR_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.IRON_JUNGLE_GUN_JUMPER, REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH_LOWER]),

LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setFromRegion(REGION_INDICIES.IRON_JUNGLE_ROCKET)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_GUN_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH_DARK,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setFromRegion(REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH),

LevelRegion(STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_UNITS,
                    REGION_RESTRICTION_TYPES.Gun),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_ZIPWIRE,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setFromRegion(0),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_UNITS_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.Gun),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICIES.SPACE_GADGET_AIR_SAUCER),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_WARP_HOLE,
                    REGION_RESTRICTION_TYPES.WarpHole),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICIES.SPACE_GADGET_WARP_HOLE_DARK,
                    REGION_RESTRICTION_TYPES.WarpHole)
    .setFromRegion(REGION_INDICIES.SPACE_GADGET_AIR_SAUCER),

LevelRegion(STAGE_LOST_IMPACT, REGION_INDICIES.LOST_IMPACT_GUN_LIFT,
                    REGION_RESTRICTION_TYPES.GunLift),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICIES.LOST_IMPACT_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICIES.LOST_IMPACT_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICIES.LOST_IMPACT_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setFromRegion(REGION_INDICIES.LOST_IMPACT_GUN_LIFT),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICIES.LOST_IMPACT_BOMB_WALL,
                    REGION_RESTRICTION_TYPES.Explosion)
    .setFromRegion(REGION_INDICIES.LOST_IMPACT_GUN_LIFT),


LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_GUN_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret),
LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_TURRET_OR_FIRE,
                    REGION_RESTRICTION_TYPES.ShootOrTurret)
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(0),
LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ZIPWIRE_NORMAL,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setLogicType(Options.LogicLevel.option_hard),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_PULLEY,
            REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate, True),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ZIP_1A,
            [REGION_RESTRICTION_TYPES.Pulley])
            .setFromRegion([REGION_INDICIES.GUN_FORTRESS_PULLEY]),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ZIP_1B,
            REGION_RESTRICTION_TYPES.Zipwire)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate, True),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ZIP_2,
                [REGION_RESTRICTION_TYPES.Zipwire])
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard, True),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ZIPWIRE_BASE,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setFromRegion(REGION_INDICIES.GUN_FORTRESS_PULLEY),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ZIPWIRE,
                    REGION_RESTRICTION_TYPES.Zipwire).
    setFromRegion([REGION_INDICIES.GUN_FORTRESS_ZIP_1B, REGION_INDICIES.GUN_FORTRESS_ZIP_2,
                  REGION_INDICIES.GUN_FORTRESS_ZIPWIRE_BASE]),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ROCKET_NORMAL,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_hard),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_WEAPON_SHOT,
                    REGION_RESTRICTION_TYPES.VacuumOrShot),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_TUNNEL_2,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICIES.GUN_FORTRESS_ROCKET_NORMAL),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_TOP_TUNNEL_2,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion( REGION_INDICIES.GUN_FORTRESS_ROCKET_NORMAL)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard, True),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_COMPUTER_2_BACK,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICIES.GUN_FORTRESS_TOP_TUNNEL_2)
    .setHardLogicOnly(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_COMPUTER_ROOM_TWO,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion([REGION_INDICIES.GUN_FORTRESS_TUNNEL_2, REGION_INDICIES.GUN_FORTRESS_COMPUTER_2_BACK]),


LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_AFTER_TUNNEL_2,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.GUN_FORTRESS_TUNNEL_2,
                   REGION_INDICIES.GUN_FORTRESS_TOP_TUNNEL_2]),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_KEY_PULLEY,
            REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICIES.GUN_FORTRESS_AFTER_TUNNEL_2),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICIES.GUN_FORTRESS_AFTER_TUNNEL_2),

    # Pulley also present here, without pulley it may not be possible at all

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ZIPLINE_HARD,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setFromRegion(REGION_INDICIES.GUN_FORTRESS_KEY_PULLEY),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_ZIPLINE_ENEMIES,
                    REGION_RESTRICTION_TYPES.Vacuum),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICIES.GUN_FORTRESS_KEY_OR_ZIPLINE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.GUN_FORTRESS_KEY_DOOR,
                    REGION_INDICIES.GUN_FORTRESS_ZIPLINE_HARD]),

# Functionally, may be no need to split CR3 etc logic, since no more CCs


LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_WORMS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_FLOATERS,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(REGION_INDICIES.BLACK_COMET_AIR_SAUCER),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_WARP_HOLE,
                    REGION_RESTRICTION_TYPES.WarpHole),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_BLACK_TURRET,
                    REGION_RESTRICTION_TYPES.BlackArmsTurret),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_FLOATERS_2,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(REGION_INDICIES.BLACK_COMET_WARP_HOLE),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_HIGHER_CREATURES,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
    .setFromRegion(REGION_INDICIES.BLACK_COMET_WARP_HOLE),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_WORMS_2,
                    REGION_RESTRICTION_TYPES.VacuumOrShot)
    .setFromRegion(REGION_INDICIES.BLACK_COMET_WARP_HOLE),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_FLOATING_ENEMY_WALL,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(REGION_INDICIES.BLACK_COMET_WARP_HOLE),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICIES.BLACK_COMET_BEHIND_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICIES.BLACK_COMET_KEY_DOOR))
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(REGION_INDICIES.BLACK_COMET_FLOATING_ENEMY_WALL),


LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICIES.LAVA_SHELTER_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICIES.LAVA_SHELTER_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICIES.LAVA_SHELTER_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
    .setFromRegion(0),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICIES.LAVA_SHELTER_PULLEY_OR_LAVA,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.LAVA_SHELTER_PULLEY,
                    REGION_INDICIES.LAVA_SHELTER_AIR_SAUCER]),
    LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICIES.LAVA_SHELTER_LIGHT_DASH_DARK,
                REGION_RESTRICTION_TYPES.LightDash)
    .setFromRegion(REGION_INDICIES.LAVA_SHELTER_PULLEY_OR_LAVA)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
    LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICIES.LAVA_SHELTER_PULLEY_DARK,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),


LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_ZIPWIRE,
                    REGION_RESTRICTION_TYPES.Zipwire),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_PULLEY_CORE,
                    REGION_RESTRICTION_TYPES.Pulley),


LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.LightDash),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_GUN_JUMPER,
                    REGION_RESTRICTION_TYPES.GunJumper)
    .setFromRegion(REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL),

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_GUN_JUMPER_PULLEY_HARD,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICIES.COSMIC_FALL_GUN_JUMPER),

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_LD_OR_JUMPER,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.COSMIC_FALL_GUN_JUMPER_PULLEY_HARD,
                    REGION_INDICIES.COSMIC_FALL_LIGHT_DASH]),


LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_COMPUTER_ROOM_1,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard),

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_COMPUTER_ROOM_2,
                    REGION_RESTRICTION_TYPES.Impassable)
    .setFromRegion(REGION_INDICIES.COSMIC_FALL_PULLEY_CORE)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate),

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_COMPUTER_ROOM,
            REGION_RESTRICTION_TYPES.NoRestriction)
            .setFromRegion([REGION_INDICIES.COSMIC_FALL_COMPUTER_ROOM_1,
                    REGION_INDICIES.COSMIC_FALL_COMPUTER_ROOM_2]),


LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_VACUUM,
                    REGION_RESTRICTION_TYPES.Vacuum)
    .setLogicType(Options.LogicLevel.option_hard),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_VACUUM_HARD,
                    REGION_RESTRICTION_TYPES.Vacuum)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_VACUUM),


LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT_BASE,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_VACUUM),


LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT_ACCESS,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT_BASE,
                    REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT_BACK]),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT_BACK,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setHardLogicOnly()
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_HARD_VACUUM_OR_BLACK_VOLT),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_HARD_VACUUM_OR_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.FINAL_HAUNT_VACUUM_HARD,
                    REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT]),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_ROCKET_NORMAL,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_HARD_VACUUM_OR_BLACK_VOLT),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_SHIELD_2,
            REGION_RESTRICTION_TYPES.NoRestriction)
.setFromRegion([REGION_INDICIES.FINAL_HAUNT_ROCKET_NORMAL]),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_SHIELD_COUNT_2,
            REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICIES.FINAL_HAUNT_SHIELD_2))
.setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
.setFromRegion([REGION_INDICIES.FINAL_HAUNT_SHIELD_4,
                REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT]),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT_2,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_ROCKET_NORMAL),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_ROCKET_NORMAL),
LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_ROCKET_NORMAL),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_SHIELD_COUNT_3,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
    .setLogicType(Options.LogicLevel.option_hard),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_KEY_DOOR_2,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_LIGHT_DASH),

LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_SHIELD_4,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setLogicType(Options.LogicLevel.option_easy)
    .setFromRegion(REGION_INDICIES.FINAL_HAUNT_LIGHT_DASH),


LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICIES.THE_LAST_WAY_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),

LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICIES.THE_LAST_WAY_VOLT_ENEMIES,
                    REGION_RESTRICTION_TYPES.BlackVolt),

LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICIES.THE_LAST_WAY_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(0),

LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICIES.THE_LAST_WAY_BEHIND_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICIES.THE_LAST_WAY_KEY_DOOR))
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(0),

LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICIES.THE_LAST_WAY_WARP_HOLE,
                    REGION_RESTRICTION_TYPES.WarpHole),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICIES.THE_LAST_WAY_VOLT_OR_WARP,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICIES.THE_LAST_WAY_WARP_HOLE,
                    REGION_INDICIES.THE_LAST_WAY_BLACK_VOLT]),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICIES.THE_LAST_WAY_LIGHT_DASH_EASY,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setLogicType(Options.LogicLevel.option_easy)
]

FINAL_STAGES = [STAGE_GUN_FORTRESS, STAGE_BLACK_COMET, STAGE_LAVA_SHELTER, STAGE_COSMIC_FALL, STAGE_FINAL_HAUNT]

# The order here matters, since this order is used to determine the flags to unlock these bosses in Select Mode
FINAL_BOSSES = [
    BOSS_BLACK_DOOM_GF,
    BOSS_DIABLON_GF ,
    BOSS_EGG_DEALER_BC,
    BOSS_DIABLON_BC,
    BOSS_EGG_DEALER_LS,
    BOSS_EGG_DEALER_CF,
    BOSS_BLACK_DOOM_CF,
    BOSS_BLACK_DOOM_FH,
    BOSS_DIABLON_FH
]

CharacterToLevel = {
    "Sonic": [STAGE_WESTOPOLIS, STAGE_LETHAL_HIGHWAY, STAGE_FINAL_HAUNT, BOSS_BLACK_BULL_LH, BOSS_BLACK_DOOM_FH],
    "Tails": [STAGE_CIRCUS_PARK, STAGE_AIR_FLEET],
    "Knuckles": [STAGE_GLYPHIC_CANYON, STAGE_CENTRAL_CITY, (STAGE_BLACK_COMET,
	REGION_INDICIES.BLACK_COMET_AIR_SAUCER), BOSS_EGG_DEALER_BC],
    "Amy": [STAGE_CRYPTIC_CASTLE, BOSS_EGG_BREAKER_CC],
    "Eggman": [(STAGE_CRYPTIC_CASTLE,
	REGION_INDICIES.CRYPTIC_CASTLE_TORCH),
	STAGE_CIRCUS_PARK, STAGE_SKY_TROOPS,
               STAGE_IRON_JUNGLE, STAGE_LAVA_SHELTER],
    "Rouge": [STAGE_DIGITAL_CIRCUIT, STAGE_DEATH_RUINS, (STAGE_GUN_FORTRESS,
	REGION_INDICIES.GUN_FORTRESS_ZIPWIRE_NORMAL
	), BOSS_BLACK_BULL_DR, BOSS_BLACK_DOOM_GF],
    "Omega": [STAGE_IRON_JUNGLE, STAGE_LAVA_SHELTER, BOSS_EGG_BREAKER_IJ, BOSS_EGG_DEALER_LS],
    "Doom": [STAGE_WESTOPOLIS, STAGE_DIGITAL_CIRCUIT, (STAGE_GLYPHIC_CANYON,
	REGION_INDICIES.GLYPHIC_CANYON_PULLEY),
             STAGE_LETHAL_HIGHWAY, STAGE_PRISON_ISLAND, STAGE_CENTRAL_CITY,
             STAGE_THE_DOOM, STAGE_SKY_TROOPS, (STAGE_MAD_MATRIX,
			 REGION_INDICIES.MAD_MATRIX_GUN),
             STAGE_DEATH_RUINS, STAGE_THE_ARK, (STAGE_AIR_FLEET,
			 REGION_INDICIES.AIR_FLEET_PULLEY),
             STAGE_SPACE_GADGET, (STAGE_GUN_FORTRESS,REGION_INDICIES.GUN_FORTRESS_ZIPWIRE_NORMAL), STAGE_BLACK_COMET,
             (STAGE_COSMIC_FALL, REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL), (STAGE_FINAL_HAUNT, REGION_INDICIES.FINAL_HAUNT_VACUUM), BOSS_DIABLON_FH, BOSS_DIABLON_GF,
             BOSS_DIABLON_BC, BOSS_HEAVY_DOG, BOSS_BLUE_FALCON],
    "Espio": [STAGE_MAD_MATRIX, BOSS_EGG_BREAKER_MM],
    "Charmy": [STAGE_PRISON_ISLAND],
    "Vector": [(STAGE_COSMIC_FALL,
	REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL), BOSS_BLACK_DOOM_CF, BOSS_EGG_DEALER_CF],
    "Maria": [STAGE_THE_DOOM, STAGE_LOST_IMPACT]
}

ALL_STAGES = list(LEVEL_ID_TO_LEVEL.keys())


DevilDoom_Name = "Devil Doom"


# Starting at Westopolis Clear
# Levels store all ranks of missions even though they don't exist
# We can abuse this :)

ITEM_TOKEN_TYPE_STANDARD = 0
ITEM_TOKEN_TYPE_ALIGNMENT = 1
ITEM_TOKEN_TYPE_FINAL = 2
ITEM_TOKEN_TYPE_OBJECTIVE = 3
ITEM_TOKEN_TYPE_BOSS = 4
ITEM_TOKEN_TYPE_FINAL_BOSS = 5

TOKEN_TYPE_TO_STRING = \
{
    ITEM_TOKEN_TYPE_STANDARD: "Base",
    ITEM_TOKEN_TYPE_ALIGNMENT: "Alignment",
    ITEM_TOKEN_TYPE_FINAL: "Final",
    ITEM_TOKEN_TYPE_OBJECTIVE: "Objective",
    ITEM_TOKEN_TYPE_BOSS: "Boss",
    ITEM_TOKEN_TYPE_FINAL_BOSS: "Final Boss"
}


def GetLevelTokenNames(stageId, alignmentId, type):
    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(type) + str(alignmentId) + "0")
    view_name = (LEVEL_ID_TO_LEVEL[stageId] + " Mission Token " + ALIGNMENT_TO_STRING[alignmentId] +
                 (" " + TOKEN_TYPE_TO_STRING[type] if type != ITEM_TOKEN_TYPE_STANDARD else "") )

    return id_name, view_name

def GetBossTokenNames(stageId, type):
    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(type) + "0")
    token_name_part = "Final Boss Token" if type == ITEM_TOKEN_TYPE_FINAL_BOSS else "Boss Token"
    view_name = f"{LEVEL_ID_TO_LEVEL[stageId]} {token_name_part}"

    return id_name, view_name

def GetLevelCompletionNames(stageId, alignmentId):

    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(alignmentId) + "1")
    view_name = LEVEL_ID_TO_LEVEL[stageId] + " Mission Clear " + ALIGNMENT_TO_STRING[alignmentId]

    return id_name, view_name


def GetLevelWarpName(stageId):
    id_name = int(str(LOCATION_ID_PLUS) + str(2) + str(stageId) + "11")
    view_name = LEVEL_ID_TO_LEVEL[stageId] + " Level Warp"

    return id_name, view_name

def GetLevelObjectNames(stageId, alignmentId, objectName, i):
    id_name =  int(str(LOCATION_ID_PLUS) + str(1) + str(stageId) + str(alignmentId) + str(i) + "0")
    objective_location_name = (LEVEL_ID_TO_LEVEL[stageId] + "-" +
                               objectName + " Count " + str(i))

    return id_name, objective_location_name

# Minimum requirements for minimal traversal (so add 1)
MINIMUM_STAGE_REQUIREMENTS = \
[
    (STAGE_WESTOPOLIS, MISSION_ALIGNMENT_HERO, 2),
    (STAGE_WESTOPOLIS, MISSION_ALIGNMENT_DARK, 6),

    (STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_HERO, 1),

    (STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_DARK, 2),
    # Circus Park Dark, probably not?

    (STAGE_CENTRAL_CITY, MISSION_ALIGNMENT_DARK, 1),
    (STAGE_MAD_MATRIX, MISSION_ALIGNMENT_HERO, 1),
    (STAGE_DEATH_RUINS, MISSION_ALIGNMENT_HERO, 5),

    (STAGE_AIR_FLEET, MISSION_ALIGNMENT_HERO, 9),
    (STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_DARK, 2),
    # Iron Jungle Dark, probably not?
    (STAGE_SPACE_GADGET, MISSION_ALIGNMENT_DARK, 1),
    (STAGE_BLACK_COMET, MISSION_ALIGNMENT_DARK, 1),
    (STAGE_LAVA_SHELTER, MISSION_ALIGNMENT_DARK, 2),
    (STAGE_FINAL_HAUNT, MISSION_ALIGNMENT_DARK, 1)


]

NON_OBJECTIVESANITY_REGIONS = \
[
    (STAGE_GLYPHIC_CANYON, REGION_INDICIES.GLYPHIC_CANYON_KEY_DOOR),
    (STAGE_GLYPHIC_CANYON, REGION_INDICIES.GLYPHIC_CANYON_BLACK_VOLT)
]