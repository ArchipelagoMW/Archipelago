from enum import Enum

LOCATION_ID_PLUS_O = 110068

from .ObjectTypes import SETObject,ObjectType

STAGE_WESTOPOLIS = 100
STAGE_DIGITAL_CIRCUIT = 200
STAGE_GLYPHIC_CANYON = 201
STAGE_LETHAL_HIGHWAY = 202
STAGE_CRYPTIC_CASTLE = 300
STAGE_PRISON_ISLAND = 301
STAGE_CIRCUS_PARK = 302
STAGE_CENTRAL_CITY = 400
STAGE_THE_DOOM = 401
STAGE_SKY_TROOPS = 402
STAGE_MAD_MATRIX = 403
STAGE_DEATH_RUINS = 404
STAGE_THE_ARK = 500
STAGE_AIR_FLEET = 501
STAGE_IRON_JUNGLE = 502
STAGE_SPACE_GADGET = 503
STAGE_LOST_IMPACT = 504
STAGE_GUN_FORTRESS = 600
STAGE_BLACK_COMET = 601
STAGE_LAVA_SHELTER = 602
STAGE_COSMIC_FALL = 603
STAGE_FINAL_HAUNT = 604

BOSS_BLACK_BULL_LH = 210
BOSS_EGG_BREAKER_CC = 310
BOSS_HEAVY_DOG = 410
BOSS_EGG_BREAKER_MM = 411
BOSS_BLACK_BULL_DR = 412
BOSS_BLUE_FALCON = 510
BOSS_EGG_BREAKER_IJ = 511
BOSS_BLACK_DOOM_GF = 610
BOSS_DIABLON_GF = 611
BOSS_EGG_DEALER_BC = 612
BOSS_DIABLON_BC = 613
BOSS_EGG_DEALER_LS = 614
BOSS_EGG_DEALER_CF = 615
BOSS_BLACK_DOOM_CF = 616
BOSS_BLACK_DOOM_FH = 617
BOSS_DIABLON_FH = 618

STAGE_THE_LAST_WAY = 700
BOSS_DEVIL_DOOM = 710

LEVEL_ID_TO_LEVEL = {
    STAGE_WESTOPOLIS: "Westopolis",
    STAGE_DIGITAL_CIRCUIT: "Digital Circuit",
    STAGE_GLYPHIC_CANYON: "Glyphic Canyon",
    STAGE_LETHAL_HIGHWAY : "Lethal Highway",
    STAGE_CRYPTIC_CASTLE : "Cryptic Castle",
    STAGE_PRISON_ISLAND : "Prison Island",
    STAGE_CIRCUS_PARK : "Circus Park",
    STAGE_CENTRAL_CITY : "Central City",
    STAGE_THE_DOOM : "The Doom",
    STAGE_SKY_TROOPS : "Sky Troops",
    STAGE_MAD_MATRIX : "Mad Matrix",
    STAGE_DEATH_RUINS : "Death Ruins",
    STAGE_THE_ARK : "The Ark",
    STAGE_AIR_FLEET : "Air Fleet",
    STAGE_IRON_JUNGLE : "Iron Jungle",
    STAGE_SPACE_GADGET : "Space Gadget",
    STAGE_LOST_IMPACT : "Lost Impact",
    STAGE_GUN_FORTRESS : "Gun Fortress",
    STAGE_BLACK_COMET : "Black Comet",
    STAGE_LAVA_SHELTER : "Lava Shelter",
    STAGE_COSMIC_FALL : "Cosmic Fall",
    STAGE_FINAL_HAUNT : "Final Haunt",

    STAGE_THE_LAST_WAY : "The Last Way",

    BOSS_BLACK_BULL_LH: "Black Bull Lethal Highway",
    BOSS_EGG_BREAKER_CC: "Egg Breaker Cryptic Castle",
    BOSS_HEAVY_DOG: "Heavy Dog",
    BOSS_EGG_BREAKER_MM: "Egg Breaker Mad Matrix",
    BOSS_BLACK_BULL_DR: "Black Bull Death Ruins",
    BOSS_BLUE_FALCON: "Blue Falcon",
    BOSS_EGG_BREAKER_IJ:"Egg Breaker Iron Jungle",
    BOSS_BLACK_DOOM_GF: "Black Doom Gun Fortress",
    BOSS_DIABLON_GF: "Diablon Gun Fortress",
    BOSS_EGG_DEALER_BC: "Egg Dealer Black Comet",
    BOSS_DIABLON_BC: "Diablon Black Comet",
    BOSS_EGG_DEALER_LS : "Egg Dealer Lava Shelter",
    BOSS_EGG_DEALER_CF: "Egg Dealer Cosmic Fall",
    BOSS_BLACK_DOOM_CF: "Black Doom Cosmic Fall",
    BOSS_BLACK_DOOM_FH : "Black Doom Final Haunt",
    BOSS_DIABLON_FH: "Diablon Final Haunt",

    BOSS_DEVIL_DOOM: "Devil Doom"
}

BOSS_STAGES = [
    BOSS_BLACK_BULL_LH,
    BOSS_EGG_BREAKER_CC,
    BOSS_HEAVY_DOG,
    BOSS_EGG_BREAKER_MM,
    BOSS_BLACK_BULL_DR,
    BOSS_BLUE_FALCON,
    BOSS_EGG_BREAKER_IJ,
    BOSS_BLACK_DOOM_GF,
    BOSS_DIABLON_GF ,
    BOSS_EGG_DEALER_BC,
    BOSS_DIABLON_BC,
    BOSS_EGG_DEALER_LS,
    BOSS_BLACK_DOOM_CF,
    BOSS_EGG_DEALER_CF,
    BOSS_BLACK_DOOM_FH,
    BOSS_DIABLON_FH,
    BOSS_DEVIL_DOOM
]

LAST_STORY_STAGES = [STAGE_THE_LAST_WAY, BOSS_DEVIL_DOOM]

def getLevelNames():
    return [ v for v in LEVEL_ID_TO_LEVEL.values() if v != "Devil Doom" ]

def getBossNames():
    return [ v[1] for v in LEVEL_ID_TO_LEVEL.items() if v[0] in BOSS_STAGES ]

def getLastStoryNames():
    return [ v[1] for v in LEVEL_ID_TO_LEVEL.items() if v[0] in LAST_STORY_STAGES ]

class REGION_INDICIES:
    WESTOPOLIS_PULLEY = 1
    WESTOPOLIS_WEAPON = 2
    WESTOPOLIS_KEY_DOOR = 3
    WESTOPOLIS_GOLD_BEETLE = 4

    DIGITAL_CIRCUIT_KEY_DOOR = 1
    DIGITAL_CIRCUIT_KEY_WARP_HOLE = 2
    DIGITAL_CIRCUIT_GOLD_BEETLE = 3
    DIGITAL_CIRCUIT_DARK_WARP_HOLE = 4

    GLYPHIC_CANYON_PULLEY = 1
    GLYPHIC_CANYON_KEY_DOOR = 2
    GLYPHIC_CANYON_BLACK_VOLT = 3

    LETHAL_HIGHWAY_KEY_DOOR = 1
    LETHAL_HIGHWAY_ROCKET = 2
    LETHAL_HIGHWAY_PULLEY = 3

    CRYPTIC_CASTLE_BALLOON = 1
    CRYPTIC_CASTLE_TORCH = 2
    CRYPTIC_CASTLE_BOMB_EASY_1 = 3
    CRYPTIC_CASTLE_HAWK = 4
    CRYPTIC_CASTLE_HAWK_RIDE = 5
    CRYPTIC_CASTLE_ENEMY_HAWKS = 6
    CRYPTIC_CASTLE_KEY_DOOR = 7
    CRYPTIC_CASTLE_BOMB_EASY_2 = 8
    CRYPTIC_CASTLE_DARK_LIGHT_DASH = 9
    CRYPTIC_CASTLE_HAWK_2 = 10
    CRYPTIC_CASTLE_HAWK_RIDE_2 = 11
    CRYPTIC_CASTLE_ENEMY_HAWKS_2 = 12


    PRISON_ISLAND_AIR_SAUCER = 1
    PRISON_ISLAND_KEY_DOOR = 2
    PRISON_ISLAND_PULLEY_EASY = 3
    PRISON_ISLAND_GOLD_BEETLE = 4

    CIRCUS_PARK_ZIP_WIRE = 1
    CIRCUS_PARK_ROCKET_ITEM = 2
    CIRCUS_PARK_ROCKET_EASY = 3
    CIRCUS_PARK_SECOND_CHECKPOINT_HERO_GOAL = 4
    CIRCUS_PARK_GUN_TURRET = 5
    CIRCUS_PARK_KEY_DOOR = 6
    CIRCUS_PARK_ROCKET = 7
    CIRCUS_PARK_PULLEY = 8
    CIRCUS_PARK_HERO_GOAL_STANDARD = 9
    CIRCUS_PARK_HERO_GOAL = 10

    CENTRAL_CITY_ROCKET_1 = 1
    CENTRAL_CITY_TRAVERSE_HARD = 2
    CENTRAL_CITY_ROCKET_1_OR_TRAVERSE_HARD = 3
    CENTRAL_CITY_BOMB_OR_BAZOOKA = 4
    CENTRAL_CITY_TRAVERSE_EASY = 5
    CENTRAL_CITY_KEY_DOOR = 6
    CENTRAL_CITY_BOMB_OR_BAZOOKA_2 = 7
    CENTRAL_CITY_GUN_TURRET = 8
    CENTRAL_CITY_ROCKET_2 = 9
    CENTRAL_CITY_BOMB_OR_BAZOOKA_3 = 10

    THE_DOOM_PULLEY = 1
    THE_DOOM_KEY_DOOR = 2
    THE_DOOM_BOMBS = 3
    THE_DOOM_THROUGH_DOOR = 4
    THE_DOOM_DOOR_1_SWITCH = 5
    THE_DOOM_FAN_ROOM = 6
    THE_DOOM_PULLEY_2 = 7
    THE_DOOM_GOLD_BEETLE = 8

    SKY_TROOPS_PULLEY = 1
    SKY_TROOPS_LIGHT_DASH = 2
    SKY_TROOPS_GUN_JUMPER_EASY = 3
    SKY_TROOPS_ROCKET_NORMAL = 4
    SKY_TROOPS_ROCKET = 5
    SKY_TROOPS_KEY_DOOR = 6
    SKY_TROOPS_BLACK_VOLT = 7
    SKY_TROOPS_BLACK_HAWK = 8
    SKY_TROOPS_HAWK_RIDE = 9
    SKY_TROOPS_HAWK_ENEMIES = 10
    SKY_TROOPS_BLACK_HAWK_CC_EASY_1 = 11
    SKY_TROOPS_BLACK_HAWK_CC_EASY_2 = 12
    SKY_TROOPS_BLACK_HAWK_CC_HARD = 13
    SKY_TROOPS_HAWK_OR_VOLT = 14

    MAD_MATRIX_GUN = 1
    MAD_MATRIX_YELLOW_ENTRY = 2
    MAD_MATRIX_GREEN_ENTRY = 3
    MAD_MATRIX_GREEN_PROGRESSION = 4
    MAD_MATRIX_RED_ENTRY = 5
    MAD_MATRIX_KEY_DOOR = 6

    DEATH_RUINS_PULLEY = 1
    DEATH_RUINS_GOLD_BEETLE = 2
    DEATH_RUINS_KEY_DOOR = 3
    DEATH_RUINS_KEY_WARP = 4
    DEATH_RUINS_WALLS = 5

    THE_ARK_BLACK_VOLT = 1
    THE_ARK_KEY_DOOR = 2

    AIR_FLEET_PULLEY = 1
    AIR_FLEET_KEY_DOOR = 2
    AIR_FLEET_AIR_SAUCER = 3
    AIR_FLEET_RAIL_HARD = 4
    AIR_FLEET_RAILS = 5
    AIR_FLEET_GOLD_BEETLE = 6

    IRON_JUNGLE_EARLY_JUMPER = 1
    IRON_JUNGLE_KEY_DOOR = 2
    IRON_JUNGLE_PULLEY_NORMAL = 3
    IRON_JUNGLE_ROCKET = 4
    IRON_JUNGLE_GOLD_BEETLE = 5
    IRON_JUNGLE_LIGHT_DASH_LOWER = 6
    IRON_JUNGLE_GUN_JUMPER = 7
    IRON_JUNGLE_JUMPER_OR_LIGHT_DASH = 8
    IRON_JUNGLE_LIGHT_DASH = 9
    IRON_JUNGLE_GUN_TURRET = 10
    IRON_JUNGLE_LIGHT_DASH_DARK = 11

    SPACE_GADGET_UNITS = 1
    SPACE_GADGET_ZIPWIRE = 2
    SPACE_GADGET_AIR_SAUCER = 3
    SPACE_GADGET_UNITS_AIR_SAUCER = 4
    SPACE_GADGET_KEY_DOOR = 5
    SPACE_GADGET_WARP_HOLE = 6
    SPACE_GADGET_WARP_HOLE_DARK = 7

    LOST_IMPACT_GUN_LIFT = 1
    LOST_IMPACT_PULLEY = 2
    LOST_IMPACT_KEY_DOOR = 3
    LOST_IMPACT_ROCKET = 4
    LOST_IMPACT_BOMB_WALL = 5

    # At start, no pulley required, but found required for tunnels
    GUN_FORTRESS_GUN_TURRET = 1
    GUN_FORTRESS_TURRET_OR_FIRE = 2
    GUN_FORTRESS_ZIPWIRE_NORMAL = 3
    GUN_FORTRESS_PULLEY = 4
    GUN_FORTRESS_ZIP_1A = 5
    GUN_FORTRESS_ZIP_1B = 6
    GUN_FORTRESS_ZIP_2 = 7
    GUN_FORTRESS_ZIPWIRE_BASE = 8
    GUN_FORTRESS_ZIPWIRE = 9
    GUN_FORTRESS_ROCKET_NORMAL = 10
    GUN_FORTRESS_WEAPON_SHOT = 11
    GUN_FORTRESS_TUNNEL_2 = 12
    GUN_FORTRESS_TOP_TUNNEL_2 = 13
    GUN_FORTRESS_COMPUTER_2_BACK = 14
    GUN_FORTRESS_COMPUTER_ROOM_TWO = 15
    GUN_FORTRESS_AFTER_TUNNEL_2 = 16
    GUN_FORTRESS_KEY_PULLEY = 17
    GUN_FORTRESS_KEY_DOOR = 18
    GUN_FORTRESS_ZIPLINE_HARD = 19
    GUN_FORTRESS_ZIPLINE_ENEMIES = 20
    GUN_FORTRESS_KEY_OR_ZIPLINE = 21

    BLACK_COMET_AIR_SAUCER = 1
    BLACK_COMET_WORMS = 2
    BLACK_COMET_FLOATERS = 3
    BLACK_COMET_WARP_HOLE = 4
    BLACK_COMET_BLACK_TURRET = 5
    BLACK_COMET_FLOATERS_2 = 6
    BLACK_COMET_HIGHER_CREATURES = 7
    BLACK_COMET_WORMS_2 = 8
    BLACK_COMET_FLOATING_ENEMY_WALL = 9
    BLACK_COMET_KEY_DOOR = 10
    BLACK_COMET_BEHIND_KEY_DOOR = 11

    LAVA_SHELTER_KEY_DOOR = 1
    LAVA_SHELTER_AIR_SAUCER = 2
    LAVA_SHELTER_PULLEY = 3
    LAVA_SHELTER_PULLEY_OR_LAVA = 4
    LAVA_SHELTER_LIGHT_DASH_DARK = 5
    LAVA_SHELTER_PULLEY_DARK = 6

    COSMIC_FALL_ZIPWIRE = 1
    COSMIC_FALL_PULLEY_NORMAL = 2
    COSMIC_FALL_PULLEY_CORE = 3
    COSMIC_FALL_KEY_DOOR = 4
    COSMIC_FALL_LIGHT_DASH = 5
    COSMIC_FALL_GUN_JUMPER = 6
    COSMIC_FALL_GUN_JUMPER_PULLEY_HARD = 7
    COSMIC_FALL_LD_OR_JUMPER = 8
    COSMIC_FALL_COMPUTER_ROOM_1 = 9
    COSMIC_FALL_COMPUTER_ROOM_2 = 10
    COSMIC_FALL_COMPUTER_ROOM = 11

    FINAL_HAUNT_VACUUM = 1
    FINAL_HAUNT_VACUUM_HARD = 2
    FINAL_HAUNT_BLACK_VOLT = 3
    FINAL_HAUNT_BLACK_VOLT_BASE = 4
    FINAL_HAUNT_BLACK_VOLT_ACCESS = 5
    FINAL_HAUNT_BLACK_VOLT_BACK = 6
    FINAL_HAUNT_HARD_VACUUM_OR_BLACK_VOLT = 7
    FINAL_HAUNT_ROCKET_NORMAL = 8

    FINAL_HAUNT_SHIELD_2 = 9
    FINAL_HAUNT_SHIELD_COUNT_2 = 10

    FINAL_HAUNT_BLACK_VOLT_2 = 11
    FINAL_HAUNT_KEY_DOOR = 12
    FINAL_HAUNT_LIGHT_DASH = 13
    FINAL_HAUNT_SHIELD_COUNT_3 = 14
    FINAL_HAUNT_KEY_DOOR_2 = 15
    FINAL_HAUNT_SHIELD_4 = 16

    THE_LAST_WAY_BLACK_VOLT = 1
    THE_LAST_WAY_VOLT_ENEMIES = 2
    THE_LAST_WAY_KEY_DOOR = 3
    THE_LAST_WAY_BEHIND_KEY_DOOR = 4
    THE_LAST_WAY_WARP_HOLE = 5
    THE_LAST_WAY_VOLT_OR_WARP = 6
    THE_LAST_WAY_LIGHT_DASH_EASY = 7


LEVEL_ID_TO_LEVEL = {
    STAGE_WESTOPOLIS: "Westopolis",
    STAGE_DIGITAL_CIRCUIT: "Digital Circuit",
    STAGE_GLYPHIC_CANYON: "Glyphic Canyon",
    STAGE_LETHAL_HIGHWAY : "Lethal Highway",
    STAGE_CRYPTIC_CASTLE : "Cryptic Castle",
    STAGE_PRISON_ISLAND : "Prison Island",
    STAGE_CIRCUS_PARK : "Circus Park",
    STAGE_CENTRAL_CITY : "Central City",
    STAGE_THE_DOOM : "The Doom",
    STAGE_SKY_TROOPS : "Sky Troops",
    STAGE_MAD_MATRIX : "Mad Matrix",
    STAGE_DEATH_RUINS : "Death Ruins",
    STAGE_THE_ARK : "The Ark",
    STAGE_AIR_FLEET : "Air Fleet",
    STAGE_IRON_JUNGLE : "Iron Jungle",
    STAGE_SPACE_GADGET : "Space Gadget",
    STAGE_LOST_IMPACT : "Lost Impact",
    STAGE_GUN_FORTRESS : "Gun Fortress",
    STAGE_BLACK_COMET : "Black Comet",
    STAGE_LAVA_SHELTER : "Lava Shelter",
    STAGE_COSMIC_FALL : "Cosmic Fall",
    STAGE_FINAL_HAUNT : "Final Haunt",

    STAGE_THE_LAST_WAY : "The Last Way",

    BOSS_BLACK_BULL_LH: "Black Bull Lethal Highway",
    BOSS_EGG_BREAKER_CC: "Egg Breaker Cryptic Castle",
    BOSS_HEAVY_DOG: "Heavy Dog",
    BOSS_EGG_BREAKER_MM: "Egg Breaker Mad Matrix",
    BOSS_BLACK_BULL_DR: "Black Bull Death Ruins",
    BOSS_BLUE_FALCON: "Blue Falcon",
    BOSS_EGG_BREAKER_IJ:"Egg Breaker Iron Jungle",
    BOSS_BLACK_DOOM_GF: "Black Doom Gun Fortress",
    BOSS_DIABLON_GF: "Diablon Gun Fortress",
    BOSS_EGG_DEALER_BC: "Egg Dealer Black Comet",
    BOSS_DIABLON_BC: "Diablon Black Comet",
    BOSS_EGG_DEALER_LS : "Egg Dealer Lava Shelter",
    BOSS_EGG_DEALER_CF: "Egg Dealer Cosmic Fall",
    BOSS_BLACK_DOOM_CF: "Black Doom Cosmic Fall",
    BOSS_BLACK_DOOM_FH : "Black Doom Final Haunt",
    BOSS_DIABLON_FH: "Diablon Final Haunt",


    BOSS_DEVIL_DOOM: "Devil Doom"
}

ALIGNMENT_TO_STRING = \
{
    0: "Dark",
    1: "Neutral",
    2: "Hero"
}

def GetMissionClearEventName(stageId, alignmentId):
    view_name = f"Story_{LEVEL_ID_TO_LEVEL[stageId]}_{ALIGNMENT_TO_STRING[alignmentId]}".replace(" ", "_").upper()
    return view_name

def GetDistributionRegionEventName(stageId, index):
    stage_name = LEVEL_ID_TO_LEVEL[stageId]
    region_name = "DISTRIBUTION_" + stage_name.upper().replace(" ", "_")+"_ENTRANCE"
    if index == 0:
        return region_name

    for name,lookup_index in REGION_INDICIES.__dict__.items():
        if name.startswith(stage_name.upper().replace(" ","_")) and \
            index == lookup_index :
            region_name = "DISTRIBUTION_" + name

    return region_name

def GetBossClearEventName(stageId, from_id, alignment_id):
    view_name = ("Story_" + LEVEL_ID_TO_LEVEL[stageId] +
                 f"_{from_id}_{alignment_id}")\
    .replace(" ", "_").upper()
    return view_name

def ObjectTypeToName(type):
    value_to_name = {v: k for k, v in ObjectType.__dict__.items() if not k.startswith('__') and not callable(v)}
    return value_to_name.get(type).replace("_", " ").title()


def GetObjectLocationName(object: SETObject):
    id_name = int(str(LOCATION_ID_PLUS_O) + str(6) + str(object.stage) + "0" + str(object.index))
    view_name = f"{LEVEL_ID_TO_LEVEL[object.stage]} {ObjectTypeToName(object.object_type)}-{object.name}"

    return id_name, view_name

def GetRegionEntranceName(base_region_name, new_region_name, restrictionTypes):

    restrict_types_as_name = ",".join([ REGION_RESTRICTION_TYPES(t).name for t in restrictionTypes ]).replace("'", "")

    connection_name = f"{base_region_name} > {new_region_name} with {restrict_types_as_name}"

    return connection_name


def GetNameForVehicle(baseName):
    return f"Vehicle:{baseName}"

class REGION_RESTRICTION_TYPES(Enum):
    KeyDoor = 1
    BlackHawk = 2
    BlackVolt = 3
    Torch = 4
    AirSaucer = 5
    Car = 6
    GunJumper = 7
    LongRangeGun = 8
    GunLift = 9
    NoRestriction = 10
    Vacuum = 11
    Gun = 12
    Heal = 13
    BlackArmsTurret = 14
    GunTurret = 15
    ShootOrTurret = 16
    AnyStageWeapon = 17
    ShadowRifle = 18

    HealCannonOrLongRangeGun = 19
    Pulley = 20
    WarpHole = 21
    Rocket = 22
    Zipwire = 23
    Explosion = 24 # Access to Bazooka, or Bombs
    LightDash = 25
    GoldBeetle = 26
    VacuumOrShot = 27
    SatelliteGun = 28
    Impassable = 29

    Region0 = 100
    Region1 = 101
    Region2 = 102
    Region3 = 103
    Region4 = 104
    Region5 = 105
    Region6 = 106
    Region7 = 107
    Region8 = 108
    Region9 = 109
    Region10 = 110
    Region11 = 111
    Region12 = 102
    Region13 = 113
    Region14 = 114
    Region15= 115
    Region16 = 116
    Region17 = 117
    Region18 = 118
    Region19 = 119
    Region20 = 120
    Region21 = 121

    @classmethod
    def RegionAccess(cls, stageRegionId):
        return REGION_RESTRICTION_TYPES(100 + stageRegionId)


def getValidPercentOverrides():
    return [
        'OED.Westopolis', 'OECD.Westopolis', 'AED.Westopolis', 'OEFD.Westopolis',
        'OEH.Westopolis', 'OECH.Westopolis', 'AEH.Westopolis', 'OEFH.Westopolis',
        'OD.Glyphic Canyon', 'CD.Glyphic Canyon', 'AD.Glyphic Canyon', 'OFD.Glyphic Canyon',
        'OEH.Glyphic Canyon', 'OECH.Glyphic Canyon', 'AEH.Glyphic Canyon', 'OEFH.Glyphic Canyon',
        'OH.Lethal Highway', 'CH.Lethal Highway', 'AH.Lethal Highway', 'OFH.Lethal Highway',
        'OD.Cryptic Castle', 'CD.Cryptic Castle', 'AD.Cryptic Castle', 'OFD.Cryptic Castle',
        'OH.Cryptic Castle', 'CH.Cryptic Castle', 'AH.Cryptic Castle', 'OFH.Cryptic Castle',
        'OED.Prison Island', 'OECD.Prison Island', 'AED.Prison Island', 'OEFD.Prison Island',
        'OH.Prison Island', 'CH.Prison Island', 'AH.Prison Island', 'OFH.Prison Island',
        'OED.Circus Park', 'OECD.Circus Park', 'AED.Circus Park', 'OEFD.Circus Park',
        'OD.Central City', 'CD.Central City', 'AD.Central City', 'OFD.Central City',
        'OH.Central City', 'CH.Central City', 'AH.Central City', 'OFH.Central City',
        'OED.The Doom', 'OECD.The Doom', 'AED.The Doom', 'OEFD.The Doom',
        'OH.The Doom', 'CH.The Doom', 'AH.The Doom', 'OFH.The Doom',
        'OD.Sky Troops', 'CD.Sky Troops', 'AD.Sky Troops', 'OFD.Sky Troops',
        'OH.Sky Troops', 'CH.Sky Troops', 'AH.Sky Troops', 'OFH.Sky Troops',
        'OD.Mad Matrix', 'CD.Mad Matrix', 'AD.Mad Matrix', 'OFD.Mad Matrix',
        'OH.Mad Matrix', 'CH.Mad Matrix', 'AH.Mad Matrix', 'OFH.Mad Matrix',
        'OEH.Death Ruins', 'OECH.Death Ruins', 'AEH.Death Ruins', 'OEFH.Death Ruins',
        'OD.The Ark', 'CD.The Ark', 'AD.The Ark', 'OFD.The Ark',
        'OD.Air Fleet', 'CD.Air Fleet', 'AD.Air Fleet', 'OFD.Air Fleet',
        'OEH.Air Fleet', 'OECH.Air Fleet', 'AEH.Air Fleet', 'OEFH.Air Fleet',
        'OED.Iron Jungle', 'OECD.Iron Jungle', 'AED.Iron Jungle', 'OEFD.Iron Jungle',
        'OH.Iron Jungle', 'CH.Iron Jungle', 'AH.Iron Jungle', 'OFH.Iron Jungle',
        'OD.Space Gadget', 'CD.Space Gadget', 'AD.Space Gadget', 'OFD.Space Gadget',
        'OEH.Lost Impact', 'OECH.Lost Impact', 'AEH.Lost Impact', 'OEFH.Lost Impact',
        'OD.Gun Fortress', 'CD.Gun Fortress', 'AD.Gun Fortress', 'OFD.Gun Fortress',
        'OED.Black Comet', 'OECD.Black Comet', 'AED.Black Comet', 'OEFD.Black Comet',
        'OD.Lava Shelter', 'CD.Lava Shelter', 'AD.Lava Shelter', 'OFD.Lava Shelter',
        'OD.Final Haunt', 'CD.Final Haunt', 'AD.Final Haunt', 'OFD.Final Haunt',
        'EG.Westopolis', 'EFG.Westopolis', 'EA.Westopolis', 'EFH.Westopolis',
        'EG.Digital Circuit', 'EFG.Digital Circuit', 'EA.Digital Circuit', 'EFH.Digital Circuit',
        'EG.Glyphic Canyon', 'EFG.Glyphic Canyon', 'EA.Glyphic Canyon', 'EFH.Glyphic Canyon',
        'EG.Lethal Highway', 'EFG.Lethal Highway', 'EA.Lethal Highway', 'EFH.Lethal Highway',
        'EA.Cryptic Castle', 'EFH.Cryptic Castle', 'EE.Cryptic Castle', 'EFE.Cryptic Castle',
        'EG.Prison Island', 'EFG.Prison Island', 'EA.Prison Island', 'EFH.Prison Island',
        'EG.Circus Park', 'EFG.Circus Park', 'EE.Circus Park', 'EFE.Circus Park',
        'EG.Central City', 'EFG.Central City', 'EA.Central City', 'EFH.Central City',
        'EG.The Doom', 'EFG.The Doom', 'EA.Sky Troops', 'EFH.Sky Troops',
        'EE.Sky Troops', 'EFE.Sky Troops', 'EA.Mad Matrix', 'EFH.Mad Matrix',
        'EE.Mad Matrix', 'EFE.Mad Matrix', 'EG.Death Ruins', 'EFG.Death Ruins',
        'EA.Death Ruins', 'EFH.Death Ruins', 'EG.The Ark', 'EFG.The Ark',
        'EA.The Ark', 'EFH.The Ark', 'EG.Air Fleet', 'EFG.Air Fleet',
        'EA.Air Fleet', 'EFH.Air Fleet', 'EG.Iron Jungle', 'EFG.Iron Jungle',
        'EE.Iron Jungle', 'EFE.Iron Jungle', 'EG.Space Gadget', 'EFG.Space Gadget',
        'EA.Space Gadget', 'EFH.Space Gadget', 'EG.Lost Impact', 'EFG.Lost Impact',
        'EA.Lost Impact', 'EFH.Lost Impact', 'EG.Gun Fortress', 'EFG.Gun Fortress',
        'EA.Gun Fortress', 'EFH.Gun Fortress', 'EG.Black Comet', 'EFG.Black Comet',
        'EA.Black Comet', 'EFH.Black Comet', 'EE.Lava Shelter', 'EFE.Lava Shelter',
        'EG.Cosmic Fall', 'EFG.Cosmic Fall', 'EA.Cosmic Fall', 'EFH.Cosmic Fall',
        'EA.Final Haunt', 'EFH.Final Haunt', 'EA.The Last Way', 'EFH.The Last Way'
    ]