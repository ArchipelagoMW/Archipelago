from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from .player_logic import LingoPlayerLogic, PlayerLocation
from .static_logic import PROGRESSION_BY_ROOM, PROGRESSIVE_ITEMS, RoomAndDoor

if TYPE_CHECKING:
    from . import LingoWorld


def lingo_can_use_entrance(state: CollectionState, room: str, door: RoomAndDoor, player: int,
                           player_logic: LingoPlayerLogic):
    if door is None:
        return True

    return _lingo_can_open_door(state, room if door.room is None else door.room, door.door, player, player_logic)


def lingo_can_use_pilgrimage(state: CollectionState, player: int, player_logic: LingoPlayerLogic):
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
        if not state.has(player_logic.ITEM_BY_DOOR[entrance[0]][entrance[1]], player):
            return False

    return True


def lingo_can_use_location(state: CollectionState, location: PlayerLocation, world: "LingoWorld",
                           player_logic: LingoPlayerLogic):
    for req_room in location.access.rooms:
        if not state.can_reach(req_room, "Region", world.player):
            return False

    for req_door in location.access.doors:
        if not _lingo_can_open_door(state, req_door.room, req_door.door, world.player, player_logic):
            return False

    if len(location.access.colors) > 0 and world.options.shuffle_colors:
        for color in location.access.colors:
            if not state.has(color.capitalize(), world.player):
                return False

    return True


def lingo_can_use_mastery_location(state: CollectionState, world: "LingoWorld"):
    return state.has("Mastery Achievement", world.player, world.options.mastery_achievements.value)


def lingo_can_use_level_2_location(state: CollectionState, world: "LingoWorld"):
    return sum(location.counting_panels for location in state.locations_checked)\
        >= world.options.level_2_requirement.value


def _lingo_can_open_door(state: CollectionState, room: str, door: str, player: int, player_logic: LingoPlayerLogic):
    """
    Determines whether a door can be opened
    """
    item_name = player_logic.ITEM_BY_DOOR[room][door]
    if item_name in PROGRESSIVE_ITEMS:
        progression = PROGRESSION_BY_ROOM[room][door]
        return state.has(item_name, player, progression.index)

    return state.has(item_name, player)


def make_location_lambda(location: PlayerLocation, world: "LingoWorld", player_logic: LingoPlayerLogic):
    if location.name == player_logic.MASTERY_LOCATION:
        return lambda state: lingo_can_use_mastery_location(state, world)

    if location.name == player_logic.LEVEL_2_LOCATION:
        return lambda state: lingo_can_use_level_2_location(state, world)

    return lambda state: lingo_can_use_location(state, location, world, player_logic)
