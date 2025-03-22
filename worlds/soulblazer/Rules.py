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
    NPCRewardID.EMBLEM_A_TILE.full_name: [NPCID.IVY.full_name, NPCID.IVY_EMBLEM_A.full_name],
    NPCRewardID.GOAT_PEN_CORNER.full_name: [NPCID.GOAT_HERB.full_name],
    NPCRewardID.TEDDY.full_name: [NPCID.TOOL_SHOP_OWNER.full_name, NPCID.TEDDY.full_name],
    NPCRewardID.PASS_TILE.full_name: [NPCID.IVY.full_name, NPCID.TULIP_PASS.full_name],
    NPCRewardID.TILE_IN_CHILDS_SECRET_CAVE.full_name: [NPCID.BOY_CAVE.full_name, ItemID.APASS.full_name],
    NPCRewardID.RECOVERY_SWORD_CRYSTAL.full_name: [
        NPCID.IVY_RECOVERY_SWORD.full_name,
        NPCID.BOY_CAVE.full_name,
        ItemID.APASS.full_name,
    ],
    NPCRewardID.VILLAGE_CHIEF.full_name: [NPCID.VILLAGE_CHIEF.full_name, NPCID.OLD_WOMAN.full_name],
    LairID.OLD_MAN.full_name: [NPCID.LISA.full_name, ItemID.DREAMROD.full_name],
    ChestID.UNDERGROUND_CASTLE_LEOS_BRUSH.full_name: [NPCID.LISA.full_name, ItemID.DREAMROD.full_name],
    # Act 2 - Greenwood
    NPCRewardID.REDHOT_MIRROR_BIRD.full_name: [NPCID.BIRD_RED_HOT_MIRROR.full_name],
    NPCRewardID.MAGIC_BELL_CRYSTAL.full_name: [
        *emblem_names,
        NPCID.DEER_MAGIC_BELL.full_name,
        NPCID.CROCODILE3.full_name,
    ],
    NPCRewardID.WOODSTIN_TRIO.full_name: [
        NPCID.DEER.full_name,
        NPCID.SQUIRREL3.full_name,
        NPCID.DOG3.full_name,
    ],
    NPCRewardID.GREENWOOD_LEAVES_TILE.full_name: [
        NPCID.MOLE_SOUL_OF_LIGHT.full_name,
        NPCID.CROCODILE.full_name,
        NPCID.CROCODILE2.full_name,
        NPCID.BIRD_GREENWOOD_LEAF.full_name,
        ItemID.DREAMROD.full_name,
    ],
    NPCRewardID.SHIELD_BRACELET_MOLE.full_name: [
        NPCID.MOLE.full_name,
        NPCID.MOLE_SHIELD_BRACELET.full_name,
        ItemID.MOLESRIBBON.full_name,
    ],
    NPCRewardID.PSYCHO_SWORD_SQUIRREL.full_name: [
        NPCID.SQUIRREL_PSYCHO_SWORD.full_name,
        ItemID.DELICIOUSSEEDS.full_name,
    ],
    NPCRewardID.EMBLEM_C_SQUIRREL.full_name: [
        NPCID.SQUIRREL_EMBLEM_C.full_name,
        NPCID.SQUIRREL_PSYCHO_SWORD.full_name,
    ],
    NPCRewardID.GREENWOODS_GUARDIAN.full_name: [NPCID.GREENWOODS_GUARDIAN.full_name],
    NPCRewardID.MOLE_SOUL_OF_LIGHT.full_name: [NPCID.MOLE_SOUL_OF_LIGHT.full_name],
    ChestID.GREENWOOD_ICE_ARMOR.full_name: [
        NPCID.MOLE.full_name,
        NPCID.SQUIRREL_ICE_ARMOR.full_name,
        ItemID.DREAMROD.full_name,
    ],
    ChestID.GREENWOOD_TUNNELS.full_name: [NPCID.MONMO.full_name, NPCID.MOLE3.full_name],
    # Act 3 - St Elles
    NPCRewardID.NORTHEASTERN_MERMAID_HERB.full_name: [NPCID.MERMAID.full_name, NPCID.DOLPHIN2.full_name],
    NPCRewardID.MAGIC_FLARE_MERMAID.full_name: [
        NPCID.MERMAID_MAGIC_FLARE.full_name,
        NPCID.MERMAID_BUBBLE_ARMOR.full_name,
    ],
    NPCRewardID.REDHOT_STICK_MERMAID.full_name: [NPCID.MERMAID_RED_HOT_STICK.full_name],
    NPCRewardID.LUE.full_name: [
        NPCID.LUE.full_name,
        NPCID.DOLPHIN_SAVES_LUE.full_name,
        NPCID.MERMAID_PEARL.full_name,
    ],
    # Logical mermaids tears. TODO: move to separate list for optional logic toggle
    NPCRewardID.MERMAID_QUEEN.full_name: [NPCID.MERMAID_QUEEN.full_name],
    NPCRewardID.ANGELFISH_SOUL_OF_SHIELD.full_name: [NPCID.ANGELFISH_SOUL_OF_SHIELD.full_name],
    LairID.MERMAID3.full_name: [ItemID.MERMAIDSTEARS.full_name],
    LairID.MERMAID_STATUE_BLESTER.full_name: [ItemID.MERMAIDSTEARS.full_name],
    ChestID.DUREAN_CRITICAL_SWORD.full_name: [ItemID.MERMAIDSTEARS.full_name],
    # Act 4 - Mountain of Souls
    NPCRewardID.MOUNTAIN_KING.full_name: [
        NPCID.DANCING_GRANDMA.full_name,
        NPCID.DANCING_GRANDMA2.full_name,
        *redhot_names,
    ],
    NPCRewardID.MUSHROOM_SHOES_BOY.full_name: [NPCID.BOY_MUSHROOM_SHOES.full_name],
    NPCRewardID.EMBLEM_E_SNAIL.full_name: [NPCID.SNAIL_EMBLEM_E.full_name],
    # Also includes path from lune to sleeping mushroom for the two locations locked behind mushroom's dream.
    NPCRewardID.EMBLEM_F_TILE.full_name: [
        NPCID.MUSHROOM_EMBLEM_F.full_name,
        NPCID.GRANDPA5.full_name,
        NPCID.MUSHROOM2.full_name,
        ItemID.DREAMROD.full_name,
    ],
    LairID.SNAIL_EMBLEM_E.full_name: [
        NPCID.MUSHROOM_EMBLEM_F.full_name,
        NPCID.GRANDPA5.full_name,
        NPCID.MUSHROOM2.full_name,
        ItemID.DREAMROD.full_name,
    ],
    # Act 5 - Leo's Lab
    NPCRewardID.EMBLEM_G_UNDER_CHEST_OF_DRAWERS.full_name: [
        NPCID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.full_name,
        NPCID.GREAT_DOOR.full_name,
        ItemID.DOORKEY.full_name,
    ],
    NPCRewardID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.full_name: [
        NPCID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.full_name,
        NPCID.GREAT_DOOR.full_name,
        ItemID.DOORKEY.full_name,
    ],
    NPCRewardID.HERB_PLANT_IN_LEOS_LAB.full_name: [
        NPCID.PLANT_HERB.full_name,
        NPCID.MOUSE.full_name,
        NPCID.CAT.full_name,
        NPCID.CAT2.full_name,
        ItemID.ACTINIDIALEAVES.full_name,
    ],
    NPCRewardID.SPARK_BOMB_MOUSE.full_name: [
        NPCID.MOUSE_SPARK_BOMB.full_name,
        NPCID.MOUSE.full_name,
        NPCID.CAT.full_name,
        NPCID.CAT2.full_name,
        ItemID.ACTINIDIALEAVES.full_name,
    ],
    NPCRewardID.LEOS_CAT_DOOR_KEY.full_name: [NPCID.CAT_DOOR_KEY.full_name, ItemID.DREAMROD.full_name],
    NPCRewardID.ACTINIDIA_PLANT.full_name: [NPCID.PLANT_ACTINIDIA_LEAVES.full_name],
    NPCRewardID.CHEST_OF_DRAWERS_HERB.full_name: [NPCID.CHEST_OF_DRAWERS2.full_name],
    NPCRewardID.MARIE.full_name: [NPCID.MARIE.full_name],
    # Potentially optional icearmor requirement.
    NPCRewardID.POWER_PLANT_CRYSTAL.full_name: [ItemID.ICEARMOR.full_name],
    NPCRewardID.GREAT_DOOR_SOUL_OF_DETECTION.full_name: [NPCID.GREAT_DOOR_SOUL_OF_DETECTION.full_name],
    LairID.DOLL.full_name: [ItemID.ICEARMOR.full_name],
    LairID.MARIE.full_name: [ItemID.ICEARMOR.full_name],
    # Act 6 - Magridd Castle
    NPCRewardID.ELEMENTAL_MAIL_SOLDIER.full_name: [
        NPCID.SOLDIER_ELEMENTAL_MAIL.full_name,
        ItemID.DREAMROD.full_name,
    ],
    NPCRewardID.SUPER_BRACELET_TILE.full_name: [
        NPCID.DR_LEO.full_name,
        NPCID.SOLDIER_WITH_LEO.full_name,
        NPCID.SOLDIER_DOK.full_name,
        NPCID.QUEEN_MAGRIDD.full_name,
    ],
    NPCRewardID.QUEEN_MAGRIDD_VIP_CARD.full_name: [NPCID.QUEEN_MAGRIDD.full_name],
    NPCRewardID.PLATINUM_CARD_SOLDIER.full_name: [
        NPCID.SOLDIER_PLATINUM_CARD.full_name,
        NPCID.SINGER_CONCERT_HALL.full_name,
        ItemID.HARPSTRING.full_name,
    ],
    NPCRewardID.MAID_HERB.full_name: [NPCID.MAID_HERB.full_name],  # anything else?
    NPCRewardID.EMBLEM_H_TILE.full_name: [NPCID.SOLDIER_CASTLE.full_name],
    NPCRewardID.KING_MAGRIDD.full_name: [NPCID.KING_MAGRIDD.full_name, NPCID.SOLDIER_CASTLE.full_name],
    NPCRewardID.LEO_ON_THE_AIRSHIP_DECK.full_name: [],
    NPCRewardID.SOLDIER_SOUL_OF_REALITY.full_name: [NPCID.SOLDIER_SOUL_OF_REALITY.full_name],
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
