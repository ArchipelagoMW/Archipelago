from dataclasses import dataclass
import typing

from Options import Choice, Range, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions, StartInventoryPool

class StartingLifeCount(Range):
    """
    How many lives to start the game with. 
    This number becomes the new default life count, meaning that it will persist after a game over.
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

class LogicZSaber(Choice):
    """
    Adds the Z-Saber to the game's logic.
    """
    display_name = "Z-Saber Logic"
    option_not_required = 5
    option_required_for_lab_1 = 0
    option_required_for_lab_2 = 1
    option_required_for_lab_3 = 2
    option_required_for_doppler = 3
    option_only_sigma = 4
    default = 2

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

class DopplerOpen(Choice):
    """
    Under what conditions will Dr. Doppler's lab open.
      multiworld: Access will require an Access Code multiworld item, similar to the main stages.
      medals: Access will be granted after collecting a certain amount of Maverick Medals.
      weapons: Access will be granted after collecting a certain amount of weapons.
      armor_upgrades: Access will be granted after collecting a certain amount of armor upgrades.
      heart_tanks: Access will be granted after collecting a certain amount of Heart Tanks.
      sub_tanks: Access will be granted after collecting a certain amount of Sub Tanks.
    """
    display_name = "Doppler Lab rules"
    option_multiworld = 0
    option_medals = 1
    option_weapons = 2
    option_armor_upgrades = 3
    option_heart_tanks = 4
    option_sub_tanks = 5
    default = 1

class DopplerMedalCount(Range):
    """
    How many Maverick Medals are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Medal Count"
    range_start = 1
    range_end = 8
    default = 8

class DopplerWeaponCount(Range):
    """
    How many weapons are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Weapon Count"
    range_start = 1
    range_end = 8
    default = 8

class DopplerArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Armor Upgrade Count"
    range_start = 1
    range_end = 8
    default = 5

class DopplerHeartTankCount(Range):
    """
    How many Heart Tanks are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Heart Tank Count"
    range_start = 1
    range_end = 8
    default = 8

class DopplerSubTankCount(Range):
    """
    How many Sub Tanks are required to access Dr. Doppler's Lab.
    """
    display_name = "Doppler Sub Tank Count"
    range_start = 1
    range_end = 4
    default = 4

class VileOpen(Range):
    """
    Under what conditions will Vile's Stage open.
      multiworld: Access will require an Access Code multiworld item, similar to the main stages.
      medals: Access will be granted after collecting a certain amount of Maverick Medals.
      weapons: Access will be granted after collecting a certain amount of weapons.
      armor_upgrades: Access will be granted after collecting a certain amount of armor upgrades.
      heart_tanks: Access will be granted after collecting a certain amount of Heart Tanks.
      sub_tanks: Access will be granted after collecting a certain amount of Sub Tanks.
    """
    display_name = "Vile Stage rules"
    option_multiworld = 0
    option_medals = 1
    option_weapons = 2
    option_armor_upgrades = 3
    option_heart_tanks = 4
    option_sub_tanks = 5
    default = 1

class VileMedalCount(Range):
    """
    How many Maverick Medals are required to access Vile's Stage.
    """
    display_name = "Vile Medal Count"
    range_start = 0
    range_end = 8
    default = 2

class VileWeaponCount(Range):
    """
    How many weapons are required to access Vile's Stage.
    """
    display_name = "Vile Weapon Count"
    range_start = 0
    range_end = 8
    default = 2

class VileArmorUpgradeCount(Range):
    """
    How many armor upgrades are required to access Vile's Stage.
    """
    display_name = "Vile Armor Upgrade Count"
    range_start = 0
    range_end = 8
    default = 3

class VileHeartTankCount(Range):
    """
    How many Heart Tanks are required to access Vile's Stage.
    """
    display_name = "Vile Heart Tank Count"
    range_start = 0
    range_end = 8
    default = 4

class VileSubTankCount(Range):
    """
    How many Sub Tanks are required to access Vile's Stage.
    """
    display_name = "Vile Sub Tank Count"
    range_start = 0
    range_end = 4
    default = 2

@dataclass
class MMX3Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    starting_life_count: StartingLifeCount
    logic_boss_weakness: LogicBossWeakness
    logic_z_saber: LogicZSaber
    pickupsanity: PickupSanity
    doppler_open: DopplerOpen
    doppler_medal_count: DopplerMedalCount
    doppler_weapon_count: DopplerWeaponCount
    doppler_upgrade_count: DopplerArmorUpgradeCount
    doppler_heart_tank_count: DopplerHeartTankCount
    doppler_sub_tank_count: DopplerSubTankCount
    vile_open: DopplerOpen
    vile_medal_count: DopplerMedalCount
    vile_weapon_count: DopplerWeaponCount
    vile_upgrade_count: DopplerArmorUpgradeCount
    vile_heart_tank_count: DopplerHeartTankCount
    vile_sub_tank_count: DopplerSubTankCount

