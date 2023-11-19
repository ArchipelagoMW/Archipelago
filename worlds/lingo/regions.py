from typing import Dict, TYPE_CHECKING

from BaseClasses import ItemClassification, Region
from .items import LingoItem
from .locations import LingoLocation
from .player_logic import LingoPlayerLogic
from .rules import lingo_can_use_entrance, lingo_can_use_pilgrimage, make_location_lambda
from .static_logic import ALL_ROOMS, PAINTINGS, Room

if TYPE_CHECKING:
    from . import LingoWorld


def create_region(room: Room, world: "LingoWorld", player_logic: LingoPlayerLogic) -> Region:
    new_region = Region(room.name, world.player, world.multiworld)
    for location in player_logic.LOCATIONS_BY_ROOM.get(room.name, {}):
        new_location = LingoLocation(world.player, location.name, location.code, new_region)
        new_location.access_rule = make_location_lambda(location, room.name, world, player_logic)
        new_region.locations.append(new_location)
        if location.name in player_logic.EVENT_LOC_TO_ITEM:
            event_name = player_logic.EVENT_LOC_TO_ITEM[location.name]
            event_item = LingoItem(event_name, ItemClassification.progression, None, world.player)
            new_location.place_locked_item(event_item)

    return new_region


def handle_pilgrim_room(regions: Dict[str, Region], world: "LingoWorld", player_logic: LingoPlayerLogic) -> None:
    target_region = regions["Pilgrim Antechamber"]
    source_region = regions["Outside The Agreeable"]
    source_region.connect(
        target_region,
        "Pilgrimage",
        lambda state: lingo_can_use_pilgrimage(state, world.player, player_logic))


def connect_painting(regions: Dict[str, Region], warp_enter: str, warp_exit: str, world: "LingoWorld",
                     player_logic: LingoPlayerLogic) -> None:
    source_painting = PAINTINGS[warp_enter]
    target_painting = PAINTINGS[warp_exit]

    target_region = regions[target_painting.room]
    source_region = regions[source_painting.room]
    source_region.connect(
        target_region,
        f"{source_painting.room} to {target_painting.room} ({source_painting.id} Painting)",
        lambda state: lingo_can_use_entrance(state, target_painting.room, source_painting.required_door, world.player,
                                             player_logic))


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

            regions[entrance.room].connect(
                regions[room.name], entrance_name,
                lambda state, r=room, e=entrance: lingo_can_use_entrance(state, r.name, e.door, world.player,
                                                                         player_logic))

    handle_pilgrim_room(regions, world, player_logic)

    if early_color_hallways:
        regions["Starting Room"].connect(regions["Outside The Undeterred"], "Early Color Hallways")

    if painting_shuffle:
        for warp_enter, warp_exit in player_logic.PAINTING_MAPPING.items():
            connect_painting(regions, warp_enter, warp_exit, world, player_logic)

    world.multiworld.regions += regions.values()
