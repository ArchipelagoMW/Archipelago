from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Range, StartInventoryPool, Toggle

class Goal(Choice):
    """Choose the end goal.
    Nap: Complete the climb to the top of Hawk Peak and take a nap
    Photo: Get your picture taken at the top of Hawk Peak
    Races: Complete all three races with Avery
    Help Everyone: Travel around Hawk Peak and help every character with their troubles
    Fishmonger: Catch one of every fish from around Hawk Peak"""
    display_name = "Goal"
    option_nap = 0
    option_photo = 1
    option_races = 2
    option_help_everyone = 3
    option_fishmonger = 4
    default = 3

class CoinsInShops(Toggle):
    """When enabled, the randomizer can place coins into locations that are purchased, such as shops."""
    display_name = "Coins in Purchaseable Locations"
    default = False

class GoldenFeathers(Range):
    """Number of Golden Feathers in the item pool.
    (Note that for the Photo and Help Everyone goals, a minimum of 12 Golden Feathers is enforced)"""
    display_name = "Golden Feathers"
    range_start = 0
    range_end = 20
    default = 20

class SilverFeathers(Range):
    """Number of Silver Feathers in the item pool."""
    display_name = "Silver Feathers"
    range_start = 0
    range_end = 20
    default = 2

class Buckets(Range):
    """Number of Buckets in the item pool."""
    display_name = "Buckets"
    range_start = 0
    range_end = 2
    default = 2

class GoldenFeatherProgression(Choice):
    """Determines which locations are considered in logic based on the required amount of golden feathers to reach them.
    Easy: Locations will be considered inaccessible until the player has enough golden feathers to easily reach them. A minimum of 10 golden feathers is recommended for this setting.
    Normal: Locations will be considered inaccessible until the player has the minimum possible number of golden feathers to reach them. A minimum of 7 golden feathers is recommended for this setting.
    Hard: Removes the requirement of golden feathers for progression entirely and glitches may need to be used to progress"""
    display_name = "Golden Feather Progression"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1

class CostMultiplier(Range):
    """The percentage that all item shop costs will be of the vanilla values."""
    display_name = "Shop Cost Multiplier"
    range_start = 25
    range_end = 200
    default = 100

class FillerCoinAmount(Choice):
    """The number of coins that will be in each filler coin item."""
    display_name = "Coins per Filler Item"
    option_7_coins = 0
    option_13_coins = 1
    option_15_coins = 2
    option_18_coins = 3
    option_21_coins = 4
    option_25_coins = 5
    option_27_coins = 6
    option_32_coins = 7
    option_33_coins = 8
    option_50_coins = 9
    default = 1

@dataclass
class ShortHikeOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    coins_in_shops: CoinsInShops
    golden_feathers: GoldenFeathers
    silver_feathers: SilverFeathers
    buckets: Buckets
    golden_feather_progression: GoldenFeatherProgression
    cost_multiplier: CostMultiplier
    filler_coin_amount: FillerCoinAmount
