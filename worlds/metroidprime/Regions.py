import typing

from .Logic import (
    can_ice_beam,
    can_missile,
    can_phazon,
    can_plasma_beam,
    can_power_beam,
    can_scan,
    can_super_missile,
    can_thermal,
    can_wave_beam,
    can_xray,
    has_required_artifact_count,
)
from .LogicCombat import can_combat_prime, can_combat_ridley
from .data.RoomNames import RoomName
from BaseClasses import CollectionState, Region

if typing.TYPE_CHECKING:
    from . import MetroidPrimeWorld


def create_regions(world: "MetroidPrimeWorld", final_boss_selection: int):
    # create all regions and populate with locations
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    for area_data in world.game_region_data.values():
        area_data.create_world_region(world)

    impact_crater = Region("Impact Crater", world.player, world.multiworld)
    world.multiworld.regions.append(impact_crater)

    mission_complete = Region("Mission Complete", world.player, world.multiworld)
    world.multiworld.regions.append(mission_complete)

    assert world.starting_room_data and world.starting_room_data.name
    starting_room = world.get_region(world.starting_room_data.name)
    menu.connect(starting_room, "Starting Room")

    def can_access_elevator(world: "MetroidPrimeWorld", state: CollectionState) -> bool:
        if world.options.pre_scan_elevators:
            return True
        return can_scan(world, state)

    for mappings in world.elevator_mapping.values():
        for elevator, target in mappings.items():
            source = world.get_region(elevator)
            destination = world.get_region(target)
            source.connect(
                destination, elevator, lambda state: can_access_elevator(world, state)
            )

    artifact_temple = world.get_region(
        RoomName.Artifact_Temple.value
    )

    if final_boss_selection == 0 or final_boss_selection == 2:
        artifact_temple.connect(
            impact_crater,
            "Crater Access",
            lambda state: (
                can_missile(world, state)
                and has_required_artifact_count(world, state)
                and can_combat_prime(world, state)
                and can_combat_ridley(world, state)
                and can_phazon(world, state)
                and can_plasma_beam(world, state)
                and can_wave_beam(world, state)
                and can_ice_beam(world, state)
                and can_power_beam(world, state)
                and can_xray(world, state, True)
                and can_thermal(world, state, True)
            ),
        )
        impact_crater.connect(mission_complete, "Mission Complete")

    elif final_boss_selection == 1:
        artifact_temple.connect(
            mission_complete,
            "Mission Complete",
            lambda state: can_missile(world, state)
            and has_required_artifact_count(world, state)
            and (can_plasma_beam(world, state) or can_super_missile(world, state))
            and can_combat_ridley(world, state),
        )
    elif final_boss_selection == 3:
        artifact_temple.connect(
            mission_complete,
            "Mission Complete",
            lambda state: (
                can_missile(world, state) and has_required_artifact_count(world, state)
            ),
        )
