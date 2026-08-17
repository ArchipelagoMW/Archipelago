from Options import Toggle, Choice, NamedRange, Range, PerGameCommonOptions, ItemsAccessibility
from dataclasses import dataclass


class ShuffleGoldenCoins(Choice):
    """
    Vanilla: Golden Coins are received when defeating bosses.
    Shuffle: Shuffle the Golden Coins into the item pool and make bosses location checks.
    Mario Coin Fragment Hunt: You start with all Golden Coins except the Mario Coin, which has been fragmented into many pieces.
    You will see a Golden Coin being received when defeating bosses regardless of whether you are actually getting a coin.
    """
    display_name = "Shuffle Golden Coins"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_mario_coin_fragment_hunt = 2


class GoldenCoinsRequired(Range):
    """
    Number of Golden Coins required to enter Mario's Castle. Ignored on Mario Coin Fragment Hunt.
    """
    display_name = "Golden Coins Required"
    range_start = 0
    range_end = 6
    default = 6


class MarioCoinFragmentPercentage(Range):
    """
    Percentage of filler items to be replaced with Mario Coin Fragments. Note that the Coinsanity and Coinsanity
    Checks options will greatly impact the number of replaceable filler items.
    """
    display_name = "Mario Coin Fragment Percentage"
    range_start = 1
    range_end = 50
    default = 20


class MarioCoinFragmentsRequiredPercentage(Range):
    """
    Percentage of the Mario Coins in the item pool that are required to put the Mario Coin together.
    """
    display_name = "Mario Coin Fragments Required Percentage"
    range_start = 1
    range_end = 100
    default = 75


class ShuffleMidwayBells(Toggle):
    """
    Shuffle Midway Bells into the item pool. You can always start at the beginning of a level after obtaining the
    Midway Bell by holding SELECT while entering the level (until you load into the level).
    The Midway Bells in levels will trigger location checks whether this option is on or not, but they will only
    set the checkpoint if this is off, otherwise you must obtain the Midway Bell item from the item pool.
    """
    display_name = "Shuffle Midway Bells"


class MariosCastleMidwayBell(Toggle):
    """
    Adds a Midway Bell to the final stage, just before the Wario fight.
    """
    display_name = "Mario's Castle Midway Bell"


class Coinsanity(Toggle):
    """
    Shuffles the singular coins found freestanding and in question mark blocks into the item pool, and adds location
    checks made by obtaining a sufficient number of coins in particular levels within a single playthrough.
    """
    display_name = "Coinsanity"


class CoinsanityChecks(Range):
    """
    Number of Coinsanity checks.
    A higher number means more checks, and smaller coin amounts per coin item in the item pool.
    If Accessibility is set to Full, auto-scroll levels may have a lower maximum count, which may lead to this
    value being limited.
    """
    display_name = "Coinsanity Checks"
    range_start = 31
    range_end = 2597
    default = 150


class DifficultyMode(Choice):
    """
    Play in normal or easy mode. You can also start in Normal Mode with an "upgrade" to Easy Mode in the item pool,
    or start in Easy Mode with a Normal Mode "trap" in the item pool.
    """
    display_name = "Difficulty Mode"
    option_normal = 0
    option_easy = 1
    option_normal_to_easy = 2
    option_easy_to_normal = 3
    default = 0


class ShufflePipeTraversal(Choice):
    """
    Single: Shuffle a Pipe Traversal item into the item pool, which is required to enter any pipes.
    Split: Shuffle 4 Pipe Traversal items, one required for entering pipes from each direction.
    Note that being unable to enter pipes is very limiting and affects nearly half of all levels.
    """
    display_name = "Shuffle Pipe Traversal"
    option_off = 0
    option_single = 1
    option_split = 2
    default = 0


class RandomizeEnemies(Toggle):
    """
    Randomize enemies throughout levels.
    """
    display_name = "Randomize Enemies"


class RandomizePlatforms(Toggle):
    """
    Randomize platforms throughout levels.
    """
    display_name = "Randomize Platforms"


class AutoScrollChances(NamedRange):
    """
    Chance per eligible level to be made into an auto scroll level. Can also set to Vanilla to leave them unchanged.
    """
    display_name = "Auto Scroll Chance"
    range_start = 0
    range_end = 100
    special_range_names = {"vanilla": -1, "none": 0, "all": 100}
    default = -1


class AutoScrollMode(Choice):
    """
    Always: Any auto scroll levels will always auto-scroll.
    Global Trap Item: Auto scroll levels will only auto-scroll after obtaining the Auto Scroll trap item.
    Level Trap Items: As with Trap Item, but there is a separate trap item for each auto scroll level.
    Global Cancel Item: Auto Scroll levels will stop auto-scrolling after obtaining the Auto Scroll Cancel item.
    Level Cancel Items: As with Cancel Item, but there is a separate cancel item for each auto scroll level.
    Chaos: Each level will randomly always auto scroll, have an Auto Scroll Trap, or have an Auto Scroll Cancel item.
    The effects of Trap and Cancel items are permanent! If Accessibility is not set to Full,
    Traps may cause locations to become permanently unreachable.
    With individual level items, the number of auto scroll levels may be limited by the available space in the item
    pool.
    """
    display_name = "Auto Scroll Mode"
    option_always = 0
    option_global_trap_item = 1
    option_level_trap_items = 2
    option_global_cancel_item = 3
    option_level_cancel_items = 4
    option_chaos = 5
    default = 0


class RandomizeMusic(Toggle):
    """
    Randomize the music that plays in levels and overworld areas.
    """
    display_name = "Randomize Music"


class EnergyLink(Toggle):
    """
    All extra lives beyond 1 are transferred into the server's shared EnergyLink storage. If you drop to 0,
    1 will be replenished if there is sufficient energy stored.
    """
    display_name = "Energy Link"
    default = 1




@dataclass
class SML2Options(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    shuffle_golden_coins: ShuffleGoldenCoins
    required_golden_coins: GoldenCoinsRequired
    mario_coin_fragment_percentage: MarioCoinFragmentPercentage
    mario_coin_fragments_required_percentage: MarioCoinFragmentsRequiredPercentage
    coinsanity: Coinsanity
    coinsanity_checks: CoinsanityChecks
    shuffle_midway_bells: ShuffleMidwayBells
    marios_castle_midway_bell: MariosCastleMidwayBell
    shuffle_pipe_traversal: ShufflePipeTraversal
    auto_scroll_mode: AutoScrollMode
    auto_scroll_chances: AutoScrollChances
    difficulty_mode: DifficultyMode
    randomize_enemies: RandomizeEnemies
    randomize_platforms: RandomizePlatforms
    randomize_music: RandomizeMusic
    energy_link: EnergyLink
