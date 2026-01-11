
import copy
from typing import Dict, Optional

from BaseClasses import Location, Region, LocationProgressType
from . import Regions, Levels, Weapons, Objects, Names
from .Levels import *
from . import Utils as ShadowUtils
from .ObjectTypes import ObjectType

from .Objects import GetEnemyDistributionInStageByBaseType
from .Weapons import WeaponAttributes


class ShadowTheHedgehogLocation(Location):
    game: str = "Shadow The Hedgehog"

    def __init__(self, player, location_name, location_id, region=None):
        super().__init__(player, location_name, location_id, region)

LOCATION_TYPE_MISSION_CLEAR = 1
LOCATION_TYPE_MISSION_OBJECTIVE = 2
LOCATION_TYPE_ENEMY = 3
LOCATION_TYPE_TOKEN = 4
LOCATION_TYPE_CHECKPOINT = 5
LOCATION_TYPE_KEY = 6
LOCATION_TYPE_OTHER = 7
LOCATION_TYPE_CHARACTER = 8
LOCATION_TYPE_BOSS = 9
LOCATION_TYPE_WARP = 10
LOCATION_TYPE_WEAPON_HOLD = 11
LOCATION_TYPE_OBJECT = 12

@dataclass
class LocationInfo:
    location_type: int
    locationId: int
    name: str
    stageId: Optional[int]
    regionId: Optional[int]
    alignmentId: Optional[int]
    count: Optional[int]
    total: Optional[int]
    other: Optional[str]

    def __init__(self, location_type: int, locationId: int,
                 name: str, stageId: Optional[int] = None,
                 regionId: Optional[int] = None, alignmentId: Optional[int] = None,
                 count: Optional[int] = None, total: Optional[int] = None,
                 other: Optional[str] = None, flag: Optional[bool] = None):
        self.location_type = location_type
        self.locationId = locationId
        self.name = name
        self.stageId = stageId
        self.regionId = regionId
        self.alignmentId = alignmentId
        self.count = count
        self.total = total
        self.other = other
        self.flag = flag



@dataclass
class MissionClearLocation:
    stageId: int
    alignmentId: int
    requirement_count: Optional[int]
    mission_object_name: Optional[str]
    distribution = None
    requirements = None
    craft_requirements = None
    logicType: int
    craftLogicType: Optional[int]

    def __init__(self, stageId, alignmentId, requirement_count,
                 mission_object_name):
        self.stageId = stageId
        self.alignmentId = alignmentId
        self.requirement_count = requirement_count
        self.mission_object_name = mission_object_name
        self.logicType = Options.LogicLevel.option_normal
        self.craft_requirements = None
        self.craftLogicType = None
        self.setEnemyDistribution()


    def setEnemyDistribution(self):
        pass
        if self.mission_object_name == "Soldier":
            self.distribution = GetEnemyDistributionInStageByBaseType(self.stageId, ENEMY_CLASS_GUN)
        elif self.mission_object_name == "Alien":
            self.distribution = GetEnemyDistributionInStageByBaseType(self.stageId, ENEMY_CLASS_ALIEN)
        elif self.mission_object_name == "Artificial Chaos":
            self.distribution = GetEnemyDistributionInStageByBaseType(self.stageId, ENEMY_CLASS_ALIEN)

    def setDistribution(self, dist):
        #if len(dist.keys()) == 0:
        #    raise Exception("Invalid Distribution")

        self.distribution = dist
        return self

    def getDistribution(self):
        if self.distribution is not None:
            return self.distribution
        else:
            return {0:self.requirement_count}

    def setRequirement(self, reqs):
        if type(reqs) is not list:
            reqs = [reqs]
        self.requirements = reqs
        return self

    def setCraftRequirement(self, reqs, level):
        if type(reqs) is not list:
            reqs = [reqs]
        self.craft_requirements = reqs
        self.craftLogicType = level
        return self

    def setLogicLevel(self, level):
        self.logicType = level
        return self


class BossClearLocation:
    stageId: int
    name: str
    logicType: int
    requirements = None

    def __init__(self, stageId):
        self.stageId = stageId
        self.name = Levels.LEVEL_ID_TO_LEVEL[stageId]
        self.logicType = Options.LogicLevel.option_normal

    def setLogicType(self, type):
        self.logicType = type
        return self

    def setRequirement(self, req):
        self.requirements = req
        return self

ENEMY_CLASS_ALIEN = 0
ENEMY_CLASS_GUN = 1
ENEMY_CLASS_EGG = 2

@dataclass
class EnemySanityLocation:
    stageId: int
    enemyClass: int
    total_count: int
    mission_object_name: Optional[str]
    distribution: None

    def __init__(self, stageId, enemyClass, total_count, mission_objective_name):
        self.stageId = stageId
        self.enemyClass = enemyClass
        self.total_count = total_count
        self.mission_object_name = mission_objective_name

    def setEnemyDistribution(self, distribution):
        self.distribution = distribution
        return self

    def getDistribution(self):

        if self.distribution is not None:
            return self.distribution
        else:
            return {0: self.requirement_count}


@dataclass
class CheckpointLocation:
    stageId: int
    total_count: int
    distribution = None
    region = []

    def __init__(self, stageId, total_count):
        self.stageId = stageId
        self.total_count = total_count
        self.region = []
        for i in range(0, total_count):
            self.region.append(0)

    def setDistribution(self, dist):
        for region,available in dist.items():
            for l in available:
                self.region[l-1] = region
        return self

    def getRegion(self, index):
        return self.region[index-1]

@dataclass
class KeyLocation:
    stageId: int
    region = []

    def __init__(self, stageId):
        self.stageId = stageId
        self.region = [0,0,0,0,0]


    def setDistribution(self, dist):
        for region, available in dist.items():
            for l in available:
                self.region[l - 1] = region
        return self

    def getRegion(self, index):
        return self.region[index]


    def setIndividual(self, key, region):
        self.region[key-1] = region
        return self


@dataclass
class CharacterLocation:
    name: str

MissionClearLocations = [
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_DARK, 35, "Soldier"),
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_NEUTRAL, None, None),
    MissionClearLocation(STAGE_WESTOPOLIS, MISSION_ALIGNMENT_HERO, 45, "Alien"),

    MissionClearLocation(STAGE_DIGITAL_CIRCUIT, MISSION_ALIGNMENT_DARK, None, None)
    .setDistribution(
        {
            REGION_INDICIES.DIGITAL_CIRCUIT_DARK_WARP_HOLE: 1
        }
    ),
    MissionClearLocation(STAGE_DIGITAL_CIRCUIT, MISSION_ALIGNMENT_HERO, None, None),
    #MissionClearLocation(STAGE_DIGITAL_CIRCUIT, MISSION_ALIGNMENT_DARK, 1, "Core"),

    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_DARK, 5, "Temple").setDistribution(
        {
            0: 1,
            REGION_INDICIES.GLYPHIC_CANYON_PULLEY: 4
        }
    ),
    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_NEUTRAL, None, None).setDistribution(
        {
            REGION_INDICIES.GLYPHIC_CANYON_PULLEY: 1
        }
        ),
    MissionClearLocation(STAGE_GLYPHIC_CANYON, MISSION_ALIGNMENT_HERO, 60, "Alien"),


    MissionClearLocation(STAGE_LETHAL_HIGHWAY, MISSION_ALIGNMENT_DARK, None, None).setDistribution(
        {
            REGION_INDICIES.LETHAL_HIGHWAY_ROCKET: 1
        }
        ),
    MissionClearLocation(STAGE_LETHAL_HIGHWAY, MISSION_ALIGNMENT_HERO, 1, "Tank").setDistribution(
        {
            REGION_INDICIES.LETHAL_HIGHWAY_ROCKET: 1
        }
        )
        .setRequirement(REGION_RESTRICTION_TYPES.Gun)
        .setCraftRequirement(REGION_RESTRICTION_TYPES.ShadowRifle, Options.LogicLevel.option_easy),

    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_DARK, 5, "Lantern")
        .setDistribution(
        {
            REGION_INDICIES.CRYPTIC_CASTLE_TORCH: 2,
            REGION_INDICIES.CRYPTIC_CASTLE_HAWK: 1,
            REGION_INDICIES.CRYPTIC_CASTLE_BOMB_EASY_2: 1,
            REGION_INDICIES.CRYPTIC_CASTLE_HAWK_2: 1
        }
        )
        .setRequirement(REGION_RESTRICTION_TYPES.Torch),
    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.CRYPTIC_CASTLE_BOMB_EASY_2: 1,
        }
    ),
    MissionClearLocation(STAGE_CRYPTIC_CASTLE, MISSION_ALIGNMENT_HERO, 2, "Cream")
        .setDistribution(
        {
            REGION_INDICIES.CRYPTIC_CASTLE_BOMB_EASY_1: 1,
            REGION_INDICIES.CRYPTIC_CASTLE_BOMB_EASY_2: 1
        }
    ),

    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_DARK, 40, "Soldier"),
    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER: 1
        }
    ),

    MissionClearLocation(STAGE_PRISON_ISLAND, MISSION_ALIGNMENT_HERO, 5, "Disc")
        .setDistribution(
        {
            0: 1,
            REGION_INDICIES.PRISON_ISLAND_PULLEY_EASY: 1,
            REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER: 3
        }
    ),

    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_DARK, 20, "Soldier"),
    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.CIRCUS_PARK_PULLEY: 1
        }
    ),
    MissionClearLocation(STAGE_CIRCUS_PARK, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            REGION_INDICIES.CIRCUS_PARK_HERO_GOAL: 1
        }
    ),

    MissionClearLocation(STAGE_CENTRAL_CITY, MISSION_ALIGNMENT_DARK, 5, "Big Bomb")
        .setDistribution(
        {
            0: 1,
            REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA: 2,
            REGION_INDICIES.CENTRAL_CITY_TRAVERSE_EASY: 1,
            REGION_INDICIES.CENTRAL_CITY_ROCKET_2: 1
        }
    ),
    MissionClearLocation(STAGE_CENTRAL_CITY, MISSION_ALIGNMENT_HERO, 20, "Little Bomb")
        .setDistribution(
            Objects.GetCentralCityBombDistribution()
        )
    .setRequirement(REGION_RESTRICTION_TYPES.Vacuum),

    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_DARK, 60, "Soldier"),
    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.THE_DOOM_DOOR_1_SWITCH: 1
        }
        ),
    MissionClearLocation(STAGE_THE_DOOM, MISSION_ALIGNMENT_HERO, 10, "Researcher")
        .setDistribution(
        {
            0: 3,
            REGION_INDICIES.THE_DOOM_BOMBS: 5,
            REGION_INDICIES.THE_DOOM_DOOR_1_SWITCH: 2,
        }
        )
        .setRequirement(REGION_RESTRICTION_TYPES.Heal),

    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_DARK, 5, "Egg Ship")
        .setDistribution(
        {
            0: 1,
            REGION_INDICIES.SKY_TROOPS_ROCKET_NORMAL: 1,
            REGION_INDICIES.SKY_TROOPS_ROCKET: 2,
            REGION_INDICIES.SKY_TROOPS_HAWK_OR_VOLT: 1
        }
        )
    .setRequirement(REGION_RESTRICTION_TYPES.BlackArmsTurret),
    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.SKY_TROOPS_HAWK_OR_VOLT: 1
        }
    ),
    MissionClearLocation(STAGE_SKY_TROOPS, MISSION_ALIGNMENT_HERO, 5, "Temple")
        .setDistribution(
        {
            0: 1,
            REGION_INDICIES.SKY_TROOPS_ROCKET_NORMAL: 1,
            REGION_INDICIES.SKY_TROOPS_ROCKET: 2,
            REGION_INDICIES.SKY_TROOPS_HAWK_OR_VOLT: 1
        }
    ),

    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_DARK, 30, "Bomb")
        .setDistribution(
        {
            REGION_INDICIES.MAD_MATRIX_GUN: 30
        }
    ),
    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.MAD_MATRIX_RED_ENTRY: 1
        }
    ),

    MissionClearLocation(STAGE_MAD_MATRIX, MISSION_ALIGNMENT_HERO, 4, "Terminal")
        .setDistribution(
        {
            REGION_INDICIES.MAD_MATRIX_GUN: 1,
            REGION_INDICIES.MAD_MATRIX_YELLOW_ENTRY: 1,
            REGION_INDICIES.MAD_MATRIX_GREEN_PROGRESSION: 1,
            REGION_INDICIES.MAD_MATRIX_RED_ENTRY: 1
        }
    ),

    MissionClearLocation(STAGE_DEATH_RUINS, MISSION_ALIGNMENT_DARK, None, None)
        .setDistribution(
        {
            REGION_INDICIES.DEATH_RUINS_WALLS: 1
        }
        ),
    MissionClearLocation(STAGE_DEATH_RUINS, MISSION_ALIGNMENT_HERO, 50, "Alien"),

    MissionClearLocation(STAGE_THE_ARK, MISSION_ALIGNMENT_DARK, 4, "Defense Unit")
        .setDistribution(
        {
            REGION_INDICIES.THE_ARK_BLACK_VOLT: 4
        }
        )
    .setRequirement(REGION_RESTRICTION_TYPES.Gun),
    MissionClearLocation(STAGE_THE_ARK, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.THE_ARK_BLACK_VOLT: 1
        }
    ),

    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_DARK, 1, "President Aircraft")
        .setDistribution(
        {
            REGION_INDICIES.AIR_FLEET_PULLEY: 1
        }
        )
    .setRequirement(REGION_RESTRICTION_TYPES.Gun)
    .setCraftRequirement(REGION_RESTRICTION_TYPES.ShadowRifle, Options.LogicLevel.option_easy),
    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.AIR_FLEET_PULLEY: 1
        }
        ),
    MissionClearLocation(STAGE_AIR_FLEET, MISSION_ALIGNMENT_HERO, 35, "Alien"),

    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_DARK, 28, "Soldier"),
    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH: 1
        }
        ),
    MissionClearLocation(STAGE_IRON_JUNGLE, MISSION_ALIGNMENT_HERO, 1, "Egg Balloon")
        .setDistribution(
        {
            REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH: 1
        }
        )
        .setRequirement(REGION_RESTRICTION_TYPES.Gun)
        .setCraftRequirement(REGION_RESTRICTION_TYPES.ShadowRifle, Options.LogicLevel.option_easy),

    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_DARK, 6, "Defense Unit")
    .setDistribution(
        {
            0: 2,
            REGION_INDICIES.SPACE_GADGET_AIR_SAUCER: 4
        })
        .setRequirement(REGION_RESTRICTION_TYPES.Gun),
    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.SPACE_GADGET_AIR_SAUCER: 1
        }),
    MissionClearLocation(STAGE_SPACE_GADGET, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            REGION_INDICIES.SPACE_GADGET_AIR_SAUCER: 1
        }),
    MissionClearLocation(STAGE_LOST_IMPACT, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.LOST_IMPACT_GUN_LIFT: 1
        }
    ),
    MissionClearLocation(STAGE_LOST_IMPACT, MISSION_ALIGNMENT_HERO, 35, "Artificial Chaos"),

    MissionClearLocation(STAGE_GUN_FORTRESS, MISSION_ALIGNMENT_DARK, 3, "Computer")
    .setRequirement(REGION_RESTRICTION_TYPES.ShootOrTurret)
    .setDistribution(
        {
            REGION_INDICIES.GUN_FORTRESS_PULLEY: 1,
            REGION_INDICIES.GUN_FORTRESS_ROCKET_NORMAL: 1,
            REGION_INDICIES.GUN_FORTRESS_KEY_OR_ZIPLINE: 1,
        }
    ),
    MissionClearLocation(STAGE_GUN_FORTRESS, MISSION_ALIGNMENT_HERO, None, None)
    .setDistribution(
        {
            REGION_INDICIES.GUN_FORTRESS_KEY_OR_ZIPLINE: 1
        }
    ),

    MissionClearLocation(STAGE_BLACK_COMET, MISSION_ALIGNMENT_DARK, 50, "Soldier"),
    MissionClearLocation(STAGE_BLACK_COMET, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            REGION_INDICIES.BLACK_COMET_FLOATING_ENEMY_WALL: 1
        }
    ),

    MissionClearLocation(STAGE_LAVA_SHELTER, MISSION_ALIGNMENT_DARK, 5, "Defense")
        .setDistribution(
        {
            0: 1,
            REGION_INDICIES.LAVA_SHELTER_PULLEY_OR_LAVA: 3,
            REGION_INDICIES.LAVA_SHELTER_PULLEY_DARK: 1
        }
    ),
    MissionClearLocation(STAGE_LAVA_SHELTER, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            REGION_INDICIES.LAVA_SHELTER_PULLEY_OR_LAVA: 1
        }
    ),
    MissionClearLocation(STAGE_COSMIC_FALL, MISSION_ALIGNMENT_DARK, None, None)
        .setDistribution(
        {
            REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL: 1
        }
    ),
    MissionClearLocation(STAGE_COSMIC_FALL, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            REGION_INDICIES.COSMIC_FALL_COMPUTER_ROOM: 1
        }
    ),
    #MissionClearLocation(STAGE_COSMIC_FALL, MISSION_ALIGNMENT_HERO, 1, "Computer Room"),

    MissionClearLocation(STAGE_FINAL_HAUNT, MISSION_ALIGNMENT_DARK, 4, "Shield")
        .setDistribution(
        {
            REGION_INDICIES.FINAL_HAUNT_VACUUM: 1,
            REGION_INDICIES.FINAL_HAUNT_SHIELD_COUNT_2: 1,
            REGION_INDICIES.FINAL_HAUNT_SHIELD_COUNT_3: 2
        }
    ),
    MissionClearLocation(STAGE_FINAL_HAUNT, MISSION_ALIGNMENT_HERO, None, None)
        .setDistribution(
        {
            REGION_INDICIES.FINAL_HAUNT_LIGHT_DASH: 1
        }
    ),

    MissionClearLocation(STAGE_THE_LAST_WAY, MISSION_ALIGNMENT_NEUTRAL, None, None)
        .setDistribution(
        {
            REGION_INDICIES.THE_LAST_WAY_VOLT_OR_WARP: 1
        }
    )

]

BossClearLocations = \
[
    BossClearLocation(BOSS_BLACK_BULL_LH)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_EGG_BREAKER_CC)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_HEAVY_DOG)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_BLACK_BULL_DR)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_EGG_BREAKER_MM)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_BLUE_FALCON)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_EGG_BREAKER_IJ)
        .setRequirement(REGION_RESTRICTION_TYPES.GunTurret),
    BossClearLocation(BOSS_BLACK_DOOM_GF)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_DIABLON_GF)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_EGG_DEALER_BC)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_DIABLON_BC)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_EGG_DEALER_LS)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_BLACK_DOOM_CF)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_EGG_DEALER_CF)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_DIABLON_FH)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_BLACK_DOOM_FH)
        .setRequirement(REGION_RESTRICTION_TYPES.AnyStageWeapon)
        .setLogicType(Options.BossLogicLevel.option_easy),
    BossClearLocation(BOSS_DEVIL_DOOM)
]

def GetEnemyLocationName(stageId, enemyClass, objectName, i):
    id_name = int(str(LOCATION_ID_PLUS) + str(1) + str(stageId) + str(enemyClass) + str(i) + "3")
    objective_location_name = "Enemysanity:" + (LEVEL_ID_TO_LEVEL[stageId] + " " + objectName + " (" + str(i) + ")")

    return id_name, objective_location_name

def GetCheckpointLocationName(stageId, objectName, i):
    id_name = int(str(LOCATION_ID_PLUS) + str(1) + str(stageId) + str(0) + str(i) + "4")
    objective_location_name = "Checkpointsanity:" + (LEVEL_ID_TO_LEVEL[stageId] + " " + objectName + " (" + str(i) + ")")

    return id_name, objective_location_name

def GetCharacterLocationName(objectName,i):
    id_name = int(str(LOCATION_ID_PLUS) + str(1) + "000" + str(0) + str(i) + "5")
    objective_location_name = "Charactersanity:" + objectName

    return id_name, objective_location_name

def GetKeysanityLocationName(stageId, i):
    id_name = int(str(LOCATION_ID_PLUS) + str(0) + str(stageId) + str(i+1) + "7")
    view_name = (LEVEL_ID_TO_LEVEL[stageId] + " Key " + str(i+1))

    return id_name, view_name

def GetWeaponsanityLocationName(weaponName, weaponId):
    id_name = int(str(LOCATION_ID_PLUS) + str(weaponId) + "8")
    view_name = "Held Weapon:" + weaponName

    return id_name, view_name

def GetBossLocationName(bossName, bossStageId):
    id_name = int(str(LOCATION_ID_PLUS) + str(bossStageId) + str(LOCATION_TYPE_BOSS))
    view_name = "Boss:" + bossName

    return id_name, view_name

def GetClearLocation():
    return [LocationInfo(LOCATION_TYPE_OTHER, LOCATION_ID_PLUS + 1000, Levels.DevilDoom_Name,
                  stageId=None, alignmentId=None, total=None, count=None, other=None)]


def GetEnemySanityLocations():
    EnemySanityLocations = []
    for stage in [ s for s in Levels.ALL_STAGES if s not in Levels.BOSS_STAGES ]:
        dark_mission_enemies = GetEnemyDistributionInStageByBaseType(stage, ENEMY_CLASS_GUN)
        hero_mission_enemies = GetEnemyDistributionInStageByBaseType(stage, ENEMY_CLASS_ALIEN)
        egg_enemies = GetEnemyDistributionInStageByBaseType(stage, ENEMY_CLASS_EGG)

        if len(dark_mission_enemies.keys()) > 0:
            count = 0
            for items in dark_mission_enemies.values():
                count += items

            EnemySanityLocations.append(
                EnemySanityLocation(stage, ENEMY_CLASS_GUN, count, "GUN Soldier")
                    .setEnemyDistribution(dark_mission_enemies),
            )

        if len(hero_mission_enemies.keys()) > 0:
            count = 0
            for items in hero_mission_enemies.values():
                count += items
            EnemySanityLocations.append(
                EnemySanityLocation(stage, ENEMY_CLASS_ALIEN, count, "Black Alien")
                    .setEnemyDistribution(hero_mission_enemies),
            )

        if len(egg_enemies.keys()) > 0:
            count = 0
            for items in egg_enemies.values():
                count += items
            EnemySanityLocations.append(
                EnemySanityLocation(stage, ENEMY_CLASS_EGG, count, "Egg Robot")
                    .setEnemyDistribution(egg_enemies),
            )

    return EnemySanityLocations



#EnemySanityLocations = \
#[
#    EnemySanityLocation(STAGE_WESTOPOLIS, ENEMY_CLASS_ALIEN, 45, "Black Arm"),
#    EnemySanityLocation(STAGE_WESTOPOLIS, ENEMY_CLASS_GUN, 36, "GUN Soldier"),
#
#    EnemySanityLocation(STAGE_DIGITAL_CIRCUIT, ENEMY_CLASS_GUN, 46, "GUN Soldier"),
#    EnemySanityLocation(STAGE_DIGITAL_CIRCUIT, ENEMY_CLASS_ALIEN, 17, "Black Arm"),
#
#    EnemySanityLocation(STAGE_GLYPHIC_CANYON, ENEMY_CLASS_GUN, 8, "GUN Soldier"),
#    EnemySanityLocation(STAGE_GLYPHIC_CANYON, ENEMY_CLASS_ALIEN, 60, "Black Arm"),
#
#    EnemySanityLocation(STAGE_LETHAL_HIGHWAY, ENEMY_CLASS_GUN, 30, "GUN Soldier"),
#    EnemySanityLocation(STAGE_LETHAL_HIGHWAY, ENEMY_CLASS_ALIEN, 137, "Black Arm"),
#
#    EnemySanityLocation(STAGE_CRYPTIC_CASTLE, ENEMY_CLASS_EGG, 17, "Egg Pawn"),
#    EnemySanityLocation(STAGE_CRYPTIC_CASTLE, ENEMY_CLASS_ALIEN, 52, "Black Arm"),
#
#    EnemySanityLocation(STAGE_PRISON_ISLAND, ENEMY_CLASS_GUN, 41, "GUN Soldier"),
#    EnemySanityLocation(STAGE_PRISON_ISLAND, ENEMY_CLASS_ALIEN, 88, "Black Arm"),
#
#    EnemySanityLocation(STAGE_CIRCUS_PARK, ENEMY_CLASS_GUN, 21, "GUN Soldier"),
#    EnemySanityLocation(STAGE_CIRCUS_PARK, ENEMY_CLASS_EGG, 29, "Egg Pawn"),
#
#    #EnemySanityLocation(STAGE_CENTRAL_CITY, ENEMY_CLASS_GUN, 100, "GUN Soldier"),
#    #EnemySanityLocation(STAGE_CENTRAL_CITY, ENEMY_CLASS_ALIEN, 100, "Black Arm"),
#    # 39 BA, 28G, time limit..
#
#    EnemySanityLocation(STAGE_THE_DOOM, ENEMY_CLASS_GUN, 60, "GUN Soldier"),
#
#    EnemySanityLocation(STAGE_SKY_TROOPS, ENEMY_CLASS_ALIEN, 73, "Black Arm"),
#    EnemySanityLocation(STAGE_SKY_TROOPS, ENEMY_CLASS_EGG, 11, "Egg Pawn"),
#
#    EnemySanityLocation(STAGE_MAD_MATRIX, ENEMY_CLASS_EGG, 31, "Egg Pawn"),
#    EnemySanityLocation(STAGE_MAD_MATRIX, ENEMY_CLASS_ALIEN, 8, "Black Arm"),
#
#    EnemySanityLocation(STAGE_DEATH_RUINS, ENEMY_CLASS_GUN, 21, "GUN Soldier"),
#    EnemySanityLocation(STAGE_DEATH_RUINS, ENEMY_CLASS_ALIEN, 50, "Black Arm"),
#
#    EnemySanityLocation(STAGE_THE_ARK, ENEMY_CLASS_GUN, 74, "GUN Soldier"),
#    EnemySanityLocation(STAGE_THE_ARK, ENEMY_CLASS_ALIEN, 21, "Black Arm"),
#
#    EnemySanityLocation(STAGE_AIR_FLEET, ENEMY_CLASS_GUN, 48, "GUN Soldier"),
#    EnemySanityLocation(STAGE_AIR_FLEET, ENEMY_CLASS_ALIEN, 35, "Black Arm"),
##
#    EnemySanityLocation(STAGE_IRON_JUNGLE, ENEMY_CLASS_GUN, 28, "GUN Soldier"),
#    EnemySanityLocation(STAGE_IRON_JUNGLE, ENEMY_CLASS_EGG, 37, "Egg Pawn"),
#
#    EnemySanityLocation(STAGE_SPACE_GADGET, ENEMY_CLASS_GUN, 25, "GUN Soldier"),
#    EnemySanityLocation(STAGE_SPACE_GADGET, ENEMY_CLASS_ALIEN, 33, "Black Arm"),
#
#    EnemySanityLocation(STAGE_LOST_IMPACT, ENEMY_CLASS_GUN, 37, "GUN Soldier"),
#    EnemySanityLocation(STAGE_LOST_IMPACT, ENEMY_CLASS_ALIEN, 35, "Artificial Chaos"),
#
#    EnemySanityLocation(STAGE_GUN_FORTRESS, ENEMY_CLASS_GUN, 94, "GUN Soldier"),
#    EnemySanityLocation(STAGE_GUN_FORTRESS, ENEMY_CLASS_ALIEN, 18, "Black Arm"),
#
#    EnemySanityLocation(STAGE_BLACK_COMET, ENEMY_CLASS_GUN, 53, "GUN Soldier"),
#    EnemySanityLocation(STAGE_BLACK_COMET, ENEMY_CLASS_ALIEN, 83, "Black Arm"),
#    # To Handle random respawns from the ships -- might want to make BA lower
#
#    EnemySanityLocation(STAGE_LAVA_SHELTER, ENEMY_CLASS_EGG, 74, "Egg Robot"),
#
#    EnemySanityLocation(STAGE_COSMIC_FALL, ENEMY_CLASS_GUN, 7, "GUN Soldier"),
#    EnemySanityLocation(STAGE_COSMIC_FALL, ENEMY_CLASS_ALIEN, 24, "Black Arm"),
#
#    EnemySanityLocation(STAGE_FINAL_HAUNT, ENEMY_CLASS_ALIEN, 122, "Black Arm"),
#]

CheckpointLocations = \
[
    CheckpointLocation(STAGE_WESTOPOLIS, 6),
    CheckpointLocation(STAGE_DIGITAL_CIRCUIT, 7)
        .setDistribution(
        {
            0: [1,2,3,4,5,6],
            REGION_INDICIES.DIGITAL_CIRCUIT_DARK_WARP_HOLE: [7]
        }
    ),
    CheckpointLocation(STAGE_GLYPHIC_CANYON, 8)
        .setDistribution(
        {
            0: [1,2,3],
            REGION_INDICIES.GLYPHIC_CANYON_PULLEY: [4,5,6,7,8]
        }
    ),
    CheckpointLocation(STAGE_LETHAL_HIGHWAY, 5)
        .setDistribution(
        {
            0: [1,2],
            REGION_INDICIES.LETHAL_HIGHWAY_ROCKET: [3,4,5]
        }
    ),

    CheckpointLocation(STAGE_CRYPTIC_CASTLE, 8)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.CRYPTIC_CASTLE_TORCH: [2],
            REGION_INDICIES.CRYPTIC_CASTLE_HAWK: [3,4,5],
            REGION_INDICIES.CRYPTIC_CASTLE_BOMB_EASY_2: [6,8],
            REGION_INDICIES.CRYPTIC_CASTLE_HAWK_2: [7]
        }
    ),
    CheckpointLocation(STAGE_PRISON_ISLAND, 7)
        .setDistribution(
        {
            0: [1,2],
            REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER: [3,4,5,6,7]
        }
    ),
    CheckpointLocation(STAGE_CIRCUS_PARK, 7)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.CIRCUS_PARK_ZIP_WIRE: [2],
            REGION_INDICIES.CIRCUS_PARK_ROCKET_EASY: [3,4,5],
            REGION_INDICIES.CIRCUS_PARK_ROCKET: [6],
            REGION_INDICIES.CIRCUS_PARK_PULLEY: [7]
        }
    ),
    CheckpointLocation(STAGE_CENTRAL_CITY, 6)
        .setDistribution(
        {
            0: [2, 3],
            REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA: [1],
            REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA_2: [4],
            REGION_INDICIES.CENTRAL_CITY_ROCKET_2: [5,6]
        }
    ),
    CheckpointLocation(STAGE_THE_DOOM, 6)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.THE_DOOM_BOMBS: [2,3],
            REGION_INDICIES.THE_DOOM_DOOR_1_SWITCH: [4,5,6]
        }
    ),

    CheckpointLocation(STAGE_SKY_TROOPS, 8)
        .setDistribution(
        {
            0: [1,2],
            REGION_INDICIES.SKY_TROOPS_ROCKET_NORMAL: [3],
            REGION_INDICIES.SKY_TROOPS_ROCKET: [4,5,6],
            REGION_INDICIES.SKY_TROOPS_HAWK_OR_VOLT: [7,8]
        }
    ),

    CheckpointLocation(STAGE_MAD_MATRIX, 6)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.MAD_MATRIX_GUN: [2,4,6],
            REGION_INDICIES.MAD_MATRIX_YELLOW_ENTRY: [3],
            REGION_INDICIES.MAD_MATRIX_GREEN_ENTRY: [5]
        }
    ),
    CheckpointLocation(STAGE_DEATH_RUINS, 7)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.DEATH_RUINS_PULLEY: [2,3,4,5],
            REGION_INDICIES.DEATH_RUINS_WALLS: [6,7]
        }
    ),
    CheckpointLocation(STAGE_THE_ARK, 8)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.THE_ARK_BLACK_VOLT: [2,3,4,5,6,7,8]
        }
    ),
    CheckpointLocation(STAGE_AIR_FLEET, 8)
        .setDistribution(
        {
            REGION_INDICIES.AIR_FLEET_PULLEY: [1,2,3,4,5,6,7,8]
        }
    ),
    CheckpointLocation(STAGE_IRON_JUNGLE, 8)
        .setDistribution(
        {
            0: [1,2],
            REGION_INDICIES.IRON_JUNGLE_ROCKET: [3],
            REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH: [4,5,6,8],
            REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH_DARK: [7]
        }
    ),
    CheckpointLocation(STAGE_SPACE_GADGET, 8).
        setDistribution(
        {
            0: [1,2,3],
            REGION_INDICIES.SPACE_GADGET_ZIPWIRE: [6],
            REGION_INDICIES.SPACE_GADGET_AIR_SAUCER: [4,5,7,8]
        }
    ),
    CheckpointLocation(STAGE_LOST_IMPACT, 8)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.LOST_IMPACT_GUN_LIFT: [2,3,4,5,6,7,8]
        }
    ),
    CheckpointLocation(STAGE_GUN_FORTRESS, 7)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.GUN_FORTRESS_PULLEY: [2],
            REGION_INDICIES.GUN_FORTRESS_ZIPWIRE: [3],
            REGION_INDICIES.GUN_FORTRESS_ROCKET_NORMAL: [4,5,6,7]
        }
    ),
    CheckpointLocation(STAGE_BLACK_COMET, 8)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.BLACK_COMET_AIR_SAUCER: [2],
            REGION_INDICIES.BLACK_COMET_WARP_HOLE: [3,4,5,6],
            REGION_INDICIES.BLACK_COMET_FLOATING_ENEMY_WALL: [7,8]
        }
    ),
    CheckpointLocation(STAGE_LAVA_SHELTER, 8)
        .setDistribution(
        {
            0: [1,2],
            REGION_INDICIES.LAVA_SHELTER_PULLEY_OR_LAVA: [3, 4, 5, 7, 8],
            REGION_INDICIES.LAVA_SHELTER_PULLEY_DARK: [6]
        }
    ),
    CheckpointLocation(STAGE_COSMIC_FALL, 7)
        .setDistribution(
        {
            REGION_INDICIES.COSMIC_FALL_ZIPWIRE: [1],
            REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL: [2,3,4,5,6],
            REGION_INDICIES.COSMIC_FALL_COMPUTER_ROOM: [7]
        }
    ),

    CheckpointLocation(STAGE_FINAL_HAUNT, 8)
        .setDistribution(
        {
            0: [1,2],
            REGION_INDICIES.FINAL_HAUNT_HARD_VACUUM_OR_BLACK_VOLT: [3],
            REGION_INDICIES.FINAL_HAUNT_ROCKET_NORMAL: [4, 5],
            REGION_INDICIES.FINAL_HAUNT_LIGHT_DASH: [6,7,8],
        }
    ),

    CheckpointLocation(STAGE_THE_LAST_WAY, 7)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.THE_LAST_WAY_BLACK_VOLT: [2,3],
            REGION_INDICIES.THE_LAST_WAY_VOLT_OR_WARP: [4,5],
            REGION_INDICIES.THE_LAST_WAY_LIGHT_DASH_EASY: [6,7]
        }
    )
]

KeyLocations = \
[
    KeyLocation(STAGE_WESTOPOLIS)
        .setDistribution(
        {
            0: [1,3,4,5],
            REGION_INDICIES.WESTOPOLIS_PULLEY: [2]
        }
    ),
    KeyLocation(STAGE_DIGITAL_CIRCUIT)
        .setDistribution(
        {
            0: [1,2,3,4],
            REGION_INDICIES.DIGITAL_CIRCUIT_DARK_WARP_HOLE: [5]
        }
    ),
    KeyLocation(STAGE_GLYPHIC_CANYON)
        .setDistribution(
        {
            0: [1,2,3],
            REGION_INDICIES.GLYPHIC_CANYON_PULLEY: [4,5]
        }
    ),
    KeyLocation(STAGE_LETHAL_HIGHWAY)
        .setDistribution(
        {
            0: [1,2,3],
            REGION_INDICIES.LETHAL_HIGHWAY_ROCKET: [4],
            REGION_INDICIES.LETHAL_HIGHWAY_PULLEY: [5],
        }
    ),
    KeyLocation(STAGE_CRYPTIC_CASTLE)
        .setDistribution(
        {
            REGION_INDICIES.CRYPTIC_CASTLE_BALLOON: [1],
            REGION_INDICIES.CRYPTIC_CASTLE_HAWK: [2],
            REGION_INDICIES.CRYPTIC_CASTLE_BOMB_EASY_2: [3,4,5]
        }
    ),
    KeyLocation(STAGE_PRISON_ISLAND)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.PRISON_ISLAND_AIR_SAUCER: [2,3,4,5],
        }
    ),
    KeyLocation(STAGE_CIRCUS_PARK)
        .setDistribution(
        {
            REGION_INDICIES.CIRCUS_PARK_ZIP_WIRE: [1],
            REGION_INDICIES.CIRCUS_PARK_ROCKET_EASY: [2,3],
            REGION_INDICIES.CIRCUS_PARK_ROCKET: [4],
            REGION_INDICIES.CIRCUS_PARK_PULLEY: [5]
        }
    ),
    KeyLocation(STAGE_CENTRAL_CITY)
        .setDistribution(
        {
            0: [2],
            REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA: [1],
            REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA_2: [3],
            REGION_INDICIES.CENTRAL_CITY_ROCKET_2: [4],
            REGION_INDICIES.CENTRAL_CITY_BOMB_OR_BAZOOKA_3: [5],
        }
    ),
    KeyLocation(STAGE_THE_DOOM)
        .setDistribution(
        {
            0: [1,2],
            REGION_INDICIES.THE_DOOM_BOMBS: [3,5],
            REGION_INDICIES.THE_DOOM_PULLEY_2: [4],
        }
    ),
    KeyLocation(STAGE_SKY_TROOPS)
        .setDistribution(
        {
            REGION_INDICIES.SKY_TROOPS_GUN_JUMPER_EASY: [1],
            REGION_INDICIES.SKY_TROOPS_ROCKET_NORMAL: [2],
            REGION_INDICIES.SKY_TROOPS_ROCKET: [3,4],
            REGION_INDICIES.SKY_TROOPS_HAWK_OR_VOLT: [5]
        }
    ),
    KeyLocation(STAGE_MAD_MATRIX)
        .setDistribution(
        {
            REGION_INDICIES.MAD_MATRIX_GUN: [1],
            REGION_INDICIES.MAD_MATRIX_YELLOW_ENTRY: [2],
            REGION_INDICIES.MAD_MATRIX_GREEN_PROGRESSION: [3],
            REGION_INDICIES.MAD_MATRIX_RED_ENTRY: [4,5],
        }
    ),
    KeyLocation(STAGE_DEATH_RUINS)
        .setDistribution(
        {
            REGION_INDICIES.DEATH_RUINS_PULLEY: [1,2],
            REGION_INDICIES.DEATH_RUINS_WALLS: [3,4,5]
        }
    ),
    KeyLocation(STAGE_THE_ARK)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.THE_ARK_BLACK_VOLT: [2,3,4,5]
        }
    ),
    KeyLocation(STAGE_AIR_FLEET)
        .setDistribution(
        {
            REGION_INDICIES.AIR_FLEET_PULLEY: [1,2,3,4,5]
        }
    ),
    KeyLocation(STAGE_IRON_JUNGLE)
        .setDistribution(
        {
            REGION_INDICIES.IRON_JUNGLE_ROCKET: [1],
            REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH: [2,3,5],
            REGION_INDICIES.IRON_JUNGLE_LIGHT_DASH_DARK: [4]
        }
    ),
    KeyLocation(STAGE_SPACE_GADGET)
        .setDistribution(
        {
            0: [1,2],
            REGION_INDICIES.SPACE_GADGET_AIR_SAUCER: [3,4,5]
        }
    ),
    KeyLocation(STAGE_LOST_IMPACT)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.LOST_IMPACT_GUN_LIFT: [2,4],
            REGION_INDICIES.LOST_IMPACT_ROCKET: [3],
            REGION_INDICIES.LOST_IMPACT_BOMB_WALL: [5]
        }
    ),
    KeyLocation(STAGE_GUN_FORTRESS)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.GUN_FORTRESS_ZIPWIRE_NORMAL: [2],
            REGION_INDICIES.GUN_FORTRESS_ZIPWIRE: [3],
            REGION_INDICIES.GUN_FORTRESS_ROCKET_NORMAL: [4, 5]
        }
    ),
    KeyLocation(STAGE_BLACK_COMET)
        .setDistribution(
        {
            REGION_INDICIES.BLACK_COMET_AIR_SAUCER: [1,2],
            REGION_INDICIES.BLACK_COMET_WARP_HOLE: [3],
            REGION_INDICIES.BLACK_COMET_FLOATING_ENEMY_WALL: [4,5]
        }
    ),
    KeyLocation(STAGE_LAVA_SHELTER)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.LAVA_SHELTER_PULLEY: [2],
            REGION_INDICIES.LAVA_SHELTER_PULLEY_OR_LAVA: [3,5],
            REGION_INDICIES.LAVA_SHELTER_PULLEY_DARK: [4]
        }
    ),
    KeyLocation(STAGE_COSMIC_FALL)
        .setDistribution(
        {
            REGION_INDICIES.COSMIC_FALL_PULLEY_NORMAL: [1,2,3],
            REGION_INDICIES.COSMIC_FALL_GUN_JUMPER_PULLEY_HARD: [4],
            REGION_INDICIES.COSMIC_FALL_LD_OR_JUMPER: [5]
        }
    ),
    KeyLocation(STAGE_FINAL_HAUNT)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.FINAL_HAUNT_VACUUM: [2],
            REGION_INDICIES.FINAL_HAUNT_ROCKET_NORMAL: [3],
            REGION_INDICIES.FINAL_HAUNT_BLACK_VOLT_2: [4],
            REGION_INDICIES.FINAL_HAUNT_LIGHT_DASH: [5]
        }
    ),

    KeyLocation(STAGE_THE_LAST_WAY)
        .setDistribution(
        {
            0: [1],
            REGION_INDICIES.THE_LAST_WAY_BLACK_VOLT: [2,3,4],
            REGION_INDICIES.THE_LAST_WAY_VOLT_OR_WARP: [5]
        }
    ),

]



def GetStageInformation(stageId):
    missions = [m for m in MissionClearLocations if m.stageId == stageId]
    return missions

def GetStageEnemysanityInformation(stageId):
    return [ e for e in GetEnemySanityLocations() if e.stageId == stageId]

def GetAlignmentsForStage(stageId):
    missions = [ m.alignmentId for m in MissionClearLocations if m.stageId == stageId]

    missions_copy = copy.deepcopy(missions)
    missions.sort()
    assert missions == missions_copy

    return missions


def GetAllLocationInfo():
    mission_clear_locations = []
    token_locations = []
    mission_locations = []
    enemysanity_locations = []
    checkpointsanity_locations = []
    charactersanity_locations = []
    keysanity_locations = []
    weaponsanity_locations = []
    boss_locations = []
    warp_locations = []
    object_locations = []

    for level in Levels.ALL_STAGES:
        location_id, entry_location_name = GetLevelWarpName(level)
        info = LocationInfo(LOCATION_TYPE_WARP, location_id, entry_location_name,
                            stageId=level, alignmentId=None, count=None, total=None,
                            other=None)
        warp_locations.append(info)

    for object in Objects.GetObjectChecks():
        location_id, entry_location_name = Names.GetObjectLocationName(object)
        info = LocationInfo(LOCATION_TYPE_OBJECT, location_id, entry_location_name,
                            stageId=object.stage, alignmentId=None, count=None, total=None,
                            other=object.object_type, regionId=object.region, flag=object.is_hard)
        object_locations.append(info)

    for location in MissionClearLocations:
        location_id, completion_location_name = Levels.GetLevelCompletionNames(location.stageId, location.alignmentId)
        info = LocationInfo(LOCATION_TYPE_MISSION_CLEAR, location_id, completion_location_name,
                            stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                            other=None)
        mission_clear_locations.append(info)

        base_token_id, base_token_name = GetLevelTokenNames(location.stageId, location.alignmentId, Levels.ITEM_TOKEN_TYPE_STANDARD)
        info = LocationInfo(LOCATION_TYPE_TOKEN,base_token_id, base_token_name,
                            stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                            other=Levels.ITEM_TOKEN_TYPE_STANDARD)
        token_locations.append(info)

        if location.alignmentId != MISSION_ALIGNMENT_NEUTRAL:
            hero_or_dark_token_id, hero_or_dark_token_name = GetLevelTokenNames(location.stageId, location.alignmentId, Levels.ITEM_TOKEN_TYPE_ALIGNMENT)
            info = LocationInfo(LOCATION_TYPE_TOKEN, hero_or_dark_token_id, hero_or_dark_token_name,
                                stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                                other=Levels.ITEM_TOKEN_TYPE_ALIGNMENT)
            token_locations.append(info)

        if location.stageId in Levels.FINAL_STAGES:
            final_token_id, final_token_name = GetLevelTokenNames(location.stageId, location.alignmentId,
                                                                ITEM_TOKEN_TYPE_FINAL)
            info = LocationInfo(LOCATION_TYPE_TOKEN, final_token_id, final_token_name,
                                stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                                other=Levels.ITEM_TOKEN_TYPE_FINAL)
            token_locations.append(info)

        i = 0
        if location.requirement_count is not None:
            requirement_token_id, requirement_token_name = GetLevelTokenNames(location.stageId, location.alignmentId,
                                                                ITEM_TOKEN_TYPE_OBJECTIVE)
            info = LocationInfo(LOCATION_TYPE_TOKEN, requirement_token_id, requirement_token_name,
                                stageId=location.stageId, alignmentId=location.alignmentId, count=None, total=None,
                                other=Levels.ITEM_TOKEN_TYPE_OBJECTIVE)
            token_locations.append(info)

            for j in range(1, location.requirement_count+1):
                i += 1
                location_id, objective_location_name = (
                    GetLevelObjectNames(location.stageId, location.alignmentId, location.mission_object_name, j))
                info = LocationInfo(LOCATION_TYPE_MISSION_OBJECTIVE, location_id, objective_location_name,
                                   stageId=location.stageId, alignmentId=location.alignmentId,
                                    count=j, total=location.requirement_count, other=None)
                mission_locations.append(info)

    for enemy in GetEnemySanityLocations():
        i = 0
        for j in range(1, enemy.total_count+1):
            i += 1
            location_id, objective_location_name = (
                GetEnemyLocationName(enemy.stageId, enemy.enemyClass, enemy.mission_object_name, j))
            info = LocationInfo(LOCATION_TYPE_ENEMY, location_id, objective_location_name,
                               stageId=enemy.stageId, alignmentId=enemy.enemyClass,
                                count=j, total=enemy.total_count, other=None)
            enemysanity_locations.append(info)

    progression_locations = GetClearLocation()

    progression_locations.append(
        LocationInfo(LOCATION_TYPE_OTHER, LOCATION_ID_SHADOW_RIFLE_COMPLETE, "Shadow Rifle Complete", stageId=None, \
                     alignmentId=None, total=None, count=None, other=None))

    for location in CheckpointLocations:
        i = 0
        for j in range(1, location.total_count+1):
            i += 1
            location_id, objective_location_name = (
                GetCheckpointLocationName(location.stageId,"Checkpoint", j))
            info = LocationInfo(LOCATION_TYPE_CHECKPOINT, location_id, objective_location_name,
                               stageId=location.stageId, alignmentId=None,
                                count=j, total=location.total_count, other=None)
            checkpointsanity_locations.append(info)

    char_index = 0
    for character in CharacterToLevel.keys():
        location_id, objective_location_name = GetCharacterLocationName(character,char_index)
        info = LocationInfo(LOCATION_TYPE_CHARACTER, location_id, objective_location_name,
                            stageId=None, alignmentId=None,
                            count=None, total=None, other=character)
        charactersanity_locations.append(info)
        char_index+=1

    for key_location in KeyLocations:
        for i in range(0,5):
            key_location_id, key_location_name = GetKeysanityLocationName(key_location.stageId, i)
            info = LocationInfo(LOCATION_TYPE_KEY, key_location_id, key_location_name,
                                        stageId=key_location.stageId, alignmentId=None, count=i, total=5, other=None)
            keysanity_locations.append(info)

    for weapon in Weapons.WEAPON_INFO:
        weapon_location_id, weapon_location_name = GetWeaponsanityLocationName(weapon.name, weapon.game_id)
        info = LocationInfo(LOCATION_TYPE_WEAPON_HOLD, weapon_location_id, weapon_location_name,
                            stageId=None, alignmentId=None, count=None, total=None, other=weapon.name)
        weaponsanity_locations.append(info)

    for boss in BossClearLocations:

        if boss.stageId == BOSS_DEVIL_DOOM:
            continue

        boss_location_id, boss_location_name = GetBossLocationName(boss.name, boss.stageId)
        info = LocationInfo(LOCATION_TYPE_BOSS, boss_location_id, boss_location_name, stageId=boss.stageId,
                            alignmentId=None, count=None, total=None, other=boss.name)
        boss_locations.append(info)

        boss_token_id, boss_token_name = GetBossTokenNames(boss.stageId,
                                                            Levels.ITEM_TOKEN_TYPE_STANDARD)
        info = LocationInfo(LOCATION_TYPE_TOKEN, boss_token_id, boss_token_name,
                            stageId=boss.stageId, alignmentId=None, count=None, total=None,
                            other=Levels.ITEM_TOKEN_TYPE_BOSS)
        token_locations.append(info)

        if boss.stageId in Levels.FINAL_BOSSES:
            boss_token_id, boss_token_name = GetBossTokenNames(boss.stageId,
                                                               Levels.ITEM_TOKEN_TYPE_FINAL_BOSS)
            info = LocationInfo(LOCATION_TYPE_TOKEN, boss_token_id, boss_token_name,
                                stageId=boss.stageId, alignmentId=None, count=None, total=None,
                                other=Levels.ITEM_TOKEN_TYPE_FINAL_BOSS)
            token_locations.append(info)

    return (mission_clear_locations, mission_locations, progression_locations,
            enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
            token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
            warp_locations, object_locations)


def GetLocationDict():
    all_locations = GetAllLocationInfo()

    result = {}
    for location_type in all_locations:
        for location in location_type:
            result[location.name] = location.locationId

    return result

def GetDuplicateLocations():
    ll = GetLocationDict()
    known = {}
    for l in ll.items():
        l_name = l[0]
        l_id = l[1]
        if l_id in known:
            print(f"Found duplicate location ID ({l_id}) for: {l_name}, {known[l_id]}")

        if l_id not in known:
            known[l_id] = []

        known[l_id].append(l_name)

    return

#GetDuplicateLocations()

def GetLocationInfoDict():
    all_locations = GetAllLocationInfo()

    result = {}
    for location_type in all_locations:
        for location in location_type:
            result[location.locationId] = location

    return result



def is_token_required_by_goal(options, token : LocationInfo, available_levels):

    goal_dictates_missions = options.goal_missions > 0
    goal_dictates_dark_missions = options.goal_dark_missions > 0
    goal_dictates_hero_missions = options.goal_hero_missions > 0
    goal_dictates_final_missions = options.goal_final_missions > 0
    goal_dictates_neutral_missions = options.goal_missions > 0
    goal_dictates_progression_missions = options.goal_objective_missions > 0
    goal_dictates_boss_tokens = options.goal_bosses > 0
    goal_dictates_final_boss_tokens = options.goal_final_bosses > 0

    if token.stageId not in available_levels:
        return False

    if token.stageId == Levels.STAGE_THE_LAST_WAY and goal_dictates_neutral_missions and token.other == ITEM_TOKEN_TYPE_STANDARD and \
            (options.level_progression == Options.LevelProgression.option_select or \
            not options.include_last_way_shuffle):
        return False

    if goal_dictates_missions and token.other == ITEM_TOKEN_TYPE_STANDARD:
        return True

    if goal_dictates_dark_missions and token.other == ITEM_TOKEN_TYPE_ALIGNMENT and \
        token.alignmentId == MISSION_ALIGNMENT_DARK:
        return True

    if goal_dictates_hero_missions and token.other == ITEM_TOKEN_TYPE_ALIGNMENT and \
        token.alignmentId == MISSION_ALIGNMENT_HERO:
        return True

    if goal_dictates_neutral_missions and token.other == ITEM_TOKEN_TYPE_ALIGNMENT and \
        token.alignmentId == MISSION_ALIGNMENT_NEUTRAL:
        return True

    if goal_dictates_final_missions and token.other == ITEM_TOKEN_TYPE_FINAL:
        return True

    if goal_dictates_progression_missions and token.other == ITEM_TOKEN_TYPE_OBJECTIVE:
        return True

    if goal_dictates_boss_tokens and token.other == ITEM_TOKEN_TYPE_BOSS:
        return True

    if goal_dictates_final_boss_tokens and token.other == ITEM_TOKEN_TYPE_FINAL_BOSS:
        return True


    return False


def create_locations(world, regions: Dict[str, Region]):
    (clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
     token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
     warp_locations, object_locations) = GetAllLocationInfo()

    menu_region = regions["Menu"]

    object_location_checks = []

    for location in clear_locations:
        if location.stageId not in world.available_levels:
            continue

        if world.options.exclude_go_mode_items and location.stageId == STAGE_THE_LAST_WAY and \
            not world.options.include_last_way_shuffle:
            world.options.exclude_locations.value.add(location.name)

        within_region = regions[Regions.stage_id_to_region(location.stageId)]
        completion_location = ShadowTheHedgehogLocation(world.player, location.name, location.locationId, within_region)

        within_region.locations.append(completion_location)

    override_settings = world.options.percent_overrides

    if world.options.objective_sanity:
        for location in mission_locations:
            if location.stageId not in world.available_levels:
                continue

            location_details = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                      location.name, world.options,
                                                      location.stageId, location.alignmentId,
                                                      world.options.percent_overrides)

            result_sanity = ShadowUtils.GetObjectiveSanityFlag(world.options, location_details)
            if not result_sanity:
                continue

            if world.options.objective_sanity_system == Options.ObjectiveSanitySystem.option_individual:
                if (location.stageId, location.alignmentId) in Objects.STAGE_OBJECT_ITEMS:
                    lookup_info = Objects.STAGE_OBJECT_ITEMS[(location.stageId, location.alignmentId)]
                    is_objectable = lookup_info[1]
                    if is_objectable == Objects.WORKS_WITH_INDIVIDUAL:
                        continue

                    # Allow overriding stages to use count system here

            max_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                          location.name, world.options,
                                                          location.stageId, location.alignmentId,world.options.percent_overrides),
                location.total, location.stageId, location.alignmentId,
                override_settings)

            frequency_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_FREQUENCY,
                                                          location.name, world.options,
                                                          location.stageId, location.alignmentId,
                                                          world.options.percent_overrides),
                100, location.stageId, location.alignmentId,
                override_settings)

            if location.count <= max_required:
                if location.count % frequency_required == 0 or max_required == location.count:
                    within_region = regions[Regions.stage_id_to_region(location.stageId)]
                    completion_location = ShadowTheHedgehogLocation(world.player, location.name, location.locationId, within_region)
                    within_region.locations.append(completion_location)
                    #print("Add location", within_region.name, completion_location.name)

    if world.options.enemy_sanity and world.options.objective_sanity_system != Options.ObjectiveSanitySystem.option_individual:
        for enemy in enemysanity_locations:
            if enemy.stageId not in world.available_levels:
                continue

            if world.options.exclude_go_mode_items and enemy.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            max_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.name, world.options,
                                                          enemy.stageId, enemy.alignmentId,world.options.percent_overrides),
                enemy.total, enemy.stageId, enemy.alignmentId,
                override_settings)

            frequency_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY_FREQUENCY,
                                                          enemy.name, world.options,
                                                          enemy.stageId, enemy.alignmentId,world.options.percent_overrides),
                100, enemy.stageId, enemy.alignmentId,
                override_settings)

            if enemy.count <= max_required:
                if enemy.count % frequency_required == 0 or max_required == enemy.count:
                    within_region = regions[Regions.stage_id_to_region(enemy.stageId)]
                    #within_region = regions[Regions.get_max_stage_region_id(enemy.stageId)]
                    completion_location = ShadowTheHedgehogLocation(world.player, enemy.name, enemy.locationId, within_region)
                    within_region.locations.append(completion_location)

    if world.options.checkpoint_sanity:
        for checkpoint in checkpointsanity_locations:
            if checkpoint.stageId not in world.available_levels:
                continue

            if world.options.exclude_go_mode_items and checkpoint.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            found_check_level_info = [ c for c in CheckpointLocations if c.stageId == checkpoint.stageId ][0]
            region_index = found_check_level_info.getRegion(checkpoint.count)
            within_region = regions[Regions.stage_id_to_region(checkpoint.stageId, region_index)]
            completion_location = ShadowTheHedgehogLocation(world.player, checkpoint.name, checkpoint.locationId, within_region)
            within_region.locations.append(completion_location)

    #if world.options.key_sanity:
    #    for key in keysanity_locations:
    #        if key.stageId not in world.available_levels:
    #            continue
#
#            if world.options.exclude_go_mode_items and key.stageId == STAGE_THE_LAST_WAY and \
#                    not world.options.include_last_way_shuffle:
#                continue
#
#            found_key_level_info = [c for c in KeyLocations if c.stageId == key.stageId][0]
#            region_index = found_key_level_info.getRegion(key.count)
#            within_region = regions[Regions.stage_id_to_region(key.stageId, region_index)]
#            completion_location = ShadowTheHedgehogLocation(world.player, key.name, key.locationId, within_region)
#            within_region.locations.append(completion_location)

    for boss in boss_locations:
        if boss.stageId not in world.available_levels:
            continue
        region_name = Regions.stage_id_to_region(boss.stageId)
        if region_name not in regions:
            continue
        if boss.stageId == BOSS_DEVIL_DOOM:
            continue
        within_region = regions[region_name]
        completion_location = ShadowTheHedgehogLocation(world.player, boss.name, boss.locationId,
                                                        within_region)
        within_region.locations.append(completion_location)
        pass

    if world.options.character_sanity:
        for character in charactersanity_locations:
            region_name = Regions.character_name_to_region(character.other)
            if region_name not in regions:
                continue
            within_region = regions[region_name]
            completion_location = ShadowTheHedgehogLocation(world.player, character.name, character.locationId,
                                                            within_region)
            within_region.locations.append(completion_location)

    if world.options.weapon_sanity_hold > 0 :
        for weapon in weaponsanity_locations:
            if weapon.other not in world.available_weapons:
                continue

            if weapon.other in world.go_mode_weapons_only:
                continue

            region_name = Regions.weapon_name_to_region(weapon.other)
            within_region = regions[region_name]
            completion_location = ShadowTheHedgehogLocation(world.player, weapon.name, weapon.locationId,
                                                            within_region)
            within_region.locations.append(completion_location)

    for token in token_locations:
        goal_required = is_token_required_by_goal(world.options, token, world.available_levels)
        if not goal_required:
            continue

        within_region = regions[Regions.stage_id_to_region(token.stageId)]
        token_location = ShadowTheHedgehogLocation(world.player, token.name, token.locationId,
                                                        within_region)
        within_region.locations.append(token_location)
        world.token_locations.append(token)

    for warp in warp_locations:

        if not world.options.secret_story_progression or world.options.level_progression == Options.LevelProgression.option_select:
            continue

        if warp.stageId in Levels.LAST_STORY_STAGES and not world.options.include_last_way_shuffle:
            continue

        if warp.stageId in Levels.BOSS_STAGES and world.options.level_progression == Options.LevelProgression.option_select:
            continue

        if warp.stageId not in world.available_story_levels:
            continue

        within_region = regions[Regions.stage_id_to_region(warp.stageId)]
        warp_location = ShadowTheHedgehogLocation(world.player, warp.name, warp.locationId,
                                                   within_region)
        within_region.locations.append(warp_location)

    if world.options.rifle_components:
        rifle_location = ShadowTheHedgehogLocation(world.player, "Complete Shadow Rifle", LOCATION_ID_SHADOW_RIFLE_COMPLETE, menu_region)
        menu_region.locations.append(rifle_location)


    if world.options.shadow_boxes:
        for box_location in [ x for x in object_locations if x.other == ObjectType.SHADOW_BOX and
                              x.stageId in world.available_levels]:
            if world.options.exclude_go_mode_items and box_location.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue
            stage_region_name = Regions.stage_id_to_region(box_location.stageId, box_location.regionId)
            stage_region = regions[stage_region_name]
            box_location = ShadowTheHedgehogLocation(world.player, box_location.name,
                                                       box_location.locationId, stage_region)
            stage_region.locations.append(box_location)

    if world.options.energy_cores:

        for core_location in [ x for x in object_locations if (x.other == ObjectType.ENERGY_CORE or
                                 x.other == ObjectType.ENERGY_CORE_IN_WOOD_BOX) and
                                                              x.stageId in world.available_levels]:

            if world.options.exclude_go_mode_items and core_location.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            if core_location.regionId is not None:
                stage_region_name = Regions.stage_id_to_region(core_location.stageId, core_location.regionId)
                stage_region = regions[stage_region_name]
                core_location = ShadowTheHedgehogLocation(world.player, core_location.name,
                                                           core_location.locationId, stage_region)
                stage_region.locations.append(core_location)
            else:
                print("Error with core:", core_location)

    if world.options.door_sanity:

        for door_location in [ x for x in object_locations if x.other == ObjectType.KEY_DOOR and
                               x.stageId in world.available_levels]:

            if world.options.exclude_go_mode_items and door_location.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            stage_region_name = Regions.stage_id_to_region(door_location.stageId, door_location.regionId)
            stage_region = regions[stage_region_name]
            door_location = ShadowTheHedgehogLocation(world.player, door_location.name,
                                                       door_location.locationId, stage_region)
            stage_region.locations.append(door_location)

    if world.options.gold_beetle_sanity:

        for beetle_location in [ x for x in object_locations if x.other == ObjectType.GOLD_BEETLE and
                                 x.stageId in world.available_levels]:

            if world.options.exclude_go_mode_items and beetle_location.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            stage_region_name = Regions.stage_id_to_region(beetle_location.stageId, beetle_location.regionId)
            stage_region = regions[stage_region_name]
            beetle_location = ShadowTheHedgehogLocation(world.player, beetle_location.name,
                                                       beetle_location.locationId, stage_region)
            stage_region.locations.append(beetle_location)

    if world.options.key_sanity:

        for key_location in [ x for x in object_locations if x.other == ObjectType.KEY and
                                 x.stageId in world.available_levels]:

            if world.options.exclude_go_mode_items and key_location.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            stage_region_name = Regions.stage_id_to_region(key_location.stageId, key_location.regionId)
            stage_region = regions[stage_region_name]
            key_location = ShadowTheHedgehogLocation(world.player, key_location.name,
                                                       key_location.locationId, stage_region)
            stage_region.locations.append(key_location)


    if world.options.objective_sanity and world.options.objective_sanity_system != Options.ObjectiveSanitySystem.option_count_up:
        for i in Objects.STAGE_OBJECT_ITEMS.items():
            item_key = i[0]
            item_stage = item_key[0]
            item_alignment = item_key[1]

            item_type = i[1]
            item_type_data = item_type[0]

            if item_stage not in world.available_levels:
                continue

            if world.options.exclude_go_mode_items and item_stage == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            if item_type_data is None:
                print("Check enemy sanity values instead if possible")
            if type(item_type_data) is not list:
                item_types = [item_type_data]
            else:
                item_types = item_type_data

            if not world.options.enemy_objective_sanity:
                item_types = [ s for s in item_types if s not in Objects.GetStandardEnemyTypes() ]

            if len(item_types) == 0:
                continue

            item_allowed = item_type[1]

            if item_allowed == Objects.DOES_NOT_WORK_WITH_INDIVIDUAL:
                # Need to ensure these are included in the above system
                continue

            for search_type in item_types:
                for objective_location in [x for x in object_locations if x.other == search_type and
                                                                       x.stageId == item_stage]:

                    if (objective_location.stageId, objective_location.regionId) in NON_OBJECTIVESANITY_REGIONS:
                        continue

                    stage_region_name = Regions.stage_id_to_region(objective_location.stageId, objective_location.regionId)
                    stage_region = regions[stage_region_name]
                    new_objective_location = ShadowTheHedgehogLocation(world.player, objective_location.name,
                                                                objective_location.locationId, stage_region)
                    stage_region.locations.append(new_objective_location)
                    object_location_checks.append(objective_location)

                    #print("Add:", objective_location.name, i)


    if world.options.enemy_sanity and world.options.objective_sanity_system != Options.ObjectiveSanitySystem.option_count_up:
        enemy_types = Objects.GetStandardEnemyTypes()
        for objective_location in [x for x in object_locations if x.other in enemy_types and x not in object_location_checks and
                                   x.stageId in world.available_levels
                                    and (world.options.boss_enemy_sanity or x.stageId not in Levels.BOSS_STAGES)
                                    and (world.options.difficult_enemy_sanity or not x.flag) ]:

            if world.options.exclude_go_mode_items and objective_location.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            stage_region_name = Regions.stage_id_to_region(objective_location.stageId, objective_location.regionId)
            stage_region = regions[stage_region_name]
            new_objective_location = ShadowTheHedgehogLocation(world.player, objective_location.name,
                                                           objective_location.locationId, stage_region)
            stage_region.locations.append(new_objective_location)

    if world.options.item_sanity:
        item_types = Objects.GetItemBoxTypes()
        for objective_location in [x for x in object_locations if x.other in item_types and
                                   x.stageId in world.available_levels
                                    and (world.options.difficult_enemy_sanity or not x.flag) ]:

            if world.options.exclude_go_mode_items and objective_location.stageId == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            stage_region_name = Regions.stage_id_to_region(objective_location.stageId, objective_location.regionId)
            stage_region = regions[stage_region_name]
            new_objective_location = ShadowTheHedgehogLocation(world.player, objective_location.name,
                                                           objective_location.locationId, stage_region)
            stage_region.locations.append(new_objective_location)


    if world.options.level_progression != Options.LevelProgression.option_select:
        SetStoryClearEvents(world, world.player, regions)

    SetRegionEvents(world, world.player, regions)

    end_region = regions[Regions.stage_id_to_region(Levels.BOSS_DEVIL_DOOM)]
    devil_doom_location = ShadowTheHedgehogLocation(world.player, end_location[0].name, end_location[0].locationId, end_region)
    end_region.locations.append(devil_doom_location)

def increment_location_count(count, plus, t):
    return count + plus

def count_last_way_locations(world):
    backup_levels = world.available_levels
    backup_weapons = world.available_weapons
    restore_characters = world.options.character_sanity

    world.available_levels = [Levels.STAGE_THE_LAST_WAY]

    lw_weapons = []

    for weapon in Weapons.WEAPON_INFO:
        if WeaponAttributes.SPECIAL in weapon.attributes:
            continue
        levels_in = weapon.available_stages
        levels_in = [ (l[0] if type(l) is tuple else l) for l in levels_in  ]
        levels_left = [ l for l in levels_in if l in world.available_levels and l not in
                        [ b for b in backup_levels if b not in world.available_levels] ]
        if len(levels_left) == 0:
            continue
        lw_weapons.append(weapon.name)

    world.available_weapons = lw_weapons
    world.options.character_sanity = False

    result = count_locations(world)
    world.available_levels = backup_levels
    world.available_weapons = backup_weapons
    world.options.character_sanity = restore_characters

    return result

def count_locations(world):
    count = 0
    (mission_clear_locations, mission_locations, progression_locations,
     enemysanity_locations, checkpointsanity_locations,
     charactersanity_locations, token_locations, keysanity_locations,
     weaponsanity_locations, boss_locations, warp_locations,
     object_locations) = GetAllLocationInfo()

    mission_clear_locations = [ mc for mc in mission_clear_locations if mc.stageId
                                in world.available_levels]

    mission_locations = [ ml for ml in mission_locations if ml.stageId
                                in world.available_levels]

    enemysanity_locations = [ml for ml in enemysanity_locations if ml.stageId
                         in world.available_levels and (not world.options.exclude_go_mode_items or ml.stageId != STAGE_THE_LAST_WAY or \
                                world.options.include_last_way_shuffle)]

    checkpointsanity_locations = [ml for ml in checkpointsanity_locations if ml.stageId
                             in world.available_levels and (not world.options.exclude_go_mode_items or ml.stageId != STAGE_THE_LAST_WAY or \
                                world.options.include_last_way_shuffle)]

    charactersanity_locations = [ ml for ml in charactersanity_locations if ml.other in world.available_characters ]

    object_locations = [ml for ml in object_locations if ml.stageId
                                  in world.available_levels and (
                                              not world.options.exclude_go_mode_items or ml.stageId != STAGE_THE_LAST_WAY or \
                                              world.options.include_last_way_shuffle)]

    #keysanity_locations = [ks for ks in keysanity_locations if ks.stageId
    #                         in world.available_levels and (not world.options.exclude_go_mode_items or ks.stageId != STAGE_THE_LAST_WAY or \
    #                            world.options.include_last_way_shuffle)]

    boss_locations = [ b for b in boss_locations if b.stageId in world.available_levels ]

    weaponsanity_locations = [ml for ml in weaponsanity_locations if ml.other in world.available_weapons and
                              ml.other not in world.go_mode_weapons_only]

    override_settings = world.options.percent_overrides

    count = increment_location_count(count, len(mission_clear_locations), "mc")

    if world.options.objective_sanity:
        for location in mission_locations:

            if world.options.objective_sanity_system == Options.ObjectiveSanitySystem.option_individual:
                if (location.stageId, location.alignmentId) in Objects.STAGE_OBJECT_ITEMS:
                    lookup_info = Objects.STAGE_OBJECT_ITEMS[(location.stageId, location.alignmentId)]
                    is_objectable = lookup_info[1]
                    if is_objectable == Objects.WORKS_WITH_INDIVIDUAL:
                        continue

            location_details = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                         location.name, world.options,
                                                                         location.stageId, location.alignmentId,
                                                                         world.options.percent_overrides)

            result_sanity = ShadowUtils.GetObjectiveSanityFlag(world.options, location_details)
            if not result_sanity:
                continue

            max_required = ShadowUtils.getMaxRequired(
                location_details,
                location.total, location.stageId, location.alignmentId,
                override_settings)

            frequency_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_FREQUENCY,
                                                          location.name, world.options,
                                                          location.stageId, location.alignmentId,world.options.percent_overrides),
                100, location.stageId, location.alignmentId,
                override_settings)

            if location.count <= max_required:
                if location.count % frequency_required == 0 or max_required == location.count:
                    count = increment_location_count(count, 1, "o")

    if world.options.enemy_sanity and world.options.objective_sanity_system != Options.ObjectiveSanitySystem.option_individual:
        for enemy in enemysanity_locations:

            frequency_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY_FREQUENCY,
                                                          enemy.name, world.options,
                                                          enemy.stageId, enemy.alignmentId,world.options.percent_overrides),
                100, enemy.stageId, enemy.alignmentId,
                override_settings)

            max_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.name, world.options,
                                                          enemy.stageId, enemy.alignmentId,world.options.percent_overrides),
                enemy.total, enemy.stageId, enemy.alignmentId,
                override_settings)

            if enemy.count <= max_required:
                if enemy.count % frequency_required == 0 or max_required == enemy.count:
                    count = increment_location_count(count, 1, "e")

    if world.options.checkpoint_sanity:
        count = increment_location_count(count, len(checkpointsanity_locations), "c")

    if world.options.character_sanity:
        count = increment_location_count(count, len(charactersanity_locations), "ch")

    if world.options.key_sanity:
        count = increment_location_count(count, len([x for x in object_locations if x.other == ObjectType.KEY
                                                     if x.stageId in world.available_levels]), "c")

    count = increment_location_count(count, len(boss_locations), "b")
    #if world.options.include_last_way_shuffle and world.options.story_shuffle == Options.StoryShuffle.option_test3:
    #    count -= 1 # Devil Doom Boss

    if world.options.weapon_sanity_hold > 0:
        count = increment_location_count(count, len(weaponsanity_locations), "w")

    if world.options.shadow_boxes:
        count = increment_location_count(count, len([x for x in object_locations if x.other == ObjectType.SHADOW_BOX
                                                     if x.stageId in world.available_levels and (not world.options.exclude_go_mode_items or x.stageId != STAGE_THE_LAST_WAY or \
                                world.options.include_last_way_shuffle)]), "b")

    if world.options.gold_beetle_sanity:
        count = increment_location_count(count, len([x for x in object_locations if x.other == ObjectType.GOLD_BEETLE
                                                     if x.stageId in world.available_levels]), "g")

    if world.options.energy_cores:
        count = increment_location_count(count, len([x for x in object_locations if x.other == ObjectType.ENERGY_CORE
                                                     or x.other == ObjectType.ENERGY_CORE_IN_WOOD_BOX
                                                     if x.stageId in world.available_levels]), "c")

    if world.options.door_sanity:
        count = increment_location_count(count, len([x for x in object_locations if x.other == ObjectType.KEY_DOOR
                                                     if x.stageId in world.available_levels and (not world.options.exclude_go_mode_items or x.stageId != STAGE_THE_LAST_WAY or \
                                world.options.include_last_way_shuffle)]), "kd")

    object_location_checks = []
    if world.options.objective_sanity and world.options.objective_sanity_system != Options.ObjectiveSanitySystem.option_count_up:
        for i in Objects.STAGE_OBJECT_ITEMS.items():
            item_key = i[0]
            item_stage = item_key[0]
            item_alignment = item_key[1]

            item_type = i[1]
            item_type_data = item_type[0]

            if item_stage not in world.available_levels:
                continue

            if world.options.exclude_go_mode_items and item_stage == STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            if item_type_data is None:
                print("Check enemy sanity values instead if possible")
            if type(item_type_data) is not list:
                item_types = [item_type_data]
            else:
                item_types = item_type_data

            if not world.options.enemy_objective_sanity:
                item_types = [ s for s in item_types if s not in Objects.GetStandardEnemyTypes() ]

            if len(item_types) == 0:
                continue

            item_allowed = item_type[1]

            if item_allowed == Objects.DOES_NOT_WORK_WITH_INDIVIDUAL:
                # Need to ensure these are included in the above system
                continue

            for search_type in item_types:
                search_items = [x for x in object_locations if x.other == search_type and
                                                                       x.stageId == item_stage and
                                                             (x.stageId,x.regionId)  not in NON_OBJECTIVESANITY_REGIONS]
                object_location_checks.extend(search_items)

                count = increment_location_count(count, len(search_items), "oo")

    if world.options.enemy_sanity and world.options.objective_sanity_system != Options.ObjectiveSanitySystem.option_count_up:
        enemy_types = Objects.GetStandardEnemyTypes()
        enemy_sanity_object_checks = [x for x in object_locations if
         x.other in enemy_types and x not in object_location_checks and x.stageId in world.available_levels and
                                      (world.options.boss_enemy_sanity or x.stageId not in Levels.BOSS_STAGES)
                                      and (world.options.difficult_enemy_sanity or not x.flag) and
                                      (not world.options.exclude_go_mode_items or x.stageId != STAGE_THE_LAST_WAY or
                                       world.options.include_last_way_shuffle)]

        count = increment_location_count(count, len(enemy_sanity_object_checks), "oe")

    if world.options.item_sanity:
        item_types = Objects.GetItemBoxTypes()
        possible = [x for x in object_locations if x.other in item_types and
                                   x.stageId in world.available_levels
                                    and (world.options.difficult_enemy_sanity or not x.flag) and
                    (not world.options.exclude_go_mode_items or x.stageId != STAGE_THE_LAST_WAY or
                     world.options.include_last_way_shuffle)
                    ]

        count = increment_location_count(count, len(possible), "i")

    return count


def IsRegionAutoPassable(combined_regions, distribution):

    if len(combined_regions.keys()) == 0:
        return False

    if len(distribution.keys()) == 0:
        return False

    known = [0]
    for i in range(1, max(distribution.keys())+1):
        ref = [ c for c in combined_regions.items() if c[1] == i]
        found = False
        for r in ref:
            if r[0] in known:
                found = True
                break
        if not found:
            return False

    return True


def GetStagesWithNoRequirements(world):
    # This should also handle logic level

    logic_level = world.options.logic_level

    combined_regions = {}
    for i in Levels.INDIVIDUAL_LEVEL_REGIONS:
        if i.stageId not in combined_regions:
            combined_regions[i.stageId] = {}

        if i.logicType == Options.LogicLevel.option_easy and \
            logic_level != Options.LogicLevel.option_easy:
            for fromRegion in i.fromRegions:
                combined_regions[i.stageId][fromRegion] = i.regionIndex
        elif i.logicType == Options.LogicLevel.option_hard and \
            logic_level == Options.LogicLevel.option_hard:
            for fromRegion in i.fromRegions:
                combined_regions[i.stageId][fromRegion] = i.regionIndex

        if not world.options.weapon_sanity_unlock and IsWeaponsanityRestriction(i.restrictionTypes):
            for fromRegion in i.fromRegions:
                combined_regions[i.stageId][fromRegion] = i.regionIndex

        if not world.options.vehicle_logic and IsVeichleSanityRestriction(i.restrictionTypes):
            for fromRegion in i.fromRegions:
                combined_regions[i.stageId][fromRegion] = i.regionIndex

    # Need to handle combined regions

    # Need to limit by items not required

    stages = [m.stageId for m in MissionClearLocations
              if (m.distribution is None or
                  (
                      (len(m.distribution.keys()) == 1 and 0 in m.distribution.keys()) or

                      IsRegionAutoPassable(combined_regions[m.stageId], m.distribution)

                   ))
              and m.requirement_count is None and Levels.LEVEL_ID_TO_LEVEL[m.stageId] not in world.options.excluded_stages ]
    return list(set(stages))

def getLocationGroups():
    (clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
     token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
     warp_locations, object_locations) = GetAllLocationInfo()

    groups = {
        "Mission Clears": [c.name for c in clear_locations],
        "Hero Mission Clears": [c.name for c in clear_locations if c.alignmentId == Levels.MISSION_ALIGNMENT_HERO],
        "Dark Mission Clears": [c.name for c in clear_locations if c.alignmentId == Levels.MISSION_ALIGNMENT_DARK],
        "Neutral Mission Clears": [c.name for c in clear_locations if
                                   c.alignmentId == Levels.MISSION_ALIGNMENT_NEUTRAL],
        #"Objective Mission Clears": [c.name for c in clear_locations if c.count is not None],
        #"Objective Hero Mission Clears": [c.name for c in clear_locations if
        #                                  c.count is not None and c.alignmentId == Levels.MISSION_ALIGNMENT_HERO],
        #"Objective Dark Mission Clears": [c.name for c in clear_locations if
        #                                  c.count is not None and c.alignmentId == Levels.MISSION_ALIGNMENT_DARK],
        "Mission Objectives": [c.name for c in mission_locations],
        "Enemies": [c.name for c in enemysanity_locations],
        "GUN Enemies": [c.name for c in enemysanity_locations if c.alignmentId == ENEMY_CLASS_GUN],
        "Egg Enemies": [c.name for c in enemysanity_locations if c.alignmentId == ENEMY_CLASS_EGG],
        "Alien Enemies": [c.name for c in enemysanity_locations if c.alignmentId == ENEMY_CLASS_ALIEN],
        "Checkpoints": [c.name for c in checkpointsanity_locations],
        "Characters": [c.name for c in charactersanity_locations],
        "Keys": [c.name for c in keysanity_locations],
        "Weapons": [c.name for c in weaponsanity_locations],
        "Bosses": [c.name for c in boss_locations],
        "Final Bosses": [c.name for c in boss_locations if c.stageId in Levels.FINAL_BOSSES],
        "Objects": [c.name for c in object_locations]
        #"Shadow Boxes": [c.name for c in object_locations if c.other == ObjectType.SHADOW_BOX],
        #"Gold Beetles": [c.name for c in object_locations if c.other == ObjectType.GOLD_BEETLE],
        #"Cores": [c.name for c in object_locations if c.other == ObjectType.ENERGY_CORE or
        #          c.other == ObjectType.ENERGY_CORE_IN_WOOD_BOX],
        #"Key Doors": [c.name for c in object_locations if c.other == ObjectType.KEY_DOOR]
    }

    for type in Objects.GetPlayableObjectTypes():
        type_name = Names.ObjectTypeToName(type)
        key = type_name + "s"
        groups[key] = [c.name for c in object_locations if c.other == type]

    l_info = GetLocationInfoDict()
    remove_from_groups = []
    for i in l_info.items():
        if i[1].location_type == LOCATION_TYPE_WARP:
            remove_from_groups.append(i[0])

    for i in remove_from_groups:
        del l_info[i]

    new_groups = {}
    for level in Levels.LEVEL_ID_TO_LEVEL.keys():
        if level in Levels.BOSS_STAGES:
            continue
        group_name = Levels.LEVEL_ID_TO_LEVEL[level]
        results = [ x.name for x in l_info.values() if x.stageId == level]
        new_groups[group_name] = results

        for key, values in groups.items():
            new_key = group_name + " " + key
            values = [ v for v in values if v in results ]
            if len(values) > 1:
                new_groups[new_key] = values

    for key,value in new_groups.items():
        groups[key] = value

    return groups



def SetStoryClearEvents(world, player, regions):
    story_clear_events = []
    for story in world.shuffled_story_mode:
        if story.start_stage_id not in world.available_story_levels:
            continue

        if story.start_stage_id == Levels.STAGE_THE_LAST_WAY and not world.options.include_last_way_shuffle:
            continue

        if story.end_stage_id is not None and story.end_stage_id not in world.available_story_levels\
                and (story.boss is None or story.boss not in world.available_story_levels):
            continue

        if story.boss is not None and story.boss not in world.available_levels:
            continue

        view_name = Names.GetMissionClearEventName(story.start_stage_id, story.alignment_id)
        region_name = Regions.stage_id_to_region(story.start_stage_id, 0)
        o_region = regions[region_name]
        story_clear_event = ShadowTheHedgehogLocation(player, view_name, None, o_region)
        story_clear_event.show_in_spoiler = True
        story_clear_events.append(story_clear_event)
        o_region.locations.append(story_clear_event)

    for w in [l for l in world.shuffled_story_mode if l.boss is not None
                                                      and l.boss in world.available_story_levels
              and l.start_stage_id in world.available_levels
              and (l.end_stage_id is not None and l.end_stage_id in world.available_levels)]:
        view_name = Names.GetBossClearEventName(w.boss, w.start_stage_id, w.alignment_id)
        region_name = Regions.stage_id_to_region(w.start_stage_id, 0)
        o_region = regions[region_name]
        story_clear_event = ShadowTheHedgehogLocation(player, view_name, None, o_region)
        story_clear_event.show_in_spoiler = True
        story_clear_events.append(story_clear_event)
        o_region.locations.append(story_clear_event)

    return story_clear_events

def SetRegionEvents(world, player, regions):
    region_events = []
    for level in Levels.ALL_STAGES:
        if level in BOSS_STAGES:
            continue

        if level not in world.available_levels:
            continue

        view_name = Names.GetDistributionRegionEventName(level, 0)
        region_name = Regions.stage_id_to_region(level, 0)
        o_region = regions[region_name]
        region_event = ShadowTheHedgehogLocation(player, view_name, None, o_region)
        region_event.show_in_spoiler = False
        region_event.progress_type = LocationProgressType.PRIORITY
        o_region.locations.append(region_event)

    for region in Levels.INDIVIDUAL_LEVEL_REGIONS:
        if region.stageId not in world.available_levels:
            continue

        if world.options.logic_level != Options.LogicLevel.option_hard \
            and region.hardLogicOnly:
            continue

        view_name = Names.GetDistributionRegionEventName(region.stageId, region.regionIndex)
        region_name = Regions.stage_id_to_region(region.stageId, region.regionIndex)
        o_region = regions[region_name]
        region_event = ShadowTheHedgehogLocation(player, view_name, None, o_region)
        region_event.show_in_spoiler = False
        region_event.progress_type = LocationProgressType.PRIORITY
        #region_events.append(region_event)

        o_region.locations.append(region_event)

    #menu_region.locations.extend(region_events)



