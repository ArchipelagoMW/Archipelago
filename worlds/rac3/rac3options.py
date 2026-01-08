from dataclasses import dataclass

from Options import Accessibility, OptionGroup, ProgressionBalancing, StartInventoryPool
from worlds.AutoWorld import PerGameCommonOptions
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.options.arena_options import Arena
from worlds.rac3.options.armor_upgrade_options import ArmorUpgrade
from worlds.rac3.options.deathlink_options import Deathlink
from worlds.rac3.options.exclude_options import RAC3ExcludeLocations
from worlds.rac3.options.filler_weight_options import FillerWeight
from worlds.rac3.options.multiplier_options import BoltAndXPMultiplier
from worlds.rac3.options.nanotech_limitation_options import NanotechLimitation
from worlds.rac3.options.nanotech_options import NanotechMilestones
from worlds.rac3.options.one_hp_options import OneHpChallenge
from worlds.rac3.options.prog_weapons_options import EnableProgressiveWeapons
from worlds.rac3.options.rangers_options import Rangers
from worlds.rac3.options.ratchet_skins_options import RatchetSkin
from worlds.rac3.options.sewer_limitation_options import SewerLimitation
from worlds.rac3.options.sewer_options import SewerCrystals
from worlds.rac3.options.ship_nose_options import ShipNose
from worlds.rac3.options.ship_skin_options import ShipSkin
from worlds.rac3.options.ship_wings_options import ShipWings
from worlds.rac3.options.skillpoints_options import SkillPoints
from worlds.rac3.options.starting_weapons_options import StartingWeapons
from worlds.rac3.options.titanium_bolts_options import TitaniumBolts
from worlds.rac3.options.trap_weight_options import TrapWeight
from worlds.rac3.options.traps_options import EnableTraps
from worlds.rac3.options.trophies_options import Trophies
from worlds.rac3.options.vidcomics_options import VidComics
from worlds.rac3.options.vr_challenges_options import VRChallenges
from worlds.rac3.options.weapon_vendors_options import WeaponVendors


def create_option_groups() -> list[OptionGroup]:
    option_group_list: list[OptionGroup] = []
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
    armor_upgrade: ArmorUpgrade
    filler_weight: FillerWeight
    sewer_limitation: SewerLimitation
    traps_enabled: EnableTraps
    trap_weight: TrapWeight
    weapon_vendors: WeaponVendors
    skill_points: SkillPoints
    trophies: Trophies
    titanium_bolts: TitaniumBolts
    rangers: Rangers
    vidcomics: VidComics
    vr_challenges: VRChallenges
    arena: Arena
    sewer_crystals: SewerCrystals
    sewer_limitation: SewerLimitation
    nanotech_milestones: NanotechMilestones
    nanotech_limitation: NanotechLimitation
    exclude_locations: RAC3ExcludeLocations
    ship_nose: ShipNose
    ship_wings: ShipWings
    ship_skin: ShipSkin
    skin: RatchetSkin
    one_hp_challenge: OneHpChallenge


rac3_option_groups = [
    OptionGroup("Generic Options", [
        ProgressionBalancing,
        Accessibility,
        Deathlink,
        RAC3ExcludeLocations,
    ]),
    OptionGroup("RAC3 Game Options", [
        BoltAndXPMultiplier,
        OneHpChallenge,
    ]),
    OptionGroup("RAC3 Item Options", [
        StartingWeapons,
        EnableProgressiveWeapons,
        ArmorUpgrade,
        EnableTraps,
        TrapWeight,
        FillerWeight,
    ]),
    OptionGroup("RAC3 Location Options", [
        WeaponVendors,
        SkillPoints,
        Trophies,
        TitaniumBolts,
        Rangers,
        VidComics,
        VRChallenges,
        Arena,
        SewerCrystals,
        SewerLimitation,
        NanotechMilestones,
        NanotechLimitation,
    ]),
    OptionGroup("RAC3 Cosmetic Options", [
        ShipNose,
        ShipWings,
        ShipSkin,
        RatchetSkin,
    ]),
]

slot_data_options: list[str] = [
    RAC3OPTION.DEATHLINK,
    RAC3OPTION.START_INVENTORY_FROM_POOL,
    RAC3OPTION.STARTING_WEAPONS,
    RAC3OPTION.BOLT_AND_XP_MULTIPLIER,
    RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS,
    RAC3OPTION.ARMOR_UPGRADE,
    RAC3OPTION.SKILL_POINTS,
    RAC3OPTION.TROPHIES,
    RAC3OPTION.TITANIUM_BOLTS,
    RAC3OPTION.NANOTECH_MILESTONES,
    RAC3OPTION.NANOTECH_LIMITATION,
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
    RAC3OPTION.VR_CHALLENGES,
    RAC3OPTION.SEWER_CRYSTALS,
    RAC3OPTION.SEWER_LIMITATION,
    RAC3OPTION.WEAPON_VENDORS,
    RAC3OPTION.FILLER_WEIGHT,
    RAC3OPTION.ONE_HP_CHALLENGE,
]
