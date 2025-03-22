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
        NPCRewardID.EMBLEM_A_TILE.full_name,
        NPCRewardID.GOAT_PEN_CORNER.full_name,
        NPCRewardID.PASS_TILE.full_name,
        NPCRewardID.TILE_IN_CHILDS_SECRET_CAVE.full_name,
        NPCRewardID.RECOVERY_SWORD_CRYSTAL.full_name,
    ],
    RegionName.GRASS_VALLEY_TREASURE_ROOM: [
        NPCRewardID.GRASS_VALLEY_SECRET_ROOM_CRYSTAL.full_name,
        ChestID.GRASS_VALLEY_SECRET_CAVE_LEFT.full_name,
        ChestID.GRASS_VALLEY_SECRET_CAVE_RIGHT.full_name,
    ],
    RegionName.UNDERGROUND_CASTLE_WEST: [
        LairID.OLD_WOMAN.full_name,
        LairID.TOOL_SHOP_OWNER.full_name,
        LairID.TULIP.full_name,
        LairID.BRIDGE_GUARD.full_name,
        LairID.IVY_CHEST_ROOM.full_name,
        LairID.WATER_MILL.full_name,
        NPCRewardID.UNDERGROUND_CASTLE_CRYSTAL.full_name,
        ChestID.UNDERGROUND_CASTLE_HERB.full_name,
        ChestID.UNDERGROUND_CASTLE_12GEM.full_name,
        ChestID.UNDERGROUND_CASTLE_DREAM_ROD.full_name,
    ],
    RegionName.UNDERGROUND_CASTLE_EAST: [
        ChestID.UNDERGROUND_CASTLE_LEOS_BRUSH.full_name,
        LairID.OLD_MAN.full_name,
        LairID.OLD_MAN2.full_name,
        LairID.GOAT_HERB.full_name,
        LairID.LISA.full_name,
        LairID.TULIP2.full_name,
        LairID.ARCHITECT.full_name,
        LairID.IVY2.full_name,
        LairID.TEDDY.full_name,
        LairID.GOAT.full_name,
        LairID.TULIP3.full_name,
        LairID.LEOS_HOUSE.full_name,
    ],
    RegionName.LEOS_PAINTING: [
        LairID.VILLAGE_CHIEF.full_name,
        LairID.IVY.full_name,
        LairID.LONELY_GOAT.full_name,
        LairID.TULIP_PASS.full_name,
        LairID.BOY_CABIN.full_name,
        LairID.BOY_CAVE.full_name,
        LairID.IVY_EMBLEM_A.full_name,
        LairID.IVY_RECOVERY_SWORD.full_name,
        LairID.TULIP4.full_name,
        LairID.GOAT2.full_name,
        ChestID.LEOS_PAINTING_HERB.full_name,
        ChestID.LEOS_PAINTING_TORNADO.full_name,
    ],
    # Act 2 Regions
    RegionName.GREENWOOD: [
        NPCRewardID.REDHOT_MIRROR_BIRD.full_name,
        NPCRewardID.MAGIC_BELL_CRYSTAL.full_name,
        NPCRewardID.WOODSTIN_TRIO.full_name,
        NPCRewardID.GREENWOODS_GUARDIAN.full_name,
        NPCRewardID.GREENWOOD_LEAVES_TILE.full_name,
        NPCRewardID.SHIELD_BRACELET_MOLE.full_name,
        NPCRewardID.PSYCHO_SWORD_SQUIRREL.full_name,
        NPCRewardID.EMBLEM_C_SQUIRREL.full_name,
        NPCRewardID.MOLE_SOUL_OF_LIGHT.full_name,
        ChestID.GREENWOOD_ICE_ARMOR.full_name,
        ChestID.GREENWOOD_TUNNELS.full_name,
    ],
    RegionName.LOST_MARSHES_SOUTH: [
        LairID.BIRD.full_name,
        LairID.DOG.full_name,
        LairID.SQUIRREL_PSYCHO_SWORD.full_name,
        LairID.BIRD2.full_name,
        LairID.MOLE_SOUL_OF_LIGHT.full_name,
        LairID.CROCODILE.full_name,
        LairID.SQUIRREL.full_name,
        LairID.MOLE.full_name,
        LairID.DEER.full_name,
        LairID.DOG2.full_name,
        LairID.DOG4.full_name,
        LairID.DOG5.full_name,
        LairID.CROCODILE2.full_name,
        LairID.SQUIRREL_ICE_ARMOR.full_name,
        LairID.MOLE2.full_name,
        LairID.SQUIRREL3.full_name,
        LairID.BIRD_GREENWOOD_LEAF.full_name,
        LairID.MOLE3.full_name,
        LairID.DEER_MAGIC_BELL.full_name,
        LairID.SQUIRREL2.full_name,
        LairID.BIRD3.full_name,
        NPCRewardID.WATER_SHRINE_CRYSTAL.full_name,
        NPCRewardID.WATER_SHRINE_TILE.full_name,
        NPCRewardID.LIGHT_ARROW_CRYSTAL.full_name,
        NPCRewardID.FIRE_SHRINE_CRYSTAL.full_name,
        ChestID.WATER_SHRINE_1.full_name,
        ChestID.WATER_SHRINE_2_N.full_name,
        ChestID.WATER_SHRINE_2_HERB.full_name,
        ChestID.WATER_SHRINE_3_SE.full_name,
        ChestID.WATER_SHRINE_3_SW.full_name,
        ChestID.FIRE_SHRINE_1.full_name,
        ChestID.FIRE_SHRINE_2_DISAPPEARING.full_name,
        ChestID.FIRE_SHRINE_2_SCORPION.full_name,
        ChestID.FIRE_SHRINE_3_100GEM.full_name,
        ChestID.FIRE_SHRINE_3_60GEM.full_name,
    ],
    RegionName.LOST_MARSHES_NORTH: [
        LairID.MOLE_SHIELD_BRACELET.full_name,
        LairID.DOG3.full_name,
        LairID.SQUIRREL_EMBLEM_C.full_name,
        NPCRewardID.LOST_MARSH_CRYSTAL.full_name,
        ChestID.LIGHT_SHRINE.full_name,
    ],
    RegionName.LIGHT_SHRINE_DARK: [
        LairID.CROCODILE3.full_name,
        LairID.MONMO.full_name,
        LairID.GREENWOODS_GUARDIAN.full_name,
        LairID.BIRD_RED_HOT_MIRROR.full_name,
    ],
    # Act 3 Regions
    RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA: [
        LairID.DOLPHIN2.full_name,
        LairID.MERMAID4.full_name,
        LairID.MERMAID5.full_name,
        LairID.MERMAID6.full_name,
        LairID.MERMAID_BUBBLE_ARMOR.full_name,
        NPCRewardID.MERMAID_QUEEN.full_name,
        ChestID.SOUTHERTA.full_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTH: [
        NPCRewardID.BUBBLE_ARMOR_MERMAID.full_name,
        NPCRewardID.REDHOT_STICK_MERMAID.full_name,
        ChestID.ST_ELLIS_MERMAIDS_TEARS.full_name,
    ],
    RegionName.SEABED_SANCTUARY_WEST: [
        NPCRewardID.LUE.full_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTHWEST: [
        NPCRewardID.MAGIC_FLARE_MERMAID.full_name,
        ChestID.ST_ELLIS_BIG_PEARL.full_name,
    ],
    RegionName.SEABED_SANCTUARY_EAST: [
        NPCRewardID.NORTHEASTERN_MERMAID_HERB.full_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTHEAST: [
        NPCRewardID.ANGELFISH_SOUL_OF_SHIELD.full_name,
    ],
    RegionName.SEABED_HUB: [
        # TODO: make bubble armor requirement for this lair an optional toggle
        LairID.MERMAID_STATUE_ROCKBIRD.full_name,
    ],
    RegionName.ROCKBIRD: [
        LairID.MERMAID9.full_name,
        LairID.MERMAID_TEARS.full_name,
        LairID.MERMAID_MAGIC_FLARE.full_name,
        LairID.ANGELFISH_SOUL_OF_SHIELD.full_name,
        LairID.MERMAID_STATUE_DUREAN.full_name,
        NPCRewardID.ROCKBIRD_CRYSTAL.full_name,
        ChestID.ROCKBIRD_60GEM.full_name,
        ChestID.ROCKBIRD_HERB.full_name,
    ],
    RegionName.DUREAN: [
        LairID.DOLPHIN_PEARL.full_name,
        LairID.LUE.full_name,
        LairID.MERMAID2.full_name,
        LairID.MERMAID_NANA.full_name,
        LairID.DOLPHIN_SAVES_LUE.full_name,
        LairID.MERMAID3.full_name,
        LairID.MERMAID_RED_HOT_STICK.full_name,
        LairID.MERMAID_PEARL.full_name,
        LairID.MERMAID_STATUE_BLESTER.full_name,
        NPCRewardID.SEABED_CRYSTAL_NEAR_DUREAN.full_name,
        ChestID.DUREAN_STRANGE_BOTTLE.full_name,
        ChestID.DUREAN_CRITICAL_SWORD.full_name,
    ],
    RegionName.BLESTER: [
        LairID.ANGELFISH.full_name,
        LairID.ANGELFISH2.full_name,
        LairID.MERMAID.full_name,
        LairID.MERMAID7.full_name,
        LairID.ANGELFISH4.full_name,
        LairID.MERMAID8.full_name,
        LairID.DOLPHIN_SECRET_CAVE.full_name,
        LairID.MERMAID_STATUE_GHOST_SHIP.full_name,
        NPCRewardID.SEABED_CRYSTAL_NEAR_BLESTER.full_name,
    ],
    RegionName.GHOST_SHIP: [
        LairID.ANGELFISH3.full_name,
        LairID.DOLPHIN.full_name,
        LairID.MERMAID_QUEEN.full_name,
        ChestID.SEABED_POWER_BRACELET.full_name,
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
        LairID.GIRL.full_name,
        LairID.GRANDPA.full_name,
        LairID.MUSHROOM.full_name,
        LairID.BOY.full_name,
        LairID.GRANDPA2.full_name,
        LairID.SNAIL_JOCKEY.full_name,
        LairID.BOY_MUSHROOM_SHOES.full_name,
        LairID.GIRL2.full_name,
        NPCRewardID.MOUNTAIN_OF_SOULS_CRYSTAL.full_name,
        NPCRewardID.EMBLEM_E_SNAIL.full_name,
        NPCRewardID.MUSHROOM_SHOES_BOY.full_name,
        ChestID.MOUNTAIN_OF_SOULS_1.full_name,
        ChestID.MOUNTAIN_OF_SOULS_2_L.full_name,
        ChestID.MOUNTAIN_OF_SOULS_2_LL.full_name,
        ChestID.MOUNTAIN_OF_SOULS_2_R.full_name,
        ChestID.MOUNTAIN_OF_SOULS_2_RR.full_name,
    ],
    RegionName.MOUNTAIN_KING: [
        NPCRewardID.MOUNTAIN_KING.full_name,
    ],
    RegionName.NOME: [
        NPCRewardID.NOME.full_name,
    ],
    RegionName.LAYNOLE: [
        LairID.GRANDMA.full_name,
        LairID.MUSHROOM2.full_name,
        LairID.SNAIL_RACER.full_name,
        LairID.SNAIL_RACER2.full_name,
        LairID.GIRL3.full_name,
        LairID.MUSHROOM3.full_name,
        LairID.SNAIL.full_name,
        LairID.GRANDPA3.full_name,
        LairID.GRANDPA4.full_name,
        LairID.GRANDPA_LUNE.full_name,
        LairID.SNAIL2.full_name,
        LairID.GRANDPA5.full_name,
        ChestID.LAYNOLE_LUCKY_BLADE.full_name,
    ],
    RegionName.LUNE: [
        LairID.BOY2.full_name,
        LairID.NOME.full_name,
        LairID.MUSHROOM_EMBLEM_F.full_name,
        LairID.DANCING_GRANDMA.full_name,
        LairID.DANCING_GRANDMA2.full_name,
        LairID.SNAIL_EMBLEM_E.full_name,
        LairID.MOUNTAIN_KING.full_name,
        NPCRewardID.LUNE_CRYSTAL.full_name,
        NPCRewardID.EMBLEM_F_TILE.full_name,
        ChestID.LAYNOLE_HERB.full_name,
        ChestID.LAYNOLE_ROTATOR.full_name,
    ],
    # Act 5 Regions
    RegionName.LEOS_LAB_START: [
        LairID.PLANT.full_name,
        LairID.CAT.full_name,
        LairID.GREAT_DOOR_ZANTETSU_SWORD.full_name,
    ],
    RegionName.LEOS_LAB_MAIN: [
        NPCRewardID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.full_name,
        NPCRewardID.EMBLEM_G_UNDER_CHEST_OF_DRAWERS.full_name,
        NPCRewardID.SPARK_BOMB_MOUSE.full_name,
        NPCRewardID.HERB_PLANT_IN_LEOS_LAB.full_name,
        ChestID.LEOS_LAB_ZANTETSU.full_name,
    ],
    RegionName.LEOS_LAB_2ND_FLOOR: [
        NPCRewardID.LEOS_CAT_DOOR_KEY.full_name,
        NPCRewardID.ACTINIDIA_PLANT.full_name,
        NPCRewardID.GREAT_DOOR_SOUL_OF_DETECTION.full_name,
    ],
    RegionName.LEOS_LAB_ATTIC: [
        NPCRewardID.MARIE.full_name,
        NPCRewardID.CHEST_OF_DRAWERS_HERB.full_name,
    ],
    RegionName.LEOS_LAB_BASEMENT_1_METAL: [
        LairID.PLANT_HERB.full_name,
        LairID.CAT2.full_name,
        LairID.CAT3.full_name,
        LairID.GREAT_DOOR.full_name,
        LairID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.full_name,
    ],
    RegionName.LEOS_LAB_BASEMENT_2: [
        LairID.CAT_DOOR_KEY.full_name,
        LairID.STEPS_UPSTAIRS.full_name,
        LairID.MOUSE.full_name,
        LairID.GREAT_DOOR_MODEL_TOWNS.full_name,
        LairID.MODEL_TOWN1.full_name,
        NPCRewardID.LEOS_LAB_BASEMENT_CRYSTAL.full_name,
    ],
    RegionName.LEOS_LAB_MODEL_TOWN_1: [
        LairID.CHEST_OF_DRAWERS.full_name,
        LairID.PLANT2.full_name,
        LairID.MOUSE2.full_name,
        LairID.MOUSE3.full_name,
        LairID.MOUSE4.full_name,
        LairID.MOUSE_SPARK_BOMB.full_name,
        LairID.GREAT_DOOR_SOUL_OF_DETECTION.full_name,
        LairID.MODEL_TOWN2.full_name,
        LairID.STEPS_MARIE.full_name,
        NPCRewardID.MODEL_TOWN_1_CRYSTAL.full_name,
        ChestID.MODEL_TOWN_1_SE.full_name,
        ChestID.MODEL_TOWN_1_NL.full_name,
        ChestID.MODEL_TOWN_1_NR.full_name,
    ],
    RegionName.LEOS_LAB_MODEL_TOWN_2: [
        LairID.CHEST_OF_DRAWERS2.full_name,
        LairID.PLANT_ACTINIDIA_LEAVES.full_name,
        LairID.MOUSE5.full_name,
        LairID.CAT4.full_name,
        LairID.STAIRS_POWER_PLANT.full_name,
        ChestID.MODEL_TOWN_2_TOP.full_name,
        ChestID.MODEL_TOWN_2_BOT.full_name,
    ],
    RegionName.LEOS_LAB_POWER_PLANT: [
        LairID.DOLL.full_name,
        LairID.MARIE.full_name,
        NPCRewardID.POWER_PLANT_CRYSTAL.full_name,
        ChestID.POWER_PLANT_LIGHT_ARMOR.full_name,
    ],
    # Act 6 Regions
    RegionName.MAGRIDD_CASTLE_TOWN: [
        LairID.SOLDIER.full_name,
        NPCRewardID.HARP_STRING_TILE.full_name,
        ChestID.CASTLE_BASEMENT_1_W.full_name,
        ChestID.CASTLE_BASEMENT_1_SPIRIT_SWORD.full_name,
        NPCRewardID.ELEMENTAL_MAIL_SOLDIER.full_name,
        NPCRewardID.QUEEN_MAGRIDD_VIP_CARD.full_name,
        NPCRewardID.PLATINUM_CARD_SOLDIER.full_name,
        NPCRewardID.MAID_HERB.full_name,
        NPCRewardID.EMBLEM_H_TILE.full_name,
        NPCRewardID.KING_MAGRIDD.full_name,
        NPCRewardID.SOLDIER_SOUL_OF_REALITY.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT: [
        LairID.SOLDIER2.full_name,
        LairID.SINGER_CONCERT_HALL.full_name,
        LairID.SOLDIER3.full_name,
        LairID.SOLDIER4.full_name,
        LairID.SOLDIER5.full_name,
        LairID.SOLDIER6.full_name,
        LairID.SOLDIER_ELEMENTAL_MAIL.full_name,
        LairID.MAID.full_name,
        LairID.SOLDIER_LEFT_TOWER.full_name,
        LairID.SOLDIER_DOK.full_name,
        LairID.SOLDIER_PLATINUM_CARD.full_name,
        LairID.SINGER.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT_INVIS: [
        ChestID.CASTLE_BASEMENT_2_N.full_name,
        ChestID.CASTLE_BASEMENT_2_SW.full_name,
        ChestID.CASTLE_BASEMENT_2_MIDDLE.full_name,
        ChestID.CASTLE_BASEMENT_3.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER: [
        LairID.SOLDIER_SOUL_OF_REALITY.full_name,
        LairID.SOLDIER_WITH_LEO.full_name,
        LairID.SOLDIER_RIGHT_TOWER.full_name,
        LairID.DR_LEO.full_name,
        LairID.SOLDIER7.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER_INVIS: [
        LairID.MAID2.full_name,
        LairID.QUEEN_MAGRIDD.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER: [
        LairID.MAID_HERB.full_name,
        LairID.SOLDIER8.full_name,
        LairID.SOLDIER_CASTLE.full_name,
    ],
    # Everything past the invisible staircase
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS: [
        LairID.SOLDIER9.full_name,
        LairID.SOLDIER10.full_name,
        LairID.SOLDIER11.full_name,
        LairID.KING_MAGRIDD.full_name,
        ChestID.CASTLE_RIGHT_TOWER_2_L.full_name,
        ChestID.CASTLE_RIGHT_TOWER_2_R.full_name,
        ChestID.CASTLE_RIGHT_TOWER_3_TL.full_name,
        ChestID.CASTLE_RIGHT_TOWER_3_BR.full_name,
        NPCRewardID.SUPER_BRACELET_TILE.full_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEO: [
        NPCRewardID.LEO_ON_THE_AIRSHIP_DECK.full_name,
    ],
    # Act 7 Regions
    RegionName.WORLD_OF_EVIL: [
        ChestID.WOE_1_SE.full_name,
        ChestID.WOE_1_SW.full_name,
        ChestID.WOE_1_REDHOT_BALL.full_name,
        ChestID.WOE_2.full_name,
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
        ExitData(RegionName.GREENWOOD, [NPCID.OLD_WOMAN.full_name, NPCID.VILLAGE_CHIEF.full_name]),
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
        ExitData(RegionName.SEABED_SANCTUARY_SOUTH, [NPCID.MERMAID_BUBBLE_ARMOR.full_name]),
        ExitData(RegionName.SEABED_SANCTUARY_WEST, [NPCID.MERMAID_PEARL.full_name, NPCID.MERMAID4.full_name]),
        ExitData(RegionName.SEABED_SANCTUARY_EAST, [NPCID.DOLPHIN2.full_name]),
        ExitData(RegionName.MOUNTAIN_HUB_NORTH_SLOPE, [NPCID.MERMAID_QUEEN.full_name]),
    ],
    RegionName.SEABED_SANCTUARY_SOUTH: [
        ExitData(RegionName.SEABED_SANCTUARY_WEST, [NPCID.MERMAID_PEARL.full_name]),
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHEAST, [NPCID.ANGELFISH_SOUL_OF_SHIELD.full_name]),
        ExitData(RegionName.SEABED_HUB, [ItemID.BUBBLEARMOR.full_name]),
    ],
    RegionName.SEABED_SANCTUARY_WEST: [
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHWEST, [NPCID.DOLPHIN_PEARL.full_name]),
    ],
    RegionName.SEABED_SANCTUARY_EAST: [
        ExitData(
            RegionName.SEABED_SANCTUARY_SOUTHEAST,
            [NPCID.ANGELFISH_SOUL_OF_SHIELD.full_name, NPCID.MERMAID5.full_name],
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
                NPCID.MERMAID_PEARL.full_name,
                NPCID.DOLPHIN_SECRET_CAVE.full_name,
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
                NPCID.GIRL3.full_name,
                NPCID.GRANDPA4.full_name,
                NPCID.GRANDPA_LUNE.full_name,
                ItemID.LUCKYBLADE.full_name,
            ],
        ),
        ExitData(
            RegionName.MOUNTAIN_KING,
            [NPCID.BOY.full_name, NPCID.GRANDPA3.full_name, NPCID.MOUNTAIN_KING.full_name],
            [NPCID.BOY_MUSHROOM_SHOES.full_name, NPCID.GRANDPA.full_name],
        ),
        ExitData(
            RegionName.NOME,
            [
                NPCID.GIRL3.full_name,
                NPCID.GRANDPA4.full_name,
                NPCID.MUSHROOM2.full_name,
                NPCID.GRANDPA5.full_name,
                NPCID.MOUNTAIN_KING.full_name,
                NPCID.NOME.full_name,
            ],
        ),
    ],
    RegionName.NOME: [ExitData(RegionName.LEOS_LAB_START, [])],
    # Act 5 Exits
    RegionName.LEOS_LAB_START: [
        ExitData(RegionName.LEOS_LAB_BASEMENT_1_METAL, rule_flag=RuleFlag.CAN_CUT_METAL),
        ExitData(RegionName.LEOS_LAB_MAIN, [NPCID.GREAT_DOOR_ZANTETSU_SWORD.full_name]),
        ExitData(
            RegionName.LEOS_LAB_2ND_FLOOR,
            [NPCID.STEPS_UPSTAIRS.full_name, NPCID.GREAT_DOOR_MODEL_TOWNS.full_name],
        ),
        ExitData(RegionName.LEOS_LAB_POWER_PLANT, [NPCID.STAIRS_POWER_PLANT.full_name]),
    ],
    RegionName.LEOS_LAB_BASEMENT_1_METAL: [
        ExitData(RegionName.LEOS_LAB_BASEMENT_2, [ItemID.ICEARMOR.full_name]),
    ],
    RegionName.LEOS_LAB_2ND_FLOOR: [
        ExitData(RegionName.LEOS_LAB_MODEL_TOWN_1, [NPCID.MODEL_TOWN1.full_name]),
        ExitData(RegionName.LEOS_LAB_MODEL_TOWN_2, [NPCID.MODEL_TOWN2.full_name]),
        ExitData(RegionName.LEOS_LAB_ATTIC, [NPCID.STEPS_MARIE.full_name]),
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
