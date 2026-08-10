from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions, Toggle, DefaultOnToggle, Range, OptionGroup


class Calamity(Toggle):
    """Calamity mod bosses and events are shuffled"""

    display_name = "Calamity Mod Integration"


class Getfixedboi(Toggle):
    """
    Generation accomodates the secret, very difficult "getfixedboi" seed

    FOR THE BETA: NPC Rando is incompatible with GFB.
    If both options are selected on generation, NPC rando will be disabled.
    """

    display_name = """"getfixedboi" Seed"""


class Goal(Choice):
    """
    The victory condition for your run. Stuff after the goal will not be shuffled (if Shuffle Up To is default).
    Primordial Wyrm and Boss Rush are accessible relatively early, so consider "Items" or
    "Locations" accessibility to avoid getting stuck on the goal.

    FOR THE BETA: Note that the Wall of Flesh goal is intended to be played with NPC Rando on.
    Otherwise, the generated game will be immediately goal-able.
    """

    display_name = "Goal"
    option_wall_of_flesh = 0
    option_mechanical_bosses = 1
    option_calamitas_clone = 2
    option_plantera = 3
    option_princess = 4
    option_golem = 5
    option_empress_of_light = 6
    option_lunatic_cultist = 7
    option_astrum_deus = 8
    option_moon_lord = 9
    option_providence_the_profaned_goddess = 10
    option_devourer_of_gods = 11
    option_yharon_dragon_of_rebirth = 12
    option_zenith = 13
    option_calamity_final_bosses = 14
    option_primordial_wyrm = 15
    option_boss_rush = 16
    default = 0


class ShuffleUpTo(Choice):
    """
    Allows you to randomize checks past the set goal.
    Note that certain configurations may result in some checks only being accessible post-goal.
    """
    display_name = "Shuffle Up To"
    default = 0
    option_disable = 0
    option_mechanical_bosses = 1
    option_plantera = 3
    option_golem = 5
    option_lunatic_cultist = 7
    option_moon_lord = 9
    option_providence_the_profaned_goddess = 10
    option_devourer_of_gods = 11
    option_yharon_dragon_of_rebirth = 12
    option_calamity_final_bosses = 14
    option_all = -1

class RandomizeNPCs(Toggle):
    """
    Randomizes all vanilla NPCs, putting them into the item pool. Fulfilling a certain NPC's recruit criteria rewards a check.
    """
    display_name = "Randomize NPCs"
    default = True


class EarlyAchievements(DefaultOnToggle):
    """Adds checks upon collecting early Pre-Hardmode achievements. Adds many sphere 1 checks."""

    display_name = "Early Pre-Hardmode Achievements"


class NormalAchievements(DefaultOnToggle):
    """
    Adds checks upon collecting achivements not covered by the other options. Achievements for
    clearing bosses and events are excluded.
    """

    display_name = "Normal Achievements"


class RareAchievements(Toggle):
    """Adds checks upon collecting grindy achievements involving rare enemies/drops"""

    display_name = "Rare Achievements"


class TimeAchievements(Toggle):
    """
    Adds checks upon collecting grindy achievements based on random time-based events, such as windy weather
    """

    display_name = "Time-based Achievements"


class CraftingAchievements(Toggle):
    """Adds checks upon collecting grindy achievements dedicated to crafting complex items"""

    display_name = "Crafting Achievements"


class GrindyAchievements(Toggle):
    """Adds checks upon collecting grindy achievements that otherwise require a lot of repetitive work"""

    display_name = "Grindy Achievements"


class FishingAchievements(Toggle):
    """Adds checks upon collecting fishing quest achievements"""

    display_name = "Fishing Quest Achievements"


class FillExtraChecksWith(Choice):
    """
    Applies if you have achievements enabled. "Useful Items" helps to make the early game less grindy.
    Items are rewarded to all players in your Terraria world.
    """

    display_name = "Fill Extra Checks With"
    option_coins = 0
    option_useful_items = 1
    default = 1

class ShimmerSkips(Toggle):
    """
    Enables sequence breaks in logic requiring the use of Shimmer to transmute/uncraft items.
    """

    display_name = "Shimmer Skips"

class HealthLogic(DefaultOnToggle):
    """
    Guarantees you will not have to fight a boss/event without access to prior health upgrades.
    For each boss, the amount of health required is based on how much health the player is expected to have before fighting them.
    Mainly alters Calamity logic, and is based off the health recommendations made by the official wiki.
    """
    display_name = "Health Logic"

class HealthLogicHandicap(Range):
    """
    If health logic is on, this option allows you to reduce how many types of health consumables are needed before a boss.
    For example, if set to 0, Moon Lord will require Life Crystals/Fruits, Sanguine Tangerine, and Miracle Fruit.
    If set to -1, you only need Sanguine Tangerine or Miracle Fruit. If set to -2, neither are required.
    """
    display_name = "Health Handicap"
    range_start = -6
    range_end = 0
    default = 0

ter_option_groups = [
    OptionGroup("Gamemode and Content", [
        Calamity,
        Getfixedboi,
        Goal,
        ShuffleUpTo,
    ]),
    OptionGroup("Checks", [
        RandomizeNPCs,
        EarlyAchievements,
        NormalAchievements,
        RareAchievements,
        TimeAchievements,
        CraftingAchievements,
        GrindyAchievements,
        FishingAchievements,
    ]),
    OptionGroup("Items", [
        FillExtraChecksWith,
    ]),
    OptionGroup("Logic", [
        ShimmerSkips,
        HealthLogic,
        HealthLogicHandicap,
    ]),
]

@dataclass
class TerrariaOptions(PerGameCommonOptions):
    calamity: Calamity
    getfixedboi: Getfixedboi
    goal: Goal
    shuffle_to: ShuffleUpTo
    randomize_npcs: RandomizeNPCs
    early_achievements: EarlyAchievements
    normal_achievements: NormalAchievements
    rare_achievements: RareAchievements
    time_achievements: TimeAchievements
    crafting_achievements: CraftingAchievements
    grindy_achievements: GrindyAchievements
    fishing_achievements: FishingAchievements
    fill_extra_checks_with: FillExtraChecksWith
    shimmer_skips: ShimmerSkips
    health_logic: HealthLogic
    health_logic_handicap: HealthLogicHandicap
    death_link: DeathLink
