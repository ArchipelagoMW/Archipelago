import logging
from typing import Dict, List, Callable, TYPE_CHECKING, NamedTuple
from BaseClasses import MultiWorld, Region, Entrance, CollectionState
from .Items import swords_table, stones_table, redhots_table
from .Names import RegionName, ItemName, LairName, ChestName, NPCName, NPCRewardName
from .Locations import SoulBlazerLocation, all_locations_table
from .Options import SoulBlazerOptions
from .Rules import no_requirement, RuleFlag, rule_for_flag

if TYPE_CHECKING:
    from . import SoulBlazerWorld


locations_for_region: Dict[str, List[str]] = {
    RegionName.MENU: [],
    # Act 1 Regions
    RegionName.TRIAL_ROOM: [
        ChestName.TRIAL_ROOM,
        NPCRewardName.MAGICIAN,
        NPCRewardName.MAGICIAN_SOUL,
    ],
    RegionName.GRASS_VALLEY_WEST: [
        NPCRewardName.TOOL_SHOP_OWNER,
        NPCRewardName.TEDDY,
        NPCRewardName.VILLAGE_CHIEF,
    ],
    RegionName.GRASS_VALLEY_EAST: [
        NPCRewardName.EMBLEM_A_TILE,
        NPCRewardName.GOAT_PEN_CORNER,
        NPCRewardName.PASS_TILE,
        NPCRewardName.TILE_IN_CHILDS_SECRET_CAVE,
        NPCRewardName.RECOVERY_SWORD_CRYSTAL,
    ],
    RegionName.GRASS_VALLEY_TREASURE_ROOM: [
        NPCRewardName.GRASS_VALLEY_SECRET_ROOM_CRYSTAL,
        ChestName.GRASS_VALLEY_SECRET_CAVE_LEFT,
        ChestName.GRASS_VALLEY_SECRET_CAVE_RIGHT,
    ],
    RegionName.UNDERGROUND_CASTLE_WEST: [
        LairName.OLD_WOMAN,
        LairName.TOOL_SHOP_OWNER,
        LairName.TULIP,
        LairName.BRIDGE_GUARD,
        LairName.IVY_CHEST_ROOM,
        LairName.WATER_MILL,
        NPCRewardName.UNDERGROUND_CASTLE_CRYSTAL,
        ChestName.UNDERGROUND_CASTLE_HERB,
        ChestName.UNDERGROUND_CASTLE_12GEM,
        ChestName.UNDERGROUND_CASTLE_DREAM_ROD,
    ],
    RegionName.UNDERGROUND_CASTLE_EAST: [
        ChestName.UNDERGROUND_CASTLE_LEOS_BRUSH,
        LairName.OLD_MAN,
        LairName.OLD_MAN2,
        LairName.GOAT_HERB,
        LairName.LISA,
        LairName.TULIP2,
        LairName.ARCHITECT,
        LairName.IVY2,
        LairName.TEDDY,
        LairName.GOAT,
        LairName.TULIP3,
        LairName.LEOS_HOUSE,
    ],
    RegionName.LEOS_PAINTING: [
        LairName.VILLAGE_CHIEF,
        LairName.IVY,
        LairName.LONELY_GOAT,
        LairName.TULIP_PASS,
        LairName.BOY_CABIN,
        LairName.BOY_CAVE,
        LairName.IVY_EMBLEM_A,
        LairName.IVY_RECOVERY_SWORD,
        LairName.TULIP4,
        LairName.GOAT2,
        ChestName.LEOS_PAINTING_HERB,
        ChestName.LEOS_PAINTING_TORNADO,
    ],
    # Act 2 Regions
    RegionName.GREENWOOD: [
        NPCRewardName.REDHOT_MIRROR_BIRD,
        NPCRewardName.MAGIC_BELL_CRYSTAL,
        NPCRewardName.WOODSTIN_TRIO,
        NPCRewardName.GREENWOODS_GUARDIAN,
        NPCRewardName.GREENWOOD_LEAVES_TILE,
        NPCRewardName.SHIELD_BRACELET_MOLE,
        NPCRewardName.PSYCHO_SWORD_SQUIRREL,
        NPCRewardName.EMBLEM_C_SQUIRREL,
        NPCRewardName.MOLE_SOUL_OF_LIGHT,
        ChestName.GREENWOOD_ICE_ARMOR,
        ChestName.GREENWOOD_TUNNELS,
    ],
    RegionName.LOST_MARSHES_SOUTH: [
        LairName.BIRD,
        LairName.DOG,
        LairName.SQUIRREL_PSYCHO_SWORD,
        LairName.BIRD2,
        LairName.MOLE_SOUL_OF_LIGHT,
        LairName.CROCODILE,
        LairName.SQUIRREL,
        LairName.MOLE,
        LairName.DEER,
        LairName.DOG2,
        LairName.DOG4,
        LairName.DOG5,
        LairName.CROCODILE2,
        LairName.SQUIRREL_ICE_ARMOR,
        LairName.MOLE2,
        LairName.SQUIRREL3,
        LairName.BIRD_GREENWOOD_LEAF,
        LairName.MOLE3,
        LairName.DEER_MAGIC_BELL,
        LairName.SQUIRREL2,
        LairName.BIRD3,
        NPCRewardName.WATER_SHRINE_CRYSTAL,
        NPCRewardName.WATER_SHRINE_TILE,
        NPCRewardName.LIGHT_ARROW_CRYSTAL,
        NPCRewardName.FIRE_SHRINE_CRYSTAL,
        ChestName.WATER_SHRINE_1,
        ChestName.WATER_SHRINE_2_N,
        ChestName.WATER_SHRINE_2_HERB,
        ChestName.WATER_SHRINE_3_SE,
        ChestName.WATER_SHRINE_3_SW,
        ChestName.FIRE_SHRINE_1,
        ChestName.FIRE_SHRINE_2_DISAPPEARING,
        ChestName.FIRE_SHRINE_2_SCORPION,
        ChestName.FIRE_SHRINE_3_100GEM,
        ChestName.FIRE_SHRINE_3_60GEM,
    ],
    RegionName.LOST_MARSHES_NORTH: [
        LairName.MOLE_SHIELD_BRACELET,
        LairName.DOG3,
        LairName.SQUIRREL_EMBLEM_C,
        NPCRewardName.LOST_MARSH_CRYSTAL,
        ChestName.LIGHT_SHRINE,
    ],
    RegionName.LIGHT_SHRINE_DARK: [
        LairName.CROCODILE3,
        LairName.MONMO,
        LairName.GREENWOODS_GUARDIAN,
        LairName.BIRD_RED_HOT_MIRROR,
    ],
    # Act 3 Regions
    RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA: [
        LairName.DOLPHIN2,
        LairName.MERMAID4,
        LairName.MERMAID5,
        LairName.MERMAID6,
        LairName.MERMAID_BUBBLE_ARMOR,
        NPCRewardName.MERMAID_QUEEN,
        ChestName.SOUTHERTA,
    ],
    RegionName.SEABED_SANCTUARY_SOUTH: [
        NPCRewardName.BUBBLE_ARMOR_MERMAID,
        NPCRewardName.REDHOT_STICK_MERMAID,
        ChestName.ST_ELLIS_MERMAIDS_TEARS,
    ],
    RegionName.SEABED_SANCTUARY_WEST: [
        NPCRewardName.LUE,
    ],
    RegionName.SEABED_SANCTUARY_SOUTHWEST: [
        NPCRewardName.MAGIC_FLARE_MERMAID,
        ChestName.ST_ELLIS_BIG_PEARL,
    ],
    RegionName.SEABED_SANCTUARY_EAST: [
        NPCRewardName.NORTHEASTERN_MERMAID_HERB,
    ],
    RegionName.SEABED_SANCTUARY_SOUTHEAST: [
        NPCRewardName.ANGELFISH_SOUL_OF_SHIELD,
    ],
    RegionName.SEABED_HUB: [
        # TODO: make bubble armor requirement for this lair an optional toggle
        LairName.MERMAID_STATUE_ROCKBIRD,
    ],
    RegionName.ROCKBIRD: [
        LairName.MERMAID9,
        LairName.MERMAID_TEARS,
        LairName.MERMAID_MAGIC_FLARE,
        LairName.ANGELFISH_SOUL_OF_SHIELD,
        LairName.MERMAID_STATUE_DUREAN,
        NPCRewardName.ROCKBIRD_CRYSTAL,
        ChestName.ROCKBIRD_60GEM,
        ChestName.ROCKBIRD_HERB,
    ],
    RegionName.DUREAN: [
        LairName.DOLPHIN_PEARL,
        LairName.LUE,
        LairName.MERMAID2,
        LairName.MERMAID_NANA,
        LairName.DOLPHIN_SAVES_LUE,
        LairName.MERMAID3,
        LairName.MERMAID_RED_HOT_STICK,
        LairName.MERMAID_PEARL,
        LairName.MERMAID_STATUE_BLESTER,
        NPCRewardName.SEABED_CRYSTAL_NEAR_DUREAN,
        ChestName.DUREAN_STRANGE_BOTTLE,
        ChestName.DUREAN_CRITICAL_SWORD,
    ],
    RegionName.BLESTER: [
        LairName.ANGELFISH,
        LairName.ANGELFISH2,
        LairName.MERMAID,
        LairName.MERMAID7,
        LairName.ANGELFISH4,
        LairName.MERMAID8,
        LairName.DOLPHIN_SECRET_CAVE,
        LairName.MERMAID_STATUE_GHOST_SHIP,
        NPCRewardName.SEABED_CRYSTAL_NEAR_BLESTER,
    ],
    RegionName.GHOST_SHIP: [
        LairName.ANGELFISH3,
        LairName.DOLPHIN,
        LairName.MERMAID_QUEEN,
        ChestName.SEABED_POWER_BRACELET,
        ChestName.GHOST_SHIP,
    ],
    RegionName.SEABED_SECRET_CAVE: [
        ChestName.SEABED_SECRET_TL,
        ChestName.SEABED_SECRET_TR,
        ChestName.SEABED_SECRET_BL,
        ChestName.SEABED_SECRET_BR,
    ],
    # Act 4 Regions
    RegionName.MOUNTAIN_HUB_NORTH_SLOPE: [
        LairName.GIRL,
        LairName.GRANDPA,
        LairName.MUSHROOM,
        LairName.BOY,
        LairName.GRANDPA2,
        LairName.SNAIL_JOCKEY,
        LairName.BOY_MUSHROOM_SHOES,
        LairName.GIRL2,
        NPCRewardName.MOUNTAIN_OF_SOULS_CRYSTAL,
        NPCRewardName.EMBLEM_E_SNAIL,
        NPCRewardName.MUSHROOM_SHOES_BOY,
        ChestName.MOUNTAIN_OF_SOULS_1,
        ChestName.MOUNTAIN_OF_SOULS_2_L,
        ChestName.MOUNTAIN_OF_SOULS_2_LL,
        ChestName.MOUNTAIN_OF_SOULS_2_R,
        ChestName.MOUNTAIN_OF_SOULS_2_RR,
    ],
    RegionName.MOUNTAIN_KING: [
        NPCRewardName.MOUNTAIN_KING,
    ],
    RegionName.NOME: [
        NPCRewardName.NOME,
    ],
    RegionName.LAYNOLE: [
        LairName.GRANDMA,
        LairName.MUSHROOM2,
        LairName.SNAIL_RACER,
        LairName.SNAIL_RACER2,
        LairName.GIRL3,
        LairName.MUSHROOM3,
        LairName.SNAIL,
        LairName.GRANDPA3,
        LairName.GRANDPA4,
        LairName.GRANDPA_LUNE,
        LairName.SNAIL2,
        LairName.GRANDPA5,
        ChestName.LAYNOLE_LUCKY_BLADE,
    ],
    RegionName.LUNE: [
        LairName.BOY2,
        LairName.NOME,
        LairName.MUSHROOM_EMBLEM_F,
        LairName.DANCING_GRANDMA,
        LairName.DANCING_GRANDMA2,
        LairName.SNAIL_EMBLEM_E,
        LairName.MOUNTAIN_KING,
        NPCRewardName.LUNE_CRYSTAL,
        NPCRewardName.EMBLEM_F_TILE,
        ChestName.LAYNOLE_HERB,
        ChestName.LAYNOLE_ROTATOR,
    ],
    # Act 5 Regions
    RegionName.LEOS_LAB_START: [
        LairName.PLANT,
        LairName.CAT,
        LairName.GREAT_DOOR_ZANTETSU_SWORD,
    ],
    RegionName.LEOS_LAB_MAIN: [
        NPCRewardName.CHEST_OF_DRAWERS_MYSTIC_ARMOR,
        NPCRewardName.EMBLEM_G_UNDER_CHEST_OF_DRAWERS,
        NPCRewardName.SPARK_BOMB_MOUSE,
        NPCRewardName.HERB_PLANT_IN_LEOS_LAB,
        ChestName.LEOS_LAB_ZANTETSU,
    ],
    RegionName.LEOS_LAB_2ND_FLOOR: [
        NPCRewardName.LEOS_CAT_DOOR_KEY,
        NPCRewardName.ACTINIDIA_PLANT,
        NPCRewardName.GREAT_DOOR_SOUL_OF_DETECTION,
    ],
    RegionName.LEOS_LAB_ATTIC: [
        NPCRewardName.MARIE,
        NPCRewardName.CHEST_OF_DRAWERS_HERB,
    ],
    RegionName.LEOS_LAB_BASEMENT_1_METAL: [
        LairName.PLANT_HERB,
        LairName.CAT2,
        LairName.CAT3,
        LairName.GREAT_DOOR,
        LairName.CHEST_OF_DRAWERS_MYSTIC_ARMOR,
    ],
    RegionName.LEOS_LAB_BASEMENT_2: [
        LairName.CAT_DOOR_KEY,
        LairName.STEPS_UPSTAIRS,
        LairName.MOUSE,
        LairName.GREAT_DOOR_MODEL_TOWNS,
        LairName.MODEL_TOWN1,
        NPCRewardName.LEOS_LAB_BASEMENT_CRYSTAL,
    ],
    RegionName.LEOS_LAB_MODEL_TOWN_1: [
        LairName.CHEST_OF_DRAWERS,
        LairName.PLANT2,
        LairName.MOUSE2,
        LairName.MOUSE3,
        LairName.MOUSE4,
        LairName.MOUSE_SPARK_BOMB,
        LairName.GREAT_DOOR_SOUL_OF_DETECTION,
        LairName.MODEL_TOWN2,
        LairName.STEPS_MARIE,
        NPCRewardName.MODEL_TOWN_1_CRYSTAL,
        ChestName.MODEL_TOWN_1_SE,
        ChestName.MODEL_TOWN_1_NL,
        ChestName.MODEL_TOWN_1_NR,
    ],
    RegionName.LEOS_LAB_MODEL_TOWN_2: [
        LairName.CHEST_OF_DRAWERS2,
        LairName.PLANT_ACTINIDIA_LEAVES,
        LairName.MOUSE5,
        LairName.CAT4,
        LairName.STAIRS_POWER_PLANT,
        ChestName.MODEL_TOWN_2_TOP,
        ChestName.MODEL_TOWN_2_BOT,
    ],
    RegionName.LEOS_LAB_POWER_PLANT: [
        LairName.DOLL,
        LairName.MARIE,
        NPCRewardName.POWER_PLANT_CRYSTAL,
        ChestName.POWER_PLANT_LIGHT_ARMOR,
    ],
    # Act 6 Regions
    RegionName.MAGRIDD_CASTLE_TOWN: [
        LairName.SOLDIER,
        NPCRewardName.HARP_STRING_TILE,
        ChestName.CASTLE_BASEMENT_1_W,
        ChestName.CASTLE_BASEMENT_1_SPIRIT_SWORD,
        NPCRewardName.ELEMENTAL_MAIL_SOLDIER,
        NPCRewardName.QUEEN_MAGRIDD_VIP_CARD,
        NPCRewardName.PLATINUM_CARD_SOLDIER,
        NPCRewardName.MAID_HERB,
        NPCRewardName.EMBLEM_H_TILE,
        NPCRewardName.KING_MAGRIDD,
        NPCRewardName.SOLDIER_SOUL_OF_REALITY,
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT: [
        LairName.SOLDIER2,
        LairName.SINGER_CONCERT_HALL,
        LairName.SOLDIER3,
        LairName.SOLDIER4,
        LairName.SOLDIER5,
        LairName.SOLDIER6,
        LairName.SOLDIER_ELEMENTAL_MAIL,
        LairName.MAID,
        LairName.SOLDIER_LEFT_TOWER,
        LairName.SOLDIER_DOK,
        LairName.SOLDIER_PLATINUM_CARD,
        LairName.SINGER,
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT_INVIS: [
        ChestName.CASTLE_BASEMENT_2_N,
        ChestName.CASTLE_BASEMENT_2_SW,
        ChestName.CASTLE_BASEMENT_2_MIDDLE,
        ChestName.CASTLE_BASEMENT_3,
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER: [
        LairName.SOLDIER_SOUL_OF_REALITY,
        LairName.SOLDIER_WITH_LEO,
        LairName.SOLDIER_RIGHT_TOWER,
        LairName.DR_LEO,
        LairName.SOLDIER7,
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER_INVIS: [
        LairName.MAID2,
        LairName.QUEEN_MAGRIDD,
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER: [
        LairName.MAID_HERB,
        LairName.SOLDIER8,
        LairName.SOLDIER_CASTLE,
    ],
    # Everything past the invisible staircase
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS: [
        LairName.SOLDIER9,
        LairName.SOLDIER10,
        LairName.SOLDIER11,
        LairName.KING_MAGRIDD,
        ChestName.CASTLE_RIGHT_TOWER_2_L,
        ChestName.CASTLE_RIGHT_TOWER_2_R,
        ChestName.CASTLE_RIGHT_TOWER_3_TL,
        ChestName.CASTLE_RIGHT_TOWER_3_BR,
        NPCRewardName.SUPER_BRACELET_TILE,
    ],
    RegionName.MAGRIDD_CASTLE_LEO: [
        NPCRewardName.LEO_ON_THE_AIRSHIP_DECK,
    ],
    # Act 7 Regions
    RegionName.WORLD_OF_EVIL: [
        ChestName.WOE_1_SE,
        ChestName.WOE_1_SW,
        ChestName.WOE_1_REDHOT_BALL,
        ChestName.WOE_2,
        ChestName.DAZZLING_SPACE_SE,
        ChestName.DAZZLING_SPACE_SW,
    ],
    RegionName.DEATHTOLL: [
        # Victory event is placed here later.
    ],
}


class ExitData(NamedTuple):
    destination: str
    """The destination region name."""
    has_all: List[str] = []
    """List of item names, all of which are required to use this exit."""
    # TODO: Might need to refactor this data structure if any location has multiple 'any' dependencies
    # TODO: if the only any ends up being swords/magic then change this to flag instead?
    has_any: List[str] = []
    """List of item names, where only one are required to use this exit."""
    # TODO: May have to refactor data structure if location reachable requirements are needed
    rule_flag: RuleFlag = RuleFlag.NONE


exits_for_region: Dict[str, List[ExitData]] = {
    RegionName.MENU: [
        ExitData(RegionName.TRIAL_ROOM),
    ],
    # Act 1 Exits
    RegionName.TRIAL_ROOM: [
        ExitData(RegionName.GRASS_VALLEY_WEST, rule_flag=RuleFlag.HAS_SWORD),
    ],
    RegionName.GRASS_VALLEY_WEST: [
        ExitData(RegionName.GRASS_VALLEY_EAST, [NPCName.BRIDGE_GUARD]),
        ExitData(RegionName.UNDERGROUND_CASTLE_WEST),
        ExitData(RegionName.GREENWOOD, [NPCName.OLD_WOMAN, NPCName.VILLAGE_CHIEF]),
    ],
    RegionName.GRASS_VALLEY_EAST: [
        ExitData(RegionName.GRASS_VALLEY_TREASURE_ROOM, [NPCName.IVY_CHEST_ROOM]),
        ExitData(RegionName.LEOS_PAINTING, [NPCName.ARCHITECT, NPCName.LEOS_HOUSE, ItemName.LEOSBRUSH]),
    ],
    RegionName.UNDERGROUND_CASTLE_WEST: [
        ExitData(RegionName.UNDERGROUND_CASTLE_EAST, [NPCName.BRIDGE_GUARD, NPCName.WATER_MILL])
    ],
    # Act 2 Exits
    RegionName.GREENWOOD: [
        ExitData(RegionName.LOST_MARSHES_SOUTH),
        ExitData(RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA, [NPCName.GREENWOODS_GUARDIAN]),
    ],
    RegionName.LOST_MARSHES_SOUTH: [
        ExitData(RegionName.LOST_MARSHES_NORTH, [ItemName.TURBOSLEAVES]),
    ],
    RegionName.LOST_MARSHES_NORTH: [
        ExitData(RegionName.LIGHT_SHRINE_DARK, [ItemName.SOUL_LIGHT]),
    ],
    # Act 3 Exits
    RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA: [
        ExitData(RegionName.SEABED_SANCTUARY_SOUTH, [NPCName.MERMAID_BUBBLE_ARMOR]),
        ExitData(RegionName.SEABED_SANCTUARY_WEST, [NPCName.MERMAID_PEARL, NPCName.MERMAID4]),
        ExitData(RegionName.SEABED_SANCTUARY_EAST, [NPCName.DOLPHIN2]),
        ExitData(RegionName.MOUNTAIN_HUB_NORTH_SLOPE, [NPCName.MERMAID_QUEEN]),
    ],
    RegionName.SEABED_SANCTUARY_SOUTH: [
        ExitData(RegionName.SEABED_SANCTUARY_WEST, [NPCName.MERMAID_PEARL]),
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHEAST, [NPCName.ANGELFISH_SOUL_OF_SHIELD]),
        ExitData(RegionName.SEABED_HUB, [ItemName.BUBBLEARMOR]),
    ],
    RegionName.SEABED_SANCTUARY_WEST: [
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHWEST, [NPCName.DOLPHIN_PEARL]),
    ],
    RegionName.SEABED_SANCTUARY_EAST: [
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHEAST, [NPCName.ANGELFISH_SOUL_OF_SHIELD, NPCName.MERMAID5])
    ],
    RegionName.SEABED_HUB: [
        ExitData(RegionName.ROCKBIRD, [NPCName.MERMAID_STATUE_ROCKBIRD]),
        ExitData(RegionName.DUREAN, [NPCName.MERMAID_STATUE_DUREAN]),
        ExitData(RegionName.BLESTER, [NPCName.MERMAID_STATUE_BLESTER]),
        ExitData(RegionName.GHOST_SHIP, [NPCName.MERMAID_STATUE_GHOST_SHIP]),
    ],
    RegionName.GHOST_SHIP: [
        ExitData(
            RegionName.SEABED_SECRET_CAVE,
            [NPCName.MERMAID_PEARL, NPCName.DOLPHIN_SECRET_CAVE, ItemName.DREAMROD, ItemName.BIGPEARL],
        ),
    ],
    # Act 4 Exits
    RegionName.MOUNTAIN_HUB_NORTH_SLOPE: [
        ExitData(RegionName.LAYNOLE, [ItemName.MUSHROOMSHOES]),
        ExitData(RegionName.LUNE, [NPCName.GIRL3, NPCName.GRANDPA4, NPCName.GRANDPA_LUNE, ItemName.LUCKYBLADE]),
        ExitData(
            RegionName.MOUNTAIN_KING,
            [NPCName.BOY, NPCName.GRANDPA3, NPCName.MOUNTAIN_KING],
            [NPCName.BOY_MUSHROOM_SHOES, NPCName.GRANDPA],
        ),
        ExitData(
            RegionName.NOME,
            [NPCName.GIRL3, NPCName.GRANDPA4, NPCName.MUSHROOM2, NPCName.GRANDPA5, NPCName.MOUNTAIN_KING, NPCName.NOME],
        ),
    ],
    RegionName.NOME: [ExitData(RegionName.LEOS_LAB_START, [])],
    # Act 5 Exits
    RegionName.LEOS_LAB_START: [
        ExitData(RegionName.LEOS_LAB_BASEMENT_1_METAL, rule_flag=RuleFlag.CAN_CUT_METAL),
        ExitData(RegionName.LEOS_LAB_MAIN, [NPCName.GREAT_DOOR_ZANTETSU_SWORD]),
        ExitData(RegionName.LEOS_LAB_2ND_FLOOR, [NPCName.STEPS_UPSTAIRS, NPCName.GREAT_DOOR_MODEL_TOWNS]),
        ExitData(RegionName.LEOS_LAB_POWER_PLANT, [NPCName.STAIRS_POWER_PLANT]),
    ],
    RegionName.LEOS_LAB_BASEMENT_1_METAL: [
        ExitData(RegionName.LEOS_LAB_BASEMENT_2, [ItemName.ICEARMOR]),
    ],
    RegionName.LEOS_LAB_2ND_FLOOR: [
        ExitData(RegionName.LEOS_LAB_MODEL_TOWN_1, [NPCName.MODEL_TOWN1]),
        ExitData(RegionName.LEOS_LAB_MODEL_TOWN_2, [NPCName.MODEL_TOWN2]),
        ExitData(RegionName.LEOS_LAB_ATTIC, [NPCName.STEPS_MARIE]),
    ],
    RegionName.LEOS_LAB_ATTIC: [
        ExitData(RegionName.MAGRIDD_CASTLE_TOWN, [NPCName.MARIE]),
    ],
    # Act 6 Exits
    RegionName.MAGRIDD_CASTLE_TOWN: [
        ExitData(RegionName.MAGRIDD_CASTLE_BASEMENT, rule_flag=RuleFlag.CAN_CUT_SPIRIT),
        ExitData(RegionName.MAGRIDD_CASTLE_LEFT_TOWER, [NPCName.SOLDIER_LEFT_TOWER, ItemName.PLATINUMCARD]),
        ExitData(RegionName.MAGRIDD_CASTLE_RIGHT_TOWER, [NPCName.SOLDIER_RIGHT_TOWER, ItemName.VIPCARD]),
        ExitData(
            RegionName.WORLD_OF_EVIL,
            [NPCName.SOLDIER_CASTLE, NPCName.KING_MAGRIDD],
            rule_flag=RuleFlag.HAS_STONES,
        ),
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT: [
        ExitData(RegionName.MAGRIDD_CASTLE_BASEMENT_INVIS, [ItemName.SOUL_REALITY]),
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER: [
        ExitData(RegionName.MAGRIDD_CASTLE_LEFT_TOWER_INVIS, [ItemName.SOUL_REALITY]),
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER: [
        ExitData(RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS, [ItemName.SOUL_REALITY]),
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS: [
        ExitData(RegionName.MAGRIDD_CASTLE_LEO, [NPCName.DR_LEO, NPCName.SOLDIER_WITH_LEO, NPCName.SOLDIER_DOK])
    ],
    RegionName.MAGRIDD_CASTLE_LEO: [
        # The platinum card soldier blows up, letting you get in without platinum card
        ExitData(RegionName.MAGRIDD_CASTLE_LEFT_TOWER, [NPCName.SOLDIER_LEFT_TOWER])
    ],
    # Act 7 Exits
    RegionName.WORLD_OF_EVIL: [
        ExitData(
            RegionName.DEATHTOLL,
            [ItemName.SOULARMOR, ItemName.SOULBLADE, ItemName.PHOENIX],
            [],
            RuleFlag.PHOENIX_CUTSCENE,
        )
    ],
}

exits_for_region_open_mode: Dict[str, List[ExitData]] = {
    # Grass Valley west now connects to all Act Hubs
    RegionName.GRASS_VALLEY_WEST: [
        ExitData(RegionName.GRASS_VALLEY_EAST, [NPCName.BRIDGE_GUARD]),
        ExitData(RegionName.UNDERGROUND_CASTLE_WEST),
        ExitData(RegionName.GREENWOOD),
        ExitData(RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA),
        ExitData(RegionName.MOUNTAIN_HUB_NORTH_SLOPE),
        ExitData(RegionName.LEOS_LAB_START),
        ExitData(RegionName.MAGRIDD_CASTLE_TOWN),
        ExitData(RegionName.WORLD_OF_EVIL, rule_flag=RuleFlag.HAS_STONES),
    ],
}

exits_for_region_open_deathtoll: Dict[str, List[ExitData]] = {
    # No longer needs Phoenix/Dancing Grandma cutscene.
    RegionName.WORLD_OF_EVIL: [
        ExitData(
            RegionName.DEATHTOLL,
            [
                ItemName.SOULARMOR,
                ItemName.SOULBLADE,
                ItemName.PHOENIX,
            ],
        )
    ],
}


def get_rule_for_exit(data: ExitData, player: int) -> Callable[[CollectionState], bool]:
    """Returns the access rule for the given exit."""

    if not data.has_all and not data.has_any:

        def rule_simple(state: CollectionState) -> bool:
            return rule_for_flag[data.rule_flag](state, player)

        return rule_simple

    def rule(state: CollectionState) -> bool:
        return (
            rule_for_flag[data.rule_flag](state, player)
            and state.has_all(data.has_all, player)
            and (not data.has_any or state.has_any(data.has_any, player))
        )

    return rule


def create_regions(world: "SoulBlazerWorld") -> None:
    """
    Creates and connects regions for the world.
    Also sets up entrance rules.
    """

    # Create all regions
    regions = {k: Region(k, world.player, world.multiworld) for k in locations_for_region.keys()}
    world.multiworld.regions += regions.values()

    all_locations: List[SoulBlazerLocation] = []

    # Populate each region with locations and exits
    for region in regions.values():
        locations = [
            SoulBlazerLocation(world.player, loc, data, region)
            for loc in locations_for_region[region.name]
            for data in [all_locations_table[loc]]
        ]

        region.locations += locations
        all_locations += locations
        exits = {**exits_for_region}
        exits = {**exits, **exits_for_region_open_deathtoll} if world.options.open_deathtoll else exits
        exits = {**exits, **exits_for_region_open_mode} if world.options.act_progression == "open" else exits

        for exit_data in exits.get(region.name, []):
            connect_to = regions[exit_data.destination]
            region.connect(connect_to, None, get_rule_for_exit(exit_data, world.player))

    # All of the locations should have been placed in regions.
    # TODO: Delete once confident that all locations are in or move into a test instead?
    if len(all_locations) < len(all_locations_table):
        all_location_names = {loc.name for loc in all_locations}
        all_locations_table_names = {*all_locations_table.keys()}
        unplaced = all_locations_table_names - all_location_names
        logging.warning("Soulblazer: Regions do not contain all locations. Something is likely broken with the logic.")
        for loc in unplaced:
            logging.warning(loc)
