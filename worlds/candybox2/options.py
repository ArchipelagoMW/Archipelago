from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, DeathLink, Range, Toggle


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
    range_start = 10_000
    range_end = 1_000_000_000
    default = 750_000

class SorceressHatPrice(Range):
    """The price (in lollipops) required to buy the Sorceress' Hat."""
    display_name = "Sorceress' Hat Price"
    range_start = 10_000
    range_end = 1_000_000_000
    default = 2_500_000

class TeapotHP(Range):
    """The teapot boss's total HP."""
    display_name = "Teapot Boss HP"
    range_start = 1000
    range_end = 10_000_000
    default = 100_000

class StartingWeapon(Choice):
    """
    Select the weapon that you will start the game with
    """
    display_name = "Starting Weapon"
    default = 61

    option_nothing = 61
    option_wooden_sword = 23
    option_iron_axe = 24
    option_tribal_spear = 36
    option_monkey_wizard_staff = 16
    option_polished_silver_sword = 25
    option_trolls_bludgeon = 9
    option_summoning_tribal_spear = 30
    option_enchanted_monkey_wizard_staff = 31
    option_giant_spoon = 37
    option_giant_spoon_of_doom = 35
    option_scythe = 27

class RandomiseHpBar(Toggle):
    """Whether the HP Bar must be an item found elsewhere"""
    display_name = "Randomise HP Bar"
    default = True

class EnergyLink(Toggle):
    """Allow sending energy to other worlds. Candy and lollipops can be converted to energy. 25% of the energy is lost in the transfer."""
    display_name = "Energy Link"

class Gifting(Toggle):
    """Do you want to enable gifting items to and from other Archipelago slots?
    Items can only be sent to games that also support gifting"""
    display_name = "Gifting"
    default = 1

@dataclass
class CandyBox2Options(PerGameCommonOptions):
    progression_balancing = True

    quest_randomisation: QuestRandomisation
    death_link: DeathLink
    starting_weapon: StartingWeapon
    candy_production_multiplier: CandyProductionMultiplier
    lollipop_production_multiplier: LollipopProductionMultiplier
    candy_merchant_hat_price: CandyMerchantHatPrice
    sorceress_hat_price: SorceressHatPrice
    teapot_hp: TeapotHP
    randomise_hp_bar: RandomiseHpBar
    energy_link: EnergyLink
    gifting: Gifting
