from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions

class Goal(Choice):
    """
    Determines the goal of the seed

    Boss Cass Bust-Up: Boss Cass must be beaten-up
    """
    display_name = "Goal Chapter"
    option_Chapter_1 = 1
    option_Chapter_2 = 2
    option_Chapter_3 = 3
    option_Chapter_4 = 4
    option_Chapter_5 = 5
    option_Chapter_6 = 6
    option_Chapter_7 = 7
    option_Chapter_8 = 8
    option_Chapter_9 = 9
    option_Chapter_10 = 10
    default = 3

class IngredientItems(Choice):
    option_vanilla = 0
    option_seed_items = 1
    option_infinite_items = 2
    default = 1

class MerchantSummons(Choice):
    option_Alchemy_created = 0
    option_infinite = 1
    default = 0


@dataclass
class potion_craft_option_groups(PerGameCommonOptions):
    OptionGroup("Goal Options", [
        Goal,

    ]),
    OptionGroup("Death Link", [
        DeathLink
    ])

@dataclass
class PotionCraftOptions(PerGameCommonOptions):
    goal: Goal


    death_link: DeathLink