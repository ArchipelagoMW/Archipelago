from dataclasses import dataclass
from typing import Any, List

from Options import Choice, ExcludeLocations, ItemDict, OptionGroup, StartInventoryPool
from Rac3Addresses import RAC3TAG
from worlds.AutoWorld import PerGameCommonOptions
from worlds.rac3 import RAC3OPTION
from .Items import default_starting_weapons


def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in rac3_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list


class StartingWeapons(ItemDict):
    """
    Determines which weapons you will be starting the game with, provide a count of the weapons you want to be picked
    between, 2 are selected to be placed on Veldin.
    """
    display_name = "Starting Weapons"
    min = 0
    max = 5
    default = default_starting_weapons
    valid_keys = default_starting_weapons.keys()


class BoltAndXPMultiplier(Choice):
    """
    Determines what your bolts and xp will be multiplied by, recommended to go with x6 if you hate grinding,
    x10 if you're looking to do a sync.
    Dev comment: This currently uses the NG+ multiplier so only bolt gain is affected, weapon xp gain is not.
    """
    display_name = "BoltAndXPMultiplier"
    option_x1 = 1
    option_x2 = 2
    option_x4 = 4
    option_x6 = 6
    option_x8 = 8
    option_x10 = 10
    default = 1


class EnableProgressiveWeapons(Choice):
    """
    Determines whether weapon level-ups are progressive items or not.
    Disabled: Weapon leveling and exp functions like in the vanilla game.
    Enabled: Weapon level-ups are progressive items placed in the item pool and weapon exp is disabled.
    """
    display_name = "EnableProgressiveWeapons"
    option_disable = 0
    option_enable = 1
    default = 1


class ExtraArmorUpgrade(Choice):
    """
    Determines how many extra progressive ArmorUpgrade items are included in the item pool. 1~2 is recommended.
    """
    display_name = "ExtraArmorUpgrade"
    option_no_extra = 0
    option_extra_1 = 1
    option_extra_2 = 2
    option_extra_3 = 3
    option_extra_4 = 4
    default = 0


class SkillPoints(Choice):
    """
    Determines which skill points are locations in the world.
    None: No skill points are locations.
    Simple: 15 simple skill points are locations. Still taking feedback on the selection:
    - Stay Squeaky Clean
    - Reflect on how to score
    - Lights, camera action!
    - Flee Flawlessly
    - Search for sunken treasure
    - Be a sharpshooter
    - Beat Helga's Best Time
    - Bugs to Birdie
    - Get to the belt
    - Feeling Lucky?
    - 2002 was a good year in the city
    - Aim High
    - Go for hang time
    - Break the Dan
    - You break it, you win it
    Every Skill Point: All 30 skill points are locations.
    """
    display_name = RAC3OPTION.SKILL_POINTS
    option_none = 0
    option_simple = 1
    option_every_skill_point = 2
    default = 1


class Trophies(Choice):
    """
    Determines which trophies are locations in the world.
    None: No trophies are locations.
    Collectables: Only the collectable trophies found on various planets are locations.
    Every Trophy: All special trophies that do not require NG+ are now also locations.
    """
    display_name = RAC3OPTION.TROPHIES
    option_none = 0
    option_collectables = 1
    option_every_trophy = 2
    default = 1


class TitaniumBolts(Choice):
    """
    Determines whether titanium bolts are locations in the world.
    Disabled: No titanium bolts are locations.
    Enabled: All titanium bolts are locations.
    """
    display_name = RAC3OPTION.TITANIUM_BOLTS
    option_disabled = 0
    option_enabled = 1
    default = 1


class NanotechMilestones(Choice):
    """
    Determines whether nanotech milestones are locations in the world.
    None: No nanotech milestones are locations.
    Every 5: Makes every 5 nanotech milestones locations starting from nanotech level 15.
    Every 10: Makes every 10 nanotech milestones locations starting from nanotech level 20.
    Every 20: Makes every 20 nanotech milestones locations starting from nanotech level 20.
    All: All nanotech milestones are locations.
    """
    display_name = RAC3OPTION.NANOTECH_MILESTONES
    option_none = 0
    option_every_5 = 1
    option_every_10 = 2
    option_every_20 = 3
    option_all = 4
    default = 0


class ShipWings(Choice):
    """
    Cosmetic:
    What Wings should you have on the ship?
    """
    display_name = RAC3OPTION.SHIP_WINGS
    option_standard = 0
    option_hi_lift = 4
    option_heavy_ordinance = 8


class ShipNose(Choice):
    """
    Cosmetic:
    What Nose should you have on the ship?
    """
    display_name = RAC3OPTION.SHIP_NOSE
    option_standard = 0
    option_split = 1
    option_scoop = 2


class ShipSkin(Choice):
    """
    Cosmetic:
    What Skin should you have on the ship?
    """
    display_name = RAC3OPTION.SHIP_SKIN
    option_Blargian_Red = 0
    option_Orxon_Green = 1
    option_Bogon_Blue = 2
    option_Insomniac_Special = 3
    option_Dark_Nebula = 4
    option_Dreks_Black_Heart = 5
    option_Space_Storm = 6
    option_Lunar_Eclipse = 7
    option_Plaidtastic = 8
    option_Supernova = 9
    option_Solar_Wind = 10
    option_Clowner = 11
    option_Silent_Strike = 12
    option_Lombax_Orange = 13
    option_Neutron_Star = 14
    option_Star_Traveller = 15
    option_Hooked_On_Onyx = 16
    option_Tyhrranoid_Void = 17
    option_Zeldren_Sunset = 18
    option_Ghost_Pirate_Purple = 19
    option_Qwark_Green = 20
    option_Agent_Orange = 21
    option_Helgas_Hues = 22
    option_Ameboid_Green = 23
    option_Pulsing_Purple = 24
    option_Obani_Orange = 25
    option_Low_Rider = 26
    option_Black_Hole = 27
    option_Sun_Storm = 28
    option_Sasha_Scarlet = 29
    option_Florana_Breeze = 30
    option_Ozzy_Kamikaze = 31


class RatchetSkin(Choice):
    """
    Cosmetic:
    What Skin should Ratchet have?
    """
    display_name = RAC3OPTION.SKIN
    option_default = 0
    option_old_school = 5
    option_snowman = 6
    option_tuxedo = 7
    option_buginoid = 8
    option_brainius = 9
    option_unused_robot = 10
    option_robo_rooster = 11
    option_trooper = 12
    option_robo = 13


class RAC3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({RAC3TAG.UNSTABLE, RAC3TAG.LONG_TROPHY})


@dataclass
class RaC3Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    starting_weapons: StartingWeapons
    bolt_and_xp_multiplier: BoltAndXPMultiplier
    enable_progressive_weapons: EnableProgressiveWeapons
    extra_armor_upgrade: ExtraArmorUpgrade
    skill_points: SkillPoints
    trophies: Trophies
    titanium_bolts: TitaniumBolts
    nanotech_milestones: NanotechMilestones
    exclude_locations: RAC3ExcludeLocations
    ship_nose: ShipNose
    ship_wings: ShipWings
    ship_skin: ShipSkin
    skin: RatchetSkin


rac3_option_groups: dict[str, List[Any]] = {
    "General Options": [StartInventoryPool, StartingWeapons, BoltAndXPMultiplier, EnableProgressiveWeapons,
                        ExtraArmorUpgrade, SkillPoints, Trophies, TitaniumBolts, NanotechMilestones],
    "Cosmetic Options": [ShipNose, ShipWings, ShipSkin, RatchetSkin],
}

slot_data_options: list[str] = [
    RAC3OPTION.START_INVENTORY_FROM_POOL,
    RAC3OPTION.STARTING_WEAPONS,
    RAC3OPTION.BOLT_AND_XP_MULTIPLIER,
    RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS,
    RAC3OPTION.EXTRA_ARMOR_UPGRADE,
    RAC3OPTION.SKILL_POINTS,
    RAC3OPTION.TROPHIES,
    RAC3OPTION.TITANIUM_BOLTS,
    RAC3OPTION.NANOTECH_MILESTONES,
    RAC3OPTION.EXCLUDE
]
