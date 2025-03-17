from typing import Callable

from BaseClasses import CollectionState
from .Data.Enums import RuleFlag, ItemID, SoulID, LairID, ChestID, NPCRewardID, NPCID
from .Items import castable_magic_names, sword_names, emblem_names, redhot_names

# if TYPE_CHECKING:
#    from . import SoulBlazerWorld

metal_cutting_swords = [ItemID.ZANTETSUSWORD.display_name, ItemID.SOULBLADE.display_name]
spirit_cutting_swords = [ItemID.SPIRITSWORD.display_name, ItemID.SOULBLADE.display_name]
thunder_items = [ItemID.THUNDERRING.display_name, *metal_cutting_swords]


def no_requirement(state: CollectionState, player: int | None = None) -> bool:
    return True


def can_cut_metal(state: CollectionState, player: int) -> bool:
    return state.has_any(metal_cutting_swords, player)


def can_cut_spirit(state: CollectionState, player: int) -> bool:
    return state.has_any(spirit_cutting_swords, player)


def has_thunder(state: CollectionState, player: int) -> bool:
    return state.has_any(thunder_items, player)


def has_magic(state: CollectionState, player: int) -> bool:
    return state.has(SoulID.SOUL_MAGICIAN.display_name, player) and state.has_any(castable_magic_names, player)


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has_any(sword_names, player)


def has_stones(state: CollectionState, player: int) -> bool:
    count: int = state.multiworld.worlds[player].options.stones_count.value
    return state.has_group("stones", player, count)


def has_phoenix_cutscene(state: CollectionState, player: int) -> bool:
    return state.can_reach_location(NPCRewardID.MOUNTAIN_KING.display_name, player)


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
    NPCRewardID.TOOL_SHOP_OWNER.display_name: [NPCID.TOOL_SHOP_OWNER.display_name],
    NPCRewardID.EMBLEM_A_TILE.display_name: [NPCID.IVY.display_name, NPCID.IVY_EMBLEM_A.display_name],
    NPCRewardID.GOAT_PEN_CORNER.display_name: [NPCID.GOAT_HERB.display_name],
    NPCRewardID.TEDDY.display_name: [NPCID.TOOL_SHOP_OWNER.display_name, NPCID.TEDDY.display_name],
    NPCRewardID.PASS_TILE.display_name: [NPCID.IVY.display_name, NPCID.TULIP_PASS.display_name],
    NPCRewardID.TILE_IN_CHILDS_SECRET_CAVE.display_name: [NPCID.BOY_CAVE.display_name, ItemID.APASS.display_name],
    NPCRewardID.RECOVERY_SWORD_CRYSTAL.display_name: [
        NPCID.IVY_RECOVERY_SWORD.display_name,
        NPCID.BOY_CAVE.display_name,
        ItemID.APASS.display_name,
    ],
    NPCRewardID.VILLAGE_CHIEF.display_name: [NPCID.VILLAGE_CHIEF.display_name, NPCID.OLD_WOMAN.display_name],
    LairID.OLD_MAN.display_name: [NPCID.LISA.display_name, ItemID.DREAMROD.display_name],
    ChestID.UNDERGROUND_CASTLE_LEOS_BRUSH.display_name: [NPCID.LISA.display_name, ItemID.DREAMROD.display_name],
    # Act 2 - Greenwood
    NPCRewardID.REDHOT_MIRROR_BIRD.display_name: [NPCID.BIRD_RED_HOT_MIRROR.display_name],
    NPCRewardID.MAGIC_BELL_CRYSTAL.display_name: [
        *emblem_names,
        NPCID.DEER_MAGIC_BELL.display_name,
        NPCID.CROCODILE3.display_name,
    ],
    NPCRewardID.WOODSTIN_TRIO.display_name: [
        NPCID.DEER.display_name,
        NPCID.SQUIRREL3.display_name,
        NPCID.DOG3.display_name,
    ],
    NPCRewardID.GREENWOOD_LEAVES_TILE.display_name: [
        NPCID.MOLE_SOUL_OF_LIGHT.display_name,
        NPCID.CROCODILE.display_name,
        NPCID.CROCODILE2.display_name,
        NPCID.BIRD_GREENWOOD_LEAF.display_name,
        ItemID.DREAMROD.display_name,
    ],
    NPCRewardID.SHIELD_BRACELET_MOLE.display_name: [
        NPCID.MOLE.display_name,
        NPCID.MOLE_SHIELD_BRACELET.display_name,
        ItemID.MOLESRIBBON.display_name,
    ],
    NPCRewardID.PSYCHO_SWORD_SQUIRREL.display_name: [
        NPCID.SQUIRREL_PSYCHO_SWORD.display_name,
        ItemID.DELICIOUSSEEDS.display_name,
    ],
    NPCRewardID.EMBLEM_C_SQUIRREL.display_name: [
        NPCID.SQUIRREL_EMBLEM_C.display_name,
        NPCID.SQUIRREL_PSYCHO_SWORD.display_name,
    ],
    NPCRewardID.GREENWOODS_GUARDIAN.display_name: [NPCID.GREENWOODS_GUARDIAN.display_name],
    NPCRewardID.MOLE_SOUL_OF_LIGHT.display_name: [NPCID.MOLE_SOUL_OF_LIGHT.display_name],
    ChestID.GREENWOOD_ICE_ARMOR.display_name: [
        NPCID.MOLE.display_name,
        NPCID.SQUIRREL_ICE_ARMOR.display_name,
        ItemID.DREAMROD.display_name,
    ],
    ChestID.GREENWOOD_TUNNELS.display_name: [NPCID.MONMO.display_name, NPCID.MOLE3.display_name],
    # Act 3 - St Elles
    NPCRewardID.NORTHEASTERN_MERMAID_HERB.display_name: [NPCID.MERMAID.display_name, NPCID.DOLPHIN2.display_name],
    NPCRewardID.MAGIC_FLARE_MERMAID.display_name: [
        NPCID.MERMAID_MAGIC_FLARE.display_name,
        NPCID.MERMAID_BUBBLE_ARMOR.display_name,
    ],
    NPCRewardID.REDHOT_STICK_MERMAID.display_name: [NPCID.MERMAID_RED_HOT_STICK.display_name],
    NPCRewardID.LUE.display_name: [
        NPCID.LUE.display_name,
        NPCID.DOLPHIN_SAVES_LUE.display_name,
        NPCID.MERMAID_PEARL.display_name,
    ],
    # Logical mermaids tears. TODO: move to separate list for optional logic toggle
    NPCRewardID.MERMAID_QUEEN.display_name: [NPCID.MERMAID_QUEEN.display_name],
    NPCRewardID.ANGELFISH_SOUL_OF_SHIELD.display_name: [NPCID.ANGELFISH_SOUL_OF_SHIELD.display_name],
    LairID.MERMAID3.display_name: [ItemID.MERMAIDSTEARS.display_name],
    LairID.MERMAID_STATUE_BLESTER.display_name: [ItemID.MERMAIDSTEARS.display_name],
    ChestID.DUREAN_CRITICAL_SWORD.display_name: [ItemID.MERMAIDSTEARS.display_name],
    # Act 4 - Mountain of Souls
    NPCRewardID.MOUNTAIN_KING.display_name: [
        NPCID.DANCING_GRANDMA.display_name,
        NPCID.DANCING_GRANDMA2.display_name,
        *redhot_names,
    ],
    NPCRewardID.MUSHROOM_SHOES_BOY.display_name: [NPCID.BOY_MUSHROOM_SHOES.display_name],
    NPCRewardID.EMBLEM_E_SNAIL.display_name: [NPCID.SNAIL_EMBLEM_E.display_name],
    # Also includes path from lune to sleeping mushroom for the two locations locked behind mushroom's dream.
    NPCRewardID.EMBLEM_F_TILE.display_name: [
        NPCID.MUSHROOM_EMBLEM_F.display_name,
        NPCID.GRANDPA5.display_name,
        NPCID.MUSHROOM2.display_name,
        ItemID.DREAMROD.display_name,
    ],
    LairID.SNAIL_EMBLEM_E.display_name: [
        NPCID.MUSHROOM_EMBLEM_F.display_name,
        NPCID.GRANDPA5.display_name,
        NPCID.MUSHROOM2.display_name,
        ItemID.DREAMROD.display_name,
    ],
    # Act 5 - Leo's Lab
    NPCRewardID.EMBLEM_G_UNDER_CHEST_OF_DRAWERS.display_name: [
        NPCID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.display_name,
        NPCID.GREAT_DOOR.display_name,
        ItemID.DOORKEY.display_name,
    ],
    NPCRewardID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.display_name: [
        NPCID.CHEST_OF_DRAWERS_MYSTIC_ARMOR.display_name,
        NPCID.GREAT_DOOR.display_name,
        ItemID.DOORKEY.display_name,
    ],
    NPCRewardID.HERB_PLANT_IN_LEOS_LAB.display_name: [
        NPCID.PLANT_HERB.display_name,
        NPCID.MOUSE.display_name,
        NPCID.CAT.display_name,
        NPCID.CAT2.display_name,
        ItemID.ACTINIDIALEAVES.display_name,
    ],
    NPCRewardID.SPARK_BOMB_MOUSE.display_name: [
        NPCID.MOUSE_SPARK_BOMB.display_name,
        NPCID.MOUSE.display_name,
        NPCID.CAT.display_name,
        NPCID.CAT2.display_name,
        ItemID.ACTINIDIALEAVES.display_name,
    ],
    NPCRewardID.LEOS_CAT_DOOR_KEY.display_name: [NPCID.CAT_DOOR_KEY.display_name, ItemID.DREAMROD.display_name],
    NPCRewardID.ACTINIDIA_PLANT.display_name: [NPCID.PLANT_ACTINIDIA_LEAVES.display_name],
    NPCRewardID.CHEST_OF_DRAWERS_HERB.display_name: [NPCID.CHEST_OF_DRAWERS2.display_name],
    NPCRewardID.MARIE.display_name: [NPCID.MARIE.display_name],
    # Potentially optional icearmor requirement.
    NPCRewardID.POWER_PLANT_CRYSTAL.display_name: [ItemID.ICEARMOR.display_name],
    NPCRewardID.GREAT_DOOR_SOUL_OF_DETECTION.display_name: [NPCID.GREAT_DOOR_SOUL_OF_DETECTION.display_name],
    LairID.DOLL.display_name: [ItemID.ICEARMOR.display_name],
    LairID.MARIE.display_name: [ItemID.ICEARMOR.display_name],
    # Act 6 - Magridd Castle
    NPCRewardID.ELEMENTAL_MAIL_SOLDIER.display_name: [
        NPCID.SOLDIER_ELEMENTAL_MAIL.display_name,
        ItemID.DREAMROD.display_name,
    ],
    NPCRewardID.SUPER_BRACELET_TILE.display_name: [
        NPCID.DR_LEO.display_name,
        NPCID.SOLDIER_WITH_LEO.display_name,
        NPCID.SOLDIER_DOK.display_name,
        NPCID.QUEEN_MAGRIDD.display_name,
    ],
    NPCRewardID.QUEEN_MAGRIDD_VIP_CARD.display_name: [NPCID.QUEEN_MAGRIDD.display_name],
    NPCRewardID.PLATINUM_CARD_SOLDIER.display_name: [
        NPCID.SOLDIER_PLATINUM_CARD.display_name,
        NPCID.SINGER_CONCERT_HALL.display_name,
        ItemID.HARPSTRING.display_name,
    ],
    NPCRewardID.MAID_HERB.display_name: [NPCID.MAID_HERB.display_name],  # anything else?
    NPCRewardID.EMBLEM_H_TILE.display_name: [NPCID.SOLDIER_CASTLE.display_name],
    NPCRewardID.KING_MAGRIDD.display_name: [NPCID.KING_MAGRIDD.display_name, NPCID.SOLDIER_CASTLE.display_name],
    NPCRewardID.LEO_ON_THE_AIRSHIP_DECK.display_name: [],
    NPCRewardID.SOLDIER_SOUL_OF_REALITY.display_name: [NPCID.SOLDIER_SOUL_OF_REALITY.display_name],
    LairID.KING_MAGRIDD.display_name: [ItemID.AIRSHIPKEY.display_name],
    # Act 7 - World of Evil
    ChestID.DAZZLING_SPACE_SE.display_name: [ItemID.SOULARMOR.display_name],
    ChestID.DAZZLING_SPACE_SW.display_name: [ItemID.SOULARMOR.display_name],
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
