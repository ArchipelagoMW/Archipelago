from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Range, Toggle, DefaultOnToggle

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

class ShowGoldenChests(DefaultOnToggle):
    """Turns chests that contain items required for progression into golden chests."""
    display_name = "Progression Items in Golden Chests"

class SkipCutscenes(DefaultOnToggle):
    """Skip major cutscenes."""
    display_name = "Skip Cutscenes"

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
    Easy: Locations will be considered inaccessible until the player has enough golden feathers to easily reach them
    Normal: Locations will be considered inaccessible until the player has the minimum possible number of golden feathers to reach them
    Hard: Removes the requirement of golden feathers for progression entirely and glitches may need to be used to progress"""
    display_name = "Golden Feather Progression"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1

@dataclass
class ShortHikeOptions(PerGameCommonOptions):
    goal: Goal
    show_golden_chests: ShowGoldenChests
    skip_cutscenes: SkipCutscenes
    coins_in_shops: CoinsInShops
    golden_feathers: GoldenFeathers
    silver_feathers: SilverFeathers
    buckets: Buckets
    golden_feather_progression: GoldenFeatherProgression