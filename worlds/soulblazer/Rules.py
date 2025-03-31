from typing import Callable

from BaseClasses import CollectionState
from .Data.Enums import RuleFlag, ItemID, SoulID, LairID, ChestID, NPCRewardID, NPCID
from .Items import castable_magic_names, sword_names, emblem_names, redhot_names

# if TYPE_CHECKING:
#    from . import SoulBlazerWorld

metal_cutting_swords = [ItemID.ZANTETSUSWORD.full_name, ItemID.SOULBLADE.full_name]
spirit_cutting_swords = [ItemID.SPIRITSWORD.full_name, ItemID.SOULBLADE.full_name]
thunder_items = [ItemID.THUNDERRING.full_name, *metal_cutting_swords]


def no_requirement(state: CollectionState, player: int | None = None) -> bool:
    return True


def can_cut_metal(state: CollectionState, player: int) -> bool:
    return state.has_any(metal_cutting_swords, player)


def can_cut_spirit(state: CollectionState, player: int) -> bool:
    return state.has_any(spirit_cutting_swords, player)


def has_thunder(state: CollectionState, player: int) -> bool:
    return state.has_any(thunder_items, player)


def has_magic(state: CollectionState, player: int) -> bool:
    return state.has(SoulID.SOUL_MAGICIAN.full_name, player) and state.has_any(castable_magic_names, player)


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has_any(sword_names, player)


def has_stones(state: CollectionState, player: int) -> bool:
    count: int = state.multiworld.worlds[player].options.stones_count.value
    return state.has_group("stones", player, count)


def has_phoenix_cutscene(state: CollectionState, player: int) -> bool:
    return state.can_reach_location(NPCRewardID.MOUNTAIN_KING.full_name, player)


rule_for_flag = {
    RuleFlag.NONE: no_requirement,
    RuleFlag.CAN_CUT_METAL: can_cut_metal,
    RuleFlag.CAN_CUT_SPIRIT: can_cut_spirit,
    RuleFlag.HAS_THUNDER: has_thunder,
    RuleFlag.HAS_MAGIC: has_magic,
    RuleFlag.HAS_SWORD: has_sword,
    RuleFlag.HAS_STONES: has_stones,
    RuleFlag.PHOENIX_CUTSCENE: has_phoenix_cutscene,
}

# Many locations depend on one or two NPC releases so rather than create regions to hold one location,
# we put these location-specific dependencies here.
location_dependencies: dict[str, list[str]] = {
    # Act 1 - Grass Valley
    NPCRewardID.TOOL_SHOP_OWNER.full_name: [NPCID.TOOL_SHOP_OWNER.full_name],
    NPCRewardID.GRASS_VALLEY_SE_CLIFF_TILE.full_name: [NPCID.IVY_SE.full_name, NPCID.IVY_CLIFF_TILE.full_name],
    NPCRewardID.GOAT_PEN_CORNER.full_name: [NPCID.GOAT_PEN.full_name],
    NPCRewardID.TEDDY.full_name: [NPCID.TOOL_SHOP_OWNER.full_name, NPCID.TEDDY.full_name],
    NPCRewardID.UNDER_TULIP_TILE.full_name: [NPCID.IVY_SE.full_name, NPCID.TULIP_SLEEPING_PUSH.full_name],
    NPCRewardID.HIDEOUT_CLIFF_TILE.full_name: [NPCID.BOY_CAVE.full_name, ItemID.APASS.full_name],
    NPCRewardID.HIDEOUT_CLIFF_CRYSTAL.full_name: [
        NPCID.IVY_HIDEOUT_CRYSTAL.full_name,
        NPCID.BOY_CAVE.full_name,
        ItemID.APASS.full_name,
    ],
    NPCRewardID.VILLAGE_CHIEF.full_name: [NPCID.VILLAGE_CHIEF.full_name, NPCID.OLD_WOMAN_CHIEFS_HOUSE.full_name],
    LairID.LONELY_OLD_MAN.full_name: [NPCID.LISA.full_name, ItemID.DREAMROD.full_name],
    ChestID.UNDERGROUND_CASTLE_CENTER.full_name: [NPCID.LISA.full_name, ItemID.DREAMROD.full_name],
    # Act 2 - Greenwood
    NPCRewardID.SHY_BIRD.full_name: [NPCID.SHY_BIRD.full_name],
    NPCRewardID.MASTER_CRYSTAL.full_name: [
        *emblem_names,
        NPCID.DEER_MASTER_CRYSTAL.full_name,
        NPCID.CROCODILE_W.full_name,
    ],
    NPCRewardID.WOODSTIN_TRIO.full_name: [
        NPCID.DEER_WOODSTIN.full_name,
        NPCID.SQUIRREL_WOODSTIN.full_name,
        NPCID.DOG_WOODSTIN.full_name,
    ],
    NPCRewardID.TURBOS_REMAINS_TILE.full_name: [
        NPCID.MOLE_WITH_SOUL.full_name,
        NPCID.CROCODILE_CENTER.full_name,
        NPCID.CROCODILE_GRAVEYARD.full_name,
        NPCID.BIRD_SLEEPING_TURBO.full_name,
        ItemID.DREAMROD.full_name,
    ],
    NPCRewardID.MOLES_REWARD.full_name: [
        NPCID.MOLE_HOLE_TO_STUMP.full_name,
        NPCID.MOLE_WITH_GIFT.full_name,
        ItemID.MOLESRIBBON.full_name,
    ],
    NPCRewardID.HUNGRY_SQUIRREL.full_name: [
        NPCID.SQUIRREL_HUNGRY.full_name,
        ItemID.DELICIOUSSEEDS.full_name,
    ],
    NPCRewardID.NOT_HUNGRY_SQUIRREL.full_name: [
        NPCID.SQUIRREL_NOT_HUNGRY.full_name,
        NPCID.SQUIRREL_HUNGRY.full_name,
    ],
    NPCRewardID.GREENWOODS_GUARDIAN.full_name: [NPCID.GREENWOODS_GUARDIAN.full_name],
    NPCRewardID.MOLE_SOUL.full_name: [NPCID.MOLE_WITH_SOUL.full_name],
    ChestID.GREENWOOD_DREAM.full_name: [
        NPCID.MOLE_HOLE_TO_STUMP.full_name,
        NPCID.SQUIRREL_SLEEPING_STUMP.full_name,
        ItemID.DREAMROD.full_name,
    ],
    ChestID.GREENWOOD_TUNNELS.full_name: [NPCID.MONMO.full_name, NPCID.MOLE_HOLE_FOR_BLIND_MOLE.full_name],
    # Act 3 - St Elles
    NPCRewardID.NORTHEAST_MERMAID.full_name: [NPCID.MERMAID_NE_HOUSE.full_name, NPCID.DOLPHIN_NE_PLATFORM.full_name],
    NPCRewardID.COMMON_HOUSE_W_ROOM_MERMAID.full_name: [
        NPCID.MERMAID_COMMON_W_ITEM.full_name,
        NPCID.MERMAID_COMMON_MAIN.full_name,
    ],
    NPCRewardID.COMMON_HOUSE_N_MERMAID.full_name: [NPCID.MERMAID_COMMON_N_ITEM.full_name],
    NPCRewardID.LUE.full_name: [
        NPCID.LUE.full_name,
        NPCID.DOLPHIN_SAVES_LUE.full_name,
        NPCID.MERMAID_W_GUARD.full_name,
    ],
    # Logical mermaids tears. TODO: move to separate list for optional logic toggle
    NPCRewardID.MERMAID_QUEEN.full_name: [NPCID.MERMAID_QUEEN.full_name],
    NPCRewardID.ANGELFISH_SOUL.full_name: [NPCID.ANGELFISH_WITH_SOUL.full_name],
    LairID.MERMAID_ATTENDANT_L.full_name: [ItemID.MERMAIDSTEARS.full_name],
    LairID.MERMAID_STATUE_BLESTER.full_name: [ItemID.MERMAIDSTEARS.full_name],
    ChestID.DUREAN_LAVA_RIVER.full_name: [ItemID.MERMAIDSTEARS.full_name],
    # Act 4 - Mountain of Souls
    NPCRewardID.MOUNTAIN_KING.full_name: [
        NPCID.DANCING_GRANDMA_R.full_name,
        NPCID.DANCING_GRANDMA_L.full_name,
        *redhot_names,
    ],
    NPCRewardID.BOY_WITH_GIFT.full_name: [NPCID.BOY_WITH_GIFT.full_name],
    NPCRewardID.SECRET_SNAIL.full_name: [NPCID.SNAIL_SECRET_ROOM.full_name],
    # Also includes path from lune to sleeping mushroom for the two locations locked behind mushroom's dream.
    NPCRewardID.MUSHROOMS_DREAM_TILE.full_name: [
        NPCID.SLEEPING_MUSHROOM.full_name,
        NPCID.GRANDPA_JAIL.full_name,
        NPCID.MUSHROOM_S_TUNNEL.full_name,
        ItemID.DREAMROD.full_name,
    ],
    LairID.SNAIL_SECRET_ROOM.full_name: [
        NPCID.SLEEPING_MUSHROOM.full_name,
        NPCID.GRANDPA_JAIL.full_name,
        NPCID.MUSHROOM_S_TUNNEL.full_name,
        ItemID.DREAMROD.full_name,
    ],
    # Act 5 - Leo's Lab
    NPCRewardID.UNDER_CHEST_OF_DRAWERS_TILE.full_name: [
        NPCID.CHEST_OF_DRAWERS_LOCKED_RM.full_name,
        NPCID.GREAT_DOOR_LOCKED.full_name,
        ItemID.DOORKEY.full_name,
    ],
    NPCRewardID.LOCKED_ROOM_CHEST_OF_DRAWERS.full_name: [
        NPCID.CHEST_OF_DRAWERS_LOCKED_RM.full_name,
        NPCID.GREAT_DOOR_LOCKED.full_name,
        ItemID.DOORKEY.full_name,
    ],
    NPCRewardID.MOUSEHOLE_PLANT.full_name: [
        NPCID.PLANT_MOUSEHOLE.full_name,
        NPCID.MOUSE_OUTSIDE_HOLE.full_name,
        NPCID.CAT_STALKING_1.full_name,
        NPCID.CAT_STALKING_2.full_name,
        ItemID.ACTINIDIALEAVES.full_name,
    ],
    NPCRewardID.MOUSE_WITH_GIFT.full_name: [
        NPCID.MOUSE_WITH_GIFT.full_name,
        NPCID.MOUSE_OUTSIDE_HOLE.full_name,
        NPCID.CAT_STALKING_1.full_name,
        NPCID.CAT_STALKING_2.full_name,
        ItemID.ACTINIDIALEAVES.full_name,
    ],
    NPCRewardID.SLEEPING_CAT.full_name: [NPCID.CAT_SLEEPING.full_name, ItemID.DREAMROD.full_name],
    NPCRewardID.ACTINIDIA_PLANT.full_name: [NPCID.PLANT_ACTINIDIA.full_name],
    NPCRewardID.ATTIC_CHEST_OF_DRAWERS.full_name: [NPCID.CHEST_OF_DRAWERS_ATTIC.full_name],
    NPCRewardID.MARIE.full_name: [NPCID.MARIE.full_name],
    # Potentially optional icearmor requirement.
    NPCRewardID.POWER_PLANT_CRYSTAL.full_name: [ItemID.ICEARMOR.full_name],
    NPCRewardID.GREAT_DOOR_SOUL.full_name: [NPCID.GREAT_DOOR_WITH_SOUL.full_name],
    LairID.DOLL_CHAPEL.full_name: [ItemID.ICEARMOR.full_name],
    LairID.MARIE.full_name: [ItemID.ICEARMOR.full_name],
    # Act 6 - Magridd Castle
    NPCRewardID.SLEEPING_SOLDIER.full_name: [
        NPCID.SOLDIER_SLEEPING.full_name,
        ItemID.DREAMROD.full_name,
    ],
    NPCRewardID.QUEEN_MAGRIDD_TILE.full_name: [
        NPCID.DR_LEO.full_name,
        NPCID.SOLDIER_WITH_LEO.full_name,
        NPCID.SOLDIER_DOK.full_name,
        NPCID.QUEEN_MAGRIDD.full_name,
    ],
    NPCRewardID.QUEEN_MAGRIDD_ITEM.full_name: [NPCID.QUEEN_MAGRIDD.full_name],
    NPCRewardID.UNDER_SOLDIER_TILE.full_name: [
        NPCID.SOLDIER_CONCERT_ITEM.full_name,
        NPCID.SINGER_CONCERT_HALL.full_name,
        ItemID.HARPSTRING.full_name,
    ],
    NPCRewardID.MAID_AT_BAR.full_name: [NPCID.MAID_BAR.full_name],  # anything else?
    NPCRewardID.CASTLE_GROUNDS_TILE.full_name: [NPCID.SOLDIER_CASTLE.full_name],
    NPCRewardID.KING_MAGRIDD.full_name: [NPCID.KING_MAGRIDD.full_name, NPCID.SOLDIER_CASTLE.full_name],
    NPCRewardID.LEO_ON_THE_AIRSHIP_DECK.full_name: [],
    NPCRewardID.SOLDIER_SOUL.full_name: [NPCID.SOLDIER_WITH_SOUL.full_name],
    LairID.KING_MAGRIDD.full_name: [ItemID.AIRSHIPKEY.full_name],
    # Act 7 - World of Evil
    ChestID.DAZZLING_SPACE_SE.full_name: [ItemID.SOULARMOR.full_name],
    ChestID.DAZZLING_SPACE_SW.full_name: [ItemID.SOULARMOR.full_name],
}


def get_rule_for_location(name: str, player: int, flag: RuleFlag) -> Callable[[CollectionState], bool]:
    """Returns the access rule for the given location."""

    dependencies = location_dependencies.get(name, [])

    if flag == RuleFlag.NONE and not dependencies:
        return no_requirement

    def rule(state: CollectionState) -> bool:
        return rule_for_flag[flag](state, player) and state.has_all(dependencies, player)

    return rule


# def set_rules(world: "SoulBlazerWorld") -> None:
#    # TODO: Cant create locations during rule generation.
#    # AssertionError: 295 != 296 : Soul Blazer modified locations count during rule creation
#    region = world.multiworld.get_region(RegionName.DEATHTOLL, world.player)
#    region.locations.append(world.create_victory_event(region))
#    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
