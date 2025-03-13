from dataclasses import dataclass, replace
from dataclass_wizard import YAMLWizard
from BaseClasses import ItemClassification
from .Enums import ItemID, IDOffset, LairID
from ..Util import int_to_bcd
from ..Names import ItemName, NPCName

@dataclass(frozen=True)
class SoulBlazerItemData:
    aname: str
    """String representation of the item"""

    bid: int
    """Internal item ID"""

    coperand: int
    """Either Gems/Exp Quantity or Lair ID"""

    dclassification: int

    edescription: str = ""

    def duplicate(self, **changes) -> "SoulBlazerItemData":
        """Returns a copy of this ItemData with the specified changes."""
        return replace(self, **changes)

    @property
    def code(self) -> int:
        """The unique ID used by archipelago for this item"""

        if self.id == ItemID.LAIR_RELEASE:
            return IDOffset.BASE_ID + IDOffset.LAIR_ID_OFFSET + self.operand
        elif self.id == ItemID.SOUL:
            return IDOffset.BASE_ID + IDOffset.SOUL_OFFSET + self.operand
        return IDOffset.BASE_ID + self.id

    @property
    def operand_bcd(self) -> int:
        return int_to_bcd(self.operand)

    @property
    def operand_for_id(self) -> int:
        if self.id == ItemID.GEMS or self.id == ItemID.EXP:
            return self.operand_bcd
        return self.operand
    
@dataclass(frozen=True)
class SoulBlazerItemsData(YAMLWizard):
    aswords: list[SoulBlazerItemData]
    barmors: list[SoulBlazerItemData]
    cmagics: list[SoulBlazerItemData]
    dinventory_items: list[SoulBlazerItemData]
    emisc_items: list[SoulBlazerItemData]
    fnpc_releases: list[SoulBlazerItemData]
    gsouls: list[SoulBlazerItemData]
    hspecial_items: list[SoulBlazerItemData]

    @property
    def all_items(self) -> list[SoulBlazerItemData]:
        return [*self.swords, *self.armors, *self.magics, *self.inventory_items, *self.misc_items, *self.npc_releases, *self.souls, *self.special_items]


swords_table = [
    SoulBlazerItemData(ItemName.LIFESWORD    , int(ItemID.LIFESWORD    ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.PSYCHOSWORD  , int(ItemID.PSYCHOSWORD  ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.CRITICALSWORD, int(ItemID.CRITICALSWORD), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.LUCKYBLADE   , int(ItemID.LUCKYBLADE   ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.ZANTETSUSWORD, int(ItemID.ZANTETSUSWORD), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.SPIRITSWORD  , int(ItemID.SPIRITSWORD  ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.RECOVERYSWORD, int(ItemID.RECOVERYSWORD), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.SOULBLADE    , int(ItemID.SOULBLADE    ), 0x00, int(ItemClassification.progression)),
]

armors_table = [
    SoulBlazerItemData(ItemName.IRONARMOR     , int(ItemID.IRONARMOR     ), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.ICEARMOR      , int(ItemID.ICEARMOR      ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.BUBBLEARMOR   , int(ItemID.BUBBLEARMOR   ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.MAGICARMOR    , int(ItemID.MAGICARMOR    ), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.MYSTICARMOR   , int(ItemID.MYSTICARMOR   ), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.LIGHTARMOR    , int(ItemID.LIGHTARMOR    ), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.ELEMENTALARMOR, int(ItemID.ELEMENTALARMOR), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.SOULARMOR     , int(ItemID.SOULARMOR     ), 0x00, int(ItemClassification.progression)),
]

castable_magic_table = [
    SoulBlazerItemData(ItemName.FLAMEBALL  , int(ItemID.FLAMEBALL  ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.LIGHTARROW , int(ItemID.LIGHTARROW ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.MAGICFLARE , int(ItemID.MAGICFLARE ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.ROTATOR    , int(ItemID.ROTATOR    ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.SPARKBOMB  , int(ItemID.SPARKBOMB  ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.FLAMEPILLAR, int(ItemID.FLAMEPILLAR), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.TORNADO    , int(ItemID.TORNADO    ), 0x00, int(ItemClassification.progression)),
]

magic_table = [
    *castable_magic_table,
    SoulBlazerItemData(ItemName.PHOENIX, int(ItemID.PHOENIX    ), 0x00, int(ItemClassification.progression)),
]

emblems_table = [
    SoulBlazerItemData(ItemName.EMBLEMA, int(ItemID.EMBLEMA), 0x00, int(ItemClassification.progression_skip_balancing)),
    SoulBlazerItemData(ItemName.EMBLEMB, int(ItemID.EMBLEMB), 0x00, int(ItemClassification.progression_skip_balancing)),
    SoulBlazerItemData(ItemName.EMBLEMC, int(ItemID.EMBLEMC), 0x00, int(ItemClassification.progression_skip_balancing)),
    SoulBlazerItemData(ItemName.EMBLEMD, int(ItemID.EMBLEMD), 0x00, int(ItemClassification.progression_skip_balancing)),
    SoulBlazerItemData(ItemName.EMBLEME, int(ItemID.EMBLEME), 0x00, int(ItemClassification.progression_skip_balancing)),
    SoulBlazerItemData(ItemName.EMBLEMF, int(ItemID.EMBLEMF), 0x00, int(ItemClassification.progression_skip_balancing)),
    SoulBlazerItemData(ItemName.EMBLEMG, int(ItemID.EMBLEMG), 0x00, int(ItemClassification.progression_skip_balancing)),
    SoulBlazerItemData(ItemName.EMBLEMH, int(ItemID.EMBLEMH), 0x00, int(ItemClassification.progression_skip_balancing)),
]

redhots_table = [
    SoulBlazerItemData(ItemName.REDHOTMIRROR, int(ItemID.REDHOTMIRROR), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.REDHOTBALL  , int(ItemID.REDHOTBALL  ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.REDHOTSTICK , int(ItemID.REDHOTSTICK ), 0x00, int(ItemClassification.progression)),
]

stones_table = [
    SoulBlazerItemData(ItemName.BROWNSTONE , int(ItemID.BROWNSTONE ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.GREENSTONE , int(ItemID.GREENSTONE ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.BLUESTONE  , int(ItemID.BLUESTONE  ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.SILVERSTONE, int(ItemID.SILVERSTONE), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.PURPLESTONE, int(ItemID.PURPLESTONE), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.BLACKSTONE , int(ItemID.BLACKSTONE ), 0x00, int(ItemClassification.progression)),
]

inventory_items_table = [
    SoulBlazerItemData(ItemName.GOATSFOOD      , int(ItemID.GOATSFOOD      ), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.HARPSTRING     , int(ItemID.HARPSTRING     ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.APASS          , int(ItemID.APASS          ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.DREAMROD       , int(ItemID.DREAMROD       ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.LEOSBRUSH      , int(ItemID.LEOSBRUSH      ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.TURBOSLEAVES   , int(ItemID.TURBOSLEAVES   ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.MOLESRIBBON    , int(ItemID.MOLESRIBBON    ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.BIGPEARL       , int(ItemID.BIGPEARL       ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.MERMAIDSTEARS  , int(ItemID.MERMAIDSTEARS  ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.MUSHROOMSHOES  , int(ItemID.MUSHROOMSHOES  ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.AIRSHIPKEY     , int(ItemID.AIRSHIPKEY     ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.THUNDERRING    , int(ItemID.THUNDERRING    ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.DELICIOUSSEEDS , int(ItemID.DELICIOUSSEEDS ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.ACTINIDIALEAVES, int(ItemID.ACTINIDIALEAVES), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.DOORKEY        , int(ItemID.DOORKEY        ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.PLATINUMCARD   , int(ItemID.PLATINUMCARD   ), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.VIPCARD        , int(ItemID.VIPCARD        ), 0x00, int(ItemClassification.progression)),
    *emblems_table,
    *redhots_table,
    SoulBlazerItemData(ItemName.POWERBRACELET , int(ItemID.POWERBRACELET  ), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.SHIELDBRACELET, int(ItemID.SHIELDBRACELET ), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.SUPERBRACELET , int(ItemID.SUPERBRACELET  ), 0x00, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.MEDICALHERB   , int(ItemID.MEDICALHERB    ), 0x00, int(ItemClassification.filler)),
    SoulBlazerItemData(ItemName.STRANGEBOTTLE , int(ItemID.STRANGEBOTTLE  ), 0x00, int(ItemClassification.filler)),
    *stones_table,
    SoulBlazerItemData(ItemName.MAGICBELL, int(ItemID.MAGICBELL      ), 0x00, int(ItemClassification.useful)),
]


misc_table = [
    SoulBlazerItemData(ItemName.NOTHING, int(ItemID.NOTHING), 0x00, int(ItemClassification.filler)),
    SoulBlazerItemData(ItemName.GEMS   , int(ItemID.GEMS   ), 100 , int(ItemClassification.filler)),
    SoulBlazerItemData(ItemName.EXP    , int(ItemID.EXP    ), 250 , int(ItemClassification.filler)),
]

# repeatable_items_table = {
#     ItemName.MEDICALHERB   : inventory_items_table[ItemName.MEDICALHERB],
#     ItemName.STRANGEBOTTLE : inventory_items_table[ItemName.STRANGEBOTTLE],
#     **misc_table,
# }

items_table = [
    *swords_table,
    *armors_table,
    *magic_table,
    *inventory_items_table,
]

npc_release_table = [
    SoulBlazerItemData(NPCName.OLD_WOMAN                    , int(ItemID.LAIR_RELEASE), int(LairID.OLD_WOMAN                    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.TOOL_SHOP_OWNER              , int(ItemID.LAIR_RELEASE), int(LairID.TOOL_SHOP_OWNER              ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.TULIP                        , int(ItemID.LAIR_RELEASE), int(LairID.TULIP                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.BRIDGE_GUARD                 , int(ItemID.LAIR_RELEASE), int(LairID.BRIDGE_GUARD                 ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.VILLAGE_CHIEF                , int(ItemID.LAIR_RELEASE), int(LairID.VILLAGE_CHIEF                ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.IVY_CHEST_ROOM               , int(ItemID.LAIR_RELEASE), int(LairID.IVY_CHEST_ROOM               ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.WATER_MILL                   , int(ItemID.LAIR_RELEASE), int(LairID.WATER_MILL                   ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GOAT_HERB                    , int(ItemID.LAIR_RELEASE), int(LairID.GOAT_HERB                    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.LISA                         , int(ItemID.LAIR_RELEASE), int(LairID.LISA                         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.TULIP2                       , int(ItemID.LAIR_RELEASE), int(LairID.TULIP2                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.ARCHITECT                    , int(ItemID.LAIR_RELEASE), int(LairID.ARCHITECT                    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.IVY                          , int(ItemID.LAIR_RELEASE), int(LairID.IVY                          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GOAT                         , int(ItemID.LAIR_RELEASE), int(LairID.GOAT                         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.TEDDY                        , int(ItemID.LAIR_RELEASE), int(LairID.TEDDY                        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.TULIP3                       , int(ItemID.LAIR_RELEASE), int(LairID.TULIP3                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.LEOS_HOUSE                   , int(ItemID.LAIR_RELEASE), int(LairID.LEOS_HOUSE                   ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.LONELY_GOAT                  , int(ItemID.LAIR_RELEASE), int(LairID.LONELY_GOAT                  ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.TULIP_PASS                   , int(ItemID.LAIR_RELEASE), int(LairID.TULIP_PASS                   ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.BOY_CABIN                    , int(ItemID.LAIR_RELEASE), int(LairID.BOY_CABIN                    ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.BOY_CAVE                     , int(ItemID.LAIR_RELEASE), int(LairID.BOY_CAVE                     ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.OLD_MAN                      , int(ItemID.LAIR_RELEASE), int(LairID.OLD_MAN                      ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.OLD_MAN2                     , int(ItemID.LAIR_RELEASE), int(LairID.OLD_MAN2                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.IVY2                         , int(ItemID.LAIR_RELEASE), int(LairID.IVY2                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.IVY_EMBLEM_A                 , int(ItemID.LAIR_RELEASE), int(LairID.IVY_EMBLEM_A                 ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.IVY_RECOVERY_SWORD           , int(ItemID.LAIR_RELEASE), int(LairID.IVY_RECOVERY_SWORD           ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.TULIP4                       , int(ItemID.LAIR_RELEASE), int(LairID.TULIP4                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.GOAT2                        , int(ItemID.LAIR_RELEASE), int(LairID.GOAT2                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.BIRD_RED_HOT_MIRROR          , int(ItemID.LAIR_RELEASE), int(LairID.BIRD_RED_HOT_MIRROR          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.BIRD                         , int(ItemID.LAIR_RELEASE), int(LairID.BIRD                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.DOG                          , int(ItemID.LAIR_RELEASE), int(LairID.DOG                          ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.DOG2                         , int(ItemID.LAIR_RELEASE), int(LairID.DOG2                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.DOG3                         , int(ItemID.LAIR_RELEASE), int(LairID.DOG3                         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOLE_SHIELD_BRACELET         , int(ItemID.LAIR_RELEASE), int(LairID.MOLE_SHIELD_BRACELET         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SQUIRREL_EMBLEM_C            , int(ItemID.LAIR_RELEASE), int(LairID.SQUIRREL_EMBLEM_C            ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SQUIRREL_PSYCHO_SWORD        , int(ItemID.LAIR_RELEASE), int(LairID.SQUIRREL_PSYCHO_SWORD        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.BIRD2                        , int(ItemID.LAIR_RELEASE), int(LairID.BIRD2                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MOLE_SOUL_OF_LIGHT           , int(ItemID.LAIR_RELEASE), int(LairID.MOLE_SOUL_OF_LIGHT           ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DEER                         , int(ItemID.LAIR_RELEASE), int(LairID.DEER                         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.CROCODILE                    , int(ItemID.LAIR_RELEASE), int(LairID.CROCODILE                    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SQUIRREL                     , int(ItemID.LAIR_RELEASE), int(LairID.SQUIRREL                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.GREENWOODS_GUARDIAN          , int(ItemID.LAIR_RELEASE), int(LairID.GREENWOODS_GUARDIAN          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOLE                         , int(ItemID.LAIR_RELEASE), int(LairID.MOLE                         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DOG4                         , int(ItemID.LAIR_RELEASE), int(LairID.DOG4                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SQUIRREL_ICE_ARMOR           , int(ItemID.LAIR_RELEASE), int(LairID.SQUIRREL_ICE_ARMOR           ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SQUIRREL2                    , int(ItemID.LAIR_RELEASE), int(LairID.SQUIRREL2                    ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.DOG5                         , int(ItemID.LAIR_RELEASE), int(LairID.DOG5                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.CROCODILE2                   , int(ItemID.LAIR_RELEASE), int(LairID.CROCODILE2                   ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOLE2                        , int(ItemID.LAIR_RELEASE), int(LairID.MOLE2                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SQUIRREL3                    , int(ItemID.LAIR_RELEASE), int(LairID.SQUIRREL3                    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.BIRD_GREENWOOD_LEAF          , int(ItemID.LAIR_RELEASE), int(LairID.BIRD_GREENWOOD_LEAF          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOLE3                        , int(ItemID.LAIR_RELEASE), int(LairID.MOLE3                        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DEER_MAGIC_BELL              , int(ItemID.LAIR_RELEASE), int(LairID.DEER_MAGIC_BELL              ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.BIRD3                        , int(ItemID.LAIR_RELEASE), int(LairID.BIRD3                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.CROCODILE3                   , int(ItemID.LAIR_RELEASE), int(LairID.CROCODILE3                   ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MONMO                        , int(ItemID.LAIR_RELEASE), int(LairID.MONMO                        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DOLPHIN                      , int(ItemID.LAIR_RELEASE), int(LairID.DOLPHIN                      ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.ANGELFISH                    , int(ItemID.LAIR_RELEASE), int(LairID.ANGELFISH                    ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MERMAID                      , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID                      ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.ANGELFISH2                   , int(ItemID.LAIR_RELEASE), int(LairID.ANGELFISH2                   ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MERMAID_PEARL                , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_PEARL                ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID2                     , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID2                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.DOLPHIN_SAVES_LUE            , int(ItemID.LAIR_RELEASE), int(LairID.DOLPHIN_SAVES_LUE            ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID_STATUE_BLESTER       , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_STATUE_BLESTER       ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID_RED_HOT_STICK        , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_RED_HOT_STICK        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.LUE                          , int(ItemID.LAIR_RELEASE), int(LairID.LUE                          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID3                     , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID3                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MERMAID_NANA                 , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_NANA                 ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MERMAID4                     , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID4                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.DOLPHIN2                     , int(ItemID.LAIR_RELEASE), int(LairID.DOLPHIN2                     ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID_STATUE_ROCKBIRD      , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_STATUE_ROCKBIRD      ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID_BUBBLE_ARMOR         , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_BUBBLE_ARMOR         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID5                     , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID5                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MERMAID6                     , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID6                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MERMAID_TEARS                , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_TEARS                ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MERMAID_STATUE_DUREAN        , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_STATUE_DUREAN        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.ANGELFISH3                   , int(ItemID.LAIR_RELEASE), int(LairID.ANGELFISH3                   ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.ANGELFISH_SOUL_OF_SHIELD     , int(ItemID.LAIR_RELEASE), int(LairID.ANGELFISH_SOUL_OF_SHIELD     ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID_MAGIC_FLARE          , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_MAGIC_FLARE          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID_QUEEN                , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_QUEEN                ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID_STATUE_GHOST_SHIP    , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID_STATUE_GHOST_SHIP    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DOLPHIN_SECRET_CAVE          , int(ItemID.LAIR_RELEASE), int(LairID.DOLPHIN_SECRET_CAVE          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID7                     , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID7                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.ANGELFISH4                   , int(ItemID.LAIR_RELEASE), int(LairID.ANGELFISH4                   ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MERMAID8                     , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID8                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.DOLPHIN_PEARL                , int(ItemID.LAIR_RELEASE), int(LairID.DOLPHIN_PEARL                ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MERMAID9                     , int(ItemID.LAIR_RELEASE), int(LairID.MERMAID9                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.GRANDPA                      , int(ItemID.LAIR_RELEASE), int(LairID.GRANDPA                      ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GIRL                         , int(ItemID.LAIR_RELEASE), int(LairID.GIRL                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MUSHROOM                     , int(ItemID.LAIR_RELEASE), int(LairID.MUSHROOM                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.BOY                          , int(ItemID.LAIR_RELEASE), int(LairID.BOY                          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GRANDPA2                     , int(ItemID.LAIR_RELEASE), int(LairID.GRANDPA2                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SNAIL_JOCKEY                 , int(ItemID.LAIR_RELEASE), int(LairID.SNAIL_JOCKEY                 ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.NOME                         , int(ItemID.LAIR_RELEASE), int(LairID.NOME                         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.BOY2                         , int(ItemID.LAIR_RELEASE), int(LairID.BOY2                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MUSHROOM_EMBLEM_F            , int(ItemID.LAIR_RELEASE), int(LairID.MUSHROOM_EMBLEM_F            ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DANCING_GRANDMA              , int(ItemID.LAIR_RELEASE), int(LairID.DANCING_GRANDMA              ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DANCING_GRANDMA2             , int(ItemID.LAIR_RELEASE), int(LairID.DANCING_GRANDMA2             ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SNAIL_EMBLEM_E               , int(ItemID.LAIR_RELEASE), int(LairID.SNAIL_EMBLEM_E               ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.BOY_MUSHROOM_SHOES           , int(ItemID.LAIR_RELEASE), int(LairID.BOY_MUSHROOM_SHOES           ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GRANDMA                      , int(ItemID.LAIR_RELEASE), int(LairID.GRANDMA                      ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.GIRL2                        , int(ItemID.LAIR_RELEASE), int(LairID.GIRL2                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MUSHROOM2                    , int(ItemID.LAIR_RELEASE), int(LairID.MUSHROOM2                    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SNAIL_RACER                  , int(ItemID.LAIR_RELEASE), int(LairID.SNAIL_RACER                  ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SNAIL_RACER2                 , int(ItemID.LAIR_RELEASE), int(LairID.SNAIL_RACER2                 ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.GIRL3                        , int(ItemID.LAIR_RELEASE), int(LairID.GIRL3                        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MUSHROOM3                    , int(ItemID.LAIR_RELEASE), int(LairID.MUSHROOM3                    ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SNAIL                        , int(ItemID.LAIR_RELEASE), int(LairID.SNAIL                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.GRANDPA3                     , int(ItemID.LAIR_RELEASE), int(LairID.GRANDPA3                     ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SNAIL2                       , int(ItemID.LAIR_RELEASE), int(LairID.SNAIL2                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.GRANDPA4                     , int(ItemID.LAIR_RELEASE), int(LairID.GRANDPA4                     ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GRANDPA_LUNE                 , int(ItemID.LAIR_RELEASE), int(LairID.GRANDPA_LUNE                 ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GRANDPA5                     , int(ItemID.LAIR_RELEASE), int(LairID.GRANDPA5                     ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOUNTAIN_KING                , int(ItemID.LAIR_RELEASE), int(LairID.MOUNTAIN_KING                ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.PLANT_HERB                   , int(ItemID.LAIR_RELEASE), int(LairID.PLANT_HERB                   ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.PLANT                        , int(ItemID.LAIR_RELEASE), int(LairID.PLANT                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.CHEST_OF_DRAWERS_MYSTIC_ARMOR, int(ItemID.LAIR_RELEASE), int(LairID.CHEST_OF_DRAWERS_MYSTIC_ARMOR), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.CAT                          , int(ItemID.LAIR_RELEASE), int(LairID.CAT                          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GREAT_DOOR_ZANTETSU_SWORD    , int(ItemID.LAIR_RELEASE), int(LairID.GREAT_DOOR_ZANTETSU_SWORD    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.CAT2                         , int(ItemID.LAIR_RELEASE), int(LairID.CAT2                         ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GREAT_DOOR                   , int(ItemID.LAIR_RELEASE), int(LairID.GREAT_DOOR                   ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.CAT3                         , int(ItemID.LAIR_RELEASE), int(LairID.CAT3                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MODEL_TOWN1                  , int(ItemID.LAIR_RELEASE), int(LairID.MODEL_TOWN1                  ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.GREAT_DOOR_MODEL_TOWNS       , int(ItemID.LAIR_RELEASE), int(LairID.GREAT_DOOR_MODEL_TOWNS       ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.STEPS_UPSTAIRS               , int(ItemID.LAIR_RELEASE), int(LairID.STEPS_UPSTAIRS               ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.CAT_DOOR_KEY                 , int(ItemID.LAIR_RELEASE), int(LairID.CAT_DOOR_KEY                 ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOUSE                        , int(ItemID.LAIR_RELEASE), int(LairID.MOUSE                        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MARIE                        , int(ItemID.LAIR_RELEASE), int(LairID.MARIE                        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DOLL                         , int(ItemID.LAIR_RELEASE), int(LairID.DOLL                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.CHEST_OF_DRAWERS             , int(ItemID.LAIR_RELEASE), int(LairID.CHEST_OF_DRAWERS             ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.PLANT2                       , int(ItemID.LAIR_RELEASE), int(LairID.PLANT2                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MOUSE2                       , int(ItemID.LAIR_RELEASE), int(LairID.MOUSE2                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MOUSE_SPARK_BOMB             , int(ItemID.LAIR_RELEASE), int(LairID.MOUSE_SPARK_BOMB             ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOUSE3                       , int(ItemID.LAIR_RELEASE), int(LairID.MOUSE3                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.GREAT_DOOR_SOUL_OF_DETECTION , int(ItemID.LAIR_RELEASE), int(LairID.GREAT_DOOR_SOUL_OF_DETECTION ), int(ItemClassification.progression)), 
    SoulBlazerItemData(NPCName.MODEL_TOWN2                  , int(ItemID.LAIR_RELEASE), int(LairID.MODEL_TOWN2                  ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOUSE4                       , int(ItemID.LAIR_RELEASE), int(LairID.MOUSE4                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.STEPS_MARIE                  , int(ItemID.LAIR_RELEASE), int(LairID.STEPS_MARIE                  ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.CHEST_OF_DRAWERS2            , int(ItemID.LAIR_RELEASE), int(LairID.CHEST_OF_DRAWERS2            ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.PLANT_ACTINIDIA_LEAVES       , int(ItemID.LAIR_RELEASE), int(LairID.PLANT_ACTINIDIA_LEAVES       ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MOUSE5                       , int(ItemID.LAIR_RELEASE), int(LairID.MOUSE5                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.CAT4                         , int(ItemID.LAIR_RELEASE), int(LairID.CAT4                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.STAIRS_POWER_PLANT           , int(ItemID.LAIR_RELEASE), int(LairID.STAIRS_POWER_PLANT           ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER                      , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER                      ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER2                     , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER2                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER3                     , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER3                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER_ELEMENTAL_MAIL       , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER_ELEMENTAL_MAIL       ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER4                     , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER4                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER5                     , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER5                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SINGER_CONCERT_HALL          , int(ItemID.LAIR_RELEASE), int(LairID.SINGER_CONCERT_HALL          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER6                     , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER6                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MAID                         , int(ItemID.LAIR_RELEASE), int(LairID.MAID                         ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER_LEFT_TOWER           , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER_LEFT_TOWER           ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER_DOK                  , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER_DOK                  ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER_PLATINUM_CARD        , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER_PLATINUM_CARD        ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SINGER                       , int(ItemID.LAIR_RELEASE), int(LairID.SINGER                       ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER_SOUL_OF_REALITY      , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER_SOUL_OF_REALITY      ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.MAID2                        , int(ItemID.LAIR_RELEASE), int(LairID.MAID2                        ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.QUEEN_MAGRIDD                , int(ItemID.LAIR_RELEASE), int(LairID.QUEEN_MAGRIDD                ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER_WITH_LEO             , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER_WITH_LEO             ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER_RIGHT_TOWER          , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER_RIGHT_TOWER          ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.DR_LEO                       , int(ItemID.LAIR_RELEASE), int(LairID.DR_LEO                       ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER7                     , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER7                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER8                     , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER8                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.MAID_HERB                    , int(ItemID.LAIR_RELEASE), int(LairID.MAID_HERB                    ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER_CASTLE               , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER_CASTLE               ), int(ItemClassification.progression)),
    SoulBlazerItemData(NPCName.SOLDIER9                     , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER9                     ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER10                    , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER10                    ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.SOLDIER11                    , int(ItemID.LAIR_RELEASE), int(LairID.SOLDIER11                    ), int(ItemClassification.filler)),
    SoulBlazerItemData(NPCName.KING_MAGRIDD                 , int(ItemID.LAIR_RELEASE), int(LairID.KING_MAGRIDD                 ), int(ItemClassification.progression)),
]

souls_table = [
    SoulBlazerItemData(ItemName.SOUL_MAGICIAN , int(ItemID.SOUL), 0x00, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.SOUL_LIGHT    , int(ItemID.SOUL), 0x01, int(ItemClassification.progression)),
    SoulBlazerItemData(ItemName.SOUL_SHIELD   , int(ItemID.SOUL), 0x02, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.SOUL_DETECTION, int(ItemID.SOUL), 0x03, int(ItemClassification.useful)),
    SoulBlazerItemData(ItemName.SOUL_REALITY  , int(ItemID.SOUL), 0x04, int(ItemClassification.progression)),
]

special_table = [
    SoulBlazerItemData(ItemName.VICTORY, int(ItemID.VICTORY), 0x00, int(ItemClassification.progression))
]

all_items_table = [
    *items_table,
    *misc_table,
    *npc_release_table,
    *souls_table,
    *special_table,
]

def dump_location_yaml() -> None:
    locations: SoulBlazerItemsData = SoulBlazerItemsData(swords_table, armors_table, magic_table, inventory_items_table, misc_table, npc_release_table, souls_table, special_table )
    yaml = locations.to_yaml_file("worlds/soulblazer/Data/SoulBlazerItems.yaml")


if __name__ == '__main__':
    dump_location_yaml()
    