
class ObjectType:
    SHADOW_BOX = 1

    VEHICLE = 2

    class ObjectTypeVehicle:
        STANDARD_CAR = 1
        CONVERTIBLE = 2
        ARMORED_CAR = 3
        GUN_MOTORCYCLE = 4
        GUN_JUMPER = 5
        GUN_CANNON = 6
        AIR_SAUCER = 7
        BLACK_HAWK = 8
        BLACK_VOLT = 9
        GUN_TURRET = 10
        BLACK_TURRET = 11
        GUN_LIFT = 12
        GUN_LIFT_FAST = 13

    ENERGY_CORE = 4

    LIGHT_DASH_TRAIL = 5

    STANDARD_PULLEY = 6
    SPACE_ZIPWIRE = 7
    GUN_ZIPWIRE = 8
    CIRCUS_ZIPWIRE = 9

    BOMB = 10
    BOMB_SERVER= 11
    HEAL_UNIT = 12
    HEAL_SERVER = 13

    WARP_HOLE = 14
    ROCKET = 15

    KEY_DOOR = 16
    BALLOON_ZIPWIRE = 17

    SMALL_BOMB = 20
    SMALL_BOMB_AUTO_DETONATE = 21
    LIGHT_DASH_TRAIL_ANTI_TRAP = 22
    WARP_HOLE_ANTI_TRAP = 23

    GUN_SOLDIER = 30
    GUN_BEETLE = 31
    GOLD_BEETLE = 32
    BIG_FOOT = 33
    GUN_ROBOT = 34

    EGG_CLOWN = 35
    EGG_PAWN = 36
    SHADOW_ANDROID = 37

    BLACK_ASSASSIN = 40
    BLACK_VOLT = 41
    BLACK_HAWK = 42
    BLACK_WARRIOR = 43
    BLACK_OAK = 44
    BLACK_WING = 45
    BLACK_WORM = 46
    BLACK_LARVAE = 47

    ARTIFICIAL_CHAOS = 48

    ENERGY_CORE_IN_WOOD_BOX = 49
    ENERGY_CORE_IN_METAL_BOX = 50

    DIGITAL_CORE = 51
    GLYPHIC_CANYON_TEMPLE = 52
    LETHAL_HIGHWAY_TANK = 53
    CRYPTIC_CASTLE_LANTERN = 54
    CREAM = 55
    CHEESE = 56
    PRISON_ISLAND_DISC = 57
    CENTRAL_CITY_BIG_BOMB = 58
    DOOM_RESEARCHER = 59
    SKY_TROOPS_EGG_SHIP = 60
    SKY_TROOPS_TEMPLE = 61
    MAD_MATRIX_BOMB = 62
    MAD_MATRIX_TERMINAL = 63
    THE_ARK_DEFENSE_UNIT = 64
    AIR_FLEET_PRESIDENT_POD = 65
    IRON_JUNGLE_EGG_BALLOON = 66
    SPACE_GADGET_DEFENSE_UNIT = 67
    GUN_FORTRESS_COMPUTER = 68
    LAVA_SHELTER_DEFENSE = 69
    COSMIC_FALL_COMPUTER_ROOM = 70
    FINAL_HAUNT_SHIELD = 71

    PARTNER = 72

    KEY = 73
    GOAL_RING = 74
    FIRE = 75
    POISON_GAS = 76
    DARK_SPIN_ENTRY = 77
    DEFENSE_PROGRAM = 78
    RING_OF_FIRE = 79
    HELICOPTER = 80
    CLEAR_TRIGGER = 81

    ITEM_CAPSULE = 82
    BALLOON_ITEM = 83
    ITEM_IN_BOX = 84
    ITEM_IN_METAL_BOX = 85

    BLACK_WING_LOTTERY = 86
    EGG_PAWN_LOTTERY = 87


class SETObject:
    object_type: int
    stage: int
    index: int
    name: str
    vehicle: int
    restrictionType: int
    is_hard: bool
    weapon: int

    def __init__(self, object_type, stage, index, name,
                 vehicle=None, region=None, count=1, restrictionType=10, is_hard=False, weapon=None):
        self.object_type = object_type
        self.stage = stage
        self.index = index
        self.name = name
        self.vehicle = vehicle
        self.region = region
        self.count = count
        self.restrictionType = restrictionType
        self.is_hard = is_hard
        self.weapon = weapon
