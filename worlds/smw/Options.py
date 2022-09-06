import typing

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionList


class Goal(Choice):
    """
    Determines the goal of the seed
    Bowser: Defeat Koopalings, reach Bowser's Castle and defeat Bowser
    Yoshi Egg Hunt: Find a certain number of Yoshi Eggs
    """
    display_name = "Goal"
    option_bowser = 0
    option_yoshi_egg_hunt = 1
    default = 0


class BossesRequired(Range):
    """
    How many Bosses (Koopalings or Reznor) must be defeated in order to defeat Bowser
    """
    display_name = "Bosses Required"
    range_start = 0
    range_end = 11
    default = 7


class NumberOfYoshiEggs(Range):
    """
    How many Yoshi Eggs are in the pool for Yoshi Egg Hunt
    """
    display_name = "Total Number of Yoshi Eggs"
    range_start = 1
    range_end = 80
    default = 50


class PercentageOfYoshiEggs(Range):
    """
    What Percentage of Yoshi Eggs are required to finish Yoshi Egg Hunt
    """
    display_name = "Required Percentage of Yoshi Eggs"
    range_start = 1
    range_end = 100
    default = 100


class DragonCoinChecks(Toggle):
    """
    Whether collecting 5 Dragon Coins in each level will grant a check
    """
    display_name = "Dragon Coin Checks"


class LevelShuffle(Toggle):
    """
    Whether levels are shuffled
    """
    display_name = "Level Shuffle"


class DisplaySentItemPopups(Choice):
    """
    What messages to display in-game for items sent
    """
    option_none = 0
    option_all = 1
    default = 1


class DisplayReceivedItemPopups(Choice):
    """
    What messages to display in-game for items received
    """
    option_none = 0
    option_all = 1
    option_progression = 2
    default = 2


class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2


class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the level to become slippery
    """
    display_name = "Ice Trap Weight"


class StunTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which briefly stuns Mario
    """
    display_name = "Stun Trap Weight"


class LiteratureTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the player to read literature
    """
    display_name = "Literature Trap Weight"


class Autosave(DefaultOnToggle):
    """
    Whether a save prompt will appear after every level
    """
    display_name = "Autosave"


class MusicShuffle(Toggle):
    """
    Whether music is shuffled
    """
    display_name = "Music Shuffle"


class PaletteShuffle(Toggle):
    """
    Whether to shuffle level palettes
    """
    display_name = "Palette Shuffle"


class StartingLifeCount(Range):
    """
    How many extra lives to start the game with
    """
    display_name = "Starting Life Count"
    range_start = 1
    range_end = 99
    default = 5



smw_options: typing.Dict[str, type(Option)] = {
    "death_link": DeathLink,
    "goal": Goal,
    "bosses_required": BossesRequired,
    "number_of_yoshi_eggs": NumberOfYoshiEggs,
    "percentage_of_yoshi_eggs": PercentageOfYoshiEggs,
    "dragon_coin_checks": DragonCoinChecks,
    "level_shuffle": LevelShuffle,
    "display_sent_item_popups": DisplaySentItemPopups,
    "display_received_item_popups": DisplayReceivedItemPopups,
    "trap_fill_percentage": TrapFillPercentage,
    "ice_trap_weight": IceTrapWeight,
    "stun_trap_weight": StunTrapWeight,
    "literature_trap_weight": LiteratureTrapWeight,
    "autosave": Autosave,
    "music_shuffle": MusicShuffle,
    "palette_shuffle": PaletteShuffle,
    "starting_life_count": StartingLifeCount,
}
