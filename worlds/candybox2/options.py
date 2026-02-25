from dataclasses import dataclass

from Options import Choice, DeathLink, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range, Toggle


class QuestRandomisation(Choice):
    """
    Determine logic for entrance randomisation

    Off - Do not randomise entrances

    Quests Only - Randomise every quest

    Quests and Rooms Separate - Randomise every quest and every room

    Everything - Randomise every quest and room together
    """

    display_name = "Entrance Randomisation"

    option_off = 0
    option_quests_only = 2
    option_quests_and_rooms_separate = 3
    option_everything = 4


class CandyProductionMultiplier(Range):
    """The number of candies generated per second will be multiplied by this number."""

    display_name = "Candy Production Multiplier"
    range_start = 1
    range_end = 100
    default = 1


class CandyDropMultiplier(Range):
    """The number of candies dropped in quests will be multiplied by this number."""

    display_name = "Candy Drop Multiplier"
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
    """The price (in thousands of candies) required to buy the Candy Merchant's Hat."""

    display_name = "Candy Merchant's Hat Price (x1000)"
    range_start = 10
    range_end = 1_000_000
    default = 750


class SorceressHatPrice(Range):
    """The price (in thousands of lollipops) required to buy the Sorceress' Hat."""

    display_name = "Sorceress' Hat Price (x1000)"
    range_start = 10
    range_end = 1_000_000
    default = 2_500


class TeapotHP(Range):
    """The teapot boss's total HP."""

    display_name = "Teapot Boss HP"
    range_start = 1000
    range_end = 10_000_000
    default = 100_000


class StartingWeapon(Choice):
    """
    Select the weapon that you will start the game with.

    Progressive Weapons will give you the next weapon in the sequence each time you get it.
    """

    display_name = "Starting Weapon"
    default = 61

    option_nothing = 61
    option_progressive_weapons = -1
    option_wooden_sword = 23
    option_iron_axe = 24
    option_polished_silver_sword = 25
    option_trolls_bludgeon = 9
    option_monkey_wizard_staff = 16
    option_enchanted_monkey_wizard_staff = 31
    option_tribal_spear = 36
    option_summoning_tribal_spear = 30
    option_giant_spoon = 37
    option_scythe = 27
    option_giant_spoon_of_doom = 35


class Grimoire(Choice):
    """
    Select how spells will be itemised

    Individual Grimoires - The item pool will be filled with Beginner's Grimoire, Advanced Grimoire and Black Magic Grimoire

    Progressive Grimoires - The item pool will have three Progressive Grimoires

    Individual Spells - The item pool will contain each spell individually. Buying the Beginner's Grimoire will send three checks. Obtaining the other grimoires will send two checks.
    """

    display_name = "Spells"

    option_individual_grimoires = 0
    option_progressive_grimoires = 1
    option_individual_spells = 2


class PainAuChocolatCount(Range):
    """The number of available Pains au Chocolat."""

    display_name = "Pains au Chocolat Count"
    range_start = 5
    range_end = 10
    default = 8


class RandomiseHpBar(DefaultOnToggle):
    """Whether the HP Bar must be an item found elsewhere"""

    display_name = "Randomise HP Bar"


class BrewingXPotion(Choice):
    """
    Determine whether you can brew more than one X potion at a time

    One at a time - You can only brew one X potion at a time

    Simultaneously - You can brew multiple X potions at a time, provided you have enough resources to brew them all at once.
    """

    display_name = "Brew X Potions"

    option_one_at_a_time = 0
    option_simultaneously = 1


class EnableComputer(Toggle):
    """Whether to enable The Computer. Once you have cleared the game, The Computer can be used to cheat items."""

    display_name = "Enable The Computer"


class EnergyLink(Toggle):
    """Allow sending energy to other worlds. Candy and lollipops can be converted to energy. 25% of the energy is lost in the transfer."""

    display_name = "Energy Link"


class Gifting(DefaultOnToggle):
    """Do you want to enable gifting items to and from other Archipelago slots?
    Items can only be sent to games that also support gifting"""

    display_name = "Gifting"


class ProgressiveJump(DefaultOnToggle):
    """Obtain the Pogo Stick, the Desert Bird Feather and the Rocket Boots in that order"""

    display_name = "Progressive Jump"


class CreateHints(DefaultOnToggle):
    """Do you want to create hints when you first enter a shop?"""

    display_name = "Create Hints"


class FontTrap(Range):
    """The number of font traps made available in the item pool"""

    display_name = "Font Traps"
    range_start = 0
    range_end = 5
    default = 0


class RandomiseTowerEntrance(DefaultOnToggle):
    """
    Determine whether the tower is affected by your entrance randomisation setting. Does not have any effect if entrance randomisation does not randomise rooms
    """

    display_name = "Randomise Tower Entrance"


class RandomiseXPotion(DefaultOnToggle):
    """
    Determine whether the X Potion is affected by your entrance randomisation setting. Does not have any effect if entrance randomisation does not randomise quests
    """

    display_name = "Randomise X Potion"


candy_box_2_options_groups = [
    OptionGroup("Entrances", [QuestRandomisation, RandomiseTowerEntrance, RandomiseXPotion]),
    OptionGroup(
        "Inventory Customisation", [StartingWeapon, ProgressiveJump, Grimoire, PainAuChocolatCount, RandomiseHpBar]
    ),
    OptionGroup(
        "Scaling",
        [
            CandyProductionMultiplier,
            CandyDropMultiplier,
            LollipopProductionMultiplier,
            CandyMerchantHatPrice,
            SorceressHatPrice,
            TeapotHP,
        ],
    ),
    OptionGroup("Inter-game Features", [DeathLink, EnergyLink, Gifting]),
]


@dataclass
class CandyBox2Options(PerGameCommonOptions):
    quest_randomisation: QuestRandomisation
    randomise_tower: RandomiseTowerEntrance
    randomise_x_potion: RandomiseXPotion
    death_link: DeathLink
    starting_weapon: StartingWeapon
    progressive_jump: ProgressiveJump
    candy_production_multiplier: CandyProductionMultiplier
    candy_drop_multiplier: CandyDropMultiplier
    lollipop_production_multiplier: LollipopProductionMultiplier
    candy_merchant_hat_price: CandyMerchantHatPrice
    sorceress_hat_price: SorceressHatPrice
    teapot_hp: TeapotHP
    randomise_hp_bar: RandomiseHpBar
    x_potion_brewing: BrewingXPotion
    enable_computer: EnableComputer
    grimoires: Grimoire
    pain_au_chocolat_count: PainAuChocolatCount
    energy_link: EnergyLink
    gifting: Gifting
    scouting: CreateHints
    font_traps: FontTrap
