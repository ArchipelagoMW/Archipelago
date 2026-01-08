from dataclasses import dataclass

from Options import DeathLink, DefaultOnToggle, OptionCounter, OptionSet, Toggle, Range, PerGameCommonOptions


class ForceLategame(DefaultOnToggle):
    """
    By enabling this the generation tries to avoid placing Unlocks for "early" Areas like Womb into lategame areas like Home.
    This avoid situations where the first path of progression would already be to one of the endgame bossses like Beast when you don't even have the Womb unlocked yet.
    Overall this leads to a smoother progression curve where first the easier paths open up before the hard ones.
    But experienced players may want to embrace the challenge of having to do the hard parts first when their runs are still fairly weak and disable this.
    """
    display_name = "Force Lategame to be late"

class WinCollectsMissedLocations(DefaultOnToggle):
    """
    By enabling this, succesfully winning a run unlocks all the room location checks you missed or which didn't spawn on all the stages you went through during that run.
    That means, even if a Mini Boss room didn't spawn in the Flooded Caves, you'll still get the unlock if you have been to the Flooded Caves during that run if you end it with a win.
    """
    display_name = "Win collects missed locations"

class FortunesAreHints(DefaultOnToggle):
    """
    By enabling this, playing a Fortune Telling machine gives you a hint for an item in your world.
    The hints are completly random and mostly include hints for Junk items so you'll still have to spend quite a bit of money until you get a hint for something usefull.
    """
    display_name = "Fornues are Hints"

class Goals(OptionSet):
    """
    Set of all bosses you'll have to beat to sucessfully win the game.
    Valid bosses are: ["Mom", "Mom's Heart", "Isaac", "Satan", "Blue Baby", "The Lamb", "Mega Satan", "Boss Rush", "Hush", "Beast", "Mother", "Delirium"]
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
        "Delirium"
    })
    default = frozenset({"Mega Satan", "Beast", "Mother", "Delirium"})

class ExcludeAreas(OptionSet):
    """
    Entire areas to exclude from the game. By excluding an area, none of the entrance methods to the area will be able to spawn and neither are locations placed in those areas.
    Valid areas are: ["The Void", "Ascend", "Alt Path", "Timed Areas"]
    """
    display_name = "Excluded areas"

    valid_keys = frozenset({"The Void", "Ascend", "Alt Path", "Timed Areas"})
    default = frozenset({})

class AdditionalItemLocations(Range):
    """
    Number of available AP Items that occasinally replace regular items.
    Picking up an AP Item is a location check. Once all the checks have been completed no more AP Items will spawn.
    """
    display_name = "Additional Item Locations"
    range_start = 0
    range_end = 300
    default = 80

class ItemLocationStep(Range):
    """
    Frequency of how many Items are replaced by AP Items.
    1 means, every item you see
    2 means, every second item you see
    etc.
    Fixed item drops are not replaced, only those that roll a random item from an item pool.
    """
    display_name = "Item Location Step"
    range_start = 1
    range_end = 5
    default = 3

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
    default = 85

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
        "Red Chest Item": 1,
        "Secret Room Item": 8,
        "Shop Item": 15,
        "Treasure Room Item": 15
    }

class RetainItemsPercentage(Range):
    """
    Fraction of the items you received that are re-given to you on a new run.
    """
    display_name = "Retain Items percentage"
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
    display_name = "Retain Junk percentage"
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
    Amount of 1-UPs you can receive during the session. Usefull for balancing out the death link.
    """
    display_name = "1-UPs"
    range_start = 0
    range_end = 10
    default = 3

class RetainOneUpsPercentage(Range):
    """
    Fraction of the 1-UPs you received that are re-given to you on a new run. (Will always be given immediately and not spread across floors.)
    """
    display_name = "Retain 1-UPs percentage"
    range_start = 0
    range_end = 100
    default = 100
    
@dataclass
class TboiOptions(PerGameCommonOptions):
    goals: Goals
    excluded_areas: ExcludeAreas
    force_lategame: ForceLategame
    win_collects_missed_locations: WinCollectsMissedLocations
    scatter_previous_items: ScatterPreviousItems
    additional_boss_rewards: AdditionalBossRewards
    fortunes_are_hints: FortunesAreHints
    additional_item_locations: AdditionalItemLocations
    item_location_step: ItemLocationStep
    item_weights: ItemWeights
    retain_items_percentage: RetainItemsPercentage
    junk_percentage: JunkPercentage
    junk_weights: JunkWeights
    retain_junk_percentage: RetainJunkPercentage
    trap_percentage: TrapPercentage
    trap_weights: TrapWeights
    deathlink: DeathLink
    one_ups: OneUps
    retain_one_ups_percentage: RetainOneUpsPercentage