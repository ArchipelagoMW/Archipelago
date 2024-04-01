from Options import Toggle, Choice, NamedRange, Range, PerGameCommonOptions
from dataclasses import dataclass


class ShuffleGoldenCoins(Choice):
    """Vanilla: Golden Coins are not in the item pool, you receive them when defeating bosses as in vanilla.
    Shuffle: Shuffle the Golden Coins into the item pool and open location checks on bosses.
    Mario Coin Fragment Hunt: You start with all Golden Coins except the Mario Coin, which has been fragmented into
    many pieces.
    You will see a Golden Coin being received when defeating bosses regardless of whether you are actually getting a coin."""
    display_name = "Shuffle Golden Coins"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_mario_coin_fragment_hunt = 2


class GoldenCoinsRequired(Range):
    """Number of Golden Coins required to enter Mario's Castle. Ignored on Mario Coin Fragment Hunt."""
    display_name = "Golden Coins Required"
    range_start = 0
    range_end = 6
    default = 6


class MarioCoinFragmentPercentage(Range):
    """Percentage of filler items to be replaced with Mario Coin Fragments. Note that the Coinsanity and Coinsanity
    Checks settings will greatly impact the number of replaceable filler items. There may be as few as 6 available
    slots for Mario Coin Fragments if Coinsanity is off."""
    display_name = "Mario Coin Fragment Percentage"
    range_start = 1
    range_end = 100
    default = 20


class MarioCoinFragmentsRequiredPercentage(Range):
    """Percentage of the Mario Coins in the item pool that are required to put the Mario Coin together."""
    display_name = "Mario Coin Fragments Required Percentage"
    range_start = 1
    range_end = 100
    default = 75


class ShuffleMidwayBells(Toggle):
    """Shuffle the Midway Bells into the item pool. Ringing a bell will trigger a location check.
    Obtaining a Midway Bell will be permanent, and some levels will require backtracking from the midway point to reach
    secret exits."""
    display_name = "Shuffle Midway Bells"


class Coinsanity(Toggle):
    """Shuffles the singular coins found freestanding and in question mark blocks into the item pool, and adds location
    checks made by obtaining a sufficient number of coins in particular levels within a single playthrough."""
    default_name = "Coinsanity"


class CoinsanityChecks(Range):
    """Number of Coinsanity checks.
     A higher number means more checks, and smaller coin amounts per coin item in the item pool.
     If Accessibility is set to Locations, auto-scroll levels may have a lower maximum count, which may lead to this
     value being limited."""
    default_name = "Coinsanity Checks"
    range_start = 31
    range_end = 2599
    default = 150


class DifficultyMode(Choice):
    """Play in normal or easy mode. You can also start in Normal Mode with an "upgrade" to Easy Mode in the item pool,
    or start in Easy Mode with a Normal Mode "trap" in the item pool."""
    display_name = "Difficulty Mode"
    option_normal = 0
    option_easy = 1
    option_normal_to_easy = 2
    option_easy_to_normal = 3
    default = 0


class ShufflePipeTraversal(Choice):
    """Single: Shuffle a Pipe Traversal item into the item pool, which is required to enter any pipes.
    Split: Shuffle 4 Pipe Traversal items, one required for entering pipes from each direction.
    Note that being unable to enter pipes is very limiting and affects nearly half of all levels."""
    display_name = "Shuffle Pipe Traversal"
    option_off = 0
    option_single = 1
    option_split = 2
    default = 0


class RandomizeEnemies(Toggle):
    """Randomize enemies throughout levels."""
    display_name = "Randomize Enemies"


class RandomizePlatforms(Toggle):
    """Randomize platforms throughout levels."""
    display_name = "Randomize Platforms"


class AutoScrollLevels(NamedRange):
    """Keep auto scroll levels vanilla or choose a number of levels to be randomly selected to have auto-scrolling.
    Certain levels are excluded."""
    display_name = "Auto Scroll Levels"
    range_start = 0
    range_end = 17
    special_range_names = {"vanilla": -1, "none": 0, "all": 17}
    default = -1


class AutoScrollTrap(Toggle):
    """If on, auto scroll levels will not auto scroll until you've received the Auto Scroll trap item."""
    display_name = "Auto Scroll Trap"


class RandomizeMusic(Toggle):
    """Randomize the music that plays in levels and overworld areas."""
    display_name = "Randomize Music"


class EnergyLink(Toggle):
    """All extra lives beyond 1 are transferred into the server's shared EnergyLink storage. If you drop to 0,
    1 will be replenished if there is sufficient energy stored."""
    display_name = "Energy Link"
    default = 1


@dataclass
class SML2Options(PerGameCommonOptions):
    shuffle_golden_coins: ShuffleGoldenCoins
    required_golden_coins: GoldenCoinsRequired
    mario_coin_fragment_percentage: MarioCoinFragmentPercentage
    mario_coin_fragments_required_percentage: MarioCoinFragmentsRequiredPercentage
    coinsanity: Coinsanity
    coinsanity_checks: CoinsanityChecks
    shuffle_midway_bells: ShuffleMidwayBells
    shuffle_pipe_traversal: ShufflePipeTraversal
    difficulty_mode: DifficultyMode
    randomize_enemies: RandomizeEnemies
    randomize_platforms: RandomizePlatforms
    auto_scroll_levels: AutoScrollLevels
    auto_scroll_trap: AutoScrollTrap
    randomize_music: RandomizeMusic
    energy_link: EnergyLink
