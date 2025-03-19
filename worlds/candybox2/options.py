from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice


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


@dataclass
class CandyBox2Options(PerGameCommonOptions):
    progression_balancing = True

    quest_randomisation: QuestRandomisation