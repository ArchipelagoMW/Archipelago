from dataclasses import dataclass

from Options import DeathLink, DefaultOnToggle, OptionCounter, OptionSet, Range, PerGameCommonOptions


class BadRNGProtection(DefaultOnToggle):
    """
    By enabling this, successfully winning a run unlocks all the room location checks per stage which didn't spawn on all the stages you went through during that run.
    That means, even if a Mini Boss room didn't spawn in the Flooded Caves, you'll still get the unlock if you have been to the Flooded Caves during that run upon finishing the run successfully.
    (Room Types that can be checked this way: Arcade, Challenge Room, Curse Room and Sacrifice Room)
    """
    display_name = "Bad RNG Protection"

class FortuneMachineHintPercentage(Range):
    """
    Chance for a Fortune Telling Machine to give a hint.
    """
    display_name = "Fortune Machine Hint Percentage"
    range_start = 0
    range_end = 100
    default = 30

class CrystalBallHintPercentage(Range):
    """
    Chance for a Crystal Ball to give a hint.
    """
    display_name = "Crystal Ball Hint Percentage"
    range_start = 0
    range_end = 100
    default = 100

class FortuneCookieHintPercentage(Range):
    """
    Chance for a Fortune Cookie to give a hint.
    """
    display_name = "Fortune Cookie Hint Percentage"
    range_start = 0
    range_end = 100
    default = 50

class HintTypesFromFortunes(OptionSet):
    """
    The type of items you are able to get Hints for through fortunes.
    Valid types are: ["Progression Items", "Useful Items", "Junk Items", "Traps"]
    """
    display_name = "Hint types from Fortunes"

    valid_keys = frozenset({
        "Progression Items",
        "Useful Items",
        "Junk Items",
        "Traps"
    })
    default = frozenset({"Progression Items", "Useful Items"})

class Goals(OptionSet):
    """
    Set of all bosses you'll have to beat to successfully win the game.
    Valid bosses are: ["Mom", "Mom's Heart", "Isaac", "Satan", "Blue Baby", "The Lamb", "Mega Satan", "Boss Rush", "Hush", "Beast", "Mother", "Delirium"]
    Can also be set to "All" to include all bosses, or "Random-#", where # determines the number of random bosses. For example ["Isaac", "Random-3"] will select Isaac and 3 random other Bosses
    """
    display_name = "Goals"

    valid_keys = frozenset({
        "Mom",
        "Mom's Heart",
        "Isaac",
        "Satan",
        "Blue Baby",
        "The Lamb",
        "Mega Satan",
        "Boss Rush",
        "Hush",
        "Beast",
        "Mother",
        "Delirium",
        "All",
        "Random-1",
        "Random-2",
        "Random-3",
        "Random-4",
        "Random-5",
        "Random-6",
        "Random-7",
        "Random-8",
        "Random-9",
        "Random-10",
        "Random-11"
    })
    default = frozenset({"Mega Satan", "Beast", "Mother", "Delirium"})

class ExcludedAreas(OptionSet):
    """
    Entire areas to exclude from the game. By excluding an area, none of the entrance methods to the area will be able to spawn and no location checks will be placed in those areas.
    Valid areas are: ["The Void", "Ascend", "Alt Path", "Timed Areas"]
    """
    display_name = "Excluded areas"

    valid_keys = frozenset({"The Void", "Ascend", "Alt Path", "Timed Areas"})
    default = frozenset({})

class AdditionalItemLocationsPerStage(OptionCounter):
    """
    Number of available AP Items that occasionally replace regular items.
    Picking up an AP Item is a location check. Once all the checks have been completed no more AP Items will spawn.
    (Maximum 10 per floor)
    """
    display_name = "Additional Item Locations per Stage"
    valid_keys = frozenset({
        "Basement",
        "Cellar",
        "Burning Basement",
        "Caves",
        "Catacombs",
        "Flooded Caves",
        "Depths",
        "Necropolis",
        "Dank Depths",
        "Boss Rush",
        "Womb",
        "Utero",
        "Scarred Womb",
        "???",
        "Cathedral",
        "Sheol",
        "Chest",
        "Dark Room",
        "The Void",
        "Downpour",
        "Dross",
        "Mines",
        "Ashpit",
        "Mausoleum",
        "Gehenna",
        "Corpse",
        "Home"
    })
    min = 0
    max = 10
    default = {
        "Basement": 3,
        "Cellar": 3,
        "Burning Basement": 3,
        "Caves": 3,
        "Catacombs": 3,
        "Flooded Caves": 3,
        "Depths": 3,
        "Necropolis": 3,
        "Dank Depths": 3,
        "Boss Rush": 1,
        "Womb": 1,
        "Utero": 1,
        "Scarred Womb": 1,
        "???": 2,
        "Cathedral": 0,
        "Sheol": 0,
        "Chest": 2,
        "Dark Room": 2,
        "The Void": 3,
        "Downpour": 3,
        "Dross": 3,
        "Mines": 3,
        "Ashpit": 3,
        "Mausoleum": 3,
        "Gehenna": 3,
        "Corpse": 1,
        "Home": 0
    }

class ItemLocationPercentage(Range):
    """
    Chance for an item to be replaced with an AP item (if there are still AP Item checks available for the current Stage)
    Fixed item drops are not replaced, only those that roll a random item from an item pool.
    """
    display_name = "Item Location Percentage"
    range_start = 0
    range_end = 100
    default = 50

class AdditionalBossRewards(DefaultOnToggle):
    """
    If enabled, beating each of the main bosses for the first time gives an additional amount of location checks:
    The amount of checks is determined by how deep the boss is in the run:
    Mom = 1
    Mom's Heart/Boss Rush = 2
    Isaac/Satan/Hush = 3
    Blue Baby/The Lamb = 4
    Mega Satan/Mother/Beast/Delirium = 5
    """
    display_name = "Additional Boss Rewards"

class ScatterPreviousItems(DefaultOnToggle):
    """
    When disabled, items you received in previous runs are given to you immediately on the start of a new run
    When enabled, items you received in previous runs are spread across the first six floors on a new run
    """
    display_name = "Scatter Previous Items"

class JunkPercentage(Range):
    """
    Percentage of junk items (Non-Collectable Pickups like Coins, Bombs etc.)
    """
    display_name = "Junk Percentage"
    range_start = 0
    range_end = 100
    default = 75

class TrapPercentage(Range):
    """
    Percentage of junk items to be replaced by traps
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 10

class ItemWeights(OptionCounter):
    """Specify the distribution of items that should be placed into the pool.

    If you don't want a specific type of item, set the weight to zero.
    """
    display_name = "Item Weights"
    valid_keys = frozenset({
        "Angel Deal Item",
        "Boss Item",
        "Curse Room Item",
        "Devil Deal Item",
        "Golden Chest Item",
        "Library Item",
        "Planetarium Item",
        "Red Chest Item",
        "Secret Room Item",
        "Shop Item",
        "Treasure Room Item"
    })
    min = 0
    default = {
        "Angel Deal Item": 6,
        "Boss Item": 12,
        "Curse Room Item": 4,
        "Devil Deal Item": 6,
        "Golden Chest Item": 8,
        "Library Item": 1,
        "Planetarium Item": 1,
        "Red Chest Item": 4,
        "Secret Room Item": 8,
        "Shop Item": 15,
        "Treasure Room Item": 15
    }

class RetainItemsPercentage(Range):
    """
    Fraction of the items you received that are re-given to you on a new run.
    """
    display_name = "Retain Items Percentage"
    range_start = 0
    range_end = 100
    default = 30

class JunkWeights(OptionCounter):
    """Specify the distribution of junk that should be placed into the pool.

    If you don't want a specific type of junk, set the weight to zero.
    """
    display_name = "Junk Weights"
    valid_keys = frozenset({
        "Random Bomb",
        "Random Card",
        "Random Chest",
        "Random Coin",
        "Random Heart",
        "Random Key",
        "Random Pill",
        "Random Trinket"
    })
    min = 0
    default = {
        "Random Bomb": 5,
        "Random Card": 3,
        "Random Chest": 2,
        "Random Coin": 6,
        "Random Heart": 5,
        "Random Key": 5,
        "Random Pill": 3,
        "Random Trinket": 1
    }

class RetainJunkPercentage(Range):
    """
    Fraction of the pickups you received that are re-given to you on a new run.
    """
    display_name = "Retain Junk Percentage"
    range_start = 0
    range_end = 100
    default = 10

class TrapWeights(OptionCounter):
    """Specify the distribution of traps that should be placed into the pool.

    If you don't want a specific type of trap, set the weight to zero.
    """
    display_name = "Trap Weights"
    valid_keys = frozenset({
        "Curse Trap",
        "Paralysis Trap",
        "Retro Vision Trap",
        "Teleport Trap",
        "Troll Bomb Trap",
        "Wavy Cap Trap"
    })
    min = 0
    default = {
        "Curse Trap": 20,
        "Paralysis Trap": 20,
        "Retro Vision Trap": 20,
        "Teleport Trap": 20,
        "Troll Bomb Trap": 20,
        "Wavy Cap Trap": 20
    }

class OneUps(Range):
    """
    Amount of 1-UPs you can receive during the session. Useful for balancing out the death link.
    """
    display_name = "1-UPs"
    range_start = 0
    range_end = 10
    default = 3

class RetainOneUpsPercentage(Range):
    """
    Fraction of the 1-UPs you received that are re-given to you on a new run. (Will always be given immediately and not spread across floors.)
    """
    display_name = "Retain 1-UPs Percentage"
    range_start = 0
    range_end = 100
    default = 100
    
class ExcludeItemsAsRewards(OptionSet):
    """
    Actively harmful items can be excluded here from being given as a reward to the player.
    Valid items are: ["A Pound of Flesh", "Blood Oath", "Blood Puppy", "Cursed Eye", "Curse of the Tower", "Isaac's Heart", "Kidney Stone", "Missing No", "Shard of Glass", "TMTrainer"]
    """
    display_name = "Exclude items as rewards"

    valid_keys = frozenset({
        "A Pound of Flesh",
        "Blood Oath",
        "Blood Puppy",
        "Cursed Eye",
        "Curse of the Tower",
        "Isaac's Heart",
        "Kidney Stone",
        "Missing No",
        "Shard of Glass",
        "TMTrainer"
    })
    default = frozenset({"Missing No", "TMTrainer"})

@dataclass
class TboiOptions(PerGameCommonOptions):
    goals: Goals
    excluded_areas: ExcludedAreas
    bad_rng_protection: BadRNGProtection
    additional_item_locations_per_stage: AdditionalItemLocationsPerStage
    item_location_percentage: ItemLocationPercentage
    additional_boss_rewards: AdditionalBossRewards
    scatter_previous_items: ScatterPreviousItems
    junk_percentage: JunkPercentage
    trap_percentage: TrapPercentage
    item_weights: ItemWeights
    retain_items_percentage: RetainItemsPercentage
    junk_weights: JunkWeights
    retain_junk_percentage: RetainJunkPercentage
    trap_weights: TrapWeights
    one_ups: OneUps
    retain_one_ups_percentage: RetainOneUpsPercentage
    exclude_items_as_rewards: ExcludeItemsAsRewards
    fortune_machine_hint_percentage: FortuneMachineHintPercentage
    crystal_ball_hint_percentage: CrystalBallHintPercentage
    fortune_cookie_hint_percentage: FortuneCookieHintPercentage
    hint_types_from_fortunes: HintTypesFromFortunes
    death_link: DeathLink
