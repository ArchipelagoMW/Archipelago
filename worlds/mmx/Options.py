from dataclasses import dataclass
import typing

from Options import Choice, Range, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions, StartInventoryPool

class EnergyLink(DefaultOnToggle):
    """
    Enable EnergyLink support.
    EnergyLink works as a big Sub Tank/HP pool where players can request HP manually or automatically when
    they lose HP. You make use of this feature by typing /pool, /heal <amount> or /autoheal in the client.
    """
    display_name = "Energy Link"

class StartingLifeCount(Range):
    """
    How many lives to start the game with. 
    Note: This number becomes the new default life count, meaning that it will persist after a game over.
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 9
    default = 2

class LogicBossWeakness(DefaultOnToggle):
    """
    Every main boss will logically expect you to have its weakness.
    """
    display_name = "Boss Weakness Logic"

class LogicLegSigma(DefaultOnToggle):
    """
    Sigma's Fortress will logically expect you to have the legs upgrade.
    """
    display_name = "Sigma's Fortress Legs Upgrade Logic"

class LogicChargedShotgunIce(Toggle):
    """
    Adds Charged Shotgun Ice as logic to some locations. Some of those may be hard to execute.
    """
    display_name = "Charged Shotgun Ice Logic"

class EarlyLegs(Toggle):
    """
    Places the Legs Upgrade item in sphere 1.
    """
    display_name = "Early Legs"

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

class SigmaOpen(Choice):
    """
    Under what conditions will Sigma's Fortress open.
      multiworld: Access will require an Access Code multiworld item, similar to the main stages.
      medals: Access will be granted after collecting a certain amount of Maverick Medals.
      weapons: Access will be granted after collecting a certain amount of weapons.
      armor_upgrades: Access will be granted after collecting a certain amount of armor upgrades.
      heart_tanks: Access will be granted after collecting a certain amount of Heart Tanks.
      sub_tanks: Access will be granted after collecting a certain amount of Sub Tanks.
      all: Access will be granted after collecting a certain amount of Medals, Weapons, Armor Upgrades
           Heart Tanks and Sub Tanks.
    Do not enable all on solo seeds without pickupsanity or sessions with very few items.
    There's a big chance it'll cause an error.
    """
    display_name = "Sigma Fortress Rules"
    option_multiworld = 0
    option_medals = 1
    option_weapons = 2
    option_armor_upgrades = 4
    option_heart_tanks = 8
    option_sub_tanks = 16
    option_all = 31
    default = 1

class SigmaMedalCount(Range):
    """
    How many Maverick Medals are required to access Sigma's Fortress.
    """
    display_name = "Sigma Medal Count"
    range_start = 0
    range_end = 8
    default = 8

class SigmaWeaponCount(Range):
    """
    How many weapons are required to access Sigma's Fortress.
    """
    display_name = "Sigma Weapon Count"
    range_start = 0
    range_end = 8
    default = 8

class SigmaArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access Sigma's Fortress.
    """
    display_name = "Sigma Armor Upgrade Count"
    range_start = 0
    range_end = 4
    default = 3

class SigmaHeartTankCount(Range):
    """
    How many Heart Tanks are required to access Sigma's Fortress.
    """
    display_name = "Sigma Heart Tank Count"
    range_start = 0
    range_end = 8
    default = 8

class SigmaSubTankCount(Range):
    """
    How many Sub Tanks are required to access Sigma's Fortress.
    """
    display_name = "Sigma Sub Tank Count"
    range_start = 0
    range_end = 4
    default = 4


@dataclass
class MMXOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    energy_link: EnergyLink
    starting_life_count: StartingLifeCount
    pickupsanity: PickupSanity
    logic_boss_weakness: LogicBossWeakness
    logic_leg_sigma: LogicLegSigma
    logic_charged_shotgun_ice: LogicChargedShotgunIce
    early_legs: EarlyLegs
    sigma_open: SigmaOpen
    sigma_medal_count: SigmaMedalCount
    sigma_weapon_count: SigmaWeaponCount
    sigma_upgrade_count: SigmaArmorUpgradeCount
    sigma_heart_tank_count: SigmaHeartTankCount
    sigma_sub_tank_count: SigmaSubTankCount
