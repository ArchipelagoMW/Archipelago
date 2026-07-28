from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range, DefaultOnToggle


class Character(Choice):
    """
    The character you play as during the run.
    The game will force the character picked here to be your character in-game.
    That means you don't need to unlock Scorpion/Sub-Zero first in order to play as them.
    """
    display_name = "Character"

    option_liu_kang = 0
    option_kung_lao = 1
    option_sub_zero = 2
    option_scorpion = 3

    default = option_liu_kang


class RedKoinPercent(Range):
    """
    The randomizer fills the item pool with Red Koin items which are then randomized around the multiworld.
    The number of Red Koins in the pool depends on your character (some characters have more locations than others).
    To complete the goal you need to both beat the boss goal and have a set number of Red Koins.
    This option determines what % of all the available Red Koins in the pool is needed.
    0 means the goal will be beating the boss goal only.
    100 means requiring to find ALL Red Koins from locations AND beating the boss goal.
    80 (default) means you need to find at least 80% of all Red Koins AND beat the boss goal to win.
    There is a tracker in the pause menu that shows: current amount / need for goal / total in the multiworld.
    """
    display_name = "Red Koin goal percent"
    range_start = 0
    range_end = 100

    default = 80


class BossGoal(Choice):
    #TODO rework this, you need to beat all main bosses anyway to access final boss
    """
    What bosses are needed for goal completion.
    The goal also includes getting enough Red Koins, set in the red_koin_need_percent option.
    shao_kahn_only: only the final boss of the game is needed for the goal.
    main_bosses: all main bosses (Kitana, Reptile, Baraka, Goro and Scorpion) and the final boss.
    main_and_secret_bosses: all previously mentioned bosses and all secret bosses (Ermac, Mileena and Kano).
    """
    display_name = "Boss Goal"

    option_shao_kahn_only = 0
    option_main_bosses = 1
    option_main_and_secret_bosses = 2

    default = option_shao_kahn_only


class Fatalitysanity(DefaultOnToggle):
    """
    If on, adds checks for performing all of your character's different fatalities, multalities and brutality
    """
    display_name = "Fatalitysanity"


@dataclass
class MKSMOptions(PerGameCommonOptions):
    character: Character
    red_koin_need_percent: RedKoinPercent
    boss_goal: BossGoal
    fatalitysanity: Fatalitysanity
