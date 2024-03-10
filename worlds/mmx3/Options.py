from dataclasses import dataclass
import typing

from Options import Choice, Range, Toggle, DefaultOnToggle, DeathLink, PerGameCommonOptions, StartInventoryPool

class StartingLifeCount(Range):
    """
    How many extra lives to start the game with
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 9
    default = 2

class LogicBossWeakness(DefaultOnToggle):
    """
    Los jefes requieren que tengas el arma a la que son debiles para poder pelearlos
    """
    display_name = "Boss Weakness Logic"

class LogicZSaber(Choice):
    """
    Añade el Z-Saber a la logica
    """
    display_name = "Z-Saber Logic"
    option_not_required = 5
    option_required_for_lab_1 = 0
    option_required_for_lab_2 = 1
    option_required_for_lab_3 = 2
    option_required_for_doppler = 3
    option_only_sigma = 4
    default = 3

class PickupSanity(Toggle):
    """
    Whether collecting freestanding HP & Weapon Energy capsules will grant a check
    """
    display_name = "Pickupsanity"

class DopplerOpen(Choice):
    """
    Bajo que regla se abre el Dr. Doppler Lab
    multiworld: El acceso se encuentra donde sea
    medals: Obtienes acceso al tener cierto numero de medallas
    weapons: Obtienes acceso al tener cierto numero de armas
    armor_upgrades: Obtienes acceso al tener cierto numero de upgrades
    heart_tanks: Obtienes acceso al tener cierto numero de  Heart Tanks
    sub_tanks: Obtienes acceso al tener cierto numero de los Sub Tanks
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
    Cuantas medallas se ocupan para abrir el Dr. Doppler Lab
    """
    display_name = "Doppler Medal Count"
    range_start = 1
    range_end = 8
    default = 8

class DopplerWeaponCount(Range):
    """
    Cuantas armas se ocupan para abrir el Dr. Doppler Lab
    """
    display_name = "Doppler Weapon Count"
    range_start = 1
    range_end = 8
    default = 8

class DopplerArmorUpgradeCount(Range):
    """
    Cuantos upgrades de armadura se ocupan para abrir el Dr. Doppler Lab
    """
    display_name = "Doppler Armor Upgrade Count"
    range_start = 1
    range_end = 8
    default = 5

class DopplerHeartTankCount(Range):
    """
    Cuantos Heart Tank se ocupan para abrir el Dr. Doppler Lab
    """
    display_name = "Doppler Heart Tank Count"
    range_start = 1
    range_end = 8
    default = 8

class DopplerSubTankCount(Range):
    """
    Cuantos Sub Tank se ocupan para abrir el Dr. Doppler Lab
    """
    display_name = "Doppler Sub Tank Count"
    range_start = 1
    range_end = 4
    default = 4

class VileOpen(Range):
    """
    AUN NO SIRVE (DOES NOT WORK YET)
    Bajo que regla se abre el nivel de Vile
    multiworld: El acceso se encuentra donde sea
    medals: Obtienes acceso al tener cierto numero de medallas
    weapons: Obtienes acceso al tener cierto numero de armas
    armor_upgrades: Obtienes acceso al tener cierto numero de upgrades
    heart_tanks: Obtienes acceso al tener cierto numero de  Heart Tanks
    sub_tanks: Obtienes acceso al tener cierto numero de los Sub Tanks
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
    AUN NO SIRVE (DOES NOT WORK YET)
    Cuantas medallas se ocupan para abrir el Vile Stage
    """
    display_name = "Vile Medal Count"
    range_start = 1
    range_end = 8
    default = 2

class VileWeaponCount(Range):
    """
    AUN NO SIRVE (DOES NOT WORK YET)
    Cuantas armas se ocupan para abrir el Vile Stage
    """
    display_name = "Vile Weapon Count"
    range_start = 1
    range_end = 8
    default = 8

class VileArmorUpgradeCount(Range):
    """
    AUN NO SIRVE (DOES NOT WORK YET)
    Cuantos upgrades de armadura se ocupan para abrir el Vile Stage
    """
    display_name = "Vile Armor Upgrade Count"
    range_start = 1
    range_end = 8
    default = 2

class VileHeartTankCount(Range):
    """
    AUN NO SIRVE (DOES NOT WORK YET)
    Cuantos Heart Tank se ocupan para abrir el Vile Stage
    """
    display_name = "Vile Heart Tank Count"
    range_start = 1
    range_end = 8
    default = 4

class VileSubTankCount(Range):
    """
    AUN NO SIRVE (DOES NOT WORK YET)
    Cuantos Sub Tank se ocupan para abrir el Vile Stage
    """
    display_name = "Vile Sub Tank Count"
    range_start = 1
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

