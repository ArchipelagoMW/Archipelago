from dataclasses import dataclass
from typing import Dict, List, Optional

from .RoomNames import RoomName

from .AreaNames import MetroidPrimeArea
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


@dataclass
class BlastShieldRegion:
    name: RoomName
    doors: Dict[RoomName, RoomName]
    can_be_locked: bool = False
    invalid_start_rooms: Optional[List[RoomName]] = None


@dataclass
class BlastShieldArea:
    """Regions used to determine where blast shields can be placed within a prime area"""

    area: MetroidPrimeArea
    regions: List[BlastShieldRegion]


def __get_chozo_region():
    return BlastShieldArea(
        area=MetroidPrimeArea.Chozo_Ruins,
        regions=[
            BlastShieldRegion(
                name=RoomName.Ruins_Entrance,
                doors={
                    RoomName.Transport_to_Tallon_Overworld_North: RoomName.Ruins_Entrance,
                    RoomName.Ruins_Entrance: RoomName.Main_Plaza,
                },
                invalid_start_rooms=[
                    RoomName.Warrior_Shrine,
                    RoomName.Transport_to_Chozo_Ruins_East,
                    RoomName.Arbor_Chamber,
                    RoomName.Landing_Site,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Ruined_Shrine,
                doors={
                    RoomName.Main_Plaza: RoomName.Ruined_Shrine_Access,
                },
                invalid_start_rooms=[
                    RoomName.Arboretum,
                    RoomName.Sunchamber_Lobby,
                    RoomName.Save_Station_1,
                    RoomName.Save_Station_2,
                    RoomName.Burn_Dome,
                    RoomName.Ruined_Fountain,
                    RoomName.Tower_Chamber,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Tower_of_Light,
                doors={
                    RoomName.Ruined_Shrine: RoomName.Tower_of_Light_Access,
                },
                invalid_start_rooms=[RoomName.Tower_Chamber],
            ),
            BlastShieldRegion(
                name=RoomName.Ruined_Nursery,
                can_be_locked=True,
                doors={
                    RoomName.Main_Plaza: RoomName.Nursery_Access,
                },
                invalid_start_rooms=[
                    RoomName.Arboretum,
                    RoomName.Sunchamber_Lobby,
                    RoomName.Save_Station_1,
                    RoomName.Save_Station_2,
                    RoomName.Burn_Dome,
                    RoomName.Ruined_Fountain,
                    RoomName.Tower_Chamber,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Hive_Totem,
                can_be_locked=True,
                doors={
                    RoomName.North_Atrium: RoomName.Ruined_Gallery,
                    RoomName.Totem_Access: RoomName.Hive_Totem,
                    RoomName.Transport_Access_North: RoomName.Transport_to_Magmoor_Caverns_North,
                },
                invalid_start_rooms=[RoomName.Save_Station_1, RoomName.Tower_Chamber],
            ),
            BlastShieldRegion(
                name=RoomName.Vault,
                doors={
                    RoomName.Transport_to_Magmoor_Caverns_North: RoomName.Vault_Access,
                    RoomName.Vault: RoomName.Plaza_Access,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Training_Chamber,
                doors={
                    RoomName.Main_Plaza: RoomName.Ruined_Fountain_Access,
                    RoomName.Ruined_Fountain: RoomName.Meditation_Fountain,
                    RoomName.Meditation_Fountain: RoomName.Magma_Pool,
                    RoomName.Magma_Pool: RoomName.Training_Chamber_Access,
                    RoomName.Training_Chamber_Access: RoomName.Training_Chamber,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Ruined_Fountain,
                doors={
                    RoomName.Ruined_Fountain: RoomName.Arboretum_Access,
                    RoomName.Arboretum_Access: RoomName.Arboretum,
                },
                invalid_start_rooms=[
                    RoomName.Arboretum,
                    RoomName.Sunchamber_Lobby,
                    RoomName.Save_Station_1,
                    RoomName.Save_Station_2,
                    RoomName.Burn_Dome,
                    RoomName.Ruined_Fountain,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Arboretum,
                doors={
                    RoomName.Sunchamber_Lobby: RoomName.Arboretum,
                    RoomName.Gathering_Hall_Access: RoomName.Arboretum,
                },
                invalid_start_rooms=[
                    RoomName.Arboretum,
                    RoomName.Sunchamber_Lobby,
                    RoomName.Save_Station_1,
                    RoomName.Save_Station_2,
                    RoomName.Burn_Dome,
                    RoomName.Ruined_Fountain,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Watery_Hall,
                doors={
                    RoomName.Gathering_Hall: RoomName.Watery_Hall_Access,
                    RoomName.Watery_Hall: RoomName.Dynamo_Access,
                },
                invalid_start_rooms=[
                    RoomName.Arboretum,
                    RoomName.Sunchamber_Lobby,
                    RoomName.Save_Station_1,
                    RoomName.Save_Station_2,
                    RoomName.Burn_Dome,
                    RoomName.Ruined_Fountain,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Energy_Core,
                can_be_locked=True,
                doors={
                    RoomName.Gathering_Hall: RoomName.East_Atrium,
                    RoomName.Energy_Core_Access: RoomName.Energy_Core,
                },
                invalid_start_rooms=[
                    RoomName.Arboretum,
                    RoomName.Sunchamber_Lobby,
                    RoomName.Save_Station_1,
                    RoomName.Save_Station_2,
                    RoomName.Burn_Dome,
                    RoomName.Ruined_Fountain,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Burn_Dome,
                doors={
                    RoomName.Burn_Dome_Access: RoomName.Burn_Dome,
                },
                invalid_start_rooms=[RoomName.Burn_Dome, RoomName.Arboretum],
            ),
            BlastShieldRegion(
                name=RoomName.Furnace,
                can_be_locked=True,
                doors={RoomName.Furnace: RoomName.East_Furnace_Access},
            ),
            BlastShieldRegion(
                name=RoomName.Crossway,
                doors={
                    RoomName.Crossway_Access_West: RoomName.Crossway,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Elder_Hall_Access,
                doors={
                    RoomName.Crossway: RoomName.Elder_Hall_Access,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Hall_of_the_Elders,
                doors={RoomName.Hall_of_the_Elders: RoomName.Reflecting_Pool_Access},
            ),
            BlastShieldRegion(
                name=RoomName.Reflecting_Pool,
                doors={
                    RoomName.Antechamber: RoomName.Reflecting_Pool,
                    RoomName.Save_Station_3: RoomName.Reflecting_Pool,
                    RoomName.Transport_Access_South: RoomName.Reflecting_Pool,
                },
            ),
        ],
    )


def __get_tallon_region():
    return BlastShieldArea(
        area=MetroidPrimeArea.Tallon_Overworld,
        regions=[
            BlastShieldRegion(
                name=RoomName.Alcove,
                doors={
                    RoomName.Landing_Site: RoomName.Alcove,
                },
                invalid_start_rooms=[RoomName.Arbor_Chamber],
            ),
            BlastShieldRegion(
                name=RoomName.Canyon_Cavern,
                can_be_locked=True,
                doors={RoomName.Landing_Site: RoomName.Canyon_Cavern},
                invalid_start_rooms=[
                    RoomName.Arbor_Chamber,
                    RoomName.Transport_to_Chozo_Ruins_East,
                    RoomName.Landing_Site,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Temple_Hall,
                doors={RoomName.Landing_Site: RoomName.Temple_Hall},
                invalid_start_rooms=[
                    RoomName.Arbor_Chamber,
                    RoomName.Transport_to_Chozo_Ruins_East,
                    RoomName.Landing_Site,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Waterfall_Cavern,
                can_be_locked=True,
                doors={RoomName.Landing_Site: RoomName.Waterfall_Cavern},
                invalid_start_rooms=[
                    RoomName.Transport_to_Chozo_Ruins_East,
                    RoomName.Landing_Site,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Transport_Tunnel_B,
                can_be_locked=True,
                doors={
                    RoomName.Tallon_Canyon: RoomName.Root_Tunnel,
                    RoomName.Root_Cave: RoomName.Transport_Tunnel_B,
                },
                invalid_start_rooms=[
                    RoomName.Warrior_Shrine,
                    RoomName.Arbor_Chamber,
                    RoomName.Transport_to_Chozo_Ruins_East,
                    RoomName.Landing_Site,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Transport_Tunnel_D,
                can_be_locked=True,
                doors={
                    RoomName.Great_Tree_Hall: RoomName.Transport_Tunnel_D,
                },
                invalid_start_rooms=[RoomName.Warrior_Shrine],
            ),
            BlastShieldRegion(
                name=RoomName.Transport_Tunnel_E,
                can_be_locked=True,
                doors={
                    RoomName.Great_Tree_Hall: RoomName.Transport_Tunnel_E,
                },
                invalid_start_rooms=[RoomName.Warrior_Shrine],
            ),
            BlastShieldRegion(
                name=RoomName.Great_Tree_Chamber,
                doors={RoomName.Great_Tree_Hall: RoomName.Great_Tree_Chamber},
            ),
        ],
    )


def __get_phendrana_region():
    return BlastShieldArea(
        area=MetroidPrimeArea.Phendrana_Drifts,
        regions=[
            BlastShieldRegion(
                name=RoomName.Shoreline_Entrance,
                doors={RoomName.Phendrana_Shorelines: RoomName.Shoreline_Entrance},
            ),
            BlastShieldRegion(
                name=RoomName.Temple_Entryway,
                doors={RoomName.Phendrana_Shorelines: RoomName.Temple_Entryway},
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Ice_Ruins_East,
                can_be_locked=True,
                doors={
                    RoomName.Ice_Ruins_Access: RoomName.Phendrana_Shorelines,
                    RoomName.Plaza_Walkway: RoomName.Phendrana_Shorelines,
                },
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Ice_Ruins_West,
                doors={
                    RoomName.Phendrana_Shorelines: RoomName.Ruins_Entryway,
                    RoomName.Ruins_Entryway: RoomName.Ice_Ruins_West,
                },
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Phendrana_Canyon,
                doors={RoomName.Ice_Ruins_West: RoomName.Canyon_Entryway},
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Ruined_Courtyard,
                doors={RoomName.Ice_Ruins_West: RoomName.Courtyard_Entryway},
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Quarantine_Access,
                can_be_locked=True,
                doors={RoomName.Ruined_Courtyard: RoomName.Quarantine_Access},
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Specimen_Storage,
                can_be_locked=True,
                doors={RoomName.Ruined_Courtyard: RoomName.Specimen_Storage},
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Quarantine_Cave,
                can_be_locked=True,
                doors={RoomName.Quarantine_Cave: RoomName.South_Quarantine_Tunnel},
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Research_Lab_Hydra,
                can_be_locked=True,
                doors={
                    RoomName.Research_Lab_Hydra: RoomName.Observatory_Access,
                    RoomName.Observatory: RoomName.West_Tower_Entrance,
                    RoomName.Control_Tower: RoomName.East_Tower,
                    RoomName.Research_Lab_Aether: RoomName.Research_Core_Access,
                    RoomName.Research_Core: RoomName.Pike_Access,
                },
                invalid_start_rooms=[
                    RoomName.Save_Station_B,
                    RoomName.East_Tower,
                    RoomName.Quarantine_Monitor,
                ],
            ),
            BlastShieldRegion(
                name=RoomName.Transport_to_Magmoor_Caverns_South,
                doors={
                    RoomName.Transport_to_Magmoor_Caverns_South: RoomName.Transport_Access,
                },
                invalid_start_rooms=[RoomName.Quarantine_Monitor],
            ),
            BlastShieldRegion(
                name=RoomName.Frost_Cave,
                can_be_locked=True,
                doors={
                    RoomName.Frozen_Pike: RoomName.Frost_Cave_Access,
                    RoomName.Frost_Cave: RoomName.Upper_Edge_Tunnel,
                    RoomName.Hunter_Cave: RoomName.Lower_Edge_Tunnel,
                },
                invalid_start_rooms=[RoomName.Quarantine_Monitor],
            ),
        ],
    )


def __get_magmoor_region():
    return BlastShieldArea(
        area=MetroidPrimeArea.Magmoor_Caverns,
        regions=[
            BlastShieldRegion(
                name=RoomName.Lava_Lake,
                doors={
                    RoomName.Transport_to_Chozo_Ruins_North: RoomName.Burning_Trail,
                    RoomName.Lake_Tunnel: RoomName.Lava_Lake,
                },
                invalid_start_rooms=[RoomName.Warrior_Shrine],
            ),
            BlastShieldRegion(
                name=RoomName.Pit_Tunnel,
                doors={RoomName.Lava_Lake: RoomName.Pit_Tunnel},
                invalid_start_rooms=[RoomName.Warrior_Shrine],
            ),
            BlastShieldRegion(
                name=RoomName.Storage_Cavern,
                doors={RoomName.Triclops_Pit: RoomName.Storage_Cavern},
                invalid_start_rooms=[RoomName.Warrior_Shrine],
            ),
            BlastShieldRegion(
                name=RoomName.Transport_to_Phendrana_Drifts_North,
                doors={
                    RoomName.Monitor_Station: RoomName.Transport_Tunnel_A,
                    RoomName.Transport_to_Phendrana_Drifts_North: RoomName.Transport_Tunnel_A,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Warrior_Shrine,
                doors={RoomName.Monitor_Station: RoomName.Warrior_Shrine},
                invalid_start_rooms=[RoomName.Warrior_Shrine],
            ),
            BlastShieldRegion(
                name=RoomName.Transport_Tunnel_B,
                doors={RoomName.Fiery_Shores: RoomName.Transport_Tunnel_B},
                invalid_start_rooms=[RoomName.Warrior_Shrine],
            ),
            BlastShieldRegion(
                name=RoomName.Geothermal_Core,
                doors={
                    RoomName.Transport_to_Tallon_Overworld_West: RoomName.Twin_Fires_Tunnel,
                    RoomName.Twin_Fires_Tunnel: RoomName.Twin_Fires,
                    RoomName.North_Core_Tunnel: RoomName.Geothermal_Core,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Magmoor_Workstation,
                doors={
                    RoomName.South_Core_Tunnel: RoomName.Magmoor_Workstation,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Transport_Tunnel_C,
                doors={RoomName.Magmoor_Workstation: RoomName.Transport_Tunnel_C},
            ),
            BlastShieldRegion(
                name=RoomName.Workstation_Tunnel,
                doors={RoomName.Magmoor_Workstation: RoomName.Workstation_Tunnel},
            ),
        ],
    )


def __get_phazon_region():
    return BlastShieldArea(
        area=MetroidPrimeArea.Phazon_Mines,
        regions=[
            BlastShieldRegion(
                name=RoomName.Quarry_Access,
                doors={
                    RoomName.Main_Quarry: RoomName.Quarry_Access,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Waste_Disposal,
                doors={RoomName.Main_Quarry: RoomName.Waste_Disposal},
            ),
            BlastShieldRegion(
                name=RoomName.Elite_Research,
                doors={
                    RoomName.Main_Quarry: RoomName.Security_Access_A,
                    RoomName.Security_Access_B: RoomName.Elite_Research,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Ore_Processing,
                can_be_locked=True,
                doors={RoomName.Research_Access: RoomName.Ore_Processing},
            ),
            BlastShieldRegion(
                name=RoomName.Elevator_A,
                can_be_locked=True,
                doors={
                    RoomName.Ore_Processing: RoomName.Elevator_Access_A,
                    RoomName.Elevator_Access_A: RoomName.Elevator_A,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Storage_Depot_B,
                doors={RoomName.Ore_Processing: RoomName.Storage_Depot_B},
            ),
            BlastShieldRegion(
                name=RoomName.Elite_Control,
                can_be_locked=True,
                doors={RoomName.Elite_Control_Access: RoomName.Elite_Control},
            ),
            BlastShieldRegion(
                name=RoomName.Maintenance_Tunnel,
                can_be_locked=True,
                doors={RoomName.Elite_Control: RoomName.Maintenance_Tunnel},
            ),
            BlastShieldRegion(
                name=RoomName.Ventilation_Shaft,
                can_be_locked=True,
                doors={RoomName.Elite_Control: RoomName.Ventilation_Shaft},
            ),
            BlastShieldRegion(
                name=RoomName.Metroid_Quarantine_A,
                can_be_locked=True,
                doors={
                    RoomName.Central_Dynamo: RoomName.Quarantine_Access_A,
                    RoomName.Quarantine_Access_A: RoomName.Metroid_Quarantine_A,
                    RoomName.Elevator_Access_B: RoomName.Metroid_Quarantine_A,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Metroid_Quarantine_B,
                can_be_locked=True,
                doors={
                    RoomName.Fungal_Hall_Access: RoomName.Fungal_Hall_A,
                    RoomName.Fungal_Hall_A: RoomName.Phazon_Mining_Tunnel,
                    RoomName.Fungal_Hall_B: RoomName.Quarantine_Access_B,
                    RoomName.Metroid_Quarantine_B: RoomName.Elite_Quarters_Access,
                },
            ),
            BlastShieldRegion(
                name=RoomName.Elite_Quarters,
                can_be_locked=True,
                doors={RoomName.Elite_Quarters: RoomName.Processing_Center_Access},
            ),
            BlastShieldRegion(
                name=RoomName.Phazon_Processing_Center,
                can_be_locked=True,
                doors={RoomName.Phazon_Processing_Center: RoomName.Maintenance_Tunnel},
            ),
        ],
    )


def get_valid_blast_shield_regions_by_area(
    world: "MetroidPrimeWorld", area: MetroidPrimeArea
) -> List[BlastShieldRegion]:
    region: BlastShieldArea
    if area == MetroidPrimeArea.Chozo_Ruins:
        region = __get_chozo_region()
    elif area == MetroidPrimeArea.Tallon_Overworld:
        region = __get_tallon_region()
    elif area == MetroidPrimeArea.Phendrana_Drifts:
        region = __get_phendrana_region()
    elif area == MetroidPrimeArea.Magmoor_Caverns:
        region = __get_magmoor_region()
    else:
        region = __get_phazon_region()

    if not world.starting_room_data:
        return region.regions
    if world.starting_room_data.area != area:
        return region.regions

    return [
        blast_shield_region
        for blast_shield_region in region.regions
        if blast_shield_region.invalid_start_rooms is None
        or RoomName(world.starting_room_data.name)
        not in blast_shield_region.invalid_start_rooms
    ]
