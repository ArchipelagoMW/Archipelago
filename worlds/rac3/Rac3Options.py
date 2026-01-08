from dataclasses import dataclass
from typing import Any, Dict, List

from Options import Choice, ExcludeLocations, ItemDict, OptionGroup, StartInventoryPool
from worlds.AutoWorld import PerGameCommonOptions
from .Items import default_starting_weapons

# Common variable
GAME_TITLE = "Rac3"
GAME_TITLE_FULL = "Ratchet & Clank 3"


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
    display_name = "Skill Points"
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
    display_name = "Trophies"
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
    display_name = "Titanium Bolts"
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
    display_name = "Nanotech Milestones"
    option_none = 0
    option_every_5 = 1
    option_every_10 = 2
    option_every_20 = 3
    option_all = 4
    default = 0

class RAC3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset({'Unstable', 'Long Term Trophy', 'Weapons', 'Gadgets'})


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


rac3_option_groups: Dict[str, List[Any]] = {
    "General Options": [StartInventoryPool, StartingWeapons, BoltAndXPMultiplier, EnableProgressiveWeapons,
                        ExtraArmorUpgrade, SkillPoints, Trophies, TitaniumBolts, NanotechMilestones]
}

slot_data_options: list[str] = [
    "start_inventory_from_pool"
    "starting_weapons",
    "bolt_and_xp_multiplier",
    "enable_progressive_weapons",
    "extra_armor_upgrade",
    "skill_points",
    "trophies",
    "titanium_bolts",
    "nanotech_milestones",
    "exclude_locations"
]
