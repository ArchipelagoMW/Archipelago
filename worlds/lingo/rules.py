from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from .datatypes import RoomAndDoor
from .player_logic import AccessRequirements, PlayerLocation
from .static_logic import PROGRESSIVE_DOORS_BY_ROOM, PROGRESSIVE_ITEMS

if TYPE_CHECKING:
    from . import LingoWorld


def lingo_can_use_entrance(state: CollectionState, room: str, door: RoomAndDoor, world: "LingoWorld"):
    if door is None:
        return True

    effective_room = room if door.room is None else door.room
    return _lingo_can_open_door(state, effective_room, door.door, world)


def lingo_can_do_pilgrimage(state: CollectionState, world: "LingoWorld"):
    return all(_lingo_can_open_door(state, "Sunwarps", f"{i} Sunwarp", world) for i in range(1, 7))


def lingo_can_use_location(state: CollectionState, location: PlayerLocation, world: "LingoWorld"):
    return _lingo_can_satisfy_requirements(state, location.access, world)


def lingo_can_use_mastery_location(state: CollectionState, world: "LingoWorld"):
    satisfied_count = 0
    for access_req in world.player_logic.mastery_reqs:
        if _lingo_can_satisfy_requirements(state, access_req, world):
            satisfied_count += 1
    return satisfied_count >= world.options.mastery_achievements.value


def lingo_can_use_level_2_location(state: CollectionState, world: "LingoWorld"):
    counted_panels = 0
    state.update_reachable_regions(world.player)
    for region in state.reachable_regions[world.player]:
        for access_req, panel_count in world.player_logic.counting_panel_reqs.get(region.name, []):
            if _lingo_can_satisfy_requirements(state, access_req, world):
                counted_panels += panel_count
        if counted_panels >= world.options.level_2_requirement.value - 1:
            return True
    return False


def _lingo_can_satisfy_requirements(state: CollectionState, access: AccessRequirements, world: "LingoWorld"):
    for req_room in access.rooms:
        if not state.can_reach(req_room, "Region", world.player):
            return False

    for req_door in access.doors:
        if not _lingo_can_open_door(state, req_door.room, req_door.door, world):
            return False

    if len(access.colors) > 0 and world.options.shuffle_colors:
        for color in access.colors:
            if not state.has(color.capitalize(), world.player):
                return False

    if not all(state.has(item, world.player) for item in access.items):
        return False

    if not all(state.has(item, world.player, index) for item, index in access.progression.items()):
        return False

    if access.the_master and not lingo_can_use_mastery_location(state, world):
        return False

    if access.postgame and state.has("Prevent Victory", world.player):
        return False

    return True


def _lingo_can_open_door(state: CollectionState, room: str, door: str, world: "LingoWorld"):
    """
    Determines whether a door can be opened
    """
    if door not in world.player_logic.item_by_door.get(room, {}):
        return _lingo_can_satisfy_requirements(state, world.player_logic.door_reqs[room][door], world)

    item_name = world.player_logic.item_by_door[room][door]
    if item_name in PROGRESSIVE_ITEMS:
        progression = PROGRESSIVE_DOORS_BY_ROOM[room][door]
        return state.has(item_name, world.player, progression.index)

    return state.has(item_name, world.player)


def make_location_lambda(location: PlayerLocation, world: "LingoWorld"):
    if location.name == world.player_logic.mastery_location:
        return lambda state: lingo_can_use_mastery_location(state, world)

    if world.options.level_2_requirement > 1\
            and (location.name == "Second Room - ANOTHER TRY" or location.name == world.player_logic.level_2_location):
        return lambda state: lingo_can_use_level_2_location(state, world)

    return lambda state: lingo_can_use_location(state, location, world)
