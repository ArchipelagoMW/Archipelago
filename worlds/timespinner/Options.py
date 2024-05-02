from dataclasses import dataclass
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility
from Options import PerGameCommonOptions, DeathLinkMixin
from schema import Schema, And, Optional, Or
import logging


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


class BossRando(Choice):
    "Wheter all boss locations are shuffled, and if their damage/hp should be scaled."
    display_name = "Boss Randomization"
    option_off = 0
    option_scaled = 1
    option_unscaled = 2
    alias_true = 1


class EnemyRando(Choice):
    "Wheter enemies will be randomized, and if their damage/hp should be scaled."
    display_name = "Enemy Randomization"
    option_off = 0
    option_scaled = 1
    option_unscaled = 2
    option_ryshia = 3
    alias_true = 1


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
    display_name = "Rising Tides Overrides"
    schema = Schema({
        **rising_tide_option("Xarion"),
        **rising_tide_option("Maw"),
        **rising_tide_option("AncientPyramidShaft"),
        **rising_tide_option("Sandman"),
        **rising_tide_option("CastleMoat"),
        **rising_tide_option("CastleBasement", with_save_point_option=True),
        **rising_tide_option("CastleCourtyard"),
        **rising_tide_option("LakeDesolation"),
        **rising_tide_option("LakeSerene"),
        **rising_tide_option("LakeSereneBridge"),
        **rising_tide_option("Lab"),
    })
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
        "LakeSereneBridge": { "Dry": 67, "Flooded": 33 },
        "Lab": { "Dry": 67, "Flooded": 33 },
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


class PresentAccessWithWheelAndSpindle(Toggle):
    """When inverted, allows using the refugee camp warp when both the Timespinner Wheel and Spindle is acquired."""
    display_name = "Past Wheel & Spindle Warp"

@dataclass
class TimespinnerOptions(PerGameCommonOptions, DeathLinkMixin):
    start_with_jewelry_box: StartWithJewelryBox
    downloadable_items: DownloadableItems
    eye_spy: EyeSpy
    start_with_meyef: StartWithMeyef
    quick_seed: QuickSeed
    specific_keycards: SpecificKeycards
    inverted: Inverted
    gyre_archives: GyreArchives
    cantoran: Cantoran
    lore_checks: LoreChecks
    boss_rando: BossRando
    damage_rando: DamageRando
    damage_rando_overrides: DamageRandoOverrides
    hp_cap: HpCap
    level_cap: LevelCap
    extra_earrings_xp: ExtraEarringsXP
    boss_healing: BossHealing
    shop_fill: ShopFill
    shop_warp_shards: ShopWarpShards
    shop_multiplier: ShopMultiplier
    loot_pool: LootPool
    drop_rate_category: DropRateCategory
    fixed_drop_rate: FixedDropRate
    loot_tier_distro: LootTierDistro
    show_bestiary: ShowBestiary
    show_drops: ShowDrops
    enter_sandman: EnterSandman
    dad_percent: DadPercent
    rising_tides: RisingTides
    rising_tides_overrides: RisingTidesOverrides
    unchained_keys: UnchainedKeys
    present_access_with_wheel_and_spindle: PresentAccessWithWheelAndSpindle
    trap_chance: TrapChance
    traps: Traps

@dataclass
class BackwardsCompatiableTimespinnerOptions(TimespinnerOptions):
    StartWithJewelryBox: StartWithJewelryBox
    DownloadableItems: DownloadableItems
    EyeSpy: EyeSpy
    StartWithMeyef: StartWithMeyef
    QuickSeed: QuickSeed
    SpecificKeycards: SpecificKeycards
    Inverted: Inverted
    GyreArchives: GyreArchives
    Cantoran: Cantoran
    LoreChecks: LoreChecks
    BossRando: BossRando
    DamageRando: DamageRando
    DamageRandoOverrides: DamageRandoOverrides
    HpCap: HpCap
    LevelCap: LevelCap
    ExtraEarringsXP: ExtraEarringsXP
    BossHealing: BossHealing
    ShopFill: ShopFill
    ShopWarpShards: ShopWarpShards
    ShopMultiplier: ShopMultiplier
    LootPool: LootPool
    DropRateCategory: DropRateCategory
    FixedDropRate: FixedDropRate
    LootTierDistro: LootTierDistro
    ShowBestiary: ShowBestiary
    ShowDrops: ShowDrops
    EnterSandman: EnterSandman
    DadPercent: DadPercent
    RisingTides: RisingTides
    RisingTidesOverrides: RisingTidesOverrides
    UnchainedKeys: UnchainedKeys
    PresentAccessWithWheelAndSpindle: PresentAccessWithWheelAndSpindle
    TrapChance: TrapChance
    Traps: Traps
    DeathLink: DeathLink

    def __post_init__(self):
        self.StartWithJewelryBox.visibility = Visibility.none
        self.DownloadableItems.visibility = Visibility.none
        self.EyeSpy.visibility = Visibility.none
        self.StartWithMeyef.visibility = Visibility.none
        self.QuickSeed.visibility = Visibility.none
        self.SpecificKeycards.visibility = Visibility.none
        self.Inverted.visibility = Visibility.none
        self.GyreArchives.visibility = Visibility.none
        self.Cantoran.visibility = Visibility.none
        self.LoreChecks.visibility = Visibility.none
        self.BossRando.visibility = Visibility.none
        self.DamageRando.visibility = Visibility.none
        self.DamageRandoOverrides.visibility = Visibility.none
        self.HpCap.visibility = Visibility.none
        self.LevelCap.visibility = Visibility.none
        self.ExtraEarringsXP.visibility = Visibility.none
        self.BossHealing.visibility = Visibility.none
        self.ShopFill.visibility = Visibility.none
        self.ShopWarpShards.visibility = Visibility.none
        self.ShopMultiplier.visibility = Visibility.none
        self.LootPool.visibility = Visibility.none
        self.DropRateCategory.visibility = Visibility.none
        self.FixedDropRate.visibility = Visibility.none
        self.LootTierDistro.visibility = Visibility.none
        self.ShowBestiary.visibility = Visibility.none
        self.ShowDrops.visibility = Visibility.none
        self.EnterSandman.visibility = Visibility.none
        self.DadPercent.visibility = Visibility.none
        self.RisingTides.visibility = Visibility.none
        self.RisingTidesOverrides.visibility = Visibility.none
        self.UnchainedKeys.visibility = Visibility.none
        self.PresentAccessWithWheelAndSpindle.visibility = Visibility.none
        self.TrapChance.visibility = Visibility.none
        self.Traps.visibility = Visibility.none
        self.DeathLink.visibility = Visibility.none

    def handle_backward_compatibility(o) -> None:
        has_replaced_options: bool = False

        if o.StartWithJewelryBox.value != o.StartWithJewelryBox.default and \
            o.start_with_jewelry_box.value == o.start_with_jewelry_box.default:
            o.start_with_jewelry_box.value = o.StartWithJewelryBox.value
            has_replaced_options = True
        if o.DownloadableItems.value != o.DownloadableItems.default and \
            o.downloadable_items.value == o.downloadable_items.default:
            o.downloadable_items.value = o.DownloadableItems.value
            has_replaced_options = True
        if o.EyeSpy.value != o.EyeSpy.default and \
            o.eye_spy.value == o.eye_spy.default:
            o.eye_spy.value = o.EyeSpy.value
            has_replaced_options = True
        if o.StartWithMeyef.value != o.StartWithMeyef.default and \
            o.start_with_meyef.value == o.start_with_meyef.default:
            o.start_with_meyef.value = o.StartWithMeyef.value
            has_replaced_options = True
        if o.QuickSeed.value != o.QuickSeed.default and \
            o.quick_seed.value == o.quick_seed.default:
            o.quick_seed.value = o.QuickSeed.value
            has_replaced_options = True
        if o.SpecificKeycards.value != o.SpecificKeycards.default and \
            o.specific_keycards.value == o.specific_keycards.default:
            o.specific_keycards.value = o.SpecificKeycards.value
            has_replaced_options = True
        if o.Inverted.value != o.Inverted.default and \
            o.inverted.value == o.inverted.default:
            o.inverted.value = o.Inverted.value
            has_replaced_options = True
        if o.GyreArchives.value != o.GyreArchives.default and \
            o.gyre_archives.value == o.gyre_archives.default:
            o.gyre_archives.value = o.GyreArchives.value
            has_replaced_options = True
        if o.Cantoran.value != o.Cantoran.default and \
            o.cantoran.value == o.cantoran.default:
            o.cantoran.value = o.Cantoran.value
            has_replaced_options = True
        if o.LoreChecks.value != o.LoreChecks.default and \
            o.lore_checks.value == o.lore_checks.default:
            o.lore_checks.value = o.LoreChecks.value
            has_replaced_options = True
        if o.BossRando.value != o.BossRando.default and \
            o.boss_rando.value == o.boss_rando.default:
            o.boss_rando.value = o.BossRando.value
            has_replaced_options = True
        if o.DamageRando.value != o.DamageRando.default and \
            o.damage_rando.value == o.damage_rando.default:
            o.damage_rando.value = o.DamageRando.value
            has_replaced_options = True
        if o.DamageRandoOverrides.value != o.DamageRandoOverrides.default and \
            o.damage_rando_overrides.value == o.damage_rando_overrides.default:
            o.damage_rando_overrides.value = o.DamageRandoOverrides.value
            has_replaced_options = True
        if o.HpCap.value != o.HpCap.default and \
            o.hp_cap.value == o.hp_cap.default:
            o.hp_cap.value = o.HpCap.value
            has_replaced_options = True
        if o.LevelCap.value != o.LevelCap.default and \
            o.level_cap.value == o.level_cap.default:
            o.level_cap.value = o.LevelCap.value
            has_replaced_options = True
        if o.ExtraEarringsXP.value != o.ExtraEarringsXP.default and \
            o.extra_earrings_xp.value == o.extra_earrings_xp.default:
            o.extra_earrings_xp.value = o.ExtraEarringsXP.value
            has_replaced_options = True
        if o.BossHealing.value != o.BossHealing.default and \
            o.boss_healing.value == o.boss_healing.default:
            o.boss_healing.value = o.BossHealing.value
            has_replaced_options = True
        if o.ShopFill.value != o.ShopFill.default and \
            o.shop_fill.value == o.shop_fill.default:
            o.shop_fill.value = o.ShopFill.value
            has_replaced_options = True
        if o.ShopWarpShards.value != o.ShopWarpShards.default and \
            o.shop_warp_shards.value == o.shop_warp_shards.default:
            o.shop_warp_shards.value = o.ShopWarpShards.value
            has_replaced_options = True
        if o.ShopMultiplier.value != o.ShopMultiplier.default and \
            o.shop_multiplier.value == o.shop_multiplier.default:
            o.shop_multiplier.value = o.ShopMultiplier.value
            has_replaced_options = True
        if o.LootPool.value != o.LootPool.default and \
            o.loot_pool.value == o.loot_pool.default:
            o.loot_pool.value = o.LootPool.value
            has_replaced_options = True
        if o.DropRateCategory.value != o.DropRateCategory.default and \
            o.drop_rate_category.value == o.drop_rate_category.default:
            o.drop_rate_category.value = o.DropRateCategory.value
            has_replaced_options = True
        if o.FixedDropRate.value != o.FixedDropRate.default and \
            o.fixed_drop_rate.value == o.fixed_drop_rate.default:
            o.fixed_drop_rate.value = o.FixedDropRate.value
            has_replaced_options = True
        if o.LootTierDistro.value != o.LootTierDistro.default and \
            o.loot_tier_distro.value == o.loot_tier_distro.default:
            o.loot_tier_distro.value = o.LootTierDistro.value
            has_replaced_options = True
        if o.ShowBestiary.value != o.ShowBestiary.default and \
            o.show_bestiary.value == o.show_bestiary.default:
            o.show_bestiary.value = o.ShowBestiary.value
            has_replaced_options = True
        if o.ShowDrops.value != o.ShowDrops.default and \
            o.show_drops.value == o.show_drops.default:
            o.show_drops.value = o.ShowDrops.value
            has_replaced_options = True
        if o.EnterSandman.value != o.EnterSandman.default and \
            o.enter_sandman.value == o.enter_sandman.default:
            o.enter_sandman.value = o.EnterSandman.value
            has_replaced_options = True
        if o.DadPercent.value != o.DadPercent.default and \
            o.dad_percent.value == o.dad_percent.default:
            o.dad_percent.value = o.DadPercent.value
            has_replaced_options = True
        if o.RisingTides.value != o.RisingTides.default and \
            o.rising_tides.value == o.rising_tides.default:
            o.rising_tides.value = o.RisingTides.value
            has_replaced_options = True
        if o.RisingTidesOverrides.value != o.RisingTidesOverrides.default and \
            o.rising_tides_overrides.value == o.rising_tides_overrides.default:
            o.rising_tides_overrides.value = o.RisingTidesOverrides.value
            has_replaced_options = True
        if o.UnchainedKeys.value != o.UnchainedKeys.default and \
            o.unchained_keys.value == o.unchained_keys.default:
            o.unchained_keys.value = o.UnchainedKeys.value
            has_replaced_options = True
        if o.PresentAccessWithWheelAndSpindle.value != o.PresentAccessWithWheelAndSpindle.default and \
            o.present_access_with_wheel_and_spindle.value == o.present_access_with_wheel_and_spindle.default:
            o.present_access_with_wheel_and_spindle.value = o.PresentAccessWithWheelAndSpindle.value
            has_replaced_options = True
        if o.TrapChance.value != o.TrapChance.default and \
            o.trap_chance.value == o.trap_chance.default:
            o.trap_chance.value = o.TrapChance.value
            has_replaced_options = True
        if o.Traps.value != o.Traps.default and \
            o.traps.value == o.traps.default:
            o.traps.value = o.Traps.value
            has_replaced_options = True
        if o.DeathLink.value != o.DeathLink.default and \
            o.death_link.value == o.death_link.default:
            o.death_link.value = o.DeathLink.value
            has_replaced_options = True

        if has_replaced_options:
            logging.warning("Timespinner options where renamed from PasCalCase to snake_case, plz update your yml")