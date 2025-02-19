from dataclasses import dataclass
from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool

class WordsToWin(Range):
    """How many words you have to get right to hit you goal"""
    display_name = "Words To Win"
    range_start = 1
    default = 10
    range_end = 50
    
class StartingLetters(Range):
    """How many letters you start with"""
    display_name = "Starting Letters"
    range_start = 1
    default = 1
    range_end = 26

class StartingGuesses(Range):
    """How many letters you start with"""
    display_name = "Starting Guesses"
    range_start = 1
    default = 1
    range_end = 6

class StartingCooldown(Range):
    """How many letters you start with"""
    display_name = "Starting Cooldown"
    range_start = 0
    default = 120
    range_end = 600

class TimeRewardCount(Range):
    """The number of cooldown reduction rewards in the pool"""
    display_name = "Time Reward Count"
    range_start = 0
    default = 12
    range_end = 30

class TimeRewardSeconds(Range):
    """How many seconds each time reward decreases cooldown by"""
    display_name = "Time Reward Seconds"
    range_start = 0
    default = 10
    range_end = 30

class YellowUnlocked(Toggle):
    """Whether you start with yellow tiles shown or not"""
    display_name = "Yellow Unlocked"

class UnusedLettersUnlocked(Toggle):
    """
    ==Not Yet Implimented==
    Whether you start with keyboard letters fading out when discovered not to be in the current word
    """
    display_name = "Unused Letters Unlocked"   

class ExtraItemsAsTimeRewards(Toggle):
    """Whether to fill any extra items needed with time. otherwise non-useful filler item"""
    display_name = "Extra Time Rewards"

class ShuffleTyping(Choice):
    """
    ==Not Yet Implimented==
    Whether typing on your physical keyboard mimics the layout of the game keyboard
    none: Typing is not shuffled
    querty: Typing is shuffled as if using a querty keyboard
    azerty: Typing is shuffled as if using a azerty keyboard
    dvorak: Typing is shuffled as if using a dvorak keyboard
    """
    display_name = "Unused Letters Unlocked"
    option_none = 0
    option_querty = 1
    option_azerty = 2
    option_dvorak = 3

class LetterBalancing(Range):
    """New letter usefulness, 0 = completely random, 5 = weighted to useful letters early"""
    display_name = "Letter Balancing"
    range_start = 0
    default = 2
    range_end = 5

@dataclass
class WordipelagoOptions(PerGameCommonOptions):
    words_to_win: WordsToWin
    starting_letters: StartingLetters
    starting_guesses: StartingGuesses
    starting_cooldown: StartingCooldown
    time_reward_count: TimeRewardCount
    time_reward_seconds: TimeRewardSeconds
    yellow_unlocked: YellowUnlocked
    unused_letters_unlocked: UnusedLettersUnlocked
    shuffle_typing: ShuffleTyping
    extra_items_as_time_rewards: ExtraItemsAsTimeRewards
    start_inventory_from_pool: StartInventoryPool

    # DeathLink is always on. Always.
    # death_link: DeathLink
