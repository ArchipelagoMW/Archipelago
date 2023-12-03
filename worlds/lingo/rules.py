from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from .player_logic import AccessRequirements, LingoPlayerLogic, PlayerLocation
from .static_logic import PROGRESSION_BY_ROOM, PROGRESSIVE_ITEMS, RoomAndDoor

if TYPE_CHECKING:
    from . import LingoWorld


def lingo_can_use_entrance(state: CollectionState, room: str, door: RoomAndDoor, world: "LingoWorld",
                           player_logic: LingoPlayerLogic):
    if door is None:
        return True

    effective_room = room if door.room is None else door.room
    return _lingo_can_open_door(state, effective_room, door.door, world, player_logic)


def lingo_can_use_pilgrimage(state: CollectionState, world: "LingoWorld", player_logic: LingoPlayerLogic):
    fake_pilgrimage = [
        ["Second Room", "Exit Door"], ["Crossroads", "Tower Entrance"],
        ["Orange Tower Fourth Floor", "Hot Crusts Door"], ["Outside The Initiated", "Shortcut to Hub Room"],
        ["Orange Tower First Floor", "Shortcut to Hub Room"], ["Directional Gallery", "Shortcut to The Undeterred"],
        ["Orange Tower First Floor", "Salt Pepper Door"], ["Hub Room", "Crossroads Entrance"],
        ["Champion's Rest", "Shortcut to The Steady"], ["The Bearer", "Shortcut to The Bold"],
        ["Art Gallery", "Exit"], ["The Tenacious", "Shortcut to Hub Room"],
        ["Outside The Agreeable", "Tenacious Entrance"]
    ]
    for entrance in fake_pilgrimage:
        if not _lingo_can_open_door(state, entrance[0], entrance[1], world, player_logic):
            return False

    return True


def lingo_can_use_location(state: CollectionState, location: PlayerLocation, world: "LingoWorld",
                           player_logic: LingoPlayerLogic):
    return _lingo_can_satisfy_requirements(state, location.access, world, player_logic)


def lingo_can_use_mastery_location(state: CollectionState, world: "LingoWorld", player_logic: LingoPlayerLogic):
    satisfied_count = 0
    for access_req in player_logic.mastery_reqs:
        if _lingo_can_satisfy_requirements(state, access_req, world, player_logic):
            satisfied_count += 1
    return satisfied_count >= world.options.mastery_achievements.value


def lingo_can_use_level_2_location(state: CollectionState, world: "LingoWorld", player_logic: LingoPlayerLogic):
    counted_panels = 0
    state.update_reachable_regions(world.player)
    for region in state.reachable_regions[world.player]:
        for access_req, panel_count in player_logic.counting_panel_reqs.get(region.name, []):
            if _lingo_can_satisfy_requirements(state, access_req, world, player_logic):
                counted_panels += panel_count
        if counted_panels >= world.options.level_2_requirement.value - 1:
            return True
    return False


def _lingo_can_satisfy_requirements(state: CollectionState, access: AccessRequirements, world: "LingoWorld",
                                    player_logic: LingoPlayerLogic):
    for req_room in access.rooms:
        if not state.can_reach(req_room, "Region", world.player):
            return False

    for req_door in access.doors:
        if not _lingo_can_open_door(state, req_door.room, req_door.door, world, player_logic):
            return False

    if len(access.colors) > 0 and world.options.shuffle_colors:
        for color in access.colors:
            if not state.has(color.capitalize(), world.player):
                return False

    return True


def _lingo_can_open_door(state: CollectionState, room: str, door: str, world: "LingoWorld",
                         player_logic: LingoPlayerLogic):
    """
    Determines whether a door can be opened
    """
    if door not in player_logic.item_by_door.get(room, {}):
        return _lingo_can_satisfy_requirements(state, player_logic.door_reqs[room][door], world, player_logic)

    item_name = player_logic.item_by_door[room][door]
    if item_name in PROGRESSIVE_ITEMS:
        progression = PROGRESSION_BY_ROOM[room][door]
        return state.has(item_name, world.player, progression.index)

    return state.has(item_name, world.player)


def make_location_lambda(location: PlayerLocation, world: "LingoWorld", player_logic: LingoPlayerLogic):
    if location.name == player_logic.mastery_location:
        return lambda state: lingo_can_use_mastery_location(state, world, player_logic)

    if world.options.level_2_requirement > 1\
            and (location.name == "Second Room - ANOTHER TRY" or location.name == player_logic.level_2_location):
        return lambda state: lingo_can_use_level_2_location(state, world, player_logic)

    return lambda state: lingo_can_use_location(state, location, world, player_logic)
