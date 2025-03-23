import logging
from typing import Callable, TYPE_CHECKING, NamedTuple
from BaseClasses import MultiWorld, Region, Entrance, CollectionState
from .Data.Enums import ItemID, LairID, ChestID, NPCID, NPCRewardID, SoulID
from .Names import RegionName
from .Locations import SoulBlazerLocation, locations_by_name
from .Options import SoulBlazerOptions
from .Rules import RuleFlag, rule_for_flag

if TYPE_CHECKING:
    from . import SoulBlazerWorld


locations_for_region: dict[str, list[str]] = {
    RegionName.MENU: [],
    # Act 1 Regions
    RegionName.TRIAL_ROOM: [
        ChestID.TRIAL_ROOM.full_name,
        NPCRewardID.MAGICIAN.full_name,
        NPCRewardID.MAGICIAN_SOUL.full_name,
    ],
    RegionName.GRASS_VALLEY_WEST: [
        NPCRewardID.TOOL_SHOP_OWNER.full_name,
        NPCRewardID.TEDDY.full_name,
        NPCRewardID.VILLAGE_CHIEF.full_name,
    ],
    RegionName.GRASS_VALLEY_EAST: [
        NPCRewardID.GRASS_VALLEY_SE_CLIFF_TILE.full_name,
        NPCRewardID.GOAT_PEN_CORNER.full_name,
        NPCRewardID.UNDER_TULIP_TILE.full_name,
        NPCRewardID.HIDEOUT_CLIFF_TILE.full_name,
        NPCRewardID.HIDEOUT_CLIFF_CRYSTAL.full_name,
    ],
    RegionName.GRASS_VALLEY_TREASURE_ROOM: [
        NPCRewardID.GRASS_VALLEY_SECRET_CRYSTAL.full_name,
        ChestID.GRASS_VALLEY_SECRET_L.full_name,
        ChestID.GRASS_VALLEY_SECRET_R.full_name,
    ],
    RegionName.UNDERGROUND_CASTLE_WEST: [
        LairID.OLD_WOMAN_CHIEFS_HOUSE.full_name,
        LairID.TOOL_SHOP_OWNER.full_name,
        LairID.TULIP_CHIEFS_HOUSE.full_name,
        LairID.BRIDGE_GUARD.full_name,
        LairID.IVY_CHEST_ROOM.full_name,
        LairID.WATER_MILL.full_name,
        NPCRewardID.UNDERGROUND_CASTLE_CRYSTAL.full_name,
        ChestID.UNDERGROUND_CASTLE_PILLAR.full_name,
        ChestID.UNDERGROUND_CASTLE_TORCH.full_name,
        ChestID.UNDERGROUND_CASTLE_DREAM.full_name,
    ],
    RegionName.UNDERGROUND_CASTLE_EAST: [
        ChestID.UNDERGROUND_CASTLE_CENTER.full_name,
        LairID.LONELY_OLD_MAN.full_name,
        LairID.OLD_MAN_CRAB_WALK.full_name,
        LairID.GOAT_PEN.full_name,
        LairID.LISA.full_name,
        LairID.TULIP_ABOVE_DUNGEON.full_name,
        LairID.ARCHITECT.full_name,
        LairID.IVY_NEAR_DUNGEON.full_name,
        LairID.TEDDY.full_name,
        LairID.GOURMET_GOAT.full_name,
        LairID.TULIP_LEOS_HOUSE.full_name,
        LairID.LEOS_HOUSE.full_name,
    ],
    RegionName.LEOS_PAINTING: [
        LairID.VILLAGE_CHIEF.full_name,
        LairID.IVY_SE.full_name,
        LairID.LONELY_GOAT.full_name,
        LairID.TULIP_SLEEPING_PUSH.full_name,
        LairID.BOY_CABIN.full_name,
        LairID.BOY_CAVE.full_name,
        LairID.IVY_CLIFF_TILE.full_name,
        LairID.IVY_HIDEOUT_CRYSTAL.full_name,
        LairID.TULIP_GOAT_PEN.full_name,
        LairID.GOAT_WIFE.full_name,
        ChestID.LEOS_PAINTING_CENTER.full_name,
        ChestID.LEOS_PAINTING_METAL.full_name,
    ],
    # Act 2 Regions
    RegionName.GREENWOOD: [
        NPCRewardID.SHY_BIRD.full_name,
        NPCRewardID.MASTER_CRYSTAL.full_name,
        NPCRewardID.WOODSTIN_TRIO.full_name,
        NPCRewardID.GREENWOODS_GUARDIAN.full_name,
        NPCRewardID.TURBOS_REMAINS_TILE.full_name,
        NPCRewardID.MOLES_REWARD.full_name,
        NPCRewardID.HUNGRY_SQUIRREL.full_name,
        NPCRewardID.NOT_HUNGRY_SQUIRREL.full_name,
        NPCRewardID.MOLE_SOUL.full_name,
        ChestID.GREENWOOD_DREAM.full_name,
        ChestID.GREENWOOD_TUNNELS.full_name,
    ],
    RegionName.LOST_MARSHES_SOUTH: [
        LairID.BIRD_MARSH_ENTRANCE.full_name,
        LairID.DOG_WALKABLE.full_name,
        LairID.SQUIRREL_HUNGRY.full_name,
        LairID.BIRD_SE.full_name,
        LairID.MOLE_WITH_SOUL.full_name,
        LairID.CROCODILE_CENTER.full_name,
        LairID.SQUIRREL_WEST_TREE.full_name,
        LairID.MOLE_HOLE_TO_STUMP.full_name,
        LairID.DEER_WOODSTIN.full_name,
        LairID.DOG_SNIFFING.full_name,
        LairID.DOG_WAITER.full_name,
        LairID.DOG_GRAVEYARD.full_name,
        LairID.CROCODILE_GRAVEYARD.full_name,
        LairID.SQUIRREL_SLEEPING_STUMP.full_name,
        LairID.MOLE_PEEKABOO.full_name,
        LairID.SQUIRREL_WOODSTIN.full_name,
        LairID.BIRD_SLEEPING_TURBO.full_name,
        LairID.MOLE_HOLE_FOR_BLIND_MOLE.full_name,
        LairID.DEER_MASTER_CRYSTAL.full_name,
        LairID.SQUIRREL_CAFE.full_name,
        LairID.BIRD_NE.full_name,
        NPCRewardID.WATER_SHRINE_B1_CRYSTAL.full_name,
        NPCRewardID.WATER_SHRINE_B2_TILE.full_name,
        NPCRewardID.FIRE_SHRINE_B2_CRYSTAL.full_name,
        NPCRewardID.FIRE_SHRINE_1F_CRYSTAL.full_name,
        ChestID.WATER_SHRINE_1F.full_name,
        ChestID.WATER_SHRINE_B1_WATERFALL.full_name,
        ChestID.WATER_SHRINE_B1_SPIKE.full_name,
        ChestID.WATER_SHRINE_B2_SE.full_name,
        ChestID.WATER_SHRINE_B2_SW.full_name,
        ChestID.FIRE_SHRINE_1F.full_name,
        ChestID.FIRE_SHRINE_B1_DISAPPEARING.full_name,
        ChestID.FIRE_SHRINE_B1_METAL.full_name,
        ChestID.FIRE_SHRINE_B2_MID.full_name,
        ChestID.FIRE_SHRINE_B2_END.full_name,
    ],
    RegionName.LOST_MARSHES_NORTH: [
        LairID.MOLE_WITH_GIFT.full_name,
        LairID.DOG_WOODSTIN.full_name,
        LairID.SQUIRREL_NOT_HUNGRY.full_name,
        NPCRewardID.LOST_MARSH_CRYSTAL.full_name,
        ChestID.LIGHT_SHRINE_1F_SPIRIT.full_name,
    ],
    RegionName.LIGHT_SHRINE_DARK: [
        LairID.CROCODILE_W.full_name,
        LairID.MONMO.full_name,
        LairID.GREENWOODS_GUARDIAN.full_name,
        LairID.SHY_BIRD.full_name,
    ],
    # Act 3 Regions
    RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA: [
        LairID.DOLPHIN_NE_PLATFORM.full_name,
        LairID.MERMAID_TROUPE_LEADER.full_name,
        LairID.MERMAID_E_GUARD.full_name,
        LairID.MERMAID_DANCER_KANNA.full_name,
        LairID.MERMAID_COMMON_MAIN.full_name,
        NPCRewardID.MERMAID_QUEEN.full_name,
        ChestID.SOUTHERTA_TREE_MAZE.full_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTH: [
        NPCRewardID.COMMON_HOUSE_MAIN_MERMAID.full_name,
        NPCRewardID.COMMON_HOUSE_N_MERMAID.full_name,
        ChestID.ST_ELLIS_COMMON_EAST.full_name,
    ],
    RegionName.SEABED_SANCTUARY_WEST: [
        NPCRewardID.LUE.full_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTHWEST: [
        NPCRewardID.COMMON_HOUSE_W_ROOM_MERMAID.full_name,
        ChestID.ST_ELLIS_DOLPHIN_RIDE.full_name,
    ],
    RegionName.SEABED_SANCTUARY_EAST: [
        NPCRewardID.NORTHEAST_MERMAID.full_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTHEAST: [
        NPCRewardID.ANGELFISH_SOUL.full_name,
    ],
    RegionName.SEABED_HUB: [
        # TODO: make bubble armor requirement for this lair an optional toggle
        LairID.MERMAID_STATUE_ROCKBIRD.full_name,
    ],
    RegionName.ROCKBIRD: [
        LairID.MERMAID_DANCER_ANNA.full_name,
        LairID.MERMAID_COMMON_E.full_name,
        LairID.MERMAID_COMMON_W_ITEM.full_name,
        LairID.ANGELFISH_WITH_SOUL.full_name,
        LairID.MERMAID_STATUE_DUREAN.full_name,
        NPCRewardID.ROCKBIRD_CRYSTAL.full_name,
        ChestID.ROCKBIRD_EAST_LOWER.full_name,
        ChestID.ROCKBIRD_EAST_UPPER.full_name,
    ],
    RegionName.DUREAN: [
        LairID.DOLPHIN_RIDE_CHEST.full_name,
        LairID.LUE.full_name,
        LairID.MERMAID_DANCER_NANNA.full_name,
        LairID.MERMAID_NW_HOUSE.full_name,
        LairID.DOLPHIN_SAVES_LUE.full_name,
        LairID.MERMAID_ATTENDANT_L.full_name,
        LairID.MERMAID_COMMON_N_ITEM.full_name,
        LairID.MERMAID_W_GUARD.full_name,
        LairID.MERMAID_STATUE_BLESTER.full_name,
        NPCRewardID.SEABED_CRYSTAL_NEAR_DUREAN.full_name,
        ChestID.DUREAN_EAST_ISLAND.full_name,
        ChestID.DUREAN_LAVA_RIVER.full_name,
    ],
    RegionName.BLESTER: [
        LairID.ANGELFISH_CURIOUS.full_name,
        LairID.ANGELFISH_JUMPING.full_name,
        LairID.MERMAID_NE_HOUSE.full_name,
        LairID.MERMAID_ATTENDANT_R.full_name,
        LairID.ANGELFISH_CENTER_E.full_name,
        LairID.MERMAID_COMMON_SWIMMING.full_name,
        LairID.DOLPHIN_SLEEPING.full_name,
        LairID.MERMAID_STATUE_GHOST_SHIP.full_name,
        NPCRewardID.SEABED_CRYSTAL_NEAR_BLESTER.full_name,
    ],
    RegionName.GHOST_SHIP: [
        LairID.ANGELFISH_CENTER_S.full_name,
        LairID.DOLPHIN_NW_HOUSE.full_name,
        LairID.MERMAID_QUEEN.full_name,
        ChestID.SEABED_NW_SW_COVE.full_name,
        ChestID.GHOST_SHIP.full_name,
    ],
    RegionName.SEABED_SECRET_COVE: [
        ChestID.SEABED_SECRET_TL.full_name,
        ChestID.SEABED_SECRET_TR.full_name,
        ChestID.SEABED_SECRET_BL.full_name,
        ChestID.SEABED_SECRET_BR.full_name,
    ],
    # Act 4 Regions
    RegionName.MOUNTAIN_HUB_NORTH_SLOPE: [
        LairID.GIRL_ENTRANCE.full_name,
        LairID.GRANDPA_NW.full_name,
        LairID.MUSHROOM_NE_LAKE.full_name,
        LairID.BOY_W_TUNNEL.full_name,
        LairID.GRANDPA_HUSBAND.full_name,
        LairID.SNAIL_JOCKEY_LEGEND.full_name,
        LairID.BOY_WITH_GIFT.full_name,
        LairID.GIRL_GAZING.full_name,
        NPCRewardID.MOUNTAIN_SUMMIT_CAVE_CRYSTAL.full_name,
        NPCRewardID.SECRET_SNAIL.full_name,
        NPCRewardID.BOY_WITH_GIFT.full_name,
        ChestID.MOUNTAIN_SLOPES_1_SE.full_name,
        ChestID.MOUNTAIN_SLOPES_2_L.full_name,
        ChestID.MOUNTAIN_SLOPES_2_LL.full_name,
        ChestID.MOUNTAIN_SLOPES_2_R.full_name,
        ChestID.MOUNTAIN_SLOPES_2_RR.full_name,
    ],
    RegionName.MOUNTAIN_KING: [
        NPCRewardID.MOUNTAIN_KING.full_name,
    ],
    RegionName.NOME: [
        NPCRewardID.NOME.full_name,
    ],
    RegionName.LAYNOLE: [
        LairID.GRANDMA_TELEPORT.full_name,
        LairID.MUSHROOM_S_TUNNEL.full_name,
        LairID.SNAIL_JOCKEY_FLASH.full_name,
        LairID.SNAIL_JOCKEY_UNKNOWN.full_name,
        LairID.GIRL_E_TUNNEL.full_name,
        LairID.MUSHROOM_SOLITARY_ROOM.full_name,
        LairID.SNAIL_WITH_BOY.full_name,
        LairID.GRANDPA_SW_TUNNEL.full_name,
        LairID.GRANDPA_SE_LAKE.full_name,
        LairID.GRANDPA_LUNE.full_name,
        LairID.SNAIL_WITH_GRANDPA.full_name,
        LairID.GRANDPA_JAIL.full_name,
        ChestID.LAYNOLE_W_INVIS_BRIDGE.full_name,
    ],
    RegionName.LUNE: [
        LairID.BOY_IN_JAIL.full_name,
        LairID.NOME.full_name,
        LairID.SLEEPING_MUSHROOM.full_name,
        LairID.DANCING_GRANDMA_R.full_name,
        LairID.DANCING_GRANDMA_L.full_name,
        LairID.SNAIL_SECRET_ROOM.full_name,
        LairID.MOUNTAIN_KING.full_name,
        NPCRewardID.LUNE_PASSAGE_CRYSTAL.full_name,
        NPCRewardID.MUSHROOMS_DREAM_TILE.full_name,
        ChestID.LAYNOLE_E_INVIS_BRIDGE_1.full_name,
        ChestID.LAYNOLE_E_INVIS_BRIDGE_2.full_name,
    ],
    # Act 5 Regions
    RegionName.LEOS_LAB_START: [
        LairID.PLANT_W_LAB.full_name,
        LairID.CAT_STALKING_1.full_name,
        LairID.GREAT_DOOR_MAIN_LAB.full_name,
    ],
    RegionName.LEOS_LAB_MAIN: [
        NPCRewardID.LOCKED_ROOM_CHEST_OF_DRAWERS.full_name,
        NPCRewardID.UNDER_CHEST_OF_DRAWERS_TILE.full_name,
        NPCRewardID.MOUSE_WITH_GIFT.full_name,
        NPCRewardID.MOUSEHOLE_PLANT.full_name,
        ChestID.LEOS_LAB_MAIN.full_name,
    ],
    RegionName.LEOS_LAB_2ND_FLOOR: [
        NPCRewardID.SLEEPING_CAT.full_name,
        NPCRewardID.ACTINIDIA_PLANT.full_name,
        NPCRewardID.GREAT_DOOR_SOUL.full_name,
    ],
    RegionName.LEOS_LAB_ATTIC: [
        NPCRewardID.MARIE.full_name,
        NPCRewardID.ATTIC_CHEST_OF_DRAWERS.full_name,
    ],
    RegionName.LEOS_LAB_BASEMENT_1_METAL: [
        LairID.PLANT_MOUSEHOLE.full_name,
        LairID.CAT_STALKING_2.full_name,
        LairID.CAT_LOCKED_ROOM.full_name,
        LairID.GREAT_DOOR_LOCKED.full_name,
        LairID.CHEST_OF_DRAWERS_LOCKED_RM.full_name,
    ],
    RegionName.LEOS_LAB_BASEMENT_2: [
        LairID.CAT_SLEEPING.full_name,
        LairID.STEPS_TO_2F.full_name,
        LairID.MOUSE_OUTSIDE_HOLE.full_name,
        LairID.GREAT_DOOR_MODEL_TOWNS.full_name,
        LairID.MODEL_TOWN1.full_name,
        NPCRewardID.LEOS_LAB_B2_CRYSTAL.full_name,
    ],
    RegionName.LEOS_LAB_MODEL_TOWN_1: [
        LairID.CHEST_OF_DRAWERS_EXCERCISE.full_name,
        LairID.PLANT_LOCKED_ROOM.full_name,
        LairID.MOUSE_CIRCLING_1.full_name,
        LairID.MOUSE_BEDROOM.full_name,
        LairID.MOUSE_DEVOUT.full_name,
        LairID.MOUSE_WITH_GIFT.full_name,
        LairID.GREAT_DOOR_WITH_SOUL.full_name,
        LairID.MODEL_TOWN2.full_name,
        LairID.STEPS_ATTIC.full_name,
        NPCRewardID.MODEL_TOWN_1_CRYSTAL.full_name,
        ChestID.MODEL_TOWN_1_SE.full_name,
        ChestID.MODEL_TOWN_1_NL.full_name,
        ChestID.MODEL_TOWN_1_NR.full_name,
    ],
    RegionName.LEOS_LAB_MODEL_TOWN_2: [
        LairID.CHEST_OF_DRAWERS_ATTIC.full_name,
        LairID.PLANT_ACTINIDIA.full_name,
        LairID.MOUSE_CIRCLING_2.full_name,
        LairID.CAT_ATTIC.full_name,
        LairID.STAIRS_POWER_PLANT.full_name,
        ChestID.MODEL_TOWN_2_TOP.full_name,
        ChestID.MODEL_TOWN_2_BOT.full_name,
    ],
    RegionName.LEOS_LAB_POWER_PLANT: [
        LairID.DOLL_CHAPEL.full_name,
        LairID.MARIE.full_name,
        NPCRewardID.POWER_PLANT_CRYSTAL.full_name,
        ChestID.POWER_PLANT_START.full_name,
    ],
    # Act 6 Regions
    RegionName.MAGRIDD_CASTLE_TOWN: [
        LairID.SOLDIER_NEAR_BASEMENT.full_name,
        NPCRewardID.CASTLE_B1_SKELETON_TILE.full_name,
        ChestID.CASTLE_B1_W.full_name,
        ChestID.CASTLE_B1_NE.full_name,
        NPCRewardID.SLEEPING_SOLDIER.full_name,
        NPCRewardID.QUEEN_MAGRIDD_ITEM.full_name,
        NPCRewardID.UNDER_SOLDIER_TILE.full_name,
        NPCRewardID.MAID_AT_BAR.full_name,
        NPCRewardID.CASTLE_GROUNDS_TILE.full_name,
        NPCRewardID.KING_MAGRIDD.full_name,
        NPCRewardID.SOLDIER_SOUL.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT: [
        LairID.SOLDIER_ARCHITECT.full_name,
        LairID.SINGER_CONCERT_HALL.full_name,
        LairID.SOLDIER_KNOWS_SLEEPING.full_name,
        LairID.SOLDIER_PATROLLING.full_name,
        LairID.SOLDIER_RIGHT_MOAT.full_name,
        LairID.SOLDIER_CONCERT.full_name,
        LairID.SOLDIER_SLEEPING.full_name,
        LairID.MAID_BASHFUL.full_name,
        LairID.SOLDIER_LEFT_TOWER.full_name,
        LairID.SOLDIER_DOK.full_name,
        LairID.SOLDIER_CONCERT_ITEM.full_name,
        LairID.SINGER_OUTSIDE.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT_INVIS: [
        ChestID.CASTLE_B2_INVIS_N.full_name,
        ChestID.CASTLE_B2_INVIS_SW.full_name,
        ChestID.CASTLE_B2_INVIS_DEADEND.full_name,
        ChestID.CASTLE_B3_INVIS_NW.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER: [
        LairID.SOLDIER_WITH_SOUL.full_name,
        LairID.SOLDIER_WITH_LEO.full_name,
        LairID.SOLDIER_RIGHT_TOWER.full_name,
        LairID.DR_LEO.full_name,
        LairID.SOLDIER_BASHFUL.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER_INVIS: [
        LairID.MAID_CONCERT_HALL.full_name,
        LairID.QUEEN_MAGRIDD.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER: [
        LairID.MAID_HERB.full_name,
        LairID.SOLDIER_OBSERVANT.full_name,
        LairID.SOLDIER_CASTLE.full_name,
    ],
    # Everything past the invisible staircase
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS: [
        LairID.SOLDIER_NE_BUILDING.full_name,
        LairID.SOLDIER_BAR.full_name,
        LairID.SOLDIER_UNOBSERVANT.full_name,
        LairID.KING_MAGRIDD.full_name,
        ChestID.CASTLE_RIGHT_TOWER_2F_L.full_name,
        ChestID.CASTLE_RIGHT_TOWER_2F_R.full_name,
        ChestID.CASTLE_RIGHT_TOWER_3F_TL.full_name,
        ChestID.CASTLE_RIGHT_TOWER_3F_BR.full_name,
        NPCRewardID.QUEEN_MAGRIDD_TILE.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEO: [
        NPCRewardID.LEO_ON_THE_AIRSHIP_DECK.full_name,
    ],
    # Act 7 Regions
    RegionName.WORLD_OF_EVIL: [
        ChestID.WOE_1_SE.full_name,
        ChestID.WOE_1_SW.full_name,
        ChestID.WOE_1_WARP.full_name,
        ChestID.WOE_2_E.full_name,
        ChestID.DAZZLING_SPACE_SE.full_name,
        ChestID.DAZZLING_SPACE_SW.full_name,
    ],
    RegionName.DEATHTOLL: [
        # Victory event is placed here later.
    ],
}


class ExitData(NamedTuple):
    destination: str
    """The destination region name."""
    has_all: list[str] = []
    """List of item names, all of which are required to use this exit."""
    # TODO: Might need to refactor this data structure if any location has multiple 'any' dependencies
    # TODO: if the only any ends up being swords/magic then change this to flag instead?
    has_any: list[str] = []
    """List of item names, where only one are required to use this exit."""
    # TODO: May have to refactor data structure if location reachable requirements are needed
    rule_flag: RuleFlag = RuleFlag.NONE


exits_for_region: dict[str, list[ExitData]] = {
    RegionName.MENU: [
        ExitData(RegionName.TRIAL_ROOM),
    ],
    # Act 1 Exits
    RegionName.TRIAL_ROOM: [
        ExitData(RegionName.GRASS_VALLEY_WEST, rule_flag=RuleFlag.HAS_SWORD),
    ],
    RegionName.GRASS_VALLEY_WEST: [
        ExitData(RegionName.GRASS_VALLEY_EAST, [NPCID.BRIDGE_GUARD.full_name]),
        ExitData(RegionName.UNDERGROUND_CASTLE_WEST),
        ExitData(RegionName.GREENWOOD, [NPCID.OLD_WOMAN_CHIEFS_HOUSE.full_name, NPCID.VILLAGE_CHIEF.full_name]),
    ],
    RegionName.GRASS_VALLEY_EAST: [
        ExitData(RegionName.GRASS_VALLEY_TREASURE_ROOM, [NPCID.IVY_CHEST_ROOM.full_name]),
        ExitData(
            RegionName.LEOS_PAINTING,
            [NPCID.ARCHITECT.full_name, NPCID.LEOS_HOUSE.full_name, ItemID.LEOSBRUSH.full_name],
        ),
    ],
    RegionName.UNDERGROUND_CASTLE_WEST: [
        ExitData(RegionName.UNDERGROUND_CASTLE_EAST, [NPCID.BRIDGE_GUARD.full_name, NPCID.WATER_MILL.full_name])
    ],
    # Act 2 Exits
    RegionName.GREENWOOD: [
        ExitData(RegionName.LOST_MARSHES_SOUTH),
        ExitData(RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA, [NPCID.GREENWOODS_GUARDIAN.full_name]),
    ],
    RegionName.LOST_MARSHES_SOUTH: [
        ExitData(RegionName.LOST_MARSHES_NORTH, [ItemID.TURBOSLEAVES.full_name]),
    ],
    RegionName.LOST_MARSHES_NORTH: [
        ExitData(RegionName.LIGHT_SHRINE_DARK, [SoulID.SOUL_LIGHT.full_name]),
    ],
    # Act 3 Exits
    RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA: [
        ExitData(RegionName.SEABED_SANCTUARY_SOUTH, [NPCID.MERMAID_COMMON_MAIN.full_name]),
        ExitData(RegionName.SEABED_SANCTUARY_WEST, [NPCID.MERMAID_W_GUARD.full_name, NPCID.MERMAID_TROUPE_LEADER.full_name]),
        ExitData(RegionName.SEABED_SANCTUARY_EAST, [NPCID.DOLPHIN_NE_PLATFORM.full_name]),
        ExitData(RegionName.MOUNTAIN_HUB_NORTH_SLOPE, [NPCID.MERMAID_QUEEN.full_name]),
    ],
    RegionName.SEABED_SANCTUARY_SOUTH: [
        ExitData(RegionName.SEABED_SANCTUARY_WEST, [NPCID.MERMAID_W_GUARD.full_name]),
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHEAST, [NPCID.ANGELFISH_WITH_SOUL.full_name]),
        ExitData(RegionName.SEABED_HUB, [ItemID.BUBBLEARMOR.full_name]),
    ],
    RegionName.SEABED_SANCTUARY_WEST: [
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHWEST, [NPCID.DOLPHIN_RIDE_CHEST.full_name]),
    ],
    RegionName.SEABED_SANCTUARY_EAST: [
        ExitData(
            RegionName.SEABED_SANCTUARY_SOUTHEAST,
            [NPCID.ANGELFISH_WITH_SOUL.full_name, NPCID.MERMAID_E_GUARD.full_name],
        )
    ],
    RegionName.SEABED_HUB: [
        ExitData(RegionName.ROCKBIRD, [NPCID.MERMAID_STATUE_ROCKBIRD.full_name]),
        ExitData(RegionName.DUREAN, [NPCID.MERMAID_STATUE_DUREAN.full_name]),
        ExitData(RegionName.BLESTER, [NPCID.MERMAID_STATUE_BLESTER.full_name]),
        ExitData(RegionName.GHOST_SHIP, [NPCID.MERMAID_STATUE_GHOST_SHIP.full_name]),
    ],
    RegionName.GHOST_SHIP: [
        ExitData(
            RegionName.SEABED_SECRET_COVE,
            [
                NPCID.MERMAID_W_GUARD.full_name,
                NPCID.DOLPHIN_SLEEPING.full_name,
                ItemID.DREAMROD.full_name,
                ItemID.BIGPEARL.full_name,
            ],
        ),
    ],
    # Act 4 Exits
    RegionName.MOUNTAIN_HUB_NORTH_SLOPE: [
        ExitData(RegionName.LAYNOLE, [ItemID.MUSHROOMSHOES.full_name]),
        ExitData(
            RegionName.LUNE,
            [
                NPCID.GIRL_E_TUNNEL.full_name,
                NPCID.GRANDPA_SE_LAKE.full_name,
                NPCID.GRANDPA_LUNE.full_name,
                ItemID.LUCKYBLADE.full_name,
            ],
        ),
        ExitData(
            RegionName.MOUNTAIN_KING,
            [NPCID.BOY_W_TUNNEL.full_name, NPCID.GRANDPA_SW_TUNNEL.full_name, NPCID.MOUNTAIN_KING.full_name],
            [NPCID.BOY_WITH_GIFT.full_name, NPCID.GRANDPA_NW.full_name],
        ),
        ExitData(
            RegionName.NOME,
            [
                NPCID.GIRL_E_TUNNEL.full_name,
                NPCID.GRANDPA_SE_LAKE.full_name,
                NPCID.MUSHROOM_S_TUNNEL.full_name,
                NPCID.GRANDPA_JAIL.full_name,
                NPCID.MOUNTAIN_KING.full_name,
                NPCID.NOME.full_name,
            ],
        ),
    ],
    RegionName.NOME: [ExitData(RegionName.LEOS_LAB_START, [])],
    # Act 5 Exits
    RegionName.LEOS_LAB_START: [
        ExitData(RegionName.LEOS_LAB_BASEMENT_1_METAL, rule_flag=RuleFlag.CAN_CUT_METAL),
        ExitData(RegionName.LEOS_LAB_MAIN, [NPCID.GREAT_DOOR_MAIN_LAB.full_name]),
        ExitData(
            RegionName.LEOS_LAB_2ND_FLOOR,
            [NPCID.STEPS_TO_2F.full_name, NPCID.GREAT_DOOR_MODEL_TOWNS.full_name],
        ),
        ExitData(RegionName.LEOS_LAB_POWER_PLANT, [NPCID.STEPS_POWER_PLANT.full_name]),
    ],
    RegionName.LEOS_LAB_BASEMENT_1_METAL: [
        ExitData(RegionName.LEOS_LAB_BASEMENT_2, [ItemID.ICEARMOR.full_name]),
    ],
    RegionName.LEOS_LAB_2ND_FLOOR: [
        ExitData(RegionName.LEOS_LAB_MODEL_TOWN_1, [NPCID.MODEL_TOWN1.full_name]),
        ExitData(RegionName.LEOS_LAB_MODEL_TOWN_2, [NPCID.MODEL_TOWN2.full_name]),
        ExitData(RegionName.LEOS_LAB_ATTIC, [NPCID.STEPS_ATTIC.full_name]),
    ],
    RegionName.LEOS_LAB_ATTIC: [
        ExitData(RegionName.MAGRIDD_CASTLE_TOWN, [NPCID.MARIE.full_name]),
    ],
    # Act 6 Exits
    RegionName.MAGRIDD_CASTLE_TOWN: [
        ExitData(RegionName.MAGRIDD_CASTLE_BASEMENT, rule_flag=RuleFlag.CAN_CUT_SPIRIT),
        ExitData(
            RegionName.MAGRIDD_CASTLE_LEFT_TOWER,
            [NPCID.SOLDIER_LEFT_TOWER.full_name, ItemID.PLATINUMCARD.full_name],
        ),
        ExitData(
            RegionName.MAGRIDD_CASTLE_RIGHT_TOWER, [NPCID.SOLDIER_RIGHT_TOWER.full_name, ItemID.VIPCARD.full_name]
        ),
        ExitData(
            RegionName.WORLD_OF_EVIL,
            [NPCID.SOLDIER_CASTLE.full_name, NPCID.KING_MAGRIDD.full_name],
            rule_flag=RuleFlag.HAS_STONES,
        ),
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT: [
        ExitData(RegionName.MAGRIDD_CASTLE_BASEMENT_INVIS, [SoulID.SOUL_REALITY.full_name]),
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER: [
        ExitData(RegionName.MAGRIDD_CASTLE_LEFT_TOWER_INVIS, [SoulID.SOUL_REALITY.full_name]),
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER: [
        ExitData(RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS, [SoulID.SOUL_REALITY.full_name]),
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS: [
        ExitData(
            RegionName.MAGRIDD_CASTLE_LEO,
            [NPCID.DR_LEO.full_name, NPCID.SOLDIER_WITH_LEO.full_name, NPCID.SOLDIER_DOK.full_name],
        )
    ],
    RegionName.MAGRIDD_CASTLE_LEO: [
        # The platinum card soldier blows up, letting you get in without platinum card
        ExitData(RegionName.MAGRIDD_CASTLE_LEFT_TOWER, [NPCID.SOLDIER_LEFT_TOWER.full_name])
    ],
    # Act 7 Exits
    RegionName.WORLD_OF_EVIL: [
        ExitData(
            RegionName.DEATHTOLL,
            [
                ItemID.SOULARMOR.full_name,
                ItemID.SOULBLADE.full_name,
                ItemID.PHOENIX.full_name,
                SoulID.SOUL_MAGICIAN.full_name,
            ],
            [],
            RuleFlag.PHOENIX_CUTSCENE,
        )
    ],
}

exits_for_region_open_mode: dict[str, list[ExitData]] = {
    # Grass Valley west now connects to all Act Hubs
    RegionName.GRASS_VALLEY_WEST: [
        ExitData(RegionName.GRASS_VALLEY_EAST, [NPCID.BRIDGE_GUARD.full_name]),
        ExitData(RegionName.UNDERGROUND_CASTLE_WEST),
        ExitData(RegionName.GREENWOOD),
        ExitData(RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA),
        ExitData(RegionName.MOUNTAIN_HUB_NORTH_SLOPE),
        ExitData(RegionName.LEOS_LAB_START),
        ExitData(RegionName.MAGRIDD_CASTLE_TOWN),
        ExitData(RegionName.WORLD_OF_EVIL, rule_flag=RuleFlag.HAS_STONES),
    ],
}

exits_for_region_open_deathtoll: dict[str, list[ExitData]] = {
    # No longer needs Phoenix/Dancing Grandma cutscene.
    RegionName.WORLD_OF_EVIL: [
        ExitData(
            RegionName.DEATHTOLL,
            [
                ItemID.SOULARMOR.full_name,
                ItemID.SOULBLADE.full_name,
                ItemID.PHOENIX.full_name,
                SoulID.SOUL_MAGICIAN.full_name,
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

    all_locations: list[SoulBlazerLocation] = []

    # Populate each region with locations and exits
    for region in regions.values():
        locations = [
            SoulBlazerLocation(world.player, loc, data, region)
            for loc in locations_for_region[region.name]
            for data in [locations_by_name[loc]]
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
    if len(all_locations) < len(locations_by_name):
        all_location_names = {loc.name for loc in all_locations}
        all_locations_table_names = {*locations_by_name.keys()}
        unplaced = all_locations_table_names - all_location_names
        logging.warning("Soulblazer: Regions do not contain all locations. Something is likely broken with the logic.")
        for loc in unplaced:
            logging.warning(loc)
