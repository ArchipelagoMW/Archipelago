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
        ChestID.TRIAL_ROOM.display_name,
        NPCRewardID.MAGICIAN.display_name,
        NPCRewardID.MAGICIAN_SOUL.display_name,
    ],
    RegionName.GRASS_VALLEY_WEST: [
        NPCRewardID.TOOL_SHOP_OWNER.display_name,
        NPCRewardID.TEDDY.display_name,
        NPCRewardID.VILLAGE_CHIEF.display_name,
    ],
    RegionName.GRASS_VALLEY_EAST: [
        NPCRewardID.EMBLEM_A_TILE.display_name,
        NPCRewardID.GOAT_PEN_CORNER.display_name,
        NPCRewardID.PASS_TILE.display_name,
        NPCRewardID.TILE_IN_CHILDS_SECRET_CAVE.display_name,
        NPCRewardID.RECOVERY_SWORD_CRYSTAL.display_name,
    ],
    RegionName.GRASS_VALLEY_TREASURE_ROOM: [
        NPCRewardID.GRASS_VALLEY_SECRET_ROOM_CRYSTAL.display_name,
        ChestID.GRASS_VALLEY_SECRET_CAVE_LEFT.display_name,
        ChestID.GRASS_VALLEY_SECRET_CAVE_RIGHT.display_name,
    ],
    RegionName.UNDERGROUND_CASTLE_WEST: [
        LairID.OLD_WOMAN.display_name,
        LairID.TOOL_SHOP_OWNER.display_name,
        LairID.TULIP.display_name,
        LairID.BRIDGE_GUARD.display_name,
        LairID.IVY_CHEST_ROOM.display_name,
        LairID.WATER_MILL.display_name,
        NPCRewardID.UNDERGROUND_CASTLE_CRYSTAL.display_name,
        ChestID.UNDERGROUND_CASTLE_HERB.display_name,
        ChestID.UNDERGROUND_CASTLE_12GEM.display_name,
        ChestID.UNDERGROUND_CASTLE_DREAM_ROD.display_name,
    ],
    RegionName.UNDERGROUND_CASTLE_EAST: [
        ChestID.UNDERGROUND_CASTLE_LEOS_BRUSH.display_name,
        LairID.OLD_MAN.display_name,
        LairID.OLD_MAN2.display_name,
        LairID.GOAT_HERB.display_name,
        LairID.LISA.display_name,
        LairID.TULIP2.display_name,
        LairID.ARCHITECT.display_name,
        LairID.IVY2.display_name,
        LairID.TEDDY.display_name,
        LairID.GOAT.display_name,
        LairID.TULIP3.display_name,
        LairID.LEOS_HOUSE.display_name,
    ],
    RegionName.LEOS_PAINTING: [
        LairID.VILLAGE_CHIEF.display_name,
        LairID.IVY.display_name,
        LairID.LONELY_GOAT.display_name,
        LairID.TULIP_PASS.display_name,
        LairID.BOY_CABIN.display_name,
        LairID.BOY_CAVE.display_name,
        LairID.IVY_EMBLEM_A.display_name,
        LairID.IVY_RECOVERY_SWORD.display_name,
        LairID.TULIP4.display_name,
        LairID.GOAT2.display_name,
        ChestID.LEOS_PAINTING_HERB.display_name,
        ChestID.LEOS_PAINTING_TORNADO.display_name,
    ],
    # Act 2 Regions
    RegionName.GREENWOOD: [
        NPCRewardID.REDHOT_MIRROR_BIRD.display_name,
        NPCRewardID.MAGIC_BELL_CRYSTAL.display_name,
        NPCRewardID.WOODSTIN_TRIO.display_name,
        NPCRewardID.GREENWOODS_GUARDIAN.display_name,
        NPCRewardID.GREENWOOD_LEAVES_TILE.display_name,
        NPCRewardID.SHIELD_BRACELET_MOLE.display_name,
        NPCRewardID.PSYCHO_SWORD_SQUIRREL.display_name,
        NPCRewardID.EMBLEM_C_SQUIRREL.display_name,
        NPCRewardID.MOLE_SOUL_OF_LIGHT.display_name,
        ChestID.GREENWOOD_ICE_ARMOR.display_name,
        ChestID.GREENWOOD_TUNNELS.display_name,
    ],
    RegionName.LOST_MARSHES_SOUTH: [
        LairID.BIRD.display_name,
        LairID.DOG.display_name,
        LairID.SQUIRREL_PSYCHO_SWORD.display_name,
        LairID.BIRD2.display_name,
        LairID.MOLE_SOUL_OF_LIGHT.display_name,
        LairID.CROCODILE.display_name,
        LairID.SQUIRREL.display_name,
        LairID.MOLE.display_name,
        LairID.DEER.display_name,
        LairID.DOG2.display_name,
        LairID.DOG4.display_name,
        LairID.DOG5.display_name,
        LairID.CROCODILE2.display_name,
        LairID.SQUIRREL_ICE_ARMOR.display_name,
        LairID.MOLE2.display_name,
        LairID.SQUIRREL3.display_name,
        LairID.BIRD_GREENWOOD_LEAF.display_name,
        LairID.MOLE3.display_name,
        LairID.DEER_MAGIC_BELL.display_name,
        LairID.SQUIRREL2.display_name,
        LairID.BIRD3.display_name,
        NPCRewardID.WATER_SHRINE_CRYSTAL.display_name,
        NPCRewardID.WATER_SHRINE_TILE.display_name,
        NPCRewardID.LIGHT_ARROW_CRYSTAL.display_name,
        NPCRewardID.FIRE_SHRINE_CRYSTAL.display_name,
        ChestID.WATER_SHRINE_1.display_name,
        ChestID.WATER_SHRINE_2_N.display_name,
        ChestID.WATER_SHRINE_2_HERB.display_name,
        ChestID.WATER_SHRINE_3_SE.display_name,
        ChestID.WATER_SHRINE_3_SW.display_name,
        ChestID.FIRE_SHRINE_1.display_name,
        ChestID.FIRE_SHRINE_2_DISAPPEARING.display_name,
        ChestID.FIRE_SHRINE_2_SCORPION.display_name,
        ChestID.FIRE_SHRINE_3_100GEM.display_name,
        ChestID.FIRE_SHRINE_3_60GEM.display_name,
    ],
    RegionName.LOST_MARSHES_NORTH: [
        LairID.MOLE_SHIELD_BRACELET.display_name,
        LairID.DOG3.display_name,
        LairID.SQUIRREL_EMBLEM_C.display_name,
        NPCRewardID.LOST_MARSH_CRYSTAL.display_name,
        ChestID.LIGHT_SHRINE.display_name,
    ],
    RegionName.LIGHT_SHRINE_DARK: [
        LairID.CROCODILE3.display_name,
        LairID.MONMO.display_name,
        LairID.GREENWOODS_GUARDIAN.display_name,
        LairID.BIRD_RED_HOT_MIRROR.display_name,
    ],
    # Act 3 Regions
    RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA: [
        LairID.DOLPHIN2.display_name,
        LairID.MERMAID4.display_name,
        LairID.MERMAID5.display_name,
        LairID.MERMAID6.display_name,
        LairID.MERMAID_BUBBLE_ARMOR.display_name,
        NPCRewardID.MERMAID_QUEEN.display_name,
        ChestID.SOUTHERTA.display_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTH: [
        NPCRewardID.BUBBLE_ARMOR_MERMAID.display_name,
        NPCRewardID.REDHOT_STICK_MERMAID.display_name,
        ChestID.ST_ELLIS_MERMAIDS_TEARS.display_name,
    ],
    RegionName.SEABED_SANCTUARY_WEST: [
        NPCRewardID.LUE.display_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTHWEST: [
        NPCRewardID.MAGIC_FLARE_MERMAID.display_name,
        ChestID.ST_ELLIS_BIG_PEARL.display_name,
    ],
    RegionName.SEABED_SANCTUARY_EAST: [
        NPCRewardID.NORTHEASTERN_MERMAID_HERB.display_name,
    ],
    RegionName.SEABED_SANCTUARY_SOUTHEAST: [
        NPCRewardID.ANGELFISH_SOUL_OF_SHIELD.display_name,
    ],
    RegionName.SEABED_HUB: [
        # TODO: make bubble armor requirement for this lair an optional toggle
        LairID.MERMAID_STATUE_ROCKBIRD.display_name,
    ],
    RegionName.ROCKBIRD: [
        LairID.MERMAID9.display_name,
        LairID.MERMAID_TEARS.display_name,
        LairID.MERMAID_MAGIC_FLARE.display_name,
        LairID.ANGELFISH_SOUL_OF_SHIELD.display_name,
        LairID.MERMAID_STATUE_DUREAN.display_name,
        NPCRewardID.ROCKBIRD_CRYSTAL.display_name,
        ChestID.ROCKBIRD_60GEM.display_name,
        ChestID.ROCKBIRD_HERB.display_name,
    ],
    RegionName.DUREAN: [
        LairID.DOLPHIN_PEARL.display_name,
        LairID.LUE.display_name,
        LairID.MERMAID2.display_name,
        LairID.MERMAID_NANA.display_name,
        LairID.DOLPHIN_SAVES_LUE.display_name,
        LairID.MERMAID3.display_name,
        LairID.MERMAID_RED_HOT_STICK.display_name,
        LairID.MERMAID_PEARL.display_name,
        LairID.MERMAID_STATUE_BLESTER.display_name,
        NPCRewardID.SEABED_CRYSTAL_NEAR_DUREAN.display_name,
        ChestID.DUREAN_STRANGE_BOTTLE.display_name,
        ChestID.DUREAN_CRITICAL_SWORD.display_name,
    ],
    RegionName.BLESTER: [
        LairID.ANGELFISH.display_name,
        LairID.ANGELFISH2.display_name,
        LairID.MERMAID.display_name,
        LairID.MERMAID7.display_name,
        LairID.ANGELFISH4.display_name,
        LairID.MERMAID8.display_name,
        LairID.DOLPHIN_SECRET_CAVE.display_name,
        LairID.MERMAID_STATUE_GHOST_SHIP.display_name,
        NPCRewardID.SEABED_CRYSTAL_NEAR_BLESTER.display_name,
    ],
    RegionName.GHOST_SHIP: [
        LairID.ANGELFISH3.display_name,
        LairID.DOLPHIN.display_name,
        LairID.MERMAID_QUEEN.display_name,
        ChestID.SEABED_POWER_BRACELET.display_name,
        ChestID.GHOST_SHIP.display_name,
    ],
    RegionName.SEABED_SECRET_COVE: [
        ChestID.SEABED_SECRET_TL.display_name,
        ChestID.SEABED_SECRET_TR.display_name,
        ChestID.SEABED_SECRET_BL.display_name,
        ChestID.SEABED_SECRET_BR.display_name,
    ],
    # Act 4 Regions
    RegionName.MOUNTAIN_HUB_NORTH_SLOPE: [
        LairID.GIRL.display_name,
        LairID.GRANDPA.display_name,
        LairID.MUSHROOM.display_name,
        LairID.BOY.display_name,
        LairID.GRANDPA2.display_name,
        LairID.SNAIL_JOCKEY.display_name,
        LairID.BOY_MUSHROOM_SHOES.display_name,
        LairID.GIRL2.display_name,
        NPCRewardID.MOUNTAIN_OF_SOULS_CRYSTAL.display_name,
        NPCRewardID.EMBLEM_E_SNAIL.display_name,
        NPCRewardID.MUSHROOM_SHOES_BOY.display_name,
        ChestID.MOUNTAIN_OF_SOULS_1.display_name,
        ChestID.MOUNTAIN_OF_SOULS_2_L.display_name,
        ChestID.MOUNTAIN_OF_SOULS_2_LL.display_name,
        ChestID.MOUNTAIN_OF_SOULS_2_R.display_name,
        ChestID.MOUNTAIN_OF_SOULS_2_RR.display_name,
    ],
    RegionName.MOUNTAIN_KING: [
        NPCRewardID.MOUNTAIN_KING.display_name,
    ],
    RegionName.NOME: [
        NPCRewardID.NOME.display_name,
    ],
    RegionName.LAYNOLE: [
        LairID.GRANDMA.display_name,
        LairID.MUSHROOM2.display_name,
        LairID.SNAIL_RACER.display_name,
        LairID.SNAIL_RACER2.display_name,
        LairID.GIRL3.display_name,
        LairID.MUSHROOM3.display_name,
        LairID.SNAIL.display_name,
        LairID.GRANDPA3.display_name,
        LairID.GRANDPA4.display_name,
        LairID.GRANDPA_LUNE.display_name,
        LairID.SNAIL2.display_name,
        LairID.GRANDPA5.display_name,
        ChestID.LAYNOLE_LUCKY_BLADE.display_name,
    ],
    RegionName.LUNE: [
        LairID.BOY2.display_name,
        LairID.NOME.display_name,
        LairID.MUSHROOM_EMBLEM_F.display_name,
        LairID.DANCING_GRANDMA.display_name,
        LairID.DANCING_GRANDMA2.display_name,
        LairID.SNAIL_EMBLEM_E.display_name,
        LairID.MOUNTAIN_KING.display_name,
        NPCRewardID.LUNE_CRYSTAL.display_name,
        NPCRewardID.EMBLEM_F_TILE.display_name,
        ChestID.LAYNOLE_HERB.display_name,
        ChestID.LAYNOLE_ROTATOR.display_name,
    ],
    # Act 5 Regions
    RegionName.LEOS_LAB_START: [
        LairID.PLANT.display_name,
        LairID.CAT.display_name,
        LairID.GREAT_DOOR_ZANTETSU_SWORD.display_name,
    ],
    RegionName.LEOS_LAB_MAIN: [
        NPCRewardID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.display_name,
        NPCRewardID.EMBLEM_G_UNDER_CHEST_OF_DRAWERS.display_name,
        NPCRewardID.SPARK_BOMB_MOUSE.display_name,
        NPCRewardID.HERB_PLANT_IN_LEOS_LAB.display_name,
        ChestID.LEOS_LAB_ZANTETSU.display_name,
    ],
    RegionName.LEOS_LAB_2ND_FLOOR: [
        NPCRewardID.LEOS_CAT_DOOR_KEY.display_name,
        NPCRewardID.ACTINIDIA_PLANT.display_name,
        NPCRewardID.GREAT_DOOR_SOUL_OF_DETECTION.display_name,
    ],
    RegionName.LEOS_LAB_ATTIC: [
        NPCRewardID.MARIE.display_name,
        NPCRewardID.CHEST_OF_DRAWERS_HERB.display_name,
    ],
    RegionName.LEOS_LAB_BASEMENT_1_METAL: [
        LairID.PLANT_HERB.display_name,
        LairID.CAT2.display_name,
        LairID.CAT3.display_name,
        LairID.GREAT_DOOR.display_name,
        LairID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.display_name,
    ],
    RegionName.LEOS_LAB_BASEMENT_2: [
        LairID.CAT_DOOR_KEY.display_name,
        LairID.STEPS_UPSTAIRS.display_name,
        LairID.MOUSE.display_name,
        LairID.GREAT_DOOR_MODEL_TOWNS.display_name,
        LairID.MODEL_TOWN1.display_name,
        NPCRewardID.LEOS_LAB_BASEMENT_CRYSTAL.display_name,
    ],
    RegionName.LEOS_LAB_MODEL_TOWN_1: [
        LairID.CHEST_OF_DRAWERS.display_name,
        LairID.PLANT2.display_name,
        LairID.MOUSE2.display_name,
        LairID.MOUSE3.display_name,
        LairID.MOUSE4.display_name,
        LairID.MOUSE_SPARK_BOMB.display_name,
        LairID.GREAT_DOOR_SOUL_OF_DETECTION.display_name,
        LairID.MODEL_TOWN2.display_name,
        LairID.STEPS_MARIE.display_name,
        NPCRewardID.MODEL_TOWN_1_CRYSTAL.display_name,
        ChestID.MODEL_TOWN_1_SE.display_name,
        ChestID.MODEL_TOWN_1_NL.display_name,
        ChestID.MODEL_TOWN_1_NR.display_name,
    ],
    RegionName.LEOS_LAB_MODEL_TOWN_2: [
        LairID.CHEST_OF_DRAWERS2.display_name,
        LairID.PLANT_ACTINIDIA_LEAVES.display_name,
        LairID.MOUSE5.display_name,
        LairID.CAT4.display_name,
        LairID.STAIRS_POWER_PLANT.display_name,
        ChestID.MODEL_TOWN_2_TOP.display_name,
        ChestID.MODEL_TOWN_2_BOT.display_name,
    ],
    RegionName.LEOS_LAB_POWER_PLANT: [
        LairID.DOLL.display_name,
        LairID.MARIE.display_name,
        NPCRewardID.POWER_PLANT_CRYSTAL.display_name,
        ChestID.POWER_PLANT_LIGHT_ARMOR.display_name,
    ],
    # Act 6 Regions
    RegionName.MAGRIDD_CASTLE_TOWN: [
        LairID.SOLDIER.display_name,
        NPCRewardID.HARP_STRING_TILE.display_name,
        ChestID.CASTLE_BASEMENT_1_W.display_name,
        ChestID.CASTLE_BASEMENT_1_SPIRIT_SWORD.display_name,
        NPCRewardID.ELEMENTAL_MAIL_SOLDIER.display_name,
        NPCRewardID.QUEEN_MAGRIDD_VIP_CARD.display_name,
        NPCRewardID.PLATINUM_CARD_SOLDIER.display_name,
        NPCRewardID.MAID_HERB.display_name,
        NPCRewardID.EMBLEM_H_TILE.display_name,
        NPCRewardID.KING_MAGRIDD.display_name,
        NPCRewardID.SOLDIER_SOUL_OF_REALITY.display_name,
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT: [
        LairID.SOLDIER2.display_name,
        LairID.SINGER_CONCERT_HALL.display_name,
        LairID.SOLDIER3.display_name,
        LairID.SOLDIER4.display_name,
        LairID.SOLDIER5.display_name,
        LairID.SOLDIER6.display_name,
        LairID.SOLDIER_ELEMENTAL_MAIL.display_name,
        LairID.MAID.display_name,
        LairID.SOLDIER_LEFT_TOWER.display_name,
        LairID.SOLDIER_DOK.display_name,
        LairID.SOLDIER_PLATINUM_CARD.display_name,
        LairID.SINGER.display_name,
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT_INVIS: [
        ChestID.CASTLE_BASEMENT_2_N.display_name,
        ChestID.CASTLE_BASEMENT_2_SW.display_name,
        ChestID.CASTLE_BASEMENT_2_MIDDLE.display_name,
        ChestID.CASTLE_BASEMENT_3.display_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER: [
        LairID.SOLDIER_SOUL_OF_REALITY.display_name,
        LairID.SOLDIER_WITH_LEO.display_name,
        LairID.SOLDIER_RIGHT_TOWER.display_name,
        LairID.DR_LEO.display_name,
        LairID.SOLDIER7.display_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER_INVIS: [
        LairID.MAID2.display_name,
        LairID.QUEEN_MAGRIDD.display_name,
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER: [
        LairID.MAID_HERB.display_name,
        LairID.SOLDIER8.display_name,
        LairID.SOLDIER_CASTLE.display_name,
    ],
    # Everything past the invisible staircase
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS: [
        LairID.SOLDIER9.display_name,
        LairID.SOLDIER10.display_name,
        LairID.SOLDIER11.display_name,
        LairID.KING_MAGRIDD.display_name,
        ChestID.CASTLE_RIGHT_TOWER_2_L.display_name,
        ChestID.CASTLE_RIGHT_TOWER_2_R.display_name,
        ChestID.CASTLE_RIGHT_TOWER_3_TL.display_name,
        ChestID.CASTLE_RIGHT_TOWER_3_BR.display_name,
        NPCRewardID.SUPER_BRACELET_TILE.display_name,
    ],
    RegionName.MAGRIDD_CASTLE_LEO: [
        NPCRewardID.LEO_ON_THE_AIRSHIP_DECK.display_name,
    ],
    # Act 7 Regions
    RegionName.WORLD_OF_EVIL: [
        ChestID.WOE_1_SE.display_name,
        ChestID.WOE_1_SW.display_name,
        ChestID.WOE_1_REDHOT_BALL.display_name,
        ChestID.WOE_2.display_name,
        ChestID.DAZZLING_SPACE_SE.display_name,
        ChestID.DAZZLING_SPACE_SW.display_name,
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
        ExitData(RegionName.GRASS_VALLEY_EAST, [NPCID.BRIDGE_GUARD.display_name]),
        ExitData(RegionName.UNDERGROUND_CASTLE_WEST),
        ExitData(RegionName.GREENWOOD, [NPCID.OLD_WOMAN.display_name, NPCID.VILLAGE_CHIEF.display_name]),
    ],
    RegionName.GRASS_VALLEY_EAST: [
        ExitData(RegionName.GRASS_VALLEY_TREASURE_ROOM, [NPCID.IVY_CHEST_ROOM.display_name]),
        ExitData(
            RegionName.LEOS_PAINTING,
            [NPCID.ARCHITECT.display_name, NPCID.LEOS_HOUSE.display_name, ItemID.LEOSBRUSH.display_name],
        ),
    ],
    RegionName.UNDERGROUND_CASTLE_WEST: [
        ExitData(RegionName.UNDERGROUND_CASTLE_EAST, [NPCID.BRIDGE_GUARD.display_name, NPCID.WATER_MILL.display_name])
    ],
    # Act 2 Exits
    RegionName.GREENWOOD: [
        ExitData(RegionName.LOST_MARSHES_SOUTH),
        ExitData(RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA, [NPCID.GREENWOODS_GUARDIAN.display_name]),
    ],
    RegionName.LOST_MARSHES_SOUTH: [
        ExitData(RegionName.LOST_MARSHES_NORTH, [ItemID.TURBOSLEAVES.display_name]),
    ],
    RegionName.LOST_MARSHES_NORTH: [
        ExitData(RegionName.LIGHT_SHRINE_DARK, [SoulID.SOUL_LIGHT.display_name]),
    ],
    # Act 3 Exits
    RegionName.SEABED_SANCTUARY_HUB_SOUTHERTA: [
        ExitData(RegionName.SEABED_SANCTUARY_SOUTH, [NPCID.MERMAID_BUBBLE_ARMOR.display_name]),
        ExitData(RegionName.SEABED_SANCTUARY_WEST, [NPCID.MERMAID_PEARL.display_name, NPCID.MERMAID4.display_name]),
        ExitData(RegionName.SEABED_SANCTUARY_EAST, [NPCID.DOLPHIN2.display_name]),
        ExitData(RegionName.MOUNTAIN_HUB_NORTH_SLOPE, [NPCID.MERMAID_QUEEN.display_name]),
    ],
    RegionName.SEABED_SANCTUARY_SOUTH: [
        ExitData(RegionName.SEABED_SANCTUARY_WEST, [NPCID.MERMAID_PEARL.display_name]),
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHEAST, [NPCID.ANGELFISH_SOUL_OF_SHIELD.display_name]),
        ExitData(RegionName.SEABED_HUB, [ItemID.BUBBLEARMOR.display_name]),
    ],
    RegionName.SEABED_SANCTUARY_WEST: [
        ExitData(RegionName.SEABED_SANCTUARY_SOUTHWEST, [NPCID.DOLPHIN_PEARL.display_name]),
    ],
    RegionName.SEABED_SANCTUARY_EAST: [
        ExitData(
            RegionName.SEABED_SANCTUARY_SOUTHEAST,
            [NPCID.ANGELFISH_SOUL_OF_SHIELD.display_name, NPCID.MERMAID5.display_name],
        )
    ],
    RegionName.SEABED_HUB: [
        ExitData(RegionName.ROCKBIRD, [NPCID.MERMAID_STATUE_ROCKBIRD.display_name]),
        ExitData(RegionName.DUREAN, [NPCID.MERMAID_STATUE_DUREAN.display_name]),
        ExitData(RegionName.BLESTER, [NPCID.MERMAID_STATUE_BLESTER.display_name]),
        ExitData(RegionName.GHOST_SHIP, [NPCID.MERMAID_STATUE_GHOST_SHIP.display_name]),
    ],
    RegionName.GHOST_SHIP: [
        ExitData(
            RegionName.SEABED_SECRET_COVE,
            [
                NPCID.MERMAID_PEARL.display_name,
                NPCID.DOLPHIN_SECRET_CAVE.display_name,
                ItemID.DREAMROD.display_name,
                ItemID.BIGPEARL.display_name,
            ],
        ),
    ],
    # Act 4 Exits
    RegionName.MOUNTAIN_HUB_NORTH_SLOPE: [
        ExitData(RegionName.LAYNOLE, [ItemID.MUSHROOMSHOES.display_name]),
        ExitData(
            RegionName.LUNE,
            [
                NPCID.GIRL3.display_name,
                NPCID.GRANDPA4.display_name,
                NPCID.GRANDPA_LUNE.display_name,
                ItemID.LUCKYBLADE.display_name,
            ],
        ),
        ExitData(
            RegionName.MOUNTAIN_KING,
            [NPCID.BOY.display_name, NPCID.GRANDPA3.display_name, NPCID.MOUNTAIN_KING.display_name],
            [NPCID.BOY_MUSHROOM_SHOES.display_name, NPCID.GRANDPA.display_name],
        ),
        ExitData(
            RegionName.NOME,
            [
                NPCID.GIRL3.display_name,
                NPCID.GRANDPA4.display_name,
                NPCID.MUSHROOM2.display_name,
                NPCID.GRANDPA5.display_name,
                NPCID.MOUNTAIN_KING.display_name,
                NPCID.NOME.display_name,
            ],
        ),
    ],
    RegionName.NOME: [ExitData(RegionName.LEOS_LAB_START, [])],
    # Act 5 Exits
    RegionName.LEOS_LAB_START: [
        ExitData(RegionName.LEOS_LAB_BASEMENT_1_METAL, rule_flag=RuleFlag.CAN_CUT_METAL),
        ExitData(RegionName.LEOS_LAB_MAIN, [NPCID.GREAT_DOOR_ZANTETSU_SWORD.display_name]),
        ExitData(
            RegionName.LEOS_LAB_2ND_FLOOR,
            [NPCID.STEPS_UPSTAIRS.display_name, NPCID.GREAT_DOOR_MODEL_TOWNS.display_name],
        ),
        ExitData(RegionName.LEOS_LAB_POWER_PLANT, [NPCID.STAIRS_POWER_PLANT.display_name]),
    ],
    RegionName.LEOS_LAB_BASEMENT_1_METAL: [
        ExitData(RegionName.LEOS_LAB_BASEMENT_2, [ItemID.ICEARMOR.display_name]),
    ],
    RegionName.LEOS_LAB_2ND_FLOOR: [
        ExitData(RegionName.LEOS_LAB_MODEL_TOWN_1, [NPCID.MODEL_TOWN1.display_name]),
        ExitData(RegionName.LEOS_LAB_MODEL_TOWN_2, [NPCID.MODEL_TOWN2.display_name]),
        ExitData(RegionName.LEOS_LAB_ATTIC, [NPCID.STEPS_MARIE.display_name]),
    ],
    RegionName.LEOS_LAB_ATTIC: [
        ExitData(RegionName.MAGRIDD_CASTLE_TOWN, [NPCID.MARIE.display_name]),
    ],
    # Act 6 Exits
    RegionName.MAGRIDD_CASTLE_TOWN: [
        ExitData(RegionName.MAGRIDD_CASTLE_BASEMENT, rule_flag=RuleFlag.CAN_CUT_SPIRIT),
        ExitData(
            RegionName.MAGRIDD_CASTLE_LEFT_TOWER,
            [NPCID.SOLDIER_LEFT_TOWER.display_name, ItemID.PLATINUMCARD.display_name],
        ),
        ExitData(
            RegionName.MAGRIDD_CASTLE_RIGHT_TOWER, [NPCID.SOLDIER_RIGHT_TOWER.display_name, ItemID.VIPCARD.display_name]
        ),
        ExitData(
            RegionName.WORLD_OF_EVIL,
            [NPCID.SOLDIER_CASTLE.display_name, NPCID.KING_MAGRIDD.display_name],
            rule_flag=RuleFlag.HAS_STONES,
        ),
    ],
    RegionName.MAGRIDD_CASTLE_BASEMENT: [
        ExitData(RegionName.MAGRIDD_CASTLE_BASEMENT_INVIS, [SoulID.SOUL_REALITY.display_name]),
    ],
    RegionName.MAGRIDD_CASTLE_LEFT_TOWER: [
        ExitData(RegionName.MAGRIDD_CASTLE_LEFT_TOWER_INVIS, [SoulID.SOUL_REALITY.display_name]),
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER: [
        ExitData(RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS, [SoulID.SOUL_REALITY.display_name]),
    ],
    RegionName.MAGRIDD_CASTLE_RIGHT_TOWER_INVIS: [
        ExitData(
            RegionName.MAGRIDD_CASTLE_LEO,
            [NPCID.DR_LEO.display_name, NPCID.SOLDIER_WITH_LEO.display_name, NPCID.SOLDIER_DOK.display_name],
        )
    ],
    RegionName.MAGRIDD_CASTLE_LEO: [
        # The platinum card soldier blows up, letting you get in without platinum card
        ExitData(RegionName.MAGRIDD_CASTLE_LEFT_TOWER, [NPCID.SOLDIER_LEFT_TOWER.display_name])
    ],
    # Act 7 Exits
    RegionName.WORLD_OF_EVIL: [
        ExitData(
            RegionName.DEATHTOLL,
            [
                ItemID.SOULARMOR.display_name,
                ItemID.SOULBLADE.display_name,
                ItemID.PHOENIX.display_name,
                SoulID.SOUL_MAGICIAN.display_name,
            ],
            [],
            RuleFlag.PHOENIX_CUTSCENE,
        )
    ],
}

exits_for_region_open_mode: dict[str, list[ExitData]] = {
    # Grass Valley west now connects to all Act Hubs
    RegionName.GRASS_VALLEY_WEST: [
        ExitData(RegionName.GRASS_VALLEY_EAST, [NPCID.BRIDGE_GUARD.display_name]),
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
                ItemID.SOULARMOR.display_name,
                ItemID.SOULBLADE.display_name,
                ItemID.PHOENIX.display_name,
                SoulID.SOUL_MAGICIAN.display_name,
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
