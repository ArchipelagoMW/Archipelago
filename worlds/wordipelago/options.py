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
    Whether you start with keyboard letters fading out when discovered not to be in the current word
    """
    display_name = "Unused Letters Unlocked"   

class ExtraItemsAsTimeRewards(Toggle):
    """Whether to fill any extra items needed with time. otherwise non-useful filler item"""
    display_name = "Extra Time Rewards"

class GreenChecks(Choice):
    """
    ==Not Yet Implimented==
    How checks work for green letters in words
    none: No checks for getting green letters
    best: Checks for 1-5 correct letters in a word
    composition: checks for every configuration of green letters
    complete: Best and composition combined
    """
    display_name = "Green Checks"
    option_none = 0
    option_best = 1
    option_composition = 2
    option_complete = 3
    default = 1

class YellowChecks(Choice):
    """
    ==Not Yet Implimented==
    How checks work for yellow letters in words
    none: No checks for getting yellow letters
    composition: checks for every configuration of yellow letters
    """
    display_name = "Yellow Checks"
    option_none = 0
    option_composition = 1
    default = 0

class LetterChecks(Choice):
    """
    ==Not Yet Implimented==
    Which letters do you want to unlock items for sucessfully using in a word
    none: No checks for using letters
    vowels: Checks for using vowels
    common: Checks for using vowels and common consonants
    all: Checks for using all letters
    """
    display_name = "Letter Checks"
    option_none = 0
    option_vowels = 1
    option_common = 2
    option_all = 3
    default = 2

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
    default = 0

class LetterBalancing(Range):
    """
    ==Not Yet Implimented==
    New letter usefulness, 0 = completely random, 5 = weighted to useful letters early
    """
    display_name = "Letter Balancing"
    range_start = 0
    default = 2
    range_end = 5

class ExtraTimeRewardPercent(Range):
    """Description"""
    display_name = "Extra Time Reward Percent"
    range_start = 0
    range_end = 100
    default = 20
    
class ClueItemRewardPercent(Range):
    """Description"""
    display_name = "Clue Item Reward Percent"
    range_start = 0
    range_end = 100
    default = 30
    
class ClueItemPointSize(Range):
    """Description"""
    display_name = "Clue Item Point Size"
    range_start = 0
    range_end = 100
    default = 5
    
class BadGuessTrapPercent(Range):
    """Description"""
    display_name = "Bad Guess Trap Reward Percent"
    range_start = 0
    range_end = 100
    default = 5
    
class ExtraCooldownTrapPercent(Range):
    """Description"""
    display_name = "Extra Cooldown Trap Percent"
    range_start = 0
    range_end = 100
    default = 5
    
class ExtraCooldownTrapSize(Range):
    """Description"""
    display_name = "Extra Cooldown Trap Size"
    range_start = 0
    range_end = 300
    default = 60

@dataclass
class WordipelagoOptions(PerGameCommonOptions):
    words_to_win: WordsToWin
    green_checks: GreenChecks
    yellow_checks: YellowChecks
    letter_checks: LetterChecks
    starting_letters: StartingLetters
    starting_guesses: StartingGuesses
    starting_cooldown: StartingCooldown
    time_reward_count: TimeRewardCount
    time_reward_seconds: TimeRewardSeconds
    yellow_unlocked: YellowUnlocked
    unused_letters_unlocked: UnusedLettersUnlocked
    shuffle_typing: ShuffleTyping
    extra_items_as_time_rewards: ExtraItemsAsTimeRewards

    extra_time_reward_percent: ExtraTimeRewardPercent
    clue_item_reward_percent: ClueItemRewardPercent
    clue_item_point_size: ClueItemPointSize
    bad_guess_trap_percent: BadGuessTrapPercent
    extra_cooldown_trap_percent: ExtraCooldownTrapPercent
    extra_cooldown_trap_size: ExtraCooldownTrapSize

    start_inventory_from_pool: StartInventoryPool
