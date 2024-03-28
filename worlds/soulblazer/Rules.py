from typing import Callable

from enum import IntEnum, auto
from BaseClasses import CollectionState
from .Names import ItemName, ItemID, LairName, LairID, ChestName, ChestID, NPCRewardName, NPCRewardID, NPCName
from .Items import emblems_table
from .Locations import SoulBlazerLocationData

class LocationFlag(IntEnum):
    NONE = 0
    CAN_CUT_METAL = auto()
    CAN_CUT_SPIRIT = auto()
    HAS_THUNDER = auto()
    HAS_MAGIC = auto()

metal_items = [ItemName.ZANTETSUSWORD, ItemName.SOULBLADE]
spirit_items = [ItemName.SPIRITSWORD, ItemName.SOULBLADE]
thunder_items = [ItemName.THUNDERRING, *metal_items]
magic_items = [ItemName.FLAMEBALL, ItemName.LIGHTARROW, ItemName.MAGICFLARE, ItemName.ROTATOR, ItemName.SPARKBOMB, ItemName.FLAMEPILLAR, ItemName.TORNADO]

def no_requirement(state: CollectionState, player: int) -> bool:
    return True

def can_cut_metal(state: CollectionState, player: int) -> bool:
    return state.has_any(metal_items, player)

def can_cut_spirit(state: CollectionState, player: int) -> bool:
    return state.has_any(spirit_items, player)

def has_thunder(state: CollectionState, player: int) -> bool:
    return state.has_any(thunder_items, player)

def has_magic(state: CollectionState, player: int) -> bool:
    return state.has_any(magic_items, player)

rule_for_flag = {
    LocationFlag.NONE : no_requirement,
    LocationFlag.CAN_CUT_METAL : can_cut_metal,
    LocationFlag.CAN_CUT_SPIRIT : can_cut_spirit,
    LocationFlag.HAS_THUNDER : has_thunder,
    LocationFlag.HAS_MAGIC : has_magic,
    LocationFlag.NEEDS_NPC : no_requirement, # TODO: implement?
}

# Many locations depend on one or two NPC releases so rather than create regions to hold one location,
# we put these location-specific dependencies here.
# TODO: Some of these NPCs are not locations and do not have checks. remove.
# TODO: chests too
location_dependencies = {
    # Act 1 - Grass Valley
    NPCRewardName.TOOL_SHOP_OWNER: [NPCName.TOOL_SHOP_OWNER],
    #TODO: figure out if we can patch it to make emblem A tile activatable without turning the water wheel
    NPCRewardName.EMBLEM_A_TILE: [NPCName.IVY, NPCName.IVY_EMBLEM_A, NPCName.WATER_MILL],
    NPCRewardName.GOAT_PEN_CORNER: [NPCName.GOAT_HERB],
    NPCRewardName.TEDDY: [NPCName.TOOL_SHOP_OWNER, NPCName.TEDDY],
    NPCRewardName.PASS_TILE: [NPCName.IVY, NPCName.TULIP_PASS],
    #TODO: put these two in a region?
    NPCRewardName.TILE_IN_CHILDS_SECRET_CAVE: [NPCName.BOY_CAVE, ItemName.APASS],
    NPCRewardName.RECOVERY_SWORD_CRYSTAL: [NPCName.IVY_RECOVERY_SWORD, NPCName.BOY_CAVE, ItemName.APASS],

    NPCRewardName.VILLAGE_CHIEF: [NPCName.VILLAGE_CHIEF, NPCName.OLD_WOMAN],

    NPCRewardName.MAGICIAN: [], # TODO: delete
    NPCRewardName.GRASS_VALLEY_SECRET_ROOM_CRYSTAL: [NPCName.IVY_CHEST_ROOM], # TODO: put this and two chests into region and delete.
    NPCRewardName.UNDERGROUND_CASTLE_CRYSTAL: [], # TODO: delete
    

    # Act 2 - Greenwood
    NPCRewardName.REDHOT_MIRROR_BIRD: [NPCName.BIRD_RED_HOT_MIRROR],
    NPCRewardName.MAGIC_BELL_CRYSTAL: [*emblems_table.keys(), NPCName.DEER_MAGIC_BELL, NPCName.CROCODILE3],
    NPCRewardName.WOODSTIN_TRIO: [NPCName.DEER, NPCName.SQUIRREL3, NPCName.DOG3],
    NPCRewardName.GREENWOODS_GUARDIAN: [], # TODO: delete
    NPCRewardName.GREENWOOD_LEAVES_TILE: [NPCName.MOLE_SOUL_OF_LIGHT, NPCName.CROCODILE, NPCName.CROCODILE2, NPCName.BIRD_GREENWOOD_LEAF, ItemName.DREAMROD],
    NPCRewardName.SHIELD_BRACELET_MOLE: [NPCName.MOLE, NPCName.MOLE_SHIELD_BRACELET, ItemName.MOLESRIBBON],
    NPCRewardName.PSYCHO_SWORD_SQUIRREL: [NPCName.SQUIRREL_PSYCHO_SWORD, ItemName.DELICIOUSSEEDS],
    NPCRewardName.EMBLEM_C_SQUIRREL: [NPCName.SQUIRREL_EMBLEM_C, NPCName.SQUIRREL_PSYCHO_SWORD],
    NPCRewardName.WATER_SHRINE_STRANGE_BOTTLE: [], #TODO: delete
    NPCRewardName.LIGHT_ARROW_CRYSTAL : [], #TODO: delete
    NPCRewardName.LOST_MARSH_CRYSTAL  : [], #TODO: delete
    NPCRewardName.WATER_SHRINE_CRYSTAL: [], #TODO: delete
    NPCRewardName.FIRE_SHRINE_CRYSTAL : [], #TODO: delete

    # Act 3 - St Elles
    # Notes:
    # Mermaid 4: unlocks path to West Seabed Sanctuary (make region?)
    # Dolphin 2: unlocks path to east seabed sanctuary (make region?)
    # Bubble Armor mermaid: unlocks path to south seabed sanctuary
    NPCRewardName.NORTHEASTERN_MERMAID_HERB: [NPCName.MERMAID, NPCName.DOLPHIN2],
    NPCRewardName.BUBBLE_ARMOR_MERMAID: [], #TODO: delete
    NPCRewardName.MAGIC_FLARE_MERMAID: [NPCName.MERMAID_MAGIC_FLARE, NPCName.MERMAID_BUBBLE_ARMOR],
    NPCRewardName.MERMAID_QUEEN: [], #TODO: delete
    NPCRewardName.REDHOT_STICK_MERMAID: [NPCName.MERMAID_BUBBLE_ARMOR],

    #TODO: Lue also needs 1 of Bubble mermaid or Dolphin 4. gonna need regions for those
    # MERMAID_PEARL should probably be a region too. gonna need to to do a little mapping
    NPCRewardName.LUE: [NPCName.LUE, NPCName.DOLPHIN_SAVES_LUE, NPCName.MERMAID_PEARL],

    NPCRewardName.ROCKBIRD_CRYSTAL: [],
    NPCRewardName.SEABED_CRYSTAL_NEAR_BLESTER: [],
    NPCRewardName.SEABED_CRYSTAL_NEAR_DUREAN: [],

    # Act 4 - Mountain of Souls

    #TODO: Delete these once they are no longer useful.
    LairID.DOG3:                  [LairID.DEER],
    LairID.SQUIRREL3:             [LairID.DEER],
    LairID.DOLPHIN:               [LairID.MERMAID_NANA],
    LairID.ANGELFISH:             [LairID.ANGELFISH_SOUL_OF_SHIELD],
    LairID.MERMAID2:              [LairID.MERMAID4],
    LairID.MERMAID_RED_HOT_STICK: [LairID.MERMAID_BUBBLE_ARMOR],
    LairID.MERMAID6:              [LairID.MERMAID4],
    LairID.MERMAID_TEARS:         [LairID.MERMAID_BUBBLE_ARMOR],
    LairID.MERMAID_MAGIC_FLARE:   [LairID.MERMAID_BUBBLE_ARMOR],
    LairID.ANGELFISH4:            [LairID.MERMAID5],
    LairID.MERMAID8:              [LairID.MERMAID_BUBBLE_ARMOR],
    LairID.MERMAID9:              [LairID.MERMAID4],
    LairID.NOME:                  [LairID.GRANDPA5],
    LairID.BOY2:                  [LairID.GRANDPA5],
    LairID.MUSHROOM_EMBLEM_F:     [LairID.GRANDPA5],
    LairID.GRANDMA:               [LairID.GRANDPA2],
    LairID.GIRL2:                 [LairID.BOY],
    LairID.SNAIL:                 [LairID.BOY_MUSHROOM_SHOES],
    LairID.SNAIL2:                [LairID.GRANDPA4],
    LairID.SOLDIER6:              [LairID.SINGER_CONCERT_HALL],
    LairID.SOLDIER_PLATINUM_CARD: [LairID.SINGER_CONCERT_HALL],
    LairID.MAID2:                 [LairID.SINGER_CONCERT_HALL],
    LairID.SOLDIER7:              [LairID.MAID],
    LairID.SOLDIER8:              [LairID.SOLDIER_SOUL_OF_REALITY],
    LairID.SOLDIER10:             [LairID.MAID_HERB],
    LairID.KING_MAGRIDD:          [LairID.SOLDIER_CASTLE],

}

def get_rule_for_location(name: str, player: int, flag: LocationFlag) -> Callable[[CollectionState], bool]:
    """Returns the access rule for the given location."""

    def rule(state: CollectionState) -> bool:
        return (
            rule_for_flag[flag](state, player)
            and state.has_all(location_dependencies.get(name, []), player)
        )
    
    return rule

#TODO: access rule for region/entrance