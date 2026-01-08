from collections import defaultdict
import copy
from typing import TYPE_CHECKING, Dict, List

from .RoomNames import RoomName
from .RoomData import MetroidPrimeArea

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld


default_elevator_mappings = {
    MetroidPrimeArea.Tallon_Overworld.value: {
        RoomName.Transport_to_Chozo_Ruins_West.value: RoomName.Transport_to_Tallon_Overworld_North.value,
        RoomName.Transport_to_Magmoor_Caverns_East.value: RoomName.Transport_to_Tallon_Overworld_West.value,
        RoomName.Transport_to_Chozo_Ruins_East.value: RoomName.Transport_to_Tallon_Overworld_East.value,
        RoomName.Transport_to_Chozo_Ruins_South.value: "Chozo Ruins: "
        + RoomName.Transport_to_Tallon_Overworld_South.value,
        RoomName.Transport_to_Phazon_Mines_East.value: "Phazon Mines: "
        + RoomName.Transport_to_Tallon_Overworld_South.value,
    },
    MetroidPrimeArea.Chozo_Ruins.value: {
        RoomName.Transport_to_Tallon_Overworld_North.value: RoomName.Transport_to_Chozo_Ruins_West.value,
        RoomName.Transport_to_Magmoor_Caverns_North.value: RoomName.Transport_to_Chozo_Ruins_North.value,
        RoomName.Transport_to_Tallon_Overworld_East.value: RoomName.Transport_to_Chozo_Ruins_East.value,
        "Chozo Ruins: "
        + RoomName.Transport_to_Tallon_Overworld_South.value: RoomName.Transport_to_Chozo_Ruins_South.value,
    },
    MetroidPrimeArea.Magmoor_Caverns.value: {
        RoomName.Transport_to_Chozo_Ruins_North.value: RoomName.Transport_to_Magmoor_Caverns_North.value,
        RoomName.Transport_to_Phendrana_Drifts_North.value: RoomName.Transport_to_Magmoor_Caverns_West.value,
        RoomName.Transport_to_Tallon_Overworld_West.value: RoomName.Transport_to_Magmoor_Caverns_East.value,
        RoomName.Transport_to_Phendrana_Drifts_South.value: "Phendrana Drifts: "
        + RoomName.Transport_to_Magmoor_Caverns_South.value,
        RoomName.Transport_to_Phazon_Mines_West.value: "Phazon Mines: "
        + RoomName.Transport_to_Magmoor_Caverns_South.value,
    },
    MetroidPrimeArea.Phendrana_Drifts.value: {
        RoomName.Transport_to_Magmoor_Caverns_West.value: RoomName.Transport_to_Phendrana_Drifts_North.value,
        "Phendrana Drifts: "
        + RoomName.Transport_to_Magmoor_Caverns_South.value: RoomName.Transport_to_Phendrana_Drifts_South.value,
    },
    MetroidPrimeArea.Phazon_Mines.value: {
        "Phazon Mines: "
        + RoomName.Transport_to_Tallon_Overworld_South.value: RoomName.Transport_to_Phazon_Mines_East.value,
        "Phazon Mines: "
        + RoomName.Transport_to_Magmoor_Caverns_South.value: RoomName.Transport_to_Phazon_Mines_West.value,
    },
}

ELEVATOR_USEFUL_NAMES: Dict[str, str] = {
    RoomName.Transport_to_Chozo_Ruins_West.value: "Tallon Overworld North (Tallon Canyon)",
    RoomName.Transport_to_Chozo_Ruins_East.value: "Tallon Overworld East (Frigate Crash Site)",
    RoomName.Transport_to_Magmoor_Caverns_East.value: "Tallon Overworld West (Root Cave)",
    RoomName.Transport_to_Chozo_Ruins_South.value: "Tallon Overworld South (Great Tree Hall, Upper)",
    RoomName.Transport_to_Phazon_Mines_East.value: "Tallon Overworld South (Great Tree Hall, Lower)",
    RoomName.Transport_to_Tallon_Overworld_North.value: "Chozo Ruins West (Main Plaza)",
    RoomName.Transport_to_Magmoor_Caverns_North.value: "Chozo Ruins North (Sun Tower)",
    RoomName.Transport_to_Tallon_Overworld_East.value: "Chozo Ruins East (Reflecting Pool, Save Station)",
    "Chozo Ruins: "
    + RoomName.Transport_to_Tallon_Overworld_South.value: "Chozo Ruins South (Reflecting Pool, Far End)",
    RoomName.Transport_to_Chozo_Ruins_North.value: "Magmoor Caverns North (Lava Lake)",
    RoomName.Transport_to_Phendrana_Drifts_North.value: "Magmoor Caverns West (Monitor Station)",
    RoomName.Transport_to_Tallon_Overworld_West.value: "Magmoor Caverns East (Twin Fires)",
    RoomName.Transport_to_Phazon_Mines_West.value: "Magmoor Caverns South (Magmoor Workstation, Debris)",
    RoomName.Transport_to_Phendrana_Drifts_South.value: "Magmoor Caverns South (Magmoor Workstation, Save Station)",
    RoomName.Transport_to_Magmoor_Caverns_West.value: "Phendrana Drifts North (Phendrana Shorelines)",
    "Phendrana Drifts: "
    + RoomName.Transport_to_Magmoor_Caverns_South.value: "Phendrana Drifts South (Quarantine Cave)",
    "Phazon Mines: "
    + RoomName.Transport_to_Tallon_Overworld_South.value: "Phazon Mines East (Main Quarry)",
    "Phazon Mines: "
    + RoomName.Transport_to_Magmoor_Caverns_South.value: "Phazon Mines West (Phazon Processing Center)",
}


def temple_dest(boss: int) -> str:
    if boss == 0 or boss == 2:
        return "Crater Entry Point"
    return "Credits"


# Names of the transports that the config json expects
transport_names_to_room_names: Dict[str, str] = {
    "Tallon Overworld North (Tallon Canyon)": RoomName.Transport_to_Chozo_Ruins_West.value,
    "Tallon Overworld West (Root Cave)": RoomName.Transport_to_Magmoor_Caverns_East.value,
    "Tallon Overworld East (Frigate Crash Site)": RoomName.Transport_to_Chozo_Ruins_East.value,
    "Tallon Overworld South (Great Tree Hall, Upper)": RoomName.Transport_to_Chozo_Ruins_South.value,
    "Tallon Overworld South (Great Tree Hall, Lower)": RoomName.Transport_to_Phazon_Mines_East.value,
    "Chozo Ruins West (Main Plaza)": RoomName.Transport_to_Tallon_Overworld_North.value,
    "Chozo Ruins North (Sun Tower)": RoomName.Transport_to_Magmoor_Caverns_North.value,
    "Chozo Ruins East (Reflecting Pool, Save Station)": RoomName.Transport_to_Tallon_Overworld_East.value,
    "Chozo Ruins South (Reflecting Pool, Far End)": "Chozo Ruins: "
    + RoomName.Transport_to_Tallon_Overworld_South.value,
    "Magmoor Caverns North (Lava Lake)": RoomName.Transport_to_Chozo_Ruins_North.value,
    "Magmoor Caverns West (Monitor Station)": RoomName.Transport_to_Phendrana_Drifts_North.value,
    "Magmoor Caverns East (Twin Fires)": RoomName.Transport_to_Tallon_Overworld_West.value,
    "Magmoor Caverns South (Magmoor Workstation, Save Station)": RoomName.Transport_to_Phendrana_Drifts_South.value,
    "Magmoor Caverns South (Magmoor Workstation, Debris)": RoomName.Transport_to_Phazon_Mines_West.value,
    "Phendrana Drifts North (Phendrana Shorelines)": RoomName.Transport_to_Magmoor_Caverns_West.value,
    "Phendrana Drifts South (Quarantine Cave)": "Phendrana Drifts: "
    + RoomName.Transport_to_Magmoor_Caverns_South.value,
    "Phazon Mines East (Main Quarry)": "Phazon Mines: "
    + RoomName.Transport_to_Tallon_Overworld_South.value,
    "Phazon Mines West (Phazon Processing Center)": "Phazon Mines: "
    + RoomName.Transport_to_Magmoor_Caverns_South.value,
}


def get_transport_name_by_room_name(room_name: str) -> str:
    for transport_name, room in transport_names_to_room_names.items():
        if room == room_name:
            return transport_name
    return room_name


def get_room_name_by_transport_name(transport_name: str) -> str:
    return transport_names_to_room_names.get(transport_name, transport_name)


def get_transport_data(world: "MetroidPrimeWorld") -> Dict[str, Dict[str, str]]:
    mapping = world.elevator_mapping
    data: Dict[str, Dict[str, str]] = {}
    for area in world.elevator_mapping.keys():
        data[area] = {}
        for source, dest in mapping[area].items():
            data[area][get_transport_name_by_room_name(source)] = (
                get_transport_name_by_room_name(dest)
            )

    data[MetroidPrimeArea.Tallon_Overworld.value]["Artifact Temple"] = temple_dest(
        world.options.final_bosses.value
    )
    return data


def get_region_by_elevator_name(elevator_name: str) -> str:
    for region, elevators in default_elevator_mappings.items():
        if elevator_name in elevators:
            return region
    raise ValueError(f"Could not find region for elevator {elevator_name}")


def get_random_elevator_mapping(
    world: "MetroidPrimeWorld",
) -> Dict[str, Dict[str, str]]:
    mapped_elevators: Dict[str, Dict[str, str]] = defaultdict(dict)
    available_elevators_by_region = copy.deepcopy(default_elevator_mappings)
    denied_elevators = world.starting_room_data.denied_elevators or {}

    def get_region_with_most_unshuffled_elevators() -> str:
        max_elevators = 0
        region = None
        for area, elevators in available_elevators_by_region.items():
            num_elevators = len(elevators)
            if num_elevators > max_elevators:
                max_elevators = num_elevators
                region = area
        if region is None:
            raise ValueError("No region with elevators found")
        return region

    def get_flat_list_of_available_elevators():
        elevators: List[str] = []
        for area_elevators in available_elevators_by_region.values():
            elevators.extend(area_elevators.keys())
        return elevators

    def get_random_target_region(source_region: str) -> str:
        target_regions = list(available_elevators_by_region.keys())
        target_regions.remove(source_region)
        return world.random.choice(target_regions)

    def delete_region_if_empty(region: str):
        if not available_elevators_by_region[region]:
            del available_elevators_by_region[region]

    def two_way_map_elevators(
        source_region: str,
        source_elevator: str,
        target_region: str,
        target_elevator: str,
    ):
        one_way_map_elevator(source_region, source_elevator, target_elevator)
        one_way_map_elevator(target_region, target_elevator, source_elevator)

    def one_way_map_elevator(
        source_region: str, source_elevator: str, target_elevator: str
    ):
        mapped_elevators[source_region][source_elevator] = target_elevator
        del available_elevators_by_region[source_region][source_elevator]
        delete_region_if_empty(source_region)

    # If there is an allow list for the starting room, then two way map a random set for each elevator
    if world.starting_room_data.allowed_elevators:
        for (
            source_area,
            elevators,
        ) in world.starting_room_data.allowed_elevators.items():
            for source_elevator, potential_destinations in elevators.items():
                available_options = [
                    e
                    for e in get_flat_list_of_available_elevators()
                    if e in potential_destinations
                    and get_region_by_elevator_name(e) != source_area
                ]
                destination_elevator = world.random.choice(available_options)
                target_area = get_region_by_elevator_name(destination_elevator)
                two_way_map_elevators(
                    source_area, source_elevator, target_area, destination_elevator
                )

    # Distribute denied elevators
    for source_area, elevators in denied_elevators.items():
        for source_elevator in elevators:
            destination_elevator = world.random.choice(
                [
                    e
                    for e in get_flat_list_of_available_elevators()
                    if e not in elevators[source_elevator]
                    and get_region_by_elevator_name(e) != source_area
                ]
            )
            destination_area = get_region_by_elevator_name(destination_elevator)
            two_way_map_elevators(
                source_area, source_elevator, destination_area, destination_elevator
            )

    while available_elevators_by_region:
        source_region = get_region_with_most_unshuffled_elevators()
        source_elevators = available_elevators_by_region[source_region]
        source_elevator = world.random.choice(list(source_elevators.keys()))

        target_region = get_random_target_region(source_region)
        target_elevators = available_elevators_by_region[target_region]
        target_elevator = world.random.choice(list(target_elevators.keys()))

        two_way_map_elevators(
            source_region, source_elevator, target_region, target_elevator
        )

    return mapped_elevators
