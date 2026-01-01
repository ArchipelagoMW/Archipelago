from typing import TYPE_CHECKING

from worlds.rac3.constants.data.location import RAC3_LOCATION_DATA_TABLE
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.region import RAC3REGION

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World


def get_total_locations(world: "RaC3World") -> int:
    locations = [l for l in world.multiworld.get_locations() if l.player == world.player]
    return len(locations)


def get_location_names() -> dict[str, int]:
    return {name: data.AP_CODE for name, data in RAC3_LOCATION_DATA_TABLE.items()}


def get_regions() -> list[str]:
    regions = [data.REGION for data in RAC3_LOCATION_DATA_TABLE.values()]
    return regions


def get_from_tag(tag) -> set[str]:
    return set(loc for loc in RAC3_LOCATION_DATA_TABLE.keys() if tag in RAC3_LOCATION_DATA_TABLE[loc].TAGS)


# class LocData(NamedTuple):
#     ap_code: Optional[int]
#     region: Optional[str]


# weapon_upgrades = {
#
#     "Shock Blaster: V2": LocData(50150000, "Shock Blaster Upgrades"),
#     "Shock Blaster: V3": LocData(50150001, "Shock Blaster Upgrades"),
#     "Shock Blaster: V4": LocData(50150002, "Shock Blaster Upgrades"),
#     "Shock Blaster: V5": LocData(50150003, "Shock Blaster Upgrades"),
#
#     "Nitro Launcher: V2": LocData(50150004, "Nitro Launcher Upgrades"),
#     "Nitro Launcher: V3": LocData(50150005, "Nitro Launcher Upgrades"),
#     "Nitro Launcher: V4": LocData(50150006, "Nitro Launcher Upgrades"),
#     "Nitro Launcher: V5": LocData(50150007, "Nitro Launcher Upgrades"),
#
#     "N60 Storm: V2": LocData(50150008, "N60 Storm Upgrades"),
#     "N60 Storm: V3": LocData(50150009, "N60 Storm Upgrades"),
#     "N60 Storm: V4": LocData(50150010, "N60 Storm Upgrades"),
#     "N60 Storm: V5": LocData(50150011, "N60 Storm Upgrades"),
#
#     "Plasma Whip: V2": LocData(50150012, "Plasma Whip Upgrades"),
#     "Plasma Whip: V3": LocData(50150013, "Plasma Whip Upgrades"),
#     "Plasma Whip: V4": LocData(50150014, "Plasma Whip Upgrades"),
#     "Plasma Whip: V5": LocData(50150015, "Plasma Whip Upgrades"),
#
#     "Infector: V2": LocData(50150016, "Infector Upgrades"),
#     "Infector: V3": LocData(50150017, "Infector Upgrades"),
#     "Infector: V4": LocData(50150018, "Infector Upgrades"),
#     "Infector: V5": LocData(50150019, "Infector Upgrades"),
#
#     "Suck Cannon: V2": LocData(50150020, "Suck Cannon Upgrades"),
#     "Suck Cannon: V3": LocData(50150021, "Suck Cannon Upgrades"),
#     "Suck Cannon: V4": LocData(50150022, "Suck Cannon Upgrades"),
#     "Suck Cannon: V5": LocData(50150023, "Suck Cannon Upgrades"),
#
#     "Spitting Hydra: V2": LocData(50150024, "Spitting Hydra Upgrades"),
#     "Spitting Hydra: V3": LocData(50150025, "Spitting Hydra Upgrades"),
#     "Spitting Hydra: V4": LocData(50150026, "Spitting Hydra Upgrades"),
#     "Spitting Hydra: V5": LocData(50150027, "Spitting Hydra Upgrades"),
#
#     "Agents of Doom: V2": LocData(50150028, "Agents of Doom Upgrades"),
#     "Agents of Doom: V3": LocData(50150029, "Agents of Doom Upgrades"),
#     "Agents of Doom: V4": LocData(50150030, "Agents of Doom Upgrades"),
#     "Agents of Doom: V5": LocData(50150031, "Agents of Doom Upgrades"),
#
#     "Flux Rifle: V2": LocData(50150032, "Flux Rifle Upgrades"),
#     "Flux Rifle: V3": LocData(50150033, "Flux Rifle Upgrades"),
#     "Flux Rifle: V4": LocData(50150034, "Flux Rifle Upgrades"),
#     "Flux Rifle: V5": LocData(50150035, "Flux Rifle Upgrades"),
#
#     "Annihilator: V2": LocData(50150036, "Annihilator Upgrades"),
#     "Annihilator: V3": LocData(50150037, "Annihilator Upgrades"),
#     "Annihilator: V4": LocData(50150038, "Annihilator Upgrades"),
#     "Annihilator: V5": LocData(50150039, "Annihilator Upgrades"),
#
#     "Holo-Shield Glove: V2": LocData(50150040, "Holo-Shield Glove Upgrades"),
#     "Holo-Shield Glove: V3": LocData(50150041, "Holo-Shield Glove Upgrades"),
#     "Holo-Shield Glove: V4": LocData(50150042, "Holo-Shield Glove Upgrades"),
#     "Holo-Shield Glove: V5": LocData(50150043, "Holo-Shield Glove Upgrades"),
#
#     "Disc-Blade Gun: V2": LocData(50150044, "Disc-Blade Gun Upgrades"),
#     "Disc-Blade Gun: V3": LocData(50150045, "Disc-Blade Gun Upgrades"),
#     "Disc-Blade Gun: V4": LocData(50150046, "Disc-Blade Gun Upgrades"),
#     "Disc-Blade Gun: V5": LocData(50150047, "Disc-Blade Gun Upgrades"),
#
#     "Rift Inducer: V2": LocData(50150048, "Rift Inducer Upgrades"),
#     "Rift Inducer: V3": LocData(50150049, "Rift Inducer Upgrades"),
#     "Rift Inducer: V4": LocData(50150050, "Rift Inducer Upgrades"),
#     "Rift Inducer: V5": LocData(50150051, "Rift Inducer Upgrades"),
#
#     "Qwack-O-Ray: V2": LocData(50150052, "Qwack-O-Ray Upgrades"),
#     "Qwack-O-Ray: V3": LocData(50150053, "Qwack-O-Ray Upgrades"),
#     "Qwack-O-Ray: V4": LocData(50150054, "Qwack-O-Ray Upgrades"),
#     "Qwack-O-Ray: V5": LocData(50150055, "Qwack-O-Ray Upgrades"),
#
#     "RY3N0: V2": LocData(50150056, "RY3N0 Upgrades"),
#     "RY3N0: V3": LocData(50150057, "RY3N0 Upgrades"),
#     "RY3N0: V4": LocData(50150058, "RY3N0 Upgrades"),
#     "RY3N0: V5": LocData(50150059, "RY3N0 Upgrades"),
#
#     "Mini-Turret Glove: V2": LocData(50150060, "Mini-Turret Glove Upgrades"),
#     "Mini-Turret Glove: V3": LocData(50150061, "Mini-Turret Glove Upgrades"),
#     "Mini-Turret Glove: V4": LocData(50150062, "Mini-Turret Glove Upgrades"),
#     "Mini-Turret Glove: V5": LocData(50150063, "Mini-Turret Glove Upgrades"),
#
#     "Lava Gun: V2": LocData(50150064, "Lava Gun Upgrades"),
#     "Lava Gun: V3": LocData(50150065, "Lava Gun Upgrades"),
#     "Lava Gun: V4": LocData(50150066, "Lava Gun Upgrades"),
#     "Lava Gun: V5": LocData(50150067, "Lava Gun Upgrades"),
#
#     "Shield Charger: V2": LocData(50150068, "Shield Charger Upgrades"),
#     "Shield Charger: V3": LocData(50150069, "Shield Charger Upgrades"),
#     "Shield Charger: V4": LocData(50150070, "Shield Charger Upgrades"),
#     "Shield Charger: V5": LocData(50150071, "Shield Charger Upgrades"),
#
#     "Bouncer: V2": LocData(50150072, "Bouncer Upgrades"),
#     "Bouncer: V3": LocData(50150073, "Bouncer Upgrades"),
#     "Bouncer: V4": LocData(50150074, "Bouncer Upgrades"),
#     "Bouncer: V5": LocData(50150075, "Bouncer Upgrades"),
#
#     "Plasma Coil: V2": LocData(50150076, "Plasma Coil Upgrades"),
#     "Plasma Coil: V3": LocData(50150077, "Plasma Coil Upgrades"),
#     "Plasma Coil: V4": LocData(50150078, "Plasma Coil Upgrades"),
#     "Plasma Coil: V5": LocData(50150079, "Plasma Coil Upgrades"),
#
# }

# class EventData(NamedTuple):
#     ap_code: None
#     region: Optional[str]
#
#
# rac3_events = {  # Events have no ap_code
#     "Cleared Veldin": EventData(None, RAC3REGION.VELDIN),
#     "Cleared Florana": EventData(None, RAC3REGION.FLORANA),
#     "Cleared Marcadia": EventData(None, RAC3REGION.MARCADIA),
#     "Cleared Annihilation Nation 1": EventData(None, RAC3REGION.ANNIHILATION_NATION),
#     "Cleared Annihilation Nation 2": EventData(None, RAC3REGION.ANNIHILATION_NATION_2),
#     "Cleared Aquatos": EventData(None, RAC3REGION.AQUATOS),
#     "Cleared Tyhrranosis": EventData(None, RAC3REGION.TYHRRANOSIS),
#     "Cleared Daxx": EventData(None, RAC3REGION.DAXX),
# }


all_tags: list[str] = [
    RAC3TAG.SKILLPOINT,
    RAC3TAG.T_BOLT,
    RAC3TAG.SEWER,
    RAC3TAG.VIDCOMIC,
    RAC3TAG.TROPHY,
    RAC3TAG.LONG_TROPHY,
    RAC3TAG.RANGERS,
    RAC3TAG.ARENA,
    RAC3TAG.NANOTECH,
    RAC3TAG.UNSTABLE,
    RAC3TAG.WEAPONS,
    RAC3TAG.GADGETS,
    RAC3TAG.INFOBOT,
    RAC3TAG.VR,
    RAC3TAG.ONE_HP_UNSTABLE,
]

location_groups: dict[str, set[str]] = {
    RAC3REGION.VELDIN: get_from_tag(RAC3REGION.VELDIN),
    RAC3REGION.FLORANA: get_from_tag(RAC3REGION.FLORANA),
    RAC3REGION.STARSHIP_PHOENIX: get_from_tag(RAC3REGION.STARSHIP_PHOENIX),
    RAC3REGION.MARCADIA: get_from_tag(RAC3REGION.MARCADIA),
    RAC3REGION.ANNIHILATION_NATION: get_from_tag(RAC3REGION.ANNIHILATION_NATION),
    RAC3REGION.AQUATOS: get_from_tag(RAC3REGION.AQUATOS),
    RAC3REGION.TYHRRANOSIS: get_from_tag(RAC3REGION.TYHRRANOSIS),
    RAC3REGION.DAXX: get_from_tag(RAC3REGION.DAXX),
    RAC3REGION.OBANI_GEMINI: get_from_tag(RAC3REGION.OBANI_GEMINI),
    RAC3REGION.BLACKWATER_CITY: get_from_tag(RAC3REGION.BLACKWATER_CITY),
    RAC3REGION.HOLOSTAR_STUDIOS: get_from_tag(RAC3REGION.HOLOSTAR_STUDIOS),
    RAC3REGION.OBANI_DRACO: get_from_tag(RAC3REGION.OBANI_DRACO),
    RAC3REGION.ZELDRIN_STARPORT: get_from_tag(RAC3REGION.ZELDRIN_STARPORT),
    RAC3REGION.METROPOLIS: get_from_tag(RAC3REGION.METROPOLIS),
    RAC3REGION.CRASH_SITE: get_from_tag(RAC3REGION.CRASH_SITE),
    RAC3REGION.ARIDIA: get_from_tag(RAC3REGION.ARIDIA),
    RAC3REGION.QWARKS_HIDEOUT: get_from_tag(RAC3REGION.QWARKS_HIDEOUT),
    RAC3REGION.KOROS: get_from_tag(RAC3REGION.KOROS),
    RAC3REGION.COMMAND_CENTER: get_from_tag(RAC3REGION.COMMAND_CENTER),
    RAC3TAG.SKILLPOINT: get_from_tag(RAC3TAG.SKILLPOINT),
    RAC3TAG.T_BOLT: get_from_tag(RAC3TAG.T_BOLT),
    RAC3TAG.SEWER: get_from_tag(RAC3TAG.SEWER),
    RAC3TAG.VIDCOMIC: get_from_tag(RAC3TAG.VIDCOMIC),
    RAC3TAG.TROPHY: get_from_tag(RAC3TAG.TROPHY),  # All trophies including long term
    RAC3TAG.LONG_TROPHY: get_from_tag(RAC3TAG.LONG_TROPHY),  # Long Term trophies only
    RAC3TAG.RANGERS: get_from_tag(RAC3TAG.RANGERS),
    RAC3TAG.ARENA: get_from_tag(RAC3TAG.ARENA),
    RAC3TAG.NANOTECH: get_from_tag(RAC3TAG.NANOTECH),
    RAC3TAG.UNSTABLE: get_from_tag(RAC3TAG.UNSTABLE),
    RAC3TAG.WEAPONS: get_from_tag(RAC3TAG.WEAPONS),
    RAC3TAG.GADGETS: get_from_tag(RAC3TAG.GADGETS),
    RAC3TAG.INFOBOT: get_from_tag(RAC3TAG.INFOBOT),
    RAC3TAG.ONE_HP_UNSTABLE: get_from_tag(RAC3TAG.ONE_HP_UNSTABLE),
}


def get_level_locations(region: str) -> map:
    return map(lambda l: l[0], get_level_location_data(region))


def get_level_location_data(region: str) -> filter:
    return filter(lambda l: l[1].REGION == region, RAC3_LOCATION_DATA_TABLE.items())
