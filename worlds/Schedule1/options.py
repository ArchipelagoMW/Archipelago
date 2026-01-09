from dataclasses import dataclass

from Options import (Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, 
                    Range, Toggle)

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
class Goal(Choice):
    """
    The goal to win the game.
    missions_networth: Reach a specificed net worth and complete the main story.
    networth_only: Reach a specificed net worth.
    missions_only: Complete the main story.
    """
    
    display_name = "Goal"

    option_missions_networth = 0
    option_networth_only = 1
    option_missions_only = 2

    # Choice options must define an explicit default value.
    default = option_missions_networth

class RandomizeLevelUnlocks(DefaultOnToggle):
    """
    Leveling up is always a check regardless of this option.
    Block Boss I, 30,350xp, will be the highest checks will go to.
    Things you unlock by leveling up will be shuffled into the item pool if this option is enabled.
    When this is enabled, you will no longer get level up rewards naturally.
    """
    display_name = "Randomize Level Unlocks"


class NumberOfXpBundles(Range):
    """
    Number of XP bundles to include in the item pool.
    min to max xp bundles will be interpolated based on number of bundles.
    Meaning there will be 1 min bundle and 1 max bundle and the rest will be evenly distributed in between.
    If default min/max are used, 25 bundles give max level xp. 12 gives out about a quarter of that.
    16,425 xp is needed to complete the game, but this can be done naturally, bundles speed up process.
    If 1 bundle is chosen, only the minimum xp bundle will be in the item pool.
    """
    range_start = 0
    range_end = 100
    default = 12


class AmountOfXpPerBundleMin(Range):
    """
    Min amount of XP per bundle included in the item pool.
    Each bundle is worth the specified amount of XP.
    This option is only relevant if NumberOfXpBundles > 0.
    """
    range_start = 1
    range_end = 1000
    default = 100


class AmountOfXpPerBundleMax(Range):
    """
    Max amount of XP per bundle included in the item pool.
    Each bundle is worth the specified amount of XP.
    This option is only relevant if NumberOfXpBundles > 0.
    """
    range_start = 1000
    range_end = 10000
    default = 5000


class NumberOfCashBundles(Range):
    """
    Number of cash bundles to include in the item pool.
    min to max cash bundles will be interpolated based on number of bundles.
    Meaning there will be 1 min bundle and 1 max bundle and the rest will be evenly distributed in between.
    If 1 bundle is chosen, only the minimum cash bundle will be in the item pool.
    Defaults will give out ~87k cash with 20 bundles. 46 bundles gives out ~200k cash.
    """
    range_start = 0
    range_end = 100
    default = 20


class AmountOfCashPerBundleMin(Range):
    """
    Min amount of cash per bundle included in the item pool.
    Each bundle is worth the specified amount of cash.
    This option is only relevant if NumberOfCashBundles > 0.
    """
    range_start = 1
    range_end = 1500
    default = 1500


class AmountOfCashPerBundleMax(Range):
    """
    Max amount of cash per bundle included in the item pool.
    Each bundle is worth the specified amount of cash.
    This option is only relevant if NumberOfCashBundles > 0.
    """
    range_start = 1500
    range_end = 100000
    default = 10000


class NetworthAmountRequired(Range):
    """
    The net worth amount required to win the game.
    This option is only relevant if the goal includes net worth.
    """
    range_start = 10000
    range_end = 10000000
    default = 100000


class FillerItemPoolType(Choice):
    """
    Determines which non-progress items are included in the item pool.
    - Random: Filler item pool consists of random non-progress items.
    - Random: No Bad Items: Filler items consist of non-bad filler items.
    - Random: Only Good Items: Filler items consist of only good filler items.
    """
    
    display_name = "Filler Item Pool Type"

    option_random_distribution = 0
    option_random_no_bad_items = 1
    option_random_only_good_items = 2
    random = 3

    default = option_random_distribution


class RandomizeCartelInfluence(DefaultOnToggle):
    """
    Determines if cartel influence will be randomized into the item pool.
    7 Bundles of 100 cartel influence per in-game region that applies.
    Every 100 cartel influcence by the player counts as a check regardless of this option.
    This option removes the player's ability to earn cartel influence naturally
    """
    display_name = "Randomize Cartel Influence"


class CartelInfluenceChecksPerRegion(Range):
    """
    Number of cartel influence checks to include in the item pool per region.
    Each check is worth 100 cartel influence.
    7 needed to unlock region, recommend to add extra of each region.
    This option is only relevant if Randomize Cartel Influence is enabled.
    """
    range_start = 7
    range_end = 20
    default = 10


class RandomizeDrugMakingProperties(DefaultOnToggle):
    """
    Determines if drug making properties will be added into the item pool.
    Purchasing drug making properties become checks, but you do not purchase them.
    Realtor will have AP items instead of drug making properties if this is enabled.
    This does not include ones you must purchase through missions or the sewer office.
    """
    display_name = "Randomize drug making Properties"


class RandomizeBusinessProperties(DefaultOnToggle):
    """
    Determines if business properties will be added into the item pool.
    The Realtor will have AP items instead of business properties if this is enabled.
    """
    display_name = "Randomize business making Properties"


class RandomizeDealers(DefaultOnToggle):
    """
    Determines if dealers will be added into the item pool.
    Recruiting dealers become checks, but you do not recruit them.
    This does not include Benji, who is required for story progression.
    """
    display_name = "Randomize Dealers"


class RandomizeCustomers(Choice):
    """
    Determines if customers will be added into the item pool.
    - None: Do not randomize customers
    - Checks: Unlocking customers are a check that also unlocks the customer.
    - Full: Customers are randomized into the item pool. Unlocking customers in game is only a check.
    """
    display_name = "Randomize Customers"

    option_none = 0
    option_checks = 1
    option_full = 2
    random = 3

    default = option_checks

class RecipeChecks(Range):
    """
    Number of recipe checks to include in the item pool.
    These are recipes per drug type.
    10 means 10 weed recipes, 10 meth recipes, etc. 
    """
    range_start = 0
    range_end = 15
    default = 5

class CashForTrash(Range):
    """
    Number of checks for each 10 pieces of trash collected
    50 = 500 total pieces of trash which is equal to the achiemvement.
    """
    range_start = 0
    range_end = 50
    default = 5
    

# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class Schedule1Options(PerGameCommonOptions):
    goal: Goal
    networth_amount_required: NetworthAmountRequired
    filler_item_pool_type: FillerItemPoolType
    number_of_xp_bundles: NumberOfXpBundles
    amount_of_xp_per_bundle_min: AmountOfXpPerBundleMin
    amount_of_xp_per_bundle_max: AmountOfXpPerBundleMax
    number_of_cash_bundles: NumberOfCashBundles
    amount_of_cash_per_bundle_min: AmountOfCashPerBundleMin
    amount_of_cash_per_bundle_max: AmountOfCashPerBundleMax
    randomize_level_unlocks: RandomizeLevelUnlocks
    randomize_cartel_influence: RandomizeCartelInfluence
    cartel_influence_checks_per_region: CartelInfluenceChecksPerRegion
    randomize_drug_making_properties: RandomizeDrugMakingProperties
    randomize_business_properties: RandomizeBusinessProperties
    randomize_dealers: RandomizeDealers
    randomize_customers: RandomizeCustomers
    recipe_checks: RecipeChecks
    cash_for_trash: CashForTrash



# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Gameplay Options",
        [Goal, NumberOfXpBundles, AmountOfXpPerBundleMin, AmountOfXpPerBundleMax, NumberOfCashBundles,
         AmountOfCashPerBundleMin, AmountOfCashPerBundleMax, NetworthAmountRequired, FillerItemPoolType,
         RandomizeCartelInfluence, RandomizeDrugMakingProperties, RandomizeLevelUnlocks,
         RandomizeBusinessProperties, RandomizeDealers, RandomizeCustomers, RecipeChecks, CashForTrash,
         CartelInfluenceChecksPerRegion],
    )
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "Default": {
        "goal": Goal.default,
        "number_of_xp_bundles": NumberOfXpBundles.default,
        "amount_of_xp_per_bundle_min": AmountOfXpPerBundleMin.default,
        "amount_of_xp_per_bundle_max": AmountOfXpPerBundleMax.default,
        "number_of_cash_bundles": NumberOfCashBundles.default,
        "amount_of_cash_per_bundle_min": AmountOfCashPerBundleMin.default,
        "amount_of_cash_per_bundle_max": AmountOfCashPerBundleMax.default,
        "networth_amount_required": NetworthAmountRequired.default,
        "filler_item_pool_type": FillerItemPoolType.default,
        "randomize_cartel_influence": True,
        "randomize_drug_making_properties": True,
        "randomize_business_properties": True,
        "randomize_dealers": True,
        "randomize_customers": RandomizeCustomers.default,
        "cartel_influence_checks_per_region": CartelInfluenceChecksPerRegion.default,
        "recipe_checks": RecipeChecks.default,
        "cash_for_trash": CashForTrash.default,
        "randomize_level_unlocks": True,
    }
}
