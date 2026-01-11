from . import Levels
from .ObjectTypes import ObjectType
from .Objects_BlackComet import DESIRABLE_OBJECTS_BLACK_COMET
from .Objects_CentralCity import DESIRABLE_OBJECTS_CENTRAL_CITY
from .Objects_CircusPark import DESIRABLE_OBJECTS_CIRCUS_PARK

from .Objects_CosmicFall import DESIRABLE_OBJECTS_COSMIC_FALL
from .Objects_CrypticCastle import DESIRABLE_OBJECTS_CRYPTIC_CASTLE
from .Objects_AirFleet import DESIRABLE_OBJECTS_AIR_FLEET
from .Objects_DeathRuins import DESIRABLE_OBJECTS_DEATH_RUINS
from .Objects_DigitalCircuit import DESIRABLE_OBJECTS_DIGITAL_CIRCUIT
from .Objects_FinalHaunt import DESIRABLE_OBJECTS_FINAL_HAUNT
from .Objects_GlyphicCanyon import DESIRABLE_OBJECTS_GLYPHIC_CANYON
from .Objects_GunFortress import DESIRABLE_OBJECTS_GUN_FORTRESS
from .Objects_IronJungle import DESIRABLE_OBJECTS_IRON_JUNGLE
from .Objects_LavaShelter import DESIRABLE_OBJECTS_LAVA_SHELTER
from .Objects_LethalHighway import DESIRABLE_OBJECTS_LETHAL_HIGHWAY
from .Objects_LostImpact import DESIRABLE_OBJECTS_LOST_IMPACT
from .Objects_MadMatrix import DESIRABLE_OBJECTS_MAD_MATRIX
from .Objects_PrisonIsland import DESIRABLE_OBJECTS_PRISON_ISLAND
from .Objects_SkyTroops import DESIRABLE_OBJECTS_SKY_TROOPS
from .Objects_SpaceGadget import DESIRABLE_OBJECTS_SPACE_GADGET
from .Objects_TheArk import DESIRABLE_OBJECTS_THE_ARK
from .Objects_TheDoom import DESIRABLE_OBJECTS_THE_DOOM
from .Objects_TheLastWay import DESIRABLE_OBJECTS_THE_LAST_WAY
from .Objects_Westopolis import DESIRABLE_OBJECTS_WESTOPOLIS
from .Objects_Bosses import DESIRABLE_OBJECTS_BOSSES

ENEMY_CLASS_ALIEN = 0
ENEMY_CLASS_GUN = 1
ENEMY_CLASS_EGG = 2

LOCATION_ID_PLUS = 100068

def GetObjectSanityTypes():
    return [
        ObjectType.STANDARD_PULLEY, ObjectType.LIGHT_DASH_TRAIL,
        ObjectType.LIGHT_DASH_TRAIL,ObjectType.SPACE_ZIPWIRE,
        ObjectType.GUN_ZIPWIRE, ObjectType.CIRCUS_ZIPWIRE,
        ObjectType.BOMB, ObjectType.BOMB_SERVER,
        ObjectType.HEAL_UNIT, ObjectType.HEAL_SERVER,
        ObjectType.WARP_HOLE, ObjectType.ROCKET,
        ObjectType.BALLOON_ZIPWIRE
    ]

def GetPlayableObjectTypes():
    return [
            ObjectType.GUN_SOLDIER,
            ObjectType.GOLD_BEETLE, ObjectType.SHADOW_BOX,
            ObjectType.ENERGY_CORE, ObjectType.KEY_DOOR,
            ObjectType.ENERGY_CORE_IN_WOOD_BOX,
            ObjectType.GLYPHIC_CANYON_TEMPLE,
            ObjectType.CRYPTIC_CASTLE_LANTERN,
            ObjectType.CREAM,
            ObjectType.CHEESE,
            ObjectType.PRISON_ISLAND_DISC,
            ObjectType.CENTRAL_CITY_BIG_BOMB,
            ObjectType.DOOM_RESEARCHER,
            ObjectType.SKY_TROOPS_EGG_SHIP,
            ObjectType.SKY_TROOPS_TEMPLE,
            ObjectType.MAD_MATRIX_BOMB,
            ObjectType.MAD_MATRIX_TERMINAL,
            ObjectType.THE_ARK_DEFENSE_UNIT,
            ObjectType.SPACE_GADGET_DEFENSE_UNIT,
            ObjectType.GUN_FORTRESS_COMPUTER,
            ObjectType.LAVA_SHELTER_DEFENSE,
            ObjectType.GUN_BEETLE,
            ObjectType.BIG_FOOT,
            ObjectType.GUN_ROBOT,
            ObjectType.EGG_CLOWN,
            ObjectType.EGG_PAWN,
            ObjectType.SHADOW_ANDROID,
            ObjectType.BLACK_ASSASSIN,
            ObjectType.BLACK_VOLT,
            ObjectType.BLACK_HAWK,
            ObjectType.BLACK_WARRIOR,
            ObjectType.BLACK_OAK,
            ObjectType.BLACK_WING,
            ObjectType.BLACK_WORM,
            ObjectType.BLACK_LARVAE,
            ObjectType.ARTIFICIAL_CHAOS,
            ObjectType.KEY,
            ObjectType.ITEM_CAPSULE,
            ObjectType.BALLOON_ITEM,
            ObjectType.ITEM_IN_METAL_BOX,
            ObjectType.ITEM_IN_BOX
    ]

def GetObjectChecks():
    object_check_types = GetPlayableObjectTypes()

    object_checks = [ d for d in DESIRABLE_OBJECTS if d.object_type in object_check_types ]
    return object_checks



def GetCentralCityBombDistribution():
    bombs = [ d for d in DESIRABLE_OBJECTS if d.stage == Levels.STAGE_CENTRAL_CITY and
              d.object_type == ObjectType.SMALL_BOMB]

    result = {}
    for o in bombs:
        if o.region is None:
            print("Error with enemy region:", o.stage, o.name, o.object_type)
            continue

        if o.region not in result:
            result[o.region] = 0

        result[o.region] += o.count

    return result

def GetAlienTypes():
    return [ObjectType.BLACK_ASSASSIN, ObjectType.BLACK_VOLT, ObjectType.BLACK_HAWK,
             ObjectType.BLACK_WARRIOR, ObjectType.BLACK_OAK, ObjectType.BLACK_WING,
             ObjectType.BLACK_WORM , ObjectType.BLACK_LARVAE, ObjectType.ARTIFICIAL_CHAOS]

def GetGunTypes():
    return [ObjectType.GUN_SOLDIER, ObjectType.GUN_BEETLE,
            ObjectType.BIG_FOOT, ObjectType.GUN_ROBOT]

def GetEggTypes():
    return [ObjectType.EGG_CLOWN, ObjectType.EGG_PAWN, ObjectType.SHADOW_ANDROID ]

def GetItemBoxTypes():
    return [ ObjectType.ITEM_CAPSULE, ObjectType.ITEM_IN_BOX, ObjectType.ITEM_IN_METAL_BOX, ObjectType.BALLOON_ITEM]

def GetStandardEnemyTypes():
    alien_types = GetAlienTypes()

    gun_types = GetGunTypes()

    egg_types = GetEggTypes()

    types = []
    types.extend(alien_types)
    types.extend(gun_types)
    types.extend(egg_types)

    return types


def GetEnemyDistributionInStageByBaseType(level, enemyType):
    types = []

    if enemyType == ENEMY_CLASS_ALIEN:
        types = [ObjectType.BLACK_ASSASSIN, ObjectType.BLACK_VOLT, ObjectType.BLACK_HAWK,
                 ObjectType.BLACK_WARRIOR, ObjectType.BLACK_OAK, ObjectType.BLACK_WING,
                 ObjectType.BLACK_WORM , ObjectType.BLACK_LARVAE, ObjectType.ARTIFICIAL_CHAOS]

    elif enemyType == ENEMY_CLASS_GUN:
        types = [ObjectType.GUN_SOLDIER, ObjectType.GUN_BEETLE,
                 ObjectType.BIG_FOOT, ObjectType.GUN_ROBOT]

    elif enemyType == ENEMY_CLASS_EGG:
        types = [ObjectType.EGG_CLOWN, ObjectType.EGG_PAWN, ObjectType.SHADOW_ANDROID ]

    objects = [ d for d in DESIRABLE_OBJECTS if d.stage == level and
      d.object_type in types]

    result = {}
    for o in objects:
        if o.region is None:
            print("Error with enemy region:", o.stage, o.name, o.object_type)
            continue

        if o.region not in result:
            result[o.region] = 0

        result[o.region]  += o.count

    return result


def GetTypeId(objectType):
    if objectType == ObjectType.SHADOW_BOX:
        return 0x3A

    if objectType == ObjectType.VEHICLE:
        return 0x4F

    if objectType == ObjectType.ENERGY_CORE:
        return 0x33

    if objectType == ObjectType.LIGHT_DASH_TRAIL:
        return 0x10

    if objectType == ObjectType.STANDARD_PULLEY:
        return 0x08

    if objectType == ObjectType.SPACE_ZIPWIRE:
        return 0xC88

    if objectType == ObjectType.GUN_ZIPWIRE:
        return 0xC88

    if objectType == ObjectType.CIRCUS_ZIPWIRE:
        return 0xC88

    if objectType == ObjectType.BALLOON_ZIPWIRE:
        return 0xC88

    if objectType == ObjectType.BOMB:
        return 0x0D

    if objectType == ObjectType.BOMB_SERVER:
        return 0x1006

    if objectType == ObjectType.HEAL_SERVER:
        return 0x1006

    if objectType == ObjectType.HEAL_UNIT:
        return 0x38

    if objectType == ObjectType.WARP_HOLE:
        return 0x1F

    if objectType == ObjectType.ROCKET:
        return 0x0E

    if objectType == ObjectType.KEY_DOOR:
        return 0x1E

    if objectType == ObjectType.BLACK_ASSASSIN:
        return 0x93

    if objectType == ObjectType.BLACK_HAWK:
        return 0x8E

    if objectType == ObjectType.BLACK_VOLT:
        return 0x8E

    if objectType == ObjectType.BLACK_WARRIOR:
        return 0x8D

    if objectType == ObjectType.BLACK_OAK:
        return 0x8C

    if objectType == ObjectType.BLACK_WING:
        return 0x8F

    if objectType == ObjectType.BLACK_WORM:
        return 0x90

    if objectType == ObjectType.BLACK_LARVAE:
        return 0x91

    if objectType == ObjectType.ARTIFICIAL_CHAOS:
        return 0x92

    if objectType == ObjectType.GUN_SOLDIER:
        return 0x64

    if objectType == ObjectType.GUN_BEETLE:
        return 0x65

    if objectType == ObjectType.GOLD_BEETLE:
        return 0x65

    if objectType == ObjectType.BIG_FOOT:
        return 0x66

    if objectType == ObjectType.GUN_ROBOT:
        return 0x68

    if objectType == ObjectType.EGG_CLOWN:
        return 0x78

    if objectType == ObjectType.EGG_PAWN:
        return 0x79

    if objectType == ObjectType.SHADOW_ANDROID:
        return 0x7A

    if objectType == ObjectType.SMALL_BOMB:
        return 0xFA1

    if objectType == ObjectType.SMALL_BOMB_AUTO_DETONATE:
        return 0xFA1

    if objectType == ObjectType.LIGHT_DASH_TRAIL_ANTI_TRAP:
        pass

    if objectType == ObjectType.WARP_HOLE_ANTI_TRAP:
        pass

    if objectType == ObjectType.ENERGY_CORE_IN_WOOD_BOX:
        return 0x09

    if objectType == ObjectType.ENERGY_CORE_IN_METAL_BOX:
        return 0x0A

    if objectType == ObjectType.DIGITAL_CORE:
        return 0x7DB

    if objectType == ObjectType.GLYPHIC_CANYON_TEMPLE:
        return 0x839

    if objectType == ObjectType.LETHAL_HIGHWAY_TANK:
        return 0x898

    if objectType == ObjectType.CRYPTIC_CASTLE_LANTERN:
        return 0xBC9

    if objectType == ObjectType.CREAM:
        return 0xBBD

    if objectType == ObjectType.CHEESE:
        return 0xBBE

    if objectType == ObjectType.PRISON_ISLAND_DISC:
        return 0x1453

    if objectType == ObjectType.CENTRAL_CITY_BIG_BOMB:
        return 0xFA0

    if objectType == ObjectType.DOOM_RESEARCHER:
        return 0x1005

    if objectType == ObjectType.SKY_TROOPS_EGG_SHIP:
        return 0x1069

    if objectType == ObjectType.SKY_TROOPS_TEMPLE:
        return 0x106C

    if objectType == ObjectType.MAD_MATRIX_BOMB:
        return 0x7DC

    if objectType == ObjectType.MAD_MATRIX_TERMINAL:
        return 0x7DD

    if objectType == ObjectType.THE_ARK_DEFENSE_UNIT:
        return 0x1388

    if objectType == ObjectType.AIR_FLEET_PRESIDENT_POD:
        return 0x0A

    if objectType == ObjectType.IRON_JUNGLE_EGG_BALLOON:
        return 0x140

    if objectType == ObjectType.SPACE_GADGET_DEFENSE_UNIT:
        return 0x1388

    if objectType == ObjectType.GUN_FORTRESS_COMPUTER:
        return 0x1771

    if objectType == ObjectType.LAVA_SHELTER_DEFENSE:
        return 0x1838

    if objectType == ObjectType.COSMIC_FALL_COMPUTER_ROOM:
        return 0x2595

    if objectType == ObjectType.FINAL_HAUNT_SHIELD:
        return 0x1900

    #if objectType == ObjectType.PARTNER:
    #    return 0x190

    if objectType == ObjectType.KEY:
        return 0x1D

    if objectType == ObjectType.GOAL_RING:
        return 0x14

    if objectType == ObjectType.ITEM_CAPSULE: #Item Capsule
        return 0x12

    if objectType == ObjectType.BALLOON_ITEM: # Balloon
        return 0x13

    if objectType == ObjectType.ITEM_IN_BOX:
        return 0x09

    if objectType == ObjectType.ITEM_IN_METAL_BOX:
        return 0x0A

    #if objectType == ObjectType.FIRE:
    #    return 0x34

    #if objectType == ObjectType.POISON_GAS:
    #    return 0x35

    if objectType == ObjectType.DARK_SPIN_ENTRY:
        return 0x61

    if objectType == ObjectType.DEFENSE_PROGRAM:
        return 0x7D4

    #if objectType == ObjectType.RING_OF_FIRE:
    #    return 0xC85

    #if objectType == ObjectType.HELICOPTER:
    #    return 0xFA2

    if objectType == ObjectType.CLEAR_TRIGGER:
        return 0x2595

    return None

def CheckVehicleAttributes(objectType, extra_bytes, index, link_id):

    if objectType == "Server":
        byte = extra_bytes[3]
        if byte == 0:
            return "Bomb Server"

        if byte == 1:
            return "Heal Server"

    if objectType == "Rings":
        byte_ghost = extra_bytes[(4*4)+3]
        if byte_ghost == 1:
            return "Light Dash Trail"


    if objectType == "Black Warrior":
        byte_saucer = extra_bytes[(23*4)+3]
        if byte_saucer == 0:
            return "Black Warrior"
        if byte_saucer == 1:
            return "Air Saucer Black Warrior"
        else:
            print("xx1", objectType, byte_saucer)
            return "Unknown Black Warrior"

    if objectType == "Black Assassin":
        byte_appear = extra_bytes[(7*4)+3]
        if byte_appear == 3:
            return "Air Saucer Assassin"

    if objectType == "Black Hawk":
        byte_death_type = extra_bytes[(14*4)+3]
        if byte_death_type == 0x00:
            return "Black Hawk"
        if byte_death_type == 0x01:
            return "Black Hawk Rideable"
        elif byte_death_type == 0x10:
            return "Black Volt"
        elif byte_death_type == 0x11:
            return "Black Volt Rideable"
        else:
            print("xx1", objectType, byte_death_type)
            return "Unknown Black Hawk"

    if objectType == "GUN Beetle":
        byte_golden = extra_bytes[(14*4)+3]
        if byte_golden == 0:
            return "GUN Beetle"
        elif byte_golden == 1:
            return "Gold Beetle"
        else:
            print("xx1", objectType, byte_golden)
            return "Unknown Beetle"

    if objectType == "Small Bomb":
        byte_range = int.from_bytes(extra_bytes[0:3], byteorder='little')
        return f"Small Bomb({byte_range})"


    if objectType == "Black Larvae":
        group_count = extra_bytes[(7*4)+3]
        return f"Black Larvae ({group_count})"

    if objectType in ("Wood Box", "Metal Box"):

        box_type = extra_bytes[0:4]
        box_item_bytes = extra_bytes[4:8]
        capsule_type = extra_bytes[8:12]
        weapon_type = extra_bytes[12:16]
        core_type = extra_bytes[16:20]

        box_item = int.from_bytes(box_item_bytes, byteorder='big')

        type_name = "Box"
        if box_item == 0x00:
            type_name = "Empty "+objectType
        elif box_item == 0x01:
            type_name = "Item In "+objectType
        elif box_item == 0x02:
            type_name = "Weapon In "+objectType
        elif box_item == 0x03:
            type_name = "Rings In "+objectType
        elif box_item == 0x04:
            type_name = "Heal Unit In "+objectType
        elif box_item == 0x05:
            type_name = "Core In "+objectType
        else:
            print("Unknown box type:", type_name, box_item_bytes, box_item, index)

        return type_name

    elif objectType == "Weapon Box":
        box_type = extra_bytes[0:4]
        box_weapon_bytes = extra_bytes[4:8]
        return "Weapon Box"

    if objectType == "Key":
        return "Key " + str(hex(link_id))


    return objectType


DESIRABLE_OBJECTS = []

DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_WESTOPOLIS)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_DIGITAL_CIRCUIT)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_GLYPHIC_CANYON)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_LETHAL_HIGHWAY)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_CRYPTIC_CASTLE)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_PRISON_ISLAND)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_CIRCUS_PARK)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_CENTRAL_CITY)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_THE_DOOM)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_SKY_TROOPS)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_MAD_MATRIX)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_DEATH_RUINS)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_THE_ARK)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_AIR_FLEET)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_IRON_JUNGLE)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_SPACE_GADGET)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_LOST_IMPACT)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_GUN_FORTRESS)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_BLACK_COMET)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_LAVA_SHELTER)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_COSMIC_FALL)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_FINAL_HAUNT)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_THE_LAST_WAY)
DESIRABLE_OBJECTS.extend(DESIRABLE_OBJECTS_BOSSES)

def GetDesirableObjectsForStage(stage):
    return [ o for o in DESIRABLE_OBJECTS if o.stage == stage]


def TypeToString(type):

    if type == 0x01:
        return "Spring"

    elif type == 0x02:
        return "Long Spring"

    elif type == 0x03:
        return "Dash Panel"

    elif type == 0x04:
        return "Dash Ramp"

    elif type == 0x05:
        return "Checkpoint"

    elif type == 0x06:
        return "Dash Ring"

    elif type == 0x07:
        return "Locked Case"

    elif type == 0x08:
        return "Pulley"

    elif type == 0x09:
        return "Wood Box"

    elif type == 0x0A:
        return "Metal Box"

    elif type == 0x0A:
        return "Unbreakable Box"

    elif type == 0x0C:
        return "Weapon Box"

    elif type == 0x0D:
        return "GUN Bomb"

    elif type == 0x0E:
        return "Rocket"

    elif type == 0x0F:
        return "Platform"

    elif type == 0x10:
        return "Rings"

    elif type == 0x11:
        return "Hint Ball"

    elif type == 0x12:
        return "Item Capsule"

    elif type == 0x13:
        return "Balloon"

    elif type == 0x14:
        return "Goal Ring"

    elif type == 0x15:
        return "Ball Switch"

    elif type == 0x16:
        return "Target Switch"

    elif type == 0x18:
        return "GUN Turret"

    elif type == 0x19:
        return "Weight"

    elif type == 0x1A:
        return "Wind"

    elif type == 0x1B:
        return "Roadblock"

    elif type == 0x1C:
        return "Cocoon"

    elif type == 0x1E:
        return "Secret Door"

    elif type == 0x1F:
        return "Warp Hole"

    elif type == 0x20:
        return "Weapon"

    elif type == 0x22:
        return "Red Fruit"

    elif type == 0x23:
        return "OObject"

    elif type == 0x33:
        return "Energy Core"

    elif type == 0x34:
        return "Fire"

    elif type == 0x35:
        return "Gas"

    elif type == 0x37:
        return "Cage"

    elif type == 0x38:
        return "Heal Unit"

    elif type == 0x3A:
        return "Special Weapon Box"

    elif type == 0x4F:
        return "Vehicle"

    elif type == 0x5A:
        return "Pole"

    elif type == 0x61:
        return "Dark Spin Entry"

    elif type == 0x64:
        return "GUN Soldier"

    elif type == 0x65:
        return "GUN Beetle"

    elif type == 0x66:
        return "Big Foot"

    elif type == 0x68:
        return "Gun Robot"

    elif type == 0x78:
        return "Egg Clown"

    elif type == 0x79:
        return "Egg Pawn"

    elif type == 0x7A:
        return "Shadow Android"

    elif type == 0x8C:
        return "Black Oak"

    elif type == 0x8D:
        return "Black Warrior"

    elif type == 0x8E:
        return "Black Hawk"

    elif type == 0x8F:
        return "Black Wing"

    elif type == 0x90:
        return "Black Worm"

    elif type == 0x91:
        return "Black Larvae"

    elif type == 0x92:
        return "Artificial Chaos"

    elif type == 0x93:
        return "Black Assassin"

    elif type == 0x12C:
        return "Environment Weapon"

    elif type == 0x190:
        return "Partner"

    elif type == 0x03E8:
        return "Emerald"

    elif type == 0x03E9:
        return "Building"

    elif type == 0x03EA:
        return "City Laser"

    elif type == 0x7D7:
        return "Digital Tile"

    elif type == 0x7DC:
        return "Matrix Bomb"

    elif type == 0x7DD:
        return "Matrix Terminal"

    elif type == 0x07D4:
        return "Defense Program"

    elif type == 0xC88:
        return "Zipline"

    elif type == 0xFA1:
        return "Small Bomb"

    elif type == 0x1006:
        return "Server"

    elif type == 0x1133:
        return "Proximity Door"

    elif type == 0x138A:
        return "Meteor Large"

    elif type == 0x2589:
        return "Destructible"

    elif type == 0x1D:
        return "Key"

    return str(type)

def StateToString(type, state):
    #if type == "Rings" and type == 0x1000:
    #    return "All Collected"
    #if type == "City Laser" and type == 0x1000:
    #    return "Expired"
    #if state == 0x00:
    #    return "Destroyed"
    #if state == 0x01:
    #    return "Loaded"
    #if state == 0x02:
    #    return "10 02"
    #if state == 0x03:
    ##    return "Spawned"
    #if state == 0x04:
   #     return "10 04"
   # if state == 0x05:
   #     return "10 05"
    #if state == 0x06:
    #    return "10 06"
    #if state == 0x07:
    #    return "10 07"
    #if state == 0x08:
    #    return "Defeated"
    #if state == 0x09:
     #   return "10 09"

    #if state == 0x0B:
    #    return "Corpsed"

    return state

def PrintSETChange(address, index, type, previous, new, additional_bytes, link_id):

    #if not use:
    #    return

    typeString = TypeToString(type)
    typeString = CheckVehicleAttributes(typeString, additional_bytes, index, link_id)

    found = False
    for v in ObjectType.__dict__.items():
        vIntValue = v[1]
        l = GetTypeId(vIntValue)
        if l is not None and l == type:
            found = True
            break

    if not found:
        return []

    handle_types = []
    unhandled_types = ["Destructible",
                       "City Laser", "Rings", "Box", "Empty Wood Box", "Empty Metal Box",
                       "Weapon In Wood Box", "Weapon In Metal Box", "Rings In Wood Box", "Rings In Metal Box",
                       "Black Wing", "Gun Beetle",
                       "Heal Unit In Metal Box", "Heal Unit In Wooden Box", "Weapon Box"]

    if len(handle_types) > 0 and typeString not in handle_types:
        return []

    if typeString in unhandled_types:
        return []


    oldStateString = StateToString(typeString,previous)
    newStateString = StateToString(typeString,new)

    #if typeString == "Rings":
    #    print("RINGS", address)

    DontPrintStates  = \
    [
        #["Spawned", "Loaded"],
        #["Loaded", "Spawned"],
        #["Spawned", "Expired"]
    ]

    if [oldStateString,newStateString] in DontPrintStates:
        return

    prints = []

    l = True
    if oldStateString is None:
        l = True

    if l:
        prints.append(f"SET has changed: index={index}, type={typeString}, old={oldStateString}, new={newStateString}")

    return prints


def GetSETFileLength(level):
    if level == Levels.STAGE_WESTOPOLIS:
        return 504 + 71
    elif level == Levels.STAGE_DIGITAL_CIRCUIT:
        return 529 + 125
    elif level == Levels.STAGE_GLYPHIC_CANYON:
        return 328 + 86
    elif level == Levels.STAGE_LETHAL_HIGHWAY:
        return 378 + 174
    elif level == Levels.STAGE_CRYPTIC_CASTLE:
        return 373 + 177
    elif level == Levels.STAGE_PRISON_ISLAND:
        return 526 + 152
    elif level == Levels.STAGE_CIRCUS_PARK:
        return 236 + 143
    elif level == Levels.STAGE_CENTRAL_CITY:
        return 539 + 161
    elif level == Levels.STAGE_THE_DOOM:
        return 375 + 109
    elif level == Levels.STAGE_SKY_TROOPS:
        return 312 + 78
    elif level == Levels.STAGE_MAD_MATRIX:
        return 518 + 165
    elif level == Levels.STAGE_DEATH_RUINS:
        return 458 + 30
    elif level == Levels.STAGE_THE_ARK:
        return 355 + 51
    elif level == Levels.STAGE_AIR_FLEET:
        return 420 + 113
    elif level == Levels.STAGE_IRON_JUNGLE:
        return 257 + 78
    elif level == Levels.STAGE_SPACE_GADGET:
        return 592 + 73
    elif level == Levels.STAGE_LOST_IMPACT:
        return 339 + 79
    elif level == Levels.STAGE_GUN_FORTRESS:
        return 416 + 86
    elif level == Levels.STAGE_BLACK_COMET:
        return 433 + 43
    elif level == Levels.STAGE_LAVA_SHELTER:
        return 341 + 74
    elif level == Levels.STAGE_COSMIC_FALL:
        return 252 + 87
    elif level == Levels.STAGE_FINAL_HAUNT:
        return 446 + 97
    elif level == Levels.STAGE_THE_LAST_WAY:
        return 457 + 40

    elif level == Levels.BOSS_BLACK_BULL_LH:
        return 51
    elif level == Levels.BOSS_EGG_BREAKER_CC:
        return 18
    elif level == Levels.BOSS_HEAVY_DOG:
        return 7
    elif level == Levels.BOSS_EGG_BREAKER_MM:
        return 35
    elif level == Levels.BOSS_BLACK_BULL_DR:
        return 20
    elif level == Levels.BOSS_BLUE_FALCON:
        return 12
    elif level == Levels.BOSS_EGG_BREAKER_IJ:
        return 22


    elif level == Levels.BOSS_DIABLON_GF:
        return 19
    elif level == Levels.BOSS_BLACK_DOOM_GF:
        return 13
    elif level == Levels.BOSS_DIABLON_BC:
        return 14
    elif level == Levels.BOSS_EGG_DEALER_BC:
        return 161
    elif level == Levels.BOSS_EGG_DEALER_LS:
        return 145
    elif level == Levels.BOSS_EGG_DEALER_CF:
        return 137
    elif level == Levels.BOSS_BLACK_DOOM_CF:
        return 15
    elif level == Levels.BOSS_DIABLON_FH:
        return 15
    elif level == Levels.BOSS_BLACK_DOOM_FH:
        return 11



    # Could add boxsanity for bosses too?

    return None

DOES_NOT_WORK_WITH_INDIVIDUAL = 1
WORKS_WITH_INDIVIDUAL = 2

STAGE_OBJECT_ITEMS = {
    (Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_DARK): ( [ObjectType.GUN_SOLDIER, ObjectType.GUN_BEETLE,
                                                                 ObjectType.BIG_FOOT, ObjectType.GUN_ROBOT],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_WESTOPOLIS, Levels.MISSION_ALIGNMENT_HERO): ([ObjectType.BLACK_ASSASSIN, ObjectType.BLACK_VOLT, ObjectType.BLACK_HAWK,
             ObjectType.BLACK_WARRIOR, ObjectType.BLACK_OAK, ObjectType.BLACK_WING,
             ObjectType.BLACK_WORM, ObjectType.BLACK_LARVAE],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_DIGITAL_CIRCUIT, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.DIGITAL_CORE,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_HERO): ([ObjectType.BLACK_ASSASSIN, ObjectType.BLACK_VOLT, ObjectType.BLACK_HAWK,
             ObjectType.BLACK_WARRIOR, ObjectType.BLACK_OAK, ObjectType.BLACK_WING,
             ObjectType.BLACK_WORM, ObjectType.BLACK_LARVAE],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_GLYPHIC_CANYON, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.GLYPHIC_CANYON_TEMPLE,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_LETHAL_HIGHWAY, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.LETHAL_HIGHWAY_TANK,DOES_NOT_WORK_WITH_INDIVIDUAL),
    (Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.CRYPTIC_CASTLE_LANTERN,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_CRYPTIC_CASTLE, Levels.MISSION_ALIGNMENT_HERO): ([ObjectType.CREAM, ObjectType.CHEESE],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_DARK): ( [ObjectType.GUN_SOLDIER, ObjectType.GUN_BEETLE,
                                                                    ObjectType.BIG_FOOT, ObjectType.GUN_ROBOT],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_PRISON_ISLAND, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.PRISON_ISLAND_DISC,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_CIRCUS_PARK, Levels.MISSION_ALIGNMENT_DARK): ( [ObjectType.GUN_SOLDIER, ObjectType.GUN_BEETLE,
                                                                  ObjectType.BIG_FOOT, ObjectType.GUN_ROBOT],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.CENTRAL_CITY_BIG_BOMB,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_CENTRAL_CITY, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.SMALL_BOMB,DOES_NOT_WORK_WITH_INDIVIDUAL),
    (Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_DARK): ( [ObjectType.GUN_SOLDIER, ObjectType.GUN_BEETLE,
                                                               ObjectType.BIG_FOOT, ObjectType.GUN_ROBOT],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_THE_DOOM, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.DOOM_RESEARCHER,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.SKY_TROOPS_EGG_SHIP,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_SKY_TROOPS, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.SKY_TROOPS_TEMPLE,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.MAD_MATRIX_BOMB,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_MAD_MATRIX, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.MAD_MATRIX_TERMINAL,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_DEATH_RUINS, Levels.MISSION_ALIGNMENT_HERO): ([ObjectType.BLACK_ASSASSIN, ObjectType.BLACK_VOLT, ObjectType.BLACK_HAWK,
             ObjectType.BLACK_WARRIOR, ObjectType.BLACK_OAK, ObjectType.BLACK_WING,
             ObjectType.BLACK_WORM, ObjectType.BLACK_LARVAE],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_THE_ARK, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.THE_ARK_DEFENSE_UNIT,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.AIR_FLEET_PRESIDENT_POD,DOES_NOT_WORK_WITH_INDIVIDUAL),
    (Levels.STAGE_AIR_FLEET, Levels.MISSION_ALIGNMENT_HERO): ([ObjectType.BLACK_ASSASSIN, ObjectType.BLACK_VOLT, ObjectType.BLACK_HAWK,
             ObjectType.BLACK_WARRIOR, ObjectType.BLACK_OAK, ObjectType.BLACK_WING,
             ObjectType.BLACK_WORM, ObjectType.BLACK_LARVAE],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_DARK): ( [ObjectType.GUN_SOLDIER, ObjectType.GUN_BEETLE,
                                                                  ObjectType.BIG_FOOT, ObjectType.GUN_ROBOT],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_IRON_JUNGLE, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.IRON_JUNGLE_EGG_BALLOON,DOES_NOT_WORK_WITH_INDIVIDUAL),
    (Levels.STAGE_SPACE_GADGET, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.SPACE_GADGET_DEFENSE_UNIT,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_LOST_IMPACT, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.ARTIFICIAL_CHAOS,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_GUN_FORTRESS, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.GUN_FORTRESS_COMPUTER,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_BLACK_COMET, Levels.MISSION_ALIGNMENT_DARK): ( [ObjectType.GUN_SOLDIER, ObjectType.GUN_BEETLE,
                                                                  ObjectType.BIG_FOOT, ObjectType.GUN_ROBOT],WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_LAVA_SHELTER, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.LAVA_SHELTER_DEFENSE,WORKS_WITH_INDIVIDUAL),
    (Levels.STAGE_COSMIC_FALL, Levels.MISSION_ALIGNMENT_HERO): (ObjectType.COSMIC_FALL_COMPUTER_ROOM,DOES_NOT_WORK_WITH_INDIVIDUAL),
    (Levels.STAGE_FINAL_HAUNT, Levels.MISSION_ALIGNMENT_DARK): (ObjectType.FINAL_HAUNT_SHIELD, DOES_NOT_WORK_WITH_INDIVIDUAL),
}

def GetAvailableObjects(world):
    object_types = GetObjectSanityTypes()
    relevant_objects = [ o.object_type for o in DESIRABLE_OBJECTS if o.object_type in object_types if o.stage in world.available_levels ]
    return relevant_objects

def GetAvailableVehicles(world):
    vehicle_items = set([ v.vehicle for v in DESIRABLE_OBJECTS if v.vehicle is not None and v.stage in world.available_levels ])
    return vehicle_items


def GetShadowBonusWeapons(stageId):
    box_weapons = [ m.weapon for m in GetDesirableObjectsForStage(stageId) if m.object_type == ObjectType.SHADOW_BOX
                    and m.weapon is not None ]
    return list(set(box_weapons))