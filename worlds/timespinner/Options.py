from typing import Dict, Union, List
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict, OptionList
from schema import Schema, And, Optional, Or


class StartWithJewelryBox(Toggle):
    "Start with Jewelry Box unlocked"
    display_name = "Start with Jewelry Box"


class DownloadableItems(DefaultOnToggle):
    "With the tablet you will be able to download items at terminals"
    display_name = "Downloadable items"


class EyeSpy(Toggle):
    "Requires Oculus Ring in inventory to be able to break hidden walls."
    display_name = "Eye Spy"


class StartWithMeyef(Toggle):
    "Start with Meyef, ideal for when you want to play multiplayer."
    display_name = "Start with Meyef"


class QuickSeed(Toggle):
    "Start with Talaria Attachment, Nyoom!"
    display_name = "Quick seed"


class SpecificKeycards(Toggle):
    "Keycards can only open corresponding doors"
    display_name = "Specific Keycards"


class Inverted(Toggle):
    "Start in the past"
    display_name = "Inverted"


class GyreArchives(Toggle):
    "Gyre locations are in logic. New warps are gated by Merchant Crow and Kobo"
    display_name = "Gyre Archives"


class Cantoran(Toggle):
    "Cantoran's fight and check are available upon revisiting his room"
    display_name = "Cantoran"


class LoreChecks(Toggle):
    "Memories and journal entries contain items."
    display_name = "Lore Checks"


class BossRando(Toggle):
    "Shuffles the positions of all bosses."
    display_name = "Boss Randomization"


class BossScaling(DefaultOnToggle):
    "When Boss Rando is enabled, scales the bosses' HP, XP, and ATK to the stats of the location they replace (Recommended)"
    display_name = "Scale Random Boss Stats"


class DamageRando(Choice):
    "Randomly nerfs and buffs some orbs and their associated spells as well as some associated rings."
    display_name = "Damage Rando"
    option_off = 0
    option_allnerfs = 1
    option_mostlynerfs = 2
    option_balanced = 3
    option_mostlybuffs = 4
    option_allbuffs = 5
    option_manual = 6
    alias_true = 2


class DamageRandoOverrides(OptionDict):
    """Manual +/-/normal odds for an orb. Put 0 if you don't want a certain nerf or buff to be a possibility. Orbs that
    you don't specify will roll with 1/1/1 as odds"""
    schema = Schema({
        Optional("Blue"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Blade"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Fire"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Plasma"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Iron"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Ice"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Wind"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Gun"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Umbra"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Empire"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Eye"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Blood"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("ForbiddenTome"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Shattered"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Nether"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
        Optional("Radiant"): { 
            "MinusOdds": And(int, lambda n: n >= 0), 
            "NormalOdds": And(int, lambda n: n >= 0), 
            "PlusOdds": And(int, lambda n: n >= 0) 
        },
    })
    display_name = "Damage Rando Overrides"
    default = {
        "Blue": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Blade": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Fire": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Plasma": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Iron": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Ice": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Wind": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Gun": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Umbra": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Empire": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Eye": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Blood": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "ForbiddenTome": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Shattered": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Nether": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Radiant": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
    }


class HpCap(Range):
    "Sets the number that Lunais's HP maxes out at."
    display_name = "HP Cap"
    range_start = 1
    range_end = 999
    default = 999


class LevelCap(Range):
    """Sets the max level Lunais can achieve."""
    display_name = "Level Cap"
    range_start = 1
    range_end = 99
    default = 99


class ExtraEarringsXP(Range):
    """Adds additional XP granted by Galaxy Earrings."""
    display_name = "Extra Earrings XP"
    range_start = 0
    range_end = 24
    default = 0
    

class BossHealing(DefaultOnToggle):
    "Enables/disables healing after boss fights. NOTE: Currently only applicable when Boss Rando is enabled."
    display_name = "Heal After Bosses"


class ShopFill(Choice):
    """Sets the items for sale in Merchant Crow's shops.
    Default: No sunglasses or trendy jacket, but sand vials for sale.
    Randomized: Up to 4 random items in each shop.
    Vanilla: Keep shops the same as the base game.
    Empty: Sell no items at the shop."""
    display_name = "Shop Inventory"
    option_default = 0
    option_randomized = 1
    option_vanilla = 2
    option_empty = 3


class ShopWarpShards(DefaultOnToggle):
    "Shops always sell warp shards (when keys possessed), ignoring inventory setting."
    display_name = "Always Sell Warp Shards"


class ShopMultiplier(Range):
    "Multiplier for the cost of items in the shop. Set to 0 for free shops."
    display_name = "Shop Price Multiplier"
    range_start = 0
    range_end = 10
    default = 1


class LootPool(Choice):
    """Sets the items that drop from enemies (does not apply to boss reward checks)
    Vanilla: Drops are the same as the base game
    Randomized: Each slot of every enemy's drop table is given a random use item or piece of equipment.
    Empty: Enemies drop nothing."""
    display_name = "Loot Pool"
    option_vanilla = 0
    option_randomized = 1
    option_empty = 2


class DropRateCategory(Choice):
    """Sets the drop rate when 'Loot Pool' is set to 'Random'
    Tiered: Based on item rarity/value
    Vanilla: Based on bestiary slot the item is placed into
    Random: Assigned a random tier/drop rate
    Fixed: Set by the 'Fixed Drop Rate' setting
    """
    display_name = "Drop Rate Category"
    option_tiered = 0
    option_vanilla = 1
    option_randomized = 2
    option_fixed = 3


class FixedDropRate(Range):
    "Base drop rate percentage when 'Drop Rate Category' is set to 'Fixed'"
    display_name = "Fixed Drop Rate"
    range_start = 0
    range_end = 100
    default = 5


class LootTierDistro(Choice):
    """Sets how often items of each rarity tier are placed when 'Loot Pool' is set to 'Random'
    Default Weight: Rarer items will be assigned to enemy drop slots less frequently than common items
    Full Random: Any item has an equal chance of being placed in an enemy's drop slot
    Inverted Weight: Rarest items show up the most frequently, while common items are the rarest
    """
    display_name = "Loot Tier Distrubution"
    option_default_weight = 0
    option_full_random = 1
    option_inverted_weight = 2


class ShowBestiary(Toggle):
    "All entries in the bestiary are visible, without needing to kill one of a given enemy first"
    display_name = "Show Bestiary Entries"


class ShowDrops(Toggle):
    "All item drops in the bestiary are visible, without needing an enemy to drop one of a given item first"
    display_name = "Show Bestiary Item Drops"


class EnterSandman(Toggle):
    "The Ancient Pyramid is unlocked by the Twin Pyramid Keys, but the final boss door opens if you have all 5 Timespinner pieces"
    display_name = "Enter Sandman"


class DadPercent(Toggle):
    """The win condition is beating the boss of Emperor's Tower"""
    display_name = "Dad Percent"


class RisingTides(Toggle):
    """Random areas are flooded or drained, can be further specified with RisingTidesOverrides"""
    display_name = "Rising Tides"


def rising_tide_option(location: str, with_save_point_option: bool = False) -> Dict[Optional, Or]:
    if with_save_point_option:
        return {
            Optional(location): Or(
                And({
                    Optional("Dry"): And(int, lambda n: n >= 0),
                    Optional("Flooded"): And(int, lambda n: n >= 0),
                    Optional("FloodedWithSavePointAvailable"): And(int, lambda n: n >= 0)
                }, lambda d: any(v > 0 for v in d.values())),
                "Dry",
                "Flooded",
                "FloodedWithSavePointAvailable")
        }
    else:
        return {
            Optional(location): Or(
                And({
                    Optional("Dry"): And(int, lambda n: n >= 0),
                    Optional("Flooded"): And(int, lambda n: n >= 0)
                }, lambda d: any(v > 0 for v in d.values())),
                "Dry",
                "Flooded")
        }


class RisingTidesOverrides(OptionDict):
    """Odds for specific areas to be flooded or drained, only has effect when RisingTides is on.
    Areas that are not specified will roll with the default 33% chance of getting flooded or drained"""
    schema = Schema({
        **rising_tide_option("Xarion"),
        **rising_tide_option("Maw"),
        **rising_tide_option("AncientPyramidShaft"),
        **rising_tide_option("Sandman"),
        **rising_tide_option("CastleMoat"),
        **rising_tide_option("CastleBasement", with_save_point_option=True),
        **rising_tide_option("CastleCourtyard"),
        **rising_tide_option("LakeDesolation"),
        **rising_tide_option("LakeSerene")
    })
    display_name = "Rising Tides Overrides"
    default = {
        "Xarion": { "Dry": 67, "Flooded": 33 },
        "Maw": { "Dry": 67, "Flooded": 33 },
        "AncientPyramidShaft": { "Dry": 67, "Flooded": 33 },
        "Sandman": { "Dry": 67, "Flooded": 33 },
        "CastleMoat": { "Dry": 67, "Flooded": 33 },
        "CastleBasement": { "Dry": 66, "Flooded": 17, "FloodedWithSavePointAvailable": 17 },
        "CastleCourtyard": { "Dry": 67, "Flooded": 33 },
        "LakeDesolation": { "Dry": 67, "Flooded": 33 },
        "LakeSerene": { "Dry": 33, "Flooded": 67 },
    }


class UnchainedKeys(Toggle):
    """Start with Twin Pyramid Key, which does not give free warp;
    warp items for Past, Present, (and ??? with Enter Sandman) can be found."""
    display_name = "Unchained Keys"


class TrapChance(Range):
    """Chance of traps in the item pool.
    Traps will only replace filler items such as potions, vials and antidotes"""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 10


class Traps(OptionList):
    """List of traps that may be in the item pool to find"""
    display_name = "Traps Types"
    valid_keys = { "Meteor Sparrow Trap", "Poison Trap", "Chaos Trap", "Neurotoxin Trap", "Bee Trap" }
    default = [ "Meteor Sparrow Trap", "Poison Trap", "Chaos Trap", "Neurotoxin Trap", "Bee Trap" ]


# Some options that are available in the timespinner randomizer arent currently implemented
timespinner_options: Dict[str, Option] = {
    "StartWithJewelryBox": StartWithJewelryBox,
    "DownloadableItems": DownloadableItems,
    "EyeSpy": EyeSpy,
    "StartWithMeyef": StartWithMeyef,
    "QuickSeed": QuickSeed,
    "SpecificKeycards": SpecificKeycards,
    "Inverted": Inverted,
    "GyreArchives": GyreArchives,
    "Cantoran": Cantoran,
    "LoreChecks": LoreChecks,
    "BossRando": BossRando,
    "BossScaling": BossScaling,
    "DamageRando": DamageRando,
    "DamageRandoOverrides": DamageRandoOverrides,
    "HpCap": HpCap,
    "LevelCap": LevelCap,
    "ExtraEarringsXP": ExtraEarringsXP,
    "BossHealing": BossHealing,
    "ShopFill": ShopFill,
    "ShopWarpShards": ShopWarpShards,
    "ShopMultiplier": ShopMultiplier,
    "LootPool": LootPool,
    "DropRateCategory": DropRateCategory,
    "FixedDropRate": FixedDropRate,
    "LootTierDistro": LootTierDistro,
    "ShowBestiary": ShowBestiary,
    "ShowDrops": ShowDrops,
    "EnterSandman": EnterSandman,
    "DadPercent": DadPercent,
    "RisingTides": RisingTides,
    "RisingTidesOverrides": RisingTidesOverrides,
    "UnchainedKeys": UnchainedKeys,
    "TrapChance": TrapChance,
    "Traps": Traps,
    "DeathLink": DeathLink,
}


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, Dict, List]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
