from typing import Dict, Optional, TYPE_CHECKING

from BaseClasses import Entrance, ItemClassification, Region
from .datatypes import EntranceType, Room, RoomAndDoor
from .items import LingoItem
from .locations import LingoLocation
from .options import SunwarpAccess
from .rules import lingo_can_do_pilgrimage, lingo_can_use_entrance, make_location_lambda
from .static_logic import ALL_ROOMS, PAINTINGS

if TYPE_CHECKING:
    from . import LingoWorld


def create_region(room: Room, world: "LingoWorld") -> Region:
    new_region = Region(room.name, world.player, world.multiworld)
    for location in world.player_logic.locations_by_room.get(room.name, {}):
        new_location = LingoLocation(world.player, location.name, location.code, new_region)
        new_location.access_rule = make_location_lambda(location, world)
        new_region.locations.append(new_location)
        if location.name in world.player_logic.event_loc_to_item:
            event_name = world.player_logic.event_loc_to_item[location.name]
            event_item = LingoItem(event_name, ItemClassification.progression, None, world.player)
            new_location.place_locked_item(event_item)

    return new_region


def is_acceptable_pilgrimage_entrance(entrance_type: EntranceType, world: "LingoWorld") -> bool:
    allowed_entrance_types = EntranceType.NORMAL

    if world.options.pilgrimage_allows_paintings:
        allowed_entrance_types |= EntranceType.PAINTING

    if world.options.pilgrimage_allows_roof_access:
        allowed_entrance_types |= EntranceType.CROSSROADS_ROOF_ACCESS

    return bool(entrance_type & allowed_entrance_types)


def connect_entrance(regions: Dict[str, Region], source_region: Region, target_region: Region, description: str,
                     door: Optional[RoomAndDoor], entrance_type: EntranceType, pilgrimage: bool, world: "LingoWorld"):
    connection = Entrance(world.player, description, source_region)
    connection.access_rule = lambda state: lingo_can_use_entrance(state, target_region.name, door, world)

    source_region.exits.append(connection)
    connection.connect(target_region)

    if door is not None:
        effective_room = target_region.name if door.room is None else door.room
        if door.door not in world.player_logic.item_by_door.get(effective_room, {}):
            access_reqs = world.player_logic.calculate_door_requirements(effective_room, door.door, world)
            for region in access_reqs.rooms:
                world.multiworld.register_indirect_condition(regions[region], connection)

            # This pretty much only applies to Orange Tower Sixth Floor -> Orange Tower Basement.
            if access_reqs.the_master:
                for mastery_req in world.player_logic.mastery_reqs:
                    for region in mastery_req.rooms:
                        world.multiworld.register_indirect_condition(regions[region], connection)
    
    if not pilgrimage and world.options.enable_pilgrimage and is_acceptable_pilgrimage_entrance(entrance_type, world)\
            and source_region.name != "Menu":
        for part in range(1, 6):
            pilgrimage_descriptor = f" (Pilgrimage Part {part})"
            pilgrim_source_region = regions[f"{source_region.name}{pilgrimage_descriptor}"]
            pilgrim_target_region = regions[f"{target_region.name}{pilgrimage_descriptor}"]

            effective_door = door
            if effective_door is not None:
                effective_room = target_region.name if door.room is None else door.room
                effective_door = RoomAndDoor(effective_room, door.door)

            connect_entrance(regions, pilgrim_source_region, pilgrim_target_region,
                             f"{description}{pilgrimage_descriptor}", effective_door, entrance_type, True, world)


def connect_painting(regions: Dict[str, Region], warp_enter: str, warp_exit: str, world: "LingoWorld") -> None:
    source_painting = PAINTINGS[warp_enter]
    target_painting = PAINTINGS[warp_exit]

    target_region = regions[target_painting.room]
    source_region = regions[source_painting.room]

    entrance_name = f"{source_painting.room} to {target_painting.room} ({source_painting.id} Painting)"
    connect_entrance(regions, source_region, target_region, entrance_name, source_painting.required_door,
                     EntranceType.PAINTING, False, world)


def create_regions(world: "LingoWorld") -> None:
    regions = {
        "Menu": Region("Menu", world.player, world.multiworld)
    }

    painting_shuffle = world.options.shuffle_paintings
    early_color_hallways = world.options.early_color_hallways

    # Instantiate all rooms as regions with their locations first.
    for room in ALL_ROOMS:
        regions[room.name] = create_region(room, world)

        if world.options.enable_pilgrimage:
            for part in range(1, 6):
                pilgrimage_region_name = f"{room.name} (Pilgrimage Part {part})"
                regions[pilgrimage_region_name] = Region(pilgrimage_region_name, world.player, world.multiworld)

    # Connect all created regions now that they exist.
    allowed_entrance_types = EntranceType.NORMAL | EntranceType.WARP | EntranceType.CROSSROADS_ROOF_ACCESS

    if not painting_shuffle:
        # Don't use the vanilla painting connections if we are shuffling paintings.
        allowed_entrance_types |= EntranceType.PAINTING

    if world.options.sunwarp_access != SunwarpAccess.option_disabled and not world.options.shuffle_sunwarps:
        # Don't connect sunwarps if sunwarps are disabled or if we're shuffling sunwarps.
        allowed_entrance_types |= EntranceType.SUNWARP

    for room in ALL_ROOMS:
        for entrance in room.entrances:
            effective_entrance_type = entrance.type & allowed_entrance_types
            if not effective_entrance_type:
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
                             effective_entrance_type, False, world)

    if world.options.enable_pilgrimage:
        # Connect the start of the pilgrimage. We check for all sunwarp items here.
        pilgrim_start_from = regions[world.player_logic.sunwarp_entrances[0]]
        pilgrim_start_to = regions[f"{world.player_logic.sunwarp_exits[0]} (Pilgrimage Part 1)"]

        if world.options.sunwarp_access >= SunwarpAccess.option_unlock:
            pilgrim_start_from.connect(pilgrim_start_to, f"Pilgrimage Part 1",
                                       lambda state: lingo_can_do_pilgrimage(state, world))
        else:
            pilgrim_start_from.connect(pilgrim_start_to, f"Pilgrimage Part 1")

        # Create connections between each segment of the pilgrimage.
        for i in range(1, 6):
            from_room = f"{world.player_logic.sunwarp_entrances[i]} (Pilgrimage Part {i})"
            to_room = f"{world.player_logic.sunwarp_exits[i]} (Pilgrimage Part {i+1})"
            if i == 5:
                to_room = "Pilgrim Antechamber"

            regions[from_room].connect(regions[to_room], f"Pilgrimage Part {i+1}")
    else:
        connect_entrance(regions, regions["Starting Room"], regions["Pilgrim Antechamber"], "Sun Painting",
                         RoomAndDoor("Pilgrim Antechamber", "Sun Painting"), EntranceType.PAINTING, False, world)

    if early_color_hallways:
        connect_entrance(regions, regions["Starting Room"], regions["Color Hallways"], "Early Color Hallways",
                         None, EntranceType.PAINTING, False, world)

    if painting_shuffle:
        for warp_enter, warp_exit in world.player_logic.painting_mapping.items():
            connect_painting(regions, warp_enter, warp_exit, world)

    if world.options.shuffle_sunwarps:
        for i in range(0, 6):
            if world.options.sunwarp_access == SunwarpAccess.option_normal:
                effective_door = None
            else:
                effective_door = RoomAndDoor("Sunwarps", f"{i + 1} Sunwarp")

            source_region = regions[world.player_logic.sunwarp_entrances[i]]
            target_region = regions[world.player_logic.sunwarp_exits[i]]

            entrance_name = f"{source_region.name} to {target_region.name} ({i + 1} Sunwarp)"
            connect_entrance(regions, source_region, target_region, entrance_name, effective_door, EntranceType.SUNWARP,
                             False, world)

    world.multiworld.regions += regions.values()
