from dataclasses import dataclass
from Options import Choice, DeathLink, PerGameCommonOptions, Toggle, DefaultOnToggle


class Calamity(Toggle):
    """Calamity mod bosses and events are shuffled"""

    display_name = "Calamity Mod Integration"


class Getfixedboi(Toggle):
    """Generation accomodates the secret, very difficult "getfixedboi" seed"""

    display_name = """"getfixedboi" Seed"""


class Goal(Choice):
    """
    The victory condition for your run. Stuff after the goal will not be shuffled.
    Primordial Wyrm and Boss Rush are accessible relatively early, so consider "Items" or
    "Locations" accessibility to avoid getting stuck on the goal.
    """

    display_name = "Goal"
    option_mechanical_bosses = 0
    option_calamitas_clone = 1
    option_plantera = 2
    option_golem = 3
    option_empress_of_light = 4
    option_lunatic_cultist = 5
    option_astrum_deus = 6
    option_moon_lord = 7
    option_providence_the_profaned_goddess = 8
    option_devourer_of_gods = 9
    option_yharon_dragon_of_rebirth = 10
    option_zenith = 11
    option_calamity_final_bosses = 12
    option_primordial_wyrm = 13
    option_boss_rush = 14
    default = 0


class EarlyAchievements(DefaultOnToggle):
    """Adds checks upon collecting early Pre-Hardmode achievements. Adds many sphere 1 checks."""

    display_name = "Early Pre-Hardmode Achievements"


class NormalAchievements(DefaultOnToggle):
    """
    Adds checks upon collecting achivements not covered by the other options. Achievements for
    clearing bosses and events are excluded.
    """

    display_name = "Normal Achievements"


class GrindyAchievements(Toggle):
    """Adds checks upon collecting grindy achievements"""

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


@dataclass
class TerrariaOptions(PerGameCommonOptions):
    calamity: Calamity
    getfixedboi: Getfixedboi
    goal: Goal
    early_achievements: EarlyAchievements
    normal_achievements: NormalAchievements
    grindy_achievements: GrindyAchievements
    fishing_achievements: FishingAchievements
    fill_extra_checks_with: FillExtraChecksWith
    death_link: DeathLink
