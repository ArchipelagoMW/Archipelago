from dataclasses import dataclass
from dataclass_wizard import YAMLWizard
from enum import Enum
from ..Names.ArchipelagoID import BASE_ID, LAIR_ID_OFFSET, NPC_REWARD_OFFSET
from ..Names import ChestName, LairName, NPCName, ItemName, NPCRewardName
from ..Rules import RuleFlag
from .IDs import ChestID, ItemID, LairID, NPCRewardID

#TODO move all data enums into file?
class LocationType(Enum):
    CHEST = "Chest"
    """Location checked by opening a chest."""
    NPC_REWARD = "NPC Reward"
    """Location checked by talking to an NPC or stepping on an item tile."""
    LAIR = "Lair"
    """Location checked by sealing a monster lair."""

class RuleFlag(Enum):
    NONE = "NONE"
    """No special requirement preventing access."""
    CAN_CUT_METAL = "CAN_CUT_METAL"
    """Requires a way to damage metal enemies (Zantestu Sword|Soul Blade)."""
    CAN_CUT_SPIRIT = "CAN_CUT_SPIRIT"
    """Requires a way to damage metal enemies (Spirit Sword|Soul Blade)."""
    HAS_THUNDER = "HAS_THUNDER"
    """
    Requires a way to damage metal enemies in the presence of thunder pyramids
    (Thunder Ring|Zantestu Sword|Soul Blade).
    """
    HAS_MAGIC = "HAS_MAGIC"
    """Requires a way to damage enemies outside of sword range."""
    HAS_SWORD = "HAS_SWORD"
    """
    Requires any sword. Only used as a sanity check at the start of the game
    since we prefill the first chest with a sword.
    """
    HAS_STONES = "HAS_STONES"
    """Requires the necessary number of stones. Adjustable via option."""
    PHOENIX_CUTSCENE = "PHOENIX_CUTSCENE"
    """
    Requires the Phoenix cutscene:
    Access to the Mountain King
    Both Dancing Grandmas
    The 3 Red-Hot Items
    """

#TODO: put all dataclasses in one place?

@dataclass(frozen=True)
class SoulBlazerLocationData():
    id: int
    """Internal location ID and index into ROM chest/lair/NPC reward table"""
    name: str
    """String representation of the location."""
    type: LocationType
    flag: RuleFlag = RuleFlag.NONE
    description: str = ""
    """Detailed description of location."""

    @property
    def address(self) -> int:
        """The unique ID used by archipelago for this location"""

        if self.type == LocationType.LAIR:
            return BASE_ID + LAIR_ID_OFFSET + self.id
        if self.type == LocationType.NPC_REWARD:
            return BASE_ID + NPC_REWARD_OFFSET + self.id
        return BASE_ID + self.id

@dataclass(frozen=True)
class SoulBlazerLocationsData(YAMLWizard):
    chests: list[SoulBlazerLocationData]
    lairs: list[SoulBlazerLocationData]
    npc_rewards: list[SoulBlazerLocationData]


chests: list[SoulBlazerLocationData] = [
    SoulBlazerLocationData(int(ChestID.TRIAL_ROOM                    ), ChestName.TRIAL_ROOM                     , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.GRASS_VALLEY_SECRET_CAVE_LEFT ), ChestName.GRASS_VALLEY_SECRET_CAVE_LEFT  , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.GRASS_VALLEY_SECRET_CAVE_RIGHT), ChestName.GRASS_VALLEY_SECRET_CAVE_RIGHT , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.UNDERGROUND_CASTLE_12GEM      ), ChestName.UNDERGROUND_CASTLE_12GEM       , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.UNDERGROUND_CASTLE_HERB       ), ChestName.UNDERGROUND_CASTLE_HERB        , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.UNDERGROUND_CASTLE_DREAM_ROD  ), ChestName.UNDERGROUND_CASTLE_DREAM_ROD   , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.UNDERGROUND_CASTLE_LEOS_BRUSH ), ChestName.UNDERGROUND_CASTLE_LEOS_BRUSH  , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.LEOS_PAINTING_HERB            ), ChestName.LEOS_PAINTING_HERB             , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.LEOS_PAINTING_TORNADO         ), ChestName.LEOS_PAINTING_TORNADO          , LocationType.CHEST, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(ChestID.GREENWOOD_ICE_ARMOR           ), ChestName.GREENWOOD_ICE_ARMOR            , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.GREENWOOD_TUNNELS             ), ChestName.GREENWOOD_TUNNELS              , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.WATER_SHRINE_1                ), ChestName.WATER_SHRINE_1                 , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.WATER_SHRINE_2_N              ), ChestName.WATER_SHRINE_2_N               , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.WATER_SHRINE_2_HERB           ), ChestName.WATER_SHRINE_2_HERB            , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.WATER_SHRINE_3_SW             ), ChestName.WATER_SHRINE_3_SW              , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.WATER_SHRINE_3_SE             ), ChestName.WATER_SHRINE_3_SE              , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.FIRE_SHRINE_1                 ), ChestName.FIRE_SHRINE_1                  , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.FIRE_SHRINE_2_DISAPPEARING    ), ChestName.FIRE_SHRINE_2_DISAPPEARING     , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.FIRE_SHRINE_2_SCORPION        ), ChestName.FIRE_SHRINE_2_SCORPION         , LocationType.CHEST, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(ChestID.FIRE_SHRINE_3_100GEM          ), ChestName.FIRE_SHRINE_3_100GEM           , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.FIRE_SHRINE_3_60GEM           ), ChestName.FIRE_SHRINE_3_60GEM            , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.LIGHT_SHRINE                  ), ChestName.LIGHT_SHRINE                   , LocationType.CHEST, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(ChestID.ST_ELLIS_MERMAIDS_TEARS       ), ChestName.ST_ELLIS_MERMAIDS_TEARS        , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.ST_ELLIS_BIG_PEARL            ), ChestName.ST_ELLIS_BIG_PEARL             , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.SEABED_SECRET_TL              ), ChestName.SEABED_SECRET_TL               , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.SEABED_SECRET_TR              ), ChestName.SEABED_SECRET_TR               , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.SEABED_SECRET_BL              ), ChestName.SEABED_SECRET_BL               , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.SEABED_SECRET_BR              ), ChestName.SEABED_SECRET_BR               , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.SOUTHERTA                     ), ChestName.SOUTHERTA                      , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.ROCKBIRD_HERB                 ), ChestName.ROCKBIRD_HERB                  , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.ROCKBIRD_60GEM                ), ChestName.ROCKBIRD_60GEM                 , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.DUREAN_CRITICAL_SWORD         ), ChestName.DUREAN_CRITICAL_SWORD          , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.DUREAN_STRANGE_BOTTLE         ), ChestName.DUREAN_STRANGE_BOTTLE          , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.GHOST_SHIP                    ), ChestName.GHOST_SHIP                     , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.SEABED_POWER_BRACELET         ), ChestName.SEABED_POWER_BRACELET          , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MOUNTAIN_OF_SOULS_1           ), ChestName.MOUNTAIN_OF_SOULS_1            , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MOUNTAIN_OF_SOULS_2_LL        ), ChestName.MOUNTAIN_OF_SOULS_2_LL         , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MOUNTAIN_OF_SOULS_2_L         ), ChestName.MOUNTAIN_OF_SOULS_2_L          , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MOUNTAIN_OF_SOULS_2_R         ), ChestName.MOUNTAIN_OF_SOULS_2_R          , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MOUNTAIN_OF_SOULS_2_RR        ), ChestName.MOUNTAIN_OF_SOULS_2_RR         , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.LAYNOLE_LUCKY_BLADE           ), ChestName.LAYNOLE_LUCKY_BLADE            , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.LAYNOLE_HERB                  ), ChestName.LAYNOLE_HERB                   , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.LAYNOLE_ROTATOR               ), ChestName.LAYNOLE_ROTATOR                , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.LEOS_LAB_ZANTETSU             ), ChestName.LEOS_LAB_ZANTETSU              , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.POWER_PLANT_LIGHT_ARMOR       ), ChestName.POWER_PLANT_LIGHT_ARMOR        , LocationType.CHEST, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(ChestID.MODEL_TOWN_1_SE               ), ChestName.MODEL_TOWN_1_SE                , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MODEL_TOWN_1_NL               ), ChestName.MODEL_TOWN_1_NL                , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MODEL_TOWN_1_NR               ), ChestName.MODEL_TOWN_1_NR                , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MODEL_TOWN_2_TOP              ), ChestName.MODEL_TOWN_2_TOP               , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.MODEL_TOWN_2_BOT              ), ChestName.MODEL_TOWN_2_BOT               , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_BASEMENT_1_W           ), ChestName.CASTLE_BASEMENT_1_W            , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_BASEMENT_1_SPIRIT_SWORD), ChestName.CASTLE_BASEMENT_1_SPIRIT_SWORD , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_BASEMENT_2_N           ), ChestName.CASTLE_BASEMENT_2_N            , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_BASEMENT_2_SW          ), ChestName.CASTLE_BASEMENT_2_SW           , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_BASEMENT_2_MIDDLE      ), ChestName.CASTLE_BASEMENT_2_MIDDLE       , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_BASEMENT_3             ), ChestName.CASTLE_BASEMENT_3              , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_RIGHT_TOWER_2_L        ), ChestName.CASTLE_RIGHT_TOWER_2_L         , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_RIGHT_TOWER_2_R        ), ChestName.CASTLE_RIGHT_TOWER_2_R         , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_RIGHT_TOWER_3_TL       ), ChestName.CASTLE_RIGHT_TOWER_3_TL        , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.CASTLE_RIGHT_TOWER_3_BR       ), ChestName.CASTLE_RIGHT_TOWER_3_BR        , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.WOE_1_SE                      ), ChestName.WOE_1_SE                       , LocationType.CHEST, RuleFlag.HAS_MAGIC),
    SoulBlazerLocationData(int(ChestID.WOE_1_SW                      ), ChestName.WOE_1_SW                       , LocationType.CHEST, RuleFlag.HAS_MAGIC),
    SoulBlazerLocationData(int(ChestID.WOE_1_REDHOT_BALL             ), ChestName.WOE_1_REDHOT_BALL              , LocationType.CHEST, RuleFlag.HAS_MAGIC),
    SoulBlazerLocationData(int(ChestID.WOE_2                         ), ChestName.WOE_2                          , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.DAZZLING_SPACE_SE             ), ChestName.DAZZLING_SPACE_SE              , LocationType.CHEST),
    SoulBlazerLocationData(int(ChestID.DAZZLING_SPACE_SW             ), ChestName.DAZZLING_SPACE_SW              , LocationType.CHEST),
]

lairs: list[SoulBlazerLocationData] = [
    SoulBlazerLocationData(int(LairID.OLD_WOMAN                    ), LairName.OLD_WOMAN                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.TOOL_SHOP_OWNER              ), LairName.TOOL_SHOP_OWNER               , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.TULIP                        ), LairName.TULIP                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BRIDGE_GUARD                 ), LairName.BRIDGE_GUARD                  , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.VILLAGE_CHIEF                ), LairName.VILLAGE_CHIEF                 , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.IVY_CHEST_ROOM               ), LairName.IVY_CHEST_ROOM                , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.WATER_MILL                   ), LairName.WATER_MILL                    , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GOAT_HERB                    ), LairName.GOAT_HERB                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.LISA                         ), LairName.LISA                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.TULIP2                       ), LairName.TULIP2                        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.ARCHITECT                    ), LairName.ARCHITECT                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.IVY                          ), LairName.IVY                           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GOAT                         ), LairName.GOAT                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.TEDDY                        ), LairName.TEDDY                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.TULIP3                       ), LairName.TULIP3                        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.LEOS_HOUSE                   ), LairName.LEOS_HOUSE                    , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.LONELY_GOAT                  ), LairName.LONELY_GOAT                   , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.TULIP_PASS                   ), LairName.TULIP_PASS                    , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BOY_CABIN                    ), LairName.BOY_CABIN                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BOY_CAVE                     ), LairName.BOY_CAVE                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.OLD_MAN                      ), LairName.OLD_MAN                       , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.OLD_MAN2                     ), LairName.OLD_MAN2                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.IVY2                         ), LairName.IVY2                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.IVY_EMBLEM_A                 ), LairName.IVY_EMBLEM_A                  , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.IVY_RECOVERY_SWORD           ), LairName.IVY_RECOVERY_SWORD            , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.TULIP4                       ), LairName.TULIP4                        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GOAT2                        ), LairName.GOAT2                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BIRD_RED_HOT_MIRROR          ), LairName.BIRD_RED_HOT_MIRROR           , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.BIRD                         ), LairName.BIRD                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOG                          ), LairName.DOG                           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOG2                         ), LairName.DOG2                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOG3                         ), LairName.DOG3                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOLE_SHIELD_BRACELET         ), LairName.MOLE_SHIELD_BRACELET          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SQUIRREL_EMBLEM_C            ), LairName.SQUIRREL_EMBLEM_C             , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SQUIRREL_PSYCHO_SWORD        ), LairName.SQUIRREL_PSYCHO_SWORD         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BIRD2                        ), LairName.BIRD2                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOLE_SOUL_OF_LIGHT           ), LairName.MOLE_SOUL_OF_LIGHT            , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DEER                         ), LairName.DEER                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.CROCODILE                    ), LairName.CROCODILE                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SQUIRREL                     ), LairName.SQUIRREL                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GREENWOODS_GUARDIAN          ), LairName.GREENWOODS_GUARDIAN           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOLE                         ), LairName.MOLE                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOG4                         ), LairName.DOG4                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SQUIRREL_ICE_ARMOR           ), LairName.SQUIRREL_ICE_ARMOR            , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SQUIRREL2                    ), LairName.SQUIRREL2                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOG5                         ), LairName.DOG5                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.CROCODILE2                   ), LairName.CROCODILE2                    , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOLE2                        ), LairName.MOLE2                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SQUIRREL3                    ), LairName.SQUIRREL3                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BIRD_GREENWOOD_LEAF          ), LairName.BIRD_GREENWOOD_LEAF           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOLE3                        ), LairName.MOLE3                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DEER_MAGIC_BELL              ), LairName.DEER_MAGIC_BELL               , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BIRD3                        ), LairName.BIRD3                         , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.CROCODILE3                   ), LairName.CROCODILE3                    , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MONMO                        ), LairName.MONMO                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOLPHIN                      ), LairName.DOLPHIN                       , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.ANGELFISH                    ), LairName.ANGELFISH                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID                      ), LairName.MERMAID                       , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.ANGELFISH2                   ), LairName.ANGELFISH2                    , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_PEARL                ), LairName.MERMAID_PEARL                 , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID2                     ), LairName.MERMAID2                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOLPHIN_SAVES_LUE            ), LairName.DOLPHIN_SAVES_LUE             , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_STATUE_BLESTER       ), LairName.MERMAID_STATUE_BLESTER        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_RED_HOT_STICK        ), LairName.MERMAID_RED_HOT_STICK         , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.LUE                          ), LairName.LUE                           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID3                     ), LairName.MERMAID3                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_NANA                 ), LairName.MERMAID_NANA                  , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID4                     ), LairName.MERMAID4                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOLPHIN2                     ), LairName.DOLPHIN2                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_STATUE_ROCKBIRD      ), LairName.MERMAID_STATUE_ROCKBIRD       , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_BUBBLE_ARMOR         ), LairName.MERMAID_BUBBLE_ARMOR          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID5                     ), LairName.MERMAID5                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID6                     ), LairName.MERMAID6                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_TEARS                ), LairName.MERMAID_TEARS                 , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_STATUE_DUREAN        ), LairName.MERMAID_STATUE_DUREAN         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.ANGELFISH3                   ), LairName.ANGELFISH3                    , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.ANGELFISH_SOUL_OF_SHIELD     ), LairName.ANGELFISH_SOUL_OF_SHIELD      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_MAGIC_FLARE          ), LairName.MERMAID_MAGIC_FLARE           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_QUEEN                ), LairName.MERMAID_QUEEN                 , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID_STATUE_GHOST_SHIP    ), LairName.MERMAID_STATUE_GHOST_SHIP     , LocationType.LAIR, RuleFlag.HAS_THUNDER),
    SoulBlazerLocationData(int(LairID.DOLPHIN_SECRET_CAVE          ), LairName.DOLPHIN_SECRET_CAVE           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID7                     ), LairName.MERMAID7                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.ANGELFISH4                   ), LairName.ANGELFISH4                    , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID8                     ), LairName.MERMAID8                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DOLPHIN_PEARL                ), LairName.DOLPHIN_PEARL                 , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MERMAID9                     ), LairName.MERMAID9                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GRANDPA                      ), LairName.GRANDPA                       , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GIRL                         ), LairName.GIRL                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MUSHROOM                     ), LairName.MUSHROOM                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BOY                          ), LairName.BOY                           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GRANDPA2                     ), LairName.GRANDPA2                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SNAIL_JOCKEY                 ), LairName.SNAIL_JOCKEY                  , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.NOME                         ), LairName.NOME                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BOY2                         ), LairName.BOY2                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MUSHROOM_EMBLEM_F            ), LairName.MUSHROOM_EMBLEM_F             , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DANCING_GRANDMA              ), LairName.DANCING_GRANDMA               , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DANCING_GRANDMA2             ), LairName.DANCING_GRANDMA2              , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SNAIL_EMBLEM_E               ), LairName.SNAIL_EMBLEM_E                , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.BOY_MUSHROOM_SHOES           ), LairName.BOY_MUSHROOM_SHOES            , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GRANDMA                      ), LairName.GRANDMA                       , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GIRL2                        ), LairName.GIRL2                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MUSHROOM2                    ), LairName.MUSHROOM2                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SNAIL_RACER                  ), LairName.SNAIL_RACER                   , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SNAIL_RACER2                 ), LairName.SNAIL_RACER2                  , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GIRL3                        ), LairName.GIRL3                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MUSHROOM3                    ), LairName.MUSHROOM3                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SNAIL                        ), LairName.SNAIL                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GRANDPA3                     ), LairName.GRANDPA3                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SNAIL2                       ), LairName.SNAIL2                        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GRANDPA4                     ), LairName.GRANDPA4                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GRANDPA_LUNE                 ), LairName.GRANDPA_LUNE                  , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GRANDPA5                     ), LairName.GRANDPA5                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOUNTAIN_KING                ), LairName.MOUNTAIN_KING                 , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.PLANT_HERB                   ), LairName.PLANT_HERB                    , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.PLANT                        ), LairName.PLANT                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.CHEST_OF_DRAWERS_MYSTIC_ARMOR), LairName.CHEST_OF_DRAWERS_MYSTIC_ARMOR , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.CAT                          ), LairName.CAT                           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GREAT_DOOR_ZANTETSU_SWORD    ), LairName.GREAT_DOOR_ZANTETSU_SWORD     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.CAT2                         ), LairName.CAT2                          , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.GREAT_DOOR                   ), LairName.GREAT_DOOR                    , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.CAT3                         ), LairName.CAT3                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MODEL_TOWN1                  ), LairName.MODEL_TOWN1                   , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.GREAT_DOOR_MODEL_TOWNS       ), LairName.GREAT_DOOR_MODEL_TOWNS        , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.STEPS_UPSTAIRS               ), LairName.STEPS_UPSTAIRS                , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.CAT_DOOR_KEY                 ), LairName.CAT_DOOR_KEY                  , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOUSE                        ), LairName.MOUSE                         , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.MARIE                        ), LairName.MARIE                         , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.DOLL                         ), LairName.DOLL                          , LocationType.LAIR, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(LairID.CHEST_OF_DRAWERS             ), LairName.CHEST_OF_DRAWERS              , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.PLANT2                       ), LairName.PLANT2                        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOUSE2                       ), LairName.MOUSE2                        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOUSE_SPARK_BOMB             ), LairName.MOUSE_SPARK_BOMB              , LocationType.LAIR, RuleFlag.HAS_MAGIC),
    SoulBlazerLocationData(int(LairID.MOUSE3                       ), LairName.MOUSE3                        , LocationType.LAIR, RuleFlag.HAS_MAGIC),
    SoulBlazerLocationData(int(LairID.GREAT_DOOR_SOUL_OF_DETECTION ), LairName.GREAT_DOOR_SOUL_OF_DETECTION  , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MODEL_TOWN2                  ), LairName.MODEL_TOWN2                   , LocationType.LAIR, RuleFlag.HAS_MAGIC),
    SoulBlazerLocationData(int(LairID.MOUSE4                       ), LairName.MOUSE4                        , LocationType.LAIR, RuleFlag.HAS_MAGIC),
    SoulBlazerLocationData(int(LairID.STEPS_MARIE                  ), LairName.STEPS_MARIE                   , LocationType.LAIR, RuleFlag.HAS_MAGIC),
    SoulBlazerLocationData(int(LairID.CHEST_OF_DRAWERS2            ), LairName.CHEST_OF_DRAWERS2             , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.PLANT_ACTINIDIA_LEAVES       ), LairName.PLANT_ACTINIDIA_LEAVES        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MOUSE5                       ), LairName.MOUSE5                        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.CAT4                         ), LairName.CAT4                          , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.STAIRS_POWER_PLANT           ), LairName.STAIRS_POWER_PLANT            , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER                      ), LairName.SOLDIER                       , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER2                     ), LairName.SOLDIER2                      , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.SOLDIER3                     ), LairName.SOLDIER3                      , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.SOLDIER_ELEMENTAL_MAIL       ), LairName.SOLDIER_ELEMENTAL_MAIL        , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.SOLDIER4                     ), LairName.SOLDIER4                      , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.SOLDIER5                     ), LairName.SOLDIER5                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SINGER_CONCERT_HALL          ), LairName.SINGER_CONCERT_HALL           , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.SOLDIER6                     ), LairName.SOLDIER6                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MAID                         ), LairName.MAID                          , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.SOLDIER_LEFT_TOWER           ), LairName.SOLDIER_LEFT_TOWER            , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER_DOK                  ), LairName.SOLDIER_DOK                   , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER_PLATINUM_CARD        ), LairName.SOLDIER_PLATINUM_CARD         , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.SINGER                       ), LairName.SINGER                        , LocationType.LAIR, RuleFlag.CAN_CUT_SPIRIT),
    SoulBlazerLocationData(int(LairID.SOLDIER_SOUL_OF_REALITY      ), LairName.SOLDIER_SOUL_OF_REALITY       , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MAID2                        ), LairName.MAID2                         , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.QUEEN_MAGRIDD                ), LairName.QUEEN_MAGRIDD                 , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER_WITH_LEO             ), LairName.SOLDIER_WITH_LEO              , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER_RIGHT_TOWER          ), LairName.SOLDIER_RIGHT_TOWER           , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.DR_LEO                       ), LairName.DR_LEO                        , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER7                     ), LairName.SOLDIER7                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER8                     ), LairName.SOLDIER8                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.MAID_HERB                    ), LairName.MAID_HERB                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER_CASTLE               ), LairName.SOLDIER_CASTLE                , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER9                     ), LairName.SOLDIER9                      , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER10                    ), LairName.SOLDIER10                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.SOLDIER11                    ), LairName.SOLDIER11                     , LocationType.LAIR),
    SoulBlazerLocationData(int(LairID.KING_MAGRIDD                 ), LairName.KING_MAGRIDD                  , LocationType.LAIR),
]

npc_rewards: list[SoulBlazerLocationData] = [
    SoulBlazerLocationData(int(NPCRewardID.TOOL_SHOP_OWNER                 ), NPCRewardName.TOOL_SHOP_OWNER                  , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.EMBLEM_A_TILE                   ), NPCRewardName.EMBLEM_A_TILE                    , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.GOAT_PEN_CORNER                 ), NPCRewardName.GOAT_PEN_CORNER                  , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.TEDDY                           ), NPCRewardName.TEDDY                            , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.PASS_TILE                       ), NPCRewardName.PASS_TILE                        , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.TILE_IN_CHILDS_SECRET_CAVE      ), NPCRewardName.TILE_IN_CHILDS_SECRET_CAVE       , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.VILLAGE_CHIEF                   ), NPCRewardName.VILLAGE_CHIEF                    , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MAGICIAN                        ), NPCRewardName.MAGICIAN                         , LocationType.NPC_REWARD, RuleFlag.HAS_SWORD),
    SoulBlazerLocationData(int(NPCRewardID.RECOVERY_SWORD_CRYSTAL          ), NPCRewardName.RECOVERY_SWORD_CRYSTAL           , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.GRASS_VALLEY_SECRET_ROOM_CRYSTAL), NPCRewardName.GRASS_VALLEY_SECRET_ROOM_CRYSTAL , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.UNDERGROUND_CASTLE_CRYSTAL      ), NPCRewardName.UNDERGROUND_CASTLE_CRYSTAL       , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.REDHOT_MIRROR_BIRD              ), NPCRewardName.REDHOT_MIRROR_BIRD               , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MAGIC_BELL_CRYSTAL              ), NPCRewardName.MAGIC_BELL_CRYSTAL               , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.WOODSTIN_TRIO                   ), NPCRewardName.WOODSTIN_TRIO                    , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.GREENWOODS_GUARDIAN             ), NPCRewardName.GREENWOODS_GUARDIAN              , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.GREENWOOD_LEAVES_TILE           ), NPCRewardName.GREENWOOD_LEAVES_TILE            , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.SHIELD_BRACELET_MOLE            ), NPCRewardName.SHIELD_BRACELET_MOLE             , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.PSYCHO_SWORD_SQUIRREL           ), NPCRewardName.PSYCHO_SWORD_SQUIRREL            , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.EMBLEM_C_SQUIRREL               ), NPCRewardName.EMBLEM_C_SQUIRREL                , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.WATER_SHRINE_STRANGE_BOTTLE     ), NPCRewardName.WATER_SHRINE_TILE                , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.LIGHT_ARROW_CRYSTAL             ), NPCRewardName.LIGHT_ARROW_CRYSTAL              , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.LOST_MARSH_CRYSTAL              ), NPCRewardName.LOST_MARSH_CRYSTAL               , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.WATER_SHRINE_CRYSTAL            ), NPCRewardName.WATER_SHRINE_CRYSTAL             , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.FIRE_SHRINE_CRYSTAL             ), NPCRewardName.FIRE_SHRINE_CRYSTAL              , LocationType.NPC_REWARD, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(NPCRewardID.MOUNTAIN_KING                   ), NPCRewardName.MOUNTAIN_KING                    , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MUSHROOM_SHOES_BOY              ), NPCRewardName.MUSHROOM_SHOES_BOY               , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.NOME                            ), NPCRewardName.NOME                             , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.EMBLEM_E_SNAIL                  ), NPCRewardName.EMBLEM_E_SNAIL                   , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.EMBLEM_F_TILE                   ), NPCRewardName.EMBLEM_F_TILE                    , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MOUNTAIN_OF_SOULS_CRYSTAL       ), NPCRewardName.MOUNTAIN_OF_SOULS_CRYSTAL        , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.LUNE_CRYSTAL                    ), NPCRewardName.LUNE_CRYSTAL                     , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.EMBLEM_G_UNDER_CHEST_OF_DRAWERS ), NPCRewardName.EMBLEM_G_UNDER_CHEST_OF_DRAWERS  , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.CHEST_OF_DRAWERS_MYSTIC_ARMOR   ), NPCRewardName.CHEST_OF_DRAWERS_MYSTIC_ARMOR    , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.HERB_PLANT_IN_LEOS_LAB          ), NPCRewardName.HERB_PLANT_IN_LEOS_LAB           , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.LEOS_CAT_DOOR_KEY               ), NPCRewardName.LEOS_CAT_DOOR_KEY                , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.ACTINIDIA_PLANT                 ), NPCRewardName.ACTINIDIA_PLANT                  , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.CHEST_OF_DRAWERS_HERB           ), NPCRewardName.CHEST_OF_DRAWERS_HERB            , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MARIE                           ), NPCRewardName.MARIE                            , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.SPARK_BOMB_MOUSE                ), NPCRewardName.SPARK_BOMB_MOUSE                 , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.LEOS_LAB_BASEMENT_CRYSTAL       ), NPCRewardName.LEOS_LAB_BASEMENT_CRYSTAL        , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MODEL_TOWN_1_CRYSTAL            ), NPCRewardName.MODEL_TOWN_1_CRYSTAL             , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.POWER_PLANT_CRYSTAL             ), NPCRewardName.POWER_PLANT_CRYSTAL              , LocationType.NPC_REWARD, RuleFlag.CAN_CUT_METAL),
    SoulBlazerLocationData(int(NPCRewardID.ELEMENTAL_MAIL_SOLDIER          ), NPCRewardName.ELEMENTAL_MAIL_SOLDIER           , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.SUPER_BRACELET_TILE             ), NPCRewardName.SUPER_BRACELET_TILE              , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.QUEEN_MAGRIDD_VIP_CARD          ), NPCRewardName.QUEEN_MAGRIDD_VIP_CARD           , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.PLATINUM_CARD_SOLDIER           ), NPCRewardName.PLATINUM_CARD_SOLDIER            , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MAID_HERB                       ), NPCRewardName.MAID_HERB                        , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.EMBLEM_H_TILE                   ), NPCRewardName.EMBLEM_H_TILE                    , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.KING_MAGRIDD                    ), NPCRewardName.KING_MAGRIDD                     , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.LEO_ON_THE_AIRSHIP_DECK         ), NPCRewardName.LEO_ON_THE_AIRSHIP_DECK          , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.HARP_STRING_TILE                ), NPCRewardName.HARP_STRING_TILE                 , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.NORTHEASTERN_MERMAID_HERB       ), NPCRewardName.NORTHEASTERN_MERMAID_HERB        , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.BUBBLE_ARMOR_MERMAID            ), NPCRewardName.BUBBLE_ARMOR_MERMAID             , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MAGIC_FLARE_MERMAID             ), NPCRewardName.MAGIC_FLARE_MERMAID              , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MERMAID_QUEEN                   ), NPCRewardName.MERMAID_QUEEN                    , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.REDHOT_STICK_MERMAID            ), NPCRewardName.REDHOT_STICK_MERMAID             , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.LUE                             ), NPCRewardName.LUE                              , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.ROCKBIRD_CRYSTAL                ), NPCRewardName.ROCKBIRD_CRYSTAL                 , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.SEABED_CRYSTAL_NEAR_BLESTER     ), NPCRewardName.SEABED_CRYSTAL_NEAR_BLESTER      , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.SEABED_CRYSTAL_NEAR_DUREAN      ), NPCRewardName.SEABED_CRYSTAL_NEAR_DUREAN       , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.MAGICIAN_SOUL                   ), NPCRewardName.MAGICIAN_SOUL                    , LocationType.NPC_REWARD, RuleFlag.HAS_SWORD),
    SoulBlazerLocationData(int(NPCRewardID.MOLE_SOUL_OF_LIGHT              ), NPCRewardName.MOLE_SOUL_OF_LIGHT               , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.ANGELFISH_SOUL_OF_SHIELD        ), NPCRewardName.ANGELFISH_SOUL_OF_SHIELD         , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.GREAT_DOOR_SOUL_OF_DETECTION    ), NPCRewardName.GREAT_DOOR_SOUL_OF_DETECTION     , LocationType.NPC_REWARD),
    SoulBlazerLocationData(int(NPCRewardID.SOLDIER_SOUL_OF_REALITY         ), NPCRewardName.SOLDIER_SOUL_OF_REALITY          , LocationType.NPC_REWARD),
]

def dump_location_yaml() -> None:
    locations: SoulBlazerLocationsData = SoulBlazerLocationsData(chests, lairs, npc_rewards)
    yaml = locations.to_yaml_file("worlds/soulblazer/Data/SoulBlazerLocations.yaml")


if __name__ == '__main__':
    dump_location_yaml()
    