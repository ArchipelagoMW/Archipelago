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


class BowserCastleDoors(Choice):
    """
    How the doors of Bowser's Castle behave
    Vanilla: Front and Back Doors behave as vanilla
    Fast: Both doors behave as the Back Door
    Slow: Both doors behave as the Front Door
    "Front Door" rooms depend on the `bowser_castle_rooms` option
    "Back Door" only requires going through the dark hallway to Bowser
    """
    display_name = "Bowser Castle Doors"
    option_vanilla = 0
    option_fast = 1
    option_slow = 2
    default = 0


class BowserCastleRooms(Choice):
    """
    How the rooms of Bowser's Castle Front Door behave
    Vanilla: You can choose which rooms to enter, as in vanilla
    Random Two Room: Two random rooms are chosen
    Random Five Room: Five random rooms are chosen
    Gauntlet: All eight rooms must be cleared
    Labyrinth: Which room leads to Bowser?
    """
    display_name = "Bowser Castle Rooms"
    option_vanilla = 0
    option_random_two_room = 1
    option_random_five_room = 2
    option_gauntlet = 3
    option_labyrinth = 4
    default = 1


class BossShuffle(Choice):
    """
    How bosses are shuffled
    None: Bosses are not shuffled
    Simple: Four Reznors and the seven Koopalings are shuffled around
    Full: Each boss location gets a fully random boss
    Singularity: One or two bosses are chosen and placed at every boss location
    """
    display_name = "Boss Shuffle"
    option_none = 0
    option_simple = 1
    option_full = 2
    option_singularity = 3
    default = 0


class LevelShuffle(Toggle):
    """
    Whether levels are shuffled
    """
    display_name = "Level Shuffle"


class ExcludeSpecialZone(Toggle):
    """
    If active, this option will prevent any progression items from being placed in Special Zone levels.
    Additionally, if Level Shuffle is active, Special Zone levels will not be shuffled away from their vanilla tiles.
    """
    display_name = "Exclude Special Zone"


class SwapDonutGhostHouseExits(Toggle):
    """
    If enabled, this option will swap which overworld direction the two exits of the level at the Donut Ghost House
        overworld tile go:
    False: Normal Exit goes up, Secret Exit goes right.
    True: Normal Exit goes right, Secret Exit goes up.
    """
    display_name = "Swap Donut GH Exits"


class DisplaySentItemPopups(Choice):
    """
    What messages to display in-game for items sent
    """
    display_name = "Display Sent Item Popups"
    option_none = 0
    option_all = 1
    default = 1


class DisplayReceivedItemPopups(Choice):
    """
    What messages to display in-game for items received
    """
    display_name = "Display Received Item Popups"
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


class TimerTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the timer to run low
    """
    display_name = "Timer Trap Weight"


class Autosave(DefaultOnToggle):
    """
    Whether a save prompt will appear after every level
    """
    display_name = "Autosave"


class EarlyClimb(Toggle):
    """
    Force Climb to appear early in the seed as a local item.
    This is particularly useful to prevent BK when Level Shuffle is disabled
    """
    display_name = "Early Climb"


class OverworldSpeed(Choice):
    """
    How fast Mario moves on the overworld
    """
    display_name = "Overworld Speed"
    option_slow = 0
    option_vanilla = 1
    option_fast = 2
    default = 1


class MusicShuffle(Choice):
    """
    Music shuffle type
    None: No Music is shuffled
    Consistent: Each music track is consistently shuffled throughout the game
    Full: Each individual level has a random music track
    Singularity: The entire game uses one song for overworld and one song for levels
    """
    display_name = "Music Shuffle"
    option_none = 0
    option_consistent = 1
    option_full = 2
    option_singularity = 3
    default = 0


class MarioPalette(Choice):
    """
    Mario palette color
    """
    display_name = "Mario Palette"
    option_mario = 0
    option_luigi = 1
    option_wario = 2
    option_waluigi = 3
    option_geno = 4
    option_princess = 5
    option_dark = 6
    option_sponge = 7
    default = 0


class ForegroundPaletteShuffle(Toggle):
    """
    Whether to shuffle level foreground palettes
    """
    display_name = "Foreground Palette Shuffle"


class BackgroundPaletteShuffle(Toggle):
    """
    Whether to shuffle level background palettes
    """
    display_name = "Background Palette Shuffle"


class OverworldPaletteShuffle(Toggle):
    """
    Whether to shuffle overworld palettes
    """
    display_name = "Overworld Palette Shuffle"


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
    "bowser_castle_doors": BowserCastleDoors,
    "bowser_castle_rooms": BowserCastleRooms,
    "level_shuffle": LevelShuffle,
    "exclude_special_zone": ExcludeSpecialZone,
    "boss_shuffle": BossShuffle,
    "swap_donut_gh_exits": SwapDonutGhostHouseExits,
    #"display_sent_item_popups": DisplaySentItemPopups,
    "display_received_item_popups": DisplayReceivedItemPopups,
    "trap_fill_percentage": TrapFillPercentage,
    "ice_trap_weight": IceTrapWeight,
    "stun_trap_weight": StunTrapWeight,
    "literature_trap_weight": LiteratureTrapWeight,
    "timer_trap_weight": TimerTrapWeight,
    "autosave": Autosave,
    "early_climb": EarlyClimb,
    "overworld_speed": OverworldSpeed,
    "music_shuffle": MusicShuffle,
    "mario_palette": MarioPalette,
    "foreground_palette_shuffle": ForegroundPaletteShuffle,
    "background_palette_shuffle": BackgroundPaletteShuffle,
    "overworld_palette_shuffle": OverworldPaletteShuffle,
    "starting_life_count": StartingLifeCount,
}
