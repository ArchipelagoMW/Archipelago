from dataclasses import dataclass
from BaseClasses import Region, Location, Entrance, Item, ItemClassification
from typing import Optional

from .Names import ItemID, ItemName, LairID, NPCName
from . import SoulBlazerWorld


@dataclass
class SoulBlazerItemData():
    id: int
    """Internal item ID"""

    operand: Optional[int]
    """Either Gems/Exp Quantity or Lair ID"""

    classification: ItemClassification
    
    @property
    def code(self) -> int:
        """The unique ID used by archipelago for this item"""
        if self.id == ItemID.LAIR_RELEASE:
            return SoulBlazerWorld.base_id + SoulBlazerWorld.lair_id_offset + self.operand
        return SoulBlazerWorld.base_id + self.id

    @property
    def operand_bcd(self) -> int:
        """Converts operand to/from SNES BCD"""
        bcd = self.operand % 10
        remainder = self.operand // 10
        digit = 1

        while remainder != 0:
            bcd += (remainder % 10) * (0x10**digit)
            remainder // 10
            digit += 1

        return bcd
    
    @operand_bcd.setter
    def operand_bcd(self, bcd: int):
        decimal = bcd % 0x10
        remainder = bcd // 0x10
        digit = 1

        while remainder != 0:
            decimal += (remainder % 10) * (10**digit)
            remainder // 0x10
            digit += 1

        operand = decimal



class SoulBlazerItem(Item):  # or from Items import MyGameItem
    game = "Soul Blazer"  # name of the game/world this item is from

    def __init__(self, name: str, player: int, itemData: SoulBlazerItemData):
        super().__init__(name, itemData.classification, itemData.code, player)
        self._itemData = itemData

    def set_operand(self, value: int):
        self._itemData.operamd = value
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


herb_count = 20
"""Number of Herbs in vanilla item pool"""

bottle_count = 7
"""Number of Strange Bottles in vanilla item pool"""

nothing_count = 3
"""Number of 'Nothing' rewards in vanilla item pool"""

gem_values = [1, 12, 40, 50, 50, 50, 50, 50, 60, 60, 80, 80, 80, 80, 80, 100, 100, 100, 100, 150, 200]
"""Gem reward values in vanilla item pool"""

exp_values = [1, 30, 80, 150, 180, 200, 250, 300, 300, 300, 300, 300, 400]
"""Exp reward values in vanilla item pool"""

def create_itempool(world: SoulBlazerWorld) -> list[SoulBlazerItem]:
    itempool =  [SoulBlazerItem(name, world.player, itemData) for (name, itemData) in unique_items_table.items()]
    itempool += [SoulBlazerItem(ItemName.MEDICALHERB, world.player, repeatable_items_table[ItemName.MEDICALHERB]) for _ in range(herb_count)]
    itempool += [SoulBlazerItem(ItemName.STRANGEBOTTLE, world.player, repeatable_items_table[ItemName.STRANGEBOTTLE]) for _ in range(bottle_count)]
    # TODO: Add option to replace nothings with... something
    itempool += [SoulBlazerItem(ItemName.NOTHING, world.player, repeatable_items_table[ItemName.NOTHING]) for _ in range(nothing_count)]
    # TODO: Add option for modyfing exp/gem amounts
    world.gem_items = [world.create_item(ItemName.GEMS).set_operand(value) for value in gem_values]
    itempool += world.gem_items
    world.exp_items = [world.create_item(ItemName.EXP).set_operand(value) for value in exp_values]
    itempool += world.exp_items
    
    return itempool


#TODO: Unsure which progression items should skip balancing
swords_table = {
    ItemName.LIFESWORD     : SoulBlazerItemData(ItemID.LIFESWORD    , None, ItemClassification.progression_skip_balancing),
    ItemName.PSYCHOSWORD   : SoulBlazerItemData(ItemID.PSYCHOSWORD  , None, ItemClassification.progression_skip_balancing),
    ItemName.CRITICALSWORD : SoulBlazerItemData(ItemID.CRITICALSWORD, None, ItemClassification.progression_skip_balancing),
    ItemName.LUCKYBLADE    : SoulBlazerItemData(ItemID.LUCKYBLADE   , None, ItemClassification.progression),
    ItemName.ZANTETSUSWORD : SoulBlazerItemData(ItemID.ZANTETSUSWORD, None, ItemClassification.progression),
    ItemName.SPIRITSWORD   : SoulBlazerItemData(ItemID.SPIRITSWORD  , None, ItemClassification.progression),
    ItemName.RECOVERYSWORD : SoulBlazerItemData(ItemID.RECOVERYSWORD, None, ItemClassification.progression_skip_balancing),
    ItemName.SOULBLADE     : SoulBlazerItemData(ItemID.SOULBLADE    , None, ItemClassification.progression),
}

armors_table = {
    ItemName.IRONARMOR      : SoulBlazerItemData(ItemID.IRONARMOR     , None, ItemClassification.useful),
    ItemName.ICEARMOR       : SoulBlazerItemData(ItemID.ICEARMOR      , None, ItemClassification.progression),
    ItemName.BUBBLEARMOR    : SoulBlazerItemData(ItemID.BUBBLEARMOR   , None, ItemClassification.progression),
    ItemName.MAGICARMOR     : SoulBlazerItemData(ItemID.MAGICARMOR    , None, ItemClassification.useful),
    ItemName.MYSTICARMOR    : SoulBlazerItemData(ItemID.MYSTICARMOR   , None, ItemClassification.useful),
    ItemName.LIGHTARMOR     : SoulBlazerItemData(ItemID.LIGHTARMOR    , None, ItemClassification.useful),
    ItemName.ELEMENTALARMOR : SoulBlazerItemData(ItemID.ELEMENTALARMOR, None, ItemClassification.useful),
    ItemName.SOULARMOR      : SoulBlazerItemData(ItemID.SOULARMOR     , None, ItemClassification.progression),
}

magic_table = {
    ItemName.FLAMEBALL   : SoulBlazerItemData(ItemID.FLAMEBALL  , None, ItemClassification.progression),
    ItemName.LIGHTARROW  : SoulBlazerItemData(ItemID.LIGHTARROW , None, ItemClassification.progression_skip_balancing),
    ItemName.MAGICFLARE  : SoulBlazerItemData(ItemID.MAGICFLARE , None, ItemClassification.progression_skip_balancing),
    ItemName.ROTATOR     : SoulBlazerItemData(ItemID.ROTATOR    , None, ItemClassification.progression_skip_balancing),
    ItemName.SPARKBOMB   : SoulBlazerItemData(ItemID.SPARKBOMB  , None, ItemClassification.progression_skip_balancing),
    ItemName.FLAMEPILLAR : SoulBlazerItemData(ItemID.FLAMEPILLAR, None, ItemClassification.progression_skip_balancing),
    ItemName.TORNADO     : SoulBlazerItemData(ItemID.TORNADO    , None, ItemClassification.progression_skip_balancing),
    ItemName.PHOENIX     : SoulBlazerItemData(ItemID.PHOENIX    , None, ItemClassification.progression_skip_balancing),
}

emblems_table = {
    ItemName.EMBLEMA         : SoulBlazerItemData(ItemID.EMBLEMA, None, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMB         : SoulBlazerItemData(ItemID.EMBLEMB, None, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMC         : SoulBlazerItemData(ItemID.EMBLEMC, None, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMD         : SoulBlazerItemData(ItemID.EMBLEMD, None, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEME         : SoulBlazerItemData(ItemID.EMBLEME, None, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMF         : SoulBlazerItemData(ItemID.EMBLEMF, None, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMG         : SoulBlazerItemData(ItemID.EMBLEMG, None, ItemClassification.progression_skip_balancing),
    ItemName.EMBLEMH         : SoulBlazerItemData(ItemID.EMBLEMH, None, ItemClassification.progression_skip_balancing),
}

redhots_table = {
    ItemName.REDHOTMIRROR    : SoulBlazerItemData(ItemID.REDHOTMIRROR, None, ItemClassification.progression),
    ItemName.REDHOTBALL      : SoulBlazerItemData(ItemID.REDHOTBALL  , None, ItemClassification.progression),
    ItemName.REDHOTSTICK     : SoulBlazerItemData(ItemID.REDHOTSTICK , None, ItemClassification.progression),
}

stones_table = {
    ItemName.BROWNSTONE      : SoulBlazerItemData(ItemID.BROWNSTONE , None, ItemClassification.progression),
    ItemName.GREENSTONE      : SoulBlazerItemData(ItemID.GREENSTONE , None, ItemClassification.progression),
    ItemName.BLUESTONE       : SoulBlazerItemData(ItemID.BLUESTONE  , None, ItemClassification.progression),
    ItemName.SILVERSTONE     : SoulBlazerItemData(ItemID.SILVERSTONE, None, ItemClassification.progression),
    ItemName.PURPLESTONE     : SoulBlazerItemData(ItemID.PURPLESTONE, None, ItemClassification.progression),
    ItemName.BLACKSTONE      : SoulBlazerItemData(ItemID.BLACKSTONE , None, ItemClassification.progression),
}

inventory_items_table = {
    ItemName.GOATSFOOD       : SoulBlazerItemData(ItemID.GOATSFOOD      , None, ItemClassification.useful),
    ItemName.HARPSTRING      : SoulBlazerItemData(ItemID.HARPSTRING     , None, ItemClassification.progression),
    ItemName.APASS           : SoulBlazerItemData(ItemID.APASS          , None, ItemClassification.progression),
    ItemName.DREAMROD        : SoulBlazerItemData(ItemID.DREAMROD       , None, ItemClassification.progression),
    ItemName.LEOSBRUSH       : SoulBlazerItemData(ItemID.LEOSBRUSH      , None, ItemClassification.progression),
    ItemName.TURBOSLEAVES    : SoulBlazerItemData(ItemID.TURBOSLEAVES   , None, ItemClassification.progression),
    ItemName.MOLESRIBBON     : SoulBlazerItemData(ItemID.MOLESRIBBON    , None, ItemClassification.progression),
    ItemName.BIGPEARL        : SoulBlazerItemData(ItemID.BIGPEARL       , None, ItemClassification.progression),
    ItemName.MERMAIDSTEARS   : SoulBlazerItemData(ItemID.MERMAIDSTEARS  , None, ItemClassification.progression),
    ItemName.MUSHROOMSHOES   : SoulBlazerItemData(ItemID.MUSHROOMSHOES  , None, ItemClassification.progression),
    ItemName.AIRSHIPKEY      : SoulBlazerItemData(ItemID.AIRSHIPKEY     , None, ItemClassification.progression),
    ItemName.THUNDERRING     : SoulBlazerItemData(ItemID.THUNDERRING    , None, ItemClassification.progression),
    ItemName.DELICIOUSSEEDS  : SoulBlazerItemData(ItemID.DELICIOUSSEEDS , None, ItemClassification.progression),
    ItemName.ACTINIDIALEAVES : SoulBlazerItemData(ItemID.ACTINIDIALEAVES, None, ItemClassification.progression),
    ItemName.DOORKEY         : SoulBlazerItemData(ItemID.DOORKEY        , None, ItemClassification.progression),
    ItemName.PLATINUMCARD    : SoulBlazerItemData(ItemID.PLATINUMCARD   , None, ItemClassification.progression),
    ItemName.VIPCARD         : SoulBlazerItemData(ItemID.VIPCARD        , None, ItemClassification.progression),
    **emblems_table,
    **redhots_table,
    ItemName.POWERBRACELET   : SoulBlazerItemData(ItemID.POWERBRACELET  , None, ItemClassification.useful),
    ItemName.SHIELDBRACELET  : SoulBlazerItemData(ItemID.SHIELDBRACELET , None, ItemClassification.useful),
    ItemName.SUPERBRACELET   : SoulBlazerItemData(ItemID.SUPERBRACELET  , None, ItemClassification.useful),
    ItemName.MEDICALHERB     : SoulBlazerItemData(ItemID.MEDICALHERB    , None, ItemClassification.filler),
    ItemName.STRANGEBOTTLE   : SoulBlazerItemData(ItemID.STRANGEBOTTLE  , None, ItemClassification.filler),
    **stones_table,
    ItemName.MAGICBELL       : SoulBlazerItemData(ItemID.MAGICBELL      , None, ItemClassification.useful),
}


misc_table = {
    ItemName.NOTHING : SoulBlazerItemData(ItemID.NOTHING, None, ItemClassification.trap),
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
    **misc_table,
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
    #TODO: consider putting souls in logic
    NPCName.ANGELFISH_SOUL_OF_SHIELD      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.ANGELFISH_SOUL_OF_SHIELD     , ItemClassification.useful),
    NPCName.MERMAID_MAGIC_FLARE           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_MAGIC_FLARE          , ItemClassification.progression),
    NPCName.MERMAID_QUEEN                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_QUEEN                , ItemClassification.progression),
    NPCName.MERMAID_STATUE_GHOST_SHIP     : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID_STATUE_GHOST_SHIP    , ItemClassification.progression),
    NPCName.DOLPHIN_SECRET_CAVE           : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOLPHIN_SECRET_CAVE          , ItemClassification.progression),
    NPCName.MERMAID7                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID7                     , ItemClassification.filler),
    NPCName.ANGELFISH4                    : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.ANGELFISH4                   , ItemClassification.filler),
    NPCName.MERMAID8                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID8                     , ItemClassification.filler),
    NPCName.DOLPHIN_PEARL                 : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.DOLPHIN_PEARL                , ItemClassification.progression),
    NPCName.MERMAID9                      : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.MERMAID9                     , ItemClassification.filler),
    NPCName.GRANDPA                       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GRANDPA                      , ItemClassification.filler),
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
    NPCName.GREAT_DOOR_SOUL_OF_DETECTION  : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.GREAT_DOOR_SOUL_OF_DETECTION , ItemClassification.useful), 
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
    NPCName.SOLDIER_SOUL_OF_REALITY       : SoulBlazerItemData(ItemID.LAIR_RELEASE, LairID.SOLDIER_SOUL_OF_REALITY      , ItemClassification.useful),
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

all_items_table = {
    **items_table,
    **npc_release_table,
}

unique_items_table = {
    **(x for x in all_items_table if x not in repeatable_items_table)
}