from typing import Dict, List, Callable, Optional, TYPE_CHECKING

from enum import IntEnum, auto
from BaseClasses import CollectionState
from .Names import (
    ItemName,
    ItemID,
    LairName,
    LairID,
    ChestName,
    ChestID,
    NPCRewardName,
    NPCRewardID,
    NPCName,
    RegionName,
)
from .Items import emblems_table, swords_table

if TYPE_CHECKING:
    from . import SoulBlazerWorld


class RuleFlag(IntEnum):
    NONE = 0
    """No special requirement preventing access."""
    CAN_CUT_METAL = auto()
    """Requires a way to damage metal enemies (Zantestu Sword|Soul Blade)."""
    CAN_CUT_SPIRIT = auto()
    """Requires a way to damage metal enemies (Spirit Sword|Soul Blade)."""
    HAS_THUNDER = auto()
    """
    Requires a way to damage metal enemies in the presence of thunder pyramids
    (Thunder Ring|Zantestu Sword|Soul Blade).
    """
    HAS_MAGIC = auto()
    """Requires a way to damage enemies outside of sword range."""
    HAS_SWORD = auto()
    """
    Requires any sword. Only used as a sanity check at the start of the game
    since we prefill the first chest with a sword.
    """
    HAS_STONES = auto()
    """Requires the necessary number of stones. Adjustable via option."""
    PHOENIX_CUTSCENE = auto()
    """
    Requires the Phoenix cutscene:
    Access to the Mountain King
    Both Dancing Grandmas
    The 3 Red-Hot Items
    """


metal_items = [ItemName.ZANTETSUSWORD, ItemName.SOULBLADE]
spirit_items = [ItemName.SPIRITSWORD, ItemName.SOULBLADE]
thunder_items = [ItemName.THUNDERRING, *metal_items]
magic_items = [
    ItemName.FLAMEBALL,
    ItemName.LIGHTARROW,
    ItemName.MAGICFLARE,
    ItemName.ROTATOR,
    ItemName.SPARKBOMB,
    ItemName.FLAMEPILLAR,
    ItemName.TORNADO,
]
sword_items = [*swords_table.keys()]


def no_requirement(state: CollectionState, player: Optional[int] = None) -> bool:
    return True


def can_cut_metal(state: CollectionState, player: int) -> bool:
    return state.has_any(metal_items, player)


def can_cut_spirit(state: CollectionState, player: int) -> bool:
    return state.has_any(spirit_items, player)


def has_thunder(state: CollectionState, player: int) -> bool:
    return state.has_any(thunder_items, player)


def has_magic(state: CollectionState, player: int) -> bool:
    return state.has(ItemName.SOUL_MAGICIAN, player) and state.has_any(magic_items, player)


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has_any(sword_items, player)


def has_stones(state: CollectionState, player: int) -> bool:
    count: int = state.multiworld.worlds[player].options.stones_count.value
    return state.has_group("stones", player, count)


def has_phoenix_cutscene(state: CollectionState, player: int) -> bool:
    return state.can_reach_location(NPCRewardName.MOUNTAIN_KING, player)


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
location_dependencies: Dict[str, List[str]] = {
    # Act 1 - Grass Valley
    NPCRewardName.TOOL_SHOP_OWNER: [NPCName.TOOL_SHOP_OWNER],
    NPCRewardName.EMBLEM_A_TILE: [NPCName.IVY, NPCName.IVY_EMBLEM_A],
    NPCRewardName.GOAT_PEN_CORNER: [NPCName.GOAT_HERB],
    NPCRewardName.TEDDY: [NPCName.TOOL_SHOP_OWNER, NPCName.TEDDY],
    NPCRewardName.PASS_TILE: [NPCName.IVY, NPCName.TULIP_PASS],
    NPCRewardName.TILE_IN_CHILDS_SECRET_CAVE: [NPCName.BOY_CAVE, ItemName.APASS],
    NPCRewardName.RECOVERY_SWORD_CRYSTAL: [NPCName.IVY_RECOVERY_SWORD, NPCName.BOY_CAVE, ItemName.APASS],
    NPCRewardName.VILLAGE_CHIEF: [NPCName.VILLAGE_CHIEF, NPCName.OLD_WOMAN],
    LairName.OLD_MAN: [NPCName.LISA, ItemName.DREAMROD],
    ChestName.UNDERGROUND_CASTLE_LEOS_BRUSH: [NPCName.LISA, ItemName.DREAMROD],
    # Act 2 - Greenwood
    NPCRewardName.REDHOT_MIRROR_BIRD: [NPCName.BIRD_RED_HOT_MIRROR],
    NPCRewardName.MAGIC_BELL_CRYSTAL: [*emblems_table.keys(), NPCName.DEER_MAGIC_BELL, NPCName.CROCODILE3],
    NPCRewardName.WOODSTIN_TRIO: [NPCName.DEER, NPCName.SQUIRREL3, NPCName.DOG3],
    NPCRewardName.GREENWOOD_LEAVES_TILE: [
        NPCName.MOLE_SOUL_OF_LIGHT,
        NPCName.CROCODILE,
        NPCName.CROCODILE2,
        NPCName.BIRD_GREENWOOD_LEAF,
        ItemName.DREAMROD,
    ],
    NPCRewardName.SHIELD_BRACELET_MOLE: [NPCName.MOLE, NPCName.MOLE_SHIELD_BRACELET, ItemName.MOLESRIBBON],
    NPCRewardName.PSYCHO_SWORD_SQUIRREL: [NPCName.SQUIRREL_PSYCHO_SWORD, ItemName.DELICIOUSSEEDS],
    NPCRewardName.EMBLEM_C_SQUIRREL: [NPCName.SQUIRREL_EMBLEM_C, NPCName.SQUIRREL_PSYCHO_SWORD],
    NPCRewardName.GREENWOODS_GUARDIAN: [NPCName.GREENWOODS_GUARDIAN],
    NPCRewardName.MOLE_SOUL_OF_LIGHT: [NPCName.MOLE_SOUL_OF_LIGHT],
    ChestName.GREENWOOD_ICE_ARMOR: [NPCName.MOLE, NPCName.SQUIRREL_ICE_ARMOR, ItemName.DREAMROD],
    ChestName.GREENWOOD_TUNNELS: [NPCName.MONMO, NPCName.MOLE3],
    # Act 3 - St Elles
    NPCRewardName.NORTHEASTERN_MERMAID_HERB: [NPCName.MERMAID, NPCName.DOLPHIN2],
    NPCRewardName.MAGIC_FLARE_MERMAID: [NPCName.MERMAID_MAGIC_FLARE, NPCName.MERMAID_BUBBLE_ARMOR],
    NPCRewardName.REDHOT_STICK_MERMAID: [NPCName.MERMAID_RED_HOT_STICK],
    NPCRewardName.LUE: [NPCName.LUE, NPCName.DOLPHIN_SAVES_LUE, NPCName.MERMAID_PEARL],
    # Logical mermaids tears. TODO: move to separate list for optional logic toggle
    NPCRewardName.MERMAID_QUEEN: [NPCName.MERMAID_QUEEN],
    NPCRewardName.ANGELFISH_SOUL_OF_SHIELD: [NPCName.ANGELFISH_SOUL_OF_SHIELD],
    LairName.MERMAID3: [ItemName.MERMAIDSTEARS],
    LairName.MERMAID_STATUE_BLESTER: [ItemName.MERMAIDSTEARS],
    ChestName.DUREAN_CRITICAL_SWORD: [ItemName.MERMAIDSTEARS],
    # Act 4 - Mountain of Souls
    NPCRewardName.MOUNTAIN_KING: [
        NPCName.DANCING_GRANDMA,
        NPCName.DANCING_GRANDMA2,
        ItemName.REDHOTBALL,
        ItemName.REDHOTMIRROR,
        ItemName.REDHOTSTICK,
    ],
    NPCRewardName.MUSHROOM_SHOES_BOY: [NPCName.BOY_MUSHROOM_SHOES],
    NPCRewardName.EMBLEM_E_SNAIL: [NPCName.SNAIL_EMBLEM_E],
    # Also includes path from lune to sleeping mushroom for the two locations locked behind mushroom's dream.
    NPCRewardName.EMBLEM_F_TILE: [NPCName.MUSHROOM_EMBLEM_F, NPCName.GRANDPA5, NPCName.MUSHROOM2, ItemName.DREAMROD],
    LairName.SNAIL_EMBLEM_E: [NPCName.MUSHROOM_EMBLEM_F, NPCName.GRANDPA5, NPCName.MUSHROOM2, ItemName.DREAMROD],
    # Act 5 - Leo's Lab
    NPCRewardName.EMBLEM_G_UNDER_CHEST_OF_DRAWERS: [
        NPCName.CHEST_OF_DRAWERS_MYSTIC_ARMOR,
        NPCName.GREAT_DOOR,
        ItemName.DOORKEY,
    ],
    NPCRewardName.CHEST_OF_DRAWERS_MYSTIC_ARMOR: [
        NPCName.CHEST_OF_DRAWERS_MYSTIC_ARMOR,
        NPCName.GREAT_DOOR,
        ItemName.DOORKEY,
    ],
    NPCRewardName.HERB_PLANT_IN_LEOS_LAB: [
        NPCName.PLANT_HERB,
        NPCName.MOUSE,
        NPCName.CAT,
        NPCName.CAT2,
        ItemName.ACTINIDIALEAVES,
    ],
    NPCRewardName.SPARK_BOMB_MOUSE: [
        NPCName.MOUSE_SPARK_BOMB,
        NPCName.MOUSE,
        NPCName.CAT,
        NPCName.CAT2,
        ItemName.ACTINIDIALEAVES,
    ],
    NPCRewardName.LEOS_CAT_DOOR_KEY: [NPCName.CAT_DOOR_KEY, ItemName.DREAMROD],
    NPCRewardName.ACTINIDIA_PLANT: [NPCName.PLANT_ACTINIDIA_LEAVES],
    NPCRewardName.CHEST_OF_DRAWERS_HERB: [NPCName.CHEST_OF_DRAWERS2],
    NPCRewardName.MARIE: [NPCName.MARIE],
    # Potentially optional icearmor requirement.
    NPCRewardName.POWER_PLANT_CRYSTAL: [ItemName.ICEARMOR],
    NPCRewardName.GREAT_DOOR_SOUL_OF_DETECTION: [NPCName.GREAT_DOOR_SOUL_OF_DETECTION],
    LairName.DOLL: [ItemName.ICEARMOR],
    LairName.MARIE: [ItemName.ICEARMOR],
    # Act 6 - Magridd Castle
    NPCRewardName.ELEMENTAL_MAIL_SOLDIER: [NPCName.SOLDIER_ELEMENTAL_MAIL, ItemName.DREAMROD],
    NPCRewardName.SUPER_BRACELET_TILE: [
        NPCName.DR_LEO,
        NPCName.SOLDIER_WITH_LEO,
        NPCName.SOLDIER_DOK,
        NPCName.QUEEN_MAGRIDD,
    ],
    NPCRewardName.QUEEN_MAGRIDD_VIP_CARD: [NPCName.QUEEN_MAGRIDD],
    NPCRewardName.PLATINUM_CARD_SOLDIER: [
        NPCName.SOLDIER_PLATINUM_CARD,
        NPCName.SINGER_CONCERT_HALL,
        ItemName.HARPSTRING,
    ],
    NPCRewardName.MAID_HERB: [NPCName.MAID_HERB],  # anything else?
    NPCRewardName.EMBLEM_H_TILE: [NPCName.SOLDIER_CASTLE],
    NPCRewardName.KING_MAGRIDD: [NPCName.KING_MAGRIDD, NPCName.SOLDIER_CASTLE],
    NPCRewardName.LEO_ON_THE_AIRSHIP_DECK: [],
    NPCRewardName.SOLDIER_SOUL_OF_REALITY: [NPCName.SOLDIER_SOUL_OF_REALITY],
    LairName.KING_MAGRIDD: [ItemName.AIRSHIPKEY],
    # Act 7 - World of Evil
    ChestName.DAZZLING_SPACE_SE: [ItemName.SOULARMOR],
    ChestName.DAZZLING_SPACE_SW: [ItemName.SOULARMOR],
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
