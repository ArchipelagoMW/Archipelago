from typing import Dict, Optional, TYPE_CHECKING

from BaseClasses import Entrance, ItemClassification, Region
from .items import LingoItem
from .locations import LingoLocation
from .player_logic import LingoPlayerLogic
from .rules import lingo_can_use_entrance, lingo_can_use_pilgrimage, make_location_lambda
from .static_logic import ALL_ROOMS, PAINTINGS, Room, RoomAndDoor

if TYPE_CHECKING:
    from . import LingoWorld


def create_region(room: Room, world: "LingoWorld", player_logic: LingoPlayerLogic) -> Region:
    new_region = Region(room.name, world.player, world.multiworld)
    for location in player_logic.locations_by_room.get(room.name, {}):
        new_location = LingoLocation(world.player, location.name, location.code, new_region)
        new_location.access_rule = make_location_lambda(location, world, player_logic)
        new_region.locations.append(new_location)
        if location.name in player_logic.event_loc_to_item:
            event_name = player_logic.event_loc_to_item[location.name]
            event_item = LingoItem(event_name, ItemClassification.progression, None, world.player)
            new_location.place_locked_item(event_item)

    return new_region


def handle_pilgrim_room(regions: Dict[str, Region], world: "LingoWorld", player_logic: LingoPlayerLogic) -> None:
    target_region = regions["Pilgrim Antechamber"]
    source_region = regions["Outside The Agreeable"]
    source_region.connect(
        target_region,
        "Pilgrimage",
        lambda state: lingo_can_use_pilgrimage(state, world, player_logic))


def connect_entrance(regions: Dict[str, Region], source_region: Region, target_region: Region, description: str,
                     door: Optional[RoomAndDoor], world: "LingoWorld", player_logic: LingoPlayerLogic):
    connection = Entrance(world.player, description, source_region)
    connection.access_rule = lambda state: lingo_can_use_entrance(state, target_region.name, door, world, player_logic)

    source_region.exits.append(connection)
    connection.connect(target_region)

    if door is not None:
        effective_room = target_region.name if door.room is None else door.room
        if door.door not in player_logic.item_by_door.get(effective_room, {}):
            for region in player_logic.calculate_door_requirements(effective_room, door.door, world).rooms:
                world.multiworld.register_indirect_condition(regions[region], connection)


def connect_painting(regions: Dict[str, Region], warp_enter: str, warp_exit: str, world: "LingoWorld",
                     player_logic: LingoPlayerLogic) -> None:
    source_painting = PAINTINGS[warp_enter]
    target_painting = PAINTINGS[warp_exit]

    target_region = regions[target_painting.room]
    source_region = regions[source_painting.room]

    entrance_name = f"{source_painting.room} to {target_painting.room} ({source_painting.id} Painting)"
    connect_entrance(regions, source_region, target_region, entrance_name, source_painting.required_door, world,
                     player_logic)


def create_regions(world: "LingoWorld", player_logic: LingoPlayerLogic) -> None:
    regions = {
        "Menu": Region("Menu", world.player, world.multiworld)
    }

    painting_shuffle = world.options.shuffle_paintings
    early_color_hallways = world.options.early_color_hallways

    # Instantiate all rooms as regions with their locations first.
    for room in ALL_ROOMS:
        regions[room.name] = create_region(room, world, player_logic)

    # Connect all created regions now that they exist.
    for room in ALL_ROOMS:
        for entrance in room.entrances:
            # Don't use the vanilla painting connections if we are shuffling paintings.
            if entrance.painting and painting_shuffle:
                continue

            entrance_name = f"{entrance.room} to {room.name}"
            if entrance.door is not None:
                if entrance.door.room is not None:
                    entrance_name += f" (through {entrance.door.room} - {entrance.door.door})"
                else:
                    entrance_name += f" (through {room.name} - {entrance.door.door})"

            connect_entrance(regions, regions[entrance.room], regions[room.name], entrance_name, entrance.door, world,
                             player_logic)

    handle_pilgrim_room(regions, world, player_logic)

    if early_color_hallways:
        regions["Starting Room"].connect(regions["Outside The Undeterred"], "Early Color Hallways")

    if painting_shuffle:
        for warp_enter, warp_exit in player_logic.painting_mapping.items():
            connect_painting(regions, warp_enter, warp_exit, world, player_logic)

    world.multiworld.regions += regions.values()
