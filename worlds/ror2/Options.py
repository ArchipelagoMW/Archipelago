from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, DeathLink, Range, Choice, PerGameCommonOptions


# NOTE be aware that since the range of item ids that RoR2 uses is based off of the maximums of checks
# Be careful when changing the range_end values not to go into another game's IDs
# NOTE that these changes to range_end must also be reflected in the RoR2 client so it understands the same ids.

class Goal(Choice):
    """
    Classic Mode: Every Item pickup increases fills a progress bar which gives location checks.

    Explore Mode: Each environment will have location checks within each environment.
    environments will be locked in the item pool until received.
    """
    display_name = "Game Mode"
    option_classic = 0
    option_explore = 1
    default = 1


class TotalLocations(Range):
    """Classic Mode: Number of location checks which are added to the Risk of Rain playthrough."""
    display_name = "Total Locations"
    range_start = 40
    range_end = 250
    default = 40


class ChestsPerEnvironment(Range):
    """Explore Mode: The number of chest locations per environment."""
    display_name = "Chests per Environment"
    range_start = 2
    range_end = 20
    default = 10


class ShrinesPerEnvironment(Range):
    """Explore Mode: The number of shrine locations per environment."""
    display_name = "Shrines per Environment"
    range_start = 2
    range_end = 20
    default = 5


class ScavengersPerEnvironment(Range):
    """Explore Mode: The number of scavenger locations per environment."""
    display_name = "Scavenger per Environment"
    range_start = 0
    range_end = 1
    default = 0


class ScannersPerEnvironment(Range):
    """Explore Mode: The number of scanners locations per environment."""
    display_name = "Radio Scanners per Environment"
    range_start = 0
    range_end = 1
    default = 1


class AltarsPerEnvironment(Range):
    """Explore Mode: The number of altars locations per environment."""
    display_name = "Newts Per Environment"
    range_start = 0
    range_end = 2
    default = 1


class TotalRevivals(Range):
    """Total Percentage of `Dio's Best Friend` item put in the item pool."""
    display_name = "Total Revives as percentage"
    range_start = 0
    range_end = 10
    default = 4


class ItemPickupStep(Range):
    """
    Number of items to pick up before an AP Check is completed.
    Setting to 1 means every other pickup.
    Setting to 2 means every third pickup. So on...
    """
    display_name = "Item Pickup Step"
    range_start = 0
    range_end = 5
    default = 1


class ShrineUseStep(Range):
    """
    Explore Mode:
    Number of shrines to use up before an AP Check is completed.
    Setting to 1 means every other pickup.
    Setting to 2 means every third pickup. So on...
    """
    display_name = "Shrine use Step"
    range_start = 0
    range_end = 3
    default = 0


class AllowLunarItems(DefaultOnToggle):
    """Allows Lunar items in the item pool."""
    display_name = "Enable Lunar Item Shuffling"


class StartWithRevive(DefaultOnToggle):
    """Start the game with a `Dio's Best Friend` item."""
    display_name = "Start with a Revive"


class FinalStageDeath(Toggle):
    """The following will count as a win if set to true:
    Dying in Commencement.
    Dying in The Planetarium.
    Obliterating yourself"""
    display_name = "Final Stage Death is Win"


class BeginWithLoop(Toggle):
    """
    Enable to precollect a full loop of environments.
    Only has an effect with Explore Mode.
    """
    display_name = "Begin With Loop"


class DLC_SOTV(Toggle):
    """
     Enable if you are using SOTV DLC.
     Affects environment availability for Explore Mode.
     Adds Void Items into the item pool
     """
    display_name = "Enable DLC - SOTV"


class GreenScrap(Range):
    """Weight of Green Scraps in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Green Scraps"
    range_start = 0
    range_end = 100
    default = 16


class RedScrap(Range):
    """Weight of Red Scraps in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Red Scraps"
    range_start = 0
    range_end = 100
    default = 4


class YellowScrap(Range):
    """Weight of yellow scraps in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Yellow Scraps"
    range_start = 0
    range_end = 100
    default = 1


class WhiteScrap(Range):
    """Weight of white scraps in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "White Scraps"
    range_start = 0
    range_end = 100
    default = 32


class CommonItem(Range):
    """Weight of common items in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Common Items"
    range_start = 0
    range_end = 100
    default = 64


class UncommonItem(Range):
    """Weight of uncommon items in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Uncommon Items"
    range_start = 0
    range_end = 100
    default = 32


class LegendaryItem(Range):
    """Weight of legendary items in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Legendary Items"
    range_start = 0
    range_end = 100
    default = 8


class BossItem(Range):
    """Weight of boss items in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Boss Items"
    range_start = 0
    range_end = 100
    default = 4


class LunarItem(Range):
    """Weight of lunar items in the item pool.

    (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Lunar Items"
    range_start = 0
    range_end = 100
    default = 16


class VoidItem(Range):
    """Weight of void items in the item pool.

    (Ignored unless Item Weight Presets is 'No')

    (Ignored if Enable DLC - SOTV is 'No') """
    display_name = "Void Items"
    range_start = 0
    range_end = 100
    default = 16


class Equipment(Range):
    """Weight of equipment items in the item pool.

     (Ignored unless Item Weight Presets is 'No')"""
    display_name = "Equipment"
    range_start = 0
    range_end = 100
    default = 32


class ItemPoolPresetToggle(Toggle):
    """Will use the item weight presets when set to true, otherwise will use the custom set item pool weights."""
    display_name = "Use Item Weight Presets"


class ItemWeights(Choice):
    """Set item_pool_presets to true if you want to use one of these presets.
    Preset choices for determining the weights of the item pool.
    - New is a test for a potential adjustment to the default weights.
    - Uncommon puts a large number of uncommon items in the pool.
    - Legendary puts a large number of legendary items in the pool.
    - Lunartic makes everything a lunar item.
    - Chaos generates the pool completely at random with rarer items having a slight cap to prevent this option being too easy.
    - No Scraps removes all scrap items from the item pool.
    - Even generates the item pool with every item having an even weight.
    - Scraps Only will be only scrap items in the item pool.
    - Void makes everything a void item."""
    display_name = "Item Weights"
    option_default = 0
    option_new = 1
    option_uncommon = 2
    option_legendary = 3
    option_lunartic = 4
    option_chaos = 5
    option_no_scraps = 6
    option_even = 7
    option_scraps_only = 8
    option_void = 9


@dataclass
class ROR2Options(PerGameCommonOptions):
    goal: Goal
    total_locations: TotalLocations
    chests_per_stage: ChestsPerEnvironment
    shrines_per_stage: ShrinesPerEnvironment
    scavengers_per_stage: ScavengersPerEnvironment
    scanner_per_stage: ScannersPerEnvironment
    altars_per_stage: AltarsPerEnvironment
    total_revivals: TotalRevivals
    start_with_revive: StartWithRevive
    final_stage_death: FinalStageDeath
    begin_with_loop: BeginWithLoop
    dlc_sotv: DLC_SOTV
    death_link: DeathLink
    item_pickup_step: ItemPickupStep
    shrine_use_step: ShrineUseStep
    enable_lunar: AllowLunarItems
    item_weights: ItemWeights
    item_pool_presets: ItemPoolPresetToggle
    # define the weights of the generated item pool.
    green_scrap: GreenScrap
    red_scrap: RedScrap
    yellow_scrap: YellowScrap
    white_scrap: WhiteScrap
    common_item: CommonItem
    uncommon_item: UncommonItem
    legendary_item: LegendaryItem
    boss_item: BossItem
    lunar_item: LunarItem
    void_item: VoidItem
    equipment: Equipment
