from dataclasses import dataclass
from typing import Any, List

from worlds.rac3.constants.Rac3Options import RAC3OPTION
from Options import OptionGroup, StartInventoryPool
from worlds.rac3.options.Deathlink import Deathlink
from worlds.rac3.options.Exclude import RAC3ExcludeLocations
from worlds.rac3.options.ExtraArmor import ExtraArmorUpgrade
from worlds.rac3.options.Multiplier import BoltAndXPMultiplier
from worlds.rac3.options.Nanotech import NanotechMilestones
from worlds.rac3.options.ProgWeapons import EnableProgressiveWeapons
from worlds.rac3.options.RatchetSkins import RatchetSkin
from worlds.rac3.options.ShipNose import ShipNose
from worlds.rac3.options.ShipSkin import ShipSkin
from worlds.rac3.options.ShipWings import ShipWings
from worlds.rac3.options.Skillpoints import SkillPoints
from worlds.rac3.options.StartingWeapons import StartingWeapons
from worlds.rac3.options.TitaniumBolts import TitaniumBolts
from worlds.rac3.options.Traps import EnableTraps
from worlds.rac3.options.TrapWeight import TrapWeight
from worlds.rac3.options.Trophies import Trophies
from worlds.AutoWorld import PerGameCommonOptions
from worlds.rac3.options.Rangers import Rangers
from worlds.rac3.options.Arena import Arena
from worlds.rac3.options.VidComics import VidComics


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
    vidcomics: VidComics


rac3_option_groups: dict[str, List[Any]] = {
    "Game Options": [StartInventoryPool, StartingWeapons, BoltAndXPMultiplier, EnableProgressiveWeapons,
                        ExtraArmorUpgrade, SkillPoints, Trophies, TitaniumBolts, NanotechMilestones, EnableTraps, TrapWeight, Rangers, Arena, VidComics],
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
    RAC3OPTION.VIDCOMICS,
]
