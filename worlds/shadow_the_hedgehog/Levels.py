from dataclasses import dataclass

from . import Options, Names
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
class BacktrackRegion:
    stageId: int
    backtrackToRegion: int
    backtrackFromRegion: int
    logicType: int
    hardLogicOnly: bool
    iccLogicOnly: bool
    restrictionTypes: list[REGION_RESTRICTION_TYPES]

    def __init__(self, stageId, fromRegion, toRegion,
                 logicType, restrictionTypes):
        self.stageId = stageId
        self.backtrackToRegion = toRegion
        self.backtrackFromRegion = fromRegion
        self.logicType = logicType
        self.hardLogicOnly = False
        self.iccLogicOnly = False

        if type(restrictionTypes) != list:
            self.restrictionTypes = [restrictionTypes]
        else:
            self.restrictionTypes = restrictionTypes

    def setHardLogicOnly(self):
        self.hardLogicOnly = True
        return self


@dataclass
class EscapePath:
    stageId: int
    escapeFrom: int
    escapeVia: []

    def __init__(self, stageId, escapeFrom, escapeVia):
        self.stageId = stageId
        self.escapeFrom = escapeFrom
        self.escapeVia = escapeVia


@dataclass
class LevelRegion:
    stageId: int
    regionIndex: int
    restrictionTypes: list[REGION_RESTRICTION_TYPES]
    logicType: int
    chaosControlLogicType: int
    fromRegions: list
    hardLogicOnly: bool = False
    iccLogicOnly: bool = False
    isDiversion: bool = False

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

    def setICCLogicOnly(self):
        self.iccLogicOnly = True
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

    def setAsDiversion(self):
        self.isDiversion = True
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

    if region.hardLogicOnly:
        if logic_level != Options.LogicLevel.option_hard:
            return False

    if region.logicType == Options.LogicLevel.option_easy and \
            logic_level != Options.LogicLevel.option_easy:
        return False

    if region.logicType == Options.LogicLevel.option_hard and \
            logic_level  == Options.LogicLevel.option_hard:
        return False

    if len(region_restrictions) == 1 and REGION_RESTRICTION_TYPES.NoRestriction in region_restrictions and \
        len(region.fromRegions) == 1:
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
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_CHECKPOINT_ONE,
            REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_CHECKPOINT_TWO,
            REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_PULLEY,
                [REGION_RESTRICTION_TYPES.Pulley])
    .setLogicType(Options.LogicLevel.option_hard)
    .setAsDiversion(),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_BEHIND_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.WESTOPOLIS_CHECKPOINT_TWO),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_CHECKPOINT_THREE,
            REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_WEAPON,
                REGION_RESTRICTION_TYPES.LongRangeGun)
    .setAsDiversion(),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_CHECKPOINT_FOUR,
            REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.WESTOPOLIS_CHECKPOINT_THREE),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_KEY_DOOR,
            REGION_RESTRICTION_TYPES.KeyDoor)
        .setAsDiversion(),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_CHECKPOINT_FIVE,
            REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.WESTOPOLIS_CHECKPOINT_FOUR),
LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_GOLD_BEETLE,
            REGION_RESTRICTION_TYPES.GoldBeetle)
    .setAsDiversion(),
    LevelRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_CHECKPOINT_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.WESTOPOLIS_CHECKPOINT_FIVE),

    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_ZERO,
            REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_BEHIND_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_TWO,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_BEHIND_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_BELOW_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_KEY_WARP_HOLE,
                REGION_RESTRICTION_TYPES.WarpHole)
    .setAsDiversion(),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_GOLD_BEETLE,
            REGION_RESTRICTION_TYPES.GoldBeetle)
    .setFromRegion(REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_FOUR)
    .setAsDiversion(),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_FIVE,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_FOUR),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_DARK_WARP_HOLE,
                REGION_RESTRICTION_TYPES.WarpHole),
    LevelRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_SEVEN,
                REGION_RESTRICTION_TYPES.NoRestriction),

    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_TWO,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_PULLEY,
                REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_FIVE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_BLACK_VOLT,
                REGION_RESTRICTION_TYPES.BlackVolt).setAsDiversion(),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_FOUR),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_SEVEN,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_EIGHT,
                REGION_RESTRICTION_TYPES.NoRestriction),



    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_ONE_FALL,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_TWO,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_TWO_FALL,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor)
        .setAsDiversion(),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_ROCKET,
                REGION_RESTRICTION_TYPES.Rocket)
        .setFromRegion(REGION_INDICES.LETHAL_HIGHWAY_TWO_FALL)
        .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_THREE_FALL,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_THREE_FALL_2,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_FIVE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_FIVE_BOMB,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_FIVE_ROCKET,
                REGION_RESTRICTION_TYPES.Rocket),
    LevelRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_FIVE_FALL,
                REGION_RESTRICTION_TYPES.NoRestriction),


    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_BALLOON,
                REGION_RESTRICTION_TYPES.Zipwire).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_TORCH,
                REGION_RESTRICTION_TYPES.Torch),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_TWO,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_TWO_BALLOON,
                REGION_RESTRICTION_TYPES.Zipwire),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_BOMB_EASY_1,
                REGION_RESTRICTION_TYPES.Explosion)
        .setLogicType(Options.LogicLevel.option_easy).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_TWO_LOWER,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_HAWK,
                REGION_RESTRICTION_TYPES.BlackHawk),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_HAWK_RIDE,
                REGION_RESTRICTION_TYPES.BlackHawk)
    .setFromRegion(REGION_INDICES.CRYPTIC_CASTLE_HAWK).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_HAWK_END_ITEM,
                REGION_RESTRICTION_TYPES.NoRestriction).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_ENEMY_HAWKS,
                REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.CRYPTIC_CASTLE_HAWK),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_TOP_PATH,
                REGION_RESTRICTION_TYPES.Torch)
    .setFromRegion(REGION_INDICES.CRYPTIC_CASTLE_TWO_BALLOON),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_UPPER_HAWK_RIDE,
                REGION_RESTRICTION_TYPES.BlackHawk),
LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_UPPER_HAWK_END_ITEM,
                REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_THREE_OR_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_THREE,
        REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_FOUR]),
LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_FIVE,
                REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_FIVE_BALLOON,
                REGION_RESTRICTION_TYPES.Zipwire),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_BOMB_EASY_2,
                REGION_RESTRICTION_TYPES.Explosion)
        .setFromRegion(REGION_INDICES.CRYPTIC_CASTLE_FIVE_BALLOON)
        .setLogicType(Options.LogicLevel.option_easy),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_FIVE_TORCH,
                REGION_RESTRICTION_TYPES.Torch),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_WIND_BOTTOM,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_SIX_DARK,
                REGION_RESTRICTION_TYPES.Torch).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_SIX_BALLOON,
                REGION_RESTRICTION_TYPES.Zipwire).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_DARK_LIGHT_DASH,
                REGION_RESTRICTION_TYPES.LightDash)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_HAWK_2,
                REGION_RESTRICTION_TYPES.BlackHawk),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_HAWK_RIDE_2,
                REGION_RESTRICTION_TYPES.BlackHawk).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_END_HAWK_2_ITEM,
                REGION_RESTRICTION_TYPES.NoRestriction).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_ENEMY_HAWKS_2,
                REGION_RESTRICTION_TYPES.VacuumOrShot)
        .setFromRegion(REGION_INDICES.CRYPTIC_CASTLE_HAWK_RIDE_2).setAsDiversion(),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_SEVEN,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.CRYPTIC_CASTLE_HAWK_2),
    LevelRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_EIGHT,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_SIX),

    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_TWO,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_AIR_SAUCER,
                REGION_RESTRICTION_TYPES.AirSaucer)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_KEY_DOOR,
                REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_PULLEY_EASY,
                REGION_RESTRICTION_TYPES.Pulley)
        .setLogicType(Options.LogicLevel.option_easy).setAsDiversion()
        .setFromRegion(REGION_INDICES.PRISON_ISLAND_CHECKPOINT_THREE),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.PRISON_ISLAND_CHECKPOINT_THREE),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_FOUR_AIR_SAUCER,
                REGION_RESTRICTION_TYPES.AirSaucer)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_GOLD_BEETLE,
                REGION_RESTRICTION_TYPES.GoldBeetle).setAsDiversion(),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_FIVE,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.PRISON_ISLAND_FOUR_AIR_SAUCER),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_SIX_AIR_SAUCER,
                REGION_RESTRICTION_TYPES.AirSaucer)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_SEVEN,
                REGION_RESTRICTION_TYPES.NoRestriction),

    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_ZIP_WIRE,
                REGION_RESTRICTION_TYPES.Zipwire),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_GUN_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_ROCKET_ITEM,
                REGION_RESTRICTION_TYPES.Rocket)
        .setFromRegion(REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO).setAsDiversion(),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_TWO_LOWER,
                REGION_RESTRICTION_TYPES.NoRestriction)
            .setFromRegion(REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_THREE_LOWER,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
        .setFromRegion(REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FOUR).setAsDiversion(),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_FOUR_LOWER,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FOUR),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FIVE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket)
        .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_BACK,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.CIRCUS_PARK_SIX_BACK),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_SIX_ZIPWIRE,
                REGION_RESTRICTION_TYPES.Zipwire),
    LevelRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_SEVEN,
                REGION_RESTRICTION_TYPES.NoRestriction),

    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_BOMB_OR_BAZOOKA,
                    REGION_RESTRICTION_TYPES.Explosion)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_BOMB_ROCKET,
                REGION_RESTRICTION_TYPES.Rocket).setLogicType(Options.LogicLevel.option_easy).setAsDiversion(),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_ROCKET_LANDING,
                REGION_RESTRICTION_TYPES.NoRestriction).setAsDiversion(),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_ROCKET_1,
                    REGION_RESTRICTION_TYPES.Rocket)
        .setLogicType(Options.LogicLevel.option_hard)
        .setFromRegion(REGION_INDICES.CENTRAL_CITY_CHECKPOINT_ZERO).setAsDiversion(),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_TRAVERSE_HARD,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setHardLogicOnly()
    .setFromRegion(REGION_INDICES.CENTRAL_CITY_CHECKPOINT_ZERO).setAsDiversion(),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_ROCKET_1_OR_TRAVERSE_HARD,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.CENTRAL_CITY_TRAVERSE_HARD,
                    REGION_INDICES.CENTRAL_CITY_ROCKET_1]),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_TWO,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([REGION_INDICES.CENTRAL_CITY_CHECKPOINT_ZERO,
                        REGION_INDICES.CENTRAL_CITY_ROCKET_1_OR_TRAVERSE_HARD]),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_TRAVERSE_EASY,
                    REGION_RESTRICTION_TYPES.Car)
        .setLogicType(Options.LogicLevel.option_easy).setAsDiversion(),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_BOMB_OR_BAZOOKA_2,
                REGION_RESTRICTION_TYPES.Explosion)
        .setFromRegion(REGION_INDICES.CENTRAL_CITY_TRAVERSE_EASY)
        .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_GUN_TURRET,
                REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_ROCKET_2,
                    REGION_RESTRICTION_TYPES.Rocket)
        .setFromRegion(REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FOUR),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FIVE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_GUN_TURRET_2,
                REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_FIVE_TRAVERSE,
                REGION_RESTRICTION_TYPES.Car).setFromRegion(REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FIVE),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_FIVE_ROCKET,
                REGION_RESTRICTION_TYPES.Rocket)
        .setFromRegion(REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FIVE),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_BEHIND_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([REGION_INDICES.CENTRAL_CITY_FIVE_ROCKET,
                        REGION_INDICES.CENTRAL_CITY_FIVE_TRAVERSE]),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_BOMB_OR_BAZOOKA_3,
                REGION_RESTRICTION_TYPES.Explosion)
        .setLogicType(Options.LogicLevel.option_hard).setAsDiversion(),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_PULLEY,
                REGION_RESTRICTION_TYPES.Pulley).setAsDiversion(),
    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_BOMBS,
                    REGION_RESTRICTION_TYPES.Explosion)
        .setFromRegion(REGION_INDICES.THE_DOOM_CHECKPOINT_ONE)
        .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_TWO,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_THREE,
                REGION_RESTRICTION_TYPES.NoRestriction),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_SECRET_PATH,
                [REGION_RESTRICTION_TYPES.KeyDoor,
                 REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.THE_DOOM_KEY_DOOR)]),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_THROUGH_DOOR,
                REGION_RESTRICTION_TYPES.SatelliteGun)
    .setHardLogicOnly()
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
    .setFromRegion(REGION_INDICES.THE_DOOM_CHECKPOINT_ONE),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_DOOR_1_SWITCH,
                REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.THE_DOOM_CHECKPOINT_THREE, REGION_INDICES.THE_DOOM_THROUGH_DOOR]),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_FOUR,
                REGION_RESTRICTION_TYPES.NoRestriction),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_FAN_ROOM,
                REGION_RESTRICTION_TYPES.VacuumOrShot)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate)
    .setFromRegion(REGION_INDICES.THE_DOOM_DOOR_1_SWITCH).setAsDiversion(),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_PULLEY_2,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICES.THE_DOOM_CHECKPOINT_TWO).setAsDiversion(),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_WALL_ROOM,
                REGION_RESTRICTION_TYPES.Explosion)
    .setFromRegion(REGION_INDICES.THE_DOOM_DOOR_1_SWITCH).setAsDiversion(),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_GOLD_BEETLE,
                REGION_RESTRICTION_TYPES.GoldBeetle)
    .setFromRegion(REGION_INDICES.THE_DOOM_WALL_ROOM).setAsDiversion(),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_FIVE,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.THE_DOOM_CHECKPOINT_FOUR),

    LevelRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_SIX,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([REGION_INDICES.THE_DOOM_CHECKPOINT_FIVE,
                        REGION_INDICES.THE_DOOM_SECRET_PATH]),


LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_ONE_TURRET,
                    REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction).
    setFromRegion(REGION_INDICES.SKY_TROOPS_CHECKPOINT_ONE),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley).setAsDiversion(),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.LightDash),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_GUN_JUMPER,
                    REGION_RESTRICTION_TYPES.GunJumper)
    .setLogicType(Options.LogicLevel.option_easy),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_ROCKET_NORMAL,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_THREE_LOWER,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_THREE_TURRET,
                    REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_GUN_JUMPER_2,
                    REGION_RESTRICTION_TYPES.GunJumper)
    .setLogicType(Options.LogicLevel.option_easy)
    .setFromRegion(REGION_INDICES.SKY_TROOPS_THREE_LOWER),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_ROCKET_2,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),


LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_FOUR_TURRET,
                    REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.SKY_TROOPS_CHECKPOINT_FOUR),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_ROCKET_3,
                    REGION_RESTRICTION_TYPES.Rocket),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_BLACK_HAWK,
                    REGION_RESTRICTION_TYPES.BlackHawk)
    .setFromRegion(REGION_INDICES.SKY_TROOPS_CHECKPOINT_SIX),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_HAWK_RIDE,
                    REGION_RESTRICTION_TYPES.BlackHawk).setAsDiversion(),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_HAWK_ENEMIES,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion()
    .setFromRegion(REGION_INDICES.SKY_TROOPS_BLACK_HAWK),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_EASY_1,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setFromRegion(REGION_INDICES.SKY_TROOPS_CHECKPOINT_SIX),

LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_EASY_2,
                    REGION_RESTRICTION_TYPES.BlackHawk)
    .setFromRegion(REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_EASY_1)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),

LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_HARD,
                    REGION_RESTRICTION_TYPES.BlackHawk)
    .setFromRegion(REGION_INDICES.SKY_TROOPS_CHECKPOINT_SIX)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard),

LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_HAWK_OR_VOLT,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.SKY_TROOPS_BLACK_VOLT,
                    REGION_INDICES.SKY_TROOPS_BLACK_HAWK,
                    REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_HARD,
                    REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_EASY_2
                    ]),

    LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_END_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket),
    LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_SEVEN,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([REGION_INDICES.SKY_TROOPS_BLACK_VOLT,
                        REGION_INDICES.SKY_TROOPS_END_ROCKET, REGION_INDICES.SKY_TROOPS_BLACK_HAWK]),
LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_SEVEN_TURRET,
                    REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
    LevelRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_EIGHT,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.SKY_TROOPS_CHECKPOINT_SEVEN),

    LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_BEFORE_WALL,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_BEFORE_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_GUN,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setLogicType(Options.LogicLevel.option_easy),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_BLUE_TERMINAL,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.MAD_MATRIX_BLUE_TERMINAL,
                    REGION_INDICES.MAD_MATRIX_CHECKPOINT_TWO,
                    REGION_INDICES.MAD_MATRIX_CHECKPOINT_FOUR,
                    REGION_INDICES.MAD_MATRIX_CHECKPOINT_SIX]),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_YELLOW_ENTRY,
                    REGION_RESTRICTION_TYPES.WarpHole)
    .setFromRegion(REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_YELLOW_START,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_YELLOW_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.LightDash)
        .setLogicType(Options.LogicLevel.option_easy)
    ,
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_GREEN_ENTRY,
                    REGION_RESTRICTION_TYPES.WarpHole)
    .setFromRegion(REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_GREEN_START,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_GREEN_PROGRESSION,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate,
                  chaosControlRequiresHeal=True),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM),
LevelRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_RED_ENTRY,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setFromRegion(REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM).setAsDiversion(),

LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_RAIL_SECTION,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_GOLD_BEETLE,
            REGION_RESTRICTION_TYPES.GoldBeetle).setAsDiversion(),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.DEATH_RUINS_RAIL_SECTION),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_KEY_WARP,
                    REGION_RESTRICTION_TYPES.WarpHole).setAsDiversion(),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.DEATH_RUINS_RAIL_SECTION),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_FIVE_WALLS,
                    REGION_RESTRICTION_TYPES.Explosion)
    .setLogicType(Options.LogicLevel.option_easy),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_SIX_WALLS,
                    REGION_RESTRICTION_TYPES.Explosion)
    .setLogicType(Options.LogicLevel.option_easy).setAsDiversion(),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_SIX_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley),
LevelRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_UNIT_ONE,
                    REGION_RESTRICTION_TYPES.LongRangeGun).setAsDiversion(),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_TWO_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setFromRegion(REGION_INDICES.THE_ARK_CHECKPOINT_TWO),

LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_BEFORE_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_THREE_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_FOUR_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt),

LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_UNIT_TWO,
                    REGION_RESTRICTION_TYPES.LongRangeGun).setAsDiversion(),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_FIVE_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setFromRegion(REGION_INDICES.THE_ARK_CHECKPOINT_FIVE),

LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_BEFORE_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_SIX_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt),

LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.THE_ARK_SIX_BLACK_VOLT),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_UNIT_3,
                    REGION_RESTRICTION_TYPES.LongRangeGun).setAsDiversion(),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_SEVEN_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setFromRegion(REGION_INDICES.THE_ARK_CHECKPOINT_SEVEN),

LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_GOLD_BEETLE,
                    REGION_RESTRICTION_TYPES.NoRestriction).setAsDiversion(),
LevelRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_EIGHT,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.THE_ARK_SEVEN_VOLT),



# need to work out the hard logic for this
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_KEYDOOR_ENTRANCE,
                    REGION_RESTRICTION_TYPES.NoRestriction).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_RAIL_HARD,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setHardLogicOnly()
    .setFromRegion(REGION_INDICES.AIR_FLEET_PULLEY).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_RAILS,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.AIR_FLEET_RAIL_HARD,
                    REGION_INDICES.AIR_FLEET_AIR_SAUCER]),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_SECRET_1,
                    REGION_RESTRICTION_TYPES.NoRestriction).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_BEHIND_CHECK_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.AIR_FLEET_PULLEY),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_GOLD_BEETLE,
                    REGION_RESTRICTION_TYPES.GoldBeetle).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_TWO),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_THREE_FLOATERS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),
# Note that because the level is linear, access to first rails is enough,
    # but if this changes, this logic will be more complex
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_SECRET_2,
                    [REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.AIR_FLEET_AIR_SAUCER)]
            ).setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_THREE).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_THREE_LOWER,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_THREE),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_FOUR_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_FOUR),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_FIVE_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_FIVE_FLOATERS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion()
    .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_FIVE),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_FIVE),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_SIX_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion()
    .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_FIVE),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_SECRET_3,
                    [REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.AIR_FLEET_AIR_SAUCER)])
            .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_SIX)
            .setLogicType(Options.LogicLevel.option_hard).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_OUTSIDE_SECTION,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_SIX),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_SEVEN_DESCEND,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),
LevelRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_EIGHT,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.AIR_FLEET_CHECKPOINT_SEVEN),


LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_ZERO_BACKTRACK,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_EARLY_JUMPER,
                    REGION_RESTRICTION_TYPES.GunJumper).setAsDiversion(),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.IRON_JUNGLE_CHECKPOINT_ONE),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_ANDROID_HOLE_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_PULLEY_NORMAL,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICES.IRON_JUNGLE_ANDROID_HOLE_ONE)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_ROCKET_LANDING,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_GOLD_BEETLE,
                    REGION_RESTRICTION_TYPES.GoldBeetle).setAsDiversion(),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.IRON_JUNGLE_ROCKET_LANDING),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_LIGHT_DASH_LOWER,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setLogicType(Options.LogicLevel.option_easy)
    .setFromRegion(REGION_INDICES.IRON_JUNGLE_CHECKPOINT_THREE),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_GUN_JUMPER,
                    REGION_RESTRICTION_TYPES.GunJumper)
    .setFromRegion(REGION_INDICES.IRON_JUNGLE_CHECKPOINT_THREE),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_JUMPER_OR_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.IRON_JUNGLE_GUN_JUMPER, REGION_INDICES.IRON_JUNGLE_LIGHT_DASH_LOWER]),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_GUN_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_ANDROID_HOLE_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FOUR),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_PULLEY_2,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_easy),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_ANDROID_HOLE_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_HERO_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_HERO_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_LIGHT_DASH_DARK,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setFromRegion(REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FIVE),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_DARK_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_EIGHT,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.IRON_JUNGLE_DARK_PULLEY,
                    REGION_INDICES.IRON_JUNGLE_HERO_ROCKET]),

LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_TWO_LOWER,
                    REGION_RESTRICTION_TYPES.Gun)
    .setLogicType(Options.LogicLevel.option_easy),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_ZIPWIRE,
                    REGION_RESTRICTION_TYPES.Zipwire),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_POST_ZIP,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_AIR_SAUCER_HERO,
                    REGION_RESTRICTION_TYPES.AirSaucer)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_THREE_LOWER,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_FOUR_ZIPWIRE,
                    REGION_RESTRICTION_TYPES.Zipwire),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICES.SPACE_GADGET_CHECKPOINT_FOUR).setAsDiversion(),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_WARP_HOLE,
                    REGION_RESTRICTION_TYPES.WarpHole),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_ABOVE_GOAL,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.SPACE_GADGET_FOUR_ZIPWIRE,
                    REGION_INDICES.SPACE_GADGET_WARP_HOLE]),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.SPACE_GADGET_ABOVE_GOAL,
                    REGION_INDICES.SPACE_GADGET_WARP_HOLE_DARK]),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_ZIPWIRE_DARK,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setFromRegion(REGION_INDICES.SPACE_GADGET_TWO_LOWER),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_DARK_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer)
    .setLogicType(Options.LogicLevel.option_hard),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_EIGHT,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_LAST_DARK_ROOM,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_WARP_HOLE_DARK,
                    REGION_RESTRICTION_TYPES.WarpHole),


LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_BACK_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_GUN_LIFT,
                    REGION_RESTRICTION_TYPES.GunLift),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_TWO_GUN_LIFT,
                    REGION_RESTRICTION_TYPES.GunLift),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley).setAsDiversion(),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.LOST_IMPACT_CHECKPOINT_THREE),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_FOUR_GUN_LIFT,
                    REGION_RESTRICTION_TYPES.GunLift),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_ROCKET,
                    REGION_RESTRICTION_TYPES.Rocket).setAsDiversion(),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_FIVE_GUN_LIFT,
                    REGION_RESTRICTION_TYPES.GunLift)
    .setFromRegion(REGION_INDICES.LOST_IMPACT_CHECKPOINT_FIVE),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_BEHIND_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_SEVEN_GUN_LIFT,
                    REGION_RESTRICTION_TYPES.GunLift),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_EIGHT,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_BOMB_WALL,
                    REGION_RESTRICTION_TYPES.Explosion).setAsDiversion(),
LevelRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_EIGHT_GUN_LIFT,
                    REGION_RESTRICTION_TYPES.GunLift)
    .setFromRegion(REGION_INDICES.LOST_IMPACT_CHECKPOINT_EIGHT),


LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_GUN_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),
LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_TURRET_OR_FIRE,
                    REGION_RESTRICTION_TYPES.ShootOrTurret)
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_CHECKPOINT_ONE),
LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ZIPWIRE_NORMAL,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setLogicType(Options.LogicLevel.option_hard),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_PULLEY,
            REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate, True),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_TWO_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ZIP_1A,
            [REGION_RESTRICTION_TYPES.Pulley])
            .setFromRegion([REGION_INDICES.GUN_FORTRESS_CHECKPOINT_TWO]),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ZIP_1B,
            REGION_RESTRICTION_TYPES.Zipwire)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_intermediate, True),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ZIP_2,
                [REGION_RESTRICTION_TYPES.Zipwire])
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard, True),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ZIPWIRE_BASE,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_PULLEY),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ZIPWIRE,
                    REGION_RESTRICTION_TYPES.Zipwire).
    setFromRegion([REGION_INDICES.GUN_FORTRESS_ZIP_1B, REGION_INDICES.GUN_FORTRESS_ZIP_2,
                  REGION_INDICES.GUN_FORTRESS_ZIPWIRE_BASE]),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ROCKET_NORMAL,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_hard),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_WEAPON_SHOT,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_TUNNEL_2,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_ROCKET_NORMAL),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_TOP_TUNNEL_2,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion( REGION_INDICES.GUN_FORTRESS_ROCKET_NORMAL)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard, True),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_COMPUTER_2_BACK,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_TOP_TUNNEL_2)
    .setHardLogicOnly().setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_COMPUTER_ROOM_TWO,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion([REGION_INDICES.GUN_FORTRESS_TUNNEL_2, REGION_INDICES.GUN_FORTRESS_COMPUTER_2_BACK]).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_COMPUTER_ROOM_TWO_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret)
    .setFromRegion([REGION_INDICES.GUN_FORTRESS_COMPUTER_ROOM_TWO]).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_AFTER_TUNNEL_2,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.GUN_FORTRESS_TUNNEL_2,
                   REGION_INDICES.GUN_FORTRESS_TOP_TUNNEL_2]),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_KEY_PULLEY,
            REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_AFTER_TUNNEL_2),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_BELOW_KEY_FIVE,
            REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_AFTER_TUNNEL_2),
    # Pulley also present here, without pulley it may not be possible at all

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ZIPLINE_HARD,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_KEY_PULLEY),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_ZIPLINE_ENEMIES,
                    REGION_RESTRICTION_TYPES.Vacuum).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_POST_ZIPLINE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_ZIPLINE_HARD).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_KEY_OR_ZIPLINE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.GUN_FORTRESS_KEY_DOOR,
                    REGION_INDICES.GUN_FORTRESS_ZIPLINE_HARD]),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_TUNNEL_3,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_hard).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_FINAL_UPPER_ROUTE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.GUN_FORTRESS_CHECKPOINT_SIX),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_COMPUTER_ROOM_3_BACK,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_hard).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_COMPUTER_ROOM_3,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion([REGION_INDICES.GUN_FORTRESS_COMPUTER_ROOM_3_BACK,
                   REGION_INDICES.GUN_FORTRESS_TUNNEL_3]).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_COMPUTER_ROOM_3_TURRET,
                    REGION_RESTRICTION_TYPES.GunTurret)
    .setFromRegion([REGION_INDICES.GUN_FORTRESS_COMPUTER_ROOM_TWO]).setAsDiversion(),

LevelRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.GUN_FORTRESS_FINAL_UPPER_ROUTE),

# Functionally, may be no need to split CR3 etc logic, since no more CCs


LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_WORMS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.BLACK_COMET_AIR_SAUCER),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_TWO_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_TWO_WORMS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_TWO_TRIANGLE_JUMP,
            REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.BLACK_COMET_CHECKPOINT_TWO),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_TWO_UP,
            REGION_RESTRICTION_TYPES.NoRestriction).setFromRegion(
    [REGION_INDICES.BLACK_COMET_TWO_TRIANGLE_JUMP,
     REGION_INDICES.BLACK_COMET_TWO_AIR_SAUCER]
),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_LATER_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_LATER_WORMS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FIRST_WARP_HOLE_AREA,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.BLACK_COMET_LATER_AIR_SAUCER),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FIRST_WARP_FLOATERS,
                    REGION_RESTRICTION_TYPES.LongRangeGun).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_WARP_HOLE,
                    REGION_RESTRICTION_TYPES.WarpHole)
    .setFromRegion(REGION_INDICES.BLACK_COMET_FIRST_WARP_HOLE_AREA),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_THREE_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_THREE_WORMS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_THREE_FLOATERS,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(REGION_INDICES.BLACK_COMET_THREE_AIR_SAUCER).setAsDiversion(),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.BLACK_COMET_THREE_AIR_SAUCER),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_BEHIND_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.BLACK_COMET_KEY_DOOR))
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(REGION_INDICES.BLACK_COMET_CHECKPOINT_FOUR).setAsDiversion(),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_BLACK_TURRET,
                    REGION_RESTRICTION_TYPES.BlackArmsTurret)
    .setFromRegion(REGION_INDICES.BLACK_COMET_CHECKPOINT_FOUR).setAsDiversion(),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FOUR_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer)
    .setFromRegion(REGION_INDICES.BLACK_COMET_CHECKPOINT_FOUR),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FOUR_WORMS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FOUR_GUN_PATH,
                    REGION_RESTRICTION_TYPES.AirSaucer)
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(REGION_INDICES.BLACK_COMET_FOUR_AIR_SAUCER),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_BLACK_TURRET_2,
                    REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_WARP_HOLE_2,
                    REGION_RESTRICTION_TYPES.WarpHole)
    .setFromRegion(REGION_INDICES.BLACK_COMET_FOUR_GUN_PATH),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FIVE_TURRET,
                    REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FIVE_WEAPON_FRONT,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(REGION_INDICES.BLACK_COMET_CHECKPOINT_FIVE),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FIVE_WEAPON_BACK,
                    REGION_RESTRICTION_TYPES.LongRangeGun),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FIVE_WEAPON,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.BLACK_COMET_FIVE_WEAPON_FRONT,
                    REGION_INDICES.BLACK_COMET_FIVE_WEAPON_BACK]),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FIVE_PIT,
                    REGION_RESTRICTION_TYPES.AirSaucer)
    .setLogicType(Options.LogicLevel.option_hard),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_ONSLAUGHT_LOWER,
                    REGION_RESTRICTION_TYPES.AirSaucer),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_ONSLAUGHT_FLOATERS,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(REGION_INDICES.BLACK_COMET_ONSLAUGHT_LOWER).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_HIGHER_CREATURES,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
    .setFromRegion(REGION_INDICES.BLACK_COMET_FIVE_PIT),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FLOATERS_FROM_ABOVE,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(REGION_INDICES.BLACK_COMET_HIGHER_CREATURES).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_ONSLAUGHT_END,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.BLACK_COMET_HIGHER_CREATURES,
                    REGION_INDICES.BLACK_COMET_ONSLAUGHT_LOWER]),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_WARP_HOLE_3,
                    REGION_RESTRICTION_TYPES.WarpHole),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_SIX_LOWER,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_SIX_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_SIX_WORMS,
                    REGION_RESTRICTION_TYPES.VacuumOrShot)
    .setFromRegion(REGION_INDICES.BLACK_COMET_SIX_AIR_SAUCER).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_FLOATING_ENEMY_WALL,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setFromRegion(REGION_INDICES.BLACK_COMET_SIX_AIR_SAUCER),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_END_OF_CHECK_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_END_WORMS,
                    REGION_RESTRICTION_TYPES.NoRestriction).setAsDiversion(),

LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.BLACK_COMET_END_OF_CHECK_SIX),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_SEVEN_DROP,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_SEVEN_ENEMY_FAR,
                    REGION_RESTRICTION_TYPES.LongRangeGun)
    .setLogicType(Options.LogicLevel.option_hard).setAsDiversion(),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_SEVEN_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer)
    .setFromRegion(REGION_INDICES.BLACK_COMET_SEVEN_DROP),
LevelRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_EIGHT,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.BLACK_COMET_SEVEN_AIR_SAUCER),


LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_LOWER_ZERO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_AIR_SAUCER,
                    REGION_RESTRICTION_TYPES.AirSaucer).setAsDiversion(),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_ONE_LOWER,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.LAVA_SHELTER_CHECKPOINT_ONE),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_PULLEY,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_SECRET,
                    REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.LAVA_SHELTER_AIR_SAUCER))
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_PULLEY_OR_LAVA,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.LAVA_SHELTER_PULLEY,
                    REGION_INDICES.LAVA_SHELTER_SECRET]),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_DEFENSE_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_LIGHT_DASH_DARK,
                REGION_RESTRICTION_TYPES.LightDash)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
    LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_PULLEY_DARK,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FIVE),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_WIND,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_EIGHT,
                    REGION_RESTRICTION_TYPES.NoRestriction),


LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_ZIPWIRE,
                    REGION_RESTRICTION_TYPES.Zipwire),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_FIRST_ENEMIES,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_ONE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_PULLEY_NORMAL,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setLogicType(Options.LogicLevel.option_hard).setAsDiversion(),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_ONE_AWAY,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_ZIPWIRE_ENTRY,
                    REGION_RESTRICTION_TYPES.Zipwire),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_TWO_AWAY,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_PULLEY_CORE,
                    REGION_RESTRICTION_TYPES.Pulley).setAsDiversion(),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_ZIPWIRE_TO_3,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setFromRegion(REGION_INDICES.COSMIC_FALL_TWO_AWAY),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_BALLOON_RISE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_FOUR_AWAY,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_ZIPWIRE_TO_5,
                    REGION_RESTRICTION_TYPES.Zipwire),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_LIGHT_DASH_UNLOCK,
                    REGION_RESTRICTION_TYPES.LightDash).setAsDiversion(),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_ZIPWIRE_TO_6,
                    REGION_RESTRICTION_TYPES.Zipwire)
    .setFromRegion(REGION_INDICES.COSMIC_FALL_CHECKPOINT_FIVE),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.COSMIC_FALL_KEY_DOOR)),
LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_GUN_JUMPER,
                    REGION_RESTRICTION_TYPES.GunJumper)
    .setFromRegion(REGION_INDICES.COSMIC_FALL_CHECKPOINT_SIX),

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_GUN_JUMPER_PULLEY_HARD,
                    REGION_RESTRICTION_TYPES.Pulley)
    .setFromRegion(REGION_INDICES.COSMIC_FALL_GUN_JUMPER),

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_LD_OR_JUMPER,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.COSMIC_FALL_GUN_JUMPER,
                    REGION_INDICES.COSMIC_FALL_LIGHT_DASH,
                    REGION_INDICES.COSMIC_FALL_GUN_JUMPER_PULLEY_HARD]),

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_COMPUTER_ROOM_1,
                    REGION_RESTRICTION_TYPES.Rocket)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_hard),

# If CC intermediate is on
# You need Zipwire, Check 6 and Pulley Core regions

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_COMPUTER_ROOM_2,
                    [REGION_RESTRICTION_TYPES.Zipwire,
                     REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.COSMIC_FALL_PULLEY_CORE)])
    .setFromRegion(REGION_INDICES.COSMIC_FALL_CHECKPOINT_SIX)
    .setICCLogicOnly(),

LevelRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_SEVEN,
            REGION_RESTRICTION_TYPES.NoRestriction)
            .setFromRegion([REGION_INDICES.COSMIC_FALL_COMPUTER_ROOM_1,
                    REGION_INDICES.COSMIC_FALL_COMPUTER_ROOM_2]),


    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_ONE,
                        REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_ONE_TURRET,
                        REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_TWO,
                        REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_CHECKPOINT_ONE),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_VACUUM,
                        REGION_RESTRICTION_TYPES.Vacuum)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SHIELD_ONE,
                        REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_HERO_SPLIT,
                        REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_VACUUM),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_VACUUM_HARD,
                        REGION_RESTRICTION_TYPES.Vacuum)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),

    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_BLACK_VOLT,
                        REGION_RESTRICTION_TYPES.BlackVolt)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_SHIELD_ONE),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_BLACK_VOLT_FLYING,
                        REGION_RESTRICTION_TYPES.BlackVolt).setAsDiversion(),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_BLACK_VOLT_GROUND,
                        REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_BLACK_VOLT),

    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_HARD_VACUUM_OR_BLACK_VOLT,
                        REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([REGION_INDICES.FINAL_HAUNT_VACUUM_HARD,
                        REGION_INDICES.FINAL_HAUNT_BLACK_VOLT_GROUND]),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_THREE,
                        REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_BEFORE_ROCKET,
                        REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_ROCKET_NORMAL,
                        REGION_RESTRICTION_TYPES.Rocket)
        .setLogicType(Options.LogicLevel.option_hard),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_FOUR,
                        REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SHIELD_TWO,
                        REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_FOUR_LOWER,
                        REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_CHECKPOINT_FOUR),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_FOUR_VACUUM,
                        REGION_RESTRICTION_TYPES.Vacuum),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_FIVE,
                        REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_FIVE_VACUUM,
                        REGION_RESTRICTION_TYPES.Vacuum),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_BLACK_VOLT_2,
                        REGION_RESTRICTION_TYPES.BlackVolt)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_SHIELD_TWO),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_DARK_TURRET,
                REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),

    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_VOLT_OR_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([REGION_INDICES.FINAL_HAUNT_FIVE_VACUUM,
                    REGION_INDICES.FINAL_HAUNT_BLACK_VOLT_2]),

    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_KEY_DOOR,
                        REGION_RESTRICTION_TYPES.KeyDoor)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_ROCKET_NORMAL).setAsDiversion(),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SECRET_TURRET,
                REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_LIGHT_DASH,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_VOLT_OR_FIVE),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_LIGHT_DASH),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SHIELD_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SHIELD_ESCAPE_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion([REGION_INDICES.FINAL_HAUNT_CHECKPOINT_SIX,
                       REGION_INDICES.FINAL_HAUNT_SHIELD_ESCAPE_BLACK_VOLT]),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SEVEN_TURRET,
                REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_KEY_DOOR_3,
                    REGION_RESTRICTION_TYPES.KeyDoor).setAsDiversion(),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_BEHIND_KEY_DOOR_3,
                    REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.FINAL_HAUNT_KEY_DOOR_3))
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(REGION_INDICES.FINAL_HAUNT_CHECKPOINT_SEVEN).setAsDiversion(),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SECRET_TURRET_2,
                REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_EIGHT,
                    REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.FINAL_HAUNT_CHECKPOINT_SEVEN),
    LevelRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_HERO_GOAL,
                    REGION_RESTRICTION_TYPES.NoRestriction).setAsDiversion(),

    LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_KEY_DOOR_ROOM,
                REGION_RESTRICTION_TYPES.NoRestriction),
    LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_TURRET,
                REGION_RESTRICTION_TYPES.BlackArmsTurret).setAsDiversion(),
    LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.KeyDoor)
    .setFromRegion(REGION_INDICES.THE_LAST_WAY_KEY_DOOR_ROOM).setAsDiversion(),
    LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_BEHIND_KEY_DOOR,
                    REGION_RESTRICTION_TYPES.RegionAccess(REGION_INDICES.THE_LAST_WAY_KEY_DOOR))
    .setLogicType(Options.LogicLevel.option_hard)
    .setFromRegion(REGION_INDICES.THE_LAST_WAY_KEY_DOOR_ROOM).setAsDiversion(),
    LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_WARP_HOLE,
                    REGION_RESTRICTION_TYPES.WarpHole),
    LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_ONE,
                REGION_RESTRICTION_TYPES.NoRestriction)
        .setFromRegion(REGION_INDICES.THE_LAST_WAY_KEY_DOOR_ROOM),
    LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_BLACK_VOLT,
                    REGION_RESTRICTION_TYPES.BlackVolt)
    .setLogicType(Options.LogicLevel.option_normal, Options.ChaosControlLogicLevel.option_easy),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_VOLT_ENEMIES,
                    REGION_RESTRICTION_TYPES.BlackVolt).setAsDiversion(),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_BLACK_VOLT_GROUND,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion(REGION_INDICES.THE_LAST_WAY_BLACK_VOLT),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_TWO,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_THREE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_PRE_CHAOS_CONTROL_1,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_POST_CHAOS_CONTROL_1,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_PRE_CHAOS_CONTROL_2,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_ABOVE_4,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_FOUR,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_VOLT_OR_WARP,
                    REGION_RESTRICTION_TYPES.NoRestriction)
    .setFromRegion([REGION_INDICES.THE_LAST_WAY_WARP_HOLE,
                    REGION_INDICES.THE_LAST_WAY_ABOVE_4]),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_FIVE,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_LIGHT_DASH_EASY,
                    REGION_RESTRICTION_TYPES.LightDash)
    .setLogicType(Options.LogicLevel.option_easy),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHAOS_CONTROL_3,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_SIX,
                    REGION_RESTRICTION_TYPES.NoRestriction),
LevelRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_SEVEN,
                    REGION_RESTRICTION_TYPES.NoRestriction),

LevelRegion(BOSS_EGG_BREAKER_IJ, REGION_INDICES.EGG_BREAKER_IRON_JUNGLE_TURRET,
            REGION_RESTRICTION_TYPES.GunTurret).setAsDiversion()
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
    (STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_KEY_DOOR),
    (STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_BLACK_VOLT)
]





    #if stage == STAGE_GUN_FORTRESS:
    #    return REGION_INDICES.GUN_FORTRESS_CHECKPOINT_TWO

    #return 0

BACKTRACKING_REGIONS = [

    BacktrackRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_CHECKPOINT_THREE,
                    REGION_INDICES.WESTOPOLIS_BEHIND_THREE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_WESTOPOLIS, REGION_INDICES.WESTOPOLIS_CHECKPOINT_FIVE,
                    REGION_INDICES.WESTOPOLIS_CHECKPOINT_FOUR, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),

    BacktrackRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_ONE,
                    REGION_INDICES.DIGITAL_CIRCUIT_BEHIND_ONE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_THREE,
                    REGION_INDICES.DIGITAL_CIRCUIT_BEHIND_THREE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_DIGITAL_CIRCUIT, REGION_INDICES.DIGITAL_CIRCUIT_CHECKPOINT_FOUR,
                    REGION_INDICES.DIGITAL_CIRCUIT_BELOW_FOUR, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),

    BacktrackRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_FOUR,
                    REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_THREE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_GLYPHIC_CANYON, REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_SEVEN,
                    REGION_INDICES.GLYPHIC_CANYON_CHECKPOINT_SIX, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),

    BacktrackRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_ONE,
                    REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_ZERO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_TWO,
                    REGION_INDICES.LETHAL_HIGHWAY_ONE_FALL, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_THREE,
                    REGION_INDICES.LETHAL_HIGHWAY_TWO_FALL, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_FOUR,
                    REGION_INDICES.LETHAL_HIGHWAY_THREE_FALL_2, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_THREE_FALL_2,
                    REGION_INDICES.LETHAL_HIGHWAY_THREE_FALL, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_FIVE,
                    REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_FOUR, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_FIVE_BOMB,
                    REGION_INDICES.LETHAL_HIGHWAY_CHECKPOINT_FIVE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_FIVE_ROCKET,
                    REGION_INDICES.LETHAL_HIGHWAY_FIVE_BOMB, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),

    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_ONE,
                    REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_ZERO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.Zipwire),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_TOP_PATH,
                    REGION_INDICES.CRYPTIC_CASTLE_TWO_LOWER, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_FOUR,
                    REGION_INDICES.CRYPTIC_CASTLE_HAWK_END_ITEM, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_THREE,
                    REGION_INDICES.CRYPTIC_CASTLE_UPPER_HAWK_END_ITEM, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_FOUR,
                    REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_THREE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_FIVE,
                    REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_FOUR, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_FIVE,
                    REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_THREE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_SIX,
                    REGION_INDICES.CRYPTIC_CASTLE_WIND_BOTTOM, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_WIND_BOTTOM,
                    REGION_INDICES.CRYPTIC_CASTLE_FIVE_BALLOON, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.Torch).setHardLogicOnly(),
    BacktrackRegion(STAGE_CRYPTIC_CASTLE, REGION_INDICES.CRYPTIC_CASTLE_CHECKPOINT_SEVEN,
                    REGION_INDICES.CRYPTIC_CASTLE_END_HAWK_2_ITEM, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),

    BacktrackRegion(STAGE_PRISON_ISLAND, REGION_INDICES.PRISON_ISLAND_CHECKPOINT_ONE,
                    REGION_INDICES.PRISON_ISLAND_CHECKPOINT_ZERO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoRestriction),

    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_ONE,
                    REGION_INDICES.CENTRAL_CITY_CHECKPOINT_ZERO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_TWO,
                    REGION_INDICES.CENTRAL_CITY_CHECKPOINT_ZERO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_THREE,
                    REGION_INDICES.CENTRAL_CITY_CHECKPOINT_TWO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FOUR,
                    REGION_INDICES.CENTRAL_CITY_CHECKPOINT_THREE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.Explosion).setHardLogicOnly(),
    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FIVE,
                    REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FOUR, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_SIX,
                    REGION_INDICES.CENTRAL_CITY_BEHIND_SIX, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_SIX,
                    REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FIVE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoBacktracking).setHardLogicOnly(),
    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_SIX,
                    REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FOUR, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.Explosion),
    BacktrackRegion(STAGE_CENTRAL_CITY, REGION_INDICES.CENTRAL_CITY_CHECKPOINT_FOUR,
                    REGION_INDICES.CENTRAL_CITY_CHECKPOINT_SIX, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.Explosion).setHardLogicOnly(),

    BacktrackRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ONE,
                    REGION_INDICES.CIRCUS_PARK_CHECKPOINT_ZERO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_THREE,
                    REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_TWO_LOWER,
                    REGION_INDICES.CIRCUS_PARK_CHECKPOINT_TWO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.LightDash).setHardLogicOnly(),
    BacktrackRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FOUR,
                    REGION_INDICES.CIRCUS_PARK_THREE_LOWER, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoBacktracking).setHardLogicOnly(),
    BacktrackRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FIVE,
                    REGION_INDICES.CIRCUS_PARK_FOUR_LOWER, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_FOUR_LOWER,
                    REGION_INDICES.CIRCUS_PARK_CHECKPOINT_FOUR, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoBacktracking).setHardLogicOnly(),
    BacktrackRegion(STAGE_CIRCUS_PARK, REGION_INDICES.CIRCUS_PARK_CHECKPOINT_SIX,
                    REGION_INDICES.CIRCUS_PARK_SIX_BACK, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),


    BacktrackRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_TWO,
                    REGION_INDICES.THE_DOOM_CHECKPOINT_ONE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.Explosion),
    BacktrackRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_THREE,
                    REGION_INDICES.THE_DOOM_CHECKPOINT_TWO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_FOUR,
                    REGION_INDICES.THE_DOOM_CHECKPOINT_THREE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.Explosion),
    BacktrackRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_FIVE,
                    REGION_INDICES.THE_DOOM_CHECKPOINT_FOUR, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_FIVE,
                    REGION_INDICES.THE_DOOM_CHECKPOINT_ONE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    BacktrackRegion(STAGE_THE_DOOM, REGION_INDICES.THE_DOOM_CHECKPOINT_SIX,
                    REGION_INDICES.THE_DOOM_CHECKPOINT_FIVE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),

    BacktrackRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_GUN_JUMPER,
                    REGION_INDICES.SKY_TROOPS_CHECKPOINT_TWO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_GUN_JUMPER_2,
                    REGION_INDICES.SKY_TROOPS_THREE_LOWER, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_SKY_TROOPS, REGION_INDICES.SKY_TROOPS_CHECKPOINT_EIGHT,
                    REGION_INDICES.SKY_TROOPS_CHECKPOINT_SEVEN, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction),

    BacktrackRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_ONE,
                    REGION_INDICES.MAD_MATRIX_BEFORE_ONE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM,
                    REGION_INDICES.MAD_MATRIX_BLUE_TERMINAL, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_THREE,
                    REGION_INDICES.MAD_MATRIX_YELLOW_START,Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CHECKPOINT_FIVE,
                    REGION_INDICES.MAD_MATRIX_GREEN_START, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_GREEN_PROGRESSION,
                    REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_YELLOW_LIGHT_DASH,
                    REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM,
                    REGION_INDICES.MAD_MATRIX_CHECKPOINT_TWO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    BacktrackRegion(STAGE_MAD_MATRIX, REGION_INDICES.MAD_MATRIX_CIRCUIT_ROOM,
                    REGION_INDICES.MAD_MATRIX_CHECKPOINT_FOUR, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction),

    BacktrackRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_TWO,
                    REGION_INDICES.DEATH_RUINS_CHECKPOINT_ONE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_TWO,
                    REGION_INDICES.DEATH_RUINS_PULLEY, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_FOUR,
                    REGION_INDICES.DEATH_RUINS_RAIL_SECTION, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_FIVE,
                    REGION_INDICES.DEATH_RUINS_RAIL_SECTION,Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_DEATH_RUINS, REGION_INDICES.DEATH_RUINS_CHECKPOINT_SIX,
                    REGION_INDICES.DEATH_RUINS_CHECKPOINT_FIVE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),


    BacktrackRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_THREE,
                    REGION_INDICES.THE_ARK_BEFORE_THREE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_SIX,
                    REGION_INDICES.THE_ARK_BEFORE_SIX, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_THE_ARK, REGION_INDICES.THE_ARK_CHECKPOINT_EIGHT,
                    REGION_INDICES.THE_ARK_GOLD_BEETLE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),

    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_ONE,
                    REGION_INDICES.AIR_FLEET_PULLEY, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_ONE,
                    REGION_INDICES.AIR_FLEET_SECRET_1, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_ONE,
                    REGION_INDICES.AIR_FLEET_CHECKPOINT_ZERO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_ONE,
                    REGION_INDICES.AIR_FLEET_KEYDOOR_ENTRANCE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_RAILS,
                    REGION_INDICES.AIR_FLEET_CHECKPOINT_ZERO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction),

    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_TWO,
                    REGION_INDICES.AIR_FLEET_CHECKPOINT_ONE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_FOUR,
                    REGION_INDICES.AIR_FLEET_THREE_LOWER, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.SatelliteGun).setHardLogicOnly(),
    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_FIVE,
                    REGION_INDICES.AIR_FLEET_CHECKPOINT_FOUR, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_SIX,
                    REGION_INDICES.AIR_FLEET_CHECKPOINT_FIVE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_AIR_FLEET, REGION_INDICES.AIR_FLEET_CHECKPOINT_SEVEN,
                    REGION_INDICES.AIR_FLEET_OUTSIDE_SECTION, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),


    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_ZERO_BACKTRACK,
                    REGION_INDICES.IRON_JUNGLE_CHECKPOINT_ZERO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_ONE,
                    REGION_INDICES.IRON_JUNGLE_ZERO_BACKTRACK, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_TWO,
                    REGION_INDICES.IRON_JUNGLE_CHECKPOINT_ONE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_TWO,
                    REGION_INDICES.IRON_JUNGLE_EARLY_JUMPER, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),

    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_THREE,
                    REGION_INDICES.IRON_JUNGLE_ROCKET_LANDING, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),

    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_JUMPER_OR_LIGHT_DASH,
                    REGION_INDICES.IRON_JUNGLE_GUN_JUMPER, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.LightDash).setHardLogicOnly(),
    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FOUR,
                    REGION_INDICES.IRON_JUNGLE_CHECKPOINT_THREE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.LightDash).setHardLogicOnly(),
    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FIVE,
                    REGION_INDICES.IRON_JUNGLE_ANDROID_HOLE_TWO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_SIX,
                    REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FIVE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_IRON_JUNGLE, REGION_INDICES.IRON_JUNGLE_CHECKPOINT_SEVEN,
                    REGION_INDICES.IRON_JUNGLE_CHECKPOINT_FIVE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.LightDash).setHardLogicOnly(),

    BacktrackRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_FOUR,
                    REGION_INDICES.SPACE_GADGET_POST_ZIP, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_FOUR,
                    REGION_INDICES.SPACE_GADGET_THREE_LOWER, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_CHECKPOINT_FIVE,
                    REGION_INDICES.SPACE_GADGET_ABOVE_GOAL, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_SPACE_GADGET, REGION_INDICES.SPACE_GADGET_LAST_DARK_ROOM,
                    REGION_INDICES.SPACE_GADGET_CHECKPOINT_EIGHT, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),


    BacktrackRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_ONE,
                    REGION_INDICES.LOST_IMPACT_CHECKPOINT_ZERO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_FOUR,
                    REGION_INDICES.LOST_IMPACT_CHECKPOINT_THREE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_CHECKPOINT_SIX,
                    REGION_INDICES.LOST_IMPACT_BEHIND_SIX, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LOST_IMPACT, REGION_INDICES.LOST_IMPACT_EIGHT_GUN_LIFT,
                    REGION_INDICES.LOST_IMPACT_CHECKPOINT_SEVEN, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction),

    BacktrackRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_ONE,
                    REGION_INDICES.GUN_FORTRESS_CHECKPOINT_ZERO, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_TWO,
                    REGION_INDICES.GUN_FORTRESS_CHECKPOINT_ONE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_THREE,
                    REGION_INDICES.GUN_FORTRESS_ZIPWIRE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_FIVE,
                    REGION_INDICES.GUN_FORTRESS_BELOW_KEY_FIVE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_GUN_FORTRESS, REGION_INDICES.GUN_FORTRESS_CHECKPOINT_SIX,
                    REGION_INDICES.GUN_FORTRESS_POST_ZIPLINE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),

    BacktrackRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_THREE,
                    REGION_INDICES.BLACK_COMET_FIRST_WARP_HOLE_AREA, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.WarpHole).setHardLogicOnly(),
    BacktrackRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_FIVE,
                    REGION_INDICES.BLACK_COMET_FOUR_GUN_PATH, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.WarpHole).setHardLogicOnly(),
    BacktrackRegion(STAGE_BLACK_COMET, REGION_INDICES.BLACK_COMET_CHECKPOINT_SIX,
                    REGION_INDICES.BLACK_COMET_FIVE_PIT, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.WarpHole).setHardLogicOnly(),

    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_ONE,
                    REGION_INDICES.LAVA_SHELTER_LOWER_ZERO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_TWO,
                    REGION_INDICES.LAVA_SHELTER_ONE_LOWER, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_THREE,
                    REGION_INDICES.LAVA_SHELTER_PULLEY_OR_LAVA, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FOUR,
                    REGION_INDICES.LAVA_SHELTER_CHECKPOINT_THREE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoBacktracking).setHardLogicOnly(),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FIVE,
                    REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FOUR, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_DEFENSE_FOUR,
                    REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FIVE, Options.LogicLevel.option_hard,
                    REGION_RESTRICTION_TYPES.LightDash),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_SEVEN,
                    REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FIVE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_SIX,
                    REGION_INDICES.LAVA_SHELTER_PULLEY_DARK, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_SIX,
                    REGION_INDICES.LAVA_SHELTER_CHECKPOINT_FIVE, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_LAVA_SHELTER, REGION_INDICES.LAVA_SHELTER_CHECKPOINT_EIGHT,
                    REGION_INDICES.LAVA_SHELTER_WIND, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),

    BacktrackRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_ONE,
                    REGION_INDICES.COSMIC_FALL_FIRST_ENEMIES, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_TWO_AWAY,
                    REGION_INDICES.COSMIC_FALL_CHECKPOINT_TWO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_COSMIC_FALL, REGION_INDICES.COSMIC_FALL_CHECKPOINT_FOUR,
                    REGION_INDICES.COSMIC_FALL_BALLOON_RISE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),


    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_TWO,
                    REGION_INDICES.FINAL_HAUNT_CHECKPOINT_ONE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_VACUUM,
                    REGION_INDICES.FINAL_HAUNT_CHECKPOINT_TWO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction),
    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_THREE,
                    REGION_INDICES.FINAL_HAUNT_HERO_SPLIT, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_THREE,
                    REGION_INDICES.FINAL_HAUNT_BLACK_VOLT_GROUND, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SHIELD_TWO,
                    REGION_INDICES.FINAL_HAUNT_CHECKPOINT_FOUR, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_CHECKPOINT_FIVE,
                    REGION_INDICES.FINAL_HAUNT_FOUR_LOWER, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    # Caveat, if you've been to check 5 you can get back, but if not?
    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_FIVE_VACUUM,
                    REGION_INDICES.FINAL_HAUNT_CHECKPOINT_FIVE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_VOLT_OR_FIVE,
                    REGION_INDICES.FINAL_HAUNT_CHECKPOINT_FIVE, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_FINAL_HAUNT, REGION_INDICES.FINAL_HAUNT_SHIELD_THREE,
                    REGION_INDICES.FINAL_HAUNT_CHECKPOINT_SIX, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),


    BacktrackRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_ONE,
                    REGION_INDICES.THE_LAST_WAY_KEY_DOOR_ROOM, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_TWO,
                    REGION_INDICES.THE_LAST_WAY_BLACK_VOLT_GROUND, Options.LogicLevel.option_easy,
                    REGION_RESTRICTION_TYPES.NoBacktracking),
    BacktrackRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_THREE,
                    REGION_INDICES.THE_LAST_WAY_CHECKPOINT_TWO, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_FOUR,
                    REGION_INDICES.THE_LAST_WAY_PRE_CHAOS_CONTROL_2, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
    BacktrackRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_FOUR,
                    REGION_INDICES.THE_LAST_WAY_BEHIND_KEY_DOOR, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.WarpHole).setHardLogicOnly(),
    BacktrackRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_BEHIND_KEY_DOOR,
                    REGION_INDICES.THE_LAST_WAY_KEY_DOOR_ROOM, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.KeyDoor).setHardLogicOnly(),
    BacktrackRegion(STAGE_THE_LAST_WAY, REGION_INDICES.THE_LAST_WAY_CHECKPOINT_FIVE,
                    REGION_INDICES.THE_LAST_WAY_CHECKPOINT_FOUR, Options.LogicLevel.option_normal,
                    REGION_RESTRICTION_TYPES.NoRestriction).setHardLogicOnly(),
]

# ManualEscapePaths = [
#     EscapePath(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_TWO_FALL,
#                [REGION_INDICES.LETHAL_HIGHWAY_ROCKET]),
#     EscapePath(STAGE_LETHAL_HIGHWAY, [REGION_INDICES.LETHAL_HIGHWAY_FIVE_BOMB,
#                                       REGION_INDICES.LETHAL_HIGHWAY_FIVE_ROCKET,
#                                       REGION_INDICES.LETHAL_HIGHWAY_FIVE_FALL],
#                []),
#     EscapePath(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_FIVE_ROCKET,
#                []),
#     EscapePath(STAGE_LETHAL_HIGHWAY, REGION_INDICES.LETHAL_HIGHWAY_FIVE_FALL,
#                []),
# ]

HasCheckpointZeroCache = {}

def HasCheckpointZero(stage):

    if stage in HasCheckpointZeroCache:
        return HasCheckpointZeroCache[stage]

    stage_name = LEVEL_ID_TO_LEVEL[stage].replace(" ", "_")
    checkpoint_keys = list([k for k in REGION_INDICES.__dict__.items() if
                            k[0].startswith(stage_name.upper()) and "CHECKPOINT_" in k[0] and
                            "CHECKPOINT_ZERO" in k[0]])

    hasCheckpointZero = len(checkpoint_keys) > 0
    HasCheckpointZeroCache[stage] = hasCheckpointZero
    return hasCheckpointZero

def stage_id_to_region(level_id: int, region_id) -> str:
    if level_id in BOSS_STAGES:
        raise Exception("Wrong function called" + str(level_id))
    region_name_base = Names.GetRegionName(level_id, region_id)
    region_name = "REGION_" + region_name_base
    return region_name

def boss_stage_id_to_region(level_id: int, region_id=0) -> str:
    if level_id not in BOSS_STAGES:
        raise Exception("Wrong function called" + str(level_id))
    level_name = LEVEL_ID_TO_LEVEL[level_id]
    region_name = "BOSS_REGION_" + level_name + "_" + str(region_id)
    return region_name



def BasePath(graph, start, goals, path=None):
    if path is None:
        path = []
    path = path + [start]  # create new list including this node

    if start in goals:
        return [path]  # one complete path found

    if start not in graph:
        return []  # dead end

    paths = []
    for neighbor in graph[start]:
        if neighbor not in path:  # avoid cycles / revisits
            new_paths = BasePath(graph, neighbor, goals, path)
            for p in new_paths:
                paths.append(p)
    return paths

def CheckpointEscapePathing(stage):
    graph = {}

    LH_regions = [i for i in INDIVIDUAL_LEVEL_REGIONS if i.stageId == stage]
    for region in LH_regions:
        fromRegions = region.fromRegions
        for i in fromRegions:
            if i not in graph:
                graph[i] = []

            graph[i].append(region.regionIndex)

        if region.isDiversion:
            for from_region in fromRegions:
                if region.regionIndex not in graph:
                    graph[region.regionIndex] = []

                toResult = str(from_region) + "d"
                graph[region.regionIndex].append(toResult)

                if toResult not in graph:
                    graph[toResult] = []

                graph[toResult].append(from_region)

    LH_bt_regions = [b for b in BACKTRACKING_REGIONS if b.stageId == stage]
    for b_region in LH_bt_regions:
        if b_region.backtrackFromRegion not in graph:
            graph[b_region.backtrackFromRegion] = []

        backtrackTo = str(b_region.backtrackToRegion) + "/" + str(b_region.backtrackFromRegion) + "b"
        graph[b_region.backtrackFromRegion].append(backtrackTo)

        if backtrackTo not in graph:
            graph[backtrackTo] = []

        graph[backtrackTo].append(b_region.backtrackToRegion)


    all_region_names = REGION_INDICES.__dict__.items()
    stage_name = LEVEL_ID_TO_LEVEL[stage].replace(" ", "_")
    stage_keys = [c for c in all_region_names if c[0].startswith(stage_name.upper())]
    checkpoint_keys = list([k for k in all_region_names if
                            k[0].startswith(stage_name.upper()) and
                            "CHECKPOINT_" in k[0] and "CHECKPOINT_ZERO" not in k[0]
                            ])

    checkpoint_indexes = [c[1] for c in checkpoint_keys]

    results = {}
    available_paths = BasePath(graph, 0, checkpoint_indexes, None)
    results[0] = available_paths
    for region in stage_keys:
        if region[1] == 0:
            continue

        available_paths = BasePath(graph, region[1], checkpoint_indexes, None)
        results[region[1]] = available_paths

    return results

def GenerateCheckpointPaths():
    checkpoint_paths = {}
    for stage in ALL_STAGES:
        results = CheckpointEscapePathing(stage)
        checkpoint_paths[stage] = results

    return checkpoint_paths


RegionEscapes = GenerateCheckpointPaths()
