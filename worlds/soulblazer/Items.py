from dataclasses import dataclass, replace
from BaseClasses import Region, Location, Entrance, Item, ItemClassification
from typing import Optional, TYPE_CHECKING, List, Dict
from .Names import ItemID, ItemName, LairID, NPCName
from .Names.ArchipelagoID import BASE_ID, LAIR_ID_OFFSET, SOUL_OFFSET
from .Util import int_to_bcd

if TYPE_CHECKING:
    from . import SoulBlazerWorld


@dataclass(frozen=True)
class SoulBlazerItemData:
    id: int
    """Internal item ID"""

    operand: int
    """Either Gems/Exp Quantity or Lair ID"""

    classification: ItemClassification

    def duplicate(self, **changes) -> "SoulBlazerItemData":
        """Returns a copy of this ItemData with the specified changes."""
        return replace(self, **changes)

    @property
    def code(self) -> int:
        """The unique ID used by archipelago for this item"""

        if self.id == ItemID.LAIR_RELEASE:
            return BASE_ID + LAIR_ID_OFFSET + self.operand
        elif self.id == ItemID.SOUL:
            return BASE_ID + SOUL_OFFSET + self.operand
        return BASE_ID + self.id

    @property
    def operand_bcd(self) -> int:
        return int_to_bcd(self.operand)

    @property
    def operand_for_id(self) -> int:
        if self.id == ItemID.GEMS or self.id == ItemID.EXP:
            return self.operand_bcd
        return self.operand


class SoulBlazerItem(Item):
    game = "Soul Blazer"

    def __init__(self, name: str, player: int, itemData: SoulBlazerItemData):
        super().__init__(name, itemData.classification, itemData.code, player)
        self._itemData = itemData

    def set_operand(self, value: int) -> 'SoulBlazerItem':
        self._itemData = self._itemData.duplicate(operand=value)
        return self

    @property
    def id(self) -> int:
        return self._itemData.id

    @property
    def operand(self) -> int:
        return self._itemData.operand

    @operand.setter
    def operand(self, value: int):
        self._itemData.operand = value

    @property
    def operand_bcd(self) -> int:
        return self._itemData.operand_bcd

    @operand_bcd.setter
    def operand_bcd(self, bcd: int):
        self._itemData.operand_bcd = bcd

    @property
    def operand_for_id(self) -> int:
        return self._itemData.operand_for_id


herb_count = 20
"""Number of Herbs in vanilla item pool"""

bottle_count = 7
"""Number of Strange Bottles in vanilla item pool"""

nothing_count = 3
"""Number of 'Nothing' rewards in vanilla item pool"""

gem_values_vanilla = [1, 12, 40, 50, 50, 50, 50, 50, 60, 60, 80, 80, 80, 80, 80, 100, 100, 100, 100, 150, 200]
"""Gem reward values in vanilla item pool"""

exp_values_vanilla = [1, 30, 80, 150, 180, 200, 250, 300, 300, 300, 300, 300, 400]
"""Exp reward values in vanilla item pool"""


def create_gem_pool(world: "SoulBlazerWorld") -> List[int]:
    if world.options.gem_exp_pool == "random_range":
        return [world.random.randint(1, 999) for _ in range(len(gem_values_vanilla))]
    if world.options.gem_exp_pool == "improved":
        return [gem * 2 for gem in gem_values_vanilla]

    return gem_values_vanilla[:]


def create_exp_pool(world: "SoulBlazerWorld") -> List[int]:
    if world.options.gem_exp_pool == "random_range":
        return [world.random.randint(1, 9999) for _ in range(len(exp_values_vanilla))]
    if world.options.gem_exp_pool == "improved":
        return [exp * 10 for exp in exp_values_vanilla]

    return exp_values_vanilla[:]


def create_itempool(world: "SoulBlazerWorld") -> List[SoulBlazerItem]:
    itempool = [SoulBlazerItem(name, world.player, itemData) for (name, itemData) in unique_items_table.items()]
    itempool += [
        SoulBlazerItem(ItemName.MEDICALHERB, world.player, repeatable_items_table[ItemName.MEDICALHERB])
        for _ in range(herb_count)
    ]
    itempool += [
        SoulBlazerItem(ItemName.STRANGEBOTTLE, world.player, repeatable_items_table[ItemName.STRANGEBOTTLE])
        for _ in range(bottle_count)
    ]
    # TODO: Add option to replace nothings with... something?
    itempool += [
        SoulBlazerItem(ItemName.NOTHING, world.player, repeatable_items_table[ItemName.NOTHING])
        for _ in range(nothing_count)
    ]
    world.gem_items = [world.create_item(ItemName.GEMS).set_operand(value) for value in create_gem_pool(world)]
    itempool += world.gem_items
    world.exp_items = [world.create_item(ItemName.EXP).set_operand(value) for value in create_exp_pool(world)]
    itempool += world.exp_items

    return itempool


# TODO: Unsure which progression items should skip balancing
swords_table = {
    ItemName.LIFESWORD     : SoulBlazerItemData(ItemID.LIFESWORD    , 0x00, ItemClassification.progression),
    ItemName.PSYCHOSWORD   : SoulBlazerItemData(ItemID.PSYCHOSWORD  , 0x00, ItemClassification.progression),
    ItemName.CRITICALSWORD : SoulBlazerItemData(ItemID.CRITICALSWORD, 0x00, ItemClassification.progression),
    ItemName.LUCKYBLADE    : SoulBlazerItemData(ItemID.LUCKYBLADE   , 0x00, ItemClassification.progression),
    ItemName.ZANTETSUSWORD : SoulBlazerItemData(ItemID.ZANTETSUSWORD, 0x00, ItemClassification.progression),
    ItemName.SPIRITSWORD   : SoulBlazerItemData(ItemID.SPIRITSWORD  , 0x00, ItemClassification.progression),
    ItemName.RECOVERYSWORD : SoulBlazerItemData(ItemID.RECOVERYSWORD, 0x00, ItemClassification.progression),
    ItemName.SOULBLADE     : SoulBlazerItemData(ItemID.SOULBLADE    , 0x00, ItemClassification.progression),
}

armors_table = {
    ItemName.IRONARMOR      : SoulBlazerItemData(ItemID.IRONARMOR     , 0x00, ItemClassification.useful),
    ItemName.ICEARMOR       : SoulBlazerItemData(ItemID.ICEARMOR      , 0x00, ItemClassification.progression),
    ItemName.BUBBLEARMOR    : SoulBlazerItemData(ItemID.BUBBLEARMOR   , 0x00, ItemClassification.progression),
    ItemName.MAGICARMOR     : SoulBlazerItemData(ItemID.MAGICARMOR    , 0x00, ItemClassification.useful),
    ItemName.MYSTICARMOR    : SoulBlazerItemData(ItemID.MYSTICARMOR   , 0x00, ItemClassification.useful),
    ItemName.LIGHTARMOR     : SoulBlazerItemData(ItemID.LIGHTARMOR    , 0x00, ItemClassification.useful),
    ItemName.ELEMENTALARMOR : SoulBlazerItemData(ItemID.ELEMENTALARMOR, 0x00, ItemClassification.useful),
    ItemName.SOULARMOR      : SoulBlazerItemData(ItemID.SOULARMOR     , 0x00, ItemClassification.progression),
}

castable_magic_table = {
    ItemName.FLAMEBALL   : SoulBlazerItemData(ItemID.FLAMEBALL  , 0x00, ItemClassification.progression),
    ItemName.LIGHTARROW  : SoulBlazerItemData(ItemID.LIGHTARROW , 0x00, ItemClassification.progression),
    ItemName.MAGICFLARE  : SoulBlazerItemData(ItemID.MAGICFLARE , 0x00, ItemClassification.progression),
    ItemName.ROTATOR     : SoulBlazerItemData(ItemID.ROTATOR    , 0x00, ItemClassification.progression),
    ItemName.SPARKBOMB   : SoulBlazerItemData(ItemID.SPARKBOMB  , 0x00, ItemClassification.progression),
    ItemName.FLAMEPILLAR : SoulBlazerItemData(ItemID.FLAMEPILLAR, 0x00, ItemClassification.progression),
    ItemName.TORNADO     : SoulBlazerItemData(ItemID.TORNADO    , 0x00, ItemClassification.progression),
}

magic_table = {
    **castable_magic_table,
    ItemName.PHOENIX     : SoulBlazerItemData(ItemID.PHOENIX    , 0x00, ItemClassification.progression),
}

emblems_table = {
    ItemName.EMBLEMA         : SoulBlazerItemData(ItemID.EMBLEMA, 0x00, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMB         : SoulBlazerItemData(ItemID.EMBLEMB, 0x00, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMC         : SoulBlazerItemData(ItemID.EMBLEMC, 0x00, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMD         : SoulBlazerItemData(ItemID.EMBLEMD, 0x00, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEME         : SoulBlazerItemData(ItemID.EMBLEME, 0x00, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMF         : SoulBlazerItemData(ItemID.EMBLEMF, 0x00, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMG         : SoulBlazerItemData(ItemID.EMBLEMG, 0x00, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMH         : SoulBlazerItemData(ItemID.EMBLEMH, 0x00, ItemClassification.progression_skip_balancing),
}

redhots_table = {
    ItemName.REDHOTMIRROR    : SoulBlazerItemData(ItemID.REDHOTMIRROR, 0x00, ItemClassification.progression),
    ItemName.REDHOTBALL      : SoulBlazerItemData(ItemID.REDHOTBALL  , 0x00, ItemClassification.progression),
    ItemName.REDHOTSTICK     : SoulBlazerItemData(ItemID.REDHOTSTICK , 0x00, ItemClassification.progression),
}

stones_table = {
    ItemName.BROWNSTONE      : SoulBlazerItemData(ItemID.BROWNSTONE , 0x00, ItemClassification.progression),
    ItemName.GREENSTONE      : SoulBlazerItemData(ItemID.GREENSTONE , 0x00, ItemClassification.progression),
    ItemName.BLUESTONE       : SoulBlazerItemData(ItemID.BLUESTONE  , 0x00, ItemClassification.progression),
    ItemName.SILVERSTONE     : SoulBlazerItemData(ItemID.SILVERSTONE, 0x00, ItemClassification.progression),
    ItemName.PURPLESTONE     : SoulBlazerItemData(ItemID.PURPLESTONE, 0x00, ItemClassification.progression),
    ItemName.BLACKSTONE      : SoulBlazerItemData(ItemID.BLACKSTONE , 0x00, ItemClassification.progression),
}

inventory_items_table = {
    ItemName.GOATSFOOD       : SoulBlazerItemData(ItemID.GOATSFOOD      , 0x00, ItemClassification.useful),
    ItemName.HARPSTRING      : SoulBlazerItemData(ItemID.HARPSTRING     , 0x00, ItemClassification.progression),
    ItemName.APASS           : SoulBlazerItemData(ItemID.APASS          , 0x00, ItemClassification.progression),
    ItemName.DREAMROD        : SoulBlazerItemData(ItemID.DREAMROD       , 0x00, ItemClassification.progression),
    ItemName.LEOSBRUSH       : SoulBlazerItemData(ItemID.LEOSBRUSH      , 0x00, ItemClassification.progression),
    ItemName.TURBOSLEAVES    : SoulBlazerItemData(ItemID.TURBOSLEAVES   , 0x00, ItemClassification.progression),
    ItemName.MOLESRIBBON     : SoulBlazerItemData(ItemID.MOLESRIBBON    , 0x00, ItemClassification.progression),
    ItemName.BIGPEARL        : SoulBlazerItemData(ItemID.BIGPEARL       , 0x00, ItemClassification.progression),
    ItemName.MERMAIDSTEARS   : SoulBlazerItemData(ItemID.MERMAIDSTEARS  , 0x00, ItemClassification.progression),
    ItemName.MUSHROOMSHOES   : SoulBlazerItemData(ItemID.MUSHROOMSHOES  , 0x00, ItemClassification.progression),
    ItemName.AIRSHIPKEY      : SoulBlazerItemData(ItemID.AIRSHIPKEY     , 0x00, ItemClassification.progression),
    ItemName.THUNDERRING     : SoulBlazerItemData(ItemID.THUNDERRING    , 0x00, ItemClassification.progression),
    ItemName.DELICIOUSSEEDS  : SoulBlazerItemData(ItemID.DELICIOUSSEEDS , 0x00, ItemClassification.progression),
    ItemName.ACTINIDIALEAVES : SoulBlazerItemData(ItemID.ACTINIDIALEAVES, 0x00, ItemClassification.progression),
    ItemName.DOORKEY         : SoulBlazerItemData(ItemID.DOORKEY        , 0x00, ItemClassification.progression),
    ItemName.PLATINUMCARD    : SoulBlazerItemData(ItemID.PLATINUMCARD   , 0x00, ItemClassification.progression),
    ItemName.VIPCARD         : SoulBlazerItemData(ItemID.VIPCARD        , 0x00, ItemClassification.progression),
    **emblems_table,
    **redhots_table,
    ItemName.POWERBRACELET   : SoulBlazerItemData(ItemID.POWERBRACELET  , 0x00, ItemClassification.useful),
    ItemName.SHIELDBRACELET  : SoulBlazerItemData(ItemID.SHIELDBRACELET , 0x00, ItemClassification.useful),
    ItemName.SUPERBRACELET   : SoulBlazerItemData(ItemID.SUPERBRACELET  , 0x00, ItemClassification.useful),
    ItemName.MEDICALHERB     : SoulBlazerItemData(ItemID.MEDICALHERB    , 0x00, ItemClassification.filler),
    ItemName.STRANGEBOTTLE   : SoulBlazerItemData(ItemID.STRANGEBOTTLE  , 0x00, ItemClassification.filler),
    **stones_table,
    ItemName.MAGICBELL       : SoulBlazerItemData(ItemID.MAGICBELL      , 0x00, ItemClassification.useful),
}


misc_table = {
    ItemName.NOTHING : SoulBlazerItemData(ItemID.NOTHING, 0x00, ItemClassification.filler),
    ItemName.GEMS    : SoulBlazerItemData(ItemID.GEMS   , 100 , ItemClassification.filler),
    ItemName.EXP     : SoulBlazerItemData(ItemID.EXP    , 250 , ItemClassification.filler),
}

repeatable_items_table = {
    ItemName.MEDICALHERB   : inventory_items_table[ItemName.MEDICALHERB],
    ItemName.STRANGEBOTTLE : inventory_items_table[ItemName.STRANGEBOTTLE],
    **misc_table,
}

items_table = {
    **swords_table,
    **armors_table,
    **magic_table,
    **inventory_items_table,
}

npc_release_table = {
    NPCName.OLD_WOMAN                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.OLD_WOMAN                    , ItemClassification.progression),
    NPCName.TOOL_SHOP_OWNER               : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.TOOL_SHOP_OWNER              , ItemClassification.progression),
    NPCName.TULIP                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.TULIP                        , ItemClassification.filler),
    NPCName.BRIDGE_GUARD                  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BRIDGE_GUARD                 , ItemClassification.progression),
    NPCName.VILLAGE_CHIEF                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.VILLAGE_CHIEF                , ItemClassification.progression),
    NPCName.IVY_CHEST_ROOM                : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.IVY_CHEST_ROOM               , ItemClassification.progression),
    NPCName.WATER_MILL                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.WATER_MILL                   , ItemClassification.progression),
    NPCName.GOAT_HERB                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GOAT_HERB                    , ItemClassification.progression),
    NPCName.LISA                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.LISA                         , ItemClassification.progression),
    NPCName.TULIP2                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.TULIP2                       , ItemClassification.filler),
    NPCName.ARCHITECT                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.ARCHITECT                    , ItemClassification.progression),
    NPCName.IVY                           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.IVY                          , ItemClassification.progression),
    NPCName.GOAT                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GOAT                         , ItemClassification.progression),
    NPCName.TEDDY                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.TEDDY                        , ItemClassification.progression),
    NPCName.TULIP3                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.TULIP3                       , ItemClassification.filler),
    NPCName.LEOS_HOUSE                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.LEOS_HOUSE                   , ItemClassification.progression),
    NPCName.LONELY_GOAT                   : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.LONELY_GOAT                  , ItemClassification.filler),
    NPCName.TULIP_PASS                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.TULIP_PASS                   , ItemClassification.progression),
    NPCName.BOY_CABIN                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BOY_CABIN                    , ItemClassification.filler),
    NPCName.BOY_CAVE                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BOY_CAVE                     , ItemClassification.progression),
    NPCName.OLD_MAN                       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.OLD_MAN                      , ItemClassification.filler),
    NPCName.OLD_MAN2                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.OLD_MAN2                     , ItemClassification.filler),
    NPCName.IVY2                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.IVY2                         , ItemClassification.filler),
    NPCName.IVY_EMBLEM_A                  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.IVY_EMBLEM_A                 , ItemClassification.progression),
    NPCName.IVY_RECOVERY_SWORD            : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.IVY_RECOVERY_SWORD           , ItemClassification.progression),
    NPCName.TULIP4                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.TULIP4                       , ItemClassification.filler),
    NPCName.GOAT2                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GOAT2                        , ItemClassification.filler),
    NPCName.BIRD_RED_HOT_MIRROR           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BIRD_RED_HOT_MIRROR          , ItemClassification.progression),
    NPCName.BIRD                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BIRD                         , ItemClassification.filler),
    NPCName.DOG                           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOG                          , ItemClassification.filler),
    NPCName.DOG2                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOG2                         , ItemClassification.filler),
    NPCName.DOG3                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOG3                         , ItemClassification.progression),
    NPCName.MOLE_SHIELD_BRACELET          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOLE_SHIELD_BRACELET         , ItemClassification.progression),
    NPCName.SQUIRREL_EMBLEM_C             : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SQUIRREL_EMBLEM_C            , ItemClassification.progression),
    NPCName.SQUIRREL_PSYCHO_SWORD         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SQUIRREL_PSYCHO_SWORD        , ItemClassification.progression),
    NPCName.BIRD2                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BIRD2                        , ItemClassification.filler),
    NPCName.MOLE_SOUL_OF_LIGHT            : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOLE_SOUL_OF_LIGHT           , ItemClassification.progression),
    NPCName.DEER                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DEER                         , ItemClassification.progression),
    NPCName.CROCODILE                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CROCODILE                    , ItemClassification.progression),
    NPCName.SQUIRREL                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SQUIRREL                     , ItemClassification.filler),
    NPCName.GREENWOODS_GUARDIAN           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GREENWOODS_GUARDIAN          , ItemClassification.progression),
    NPCName.MOLE                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOLE                         , ItemClassification.progression),
    NPCName.DOG4                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOG4                         , ItemClassification.filler),
    NPCName.SQUIRREL_ICE_ARMOR            : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SQUIRREL_ICE_ARMOR           , ItemClassification.progression),
    NPCName.SQUIRREL2                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SQUIRREL2                    , ItemClassification.filler),
    NPCName.DOG5                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOG5                         , ItemClassification.filler),
    NPCName.CROCODILE2                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CROCODILE2                   , ItemClassification.progression),
    NPCName.MOLE2                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOLE2                        , ItemClassification.filler),
    NPCName.SQUIRREL3                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SQUIRREL3                    , ItemClassification.progression),
    NPCName.BIRD_GREENWOOD_LEAF           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BIRD_GREENWOOD_LEAF          , ItemClassification.progression),
    NPCName.MOLE3                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOLE3                        , ItemClassification.progression),
    NPCName.DEER_MAGIC_BELL               : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DEER_MAGIC_BELL              , ItemClassification.progression),
    NPCName.BIRD3                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BIRD3                        , ItemClassification.filler),
    NPCName.CROCODILE3                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CROCODILE3                   , ItemClassification.progression),
    NPCName.MONMO                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MONMO                        , ItemClassification.progression),
    NPCName.DOLPHIN                       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOLPHIN                      , ItemClassification.filler),
    NPCName.ANGELFISH                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.ANGELFISH                    , ItemClassification.filler),
    NPCName.MERMAID                       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID                      , ItemClassification.progression),
    NPCName.ANGELFISH2                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.ANGELFISH2                   , ItemClassification.filler),
    NPCName.MERMAID_PEARL                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_PEARL                , ItemClassification.progression),
    NPCName.MERMAID2                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID2                     , ItemClassification.filler),
    NPCName.DOLPHIN_SAVES_LUE             : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOLPHIN_SAVES_LUE            , ItemClassification.progression),
    NPCName.MERMAID_STATUE_BLESTER        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_STATUE_BLESTER       , ItemClassification.progression),
    NPCName.MERMAID_RED_HOT_STICK         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_RED_HOT_STICK        , ItemClassification.progression),
    NPCName.LUE                           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.LUE                          , ItemClassification.progression),
    NPCName.MERMAID3                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID3                     , ItemClassification.filler),
    NPCName.MERMAID_NANA                  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_NANA                 , ItemClassification.filler),
    NPCName.MERMAID4                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID4                     , ItemClassification.filler),
    NPCName.DOLPHIN2                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOLPHIN2                     , ItemClassification.progression),
    NPCName.MERMAID_STATUE_ROCKBIRD       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_STATUE_ROCKBIRD      , ItemClassification.progression),
    NPCName.MERMAID_BUBBLE_ARMOR          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_BUBBLE_ARMOR         , ItemClassification.progression),
    NPCName.MERMAID5                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID5                     , ItemClassification.filler),
    NPCName.MERMAID6                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID6                     , ItemClassification.filler),
    NPCName.MERMAID_TEARS                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_TEARS                , ItemClassification.filler),
    NPCName.MERMAID_STATUE_DUREAN         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_STATUE_DUREAN        , ItemClassification.progression),
    NPCName.ANGELFISH3                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.ANGELFISH3                   , ItemClassification.filler),
    NPCName.ANGELFISH_SOUL_OF_SHIELD      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.ANGELFISH_SOUL_OF_SHIELD     , ItemClassification.progression),
    NPCName.MERMAID_MAGIC_FLARE           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_MAGIC_FLARE          , ItemClassification.progression),
    NPCName.MERMAID_QUEEN                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_QUEEN                , ItemClassification.progression),
    NPCName.MERMAID_STATUE_GHOST_SHIP     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_STATUE_GHOST_SHIP    , ItemClassification.progression),
    NPCName.DOLPHIN_SECRET_CAVE           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOLPHIN_SECRET_CAVE          , ItemClassification.progression),
    NPCName.MERMAID7                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID7                     , ItemClassification.filler),
    NPCName.ANGELFISH4                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.ANGELFISH4                   , ItemClassification.filler),
    NPCName.MERMAID8                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID8                     , ItemClassification.filler),
    NPCName.DOLPHIN_PEARL                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOLPHIN_PEARL                , ItemClassification.progression),
    NPCName.MERMAID9                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID9                     , ItemClassification.filler),
    NPCName.GRANDPA                       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GRANDPA                      , ItemClassification.progression),
    NPCName.GIRL                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GIRL                         , ItemClassification.filler),
    NPCName.MUSHROOM                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MUSHROOM                     , ItemClassification.filler),
    NPCName.BOY                           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BOY                          , ItemClassification.progression),
    NPCName.GRANDPA2                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GRANDPA2                     , ItemClassification.filler),
    NPCName.SNAIL_JOCKEY                  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SNAIL_JOCKEY                 , ItemClassification.filler),
    NPCName.NOME                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.NOME                         , ItemClassification.progression),
    NPCName.BOY2                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BOY2                         , ItemClassification.filler),
    NPCName.MUSHROOM_EMBLEM_F             : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MUSHROOM_EMBLEM_F            , ItemClassification.progression),
    NPCName.DANCING_GRANDMA               : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DANCING_GRANDMA              , ItemClassification.progression),
    NPCName.DANCING_GRANDMA2              : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DANCING_GRANDMA2             , ItemClassification.progression),
    NPCName.SNAIL_EMBLEM_E                : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SNAIL_EMBLEM_E               , ItemClassification.progression),
    NPCName.BOY_MUSHROOM_SHOES            : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.BOY_MUSHROOM_SHOES           , ItemClassification.progression),
    NPCName.GRANDMA                       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GRANDMA                      , ItemClassification.filler),
    NPCName.GIRL2                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GIRL2                        , ItemClassification.filler),
    NPCName.MUSHROOM2                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MUSHROOM2                    , ItemClassification.progression),
    NPCName.SNAIL_RACER                   : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SNAIL_RACER                  , ItemClassification.filler),
    NPCName.SNAIL_RACER2                  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SNAIL_RACER2                 , ItemClassification.filler),
    NPCName.GIRL3                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GIRL3                        , ItemClassification.progression),
    NPCName.MUSHROOM3                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MUSHROOM3                    , ItemClassification.filler),
    NPCName.SNAIL                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SNAIL                        , ItemClassification.filler),
    NPCName.GRANDPA3                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GRANDPA3                     , ItemClassification.progression),
    NPCName.SNAIL2                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SNAIL2                       , ItemClassification.filler),
    NPCName.GRANDPA4                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GRANDPA4                     , ItemClassification.progression),
    NPCName.GRANDPA_LUNE                  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GRANDPA_LUNE                 , ItemClassification.progression),
    NPCName.GRANDPA5                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GRANDPA5                     , ItemClassification.progression),
    NPCName.MOUNTAIN_KING                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOUNTAIN_KING                , ItemClassification.progression),
    NPCName.PLANT_HERB                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.PLANT_HERB                   , ItemClassification.progression),
    NPCName.PLANT                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.PLANT                        , ItemClassification.filler),
    NPCName.CHEST_OF_DRAWERS_MYSTIC_ARMOR : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CHEST_OF_DRAWERS_MYSTIC_ARMOR, ItemClassification.progression),
    NPCName.CAT                           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CAT                          , ItemClassification.progression),
    NPCName.GREAT_DOOR_ZANTETSU_SWORD     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GREAT_DOOR_ZANTETSU_SWORD    , ItemClassification.progression),
    NPCName.CAT2                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CAT2                         , ItemClassification.progression),
    NPCName.GREAT_DOOR                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GREAT_DOOR                   , ItemClassification.progression),
    NPCName.CAT3                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CAT3                         , ItemClassification.filler),
    NPCName.MODEL_TOWN1                   : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MODEL_TOWN1                  , ItemClassification.progression),
    NPCName.GREAT_DOOR_MODEL_TOWNS        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GREAT_DOOR_MODEL_TOWNS       , ItemClassification.progression),
    NPCName.STEPS_UPSTAIRS                : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.STEPS_UPSTAIRS               , ItemClassification.progression),
    NPCName.CAT_DOOR_KEY                  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CAT_DOOR_KEY                 , ItemClassification.progression),
    NPCName.MOUSE                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOUSE                        , ItemClassification.progression),
    NPCName.MARIE                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MARIE                        , ItemClassification.progression),
    NPCName.DOLL                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOLL                         , ItemClassification.filler),
    NPCName.CHEST_OF_DRAWERS              : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CHEST_OF_DRAWERS             , ItemClassification.filler),
    NPCName.PLANT2                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.PLANT2                       , ItemClassification.filler),
    NPCName.MOUSE2                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOUSE2                       , ItemClassification.filler),
    NPCName.MOUSE_SPARK_BOMB              : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOUSE_SPARK_BOMB             , ItemClassification.progression),
    NPCName.MOUSE3                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOUSE3                       , ItemClassification.filler),
    NPCName.GREAT_DOOR_SOUL_OF_DETECTION  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GREAT_DOOR_SOUL_OF_DETECTION , ItemClassification.progression), 
    NPCName.MODEL_TOWN2                   : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MODEL_TOWN2                  , ItemClassification.progression),
    NPCName.MOUSE4                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOUSE4                       , ItemClassification.filler),
    NPCName.STEPS_MARIE                   : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.STEPS_MARIE                  , ItemClassification.progression),
    NPCName.CHEST_OF_DRAWERS2             : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CHEST_OF_DRAWERS2            , ItemClassification.progression),
    NPCName.PLANT_ACTINIDIA_LEAVES        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.PLANT_ACTINIDIA_LEAVES       , ItemClassification.progression),
    NPCName.MOUSE5                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MOUSE5                       , ItemClassification.filler),
    NPCName.CAT4                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.CAT4                         , ItemClassification.filler),
    NPCName.STAIRS_POWER_PLANT            : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.STAIRS_POWER_PLANT           , ItemClassification.progression),
    NPCName.SOLDIER                       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER                      , ItemClassification.filler),
    NPCName.SOLDIER2                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER2                     , ItemClassification.filler),
    NPCName.SOLDIER3                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER3                     , ItemClassification.filler),
    NPCName.SOLDIER_ELEMENTAL_MAIL        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_ELEMENTAL_MAIL       , ItemClassification.progression),
    NPCName.SOLDIER4                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER4                     , ItemClassification.filler),
    NPCName.SOLDIER5                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER5                     , ItemClassification.filler),
    NPCName.SINGER_CONCERT_HALL           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SINGER_CONCERT_HALL          , ItemClassification.progression),
    NPCName.SOLDIER6                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER6                     , ItemClassification.filler),
    NPCName.MAID                          : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MAID                         , ItemClassification.filler),
    NPCName.SOLDIER_LEFT_TOWER            : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_LEFT_TOWER           , ItemClassification.progression),
    NPCName.SOLDIER_DOK                   : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_DOK                  , ItemClassification.progression),
    NPCName.SOLDIER_PLATINUM_CARD         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_PLATINUM_CARD        , ItemClassification.progression),
    NPCName.SINGER                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SINGER                       , ItemClassification.filler),
    NPCName.SOLDIER_SOUL_OF_REALITY       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_SOUL_OF_REALITY      , ItemClassification.progression),
    NPCName.MAID2                         : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MAID2                        , ItemClassification.filler),
    NPCName.QUEEN_MAGRIDD                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.QUEEN_MAGRIDD                , ItemClassification.progression),
    NPCName.SOLDIER_WITH_LEO              : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_WITH_LEO             , ItemClassification.progression),
    NPCName.SOLDIER_RIGHT_TOWER           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_RIGHT_TOWER          , ItemClassification.progression),
    NPCName.DR_LEO                        : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DR_LEO                       , ItemClassification.progression),
    NPCName.SOLDIER7                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER7                     , ItemClassification.filler),
    NPCName.SOLDIER8                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER8                     , ItemClassification.filler),
    NPCName.MAID_HERB                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MAID_HERB                    , ItemClassification.progression),
    NPCName.SOLDIER_CASTLE                : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_CASTLE               , ItemClassification.progression),
    NPCName.SOLDIER9                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER9                     , ItemClassification.filler),
    NPCName.SOLDIER10                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER10                    , ItemClassification.filler),
    NPCName.SOLDIER11                     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER11                    , ItemClassification.filler),
    NPCName.KING_MAGRIDD                  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.KING_MAGRIDD                 , ItemClassification.progression),
}

souls_table = {
    ItemName.SOUL_MAGICIAN : SoulBlazerItemData(ItemID.SOUL, 0x00, ItemClassification.progression),
    ItemName.SOUL_LIGHT : SoulBlazerItemData(ItemID.SOUL, 0x01, ItemClassification.progression),
    ItemName.SOUL_SHIELD : SoulBlazerItemData(ItemID.SOUL, 0x02, ItemClassification.useful),
    ItemName.SOUL_DETECTION : SoulBlazerItemData(ItemID.SOUL, 0x03, ItemClassification.useful),
    ItemName.SOUL_REALITY : SoulBlazerItemData(ItemID.SOUL, 0x04, ItemClassification.progression),
}

special_table = {
    ItemName.VICTORY: SoulBlazerItemData(ItemID.VICTORY, 0x00, ItemClassification.progression)
}

all_items_table = {
    **items_table,
    **misc_table,
    **npc_release_table,
    **souls_table,
    **special_table,
}

unique_items_table = {k: v for k, v in all_items_table.items() if k not in repeatable_items_table and k != ItemName.VICTORY}

item_name_groups = {
    "swords": swords_table.keys(),
    "armors": armors_table.keys(),
    "magic": magic_table.keys(),
    "stones": stones_table.keys(),
    "emblems": emblems_table.keys(),
    "redhots": redhots_table.keys(),
    "souls": souls_table.keys(),
}
