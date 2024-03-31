from typing import Callable, TYPE_CHECKING, NamedTuple
from BaseClasses import MultiWorld, Region, Entrance
from .Items import swords_table
from .Names import RegionName, ItemName, LairName, ChestName, NPCName, NPCRewardName

if TYPE_CHECKING:
    from . import SoulBlazerWorld

# TODO: I dont think this is needed since we can just use locations_for_region.keys()?
regions_act1: list[str] = [
    RegionName.TRIAL_ROOM,
    RegionName.GRASS_VALLEY_WEST,
    RegionName.GRASS_VALLEY_EAST,
    RegionName.GRASS_VALLEY_TREASURE_ROOM,
    RegionName.UNDERGROUND_CASTLE_WEST,
    RegionName.UNDERGROUND_CASTLE_EAST,
    RegionName.LEOS_PAINTING,
]

locations_for_region: dict[str, list[str]] = {
    # Act 1 Regions
    # We could probably merge this region with Grass Valley West since we prefill the starting sword.
    RegionName.TRIAL_ROOM: [
        ChestName.TRIAL_ROOM,
        NPCRewardName.MAGICIAN,
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
        ChestName.LEOS_PAINTING_TORNADO
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
        LairName.CROCODILE3,
        LairName.MONMO,
        LairName.GREENWOODS_GUARDIAN,
        LairName.BIRD_RED_HOT_MIRROR,
        NPCRewardName.LOST_MARSH_CRYSTAL,
        ChestName.LIGHT_SHRINE,
    ]
}


class ExitData(NamedTuple):
    destination: str
    """The destination region name."""
    has_all: list[str] = []
    """List of item names, all of which are required to use this exit."""
    # TODO: Might need to refactor this data structure if any location has multiple 'any' dependencies
    has_any: list[str] = []
    """List of item names, where only one are required to use this exit."""
    # TODO: May have to refactor data structure if location reachable requirements are needed


# TODO: move this to rules?
exits_for_region: dict[str, ExitData] = {
    RegionName.MENU: [
        ExitData(RegionName.TRIAL_ROOM),
    ],
    # Act 1 Exits
    RegionName.TRIAL_ROOM: [
        ExitData(RegionName.GRASS_VALLEY_WEST, [], swords_table.keys()),
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
    # TODO: Add region/exit for Light Shrine Dark rooms?
    RegionName.GREENWOOD: [
        ExitData(RegionName.LOST_MARSHES_SOUTH),
        ExitData(RegionName.SEABED_SANCTUARY_HUB, [NPCName.GREENWOODS_GUARDIAN]),
    ],
    RegionName.LOST_MARSHES_SOUTH: [
        ExitData(RegionName.LOST_MARSHES_NORTH, [ItemName.TURBOSLEAVES])
    ]
}


def create_regions(world: "SoulBlazerWorld") -> None:
    """
    Creates and connects regions for the world.
    Also sets up entrance rules.
    """

    # Root region required by Archipelago

    menu_region = Region(RegionName.MENU, world.player, world.multiworld)
    world.multiworld.regions += menu_region


def get_rule_for_exit(exit_data: ExitData):
    # TODO: Implement
    pass
