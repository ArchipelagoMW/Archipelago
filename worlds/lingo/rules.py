from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from .options import VictoryCondition
from .player_logic import LingoPlayerLogic, PlayerLocation
from .static_logic import PANELS_BY_ROOM, PROGRESSION_BY_ROOM, PROGRESSIVE_ITEMS, RoomAndDoor

if TYPE_CHECKING:
    from . import LingoWorld


def lingo_can_use_entrance(state: CollectionState, room: str, door: RoomAndDoor, player: int,
                           player_logic: LingoPlayerLogic):
    if door is None:
        return True

    return _lingo_can_open_door(state, room, room if door.room is None else door.room, door.door, player, player_logic)


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


def lingo_can_use_location(state: CollectionState, location: PlayerLocation, room_name: str, world: "LingoWorld",
                           player_logic: LingoPlayerLogic):
    for panel in location.panels:
        panel_room = room_name if panel.room is None else panel.room
        if not _lingo_can_solve_panel(state, room_name, panel_room, panel.panel, world, player_logic):
            return False

    return True


def lingo_can_use_mastery_location(state: CollectionState, world: "LingoWorld"):
    return state.has("Mastery Achievement", world.player, world.options.mastery_achievements.value)


def _lingo_can_open_door(state: CollectionState, start_room: str, room: str, door: str, player: int,
                         player_logic: LingoPlayerLogic):
    """
    Determines whether a door can be opened
    """
    item_name = player_logic.ITEM_BY_DOOR[room][door]
    if item_name in PROGRESSIVE_ITEMS:
        progression = PROGRESSION_BY_ROOM[room][door]
        return state.has(item_name, player, progression.index)

    return state.has(item_name, player)


def _lingo_can_solve_panel(state: CollectionState, start_room: str, room: str, panel: str, world: "LingoWorld",
                           player_logic: LingoPlayerLogic):
    """
    Determines whether a panel can be solved
    """
    if start_room != room and not state.can_reach(room, "Region", world.player):
        return False

    if room == "Second Room" and panel == "ANOTHER TRY" \
            and world.options.victory_condition == VictoryCondition.option_level_2 \
            and not state.has("Counting Panel Solved", world.player, world.options.level_2_requirement.value - 1):
        return False

    panel_object = PANELS_BY_ROOM[room][panel]
    for req_room in panel_object.required_rooms:
        if not state.can_reach(req_room, "Region", world.player):
            return False

    for req_door in panel_object.required_doors:
        if not _lingo_can_open_door(state, start_room, room if req_door.room is None else req_door.room,
                                    req_door.door, world.player, player_logic):
            return False

    for req_panel in panel_object.required_panels:
        if not _lingo_can_solve_panel(state, start_room, room if req_panel.room is None else req_panel.room,
                                      req_panel.panel, world, player_logic):
            return False

    if len(panel_object.colors) > 0 and world.options.shuffle_colors:
        for color in panel_object.colors:
            if not state.has(color.capitalize(), world.player):
                return False

    return True


def make_location_lambda(location: PlayerLocation, room_name: str, world: "LingoWorld", player_logic: LingoPlayerLogic):
    if location.name == player_logic.MASTERY_LOCATION:
        return lambda state: lingo_can_use_mastery_location(state, world)

    return lambda state: lingo_can_use_location(state, location, room_name, world, player_logic)
