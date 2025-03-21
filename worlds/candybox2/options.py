from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, DeathLink, Range


class QuestRandomisation(Choice):
    """
    Determine logic for quest randomisation

    Off - Do not randomise quests

    Except X Potion Quest - Randomise every quest, except for the X Potion Quest

    Everything - Randomise every quest, including the X Potion Quest
    """
    display_name = "Quest Randomisation"

    option_off = 0
    option_except_x_potion_quest = 1
    option_everything = 2


class CandyProductionMultiplier(Range):
    """The number of candies generated per second will be multiplied by this number."""
    display_name = "Candy Production Multiplier"
    range_start = 1
    range_end = 100
    default = 1


class LollipopProductionMultiplier(Range):
    """The number of lollipops generated per second will be multiplied by this number."""
    display_name = "Lollipop Production Multiplier"
    range_start = 1
    range_end = 100
    default = 1


@dataclass
class CandyBox2Options(PerGameCommonOptions):
    progression_balancing = True

    quest_randomisation: QuestRandomisation
    death_link: DeathLink
    candy_production_multiplier: CandyProductionMultiplier
    lollipop_production_multiplier: LollipopProductionMultiplier