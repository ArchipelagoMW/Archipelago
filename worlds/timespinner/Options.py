from dataclasses import dataclass
from typing import Type, Any
from typing import Dict
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, OptionDict, OptionList, Visibility, Option
from Options import PerGameCommonOptions, DeathLinkMixin, AssembleOptions
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
    """Sets the number that Lunais's HP maxes out at."""
    display_name = "HP Cap"
    range_start = 1
    range_end = 999
    default = 999

class AuraCap(Range):
    """Sets the maximum Aura Lunais is allowed to have. Level 1 is 80. Djinn Inferno costs 45."""
    display_name = "Aura Cap"
    range_start = 45
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
    valid_keys = { "Meteor Sparrow Trap", "Poison Trap", "Chaos Trap", "Neurotoxin Trap", "Bee Trap", "Throw Stun Trap" }
    default = [ "Meteor Sparrow Trap", "Poison Trap", "Chaos Trap", "Neurotoxin Trap", "Bee Trap", "Throw Stun Trap" ]

class PresentAccessWithWheelAndSpindle(Toggle):
    """When inverted, allows using the refugee camp warp when both the Timespinner Wheel and Spindle is acquired."""
    display_name = "Back to the future"

class PrismBreak(Toggle):
    """Adds 3 Laser Access items to the item pool to remove the lasers blocking the military hangar area
    instead of needing to beat the Golden Idol, Aelana, and The Maw."""
    display_name = "Prism Break"

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
    enemy_rando: EnemyRando
    damage_rando: DamageRando
    damage_rando_overrides: DamageRandoOverrides
    hp_cap: HpCap
    aura_cap: AuraCap
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
    back_to_the_future: PresentAccessWithWheelAndSpindle
    prism_break: PrismBreak
    trap_chance: TrapChance
    traps: Traps

class HiddenDamageRandoOverrides(DamageRandoOverrides): 
    """Manual +/-/normal odds for an orb. Put 0 if you don't want a certain nerf or buff to be a possibility. Orbs that
    you don't specify will roll with 1/1/1 as odds"""
    visibility = Visibility.none

class HiddenRisingTidesOverrides(RisingTidesOverrides):
    """Odds for specific areas to be flooded or drained, only has effect when RisingTides is on.
    Areas that are not specified will roll with the default 33% chance of getting flooded or drained"""
    visibility = Visibility.none

class HiddenTraps(Traps):
    """List of traps that may be in the item pool to find"""
    visibility = Visibility.none

class HiddenDeathLink(DeathLink):
    """When you die, everyone who enabled death link dies. Of course, the reverse is true too."""
    visibility = Visibility.none

def hidden(option: Type[Option[Any]]) -> Type[Option]:
    new_option = AssembleOptions(f"{option.__name__}Hidden", option.__bases__, vars(option).copy())
    new_option.visibility = Visibility.none
    new_option.__doc__ = option.__doc__
    globals()[f"{option.__name__}Hidden"] = new_option
    return new_option
    
class HasReplacedCamelCase(Toggle):
    """For internal use will display a warning message if true"""
    visibility = Visibility.none

@dataclass
class BackwardsCompatiableTimespinnerOptions(TimespinnerOptions):
    StartWithJewelryBox: hidden(StartWithJewelryBox) # type: ignore
    DownloadableItems: hidden(DownloadableItems) # type: ignore
    EyeSpy: hidden(EyeSpy) # type: ignore
    StartWithMeyef: hidden(StartWithMeyef) # type: ignore
    QuickSeed: hidden(QuickSeed) # type: ignore
    SpecificKeycards: hidden(SpecificKeycards) # type: ignore
    Inverted: hidden(Inverted) # type: ignore
    GyreArchives: hidden(GyreArchives) # type: ignore
    Cantoran: hidden(Cantoran) # type: ignore
    LoreChecks: hidden(LoreChecks) # type: ignore
    BossRando: hidden(BossRando) # type: ignore
    EnemyRando: hidden(EnemyRando) # type: ignore
    DamageRando: hidden(DamageRando) # type: ignore
    DamageRandoOverrides: HiddenDamageRandoOverrides
    HpCap: hidden(HpCap) # type: ignore
    LevelCap: hidden(LevelCap) # type: ignore
    ExtraEarringsXP: hidden(ExtraEarringsXP) # type: ignore
    BossHealing: hidden(BossHealing) # type: ignore
    ShopFill: hidden(ShopFill) # type: ignore
    ShopWarpShards: hidden(ShopWarpShards) # type: ignore
    ShopMultiplier: hidden(ShopMultiplier) # type: ignore
    LootPool: hidden(LootPool) # type: ignore
    DropRateCategory: hidden(DropRateCategory) # type: ignore
    FixedDropRate: hidden(FixedDropRate) # type: ignore
    LootTierDistro: hidden(LootTierDistro) # type: ignore
    ShowBestiary: hidden(ShowBestiary) # type: ignore
    ShowDrops: hidden(ShowDrops) # type: ignore
    EnterSandman: hidden(EnterSandman) # type: ignore
    DadPercent: hidden(DadPercent) # type: ignore
    RisingTides: hidden(RisingTides) # type: ignore
    RisingTidesOverrides: HiddenRisingTidesOverrides
    UnchainedKeys: hidden(UnchainedKeys) # type: ignore
    PresentAccessWithWheelAndSpindle: hidden(PresentAccessWithWheelAndSpindle) # type: ignore
    TrapChance: hidden(TrapChance) # type: ignore
    Traps: HiddenTraps # type: ignore
    DeathLink: HiddenDeathLink # type: ignore
    has_replaced_options: HasReplacedCamelCase

    def handle_backward_compatibility(self) -> None:
        if self.StartWithJewelryBox != StartWithJewelryBox.default and \
            self.start_with_jewelry_box == StartWithJewelryBox.default:
            self.start_with_jewelry_box.value = self.StartWithJewelryBox.value
            self.has_replaced_options.value = Toggle.option_true
        if self.DownloadableItems != DownloadableItems.default and \
            self.downloadable_items == DownloadableItems.default:
            self.downloadable_items.value = self.DownloadableItems.value
            self.has_replaced_options.value = Toggle.option_true
        if self.EyeSpy != EyeSpy.default and \
            self.eye_spy == EyeSpy.default:
            self.eye_spy.value = self.EyeSpy.value
            self.has_replaced_options.value = Toggle.option_true
        if self.StartWithMeyef != StartWithMeyef.default and \
            self.start_with_meyef == StartWithMeyef.default:
            self.start_with_meyef.value = self.StartWithMeyef.value
            self.has_replaced_options.value = Toggle.option_true
        if self.QuickSeed != QuickSeed.default and \
            self.quick_seed == QuickSeed.default:
            self.quick_seed.value = self.QuickSeed.value
            self.has_replaced_options.value = Toggle.option_true
        if self.SpecificKeycards != SpecificKeycards.default and \
            self.specific_keycards == SpecificKeycards.default:
            self.specific_keycards.value = self.SpecificKeycards.value
            self.has_replaced_options.value = Toggle.option_true
        if self.Inverted != Inverted.default and \
            self.inverted == Inverted.default:
            self.inverted.value = self.Inverted.value
            self.has_replaced_options.value = Toggle.option_true
        if self.GyreArchives != GyreArchives.default and \
            self.gyre_archives == GyreArchives.default:
            self.gyre_archives.value = self.GyreArchives.value
            self.has_replaced_options.value = Toggle.option_true
        if self.Cantoran != Cantoran.default and \
            self.cantoran == Cantoran.default:
            self.cantoran.value = self.Cantoran.value
            self.has_replaced_options.value = Toggle.option_true
        if self.LoreChecks != LoreChecks.default and \
            self.lore_checks == LoreChecks.default:
            self.lore_checks.value = self.LoreChecks.value
            self.has_replaced_options.value = Toggle.option_true
        if self.BossRando != BossRando.default and \
            self.boss_rando == BossRando.default:
            self.boss_rando.value = self.BossRando.value
            self.has_replaced_options.value = Toggle.option_true
        if self.EnemyRando != EnemyRando.default and \
            self.enemy_rando == EnemyRando.default:
            self.enemy_rando.value = self.EnemyRando.value
            self.has_replaced_options.value = Toggle.option_true
        if self.DamageRando != DamageRando.default and \
            self.damage_rando == DamageRando.default:
            self.damage_rando.value = self.DamageRando.value
            self.has_replaced_options.value = Toggle.option_true
        if self.DamageRandoOverrides != DamageRandoOverrides.default and \
            self.damage_rando_overrides == DamageRandoOverrides.default:
            self.damage_rando_overrides.value = self.DamageRandoOverrides.value
            self.has_replaced_options.value = Toggle.option_true
        if self.HpCap != HpCap.default and \
            self.hp_cap == HpCap.default:
            self.hp_cap.value = self.HpCap.value
            self.has_replaced_options.value = Toggle.option_true
        if self.LevelCap != LevelCap.default and \
            self.level_cap == LevelCap.default:
            self.level_cap.value = self.LevelCap.value
            self.has_replaced_options.value = Toggle.option_true
        if self.ExtraEarringsXP != ExtraEarringsXP.default and \
            self.extra_earrings_xp == ExtraEarringsXP.default:
            self.extra_earrings_xp.value = self.ExtraEarringsXP.value
            self.has_replaced_options.value = Toggle.option_true
        if self.BossHealing != BossHealing.default and \
            self.boss_healing == BossHealing.default:
            self.boss_healing.value = self.BossHealing.value
            self.has_replaced_options.value = Toggle.option_true
        if self.ShopFill != ShopFill.default and \
            self.shop_fill == ShopFill.default:
            self.shop_fill.value = self.ShopFill.value
            self.has_replaced_options.value = Toggle.option_true
        if self.ShopWarpShards != ShopWarpShards.default and \
            self.shop_warp_shards == ShopWarpShards.default:
            self.shop_warp_shards.value = self.ShopWarpShards.value
            self.has_replaced_options.value = Toggle.option_true
        if self.ShopMultiplier != ShopMultiplier.default and \
            self.shop_multiplier == ShopMultiplier.default:
            self.shop_multiplier.value = self.ShopMultiplier.value
            self.has_replaced_options.value = Toggle.option_true
        if self.LootPool != LootPool.default and \
            self.loot_pool == LootPool.default:
            self.loot_pool.value = self.LootPool.value
            self.has_replaced_options.value = Toggle.option_true
        if self.DropRateCategory != DropRateCategory.default and \
            self.drop_rate_category == DropRateCategory.default:
            self.drop_rate_category.value = self.DropRateCategory.value
            self.has_replaced_options.value = Toggle.option_true
        if self.FixedDropRate != FixedDropRate.default and \
            self.fixed_drop_rate == FixedDropRate.default:
            self.fixed_drop_rate.value = self.FixedDropRate.value
            self.has_replaced_options.value = Toggle.option_true
        if self.LootTierDistro != LootTierDistro.default and \
            self.loot_tier_distro == LootTierDistro.default:
            self.loot_tier_distro.value = self.LootTierDistro.value
            self.has_replaced_options.value = Toggle.option_true
        if self.ShowBestiary != ShowBestiary.default and \
            self.show_bestiary == ShowBestiary.default:
            self.show_bestiary.value = self.ShowBestiary.value
            self.has_replaced_options.value = Toggle.option_true
        if self.ShowDrops != ShowDrops.default and \
            self.show_drops == ShowDrops.default:
            self.show_drops.value = self.ShowDrops.value
            self.has_replaced_options.value = Toggle.option_true
        if self.EnterSandman != EnterSandman.default and \
            self.enter_sandman == EnterSandman.default:
            self.enter_sandman.value = self.EnterSandman.value
            self.has_replaced_options.value = Toggle.option_true
        if self.DadPercent != DadPercent.default and \
            self.dad_percent == DadPercent.default:
            self.dad_percent.value = self.DadPercent.value
            self.has_replaced_options.value = Toggle.option_true
        if self.RisingTides != RisingTides.default and \
            self.rising_tides == RisingTides.default:
            self.rising_tides.value = self.RisingTides.value
            self.has_replaced_options.value = Toggle.option_true
        if self.RisingTidesOverrides != RisingTidesOverrides.default and \
            self.rising_tides_overrides == RisingTidesOverrides.default:
            self.rising_tides_overrides.value = self.RisingTidesOverrides.value
            self.has_replaced_options.value = Toggle.option_true
        if self.UnchainedKeys != UnchainedKeys.default and \
            self.unchained_keys == UnchainedKeys.default:
            self.unchained_keys.value = self.UnchainedKeys.value
            self.has_replaced_options.value = Toggle.option_true
        if self.PresentAccessWithWheelAndSpindle != PresentAccessWithWheelAndSpindle.default and \
            self.back_to_the_future == PresentAccessWithWheelAndSpindle.default:
            self.back_to_the_future.value = self.PresentAccessWithWheelAndSpindle.value
            self.has_replaced_options.value = Toggle.option_true
        if self.TrapChance != TrapChance.default and \
            self.trap_chance == TrapChance.default:
            self.trap_chance.value = self.TrapChance.value
            self.has_replaced_options.value = Toggle.option_true
        if self.Traps != Traps.default and \
            self.traps == Traps.default:
            self.traps.value = self.Traps.value
            self.has_replaced_options.value = Toggle.option_true
        if self.DeathLink != DeathLink.default and \
            self.death_link == DeathLink.default:
            self.death_link.value = self.DeathLink.value
            self.has_replaced_options.value = Toggle.option_true
