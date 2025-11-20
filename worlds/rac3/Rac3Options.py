from dataclasses import dataclass
from typing import Any, List

from constants.Rac3Options import RAC3OPTION
from Options import OptionGroup, StartInventoryPool
from options.Deathlink import Deathlink
from options.Exclude import RAC3ExcludeLocations
from options.ExtraArmor import ExtraArmorUpgrade
from options.Multiplier import BoltAndXPMultiplier
from options.Nanotech import NanotechMilestones
from options.ProgWeapons import EnableProgressiveWeapons
from options.RatchetSkins import RatchetSkin
from options.ShipNose import ShipNose
from options.ShipSkin import ShipSkin
from options.ShipWings import ShipWings
from options.Skillpoints import SkillPoints
from options.StartingWeapons import StartingWeapons
from options.TitaniumBolts import TitaniumBolts
from options.Traps import EnableTraps
from options.TrapWeight import TrapWeight
from options.Trophies import Trophies
from worlds.AutoWorld import PerGameCommonOptions
from options.Rangers import Rangers
from options.Arena import Arena


def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in rac3_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list


@dataclass
class RaC3Options(PerGameCommonOptions):

    deathlink: Deathlink
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
    traps_enabled: EnableTraps
    trap_weight: TrapWeight
    rangers: Rangers
    arena: Arena


rac3_option_groups: dict[str, List[Any]] = {
    "Game Options": [StartInventoryPool, StartingWeapons, BoltAndXPMultiplier, EnableProgressiveWeapons,
                        ExtraArmorUpgrade, SkillPoints, Trophies, TitaniumBolts, NanotechMilestones, EnableTraps, TrapWeight, Rangers, Arena],
    "Cosmetic Options": [ShipNose, ShipWings, ShipSkin, RatchetSkin],
    "Generic Options": [Deathlink, RAC3ExcludeLocations],
}

slot_data_options: list[str] = [
    RAC3OPTION.DEATHLINK,
    RAC3OPTION.START_INVENTORY_FROM_POOL,
    RAC3OPTION.STARTING_WEAPONS,
    RAC3OPTION.BOLT_AND_XP_MULTIPLIER,
    RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS,
    RAC3OPTION.EXTRA_ARMOR_UPGRADE,
    RAC3OPTION.SKILL_POINTS,
    RAC3OPTION.TROPHIES,
    RAC3OPTION.TITANIUM_BOLTS,
    RAC3OPTION.NANOTECH_MILESTONES,
    RAC3OPTION.EXCLUDE,
    RAC3OPTION.SHIP_NOSE,
    RAC3OPTION.SHIP_WINGS,
    RAC3OPTION.SHIP_SKIN,
    RAC3OPTION.SKIN,
    RAC3OPTION.ENABLE_TRAPS,
    RAC3OPTION.TRAP_WEIGHT,
    RAC3OPTION.RANGERS,
    RAC3OPTION.ARENA,
]
