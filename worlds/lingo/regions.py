from typing import Dict, Optional, TYPE_CHECKING

from BaseClasses import Entrance, ItemClassification, Region
from .items import LingoItem
from .locations import LingoLocation
from .options import SunwarpAccess
from .player_logic import LingoPlayerLogic
from .rules import lingo_can_do_pilgrimage, lingo_can_do_pilgrimage_segment, lingo_can_use_entrance,\
    make_location_lambda
from .static_logic import ALL_ROOMS, PAINTINGS, EntranceType, Room, RoomAndDoor

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


def connect_entrance(regions: Dict[str, Region], source_region: Region, target_region: Region, description: str,
                     door: Optional[RoomAndDoor], entrance_type: EntranceType, world: "LingoWorld",
                     player_logic: LingoPlayerLogic):
    connection = Entrance(world.player, description, source_region)
    connection.access_rule = lambda state: lingo_can_use_entrance(state, target_region.name, door, entrance_type, world,
                                                                  player_logic)

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
    connect_entrance(regions, source_region, target_region, entrance_name, source_painting.required_door,
                     EntranceType.PAINTING, world, player_logic)


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
            if entrance.type == EntranceType.PAINTING and painting_shuffle:
                continue

            # Don't connect sunwarps if sunwarps are disabled.
            if entrance.type == EntranceType.SUNWARP and world.options.sunwarp_access == SunwarpAccess.option_disabled:
                continue

            entrance_name = f"{entrance.room} to {room.name}"
            if entrance.door is not None:
                if entrance.door.room is not None:
                    entrance_name += f" (through {entrance.door.room} - {entrance.door.door})"
                else:
                    entrance_name += f" (through {room.name} - {entrance.door.door})"

            effective_door = entrance.door
            if entrance.type == EntranceType.SUNWARP and world.options.sunwarp_access == SunwarpAccess.option_normal:
                effective_door = None

            connect_entrance(regions, regions[entrance.room], regions[room.name], entrance_name, effective_door,
                             entrance.type, world, player_logic)

    if world.options.enable_pilgrimage:
        # Create connections from Menu for the beginning of each pilgrimage segment.
        sunwarp_entrances = ["Crossroads", "Orange Tower Third Floor", "Outside The Initiated",
                             "Outside The Undeterred", "Color Hunt"]
        
        def connect_pilgrimage_segment(i: int):
            regions["Menu"].connect(regions[sunwarp_entrances[i]], f"Pilgrimage Part {i+1}",
                                    lambda state: lingo_can_do_pilgrimage_segment(state, i+1, world))
        
        for i in range(0, len(sunwarp_entrances)):
            connect_pilgrimage_segment(i)

        # Create the actual pilgrimage.
        regions["Hub Room"].connect(regions["Pilgrim Antechamber"], "Pilgrimage",
                                    lambda state: lingo_can_do_pilgrimage(state, world, player_logic))
    else:
        connect_entrance(regions, regions["Starting Room"], regions["Pilgrim Antechamber"], "Sun Painting",
                         RoomAndDoor("Pilgrim Antechamber", "Sun Painting"), EntranceType.PAINTING, world, player_logic)

    if early_color_hallways:
        connect_entrance(regions, regions["Starting Room"], regions["Outside The Undeterred"], "Early Color Hallways",
                         None, EntranceType.PAINTING, world, player_logic)

    if painting_shuffle:
        for warp_enter, warp_exit in player_logic.painting_mapping.items():
            connect_painting(regions, warp_enter, warp_exit, world, player_logic)

    world.multiworld.regions += regions.values()
