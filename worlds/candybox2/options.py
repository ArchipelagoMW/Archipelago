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


class CandyMerchantHatPrice(Range):
    """The price (in candies) required to buy the Candy Merchant's Hat."""
    display_name = "Candy Merchant's Hat Price"
    range_start = 10000
    range_end = 1000000000
    default = 1000000

class SorceressHatPrice(Range):
    """The price (in lollipops) required to buy the Sorceress' Hat."""
    display_name = "Sorceress' Hat Price"
    range_start = 10000
    range_end = 1000000000
    default = 1000000000

class TeapotHP(Range):
    """The teapot boss's total HP."""
    display_name = "Teapot Boss HP"
    range_start = 10000
    range_end = 10000000
    default = 100000

@dataclass
class CandyBox2Options(PerGameCommonOptions):
    progression_balancing = True

    quest_randomisation: QuestRandomisation
    death_link: DeathLink
    candy_production_multiplier: CandyProductionMultiplier
    lollipop_production_multiplier: LollipopProductionMultiplier
    candy_merchant_hat_price: CandyMerchantHatPrice
    sorceress_hat_price: SorceressHatPrice
    teapot_hp: TeapotHP